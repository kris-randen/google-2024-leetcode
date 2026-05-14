"""
Part 12 — Advanced Dynamic Programming Optimizations

Scope:
    Rolling variables / rolling rows
    Prefix-sum transition acceleration
    Sliding-window / monotonic deque DP
    Left-right pass optimization
    Binary search + DP/greedy feasibility boundary
    Divide-and-conquer style partition awareness
    Super Egg Drop moves-DP transformation
    Sparse memoization / pruning
    State compression

Representative problems:
    837. New 21 Game
    887. Super Egg Drop
    410. Split Array Largest Sum
    813. Largest Sum of Averages
    1425. Constrained Subsequence Sum
    1478. Allocate Mailboxes
    1696. Jump Game VI
    1937. Maximum Number of Points with Cost
    2209. Minimum White Tiles After Covering With Carpets

Core mental model:
    Advanced DP optimization usually means one of these:

        1. Same recurrence, less space.
        2. Same states, faster transition.
        3. Different state definition that collapses expensive dimensions.
        4. DP used only as feasibility inside another algorithm.
        5. Precompute expensive subproblem costs.

    Always start from the slow recurrence first.









# Part 12 — Advanced DP Optimizations

Python file:

[Download Part 12 — Advanced DP Optimizations Python file](sandbox:/mnt/data/dp_part12_advanced_optimizations.py)

## What Part 12 covers

```text id="l1gmro"
Advanced DP Optimizations
    -> rolling variables / rolling rows
    -> prefix-sum transition acceleration
    -> sliding-window probability DP
    -> monotonic deque DP
    -> left/right pass optimization
    -> binary search + feasibility
    -> partition DP with precomputed cost
    -> state transformation
    -> sparse memoization
```

## Core mental model

Advanced DP optimization usually means one of these:

```text id="6xy687"
1. Same recurrence, less space.
2. Same states, faster transition.
3. Different state definition that collapses expensive dimensions.
4. DP used only as feasibility inside binary search.
5. Expensive subproblem costs precomputed once.
6. Sparse memoization instead of dense tables.
```

Always start from the slow recurrence first.

---

## Main optimization families

### 1. Rolling space

Use when each state only reads the previous row/layer.

```text id="741vm0"
dp[i][j]
-> prev[j], curr[j]
```

Representative problems:

```text id="tez4ho"
62. Unique Paths
64. Minimum Path Sum
72. Edit Distance
1143. LCS
```

---

### 2. Prefix-sum transition acceleration

Use when recurrence has repeated range sums.

Slow:

```text id="7h6rzk"
sum(nums[l:r]) = O(n)
```

Fast:

```text id="2isqf9"
sum(nums[l:r]) = prefix[r] - prefix[l]
```

Representative problems:

```text id="386in7"
813. Largest Sum of Averages
1155. Dice Rolls With Target Sum
1478. Allocate Mailboxes
```

---

### 3. Monotonic deque DP

Use when recurrence is:

```text id="opyzf8"
dp[i] = value[i] + max/min(dp[j]) over j in sliding window
```

Maintain best candidate in a deque.

Representative problems:

```text id="6ukn2g"
1425. Constrained Subsequence Sum
1696. Jump Game VI
862. Shortest Subarray With Sum At Least K
```

---

### 4. Left/right pass optimization

Use when recurrence has:

```text id="b24xhf"
max(prev[pc] - abs(c - pc))
```

Split absolute value:

```text id="pz1lv9"
pc <= c:
    prev[pc] + pc - c

pc >= c:
    prev[pc] - pc + c
```

Representative problem:

```text id="9dz7yn"
1937. Maximum Number of Points with Cost
```

Also similar to “track best and second-best”:

```text id="8x6wa3"
1289. Minimum Falling Path Sum II
```

---

### 5. Binary search + feasibility

Use when:

```text id="s7i7uf"
answer is monotone
```

Example:

```text id="x667bb"
Can we split array with largest part sum <= X?
```

If yes for `X`, then yes for all larger values.

Representative problems:

```text id="tzb6m2"
410. Split Array Largest Sum
1011. Capacity to Ship Packages Within D Days
2064. Minimized Maximum of Products Distributed to Any Store
2616. Minimize the Maximum Difference of Pairs
```

This is a DP/Greedy boundary pattern.

---

### 6. Partition DP with precomputed cost

Use when recurrence is:

```text id="2g06n9"
dp[groups][i] = min/max over cut j:
    dp[groups-1][j] + cost(j, i)
```

Optimization:

```text id="c74mbl"
precompute cost(j, i)
```

Representative problems:

```text id="4sfol0"
813. Largest Sum of Averages
1478. Allocate Mailboxes
2209. Minimum White Tiles After Covering With Carpets
```

---

### 7. State transformation

Use when the obvious state is too expensive.

Example: Super Egg Drop.

Bad state:

```text id="cz1wgk"
dp[eggs][floors] = minimum moves
```

Better state:

```text id="fj9ek4"
cover[moves][eggs] = maximum floors checkable
```

Recurrence:

```text id="gwwum0"
cover[e] = cover[e] + cover[e - 1] + 1
```

Representative problems:

```text id="cdd59w"
887. Super Egg Drop
1884. Egg Drop With 2 Eggs and N Floors
1553. Minimum Number of Days to Eat N Oranges
818. Race Car
```

---

## Most important traps

```text id="e13t8a"
1. Optimizing before writing the slow recurrence.
2. Rolling rows when the recurrence still needs older rows.
3. Using prefix sums but mixing inclusive and half-open ranges.
4. Using deque when the candidate window is not monotonic or not sliding.
5. Forgetting to expire old deque indices.
6. Applying binary search without proving monotonic feasibility.
7. In bounded-step graph DP, updating in-place and using too many steps.
8. Treating sparse-state problems as dense arrays.
9. Missing state transformation opportunities like Egg Drop.
```

Next natural step: **Part 13 — Final Toolkit + Practice Plan**.



"""

