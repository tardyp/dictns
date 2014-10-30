# dictns [![Build Status](https://travis-ci.org/tardyp/dictns.png?branch=master)](https://travis-ci.org/tardyp/dictns)

simple python class that merges dictionary and object APIs

Those Namespace objects work in a similar way as javascript objects.
intended to help deadling with deep json objects, and save you a lot of [''] in your code

usage:

    from namespace import Namespace
    n = Namespace(dict(a=1, b=3, c=dict(d=4)))
    assert(n['a'] == n.a)
    assert(n['c']['c']['d'] == n.c.d)

you can wrap dicts and lists inside Namespace

    n = Namespace([dict(a=1, b=3, c=[dict(d=4)])])
    assert(n[0]['a'] == n[0].a)
    assert(n[0]['c']['c'][0]['d'] == n[0].c[0].d)

you can also wrap dict subclasses like OrederedDict, but the resulting Namespace
does not inherit original object characteristics (i.e. order in OrderedDict)

see unit tests for more usage examples

ChangeLog:

- 1.0: initial version

- 1.1: Added Namespace comparaison tools

- 1.2: Namespace now support dict and list subclasses as input

- 1.2.1:
    - fix for compatibility with getattr() buildin method. When an invalid key is requested, it
      now raises a AttributeError instead of a KeyError.
    - allow initialization without arg: Namespace() is equivalent to Namespace({})


Developping
-----------

Launch unit tests:

    python test/test_namespace.py
