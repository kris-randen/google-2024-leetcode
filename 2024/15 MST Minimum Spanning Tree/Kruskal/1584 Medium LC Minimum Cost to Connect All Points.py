"""

1584. Min Cost to Connect All Points
Medium
You are given an array points representing integer coordinates of some points on a 2D-plane, where points[i] = [xi, yi].

The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between them: |xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.

Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.

 

Example 1:


Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
Output: 20
Explanation: 

We can connect the points as shown above to get the minimum cost of 20.
Notice that there is a unique path between every pair of points.
Example 2:

Input: points = [[3,12],[-2,5],[-4,1]]
Output: 18
 

"""

class UF:
    def __init__(self, n):
        self.id = [i for i in range(n)]
        self.sz = {i: 1 for i in range(n)}

    def unione(self, e):        self.union(e[0], e[1])
    def union(self, p, q):      self.update(*self.split(p, q)) if not self.find(p, q) else None
    def update(self, s, l):     self.assign(s, l); self.sizeup(s, l)
    def assign(self, s, l):     self.id[s] = l
    def sizeup(self, s, l):     self.sz[l] += self.sz.pop(s)
    def split(self, p, q):      self.pair(*self.roots(p, q))
    def pair(self, s, l):       return (s, l) if self.sz[s] < self.sz[l] else (l, s)
    def finde(self, e):         self.find(e[0], e[1])
    def find(self, p, q):       return self.root(p) == self.root(q)
    def roots(self, p, q):      return self.root(p), self.root(q)
    def root(self, p):
        if not p == self.id[p]: self.id[p] = self.root(self.id[p])
        return self.id[p]


def dist(p, q):         return abs(p[0] - q[0]) + abs(p[1] - q[1])
def edges(ps):          return [
                                    (ps[i], ps[j], dist(ps[i], ps[j])) 
                                    for i in range(n := len(ps)) 
                                    for j in range(i + 1, n)
                               ]

def kruskalMST(n, wes):
    uf, hs, mst = UF(n, wes), Heap(wes), set()
    while hs and len(mst) < n - 1:
        if not uf.finde(we := hs.pop()):
            uf.unione(we); mst.add(we)
    return (
            sum(we[2] for we in mst)
            if len(uf.sz) == 1 else -1
           )






