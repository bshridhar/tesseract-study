"""Pydantic models for Intersection of Two Arrays API"""
from pydantic import BaseModel, Field, validator
from typing import List


class IntersectionRequest(BaseModel):
    """Request model for intersection endpoint"""
    nums1: List[int] = Field(..., description="First array of integers")
    nums2: List[int] = Field(..., description="Second array of integers")
    
    @validator('nums1', 'nums2')
    def validate_array_length(cls, v):
        if len(v) < 1:
            raise ValueError('Array must contain at least 1 element')
        if len(v) > 1000:
            raise ValueError('Array must not exceed 1000 elements')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "nums1": [1, 2, 2, 1],
                "nums2": [2, 2]
            }
        }


class IntersectionResponse(BaseModel):
    """Response model for intersection endpoint"""
    intersection: List[int] = Field(..., description="Array of unique elements present in both arrays")
    
    class Config:
        json_schema_extra = {
            "example": {
                "intersection": [2]
            }
        }
