"""Unit tests for is_anagram algorithm"""
import pytest
from app.algorithms import day2_20251124


def test_is_anagram_basic():
    """Test basic anagram case"""
    result = day2_20251124.is_anagram(["anagram", "nagaram"])
    assert result is True


def test_is_anagram_not_anagram():
    """Test strings that are not anagrams"""
    result = day2_20251124.is_anagram(["rat", "car"])
    assert result is False


def test_is_anagram_same_string():
    """Test same string twice"""
    result = day2_20251124.is_anagram(["hello", "hello"])
    assert result is True


def test_is_anagram_empty_strings():
    """Test empty strings"""
    result = day2_20251124.is_anagram(["", ""])
    assert result is True


def test_is_anagram_different_lengths():
    """Test strings with different lengths"""
    result = day2_20251124.is_anagram(["abc", "abcd"])
    assert result is False


def test_is_anagram_case_sensitive():
    """Test that comparison is case sensitive"""
    result = day2_20251124.is_anagram(["Anagram", "nagaram"])
    assert result is False


def test_is_anagram_with_spaces():
    """Test anagrams with spaces - spaces are counted as characters"""
    result = day2_20251124.is_anagram(["a gentleman", "elegant man"])
    assert result is True  # "a gentleman" and "elegant man" ARE anagrams (same chars including space)
    
    # Test case where spaces make them NOT anagrams
    result = day2_20251124.is_anagram(["hello world", "worldhello"])
    assert result is False  # Different number of spaces


def test_is_anagram_single_character():
    """Test single character strings"""
    result = day2_20251124.is_anagram(["a", "a"])
    assert result is True
    
    result = day2_20251124.is_anagram(["a", "b"])
    assert result is False


def test_is_anagram_repeated_characters():
    """Test with repeated characters"""
    result = day2_20251124.is_anagram(["aab", "baa"])
    assert result is True
    
    result = day2_20251124.is_anagram(["aab", "bba"])
    assert result is False


def test_is_anagram_unicode():
    """Test with unicode characters"""
    result = day2_20251124.is_anagram(["café", "éfac"])
    assert result is True
