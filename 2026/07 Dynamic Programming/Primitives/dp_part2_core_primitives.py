"""
Part 2 — Core Dynamic Programming Primitives

This file is intentionally a toolkit, not a dump of full LeetCode solutions.

Mental model:
    DP = subproblem DAG + recurrence edges + topological order.

SRTBOT:
    S — Subproblems
    R — Relationships / recurrence edges
    T — Topological order / evaluation order
    B — Base cases
    O — Original problem / answer extraction
    T — Time complexity = number of states × transition cost


# Part 2 — Core DP Primitives

The biggest mental upgrade is this:

```text
Dynamic Programming is not primarily about tables.

A DP table is just one possible storage format for values on a DAG of subproblems.
```

The reusable primitive stack is:

```text
state
+ recurrence edge
+ aggregation operator
+ topological order
+ base case
+ answer extraction
+ complexity accounting
```

Everything else — House Robber, Stock, Knapsack, Stone Game, Edit Distance, LIS — is built from these.

---

# 0. The Fundamental DP Object Model

```text
subproblem = vertex in a DAG

recurrence = directed edges from a state to smaller/dependent states

topological order = valid order in which states can be solved

base cases = source/sink vertices whose values are known

answer = one distinguished state or aggregation over final states

complexity = number of states × transition cost
```

So the SRTBOT frame becomes:

```text
S — What are the states?
R — What smaller states does each state depend on?
T — In what order are those states evaluated?
B — What states are known initially?
O — Which state gives the final answer?
T — How many states × how much work per state?
```

That is the master primitive.

---

# 1. Primitive: State Shape

## What it is

A **state** is the smallest reusable question whose answer can help build larger answers.

Examples:

```text
dp[i]
    answer for prefix nums[:i]
    or suffix nums[i:]

dp[i][j]
    answer involving two prefixes
    or grid cell
    or interval boundary

dp[l][r]
    answer for subarray/string interval nums[l:r+1]

dp[i][w]
    answer using first i items with capacity w

dp[day][holding]
    answer after processing day with stock holding state

dfs(node) -> tuple
    answer for subtree rooted at node

dp[mask]
    answer for chosen subset represented by bitmask
```

## Mental invariant

```text
A state must contain exactly enough information to make the future independent of the past.
```

This is the DP version of a Markov state.

If two partial histories lead to the same state, then from that state onward they should behave the same.

## Why it matters

Most DP difficulty is **state discovery**, not coding.

Bad state:

```text
"best answer so far"
```

Good state:

```text
"best answer after processing first i elements, ending with status s"
```

The second one tells you exactly what information has been preserved.

## Common traps

### Trap 1 — Missing a constraint dimension

Example: Stock with cooldown.

Wrong state:

```text
dp[day][holding]
```

May be insufficient if cooldown is not encoded.

Better state options:

```text
dp[day][holding][cooldown]
```

or compressed states:

```text
hold
sold
rest
```

### Trap 2 — Too much state

Example: House Robber.

Bad:

```text
dp[i][all previous choices]
```

Good:

```text
dp[i] = best answer for nums[:i]
```

Because only the previous two prefixes matter.

---

# 2. Primitive: Recurrence Edge

## What it is

A recurrence edge says:

```text
state -> smaller/dependency states
```

For a top-down recurrence:

```text
solve(state) = aggregate(solve(next_state) + cost)
```

For a bottom-up recurrence:

```text
dp[state] = aggregate(dp[previous_state] + cost)
```

## Core recurrence families

```text
take / skip
extend / restart
match / mismatch
choose previous index
choose split point
choose capacity inclusion
choose next mask
buy / sell / hold / rest
choose left / choose right
sum over all ways
min over all cuts
max over all partitions
```

## Mental invariant

```text
Every recurrence edge must move toward a smaller/already-solvable state.
```

If recurrence edges can cycle without memoization or without an acyclic ordering, it is not ordinary DP yet. It may be graph shortest path, game search, or needs cycle handling.

## Examples

### House Robber

```text
dp[i] = max(
    dp[i - 1],              # skip house i-1
    dp[i - 2] + nums[i-1]   # rob house i-1
)
```

This is:

```text
prefix state
+ take/skip transition
```

### Edit Distance

```text
dp[i][j] = min(
    dp[i-1][j] + 1,        # delete
    dp[i][j-1] + 1,        # insert
    dp[i-1][j-1] + cost    # replace/match
)
```

This is:

```text
two-prefix state
+ match/mismatch transition
+ min aggregation
```

### Interval Game

```text
dp[l][r] = max(
    nums[l] - dp[l+1][r],
    nums[r] - dp[l][r-1]
)
```

This is:

```text
interval state
+ choose boundary
+ score-difference invariant
```

---

# 3. Primitive: Aggregation Operator

## What it is

The recurrence usually combines candidate transitions using an aggregation operator.

Common operators:

```text
max     optimization / best score
min     minimum cost
sum     count all ways
any     feasibility
all     universal validity
```

## Mental invariant

```text
The aggregation operator reveals the problem type.
```

| Problem language            | Usually means       |
| --------------------------- | ------------------- |
| maximum / best / profit     | `max`               |
| minimum / fewest / cheapest | `min`               |
| number of ways              | `sum`               |
| possible / can / exists     | `any` / boolean OR  |
| all paths valid             | `all` / boolean AND |

## Why it matters

Two problems may have the same state shape but different aggregation.

Example: Coin Change.

### Minimum coins

```text
dp[x] = min(dp[x - coin] + 1)
```

### Number of ways

```text
dp[x] += dp[x - coin]
```

Same capacity state. Different aggregation. Completely different loop semantics.

---

# 4. Primitive: Sentinel and Neutral Element

## What it is

Every DP needs correct initial values.

For `min` DP:

```text
sentinel = +infinity
neutral base = 0
```

For `max` DP:

```text
sentinel = -infinity
neutral base = 0 or problem-specific value
```

For counting DP:

```text
sentinel = 0
base count = 1
```

For boolean feasibility:

```text
sentinel = False
base feasible = True
```

## Mental invariant

```text
Impossible states must not accidentally win.
Base states must be exactly the empty-solution truth.
```

## Examples

### Coin Change minimum coins

```python
INF = 10**18
dp = [INF] * (amount + 1)
dp[0] = 0
```

### Coin Change number of ways

```python
dp = [0] * (amount + 1)
dp[0] = 1
```

### Knapsack max value

```python
dp = [0] * (capacity + 1)
```

or, if exact-fill is required:

```python
NEG = -10**18
dp = [NEG] * (capacity + 1)
dp[0] = 0
```

That distinction matters.

---

# 5. Primitive: Topological Order

## What it is

The topological order is the order in which states are computed so dependencies are ready first.

Common orders:

```text
increasing i
decreasing i
row-major grid order
reverse row-major grid order
increasing interval length
increasing capacity
decreasing capacity
increasing mask
postorder tree traversal
topological order of DAG
```

## Mental invariant

```text
When computing dp[state], every state it reads must already be correct.
```

## Examples

### Prefix DP

```text
dp[i] reads dp[i-1], dp[i-2]
therefore compute i increasing
```

### Suffix DP

```text
dp[i] reads dp[i+1], dp[i+2]
therefore compute i decreasing
```

### Interval DP

```text
dp[l][r] reads shorter intervals
therefore compute by increasing length
```

### 0/1 Knapsack 1D

```text
dp[w] reads previous item layer dp[w - weight]
therefore capacity must go backward
```

### Unbounded Knapsack 1D

```text
dp[w] may reuse same item again
therefore capacity goes forward
```

This is one of the most important DP trap zones.

---

# 6. Primitive: Base Case

## What it is

Base cases are known states from which the rest of the DAG grows.

## Mental invariant

```text
A base case is not a hack to avoid index errors.
A base case is a mathematically meaningful smallest subproblem.
```

## Examples

### Empty prefix

```text
dp[0] = 0
```

Means:

```text
best answer on empty array is 0
```

### Empty string alignment

```text
edit_distance("", word) = len(word)
edit_distance(word, "") = len(word)
```

### Empty capacity

```text
dp[0] = 0
```

Means:

```text
capacity 0 has zero cost / one empty way / zero value
```

Depending on problem type.

### Interval DP

```text
dp[i][i] = base value for one element
dp[i][i-1] = empty interval, if using empty intervals
```

## Trap

Do not add redundant base cases blindly.

Example:

```python
if n == 0:
    return 0
if n == 1:
    return nums[0]
```

May be fine, but a cleaner DP can often absorb this with sentinel initialization:

```python
prev2 = 0
prev1 = 0

for x in nums:
    prev2, prev1 = prev1, max(prev1, prev2 + x)

return prev1
```

---

# 7. Primitive: Original Answer Extraction

## What it is

After filling DP states, you still need to know which state answers the original problem.

Examples:

```text
dp[n]
dp[n][m]
dp[0][n-1]
max(dp)
max(dp[n][state] for terminal states)
dfs(root)
dp[(1 << n) - 1]
```

## Mental invariant

```text
The original problem must be represented by one state or a clean aggregation over terminal states.
```

## Examples

### House Robber

```text
answer = dp[n]
```

### Stock

```text
answer = cash / not-holding state
```

Not holding stock at the end is valid. Holding stock at the end usually means unrealized profit and should not be chosen unless the problem says otherwise.

### LIS

```text
answer = max(dp)
```

Because `dp[i]` means LIS ending at `i`, not LIS over full prefix.

This distinction matters:

```text
dp[i] = best ending at i        -> answer is max(dp)
dp[i] = best in prefix nums[:i] -> answer is dp[n]
```

---

# 8. Primitive: Complexity Accounting

## What it is

DP complexity is usually:

```text
number of states × transition cost
```

## Examples

### House Robber

```text
states: n
transition per state: O(1)
time: O(n)
space: O(n), or O(1) after rolling
```

### Edit Distance

```text
states: n × m
transition per state: O(1)
time: O(nm)
space: O(nm), or O(min(n, m)) with rolling rows
```

### Interval split DP

```text
states: O(n²)
transition: choose split k -> O(n)
time: O(n³)
space: O(n²)
```

### Bitmask DP

```text
states: 2^n
transition: O(n)
time: O(n 2^n)
space: O(2^n)
```

## Mental invariant

```text
Never say O(n²) just because the table is 2D.
Always multiply by transition cost.
```

This is why interval DP often becomes O(n³), not O(n²).

---

# 9. Core Python Templates

These are not full solutions. They are the reusable skeletons.

## 9.1 Top-Down Memo Skeleton

```python
from functools import cache
from typing import Callable, Iterable, TypeVar

State = TypeVar("State")
Value = TypeVar("Value")


def memo_dp(
    start: State,
    base: Callable[[State], Value | None],
    transitions: Callable[[State], Iterable[State]],
    combine: Callable[[State, list[Value]], Value],
) -> Value:
    @cache
    def solve(state: State) -> Value:
        known = base(state)

        if known is not None:
            return known

        vals = [solve(nxt) for nxt in transitions(state)]
        return combine(state, vals)

    return solve(start)
```

This is conceptually useful, but in interviews you usually write the specialized version directly.

Example shape:

```python
from functools import cache


def top_down_example(n: int) -> int:
    @cache
    def dp(i: int) -> int:
        if i <= 1:
            return i

        return dp(i - 1) + dp(i - 2)

    return dp(n)
```

---

## 9.2 Bottom-Up 1D Prefix DP

```python
def prefix_dp(nums: list[int]) -> list[int]:
    n = len(nums)
    dp = [0] * (n + 1)

    for i, x in enumerate(nums, start=1):
        dp[i] = transition_prefix(dp, nums, i, x)

    return dp


def transition_prefix(
    dp: list[int],
    nums: list[int],
    i: int,
    x: int,
) -> int:
    raise NotImplementedError
```

For real problems, this becomes something like:

```python
def house_robber_path(nums: list[int]) -> int:
    dp = [0] * (len(nums) + 1)

    for i, x in enumerate(nums, start=1):
        skip = dp[i - 1]
        take = dp[i - 2] + x
        dp[i] = max(skip, take)

    return dp[-1]
```

Composition:

```text
prefix state
+ take/skip recurrence
+ max aggregation
-> House Robber path skeleton
```

---

## 9.3 Rolling Two-Variable DP

```python
def rolling_take_skip(nums: list[int]) -> int:
    prev2 = 0
    prev1 = 0

    for x in nums:
        curr = max(prev1, prev2 + x)
        prev2, prev1 = prev1, curr

    return prev1
```

Mental model:

```text
prev2 = dp[i - 2]
prev1 = dp[i - 1]
curr  = dp[i]
```

This is the clean House Robber primitive.

---

## 9.4 Grid DP Skeleton

```python
def grid_dp(grid: list[list[int]]) -> list[list[int]]:
    if not grid or not grid[0]:
        return []

    rows = len(grid)
    cols = len(grid[0])
    dp = [[0] * cols for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            dp[r][c] = transition_grid(grid, dp, r, c)

    return dp


def transition_grid(
    grid: list[list[int]],
    dp: list[list[int]],
    r: int,
    c: int,
) -> int:
    raise NotImplementedError
```

Example: minimum path sum style.

```python
def min_path_sum(grid: list[list[int]]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    dp = [[0] * cols for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            best_prev = min(
                dp[r - 1][c] if r > 0 else float("inf"),
                dp[r][c - 1] if c > 0 else float("inf"),
            )

            dp[r][c] = grid[r][c] + (0 if r == c == 0 else best_prev)

    return dp[-1][-1]
```

Composition:

```text
cell state dp[r][c]
+ top/left predecessor recurrence
+ row-major order
-> grid path DP
```

---

## 9.5 Two-Sequence DP Skeleton

```python
def two_sequence_dp(a: str, b: str) -> list[list[int]]:
    n = len(a)
    m = len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    initialize_two_sequence(dp, a, b)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = transition_two_sequence(a, b, dp, i, j)

    return dp


def initialize_two_sequence(
    dp: list[list[int]],
    a: str,
    b: str,
) -> None:
    pass


def transition_two_sequence(
    a: str,
    b: str,
    dp: list[list[int]],
    i: int,
    j: int,
) -> int:
    raise NotImplementedError
```

LCS specialization:

```python
def lcs_length(a: str, b: str) -> int:
    n = len(a)
    m = len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]
```

Composition:

```text
two-prefix state
+ match/mismatch recurrence
+ row-major order
-> LCS / Edit Distance / Distinct Subsequences family
```

---

## 9.6 Interval DP by Length

```python
def interval_dp(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(1, n + 1):
        for l in range(0, n - length + 1):
            r = l + length - 1
            dp[l][r] = transition_interval(nums, dp, l, r)

    return dp


def transition_interval(
    nums: list[int],
    dp: list[list[int]],
    l: int,
    r: int,
) -> int:
    raise NotImplementedError
```

Stone Game score-difference specialization:

```python
def score_difference_game(nums: list[int]) -> int:
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(1, n + 1):
        for l in range(0, n - length + 1):
            r = l + length - 1

            if l == r:
                dp[l][r] = nums[l]
            else:
                take_left = nums[l] - dp[l + 1][r]
                take_right = nums[r] - dp[l][r - 1]
                dp[l][r] = max(take_left, take_right)

    return dp[0][n - 1]
```

Composition:

```text
interval state
+ increasing length order
+ choose boundary transition
+ score-difference invariant
-> Predict the Winner / Stone Game family
```

---

## 9.7 0/1 Knapsack Reverse Loop

```python
def zero_one_knapsack(
    weights: list[int],
    values: list[int],
    capacity: int,
) -> int:
    dp = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        for cap in range(capacity, weight - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - weight] + value)

    return dp[capacity]
```

Mental invariant:

```text
Backward capacity loop ensures each item is used at most once.
```

If you loop forward, you accidentally allow repeated use of the same item.

---

## 9.8 Unbounded Knapsack Forward Loop

```python
def unbounded_knapsack(
    weights: list[int],
    values: list[int],
    capacity: int,
) -> int:
    dp = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        for cap in range(weight, capacity + 1):
            dp[cap] = max(dp[cap], dp[cap - weight] + value)

    return dp[capacity]
```

Mental invariant:

```text
Forward capacity loop allows the current item to be reused.
```

This distinction is huge:

```text
0/1 item usage       -> reverse capacity
unbounded item usage -> forward capacity
```

---

## 9.9 Stock State Machine Skeleton

```python
def stock_unlimited(prices: list[int]) -> int:
    hold = float("-inf")
    cash = 0

    for price in prices:
        hold = max(hold, cash - price)
        cash = max(cash, hold + price)

    return cash
```

Safer update when old states must be preserved:

```python
def stock_state_machine(prices: list[int]) -> int:
    hold = float("-inf")
    cash = 0

    for price in prices:
        old_hold = hold
        old_cash = cash

        hold = max(old_hold, old_cash - price)
        cash = max(old_cash, old_hold + price)

    return cash
```

Mental model:

```text
hold = best profit after today while holding stock
cash = best profit after today while not holding stock
```

Stock variants add constraints:

```text
transaction limit -> add transaction dimension
cooldown          -> add sold/rest states or shifted recurrence
fee               -> subtract fee on buy or sell
```

---

# 10. The Core Composition Chains

## Chain 1 — House Robber

```text
prefix state dp[i]
+ take/skip recurrence
+ max aggregation
+ rolling two-variable compression
-> House Robber path skeleton
-> 198, 213, 740
```

## Chain 2 — Stock

```text
day index
+ holding/not-holding state
+ buy/sell/rest transitions
+ terminal answer = not holding
-> Stock state-machine skeleton
-> 121, 122, 123, 188, 309, 714
```

## Chain 3 — Knapsack

```text
capacity state dp[w]
+ include/exclude transition
+ max/sum/min aggregation
+ reverse or forward capacity loop
-> Knapsack / Coin Change skeleton
-> 416, 474, 494, 518, 879, 1049
```

## Chain 4 — Two-Sequence DP

```text
two-prefix state dp[i][j]
+ match/mismatch transition
+ row-major table order
-> Alignment skeleton
-> 72, 97, 115, 583, 712, 1035, 1143, 1092
```

## Chain 5 — Interval DP

```text
interval state dp[l][r]
+ choose boundary or split point
+ increasing interval length
-> Interval DP skeleton
-> 312, 375, 486, 877, 1000, 1039, 1547, 1690
```

---

# 11. The Core Diagnostic Questions

For any DP problem, run this checklist:

```text
1. What is the state?
2. What information must the state remember?
3. What choices are available from this state?
4. Do choices reduce to smaller states?
5. What is the aggregation operator?
6. What are the base cases?
7. What order makes dependencies available?
8. Which state gives the final answer?
9. How many states exist?
10. How expensive is each transition?
11. Can space be compressed?
12. Is this really DP, or is it Greedy / BFS / shortest path / backtracking?
```

The next part should be:

```text
Part 3 — 1D DP Families

Fibonacci
-> Climbing Stairs
-> Min Cost Climbing Stairs
-> Decode Ways
-> House Robber I
-> House Robber II
-> Delete and Earn
-> House Robber III as tree-state evolution
```


"""

