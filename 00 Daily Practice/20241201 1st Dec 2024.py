"""

Heap

"""

class Heap:
    def __init__(self, vs, cmp=lambda x, y: x < y):
        self.pq = [None] + vs
        self.N = None
        self.cmp = cmp
        self.heapify()

    def __len__(self):
        return self.N if self.N else len(self.pq) - 1
    def __bool__(self):
        return len(self) > 0
    def __iter__(self):
        heap = Heap(self.pq[1:], self.cmp)
        while heap:
            yield heap.pop()

    def val(self, i):       return self.pq[i]
    def isval(self, i):     return 1 <= i <= len(self)
    def valid(self, i):     return i if self.isval(i) else None
    def prior(self, i, j):
        return i if self.cmp(self.val(i), self.val(j)) else j

    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def up(self, i):        return i // 2
    def lt(self, i):        return 2 * i
    def rt(self, i):        return 2 * i + 1
    def parent(self, c):    return self.valid(self.up(c))
    def left(self, p):      return self.valid(self.lt(p))
    def right(self, p):     return self.valid(self.rt(p))
    def child(self, p):     return self.pref(self.left(p), self.right(p))

    def balup(self, c):     return self.pref(p := self.parent(c), c) == p
    def baldn(self, p):     return self.pref(c := self.child(p), p) == p
    def unbalup(self, c):   return None if self.balup(c) else self.parent(c)
    def unbaldn(self, p):   return None if self.baldn(p) else self.child(p)

    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        return j

    def swapend(self):
        self.swap(1, len(self))

    def swim(self, c):
        while p := self.unbalup(c):
            c = self.swap(c, p)

    def swimend(self):
        self.swim(len(self))

    def sink(self, p):
        while c := self.unbaldn(p):
            p = self.swap(p, c)

    def sinktop(self):
        self.sink(1)

    def peek(self):
        return self.pq[1] if self else None

    def pop(self):
        if (top := self.peek()) is None: return None
        self.swapend()
        self.pq.pop()
        self.sinktop()
        return top

    def insert(self, v):
        self.pq.append(v); self.swimend()

    def heapify(self):
        for p in reversed(range(1, len(self) // 2 + 1)): self.sink(p)

    def sorted(self):
        return list(self)

class IndexHeap:
    def __init__(self, vs=None, cmp=lambda x, y: x < y):
        self.pq = [None] + (vs if vs else [])
        self.qp = {v: i for i, v in enumerate(self.pq) if i >= 1}
        self.N = None; self.cmp = cmp; self.heapify()

    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j
        return j

    def swapend(self):
        self.swap(1, len(self))

    def __len__(self):
        return self.N if self.N else len(self.pq) - 1
    def __bool__(self):
        return len(self) > 0
    def __iter__(self):
        heap = IndexHeap(self.pq[1:], self.cmp)
        while heap:
            yield heap.pop()

    def prior(self, i, j):
        return i if self.cmp(self.val(i), self.val(j)) else j
    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def val(self, i):       return self.pq[i]
    def isval(self, i):     return 1 <= i <= len(self)
    def valid(self, i):     return i if self.isval(i) else None
    def up(self, i):        return i // 2
    def lt(self, i):        return 2 * i
    def rt(self, i):        return 2 * i + 1
    def parent(self, c):    return self.valid(self.up(c))
    def left(self, p):      return self.valid(self.lt(p))
    def right(self, p):     return self.valid(self.rt(p))
    def child(self, p):     return self.pref(
                                                self.left(p),
                                                self.right(p)
                                            )

    def balup(self, c):
        return self.pref(p := self.parent(c), c) == p
    def baldn(self, p):
        return self.pref(c := self.child(p), p) == p

    def unbalup(self, c):
        return None if self.balup(c) else self.parent(c)
    def unbaldn(self, p):
        return None if self.baldn(p) else self.child(p)

    def swim(self, c):
        while p := self.unbalup(c): c = self.swap(c, p)
    def sink(self, p):
        while c := self.unbaldn(p): p = self.swap(p, c)
    def sinktop(self):
        self.sink(1)
    def swimbot(self):
        self.swim(len(self))

    def peek(self):
        return self.pq[1]

    # noinspection PyNoneFunctionAssignment
    def pop(self):
        if (top := self.peek()) is None: return None
        self.swapend()
        self.pq.pop()
        self.qp.pop(top)
        self.sinktop()
        return top

    def insert(self, v):
        self.pq.append(v)
        self.qp[v] = len(self)
        self.swimbot()

    def update(self, u, v):
        p = self.qp[u]; self.qp.pop(u)
        self.pq[p] = v; self.qp[v] = p
        self.sink(p);   self.swim(p)

    def delete(self, u):
        p = self.qp[u]
        self.qp.pop(u)
        self.swap(p, len(self))
        self.pq.pop()
        self.sink(p)

    def heapify(self):
        for p in reversed(range(1, len(self))): self.sink(p)

    def sorted(self):
        return list(self)






