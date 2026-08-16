"""

323. Number of Connected Components in an Undirected Graph
Solved
Medium

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
edges[i] = [ai, bi]
ai != bi
There are no repeated edges.

"""

from typing import List

def graph(n: int, edges: List[List[int]]) -> List[List[int]]:
    g = [[] for _ in range(n)]

    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    return g


def vertices(g: List[List[int]]) -> range:
    return range(len(g))


def components(g: List[List[int]]) -> int:
    seen = [False] * len(g)

    def dfs(v: int):
        seen[v] = True

        for w in g[v]:
            if not seen[w]:
                dfs(w)

    count = 0
    for v in vertices(g):
        if not seen[v]:
            dfs(v)
            count += 1

    return count



class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        return components(graph(n, edges))