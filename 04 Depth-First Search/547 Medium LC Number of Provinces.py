"""


Code
Testcase
Testcase
Test Result
547. Number of Provinces
Solved
Medium
Topics
Companies
There are n cities. Some of them are connected, while some are not. If city a is connected directly with city b, and city b is connected directly with city c, then city a is connected indirectly with city c.

A province is a group of directly or indirectly connected cities and no other cities outside of the group.

You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.

Return the total number of provinces.



Example 1:


Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
Output: 2
Example 2:


Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
Output: 3


Constraints:

1 <= n <= 200
n == isConnected.length
n == isConnected[i].length
isConnected[i][j] is 1 or 0.
isConnected[i][i] == 1
isConnected[i][j] == isConnected[j][i]

"""

from typing import List


def dfs(rs):
    def nbs(u):     return (v for v, c in enumerate(rs[u]) if c == 1)

    def visit(u):
        visited.add(u)
        for v in nbs(u):
            if v not in visited: visit(v)

    visited = set(); count = 0
    for v in range(len(rs)):
        if v not in visited:
            visit(v); count += 1

    return count

class UnionFind:
    def __init__(self, n):
        self.id = [i for i in range(n)]
        self.sz = {i: 1 for i in range(n)}

    def root(self, p):
        if not p == self.id[p]:
            self.id[p] = self.root(self.id[p])
        return self.id[p]

    def find(self, p, q):
        return self.root(p) == self.root(q)

    def split(self, p, q):
        s, l = self.root(p), self.root(q)
        return (s, l) if self.sz[s] < self.sz[l] else (l, s)

    def union(self, p, q):
        if self.find(p, q): return
        s, l = self.split(p, q)
        self.id[s] = l
        self.sz[l] += self.sz.pop(s)

    def count(self):
        return len(self.sz)

def provinces(rs):
    def nbs(v):
        return (w for w, c in enumerate(rs[v]) if c == 1)

    uf = UnionFind(n := len(rs))
    for u in range(n):
        for v in nbs(u):
            uf.union(u, v)

    return uf.count()

class Solution:
    def findCircleNum(self, rs: List[List[int]]) -> int:
        return dfs(rs)