"""
Graph Primitives — Part 1: Core DFS / BFS / Grid Traversal

LeetCode-style version.

Design rule:
    Keep the code boring and fast to write.

Explicit unweighted graph:
    g[v] = [w1, w2, w3]
    for w in g[v]:
        ...

Explicit weighted graph:
    g[v] = [(w1, wt1), (w2, wt2)]
    for w, wt in g[v]:
        ...

Grid graph:
    Do not build adjacency lists.
    Use (r, c) coordinates and neighbors4 / neighbors8.

This file follows the primitive style:
    primitive -> why it exists -> how it composes -> problem solution skeletons
"""

from collections import deque


# ============================================================
# 0. GRAPH REPRESENTATION PRIMITIVES
# ============================================================

"""
Why these primitives exist
--------------------------
Most LeetCode graph problems start with an edge list.
Before DFS/BFS/Dijkstra/DSU can do anything, we need a cheap adjacency list.

The key convention:
    unweighted: for w in g[v]
    weighted:   for w, wt in g[v]

No wrapper classes. No Mapping. No Callable. No graph_neighbors adapter.
"""


def graph(n, edges):
    g = [[] for _ in range(n)]

    for v, w in edges:
        g[v].append(w)
        g[w].append(v)

    return g



def digraph(n, edges):
    g = [[] for _ in range(n)]

    for v, w in edges:
        g[v].append(w)

    return g



def wgraph(n, edges):
    g = [[] for _ in range(n)]

    for v, w, wt in edges:
        g[v].append((w, wt))
        g[w].append((v, wt))

    return g



def wdigraph(n, edges):
    g = [[] for _ in range(n)]

    for v, w, wt in edges:
        g[v].append((w, wt))

    return g


# Composition chain:
#     edge list -> graph / digraph -> DFS / BFS / topo / Dijkstra later
#
# Representative problems:
#     1971. Find if Path Exists in Graph
#     323. Number of Connected Components in an Undirected Graph
#     743. Network Delay Time       # weighted directed graph, later Dijkstra
#     1584. Min Cost to Connect All Points  # weighted complete graph / MST later


# ============================================================
# 1. DFS REACHABILITY PRIMITIVES
# ============================================================

"""
Why this primitive exists
-------------------------
DFS answers the most basic graph question:
    What can I reach from this start node?

Core invariant:
    Once v is added to seen, every recursive call from v explores only unseen neighbors.

This builds up to:
    reachable set
    path existence
    connected components
    grid flood fill
"""


def dfs(v, g, seen):
    seen.add(v)

    for w in g[v]:
        if w not in seen:
            dfs(w, g, seen)



def reachable(g, start):
    seen = set()
    dfs(start, g, seen)
    return seen



def has_path(g, src, dst):
    return dst in reachable(g, src)


# Problem 1971. Find if Path Exists in Graph
# Reduction:
#     Build an undirected graph and ask whether dst is reachable from src.


class Solution1971:
    def validPath(self, n, edges, source, destination):
        g = graph(n, edges)
        return has_path(g, source, destination)


# ============================================================
# 2. CONNECTED COMPONENT PRIMITIVES
# ============================================================

"""
Why this primitive exists
-------------------------
A connected component is exactly what one DFS collects from an unvisited node.

We keep the group.append() style because it is visually clean:
    group = []
    collect(v, g, seen, group)
    groups.append(group)

Core invariant:
    collect(v, ...) appends exactly all nodes in v's component that were unseen
    before this DFS started.

This builds up to:
    number of components
    component sizes
    unreachable pairs
    complete component checks
"""


def collect(v, g, seen, group):
    seen.add(v)
    group.append(v)

    for w in g[v]:
        if w not in seen:
            collect(w, g, seen, group)



def components(g):
    seen = set()
    groups = []

    for v in range(len(g)):
        if v not in seen:
            group = []
            collect(v, g, seen, group)
            groups.append(group)

    return groups



def component_count(g):
    return len(components(g))


# Problem 323. Number of Connected Components in an Undirected Graph
# Reduction:
#     Each DFS from an unseen vertex gives one component.


class Solution323:
    def countComponents(self, n, edges):
        return component_count(graph(n, edges))


# Problem 2316. Count Unreachable Pairs of Nodes in an Undirected Graph
# Reduction:
#     Two nodes are unreachable iff they are in different components.
#     If component sizes are s1, s2, ..., answer is sum of prior_size * current_size.


class Solution2316:
    def countPairs(self, n, edges):
        total = 0
        seen = 0

        for group in components(graph(n, edges)):
            total += seen * len(group)
            seen += len(group)

        return total