from __future__ import annotations

from bisect import bisect_left
from collections import deque
from functools import cache
from math import inf
from typing import Callable, Deque, Iterable, Iterator, Optional, Sequence, TypeVar


State = TypeVar("State")
Value = TypeVar("Value")


# =============================================================================
# Level 0 — Diagnostics / Utility Primitives
# =============================================================================


def impossible_min() -> float:
    """
    Sentinel for min-cost DP.

    Invariant:
        Impossible states must not accidentally win a min().
    """
    return inf


def impossible_max() -> float:
    """
    Sentinel for max-value DP.

    Invariant:
        Impossible states must not accidentally win a max().
    """
    return -inf


def state_count_1d(n: int) -> int:
    return n + 1


def state_count_2d(n: int, m: int) -> int:
    return (n + 1) * (m + 1)


def state_count_interval(n: int) -> int:
    return n * (n + 1) // 2


def state_count_bitmask(n: int) -> int:
    return 1 << n


# =============================================================================
# Level 1 — Generic Memoized DP Skeleton
# =============================================================================


def memo_dp(
    start: State,
    base: Callable[[State], Optional[Value]],
    transitions: Callable[[State], Iterable[State]],
    combine: Callable[[State, list[Value]], Value],
) -> Value:
    """
    Generic top-down memo DP.

    This is mainly pedagogical. In interviews, usually write the specialized
    recurrence directly.

    S:
        State is provided by caller.

    R:
        transitions(state) returns dependency states.

    T:
        Top-down DFS with memoization implicitly evaluates the reachable
        subproblem DAG.

    B:
        base(state) returns a known value or None.

    O:
        answer is solve(start).

    T:
        number of reachable states × transition cost.
    """

    @cache
    def solve(state: State) -> Value:
        known = base(state)

        if known is not None:
            return known

        vals = [solve(nxt) for nxt in transitions(state)]
        return combine(state, vals)

    return solve(start)


