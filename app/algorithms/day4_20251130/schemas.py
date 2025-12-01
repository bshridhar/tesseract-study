"""Pydantic models for Contains Diplicate API"""
from pydantic import BaseModel, Field, validator
from typing import List

from app.algorithms.day4_20251130.algorithm import contains_duplicate

class ContainsDuplicateRequest(BaseModel):
    """Request model for contains duplicate endpoint"""
    nums: List[int] = Field(..., description="Array of integers")

    @validator('nums')
    def validate_array_length(cls, v):
        if (len(v) < 1):
            raise ValueError('Array must contain at least 1 element')
        if (len(v) > 1000):
            raise ValueError('Array must not exceed 1000 elements')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "nums": [1, 2, 2, 1]
            }
        }
    
class ContainsDuplicateResponse(BaseModel):
    """Response model for contains duplicate endpoint"""
    contains_duplicate: bool = Field(..., description="True if any value appears at least twice, False otherwise")
    
    class Config:
        json_schema_extra = {
            "example": {
                "contains_duplicate": True
            }
        }

