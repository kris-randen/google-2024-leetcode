"""

2685. Count the Number of Complete Components
Medium
Topics
Hint
You are given an integer n. There is an undirected graph with n vertices, numbered from 0 to n - 1. You are given a 2D integer array edges where edges[i] = [ai, bi] denotes that there exists an undirected edge connecting vertices ai and bi.

Return the number of complete connected components of the graph.

A connected component is a subgraph of a graph in which there exists a path between any two vertices, and no vertex of the subgraph shares an edge with a vertex outside of the subgraph.

A connected component is said to be complete if there exists an edge between every pair of its vertices.



Example 1:



Input: n = 6, edges = [[0,1],[0,2],[1,2],[3,4]]
Output: 3
Explanation: From the picture above, one can see that all of the components of this graph are complete.
Example 2:



Input: n = 6, edges = [[0,1],[0,2],[1,2],[3,4],[3,5]]
Output: 1
Explanation: The component containing vertices 0, 1, and 2 is complete since there is an edge between every pair of two vertices. On the other hand, the component containing vertices 3, 4, and 5 is not complete since there is no edge between vertices 4 and 5. Thus, the number of complete components in this graph is 1.


Constraints:

1 <= n <= 50
0 <= edges.length <= n * (n - 1) / 2
edges[i].length == 2
0 <= ai, bi <= n - 1
ai != bi
There are no repeated edges.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
27.3K
Submissions

Runtime 718 ms Beats 5.31%
Memory 17.40 MB Beats 10.47%

"""

class UnionFind:
    def __init__(self, n):
        self.id = [i for i in range(n)];
        self.max = 1
        self.comps = {i: {i} for i in range(n)}

    def size(self, i):
        return len(self.comps[i])

    @property
    def count(self):
        return len(self.comps)

    def parent(self, i):
        return self.id[i]

    def is_root(self, i):
        return i == self.parent(i)

    def is_not_root(self, i):
        return not self.is_root(i)

    def path(self, i):
        p = [i]
        while self.is_not_root(i):
            i = self.parent(i)
            p += [i]
        return p

    def assign(self, i, p):
        self.id[i] = p

    def compress(self, path):
        root = path[-1]
        for p in path: self.assign(p, root)
        return root

    def find(self, i):
        return self.compress(self.path(i))

    def split(self, p, q):
        return (p, q) if self.size(p) > self.size(q) else (q, p)

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if p != q: self.join(p, q)

    def merge(self, s, l):
        self.comps[l].update(self.comps.pop(s))

    def join(self, p, q):
        l, s = self.split(p, q)
        self.assign(s, l)
        self.merge(s, l)
        self.max = max(self.max, self.size(l))

def connected(u, v, edges_set):
    return (u, v) in edges_set or (v, u) in edges_set

def is_complete(comp, edges_set):
    vs = list(comp)
    m = len(vs)
    for i in range(m):
        for j in range(i + 1, m):
            if not connected(vs[i], vs[j], edges_set):
                return False
    return True


def tuplify(edges):
    return set(map(lambda x: (x[0], x[1]), edges))

def num_complete_cc(n, edges):
    uf = UnionFind(n); edges_set = tuplify(edges)
    for u, v in edges:
        uf.union(u, v)
    count = 0
    for root in uf.comps:
        if is_complete(uf.comps[root], edges_set): count += 1
    return count

