"""get the version from VERSION file"""
import os


def _get_version():
    file_path = os.path.join('../../', 'VERSION')
    if not os.path.exists(file_path):
        return '0.0.0'
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip('\n')


version = _get_version()