# =============================================================================
# Level 2 — 1D Prefix / Suffix DP Primitives
# =============================================================================


def fibonacci(n: int) -> int:
    """
    dp[i] = dp[i - 1] + dp[i - 2]

    State:
        dp[i] = ith Fibonacci number.

    Topological order:
        increasing i.

    Space:
        O(1) via rolling variables.
    """
    if n <= 1:
        return n

    prev2 = 0
    prev1 = 1

    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2

    return prev1


def climb_stairs(n: int) -> int:
    """
    Same skeleton as Fibonacci.

    State:
        ways[i] = number of ways to reach step i.

    Recurrence:
        ways[i] = ways[i - 1] + ways[i - 2]
    """
    prev2 = 1
    prev1 = 1

    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2

    return prev1


def min_cost_climbing_stairs(cost: list[int]) -> int:
    """
    Prefix DP with local transition.

    State:
        dp[i] = minimum cost to reach step i.

    Recurrence:
        dp[i] = min(dp[i - 1] + cost[i - 1],
                    dp[i - 2] + cost[i - 2])

    Original problem:
        dp[n], where n is the virtual top.
    """
    prev2 = 0
    prev1 = 0

    for i in range(2, len(cost) + 1):
        curr = min(prev1 + cost[i - 1], prev2 + cost[i - 2])
        prev2, prev1 = prev1, curr

    return prev1


