"""
Part 6 — Knapsack / Capacity Dynamic Programming Families

Scope:
    0/1 Knapsack
    Unbounded Knapsack
    Subset Sum
    Partition Equal Subset Sum
    Target Sum
    Last Stone Weight II
    Ones and Zeroes
    Coin Change
    Coin Change II
    Combination Sum IV
    Number of Dice Rolls With Target Sum
    Profitable Schemes
    Form Largest Integer With Digits That Add up to Target

Core mental model:
    Capacity DP adds an integer resource dimension:
        sum
        capacity
        target
        budget
        people
        profit
        zeros/ones

    The most important primitive is not the table.
    It is the loop direction.

Critical loop rules:
    0/1 item used at most once:
        iterate capacity backward

    Unbounded item can be reused:
        iterate capacity forward

    Count combinations:
        item outer, capacity inner

    Count permutations:
        capacity outer, item inner

SRTBOT:
    S — Subproblems
    R — Relationships / include-exclude or add-item transitions
    T — Topological order / reverse or forward capacity
    B — Base cases
    O — Original problem / answer extraction
    T — Time complexity = states × transition cost





# Part 6 — Knapsack / Capacity DP

Python file:

[Download Part 6 — Knapsack / Capacity DP Python file](sandbox:/mnt/data/dp_part6_knapsack_capacity_dp.py)

## What Part 6 covers

```text
Knapsack / Capacity DP
    -> 0/1 Knapsack
    -> Subset Sum
    -> Partition Equal Subset Sum
    -> Target Sum
    -> Last Stone Weight II
    -> Ones and Zeroes
    -> Profitable Schemes
    -> Unbounded Knapsack
    -> Coin Change
    -> Coin Change II
    -> Combination Sum IV
    -> Dice Rolls With Target Sum
    -> Form Largest Integer With Digits That Add up to Target
```

## Core mental model

Capacity DP adds an integer resource dimension:

```text
dp[w]
dp[sum]
dp[target]
dp[people][profit]
dp[zeros][ones]
```

The most important question is:

```text
Can I use the current item once or many times?
```

That determines loop direction.

---

## The two most important loop rules

### 1. 0/1 item usage

Each item can be used at most once.

```python
for item in items:
    for w in range(capacity, weight - 1, -1):
        dp[w] = combine(dp[w], dp[w - weight] + value)
```

Why backward?

```text
Backward loop preserves the previous item-layer.
So the current item cannot consume itself again.
```

Used by:

```text
416. Partition Equal Subset Sum
494. Target Sum
474. Ones and Zeroes
1049. Last Stone Weight II
879. Profitable Schemes
```

---

### 2. Unbounded item usage

Each item can be reused many times.

```python
for item in items:
    for w in range(weight, capacity + 1):
        dp[w] = combine(dp[w], dp[w - weight] + value)
```

Why forward?

```text
Forward loop allows dp[w - weight] to already include the current item.
So the current item can be reused.
```

Used by:

```text
322. Coin Change
518. Coin Change II
343. Integer Break
1449. Form Largest Integer With Digits That Add up to Target
```

---

## Counting loop-order rule

This is the second big trap.

### Combinations: order does not matter

```python
for coin in coins:
    for x in range(coin, amount + 1):
        dp[x] += dp[x - coin]
```

This counts:

```text
1 + 2
```

and

```text
2 + 1
```

as the same combination.

Used by:

```text
518. Coin Change II
```

---

### Permutations: order matters

```python
for x in range(1, target + 1):
    for num in nums:
        if x >= num:
            dp[x] += dp[x - num]
```

This counts:

```text
1 + 2
```

and

```text
2 + 1
```

as different ordered sequences.

Used by:

```text
377. Combination Sum IV
```

---

## SRTBOT for 0/1 Knapsack

```text
S — dp[w] = best/count/possible value at capacity or sum w

R — skip current item or take current item once:
        dp[w] = combine(dp[w], dp[w - weight] + value)

T — item loop outside, capacity loop backward

B — dp[0] = neutral value

O — dp[target] or dp[capacity]

T — O(number_of_items × capacity)
```

---

## SRTBOT for Unbounded Knapsack

```text
S — dp[w] = best/count/min value for amount w

R — use current item:
        dp[w] = combine(dp[w], dp[w - weight] + contribution)

T — item loop outside, capacity loop forward

B — dp[0] = neutral value

O — dp[target]

T — O(number_of_items × capacity)
```

---

## Composition chains

```text
capacity state dp[s]
+ boolean feasibility
+ reverse loop
-> Subset Sum
-> 416, 1049
```

```text
target algebra transformation
+ subset-count DP
+ reverse loop
-> Target Sum
-> 494
```

```text
two capacity dimensions
+ 0/1 reverse loops in both dimensions
-> Ones and Zeroes
-> 474
```

```text
amount state dp[x]
+ min aggregation
+ forward loop
-> Coin Change minimum coins
-> 322
```

```text
amount state dp[x]
+ sum aggregation
+ item outer loop
-> Coin Change combinations
-> 518
```

```text
amount state dp[x]
+ sum aggregation
+ amount outer loop
-> ordered Combination Sum
-> 377
```

## Most important traps

```text
1. Forward loop accidentally turns 0/1 knapsack into unbounded knapsack.
2. Reverse loop accidentally prevents reuse in unbounded knapsack.
3. dp[0] means different things:
       min coins: 0
       counting: 1
       feasibility: True
       exact string construction: ""
4. Exact-fill DP needs impossible sentinels.
5. At-most-capacity DP can often start with zeros.
6. Coin Change and Coin Change II are not the same recurrence objective.
7. Combination Sum IV counts ordered sequences, not combinations.
8. Target Sum is usually easier after algebraic reduction to subset-count DP.
9. Multi-capacity DP needs all 0/1 dimensions looped backward.
```

Next natural step: **Part 7 — Interval DP**.

"""

