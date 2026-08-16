"""
Graph Katha — Reusable Graph Primitives

Style:
    Small composable primitives, similar to the linked-list / BST toolkit.

Core representation:
    Graph:
        g[v] = list of neighbors of v

    Weighted graph:
        g[v] = list of (neighbor, weight) pairs

Main mental model:
    DFS gives structure.
    BFS gives shortest unweighted distance.
    Reverse postorder gives dependency order.
    Components give equivalence classes.
    Relaxation gives shortest paths.
    DSU gives dynamic connectivity.
    Low-link gives critical graph structure.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Iterable, Iterator, Optional, TypeAlias


Graph: TypeAlias = list[list[int]]
WGraph: TypeAlias = list[list[tuple[int, float]]]
Edge: TypeAlias = tuple[int, int, float]

INF = float("inf")
NEG_INF = float("-inf")


# =============================================================================
# Level 0 — Basic graph representation utilities
# =============================================================================

def vertices(g: Graph | WGraph) -> range:
    """Return the vertex range for adjacency-list graphs."""
    return range(len(g))


def reverse_graph(g: Graph) -> Graph:
    """
    Reverse every directed edge.

    If g has edge v -> w, the reversed graph has edge w -> v.
    For undirected graphs this usually returns an equivalent graph.
    """
    r: Graph = [[] for _ in g]

    for v in vertices(g):
        for w in g[v]:
            r[w].append(v)

    return r


def weighted_edges(g: WGraph) -> Iterator[Edge]:
    """Yield all directed weighted edges as (v, w, weight)."""
    for v, nbrs in enumerate(g):
        for w, wt in nbrs:
            yield v, w, wt


def reverse_weighted_graph(g: WGraph) -> WGraph:
    """
    Reverse every directed weighted edge.

    If g has edge v -> w with weight wt,
    the reversed graph has edge w -> v with the same weight.
    """
    r: WGraph = [[] for _ in g]

    for v, nbrs in enumerate(g):
        for w, wt in nbrs:
            r[w].append((v, wt))

    return r


def weighted_to_unweighted(g: WGraph) -> Graph:
    """Drop weights and keep only graph shape."""
    return [[w for w, _ in nbrs] for nbrs in g]


def undirected_graph(n: int, edges: Iterable[tuple[int, int]]) -> Graph:
    """Build an undirected unweighted graph."""
    g: Graph = [[] for _ in range(n)]

    for v, w in edges:
        g[v].append(w)
        g[w].append(v)

    return g


def directed_graph(n: int, edges: Iterable[tuple[int, int]]) -> Graph:
    """Build a directed unweighted graph."""
    g: Graph = [[] for _ in range(n)]

    for v, w in edges:
        g[v].append(w)

    return g


def undirected_weighted_graph(n: int, edges: Iterable[Edge]) -> WGraph:
    """Build an undirected weighted graph."""
    g: WGraph = [[] for _ in range(n)]

    for v, w, wt in edges:
        g[v].append((w, wt))
        g[w].append((v, wt))

    return g


def directed_weighted_graph(n: int, edges: Iterable[Edge]) -> WGraph:
    """Build a directed weighted graph."""
    g: WGraph = [[] for _ in range(n)]

    for v, w, wt in edges:
        g[v].append((w, wt))

    return g


# =============================================================================
# Level 1 — DFS, BFS, and path reconstruction
# =============================================================================

@dataclass
class DFSResult:
    """
    DFS traversal result.

    marked[v]:
        True iff v was reached.

    edge_to[v]:
        Parent/predecessor that first discovered v.

    pre:
        Discovery order.

    post:
        Finish order.
    """
    marked: list[bool]
    edge_to: list[Optional[int]]
    pre: list[int]
    post: list[int]


def dfs(g: Graph, s: int) -> DFSResult:
    """
    Depth-first search from a single source.

    Primitive:
        reachability + edge_to + preorder + postorder

    Mental model:
        edge_to[w] = v means v discovered w.
    """
    marked = [False] * len(g)
    edge_to: list[Optional[int]] = [None] * len(g)
    pre: list[int] = []
    post: list[int] = []

    def visit(v: int) -> None:
        marked[v] = True
        pre.append(v)

        for w in g[v]:
            if not marked[w]:
                edge_to[w] = v
                visit(w)

        post.append(v)

    visit(s)
    return DFSResult(marked, edge_to, pre, post)


@dataclass
class BFSResult:
    """
    BFS traversal result.

    marked[v]:
        True iff v was reached.

    edge_to[v]:
        Parent/predecessor that first discovered v.

    dist[v]:
        Unweighted shortest-path distance from the source.
        -1 means unreachable.
    """
    marked: list[bool]
    edge_to: list[Optional[int]]
    dist: list[int]


def bfs(g: Graph, s: int) -> BFSResult:
    """
    Breadth-first search from a single source.

    Invariant:
        When BFS first discovers a vertex, it has found the shortest
        unweighted path to that vertex.
    """
    marked = [False] * len(g)
    edge_to: list[Optional[int]] = [None] * len(g)
    dist = [-1] * len(g)

    q = deque([s])
    marked[s] = True
    dist[s] = 0

    while q:
        v = q.popleft()

        for w in g[v]:
            if not marked[w]:
                marked[w] = True
                edge_to[w] = v
                dist[w] = dist[v] + 1
                q.append(w)

    return BFSResult(marked, edge_to, dist)


def multi_source_bfs(g: Graph, sources: Iterable[int]) -> BFSResult:
    """
    BFS from many sources simultaneously.

    Useful for:
        Rotting Oranges
        01 Matrix
        As Far from Land as Possible
        Shortest Bridge expansion
        nearest-source problems

    Mental model:
        All sources start at distance 0.
    """
    marked = [False] * len(g)
    edge_to: list[Optional[int]] = [None] * len(g)
    dist = [-1] * len(g)
    q = deque()

    for s in sources:
        if marked[s]:
            continue

        marked[s] = True
        dist[s] = 0
        q.append(s)

    while q:
        v = q.popleft()

        for w in g[v]:
            if not marked[w]:
                marked[w] = True
                edge_to[w] = v
                dist[w] = dist[v] + 1
                q.append(w)

    return BFSResult(marked, edge_to, dist)


def path_to(edge_to: list[Optional[int]], s: int, t: int) -> list[int]:
    """
    Reconstruct a path from s to t using an edge_to predecessor array.

    Works for DFS, BFS, Dijkstra, Bellman-Ford, and DAG shortest paths,
    as long as edge_to[v] stores the predecessor of v.

    Returns [] if t cannot be traced back to s.
    """
    path = []
    v: Optional[int] = t

    while v is not None:
        path.append(v)

        if v == s:
            return path[::-1]

        v = edge_to[v]

    return []


# =============================================================================
# Level 2 — DFS-all, orderings, cycles, components, SCC
# =============================================================================

def dfs_all(g: Graph, order: Optional[Iterable[int]] = None) -> DFSResult:
    """
    DFS over all vertices.

    This is the base primitive for:
        connected components
        topological order
        reverse postorder
        Kosaraju SCC
        full graph traversal

    Important:
        Use `order is None`, not `order or vertices(g)`,
        so an explicit iterable is respected.
    """
    marked = [False] * len(g)
    edge_to: list[Optional[int]] = [None] * len(g)
    pre: list[int] = []
    post: list[int] = []

    def visit(v: int) -> None:
        marked[v] = True
        pre.append(v)

        for w in g[v]:
            if not marked[w]:
                edge_to[w] = v
                visit(w)

        post.append(v)

    iterable = vertices(g) if order is None else order

    for v in iterable:
        if not marked[v]:
            visit(v)

    return DFSResult(marked, edge_to, pre, post)


def reverse_post_order(g: Graph) -> list[int]:
    """
    Return vertices in reverse DFS postorder.

    DAG mental model:
        postorder:
            child/subproblem finishes before parent

        reverse postorder:
            producer/dependency appears before dependent consumer

    In a DAG, reverse postorder is a topological order.
    """
    return dfs_all(g).post[::-1]


WHITE, GRAY, BLACK = 0, 1, 2


def has_directed_cycle(g: Graph) -> bool:
    """
    Detect a cycle in a directed graph using DFS colors.

    Invariant:
        WHITE = unvisited
        GRAY  = currently on recursion stack
        BLACK = fully processed

    An edge to a GRAY vertex is a back edge, hence a directed cycle.
    """
    color = [WHITE] * len(g)

    def visit(v: int) -> bool:
        color[v] = GRAY

        for w in g[v]:
            if color[w] == GRAY:
                return True
            if color[w] == WHITE and visit(w):
                return True

        color[v] = BLACK
        return False

    return any(
        color[v] == WHITE and visit(v)
        for v in vertices(g)
    )


def has_undirected_cycle(g: Graph) -> bool:
    """
    Detect a cycle in an undirected graph.

    Invariant:
        Seeing an already-marked vertex is allowed only if it is
        the parent edge we came from. Otherwise, we found a cycle.

    Note:
        This simple version assumes no parallel-edge special handling.
    """
    marked = [False] * len(g)

    def visit(v: int, parent: int) -> bool:
        marked[v] = True

        for w in g[v]:
            if not marked[w]:
                if visit(w, v):
                    return True
            elif w != parent:
                return True

        return False

    return any(
        not marked[v] and visit(v, -1)
        for v in vertices(g)
    )


def topological_order(g: Graph) -> Optional[list[int]]:
    """
    DFS-based topological order.

    Returns:
        reverse postorder if graph is a DAG
        None if graph has a directed cycle
    """
    if has_directed_cycle(g):
        return None

    return reverse_post_order(g)


def kahn_topological_order(g: Graph) -> Optional[list[int]]:
    """
    Kahn's BFS-style topological sort.

    Better than DFS topo for:
        dependency unlocking
        recipe/supply problems
        course schedule with indegrees
        layer-by-layer build ordering

    Returns None if a directed cycle exists.
    """
    indegree = [0] * len(g)

    for v in vertices(g):
        for w in g[v]:
            indegree[w] += 1

    q = deque(v for v in vertices(g) if indegree[v] == 0)
    order: list[int] = []

    while q:
        v = q.popleft()
        order.append(v)

        for w in g[v]:
            indegree[w] -= 1

            if indegree[w] == 0:
                q.append(w)

    return order if len(order) == len(g) else None


@dataclass
class Components:
    """
    Component result.

    count:
        Number of components.

    id[v]:
        Component id of vertex v.

    size[cid]:
        Number of vertices in component cid.
    """
    count: int
    id: list[int]
    size: list[int]

    def connected(self, v: int, w: int) -> bool:
        """Return True iff v and w belong to the same component."""
        return self.id[v] == self.id[w]

    def component_size(self, v: int) -> int:
        """Return the size of v's component."""
        return self.size[self.id[v]]