def take_skip_prefix(nums: list[int]) -> int:
    """
    Generic take-or-skip 1D prefix primitive.

    Canonical use:
        House Robber path.

    State:
        dp[i] = best answer for nums[:i].

    Recurrence:
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1])

    Space compression:
        prev2 = dp[i - 2]
        prev1 = dp[i - 1]
    """
    prev2 = 0
    prev1 = 0

    for x in nums:
        curr = max(prev1, prev2 + x)
        prev2, prev1 = prev1, curr

    return prev1


def house_robber_path(nums: list[int]) -> int:
    return take_skip_prefix(nums)


def house_robber_cycle(nums: list[int]) -> int:
    """
    House Robber II.

    Reduction:
        Cycle breaks into two path cases:
            exclude last
            exclude first

    This composes:
        cycle constraint + path primitive.
    """
    if len(nums) <= 1:
        return nums[0] if nums else 0

    return max(
        house_robber_path(nums[:-1]),
        house_robber_path(nums[1:]),
    )


def decode_ways(s: str) -> int:
    """
    1D prefix counting DP.

    State:
        dp[i] = number of ways to decode s[:i].

    Recurrence:
        use one char if valid
        use two chars if valid

    Aggregation:
        sum, not min/max.
    """
    prev2 = 1
    prev1 = 0 if not s or s[0] == "0" else 1

    for i in range(2, len(s) + 1):
        one = s[i - 1]
        two = s[i - 2:i]

        curr = 0

        if one != "0":
            curr += prev1

        if "10" <= two <= "26":
            curr += prev2

        prev2, prev1 = prev1, curr

    return prev1