from __future__ import annotations

from collections import deque
from functools import cache
from math import inf
from bisect import bisect_left


# =============================================================================
# Level 0 — Utility Primitives
# =============================================================================


def prefix_sums(nums: list[int]) -> list[int]:
    """
    ps[i] = sum(nums[:i])
    sum nums[l:r] = ps[r] - ps[l]
    """
    ps = [0]

    for x in nums:
        ps.append(ps[-1] + x)

    return ps


def range_sum(ps: list[int], l: int, r: int) -> int:
    return ps[r] - ps[l]


def min_plus(a: float, b: float) -> float:
    return a if a < b else b


def max_plus(a: float, b: float) -> float:
    return a if a > b else b


# =============================================================================
# Level 1 — Rolling Space Optimization
# =============================================================================


def edit_distance_rolling(a: str, b: str) -> int:
    """
    Rolling-row optimization for 2D sequence DP.

    Original:
        dp[i][j] = min edits for a[:i], b[:j]

    Observation:
        Row i only reads:
            previous row i-1
            current row i, previous column j-1

    Space:
        O(len(b)) instead of O(len(a) * len(b)).
    """
    if len(b) > len(a):
        a, b = b, a

    prev = list(range(len(b) + 1))

    for i in range(1, len(a) + 1):
        curr = [i] + [0] * len(b)

        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            curr[j] = min(
                prev[j] + 1,
                curr[j - 1] + 1,
                prev[j - 1] + cost,
            )

        prev = curr

    return prev[-1]


def unique_paths_rolling(rows: int, cols: int) -> int:
    """
    Rolling-row grid DP.

    dp[c] = ways to reach current row's column c.

    Recurrence:
        dp[c] = dp[c] + dp[c - 1]
                top    left
    """
    dp = [1] * cols

    for _ in range(1, rows):
        for c in range(1, cols):
            dp[c] += dp[c - 1]

    return dp[-1]


# =============================================================================
# Level 2 — Prefix-Sum Transition Acceleration
# =============================================================================


