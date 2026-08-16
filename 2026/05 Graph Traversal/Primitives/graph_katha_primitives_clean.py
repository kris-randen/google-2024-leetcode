from __future__ import annotations

from collections import deque
from heapq import heappop, heappush


INF = float("inf")
NEG_INF = float("-inf")


def vertices(g):
    return range(len(g))


def reverse_graph(g):
    r = [[] for _ in g]

    for v in vertices(g):
        for w in g[v]:
            r[w].append(v)

    return r


def weighted_edges(g):
    for v, nbrs in enumerate(g):
        for w, wt in nbrs:
            yield v, w, wt


def reverse_weighted_graph(g):
    r = [[] for _ in g]

    for v, nbrs in enumerate(g):
        for w, wt in nbrs:
            r[w].append((v, wt))

    return r


def weighted_to_unweighted(g):
    return [[w for w, _ in nbrs] for nbrs in g]


def directed_graph(n, edges):
    g = [[] for _ in range(n)]

    for v, w in edges:
        g[v].append(w)

    return g


def undirected_graph(n, edges):
    g = [[] for _ in range(n)]

    for v, w in edges:
        g[v].append(w)
        g[w].append(v)

    return g


def directed_weighted_graph(n, edges):
    g = [[] for _ in range(n)]

    for v, w, wt in edges:
        g[v].append((w, wt))

    return g


def undirected_weighted_graph(n, edges):
    g = [[] for _ in range(n)]

    for v, w, wt in edges:
        g[v].append((w, wt))
        g[w].append((v, wt))

    return g


class DFSResult:
    def __init__(self, marked, edge_to, post):
        self.marked = marked
        self.edge_to = edge_to
        self.post = post


def dfs(g, s):
    marked = [False] * len(g)
    edge_to = [None] * len(g)
    post = []

    def visit(v):
        marked[v] = True

        for w in g[v]:
            if not marked[w]:
                edge_to[w] = v
                visit(w)

        post.append(v)

    visit(s)
    return DFSResult(marked, edge_to, post)


def dfs_all(g, order=None):
    marked = [False] * len(g)
    edge_to = [None] * len(g)
    post = []

    def visit(v):
        marked[v] = True

        for w in g[v]:
            if not marked[w]:
                edge_to[w] = v
                visit(w)

        post.append(v)

    for v in vertices(g) if order is None else order:
        if not marked[v]:
            visit(v)

    return DFSResult(marked, edge_to, post)


class BFSResult:
    def __init__(self, marked, edge_to, dist):
        self.marked = marked
        self.edge_to = edge_to
        self.dist = dist


def bfs(g, s):
    marked = [False] * len(g)
    edge_to = [None] * len(g)
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


def multi_source_bfs(g, sources):
    marked = [False] * len(g)
    edge_to = [None] * len(g)
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


def path_to(edge_to, s, t):
    path = []
    v = t

    while v is not None:
        path.append(v)

        if v == s:
            return path[::-1]

        v = edge_to[v]

    return []


def reverse_post_order(g):
    return dfs_all(g).post[::-1]


WHITE, GRAY, BLACK = 0, 1, 2


def has_directed_cycle(g):
    color = [WHITE] * len(g)

    def visit(v):
        color[v] = GRAY

        for w in g[v]:
            if color[w] == GRAY:
                return True
            if color[w] == WHITE and visit(w):
                return True

        color[v] = BLACK
        return False

    return any(color[v] == WHITE and visit(v) for v in vertices(g))


def has_undirected_cycle(g):
    marked = [False] * len(g)

    def visit(v, parent):
        marked[v] = True

        for w in g[v]:
            if not marked[w]:
                if visit(w, v):
                    return True
            elif w != parent:
                return True

        return False

    return any(not marked[v] and visit(v, -1) for v in vertices(g))


def topological_order(g):
    if has_directed_cycle(g):
        return None

    return reverse_post_order(g)


def kahn_topological_order(g):
    indegree = [0] * len(g)

    for v in vertices(g):
        for w in g[v]:
            indegree[w] += 1

    q = deque(v for v in vertices(g) if indegree[v] == 0)
    order = []

    while q:
        v = q.popleft()
        order.append(v)

        for w in g[v]:
            indegree[w] -= 1

            if indegree[w] == 0:
                q.append(w)

    return order if len(order) == len(g) else None


class Components:
    def __init__(self, count, id, size):
        self.count = count
        self.id = id
        self.size = size

    def connected(self, v, w):
        return self.id[v] == self.id[w]

    def component_size(self, v):
        return self.size[self.id[v]]


def components(g, order=None):
    comp_id = [-1] * len(g)
    comp_size = []

    def visit(v, cid):
        comp_id[v] = cid
        size = 1

        for w in g[v]:
            if comp_id[w] == -1:
                size += visit(w, cid)

        return size

    cid = 0

    for v in vertices(g) if order is None else order:
        if comp_id[v] == -1:
            comp_size.append(visit(v, cid))
            cid += 1

    return Components(cid, comp_id, comp_size)


