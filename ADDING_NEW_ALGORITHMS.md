# Adding New Daily Algorithms

This guide shows you how to add a new algorithm following the established pattern.

## Quick Start Template

For each new day, create a module following this structure:

```
app/algorithms/dayN_YYYYMMDD/
├── __init__.py          # Exports everything
├── algorithm.py         # Core algorithm logic
├── schemas.py           # Request/Response models
└── router.py            # FastAPI endpoint
```

## Step-by-Step Guide

### Step 1: Create Module Directory

```bash
# Example for Day 2, Nov 25, 2025
mkdir -p app/algorithms/day2_20251125
```

### Step 2: Create Algorithm File

**File: `app/algorithms/day2_20251125/algorithm.py`**

```python
"""Core algorithm implementation"""
from typing import Any

def your_algorithm_name(param1: type1, param2: type2) -> return_type:
    """
    Brief description of what the algorithm does.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        Description of return value
    """
    # Your implementation here
    result = ...
    return result
```

### Step 3: Create Schemas

**File: `app/algorithms/day2_20251125/schemas.py`**

```python
"""Pydantic models for request/response validation"""
from pydantic import BaseModel
from typing import List, Optional

class YourAlgorithmRequest(BaseModel):
    """Request model for your algorithm endpoint"""
    param1: type1
    param2: type2
    
    class Config:
        json_schema_extra = {
            "example": {
                "param1": "example_value",
                "param2": "example_value"
            }
        }

class YourAlgorithmResponse(BaseModel):
    """Response model for your algorithm endpoint"""
    result: return_type
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "example_result"
            }
        }
```

### Step 4: Create Router

**File: `app/algorithms/day2_20251125/router.py`**

```python
"""FastAPI router for your algorithm endpoint"""
from fastapi import APIRouter, HTTPException
from app.config import API_PREFIX
from . import your_algorithm_name, YourAlgorithmRequest, YourAlgorithmResponse

router = APIRouter(
    prefix=API_PREFIX,  # Uses centralized config
    tags=["Your Algorithm - Day N"]
)

@router.post("/your-endpoint", response_model=YourAlgorithmResponse)
def api_your_algorithm(payload: YourAlgorithmRequest):
    """
    Brief description of what this endpoint does.
    
    Additional details about usage, edge cases, etc.
    """
    result = your_algorithm_name(payload.param1, payload.param2)
    
    # Handle error cases if needed
    if result is None:
        raise HTTPException(status_code=404, detail="Error message")
    
    return {"result": result}
```

### Step 5: Create __init__.py

**File: `app/algorithms/day2_20251125/__init__.py`**

```python
from .algorithm import your_algorithm_name
from .schemas import YourAlgorithmRequest, YourAlgorithmResponse
from .router import router

__all__ = ["your_algorithm_name", "YourAlgorithmRequest", "YourAlgorithmResponse", "router"]
```

### Step 6: Register Router in main.py

**Edit: `app/main.py`**

```python
# Add import at top
from app.algorithms.day2_20251125 import router as day2_router

# Add after other router includes
app.include_router(day2_router)
```

### Step 7: Create Tests

#### Unit Tests

**File: `tests/algorithms/day2_20251125/test_algorithm.py`**

```bash
# Create test directory
mkdir -p tests/algorithms/day2_20251125
touch tests/algorithms/day2_20251125/__init__.py
```

```python
"""Unit tests for your algorithm"""
import pytest
from app.algorithms import day2_20251125

def test_basic_case():
    """Test basic functionality"""
    result = day2_20251125.your_algorithm_name(param1, param2)
    assert result == expected_value

def test_edge_case_1():
    """Test edge case description"""
    result = day2_20251125.your_algorithm_name(edge_param1, edge_param2)
    assert result == expected_edge_result

def test_no_solution():
    """Test when no solution exists"""
    result = day2_20251125.your_algorithm_name(bad_param1, bad_param2)
    assert result is None  # or whatever error condition

# Add more edge case tests...
```

