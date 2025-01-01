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
 

Constraints:

2 <= n <= 100
1 <= edges.length <= n * (n - 1) / 2
edges[i].length == 3
0 <= fromi < toi < n
1 <= weighti, distanceThreshold <= 10^4
All pairs (fromi, toi) are distinct.


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



"""






def threshcity(n, es, td):
    def floydwarshall(dist):
        for k in range(n := len(dist)):
            for i in range(n):
                for j in range(n):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        return dist

    def thresh(dist, td):
        return [sum(1 for w in range(n) if dist[v][w] <= td and not v == w) for v in range(n)]

    dist = [[float('inf')] * n for _ in range(n)]
    for u, v, wt in es:
        dist[u][v] = wt; dist[v][u] = wt

    return -min((nd, -v) for v, nd in enumerate(thresh(floydwarshall(dist), td)))[1]


class Solution:
    def findTheCity(self, n: int, es: List[List[int]], td: int) -> int:
        return threshcity(n, es, td)















