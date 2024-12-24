"""

1976. Number of Ways to Arrive at Destination
Medium
Topics
Companies
Hint
You are in a city that consists of n intersections numbered from 0 to n - 1 with bi-directional roads between some intersections. The inputs are generated such that you can reach any intersection from any other intersection and that there is at most one road between any two intersections.

You are given an integer n and a 2D integer array roads where roads[i] = [ui, vi, timei] means that there is a road between intersections ui and vi that takes timei minutes to travel. You want to know in how many ways you can travel from intersection 0 to intersection n - 1 in the shortest amount of time.

Return the number of ways you can arrive at your destination in the shortest amount of time. Since the answer may be large, return it modulo 109 + 7.

 

Example 1:


Input: n = 7, roads = [[0,6,7],[0,1,2],[1,2,3],[1,3,3],[6,3,3],[3,5,1],[6,5,1],[2,5,1],[0,4,5],[4,6,2]]
Output: 4
Explanation: The shortest amount of time it takes to go from intersection 0 to intersection 6 is 7 minutes.
The four ways to get there in 7 minutes are:
- 0 ➝ 6
- 0 ➝ 4 ➝ 6
- 0 ➝ 1 ➝ 2 ➝ 5 ➝ 6
- 0 ➝ 1 ➝ 3 ➝ 5 ➝ 6
Example 2:

Input: n = 2, roads = [[1,0,10]]
Output: 1
Explanation: There is only one way to go from intersection 0 to intersection 1, and it takes 10 minutes.
 

Constraints:

1 <= n <= 200
n - 1 <= roads.length <= n * (n - 1) / 2
roads[i].length == 3
0 <= ui, vi <= n - 1
1 <= timei <= 109
ui != vi
There is at most one road connecting any two intersections.
You can reach any intersection from any other intersection.

"""

from collections import defaultdict

class Graph:
    def __init__(self, V, es=None):
        self.V = V; self.adj = defaultdict(dict)
        self.es = es if es else []; self.connect()

    def add(self, e):
        self.adj[e[0]][e[1]] = e[2]
        self.adj[e[1]][e[0]] = e[2]
    def connect(self):
        for e in self.es: self.add(e)

def dijkstra(g, s):
    dist = {v: (0 if v == s else float('inf')) for v in range(g.V)}
    parents = defaultdict(list); hs = IndexHeap(dist)
    while hs:
        u, du = hs.pop(); dist[u] = du
        for v in g.adj[u]:
            if dist[v] >= (duv := dist[u] + g.adj[u][v]):
                if dist[v] == duv:
                    parents[v].append(u)
                else:
                    parents[v] = [u]
                dist[v] = duv
                hs.update(v, dist[v])
    return dist, parents

def paths(n, es):
    def num(ps, s, t):
        if t == s: return 1
        return sum(num(ps, s, v) for v in ps[t])
    _, ps = dijkstra(Graph(n, es), 0)
    return num(ps, 0, n - 1)
























