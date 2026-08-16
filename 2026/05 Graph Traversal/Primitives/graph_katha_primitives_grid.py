from collections import deque
from heapq import heappop, heappush


INF = float("inf")

DIR4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIR8 = DIR4 + [(1, 1), (1, -1), (-1, 1), (-1, -1)]


# =============================================================================
# Basic grid navigation
# =============================================================================

def rows(grid):
    return len(grid)


def cols(grid):
    return len(grid[0]) if grid else 0


def inside(grid, r, c):
    return 0 <= r < rows(grid) and 0 <= c < cols(grid)


def cells(grid):
    for r in range(rows(grid)):
        for c in range(cols(grid)):
            yield r, c


def neighbors(grid, r, c, dirs=DIR4):
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc

        if inside(grid, nr, nc):
            yield nr, nc


def on_boundary(grid, r, c):
    return r == 0 or c == 0 or r == rows(grid) - 1 or c == cols(grid) - 1


def boundary_cells(grid):
    seen = set()

    for r in range(rows(grid)):
        for c in (0, cols(grid) - 1):
            if inside(grid, r, c) and (r, c) not in seen:
                seen.add((r, c))
                yield r, c

    for c in range(cols(grid)):
        for r in (0, rows(grid) - 1):
            if inside(grid, r, c) and (r, c) not in seen:
                seen.add((r, c))
                yield r, c


def cell_id(grid, r, c):
    return r * cols(grid) + c


def cell_pos(grid, v):
    return divmod(v, cols(grid))


# =============================================================================
# Flood fill / connected components
# =============================================================================

def flood_fill(grid, sr, sc, good, seen=None, dirs=DIR4):
    if seen is None:
        seen = set()

    if not inside(grid, sr, sc) or (sr, sc) in seen or not good(sr, sc):
        return []

    stack = [(sr, sc)]
    seen.add((sr, sc))
    comp = []

    while stack:
        r, c = stack.pop()
        comp.append((r, c))

        for nr, nc in neighbors(grid, r, c, dirs):
            if (nr, nc) not in seen and good(nr, nc):
                seen.add((nr, nc))
                stack.append((nr, nc))

    return comp


def grid_components(grid, good, dirs=DIR4):
    seen = set()
    comps = []

    for r, c in cells(grid):
        if (r, c) not in seen and good(r, c):
            comps.append(flood_fill(grid, r, c, good, seen, dirs))

    return comps


def count_grid_components(grid, good, dirs=DIR4):
    seen = set()
    count = 0

    for r, c in cells(grid):
        if (r, c) not in seen and good(r, c):
            flood_fill(grid, r, c, good, seen, dirs)
            count += 1

    return count


def max_component_size(grid, good, dirs=DIR4):
    seen = set()
    best = 0

    for r, c in cells(grid):
        if (r, c) not in seen and good(r, c):
            comp = flood_fill(grid, r, c, good, seen, dirs)
            best = max(best, len(comp))

    return best


def count_valid_components(grid, good, valid, dirs=DIR4):
    seen = set()
    count = 0

    for r, c in cells(grid):
        if (r, c) not in seen and good(r, c):
            comp = flood_fill(grid, r, c, good, seen, dirs)

            if all(valid(x, y) for x, y in comp):
                count += 1

    return count


def count_closed_components(grid, good, dirs=DIR4):
    return count_valid_components(
        grid,
        good,
        valid=lambda r, c: not on_boundary(grid, r, c),
        dirs=dirs
    )


def erase_component(grid, sr, sc, old, new, dirs=DIR4):
    if not inside(grid, sr, sc) or grid[sr][sc] != old:
        return 0

    stack = [(sr, sc)]
    grid[sr][sc] = new
    size = 0

    while stack:
        r, c = stack.pop()
        size += 1

        for nr, nc in neighbors(grid, r, c, dirs):
            if grid[nr][nc] == old:
                grid[nr][nc] = new
                stack.append((nr, nc))

    return size


def first_component(grid, good, dirs=DIR4):
    seen = set()

    for r, c in cells(grid):
        if good(r, c):
            return flood_fill(grid, r, c, good, seen, dirs)

    return []


# =============================================================================
# Boundary reachability
# =============================================================================

def boundary_reachable(grid, good, dirs=DIR4):
    seen = set()

    for r, c in boundary_cells(grid):
        if (r, c) not in seen and good(r, c):
            flood_fill(grid, r, c, good, seen, dirs)

    return seen


def unsafe_cells(grid, good, dirs=DIR4):
    safe = boundary_reachable(grid, good, dirs)

    return [
        (r, c)
        for r, c in cells(grid)
        if good(r, c) and (r, c) not in safe
    ]


# =============================================================================
# Grid BFS
# =============================================================================

