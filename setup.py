import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="taskwarrior-scripts",
    version="0.0.3",
    author="Drew Stinnett",
    author_email="drew.stinnett@duke.edu",
    description=("Misc. taskwarrior helper scripts"),
    license="BSD",
    keywords="taskwarrior",
    packages=find_packages(),
    scripts=[
        'scripts/taskw-boss-day.py',
        'scripts/taskw-module-promotion.py'
    ],
    long_description=read('README.md'),
)
