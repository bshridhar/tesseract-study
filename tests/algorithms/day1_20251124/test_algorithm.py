"""Unit tests for two_sum algorithm"""
import pytest
from app.algorithms import day1_20251124


def test_two_sum_basic():
    """Test basic two sum case"""
    result = day1_20251124.two_sum([2, 7, 11, 15], 9)
    assert result == [0, 1]


def test_two_sum_different_order():
    """Test when solution is at different indices"""
    result = day1_20251124.two_sum([3, 2, 4], 6)
    assert result == [1, 2]


def test_two_sum_negative_numbers():
    """Test with negative numbers"""
    result = day1_20251124.two_sum([-1, -2, -3, -4, -5], -8)
    assert result == [2, 4]


def test_two_sum_no_solution():
    """Test when no solution exists"""
    result = day1_20251124.two_sum([1, 2, 3], 7)
    assert result is None


def test_two_sum_same_element_twice():
    """Test when using same element twice is needed"""
    result = day1_20251124.two_sum([3, 3], 6)
    assert result == [0, 1]


def test_two_sum_empty_array():
    """Test with empty array"""
    result = day1_20251124.two_sum([], 5)
    assert result is None


def test_two_sum_single_element():
    """Test with single element array"""
    result = day1_20251124.two_sum([5], 5)
    assert result is None


def test_two_sum_zero_target():
    """Test with zero as target"""
    result = day1_20251124.two_sum([-1, 0, 1, 2], 0)
    assert result == [0, 2]


def test_two_sum_large_numbers():
    """Test with large numbers"""
    result = day1_20251124.two_sum([1000000, 2000000, 3000000], 5000000)
    assert result == [1, 2]
