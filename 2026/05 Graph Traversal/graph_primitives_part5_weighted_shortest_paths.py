"""
Graph Primitives — Part 5: Weighted Shortest Paths

LeetCode-style version.

Part 1 covered plain DFS/BFS traversal.
Part 2 covered DFS/BFS with state.
Part 3 covered Union-Find / dynamic connectivity.
Part 4 covered MST / Kruskal / Prim.

Part 5 covers weighted shortest paths.

Core idea:
    BFS is shortest path when every edge costs 1.
    Dijkstra is BFS generalized to non-negative edge weights.
    0-1 BFS is the special fast version when every edge costs 0 or 1.
    Bellman-Ford is relaxation when we cannot use Dijkstra's greedy finalization.
    Floyd-Warshall is all-pairs shortest path for small dense graphs.

Keep it boring and fast for LeetCode.
No generics. No protocols. No type annotations.

Conventions:
    Weighted directed graph:
        g[v] = [(w, wt), ...]

    Weighted undirected graph:
        g[v] = [(w, wt), ...]

    Weighted edge list:
        edges = [[v, w, wt], ...]

Universal shortest-path state:
    dist[v]   = best known cost from source to v
    parent[v] = previous vertex on the best path

Universal relaxation atom:
    if dist[w] > dist[v] + wt:
        dist[w] = dist[v] + wt
        parent[w] = v
"""

from collections import deque
from heapq import heappush, heappop


INF = 10 ** 18
MOD = 10 ** 9 + 7


# ============================================================
# 1. WEIGHTED GRAPH BUILDERS
# ============================================================

"""
Why this primitive exists
-------------------------
Weighted shortest-path problems usually begin by turning an edge list into:

    g[v] = [(w, wt), ...]

Then every algorithm can simply write:

    for w, wt in g[v]:
        ...

That is the level of abstraction we want for LeetCode.
"""


def wdigraph(n, edges):
    g = [[] for _ in range(n)]

    for v, w, wt in edges:
        g[v].append((w, wt))

    return g



def wgraph(n, edges):
    g = [[] for _ in range(n)]

    for v, w, wt in edges:
        g[v].append((w, wt))
        g[w].append((v, wt))

    return g


# ============================================================
# 2. RELAXATION ATOM
# ============================================================

"""
Why this primitive exists
-------------------------
Shortest-path algorithms are built from one local improvement operation:

    Can path src -> ... -> v -> w improve the current best path to w?

If yes, update dist[w] and remember parent[w].

This builds up to:
    Dijkstra
    Bellman-Ford
    DAG shortest path
    0-1 BFS
    shortest-path counting
"""


def relax(dist, parent, v, w, wt):
    if dist[w] > dist[v] + wt:
        dist[w] = dist[v] + wt
        parent[w] = v
        return True

    return False


# ============================================================
# 3. DIJKSTRA — NON-NEGATIVE WEIGHTS
# ============================================================

"""
Why this primitive exists
-------------------------
Dijkstra is the default weighted shortest-path primitive for LeetCode.

Use it when:
    weights are non-negative
    graph is weighted
    we need shortest cost from one source

Mental model:
    BFS uses a queue because all next edges cost 1.
    Dijkstra uses a min-heap because different paths have different costs.

Core invariant:
    When a node is popped with cost == dist[node], that is the best known
    finalized distance for that node.

Stale heap entries:
    We may push the same vertex multiple times.
    When we pop an old worse distance, skip it.

Problems:
    743. Network Delay Time
    505. The Maze II
    1514. Path with Maximum Probability, with max-prob variant
    1976. Number of Ways to Arrive at Destination
    2577. Minimum Time to Visit a Cell In a Grid
    3123. Find Edges in Shortest Paths
"""


def dijkstra(g, src):
    dist = [INF] * len(g)
    dist[src] = 0
    heap = [(0, src)]

    while heap:
        d, v = heappop(heap)

        if d != dist[v]:
            continue

        for w, wt in g[v]:
            nd = d + wt

            if nd < dist[w]:
                dist[w] = nd
                heappush(heap, (nd, w))

    return dist


# Same skeleton, but also remembers the actual shortest-path tree.


