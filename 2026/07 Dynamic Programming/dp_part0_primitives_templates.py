# Dynamic Programming primitive templates
# Generated as a reusable DSA toolkit scaffold.
# The file is intentionally template-heavy, not problem-solution-heavy.

"""

Done — I treated the uploaded text as the actual DP deconstruction prompt. It explicitly asks to use SRTBOT as the central lens, where DP is analyzed through subproblems, recurrence relationships, topological order, base cases, original-answer extraction, and complexity.  The attached LeetCode DP list contains **651 questions**, and I parsed all 651 into the catalogue.

## Generated files

1. [DP problem catalogue CSV — 651 rows](sandbox:/mnt/data/leetcode_dp_problem_catalog.csv)
2. [DP family summary CSV](sandbox:/mnt/data/leetcode_dp_family_summary.csv)
3. [DP primitive templates Python file](sandbox:/mnt/data/dp_primitives_templates.py)
4. [DP high-level atlas markdown](sandbox:/mnt/data/dp_high_level_atlas.md)

A note on quality: the catalogue has a `confidence` column. Since many newer LeetCode titles are obscure without statements, I marked **226 rows** as `heuristic-low` instead of pretending the classification is certain.

## A. Executive Summary

Dynamic Programming is best treated as:

```text
state space
+ recurrence edges
+ topological order
+ base cases
+ answer extraction
+ complexity accounting
```

The reusable primitives are not “use DP.” They are state-shape and transition-shape primitives: prefix state, interval state, capacity state, state-machine state, bitmask state, tree tuple state, digit-tight state, and graph relaxation state.

## B. DP Mental Model using SRTBOT

```text
S — Subproblems
    What is the smallest reusable question?

R — Relationships
    Which smaller states does this state depend on?

T — Topological Order
    In what order can states be solved without cycles?

B — Base Cases
    Which states are already known?

O — Original Problem
    Which state/cell gives the final answer?

T — Time Complexity
    number of states × transition cost
```

The central move is to stop asking, “What is the trick?” and ask:

```text
What is the DAG of subproblems?
```

## C. Proposed Family Taxonomy

Core families:

| Family              | State Shape                    | Canonical Examples           |
| ------------------- | ------------------------------ | ---------------------------- |
| 1D prefix/suffix DP | `dp[i]`                        | Climbing Stairs, Decode Ways |
| House Robber        | `dp[i]`, `(skip, take)`        | 198, 213, 337, 740           |
| Kadane/local-global | `local ending at i + global`   | 53, 152, 918, 1186           |
| Stock state machine | `day × holding × constraint`   | 121, 122, 123, 188, 309, 714 |
| Grid DP             | `dp[r][c]`, layered states     | 62, 64, 174, 741, 1463       |
| Two-sequence DP     | `dp[i][j]`                     | 72, 97, 115, 1143            |
| Knapsack/capacity   | `dp[i][w]`, `dp[w]`            | 416, 474, 494, 518           |
| Interval DP         | `dp[l][r]`                     | 312, 1000, 1547              |
| Game DP             | `dp[state]`, `dp[l][r]`        | 486, 877, Stone Games        |
| LIS/chain DP        | `dp[i]`, `tails[]`             | 300, 354, 673                |
| Bitmask DP          | `dp[mask]`                     | 847, 943, 1125, 1799         |
| Digit DP            | `dp[pos][tight][started][...]` | 233, 600, 902, 1012          |
| Tree DP             | `dfs(node) -> tuple`           | 124, 337, 834, 968           |
| Graph-as-DP         | `dp[v]`, `dp[steps][v]`        | 787, 1548, 1928              |
| Monotonic deque DP  | `dp[i] + window best`          | 1425, 1696                   |

## D. Ranked Primitive Toolkit

Top primitives to drill first:

1. `dp[i]` prefix state
2. take-or-skip recurrence
3. rolling two-variable compression
4. local/global Kadane state
5. grid neighbor recurrence
6. two-sequence `dp[i][j]` alignment
7. 0/1 knapsack reverse loop
8. unbounded knapsack forward loop
9. interval DP by increasing length
10. stock holding/not-holding state machine
11. tree DP returning tuple states
12. bitmask `dp[mask]`
13. digit DP with tight flag
14. monotonic deque transition optimization
15. LIS patience sorting helper

## E. Series Evolution Plan

The major series should be expanded in this order:

```text
House Robber:
198 -> 213 -> 337 -> 740 -> House Robber IV boundary

Stock:
121 -> 122 -> 123 -> 188 -> 309 -> 714

Knapsack / Coin Change:
subset sum -> partition -> target sum -> 0/1 knapsack
coin change min -> coin change count -> Combination Sum IV

Stone Game:
score-difference interval DP
-> prefix-sum optimized variants
-> minimax/game-theory exceptions

Jump Game:
greedy frontier
-> graph reachability
-> DP
-> monotonic deque DP

LIS:
O(n²) previous-choice DP
-> O(n log n) patience sorting
-> counting LIS
-> Russian Doll / String Chain / Arithmetic variants
```

## F. CSV Catalogue Schema

The generated catalogue includes:

```text
problem_id
title
difficulty
acceptance_rate_if_available
inferred_family
subfamily
state_shape
recurrence_shape
evaluation_order
transition_cost
likely_time_complexity
likely_space_complexity
top_down_or_bottom_up_preferred
optimization_primitives
representative_or_not
confidence
notes
```

This matches the requested catalogue shape from the uploaded prompt.

## G. Highest-ROI Expansion Order

I’d proceed like this:

1. Part 2 — Core DP primitives
2. Part 3 — 1D DP + House Robber
3. Part 4 — Grid DP
4. Part 5 — Two-sequence DP
5. Part 6 — Knapsack + Coin Change
6. Part 7 — Interval DP
7. Part 8 — Stock series
8. Part 9 — Stone Game series
9. Part 10 — LIS / sequence optimization
10. Part 11 — Bitmask, Digit, Tree, Graph DP
11. Part 12 — Advanced optimizations

## H. Next Deliverables

The next natural step is **Part 2 — Core DP Primitives**, where we build the actual study toolkit in the same style as your linked-list/tree/graph primitive files: primitive, invariant, why it exists, composition chains, traps, and compact Python templates.

"""

