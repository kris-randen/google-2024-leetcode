"""
Index Heap
"""


class IndexHeap:
    def __init__(self, kvs=None, cmp=lambda x, y: x < y):
        self.kvs = kvs if kvs else {}
        self.p = [None] + list(self.kvs.keys())
        self.q = {v: i for i, v in enumerate(self.p) if i >= 1}
        self.cmp = cmp; self.heapify()

    def __len__(self):
        return len(self.p) - 1
    def __bool__(self):
        return len(self) > 0
    def __iter__(self):
        heap = IndexHeap(self.kvs.copy(), self.cmp)
        while heap:
            yield heap.pop()

    def prior(self, i, j):
        return i if self.cmp(self.val(i), self.val(j)) else j
    def val(self, i):
        return self.kvs[self.p[i]]
    def isvalid(self, i):
        return 1 <= i <= len(self)
    def valid(self, i):
        return i if self.isvalid(i) else None
    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def up(self, i):
        return i // 2
    def lt(self, i):
        return i * 2
    def rt(self, i):
        return i * 2 + 1

    def parent(self, c):
        return self.valid(self.up(c))
    def left(self, p):
        return self.valid(self.lt(p))
    def right(self, p):
        return self.valid(self.rt(p))
    def child(self, p):
        return self.pref(self.left(p), self.right(p))

    def balup(self, c):
        return self.pref(p := self.parent(c), c) == p
    def baldn(self, p):
        return self.pref(c := self.child(p), p) == p

    def unbalup(self, c):
        return self.parent(c) if not self.balup(c) else None
    def unbaldn(self, p):
        return self.child(p) if not self.baldn(p) else None

    def swap(self, i, j):
        self.p[i], self.p[j] = self.p[j], self.p[i]
        self.q[self.p[i]], self.q[self.p[j]] = i, j
        return j
    def swim(self, c):
        while p := self.unbalup(c):
            c = self.swap(c, p)
    def sink(self, p):
        while c := self.unbaldn(p):
            p = self.swap(p, c)

    def swapend(self):
        self.swap(1, len(self))
    def swimbot(self):
        self.swim(len(self))
    def sinktop(self):
        self.sink(1)
    def sinkswim(self, k):
        self.sink(k); self.swim(k)

    def peek(self):
        return self.p[1]

    def pop(self):
        if (top := self.peek()) is None: return None
        self.swapend();     self.p.pop()
        self.q.pop(top);    self.kvs.pop(top)
        self.sinktop();     return top

    def delete(self, key):
        k = self.q[key];    self.swap(k, len(self))
        self.q.pop(key);    self.kvs.pop(key)
        self.p.pop();       self.sinkswim(k)

    def update(self, key, newval):
        k = self.q[key]
        self.kvs[key] = newval
        self.sinkswim(k)

    def heapify(self):
        for p in reversed(range(1, len(self))): self.sink(p)

    def sorted(self):
        return list(self)

if __name__ == '__main__':
    kvs = {23: 2 * 23, 3: 2 * 3, 7: 2 * 7, 9: 2 * 9, 11: 2 * 11, 5: 2 * 5, 4: 2 * 4, 2: 2 * 2, 1: 2 * 1}
    hvs = IndexHeap(kvs)
    print(f'hvs p {hvs.p}')
    for v in hvs:
        print(v, hvs.kvs[v])
    print(f'hvs p {hvs.p}')
    print(f'sorted hvs keys {hvs.sorted()}')
    hvs.delete(23)
    print(f'hvs p {hvs.p}')                 
    print(f'sorted hvs keys {hvs.sorted()}')