# =============================================================================
# Level 3 — Local / Global Kadane-Style DP
# =============================================================================


def max_subarray_sum(nums: list[int]) -> int:
    """
    Kadane skeleton.

    State:
        local = best subarray sum ending at current index.
        best  = best subarray sum seen anywhere.

    Recurrence:
        local = max(x, local + x)

    Trap:
        This is subarray DP, not subsequence DP.
    """
    local = nums[0]
    best = nums[0]

    for x in nums[1:]:
        local = max(x, local + x)
        best = max(best, local)

    return best


def max_product_subarray(nums: list[int]) -> int:
    """
    Local/global DP with two local states.

    Why two states:
        A negative number can turn the minimum product into the maximum product.

    State:
        hi = maximum product ending here
        lo = minimum product ending here
    """
    hi = nums[0]
    lo = nums[0]
    best = nums[0]

    for x in nums[1:]:
        a = x
        b = hi * x
        c = lo * x

        hi = max(a, b, c)
        lo = min(a, b, c)
        best = max(best, hi)

    return best


# =============================================================================
# Level 4 — Grid DP Primitives
# =============================================================================


def unique_paths(rows: int, cols: int) -> int:
    """
    Grid counting DP.

    State:
        dp[r][c] = number of ways to reach cell (r, c).

    Recurrence:
        from top + from left.

    Space:
        O(cols) rolling row.
    """
    dp = [1] * cols

    for _ in range(1, rows):
        for c in range(1, cols):
            dp[c] += dp[c - 1]

    return dp[-1]


