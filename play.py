class LimitedSizeList():
    """Dict with a limited length, ejecting LRUs as needed."""

    def __init__(self, *args, cache_len: int = 10, **kwargs):
        assert cache_len > 0
        self.cache_len = cache_len
        self._list = []

    def set_item(self, key, value):
        kv = (key, value)
        data = self._list

        if kv in data:
           data.remove(kv)

        data.insert(0, kv)

        while len(data) > self.cache_len:
            data.remove(data[-1])

    def get_item(self, key):
        val = None
        for kv in self._list:
            if kv[0] == key:
                val = kv[1]
                break
        return val
    
    def __repr__(self):
        # convert list of key-value pairs to dict
        return repr(dict(self._list))
    
ratings = LimitedSizeList(cache_len=10)

for k in range(15, 1, -1):
    ratings.set_item(k, str(k))

print(ratings)