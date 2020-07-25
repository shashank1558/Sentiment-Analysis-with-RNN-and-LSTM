"""
This solves the problem of relative imports.
To install use following command in setup.py directory 
    $ pip install -e .  #For virtual env other than conda 
    $ conda develop setup.py # For conda virtual env
Direct imports from root directory will be enabled

Courtesy : https://stackoverflow.com/a/50194143

"""

from setuptools import setup, find_packages

setup(
    name='sentiment_project',
    version='1.0',
    packages=find_packages(),
    )