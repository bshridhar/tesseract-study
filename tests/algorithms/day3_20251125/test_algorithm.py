"""Unit tests for intersection algorithm"""
import pytest
from app.algorithms import day3_20251125


def test_intersection_basic():
    """Test basic intersection case"""
    result = day3_20251125.intersection([1, 2, 2, 1], [2, 2])
    assert set(result) == {2}


def test_intersection_multiple_elements():
    """Test intersection with multiple elements"""
    result = day3_20251125.intersection([4, 9, 5], [9, 4, 9, 8, 4])
    assert set(result) == {4, 9}


def test_intersection_no_common_elements():
    """Test when arrays have no common elements"""
    result = day3_20251125.intersection([1, 2, 3], [4, 5, 6])
    assert result == []


def test_intersection_all_common():
    """Test when all elements are common"""
    result = day3_20251125.intersection([1, 2, 3], [1, 2, 3])
    assert set(result) == {1, 2, 3}


def test_intersection_single_element_arrays():
    """Test with single element arrays"""
    result = day3_20251125.intersection([1], [1])
    assert result == [1]
    
    result = day3_20251125.intersection([1], [2])
    assert result == []


def test_intersection_with_duplicates():
    """Test that duplicates are removed from result"""
    result = day3_20251125.intersection([1, 1, 1, 1], [1, 1])
    assert result == [1]


def test_intersection_with_zeros():
    """Test intersection with zeros"""
    result = day3_20251125.intersection([0, 1, 2], [0, 3, 4])
    assert result == [0]


def test_intersection_negative_numbers():
    """Test intersection with negative numbers"""
    result = day3_20251125.intersection([-1, -2, 0, 1], [-2, 0, 2])
    assert set(result) == {-2, 0}


def test_intersection_large_arrays():
    """Test with larger arrays"""
    nums1 = list(range(100, 200))
    nums2 = list(range(150, 250))
    result = day3_20251125.intersection(nums1, nums2)
    expected = set(range(150, 200))
    assert set(result) == expected


def test_intersection_one_subset_of_other():
    """Test when one array is subset of another"""
    result = day3_20251125.intersection([1, 2, 3], [1, 2, 3, 4, 5])
    assert set(result) == {1, 2, 3}
