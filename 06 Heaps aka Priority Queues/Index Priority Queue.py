
class Heap:
    def __init__(self, vs=None, compare=lambda a, b: a < b):
        self.vs = [None] + vs if vs else [None]
        self.compare = compare; self.N = None; self.heapify()

    @property
    def size(self):
        return (len(self.vs) - 1) if self.N is None else self.N

    def isvalid(self, i):
        return i is not None and 1 <= i <= self.size

    def valid(self, i):
        return i if self.isvalid(i) else None

    def val(self, i):
        return self.vs[i] if self.isvalid(i) else None

    def comp(self, i, j):
        return self.compare(self.val(i), self.val(j))

    def pref(self, i, j):
        if self.isvalid(i) and self.isvalid(j):
            return i if self.comp(i, j) else j
        return i if not self.valid(j) else j

    def up(self, i):     return i // 2

    def lt(self, i):     return 2 * i

    def rt(self, i):     return 2 * i + 1

    def parent(self, c): return self.valid(self.up(c))

    def left(self, p):   return self.valid(self.lt(p))

    def right(self, p):  return self.valid(self.rt(p))

    def child(self, p):  return self.pref(self.left(p), self.right(p))

    def swap(self, i, j):
        self.vs[i], self.vs[j] = self.vs[j], self.vs[i]
        return j

    def bal_up(self, c):
        p = self.parent(c)
        return not p or self.pref(c, p) == p

    def bal_dn(self, p):
        return (c := self.child(p)) is None or self.pref(p, c) == p

    def unbal_up(self, c):
        return self.parent(c) if not self.bal_up(c) else None

    def unbal_dn(self, p):
        return self.child(p) if not self.bal_dn(p) else None

    def swim(self, c):
        while p := self.unbal_up(c):
            c = self.swap(c, p)

    def sink(self, p):
        while c := self.unbal_dn(p):
            p = self.swap(p, c)

    def heapify(self):
        for p in range(self.size, 0, -1): self.sink(p)

    def sort(self):
        self.N = self.size
        while self.N > 0:
            self.swap(1, self.N)
            self.N -= 1
            self.sink(1)
        self.N = None

from toolz.sandbox import unzip

class IndexHeap:
    def __init__(self, kvs:dict = None, compare=lambda a, b: a < b):
        self.kvs = {} if not kvs else kvs
        self.pq = [None] + list(self.kvs.keys())
        self.qp = {k: i for i, k in enumerate(self.kvs)}
        self.compare = compare; self.N = None
        self.heapify()

    def heapify(self):
        for p in reversed(range(1, self.size)): self.sink(p)


    @property
    def keys(self):
        return self.pq[1:]

    @property
    def vals(self):
        return [self.kvs[key] for key in self.keys]

    @property
    def size(self):
        return len(self.kvs) if self.N is None else self.N

    def sink(self, p):
        while c := self.unbal_dn(p): p = self.swap(p, c)

    def swim(self, c):
        while p := self.unbal_up(c): c = self.swap(c, p)

    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j
        return j

    def unbal_up(self, c):
        return self.parent(c) if not self.bal_up(c) else None

    def unbal_dn(self, p):
        return self.child(p) if not self.bal_dn(p) else None

    def bal_dn(self, p):
        return self.pref(p, c := self.child(p)) == p

    def bal_up(self, c):
        return self.pref(c, p := self.parent(c)) == p

    def parent(self, c): return self.valid(self.up(c))

    def child(self, p):  return self.pref(self.left(p), self.right(p))

    def left(self, p):   return self.valid(self.lt(p))

    def right(self, p):  return self.valid(self.rt(p))

    def up(self, i):     return i // 2

    def lt(self, i):     return 2 * i

    def rt(self, i):     return 2 * i + 1

    def valid(self, i):
        return i if self.is_valid(i) else None

    def is_valid(self, i):
        return i is not None and 1 <= i <= self.size

    def pref(self, i, j):
        if self.valid(i) and self.valid(j):
            return i if self.comp(i, j) else j
        return i if not j else j

    def comp(self, i, j):
        return self.compare(self.val(i), self.val(j))

    def val(self, i):
        return self.kvs[self.pq[i]]

    def contains(self, k):
        return k in self.kvs

    def push(self, key, val):
        if self.contains(key): self.update(key, val)
        self.kvs[key] = val; self.pq.append(key)
        self.qp[key] = self.size; self.swim(self.size)

    def top(self):
        return self.val(1) if self.kvs else None

    def pop(self):
        if (top := self.top()) is None: return
        self.swap(1, self.size)
        self.delete(self.size)
        self.sink(1); return top

    def update(self, key, val):
        if not self.contains(key): self.push(key, val)
        self.kvs[key] = val
        self.swim(self.qp[key])
        self.sink(self.qp[key])

    def delete(self, key):
        if not self.contains(key): return
        k = self.qp[key]; val = self.val(k)
        self.swap(k, self.size)
        self.kvs.pop(key); self.qp.pop(key)
        self.pq.pop(); self.sink(k)

    def sort(self):
        self.N = self.size
        while self.N > 0:
            self.swap(1, self.N)
            self.N -= 1
            self.sink(1)
        self.N = None

    def sorted_pairs(self):
        self.sort()
        sorted_ps = zip(self.keys, self.vals)
        self.heapify()
        return sorted_ps

    def sorted_keys(self):
        return unzip(self.sorted_pairs())[0]

    def sorted_vals(self):
        return unzip(self.sorted_pairs())[1]

def printh(ih):
    print(f'index heap pq {ih.pq}')
    print(f'index heap qp {ih.qp}')
    print(f'index heap kvs {ih.kvs}')
    print(f'index heap keys {ih.keys}')
    print(f'index heap vals {ih.vals}')


if __name__ == '__main__':
    vs = [2, 9, 1, 0, 5, 11, 17]
    kvs = {1: 5, 2: 11, 5: 7, 4: 23, 0: -5, 8: 13}
    h = Heap(vs)
    ih = IndexHeap(kvs)
    printh(ih)
    print(f'pushing key 11 val -7')
    ih.push(11, -7)
    printh(ih)
    ih.sort()
    print(f'sorted')
    printh(ih)
    ih.delete(1)
    ih.delete(2)
    ih.delete(0)
    ih.delete(8)
    printh(ih)





















