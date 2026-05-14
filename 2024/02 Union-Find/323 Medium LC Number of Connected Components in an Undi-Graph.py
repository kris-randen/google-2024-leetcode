"""

323. Number of Connected Components in an Undirected Graph
Medium
Topics
Companies
You have a graph of n nodes. You are given an integer n and an array edges where edges[i] = [ai, bi] indicates that there is an edge between ai and bi in the graph.

Return the number of connected components in the graph.



Example 1:


Input: n = 5, edges = [[0,1],[1,2],[3,4]]
Output: 2
Example 2:


Input: n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]
Output: 1


Constraints:

1 <= n <= 2000
1 <= edges.length <= 5000
edges[i].length == 2
0 <= ai <= bi < n
ai != bi
There are no repeated edges.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
409.4K
Submissions
649.8K

Runtime 104 ms Beats 8.88%
Memory 18.39 MB Beats 42.33%

"""

class UnionFind:
    def __init__(self, n):
        self.id = [i for i in range(n)]
        self.sz = [1 for _ in range(n)]
        self.count = n

    def size(self, i):
        return self.sz[i]

    def parent(self, i):
        return self.id[i]

    def is_root(self, i):
        return i == self.parent(i)

    def not_root(self, i):
        return not self.is_root(i)

    def path(self, i):
        p = [i]
        while self.not_root(i):
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

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if p == q: return
        self.count -= 1
        return self.join(p, q)

    def split(self, p, q):
        return (p, q) if self.size(p) > self.size(q) else (q, p)

    def merge(self, s, l):
        self.sz[l] += self.sz[s]

    def join(self, p, q):
        l,s = self.split(p, q)
        self.assign(s, l)
        self.merge(s, l)

def connected_comps(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.count