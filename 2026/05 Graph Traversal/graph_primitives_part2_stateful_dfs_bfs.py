"""
Graph Primitives — Part 2: Stateful DFS / BFS

LeetCode-style version.

Part 1 covered plain traversal:
    dfs reachability
    connected components
    bfs distance
    multi-source bfs
    grid flood fill

Part 2 adds the important missing layer:
    traversal + state

The state is usually one of:
    parent          # undirected cycle / path reconstruction
    color           # directed cycle / bipartite / safe states
    order           # postorder / topological order
    indegree        # Kahn BFS topo
    path            # DFS backtracking
    boundary seen   # grid regions connected to border/ocean

Design rule:
    Keep code boring and fast to write.
    No graph classes. No Callable. No TypeVar. No Mapping.

Graph convention:
    g[v] = [w1, w2, w3]
    for w in g[v]:
        ...
"""

from collections import deque

# ============================================================
# 0. BASIC BUILDERS USED BY THIS FILE
# ============================================================

"""
Why these primitives exist
--------------------------
Part 2 still starts from the same simple graph representation.
Most stateful graph problems need either an undirected graph or a digraph.
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



def reverse_graph(g):
    rev = [[] for _ in range(len(g))]

    for v in range(len(g)):
        for w in g[v]:
            rev[w].append(v)

    return rev


# ============================================================
# 1. UNDIRECTED CYCLE DETECTION: DFS + PARENT
# ============================================================

"""
Why this primitive exists
-------------------------
In an undirected graph, every edge appears twice:
    v -> w
    w -> v

So when DFS at v sees an already-seen neighbor w, that is NOT automatically
cycle evidence. It may just be the edge back to v's parent.

Core state:
    parent

Core invariant:
    If DFS sees a visited neighbor that is not the parent, there is a cycle.

This builds up to:
    graph valid tree
    cycle checks in undirected graphs
    tree recognition
"""


def has_cycle_undirected(g):
    seen = set()

    def dfs(v, parent):
        seen.add(v)

        for w in g[v]:
            if w == parent:
                continue

            if w in seen or dfs(w, v):
                return True

        return False

    for v in range(len(g)):
        if v not in seen and dfs(v, -1):
            return True

    return False



def is_connected(g):
    if not g:
        return True

    seen = set()

    def dfs(v):
        seen.add(v)

        for w in g[v]:
            if w not in seen:
                dfs(w)

    dfs(0)
    return len(seen) == len(g)


# Problem 261. Graph Valid Tree
# Reduction:
#     A graph is a tree iff it is connected and acyclic.
#     Equivalently for n nodes: exactly n - 1 edges and connected.


class Solution261:
    def validTree(self, n, edges):
        return len(edges) == n - 1 and is_connected(graph(n, edges))


# ============================================================
# 2. DIRECTED CYCLE DETECTION: DFS COLOR STATE
# ============================================================

"""
Why this primitive exists
-------------------------
Directed cycles are different from undirected cycles.
The important question is not just "have I seen this node before?"
It is:
    Is this node currently in my recursion stack?

Core state:
    color[v]

Meaning:
    0 = unvisited
    1 = visiting / currently on recursion stack
    2 = done / fully processed

Core invariant:
    edge to color 1 means a directed cycle.

This builds up to:
    course schedule
    eventual safe states
    topological sort validation
"""


def has_cycle_directed(g):
    color = [0] * len(g)

    def dfs(v):
        color[v] = 1

        for w in g[v]:
            if color[w] == 1:
                return True
            if color[w] == 0 and dfs(w):
                return True

        color[v] = 2
        return False

    for v in range(len(g)):
        if color[v] == 0 and dfs(v):
            return True

    return False


# Problem 207. Course Schedule
# Reduction:
#     Courses form a dependency digraph.
#     Can finish all courses iff there is no directed cycle.
#
# LeetCode gives prerequisite pair [a, b] meaning:
#     to take a, first take b
# So edge is:
#     b -> a


class Solution207DFS:
    def canFinish(self, n, prerequisites):
        edges = [[b, a] for a, b in prerequisites]
        return not has_cycle_directed(digraph(n, edges))


# ============================================================
# 3. DFS TOPOLOGICAL SORT: POSTORDER / REVERSE POSTORDER
# ============================================================

"""
Why this primitive exists
-------------------------
Topological order is dependency-safe order.
For every edge v -> w, v must appear before w.

DFS rule:
    append node after all children are processed
    reverse that postorder

Core state:
    color for cycle detection
    order for postorder

Core invariant:
    In a DAG, reverse DFS postorder is a valid topological order.

This builds up to:
    course order
    alien dictionary
    DAG dynamic programming
    longest / shortest path in DAG later
