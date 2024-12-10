"""

Daily Practice

"""


"""

Union Find

"""



class DynamicUnionFind:
    def __init__(self, n=0):
        self.id = {i: i for i in range(n)}
        self.sz = {i: 1 for i in range(n)}

    def add(self, p):
        if p in self.id: return
        self.id[p] = p; self.sz[p] = 1

    def root(self, p):
        if not self.id[p] == p:
            self.id[p] = self.root(self.id[p])
        return self.id[p]

    def find(self, p, q):
        return self.root(p) == self.root(q)

    def split(self, p, q):
        s, l = self.root(p), self.root(q)
        return (s, l) if self.sz[s] < self.sz[l] else (l, s)

    def union(self, p, q):
        s, l = self.split(p, q)
        self.id[s] = l
        self.sz[l] += self.sz.pop(s)



"""

Index Heap

"""




class IndexHeap:
    def __init__(self, vs=None, cmp=lambda x, y: x < y):
        self.pq = [None] + (vs if vs else [])
        self.qp = {v: i for i, v in enumerate(self.pq) if i >= 1}
        self.cmp = cmp; self.heapify()

    def __len__(self):
        return len(self.pq) - 1
    def __bool__(self):
        return len(self) > 0
    def __iter__(self):
        heap = IndexHeap(self.pq[1:], self.cmp)
        while heap:
            yield heap.pop()

    def peek(self):
        return self.pq[1] if self else None
    def pop(self):
        if (top := self.peek()) is None: return None
        self.swapend(); self.pq.pop()
        self.qp.pop(top); self.sinktop()
        return top
    def push(self, v):
        self.pq.append(v)
        self.qp[v] = len(self)
        self.swimbot()
    def sorted(self):
        return list(self)


    def heapify(self):
        for p in reversed(range(1, len(self) // 2 + 1)): self.sink(p)
    def swim(self, c):
        while p := self.unbalup(c): c = self.swap(c, p)
    def sink(self, p):
        while c := self.unbaldn(p): p = self.swap(p, c)
    def unbalup(self, c):
        return self.parent(c) if not self.balup(c) else None
    def unbaldn(self, p):
        return self.child(p) if not self.baldn(p) else None
    def balup(self, c):
        return self.pref(p := self.parent(c), c) == p
    def baldn(self, p):
        return self.pref(c := self.child(p), p) == p
    def parent(self, c):
        return self.valid(self.up(c))
    def child(self, p):
        return self.pref(self.left(p), self.right(p))
    def left(self, p):
        return self.valid(self.lt(p))
    def right(self, p):
        return self.valid(self.rt(p))
    def up(self, i):
        return i // 2
    def lt(self, i):
        return i * 2
    def rt(self, i):
        return i * 2 + 1
    def valid(self, i):
        return i if self.isval(i) else None
    def isval(self, i):
        return 1 <= i <= len(self)
    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j
        return j
    def swapend(self):
        self.swap(1, len(self))
    def swimbot(self):
        self.swim(len(self))
    def sinktop(self):
        self.sink(1)
    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j
    def prior(self, i, j):
        return i if self.cmp(self.val(i), self.val(j)) else j
    def val(self, i):
        return self.pq[i]

if __name__ == '__main__':
    vs = [2, 3, 7, 0, -7, 13, -2]
    hs = IndexHeap(vs)
    print(f'heap {hs.pq}')
    sh = hs.sorted()
    print(f'sorted {sh}')




















