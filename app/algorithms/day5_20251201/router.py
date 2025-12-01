"""FastAPI router for Move Zeroes API endpoint"""
from fastapi import APIRouter
from app.algorithms.day5_20251201.algorithm import moveZeroes
from app.algorithms.day5_20251201.schemas import MoveZeroesRequest, MoveZeroesResponse
from app.config import API_PREFIX

router = APIRouter(
    prefix=API_PREFIX,
    tags=["Move Zeroes - Day 5"]
)


@router.post("/move-zeroes", response_model=MoveZeroesResponse)
def api_move_zeroes(payload: MoveZeroesRequest):
    """
    Move all zeroes in an array to the end while maintaining the relative order of non-zero elements.
    
    Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.
    Note that you must do this in-place without making a copy of the array.
    
    **Example:**
    - Input: nums = [0,1,0,3,12]
    - Output: [1,3,12,0,0]
    
    **Complexity:**
    - Time: O(n) where n is the length of the array
    - Space: O(1) as we modify the array in-place
    """
    # Create a copy since we need to return the result
    nums_copy = payload.nums.copy()
    moveZeroes(nums_copy)
    return {"result": nums_copy}
