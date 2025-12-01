from pydantic import BaseModel
from typing import List

class TwoSumRequest(BaseModel):
    nums: List[int]
    target: int

class TwoSumResponse(BaseModel):
    indices: List[int]
