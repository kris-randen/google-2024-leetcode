"""
Part 4 — Grid Dynamic Programming Families

Scope:
    Unique Paths
    Unique Paths II
    Minimum Path Sum
    Triangle
    Minimum Falling Path Sum
    Minimum Falling Path Sum II
    Dungeon Game
    Out of Boundary Paths
    Knight Probability in Chessboard
    Number of Paths with Max Score
    Cherry Pickup I
    Cherry Pickup II

Core mental model:
    Grid DP = DP where the state space has geometry.

    Instead of dp[i], the basic state is usually:
        dp[r][c]

    But harder variants expand the state:
        dp[step][r][c]
        dp[r1][c1][r2][c2]
        dp[row][col1][col2]
        dp[move][r][c]

SRTBOT:
    S — Subproblems
    R — Relationships / neighbor transitions
    T — Topological order / evaluation order
    B — Base cases
    O — Original problem / answer extraction
    T — Time complexity = states × transition cost


# Part 4 — Grid DP

Python file first:

[Download Part 4 — Grid DP Python file](sandbox:/mnt/data/dp_part4_grid_dp.py)

## What Part 4 covers

```text
Grid DP
    -> basic forward grid DP
    -> obstacle grid DP
    -> min-cost grid DP
    -> triangle / ragged grid DP
    -> falling path DP
    -> reverse grid DP
    -> move-step distribution DP
    -> tuple-valued grid DP
    -> multi-agent grid DP
```

## Core mental model

Grid DP is where topological order becomes visually obvious.

```text
dp[r][c] = answer for a cell
```

But the meaning of “answer for a cell” changes by problem:

```text
ways to reach this cell
minimum cost to reach this cell
minimum health needed before entering this cell
probability of being at this cell after k moves
best score and count of best paths from this cell
best result with two agents at two columns
```

## Main state shapes

| Family                | State                                           | Order                             |
| --------------------- | ----------------------------------------------- | --------------------------------- |
| Unique Paths          | `dp[r][c] = ways to reach cell`                 | row-major                         |
| Minimum Path Sum      | `dp[r][c] = min cost to reach cell`             | row-major                         |
| Triangle              | `dp[row][c]` on ragged grid                     | row-major, backward column update |
| Falling Path          | `dp[r][c] = best path ending at cell`           | row-major                         |
| Dungeon Game          | `dp[r][c] = health needed before entering cell` | reverse grid                      |
| Out of Boundary Paths | `dp[move][r][c]`                                | increasing moves                  |
| Knight Probability    | probability distribution over cells             | increasing moves                  |
| Paths With Max Score  | `(best_score, count)` per cell                  | reverse grid                      |
| Cherry Pickup II      | `dp[row][c1][c2]`                               | row layers                        |
| Cherry Pickup I       | `dp[step][r1][r2]`                              | step layers                       |

## Most important traps

```text
1. Forward grid order is wrong when the state depends on the future.
2. Dungeon Game is not a max/min path-sum problem.
3. Obstacles are impossible states, not high-cost states.
4. Triangle rolling DP must update columns backward.
5. Cherry Pickup I is not two independent paths; it is two synchronized walkers.
6. If two agents land on the same cell, collect it once.
7. Some grid answers are at dp[-1][-1]; others are min/max over the final row.
```

## Composition chains

```text
cell state dp[r][c]
+ top/left predecessors
+ row-major order
-> Unique Paths / Minimum Path Sum
```

```text
cell state dp[r][c]
+ down/right successors
+ reverse grid order
-> Dungeon Game / Paths With Max Score
```

```text
move-layer state dp[move][r][c]
+ probability/count distribution
+ rolling layers
-> Out of Boundary Paths / Knight Probability
```

```text
two-agent row state dp[row][c1][c2]
+ 9 transition combinations
+ collect same cell once
-> Cherry Pickup II
```

```text
step state dp[step][r1][r2]
+ c1 = step - r1
+ c2 = step - r2
-> Cherry Pickup I
```

Next natural step: **Part 5 — Two-Sequence DP**.

"""

from __future__ import annotations

from functools import cache
from math import inf
from typing import Iterable


# =============================================================================
# Level 0 — Grid Utilities
# =============================================================================


def shape(grid: list[list[int]]) -> tuple[int, int]:
    return len(grid), len(grid[0]) if grid else 0