# ============================================================
# 3. BFS DISTANCE / PARENT PRIMITIVES
# ============================================================

"""
Why this primitive exists
-------------------------
BFS is shortest path when every edge has weight 1.

Core invariant:
    The first time a node receives dist[w], that is the minimum edge-count
    distance from the start.

This builds up to:
    shortest unweighted paths
    level order traversal
    parent path reconstruction
    multi-source wave expansion
"""


def bfs_dist(g, start):
    dist = [-1] * len(g)
    q = deque([start])
    dist[start] = 0

    while q:
        v = q.popleft()

        for w in g[v]:
            if dist[w] == -1:
                dist[w] = dist[v] + 1
                q.append(w)

    return dist



def bfs_parent(g, start):
    parent = [-1] * len(g)
    q = deque([start])
    parent[start] = start

    while q:
        v = q.popleft()

        for w in g[v]:
            if parent[w] == -1:
                parent[w] = v
                q.append(w)

    return parent



def path(parent, dst):
    if parent[dst] == -1:
        return []

    ans = []

    while parent[dst] != dst:
        ans.append(dst)
        dst = parent[dst]

    ans.append(dst)
    return ans[::-1]



def shortest_path(g, src, dst):
    return path(bfs_parent(g, src), dst)


# Problem pattern:
#     BFS parent is needed when the question asks for the actual path.
#     BFS distance is enough when the question asks only for the length.


class Solution1971BFS:
    def validPath(self, n, edges, source, destination):
        return bfs_dist(graph(n, edges), source)[destination] != -1


# ============================================================
# 4. MULTI-SOURCE BFS PRIMITIVE
# ============================================================

"""
Why this primitive exists
-------------------------
Some BFS problems have many starting points:
    all gates
    all rotten oranges
    all zeros
    all land cells

Core invariant:
    Every source starts at distance 0.
    BFS then computes distance to the nearest source.

This builds up to:
    rotting/spreading problems
    nearest-source distance problems
    boundary escape/enclosure problems
"""

def multi_bfs_dist(g, starts):
    dist = [-1] * len(g)
    q = deque()

    for s in starts:
        dist[s] = 0
        q.append(s)

    while q:
        v = q.popleft()

        for w in g[v]:
            if dist[w] == -1:
                dist[w] = dist[v] + 1
                q.append(w)

    return dist


# Representative problems:
#     286. Walls and Gates
#     542. 01 Matrix
#     994. Rotting Oranges
#     1162. As Far from Land as Possible
#     1765. Map of Highest Peak


# ============================================================
# 5. GRID GRAPH PRIMITIVES
# ============================================================

"""
Why this primitive exists
-------------------------
A grid is already a graph:
    node = (r, c)
    edge = legal move to neighbor cell

For LeetCode, do not build an adjacency list for grids.
Use coordinate helpers.

Core distinction:
    DFS grid = region/component discovery
    BFS grid = shortest distance/wave propagation
"""


DIRS4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]

DIRS8 = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (1, -1), (-1, 1), (-1, -1),
]



def inside(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])



def neighbors4(grid, r, c):
    for dr, dc in DIRS4:
        nr, nc = r + dr, c + dc

        if inside(grid, nr, nc):
            yield nr, nc



def neighbors8(grid, r, c):
    for dr, dc in DIRS8:
        nr, nc = r + dr, c + dc

        if inside(grid, nr, nc):
            yield nr, nc


# ============================================================
# 6. GRID DFS / ISLAND COMPONENT PRIMITIVES
# ============================================================

"""
Why this primitive exists
-------------------------
Island problems are connected-component problems on a grid.

Primitive:
    collect all cells connected to one land cell.

Core invariant:
    collect_land(...) appends exactly the current island's cells to group.

This builds up to:
    number of islands
    max area of island
    closed islands
    enclaves
    sub-islands
"""


def collect_land(grid, r, c, seen, group, land):
    seen.add((r, c))
    group.append((r, c))

    for nr, nc in neighbors4(grid, r, c):
        if (nr, nc) not in seen and grid[nr][nc] == land:
            collect_land(grid, nr, nc, seen, group, land)



def island_groups(grid, land=1):
    seen = set()
    groups = []

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == land and (r, c) not in seen:
                group = []
                collect_land(grid, r, c, seen, group, land)
                groups.append(group)

    return groups


# Problem 200. Number of Islands
# Reduction:
#     number of islands = number of connected land components
# Note:
#     LC 200 uses string "1".


class Solution200:
    def numIslands(self, grid):
        return len(island_groups(grid, "1"))