from __future__ import annotations

from math import inf


# =============================================================================
# Level 0 — Capacity DP Utility Primitives
# =============================================================================


def impossible_min() -> float:
    return inf


def impossible_max() -> float:
    return -inf


def exact_fill_max_array(capacity: int) -> list[float]:
    """
    For exact-fill max-value DP.

    dp[w] = max value for exactly weight w.

    Impossible states must be -inf.
    Empty capacity is exactly achievable with value 0.
    """
    dp = [-inf] * (capacity + 1)
    dp[0] = 0
    return dp


def at_most_capacity_max_array(capacity: int) -> list[int]:
    """
    For at-most-capacity max-value DP.

    dp[w] = max value using capacity at most w.

    Starting all zeros is valid because choosing nothing is always feasible.
    """
    return [0] * (capacity + 1)


def count_array(target: int) -> list[int]:
    """
    For counting ways to form target.

    dp[0] = 1 means there is one empty way to form sum 0.
    """
    dp = [0] * (target + 1)
    dp[0] = 1
    return dp


def feasible_array(target: int) -> list[bool]:
    """
    For boolean feasibility.

    dp[0] = True means sum 0 is achievable by choosing nothing.
    """
    dp = [False] * (target + 1)
    dp[0] = True
    return dp


# =============================================================================
# Level 1 — 0/1 Knapsack Primitives
# =============================================================================


def zero_one_knapsack(
    weights: list[int],
    values: list[int],
    capacity: int,
) -> int:
    """
    Classical 0/1 knapsack.

    S:
        dp[w] = max value achievable with processed items and capacity at most w.

    R:
        For each item:
            skip item:
                dp[w]
            take item:
                dp[w - weight] + value

    T:
        capacity decreasing.

    B:
        dp[w] = 0 for all w, because choosing nothing is feasible.

    O:
        dp[capacity]

    T:
        O(n * capacity)

    Critical invariant:
        Reverse capacity loop ensures each item is used at most once.
    """
    dp = at_most_capacity_max_array(capacity)

    for weight, value in zip(weights, values):
        for w in range(capacity, weight - 1, -1):
            dp[w] = max(dp[w], dp[w - weight] + value)

    return dp[capacity]


def subset_sum_possible(nums: list[int], target: int) -> bool:
    """
    0/1 feasibility DP.

    S:
        dp[s] = whether sum s is achievable using processed numbers.

    R:
        dp[s] = dp[s] or dp[s - x]

    T:
        s decreasing for each x.

    B:
        dp[0] = True.

    O:
        dp[target]

    Trap:
        Forward loop would allow using x multiple times.
    """
    dp = feasible_array(target)

    for x in nums:
        for s in range(target, x - 1, -1):
            dp[s] = dp[s] or dp[s - x]

    return dp[target]


