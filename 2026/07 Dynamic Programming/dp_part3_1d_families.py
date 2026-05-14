"""
Part 3 — 1D Dynamic Programming Families

Scope:
    Fibonacci / stair-step recurrence
    prefix/suffix state
    take-or-skip recurrence
    House Robber I
    House Robber II
    Delete and Earn
    House Robber III as the tree-state mutation
    Decode Ways
    Kadane-style local/global DP
    Brainpower-style suffix DP

Mental model:
    Most beginner DP problems become easy once you name the state precisely.

SRTBOT:
    S — Subproblems
    R — Relationships / recurrence edges
    T — Topological order / evaluation order
    B — Base cases
    O — Original problem / final answer extraction
    T — Time complexity = states × transition cost


# Part 3 — 1D DP Families

Python file first, since this should stay consistent with the primitives format:

[Download Part 3 — 1D DP Families Python file](sandbox:/mnt/data/dp_part3_1d_families.py)

## 1. What Part 3 covers

This is the first “real” DP family after the generic primitives:

```text
1D DP
    -> Fibonacci / stair-step recurrence
    -> prefix parsing / Decode Ways
    -> take-or-skip / House Robber
    -> cycle mutation / House Robber II
    -> value-line mutation / Delete and Earn
    -> tree mutation / House Robber III
    -> suffix jump DP / Brainpower, Tickets
    -> local-global DP / Kadane variants
    -> tiny state-machine DP / Wiggle, Alternating Sum
```

The key point:

```text
Most 1D DP is not about arrays.

It is about deciding what dp[i] means.
```

---

# 2. Core 1D DP Mental Model

There are only a few dominant state shapes.

## A. Prefix state

```text
dp[i] = answer for nums[:i]
```

Used by:

```text
Climbing Stairs
Min Cost Climbing Stairs
Decode Ways
House Robber
Coin-style prefix parsing
```

## B. Suffix state

```text
dp[i] = answer for nums[i:]
```

Used when the recurrence naturally jumps forward:

```text
Solving Questions With Brainpower
Minimum Cost For Tickets
Word Break-style suffix recursion
```

## C. Ending-at-i state

```text
dp[i] = best answer ending exactly at i
```

Used by:

```text
Maximum Subarray
Maximum Product Subarray
LIS O(n²)
Arithmetic subsequence variants
```

Important distinction:

```text
prefix best:
    answer = dp[n]

ending-at-i best:
    answer = max(dp)
```

This is a common bug source.

---

# 3. Family 1 — Fibonacci / Stair-Step DP

Canonical recurrence:

```text
dp[i] = dp[i - 1] + dp[i - 2]
```

SRTBOT:

```text
S — dp[i] = number/value for size i
R — depends on i-1 and i-2
T — increasing i
B — dp[0], dp[1]
O — dp[n]
T — O(n) states × O(1) transition = O(n)
```

Representative problems:

```text
509. Fibonacci Number
70. Climbing Stairs
746. Min Cost Climbing Stairs
1137. N-th Tribonacci Number
790. Domino and Tromino Tiling
```

Core evolution:

```text
Fibonacci
-> Climbing Stairs: same recurrence, different base meaning
-> Min Cost Climbing Stairs: same step graph, min aggregation
-> Tribonacci: depends on last 3
-> Tiling: needs auxiliary state or derived recurrence
```

---

# 4. Family 2 — Prefix Parsing / Decode Ways

Canonical state:

```text
dp[i] = number of ways to parse s[:i]
```

Canonical recurrence:

```text
dp[i] += dp[i - 1] if last token is valid
dp[i] += dp[i - 2] if last two-character token is valid
```

SRTBOT:

```text
S — prefixes of the string
R — valid last token of length 1 or 2
T — increasing i
B — dp[0] = 1
O — dp[n]
T — O(n)
```

Representative problems:

```text
91. Decode Ways
639. Decode Ways II
1416. Restore The Array
2266. Count Number of Texts
```

Common trap:

```text
"0" is not valid alone.
"10" and "20" are valid.
"06" is not valid.
```

This family is not “Fibonacci” even if it sometimes looks like it. It is:

```text
prefix parsing
+ valid token lengths
+ sum aggregation
```

---

# 5. Family 3 — Take-or-Skip / House Robber Path

Canonical state:

```text
dp[i] = best answer using nums[:i]
```

Canonical recurrence:

```text
dp[i] = max(
    dp[i - 1],              # skip nums[i - 1]
    dp[i - 2] + nums[i - 1] # take nums[i - 1]
)
```

SRTBOT:

```text
S — prefix nums[:i]
R — skip current or take current
T — increasing i
B — dp[0] = 0, dp[1] = nums[0]
O — dp[n]
T — O(n)
```

Composition chain:

```text
prefix state
+ take/skip recurrence
+ max aggregation
+ rolling variables
-> House Robber path skeleton
-> 198
```

The core rolling primitive:

```python
def take_skip_path(values: list[int]) -> int:
    prev2 = 0
    prev1 = 0

    for x in values:
        prev2, prev1 = prev1, max(prev1, prev2 + x)

    return prev1
```

---

# 6. House Robber Evolution Ladder

## 6.1 House Robber I — Path graph

```text
Problem:
    Cannot take adjacent houses.

Reduction:
    Weighted independent set on a path graph.

State:
    dp[i] = best value from first i houses.
```

Skeleton:

```text
take-or-skip over index
```

---

## 6.2 House Robber II — Cycle graph

New constraint:

```text
first and last are adjacent
```

Reduction:

```text
cycle
-> two path cases:
    exclude last
    exclude first
```

Composition chain:

```text
cycle constraint
+ split into two path graphs
+ House Robber I primitive
-> House Robber II
```

Code shape:

```python
def house_robber_ii(nums: list[int]) -> int:
    if len(nums) <= 1:
        return nums[0] if nums else 0

    return max(
        take_skip_path(nums[:-1]),
        take_skip_path(nums[1:]),
    )
```

---

## 6.3 Delete and Earn — Value-line graph

New shape:

```text
Original array order does not matter.
Numeric adjacency matters.
```

Taking value `x` deletes `x - 1` and `x + 1`.

Reduction:

```text
nums
-> bucket by value
-> points[x] = x * count[x]
-> House Robber on value line
```

Composition chain:

```text
frequency aggregation
+ value-line adjacency
+ House Robber path primitive
-> Delete and Earn
```

This is a beautiful reduction because it teaches:

```text
The "path" in House Robber does not have to be the input array.
The path can be a transformed value axis.
```

---

## 6.4 House Robber III — Tree graph

New shape:

```text
houses are nodes in a binary tree
parent and child cannot both be robbed
```

Now prefix DP no longer works because there is no linear prefix.

State becomes structural:

```text
dfs(node) -> (skip_node, take_node)
```

Recurrence:

```text
take node:
    node.val + left.skip + right.skip

skip node:
    max(left.skip, left.take) + max(right.skip, right.take)
```

Composition chain:

```text
take/skip primitive
+ tree postorder evaluation
+ tuple state per node
-> House Robber III
```

This is the first major lesson:

```text
Same recurrence idea.
Different state shape.
```

Path:

```text
dp[i]
```

Tree:

```text
dfs(node) -> (skip, take)
```

---

# 7. Family 4 — Suffix Jump DP

Canonical state:

```text
dp[i] = best answer from suffix nums[i:]
```

Used when taking an action jumps to a future index.

Example: Brainpower.

```text
dp[i] = max(
    dp[i + 1],
    points[i] + dp[i + brainpower[i] + 1]
)
```

SRTBOT:

```text
S — suffix starting at i
R — skip current or take current and jump
T — decreasing i
B — dp[n] = 0
O — dp[0]
T — O(n), if jump target is O(1)
```

Representative problems:

```text
2140. Solving Questions With Brainpower
983. Minimum Cost For Tickets
1105. Filling Bookcase Shelves
2052. Minimum Cost to Separate Sentence Into Rows
```

This is House Robber-like, but with variable jump distance:

```text
House Robber:
    take -> i + 2

Brainpower:
    take -> i + brainpower[i] + 1
```

---

# 8. Family 5 — Local / Global Kadane DP

Canonical state:

```text
local = best answer ending exactly here
best  = best answer anywhere so far
```

For Maximum Subarray:

```text
local = max(x, local + x)
best = max(best, local)
```

SRTBOT:

```text
S — best subarray ending at i
R — extend previous or restart at current
T — increasing i
B — local = nums[0]
O — best over all local states
T — O(n)
```

Representative problems:

```text
53. Maximum Subarray
152. Maximum Product Subarray
918. Maximum Sum Circular Subarray
1186. Maximum Subarray Sum with One Deletion
1191. K-Concatenation Maximum Sum
1567. Maximum Length of Subarray With Positive Product
1746. Maximum Subarray Sum After One Operation
1749. Maximum Absolute Sum of Any Subarray
```

Important distinction:

```text
Subarray:
    contiguous
    local ending-at-i state is natural

Subsequence:
    not necessarily contiguous
    usually needs take/skip, previous-choice, or state-machine DP
```

---

# 9. Family 6 — Tiny State-Machine 1D DP

Some 1D DP does not look like `dp[i]`, but it still has a small state carried across the scan.

Examples:

```text
Wiggle Subsequence:
    up, down

Maximum Alternating Subsequence Sum:
    even, odd

Stock I/II:
    hold, cash
```

For Wiggle:

```text
up   = best length ending with positive difference
down = best length ending with negative difference
```

For Alternating Sum:

```text
even = best after selecting even number of elements
odd  = best after selecting odd number of elements
```

Composition chain:

```text
scan index
+ finite status variable
+ transition between statuses
-> tiny 1D state-machine DP
```

Representative problems:

```text
376. Wiggle Subsequence
978. Longest Turbulent Subarray
1911. Maximum Alternating Subsequence Sum
2036. Maximum Alternating Subarray Sum
```

---

# 10. DP vs Greedy Boundary in Part 3

Some of these problems look greedy because the state is tiny.

## Kadane

Looks greedy:

```text
if current sum becomes bad, restart
```

But the real invariant is DP:

```text
local(i) = best subarray ending exactly at i
```

## Wiggle

Can be solved greedily, but the clean DP state is:

```text
up/down
```

## House Robber

Cannot be solved by “take bigger of adjacent pair” greedily.

Counterexample:

```text
[2, 1, 1, 2]
```

Greedy local choices can miss the global optimum.

DP works because:

```text
dp[i] preserves enough prefix history.
```

---

# 11. Highest-ROI Practice Order for Part 3

Practice in this order:

```text
1. 70. Climbing Stairs
2. 746. Min Cost Climbing Stairs
3. 91. Decode Ways
4. 198. House Robber
5. 213. House Robber II
6. 740. Delete and Earn
7. 337. House Robber III
8. 2140. Solving Questions With Brainpower
9. 983. Minimum Cost For Tickets
10. 53. Maximum Subarray
11. 152. Maximum Product Subarray
12. 1186. Maximum Subarray Sum with One Deletion
13. 376. Wiggle Subsequence
14. 1911. Maximum Alternating Subsequence Sum
```

Mastery means:

```text
You can name the state before writing code.
You know whether answer is dp[n], dp[0], max(dp), or max terminal states.
You know whether the direction is increasing i or decreasing i.
You can explain why rolling variables are safe.
You can identify when a path DP mutates into tree DP or value-axis DP.
```

The next natural step is **Part 4 — Grid DP**, because it extends 1D state into `dp[r][c]` and makes topological order much more visible.



"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Optional


# =============================================================================
# 1. Fibonacci / Stair-Step Family
# =============================================================================


def fib(n: int) -> int:
    """
    S:
        f(i) = ith Fibonacci number.

    R:
        f(i) = f(i - 1) + f(i - 2)

    T:
        increasing i.

    B:
        f(0) = 0
        f(1) = 1

    O:
        f(n)

    T:
        O(n) time, O(1) space.
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
    Same recurrence shape as Fibonacci.

    S:
        ways(i) = number of ways to reach step i.

    R:
        ways(i) = ways(i - 1) + ways(i - 2)

    B:
        ways(0) = 1
        ways(1) = 1

    O:
        ways(n)

    This is Fibonacci with a shifted base interpretation.
    """
    prev2 = 1
    prev1 = 1

    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2

    return prev1


def min_cost_climbing_stairs(cost: list[int]) -> int:
    """
    Stair-step recurrence with min aggregation.

    S:
        dp(i) = minimum cost to reach step i.

    R:
        dp(i) = min(
            dp(i - 1) + cost[i - 1],
            dp(i - 2) + cost[i - 2],
        )

    T:
        increasing i.

    B:
        dp(0) = 0
        dp(1) = 0

    O:
        dp(n), where n is the virtual top beyond the last stair.

    Trap:
        The final answer is not necessarily standing on the last index.
        It is standing on the virtual top.
    """
    prev2 = 0
    prev1 = 0

    for i in range(2, len(cost) + 1):
        curr = min(prev1 + cost[i - 1], prev2 + cost[i - 2])
        prev2, prev1 = prev1, curr

    return prev1


def num_tilings(n: int) -> int:
    """
    Domino and Tromino tiling style recurrence.

    This is still 1D DP, but the recurrence is less local-looking unless
    derived using auxiliary states.

    LeetCode:
        790. Domino and Tromino Tiling

    Known compressed recurrence:
        dp[n] = 2 * dp[n - 1] + dp[n - 3]

    B:
        dp[0] = 1
        dp[1] = 1
        dp[2] = 2
    """
    mod = 10**9 + 7

    if n <= 2:
        return [1, 1, 2][n]

    a = 1
    b = 1
    c = 2

    for _ in range(3, n + 1):
        a, b, c = b, c, (2 * c + a) % mod

    return c


# =============================================================================
# 2. Decode Ways / Prefix Parsing Family
# =============================================================================


def decode_ways(s: str) -> int:
    """
    LeetCode:
        91. Decode Ways

    S:
        dp(i) = number of ways to decode s[:i].

    R:
        Use last one char if valid:
            dp(i) += dp(i - 1)

        Use last two chars if valid:
            dp(i) += dp(i - 2)

    T:
        increasing i.

    B:
        dp(0) = 1
        dp(1) = 1 if s[0] != '0' else 0

    O:
        dp(n)

    Trap:
        '0' cannot stand alone.
        '10' and '20' are valid.
        '06' is not valid.
    """
    if not s:
        return 0

    prev2 = 1
    prev1 = 0 if s[0] == "0" else 1

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


def count_texts(pressed_keys: str) -> int:
    """
    LeetCode:
        2266. Count Number of Texts

    Same prefix parsing skeleton as Decode Ways.

    S:
        dp(i) = number of ways to parse pressed_keys[:i].

    R:
        Look backward up to 3 or 4 equal digits depending on key.

    T:
        increasing i.

    B:
        dp(0) = 1

    O:
        dp(n)
    """
    mod = 10**9 + 7
    n = len(pressed_keys)
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        digit = pressed_keys[i - 1]
        limit = 4 if digit in "79" else 3

        for size in range(1, limit + 1):
            if i - size < 0:
                break

            if pressed_keys[i - size:i] != digit * size:
                break

            dp[i] = (dp[i] + dp[i - size]) % mod

    return dp[n]


# =============================================================================
# 3. Take-or-Skip / Weighted Independent Set on Path
# =============================================================================


def take_skip_path(values: list[int]) -> int:
    """
    Generic take-or-skip path primitive.

    S:
        dp(i) = best value using values[:i].

    R:
        skip current:
            dp(i - 1)

        take current:
            dp(i - 2) + values[i - 1]

        dp(i) = max(skip, take)

    T:
        increasing i.

    B:
        dp(0) = 0
        dp(1) = max(0, values[0]) in generic form.
        For House Robber with non-negative values, rolling zero base is enough.

    O:
        dp(n)

    Complexity:
        O(n) time, O(1) space.
    """
    prev2 = 0
    prev1 = 0

    for x in values:
        prev2, prev1 = prev1, max(prev1, prev2 + x)

    return prev1


def house_robber(nums: list[int]) -> int:
    """
    LeetCode:
        198. House Robber

    Reduction:
        Weighted independent set on a path graph.

    Composition:
        prefix state
        + take-or-skip recurrence
        + rolling variables
    """
    return take_skip_path(nums)


def house_robber_ii(nums: list[int]) -> int:
    """
    LeetCode:
        213. House Robber II

    New constraint:
        first and last houses are adjacent.

    Reduction:
        Cycle -> two path problems.

    Cases:
        1. Exclude last house: nums[:-1]
        2. Exclude first house: nums[1:]

    Answer:
        max(case1, case2)

    Trap:
        Need to handle n <= 1 separately.
    """
    if len(nums) <= 1:
        return nums[0] if nums else 0

    return max(
        take_skip_path(nums[:-1]),
        take_skip_path(nums[1:]),
    )


def delete_and_earn(nums: list[int]) -> int:
    """
    LeetCode:
        740. Delete and Earn

    Reduction:
        Values become houses on a number line.

        Taking value x earns:
            x * count[x]

        But then x - 1 and x + 1 cannot be taken.

    This is House Robber over compressed value buckets.

    S:
        bucket[v] = total points available at value v.
        Then solve take-or-skip over v = 0..max(nums).

    Trap:
        The adjacency is by numeric value, not original index.
    """
    if not nums:
        return 0

    points = Counter(nums)
    values = [0] * (max(points) + 1)

    for x, count in points.items():
        values[x] = x * count

    return take_skip_path(values)


# =============================================================================
# 4. House Robber III — Tree Mutation of Take-or-Skip
# =============================================================================


@dataclass
class TreeNode:
    val: int = 0
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def house_robber_iii(root: Optional[TreeNode]) -> int:
    """
    LeetCode:
        337. House Robber III

    This is no longer 1D prefix DP. It is the structural mutation of
    House Robber from path graph -> tree graph.

    S:
        dfs(node) returns two values:
            skip = best value in subtree if node is skipped
            take = best value in subtree if node is taken

    R:
        take node:
            node.val + left.skip + right.skip

        skip node:
            max(left.skip, left.take) + max(right.skip, right.take)

    T:
        postorder traversal because parent depends on child states.

    B:
        dfs(None) = (0, 0)

    O:
        max(skip_root, take_root)

    Complexity:
        O(n) time, O(h) recursion stack.
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


