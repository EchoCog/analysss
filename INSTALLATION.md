# Installation Guide

This guide provides detailed instructions for installing and configuring the Analysis Repository.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/rzonedevops/analysis.git
cd analysis

# Run automated setup
./scripts/setup_environment.sh

# Activate virtual environment
source venv/bin/activate

# Verify installation
pytest tests/
```

## Detailed Installation

### Prerequisites

- **Python**: 3.8 or higher
- **Git**: Latest version
- **PostgreSQL**: 12+ (optional, for local database development)
- **Node.js**: 18+ (for frontend development)

### System Requirements

- **OS**: Linux, macOS, or Windows (WSL recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB minimum

### Step-by-Step Installation

#### 1. Clone Repository

```bash
git clone https://github.com/rzonedevops/analysis.git
cd analysis
```

#### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

**Option A: Using requirements.txt (Recommended)**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Option B: Using pyproject.toml**
```bash
pip install --upgrade pip
pip install -e .
```

**Option C: With all optional dependencies**
```bash
pip install -e ".[dev,database,fraud-analysis]"
```

#### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env  # or use your preferred editor
```

**Required Configuration**:
```bash
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

**Optional Database Configuration**:
```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# Neon
NEON_CONNECTION_STRING=postgresql://user:password@host.neon.tech/database
```

**Optional AI Configuration**:
```bash
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4
```

#### 5. Initialize Database (Optional)

If using database features:

```bash
# Run migrations
python scripts/run_migrations.py

# Verify schema
python scripts/run_migrations.py --verify-only
```

#### 6. Install Pre-commit Hooks (Development)

```bash
pip install pre-commit
pre-commit install
```

#### 7. Verify Installation

```bash
# Run tests
pytest tests/ -v

# Check code quality
black --check src/
flake8 src/
```

## Frontend Setup (Optional)

If working with the React frontend:

```bash
cd analysis-frontend

# Install dependencies
npm install

# Start development server
npm start
```

## Docker Installation (Alternative)

```bash
# Build Docker image
docker build -t analysis-repo .

# Run container
docker run -p 5000:5000 -v $(pwd):/app analysis-repo
```

## Troubleshooting

### Common Issues

#### Issue: Python version too old

**Solution**:
```bash
# Install Python 3.11 (Ubuntu/Debian)
sudo apt update
sudo apt install python3.11 python3.11-venv

# Use specific Python version
python3.11 -m venv venv
```

#### Issue: pip install fails with dependency conflicts

**Solution**:
```bash
# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install with no cache
pip install --no-cache-dir -r requirements.txt
```

#### Issue: Database connection fails

**Solution**:
1. Verify credentials in `.env`
2. Check network connectivity
3. Ensure database is accessible
4. Test connection:
   ```bash
   python -c "from src.database_sync.real_time_sync import RealTimeDatabaseSync; sync = RealTimeDatabaseSync()"
   ```

#### Issue: Import errors

**Solution**:
```bash
# Install in editable mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Platform-Specific Issues

#### macOS

**Issue**: psycopg2 installation fails

**Solution**:
```bash
# Install PostgreSQL
brew install postgresql

# Install with binary
pip install psycopg2-binary
```

#### Windows

**Issue**: Scripts not executable

**Solution**:
```bash
# Use Python directly
python scripts/setup_environment.sh

# Or use WSL (recommended)
```

## Dependency Management

### Core Dependencies

- **torch**: Deep learning framework
- **transformers**: NLP models
- **networkx**: Graph analysis
- **flask**: Web API
- **pydantic**: Data validation

### Optional Dependencies

**Development**:
- black, flake8, isort (code quality)
- pytest, pytest-cov (testing)
- mypy (type checking)

**Database**:
- supabase (Supabase client)
- psycopg2-binary (PostgreSQL)
- sqlalchemy (ORM)

**Fraud Analysis**:
- scikit-learn (ML)
- xgboost (gradient boosting)
- pandas (data analysis)

## Upgrading

### Upgrade Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Upgrade all packages
pip install --upgrade -r requirements.txt

# Or upgrade specific package
pip install --upgrade torch
```

### Upgrade Database Schema

```bash
# Run latest migrations
python scripts/run_migrations.py

# Verify schema
python scripts/run_migrations.py --verify-only
```

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Remove configuration
rm .env

# Remove logs and outputs
rm -rf logs/ analysis_outputs/
```

## Next Steps

After installation:

1. **Read Documentation**: Start with [README.md](README.md)
2. **Review Architecture**: See [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)
3. **Explore Examples**: Check `docs/` directory
4. **Run Tests**: Verify everything works
5. **Start Development**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Support

- **Issues**: [GitHub Issues](https://github.com/rzonedevops/analysis/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rzonedevops/analysis/discussions)
- **Email**: devops@rzone.dev

---

**Installation successful?** Start with the [Quick Reference Guide](ANALYSIS_QUICK_REFERENCE.md)!

