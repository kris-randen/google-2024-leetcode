"""

529. Minesweeper
Solved
Medium
Topics
Companies
Let's play the minesweeper game (Wikipedia, online game)!

You are given an m x n char matrix board representing the game board where:

'M' represents an unrevealed mine,
'E' represents an unrevealed empty square,
'B' represents a revealed blank square that has no adjacent mines (i.e., above, below, left, right, and all 4 diagonals),
digit ('1' to '8') represents how many mines are adjacent to this revealed square, and
'X' represents a revealed mine.
You are also given an integer array click where click = [clickr, clickc] represents the next click position among all the unrevealed squares ('M' or 'E').

Return the board after revealing this position according to the following rules:

If a mine 'M' is revealed, then the game is over. You should change it to 'X'.
If an empty square 'E' with no adjacent mines is revealed, then change it to a revealed blank 'B' and all of its adjacent unrevealed squares should be revealed recursively.
If an empty square 'E' with at least one adjacent mine is revealed, then change it to a digit ('1' to '8') representing the number of adjacent mines.
Return the board when no more squares will be revealed.


Example 1:


Input: board = [["E","E","E","E","E"],["E","E","M","E","E"],["E","E","E","E","E"],["E","E","E","E","E"]], click = [3,0]
Output: [["B","1","E","1","B"],["B","1","M","1","B"],["B","1","1","1","B"],["B","B","B","B","B"]]
Example 2:


Input: board = [["B","1","E","1","B"],["B","1","M","1","B"],["B","1","1","1","B"],["B","B","B","B","B"]], click = [1,2]
Output: [["B","1","E","1","B"],["B","1","X","1","B"],["B","1","1","1","B"],["B","B","B","B","B"]]


Constraints:

m == board.length
n == board[i].length
1 <= m, n <= 50
board[i][j] is either 'M', 'E', 'B', or a digit from '1' to '8'.
click.length == 2
0 <= clickr < m
0 <= clickc < n
board[clickr][clickc] is either 'M' or 'E'.

"""
from typing import List


def dfs(b, p):
    def value(p):
        return b[p[0]][p[1]]

    def valid(p):
        return 0 <= p[0] < m and 0 <= p[1] < n

    def mine(p):
        return value(p) == 'M'

    def empty(p):
        return value(p) == 'E'

    def unmarked(p):
        return mine(p) or empty(p)

    def markx(p):
        b[p[0]][p[1]] = 'X'

    def markb(p):
        b[p[0]][p[1]] = 'B'

    def markd(p):
        b[p[0]][p[1]] = f'{digit(p)}'

    def up(p):
        return p[0] - 1, p[1]

    def dn(p):
        return p[0] + 1, p[1]

    def lt(p):
        return p[0], p[1] - 1

    def rt(p):
        return p[0], p[1] + 1

    def ul(p):
        return p[0] - 1, p[1] - 1

    def ur(p):
        return p[0] - 1, p[1] + 1

    def dl(p):
        return p[0] + 1, p[1] - 1

    def dr(p):
        return p[0] + 1, p[1] + 1

    def adj(p):
        return up(p), dn(p), lt(p), rt(p), ul(p), ur(p), dl(p), dr(p)

    def nbs(p):
        return (nb for nb in adj(p) if valid(nb))

    def nbe(p):
        return (nb for nb in nbs(p) if not mine(nb))

    def blank(p):
        return not any(mine(nb) for nb in nbs(p))

    def isdig(p):
        return any(mine(nb) for nb in nbs(p))

    def digit(p):
        return sum((1 if mine(nb) else 0) for nb in nbs(p))

    def visit(p):
        if mine(p):     markx(p); return
        if digit(p):    markd(p); return
        markb(p)
        for nb in nbe(p):
            if unmarked(nb): visit(nb)

    m, n = len(b), len(b[0]); visit(p)
    return b


class Solution:
    def updateBoard(self, b: List[List[str]], p: List[int]) -> List[List[str]]:
        return dfs(b, p)