# =============================================================================
# 5. Suffix DP / Jump Forward Families
# =============================================================================


def most_points(questions: list[list[int]]) -> int:
    """
    LeetCode:
        2140. Solving Questions With Brainpower

    S:
        dp(i) = max points obtainable from questions[i:].

    R:
        skip question i:
            dp(i + 1)

        solve question i:
            points[i] + dp(i + brainpower[i] + 1)

    T:
        decreasing i because dp(i) depends on future suffix states.

    B:
        dp(n) = 0 and dp(i) = 0 for i >= n.

    O:
        dp(0)

    This is House Robber-like take/skip, but the skip distance is variable.
    """
    n = len(questions)
    dp = [0] * (n + 1)

    for i in range(n - 1, -1, -1):
        points, jump = questions[i]
        nxt = min(n, i + jump + 1)
        take = points + dp[nxt]
        skip = dp[i + 1]
        dp[i] = max(skip, take)

    return dp[0]


def min_cost_tickets(days: list[int], costs: list[int]) -> int:
    """
    LeetCode:
        983. Minimum Cost For Tickets

    S:
        dp(i) = min cost to cover travel days starting at index i.

    R:
        choose one of the passes: 1-day, 7-day, 30-day.
        Jump to first uncovered travel day.

    T:
        decreasing i.

    B:
        dp(n) = 0

    O:
        dp(0)

    This is suffix DP with variable jump transitions.
    """
    n = len(days)
    durations = [1, 7, 30]
    dp = [0] * (n + 1)

    for i in range(n - 1, -1, -1):
        best = float("inf")

        for duration, cost in zip(durations, costs):
            j = i

            while j < n and days[j] < days[i] + duration:
                j += 1

            best = min(best, cost + dp[j])

        dp[i] = best

    return dp[0]