def min_path_sum(grid: list[list[int]]) -> int:
    """
    Grid min-cost DP.

    State:
        dp[c] = min path sum to current row's cell c.

    Topological order:
        row-major, because each cell depends on top and left.
    """
    cols = len(grid[0])
    dp = [inf] * cols
    dp[0] = 0

    for row in grid:
        for c, x in enumerate(row):
            left = dp[c - 1] if c > 0 else inf
            top = dp[c]
            dp[c] = x + min(top, left)

    return int(dp[-1])


def min_falling_path_sum(grid: list[list[int]]) -> int:
    """
    Grid DP with three predecessors.

    State:
        dp[c] = best path ending at column c in previous row.

    Recurrence:
        current[c] = grid[r][c] + min(prev[c-1], prev[c], prev[c+1])
    """
    prev = grid[0][:]

    for row in grid[1:]:
        curr = [0] * len(row)

        for c, x in enumerate(row):
            best = prev[c]

            if c > 0:
                best = min(best, prev[c - 1])

            if c + 1 < len(row):
                best = min(best, prev[c + 1])

            curr[c] = x + best

        prev = curr

    return min(prev)


# =============================================================================
# Level 5 — Two-Sequence DP Primitives
# =============================================================================


def lcs_length(a: str, b: str) -> int:
    """
    Longest Common Subsequence.

    State:
        dp[i][j] = LCS length of a[:i] and b[:j].

    Recurrence:
        match     -> 1 + dp[i-1][j-1]
        mismatch  -> max(dp[i-1][j], dp[i][j-1])

    Space:
        O(min(n, m)) possible, but table version is clearer.
    """
    n = len(a)
    m = len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]


def edit_distance(a: str, b: str) -> int:
    """
    Edit Distance.

    State:
        dp[i][j] = min edits to convert a[:i] -> b[:j].

    Base:
        empty prefix to non-empty prefix costs length.

    Recurrence:
        delete, insert, replace/match.
    """
    n = len(a)
    m = len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i

    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )

    return dp[n][m]


def distinct_subsequences(source: str, target: str) -> int:
    """
    Count target as a subsequence of source.

    State:
        dp[i][j] = number of ways target[:j] appears in source[:i].

    Recurrence:
        skip source[i-1]
        use source[i-1] if it matches target[j-1]
    """
    n = len(source)
    m = len(target)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = 1

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = dp[i - 1][j]

            if source[i - 1] == target[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]

    return dp[n][m]


# =============================================================================
# Level 6 — Interval DP Primitives
# =============================================================================


def score_difference_game(nums: list[int]) -> int:
    """
    Interval game DP.

    State:
        dp[l][r] = maximum score difference current player can force
                  over opponent from nums[l:r+1].

    Recurrence:
        take_left  = nums[l] - dp[l+1][r]
        take_right = nums[r] - dp[l][r-1]

    Topological order:
        increasing interval length.
    """
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(1, n + 1):
        for l in range(0, n - length + 1):
            r = l + length - 1

            if l == r:
                dp[l][r] = nums[l]
            else:
                take_left = nums[l] - dp[l + 1][r]
                take_right = nums[r] - dp[l][r - 1]
                dp[l][r] = max(take_left, take_right)

    return dp[0][n - 1]


def min_cost_cut_positions(n: int, cuts: list[int]) -> int:
    """
    Interval split DP.

    Example skeleton:
        Minimum Cost to Cut a Stick.

    State:
        dp[l][r] = min cost to finish cuts strictly between points[l], points[r].

    Recurrence:
        choose first cut k inside interval.
    """
    points = [0] + sorted(cuts) + [n]
    m = len(points)
    dp = [[0] * m for _ in range(m)]

    for width in range(2, m):
        for l in range(0, m - width):
            r = l + width

            dp[l][r] = min(
                points[r] - points[l] + dp[l][k] + dp[k][r]
                for k in range(l + 1, r)
            )

    return dp[0][m - 1]


# =============================================================================
# Level 7 — Knapsack / Capacity DP Primitives
# =============================================================================


def zero_one_knapsack(
    weights: list[int],
    values: list[int],
    capacity: int,
) -> int:
    """
    0/1 knapsack.

    State:
        dp[w] = max value achievable with processed items and capacity w.

    Critical invariant:
        Iterate capacity backward so each item is used at most once.
    """
    dp = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        for cap in range(capacity, weight - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - weight] + value)

    return dp[capacity]


def unbounded_knapsack(
    weights: list[int],
    values: list[int],
    capacity: int,
) -> int:
    """
    Unbounded knapsack.

    Critical invariant:
        Iterate capacity forward so current item can be reused.
    """
    dp = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        for cap in range(weight, capacity + 1):
            dp[cap] = max(dp[cap], dp[cap - weight] + value)

    return dp[capacity]


