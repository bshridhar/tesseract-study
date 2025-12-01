from typing import List, Optional

def moveZeroes(nums: List[int]) -> None:
  """
  Moves all zeroes in the list to the end while maintaining the order of the non-zero elements.
  
  Args:
      nums: List of integers to be modified in place
  
  Returns:
      None
  
  Time Complexity: O(n) where n = len(nums)
      - Single pass through the list
  
  Space Complexity: O(1)
      - No additional space used
  """
  last_non_zero_index = 0
  cur_index = 0
  while cur_index < len(nums):
    # if nums[cur_index] != 0:
    #   temp = nums[cur_index]
    #   nums[cur_index] = nums[last_non_zero_index]
    #   nums[last_non_zero_index] = temp
    #   last_non_zero_index += 1
    # cur_index += 1
    if nums[cur_index] != 0:
      nums[last_non_zero_index], nums[cur_index] = nums[cur_index], nums[last_non_zero_index]
      last_non_zero_index += 1
    cur_index += 1

  return None


if __name__ == "__main__":
  # Test cases
  print("Testing Move Zeroes Algorithm\n")
  
  # Test case 1
  test1 = [0, 1, 0, 3, 12]
  print(f"Test 1 Input:  {test1}")
  moveZeroes(test1)
  print(f"Test 1 Output: {test1}")
  print(f"Expected:      [1, 3, 12, 0, 0]\n")
  
  # Test case 2
  test2 = [0]
  print(f"Test 2 Input:  {test2}")
  moveZeroes(test2)
  print(f"Test 2 Output: {test2}")
  print(f"Expected:      [0]\n")
  
  # Test case 3
  test3 = [1, 2, 3]
  print(f"Test 3 Input:  {test3}")
  moveZeroes(test3)
  print(f"Test 3 Output: {test3}")
  print(f"Expected:      [1, 2, 3]\n")
  
  # Test case 4
  test4 = [0, 0, 1]
  print(f"Test 4 Input:  {test4}")
  moveZeroes(test4)
  print(f"Test 4 Output: {test4}")
  print(f"Expected:      [1, 0, 0]\n")