def dijkstra_parent(g, src):
    dist = [INF] * len(g)
    parent = [-1] * len(g)
    dist[src] = 0
    parent[src] = src
    heap = [(0, src)]

    while heap:
        d, v = heappop(heap)

        if d != dist[v]:
            continue

        for w, wt in g[v]:
            if dist[w] > d + wt:
                dist[w] = d + wt
                parent[w] = v
                heappush(heap, (dist[w], w))

    return dist, parent



def path(parent, dst):
    if parent[dst] == -1:
        return []

    ans = []

    while parent[dst] != dst:
        ans.append(dst)
        dst = parent[dst]

    ans.append(dst)
    return ans[::-1]


# ============================================================
# 4. PROBLEM 743 — NETWORK DELAY TIME
# ============================================================

"""
Problem 743. Network Delay Time

Reduction:
    Signal starts at k.
    Directed weighted edges represent travel time.
    All nodes receive signal when the farthest reachable node receives it.

Composition:
    weighted directed graph
    + Dijkstra from k
    + max distance
    -> answer

Trap:
    Input nodes are 1-indexed.
"""


class Solution743:
    def networkDelayTime(self, times, n, k):
        edges = []

        for v, w, wt in times:
            edges.append([v - 1, w - 1, wt])

        dist = dijkstra(wdigraph(n, edges), k - 1)
        ans = max(dist)

        return -1 if ans == INF else ans


# ============================================================
# 5. DIJKSTRA VARIANT — COUNT SHORTEST PATHS
# ============================================================

"""
Why this primitive exists
-------------------------
Sometimes shortest-path problems ask:

    What is the minimum distance?
    How many different shortest paths achieve it?

Add one more array:
    ways[v] = number of shortest paths from source to v

Relaxation rules:
    strictly better path:
        dist[w] = new distance
        ways[w] = ways[v]

    equally good path:
        ways[w] += ways[v]

Problem:
    1976. Number of Ways to Arrive at Destination
"""


def dijkstra_count_paths(g, src):
    dist = [INF] * len(g)
    ways = [0] * len(g)
    dist[src] = 0
    ways[src] = 1
    heap = [(0, src)]

    while heap:
        d, v = heappop(heap)

        if d != dist[v]:
            continue

        for w, wt in g[v]:
            nd = d + wt

            if nd < dist[w]:
                dist[w] = nd
                ways[w] = ways[v]
                heappush(heap, (nd, w))

            elif nd == dist[w]:
                ways[w] = (ways[w] + ways[v]) % MOD

    return dist, ways


class Solution1976:
    def countPaths(self, n, roads):
        dist, ways = dijkstra_count_paths(wgraph(n, roads), 0)
        return ways[n - 1]


# ============================================================
# 6. DIJKSTRA VARIANT — MAXIMUM PROBABILITY PATH
# ============================================================

"""
Problem 1514. Path with Maximum Probability

Reduction:
    Edge weights are probabilities.
    Path score is product of probabilities.
    We want maximum product path.

This is Dijkstra-shaped, but the comparison is reversed:
    normal Dijkstra minimizes total cost
    probability Dijkstra maximizes product

Use a max-heap by pushing negative probabilities.

Composition:
    weighted undirected graph with probability weights
    + max-heap frontier
    -> best probability
"""


def max_probability(g, src):
    prob = [0] * len(g)
    prob[src] = 1
    heap = [(-1, src)]

    while heap:
        p, v = heappop(heap)
        p = -p

        if p != prob[v]:
            continue

        for w, wt in g[v]:
            np = p * wt

            if np > prob[w]:
                prob[w] = np
                heappush(heap, (-np, w))

    return prob


class Solution1514:
    def maxProbability(self, n, edges, succProb, start, end):
        weighted = []

        for i, (v, w) in enumerate(edges):
            weighted.append([v, w, succProb[i]])

        return max_probability(wgraph(n, weighted), start)[end]


# ============================================================
# 7. 0-1 BFS
# ============================================================

"""
Why this primitive exists
-------------------------
If every edge weight is either 0 or 1, Dijkstra works but is overkill.

0-1 BFS uses a deque:
    cost 0 edge -> push left
    cost 1 edge -> push right

Mental model:
    This preserves the same ordering idea as Dijkstra without a heap.

Use it when:
    weights are only 0 and 1
    grid movement has free moves and paid moves
    problem asks minimum changes / minimum obstacles / minimum reversals

Problems:
    1368. Minimum Cost to Make at Least One Valid Path in a Grid
    2290. Minimum Obstacle Removal to Reach Corner
    3650. Minimum Cost Path with Edge Reversals
"""


