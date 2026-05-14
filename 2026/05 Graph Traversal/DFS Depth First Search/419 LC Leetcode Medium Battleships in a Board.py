"""

419. Battleships in a Board
Medium

Given an m x n matrix board where each cell is a battleship 'X' or empty '.', return the number of the battleships on board.

Battleships can only be placed horizontally or vertically on board. In other words, they can only be made of the shape 1 x k (1 row, k columns) or k x 1 (k rows, 1 column), where k can be of any size. At least one horizontal or vertical cell separates between two battleships (i.e., there are no adjacent battleships).



Example 1:


Input: board = [["X",".",".","X"],[".",".",".","X"],[".",".",".","X"]]
Output: 2
Example 2:

Input: board = [["."]]
Output: 0


Constraints:

m == board.length
n == board[i].length
1 <= m, n <= 200
board[i][j] is either '.' or 'X'.


Follow up: Could you do it in one-pass, using only O(1) extra memory and without modifying the values board?


Seen this question in a real interview before?
1/6
Yes
No
Accepted
285,240/368K
Acceptance Rate
77.5%

"""

from typing import List, Iterator, Callable

Grid = list[list[str]]
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

def value(grid: Grid, p: Cell) -> str:
    r, c = p
    return grid[r][c]

def set_value(grid: Grid, p: Cell, val: str):
    r, c = p
    grid[r][c] = val


def in_bounds(grid: Grid, p: Cell) -> bool:
    r, c = p
    return 0 <= r < rows(grid) and 0 <= c < cols(grid)

def add(p: Cell, q: Cell) -> Cell:
    return p[0] + q[0], p[1] + q[1]

def neighbors(grid: Grid, p: Cell, dirs: tuple[Cell, ...] = DIRS4) -> Iterator[Cell]:
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


def is_ship(grid: Grid, p: Cell) -> bool:
    return value(grid, p) == "X"

def is_water(grid: Grid, p: Cell) -> bool:
    return value(grid, p) == "."


def count_ship(grid: Grid, p: Cell):
    if not is_ship(grid, p):
        return

    set_value(grid, p, "Y")
    for nbr in valid_neighbors(grid, p, lambda q: is_ship(grid, q)):
        count_ship(grid, nbr)

def count_all_ships(grid: Grid):
    count = 0

    for p in cells(grid):
        if is_ship(grid, p):
            count += 1
            count_ship(grid, p)

    return count



class Solution:
    def countBattleships(self, board: List[List[str]]) -> int:
        return count_all_ships(board)