from __future__ import annotations

from bisect import bisect_left
from collections import deque
from functools import cache
from math import inf
from typing import Callable, Iterable, Sequence, TypeVar, Optional

T = TypeVar("T")


# -----------------------------------------------------------------------------
# Level 0: small testing / reference utilities
# -----------------------------------------------------------------------------


def checked_min(candidates: Iterable[int], default: int = inf) -> int:
    return min(candidates, default=default)


def checked_max(candidates: Iterable[int], default: int = -inf) -> int:
    return max(candidates, default=default)


# -----------------------------------------------------------------------------
# Level 1: top-down memoization skeleton
# -----------------------------------------------------------------------------


def top_down_index_dp(n: int, solve_state: Callable[[int], int]) -> int:
    """
    Shape:
        state = i
        answer = f(n) or f(0), depending on convention.

    This is a wrapper shape only. In real problems, define f with @cache where
    the recurrence references strictly smaller states.
    """
    return solve_state(n)


def memoized_dfs_example(nums: Sequence[int]) -> int:
    """
    Example composition: suffix take/skip.
    Problem shape: best answer from nums[i:].
    """

    @cache
    def best_from(i: int) -> int:
        if i >= len(nums):
            return 0
        return max(best_from(i + 1), nums[i] + best_from(i + 2))

    return best_from(0)


# -----------------------------------------------------------------------------
# Level 2: 1D prefix / rolling DP
# -----------------------------------------------------------------------------


def take_skip_path(values: Sequence[int]) -> int:
    """
    House Robber path skeleton.

    State:
        best answer on processed prefix.

    Invariant:
        prev2 = best before previous item
        prev1 = best before current item
    """
    prev2 = prev1 = 0

    for value in values:
        prev2, prev1 = prev1, max(prev1, prev2 + value)

    return prev1


def max_subarray_sum(nums: Sequence[int]) -> int:
    """
    Kadane local/global skeleton.

    State:
        local = best subarray sum ending at current index.
        global_best = best subarray sum seen anywhere.
    """
    local = global_best = nums[0]

    for x in nums[1:]:
        local = max(x, local + x)
        global_best = max(global_best, local)

    return global_best