def in_bounds(rows: int, cols: int, r: int, c: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def top_left_predecessors(r: int, c: int) -> Iterable[tuple[int, int]]:
    """
    Predecessors for grids where movement is only down/right.

    If dp[r][c] means answer to reach (r, c), then predecessors are:
        (r - 1, c)
        (r, c - 1)
    """
    if r > 0:
        yield r - 1, c

    if c > 0:
        yield r, c - 1


def bottom_right_successors(rows: int, cols: int, r: int, c: int) -> Iterable[tuple[int, int]]:
    """
    Successors for reverse grid DP from target back to start.

    Used when dp[r][c] means answer needed from (r, c) to target.
    """
    if r + 1 < rows:
        yield r + 1, c

    if c + 1 < cols:
        yield r, c + 1


def falling_predecessor_cols(cols: int, c: int) -> Iterable[int]:
    """
    Predecessor columns for falling path problems:
        above-left, above, above-right
    """
    for pc in (c - 1, c, c + 1):
        if 0 <= pc < cols:
            yield pc


def four_dirs() -> tuple[tuple[int, int], ...]:
    return ((1, 0), (-1, 0), (0, 1), (0, -1))


def knight_dirs() -> tuple[tuple[int, int], ...]:
    return (
        (1, 2),
        (1, -2),
        (-1, 2),
        (-1, -2),
        (2, 1),
        (2, -1),
        (-2, 1),
        (-2, -1),
    )


# =============================================================================
# Level 1 — Basic Forward Grid DP
# =============================================================================


def unique_paths(rows: int, cols: int) -> int:
    """
    LeetCode:
        62. Unique Paths

    S:
        dp[r][c] = number of ways to reach cell (r, c).

    R:
        dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

    T:
        row-major order.

    B:
        first row and first column are 1.

    O:
        dp[rows - 1][cols - 1]

    T:
        O(rows * cols) time.
        O(cols) space with rolling row.
    """
    dp = [1] * cols

    for _ in range(1, rows):
        for c in range(1, cols):
            dp[c] += dp[c - 1]

    return dp[-1]


def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    """
    LeetCode:
        63. Unique Paths II

    Same as Unique Paths, but obstacle cells have 0 ways.

    S:
        dp[c] = number of ways to reach current row's cell c.

    R:
        if obstacle:
            dp[c] = 0
        else:
            dp[c] = from_top + from_left

    Trap:
        The starting cell can be blocked.
    """
    rows, cols = shape(grid)
    dp = [0] * cols
    dp[0] = 1 if grid[0][0] == 0 else 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                dp[c] = 0
            elif c > 0:
                dp[c] += dp[c - 1]

    return dp[-1]


def min_path_sum(grid: list[list[int]]) -> int:
    """
    LeetCode:
        64. Minimum Path Sum

    S:
        dp[r][c] = min path cost to reach cell (r, c).

    R:
        grid[r][c] + min(top, left)

    T:
        row-major.

    B:
        start cell has cost grid[0][0].

    O:
        target cell.

    Space:
        O(cols).
    """
    rows, cols = shape(grid)
    dp = [inf] * cols
    dp[0] = 0

    for r in range(rows):
        for c in range(cols):
            top = dp[c]
            left = dp[c - 1] if c > 0 else inf
            dp[c] = grid[r][c] + min(top, left)

    return int(dp[-1])


# =============================================================================
# Level 2 — Triangle / Ragged Grid DP
# =============================================================================


def minimum_total_triangle(triangle: list[list[int]]) -> int:
    """
    LeetCode:
        120. Triangle

    This is grid DP on a ragged triangular grid.

    S:
        dp[c] = min path sum to current row's c-th position.

    R:
        from previous row c-1 or c.

    T:
        row-major, but c must be processed backward if using one array.

    B:
        dp[0] = 0 before processing first row.

    O:
        min(dp over final row)

    Trap:
        Forward c update would overwrite dp[c - 1] before it is used.
    """
    dp = [inf] * (len(triangle) + 1)
    dp[0] = 0

    for row in triangle:
        for c in range(len(row) - 1, -1, -1):
            dp[c] = row[c] + min(dp[c], dp[c - 1] if c > 0 else inf)

    return int(min(dp[:len(triangle[-1])]))


# =============================================================================
# Level 3 — Falling Path DP
# =============================================================================


def min_falling_path_sum(grid: list[list[int]]) -> int:
    """
    LeetCode:
        931. Minimum Falling Path Sum

    S:
        dp[c] = min falling path sum ending at column c in previous row.

    R:
        curr[c] = grid[r][c] + min(prev[c - 1], prev[c], prev[c + 1])

    T:
        row by row.

    B:
        first row values.

    O:
        min over final row.
    """
    prev = grid[0][:]
    cols = len(prev)

    for row in grid[1:]:
        curr = [0] * cols

        for c, x in enumerate(row):
            curr[c] = x + min(prev[pc] for pc in falling_predecessor_cols(cols, c))

        prev = curr

    return min(prev)


def min_falling_path_sum_ii(grid: list[list[int]]) -> int:
    """
    LeetCode:
        1289. Minimum Falling Path Sum II

    Constraint:
        Cannot use same column as previous row.

    Naive recurrence:
        curr[c] = grid[r][c] + min(prev[pc] for pc != c)
        O(rows * cols^2)

    Optimization:
        Track smallest and second-smallest previous values.
        If c used previous smallest column, use second-smallest.
        Otherwise use smallest.

    T:
        O(rows * cols)
    """
    prev = grid[0][:]
    cols = len(prev)

    for row in grid[1:]:
        min1_val = inf
        min2_val = inf
        min1_col = -1

        for c, val in enumerate(prev):
            if val < min1_val:
                min2_val = min1_val
                min1_val = val
                min1_col = c
            elif val < min2_val:
                min2_val = val

        curr = [0] * cols

        for c, x in enumerate(row):
            best_prev = min2_val if c == min1_col else min1_val
            curr[c] = x + best_prev

        prev = curr

    return min(prev)


# =============================================================================
# Level 4 — Reverse Grid DP
# =============================================================================


def calculate_minimum_hp(dungeon: list[list[int]]) -> int:
    """
    LeetCode:
        174. Dungeon Game

    This is reverse grid DP.

    Wrong instinct:
        Find min/max path sum forward.

    Correct state:
        dp[r][c] = minimum health needed before entering cell (r, c)
                  so that knight can survive to the princess.

    R:
        need_after = min(dp[down], dp[right])
        need_here = max(1, need_after - dungeon[r][c])

    T:
        reverse row-major from bottom-right to top-left.

    B:
        princess cell.

    O:
        dp[0][0]

    Trap:
        Health must never drop below 1 at any point.
    """
    rows, cols = shape(dungeon)
    dp = [[inf] * (cols + 1) for _ in range(rows + 1)]

    dp[rows][cols - 1] = 1
    dp[rows - 1][cols] = 1

    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            need_after = min(dp[r + 1][c], dp[r][c + 1])
            dp[r][c] = max(1, need_after - dungeon[r][c])

    return int(dp[0][0])


# =============================================================================
# Level 5 — Move-Step Distribution DP
# =============================================================================


def find_paths_out_of_boundary(
    rows: int,
    cols: int,
    max_move: int,
    start_row: int,
    start_col: int,
) -> int:
    """
    LeetCode:
        576. Out of Boundary Paths

    S:
        dp[move][r][c] = number of ways to be at cell (r, c)
                         after exactly move moves.

    Instead of storing all moves, roll layers.

    R:
        From each in-bounds cell, move in 4 directions.
        If next cell is out of bounds, add to answer.

    T:
        increasing move count.

    B:
        one way to start at start cell with 0 moves.

    O:
        total exits over <= max_move moves.

    T:
        O(max_move * rows * cols * 4)
    """
    mod = 10**9 + 7
    curr = [[0] * cols for _ in range(rows)]
    curr[start_row][start_col] = 1
    total = 0

    for _ in range(max_move):
        nxt = [[0] * cols for _ in range(rows)]

        for r in range(rows):
            for c in range(cols):
                ways = curr[r][c]

                if ways == 0:
                    continue

                for dr, dc in four_dirs():
                    nr = r + dr
                    nc = c + dc

                    if in_bounds(rows, cols, nr, nc):
                        nxt[nr][nc] = (nxt[nr][nc] + ways) % mod
                    else:
                        total = (total + ways) % mod

        curr = nxt

    return total


def knight_probability(n: int, k: int, row: int, column: int) -> float:
    """
    LeetCode:
        688. Knight Probability in Chessboard

    S:
        prob[r][c] = probability of being at cell (r, c) after current move.

    R:
        Distribute probability equally to valid knight moves.

    T:
        increasing move count.

    B:
        probability 1 at starting cell.

    O:
        total probability remaining on board after k moves.
    """
    curr = [[0.0] * n for _ in range(n)]
    curr[row][column] = 1.0

    for _ in range(k):
        nxt = [[0.0] * n for _ in range(n)]

        for r in range(n):
            for c in range(n):
                p = curr[r][c]

                if p == 0:
                    continue

                share = p / 8.0

                for dr, dc in knight_dirs():
                    nr = r + dr
                    nc = c + dc

                    if in_bounds(n, n, nr, nc):
                        nxt[nr][nc] += share

        curr = nxt

    return sum(map(sum, curr))


# =============================================================================
# Level 6 — Path With Value + Count State
# =============================================================================


def paths_with_max_score(board: list[str]) -> list[int]:
    """
    LeetCode:
        1301. Number of Paths with Max Score

    Movement:
        From S to E, can move up, left, or diagonal up-left.
        Equivalently compute reverse from E to S.

    State:
        dp_score[r][c] = max score from cell to end.
        dp_count[r][c] = number of ways to achieve that max score.

    This demonstrates tuple-valued DP:
        each state stores (best_score, number_of_best_paths).

    Trap:
        Need to ignore blocked cells and impossible predecessor states.
    """
    mod = 10**9 + 7
    n = len(board)

    score = [[-inf] * n for _ in range(n)]
    count = [[0] * n for _ in range(n)]

    score[n - 1][n - 1] = 0
    count[n - 1][n - 1] = 1

    for r in range(n - 1, -1, -1):
        for c in range(n - 1, -1, -1):
            if board[r][c] == "X" or (r == n - 1 and c == n - 1):
                continue

            best = -inf
            ways = 0

            for nr, nc in ((r + 1, c), (r, c + 1), (r + 1, c + 1)):
                if not in_bounds(n, n, nr, nc):
                    continue

                candidate = score[nr][nc]

                if candidate > best:
                    best = candidate
                    ways = count[nr][nc]
                elif candidate == best:
                    ways = (ways + count[nr][nc]) % mod

            if ways == 0:
                continue

            cell = 0 if board[r][c] in "SE" else int(board[r][c])
            score[r][c] = best + cell
            count[r][c] = ways

    if count[0][0] == 0:
        return [0, 0]

    return [int(score[0][0]) % mod, count[0][0] % mod]


# =============================================================================
# Level 7 — Multi-Agent Grid DP
# =============================================================================


def cherry_pickup_ii(grid: list[list[int]]) -> int:
    """
    LeetCode:
        1463. Cherry Pickup II

    Two robots start at:
        (0, 0)
        (0, cols - 1)

    Both move one row down each step, with column delta in {-1, 0, 1}.

    State:
        dp[c1][c2] = max cherries after processing current row
                     with robot1 at c1 and robot2 at c2.

    R:
        transition from previous columns pc1, pc2.

    T:
        row by row.

    B:
        row 0 with robots at endpoints.

    O:
        max over dp after final row.

    Complexity:
        O(rows * cols^2 * 9)

    This is the cleanest multi-agent grid DP.
    """
    rows, cols = shape(grid)
    neg = -10**18

    dp = [[neg] * cols for _ in range(cols)]
    dp[0][cols - 1] = grid[0][0] + (grid[0][cols - 1] if cols > 1 else 0)

    for r in range(1, rows):
        nxt = [[neg] * cols for _ in range(cols)]

        for pc1 in range(cols):
            for pc2 in range(cols):
                prev = dp[pc1][pc2]

                if prev == neg:
                    continue

                for dc1 in (-1, 0, 1):
                    for dc2 in (-1, 0, 1):
                        c1 = pc1 + dc1
                        c2 = pc2 + dc2

                        if not (0 <= c1 < cols and 0 <= c2 < cols):
                            continue

                        gain = grid[r][c1]

                        if c1 != c2:
                            gain += grid[r][c2]

                        nxt[c1][c2] = max(nxt[c1][c2], prev + gain)

        dp = nxt

    return max(max(row) for row in dp)


def cherry_pickup(grid: list[list[int]]) -> int:
    """
    LeetCode:
        741. Cherry Pickup

    Classic transformation:
        A person going start -> end and back is equivalent to
        two people walking start -> end simultaneously.

    State compression:
        At step k:
            person1 at (r1, c1)
            person2 at (r2, c2)

        Since r + c = k:
            c1 = k - r1
            c2 = k - r2

        So state can be:
            dp[r1][r2] at current step k.

    R:
        each person came from up or left, so 4 predecessor combinations.

    T:
        increasing step k from 0 to 2n - 2.

    B:
        dp[0][0] = grid[0][0]

    O:
        dp[n-1][n-1] after final step.

    Trap:
        If both people stand on the same cell, count cherries once.
    """
    n = len(grid)
    neg = -10**18

    dp = [[neg] * n for _ in range(n)]
    dp[0][0] = grid[0][0]

    for k in range(1, 2 * n - 1):
        nxt = [[neg] * n for _ in range(n)]

        r_min = max(0, k - (n - 1))
        r_max = min(n - 1, k)

        for r1 in range(r_min, r_max + 1):
            c1 = k - r1

            if grid[r1][c1] == -1:
                continue

            for r2 in range(r_min, r_max + 1):
                c2 = k - r2

                if grid[r2][c2] == -1:
                    continue

                best_prev = neg

                for pr1 in (r1, r1 - 1):
                    for pr2 in (r2, r2 - 1):
                        pc1 = k - 1 - pr1
                        pc2 = k - 1 - pr2

                        if (
                            0 <= pr1 < n
                            and 0 <= pr2 < n
                            and 0 <= pc1 < n
                            and 0 <= pc2 < n
                        ):
                            best_prev = max(best_prev, dp[pr1][pr2])

                if best_prev == neg:
                    continue

                gain = grid[r1][c1]

                if r1 != r2:
                    gain += grid[r2][c2]

                nxt[r1][r2] = best_prev + gain

        dp = nxt

    return max(0, dp[n - 1][n - 1])


# =============================================================================
# Part 4 Problem Map
# =============================================================================


PART_4_PROBLEM_MAP = {
    "basic_forward_grid_dp": [
        62,
        63,
        64,
    ],
    "ragged_grid_dp": [
        120,
    ],
    "falling_path_dp": [
        931,
        1289,
    ],
    "reverse_grid_dp": [
        174,
    ],
    "move_step_distribution_dp": [
        576,
        688,
    ],
    "tuple_valued_grid_dp": [
        1301,
    ],
    "multi_agent_grid_dp": [
        741,
        1463,
    ],
}


GRID_DP_DIAGNOSTIC_CHECKLIST = [
    "What does dp[r][c] mean: reaching this cell or surviving from this cell?",
    "Which neighbors does the recurrence read?",
    "Does the recurrence require row-major or reverse order?",
    "Are obstacles impossible states or just high-cost cells?",
    "Is the answer at one target cell or aggregated over a boundary row/column?",
    "Can the row dimension be rolled?",
    "Does the problem need extra dimensions: move count, health, score count, or multiple agents?",
    "Are two agents allowed to collect the same cell once or twice?",
    "Is the grid rectangular, triangular, or irregular?",
    "Is the state value scalar, boolean, probability, or tuple-valued?",
]


if __name__ == "__main__":
    assert unique_paths(3, 7) == 28
    assert unique_paths_with_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
    assert min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
    assert minimum_total_triangle([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]) == 11
    assert min_falling_path_sum([[2, 1, 3], [6, 5, 4], [7, 8, 9]]) == 13
    assert min_falling_path_sum_ii([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 13
    assert calculate_minimum_hp([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]) == 7
    assert find_paths_out_of_boundary(2, 2, 2, 0, 0) == 6
    assert abs(knight_probability(3, 2, 0, 0) - 0.0625) < 1e-9
    assert paths_with_max_score(["E23", "2X2", "12S"]) == [7, 1]
    assert cherry_pickup_ii([[3, 1, 1], [2, 5, 1], [1, 5, 5], [2, 1, 1]]) == 24
    assert cherry_pickup([[0, 1, -1], [1, 0, -1], [1, 1, 1]]) == 5