def zero_one_bfs(g, src):
    dist = [INF] * len(g)
    dist[src] = 0
    dq = deque([src])

    while dq:
        v = dq.popleft()

        for w, wt in g[v]:
            nd = dist[v] + wt

            if nd < dist[w]:
                dist[w] = nd

                if wt == 0:
                    dq.appendleft(w)
                else:
                    dq.append(w)

    return dist


# ============================================================
# 8. PROBLEM 1368 — MINIMUM COST TO MAKE VALID PATH IN GRID
# ============================================================

"""
Problem 1368. Minimum Cost to Make at Least One Valid Path in a Grid

Grid encoding:
    1 = right
    2 = left
    3 = down
    4 = up

Reduction:
    From each cell, moving in the cell's arrow direction costs 0.
    Moving in any other direction costs 1 because we must change that arrow.

So the grid becomes a 0-1 weighted graph.

Composition:
    cell id = r * cols + c
    + 0-1 weighted neighbors
    + zero_one_bfs
    -> minimum modification cost
"""


GRID_DIRS_1368 = [None, (0, 1), (0, -1), (1, 0), (-1, 0)]


def inside_rc(rows, cols, r, c):
    return 0 <= r < rows and 0 <= c < cols


class Solution1368:
    def minCost(self, grid):
        rows = len(grid)
        cols = len(grid[0])
        n = rows * cols
        g = [[] for _ in range(n)]

        for r in range(rows):
            for c in range(cols):
                v = r * cols + c

                for d in range(1, 5):
                    dr, dc = GRID_DIRS_1368[d]
                    nr, nc = r + dr, c + dc

                    if inside_rc(rows, cols, nr, nc):
                        w = nr * cols + nc
                        cost = 0 if grid[r][c] == d else 1
                        g[v].append((w, cost))

        return zero_one_bfs(g, 0)[n - 1]


# ============================================================
# 9. PROBLEM 2290 — MINIMUM OBSTACLE REMOVAL
# ============================================================

"""
Problem 2290. Minimum Obstacle Removal to Reach Corner

Reduction:
    Moving into an empty cell costs 0.
    Moving into an obstacle cell costs 1 because we remove it.

Again this is 0-1 BFS.
"""


DIRS4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Solution2290:
    def minimumObstacles(self, grid):
        rows = len(grid)
        cols = len(grid[0])
        n = rows * cols
        g = [[] for _ in range(n)]

        for r in range(rows):
            for c in range(cols):
                v = r * cols + c

                for dr, dc in DIRS4:
                    nr, nc = r + dr, c + dc

                    if inside_rc(rows, cols, nr, nc):
                        w = nr * cols + nc
                        g[v].append((w, grid[nr][nc]))

        return zero_one_bfs(g, 0)[n - 1]


# ============================================================
# 10. BELLMAN-FORD / K-EDGE RELAXATION
# ============================================================

"""
Why this primitive exists
-------------------------
Dijkstra needs non-negative weights and greedily finalizes nodes.
Bellman-Ford does not greedily finalize nodes.
It repeatedly relaxes edges.

Useful when:
    weights may be negative
    we need shortest path with at most k edges
    graph is naturally given as an edge list

Core invariant:
    After i passes, dist[v] is the best distance using at most i edges.

For LeetCode, the most common version is the bounded version:
    cheapest flight with at most k stops
    = at most k + 1 edges

Problem:
    787. Cheapest Flights Within K Stops
"""


def bellman_ford(n, edges, src):
    dist = [INF] * n
    dist[src] = 0

    for _ in range(n - 1):
        changed = False
        new = dist[:]

        for v, w, wt in edges:
            if dist[v] != INF and new[w] > dist[v] + wt:
                new[w] = dist[v] + wt
                changed = True

        dist = new

        if not changed:
            break

    return dist



