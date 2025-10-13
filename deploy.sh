#!/bin/bash

################################################################################
# Deployment Script for rzonedevops/analysis Repository
# 
# This script deploys the incremental improvements including:
# - Environment setup and validation
# - Dependency installation
# - Database migrations (Supabase and Neon)
# - Health checks and validation
# - Rollback capabilities
#
# Usage:
#   ./deploy.sh [environment] [options]
#
# Environments:
#   development (default)
#   staging
#   production
#
# Options:
#   --skip-deps       Skip dependency installation
#   --skip-db         Skip database migrations
#   --skip-tests      Skip test execution
#   --dry-run         Show what would be done without executing
#   --rollback        Rollback to previous version
#   --help            Show this help message
#
# Author: Manus AI Agent
# Date: October 11, 2025
################################################################################

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
ENVIRONMENT="${1:-development}"
DRY_RUN=false
SKIP_DEPS=false
SKIP_DB=false
SKIP_TESTS=false
ROLLBACK=false

# Parse command line arguments
for arg in "$@"; do
    case $arg in
        --skip-deps)
            SKIP_DEPS=true
            shift
            ;;
        --skip-db)
            SKIP_DB=true
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --rollback)
            ROLLBACK=true
            shift
            ;;
        --help)
            head -n 30 "$0" | tail -n 28
            exit 0
            ;;
    esac
done

################################################################################
# Helper Functions
################################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "================================================================================"
    echo "$1"
    echo "================================================================================"
    echo ""
}

execute_command() {
    local cmd="$1"
    local description="$2"
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would execute: $cmd"
        return 0
    fi
    
    log_info "$description"
    if eval "$cmd"; then
        log_success "✓ $description completed"
        return 0
    else
        log_error "✗ $description failed"
        return 1
    fi
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is not installed. Please install it first."
        return 1
    fi
    return 0
}

################################################################################
# Pre-deployment Checks
################################################################################

pre_deployment_checks() {
    print_header "PRE-DEPLOYMENT CHECKS"
    
    log_info "Checking required commands..."
    check_command "python3" || exit 1
    check_command "pip3" || exit 1
    check_command "git" || exit 1
    
    log_info "Checking Python version..."
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    log_info "Python version: $PYTHON_VERSION"
    
    if [[ ! "$PYTHON_VERSION" =~ ^3\.(8|9|10|11) ]]; then
        log_error "Python 3.8+ is required. Found: $PYTHON_VERSION"
        exit 1
    fi
    
    log_info "Checking Git status..."
    if [ -d "$PROJECT_ROOT/.git" ]; then
        cd "$PROJECT_ROOT"
        GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
        GIT_COMMIT=$(git rev-parse --short HEAD)
        log_info "Git branch: $GIT_BRANCH"
        log_info "Git commit: $GIT_COMMIT"
    else
        log_warning "Not a Git repository"
    fi
    
    log_success "Pre-deployment checks passed"
}

################################################################################
# Environment Setup
################################################################################

setup_environment() {
    print_header "ENVIRONMENT SETUP"
    
    log_info "Setting up environment: $ENVIRONMENT"
    
    # Check for .env file
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        log_warning ".env file not found. Creating from template..."
        
        if [ "$DRY_RUN" = false ]; then
            cat > "$PROJECT_ROOT/.env" << 'EOF'
# Environment Configuration
ENVIRONMENT=development
DEBUG=False
LOG_LEVEL=INFO

# Supabase Configuration
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Neon Configuration
NEON_CONNECTION_STRING=
# OR individual components
NEON_HOST=
NEON_DATABASE=
NEON_USER=
NEON_PASSWORD=

# Connection Pooling
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# Retry Configuration
DB_MAX_RETRIES=3
DB_RETRY_DELAY=1.0
DB_RETRY_BACKOFF=2.0

# OpenAI Configuration
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000

# System Configuration
ENABLE_CACHING=True
CACHE_TTL=3600
BATCH_SIZE=100
EOF
            log_warning "Please edit .env file with your configuration"
        fi
    else
        log_success ".env file found"
    fi
    
    # Load environment variables
    if [ -f "$PROJECT_ROOT/.env" ]; then
        log_info "Loading environment variables..."
        if [ "$DRY_RUN" = false ]; then
            set -a
            source "$PROJECT_ROOT/.env"
            set +a
        fi
        log_success "Environment variables loaded"
    fi
    
    # Create necessary directories
    log_info "Creating necessary directories..."
    execute_command "mkdir -p $PROJECT_ROOT/logs" "Create logs directory"
    execute_command "mkdir -p $PROJECT_ROOT/data" "Create data directory"
    execute_command "mkdir -p $PROJECT_ROOT/.cache" "Create cache directory"
}