def grid_bfs(grid, start, good, dirs=DIR4):
    dist = [[-1] * cols(grid) for _ in range(rows(grid))]
    edge_to = {}

    sr, sc = start

    if not inside(grid, sr, sc) or not good(sr, sc):
        return dist, edge_to

    q = deque([(sr, sc)])
    dist[sr][sc] = 0

    while q:
        r, c = q.popleft()

        for nr, nc in neighbors(grid, r, c, dirs):
            if dist[nr][nc] == -1 and good(nr, nc):
                dist[nr][nc] = dist[r][c] + 1
                edge_to[(nr, nc)] = (r, c)
                q.append((nr, nc))

    return dist, edge_to


def grid_path(edge_to, start, target):
    path = []
    curr = target

    while curr is not None:
        path.append(curr)

        if curr == start:
            return path[::-1]

        curr = edge_to.get(curr)

    return []


def shortest_path_grid(grid, start, target, good, dirs=DIR4):
    dist, _ = grid_bfs(grid, start, good, dirs)
    tr, tc = target

    if not inside(grid, tr, tc):
        return -1

    return dist[tr][tc]


def multi_source_grid_bfs(grid, sources, good=lambda r, c: True, dirs=DIR4):
    dist = [[-1] * cols(grid) for _ in range(rows(grid))]
    q = deque()

    for r, c in sources:
        if inside(grid, r, c) and dist[r][c] == -1:
            dist[r][c] = 0
            q.append((r, c))

    while q:
        r, c = q.popleft()

        for nr, nc in neighbors(grid, r, c, dirs):
            if dist[nr][nc] == -1 and good(nr, nc):
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))

    return dist


def grid_bfs_levels(grid, sources, good=lambda r, c: True, dirs=DIR4):
    seen = set()
    q = deque()

    for r, c in sources:
        if inside(grid, r, c) and (r, c) not in seen:
            seen.add((r, c))
            q.append((r, c))

    level = 0

    while q:
        current = []

        for _ in range(len(q)):
            r, c = q.popleft()
            current.append((r, c))

            for nr, nc in neighbors(grid, r, c, dirs):
                if (nr, nc) not in seen and good(nr, nc):
                    seen.add((nr, nc))
                    q.append((nr, nc))

        yield level, current
        level += 1


# =============================================================================
# Reverse reachability / monotone grid flow
# =============================================================================

def reverse_monotone_reachable(grid, sources, can_reverse_enter, dirs=DIR4):
    seen = set()
    q = deque()

    for r, c in sources:
        if inside(grid, r, c) and (r, c) not in seen:
            seen.add((r, c))
            q.append((r, c))

    while q:
        r, c = q.popleft()

        for nr, nc in neighbors(grid, r, c, dirs):
            if (nr, nc) not in seen and can_reverse_enter(r, c, nr, nc):
                seen.add((nr, nc))
                q.append((nr, nc))

    return seen


def pacific_sources(grid):
    return [(0, c) for c in range(cols(grid))] + [
        (r, 0) for r in range(rows(grid))
    ]


def atlantic_sources(grid):
    m, n = rows(grid), cols(grid)

    return [(m - 1, c) for c in range(n)] + [
        (r, n - 1) for r in range(m)
    ]


# =============================================================================
# Weighted grid shortest paths
# =============================================================================

def zero_one_bfs_grid(grid, start, edge_cost, good=lambda r, c: True, dirs=DIR4):
    dist = [[INF] * cols(grid) for _ in range(rows(grid))]
    sr, sc = start

    if not inside(grid, sr, sc) or not good(sr, sc):
        return dist

    dq = deque([(sr, sc)])
    dist[sr][sc] = 0

    while dq:
        r, c = dq.popleft()

        for nr, nc in neighbors(grid, r, c, dirs):
            if not good(nr, nc):
                continue

            wt = edge_cost(r, c, nr, nc)
            nd = dist[r][c] + wt

            if nd < dist[nr][nc]:
                dist[nr][nc] = nd

                if wt == 0:
                    dq.appendleft((nr, nc))
                else:
                    dq.append((nr, nc))

    return dist


def dijkstra_grid(grid, start, edge_cost, good=lambda r, c: True, dirs=DIR4):
    dist = [[INF] * cols(grid) for _ in range(rows(grid))]
    sr, sc = start

    if not inside(grid, sr, sc) or not good(sr, sc):
        return dist

    dist[sr][sc] = 0
    pq = [(0, sr, sc)]

    while pq:
        d, r, c = heappop(pq)

        if d != dist[r][c]:
            continue

        for nr, nc in neighbors(grid, r, c, dirs):
            if not good(nr, nc):
                continue

            nd = d + edge_cost(r, c, nr, nc)

            if nd < dist[nr][nc]:
                dist[nr][nc] = nd
                heappush(pq, (nd, nr, nc))

    return dist


