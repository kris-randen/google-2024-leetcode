"""

200. Number of Islands
Solved
Medium

Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.



Example 1:

Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1
Example 2:

Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3


Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 300
grid[i][j] is '0' or '1'.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
4,172,786/6.5M
Acceptance Rate
64.3%

"""

from typing import List, Iterator, Callable

Cell = tuple[int, int]
Grid = list[list[str]]


def rows(grid: Grid) -> int:
    return len(grid)

def cols(grid: Grid) -> int:
    return len(grid[0]) if grid else 0

DIRS4: tuple[Cell, ...] = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


def value(grid: Grid, p: Cell) -> str:
    r, c = p
    return grid[r][c]

def add(p: Cell, q: Cell) -> Cell:
    return p[0] + q[0], p[1] + q[1]

def inbounds(grid: Grid, p: Cell) -> bool:
    r, c = p
    return 0 <= r < rows(grid) and 0 <= c < cols(grid)

def cells(grid: Grid) -> Iterator[Cell]:
    for r in range(rows(grid)):
        for c in range(cols(grid)):
            yield r, c

def neighbors(
        grid: Grid,
        p: Cell,
        dirs: tuple[Cell, ...] = DIRS4
) -> Iterator[Cell]:
    for d in dirs:
        q = add(p, d)

        if inbounds(grid, q):
            yield q

def valid_neighbors(
        grid: Grid,
        p: Cell,
        valid: Callable[[Cell], bool],
        dirs: tuple[Cell, ...] = DIRS4
) -> Iterator[Cell]:
    return (for q in neighbors(grid, p, dirs) if valid(q))

def is_land(grid: Grid, p: Cell) -> bool:
    return value(grid, p) == "1"

def sink_island(
        grid: Grid,
        p: Cell
):
    r, c = p
    grid[r][c] = "0"

    for q in valid_neighbors(grid, p, lambda r: is_land(grid, r)):
        sink_island(grid, q)

def num_islands(grid: Grid) -> int:
    count = 0

    for p in cells(grid):
        if is_land(grid, p):
            count += 1
            sink_island(grid, p)

    return count

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        return num_islands(grid)