def components(g: Graph, order: Optional[Iterable[int]] = None) -> Components:
    """
    Generic DFS component primitive.

    For undirected connected components:
        components(g)

    For Kosaraju SCC:
        components(g, reverse_post_order(reverse_graph(g)))

    This is the important Sedgewick-style reuse point.
    """
    comp_id = [-1] * len(g)
    comp_size: list[int] = []

    def visit(v: int, cid: int) -> int:
        comp_id[v] = cid
        size = 1

        for w in g[v]:
            if comp_id[w] == -1:
                size += visit(w, cid)

        return size

    cid = 0
    iterable = vertices(g) if order is None else order

    for v in iterable:
        if comp_id[v] == -1:
            comp_size.append(visit(v, cid))
            cid += 1

    return Components(cid, comp_id, comp_size)


def connected_components(g: Graph) -> Components:
    """Connected components of an undirected graph."""
    return components(g)


def strongly_connected_components(g: Graph) -> Components:
    """
    Kosaraju-Sharir strongly connected components.

    Composition:
        reverse graph
        + reverse postorder on reversed graph
        + components on original graph
        = strongly connected components
    """
    order = reverse_post_order(reverse_graph(g))
    return components(g, order)


def is_bipartite(g: Graph) -> bool:
    """
    Bipartite check using BFS coloring.

    Invariant:
        Every edge must connect opposite colors.

    Works for disconnected graphs.
    """
    color: list[Optional[int]] = [None] * len(g)

    for s in vertices(g):
        if color[s] is not None:
            continue

        q = deque([s])
        color[s] = 0

        while q:
            v = q.popleft()

            for w in g[v]:
                if color[w] is None:
                    color[w] = 1 - color[v]
                    q.append(w)
                elif color[w] == color[v]:
                    return False

    return True