def can_partition(nums: list[int]) -> bool:
    """
    LeetCode:
        416. Partition Equal Subset Sum

    Reduction:
        Can nums be split into two subsets with equal sum?
        Equivalent to subset sum target = total / 2.

    Trap:
        Odd total immediately impossible.
    """
    total = sum(nums)

    if total % 2:
        return False

    return subset_sum_possible(nums, total // 2)


def last_stone_weight_ii(stones: list[int]) -> int:
    """
    LeetCode:
        1049. Last Stone Weight II

    Reduction:
        Split stones into two groups with sums s and total-s.
        Final difference = abs(total - 2s).
        Choose s as close as possible to total // 2.

    This is Partition Equal Subset Sum's optimization variant.
    """
    total = sum(stones)
    target = total // 2
    dp = feasible_array(target)

    for x in stones:
        for s in range(target, x - 1, -1):
            dp[s] = dp[s] or dp[s - x]

    best = max(s for s, ok in enumerate(dp) if ok)
    return total - 2 * best


def find_target_sum_ways(nums: list[int], target: int) -> int:
    """
    LeetCode:
        494. Target Sum

    Algebraic reduction:
        Let P be sum of positive-signed numbers.
        Let N be sum of negative-signed numbers.

            P - N = target
            P + N = total

        Therefore:
            P = (total + target) / 2

    Count subsets with sum P.

    S:
        dp[s] = number of ways to choose processed nums summing to s.

    T:
        reverse loop because each number is used once.

    Trap:
        If total + target is odd or negative, answer is 0.
    """
    total = sum(nums)
    want = total + target

    if want < 0 or want % 2:
        return 0

    subset = want // 2
    dp = count_array(subset)

    for x in nums:
        for s in range(subset, x - 1, -1):
            dp[s] += dp[s - x]

    return dp[subset]


def find_target_sum_ways_shifted(nums: list[int], target: int) -> int:
    """
    Direct signed-sum DP using offset.

    This is less elegant than the subset-sum reduction but useful when
    the algebraic transformation is not obvious.

    State:
        ways[sum] = number of ways to reach signed sum.

    Complexity:
        O(n * total_sum)
    """
    total = sum(nums)

    if abs(target) > total:
        return 0

    offset = total
    ways = [0] * (2 * total + 1)
    ways[offset] = 1

    for x in nums:
        nxt = [0] * (2 * total + 1)

        for s, count in enumerate(ways):
            if count == 0:
                continue

            nxt[s + x] += count
            nxt[s - x] += count

        ways = nxt

    return ways[target + offset]


# =============================================================================
# Level 2 — Multi-Capacity 0/1 Knapsack
# =============================================================================


def find_max_form(strs: list[str], m: int, n: int) -> int:
    """
    LeetCode:
        474. Ones and Zeroes

    0/1 knapsack with two capacity dimensions:
        zeros capacity m
        ones capacity n

    S:
        dp[z][o] = max number of strings using at most z zeros and o ones.

    R:
        take current string:
            dp[z - zeros][o - ones] + 1

    T:
        both dimensions decreasing because each string can be used once.

    O:
        dp[m][n]

    Trap:
        Both loops must go backward.
    """
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for s in strs:
        zeros = s.count("0")
        ones = len(s) - zeros

        for z in range(m, zeros - 1, -1):
            for o in range(n, ones - 1, -1):
                dp[z][o] = max(dp[z][o], dp[z - zeros][o - ones] + 1)

    return dp[m][n]


def profitable_schemes(
    n: int,
    min_profit: int,
    group: list[int],
    profit: list[int],
) -> int:
    """
    LeetCode:
        879. Profitable Schemes

    Multi-dimensional 0/1 counting DP.

    S:
        dp[people][profit] = number of schemes using processed crimes
                             with at most people people and capped profit.

    Profit dimension is capped at min_profit:
        any profit >= min_profit is collapsed to min_profit.

    R:
        take/skip each crime.

    T:
        people decreasing and profit decreasing, because each crime is used once.

    O:
        sum(dp[people][min_profit]) over people <= n

    Trap:
        Profit must be capped to avoid unnecessary huge state.
    """
    mod = 10**9 + 7
    dp = [[0] * (min_profit + 1) for _ in range(n + 1)]
    dp[0][0] = 1

    for people, earn in zip(group, profit):
        for used in range(n, people - 1, -1):
            for p in range(min_profit, -1, -1):
                new_profit = min(min_profit, p + earn)
                dp[used][new_profit] = (
                    dp[used][new_profit]
                    + dp[used - people][p]
                ) % mod

    return sum(dp[used][min_profit] for used in range(n + 1)) % mod


# =============================================================================
# Level 3 — Unbounded Knapsack Primitives
# =============================================================================


def unbounded_knapsack(
    weights: list[int],
    values: list[int],
    capacity: int,
) -> int:
    """
    Classical unbounded knapsack.

    S:
        dp[w] = max value achievable with capacity at most w.

    R:
        take current item again:
            dp[w - weight] + value

    T:
        capacity increasing.

    Critical invariant:
        Forward capacity loop allows the same item to be reused.
    """
    dp = at_most_capacity_max_array(capacity)

    for weight, value in zip(weights, values):
        for w in range(weight, capacity + 1):
            dp[w] = max(dp[w], dp[w - weight] + value)

    return dp[capacity]


def coin_change_min(coins: list[int], amount: int) -> int:
    """
    LeetCode:
        322. Coin Change

    Unbounded min-count DP.

    S:
        dp[x] = fewest coins needed to form amount x.

    R:
        dp[x] = min(dp[x], dp[x - coin] + 1)

    T:
        forward amount loop for each coin.

    B:
        dp[0] = 0
        others = +inf

    O:
        dp[amount], or -1 if impossible.
    """
    dp = [inf] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return -1 if dp[amount] == inf else int(dp[amount])


def coin_change_combinations(amount: int, coins: list[int]) -> int:
    """
    LeetCode:
        518. Coin Change II

    Count combinations, order-insensitive.

    S:
        dp[x] = number of combinations to form x using processed coin types.

    T:
        coin outer, amount inner increasing.

    Why coin outer?
        It fixes an ordering on coin types, so [2,1,1] and [1,2,1]
        are not counted separately.
    """
    dp = count_array(amount)

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] += dp[x - coin]

    return dp[amount]


