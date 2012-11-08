#!/usr/bin/env python
from setuptools import setup

requires = [
    'Flask==0.9',
    'scales==1.0.2',
    'gevent==0.13.8',
]

setup(
    name='Scales Example',
    version='0.1',
    description='Example of scales in action',
    author='Greg Reinbach',
    author_email='greg@reinbach.com',
    install_requires=requires,
)