"""
utils to help plugins more stronger
"""
import re


def is_regex_pattern(pattern: str) -> bool:
    """check if the string is a valid regex pattern"""
    try:
        re.compile(pattern)
        is_valid = True
    except re.error:
        is_valid = False
    return is_valid
