class HeapDict:
    def __init__(self, weights=None, compare=lambda x, y: x < y):
        self.wts = {} if not weights else weights
        self.pq = [None] + list(self.wts.keys())
        self.qp = {k: i for i, k in enumerate(self.pq)}
        self.compare = compare
        self.N = None
        self.heapify()

    def size(self):
        return self.N if self.N else len(self.wts)

    def key(self, i):
        return self.pq[i]

    def keys(self):
        return self.pq[1:].copy()

    def vals(self):
        return list(map(lambda key: self.wts[key], self.keys()))

    def val(self, i):
        return self.wts[self.key(i)]

    def cmp(self, i, j):
        return self.compare(self.val(i), self.val(j))

    def pref(self, i, j):
        if i and j:
            return i if self.cmp(i, j) else j
        return i if not j else j

    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j

    def climb(self, i, j):
        self.swap(i, j); return j

    def up(self, i):
        return i // 2

    def left(self, i):
        return 2 * i

    def right(self, i):
        return 2 * i + 1

    def valid(self, i):
        return i if (i and 1 <= i <= self.size()) else None

    def parent(self, c):
        return self.valid(self.up(c))

    def l_child(self, p):
        return self.valid(self.left(p))

    def r_child(self, p):
        return self.valid(self.right(p))

    def child(self, p):
        return self.pref(self.l_child(p), self.r_child(p))

    def bal_up(self, c):
        p = self.parent(c)
        return not p or self.pref(p, c) == p

    def bal_dn(self, p):
        c = self.child(p)
        return not c or self.pref(p, c) == p

    def unbal_up(self, c):
        return self.parent(c) if not self.bal_up(c) else None

    def unbal_dn(self, p):
        return self.child(p) if not self.bal_dn(p) else None

    def swim(self, c):
        while not self.bal_up(c):
            c = self.climb(c, self.unbal_up(c))

    def sink(self, p):
        while not self.bal_dn(p):
            p = self.climb(p, self.unbal_dn(p))

    def heapify(self):
        for p in range(self.size(), 0, -1):
            self.sink(p)

    def sort(self):
        self.N = self.size()
        while self.N > 1:
            self.swap(1, self.N)
            self.N -= 1
            self.sink(1)
        self.N = None
        return self.keys()

    def sorted_keys(self):
        keys = self.sort()
        self.heapify()
        return keys

    def sorted_vals(self):
        return list(map(lambda key: self.wts[key],
                        self.sorted_keys()))

    def sorted_key_vals(self):
        return list(zip(self.sorted_keys(), self.sorted_vals()))

    def sorted(self, on=0):
        if on == 0: return self.sorted_keys()
        if on == 1: return self.sorted_vals()
        if on == 2: return self.sorted_key_vals()


class UnionFind:
    def __init__(self, n):

        pass

if __name__ == '__main__':
    weights = dict(enumerate([4, 2, 1, 7, 11, 3, 19], start=1))
    pq = HeapDict(weights)
    print(list(zip(pq.keys(), pq.vals())))
    print(pq.wts)
    print(pq.sorted_vals())
    print(pq.sorted_keys())