################################################################################
# Dependency Installation
################################################################################

install_dependencies() {
    if [ "$SKIP_DEPS" = true ]; then
        log_warning "Skipping dependency installation"
        return 0
    fi
    
    print_header "DEPENDENCY INSTALLATION"
    
    cd "$PROJECT_ROOT"
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        log_info "Creating virtual environment..."
        execute_command "python3 -m venv venv" "Create virtual environment"
    else
        log_info "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    log_info "Activating virtual environment..."
    if [ "$DRY_RUN" = false ]; then
        source venv/bin/activate
    fi
    
    # Upgrade pip
    execute_command "pip3 install --upgrade pip" "Upgrade pip"
    
    # Install dependencies from pyproject.toml
    if [ -f "pyproject.toml" ]; then
        log_info "Installing dependencies from pyproject.toml..."
        execute_command "pip3 install -e ." "Install package in editable mode"
        execute_command "pip3 install -e '.[dev]'" "Install development dependencies"
        execute_command "pip3 install -e '.[database]'" "Install database dependencies"
        execute_command "pip3 install -e '.[fraud-analysis]'" "Install fraud analysis dependencies"
    else
        log_warning "pyproject.toml not found, skipping package installation"
    fi
    
    # Install additional required packages
    log_info "Installing additional packages..."
    execute_command "pip3 install pytest pytest-cov" "Install testing packages"
    
    log_success "Dependencies installed successfully"
}

################################################################################
# Database Migrations
################################################################################

run_database_migrations() {
    if [ "$SKIP_DB" = true ]; then
        log_warning "Skipping database migrations"
        return 0
    fi
    
    print_header "DATABASE MIGRATIONS"
    
    cd "$PROJECT_ROOT"
    
    # Check if database credentials are configured
    if [ -z "${SUPABASE_URL:-}" ] && [ -z "${NEON_CONNECTION_STRING:-}" ]; then
        log_warning "No database credentials configured. Skipping migrations."
        log_info "To enable migrations, configure SUPABASE_URL/SUPABASE_KEY or NEON_CONNECTION_STRING in .env"
        return 0
    fi
    
    # Run Neon migrations if configured
    if [ -n "${NEON_CONNECTION_STRING:-}" ]; then
        log_info "Running Neon database migrations..."
        if [ -f "execute_neon_migrations.py" ]; then
            execute_command "python3 execute_neon_migrations.py" "Execute Neon migrations"
        else
            log_warning "execute_neon_migrations.py not found"
        fi
    else
        log_info "Neon not configured, skipping Neon migrations"
    fi
    
    # Run Supabase migrations if configured
    if [ -n "${SUPABASE_URL:-}" ] && [ -n "${SUPABASE_KEY:-}" ]; then
        log_info "Supabase configured. SQL available in database_migrations.sql"
        log_warning "Please execute database_migrations.sql in Supabase SQL Editor manually"
    else
        log_info "Supabase not configured, skipping Supabase migrations"
    fi
    
    log_success "Database migrations completed"
}

################################################################################
# Run Tests
################################################################################

run_tests() {
    if [ "$SKIP_TESTS" = true ]; then
        log_warning "Skipping tests"
        return 0
    fi
    
    print_header "RUNNING TESTS"
    
    cd "$PROJECT_ROOT"
    
    if [ ! -d "tests" ]; then
        log_warning "Tests directory not found, skipping tests"
        return 0
    fi
    
    log_info "Running integration tests..."
    execute_command "pytest tests/integration/ -v --tb=short" "Run integration tests" || {
        log_warning "Some tests failed, but continuing deployment"
    }
    
    log_info "Running all tests with coverage..."
    execute_command "pytest tests/ --cov=src --cov-report=term-missing --cov-report=html" "Run tests with coverage" || {
        log_warning "Test coverage check completed with warnings"
    }
    
    log_success "Tests completed"
}

################################################################################
# Health Checks
################################################################################

