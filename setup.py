#!/usr/bin/env python
"""Installs dictns using setuptools

Run:
    python setup.py install
to install the package from the source archive.
"""

from setuptools import setup

version = 1.2

if __name__ == "__main__":
    extraArguments = {
        'classifiers': [
            """License :: OSI Approved :: BSD License""",
            """Programming Language :: Python""",
            """Topic :: Software Development :: Libraries :: Python Modules""",
            """Intended Audience :: Developers""",
        ],
        'keywords': 'dict, object',
        'long_description': """simple class that merges dictionary and object API

This Namespace objects work in a similar way as javascript objects.
usage:
    from dictns import Namespace
    n = Namespace(dict(a=1, b=3, c=dict(d=4)))
    assert(n['a'] == n.a)
    assert(n['c']['c] == n.c.d)
""",
        'platforms': ['Any'],
    }
    # Now the actual set up call
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
        **extraArguments
    )
