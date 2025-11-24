# Projects

This directory contains example FastAPI applications and mini-projects built during the Tesseract Study program.

## Structure

```
projects/
├── README.md           # This file
└── [project-name]/     # Individual project directories
```

## Project Guidelines

Each project should be self-contained with:
- `README.md` - Project overview and setup instructions
- `requirements.txt` - Project-specific dependencies
- `app/` or `src/` - Source code
- `tests/` - Unit and integration tests
- `.env.example` - Environment variable template (if needed)

## Example Projects

### Starter Projects
- **fastapi-hello-world** - Basic FastAPI application
- **crud-api** - REST API with CRUD operations
- **auth-system** - Authentication and authorization

### Intermediate Projects
- **todo-api** - Task management API
- **blog-api** - Blog platform with posts and comments
- **user-management** - User registration and profile management

### Advanced Projects
- **microservices-demo** - Microservices architecture example
- **realtime-chat** - WebSocket-based chat application
- **file-upload-service** - File handling and storage

## Creating a New Project

```bash
# Create project directory
mkdir projects/my-project
cd projects/my-project

# Initialize project structure
mkdir -p app tests
touch README.md requirements.txt app/__init__.py tests/__init__.py

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pytest
```

## Running Projects

Each project should include run instructions in its README, typically:

```bash
cd projects/project-name
source .venv/bin/activate  # or use root .venv
uvicorn app.main:app --reload
```

## Best Practices

1. **Documentation** - Every project needs clear README
2. **Testing** - Write tests for core functionality
3. **Code Quality** - Use black, flake8, mypy
4. **Version Control** - Commit meaningful changes
5. **Dependencies** - Keep requirements.txt updated

## Learning Path

1. Start with simple CRUD operations
2. Add authentication and authorization
3. Implement database integration
4. Build real-world features
5. Explore advanced patterns
