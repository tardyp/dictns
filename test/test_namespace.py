import unittest
import dictns as namespace
import pickle
import json
from copy import deepcopy, copy

class Namespace(unittest.TestCase):

    def test_basic(self):
        n = namespace.Namespace({'a': {'b': {'c': 1}}})

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
        n.a.b = namespace.Namespace({'e': 4})
        self.assertEqual(n.a.b.e, 4)
        self.assertRaises(KeyError, lambda: n.a.b.d == 3)
        self.assertEqual(namespace.Namespace(1), 1)
        self.assertEqual(namespace.Namespace([1]), [1])
        self.assertEqual(namespace.Namespace("1"), "1")
        self.assertEqual(namespace.Namespace(["1"]), ["1"])

        self.assertRaises(KeyError, lambda: n["__getitem__"])
        n.a['b'] = {'f': 5}
        self.assertEqual(n.a.b.f, 5)

    def test_nonzero(self):
        n = namespace.Namespace({'a': {'b': {'c': 1}}})
        self.failUnless(n)
        n = namespace.Namespace({})
        self.failIf(n)

    def test_list(self):
        n = namespace.Namespace([{'a': {'b': {
                                'c': 1}}}, {'a': {'b': {'c': 2}}}])
        self.assertEqual(n[0].a.b.c, 1)
        self.assertEqual(n[1].a.b.c, 2)
        for i in n:
            self.assertEqual(i.a.b.c, i.a.b.c)

    def test_jsondump(self):
        s = '[{"a": {"b": {"c": 1}}}, {"a": {"b": {"c": 2}}}]'
        n = namespace.Namespace(json.loads(s))
        self.assertEqual(json.dumps(n), s)

    def test_prettyprint(self):
        n = namespace.Namespace({'a': [{'b': {'c': 1}}]})
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
        self.assertEqual(namespace.documentNamespace(n), expected)

    def test_pickle(self):
        n = namespace.Namespace([{'a': {'b': {
                                'c': 1}}}, {'a': {'b': {'c': 2}}}])
        s = pickle.dumps(n)
        n = pickle.loads(s)
        self.assertEqual(n[0].a.b.c, 1)
        self.assertEqual(n[1].a.b.c, 2)
        for i in n:
            self.assertEqual(i.a.b.c, i.a.b.c)

    def test_deepcopy(self):
        a = namespace.Namespace(
            {'a': dict(b=[1, 2, 3])})

        b = deepcopy(a)
        self.assertEqual(a, b)
        self.assertNotEqual(id(a), id(b))
        self.assertNotEqual(id(a.a.b), id(b.a.b))

    def test_copy(self):
        a = namespace.Namespace(
            {'a': dict(b=[1, 2, 3])})

        b = copy(a)
        self.assertEqual(a, b)
        self.assertNotEqual(id(a), id(b))
        self.assertEqual(id(a.a.b), id(b.a.b))
