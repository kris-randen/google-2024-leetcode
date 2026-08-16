"""
Part 10 — LIS / Sequence Optimization Dynamic Programming

Scope:
    300. Longest Increasing Subsequence
    673. Number of Longest Increasing Subsequence
    354. Russian Doll Envelopes
    368. Largest Divisible Subset
    646. Maximum Length of Pair Chain
    873. Length of Longest Fibonacci Subsequence
    1027. Longest Arithmetic Subsequence
    1048. Longest String Chain
    1218. Longest Arithmetic Subsequence of Given Difference
    1626. Best Team With No Conflicts
    1671. Minimum Number of Removals to Make Mountain Array

Core mental model:
    Sequence optimization DP usually uses:

        dp[i] = best valid structure ending exactly at i

    This differs from prefix DP:

        prefix dp[i] = best answer over nums[:i]

    Ending-at-i DP often has answer:

        max(dp)

    not dp[-1].

Main recurrence:
    dp[i] = 1 + max(dp[j]) over previous compatible j < i

Optimization paths:
    1. O(n^2) previous-choice DP
    2. O(n log n) patience sorting frontier for LIS length
    3. Hash-map DP when compatibility is value-derived
    4. Sorting / ordering reduction before applying LIS-style DP
    5. Counting variant with (length, count)







# Part 10 — LIS / Sequence Optimization

Python file:

[Download Part 10 — LIS / Sequence Optimization Python file](sandbox:/mnt/data/dp_part10_lis_sequence_optimization.py)

## What Part 10 covers

```text id="7yyhsq"
LIS / Sequence Optimization
    -> 300. Longest Increasing Subsequence
    -> 673. Number of Longest Increasing Subsequence
    -> 354. Russian Doll Envelopes
    -> 368. Largest Divisible Subset
    -> 646. Maximum Length of Pair Chain
    -> 873. Length of Longest Fibonacci Subsequence
    -> 1027. Longest Arithmetic Subsequence
    -> 1048. Longest String Chain
    -> 1218. Longest Arithmetic Subsequence of Given Difference
    -> 1626. Best Team With No Conflicts
    -> 1671. Minimum Removals to Make Mountain Array
```

## Core mental model

This family usually starts with:

```text id="0yc6jy"
dp[i] = best valid structure ending exactly at i
```

That is different from prefix DP:

```text id="f7utkk"
dp[i] = best answer over nums[:i]
```

So the final answer is often:

```text id="1t3pcz"
max(dp)
```

not:

```text id="aacg57"
dp[-1]
```

## Main recurrence

```text id="yiwkog"
dp[i] = 1 + max(
    dp[j]
    for j < i
    if j is compatible with i
)
```

The whole family is about defining “compatible.”

Examples:

```text id="ls5vzf"
LIS:
    nums[j] < nums[i]

Largest Divisible Subset:
    nums[i] % nums[j] == 0

Pair Chain:
    pairs[j][1] < pairs[i][0]

String Chain:
    words[j] is predecessor of words[i]

Arithmetic Subsequence:
    same difference
```

## Optimization ladder

```text id="c126nl"
O(n²) previous-choice DP
-> O(n log n) patience sorting frontier
-> hash-map DP when compatibility is value-derived
-> sort/order reduction before applying LIS
-> weighted/counting variants
```

## Key composition chains

```text id="ivnevb"
ending-at-i state
+ choose previous compatible index
+ max aggregation
-> O(n²) LIS
```

```text id="i82q0t"
minimum possible tail per length
+ binary search replacement
-> O(n log n) LIS length
```

```text id="vj2e4p"
sort width increasing
+ equal width height decreasing
+ LIS over heights
-> Russian Doll Envelopes
```

```text id="byhxs3"
ending-at-i state
+ length/count pair
+ add counts on equal best length
-> Number of LIS
```

```text id="9lj0r6"
value-keyed hash map
+ fixed difference
-> Longest Arithmetic Subsequence of Given Difference
```

```text id="nyxfvx"
sort by length
+ delete one character to find predecessor
+ hash map best[word]
-> Longest String Chain
```

## Most important traps

```text id="2wiy9c"
1. Returning dp[-1] for ending-at-i DP.
2. Treating tails[] as the actual LIS sequence.
3. Forgetting equal-width descending sort in Russian Doll Envelopes.
4. Counting LIS needs both length and count.
5. Arithmetic subsequence needs diff as part of the state.
6. Fixed-difference arithmetic subsequence can collapse to best[value].
7. String Chain is easier by deleting one char from current word than by trying all insertions.
8. Mountain Array needs LIS from left and LIS from right, with a valid peak on both sides.
```

Next natural step: **Part 11 — Bitmask / Digit / Tree / Graph DP**.


"""

