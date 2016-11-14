try:
    import unittest2 as unittest
except ImportError:
    import unittest

import collections
import json
import pickle
import weakref
from copy import copy, deepcopy
from textwrap import dedent

from dictns import Namespace, compareNamespace, documentNamespace, filterDelta


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
        self.assertRaises(AttributeError, lambda: n.a.b.d == 3)
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

    def test_emptynamespace(self):
        n = Namespace()
        self.assertFalse(n)
        self.assertEqual(n, {})

    def test_list(self):
        n = Namespace([{
            'a': {
                'b': {
                    'c': 1
                }
            }
        }, {
            'a': {
                'b': {
                    'c': 2
                }
            }
        }])
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
        expected = dedent("""\
            {
                "a": [
                    {
                        "b": {
                            "c": 1
                        }
                    }
                ]
            }""")
        self.assertEqual(repr(n), expected)
        expected = dedent("""\
            a -> list
            a[i] -> dict
            a[i].b -> dict
            a[i].b.c -> int
            """)
        self.assertEqual(documentNamespace(n), expected)

    def test_pickle(self):
        n = Namespace([{
            'a': {
                'b': {
                    'c': 1
                }
            }
        }, {
            'a': {
                'b': {
                    'c': 2
                }
            }
        }])
        s = pickle.dumps(n)
        n = pickle.loads(s)
        self.assertEqual(n[0].a.b.c, 1)
        self.assertEqual(n[1].a.b.c, 2)
        for i in n:
            self.assertEqual(i.a.b.c, i.a.b.c)

    def test_deepcopy(self):
        a = Namespace({
            'a': dict(b=[1, 2, 3])
        })
        b = deepcopy(a)
        self.assertEqual(a, b)
        self.assertNotEqual(id(a), id(b))
        self.assertNotEqual(id(a.a.b), id(b.a.b))

    def test_copy(self):
        a = Namespace({
            'a': dict(b=[1, 2, 3])
        })

        b = copy(a)
        self.assertEqual(a, b)
        self.assertNotEqual(id(a), id(b))
        self.assertEqual(id(a.a.b), id(b.a.b))

    def test_getattrcompat(self):

        class Obj:
            a = Namespace({'a': 1})

        o = Obj

        self.assertEqual(getattr(o, "a", 987), {'a': 1})
        self.assertEqual(getattr(o.a, "a", 987), 1)
        self.assertEqual(getattr(o.a, "invalid member", 987), 987)

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

    def testWeakref(self):
        n = Namespace({'a': {'b': {'c': 1}}})
        weakref.ref(n)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNamespace)
    unittest.TextTestRunner(verbosity=2).run(suite)
