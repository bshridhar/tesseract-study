"""FastAPI router for Intersection of Two Arrays API endpoint"""
from fastapi import APIRouter
from app.algorithms.day4_20251130.algorithm import contains_duplicate
from app.algorithms.day4_20251130.schemas import ContainsDuplicateRequest, ContainsDuplicateResponse
from app.config import API_PREFIX

router = APIRouter(
    prefix=API_PREFIX,
    tags=["Contains Duplicates - Day 4"]
)


@router.post("/contains-duplicate", response_model=ContainsDuplicateResponse)
def api_contains_duplicate(payload: ContainsDuplicateRequest):
    """
    Check if the array contains any duplicates.
    
    Given an integer array nums, return true if any value appears at least twice in the array and return false if every element is distinct.
    
    **Example:**
    - Input: nums = [1,2,2,1]
    - Output: True
    
    **Complexity:**
    - Time: O(n) where n is the length of the array
    - Space: O(n) for set storage
    """
    result = contains_duplicate(payload.nums)
    return {"contains_duplicate": result}