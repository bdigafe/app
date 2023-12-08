import random


class LimitedSizeList():
    """Dict with a limited length, ejecting LRUs as needed."""

    def __init__(self, *args, cache_len: int = 10, **kwargs):
        assert cache_len > 0
        self.cache_len = cache_len
        self._list = []

    def __len__(self):
        return len(self._list)
    
    def __contains__(self, key):
        for kv in self._list:
            if kv[0] == key:
                return True
        return False
    
    def __getitem__(self, key):
        kv = self._get_item(key)
        if not kv is None:
            return kv[1]
        return None
    
    def __setitem__(self, key, value):
        self._set_item(key, value)

    def __delitem__(self, key):
        item  = self._get_item(key)
        if item in self._list:
            self._list.remove(item)

    def __iter__(self): 
        return self._list.__iter__()

    def _set_item(self, key, value):
        data = self._list

        item = self._get_item(key)
        if item in data:
           data.remove(item)

        kv = (key, value)
        data.insert(0, kv)

        while len(data) > self.cache_len:
            data.remove(data[-1])

    def _get_item(self, key):
        kv = None
        for kv in self._list:
            if kv[0] == key:
                return kv
    
        return None
    
    def __repr__(self):
        # convert list of key-value pairs to dict
        return repr(dict(self._list))

    
ratings = LimitedSizeList(cache_len=10)

for k in range(1, 15, 1):
    l = random.randint(1, 100)
    ratings[l]= l
    
print(ratings)

del ratings[-1]
ratings[999] = 999

print(ratings)