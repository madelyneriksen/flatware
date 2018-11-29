"""
Setup file for flatware
"""


import os
from setuptools import setup


def read(filename):
    """Read a filename as a string"""
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="flatware",
    version="0.1.0",
    author="Madelyn Eriksen",
    author_email="madelyn.eriksen@gmail.com",
    description="Create and use single file templates.",
    url="https://github.com/madelyneriksen/flatware",
    packages=['flatware'],
    install_requires=['jinja2'],
    long_description=read('README.md'),
    entry_points={
        'console_scripts': [
            'flatware = flatware.cli:main',
        ],
    }
)
