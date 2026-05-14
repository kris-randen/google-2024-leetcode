"""
Graph Primitives — Part 4: Minimum Spanning Tree / Kruskal / Prim

LeetCode-style version.

Part 1 covered plain DFS/BFS traversal.
Part 2 covered DFS/BFS with state.
Part 3 covered Union-Find / dynamic connectivity.

Part 4 covers Minimum Spanning Tree.

Core idea:
    Given a connected weighted undirected graph, choose edges that connect all
    vertices with minimum total weight and no cycles.

Two main skeletons:
    Kruskal = sort edges + UnionFind
    Prim    = grow one tree using a min-heap frontier

Keep it boring and fast for LeetCode.
No generics. No protocols. No type annotations.

Conventions:
    Unweighted graph:
        g[v] = [w1, w2, ...]

    Weighted graph:
        g[v] = [(w1, wt1), (w2, wt2), ...]

    Weighted edge list:
        edges = [[v, w, wt], ...]

    Indexed weighted edge list, for critical-edge problems:
        edges = [[v, w, wt, index], ...]
"""

from heapq import heappush, heappop


# ============================================================
# 1. UNION-FIND CORE, REPEATED HERE SO THIS FILE IS STANDALONE
# ============================================================

"""
Why this primitive exists
-------------------------
Kruskal needs to know whether adding an edge creates a cycle.

For an undirected graph:
    edge (v, w) creates a cycle iff v and w are already connected.

Union-Find answers that in almost constant time.

Core invariant:
    uf.union(v, w) returns False exactly when edge (v, w) is redundant.

This builds up to:
    Kruskal MST
    critical / pseudo-critical MST edges
"""


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n

    def find(self, x):
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]

        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return False

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1

        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)


# ============================================================
# 2. WEIGHTED GRAPH BUILDERS
# ============================================================

"""
Why this primitive exists
-------------------------
MST problems are undirected weighted graph problems.

Sometimes LeetCode gives us edges directly.
Sometimes we need adjacency lists for Prim.

Keep both representations simple:
    edge list for Kruskal
    adjacency list for Prim

Weighted edge list:
    [v, w, wt]

Weighted adjacency list:
    g[v] = [(w, wt), ...]
"""


def wgraph(n, edges):
    g = [[] for _ in range(n)]

    for v, w, wt in edges:
        g[v].append((w, wt))
        g[w].append((v, wt))

    return g


# ============================================================
# 3. KRUSKAL MST
# ============================================================

"""
Why this primitive exists
-------------------------
Kruskal is the simplest MST primitive for LeetCode.

Core algorithm:
    sort all edges by weight
    scan from smallest to largest
    add edge if it connects two different components
    skip edge if it creates a cycle

Composition:
    weighted edge list
    + sort by weight
    + UnionFind cycle check
    -> MST weight

Core invariant:
    At every step, the selected edges form a forest.
    Each accepted edge is the cheapest safe edge at that moment.

Problems:
    1135. Connecting Cities With Minimum Cost
    1168. Optimize Water Distribution in a Village
    1584. Min Cost to Connect All Points
    1489. Find Critical and Pseudo-Critical Edges in MST
"""


def mst_weight(n, edges):
    uf = UnionFind(n)
    total = 0
    used = 0

    for v, w, wt in sorted(edges, key=lambda e: e[2]):
        if uf.union(v, w):
            total += wt
            used += 1

            if used == n - 1:
                return total

    return total if used == n - 1 else -1


# Same primitive, but also returns the chosen tree edges.
# Useful while debugging / studying MST construction.


def mst_edges(n, edges):
    uf = UnionFind(n)
    total = 0
    tree = []

    for v, w, wt in sorted(edges, key=lambda e: e[2]):
        if uf.union(v, w):
            total += wt
            tree.append([v, w, wt])

    return (total, tree) if len(tree) == n - 1 else (-1, tree)


# ============================================================
# 4. PROBLEM 1135 — CONNECTING CITIES WITH MINIMUM COST
# ============================================================

"""
Problem 1135. Connecting Cities With Minimum Cost

Reduction:
    Cities are vertices.
    Connections are weighted undirected edges.
    Minimum cost to connect all cities = MST weight.

Trap:
    Cities are 1-indexed, so convert to 0-indexed before using UnionFind(n).
    
"""


class Solution1135:
    def minimumCost(self, n, connections):
        edges = []

        for a, b, cost in connections:
            edges.append([a - 1, b - 1, cost])

        return mst_weight(n, edges)


# ============================================================
# 5. PROBLEM 1584 — MIN COST TO CONNECT ALL POINTS
# ============================================================

"""
Problem 1584. Min Cost to Connect All Points

Reduction:
    Every point is a vertex.
    Cost between two points is Manhattan distance.
    We need minimum cost to connect all points.
    That is MST on the complete graph.

Composition:
    build all O(n^2) Manhattan edges
    + Kruskal
    -> answer

For LeetCode constraints, this straightforward O(n^2 log n) version is fine.
"""


def manhattan_edges(points):
    edges = []

    for i in range(len(points)):
        x1, y1 = points[i]

        for j in range(i + 1, len(points)):
            x2, y2 = points[j]
            wt = abs(x1 - x2) + abs(y1 - y2)
            edges.append([i, j, wt])

    return edges


