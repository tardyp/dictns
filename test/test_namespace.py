try:
    import unittest2 as unittest
except ImportError:
    import unittest

import pickle
import json
import collections
from copy import deepcopy, copy
from dictns import compareNamespace
from dictns import documentNamespace
from dictns import filterDelta
from dictns import Namespace


class TestNamespace(unittest.TestCase):

    def test_basic(self):
        n = Namespace({'a': {'b': {'c': 1}}})

        self.assertEqual(n.a.b.c, 1)
        self.assertEqual(n['a']['b']['c'], 1)
        self.assertEqual(n['a'].b['c'], 1)
        self.assertEqual(n['a']['b'].c, 1)
        self.assertEqual(n['a'].b.c, 1)
        self.assertEqual(list(n.keys()), ['a'])
        self.assertEqual(list(n.a.b.values()), [1])
        self.assertEqual(list(n.a.b.items()), [('c', 1)])
        n.a.b.c = 2
        self.assertEqual('a' in n, True)
        self.assertEqual('b' in n, False)

        self.assertEqual(n['a']['b']['c'], 2)
        n.a.b = {'d': 3}
        self.assertEqual(n.a.b.d, 3)
        n.a.b = Namespace({'e': 4})
        self.assertEqual(n.a.b.e, 4)
        self.assertRaises(KeyError, lambda: n.a.b.d == 3)
        self.assertEqual(Namespace(1), 1)
        self.assertEqual(Namespace([1]), [1])
        self.assertEqual(Namespace("1"), "1")
        self.assertEqual(Namespace(["1"]), ["1"])

        self.assertRaises(KeyError, lambda: n["__getitem__"])
        n.a['b'] = {'f': 5}
        self.assertEqual(n.a.b.f, 5)

    def test_nonzero(self):
        n = Namespace({'a': {'b': {'c': 1}}})
        self.assertTrue(n)
        n = Namespace({})
        self.assertFalse(n)

    def test_list(self):
        n = Namespace([{'a': {'b': {
                                'c': 1}}}, {'a': {'b': {'c': 2}}}])
        self.assertEqual(n[0].a.b.c, 1)
        self.assertEqual(n[1].a.b.c, 2)
        for i in n:
            self.assertEqual(i.a.b.c, i.a.b.c)

    def test_jsondump(self):
        s = '[{"a": {"b": {"c": 1}}}, {"a": {"b": {"c": 2}}}]'
        n = Namespace(json.loads(s))
        self.assertEqual(json.dumps(n), s)

    def test_prettyprint(self):
        n = Namespace({'a': [{'b': {'c': 1}}]})
        expected = """\
{
    "a": [
        {
            "b": {
                "c": 1
            }
        }
    ]
}"""
        self.assertEqual(repr(n), expected)
        expected = """\
a -> list
a[i] -> dict
a[i].b -> dict
a[i].b.c -> int
"""
        self.assertEqual(documentNamespace(n), expected)

    def test_pickle(self):
        n = Namespace([{'a': {'b': {
                                'c': 1}}}, {'a': {'b': {'c': 2}}}])
        s = pickle.dumps(n)
        n = pickle.loads(s)
        self.assertEqual(n[0].a.b.c, 1)
        self.assertEqual(n[1].a.b.c, 2)
        for i in n:
            self.assertEqual(i.a.b.c, i.a.b.c)

    def test_deepcopy(self):
        a = Namespace(
            {'a': dict(b=[1, 2, 3])})

        b = deepcopy(a)
        self.assertEqual(a, b)
        self.assertNotEqual(id(a), id(b))
        self.assertNotEqual(id(a.a.b), id(b.a.b))

    def test_copy(self):
        a = Namespace(
            {'a': dict(b=[1, 2, 3])})

        b = copy(a)
        self.assertEqual(a, b)
        self.assertNotEqual(id(a), id(b))
        self.assertEqual(id(a.a.b), id(b.a.b))

    def testCompareNamespace(self):
        nOld = Namespace({'color': 'red',
                          'size': 5,
                          'form': 'square',
                          'owner': {'name': 'bob', 'age': 12, 'nationality': 'French'}})
        nNew = Namespace({'color': 'red',
                          'size': 8,
                          'owner': {'name': 'john', 'age': 12, 'genre': 'M'},
                          'protected': True})

        namespaceDelta = compareNamespace(nOld, nNew)
        filteredDelta = filterDelta(namespaceDelta)

        self.assertEqual(set(filteredDelta.removed.keys()), set(['form', 'owner.nationality']))
        self.assertEqual(set(filteredDelta.added.keys()), set(['protected', 'owner.genre']))
        self.assertEqual(set(filteredDelta.changed.keys()), set(['size', 'owner.name']))
        self.assertEqual(set(filteredDelta.unchanged.keys()), set(['color', 'owner.age']))

        item = filteredDelta.changed['owner.name']
        self.assertEqual(item.parent, 'owner')
        self.assertEqual(item.old, 'bob')
        self.assertEqual(item.new, 'john')

        item = filteredDelta.removed['form']
        self.assertEqual(item.parent, None)
        self.assertEqual(item.old, 'square')
        self.assertEqual(item.new, None)

    @unittest.skipUnless(
        hasattr(collections, "OrderedDict"),
        "python version does not support OrderedDict")
    def testOrderedDict(self):
        ordered = collections.OrderedDict([("a", "b"), ("c", "d")])
        nsordered = Namespace(ordered)
        self.assertEqual(nsordered.a, ordered["a"])
        self.assertEqual(nsordered.c, nsordered.values()[-1])
        ordered['e'] = 'f'
        self.assertEqual(nsordered.c, nsordered.values()[-1])
        nsordered['e'] = 'f'
        self.assertEqual(nsordered.e, nsordered.values()[-1])
        for i in xrange(1000):
            nsordered[str(i)] = i
            ordered[str(i)] = i

        # Namespace of an OrderedDict is *not* ordered
        self.assertEqual(999, ordered.values()[-1])
        self.assertNotEqual(999, nsordered.values()[-1])

        nsordered = Namespace(ordered)
        # still not ordered...
        self.assertNotEqual(999, nsordered.values()[-1])
