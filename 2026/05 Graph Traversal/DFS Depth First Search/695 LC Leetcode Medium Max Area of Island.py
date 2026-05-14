"""

695. Max Area of Island
Solved
Medium
Topics
conpanies icon
Companies
You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.

The area of an island is the number of cells with a value 1 in the island.

Return the maximum area of an island in grid. If there is no island, return 0.



Example 1:


Input: grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
Output: 6
Explanation: The answer is not 11, because the island must be connected 4-directionally.
Example 2:

Input: grid = [[0,0,0,0,0,0,0,0]]
Output: 0


Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 50
grid[i][j] is either 0 or 1.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,245,114/1.7M
Acceptance Rate
74.0%

"""
from collections.abc import Callable
from typing import Iterator, List

Cell = tuple[int, int]
Grid = list[list[int]]

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

def value(grid: Grid, p: Cell) -> str:
    r, c = p
    return grid[r][c]

def add(p: Cell, q: Cell) -> Cell:
    return p[0] + q[0], p[1] + q[1]

def in_bounds(grid: Grid, p: Cell) -> bool:
    r, c = p
    return 0 <= r < rows(grid) and 0 <= c < cols(grid)

def is_land(grid: Grid, p: Cell) -> bool:
    return value(grid, p) == 1

def neighbors(
        grid: Grid,
        p: Cell,
        dirs: tuple[Cell, ...] = DIRS4
) -> Iterator[Cell]:
    for d in dirs:
        q = add(p, d)

        if in_bounds(grid, q):
            yield q

def valid_neighbors(
        grid: Grid,
        p: Cell,
        valid: Callable[[Cell], bool],
        dirs: tuple[Cell, ...] = DIRS4
) -> Iterator[Cell]:
    return (q for q in neighbors(grid, p, dirs) if valid(q))

def unseen_land(
        grid: Grid,
        p: Cell,
        seen: set[Cell]
) -> bool:
    return p not in seen and is_land(grid, p)


def component_size(
        grid: Grid,
        start: Cell,
        seen: set[Cell]
) -> int:
    size = 0

    def dfs(p: Cell) -> None:
        nonlocal size

        seen.add(p)
        size += 1

        for q in valid_neighbors(grid, p, lambda q: unseen_land(grid, q, seen)):
            dfs(q)

    dfs(start)
    return size

def max_component(grid: Grid):
    max_size, seen = 0, set()

    for p in cells(grid):
        if unseen_land(grid, p, seen):
            size = component_size(grid, p, seen)
            max_size = max(max_size, size)

    return max_size


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        return max_component(grid)
