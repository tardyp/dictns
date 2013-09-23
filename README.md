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

see unit tests for more usage examples
