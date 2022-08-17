import collections

class OrderedSet(collections.OrderedDict, collections.MutableSet):
    def add(self, elem):
        self[elem] = None