"""


def topo_dfs(g):
    color = [0] * len(g)
    order = []

    def dfs(v):
        color[v] = 1

        for w in g[v]:
            if color[w] == 1:
                return False
            if color[w] == 0 and not dfs(w):
                return False

        color[v] = 2
        order.append(v)
        return True

    for v in range(len(g)):
        if color[v] == 0 and not dfs(v):
            return []

    return order[::-1]


# Problem 210. Course Schedule II
# Reduction:
#     Return any topological order of the course dependency graph.


class Solution210DFS:
    def findOrder(self, n, prerequisites):
        edges = [[b, a] for a, b in prerequisites]
        return topo_dfs(digraph(n, edges))


# ============================================================
# 4. KAHN TOPOLOGICAL SORT: BFS + INDEGREE
# ============================================================

"""
Why this primitive exists
-------------------------
Kahn's algorithm is the BFS-style topological sort.

Core state:
    indegree[v] = number of unresolved prerequisites of v

Core invariant:
    A node with indegree 0 is currently safe to process.

This builds up to:
    course schedule
    recipe/supply problems
    layered dependency processing
    detecting whether topo order exists
"""


def topo_kahn(g):
    indeg = [0] * len(g)

    for v in range(len(g)):
        for w in g[v]:
            indeg[w] += 1

    q = deque(v for v in range(len(g)) if indeg[v] == 0)
    order = []

    while q:
        v = q.popleft()
        order.append(v)

        for w in g[v]:
            indeg[w] -= 1

            if indeg[w] == 0:
                q.append(w)

    return order if len(order) == len(g) else []


class Solution207Kahn:
    def canFinish(self, n, prerequisites):
        edges = [[b, a] for a, b in prerequisites]
        return len(topo_kahn(digraph(n, edges))) == n


class Solution210Kahn:
    def findOrder(self, n, prerequisites):
        edges = [[b, a] for a, b in prerequisites]
        return topo_kahn(digraph(n, edges))


# ============================================================
# 5. BIPARTITE CHECKING: BFS/DFS + TWO-COLOR STATE
# ============================================================

"""
Why this primitive exists
-------------------------
A graph is bipartite if every edge connects opposite colors.

Core state:
    color[v] = -1 / 0 / 1

Core invariant:
    If v has color c, every neighbor must have color 1 - c.

This builds up to:
    is graph bipartite
    possible bipartition
    odd-cycle detection in undirected graphs
"""


def is_bipartite(g):
    color = [-1] * len(g)

    for start in range(len(g)):
        if color[start] != -1:
            continue

        q = deque([start])
        color[start] = 0

        while q:
            v = q.popleft()

            for w in g[v]:
                if color[w] == -1:
                    color[w] = 1 - color[v]
                    q.append(w)
                elif color[w] == color[v]:
                    return False

    return True


# Problem 785. Is Graph Bipartite?
# LeetCode already gives adjacency list.


class Solution785:
    def isBipartite(self, graph):
        return is_bipartite(graph)


# Problem 886. Possible Bipartition
# Reduction:
#     People are vertices.
#     Dislike edges mean endpoints must be in opposite groups.
#     This is exactly bipartite checking.
# Note:
#     LeetCode vertices are 1-indexed, so subtract 1.


class Solution886:
    def possibleBipartition(self, n, dislikes):
        edges = [[a - 1, b - 1] for a, b in dislikes]
        return is_bipartite(graph(n, edges))


# ============================================================
# 6. DFS BACKTRACKING PATH STATE
# ============================================================

"""
Why this primitive exists
-------------------------
Sometimes the output is not reachability or distance.
Sometimes the output is every valid path.

Core state:
    path = current recursive path

Core invariant:
    Before dfs(v) returns, path is restored to its caller's state.

This builds up to:
    all paths from source to target
    itinerary-style DFS later
    path enumeration in DAGs
"""


def all_paths(g, src, dst):
    ans = []
    path = []

    def dfs(v):
        path.append(v)

        if v == dst:
            ans.append(path.copy())
        else:
            for w in g[v]:
                dfs(w)

        path.pop()

    dfs(src)
    return ans


# Problem 797. All Paths From Source to Target
# Reduction:
#     Given DAG adjacency list, enumerate every path from 0 to n - 1.


class Solution797:
    def allPathsSourceTarget(self, graph):
        return all_paths(graph, 0, len(graph) - 1)


# ============================================================
# 7. EVENTUAL SAFE STATES: DIRECTED COLOR DFS REUSED
# ============================================================

"""
Why this primitive exists
-------------------------
A node is eventually safe if every path from it eventually ends in a terminal node.
Equivalently:
    it cannot reach a directed cycle.

This reuses color DFS, but the meaning is slightly different:
    color 0 = unknown
    color 1 = currently exploring
    color 2 = proven safe

Core invariant:
    If DFS returns True for v, v is safe and color[v] = 2.
    If DFS touches color 1, a cycle is reachable, so unsafe.

This builds up to:
    eventual safe states
    cycle-avoidance in directed graphs
"""


def eventual_safe_nodes(g):
    color = [0] * len(g)

    def safe(v):
        if color[v] != 0:
            return color[v] == 2

        color[v] = 1

        for w in g[v]:
            if not safe(w):
                return False

        color[v] = 2
        return True

    return [v for v in range(len(g)) if safe(v)]


# Problem 802. Find Eventual Safe States
# Reduction:
#     Safe nodes are exactly nodes that do not reach a directed cycle.


class Solution802:
    def eventualSafeNodes(self, graph):
        return eventual_safe_nodes(graph)


# ============================================================
# 8. BORDER / BOUNDARY GRID STATE
# ============================================================

"""
Why this primitive exists
-------------------------
Some grid problems are not about counting all components.
They are about components connected to a boundary or external source.