# =============================================================================
# Level 3 — Shortest paths
# =============================================================================

@dataclass
class SPResult:
    """
    Single-source shortest-path result.

    dist[v]:
        Distance from source to v.

    edge_to[v]:
        Predecessor of v on the shortest path.

    has_negative_cycle:
        True for Bellman-Ford when a reachable negative cycle exists.
    """
    dist: list[float]
    edge_to: list[Optional[int]]
    has_negative_cycle: bool = False


def relax(
        v: int,
        w: int,
        wt: float,
        dist: list[float],
        edge_to: list[Optional[int]]
) -> bool:
    """
    Edge relaxation primitive.

    All shortest-path algorithms reduce to this.

    Mental model:
        If going through v gives a cheaper path to w,
        commit v as the predecessor of w.
    """
    if dist[v] + wt < dist[w]:
        dist[w] = dist[v] + wt
        edge_to[w] = v
        return True

    return False


def dijkstra(g: WGraph, s: int) -> SPResult:
    """
    Dijkstra shortest paths.

    Requirement:
        All edge weights must be non-negative.

    Invariant:
        When a vertex is popped with its current best distance,
        that distance is finalized.
    """
    dist = [INF] * len(g)
    edge_to: list[Optional[int]] = [None] * len(g)

    dist[s] = 0
    pq: list[tuple[float, int]] = [(0, s)]

    while pq:
        d, v = heappop(pq)

        if d != dist[v]:
            continue

        for w, wt in g[v]:
            if relax(v, w, wt, dist, edge_to):
                heappush(pq, (dist[w], w))

    return SPResult(dist, edge_to)


