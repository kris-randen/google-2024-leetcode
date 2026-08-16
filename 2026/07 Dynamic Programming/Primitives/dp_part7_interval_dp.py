"""
Part 7 — Interval Dynamic Programming Families

Scope:
    Longest Palindromic Subsequence
    Minimum Insertions to Make a String Palindrome
    Palindromic Substrings
    Longest Palindromic Substring
    Palindrome Partitioning II
    Predict the Winner
    Burst Balloons
    Minimum Score Triangulation of Polygon
    Minimum Cost to Cut a Stick
    Minimum Cost to Merge Stones
    Strange Printer
    Remove Boxes

Core mental model:
    Interval DP uses states of the form:

        dp[l][r] = answer for interval items[l:r+1]

    or sometimes half-open:

        dp[l][r] = answer for interval items[l:r]

    The topological order is usually:
        increasing interval length

    because larger intervals depend on smaller intervals.

Main recurrence shapes:
    1. Boundary choice:
        choose left or choose right

    2. Match/shrink:
        if s[l] == s[r], use inside interval

    3. Split point:
        choose k inside interval and combine dp[l][k] + dp[k][r]

    4. Last operation / first operation:
        choose the final balloon, final cut, final print, final merge, etc.

SRTBOT:
    S — Subproblems
    R — Relationships / boundary or split transitions
    T — Topological order / increasing interval length
    B — Base cases / empty or singleton intervals
    O — Original problem / usually dp[0][n-1] or dp[0][n]
    T — Time complexity = O(n^2 states × transition cost)



# Part 7 — Interval DP

Python file:

[Download Part 7 — Interval DP Python file](sandbox:/mnt/data/dp_part7_interval_dp.py)

## What Part 7 covers

```text id="kybxsz"
Interval DP
    -> Longest Palindromic Subsequence
    -> Minimum Insertions to Make a String Palindrome
    -> Palindromic Substrings
    -> Longest Palindromic Substring
    -> Palindrome Partitioning II
    -> Palindrome Partitioning III
    -> Predict the Winner
    -> Stone Game
    -> Stone Game VII
    -> Burst Balloons
    -> Minimum Score Triangulation
    -> Minimum Cost to Cut a Stick
    -> Minimum Cost to Merge Stones
    -> Strange Printer
    -> Remove Boxes
```

## Core mental model

```text id="8jh12p"
dp[l][r] = answer for interval items[l:r+1]
```

The topological order is usually:

```text id="bwk8ig"
increasing interval length
```

because larger intervals depend on smaller intervals.

## Main recurrence shapes

### 1. Boundary choice

```text id="dyuafz"
choose left
choose right
```

Used by:

```text id="eepc47"
Predict the Winner
Stone Game
Stone Game VII
```

### 2. Match and shrink

```text id="mf1nl9"
if s[l] == s[r]:
    use dp[l+1][r-1]
else:
    use dp[l+1][r] / dp[l][r-1]
```

Used by:

```text id="m77lvh"
Longest Palindromic Subsequence
Minimum Insertions to Palindrome
Palindromic Substrings
```

### 3. Split point

```text id="20w0qi"
for k in range(l, r):
    combine dp[l][k] and dp[k+1][r]
```

Used by:

```text id="ds8y93"
Minimum Score Triangulation
Cut Stick
Merge Stones
Minimum Cost Tree From Leaf Values
```

### 4. Last operation

```text id="bt8j8n"
Choose the last balloon / last cut / last print / final merge.
```

Used by:

```text id="a09oba"
Burst Balloons
Strange Printer
Remove Boxes
```

This is often the trickiest mental move.

## Big trap

A 2D interval table does **not** imply O(n²).

```text id="mgk8nh"
states = O(n²)
transition = O(n) split point
total = O(n³)
```

That is why problems like Burst Balloons, Cut Stick, and Triangulation are usually O(n³).

## Most important composition chains

```text id="u6ukju"
interval state dp[l][r]
+ increasing length order
+ match/shrink recurrence
-> Palindromic subsequence family
```

```text id="rm738q"
interval state dp[l][r]
+ choose left/right
+ score-difference invariant
-> Predict the Winner / Stone Game family
```

```text id="ow6rn9"
open interval with sentinels
+ choose last balloon
+ split into independent left/right intervals
-> Burst Balloons
```

```text id="zjxv6p"
sentinel cut positions
+ choose first cut inside segment
+ segment length cost
-> Minimum Cost to Cut a Stick
```

```text id="drjlzt"
interval state dp[l][r]
+ extra carry dimension
+ merge equal colors later
-> Remove Boxes
```

## Diagnostic checklist

```text id="71390k"
1. Is the natural state dp[l][r]?
2. Is the interval inclusive [l, r] or half-open [l, r)?
3. Does the recurrence choose a boundary or a split point?
4. Does choosing the last operation make the problem independent?
5. What are the empty/singleton base cases?
6. Does increasing interval length make dependencies ready?
7. Is each transition O(1) or O(n)?
8. Do interval sums need prefix sums?
9. Is dp[l][r] sufficient, or do we need extra state?
10. Is there a faster non-DP solution, like monotonic stack?
```

Next natural step: **Part 8 — Stock Series**.

"""

