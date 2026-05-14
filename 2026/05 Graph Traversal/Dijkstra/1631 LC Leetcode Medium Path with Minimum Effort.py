"""

1631. Path With Minimum Effort
Solved
Medium

You are a hiker preparing for an upcoming hike. You are given heights, a 2D array of size rows x columns, where heights[row][col] represents the height of cell (row, col). You are situated in the top-left cell, (0, 0), and you hope to travel to the bottom-right cell, (rows-1, columns-1) (i.e., 0-indexed). You can move up, down, left, or right, and you wish to find a route that requires the minimum effort.

A route's effort is the maximum absolute difference in heights between two consecutive cells of the route.

Return the minimum effort required to travel from the top-left cell to the bottom-right cell.



Example 1:



Input: heights = [[1,2,2],[3,8,2],[5,3,5]]
Output: 2
Explanation: The route of [1,3,5,3,5] has a maximum absolute difference of 2 in consecutive cells.
This is better than the route of [1,2,2,2,5], where the maximum absolute difference is 3.
Example 2:



Input: heights = [[1,2,3],[3,8,4],[5,3,5]]
Output: 1
Explanation: The route of [1,2,3,4,5] has a maximum absolute difference of 1 in consecutive cells, which is better than route [1,3,5,3,5].
Example 3:


Input: heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
Output: 0
Explanation: This route does not require any effort.


Constraints:

rows == heights.length
columns == heights[i].length
1 <= rows, columns <= 100
1 <= heights[i][j] <= 106

Seen this question in a real interview before?
1/6
Yes
No
Accepted
462,327/731.9K
Acceptance Rate
63.2%

"""

from cmath import inf
from heapq import heappop, heappush
from typing import List, Iterator

Grid = List[List[int]]
Cell = tuple[int, int]

DIRS4: tuple[Cell, ...] = (
(0, 1),
(1, 0),
(0, -1),
(-1, 0)
)

def rows(grid: Grid) -> int:
    return len(grid)

def cols(grid: Grid) -> int:
    return len(grid[0]) if grid else 0

def cells(grid: Grid) -> Iterator[Cell]:
    for r in range(rows(grid)):
        for c in range(cols(grid)):
            yield r, c


def in_bounds(grid: Grid, p: Cell) -> bool:
    r, c = p
    return 0 <= r < rows(grid) and 0 <= c < cols(grid)

def value(grid: Grid, p: Cell) -> int:
    r, c = p
    return grid[r][c]

def add(p: Cell, q: Cell) -> Cell:
    return p[0] + q[0], p[1] + q[1]

def neighbors(
        grid: Grid,
        p: Cell,
        dirs: tuple[Cell, ...] = DIRS4
):
    for d in dirs:
        q = add(p, d)

        if in_bounds(grid, q):
            yield q

def length(grid, u, du, v):
    return max(du, abs(value(grid, u) - value(grid, v)))

def dijkstra(grid, source):
    dist = {p: inf for p in cells(grid)}
    dist[source] = 0
    pq = [(0, source)]

    while pq:
        du, u = heappop(pq)
        if du > dist[u]:
            continue

        for v in neighbors(grid, u):
            dv = length(grid, u, du, v)
            if dv < dist[v]:
                dist[v] = dv
                heappush(pq, (dv, v))

    return dist


def min_path(grid: Grid, source: Cell, destination: Cell) -> int:
    dist = dijkstra(grid, source)
    return dist[destination]

class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        return min_path(heights, (0, 0), (rows(heights) - 1, cols(heights) - 1))
