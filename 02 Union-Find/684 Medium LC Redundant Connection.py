"""

684. Redundant Connection
Solved
Medium
Topics
Companies
In this problem, a tree is an undirected graph that is connected and has no cycles.

You are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed. The graph is represented as an array edges of length n where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the graph.

Return an edge that can be removed so that the resulting graph is a tree of n nodes. If there are multiple answers, return the answer that occurs last in the input.



Example 1:


Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]
Example 2:


Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
Output: [1,4]


Constraints:

n == edges.length
3 <= n <= 1000
edges[i].length == 2
1 <= ai < bi <= edges.length
ai != bi
There are no repeated edges.
The given graph is connected.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
370.3K
Submissions
586.6K


Runtime 58 ms Beats 40.24%
Memory 17.04 MB Beats 38.11%

"""

class UnionFind:
    def __init__(self, n):
        self.id = [None] + [i + 1 for i in range(n)]
        self.sz = [None] + [1 for _ in range(n)]


    def size(self, p):
        return self.sz[p]

    def path(self, i):
        p = [i]
        while not i == self.id[i]:
            i = self.id[i]
            p.append(i)
        return p

    def compressed(self, path):
        root = path[-1]
        for p in path: self.id[p] = root
        return root

    def find(self, i):
        return self.compressed(self.path(i))

    def split(self, p, q):
        return (p, q) if self.size(p) > self.size(q) else (q, p)

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if p == q: return
        return self.join(p, q)

    def join(self, p, q):
        l, s = self.split(p, q)
        self.id[s] = l
        self.sz[l] += self.sz[s]
        return l


def find_redundant(edges):
    uf = UnionFind(len(edges))
    for (u, v) in edges:
        flag = uf.union(u, v)
        if not flag: return [u, v]

