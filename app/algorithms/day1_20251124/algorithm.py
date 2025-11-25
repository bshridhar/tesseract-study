from typing import List, Optional

def two_sum(nums: List[int], target: int) -> Optional[List[int]]:
  """
  Find two numbers in an array that add up to a target value.
  
  Uses a hash map to store seen numbers and their indices for O(1) lookup.
  
  Args:
      nums: List of integers to search
      target: Target sum value
  
  Returns:
      List containing indices of the two numbers, or None if no solution exists
  
  Time Complexity: O(n) where n = len(nums)
      - Single pass through the array
      - Hash map lookup is O(1) average case
  
  Space Complexity: O(n)
      - Hash map stores up to n elements in worst case
  """
  seen = {}
  for i, num in enumerate(nums):
    need = target - num
    if need in seen:
      return [seen[need], i]
    seen[num] = i
  return None
