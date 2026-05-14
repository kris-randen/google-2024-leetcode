"""

994. Rotting Oranges
Solved
Medium

You are given an m x n grid where each cell can have one of three values:

0 representing an empty cell,
1 representing a fresh orange, or
2 representing a rotten orange.
Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.



Example 1:


Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4
Example 2:

Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
Output: -1
Explanation: The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.
Example 3:

Input: grid = [[0,2]]
Output: 0
Explanation: Since there are already no fresh oranges at minute 0, the answer is just 0.


Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 10
grid[i][j] is 0, 1, or 2.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,654,069/2.8M
Acceptance Rate
58.6%

"""

from collections import deque
from collections.abc import Callable
from typing import List, Iterator

Grid = list[list[int]]
Cell = tuple[int, int]

DIRS4: tuple[Cell, ...] = \
    (
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    )

def rows(grid: Grid) -> int:
    return len(grid)

def cols(grid: Grid) -> int:
    return len(grid[0]) if grid else 0

def in_bounds(grid: Grid, p: Cell) -> bool:
    r, c = p
    return 0 <= r < rows(grid) and 0 <= c < cols(grid)

def cells(grid: Grid) -> Iterator[Cell]:
    for r in range(rows(grid)):
        for c in range(cols(grid)):
            yield r, c

def value(grid: Grid, p: Cell) -> int:
    r, c = p
    return grid[r][c]

def set_value(grid: Grid, p: Cell, val: int) -> None:
    r, c = p
    grid[r][c] = val

def rot(grid: Grid, p: Cell) -> None:
    set_value(grid, p, 2)

def add(p: Cell, q: Cell) -> Cell:
    return p[0] + q[0], p[1] + q[1]

def is_empty(grid: Grid, p: Cell) -> bool:
    return value(grid, p) == 0

def is_fresh(grid: Grid, p: Cell) -> bool:
    return value(grid, p) == 1

def is_rotten(grid: Grid, p: Cell) -> bool:
    return value(grid, p) == 2

def rotten_cells(grid: Grid) -> Iterator[Cell]:
    return (p for p in cells(grid) if is_rotten(grid, p))

def fresh_count(grid: Grid) -> int:
    return sum(1 for p in cells(grid) if is_fresh(grid, p))

def fresh_neighbors(grid: Grid, p: Cell) -> Iterator[Cell]:
    return valid_neighbors(grid, p, lambda q: is_fresh(grid, q))

def neighbors(
        grid: Grid,
        p: Cell,
        dirs: tuple[Cell, ...] = DIRS4
):
    for d in dirs:
        q = add(p, d)

        if in_bounds(grid, q):
            yield q

def valid_neighbors(
        grid: Grid,
        p: Cell,
        valid: Callable[[Cell], bool],
        dirs: tuple[Cell, ...] = DIRS4
):
    return (q for q in neighbors(grid, p, dirs) if valid(q))


def minutes_to_rot_all(grid: Grid):
    q = deque(rotten_cells(grid))
    fresh = fresh_count(grid)
    minutes = 0

    while q and fresh:
        for _ in range(len(q)):
            p = q.popleft()

            for nbr in fresh_neighbors(grid, p):
                rot(grid, nbr)
                fresh -= 1
                q.append(nbr)

        minutes += 1

    return minutes if not fresh else -1


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        return minutes_to_rot_all(grid)
