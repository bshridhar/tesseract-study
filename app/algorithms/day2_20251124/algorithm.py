from .schemas import AnagramRequest, AnagramResponse

def is_anagram(words) -> bool:
    """
    Check if two strings are anagrams using frequency dictionaries.
    
    Two strings are anagrams if they contain the same characters with the same frequencies.
    
    Args:
        words: List containing exactly 2 strings to compare
    
    Returns:
        True if strings are anagrams, False otherwise
    
    Time Complexity: O(n + m) where n = len(s), m = len(t)
        - O(n) to build frequency map for first string
        - O(m) to build frequency map for second string
        - O(k) to compare dictionaries where k = number of unique chars
    
    Space Complexity: O(n + m)
        - Two separate dictionaries storing character frequencies
        - In worst case, all characters are unique
    """
    s_freq = {}
    t_freq = {}
    s, t = words[0], words[1]
    for char in s:
        s_freq[char] = s_freq.get(char, 0) + 1
    for char in t:
        t_freq[char] = t_freq.get(char, 0) + 1
    return s_freq == t_freq

def is_anagram_single_dict(words) -> bool:
    """
    Check if two strings are anagrams using a single frequency dictionary.
    
    More space-efficient implementation that uses one dictionary.
    Increments count for first string, decrements for second string.
    
    Args:
        words: List containing exactly 2 strings to compare
    
    Returns:
        True if strings are anagrams, False otherwise
    
    Time Complexity: O(n + m) where n = len(s), m = len(t)
        - O(n) to increment counts for first string
        - O(m) to decrement counts for second string
        - O(k) to check all counts are zero, where k = unique chars
    
    Space Complexity: O(k) where k = number of unique characters
        - Single dictionary with at most k unique characters
        - More space-efficient than two-dictionary approach
    """
    freq = {}
    s, t = words[0], words[1]
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    for char in t:
        freq[char] = freq.get(char, 0) - 1
    for count in freq.values():
        if count!= 0:
            return False
    return True

__all__ = ["is_anagram", "is_anagram_single_dict", "AnagramRequest", "AnagramResponse"]