class Solution1584:
    def minCostConnectPoints(self, points):
        return mst_weight(len(points), manhattan_edges(points))


# ============================================================
# 6. PROBLEM 1168 — OPTIMIZE WATER DISTRIBUTION
# ============================================================

"""
Problem 1168. Optimize Water Distribution in a Village

Reduction:
    Each house needs water.
    It can either:
        build its own well
        or connect through pipes to another house

Virtual-node trick:
    Add node 0 as the water source.
    Building well at house i becomes edge 0 -- i with cost wells[i - 1].
    Pipes are normal weighted undirected edges.

Then the problem becomes:
    connect all houses plus virtual source with minimum cost
    = MST

Composition:
    virtual source edges
    + pipe edges
    + Kruskal
    -> minimum water cost
"""


class Solution1168:
    def minCostToSupplyWater(self, n, wells, pipes):
        edges = []

        for house, cost in enumerate(wells, start=1):
            edges.append([0, house, cost])

        for a, b, cost in pipes:
            edges.append([a, b, cost])

        return mst_weight(n + 1, edges)


# ============================================================
# 7. PRIM MST
# ============================================================

"""
Why this primitive exists
-------------------------
Prim is the other main MST skeleton.

Kruskal thinks globally:
    sort all edges
    add cheapest safe edge

Prim thinks from a growing tree:
    start anywhere
    repeatedly add the cheapest edge crossing from seen to unseen

Composition:
    weighted adjacency list
    + min-heap frontier
    + seen set
    -> MST weight

Core invariant:
    heap contains candidate crossing edges into the current tree.

This version is the simple lazy-Prim style.
It may push stale edges into the heap, then skip them when popped.
That is fine for LeetCode.
"""


def prim(g):
    if not g:
        return 0

    seen = set()
    heap = [(0, 0)]
    total = 0

    while heap and len(seen) < len(g):
        wt, v = heappop(heap)

        if v in seen:
            continue

        seen.add(v)
        total += wt

        for w, cost in g[v]:
            if w not in seen:
                heappush(heap, (cost, w))

    return total if len(seen) == len(g) else -1


# Same 1584 using Prim directly, without materializing sorted edge list for Kruskal.
# This still builds the complete graph adjacency, so it is not asymptotically better here,
# but it demonstrates the Prim skeleton clearly.


class Solution1584Prim:
    def minCostConnectPoints(self, points):
        return prim(wgraph(len(points), manhattan_edges(points)))


# ============================================================
# 8. CRITICAL / PSEUDO-CRITICAL MST EDGES
# ============================================================

"""
Why this primitive exists
-------------------------
Some MST problems ask not just for MST weight, but for the role of each edge.

Definitions:
    Critical edge:
        If removing this edge makes MST weight worse, the edge is critical.

    Pseudo-critical edge:
        If forcing this edge can still produce an MST of optimal weight,
        the edge is pseudo-critical.

Core primitive:
    run Kruskal with one edge skipped or forced.

Composition:
    base MST weight
    + Kruskal(skip edge)
    + Kruskal(force edge)
    -> classify edge

Problem:
    1489. Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree
"""


INF = 10 ** 18


def indexed_edges(edges):
    ans = []

    for i, (v, w, wt) in enumerate(edges):
        ans.append([v, w, wt, i])

    return ans


# edges format:
#     [v, w, wt, original_index]
#
# skip:
#     original index of edge to ignore
#
# force:
#     actual edge [v, w, wt, original_index] to include first


def kruskal_with_options(n, edges, skip=None, force=None):
    uf = UnionFind(n)
    total = 0
    used = 0

    if force is not None:
        v, w, wt, _ = force

        if uf.union(v, w):
            total += wt
            used += 1

    for v, w, wt, i in sorted(edges, key=lambda e: e[2]):
        if i == skip:
            continue

        if uf.union(v, w):
            total += wt
            used += 1

            if used == n - 1:
                return total

    return total if used == n - 1 else INF


class Solution1489:
    def findCriticalAndPseudoCriticalEdges(self, n, edges):
        es = indexed_edges(edges)
        base = kruskal_with_options(n, es)

        critical = []
        pseudo = []

        for edge in es:
            v, w, wt, i = edge

            without = kruskal_with_options(n, es, skip=i)

            if without > base:
                critical.append(i)
                continue

            with_edge = kruskal_with_options(n, es, force=edge)

            if with_edge == base:
                pseudo.append(i)

        return [critical, pseudo]


# ============================================================
# 9. KRUSKAL VS PRIM — WHEN TO USE WHICH
# ============================================================

"""
Use Kruskal when:
    input is already an edge list
    Union-Find code is available
    you need to classify edges
    the graph is sparse or easy to sort

Use Prim when:
    input is naturally an adjacency list
    you want to grow from one source
    you do not need edge classification

For most LeetCode MST problems:
    Kruskal is usually simpler.

The most important composition to remember:
    MST = greedy safe-edge selection

Kruskal safe-edge test:
    endpoints are in different DSU components

Prim safe-edge test:
    edge crosses from seen to unseen
"""
