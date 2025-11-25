# Test Structure

This directory mirrors the `app/` structure for easy navigation and maintenance.

## Structure

```
tests/
├── __init__.py
├── README.md                     # This file
├── test_main.py                  # API integration tests
└── algorithms/                   # Mirrors app/algorithms/
    ├── __init__.py
    └── day1_20251124/
        ├── __init__.py
        └── test_algorithm.py     # Unit tests for two_sum algorithm
```

## Test Types

### 1. Unit Tests (`tests/algorithms/dayN_DATE/test_algorithm.py`)
- Test algorithm logic directly
- Fast execution (< 1ms per test)
- No HTTP requests, no database
- Run frequently during development

**Example:**
```python
from app.algorithms import day1_20251124

def test_two_sum_basic():
    result = day1_20251124.two_sum([2, 7, 11, 15], 9)
    assert result == [0, 1]
```

### 2. API Integration Tests (`tests/test_main.py`)
- Test complete FastAPI endpoints
- Include request/response validation
- Test error handling
- Run before commits/deployments

**Example:**
```python
from fastapi.testclient import TestClient
from app.main import app

def test_two_sum_api_success():
    client = TestClient(app)
    resp = client.post("/api/two-sum", json={"nums": [2, 7], "target": 9})
    assert resp.status_code == 200
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run only unit tests
pytest tests/algorithms/

# Run only API tests
pytest tests/test_main.py

# Run specific test file
pytest tests/algorithms/day1_20251124/test_algorithm.py

# Run specific test function
pytest tests/algorithms/day1_20251124/test_algorithm.py::test_two_sum_basic

# Run with coverage report
pytest --cov=app --cov-report=html

# Run tests matching a pattern
pytest -k "two_sum"
```

## Adding Tests for New Algorithms

When you create a new algorithm module like `app/algorithms/day2_20251125/`:

1. **Create test directory:**
   ```bash
   mkdir -p tests/algorithms/day2_20251125
   touch tests/algorithms/day2_20251125/__init__.py
   ```

2. **Create unit tests** in `tests/algorithms/day2_20251125/test_algorithm.py`:
   ```python
   from app.algorithms import day2_20251125

   def test_your_algorithm():
       result = day2_20251125.your_function(param1, param2)
       assert result == expected_value
   ```

3. **Add API tests** to `tests/test_main.py`:
   ```python
   class TestYourAPI:
       def test_endpoint_success(self):
           resp = client.post("/api/your-endpoint", json={...})
           assert resp.status_code == 200
   ```

## Best Practices

1. ✅ **Descriptive Test Names**: `test_two_sum_with_negative_numbers` not `test1`
2. ✅ **Test Edge Cases**: Empty arrays, None, negative numbers, large numbers
3. ✅ **Use Docstrings**: Explain what each test verifies
4. ✅ **One Assertion Per Test**: Focus on one behavior
5. ✅ **Arrange-Act-Assert**: Clear test structure
6. ✅ **Test Error Paths**: Not just happy paths

## Coverage Goals

- **Unit Tests**: 80%+ coverage for algorithms
- **API Tests**: Cover all endpoints, status codes, validation errors

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:
- Unit tests run on every commit (fast feedback)
- Integration tests run before deployment
- Coverage reports generated automatically