def num_rolls_to_target_prefix(n: int, k: int, target: int) -> int:
    """
    LeetCode:
        1155. Number of Dice Rolls With Target Sum

    Slow recurrence:
        curr[s] = sum(prev[s - face] for face in 1..k)

    Optimization:
        curr[s] is a sliding window sum over prev.

    Complexity:
        O(n * target) instead of O(n * target * k).
    """
    mod = 10**9 + 7
    prev = [0] * (target + 1)
    prev[0] = 1

    for _ in range(n):
        curr = [0] * (target + 1)
        window = 0

        for s in range(1, target + 1):
            window += prev[s - 1]

            if s - k - 1 >= 0:
                window -= prev[s - k - 1]

            curr[s] = window % mod

        prev = curr

    return prev[target]


def number_of_ways_stay_same_place(steps: int, arr_len: int) -> int:
    """
    LeetCode:
        1269. Number of Ways to Stay in the Same Place After Some Steps

    State:
        dp[pos] = ways to be at pos after current step.

    Optimization:
        Positions beyond steps are irrelevant.
        Bound width to min(arr_len, steps + 1).

    Complexity:
        O(steps * min(arr_len, steps)).
    """
    mod = 10**9 + 7
    width = min(arr_len, steps + 1)
    dp = [0] * width
    dp[0] = 1

    for _ in range(steps):
        nxt = [0] * width

        for pos in range(width):
            total = dp[pos]

            if pos > 0:
                total += dp[pos - 1]

            if pos + 1 < width:
                total += dp[pos + 1]

            nxt[pos] = total % mod

        dp = nxt

    return dp[0]


def new_21_game(n: int, k: int, max_pts: int) -> float:
    """
    LeetCode:
        837. New 21 Game

    State:
        dp[x] = probability of ending with score x / reaching x.

    Recurrence:
        dp[x] = average of previous k-active states.

    Sliding window:
        Maintain sum of probabilities that can transition into current x.

    Complexity:
        O(n)
    """
    if k == 0 or n >= k + max_pts:
        return 1.0

    dp = [0.0] * (n + 1)
    dp[0] = 1.0
    window = 1.0
    ans = 0.0

    for x in range(1, n + 1):
        dp[x] = window / max_pts

        if x < k:
            window += dp[x]
        else:
            ans += dp[x]

        if x - max_pts >= 0:
            window -= dp[x - max_pts]

    return ans


# =============================================================================
# Level 3 — Monotonic Deque DP
# =============================================================================


def constrained_subsequence_sum(nums: list[int], k: int) -> int:
    """
    LeetCode:
        1425. Constrained Subsequence Sum

    Slow recurrence:
        dp[i] = nums[i] + max(0, max(dp[j]) for j in [i-k, i-1])

    Optimization:
        Maintain decreasing deque of candidate dp indices.

    Complexity:
        O(n)
    """
    dq: deque[int] = deque()
    dp = [0] * len(nums)
    best = nums[0]

    for i, x in enumerate(nums):
        while dq and dq[0] < i - k:
            dq.popleft()

        dp[i] = x + (max(0, dp[dq[0]]) if dq else 0)
        best = max(best, dp[i])

        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()

        dq.append(i)

    return best


def jump_game_vi(nums: list[int], k: int) -> int:
    """
    LeetCode:
        1696. Jump Game VI

    State:
        dp[i] = max score to reach index i.

    Recurrence:
        dp[i] = nums[i] + max(dp[j]) for j in [i-k, i-1]

    Monotonic deque maintains max dp[j] in the valid window.

    Complexity:
        O(n)
    """
    dq: deque[int] = deque([0])
    dp = [0] * len(nums)
    dp[0] = nums[0]

    for i in range(1, len(nums)):
        while dq and dq[0] < i - k:
            dq.popleft()

        dp[i] = nums[i] + dp[dq[0]]

        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()

        dq.append(i)

    return dp[-1]


def shortest_subarray_at_least_k(nums: list[int], k: int) -> int:
    """
    LeetCode:
        862. Shortest Subarray with Sum at Least K

    Not always tagged DP, but it is the same monotonic-prefix primitive.

    Prefix sums:
        need ps[i] - ps[j] >= k
        minimize i - j

    Maintain increasing deque of prefix indices.
    """
    ps = prefix_sums(nums)
    dq: deque[int] = deque()
    best = inf

    for i, val in enumerate(ps):
        while dq and val - ps[dq[0]] >= k:
            best = min(best, i - dq.popleft())

        while dq and ps[dq[-1]] >= val:
            dq.pop()

        dq.append(i)

    return -1 if best == inf else int(best)