#### API Integration Tests

**Add to: `tests/test_main.py`**

```python
class TestYourAlgorithmAPI:
    """Tests for /api/your-endpoint"""

    def test_success(self):
        """Test successful API call"""
        resp = client.post("/api/your-endpoint", json={
            "param1": "value1",
            "param2": "value2"
        })
        assert resp.status_code == 200
        assert resp.json() == {"result": "expected"}

    def test_validation_error(self):
        """Test invalid input"""
        resp = client.post("/api/your-endpoint", json={
            "param1": "invalid"
        })
        assert resp.status_code == 422
```

## Complete Example: Valid Anagram (Day 2)

### algorithm.py
```python
def is_anagram(s: str, t: str) -> bool:
    """Check if two strings are anagrams"""
    if len(s) != len(t):
        return False
    return sorted(s) == sorted(t)
```

### schemas.py
```python
from pydantic import BaseModel

class AnagramRequest(BaseModel):
    s: str
    t: str

class AnagramResponse(BaseModel):
    is_anagram: bool
```

### router.py
```python
from fastapi import APIRouter
from app.config import API_PREFIX
from . import is_anagram, AnagramRequest, AnagramResponse

router = APIRouter(prefix=API_PREFIX, tags=["Valid Anagram - Day 2"])

@router.post("/is-anagram", response_model=AnagramResponse)
def api_is_anagram(payload: AnagramRequest):
    """Check if two strings are anagrams"""
    result = is_anagram(payload.s, payload.t)
    return {"is_anagram": result}
```

### __init__.py
```python
from .algorithm import is_anagram
from .schemas import AnagramRequest, AnagramResponse
from .router import router

__all__ = ["is_anagram", "AnagramRequest", "AnagramResponse", "router"]
```

### main.py (add these lines)
```python
from app.algorithms.day2_20251125 import router as day2_router
app.include_router(day2_router)
```

## Running & Testing

```bash
# Run the server
uvicorn app.main:app --reload

# Test the endpoint
curl -X POST http://localhost:8000/api/is-anagram \
  -H "Content-Type: application/json" \
  -d '{"s": "anagram", "t": "nagaram"}'

# Run tests
pytest tests/algorithms/day2_20251125/
pytest tests/test_main.py::TestAnagramAPI
```

## Best Practices

1. ✅ **Descriptive Names**: Use clear function and endpoint names
2. ✅ **Type Hints**: Always include type hints for better IDE support
3. ✅ **Docstrings**: Document what each function does
4. ✅ **Error Handling**: Handle edge cases gracefully
5. ✅ **Examples**: Include example requests/responses in schemas
6. ✅ **Test Coverage**: Write unit tests for algorithm, API tests for endpoints
7. ✅ **Consistent Naming**: Follow the dayN_YYYYMMDD pattern
8. ✅ **One Algorithm Per Day**: Keep each day's work self-contained

## Checklist for New Algorithm

- [ ] Create `app/algorithms/dayN_YYYYMMDD/` directory
- [ ] Implement algorithm in `algorithm.py`
- [ ] Define schemas in `schemas.py`
- [ ] Create router in `router.py`
- [ ] Create `__init__.py` with exports
- [ ] Register router in `app/main.py`
- [ ] Create test directory `tests/algorithms/dayN_YYYYMMDD/`
- [ ] Write unit tests in `test_algorithm.py`
- [ ] Add API tests to `tests/test_main.py`
- [ ] Test locally with `uvicorn` and `pytest`
- [ ] Verify in Redoc documentation at `/redoc`
- [ ] Commit changes to git

## Tips

- Copy an existing day's structure as a starting point
- Use descriptive endpoint paths (e.g., `/api/is-anagram` not `/api/check`)
- Keep algorithms focused - one problem per day
- Test edge cases: empty inputs, invalid inputs, boundary conditions
- Use Swagger UI (`/docs`) or Redoc (`/redoc`) to test endpoints interactively