def bellman_ford(n: int, edges: list[Edge], s: int) -> SPResult:
    """
    Bellman-Ford shortest paths.

    Handles:
        negative edge weights

    Detects:
        reachable negative cycles

    Invariant:
        After i passes, all shortest paths using at most i edges are correct.
    """
    dist = [INF] * n
    edge_to: list[Optional[int]] = [None] * n

    dist[s] = 0

    for _ in range(n - 1):
        changed = False

        for v, w, wt in edges:
            if dist[v] < INF and relax(v, w, wt, dist, edge_to):
                changed = True

        if not changed:
            break

    has_negative_cycle = any(
        dist[v] < INF and dist[v] + wt < dist[w]
        for v, w, wt in edges
    )

    return SPResult(dist, edge_to, has_negative_cycle)


def dag_shortest_paths(g: WGraph, s: int) -> SPResult:
    """
    Shortest paths in a weighted DAG.

    Works even with negative weights, as long as the graph is acyclic.

    Composition:
        topological order
        + one relaxation pass in topo order
        = DAG shortest paths
    """
    order = topological_order(weighted_to_unweighted(g))

    if order is None:
        raise ValueError("Graph is not a DAG.")

    dist = [INF] * len(g)
    edge_to: list[Optional[int]] = [None] * len(g)

    dist[s] = 0

    for v in order:
        if dist[v] == INF:
            continue

        for w, wt in g[v]:
            relax(v, w, wt, dist, edge_to)

    return SPResult(dist, edge_to)