def connected_components(g):
    return components(g)


def strongly_connected_components(g):
    order = reverse_post_order(reverse_graph(g))
    return components(g, order)


def is_bipartite(g):
    color = [None] * len(g)

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


class SPResult:
    def __init__(self, dist, edge_to, has_negative_cycle=False):
        self.dist = dist
        self.edge_to = edge_to
        self.has_negative_cycle = has_negative_cycle


def relax(v, w, wt, dist, edge_to):
    if dist[v] + wt < dist[w]:
        dist[w] = dist[v] + wt
        edge_to[w] = v
        return True

    return False


def dijkstra(g, s):
    dist = [INF] * len(g)
    edge_to = [None] * len(g)

    dist[s] = 0
    pq = [(0, s)]

    while pq:
        d, v = heappop(pq)

        if d != dist[v]:
            continue

        for w, wt in g[v]:
            if relax(v, w, wt, dist, edge_to):
                heappush(pq, (dist[w], w))

    return SPResult(dist, edge_to)


def bellman_ford(n, edges, s):
    dist = [INF] * n
    edge_to = [None] * n

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


def dag_shortest_paths(g, s):
    order = topological_order(weighted_to_unweighted(g))

    if order is None:
        raise ValueError("Graph is not a DAG.")

    dist = [INF] * len(g)
    edge_to = [None] * len(g)
    dist[s] = 0

    for v in order:
        if dist[v] == INF:
            continue

        for w, wt in g[v]:
            relax(v, w, wt, dist, edge_to)

    return SPResult(dist, edge_to)


def dag_longest_paths(g, s):
    order = topological_order(weighted_to_unweighted(g))

    if order is None:
        raise ValueError("Graph is not a DAG.")

    dist = [NEG_INF] * len(g)
    edge_to = [None] * len(g)
    dist[s] = 0

    for v in order:
        if dist[v] == NEG_INF:
            continue

        for w, wt in g[v]:
            if dist[v] + wt > dist[w]:
                dist[w] = dist[v] + wt
                edge_to[w] = v

    return SPResult(dist, edge_to)


def zero_one_bfs(g, s):
    dist = [INF] * len(g)
    edge_to = [None] * len(g)

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


class APSPResult:
    def __init__(self, dist, next):
        self.dist = dist
        self.next = next


def floyd_warshall(n, edges):
    dist = [[INF] * n for _ in range(n)]
    nxt = [[None] * n for _ in range(n)]

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


def fw_path(nxt, s, t):
    if nxt[s][t] is None:
        return []

    path = [s]

    while s != t:
        s = nxt[s][t]

        if s is None:
            return []

        path.append(s)

    return path


def johnson(n, edges):
    super_source = n
    super_edges = edges + [(super_source, v, 0) for v in range(n)]

    bf = bellman_ford(n + 1, super_edges, super_source)

    if bf.has_negative_cycle:
        return None

    h = bf.dist
    reweighted_edges = [
        (v, w, wt + h[v] - h[w])
        for v, w, wt in edges
    ]

    g = [[] for _ in range(n)]

    for v, w, wt in reweighted_edges:
        g[v].append((w, wt))

    all_dist = []

    for s in range(n):
        sp = dijkstra(g, s)

        row = [
            sp.dist[t] - h[s] + h[t]
            if sp.dist[t] < INF else INF
            for t in range(n)
        ]

        all_dist.append(row)

    return all_dist


class DSU:
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
        ra, rb = self.find(a), self.find(b)

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

    def component_size(self, x):
        return self.size[self.find(x)]


class MSTResult:
    def __init__(self, weight, edges):
        self.weight = weight
        self.edges = edges


def kruskal_mst(n, edges):
    dsu = DSU(n)
    mst = []
    total = 0

    for v, w, wt in sorted(edges, key=lambda e: e[2]):
        if dsu.union(v, w):
            mst.append((v, w, wt))
            total += wt

            if len(mst) == n - 1:
                break

    return MSTResult(total, mst)


def prim_mst(g):
    marked = [False] * len(g)
    mst = []
    total = 0

    for s in range(len(g)):
        if marked[s]:
            continue

        pq = [(0, s, -1)]

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


def bridges(g):
    timer = 0
    tin = [-1] * len(g)
    low = [-1] * len(g)
    result = []

    def visit(v, parent):
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


def articulation_points(g):
    timer = 0
    tin = [-1] * len(g)
    low = [-1] * len(g)
    points = set()

    def visit(v, parent):
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


DIR4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIR8 = DIR4 + [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def inside(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def neighbors4(grid, r, c):
    for dr, dc in DIR4:
        nr, nc = r + dr, c + dc

        if inside(grid, nr, nc):
            yield nr, nc


def neighbors8(grid, r, c):
    for dr, dc in DIR8:
        nr, nc = r + dr, c + dc

        if inside(grid, nr, nc):
            yield nr, nc


def cell_id(grid, r, c):
    return r * len(grid[0]) + c


def cell_pos(grid, v):
    return divmod(v, len(grid[0]))