def shortest_with_k_edges(n, edges, src, max_edges):
    dist = [INF] * n
    dist[src] = 0

    for _ in range(max_edges):
        new = dist[:]

        for v, w, wt in edges:
            if dist[v] != INF and new[w] > dist[v] + wt:
                new[w] = dist[v] + wt

        dist = new

    return dist


class Solution787:
    def findCheapestPrice(self, n, flights, src, dst, k):
        dist = shortest_with_k_edges(n, flights, src, k + 1)
        return -1 if dist[dst] == INF else dist[dst]


# ============================================================
# 11. FLOYD-WARSHALL — ALL PAIRS SHORTEST PATHS
# ============================================================

"""
Why this primitive exists
-------------------------
Floyd-Warshall solves all-pairs shortest paths.

Use it when:
    n is small
    graph may be dense
    many source-target shortest path queries are needed

Mental model:
    Gradually allow more intermediate vertices.

Core transition:
    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

Problems:
    1334. Find the City With Smallest Number of Neighbors at Threshold
    2976. Minimum Cost to Convert String I
"""


def floyd_warshall(n, edges):
    dist = [[INF] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for v, w, wt in edges:
        dist[v][w] = min(dist[v][w], wt)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


# ============================================================
# 12. PROBLEM 2976 — MINIMUM COST TO CONVERT STRING I
# ============================================================

"""
Problem 2976. Minimum Cost to Convert String I

Reduction:
    Characters are graph nodes.
    original[i] -> changed[i] has conversion cost cost[i].
    We need cheapest conversion for each source character to target character.

Alphabet size is only 26.
So Floyd-Warshall is perfect.
"""


class Solution2976:
    def minimumCost(self, source, target, original, changed, cost):
        edges = []

        for a, b, wt in zip(original, changed, cost):
            edges.append([ord(a) - ord('a'), ord(b) - ord('a'), wt])

        dist = floyd_warshall(26, edges)
        total = 0

        for a, b in zip(source, target):
            v = ord(a) - ord('a')
            w = ord(b) - ord('a')

            if dist[v][w] == INF:
                return -1

            total += dist[v][w]

        return total


# ============================================================
# 13. PROBLEM 1334 — FIND CITY WITH SMALLEST REACHABLE COUNT
# ============================================================

"""
Problem 1334. Find the City With the Smallest Number of Neighbors at a Threshold Distance

Reduction:
    We need shortest distance between every pair of cities.
    Then count how many cities are within threshold from each city.

Composition:
    undirected weighted edges converted to two directed edges
    + Floyd-Warshall
    + count threshold neighbors
    -> answer

Tie rule:
    If counts tie, return the greatest city index.
"""


class Solution1334:
    def findTheCity(self, n, edges, distanceThreshold):
        directed = []

        for v, w, wt in edges:
            directed.append([v, w, wt])
            directed.append([w, v, wt])

        dist = floyd_warshall(n, directed)
        best_city = -1
        best_count = INF

        for v in range(n):
            count = 0

            for w in range(n):
                if v != w and dist[v][w] <= distanceThreshold:
                    count += 1

            if count <= best_count:
                best_count = count
                best_city = v

        return best_city


# ============================================================
# 14. PRACTICE ORDER FOR PART 5
# ============================================================

"""
Practice order
--------------
1. relax
2. dijkstra
3. dijkstra_parent + path
4. network delay time
5. dijkstra_count_paths
6. max_probability variant
7. zero_one_bfs
8. grid-to-0-1-graph reductions
9. bounded Bellman-Ford for k stops
10. Floyd-Warshall for small all-pairs problems

Decision guide
--------------
Unweighted shortest path:
    BFS

Weights are 0/1:
    0-1 BFS

Weights are non-negative:
    Dijkstra

At most k edges / k stops:
    bounded Bellman-Ford

Negative weights but no negative cycles:
    Bellman-Ford

All-pairs and n is small:
    Floyd-Warshall

All-pairs and n is large with non-negative weights:
    run Dijkstra from each source, or use a more advanced approach

Main traps
----------
1. Using BFS on weighted graph.
2. Using Dijkstra with negative weights.
3. Forgetting stale heap entries.
4. Updating dist in-place for k-stop Bellman-Ford.
5. Confusing stops with edges:
       k stops means at most k + 1 edges.
6. For 0-1 BFS:
       cost 0 -> appendleft
       cost 1 -> append
"""
