#!/usr/bin/env python
"""Installs namespace using setuptools

Run:
    python setup.py install
to install the package from the source archive.
"""

from setuptools import setup, find_packages

version = 1.0

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
    from namespace import Namespace
    n = Namespace(dict(a=1, b=3, c=dict(d=4)))
    assert(n['a'] == n.a)
    assert(n['c']['c] == n.c.d)
""",
        'platforms': ['Any'],
    }
    ### Now the actual set up call
    setup(
        name="namespace",
        version=version,
        url="http://github.com/tardyp/namespace",
        download_url="http://github.com/tardyp/namespace",
        description="simple class that merge dictionary and object API",
        author="Pierre Tardy",
        author_email="tardyp@gmail.com",
        install_requires=[
        ],
        license="BSD",
        namespace_packages=[
            'namespace',
        ],
        packages=find_packages(),
        options={
            'sdist': {
                'force_manifest': 1,
                'formats': ['gztar', 'zip'], },
        },
        **extraArguments
    )