from __future__ import annotations

from functools import cache
from math import inf


# =============================================================================
# Level 0 — Interval Utilities
# =============================================================================


def inclusive_intervals(n: int):
    """
    Generate inclusive intervals [l, r] in increasing length order.

    This is the canonical fill order for dp[l][r] where both l and r
    are included.
    """
    for length in range(1, n + 1):
        for l in range(0, n - length + 1):
            r = l + length - 1
            yield l, r, length


def half_open_intervals(n: int):
    """
    Generate half-open intervals [l, r) in increasing width order.

    Useful when boundaries are sentinel positions, as in cut-stick DP.
    """
    for width in range(1, n + 1):
        for l in range(0, n - width + 1):
            r = l + width
            yield l, r, width


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
    """
    Half-open range sum:
        sum nums[l:r]
    """
    return ps[r] - ps[l]


# =============================================================================
# Level 1 — Palindromic Subsequence / Match-Shrink DP
# =============================================================================


def longest_palindromic_subsequence(s: str) -> int:
    """
    LeetCode:
        516. Longest Palindromic Subsequence

    S:
        dp[l][r] = LPS length inside s[l:r+1].

    R:
        if s[l] == s[r]:
            dp[l][r] = 2 + dp[l+1][r-1]
        else:
            dp[l][r] = max(dp[l+1][r], dp[l][r-1])

    T:
        increasing interval length.

    B:
        dp[i][i] = 1

    O:
        dp[0][n-1]

    Trap:
        This is subsequence, not substring.
    """
    n = len(s)

    if n == 0:
        return 0

    dp = [[0] * n for _ in range(n)]

    for l, r, length in inclusive_intervals(n):
        if length == 1:
            dp[l][r] = 1
        elif s[l] == s[r]:
            dp[l][r] = 2 + (dp[l + 1][r - 1] if l + 1 <= r - 1 else 0)
        else:
            dp[l][r] = max(dp[l + 1][r], dp[l][r - 1])

    return dp[0][n - 1]


def min_insertions_to_palindrome(s: str) -> int:
    """
    LeetCode:
        1312. Minimum Insertion Steps to Make a String Palindrome

    Reduction:
        Minimum insertions = n - longest palindromic subsequence.

    Because all characters not in an LPS must be mirrored by insertion.
    """
    return len(s) - longest_palindromic_subsequence(s)


def min_insertions_to_palindrome_direct(s: str) -> int:
    """
    Direct interval DP.

    S:
        dp[l][r] = min insertions to make s[l:r+1] a palindrome.

    R:
        if s[l] == s[r]:
            dp[l][r] = dp[l+1][r-1]
        else:
            dp[l][r] = 1 + min(dp[l+1][r], dp[l][r-1])
    """
    n = len(s)

    if n == 0:
        return 0

    dp = [[0] * n for _ in range(n)]

    for l, r, length in inclusive_intervals(n):
        if length <= 1:
            dp[l][r] = 0
        elif s[l] == s[r]:
            dp[l][r] = dp[l + 1][r - 1] if l + 1 <= r - 1 else 0
        else:
            dp[l][r] = 1 + min(dp[l + 1][r], dp[l][r - 1])

    return dp[0][n - 1]


