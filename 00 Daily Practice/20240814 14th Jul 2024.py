class UnionFind:
    def __init__(self, vs):
        self.map = {v: i for i, v in enumerate(vs)}
        self.n = len(self.map); self.max = 1
        self.id = [i for i in range(self.n)]
        self.comps = {i: {i} for i in range(self.n)}

    @property
    def count(self):
        return len(self.comps)

    def size(self, p):
        return len(self.comps[p])

    def parent(self, i):
        return self.id[i]

    def assign(self, i, p):
        self.id[i] = p

    def is_greater(self, p, q):
        return self.size(p) > self.size(q)

    def split(self, p, q):
        return (p, q) if self.is_greater(p, q) else (q, p)

    def merge(self, s, l):
        self.comps[l].update(self.comps.pop(s))
        self.max = max(self.max, self.size(l))

    def join(self, p, q):
        l, s = self.split(p, q)
        self.assign(s, l)
        self.merge(s, l)



    def find(self, i):
        while not i == self.parent(i):
            self.assign(i, self.find(self.parent(i)))
        return self.parent(i)

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if not p == q: self.join(p, q)


class HeapDict:
    def __init__(self, weights=None, compare=lambda x, y: x < y):
        self.wts = {} if not weights else weights
        self.pq = [None] + list(self.wts.keys())
        self.qp = {k: i for i, k in enumerate(self.pq)}
        self.N = None; self.compare = compare; self.heapify()

    def size(self):
        return self.N if self.N else len(self.wts)

    @property
    def last_ind(self):
        return self.size()

    @property
    def last(self):
        return self.key(self.last_ind)

    @property
    def first_ind(self):
        return 1

    @property
    def first(self):
        return self.key(self.first_ind)

    def valid(self, i):
        return i if (i and 1 <= i <= self.size()) else None

    def key(self, i):
        return self.pq[i]

    def keys(self):
        return self.pq[1:].copy()

    def vals(self):
        return list(map(lambda key: self.wts[key], self.keys()))

    def wt(self, i):
        return self.wts[self.key(i)]

    def cmp(self, i, j):
        return self.compare(self.wt(i), self.wt(j))

    def pref(self, i, j):
        if i and j:
            return i if self.cmp(i, j) else j
        return i if not j else j

    def up(self, i):
        return i // 2

    def left(self, i):
        return 2 * i

    def right(self, i):
        return 2 * i + 1

    def l_child(self, p):
        return self.valid(self.left(p))

    def r_child(self, p):
        return self.valid(self.right(p))

    def parent(self, c):
        return self.valid(self.up(c))

    def child(self, p):
        return self.pref(self.l_child(p), self.r_child(p))

    def bal_up(self, c):
        p = self.parent(c)
        return not p or self.pref(p, c) == p

    def bal_dn(self, p):
        c = self.child(p)
        return not c or self.pref(p, c) == p

    def unbal_up(self, c):
        return None if self.bal_up(c) else self.parent(c)

    def unbal_dn(self, p):
        return None if self.bal_dn(p) else self.child(p)

    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j

    def climb(self, i, j):
        self.swap(i, j); return j

    def swim(self, c):
        while not self.bal_up(c):
            c = self.climb(c, self.unbal_up(c))

    def sink(self, p):
        while not self.bal_dn(p):
            p = self.climb(p, self.unbal_dn(p))

    def sort(self):
        self.N = self.size()
        while self.N > 1:
            self.swap(1, self.N)
            self.N -= 1
            self.sink(1)
        self.N = None; return self.keys()

    def assign(self, key, val):
        i = self.qp[key]
        self.pq[i] = key
        self.wts[key] = val
        return i

    def append(self, key, val):
        self.pq.append(key)
        self.qp[key] = self.size()
        self.wts[key] = val

    def balance(self, i):
        self.sink(i); self.swim(i)

    def update(self, key, val):
        i = self.assign(key, val)
        self.balance(i)
        self.qp[key] = i

    def push(self, key, val):
        if key in self.wts: self.update(key, val)
        self.append(key, val)
        self.swim(self.size())

    def pop(self):
        self.swap(1, self.size())
        return self.delete(self.last)

    def pop_val(self):
        val = self.wts[self.first]
        self.pop(); return val

    def pop_k_val(self):
        key, val = self.first, self.wts[self.first]
        self.pop(); return key, val

    def top(self):
        return self.first

    def delete(self, key):
        i = self.qp[key]
        self.pq.pop(i)
        self.qp.pop(key)
        self.wts.pop(key)
        return key

    def heapify(self):
        for p in range(self.size(), 0, -1):
            self.sink(p)

    def sorted_keys(self):
        ks_sorted = self.sort()
        self.heapify(); return ks_sorted

    def sorted_vals(self):
        keys = self.sorted_keys()
        return list(map(lambda key: self.wts[key], keys))

    def sorted_k_vals(self):
        return list(zip(self.sorted_keys(), self.sorted_vals()))



if __name__ == '__main__':
    vs = dict(enumerate([4, 7, 13, 9, 3, 2, 1, 5, 29], start=1))
    pq = HeapDict(vs)
    print(pq.keys())
    print(pq.vals())
    print(pq.sorted_vals())
    print(pq.keys(), pq.vals())
    print(pq.wts)
    print(pq.pop_k_val())
    # print(pq.pop_val())
    print(pq.keys())

    