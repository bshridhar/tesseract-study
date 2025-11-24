# Local Development Environment Setup Guide

This guide walks you through setting up your local development environment for the Tesseract Study project.

## ✅ Installed Tools

Your system already has:
- **Python 3.9.6** ✓
- **pip** ✓
- **Docker 28.3.3** ✓
- **docker-compose 2.40.3** ✓
- **Git** ✓
- **GitHub CLI (gh)** ✓

## 🚀 Quick Setup

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install all dependencies (dev + production)
pip install -r requirements-dev.txt

# 3. Run the FastAPI application
uvicorn app.main:app --reload --port 8000
```

## 📦 Installed Development Tools

After running `pip install -r requirements-dev.txt`, you have:

| Tool | Version | Purpose |
|------|---------|---------|
| pytest | 7.4.0 | Testing framework |
| black | 23.3.0 | Code formatter |
| flake8 | 6.0.0 | Linter for style checking |
| mypy | 1.3.0 | Static type checker |
| pytest-cov | 4.1.0 | Code coverage reports |
| ipython | 8.14.0 | Enhanced interactive Python shell |
| pre-commit | 3.3.3 | Git hooks for quality checks |

## 🛠️ Daily Development Commands

### Running the Application
```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate

# Start development server
uvicorn app.main:app --reload --port 8000

# Access the API
# - API: http://localhost:8000
# - Interactive docs: http://localhost:8000/docs
# - Alternative docs: http://localhost:8000/redoc
```

### Code Quality

```bash
# Format all code
black .

# Check code style
flake8 app/ tests/

# Type checking
mypy app/

# Run all checks together
black . && flake8 app/ tests/ && mypy app/
```

### Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_two_sum.py

# Run with coverage report
pytest --cov=app --cov-report=html

# View coverage report (opens in browser)
open htmlcov/index.html
```

### Using IPython

```bash
# Launch enhanced Python shell
ipython

# Quick testing in IPython
from app.algorithms import two_sum
two_sum([2, 7, 11, 15], 9)
```

## 🔧 Setting Up Pre-commit Hooks (Optional but Recommended)

Pre-commit hooks automatically check your code before each commit:

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually on all files
pre-commit run --all-files
```

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## 🐳 Docker Setup (When Ready for Deployment)

```bash
# Build Docker image
docker build -t tesseract-study .

# Run container
docker run -p 8000:8000 tesseract-study

# Using docker-compose (if you create docker-compose.yml)
docker-compose up -d
```

## 📝 Project Structure

```
tesseract-study/
├── .venv/                  # Virtual environment (local only)
├── app/                    # FastAPI application
│   ├── __init__.py
│   ├── main.py            # FastAPI app entry point
│   ├── algorithms.py      # Algorithm implementations
│   └── schemas.py         # Pydantic models
├── tests/                  # Test files
│   ├── __init__.py
│   └── test_two_sum.py
├── issues/                 # LeetCode problem tracking
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── README.md              # Main documentation
```

## 🔍 Troubleshooting

### Virtual environment not activated?
```bash
# You should see (.venv) in your prompt
# If not, activate it:
source .venv/bin/activate
```

### Import errors?
```bash
# Make sure you're in the project root and venv is activated
pip install -r requirements-dev.txt
```

### Port 8000 already in use?
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001

# Or find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

## 📚 Next Steps

1. ✅ Environment is set up
2. Run tests: `pytest`
3. Start the dev server: `uvicorn app.main:app --reload`
4. Visit http://localhost:8000/docs
5. Start solving LeetCode problems!

## 🎯 Recommended Workflow

1. **Before starting work:**
   ```bash
   source .venv/bin/activate
   git pull origin main
   ```

2. **While coding:**
   - Write code
   - Format: `black .`
   - Check style: `flake8 app/ tests/`
   - Run tests: `pytest`

3. **Before committing:**
   ```bash
   black .
   flake8 app/ tests/
   mypy app/
   pytest
   git add .
   git commit -m "Your message"
   ```

4. **Push and create PR:**
   ```bash
   git push origin your-branch
   gh pr create
   ```

---

**Happy Coding! 🚀**
