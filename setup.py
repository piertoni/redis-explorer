import os
from setuptools import setup, find_packages, find_namespace_packages


def abspath(*path):
    """A method to determine absolute path for a given relative path to the
    directory where this setup.py script is located"""
    setup_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(setup_dir, *path)


packages = find_packages(where=abspath("source"), exclude=[])

setup(
    name="redis-explorer",
    author="piertoni",
    version="0.1.0",
    package_dir={"": "source"},
    packages=find_namespace_packages(where="source"),
    entry_points={"console_scripts": ["redis-explorer = redis_explorer.main:main"]},
    install_requires=["redis"],
)
