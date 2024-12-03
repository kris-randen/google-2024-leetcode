"""

1962. Remove Stones to Minimize the Total
Medium
Topics
Companies
Hint
You are given a 0-indexed integer array piles, where piles[i] represents the number of stones in the ith pile, and an integer k. You should apply the following operation exactly k times:

Choose any piles[i] and remove floor(piles[i] / 2) stones from it.
Notice that you can apply the operation on the same pile more than once.

Return the minimum possible total number of stones remaining after applying the k operations.

floor(x) is the greatest integer that is smaller than or equal to x (i.e., rounds x down).



Example 1:

Input: piles = [5,4,9], k = 2
Output: 12
Explanation: Steps of a possible scenario are:
- Apply the operation on pile 2. The resulting piles are [5,4,5].
- Apply the operation on pile 0. The resulting piles are [3,4,5].
The total number of stones in [3,4,5] is 12.
Example 2:

Input: piles = [4,3,6,7], k = 3
Output: 12
Explanation: Steps of a possible scenario are:
- Apply the operation on pile 2. The resulting piles are [4,3,3,7].
- Apply the operation on pile 3. The resulting piles are [4,3,3,4].
- Apply the operation on pile 0. The resulting piles are [2,3,3,4].
The total number of stones in [2,3,3,4] is 12.


Constraints:

1 <= piles.length <= 105
1 <= piles[i] <= 104
1 <= k <= 105

"""

class Heap:
    def __init__(self, vs, cmp=lambda x, y: x < y):
        self.pq = [None] + vs; self.N = None
        self.cmp = cmp; self.heapify()

    def val(self, i):       return self.pq[i]
    def prior(self, i, j):  return i if self.cmp(self.val(i), self.val(j)) else j
    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def size(self):         return self.N if self.N else len(self.pq) - 1
    def __len__(self):
        return self.size()
    def __bool__(self):
        return len(self) > 0
    def isval(self, i):     return 1 <= i <= self.size()
    def valid(self, i):     return i if self.isval(i) else None
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

    def swim(self, c):
        while p := self.unbalup(c): c = self.swap(c, p)
    def sink(self, p):
        while c := self.unbaldn(p): p = self.swap(p, c)
    def peek(self):
        if not self:
            raise IndexError("Can't peek into an empty heap.")
        return self.pq[1]

    def pop(self):
        if not self:
            raise IndexError("Cannot pop an empty heap.")
        self.swap(1, self.size())
        top = self.pq.pop()
        self.sink(1)
        return top

    def push(self, v):
        self.pq.append(v)
        self.swim(self.size())

    def heapify(self):
        for p in reversed(range(1, self.size())): self.sink(p)

    def sort(self):
        self.N = self.size()
        while self.N > 1:
            self.swap(1, self.N)
            self.N -= 1
            self.sink(1)
        self.N = None

    def sorted(self):
        self.sort()
        result = self.pq[1:].copy()
        self.heapify()
        return result

if __name__ == '__main__':
    vs = [7, 2, 9, 11, 13, 5, 3, 29, 43]
    hs = Heap(vs)
    hs.push(19)
    print(f'heap {hs.pq}')
    hs.pop()
    hs.pop()
    print(f'heap {hs.pq}')
    # hs.sort()
    # print(f'sort {hs.pq}')
    print(f'sorted {hs.sorted()}')
    print(f'heap {hs.pq}')
    print(f'popping {hs.pop()}')
    print(f'popping {hs.pop()}')
    print(f'popping {hs.pop()}')
    print(f'popping {hs.pop()}')
    print(f'popping {hs.pop()}')
    print(f'popping {hs.pop()}')
    print(f'popping {hs.pop()}')
    print(f'popping {hs.pop()}')
    print(f'peeking {hs.peek()}')