# =============================================================================
# Level 2 — Palindromic Substring DP
# =============================================================================


def palindromic_substrings_count(s: str) -> int:
    """
    LeetCode:
        647. Palindromic Substrings

    S:
        is_pal[l][r] = whether s[l:r+1] is a palindrome.

    R:
        s[l] == s[r] and inside is palindrome.

    T:
        increasing interval length.

    B:
        length 1 is palindrome.
        length 2 is palindrome if both chars equal.

    O:
        count all true states.

    Trap:
        Substring is contiguous.
    """
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    count = 0

    for l, r, length in inclusive_intervals(n):
        if length == 1:
            is_pal[l][r] = True
        elif length == 2:
            is_pal[l][r] = s[l] == s[r]
        else:
            is_pal[l][r] = s[l] == s[r] and is_pal[l + 1][r - 1]

        if is_pal[l][r]:
            count += 1

    return count


def longest_palindromic_substring(s: str) -> str:
    """
    LeetCode:
        5. Longest Palindromic Substring

    Same is_pal interval table as Palindromic Substrings.

    O:
        longest true interval.
    """
    n = len(s)

    if n == 0:
        return ""

    is_pal = [[False] * n for _ in range(n)]
    best_l = 0
    best_len = 1

    for l, r, length in inclusive_intervals(n):
        if length == 1:
            is_pal[l][r] = True
        elif length == 2:
            is_pal[l][r] = s[l] == s[r]
        else:
            is_pal[l][r] = s[l] == s[r] and is_pal[l + 1][r - 1]

        if is_pal[l][r] and length > best_len:
            best_l = l
            best_len = length

    return s[best_l:best_l + best_len]


# =============================================================================
# Level 3 — Palindrome Partitioning
# =============================================================================


def min_cut_palindrome_partition(s: str) -> int:
    """
    LeetCode:
        132. Palindrome Partitioning II

    This combines:
        interval palindrome table
        + 1D prefix partition DP

    S:
        is_pal[l][r] = whether s[l:r+1] is palindrome.
        cuts[i] = minimum cuts needed for s[:i].

    R:
        if s[j:i] is palindrome:
            cuts[i] = min(cuts[i], cuts[j] + 1)

    Base trick:
        cuts[0] = -1
        so if s[:i] is one palindrome, cuts[i] = 0.

    O:
        cuts[n]
    """
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]

    for l, r, length in inclusive_intervals(n):
        if length == 1:
            is_pal[l][r] = True
        elif length == 2:
            is_pal[l][r] = s[l] == s[r]
        else:
            is_pal[l][r] = s[l] == s[r] and is_pal[l + 1][r - 1]

    cuts = [inf] * (n + 1)
    cuts[0] = -1

    for i in range(1, n + 1):
        for j in range(i):
            if is_pal[j][i - 1]:
                cuts[i] = min(cuts[i], cuts[j] + 1)

    return int(cuts[n])