# Problem 695. Max Area of Island
# Reduction:
#     area of island = size of connected land component
# Note:
#     LC 695 uses integer 1.


class Solution695:
    def maxAreaOfIsland(self, grid):
        return max((len(group) for group in island_groups(grid, 1)), default=0)


# Problem 1020. Number of Enclaves
# Reduction:
#     First remove/mark all land connected to boundary.
#     Remaining land cells are enclaves.


class Solution1020:
    def numEnclaves(self, grid):
        m, n = len(grid), len(grid[0])
        seen = set()

        def mark(r, c):
            if not inside(grid, r, c) or grid[r][c] == 0 or (r, c) in seen:
                return

            seen.add((r, c))

            for nr, nc in neighbors4(grid, r, c):
                mark(nr, nc)

        for r in range(m):
            mark(r, 0)
            mark(r, n - 1)

        for c in range(n):
            mark(0, c)
            mark(m - 1, c)

        return sum(
            grid[r][c] == 1 and (r, c) not in seen
            for r in range(m)
            for c in range(n)
        )


# ============================================================
# 7. GRID BFS DISTANCE PRIMITIVES
# ============================================================

"""
Why this primitive exists
-------------------------
Grid BFS solves shortest movement / spreading problems.

Core invariant:
    The first time dist[r][c] is assigned, it is the shortest distance from
    the start/source set under the chosen move rules.

This builds up to:
    shortest path in binary matrix
    nearest exit
    rotting oranges
    01 matrix
    walls and gates
"""


def grid_dist4(grid, start):
    sr, sc = start
    dist = [[-1] * len(grid[0]) for _ in range(len(grid))]
    q = deque([(sr, sc)])
    dist[sr][sc] = 0

    while q:
        r, c = q.popleft()

        for nr, nc in neighbors4(grid, r, c):
            if dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))

    return dist



def multi_grid_dist4(grid, starts):
    dist = [[-1] * len(grid[0]) for _ in range(len(grid))]
    q = deque()

    for r, c in starts:
        dist[r][c] = 0
        q.append((r, c))

    while q:
        r, c = q.popleft()

        for nr, nc in neighbors4(grid, r, c):
            if dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))

    return dist


# Problem 1091. Shortest Path in Binary Matrix
# Reduction:
#     BFS on grid with 8-direction movement.
#     Only cells with 0 are passable.


class Solution1091:
    def shortestPathBinaryMatrix(self, grid):
        n = len(grid)

        if grid[0][0] or grid[n - 1][n - 1]:
            return -1

        dist = [[-1] * n for _ in range(n)]
        q = deque([(0, 0)])
        dist[0][0] = 1

        while q:
            r, c = q.popleft()

            if r == n - 1 and c == n - 1:
                return dist[r][c]

            for nr, nc in neighbors8(grid, r, c):
                if grid[nr][nc] == 0 and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))

        return -1


# Problem 994. Rotting Oranges
# Reduction:
#     Multi-source BFS.
#     All initially rotten oranges start at minute 0.
#     Fresh oranges reached later rot at their BFS distance.


class Solution994:
    def orangesRotting(self, grid):
        m, n = len(grid), len(grid[0])
        q = deque()
        fresh = 0

        for r in range(m):
            for c in range(n):
                if grid[r][c] == 2:
                    q.append((r, c, 0))
                elif grid[r][c] == 1:
                    fresh += 1

        minutes = 0

        while q:
            r, c, minutes = q.popleft()

            for nr, nc in neighbors4(grid, r, c):
                if grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc, minutes + 1))

        return minutes if fresh == 0 else -1


# ============================================================
# 8. PRACTICE ORDER FOR THIS FILE
# ============================================================

"""
Drill order
-----------
1. graph / digraph
2. dfs / reachable / has_path
3. collect / components
4. bfs_dist
5. bfs_parent / path
6. multi_bfs_dist
7. inside / neighbors4 / neighbors8
8. collect_land / island_groups
9. grid BFS with obstacle rules written directly inside the solution

Core LeetCode set
-----------------
1971. Find if Path Exists in Graph
323. Number of Connected Components in an Undirected Graph
2316. Count Unreachable Pairs of Nodes in an Undirected Graph
200. Number of Islands
695. Max Area of Island
1020. Number of Enclaves
1091. Shortest Path in Binary Matrix
994. Rotting Oranges

What mastery looks like
-----------------------
You should be able to write these from memory:
    for w in g[v]
    if w not in seen: dfs(w)
    if dist[w] == -1: dist[w] = dist[v] + 1
    for nr, nc in neighbors4(grid, r, c)

No extra abstraction needed.
"""
