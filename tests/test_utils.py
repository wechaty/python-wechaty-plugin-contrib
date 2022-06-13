"""Unit test for utils"""
from wechaty_plugin_contrib.utils import get_invalid_packages


def test_invalid_package_finder():
    """test invalid package tester"""
    packages = ['invalid-packages-xxx', 'os', 'wechaty', 'wechaty-puppet', 'paddle']
    invalid_packages = get_invalid_packages(packages)
    assert 'invalid-packages-xxx' in invalid_packages
    assert 'paddle'