from __future__ import annotations

from bisect import bisect_left
from collections import defaultdict


# =============================================================================
# Level 0 — Utility Primitives
# =============================================================================


def strict_increasing(a: int, b: int) -> bool:
    return a < b


def non_decreasing(a: int, b: int) -> bool:
    return a <= b


def previous_choice_dp(n: int, compatible) -> list[int]:
    """
    Generic O(n^2) previous-choice DP.

    S:
        dp[i] = best chain ending exactly at i.

    R:
        dp[i] = 1 + max(dp[j] for j < i and compatible(j, i))

    T:
        increasing i.

    B:
        dp[i] = 1 for singleton chain.

    O:
        max(dp)

    The caller supplies compatible(j, i).
    """
    dp = [1] * n

    for i in range(n):
        for j in range(i):
            if compatible(j, i):
                dp[i] = max(dp[i], dp[j] + 1)

    return dp


def reconstruct_chain(parent: list[int], end: int) -> list[int]:
    """
    Reconstruct index chain from parent pointers.
    """
    chain = []

    while end != -1:
        chain.append(end)
        end = parent[end]

    chain.reverse()
    return chain


# =============================================================================
# Level 1 — LIS O(n^2)
# =============================================================================


def lis_length_quadratic(nums: list[int]) -> int:
    """
    LeetCode:
        300. Longest Increasing Subsequence

    S:
        dp[i] = LIS length ending exactly at i.

    R:
        dp[i] = 1 + max(dp[j] for j < i and nums[j] < nums[i])

    T:
        increasing i.

    B:
        dp[i] = 1

    O:
        max(dp), not dp[-1].

    Complexity:
        O(n^2)
    """
    if not nums:
        return 0

    dp = previous_choice_dp(
        len(nums),
        lambda j, i: nums[j] < nums[i],
    )

    return max(dp)