def palindrome_partition_k_changes(s: str, k: int) -> int:
    """
    LeetCode:
        1278. Palindrome Partitioning III

    Problem:
        Partition s into k non-empty substrings and change minimum characters
        so each substring is palindrome.

    Two-layer DP:
        1. cost[l][r] = min changes to make s[l:r+1] palindrome.
        2. dp[parts][i] = min changes to partition s[:i] into parts palindromes.

    Complexity:
        O(n^2 + k*n^2)
    """
    n = len(s)
    cost = [[0] * n for _ in range(n)]

    for l, r, length in inclusive_intervals(n):
        if length <= 1:
            cost[l][r] = 0
        else:
            cost[l][r] = cost[l + 1][r - 1] + (0 if s[l] == s[r] else 1)

    dp = [[inf] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = 0

    for parts in range(1, k + 1):
        for i in range(parts, n + 1):
            for j in range(parts - 1, i):
                dp[parts][i] = min(dp[parts][i], dp[parts - 1][j] + cost[j][i - 1])

    return int(dp[k][n])


# =============================================================================
# Level 4 — Boundary-Choice Game DP
# =============================================================================


def score_difference_game(nums: list[int]) -> int:
    """
    LeetCode:
        486. Predict the Winner
        877. Stone Game

    S:
        dp[l][r] = maximum score difference current player can force
                  over opponent from nums[l:r+1].

    R:
        take left:
            nums[l] - dp[l+1][r]

        take right:
            nums[r] - dp[l][r-1]

        dp[l][r] = max(take_left, take_right)

    T:
        increasing interval length.

    B:
        dp[i][i] = nums[i]

    O:
        dp[0][n-1]

    Interpretation:
        If dp[0][n-1] >= 0, first player can tie or win.
    """
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for l, r, length in inclusive_intervals(n):
        if length == 1:
            dp[l][r] = nums[l]
        else:
            take_left = nums[l] - dp[l + 1][r]
            take_right = nums[r] - dp[l][r - 1]
            dp[l][r] = max(take_left, take_right)

    return dp[0][n - 1]


def predict_the_winner(nums: list[int]) -> bool:
    return score_difference_game(nums) >= 0


def stone_game(nums: list[int]) -> bool:
    return score_difference_game(nums) > 0


def stone_game_vii(stones: list[int]) -> int:
    """
    LeetCode:
        1690. Stone Game VII

    Score gained after removing a stone is sum of remaining stones.

    S:
        dp[l][r] = maximum score difference current player can force
                  from stones[l:r+1].

    R:
        remove left:
            sum(l+1..r) - dp[l+1][r]

        remove right:
            sum(l..r-1) - dp[l][r-1]

    Uses prefix sums for O(1) interval sums.
    """
    n = len(stones)
    ps = prefix_sums(stones)
    dp = [[0] * n for _ in range(n)]

    for l, r, length in inclusive_intervals(n):
        if length == 1:
            dp[l][r] = 0
        else:
            remove_left = range_sum(ps, l + 1, r + 1) - dp[l + 1][r]
            remove_right = range_sum(ps, l, r) - dp[l][r - 1]
            dp[l][r] = max(remove_left, remove_right)

    return dp[0][n - 1]


# =============================================================================
# Level 5 — Split-Point Interval DP
# =============================================================================


def min_score_triangulation(values: list[int]) -> int:
    """
    LeetCode:
        1039. Minimum Score Triangulation of Polygon

    S:
        dp[l][r] = min triangulation score for polygon chain l..r.

    R:
        choose k as the third vertex of triangle (l, k, r):
            dp[l][k] + dp[k][r] + values[l]*values[k]*values[r]

    T:
        increasing interval width.

    B:
        fewer than 3 vertices -> 0.

    Complexity:
        O(n^3)
    """
    n = len(values)
    dp = [[0] * n for _ in range(n)]

    for length in range(3, n + 1):
        for l in range(0, n - length + 1):
            r = l + length - 1

            dp[l][r] = min(
                dp[l][k] + dp[k][r] + values[l] * values[k] * values[r]
                for k in range(l + 1, r)
            )

    return dp[0][n - 1]


def min_cost_cut_stick(n: int, cuts: list[int]) -> int:
    """
    LeetCode:
        1547. Minimum Cost to Cut a Stick

    Use half-open/sentinel interval over cut positions.

    points = [0] + sorted(cuts) + [n]

    S:
        dp[l][r] = min cost to perform all cuts strictly between
                  points[l] and points[r].

    R:
        choose first cut k:
            cost = segment_length + dp[l][k] + dp[k][r]

    T:
        increasing width between sentinel points.

    B:
        no cut between l and r -> 0.

    O:
        dp[0][m-1]

    Complexity:
        O(m^3), where m = len(cuts) + 2.
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


def burst_balloons(nums: list[int]) -> int:
    """
    LeetCode:
        312. Burst Balloons

    Key reversal:
        Instead of choosing the first balloon to burst, choose the last balloon
        to burst in an interval.

    Add sentinels:
        arr = [1] + nums + [1]

    S:
        dp[l][r] = max coins from bursting balloons strictly between l and r.

    R:
        choose k as the last balloon burst inside (l, r):
            dp[l][k] + arr[l] * arr[k] * arr[r] + dp[k][r]

    T:
        increasing interval width.

    B:
        no balloon between l and r -> 0.

    O:
        dp[0][n+1]

    Trap:
        The interval is open: balloons strictly between l and r.
    """
    arr = [1] + nums + [1]
    n = len(arr)
    dp = [[0] * n for _ in range(n)]

    for width in range(2, n):
        for l in range(0, n - width):
            r = l + width

            dp[l][r] = max(
                dp[l][k] + arr[l] * arr[k] * arr[r] + dp[k][r]
                for k in range(l + 1, r)
            )

    return dp[0][n - 1]


# =============================================================================
# Level 6 — Merge-Stones / Partition Cost DP
# =============================================================================


def merge_stones(stones: list[int], k: int) -> int:
    """
    LeetCode:
        1000. Minimum Cost to Merge Stones

    Problem:
        Merge exactly k consecutive piles into one pile, paying sum of piles.

    Feasibility:
        Each merge reduces pile count by k - 1.
        To reduce n piles to 1:
            (n - 1) % (k - 1) must be 0.

    S:
        dp[l][r] = min cost to reduce stones[l:r] to as few piles as possible
                  under k-merge rules.

    Common optimized recurrence:
        split only at steps of k-1.

        dp[l][r] = min(dp[l][m] + dp[m][r])
        if interval can be merged into one pile, add sum(l:r).

    Half-open intervals make sums cleaner.

    Complexity:
        O(n^3 / k) roughly.
    """
    n = len(stones)

    if (n - 1) % (k - 1) != 0:
        return -1

    ps = prefix_sums(stones)
    dp = [[0] * (n + 1) for _ in range(n + 1)]

    for length in range(k, n + 1):
        for l in range(0, n - length + 1):
            r = l + length
            best = inf

            for m in range(l + 1, r, k - 1):
                best = min(best, dp[l][m] + dp[m][r])

            dp[l][r] = best

            if (length - 1) % (k - 1) == 0:
                dp[l][r] += range_sum(ps, l, r)

    return int(dp[0][n])


# =============================================================================
# Level 7 — Strange Printer / Last-Operation DP
# =============================================================================


def strange_printer(s: str) -> int:
    """
    LeetCode:
        664. Strange Printer

    Compression:
        Consecutive duplicate chars can be collapsed because printing aaa
        costs the same as printing a.

    S:
        dp[l][r] = minimum turns to print s[l:r+1].

    R:
        Print s[l] separately:
            1 + dp[l+1][r]

        If s[l] == s[k], merge printing of s[l] with s[k]:
            dp[l+1][k-1] + dp[k][r]

    T:
        increasing interval length.

    B:
        single char -> 1

    Complexity:
        O(n^3)
    """
    if not s:
        return 0

    compact = []

    for ch in s:
        if not compact or compact[-1] != ch:
            compact.append(ch)

    s = "".join(compact)
    n = len(s)
    dp = [[0] * n for _ in range(n)]

    for l, r, length in inclusive_intervals(n):
        if length == 1:
            dp[l][r] = 1
            continue

        dp[l][r] = 1 + dp[l + 1][r]

        for k in range(l + 1, r + 1):
            if s[l] == s[k]:
                middle = dp[l + 1][k - 1] if l + 1 <= k - 1 else 0
                dp[l][r] = min(dp[l][r], middle + dp[k][r])

    return dp[0][n - 1]


# =============================================================================
# Level 8 — Remove Boxes / Expanded Interval State
# =============================================================================


def remove_boxes(boxes: list[int]) -> int:
    """
    LeetCode:
        546. Remove Boxes

    This is an advanced interval DP where [l, r] is not enough.

    Why [l, r] is insufficient:
        The value of removing boxes[l] depends on how many same-colored boxes
        have been carried from the left and can be merged with boxes[l].

    State:
        dp(l, r, carry) = max score from boxes[l:r+1], assuming there are
                          carry boxes equal to boxes[l] attached to the left.

    Recurrence:
        1. Remove boxes[l] plus carry now.
        2. If boxes[m] == boxes[l], remove middle first, then merge l with m.

    T:
        Top-down memo is simpler than bottom-up for this expanded interval state.
    """

    @cache
    def dp(l: int, r: int, carry: int) -> int:
        if l > r:
            return 0

        while l + 1 <= r and boxes[l + 1] == boxes[l]:
            l += 1
            carry += 1

        best = (carry + 1) ** 2 + dp(l + 1, r, 0)

        for m in range(l + 1, r + 1):
            if boxes[m] == boxes[l]:
                best = max(
                    best,
                    dp(l + 1, m - 1, 0) + dp(m, r, carry + 1),
                )

        return best

    return dp(0, len(boxes) - 1, 0)


# =============================================================================
# Level 9 — Minimum Cost Tree From Leaf Values
# =============================================================================


def minimum_cost_tree_from_leaf_values_interval(arr: list[int]) -> int:
    """
    LeetCode:
        1130. Minimum Cost Tree From Leaf Values

    Interval DP version.

    S:
        dp[l][r] = min cost to build tree from arr[l:r+1].
        mx[l][r] = max leaf value in arr[l:r+1].

    R:
        choose split k:
            dp[l][k] + dp[k+1][r] + mx[l][k] * mx[k+1][r]

    Note:
        This problem has a better monotonic-stack solution, but interval DP
        is the natural structural version.
    """
    n = len(arr)
    dp = [[0] * n for _ in range(n)]
    mx = [[0] * n for _ in range(n)]

    for i, x in enumerate(arr):
        mx[i][i] = x

    for l, r, length in inclusive_intervals(n):
        if length == 1:
            continue

        mx[l][r] = max(mx[l][r - 1], arr[r])
        dp[l][r] = min(
            dp[l][k] + dp[k + 1][r] + mx[l][k] * mx[k + 1][r]
            for k in range(l, r)
        )

    return dp[0][n - 1]


# =============================================================================
# Part 7 Problem Map
# =============================================================================


PART_7_PROBLEM_MAP = {
    "palindromic_subsequence_interval_dp": [
        516,
        1312,
    ],
    "palindromic_substring_interval_dp": [
        5,
        647,
    ],
    "palindrome_partition_dp": [
        132,
        1278,
    ],
    "boundary_choice_game_dp": [
        486,
        877,
        1690,
    ],
    "split_point_interval_dp": [
        312,
        1039,
        1547,
        1000,
        1130,
    ],
    "last_operation_interval_dp": [
        312,
        664,
        546,
    ],
    "expanded_interval_state": [
        546,
    ],
}


INTERVAL_DP_DIAGNOSTIC_CHECKLIST = [
    "Is the natural state dp[l][r] over an interval?",
    "Are l and r inclusive or is the interval half-open [l, r)?",
    "Does the recurrence choose a boundary or a split point?",
    "Does the problem become easier by choosing the last operation instead of the first?",
    "What are the empty and singleton interval base cases?",
    "Does the fill order use increasing interval length?",
    "Is transition O(1) or O(n) over split points?",
    "Do interval sums need prefix sums?",
    "Is dp[l][r] sufficient, or is extra state needed like carry/group count?",
    "Is there a non-DP optimized solution, such as monotonic stack?",
]


if __name__ == "__main__":
    assert longest_palindromic_subsequence("bbbab") == 4
    assert min_insertions_to_palindrome("mbadm") == 2
    assert min_insertions_to_palindrome_direct("mbadm") == 2

    assert palindromic_substrings_count("aaa") == 6
    assert longest_palindromic_substring("babad") in {"bab", "aba"}

    assert min_cut_palindrome_partition("aab") == 1
    assert palindrome_partition_k_changes("abc", 2) == 1

    assert predict_the_winner([1, 5, 2]) is False
    assert stone_game([5, 3, 4, 5]) is True
    assert stone_game_vii([5, 3, 1, 4, 2]) == 6

    assert min_score_triangulation([1, 3, 1, 4, 1, 5]) == 13
    assert min_cost_cut_stick(7, [1, 3, 4, 5]) == 16
    assert burst_balloons([3, 1, 5, 8]) == 167

    assert merge_stones([3, 2, 4, 1], 2) == 20
    assert merge_stones([3, 2, 4, 1], 3) == -1

    assert strange_printer("aaabbb") == 2
    assert strange_printer("aba") == 2

    assert remove_boxes([1, 3, 2, 2, 2, 3, 4, 3, 1]) == 23
    assert minimum_cost_tree_from_leaf_values_interval([6, 2, 4]) == 32