Core state:
    seen = cells reachable from boundary / ocean / outside

Core invariant:
    After boundary flood-fill, seen contains exactly the cells that can escape
    or connect to the external source.

This builds up to:
    surrounded regions
    number of enclaves
    closed islands
    pacific atlantic water flow
"""


DIRS4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]



def inside(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])



def neighbors4(grid, r, c):
    for dr, dc in DIRS4:
        nr, nc = r + dr, c + dc

        if inside(grid, nr, nc):
            yield nr, nc



def border_cells(grid):
    m, n = len(grid), len(grid[0])

    for r in range(m):
        yield r, 0
        yield r, n - 1

    for c in range(n):
        yield 0, c
        yield m - 1, c


# Problem 130. Surrounded Regions
# Reduction:
#     O's connected to the border survive.
#     All other O's are surrounded and become X.


class Solution130:
    def solve(self, board):
        m, n = len(board), len(board[0])
        safe = set()

        def mark(r, c):
            if not inside(board, r, c) or board[r][c] != 'O' or (r, c) in safe:
                return

            safe.add((r, c))

            for nr, nc in neighbors4(board, r, c):
                mark(nr, nc)

        for r, c in border_cells(board):
            mark(r, c)

        for r in range(m):
            for c in range(n):
                if board[r][c] == 'O' and (r, c) not in safe:
                    board[r][c] = 'X'


# Problem 417. Pacific Atlantic Water Flow
# Reduction:
#     Instead of asking "can this cell flow to ocean?",
#     reverse the direction:
#         from each ocean, climb to cells with height >= current height.
#     Answer = cells reachable from both oceans.


class Solution417:
    def pacificAtlantic(self, heights):
        m, n = len(heights), len(heights[0])

        pacific = [(0, c) for c in range(n)] + [(r, 0) for r in range(m)]
        atlantic = [(m - 1, c) for c in range(n)] + [(r, n - 1) for r in range(m)]

        def reachable(starts):
            seen = set(starts)
            q = deque(starts)

            while q:
                r, c = q.popleft()

                for nr, nc in neighbors4(heights, r, c):
                    if (nr, nc) not in seen and heights[nr][nc] >= heights[r][c]:
                        seen.add((nr, nc))
                        q.append((nr, nc))

            return seen

        return list(reachable(pacific) & reachable(atlantic))


# ============================================================
# 9. GRID CYCLE DETECTION: DFS + PARENT CELL
# ============================================================

"""
Why this primitive exists
-------------------------
A 2D grid can also have cycles.
This is the grid version of undirected cycle detection.

Core state:
    parent cell
    seen cells

Core invariant:
    Moving back to parent is allowed.
    Reaching any other seen cell of the same character means cycle.

This builds up to:
    Detect Cycles in 2D Grid
"""


def has_grid_cycle(grid):
    seen = set()

    def dfs(r, c, pr, pc, ch):
        seen.add((r, c))

        for nr, nc in neighbors4(grid, r, c):
            if grid[nr][nc] != ch:
                continue

            if (nr, nc) == (pr, pc):
                continue

            if (nr, nc) in seen or dfs(nr, nc, r, c, ch):
                return True

        return False

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) not in seen and dfs(r, c, -1, -1, grid[r][c]):
                return True

    return False


# Problem 1559. Detect Cycles in 2D Grid
# Reduction:
#     Same-character cells form an undirected grid graph.
#     Detect whether any connected component contains a cycle.


class Solution1559:
    def containsCycle(self, grid):
        return has_grid_cycle(grid)


# ============================================================
# 10. PRACTICE ORDER FOR THIS FILE
# ============================================================

"""
Drill order
-----------
1. has_cycle_undirected(g)
2. has_cycle_directed(g)
3. topo_dfs(g)
4. topo_kahn(g)
5. is_bipartite(g)
6. all_paths(g, src, dst)
7. eventual_safe_nodes(g)
8. border_cells(grid) + boundary flood-fill
9. pacific-atlantic reverse-flow BFS
10. has_grid_cycle(grid)

Core LeetCode set
-----------------
261. Graph Valid Tree
207. Course Schedule
210. Course Schedule II
785. Is Graph Bipartite?
886. Possible Bipartition
797. All Paths From Source to Target
802. Find Eventual Safe States
130. Surrounded Regions
417. Pacific Atlantic Water Flow
1559. Detect Cycles in 2D Grid

What mastery looks like
-----------------------
You should immediately know which extra state the traversal needs:

Undirected cycle:
    parent

Directed cycle:
    color 0/1/2

Topo sort:
    postorder reversed, or Kahn indegree

Bipartite:
    color 0/1

All paths:
    path append / recurse / pop

Boundary grid:
    mark outside-connected cells first

Pacific Atlantic:
    reverse the flow from ocean inward
"""
