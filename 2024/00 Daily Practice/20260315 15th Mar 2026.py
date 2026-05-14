from typing import Callable, Optional


def up(i):
    return i // 2

def left(i):
    return i * 2

def right(i):
    return i * 2 + 1

class Heap:
    def __init__(self, compare: Callable[[int, int], bool]):
        self.pq = []
        self.compare = compare

    def pref(self, i, j):
        if i is None: return j
        if j is None: return i
        return i if self.compare(i, j) else j

    def size(self):
        return len(self.pq)

    def valid(self, i):
        return i if i and (1 <= i < self.size()) else None

    def left_child(self, p):
        return self.valid(left(p))

    def right_child(self, p):
        return self.valid(right(p))

    def parent(self, c):
        return self.valid(up(c))

    def child(self, p):
        return self.pref(
                    self.left_child(p),
                    self.right_child(p)
                    )

    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        return i


    def bal_dn(self, p):
        return self.pref(p, self.child(p)) == p

    def bal_up(self, c):
        p = self.parent(c)
        return self.pref(c, p) == p

    def unbal_dn(self, p):
        return not self.bal_dn(p)

    def unbal_up(self, p):
        return not self.bal_up(p)

    def sink(self, p):
        while c := self.unbal_dn(p):
            p = self.swap(p, c)

    def swim(self, c):
        while p := self.unbal_up(c):
            c = self.swap(c, p)

    def heapify(self):
        for p in range(self.size(), 0, -1):
            self.sink(p)







