"""

1514. Path with Maximum Probability
Solved
Medium

You are given an undirected weighted graph of n nodes (0-indexed), represented by an edge list where edges[i] = [a, b] is an undirected edge connecting the nodes a and b with a probability of success of traversing that edge succProb[i].

Given two nodes start and end, find the path with the maximum probability of success to go from start to end and return its success probability.

If there is no path from start to end, return 0. Your answer will be accepted if it differs from the correct answer by at most 1e-5.



Example 1:



Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2], start = 0, end = 2
Output: 0.25000
Explanation: There are two paths from start to end, one having a probability of success = 0.2 and the other has 0.5 * 0.5 = 0.25.
Example 2:



Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.3], start = 0, end = 2
Output: 0.30000
Example 3:



Input: n = 3, edges = [[0,1]], succProb = [0.5], start = 0, end = 2
Output: 0.00000
Explanation: There is no path between 0 and 2.


Constraints:

2 <= n <= 10^4
0 <= start, end < n
start != end
0 <= a, b < n
a != b
0 <= succProb.length == edges.length <= 2*10^4
0 <= succProb[i] <= 1
There is at most one edge between every two nodes.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
374,913/572.2K
Acceptance Rate
65.5%

"""

from heapq import heappop, heappush
from typing import List
from math import log, inf, exp


def add_edge(g, edge, prob):
    if prob == 0: return

    u, v = edge; wt = -log(prob)
    g[u].append((v, wt))
    g[v].append((u, wt))

def graph(V: int, edges: List[List[int]], probs: List[float]):
    g = {v: [] for v in range(V)}

    for edge, prob in zip(edges, probs):
        add_edge(g, edge, prob)

    return g

def dijkstra(g, source):
    dist = {v: inf for v in g}
    dist[source] = 0; pq = [(0, source)]

    while pq:
        du, u = heappop(pq)
        if du > dist[u]:
            continue

        for v, uv in g[u]:
            if (candidate := du + uv) < dist[v]:
                dist[v] = candidate
                heappush(pq, (candidate, v))

    return dist

def max_probability(n, edges, probs, s, e):
    g = graph(n, edges, probs)
    dist = dijkstra(g, s)
    return 0 if dist[e] == inf else exp(-dist[e])

class Solution:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start_node: int, end_node: int) -> float:
        return max_probability(n, edges, succProb, start_node, end_node)