def subset_sum_possible(nums: list[int], target: int) -> bool:
    """
    0/1 feasibility DP.

    Aggregation:
        boolean OR.

    Loop direction:
        backward, because each number can be used once.
    """
    dp = [False] * (target + 1)
    dp[0] = True

    for x in nums:
        for s in range(target, x - 1, -1):
            dp[s] = dp[s] or dp[s - x]

    return dp[target]


def coin_change_min(coins: list[int], amount: int) -> int:
    """
    Unbounded min-count DP.

    State:
        dp[x] = fewest coins to make x.

    Sentinel:
        +infinity for impossible states.
    """
    dp = [inf] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return -1 if dp[amount] == inf else int(dp[amount])


def coin_change_combinations(coins: list[int], amount: int) -> int:
    """
    Count combinations, order-insensitive.

    Loop order:
        coin outer, amount inner.

    This prevents counting permutations as distinct.
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] += dp[x - coin]

    return dp[amount]


def coin_change_permutations(nums: list[int], target: int) -> int:
    """
    Count permutations / ordered sequences.

    Loop order:
        amount outer, number inner.

    This intentionally counts different orders separately.
    """
    dp = [0] * (target + 1)
    dp[0] = 1

    for x in range(1, target + 1):
        for num in nums:
            if x >= num:
                dp[x] += dp[x - num]

    return dp[target]


# =============================================================================
# Level 8 — Stock State-Machine DP Primitives
# =============================================================================


def stock_one_transaction(prices: list[int]) -> int:
    """
    Best Time to Buy and Sell Stock I.

    This is a compressed state-machine:
        best_buy = best value of -price seen so far
        best     = best sell profit so far
    """
    best_buy = -inf
    best = 0

    for price in prices:
        best_buy = max(best_buy, -price)
        best = max(best, best_buy + price)

    return int(best)


def stock_unlimited_transactions(prices: list[int]) -> int:
    """
    Unlimited transactions.

    State:
        hold = best profit after today while holding stock
        cash = best profit after today while not holding stock

    Use old states when transitions conceptually happen from yesterday.
    """
    hold = -inf
    cash = 0

    for price in prices:
        old_hold = hold
        old_cash = cash

        hold = max(old_hold, old_cash - price)
        cash = max(old_cash, old_hold + price)

    return int(cash)


def stock_with_fee(prices: list[int], fee: int) -> int:
    """
    Unlimited transactions with fee.

    Fee can be charged either on buy or sell, as long as consistent.
    This version charges fee on sell.
    """
    hold = -inf
    cash = 0

    for price in prices:
        old_hold = hold
        old_cash = cash

        hold = max(old_hold, old_cash - price)
        cash = max(old_cash, old_hold + price - fee)

    return int(cash)


def stock_with_cooldown(prices: list[int]) -> int:
    """
    Cooldown state-machine.

    States:
        hold = holding stock
        sold = sold today, cooldown tomorrow
        rest = not holding and not just sold

    Answer:
        max(sold, rest), because ending while holding has unrealized profit.
    """
    hold = -inf
    sold = -inf
    rest = 0

    for price in prices:
        old_hold = hold
        old_sold = sold
        old_rest = rest

        hold = max(old_hold, old_rest - price)
        sold = old_hold + price
        rest = max(old_rest, old_sold)

    return int(max(sold, rest))


def stock_k_transactions(prices: list[int], k: int) -> int:
    """
    At most k transactions.

    State:
        buy[t]  = best profit after t-th buy / holding
        sell[t] = best profit after t-th sell / not holding

    t is 1-indexed for transaction count.

    Complexity:
        O(nk)
    """
    buy = [-inf] * (k + 1)
    sell = [0] * (k + 1)

    for price in prices:
        for t in range(1, k + 1):
            buy[t] = max(buy[t], sell[t - 1] - price)
            sell[t] = max(sell[t], buy[t] + price)

    return int(sell[k])


# =============================================================================
# Level 9 — Tree DP Primitives
# =============================================================================


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right


def rob_tree(root: Optional[TreeNode]) -> int:
    """
    House Robber III.

    State:
        dfs(node) -> (skip_node, take_node)

    Recurrence:
        take node -> cannot take children
        skip node -> may take or skip each child

    Topological order:
        postorder, because parent depends on child states.
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


def binary_tree_max_path_sum(root: Optional[TreeNode]) -> int:
    """
    Tree DP with local return and global answer.

    Return value:
        best downward path starting at node.

    Global:
        best path through any node.
    """
    best = -inf

    def dfs(node: Optional[TreeNode]) -> int:
        nonlocal best

        if node is None:
            return 0

        left = max(0, dfs(node.left))
        right = max(0, dfs(node.right))

        best = max(best, node.val + left + right)

        return node.val + max(left, right)

    dfs(root)
    return int(best)


# =============================================================================
# Level 10 — Bitmask DP Primitives
# =============================================================================


