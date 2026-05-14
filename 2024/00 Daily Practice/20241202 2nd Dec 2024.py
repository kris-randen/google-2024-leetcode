"""

Heap
and
Index Heap

"""
import copy


class Heap:
    def __init__(self, vs=None, cmp=lambda x, y: x < y):
        self.pq = [None] + (vs if vs else [])
        self.cmp = cmp; self.heapify()

    def __len__(self):
        return len(self.pq) - 1

    def __bool__(self):
        return len(self) > 0

    def __iter__(self):
        heap = Heap(self.pq[1:].copy(), self.cmp)
        while heap:
            yield heap.pop()

    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def val(self, i):
        return self.pq[i]

    def prior(self, i, j):
        return i if self.cmp(self.val(i), self.val(j)) else j

    def isvalid(self, i):
        return 1 <= i <= len(self)

    def valid(self, i):
        return i if self.isvalid(i) else None

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
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
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

    def sinkswim(self, p):
        self.sink(p); self.swim(p)

    def peek(self):
        return self.pq[1]

    def pop(self):
        if (top := self.peek()) is None: return None
        self.swapend()
        self.pq.pop()
        self.sinktop()
        return top

    def push(self, v):
        self.pq.append(v)
        self.swimbot()

    def heapify(self):
        for p in reversed(range(1, len(self))): self.sink(p)

    def sorted(self):
        return list(self)


class IndexHeap:
    def __init__(self, kvs=None, cmp=lambda x, y: x < y):
        self.kvs = kvs if kvs else {}
        self.pq = [None] + list(self.kvs.keys())
        self.qp = {v: i for i, v in enumerate(self.pq) if i >= 1}
        self.cmp = cmp; self.heapify()

    def __len__(self):
        return len(self.pq) - 1

    def __bool__(self):
        return len(self) > 0

    def __iter__(self):
        heap = IndexHeap(self.kvs.copy(), self.cmp)
        while heap:
            yield heap.pop()

    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def prior(self, i, j):
        return i if self.cmp(self.val(i), self.val(j)) else j

    def val(self, i):
        return self.kvs[self.pq[i]]

    def isvalid(self, i):
        return 1 <= i <= len(self)

    def valid(self, i):
        return i if self.isvalid(i) else None

    def up(self, i):
        return i // 2

    def lt(self, i):
        return 2 * i

    def rt(self, i):
        return 2 * i + 1

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
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j
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

    def peek(self):
        return self.pq[1]

    def pop(self):
        if (top := self.peek()) is None: return None
        self.swapend();     self.pq.pop()
        self.qp.pop(top);   self.kvs.pop(top)
        self.sinktop();     return top

    def heapify(self):
        for p in reversed(range(1, len(self))): self.sink(p)

    def sorted(self):
        return list(self)

if __name__ == '__main__':
    vs = [23, 3, 7, 9, 11, 5, 4, 2, 1]
    hs = Heap(vs)
    print(f'pq {hs.pq}')
    print(hs.sorted())
    kvs = {23: 2*23, 3: 2*3, 7: 2*7, 9: 2*9, 11: 2*11, 5: 2*5, 4: 2*4, 2: 2*2, 1: 2*1}
    hvs = IndexHeap(kvs)
    print(f'hvs pq {hvs.pq}')
    for v in hvs:
        print(v, hvs.kvs[v])
    print(f'hvs pq {hvs.pq}')
    print(f'sorted hvs keys {hvs.sorted()}')