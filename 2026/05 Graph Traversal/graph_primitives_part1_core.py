"""
Graph Traversal Primitives — Part 1
===================================

Scope:
    - Graph representation helpers
    - DFS reachability / components
    - BFS distance / parent / shortest unweighted path
    - Multi-source BFS
    - Grid-neighbor helpers

Design style:
    - Small, composable functions
    - Plain Python data structures
    - Works for int vertices, string vertices, tuple vertices, grid cells, etc.
    - No LeetCode Solution classes here; this is the reusable toolkit layer.

Core mental model:
    Graph problem = node representation + neighbor generator + frontier policy

    DFS:
        Use when you need reachability, component discovery, flood-fill,
        recursive structure, or exhaustive exploration.

    BFS:
        Use when every edge has equal cost and you need minimum number of steps.

    Multi-source BFS:
        Use when distance is measured from the nearest among many sources.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import (
    Callable,
    Deque,
    Dict,
    Hashable,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
)


V = TypeVar("V", bound=Hashable)
Cell = Tuple[int, int]
Graph = Dict[V, List[V]]
Parent = Dict[V, Optional[V]]
Distance = Dict[V, int]


# -----------------------------------------------------------------------------
# 0. Tiny helpers
# -----------------------------------------------------------------------------


def add_vertex(graph: Graph[V], v: V) -> Graph[V]:
    graph.setdefault(v, [])
    return graph


def append_edge(graph: Graph[V], u: V, v: V) -> Graph[V]:
    graph[u].append(v)
    return graph


def vertices_of(graph: Mapping[V, Sequence[V]]) -> Iterator[V]:
    return iter(graph)


def empty_graph(vertices: Iterable[V] = ()) -> Graph[V]:
    return {v: [] for v in vertices}


# -----------------------------------------------------------------------------
# 1. Adjacency-list builders
# -----------------------------------------------------------------------------


def build_directed_adj(edges: Iterable[Tuple[V, V]], vertices: Iterable[V] = ()) -> Graph[V]:
    graph = empty_graph(vertices)
    for u, v in edges:
        add_vertex(graph, u)
        add_vertex(graph, v)
        append_edge(graph, u, v)
    return graph


def build_undirected_adj(edges: Iterable[Tuple[V, V]], vertices: Iterable[V] = ()) -> Graph[V]:
    graph = empty_graph(vertices)
    for u, v in edges:
        add_vertex(graph, u)
        add_vertex(graph, v)
        append_edge(graph, u, v)
        append_edge(graph, v, u)
    return graph


def reverse_graph(graph: Mapping[V, Iterable[V]]) -> Graph[V]:
    rev: Graph[V] = {v: [] for v in graph}
    for u, nbrs in graph.items():
        for v in nbrs:
            add_vertex(rev, v)
            append_edge(rev, v, u)
    return rev


def undirected_edges(graph: Mapping[V, Iterable[V]]) -> Iterator[Tuple[V, V]]:
    seen: Set[frozenset[V]] = set()
    for u, nbrs in graph.items():
        for v in nbrs:
            edge = frozenset((u, v))
            if edge not in seen:
                seen.add(edge)
                yield u, v


def directed_edges(graph: Mapping[V, Iterable[V]]) -> Iterator[Tuple[V, V]]:
    for u, nbrs in graph.items():
        for v in nbrs:
            yield u, v


# -----------------------------------------------------------------------------
# 2. Neighbor functions
# -----------------------------------------------------------------------------


def graph_neighbors(graph: Mapping[V, Iterable[V]]) -> Callable[[V], Iterable[V]]:
    return lambda v: graph.get(v, ())


def inside(rows: int, cols: int, cell: Cell) -> bool:
    r, c = cell
    return 0 <= r < rows and 0 <= c < cols


def neighbors4(cell: Cell) -> Iterator[Cell]:
    r, c = cell
    yield r - 1, c
    yield r + 1, c
    yield r, c - 1
    yield r, c + 1


def neighbors8(cell: Cell) -> Iterator[Cell]:
    r, c = cell
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr or dc:
                yield r + dr, c + dc


def legal_neighbors(rows: int, cols: int, raw_neighbors: Callable[[Cell], Iterable[Cell]]) -> Callable[[Cell], Iterator[Cell]]:
    def neighbors(cell: Cell) -> Iterator[Cell]:
        return (nxt for nxt in raw_neighbors(cell) if inside(rows, cols, nxt))

    return neighbors


# -----------------------------------------------------------------------------
# 3. DFS reachability primitives
# -----------------------------------------------------------------------------


def dfs_preorder(start: V, neighbors: Callable[[V], Iterable[V]]) -> Iterator[V]:
    seen: Set[V] = set()

    def visit(v: V) -> Iterator[V]:
        seen.add(v)
        yield v
        for w in neighbors(v):
            if w not in seen:
                yield from visit(w)

    yield from visit(start)


def reachable(start: V, target: V, neighbors: Callable[[V], Iterable[V]]) -> bool:
    return any(v == target for v in dfs_preorder(start, neighbors))


def reachable_set(start: V, neighbors: Callable[[V], Iterable[V]]) -> Set[V]:
    return set(dfs_preorder(start, neighbors))


def dfs_parent_tree(start: V, neighbors: Callable[[V], Iterable[V]]) -> Parent[V]:
    parent: Parent[V] = {start: None}

    def visit(v: V) -> None:
        for w in neighbors(v):
            if w not in parent:
                parent[w] = v
                visit(w)

    visit(start)
    return parent


def path_from_parent(parent: Mapping[V, Optional[V]], target: V) -> List[V]:
    path: List[V] = []
    while target in parent:
        path.append(target)
        prev = parent[target]
        if prev is None:
            return path[::-1]
        target = prev
    return []


def dfs_path(start: V, target: V, neighbors: Callable[[V], Iterable[V]]) -> List[V]:
    return path_from_parent(dfs_parent_tree(start, neighbors), target)


# -----------------------------------------------------------------------------
# 4. Connected components by DFS
# -----------------------------------------------------------------------------


def mark_component(start: V, component_id: int, component: Dict[V, int], neighbors: Callable[[V], Iterable[V]]) -> None:
    component[start] = component_id
    for w in neighbors(start):
        if w not in component:
            mark_component(w, component_id, component, neighbors)


def component_ids(vertices: Iterable[V], neighbors: Callable[[V], Iterable[V]]) -> Dict[V, int]:
    component: Dict[V, int] = {}
    for v in vertices:
        if v not in component:
            mark_component(v, len(set(component.values())), component, neighbors)
    return component


def components(vertices: Iterable[V], neighbors: Callable[[V], Iterable[V]]) -> List[List[V]]:
    ids = component_ids(vertices, neighbors)
    groups: Dict[int, List[V]] = defaultdict(list)
    for v, cid in ids.items():
        groups[cid].append(v)
    return [groups[cid] for cid in sorted(groups)]


def component_count(vertices: Iterable[V], neighbors: Callable[[V], Iterable[V]]) -> int:
    return len(components(vertices, neighbors))


def connected(u: V, v: V, component: Mapping[V, int]) -> bool:
    return u in component and v in component and component[u] == component[v]


# -----------------------------------------------------------------------------
# 5. BFS primitives
# -----------------------------------------------------------------------------


def bfs_order(starts: Iterable[V], neighbors: Callable[[V], Iterable[V]]) -> Iterator[V]:
    q: Deque[V] = deque(starts)
    seen: Set[V] = set(q)

    while q:
        v = q.popleft()
        yield v
        for w in neighbors(v):
            if w not in seen:
                seen.add(w)
                q.append(w)


def bfs_dist(starts: Iterable[V], neighbors: Callable[[V], Iterable[V]]) -> Distance[V]:
    q: Deque[V] = deque(starts)
    dist: Distance[V] = {s: 0 for s in q}

    while q:
        v = q.popleft()
        for w in neighbors(v):
            if w not in dist:
                dist[w] = dist[v] + 1
                q.append(w)
    return dist


def bfs_parent(start: V, neighbors: Callable[[V], Iterable[V]]) -> Parent[V]:
    q: Deque[V] = deque([start])
    parent: Parent[V] = {start: None}

    while q:
        v = q.popleft()
        for w in neighbors(v):
            if w not in parent:
                parent[w] = v
                q.append(w)
    return parent


def bfs_path(start: V, target: V, neighbors: Callable[[V], Iterable[V]]) -> List[V]:
    return path_from_parent(bfs_parent(start, neighbors), target)


def shortest_unweighted_distance(start: V, target: V, neighbors: Callable[[V], Iterable[V]]) -> int:
    dist = bfs_dist([start], neighbors)
    return dist.get(target, -1)


# -----------------------------------------------------------------------------
# 6. Level-order BFS helpers
# -----------------------------------------------------------------------------


def bfs_levels(starts: Iterable[V], neighbors: Callable[[V], Iterable[V]]) -> Iterator[List[V]]:
    q: Deque[V] = deque(starts)
    seen: Set[V] = set(q)

    while q:
        level: List[V] = []
        for _ in range(len(q)):
            v = q.popleft()
            level.append(v)
            for w in neighbors(v):
                if w not in seen:
                    seen.add(w)
                    q.append(w)
        yield level


def first_level_matching(starts: Iterable[V], neighbors: Callable[[V], Iterable[V]], pred: Callable[[V], bool]) -> Optional[int]:
    for depth, level in enumerate(bfs_levels(starts, neighbors)):
        if any(pred(v) for v in level):
            return depth
    return None


# -----------------------------------------------------------------------------
# 7. Grid traversal helpers
# -----------------------------------------------------------------------------


def grid_cells(rows: int, cols: int) -> Iterator[Cell]:
    for r in range(rows):
        for c in range(cols):
            yield r, c


def grid_neighbors4(rows: int, cols: int) -> Callable[[Cell], Iterator[Cell]]:
    return legal_neighbors(rows, cols, neighbors4)


def grid_neighbors8(rows: int, cols: int) -> Callable[[Cell], Iterator[Cell]]:
    return legal_neighbors(rows, cols, neighbors8)


def filtered_neighbors(raw_neighbors: Callable[[V], Iterable[V]], allowed: Callable[[V], bool]) -> Callable[[V], Iterator[V]]:
    return lambda v: (w for w in raw_neighbors(v) if allowed(w))


def flood_fill(start: V, neighbors: Callable[[V], Iterable[V]]) -> Set[V]:
    return reachable_set(start, neighbors)


def grid_component(start: Cell, rows: int, cols: int, allowed: Callable[[Cell], bool]) -> Set[Cell]:
    raw = grid_neighbors4(rows, cols)
    return flood_fill(start, filtered_neighbors(raw, allowed)) if allowed(start) else set()


def grid_components(rows: int, cols: int, allowed: Callable[[Cell], bool]) -> List[Set[Cell]]:
    seen: Set[Cell] = set()
    groups: List[Set[Cell]] = []

    for cell in grid_cells(rows, cols):
        if cell not in seen and allowed(cell):
            group = grid_component(cell, rows, cols, allowed)
            seen |= group
            groups.append(group)
    return groups


# -----------------------------------------------------------------------------
# 8. LeetCode-style recipe functions using the primitives
# -----------------------------------------------------------------------------


def valid_path(n: int, edges: List[List[int]], source: int, destination: int) -> bool:
    graph = build_undirected_adj(((u, v) for u, v in edges), range(n))
    return reachable(source, destination, graph_neighbors(graph))


def count_components(n: int, edges: List[List[int]]) -> int:
    graph = build_undirected_adj(((u, v) for u, v in edges), range(n))
    return component_count(range(n), graph_neighbors(graph))


def number_of_islands(grid: List[List[str]]) -> int:
    rows, cols = len(grid), len(grid[0]) if grid else 0
    return len(grid_components(rows, cols, lambda cell: grid[cell[0]][cell[1]] == "1"))


def max_area_of_island(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0]) if grid else 0
    groups = grid_components(rows, cols, lambda cell: grid[cell[0]][cell[1]] == 1)
    return max(map(len, groups), default=0)


def shortest_path_binary_matrix(grid: List[List[int]]) -> int:
    n = len(grid)
    if not n or grid[0][0] or grid[n - 1][n - 1]:
        return -1

    neighbors = filtered_neighbors(grid_neighbors8(n, n), lambda cell: grid[cell[0]][cell[1]] == 0)
    dist = bfs_dist([(0, 0)], neighbors)
    return dist.get((n - 1, n - 1), -2) + 1


def oranges_rotting(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0]) if grid else 0
    starts = [cell for cell in grid_cells(rows, cols) if grid[cell[0]][cell[1]] == 2]
    fresh = {cell for cell in grid_cells(rows, cols) if grid[cell[0]][cell[1]] == 1}
    allowed = lambda cell: grid[cell[0]][cell[1]] in (1, 2)
    dist = bfs_dist(starts, filtered_neighbors(grid_neighbors4(rows, cols), allowed))
    return max((dist[cell] for cell in fresh), default=0) if fresh <= dist.keys() else -1


# -----------------------------------------------------------------------------
# 9. Non-executing examples for mental rehearsal
# -----------------------------------------------------------------------------

if False:
    # 1971. Find if Path Exists in Graph
    assert valid_path(3, [[0, 1], [1, 2], [2, 0]], 0, 2) is True

    # 323. Number of Connected Components in an Undirected Graph
    assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2

    # 200. Number of Islands
    grid1 = [
        ["1", "1", "0", "0"],
        ["1", "1", "0", "0"],
        ["0", "0", "1", "0"],
    ]
    assert number_of_islands(grid1) == 2

    # 994. Rotting Oranges
    grid2 = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    assert oranges_rotting(grid2) == 4

    # 1091. Shortest Path in Binary Matrix
    grid3 = [[0, 1], [1, 0]]
    assert shortest_path_binary_matrix(grid3) == 2
