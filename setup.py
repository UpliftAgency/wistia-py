#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

from wistia_py import __version__


tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='wistia-py',
    version=__version__,
    description='A simple requests wrapper for the Wistia API',
    long_description='''
A simple requests wrapper for the Wistia API
''',
    keywords='wistia wistia-py wistia_py wistiapy wistia-python',
    author='Paul Craciunoiu',
    author_email='paul@craciunoiu.net',
    url='https://github.com/UpliftAgency/wistia-py',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.(y+1).0' notation
        # (this way you get bugfixes but no breaking changes)
        'requests',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'wistia-py=wistia_py.cli:main',
        ],
    },
)
