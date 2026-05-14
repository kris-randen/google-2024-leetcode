"""

286. Walls and Gates
Medium
Topics
conpanies icon
Companies
You are given an m x n grid rooms initialized with these three possible values.

-1 A wall or an obstacle.
0 A gate.
INF Infinity means an empty room. We use the value 231 - 1 = 2147483647 to represent INF as you may assume that the distance to a gate is less than 2147483647.
Fill each empty room with the distance to its nearest gate. If it is impossible to reach a gate, it should be filled with INF.



Example 1:


Input: rooms = [[2147483647,-1,0,2147483647],[2147483647,2147483647,2147483647,-1],[2147483647,-1,2147483647,-1],[0,-1,2147483647,2147483647]]
Output: [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]
Example 2:

Input: rooms = [[-1]]
Output: [[-1]]


Constraints:

m == rooms.length
n == rooms[i].length
1 <= m, n <= 250
rooms[i][j] is -1, 0, or 231 - 1.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
428,168/669.3K
Acceptance Rate
64.0%

"""

from collections import deque
from collections.abc import Callable
from typing import List, Iterator

Grid = list[list[int]]
Cell = tuple[int, int]

DIRS4: tuple[Cell, ...] = (
(0, 1),
(1, 0),
(0, -1),
(-1, 0)
)

EMPTY = 2147483647
WALL = -1
GATE = 0

def rows(grid: Grid) -> int:
    return len(grid)

def cols(grid: Grid) -> int:
    return len(grid[0]) if grid else 0

def cells(grid: Grid) -> Iterator[Cell]:
    for r in range(rows(grid)):
        for c in range(cols(grid)):
            yield r, c

def value(grid: Grid, p: Cell) -> int:
    r, c = p
    return grid[r][c]

def set_value(grid: Grid, p: Cell, val: int):
    r, c = p
    grid[r][c] = val

def add(p: Cell, q: Cell) -> Cell:
    return p[0] + q[0], p[1] + q[1]

def is_empty(grid: Grid, p: Cell) -> bool:
    return value(grid, p) == EMPTY

def is_a_wall(grid: Grid, p: Cell) -> bool:
    return value(grid, p) == WALL

def is_a_gate(grid: Grid, p: Cell) -> bool:
    return value(grid, p) == GATE

def in_bounds(grid: Grid, p: Cell) -> bool:
    r, c = p
    return 0 <= r < rows(grid) and 0 <= c < cols(grid)

def neighbors(grid: Grid, p: Cell, dirs: tuple[Cell, ...] = DIRS4) -> bool:
    for d in dirs:
        q = add(p, d)

        if in_bounds(grid, q):
            yield q

def valid_neighbors(grid: Grid, p: Cell, valid: Callable[[Cell], bool], dirs: tuple[Cell, ...] = DIRS4):
    return (q for q in neighbors(grid, p, dirs) if valid(q))

def empty_neighbors(grid: Grid, p: Cell) -> Iterator[Cell]:
    return (q for q in valid_neighbors(grid, p, lambda q: is_empty(grid, q)))

def empty_rooms(grid: Grid) -> Iterator[Cell]:
    return (p for p in cells(grid) if is_empty(grid, p))

def gates(grid: Grid) -> Iterator[Cell]:
    return (p for p in cells(grid) if is_a_gate(grid, p))

def mark_empty_rooms(grid: Grid):
    q = deque(gates(grid))
    level = 0

    while q:
        for _ in range(len(q)):
            p = q.popleft()

            for nbr in empty_neighbors(grid, p):
                set_value(grid, nbr, value(grid, p) + 1)
                q.append(nbr)


class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        mark_empty_rooms(rooms)
