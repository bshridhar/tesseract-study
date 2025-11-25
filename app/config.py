"""Application configuration and constants"""

# API Configuration
API_PREFIX = "/api"
API_VERSION = "v1"

# Application Metadata
APP_TITLE = "Algorithm Practice API"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = """
Daily algorithm practice with FastAPI.

## Features
- **Algorithm Solutions**: RESTful API for various algorithm problems
- **Documentation**: Interactive API docs with Swagger UI and ReDoc
- **Testing**: Comprehensive unit and integration tests

## Usage
All endpoints are prefixed with `/api`.
"""

# Documentation URLs
DOCS_URL = "/docs"
REDOC_URL = None  # Custom redoc endpoint
OPENAPI_URL = "/openapi.json"

# CORS Configuration (if needed in future)
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]
