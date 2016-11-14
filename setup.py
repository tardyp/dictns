#!/usr/bin/env python
"""Installs dictns using setuptools

Run:
    python setup.py install
to install the package from the source archive.
"""

import os

from setuptools import setup

version = "1.5"

if __name__ == "__main__":
    setup(
        name="dictns",
        version=version,
        url="http://github.com/tardyp/dictns",
        download_url="http://github.com/tardyp/dictns",
        description="simple class that merge dictionary and object API",
        author="Pierre Tardy",
        author_email="tardyp@gmail.com",
        install_requires=[
        ],
        license="BSD",
        py_modules=[
            'dictns',
        ],
        classifiers=[
            """License :: OSI Approved :: BSD License""",
            """Programming Language :: Python""",
            """Topic :: Software Development :: Libraries :: Python Modules""",
            """Intended Audience :: Developers""",
        ],
        keywords='dict, object',
        long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
        platforms=['Any'],
    )
