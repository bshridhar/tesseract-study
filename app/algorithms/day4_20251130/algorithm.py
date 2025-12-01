"""
LeetCode 217: Contains Diplicate

Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

Example 1:
Input: nums = [1,2,2,1]
Output: true

Example 2:
Input: nums = [4,9,5]
Output: false
Constraints:
- 1 <= nums.length <= 1000
- 0 <= nums[i] <= 1000
"""
from typing import List


def contains_duplicate(nums: List[int]) -> bool:
    """
    Check if any value appears at least twice in the array.
    
    Uses a set to track seen numbers in O(n) time complexity.
    
    Args:
        nums: Array of integers
    
    Returns:
        True if any value appears at least twice, False otherwise.
    
    Time Complexity O(n)
    Space Complexity O(n)
    """
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