# -----------------------------------------------------------------------------
# Level 3: grid DP
# -----------------------------------------------------------------------------


def grid_paths_count(m: int, n: int) -> int:
    """
    Unique-path grid skeleton.

    State:
        dp[c] = number of ways to reach current row, column c.
    """
    dp = [1] * n

    for _ in range(1, m):
        for c in range(1, n):
            dp[c] += dp[c - 1]

    return dp[-1]


def min_grid_path_sum(grid: Sequence[Sequence[int]]) -> int:
    """
    Min-cost grid skeleton with rolling row.
    """
    m, n = len(grid), len(grid[0])
    dp = [inf] * n
    dp[0] = 0

    for r in range(m):
        dp[0] += grid[r][0]
        for c in range(1, n):
            dp[c] = grid[r][c] + min(dp[c], dp[c - 1])

    return dp[-1]


# -----------------------------------------------------------------------------
# Level 4: two-sequence alignment DP
# -----------------------------------------------------------------------------


def lcs_length(a: str, b: str) -> int:
    """
    Two-prefix alignment skeleton.

    State:
        dp[j] = LCS length for processed prefix of a and b[:j].
    """
    dp = [0] * (len(b) + 1)

    for ca in a:
        prev_diag = 0
        for j, cb in enumerate(b, 1):
            old = dp[j]
            if ca == cb:
                dp[j] = prev_diag + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev_diag = old

    return dp[-1]


def edit_distance(a: str, b: str) -> int:
    """
    Edit-distance skeleton.

    State:
        dp[j] = edit distance between processed prefix of a and b[:j].
    """
    dp = list(range(len(b) + 1))

    for i, ca in enumerate(a, 1):
        prev_diag = dp[0]
        dp[0] = i
        for j, cb in enumerate(b, 1):
            old = dp[j]
            if ca == cb:
                dp[j] = prev_diag
            else:
                dp[j] = 1 + min(prev_diag, dp[j], dp[j - 1])
            prev_diag = old

    return dp[-1]


# -----------------------------------------------------------------------------
# Level 5: interval DP
# -----------------------------------------------------------------------------


def interval_dp_by_length(n: int, combine: Callable[[int, int, list[list[int]]], int]) -> list[list[int]]:
    """
    Generic inclusive interval [l, r] fill order.

    combine(l, r, dp) must only read shorter intervals.
    """
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            dp[l][r] = combine(l, r, dp)

    return dp


def stone_score_difference(piles: Sequence[int]) -> int:
    """
    Interval game score-difference skeleton.

    State:
        dp[l][r] = best current-player score difference on piles[l:r+1].
    """
    n = len(piles)
    dp = [[0] * n for _ in range(n)]

    for i, x in enumerate(piles):
        dp[i][i] = x

    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            take_left = piles[l] - dp[l + 1][r]
            take_right = piles[r] - dp[l][r - 1]
            dp[l][r] = max(take_left, take_right)

    return dp[0][n - 1]


# -----------------------------------------------------------------------------
# Level 6: knapsack / capacity DP
# -----------------------------------------------------------------------------


def zero_one_knapsack(weights: Sequence[int], values: Sequence[int], capacity: int) -> int:
    """
    0/1 knapsack skeleton.

    Critical invariant:
        Iterate capacity backward so each item is used at most once.
    """
    dp = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        for cap in range(capacity, weight - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - weight] + value)

    return dp[capacity]


def unbounded_knapsack(weights: Sequence[int], values: Sequence[int], capacity: int) -> int:
    """
    Unbounded knapsack skeleton.

    Critical invariant:
        Iterate capacity forward so current item can be reused.
    """
    dp = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        for cap in range(weight, capacity + 1):
            dp[cap] = max(dp[cap], dp[cap - weight] + value)

    return dp[capacity]


def coin_change_min(coins: Sequence[int], amount: int) -> int:
    """
    Unbounded min-count optimization.
    """
    dp = [0] + [inf] * amount

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return -1 if dp[amount] == inf else dp[amount]


