"""
This solves the problem of relative imports.
Use command $ pip install -e .
Direct imports from root directory will be enabled
Courtesy : https://stackoverflow.com/a/50194143
"""

from setuptools import setup, find_packages

setup(
    name='project',
    version='1.0',
    packages=find_packages(),
    )