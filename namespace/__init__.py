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


def _appendToParent(parent, k):
    """
    Return 'parent.k' or 'k' if parent is None
    """
    if parent is not None:
        return parent + "." + k
    else:
        return k


def documentNamespace(n, parent=None):
    """
    This prints the available keys and subkeys of the data, and their types,
    meant for quick auto-documentation of big json data
    """
    s = ""
    for k, v in n.items():
        me = _appendToParent(parent, k)

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


def compareNamespace(old, new, parent=None):
    """
    Recursively go through the dict tree and record the added, removed,
    changed and unchanged keys

    @param old: old Namespace
    @type old: Namespace or dict
    @param new: new Namespace
    @type new: Namespace or dict
    @param parent: parent node in Namespace / dict tree
    @type parent: str
    @return the delta between old and new Namespaces/dicts as a Namespace with
            changed, unchanged, added and removed keys
    @rtype: Namespace(dict({'changed': <compItem>,
                            'unchanged': <compItem>,
                            'added': <compItem>,
                            'removed': <compItem>}))
            type(compItem) = dict({str: {'parent': str,
                                         'old': <type>,
                                         'new': <type>}})
    """

    compareKeys = ['changed', 'unchanged', 'added', 'removed']

    namespaceDelta = Namespace({})
    for ck in compareKeys:
        namespaceDelta[ck] = {}

    def updateDelta(currentDelta, childDelta):
        """Update current delta with child delta"""
        for ck in compareKeys:
            currentDelta[ck].update(childDelta[ck])
        return currentDelta

    def do_item():

        namespaceDelta = Namespace({})
        for ck in compareKeys:
            namespaceDelta[ck] = {}

        setNew, setOld = set(new.keys()), set(old.keys())
        intersect = setNew.intersection(setOld)

        added = setNew - intersect
        removed = setOld - intersect
        changed = set(o for o in intersect if old[o] != new[o])
        unchanged = set(o for o in intersect if old[o] == new[o])

        # process added keys
        for k in added:
            me = _appendToParent(parent, k)
            vNew = new[k]
            namespaceDelta.added[me] = {'parent': parent, 'old': None, 'new': vNew}

        # process removed keys
        for k in removed:
            me = _appendToParent(parent, k)
            vOld = old[k]
            namespaceDelta.removed[me] = {'parent': parent, 'old': vOld, 'new': None}

        # process changed keys
        for k in changed:
            me = _appendToParent(parent, k)
            vOld = old[k]
            vNew = new[k]
            if vOld != vNew:
                namespaceDelta.changed[me] = {'parent': parent, 'old': vOld, 'new': vNew}
            if isinstance(vOld, dict) and isinstance(vNew, dict):
                # compare child items Namespace
                childDelta = compareNamespace(vOld, vNew, me)
                namespaceDelta = updateDelta(namespaceDelta, childDelta)

        # process unchanged keys
        for k in unchanged:
            me = _appendToParent(parent, k)
            vOld = old[k]
            vNew = new[k]
            if vOld == vNew:
                namespaceDelta.unchanged[me] = {'parent': parent, 'old': vOld, 'new': vNew}
            if isinstance(vOld, dict) and isinstance(vNew, dict):
                # compare child items Namespace
                childDelta = compareNamespace(vOld, vNew, me)
                namespaceDelta = updateDelta(namespaceDelta, childDelta)
        return namespaceDelta

    childDelta = do_item()
    namespaceDelta = updateDelta(namespaceDelta, childDelta)
    return namespaceDelta


def filterDelta(namespaceDelta):
    """
    @param namespaceDelta: the delta between old and new Namespaces or dicts as a Namespace with
                           changed, unchanged, added and removed key
    @type namespaceDelta: see compareNamespace @rtype
    @return a new namespaceDelta with parent keys removed to limit the delta to the strict minimum
    @rtype: see compareNamespace @rtype
    """
    filteredDelta = Namespace({})
    for ck in ['changed', 'unchanged', 'added', 'removed']:
        filteredDelta[ck] = namespaceDelta[ck].copy()
        for k in namespaceDelta[ck]:
            parent = namespaceDelta[ck][k]['parent']
            if parent is not None and parent in filteredDelta[ck]:
                # remove the parent key from delta
                del filteredDelta[ck][parent]
    return filteredDelta