def dag_longest_paths(g: WGraph, s: int) -> SPResult:
    """
    Longest paths in a weighted DAG.

    Useful for:
        critical path
        scheduling
        max-score path in DAG

    Requirement:
        Graph must be acyclic.
    """
    order = topological_order(weighted_to_unweighted(g))

    if order is None:
        raise ValueError("Graph is not a DAG.")

    dist = [NEG_INF] * len(g)
    edge_to: list[Optional[int]] = [None] * len(g)

    dist[s] = 0

    for v in order:
        if dist[v] == NEG_INF:
            continue

        for w, wt in g[v]:
            if dist[v] + wt > dist[w]:
                dist[w] = dist[v] + wt
                edge_to[w] = v

    return SPResult(dist, edge_to)


def zero_one_bfs(g: WGraph, s: int) -> SPResult:
    """
    0-1 BFS.

    Use when all edge weights are exactly 0 or 1.

    This is usually better than Dijkstra for 0/1 weighted graphs.

    Rule:
        weight 0 edge -> push front
        weight 1 edge -> push back
    """
    dist = [INF] * len(g)
    edge_to: list[Optional[int]] = [None] * len(g)

    dist[s] = 0
    dq = deque([s])

    while dq:
        v = dq.popleft()

        for w, wt in g[v]:
            nd = dist[v] + wt

            if nd < dist[w]:
                dist[w] = nd
                edge_to[w] = v

                if wt == 0:
                    dq.appendleft(w)
                else:
                    dq.append(w)

    return SPResult(dist, edge_to)


# =============================================================================
# Level 4 — All-pairs shortest paths
# =============================================================================

@dataclass
class APSPResult:
    """
    All-pairs shortest-path result.

    dist[i][j]:
        Shortest path distance from i to j.

    next[i][j]:
        Next vertex after i on the shortest path from i to j.
        Used for path reconstruction.
    """
    dist: list[list[float]]
    next: list[list[Optional[int]]]


def floyd_warshall(n: int, edges: list[Edge]) -> APSPResult:
    """
    Floyd-Warshall all-pairs shortest paths.

    Best for:
        small dense graphs
        all-pairs transformation costs
        transitive closure style reasoning

    Invariant:
        After processing k, dist[i][j] is the shortest path from i to j
        using only intermediate vertices from 0..k.
    """
    dist = [[INF] * n for _ in range(n)]
    nxt: list[list[Optional[int]]] = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0
        nxt[i][i] = i

    for v, w, wt in edges:
        if wt < dist[v][w]:
            dist[v][w] = wt
            nxt[v][w] = w

    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue

            for j in range(n):
                if dist[k][j] == INF:
                    continue

                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]

    return APSPResult(dist, nxt)


def fw_path(nxt: list[list[Optional[int]]], s: int, t: int) -> list[int]:
    """
    Reconstruct a Floyd-Warshall path from s to t.

    Returns [] if no path exists.
    """
    if nxt[s][t] is None:
        return []

    path = [s]

    while s != t:
        s = nxt[s][t]

        if s is None:
            return []

        path.append(s)

    return path


def johnson(n: int, edges: list[Edge]) -> Optional[list[list[float]]]:
    """
    Johnson all-pairs shortest paths.

    Use for:
        sparse graphs
        possible negative edges
        no negative cycles

    Composition:
        Bellman-Ford from super-source
        + potentials h[v]
        + reweight edges to non-negative
        + Dijkstra from every source

    Returns:
        all-pairs distance matrix, or None if a negative cycle exists.
    """
    super_source = n
    super_edges = edges + [
        (super_source, v, 0)
        for v in range(n)
    ]

    bf = bellman_ford(n + 1, super_edges, super_source)

    if bf.has_negative_cycle:
        return None

    h = bf.dist

    reweighted_edges = [
        (v, w, wt + h[v] - h[w])
        for v, w, wt in edges
    ]

    g: WGraph = [[] for _ in range(n)]

    for v, w, wt in reweighted_edges:
        g[v].append((w, wt))

    all_dist: list[list[float]] = []

    for s in range(n):
        sp = dijkstra(g, s)

        row = [
            sp.dist[t] - h[s] + h[t]
            if sp.dist[t] < INF else INF
            for t in range(n)
        ]

        all_dist.append(row)

    return all_dist


