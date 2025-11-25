from pydantic import BaseModel, Field
from typing import List

class AnagramRequest(BaseModel):
  words: List[str] = Field(..., min_items=2, max_items=2)

class AnagramResponse(BaseModel):
  is_anagram: bool