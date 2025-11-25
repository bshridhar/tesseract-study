"""API integration tests for FastAPI endpoints"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestTwoSumAPI:
    """Tests for /api/two-sum endpoint"""

    def test_two_sum_success(self):
        """Test successful two sum API call"""
        resp = client.post("/api/two-sum", json={"nums": [2, 7, 11, 15], "target": 9})
        assert resp.status_code == 200
        assert resp.json() == {"indices": [0, 1]}

    def test_two_sum_no_solution(self):
        """Test API returns 404 when no solution exists"""
        resp = client.post("/api/two-sum", json={"nums": [1, 2, 3], "target": 7})
        assert resp.status_code == 404
        assert resp.json()["detail"] == "No two sum solution found"

    def test_two_sum_invalid_input_type(self):
        """Test API validation with invalid input type"""
        resp = client.post("/api/two-sum", json={"nums": "invalid", "target": 9})
        assert resp.status_code == 422  # Validation error

    def test_two_sum_missing_nums_field(self):
        """Test API with missing nums field"""
        resp = client.post("/api/two-sum", json={"target": 9})
        assert resp.status_code == 422

    def test_two_sum_missing_target_field(self):
        """Test API with missing target field"""
        resp = client.post("/api/two-sum", json={"nums": [1, 2, 3]})
        assert resp.status_code == 422

    def test_two_sum_empty_request_body(self):
        """Test API with empty request body"""
        resp = client.post("/api/two-sum", json={})
        assert resp.status_code == 422

    def test_two_sum_with_negative_numbers(self):
        """Test API with negative numbers"""
        resp = client.post("/api/two-sum", json={"nums": [-1, -2, -3, -4], "target": -6})
        assert resp.status_code == 200
        assert resp.json() == {"indices": [1, 3]}


class TestDocumentationEndpoints:
    """Tests for documentation endpoints"""

    def test_redoc_endpoint_exists(self):
        """Test /redoc endpoint is accessible"""
        resp = client.get("/redoc")
        assert resp.status_code == 200
        assert "<!DOCTYPE html>" in resp.text
        assert "ReDoc" in resp.text

    def test_openapi_json_endpoint(self):
        """Test /openapi.json endpoint returns valid schema"""
        resp = client.get("/openapi.json")
        assert resp.status_code == 200
        data = resp.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
        assert "/api/two-sum" in data["paths"]

    def test_docs_endpoint_exists(self):
        """Test /docs (Swagger UI) endpoint is accessible"""
        resp = client.get("/docs")
        assert resp.status_code == 200


class TestAnagramAPI:
    """Tests for /api/is-anagram endpoint"""

    def test_is_anagram_success(self):
        """Test successful anagram check"""
        resp = client.post("/api/is-anagram", json={
            "words": ["anagram", "nagaram"]
        })
        assert resp.status_code == 200
        assert resp.json() == {"is_anagram": True}

    def test_is_anagram_not_anagram(self):
        """Test when strings are not anagrams"""
        resp = client.post("/api/is-anagram", json={
            "words": ["rat", "car"]
        })
        assert resp.status_code == 200
        assert resp.json() == {"is_anagram": False}

    def test_is_anagram_same_string(self):
        """Test same string twice"""
        resp = client.post("/api/is-anagram", json={
            "words": ["hello", "hello"]
        })
        assert resp.status_code == 200
        assert resp.json() == {"is_anagram": True}

    def test_is_anagram_invalid_input_type(self):
        """Test API validation with invalid input type"""
        resp = client.post("/api/is-anagram", json={
            "words": "invalid"
        })
        assert resp.status_code == 422

    def test_is_anagram_too_few_words(self):
        """Test API with only one word"""
        resp = client.post("/api/is-anagram", json={
            "words": ["only_one"]
        })
        assert resp.status_code == 422

    def test_is_anagram_too_many_words(self):
        """Test API with more than two words"""
        resp = client.post("/api/is-anagram", json={
            "words": ["one", "two", "three"]
        })
        assert resp.status_code == 422

    def test_is_anagram_missing_words_field(self):
        """Test API with missing words field"""
        resp = client.post("/api/is-anagram", json={})
        assert resp.status_code == 422


class TestIntersectionAPI:
    """Tests for /api/intersection endpoint"""

    def test_intersection_success(self):
        """Test successful intersection API call"""
        resp = client.post("/api/intersection", json={
            "nums1": [1, 2, 2, 1],
            "nums2": [2, 2]
        })
        assert resp.status_code == 200
        result = resp.json()
        assert set(result["intersection"]) == {2}

    def test_intersection_multiple_elements(self):
        """Test intersection with multiple common elements"""
        resp = client.post("/api/intersection", json={
            "nums1": [4, 9, 5],
            "nums2": [9, 4, 9, 8, 4]
        })
        assert resp.status_code == 200
        result = resp.json()
        assert set(result["intersection"]) == {4, 9}

    def test_intersection_no_common_elements(self):
        """Test when arrays have no intersection"""
        resp = client.post("/api/intersection", json={
            "nums1": [1, 2, 3],
            "nums2": [4, 5, 6]
        })
        assert resp.status_code == 200
        assert resp.json() == {"intersection": []}

    def test_intersection_invalid_input_type(self):
        """Test API validation with invalid input type"""
        resp = client.post("/api/intersection", json={
            "nums1": "invalid",
            "nums2": [1, 2]
        })
        assert resp.status_code == 422

    def test_intersection_missing_nums1(self):
        """Test API with missing nums1 field"""
        resp = client.post("/api/intersection", json={
            "nums2": [1, 2, 3]
        })
        assert resp.status_code == 422

    def test_intersection_missing_nums2(self):
        """Test API with missing nums2 field"""
        resp = client.post("/api/intersection", json={
            "nums1": [1, 2, 3]
        })
        assert resp.status_code == 422

    def test_intersection_empty_request_body(self):
        """Test API with empty request body"""
        resp = client.post("/api/intersection", json={})
        assert resp.status_code == 422


class TestStaticFiles:
    """Tests for static file serving"""

    def test_redoc_js_file_accessible(self):
        """Test that local redoc.standalone.js is accessible"""
        resp = client.get("/static/redoc.standalone.js")
        assert resp.status_code == 200