# =============================================================================
# Level 5 — DSU and minimum spanning trees
# =============================================================================

class DSU:
    """
    Disjoint Set Union / Union-Find.

    Supports:
        dynamic connectivity
        Kruskal MST
        redundant connection detection
        offline connectivity queries
        component counting under unions
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n

    def find(self, x: int) -> int:
        """
        Return representative/root of x's component.

        Uses path halving.
        """
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]

        return x

    def union(self, a: int, b: int) -> bool:
        """
        Merge components of a and b.

        Returns:
            True if a merge happened.
            False if a and b were already connected.
        """
        ra, rb = self.find(a), self.find(b)

        if ra == rb:
            return False

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1

        return True

    def connected(self, a: int, b: int) -> bool:
        """Return True iff a and b are in the same component."""
        return self.find(a) == self.find(b)

    def component_size(self, x: int) -> int:
        """Return the size of x's component."""
        return self.size[self.find(x)]


@dataclass
class MSTResult:
    """
    Minimum spanning tree / forest result.

    weight:
        Total weight.

    edges:
        Chosen MST/MSF edges.
    """
    weight: float
    edges: list[Edge]


def kruskal_mst(n: int, edges: list[Edge]) -> MSTResult:
    """
    Kruskal minimum spanning tree.

    If the graph is disconnected, this returns a minimum spanning forest.

    Invariant:
        Take the cheapest edge that connects two different components.
    """
    dsu = DSU(n)
    mst: list[Edge] = []
    total = 0.0

    for v, w, wt in sorted(edges, key=lambda e: e[2]):
        if dsu.union(v, w):
            mst.append((v, w, wt))
            total += wt

            if len(mst) == n - 1:
                break

    return MSTResult(total, mst)


def prim_mst(g: WGraph) -> MSTResult:
    """
    Lazy Prim minimum spanning tree.

    Input:
        undirected weighted adjacency list

    If the graph is disconnected, this returns a minimum spanning forest.

    Invariant:
        Maintain a cut between tree vertices and non-tree vertices.
        Choose the cheapest crossing edge.
    """
    marked = [False] * len(g)
    mst: list[Edge] = []
    total = 0.0

    for s in range(len(g)):
        if marked[s]:
            continue

        pq: list[tuple[float, int, int]] = [(0, s, -1)]

        while pq:
            wt, v, parent = heappop(pq)

            if marked[v]:
                continue

            marked[v] = True

            if parent != -1:
                mst.append((parent, v, wt))
                total += wt

            for w, edge_wt in g[v]:
                if not marked[w]:
                    heappush(pq, (edge_wt, w, v))

    return MSTResult(total, mst)


# =============================================================================
# Level 6 — Low-link structure: bridges and articulation points
# =============================================================================

def bridges(g: Graph) -> list[tuple[int, int]]:
    """
    Find all bridges / critical connections in an undirected graph.

    low[v]:
        Earliest discovery time reachable from v's subtree using
        zero or more tree edges and at most one back edge.

    Bridge rule:
        edge v-w is a bridge iff low[w] > tin[v].
    """
    timer = 0
    tin = [-1] * len(g)
    low = [-1] * len(g)
    result: list[tuple[int, int]] = []

    def visit(v: int, parent: int) -> None:
        nonlocal timer

        tin[v] = low[v] = timer
        timer += 1

        for w in g[v]:
            if w == parent:
                continue

            if tin[w] != -1:
                low[v] = min(low[v], tin[w])
            else:
                visit(w, v)
                low[v] = min(low[v], low[w])

                if low[w] > tin[v]:
                    result.append((v, w))

    for v in vertices(g):
        if tin[v] == -1:
            visit(v, -1)

    return result