def shortest_path_visiting_all_nodes(graph: list[list[int]]) -> int:
    """
    BFS over bitmask state.

    This is a DP/graph hybrid.

    State:
        (node, mask) where mask says which nodes have been visited.

    Original problem:
        any state with full mask.
    """
    n = len(graph)
    full = (1 << n) - 1

    q: Deque[tuple[int, int, int]] = deque()
    seen = set()

    for node in range(n):
        mask = 1 << node
        q.append((node, mask, 0))
        seen.add((node, mask))

    while q:
        node, mask, dist = q.popleft()

        if mask == full:
            return dist

        for nxt in graph[node]:
            nxt_state = (nxt, mask | (1 << nxt))

            if nxt_state not in seen:
                seen.add(nxt_state)
                q.append((nxt, nxt_state[1], dist + 1))

    return -1


def assignment_min_cost(cost: list[list[int]]) -> int:
    """
    Bitmask assignment DP.

    State:
        dp[mask] = min cost after assigning first popcount(mask) workers
                  to selected jobs in mask.

    Transition:
        assign next worker to one unused job.
    """
    n = len(cost)
    full = 1 << n
    dp = [inf] * full
    dp[0] = 0

    for mask in range(full):
        worker = mask.bit_count()

        if worker >= n:
            continue

        for job in range(n):
            if not (mask & (1 << job)):
                nxt = mask | (1 << job)
                dp[nxt] = min(dp[nxt], dp[mask] + cost[worker][job])

    return int(dp[-1])


# =============================================================================
# Level 11 — Digit DP Primitive
# =============================================================================


def count_without_consecutive_ones(n: int) -> int:
    """
    Digit DP example for binary representation.

    State:
        pos
        tight
        prev_one

    This counts integers x in [0, n] whose binary representation has no
    consecutive ones.
    """
    bits = bin(n)[2:]

    @cache
    def dp(pos: int, tight: bool, prev_one: bool) -> int:
        if pos == len(bits):
            return 1

        limit = int(bits[pos]) if tight else 1
        total = 0

        for bit in range(limit + 1):
            if prev_one and bit == 1:
                continue

            total += dp(
                pos + 1,
                tight and bit == limit,
                bit == 1,
            )

        return total

    return dp(0, True, False)


# =============================================================================
# Level 12 — Monotonic Deque DP Primitive
# =============================================================================


def constrained_subsequence_sum(nums: list[int], k: int) -> int:
    """
    Monotonic deque DP.

    State:
        dp[i] = best subsequence sum ending at i.

    Recurrence:
        dp[i] = nums[i] + max(0, max(dp[j]) for j in [i-k, i-1])

    Optimization:
        Maintain max dp[j] in a deque over sliding window.
    """
    dq: Deque[int] = deque()
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


# =============================================================================
# Level 13 — LIS / Binary Search Optimization Primitive
# =============================================================================


def lis_length(nums: list[int]) -> int:
    """
    Patience sorting LIS length.

    tails[len - 1] = minimum possible tail value of an increasing subsequence
                    of length len.

    This is not the same as dp[i] = LIS ending at i.
    It is an optimized representation of frontier states.
    """
    tails: list[int] = []

    for x in nums:
        i = bisect_left(tails, x)

        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x

    return len(tails)


def lis_length_quadratic(nums: list[int]) -> int:
    """
    O(n^2) LIS.

    State:
        dp[i] = LIS length ending exactly at i.

    Answer:
        max(dp), not dp[-1].
    """
    if not nums:
        return 0

    dp = [1] * len(nums)

    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


# =============================================================================
# Core Diagnostic Checklist
# =============================================================================


DP_DIAGNOSTIC_CHECKLIST = [
    "What is the state?",
    "What information must the state remember?",
    "What choices are available from this state?",
    "Do choices reduce to smaller states?",
    "What is the aggregation operator?",
    "What are the base cases?",
    "What order makes dependencies available?",
    "Which state gives the final answer?",
    "How many states exist?",
    "How expensive is each transition?",
    "Can space be compressed?",
    "Is this really DP, or is it Greedy / BFS / shortest path / backtracking?",
]


if __name__ == "__main__":
    assert fibonacci(10) == 55
    assert climb_stairs(5) == 8
    assert min_cost_climbing_stairs([10, 15, 20]) == 15
    assert house_robber_path([2, 7, 9, 3, 1]) == 12
    assert house_robber_cycle([2, 3, 2]) == 3
    assert decode_ways("226") == 3
    assert max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_product_subarray([2, 3, -2, 4]) == 6
    assert unique_paths(3, 7) == 28
    assert min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
    assert lcs_length("abcde", "ace") == 3
    assert edit_distance("horse", "ros") == 3
    assert distinct_subsequences("rabbbit", "rabbit") == 3
    assert score_difference_game([1, 5, 2]) == -2
    assert zero_one_knapsack([1, 3, 4], [15, 20, 30], 4) == 35
    assert subset_sum_possible([1, 5, 11, 5], 11)
    assert coin_change_min([1, 2, 5], 11) == 3
    assert coin_change_combinations([1, 2, 5], 5) == 4
    assert stock_one_transaction([7, 1, 5, 3, 6, 4]) == 5
    assert stock_unlimited_transactions([7, 1, 5, 3, 6, 4]) == 7
    assert stock_with_fee([1, 3, 2, 8, 4, 9], 2) == 8
    assert lis_length([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert lis_length_quadratic([10, 9, 2, 5, 3, 7, 101, 18]) == 4
