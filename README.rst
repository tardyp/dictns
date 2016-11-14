######
dictns
######


 .. image:: https://travis-ci.org/tardyp/dictns.png?branch=master
     :target: https://travis-ci.org/tardyp/dictns


simple python class that merges dictionary and object APIs

Those Namespace objects work in a similar way as javascript objects.
intended to help deadling with deep json objects, and save you a lot of [''] in your code

usage
-----

.. code-block:: python

    from dictns import Namespace
    n = Namespace(dict(a=1, b=3, c=dict(d=4)))
    assert(n['a'] == n.a)
    assert(n['c']['d'] == n.c.d)

you can wrap dicts and lists inside Namespace

.. code-block:: python

    n = Namespace([dict(a=1, b=3, c=[dict(d=4)])])
    assert(n[0]['a'] == n[0].a)
    assert(n[0]['c'][0]['d'] == n[0].c[0].d)

you can also wrap dict subclasses like OrderedDict, but the resulting Namespace
does not inherit original object characteristics (i.e. order in OrderedDict)

see unit tests for more usage examples

ChangeLog:

- 1.0: Initial version

- 1.1: Added Namespace comparaison tools

- 1.2: Namespace now support dict and list subclasses as input

- 1.3:
    - Fix for compatibility with getattr() built-in method. When an invalid key is requested, it
      now raises an AttributeError instead of a KeyError.
    - Allow initialization without arg: Namespace() is equivalent to Namespace({}).

- 1.4: Allow Namespace objects to be weak referenced

- 1.5:
    - Fix tests for 3.5 and pypy
    - Readme cleanups

Developing
----------

Launch unit tests:

    python test/test_namespace.py