def articulation_points(g: Graph) -> set[int]:
    """
    Find articulation points / cut vertices in an undirected graph.

    Non-root rule:
        v is articulation point if some child w has low[w] >= tin[v].

    Root rule:
        root is articulation point if it has more than one DFS child.
    """
    timer = 0
    tin = [-1] * len(g)
    low = [-1] * len(g)
    points: set[int] = set()

    def visit(v: int, parent: int) -> None:
        nonlocal timer

        tin[v] = low[v] = timer
        timer += 1
        children = 0

        for w in g[v]:
            if w == parent:
                continue

            if tin[w] != -1:
                low[v] = min(low[v], tin[w])
            else:
                visit(w, v)
                low[v] = min(low[v], low[w])

                if parent != -1 and low[w] >= tin[v]:
                    points.add(v)

                children += 1

        if parent == -1 and children > 1:
            points.add(v)

    for v in vertices(g):
        if tin[v] == -1:
            visit(v, -1)

    return points


# =============================================================================
# Level 7 — Grid graph primitives
# =============================================================================

DIR4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIR8 = DIR4 + [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def inside(grid: list[list[object]], r: int, c: int) -> bool:
    """Return True iff (r, c) is inside the grid."""
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def neighbors4(grid: list[list[object]], r: int, c: int) -> Iterator[tuple[int, int]]:
    """Yield 4-directional valid neighbors."""
    for dr, dc in DIR4:
        nr, nc = r + dr, c + dc

        if inside(grid, nr, nc):
            yield nr, nc


def neighbors8(grid: list[list[object]], r: int, c: int) -> Iterator[tuple[int, int]]:
    """Yield 8-directional valid neighbors."""
    for dr, dc in DIR8:
        nr, nc = r + dr, c + dc

        if inside(grid, nr, nc):
            yield nr, nc


def cell_id(grid: list[list[object]], r: int, c: int) -> int:
    """Map grid coordinate to a vertex id."""
    return r * len(grid[0]) + c


def cell_pos(grid: list[list[object]], v: int) -> tuple[int, int]:
    """Map vertex id back to grid coordinate."""
    return divmod(v, len(grid[0]))


# =============================================================================
# Composition map and drill order
# =============================================================================

"""
Core composition map:

    Reachability
        dfs / bfs

    Unweighted shortest path
        bfs + edge_to + path_to

    Connected components
        dfs-all + component id

    Strongly connected components
        reverse graph + reverse postorder + components

    Topological sort
        DAG + reverse postorder

    Dependency unlocking
        indegree + queue

    Directed cycle
        DFS recursion colors

    Undirected cycle
        DFS parent check

    Non-negative shortest path
        relax + min-heap

    Negative-edge shortest path
        repeated relaxation

    DAG shortest path
        topological order + relaxation

    All-pairs dense graph
        Floyd-Warshall dynamic programming over intermediates

    All-pairs sparse graph
        Bellman-Ford reweighting + repeated Dijkstra

    MST by edges
        sort edges + DSU

    MST by frontier
        min-heap cut expansion

    Critical edges / cut vertices
        DFS discovery time + low-link

    0/1 weighted shortest path
        deque relaxation

    Grid graph
        coordinate neighbors


Highest-ROI drill order:

    1. dfs + edge_to
    2. bfs + edge_to + dist
    3. path_to
    4. dfs_all
    5. connected_components
    6. directed cycle detection
    7. reverse_post_order
    8. topological_order
    9. kahn_topological_order
    10. strongly_connected_components
    11. bipartite check
    12. relax
    13. dijkstra
    14. bellman_ford
    15. dag_shortest_paths
    16. zero_one_bfs
    17. floyd_warshall
    18. DSU
    19. kruskal_mst
    20. prim_mst
    21. bridges
    22. articulation_points
    23. johnson
"""