# =============================================================================
# 6. Local / Global DP Families
# =============================================================================


def max_subarray(nums: list[int]) -> int:
    """
    LeetCode:
        53. Maximum Subarray

    S:
        local(i) = max subarray sum ending exactly at i.
        best(i) = max subarray sum anywhere in nums[:i+1].

    R:
        local = max(nums[i], local + nums[i])
        best = max(best, local)

    This is DP, but it looks greedy because the state is tiny.
    """
    local = nums[0]
    best = nums[0]

    for x in nums[1:]:
        local = max(x, local + x)
        best = max(best, local)

    return best


def max_subarray_with_one_deletion(nums: list[int]) -> int:
    """
    LeetCode:
        1186. Maximum Subarray Sum with One Deletion

    S:
        keep = best subarray sum ending here with no deletion.
        drop = best subarray sum ending here with one deletion used.

    R:
        keep' = max(x, keep + x)
        drop' = max(keep, drop + x)

    Why drop' can be keep:
        delete current x, so the best one-deletion sum ending here is the
        previous no-deletion sum.
    """
    keep = nums[0]
    drop = 0
    best = nums[0]

    for x in nums[1:]:
        old_keep = keep
        keep = max(x, keep + x)
        drop = max(old_keep, drop + x)
        best = max(best, keep, drop)

    return best