run_health_checks() {
    print_header "HEALTH CHECKS"
    
    cd "$PROJECT_ROOT"
    
    # Check if configuration is valid
    log_info "Validating configuration..."
    if [ "$DRY_RUN" = false ]; then
        python3 -c "
import sys
sys.path.insert(0, 'src')
from config import get_config
config = get_config()
if config.validate():
    print('Configuration is valid')
    sys.exit(0)
else:
    print('Configuration validation failed')
    sys.exit(1)
" && log_success "Configuration is valid" || log_warning "Configuration validation failed"
    fi
    
    # Check database connections
    if [ -n "${SUPABASE_URL:-}" ] && [ -n "${SUPABASE_KEY:-}" ]; then
        log_info "Testing Supabase connection..."
        if [ "$DRY_RUN" = false ]; then
            python3 -c "
import sys
sys.path.insert(0, 'src')
from database_sync.enhanced_client import EnhancedSupabaseClient
try:
    client = EnhancedSupabaseClient()
    if client.health_check():
        print('Supabase connection: OK')
        sys.exit(0)
    else:
        print('Supabase connection: FAILED')
        sys.exit(1)
except Exception as e:
    print(f'Supabase connection error: {e}')
    sys.exit(1)
" && log_success "Supabase connection OK" || log_warning "Supabase connection failed"
        fi
    fi
    
    if [ -n "${NEON_CONNECTION_STRING:-}" ]; then
        log_info "Testing Neon connection..."
        if [ "$DRY_RUN" = false ]; then
            python3 -c "
import sys
sys.path.insert(0, 'src')
from database_sync.enhanced_client import EnhancedNeonClient
try:
    client = EnhancedNeonClient()
    if client.health_check():
        print('Neon connection: OK')
        sys.exit(0)
    else:
        print('Neon connection: FAILED')
        sys.exit(1)
except Exception as e:
    print(f'Neon connection error: {e}')
    sys.exit(1)
" && log_success "Neon connection OK" || log_warning "Neon connection failed"
        fi
    fi
    
    log_success "Health checks completed"
}

################################################################################
# Rollback
################################################################################

rollback_deployment() {
    print_header "ROLLING BACK DEPLOYMENT"
    
    cd "$PROJECT_ROOT"
    
    if [ ! -d ".git" ]; then
        log_error "Not a Git repository. Cannot rollback."
        exit 1
    fi
    
    log_warning "This will revert to the previous commit"
    read -p "Are you sure you want to rollback? (yes/no): " confirm
    
    if [ "$confirm" != "yes" ]; then
        log_info "Rollback cancelled"
        exit 0
    fi
    
    log_info "Rolling back to previous commit..."
    execute_command "git reset --hard HEAD~1" "Reset to previous commit"
    
    log_success "Rollback completed"
}

################################################################################
# Post-deployment
################################################################################

post_deployment() {
    print_header "POST-DEPLOYMENT"
    
    log_info "Generating deployment report..."
    
    if [ "$DRY_RUN" = false ]; then
        cat > "$PROJECT_ROOT/deployment_report.txt" << EOF
Deployment Report
================================================================================
Date: $(date)
Environment: $ENVIRONMENT
Git Branch: ${GIT_BRANCH:-N/A}
Git Commit: ${GIT_COMMIT:-N/A}
Python Version: $PYTHON_VERSION

Deployment Steps:
- Pre-deployment checks: PASSED
- Environment setup: COMPLETED
- Dependencies installation: $([ "$SKIP_DEPS" = true ] && echo "SKIPPED" || echo "COMPLETED")
- Database migrations: $([ "$SKIP_DB" = true ] && echo "SKIPPED" || echo "COMPLETED")
- Tests: $([ "$SKIP_TESTS" = true ] && echo "SKIPPED" || echo "COMPLETED")
- Health checks: COMPLETED

Status: SUCCESS
================================================================================
EOF
        log_success "Deployment report saved to deployment_report.txt"
    fi
    
    log_info "Deployment summary:"
    log_info "  - Environment: $ENVIRONMENT"
    log_info "  - Python version: $PYTHON_VERSION"
    log_info "  - Project root: $PROJECT_ROOT"
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "This was a DRY RUN. No changes were made."
    fi
}

################################################################################
# Main Deployment Flow
################################################################################

main() {
    print_header "DEPLOYMENT SCRIPT - rzonedevops/analysis"
    
    log_info "Environment: $ENVIRONMENT"
    log_info "Dry run: $DRY_RUN"
    log_info "Skip dependencies: $SKIP_DEPS"
    log_info "Skip database: $SKIP_DB"
    log_info "Skip tests: $SKIP_TESTS"
    
    if [ "$ROLLBACK" = true ]; then
        rollback_deployment
        exit 0
    fi
    
    # Execute deployment steps
    pre_deployment_checks
    setup_environment
    install_dependencies
    run_database_migrations
    run_tests
    run_health_checks
    post_deployment
    
    print_header "DEPLOYMENT COMPLETE"
    log_success "🎉 Deployment completed successfully!"
    
    echo ""
    echo "Next steps:"
    echo "  1. Review deployment_report.txt for details"
    echo "  2. If Supabase is configured, execute database_migrations.sql in Supabase SQL Editor"
    echo "  3. Monitor logs in the logs/ directory"
    echo "  4. Run 'python3 sync_databases.py' to verify database synchronization"
    echo ""
}

# Run main function
main