def combination_sum_iv(nums: list[int], target: int) -> int:
    """
    LeetCode:
        377. Combination Sum IV

    Count permutations / ordered sequences.

    S:
        dp[x] = number of ordered sequences summing to x.

    T:
        amount outer, num inner.

    Why amount outer?
        The last chosen number varies, so order matters.
    """
    dp = count_array(target)

    for x in range(1, target + 1):
        for num in nums:
            if x >= num:
                dp[x] += dp[x - num]

    return dp[target]


def integer_break(n: int) -> int:
    """
    LeetCode:
        343. Integer Break

    Unbounded-ish integer capacity DP.

    S:
        dp[x] = max product obtainable by breaking integer x.

    R:
        split x into first part k and remaining x-k.
        remaining part can be either raw x-k or further broken dp[x-k].

    O:
        dp[n]
    """
    dp = [0] * (n + 1)

    for x in range(2, n + 1):
        for k in range(1, x):
            dp[x] = max(dp[x], k * (x - k), k * dp[x - k])

    return dp[n]


# =============================================================================
# Level 4 — Dice / Bounded Repetition Count DP
# =============================================================================


def num_rolls_to_target(n: int, k: int, target: int) -> int:
    """
    LeetCode:
        1155. Number of Dice Rolls With Target Sum

    S:
        dp[dice][sum] = number of ways after rolling dice dice.

    R:
        dp[d][s] = sum(dp[d-1][s-face]) for face in 1..k.

    T:
        increasing dice count.

    B:
        dp[0][0] = 1

    Complexity:
        O(n * target * k)

    Optimization:
        prefix sums can reduce transition when k is large.
    """
    mod = 10**9 + 7
    prev = [0] * (target + 1)
    prev[0] = 1

    for _ in range(n):
        curr = [0] * (target + 1)

        for s in range(1, target + 1):
            total = 0

            for face in range(1, k + 1):
                if s - face < 0:
                    break

                total += prev[s - face]

            curr[s] = total % mod

        prev = curr

    return prev[target]


