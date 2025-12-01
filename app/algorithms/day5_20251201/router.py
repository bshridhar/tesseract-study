"""FastAPI router for Two Sum API endpoint"""
from fastapi import APIRouter, HTTPException
from app.config import API_PREFIX
from . import two_sum, TwoSumRequest, TwoSumResponse

router = APIRouter(
    prefix=API_PREFIX,
    tags=["Two Sum - Day 1"]
)

@router.post("/two-sum", response_model=TwoSumResponse)
def api_two_sum(payload: TwoSumRequest):
    """
    Find two numbers in an array that add up to a target value.
    
    Returns the indices of the two numbers.
    """
    result = two_sum(payload.nums, payload.target)
    if result is None:
        raise HTTPException(status_code=404, detail="No two sum solution found")
    return {"indices": result}
