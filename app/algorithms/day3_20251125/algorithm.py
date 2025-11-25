"""
LeetCode 349: Intersection of Two Arrays

Given two integer arrays nums1 and nums2, return an array of their intersection.
Each element in the result must be unique and you may return the result in any order.

Example 1:
Input: nums1 = [1,2,2,1], nums2 = [2,2]
Output: [2]

Example 2:
Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
Output: [9,4] or [4,9]

Constraints:
- 1 <= nums1.length, nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 1000
"""
from typing import List


def intersection(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    Find the intersection of two arrays.
    
    Uses set intersection for O(n + m) time complexity.
    
    Args:
        nums1: First array of integers
        nums2: Second array of integers
    
    Returns:
        List of unique elements that appear in both arrays
    
    Time Complexity: O(n + m) where n = len(nums1), m = len(nums2)
    Space Complexity: O(min(n, m)) for the set storage
    """
    # Convert both arrays to sets and find intersection
    set1 = set(nums1)
    set2 = set(nums2)
    
    # Return intersection as a list
    return list(set1 & set2)