def max_product_subarray(nums: list[int]) -> int:
    """
    LeetCode:
        152. Maximum Product Subarray

    S:
        hi = max product ending here.
        lo = min product ending here.

    Why both:
        A negative number can turn minimum into maximum.
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


def wiggle_max_length(nums: list[int]) -> int:
    """
    LeetCode:
        376. Wiggle Subsequence

    S:
        up   = best wiggle subsequence ending with positive difference.
        down = best wiggle subsequence ending with negative difference.

    This is a tiny state-machine DP.
    """
    up = 1
    down = 1

    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            up = down + 1
        elif nums[i] < nums[i - 1]:
            down = up + 1

    return max(up, down)


def maximum_alternating_subsequence_sum(nums: list[int]) -> int:
    """
    LeetCode:
        1911. Maximum Alternating Subsequence Sum

    S:
        even = best alternating sum with next selected item contributing plus.
        odd  = best alternating sum with next selected item contributing minus.

    Equivalent interpretation:
        even = best after selecting even count of elements.
        odd  = best after selecting odd count of elements.
    """
    even = 0
    odd = 0

    for x in nums:
        even, odd = max(even, odd + x), max(odd, even - x)

    return even


# =============================================================================
# 7. Representative Problem Map for Part 3
# =============================================================================


PART_3_PROBLEM_MAP = {
    "fibonacci_stair_step": [
        70,
        746,
        1137,
        790,
    ],
    "prefix_parsing_counting": [
        91,
        639,
        1416,
        2266,
    ],
    "take_or_skip_path": [
        198,
        213,
        740,
        2140,
    ],
    "take_or_skip_tree": [
        337,
    ],
    "suffix_variable_jump": [
        983,
        2140,
    ],
    "local_global_kadane": [
        53,
        152,
        918,
        1186,
        1191,
        1567,
        1746,
        1749,
    ],
    "tiny_state_machine": [
        376,
        1911,
        978,
    ],
}


if __name__ == "__main__":
    assert fib(10) == 55
    assert climb_stairs(5) == 8
    assert min_cost_climbing_stairs([10, 15, 20]) == 15
    assert num_tilings(3) == 5

    assert decode_ways("226") == 3
    assert count_texts("22233") == 8

    assert house_robber([2, 7, 9, 3, 1]) == 12
    assert house_robber_ii([2, 3, 2]) == 3
    assert delete_and_earn([3, 4, 2]) == 6

    root = TreeNode(
        3,
        TreeNode(2, None, TreeNode(3)),
        TreeNode(3, None, TreeNode(1)),
    )
    assert house_robber_iii(root) == 7

    assert most_points([[3, 2], [4, 3], [4, 4], [2, 5]]) == 5
    assert min_cost_tickets([1, 4, 6, 7, 8, 20], [2, 7, 15]) == 11

    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray_with_one_deletion([1, -2, 0, 3]) == 4
    assert max_product_subarray([2, 3, -2, 4]) == 6
    assert wiggle_max_length([1, 7, 4, 9, 2, 5]) == 6
    assert maximum_alternating_subsequence_sum([4, 2, 5, 3]) == 7
