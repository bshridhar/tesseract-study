# Quick Testing Guide for Algorithm Files

This guide shows you how to quickly test algorithm implementations without starting the full API server.

## Running Tests Directly

Each algorithm file can be run directly to test the implementation:

```bash
# General pattern
source .venv/bin/activate
python app/algorithms/dayX_YYYYMMDD/algorithm.py

# Example for day5
python app/algorithms/day5_20251201/algorithm.py
```

## Expected Output

When you run an algorithm file, you'll see:
- Input test cases
- Actual output from your algorithm
- Expected output for comparison

Example output:
```
Testing Move Zeroes Algorithm

Test 1 Input:  [0, 1, 0, 3, 12]
Test 1 Output: [1, 3, 12, 0, 0]
Expected:      [1, 3, 12, 0, 0]
```

## Adding Test Cases to Existing Algorithms

If an algorithm file doesn't have test cases yet, add this pattern at the end:

```python
if __name__ == "__main__":
    # Test cases
    print("Testing [Algorithm Name]\n")
    
    # Test case 1
    test1 = [your, test, input]
    print(f"Test 1 Input:  {test1}")
    result1 = your_function(test1)  # or modify in place
    print(f"Test 1 Output: {result1}")
    print(f"Expected:      [expected, output]\n")
    
    # Add more test cases...
```

## Benefits

- **Fast iteration**: Test changes immediately without API overhead
- **Debugging**: Add print statements to trace execution
- **Validation**: Verify correctness before API integration
- **Learning**: See how the algorithm behaves with different inputs

## Testing via API

For integration testing, use the FastAPI server:

1. Start the server:
   ```bash
   source .venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```

2. Visit http://127.0.0.1:8000/docs

3. Test via the Swagger UI interface

## Testing via Unit Tests

For comprehensive testing, use pytest:

```bash
source .venv/bin/activate
pytest tests/algorithms/dayX_YYYYMMDD/test_algorithm.py
```

## Quick Command Reference

```bash
# Activate virtual environment (always do this first)
source .venv/bin/activate

# Test specific day's algorithm
python app/algorithms/day5_20251201/algorithm.py

# Run all unit tests
pytest

# Run tests for specific day
pytest tests/algorithms/day5_20251201/

# Start API server for manual testing
uvicorn app.main:app --reload --port 8000
