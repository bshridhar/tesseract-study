"""FastAPI router for Intersection of Two Arrays API endpoint"""
from fastapi import APIRouter
from app.config import API_PREFIX
from . import intersection, IntersectionRequest, IntersectionResponse

router = APIRouter(
    prefix=API_PREFIX,
    tags=["Intersection of Two Arrays - Day 3"]
)


@router.post("/intersection", response_model=IntersectionResponse)
def api_intersection(payload: IntersectionRequest):
    """
    Find the intersection of two arrays.
    
    Given two integer arrays nums1 and nums2, returns an array of their intersection.
    Each element in the result is unique and the result can be in any order.
    
    **Example:**
    - Input: nums1 = [1,2,2,1], nums2 = [2,2]
    - Output: [2]
    
    **Complexity:**
    - Time: O(n + m) where n and m are the lengths of the arrays
    - Space: O(min(n, m)) for set storage
    """
    result = intersection(payload.nums1, payload.nums2)
    return {"intersection": result}