def minimax_dijkstra_grid(grid, start, edge_cost, good=lambda r, c: True, dirs=DIR4):
    dist = [[INF] * cols(grid) for _ in range(rows(grid))]
    sr, sc = start

    if not inside(grid, sr, sc) or not good(sr, sc):
        return dist

    dist[sr][sc] = 0
    pq = [(0, sr, sc)]

    while pq:
        d, r, c = heappop(pq)

        if d != dist[r][c]:
            continue

        for nr, nc in neighbors(grid, r, c, dirs):
            if not good(nr, nc):
                continue

            nd = max(d, edge_cost(r, c, nr, nc))

            if nd < dist[nr][nc]:
                dist[nr][nc] = nd
                heappush(pq, (nd, nr, nc))

    return dist


# =============================================================================
# Grid DAG / DFS memo
# =============================================================================

def increasing_path_dp(grid, value):
    memo = {}

    def dp(r, c):
        if (r, c) in memo:
            return memo[(r, c)]

        best = 1

        for nr, nc in neighbors(grid, r, c):
            if value(nr, nc) > value(r, c):
                best = max(best, 1 + dp(nr, nc))

        memo[(r, c)] = best
        return best

    return dp


def longest_increasing_path(grid):
    if not grid:
        return 0

    dp = increasing_path_dp(grid, value=lambda r, c: grid[r][c])
    return max(dp(r, c) for r, c in cells(grid))


# =============================================================================
# Grid DSU
# =============================================================================

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


def grid_dsu(grid, good, dirs=DIR4):
    dsu = DSU(rows(grid) * cols(grid))
    active = set()

    for r, c in cells(grid):
        if not good(r, c):
            continue

        v = cell_id(grid, r, c)
        active.add(v)

        for nr, nc in neighbors(grid, r, c, dirs):
            if good(nr, nc):
                dsu.union(v, cell_id(grid, nr, nc))

    return dsu, active


def count_dsu_components(dsu, active):
    return len({dsu.find(v) for v in active})


# =============================================================================
# Representative LeetCode-style compositions
# =============================================================================

def num_islands(grid):
    return count_grid_components(
        grid,
        good=lambda r, c: grid[r][c] == "1"
    )


def max_area_of_island(grid):
    return max_component_size(
        grid,
        good=lambda r, c: grid[r][c] == 1
    )


def update_matrix(mat):
    sources = [
        (r, c)
        for r, c in cells(mat)
        if mat[r][c] == 0
    ]

    return multi_source_grid_bfs(mat, sources)


def rotting_oranges(grid):
    rotten = []

    for r, c in cells(grid):
        if grid[r][c] == 2:
            rotten.append((r, c))

    dist = multi_source_grid_bfs(
        grid,
        rotten,
        good=lambda r, c: grid[r][c] == 1
    )

    ans = 0

    for r, c in cells(grid):
        if grid[r][c] == 1:
            if dist[r][c] == -1:
                return -1
            ans = max(ans, dist[r][c])

    return ans


def shortest_path_binary_matrix(grid):
    if not grid or grid[0][0] != 0 or grid[-1][-1] != 0:
        return -1

    dist, _ = grid_bfs(
        grid,
        (0, 0),
        good=lambda r, c: grid[r][c] == 0,
        dirs=DIR8
    )

    ans = dist[rows(grid) - 1][cols(grid) - 1]
    return -1 if ans == -1 else ans + 1


def num_enclaves(grid):
    safe = boundary_reachable(
        grid,
        good=lambda r, c: grid[r][c] == 1
    )

    return sum(
        grid[r][c] == 1 and (r, c) not in safe
        for r, c in cells(grid)
    )


def pacific_atlantic(heights):
    pac = reverse_monotone_reachable(
        heights,
        pacific_sources(heights),
        can_reverse_enter=lambda r, c, nr, nc: heights[nr][nc] >= heights[r][c]
    )

    atl = reverse_monotone_reachable(
        heights,
        atlantic_sources(heights),
        can_reverse_enter=lambda r, c, nr, nc: heights[nr][nc] >= heights[r][c]
    )

    return list(pac & atl)


def shortest_bridge(grid):
    first = first_component(
        grid,
        good=lambda r, c: grid[r][c] == 1
    )

    if not first:
        return -1

    q = deque((r, c, 0) for r, c in first)
    seen = set(first)

    while q:
        r, c, d = q.popleft()

        for nr, nc in neighbors(grid, r, c):
            if (nr, nc) in seen:
                continue

            if grid[nr][nc] == 1:
                return d

            seen.add((nr, nc))
            q.append((nr, nc, d + 1))

    return -1


def minimum_effort_path(heights):
    dist = minimax_dijkstra_grid(
        heights,
        (0, 0),
        edge_cost=lambda r, c, nr, nc: abs(heights[r][c] - heights[nr][nc])
    )

    return dist[rows(heights) - 1][cols(heights) - 1]


def minimum_obstacles(grid):
    dist = zero_one_bfs_grid(
        grid,
        (0, 0),
        edge_cost=lambda r, c, nr, nc: grid[nr][nc]
    )

    return dist[rows(grid) - 1][cols(grid) - 1]
