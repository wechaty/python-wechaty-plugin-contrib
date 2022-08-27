"""
utils to help plugins more stronger
"""
import re
from typing import List
import importlib


def is_regex_pattern(pattern: str) -> bool:
    """check if the string is a valid regex pattern"""
    try:
        re.compile(pattern)
        is_valid = True
    except re.error:
        is_valid = False
    return is_valid


def get_invalid_packages(packages: List[str]) -> List[str]:
    """get invalid packages

    Args:
        packages (List[str]): source package list

    Returns:
        List[str]: invalid package list
    """
    
    invalid_packages = []
    for package in packages:
        try:
            importlib.import_module(package)
        except:
            invalid_packages.append(package)
    return invalid_packages