# =============================================================================
# Level 4 — Left/Right Pass Optimization
# =============================================================================


def max_points_with_cost(points: list[list[int]]) -> int:
    """
    LeetCode:
        1937. Maximum Number of Points with Cost

    Slow recurrence:
        dp[r][c] = points[r][c] + max(prev[pc] - abs(c - pc))

    Naive transition:
        O(cols^2) per row.

    Optimization:
        Split abs into two directional passes.

        From left:
            max(prev[pc] + pc) - c

        From right:
            max(prev[pc] - pc) + c

    Complexity:
        O(rows * cols)
    """
    rows = len(points)
    cols = len(points[0])
    prev = points[0][:]

    for r in range(1, rows):
        left = [0] * cols
        right = [0] * cols

        best = -inf

        for c in range(cols):
            best = max(best, prev[c] + c)
            left[c] = best - c

        best = -inf

        for c in range(cols - 1, -1, -1):
            best = max(best, prev[c] - c)
            right[c] = best + c

        curr = [points[r][c] + max(left[c], right[c]) for c in range(cols)]
        prev = curr

    return max(prev)


def min_falling_path_sum_ii(grid: list[list[int]]) -> int:
    """
    LeetCode:
        1289. Minimum Falling Path Sum II

    Slow recurrence:
        curr[c] = grid[r][c] + min(prev[pc] for pc != c)

    Optimization:
        Track smallest and second-smallest values in previous row.

    Complexity:
        O(rows * cols)
    """
    prev = grid[0][:]

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

        curr = [0] * len(row)

        for c, x in enumerate(row):
            curr[c] = x + (min2_val if c == min1_col else min1_val)

        prev = curr

    return int(min(prev))


# =============================================================================
# Level 5 — Binary Search + Feasibility Boundary
# =============================================================================


def split_array_largest_sum(nums: list[int], k: int) -> int:
    """
    LeetCode:
        410. Split Array Largest Sum

    This problem has a DP formulation:
        dp[parts][i] = min largest partition sum for nums[:i]

    But the common optimized solution is:
        binary search answer X
        greedy feasibility: can split into <= k parts with each sum <= X?

    This is a DP-vs-Greedy boundary pattern.
    """

    def feasible(limit: int) -> bool:
        groups = 1
        curr = 0

        for x in nums:
            if curr + x <= limit:
                curr += x
            else:
                groups += 1
                curr = x

        return groups <= k

    lo = max(nums)
    hi = sum(nums)

    while lo < hi:
        mid = (lo + hi) // 2

        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1

    return lo


def ship_within_days(weights: list[int], days: int) -> int:
    """
    LeetCode:
        1011. Capacity To Ship Packages Within D Days

    Same binary-search-on-answer + greedy feasibility primitive.
    """

    def feasible(capacity: int) -> bool:
        used = 1
        curr = 0

        for w in weights:
            if curr + w <= capacity:
                curr += w
            else:
                used += 1
                curr = w

        return used <= days

    lo = max(weights)
    hi = sum(weights)

    while lo < hi:
        mid = (lo + hi) // 2

        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1

    return lo


# =============================================================================
# Level 6 — Partition DP With Precomputed Cost
# =============================================================================