def coin_change_combinations(coins: Sequence[int], amount: int) -> int:
    """
    Order-insensitive combination counting.

    Item-first loop prevents counting permutations separately.
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] += dp[x - coin]

    return dp[amount]


# -----------------------------------------------------------------------------
# Level 7: stock state-machine DP
# -----------------------------------------------------------------------------


def stock_unlimited_with_fee(prices: Sequence[int], fee: int = 0) -> int:
    """
    Two-state stock skeleton.

    State:
        cash = best profit while not holding stock.
        hold = best profit while holding stock.
    """
    cash = 0
    hold = -inf

    for price in prices:
        old_cash = cash
        cash = max(cash, hold + price - fee)
        hold = max(hold, old_cash - price)

    return cash


def stock_with_cooldown(prices: Sequence[int]) -> int:
    """
    Cooldown stock skeleton with explicit rest/sold/hold states.
    """
    rest = 0
    sold = -inf
    hold = -inf

    for price in prices:
        prev_rest, prev_sold, prev_hold = rest, sold, hold
        rest = max(prev_rest, prev_sold)
        sold = prev_hold + price
        hold = max(prev_hold, prev_rest - price)

    return max(rest, sold)


# -----------------------------------------------------------------------------
# Level 8: tree DP returning tuple states
# -----------------------------------------------------------------------------


class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


def tree_take_skip(root: Optional[TreeNode]) -> int:
    """
    House Robber III / tree MWIS skeleton.

    Returns:
        skip = best if current node is not taken.
        take = best if current node is taken.
    """

    def dfs(node: Optional[TreeNode]) -> tuple[int, int]:
        if node is None:
            return 0, 0

        left_skip, left_take = dfs(node.left)
        right_skip, right_take = dfs(node.right)

        take = node.val + left_skip + right_skip
        skip = max(left_skip, left_take) + max(right_skip, right_take)

        return skip, take

    return max(dfs(root))


# -----------------------------------------------------------------------------
# Level 9: bitmask DP
# -----------------------------------------------------------------------------


def assignment_min_cost(cost: Sequence[Sequence[int]]) -> int:
    """
    Bitmask assignment skeleton.

    State:
        dp[mask] = min cost after assigning first popcount(mask) workers
        to the set of jobs in mask.
    """
    n = len(cost)
    dp = [inf] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        worker = mask.bit_count()
        if worker == n:
            continue
        for job in range(n):
            if not (mask >> job) & 1:
                nxt = mask | (1 << job)
                dp[nxt] = min(dp[nxt], dp[mask] + cost[worker][job])

    return dp[-1]


# -----------------------------------------------------------------------------
# Level 10: digit DP
# -----------------------------------------------------------------------------


def count_without_consecutive_ones(n: int) -> int:
    """
    Digit DP skeleton for binary digits.
    Counts x in [0, n] whose binary representation has no consecutive ones.
    """
    bits = tuple(map(int, bin(n)[2:]))

    @cache
    def f(pos: int, prev_one: bool, tight: bool) -> int:
        if pos == len(bits):
            return 1

        limit = bits[pos] if tight else 1
        total = 0

        for bit in range(limit + 1):
            if prev_one and bit == 1:
                continue
            total += f(pos + 1, bit == 1, tight and bit == limit)

        return total

    return f(0, False, True)


# -----------------------------------------------------------------------------
# Level 11: monotonic deque DP
# -----------------------------------------------------------------------------


def constrained_subsequence_sum(nums: Sequence[int], k: int) -> int:
    """
    Sliding-window max DP with monotonic deque.

    State:
        dp[i] = nums[i] + max(0, dp[j]) over i-k <= j < i.
    """
    q: deque[tuple[int, int]] = deque()
    best = -inf

    for i, x in enumerate(nums):
        while q and q[0][0] < i - k:
            q.popleft()

        prev = max(0, q[0][1] if q else 0)
        curr = x + prev
        best = max(best, curr)

        while q and q[-1][1] <= curr:
            q.pop()
        q.append((i, curr))

    return best


# -----------------------------------------------------------------------------
# Level 12: LIS patience sorting helper
# -----------------------------------------------------------------------------


def lis_length_strict(nums: Sequence[int]) -> int:
    """
    Strict LIS length in O(n log n).

    tails[len - 1] = minimum possible tail value of a strict increasing
    subsequence of length len.
    """
    tails: list[int] = []

    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x

    return len(tails)
