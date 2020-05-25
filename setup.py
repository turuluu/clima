# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.rst')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')

setup(
    long_description=readme,
    name='clima',
    version='0.5.5',
    description='Simple boilerplate for cli scripts',
    python_requires='>=3.6',
    project_urls={"homepage": "https://github.com/d3rp/clima.git"},
    author='Joni Turunen',
    author_email='rojun.itu@gmail.com',
    keywords='cli',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries', 'Topic :: Utilities',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X'
    ],
    packages=['clima', 'clima.fire'],
    package_dir={"": "."},
    package_data={},
    install_requires=[
        'bleach>=3.1.5', 'pytest-watch==4.*,>=4.2.0', 'six',
        'tabulate==0.*,>=0.8.7'
    ],
    extras_require={
        "dev": ["hypothesis", "mock", "pytest", "python-levenshtein", "twine"],
        "tests": ["pytest"]
    },
)
