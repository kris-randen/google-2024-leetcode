"""

743. Network Delay Time
Solved
Medium

You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as directed edges times[i] = (ui, vi, wi), where ui is the source node, vi is the target node, and wi is the time it takes for a signal to travel from source to target.

We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.


Example 1:


Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2
Example 2:

Input: times = [[1,2,1]], n = 2, k = 1
Output: 1
Example 3:

Input: times = [[1,2,1]], n = 2, k = 2
Output: -1


Constraints:

1 <= k <= n <= 100
1 <= times.length <= 6000
times[i].length == 3
1 <= ui, vi <= n
ui != vi
0 <= wi <= 100
All the pairs (ui, vi) are unique. (i.e., no multiple edges.)

Seen this question in a real interview before?
1/6
Yes
No
Accepted
883,887/1.5M
Acceptance Rate
60.4%

"""

from heapq import *
from typing import List
from math import inf

def graph(V: int, edges: List[tuple[int, int, int]]):
    g = {v: [] for v in range(1, V + 1)}

    for u, v, wt in edges:
        g[u].append((v, wt))

    return g

def dijkstra(g, s):
    dist = {v: inf for v in g}
    dist[s] = 0
    pq = [(0, s)]

    while pq:
        du, u = heappop(pq)
        if du > dist[u]:
            continue

        for v, uv in g[u]:
            if dist[v] > du + uv:
                dist[v] = du + uv
                heappush(pq, (dist[v], v))

    return dist

def delay_time(times, n, k) -> int:
    g = graph(n, times)
    dist = dijkstra(g, k)
    delay = max(v for u, v in dist.items())
    return -1 if delay == inf else delay

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        return delay_time(times, n, k)
