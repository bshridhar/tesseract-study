"""FastAPI router for Valid Anagram API endpoint"""
from fastapi import APIRouter
from app.config import API_PREFIX
from . import is_anagram, is_anagram_single_dict, AnagramRequest, AnagramResponse

router = APIRouter(
    prefix=API_PREFIX,
    tags=["Valid Anagram - Day 2"]
)


@router.post("/is-anagram", response_model=AnagramResponse)
def api_is_anagram(payload: AnagramRequest):
    """
    Check if two strings are anagrams.
    
    Two strings are anagrams if they contain the same characters with the same frequencies,
    just in different orders.
    
    **Example:**
    - Input: words = ["anagram", "nagaram"]
    - Output: {"is_anagram": true}
    
    **Complexity:**
    - Time: O(n) where n is the length of the strings
    - Space: O(n) for the frequency dictionaries
    """
    result = is_anagram_single_dict(payload.words)
    return {"is_anagram": result}