def largest_sum_of_averages(nums: list[int], k: int) -> float:
    """
    LeetCode:
        813. Largest Sum of Averages

    S:
        dp[parts][i] = max score for partitioning nums[:i] into parts groups.

    R:
        choose previous cut j:
            dp[parts][i] = max(dp[parts-1][j] + avg(nums[j:i]))

    Optimization:
        Prefix sums make avg(j:i) O(1).

    Complexity:
        O(k * n^2)
    """
    n = len(nums)
    ps = prefix_sums(nums)
    dp = [[-inf] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = 0.0

    for parts in range(1, k + 1):
        for i in range(parts, n + 1):
            for j in range(parts - 1, i):
                avg = range_sum(ps, j, i) / (i - j)
                dp[parts][i] = max(dp[parts][i], dp[parts - 1][j] + avg)

    return dp[k][n]


def min_distance_allocate_mailboxes(houses: list[int], k: int) -> int:
    """
    LeetCode:
        1478. Allocate Mailboxes

    Two-stage optimization:
        1. Precompute cost[l][r]:
            minimum distance to serve houses[l:r+1] with one mailbox.
            The optimal mailbox is at the median house.

        2. Partition DP:
            dp[boxes][i] = min cost to serve first i houses with boxes mailboxes.

    Complexity:
        O(n^2 + k*n^2)
    """
    houses.sort()
    n = len(houses)

    cost = [[0] * n for _ in range(n)]

    for l in range(n):
        for r in range(l, n):
            median = (l + r) // 2
            cost[l][r] = sum(abs(houses[i] - houses[median]) for i in range(l, r + 1))

    dp = [[inf] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = 0

    for boxes in range(1, k + 1):
        for i in range(1, n + 1):
            for j in range(i):
                dp[boxes][i] = min(dp[boxes][i], dp[boxes - 1][j] + cost[j][i - 1])

    return int(dp[k][n])


def minimum_white_tiles(floor: str, num_carpets: int, carpet_len: int) -> int:
    """
    LeetCode:
        2209. Minimum White Tiles After Covering With Carpets

    S:
        dp[c][i] = min visible white tiles in floor[:i] using c carpets.

    R:
        Do not cover tile i-1:
            dp[c][i-1] + white(i-1)

        Cover last carpet_len tiles ending at i:
            dp[c-1][max(0, i-carpet_len)]

    T:
        increasing carpet count and prefix length.

    Complexity:
        O(num_carpets * n)
    """
    n = len(floor)
    dp = [[inf] * (n + 1) for _ in range(num_carpets + 1)]

    for c in range(num_carpets + 1):
        dp[c][0] = 0

    for i in range(1, n + 1):
        dp[0][i] = dp[0][i - 1] + (floor[i - 1] == "1")

    for c in range(1, num_carpets + 1):
        for i in range(1, n + 1):
            visible = dp[c][i - 1] + (floor[i - 1] == "1")
            covered = dp[c - 1][max(0, i - carpet_len)]
            dp[c][i] = min(visible, covered)

    return int(dp[num_carpets][n])


# =============================================================================
# Level 7 — Super Egg Drop State Transformation
# =============================================================================


def super_egg_drop_moves(k: int, n: int) -> int:
    """
    LeetCode:
        887. Super Egg Drop

    Classic state:
        dp[eggs][floors] = min moves
    is hard to optimize.

    Better state:
        cover[moves][eggs] = maximum floors that can be checked with
                             given moves and eggs.

    Recurrence:
        With one move:
            if egg breaks:
                can check cover[m-1][e-1] floors below
            if egg survives:
                can check cover[m-1][e] floors above
            plus current floor

        cover[e] = cover[e] + cover[e-1] + 1

    O:
        smallest moves such that cover[k] >= n.

    Complexity:
        O(k * answer_moves)
    """
    cover = [0] * (k + 1)
    moves = 0

    while cover[k] < n:
        moves += 1

        for eggs in range(k, 0, -1):
            cover[eggs] = cover[eggs] + cover[eggs - 1] + 1

    return moves


def two_egg_drop(n: int) -> int:
    """
    LeetCode:
        1884. Egg Drop With 2 Eggs and N Floors

    Same moves-DP with k=2.
    """
    return super_egg_drop_moves(2, n)


# =============================================================================
# Level 8 — Sparse Memoization / Pruning
# =============================================================================


def min_days_to_eat_oranges(n: int) -> int:
    """
    LeetCode:
        1553. Minimum Number of Days to Eat N Oranges

    Naive dp over all 0..n is too large.

    Sparse memoization:
        State n only branches to n//2 and n//3.

    R:
        Eat oranges until divisible by 2, then use divide-by-2 operation.
        Eat oranges until divisible by 3, then use divide-by-3 operation.

        dp(n) = 1 + min(
            n % 2 + dp(n // 2),
            n % 3 + dp(n // 3)
        )

    Complexity:
        O(log^2 n) style number of reachable quotient states.
    """

    @cache
    def dp(x: int) -> int:
        if x <= 1:
            return x

        by_two = x % 2 + dp(x // 2)
        by_three = x % 3 + dp(x // 3)

        return 1 + min(by_two, by_three)

    return dp(n)


def racecar(target: int) -> int:
    """
    LeetCode:
        818. Race Car

    Sparse memoized DP over target distance.

    Let k = bit length needed so that 2^k - 1 >= target.

    Cases:
        1. Hit target exactly by accelerating k times.
        2. Overshoot, reverse, solve overshoot-target.
        3. Undershoot with k-1 accelerations, reverse, back up j accelerations,
           reverse again, solve remaining distance.

    This is a classic example where state transformation matters more than
    table shape.
    """

    @cache
    def dp(t: int) -> int:
        k = t.bit_length()
        full = (1 << k) - 1

        if full == t:
            return k

        best = k + 1 + dp(full - t)

        prev_full = (1 << (k - 1)) - 1

        for back_steps in range(k - 1):
            back = (1 << back_steps) - 1
            remaining = t - (prev_full - back)
            best = min(best, (k - 1) + 1 + back_steps + 1 + dp(remaining))

        return best

    return dp(target)


# =============================================================================
# Level 9 — Optimization Maps
# =============================================================================


ADVANCED_OPTIMIZATION_MAP = {
    "rolling_space": [
        62,
        64,
        72,
        1143,
    ],
    "prefix_sum_transition": [
        1155,
        813,
        1478,
    ],
    "sliding_window_probability": [
        837,
    ],
    "monotonic_deque_dp": [
        1425,
        1696,
        862,
    ],
    "left_right_pass_optimization": [
        1937,
        1289,
    ],
    "binary_search_feasibility": [
        410,
        1011,
        2064,
        2616,
    ],
    "partition_dp_precomputed_cost": [
        813,
        1478,
        2209,
    ],
    "state_transformation": [
        887,
        1884,
        1553,
        818,
    ],
}


ADVANCED_DP_OPTIMIZATION_CHECKLIST = [
    "What is the slow recurrence first?",
    "Is the bottleneck memory or transition cost?",
    "Does each state read only the previous row/layer?",
    "Can range sums or averages be made O(1) with prefix sums?",
    "Is the transition max/min over a sliding window?",
    "Can a monotonic deque maintain the best candidate?",
    "Can abs(c - pc) be split into left/right directional passes?",
    "Is the answer monotone so binary search on answer is possible?",
    "Can expensive interval/group cost be precomputed?",
    "Can the state be redefined to count capability instead of cost, as in Egg Drop?",
    "Are most states unreachable, making sparse memoization better?",
    "Is there a known convexity/monotonicity property enabling further optimization?",
]


if __name__ == "__main__":
    assert edit_distance_rolling("horse", "ros") == 3
    assert unique_paths_rolling(3, 7) == 28

    assert num_rolls_to_target_prefix(2, 6, 7) == 6
    assert number_of_ways_stay_same_place(3, 2) == 4
    assert abs(new_21_game(10, 1, 10) - 1.0) < 1e-9

    assert constrained_subsequence_sum([10, 2, -10, 5, 20], 2) == 37
    assert jump_game_vi([1, -1, -2, 4, -7, 3], 2) == 7
    assert shortest_subarray_at_least_k([2, -1, 2], 3) == 3

    assert max_points_with_cost([[1, 2, 3], [1, 5, 1], [3, 1, 1]]) == 9
    assert min_falling_path_sum_ii([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 13

    assert split_array_largest_sum([7, 2, 5, 10, 8], 2) == 18
    assert ship_within_days([1, 2, 3, 1, 1], 4) == 3

    assert abs(largest_sum_of_averages([9, 1, 2, 3, 9], 3) - 20.0) < 1e-9
    assert min_distance_allocate_mailboxes([1, 4, 8, 10, 20], 3) == 5
    assert minimum_white_tiles("10110101", 2, 2) == 2

    assert super_egg_drop_moves(1, 2) == 2
    assert super_egg_drop_moves(2, 6) == 3
    assert two_egg_drop(100) == 14

    assert min_days_to_eat_oranges(10) == 4
    assert racecar(3) == 2
    assert racecar(6) == 5
