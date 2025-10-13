#!/bin/bash
# Environment Setup Script for rzonedevops/analysis
# This script automates the setup of the development environment

set -e  # Exit on error

echo "=========================================="
echo "  Analysis Repository Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "ℹ $1"
}

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.8"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_success "Python $PYTHON_VERSION detected"
else
    print_error "Python 3.8 or higher required. Found: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
echo ""
echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# Install dependencies
echo ""
echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Core dependencies installed"
else
    print_warning "requirements.txt not found, installing from pyproject.toml"
    pip install -e .
fi

# Install development dependencies
echo ""
read -p "Install development dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install -e ".[dev]"
    print_success "Development dependencies installed"
fi

# Install database dependencies
echo ""
read -p "Install database dependencies (Supabase/Neon)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install -e ".[database]"
    print_success "Database dependencies installed"
fi

# Install fraud analysis dependencies
echo ""
read -p "Install fraud analysis dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install -e ".[fraud-analysis]"
    print_success "Fraud analysis dependencies installed"
fi

# Setup .env file
echo ""
echo "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_success ".env file created from template"
    print_warning "Please edit .env file with your configuration"
else
    print_warning ".env file already exists"
fi

# Install pre-commit hooks
echo ""
read -p "Install pre-commit hooks? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v pre-commit &> /dev/null; then
        pre-commit install
        print_success "Pre-commit hooks installed"
    else
        print_warning "pre-commit not found. Install with: pip install pre-commit"
    fi
fi

# Create necessary directories
echo ""
echo "Creating directory structure..."
mkdir -p logs
mkdir -p analysis_outputs
mkdir -p hypergraph_visualizations
print_success "Directory structure created"

# Run initial tests
echo ""
read -p "Run tests to verify installation? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v pytest &> /dev/null; then
        pytest tests/ -v --maxfail=3 || print_warning "Some tests failed"
    else
        print_warning "pytest not installed. Install dev dependencies to run tests."
    fi
fi

# Display next steps
echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
print_info "Next steps:"
echo "  1. Edit .env file with your configuration"
echo "  2. Activate virtual environment: source venv/bin/activate"
echo "  3. Run migrations: python scripts/run_migrations.py"
echo "  4. Start development!"
echo ""
print_info "Useful commands:"
echo "  - Run tests: pytest tests/"
echo "  - Format code: black src/ tests/"
echo "  - Check code: flake8 src/ tests/"
echo "  - Run migrations: python scripts/run_migrations.py"
echo ""
print_success "Happy coding! 🚀"

