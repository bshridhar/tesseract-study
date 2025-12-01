"""Pydantic models for Move Zeroes API"""
from pydantic import BaseModel, Field, validator
from typing import List

class MoveZeroesRequest(BaseModel):
    """Request model for move zeroes endpoint"""
    nums: List[int] = Field(..., description="Array of integers to be modified")

    @validator('nums')
    def validate_array_length(cls, v):
        if len(v) < 1:
            raise ValueError('Array must contain at least 1 element')
        if len(v) > 10000:
            raise ValueError('Array must not exceed 10000 elements')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "nums": [0, 1, 0, 3, 12]
            }
        }
    
class MoveZeroesResponse(BaseModel):
    """Response model for move zeroes endpoint"""
    result: List[int] = Field(..., description="Array with all zeros moved to the end")
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": [1, 3, 12, 0, 0]
            }
        }
