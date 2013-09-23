import json
from copy import deepcopy, copy


class Namespace(dict):
    """
    A convenience class that makes a json like dict of (dicts,lists,strings,integers)
    looks like a python object allowing syntax sugar like mydict.key1.key2.key4 = 5
    this object also looks like a dict so that you can walk items(), keys() or values()

    input should always be json-able but this is checked only in pedentic mode, for
    obvious performance reason
    """
    __slots__ = []

    def __init__(self, d):
        dict.__init__(self, d)
        for k, v in d.items():
            # if already a Namespace, this will not match
            if type(v) in (dict, list):
                dict.__setitem__(self, k, Namespace(v))

    def __new__(cls, v):
        if type(v) == dict:
            return dict.__new__(cls, v)
        elif type(v) == list:
            return [Namespace(i) for i in v]
        else:
            return v
# pretty printing

    def __repr__(self):
        """ pretty printed __repr__, for debugging"""
        d = dict(self)
        try:
            return json.dumps(d, indent=4)
        except Exception:
            return repr(d)

# on the fly conversion
    def __setitem__(self, k, v):
        dict.__setitem__(self, k, Namespace(v))

# object like accessors
    __getattr__ = dict.__getitem__
    __setattr__ = __setitem__

    def __getstate__(self):
        return self

    def __setstate__(self, _dict):
        self.__init__(_dict)

# deepcopy
    def __deepcopy__(self, memo):
        return Namespace(deepcopy(dict(self)))

# copy
    def __copy__(self):
        return Namespace(dict(self))


def documentNamespace(n, parent=None):
    """This prints the available keys and subkeys of the data, and their types,
    meant for quick auto-documentation of big json data
    """
    s = ""
    for k, v in n.items():
        if parent:
            me = parent + "." + k
        else:
            me = k

        def do_item(me, v):
            t = type(v).__name__
            if t == "Namespace":
                t = "dict"
            s = me + " -> " + t + "\n"
            if isinstance(v, dict):
                v = Namespace(v)
                s += documentNamespace(v, me)
            elif type(v) == list:
                if len(v) > 0:
                    v = v[0]
                    s += do_item(me + "[i]", v)
            return s
        s += do_item(me, v)
    return s
