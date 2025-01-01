"""

1334. Find the City With the Smallest Number of Neighbors at a Threshold Distance
Solved
Medium

There are n cities numbered from 0 to n-1. Given the array edges where edges[i] = [fromi, toi, weighti] represents a bidirectional and weighted edge between cities fromi and toi, and given the integer distanceThreshold.

Return the city with the smallest number of cities that are reachable through some path and whose distance is at most distanceThreshold, If there are multiple such cities, return the city with the greatest number.

Notice that the distance of a path connecting cities i and j is equal to the sum of the edges' weights along that path.


Example 1:

Input: n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4
Output: 3
Explanation: The figure above describes the graph. 
The neighboring cities at a distanceThreshold = 4 for each city are:
City 0 -> [City 1, City 2] 
City 1 -> [City 0, City 2, City 3] 
City 2 -> [City 0, City 1, City 3] 
City 3 -> [City 1, City 2] 
Cities 0 and 3 have 2 neighboring cities at a distanceThreshold = 4, but we have to return city 3 since it has the greatest number.


Example 2:

Input: n = 5, edges = [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]], distanceThreshold = 2
Output: 0
Explanation: The figure above describes the graph. 
The neighboring cities at a distanceThreshold = 2 for each city are:
City 0 -> [City 1] 
City 1 -> [City 0, City 4] 
City 2 -> [City 3, City 4] 
City 3 -> [City 2, City 4]
City 4 -> [City 1, City 2, City 3] 
The city 0 has 1 neighboring city at a distanceThreshold = 2.


Performance with V X Dijkstra

Runtime 130 ms Beats 85.05%
Memory 19.46 MB Beats 5.90%

Time Complexity
O(V^2 log(V))


Performance with Floyd-Warshall

Runtime 379 ms Beats 45.93%
Memory 18.85 MB Beats 26.15%

Time Complexity
O(V^3)


Performance with Johnson

Runtime 340 ms Beats 49.00%
Memory 19.91 MB Beats 5.90%

"""

from heapq import heappush as push, heappop as pop

class Graph:
    def __init__(self, V, es=None):
        self.V, self.Vs = V, range(V)
        self.adj = defaultdict(dict)
        self.es = es if es else []
        for e in self.es: self.add(e)

    def add(self, e):
        u, v, w = e
        self.adj[u][v] = w
        self.adj[v][u] = w


def threshcity(n, es, td):
    def johnson(g):
        def augment(g):
            st = (W := g.V + 1) - 1; h = [0] * W
            g.V = W; g.Vs = range(W)
            for v in g.Vs: g.adj[st][v] = 0

            bd = bellman(g, st)
            for v in g.Vs: h[v] = bd[v]

            for u in g.Vs:
                for v in g.adj[u]: 
                    g.adj[u][v] += h[v] - h[u]

            return g, h

        def bellman(g, s):
            def relax(v, w):
                if dist[w] > (dvw := dist[v] + g.adj[v][w]):
                    dist[w] = dvw

            dist = {v: (0 if v == s else float('inf')) for v in g.Vs}

            for _ in range(g.V):
                for v in g.Vs:
                    for w in g.adj[v]:
                        relax(v, w)

            return dist

        def dijkstra(g, s):
            dist = {v: (0 if v == s else float('inf')) for v in g.Vs}
            pq = [(0, s)]
            while pq:
                du, u = pop(pq)
                if du > dist[u]: continue
                for v in g.adj[u]:
                    if dist[v] > (duv := dist[u] + g.adj[u][v]):
                        dist[v] = duv; push(pq, (duv, v))
            return dist

        g, h = augment(g)
        dists = defaultdict(dict)

        for v in g.Vs: dists[v] = dijkstra(g, v)

        for v in g.Vs:
            for w in g.Vs:
                dists[v][w] = dists[v][w] + h[v] - h[w]

        return dists

    def thresh(dist, s, td):    return sum(1 for v in dist if dist[v] <= td and not v == s)

    def threshs(dists, td):     return {v: thresh(dists[v], v, td) for v in dists}

    return -min((nd, -v) for v, nd in threshs(
                                                johnson(Graph(n, es)), td
                                             ).items())[1]

class Solution:
    def findTheCity(self, n: int, es: List[List[int]], td: int) -> int:
        return threshcity(n, es, td)