def lis_sequence_quadratic(nums: list[int]) -> list[int]:
    """
    Reconstruct one LIS using parent pointers.

    This is useful for understanding the structure, even though LeetCode 300
    only asks for length.
    """
    if not nums:
        return []

    n = len(nums)
    dp = [1] * n
    parent = [-1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j

    end = max(range(n), key=lambda i: dp[i])
    return [nums[i] for i in reconstruct_chain(parent, end)]


# =============================================================================
# Level 2 — LIS O(n log n) Patience Sorting Frontier
# =============================================================================


def lis_length(nums: list[int]) -> int:
    """
    O(n log n) LIS length.

    State representation:
        tails[k] = minimum possible tail value of an increasing subsequence
                  of length k + 1.

    Important:
        tails is not itself necessarily a valid subsequence.
        It is a frontier of best possible tail values.

    For strict LIS:
        use bisect_left.
    """
    tails: list[int] = []

    for x in nums:
        i = bisect_left(tails, x)

        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x

    return len(tails)


def lis_sequence(nums: list[int]) -> list[int]:
    """
    Reconstruct one LIS in O(n log n).

    Additional arrays:
        tails_idx[length] = index of best tail for subsequence length+1.
        parent[i] = previous index before i in reconstructed subsequence.
    """
    if not nums:
        return []

    tails: list[int] = []
    tails_idx: list[int] = []
    parent = [-1] * len(nums)

    for i, x in enumerate(nums):
        pos = bisect_left(tails, x)

        if pos > 0:
            parent[i] = tails_idx[pos - 1]

        if pos == len(tails):
            tails.append(x)
            tails_idx.append(i)
        else:
            tails[pos] = x
            tails_idx[pos] = i

    return [nums[i] for i in reconstruct_chain(parent, tails_idx[-1])]


# =============================================================================
# Level 3 — Counting LIS
# =============================================================================


def find_number_of_lis(nums: list[int]) -> int:
    """
    LeetCode:
        673. Number of Longest Increasing Subsequence

    S:
        length[i] = LIS length ending at i.
        count[i]  = number of LIS of length[i] ending at i.

    R:
        For each compatible previous j:
            candidate = length[j] + 1

            if candidate > length[i]:
                length[i] = candidate
                count[i] = count[j]

            if candidate == length[i]:
                count[i] += count[j]

    O:
        sum count[i] for length[i] == max_len
    """
    if not nums:
        return 0

    n = len(nums)
    length = [1] * n
    count = [1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] >= nums[i]:
                continue

            candidate = length[j] + 1

            if candidate > length[i]:
                length[i] = candidate
                count[i] = count[j]
            elif candidate == length[i]:
                count[i] += count[j]

    best = max(length)
    return sum(c for l, c in zip(length, count) if l == best)


# =============================================================================
# Level 4 — Sorting Reductions to LIS
# =============================================================================


def max_envelopes(envelopes: list[list[int]]) -> int:
    """
    LeetCode:
        354. Russian Doll Envelopes

    Reduction:
        Sort by width increasing.
        For equal width, sort height decreasing.
        Then run strict LIS on heights.

    Why height descending for equal width?
        Equal-width envelopes cannot nest.
        Descending height prevents equal-width envelopes from being chained
        by the height LIS.
    """
    envelopes.sort(key=lambda e: (e[0], -e[1]))
    heights = [h for _, h in envelopes]
    return lis_length(heights)


def find_longest_chain(pairs: list[list[int]]) -> int:
    """
    LeetCode:
        646. Maximum Length of Pair Chain

    DP version:
        Sort pairs by first value.
        dp[i] = longest chain ending at pair i.

    Note:
        This problem also has a greedy earliest-end solution.
    """
    pairs.sort()
    n = len(pairs)

    if n == 0:
        return 0

    dp = previous_choice_dp(
        n,
        lambda j, i: pairs[j][1] < pairs[i][0],
    )

    return max(dp)


def best_team_score(scores: list[int], ages: list[int]) -> int:
    """
    LeetCode:
        1626. Best Team With No Conflicts

    Reduction:
        Sort players by age, then score.
        Choose a subsequence with non-decreasing scores.

    S:
        dp[i] = best team score ending with player i.

    R:
        if scores[j] <= scores[i]:
            dp[i] = max(dp[i], dp[j] + scores[i])

    This is weighted LIS.
    """
    players = sorted(zip(ages, scores))
    n = len(players)
    dp = [0] * n

    for i, (_, score_i) in enumerate(players):
        dp[i] = score_i

        for j in range(i):
            _, score_j = players[j]

            if score_j <= score_i:
                dp[i] = max(dp[i], dp[j] + score_i)

    return max(dp) if dp else 0


# =============================================================================
# Level 5 — Divisibility / Chain DP
# =============================================================================


def largest_divisible_subset(nums: list[int]) -> list[int]:
    """
    LeetCode:
        368. Largest Divisible Subset

    Reduction:
        Sort nums.
        Build longest chain where nums[i] % nums[j] == 0.
    """
    if not nums:
        return []

    nums.sort()
    n = len(nums)
    dp = [1] * n
    parent = [-1] * n

    for i in range(n):
        for j in range(i):
            if nums[i] % nums[j] == 0 and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j

    end = max(range(n), key=lambda i: dp[i])
    return [nums[i] for i in reconstruct_chain(parent, end)]


# =============================================================================
# Level 6 — Arithmetic / Fibonacci-like Subsequences
# =============================================================================


def longest_arith_seq_length(nums: list[int]) -> int:
    """
    LeetCode:
        1027. Longest Arithmetic Subsequence

    S:
        dp[i][diff] = length of arithmetic subsequence ending at i
                      with common difference diff.

    R:
        dp[i][diff] = dp[j][diff] + 1

    B:
        A pair has length 2.
    """
    n = len(nums)

    if n <= 2:
        return n

    dp: list[dict[int, int]] = [defaultdict(lambda: 1) for _ in nums]
    best = 2

    for i in range(n):
        for j in range(i):
            diff = nums[i] - nums[j]
            dp[i][diff] = max(dp[i][diff], dp[j][diff] + 1)
            best = max(best, dp[i][diff])

    return best


def longest_subsequence_given_difference(arr: list[int], difference: int) -> int:
    """
    LeetCode:
        1218. Longest Arithmetic Subsequence of Given Difference

    Optimization:
        Since diff is fixed, state can be keyed by value.

    S:
        best[x] = longest valid subsequence ending with value x.

    R:
        best[x] = best[x - difference] + 1
    """
    best: dict[int, int] = defaultdict(int)
    ans = 0

    for x in arr:
        best[x] = best[x - difference] + 1
        ans = max(ans, best[x])

    return ans


def len_longest_fib_subseq(arr: list[int]) -> int:
    """
    LeetCode:
        873. Length of Longest Fibonacci Subsequence

    S:
        dp[j][i] = length of fib-like subsequence ending with arr[j], arr[i].

    R:
        Need arr[k] + arr[j] = arr[i], so arr[k] = arr[i] - arr[j].
        If k < j:
            dp[j][i] = dp[k][j] + 1

    O:
        max dp[j][i], but return 0 if best < 3.
    """
    n = len(arr)
    pos = {x: i for i, x in enumerate(arr)}
    dp = [[2] * n for _ in range(n)]
    best = 0

    for i in range(n):
        for j in range(i):
            prev = arr[i] - arr[j]
            k = pos.get(prev)

            if k is not None and k < j:
                dp[j][i] = dp[k][j] + 1
                best = max(best, dp[j][i])

    return best if best >= 3 else 0


# =============================================================================
# Level 7 — String Chain DP
# =============================================================================


def is_predecessor(shorter: str, longer: str) -> bool:
    """
    True if longer can be formed by inserting exactly one char into shorter.
    """
    if len(longer) != len(shorter) + 1:
        return False

    i = 0
    j = 0
    skipped = False

    while i < len(shorter) and j < len(longer):
        if shorter[i] == longer[j]:
            i += 1
            j += 1
        elif not skipped:
            skipped = True
            j += 1
        else:
            return False

    return True


def longest_str_chain_quadratic(words: list[str]) -> int:
    """
    LeetCode:
        1048. Longest String Chain

    O(n^2 * L) previous-choice version.

    S:
        dp[i] = longest chain ending at words[i].

    Order:
        sort by word length.
    """
    words.sort(key=len)
    n = len(words)

    if n == 0:
        return 0

    dp = [1] * n

    for i in range(n):
        for j in range(i):
            if is_predecessor(words[j], words[i]):
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def longest_str_chain(words: list[str]) -> int:
    """
    Optimized hash-map version.

    S:
        best[word] = longest chain ending at word.

    R:
        Remove one char from word to form predecessor.
        best[word] = 1 + max(best[pred])
    """
    words.sort(key=len)
    best: dict[str, int] = {}
    ans = 0

    for word in words:
        curr = 1

        for i in range(len(word)):
            pred = word[:i] + word[i + 1:]
            curr = max(curr, best.get(pred, 0) + 1)

        best[word] = curr
        ans = max(ans, curr)

    return ans


# =============================================================================
# Level 8 — Mountain Sequence DP
# =============================================================================


def minimum_mountain_removals(nums: list[int]) -> int:
    """
    LeetCode:
        1671. Minimum Number of Removals to Make Mountain Array

    Need a subsequence that strictly increases then strictly decreases.

    S:
        left[i] = LIS length ending at i.
        right[i] = LDS length starting at i.

    Peak condition:
        left[i] > 1 and right[i] > 1

    Answer:
        n - max(left[i] + right[i] - 1)
    """
    n = len(nums)
    left = [1] * n
    right = [1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                left[i] = max(left[i], left[j] + 1)

    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            if nums[j] < nums[i]:
                right[i] = max(right[i], right[j] + 1)

    best = 0

    for i in range(n):
        if left[i] > 1 and right[i] > 1:
            best = max(best, left[i] + right[i] - 1)

    return n - best


def lis_lengths_ending_at_each_index(nums: list[int]) -> list[int]:
    """
    O(n log n) helper:
        lengths[i] = LIS length ending at i under patience frontier.

    Useful for mountain-array optimization.
    """
    tails: list[int] = []
    lengths = [0] * len(nums)

    for i, x in enumerate(nums):
        pos = bisect_left(tails, x)

        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x

        lengths[i] = pos + 1

    return lengths


def minimum_mountain_removals_fast(nums: list[int]) -> int:
    """
    O(n log n) mountain removals using LIS length at each index.
    """
    n = len(nums)
    left = lis_lengths_ending_at_each_index(nums)
    right = list(reversed(lis_lengths_ending_at_each_index(list(reversed(nums)))))

    best = 0

    for i in range(n):
        if left[i] > 1 and right[i] > 1:
            best = max(best, left[i] + right[i] - 1)

    return n - best


# =============================================================================
# Level 9 — Series / Family Maps
# =============================================================================


SEQUENCE_OPTIMIZATION_LADDER = {
    "300_lis": {
        "family": "previous-choice DP -> patience sorting optimization",
        "state": "dp[i] = LIS ending at i",
        "optimized_state": "tails[length] = minimum tail",
    },
    "673_number_of_lis": {
        "family": "counting LIS",
        "state": "(length[i], count[i])",
        "transition": "replace count on better length; add count on equal length",
    },
    "354_russian_doll": {
        "family": "sort reduction to LIS",
        "state": "LIS over heights after width sorting",
        "trap": "equal widths sorted by height descending",
    },
    "368_largest_divisible_subset": {
        "family": "chain DP with divisibility compatibility",
        "state": "dp[i] = best divisible chain ending at i",
    },
    "1027_arithmetic_subsequence": {
        "family": "ending pair / diff-state DP",
        "state": "dp[i][diff]",
    },
    "1218_fixed_difference": {
        "family": "hash-map optimized arithmetic DP",
        "state": "best[value]",
    },
    "873_fibonacci_subsequence": {
        "family": "ending pair DP",
        "state": "dp[j][i] = best ending with arr[j], arr[i]",
    },
    "1048_string_chain": {
        "family": "predecessor deletion hash DP",
        "state": "best[word]",
    },
    "1626_best_team": {
        "family": "weighted LIS after sorting",
        "state": "dp[i] = best team score ending at i",
    },
    "1671_mountain": {
        "family": "LIS from left + LIS from right",
        "state": "left[i], right[i]",
    },
}


PART_10_PROBLEM_MAP = {
    "basic_lis": [
        300,
    ],
    "counting_lis": [
        673,
    ],
    "sort_reduction_to_lis": [
        354,
        1626,
    ],
    "chain_dp": [
        368,
        646,
        1048,
    ],
    "arithmetic_sequence_dp": [
        1027,
        1218,
        873,
    ],
    "mountain_sequence_dp": [
        1671,
    ],
}


SEQUENCE_DP_DIAGNOSTIC_CHECKLIST = [
    "Does dp[i] mean best ending exactly at i or best over prefix nums[:i]?",
    "If dp[i] means ending at i, is the final answer max(dp)?",
    "What makes j compatible with i?",
    "Is the transition choose-previous-index O(n^2)?",
    "Can compatibility be optimized with binary search, sorting, or a hash map?",
    "Does sorting preserve the original problem constraints?",
    "For equal keys, do we need ascending or descending tie-breaks?",
    "Are we counting optimal chains or just finding the length?",
    "Do we need parent pointers to reconstruct the sequence?",
    "Is this actually greedy after sorting, like pair chain, or DP?",
]


if __name__ == "__main__":
    assert lis_length_quadratic([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert lis_length([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert len(lis_sequence_quadratic([10, 9, 2, 5, 3, 7, 101, 18])) == 4
    assert len(lis_sequence([10, 9, 2, 5, 3, 7, 101, 18])) == 4

    assert find_number_of_lis([1, 3, 5, 4, 7]) == 2
    assert max_envelopes([[5, 4], [6, 4], [6, 7], [2, 3]]) == 3
    assert find_longest_chain([[1, 2], [2, 3], [3, 4]]) == 2
    assert best_team_score([1, 3, 5, 10, 15], [1, 2, 3, 4, 5]) == 34

    assert largest_divisible_subset([1, 2, 4, 8]) == [1, 2, 4, 8]
    assert longest_arith_seq_length([3, 6, 9, 12]) == 4
    assert longest_subsequence_given_difference([1, 2, 3, 4], 1) == 4
    assert len_longest_fib_subseq([1, 2, 3, 4, 5, 6, 7, 8]) == 5

    assert is_predecessor("abc", "abac")
    assert not is_predecessor("abc", "abdcx")
    assert longest_str_chain(["a", "b", "ba", "bca", "bda", "bdca"]) == 4
    assert longest_str_chain_quadratic(["a", "b", "ba", "bca", "bda", "bdca"]) == 4

    assert minimum_mountain_removals([2, 1, 1, 5, 6, 2, 3, 1]) == 3
    assert minimum_mountain_removals_fast([2, 1, 1, 5, 6, 2, 3, 1]) == 3