def num_rolls_to_target_prefix(n: int, k: int, target: int) -> int:
    """
    Prefix-sum optimized dice DP.

    R:
        curr[s] = prev[s-1] + prev[s-2] + ... + prev[s-k]

    Use sliding window over prev.
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


# =============================================================================
# Level 5 — Exact Target String Construction DP
# =============================================================================


def largest_number_with_cost(cost: list[int], target: int) -> str:
    """
    LeetCode:
        1449. Form Largest Integer With Digits That Add up to Target

    This is unbounded exact-fill max DP with lexicographic reconstruction.

    S:
        dp[t] = largest string number constructible with exact cost t.

    R:
        choose digit d with cost[d], append it.

    Since larger length is better first, and lexicographic order among same length
    matters, comparing strings directly works if we build carefully.

    B:
        dp[0] = ""
        impossible states = None

    O:
        dp[target], or "0" if impossible.

    Trap:
        This is exact target. dp[t] cannot default to "" for all t.
    """
    dp: list[str | None] = [None] * (target + 1)
    dp[0] = ""

    def better(a: str | None, b: str | None) -> str | None:
        if a is None:
            return b

        if b is None:
            return a

        if len(a) != len(b):
            return a if len(a) > len(b) else b

        return max(a, b)

    for t in range(1, target + 1):
        best: str | None = None

        for digit in range(9, 0, -1):
            c = cost[digit - 1]

            if t >= c and dp[t - c] is not None:
                best = better(best, str(digit) + dp[t - c])

        dp[t] = best

    return dp[target] if dp[target] is not None else "0"


# =============================================================================
# Level 6 — Boundary / Recognition Helpers
# =============================================================================


def is_zero_one_loop_direction(item_can_be_reused: bool) -> str:
    """
    A tiny helper to encode the most important capacity-DP question.
    """
    return "forward" if item_can_be_reused else "backward"


def count_loop_order(order_matters: bool) -> str:
    """
    Counting loop-order rule.

    order_matters = False:
        combinations
        item outer, capacity inner

    order_matters = True:
        permutations
        capacity outer, item inner
    """
    return "capacity_outer" if order_matters else "item_outer"


# =============================================================================
# Part 6 Problem Map
# =============================================================================


PART_6_PROBLEM_MAP = {
    "zero_one_knapsack_feasibility": [
        416,
        1049,
    ],
    "zero_one_knapsack_counting": [
        494,
        879,
    ],
    "multi_capacity_zero_one": [
        474,
        879,
    ],
    "unbounded_knapsack_optimization": [
        322,
        343,
        1449,
    ],
    "unbounded_knapsack_count_combinations": [
        518,
    ],
    "unbounded_knapsack_count_permutations": [
        377,
    ],
    "bounded_repetition_counting": [
        1155,
    ],
}


CAPACITY_DP_DIAGNOSTIC_CHECKLIST = [
    "What is the capacity/target dimension?",
    "Is the item used at most once or repeatedly?",
    "Is the state exact-fill or at-most-capacity?",
    "Is the aggregation max, min, count, or boolean feasibility?",
    "What is dp[0]: 0, 1, True, or empty string?",
    "What sentinel represents impossible states?",
    "Should capacity loop backward or forward?",
    "For counting, are combinations or permutations being counted?",
    "Does the problem need more than one capacity dimension?",
    "Can one dimension be capped, such as profit >= min_profit?",
]


if __name__ == "__main__":
    assert zero_one_knapsack([1, 3, 4], [15, 20, 30], 4) == 35
    assert subset_sum_possible([3, 34, 4, 12, 5, 2], 9)
    assert can_partition([1, 5, 11, 5])
    assert not can_partition([1, 2, 3, 5])
    assert last_stone_weight_ii([2, 7, 4, 1, 8, 1]) == 1
    assert find_target_sum_ways([1, 1, 1, 1, 1], 3) == 5
    assert find_target_sum_ways_shifted([1, 1, 1, 1, 1], 3) == 5

    assert find_max_form(["10", "0001", "111001", "1", "0"], 5, 3) == 4
    assert profitable_schemes(5, 3, [2, 2], [2, 3]) == 2

    assert unbounded_knapsack([1, 3, 4], [15, 20, 30], 4) == 60
    assert coin_change_min([1, 2, 5], 11) == 3
    assert coin_change_combinations(5, [1, 2, 5]) == 4
    assert combination_sum_iv([1, 2, 3], 4) == 7
    assert integer_break(10) == 36

    assert num_rolls_to_target(2, 6, 7) == 6
    assert num_rolls_to_target_prefix(2, 6, 7) == 6
    assert largest_number_with_cost([4, 3, 2, 5, 6, 7, 2, 5, 5], 9) == "7772"

    assert is_zero_one_loop_direction(False) == "backward"
    assert is_zero_one_loop_direction(True) == "forward"
    assert count_loop_order(False) == "item_outer"
    assert count_loop_order(True) == "capacity_outer"
