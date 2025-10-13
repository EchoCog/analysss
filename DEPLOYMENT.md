# Deployment Guide

## Overview

This guide covers deploying the rzonedevops/analysis repository improvements to various environments.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Deployment Methods](#deployment-methods)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Monitoring & Health Checks](#monitoring--health-checks)
7. [Rollback Procedures](#rollback-procedures)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- Python 3.8+ (3.11 recommended)
- pip 21.0+
- Git 2.30+
- Docker 20.10+ (for containerized deployment)
- Docker Compose 2.0+ (for containerized deployment)

### Required Credentials
- Supabase URL and API Key (optional)
- Neon PostgreSQL connection string (optional)
- OpenAI API Key (optional)

### System Requirements
- **Memory:** 2GB minimum, 4GB recommended
- **Storage:** 500MB for application, additional for data
- **CPU:** 2 cores minimum

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/rzonedevops/analysis.git
cd analysis
```

### 2. Run Deployment Script

```bash
chmod +x deploy.sh
./deploy.sh development
```

The deployment script will:
- ✅ Check prerequisites
- ✅ Set up environment
- ✅ Install dependencies
- ✅ Run database migrations
- ✅ Execute tests
- ✅ Perform health checks

---

## Deployment Methods

### Method 1: Bash Script (Recommended for Development)

```bash
# Development environment
./deploy.sh development

# Staging environment
./deploy.sh staging

# Production environment
./deploy.sh production

# Dry run (preview without executing)
./deploy.sh production --dry-run

# Skip specific steps
./deploy.sh development --skip-tests --skip-deps
```

**Options:**
- `--skip-deps` - Skip dependency installation
- `--skip-db` - Skip database migrations
- `--skip-tests` - Skip test execution
- `--dry-run` - Preview deployment without executing
- `--rollback` - Rollback to previous version
- `--help` - Show help message

---

### Method 2: Docker (Recommended for Production)

#### Build and Run with Docker Compose

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env

# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f analysis

# Stop services
docker-compose down
```

#### Build Docker Image Manually

```bash
# Build image
docker build -t rzonedevops-analysis:latest .

# Run container
docker run -d \
  --name analysis \
  --env-file .env \
  -p 5000:5000 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  rzonedevops-analysis:latest
```

---

### Method 3: GitHub Actions (CI/CD)

The repository includes a GitHub Actions workflow for automated deployment.

#### Setup

1. **Configure Secrets** in GitHub repository settings:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `NEON_CONNECTION_STRING`
   - `OPENAI_API_KEY`

2. **Trigger Deployment:**

   - **Automatic:** Push to `main` or `staging` branch
   - **Manual:** Go to Actions → Deploy Analysis System → Run workflow

#### Workflow Steps

1. ✅ Run tests and linting
2. ✅ Build Docker image
3. ✅ Push to GitHub Container Registry
4. ✅ Deploy to environment
5. ✅ Run database migrations
6. ✅ Perform health checks
7. ✅ Generate deployment report

---

## Environment Configuration

### Create .env File

```bash
cp .env.example .env
```

### Required Variables

```bash
# Environment
ENVIRONMENT=production  # development, staging, production
DEBUG=False
LOG_LEVEL=INFO

# Supabase (optional)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Neon (optional)
NEON_CONNECTION_STRING=postgresql://user:pass@host/db

# OpenAI (optional)
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4
```

### Optional Variables

```bash
# Connection Pooling
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# Retry Configuration
DB_MAX_RETRIES=3
DB_RETRY_DELAY=1.0
DB_RETRY_BACKOFF=2.0

# System
ENABLE_CACHING=True
CACHE_TTL=3600
BATCH_SIZE=100
```

---

## Database Setup

### Neon PostgreSQL

#### Automatic Migration (Recommended)

```bash
python execute_neon_migrations.py
```

This will:
- Create all required tables
- Create all indexes
- Verify schema integrity

#### Manual Migration

Execute the SQL in `database_migrations.sql` in your Neon SQL Editor.

---

### Supabase

#### Manual Migration (Required)

1. Open Supabase SQL Editor
2. Copy content from `database_migrations.sql`
3. Execute the SQL

#### Verify Migration

```bash
python -c "
from src.database_sync.enhanced_client import EnhancedSupabaseClient
client = EnhancedSupabaseClient()
print('Health check:', client.health_check())
"
```

---

### Schema Validation

```bash
python -c "
from src.database_sync.schema_validator import SchemaValidator
validator = SchemaValidator()
migrations = validator.generate_all_migrations()
print(f'Generated {len(migrations)} table migrations')
"
```

---

## Monitoring & Health Checks

### Manual Health Check

```bash
python -c "
import sys
sys.path.insert(0, 'src')
from config import get_config
from database_sync.enhanced_client import EnhancedSupabaseClient, EnhancedNeonClient

config = get_config()
print('Config valid:', config.validate())

if config.database.supabase_url:
    supabase = EnhancedSupabaseClient()
    print('Supabase health:', supabase.health_check())

if config.database.neon_connection_string:
    neon = EnhancedNeonClient()
    print('Neon health:', neon.health_check())
"
```

### Docker Health Check

```bash
docker-compose ps
docker inspect --format='{{.State.Health.Status}}' rzonedevops-analysis
```

### Logs

```bash
# View application logs
tail -f logs/application.log

# Docker logs
docker-compose logs -f analysis

# Specific service logs
docker-compose logs -f redis
```

---

## Rollback Procedures

### Method 1: Using Deployment Script

```bash
./deploy.sh --rollback
```

This will revert to the previous Git commit.

### Method 2: Manual Git Rollback

```bash
# View commit history
git log --oneline -10

# Rollback to specific commit
git reset --hard <commit-hash>

# Force push (use with caution)
git push origin main --force
```

### Method 3: Docker Rollback

```bash
# Stop current containers
docker-compose down

# Pull previous image version
docker pull ghcr.io/rzonedevops/analysis:previous-tag

# Update docker-compose.yml with previous tag
# Restart services
docker-compose up -d
```

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Failed

**Symptoms:**
- Health check fails
- Connection timeout errors

**Solutions:**
```bash
# Check environment variables
echo $NEON_CONNECTION_STRING
echo $SUPABASE_URL

# Test connection manually
psql $NEON_CONNECTION_STRING -c "SELECT 1"

# Verify credentials in .env file
cat .env | grep -E "(NEON|SUPABASE)"
```

#### 2. Migration Failures

**Symptoms:**
- Table already exists errors
- Permission denied errors

**Solutions:**
```bash
# Check existing tables
python -c "
from src.database_sync.enhanced_client import EnhancedNeonClient
client = EnhancedNeonClient()
with client.session() as session:
    result = session.execute(\"\"\"
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public'
    \"\"\")
    for row in result:
        print(row[0])
"

# Drop and recreate (CAUTION: Data loss)
# Only for development environments
python -c "
from src.database_sync.enhanced_client import EnhancedNeonClient
client = EnhancedNeonClient()
with client.session() as session:
    session.execute('DROP TABLE IF EXISTS evidence CASCADE')
    # Repeat for other tables
"
```

#### 3. Dependency Installation Errors

**Symptoms:**
- pip install failures
- Module not found errors

**Solutions:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -e . -v

# Clear pip cache
pip cache purge

# Use requirements.txt as fallback
pip install -r requirements.txt
```

#### 4. Test Failures

**Symptoms:**
- pytest failures
- Import errors in tests

**Solutions:**
```bash
# Run tests with verbose output
pytest tests/ -vv

# Run specific test
pytest tests/integration/test_database_sync.py::TestEnhancedSupabaseClient -v

# Skip failing tests temporarily
pytest tests/ -v --ignore=tests/integration/
```

#### 5. Docker Build Failures

**Symptoms:**
- Build context errors
- Layer caching issues

**Solutions:**
```bash
# Clean build without cache
docker-compose build --no-cache

# Remove all containers and volumes
docker-compose down -v

# Prune Docker system
docker system prune -a
```

---

## Performance Tuning

### Database Connection Pooling

Adjust in `.env`:
```bash
DB_POOL_SIZE=20          # Increase for high concurrency
DB_MAX_OVERFLOW=40       # Allow more overflow connections
DB_POOL_TIMEOUT=60       # Increase timeout for slow queries
```

### Batch Processing

Adjust in `.env`:
```bash
BATCH_SIZE=500           # Increase for bulk operations
```

### Caching

Enable Redis caching:
```bash
ENABLE_CACHING=True
CACHE_TTL=7200           # 2 hours
```

---

## Security Best Practices

1. **Never commit .env files** to version control
2. **Use environment-specific secrets** in GitHub Actions
3. **Rotate credentials regularly**
4. **Enable audit logging** in production
5. **Use HTTPS** for all external connections
6. **Implement rate limiting** on API endpoints
7. **Regular security updates** for dependencies

---

## Support

For issues or questions:

1. Check [IMPROVEMENTS.md](IMPROVEMENTS.md) for detailed documentation
2. Review [GitHub Issues](https://github.com/rzonedevops/analysis/issues)
3. Check deployment logs in `logs/` directory
4. Review `deployment_report.txt` after deployment

---

## Changelog

### v0.5.0 (October 11, 2025)
- ✅ Added centralized configuration management
- ✅ Implemented custom exception hierarchy
- ✅ Added retry logic with exponential backoff
- ✅ Created enhanced database clients
- ✅ Implemented automated schema validation
- ✅ Added comprehensive integration tests
- ✅ Created deployment scripts and Docker support

---

**Last Updated:** October 11, 2025
**Version:** 0.5.0

