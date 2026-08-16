"""
Part 5 — Two-Sequence Dynamic Programming Families

Scope:
    Longest Common Subsequence
    Uncrossed Lines
    Edit Distance
    Delete Operation for Two Strings
    Minimum ASCII Delete Sum
    Distinct Subsequences
    Interleaving String
    Shortest Common Supersequence
    Maximum Length of Repeated Subarray
    Minimum Window Subsequence
    Regular Expression Matching
    Wildcard Matching

Core mental model:
    Two-sequence DP usually starts with:

        dp[i][j] = answer for a[:i] and b[:j]

    The two indices represent a Cartesian product of prefix states.

Main distinction:
    Subsequence:
        Can skip characters.
        Usually reads dp[i-1][j], dp[i][j-1], dp[i-1][j-1].

    Substring / repeated subarray:
        Must be contiguous.
        Usually resets to 0 on mismatch.

SRTBOT:
    S — Subproblems
    R — Relationships / match-mismatch transitions
    T — Topological order / row-major table fill
    B — Base cases / empty prefix row and column
    O — Original problem / answer extraction
    T — Time complexity = states × transition cost


# Part 5 — Two-Sequence DP

Python file:

[Download Part 5 — Two-Sequence DP Python file](sandbox:/mnt/data/dp_part5_two_sequence_dp.py)

## What Part 5 covers

```text
Two-sequence DP
    -> LCS
    -> Edit Distance
    -> Delete Operation for Two Strings
    -> Minimum ASCII Delete Sum
    -> Distinct Subsequences
    -> Interleaving String
    -> Shortest Common Supersequence
    -> Maximum Length of Repeated Subarray
    -> Minimum Window Subsequence
    -> Regex / Wildcard Matching
```

## Core primitive

```text
dp[i][j] = answer for a[:i] and b[:j]
```

This is the Cartesian product of two prefix state spaces.

## Main distinction

```text
Subsequence DP:
    characters may be skipped
    mismatch usually reads dp[i-1][j] or dp[i][j-1]

Substring / repeated-subarray DP:
    characters must be contiguous
    mismatch usually resets to 0
```

## Key composition chains

```text
two-prefix state
+ match/mismatch recurrence
+ max aggregation
-> LCS / Uncrossed Lines
```

```text
two-prefix state
+ delete/insert/replace recurrence
+ min aggregation
-> Edit Distance
```

```text
source-prefix × target-prefix state
+ skip/use current source char
+ sum aggregation
-> Distinct Subsequences
```

```text
two-prefix state
+ consume from either string
+ boolean OR
-> Interleaving String
```

```text
two-prefix state
+ contiguous suffix recurrence
+ reset on mismatch
-> Maximum Length of Repeated Subarray
```

## Most important traps

```text
1. dp[i][j] usually refers to prefixes, not characters i and j directly.
2. Current characters are a[i-1], b[j-1].
3. LCS answer is dp[n][m].
4. Longest common substring answer is max(dp), not necessarily dp[n][m].
5. Distinct Subsequences is counting, not max/min.
6. Regex '*' and wildcard '*' mean different things.
7. Rolling 1D DP direction matters.
```

Next natural step: **Part 6 — Knapsack / Capacity DP**.

"""

from __future__ import annotations

from math import inf


# =============================================================================
# Level 0 — Utility Primitives
# =============================================================================


def table(rows: int, cols: int, value=0):
    return [[value for _ in range(cols)] for _ in range(rows)]


def same(a: str, b: str, i: int, j: int) -> bool:
    """
    Compare current characters for prefix-index DP.

    dp index:
        i means prefix a[:i]
        j means prefix b[:j]

    current chars:
        a[i - 1]
        b[j - 1]
    """
    return a[i - 1] == b[j - 1]


# =============================================================================
# Level 1 — LCS / Subsequence Optimization
# =============================================================================


def lcs_length(a: str, b: str) -> int:
    """
    LeetCode:
        1143. Longest Common Subsequence

    S:
        dp[i][j] = LCS length of a[:i] and b[:j].

    R:
        if a[i-1] == b[j-1]:
            dp[i][j] = 1 + dp[i-1][j-1]
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    T:
        row-major increasing i, j.

    B:
        dp[0][j] = 0
        dp[i][0] = 0

    O:
        dp[n][m]

    Complexity:
        O(nm) time, O(nm) space.
    """
    n = len(a)
    m = len(b)
    dp = table(n + 1, m + 1, 0)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if same(a, b, i, j):
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]


def lcs_length_rolling(a: str, b: str) -> int:
    """
    LCS with O(min(n, m)) space.

    Invariant:
        prev[j] = dp[i-1][j]
        curr[j] = dp[i][j]

    Trap:
        dp[i-1][j-1] must be read from prev[j-1], not curr[j-1].
    """
    if len(b) > len(a):
        a, b = b, a

    prev = [0] * (len(b) + 1)

    for i in range(1, len(a) + 1):
        curr = [0] * (len(b) + 1)

        for j in range(1, len(b) + 1):
            if same(a, b, i, j):
                curr[j] = 1 + prev[j - 1]
            else:
                curr[j] = max(prev[j], curr[j - 1])

        prev = curr

    return prev[-1]


def uncrossed_lines(a: list[int], b: list[int]) -> int:
    """
    LeetCode:
        1035. Uncrossed Lines

    Reduction:
        LCS over integer arrays.

    State:
        dp[i][j] = max uncrossed lines using a[:i], b[:j].
    """
    n = len(a)
    m = len(b)
    dp = table(n + 1, m + 1, 0)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]


# =============================================================================
# Level 2 — Edit Distance / Alignment Cost
# =============================================================================


def edit_distance(a: str, b: str) -> int:
    """
    LeetCode:
        72. Edit Distance

    S:
        dp[i][j] = min edits to convert a[:i] into b[:j].

    R:
        delete from a:
            dp[i-1][j] + 1

        insert into a:
            dp[i][j-1] + 1

        replace/match:
            dp[i-1][j-1] + cost

    T:
        row-major.

    B:
        dp[i][0] = i
        dp[0][j] = j

    O:
        dp[n][m]
    """
    n = len(a)
    m = len(b)
    dp = table(n + 1, m + 1, 0)

    for i in range(n + 1):
        dp[i][0] = i

    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if same(a, b, i, j) else 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )

    return dp[n][m]


def delete_operation_distance(a: str, b: str) -> int:
    """
    LeetCode:
        583. Delete Operation for Two Strings

    Version 1:
        Reduce to LCS.

    Need to delete:
        len(a) - lcs + len(b) - lcs

    This teaches that not every two-string DP needs a new recurrence.
    """
    keep = lcs_length(a, b)
    return len(a) + len(b) - 2 * keep


def delete_operation_distance_direct(a: str, b: str) -> int:
    """
    Direct DP for delete-only edit distance.

    S:
        dp[i][j] = min deletions to make a[:i] and b[:j] equal.

    R:
        if chars match:
            dp[i][j] = dp[i-1][j-1]
        else:
            delete from a or delete from b:
            1 + min(dp[i-1][j], dp[i][j-1])
    """
    n = len(a)
    m = len(b)
    dp = table(n + 1, m + 1, 0)

    for i in range(n + 1):
        dp[i][0] = i

    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if same(a, b, i, j):
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]


def minimum_delete_sum(a: str, b: str) -> int:
    """
    LeetCode:
        712. Minimum ASCII Delete Sum for Two Strings

    Same structural skeleton as delete-only edit distance,
    but deletion cost is ASCII value, not 1.

    S:
        dp[i][j] = min ASCII delete cost to make a[:i], b[:j] equal.
    """
    n = len(a)
    m = len(b)
    dp = table(n + 1, m + 1, 0)

    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + ord(a[i - 1])

    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + ord(b[j - 1])

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if same(a, b, i, j):
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    ord(a[i - 1]) + dp[i - 1][j],
                    ord(b[j - 1]) + dp[i][j - 1],
                )

    return dp[n][m]


# =============================================================================
# Level 3 — Counting Subsequences
# =============================================================================


def distinct_subsequences(source: str, target: str) -> int:
    """
    LeetCode:
        115. Distinct Subsequences

    S:
        dp[i][j] = number of ways target[:j] appears as a subsequence
                  in source[:i].

    R:
        Always skip source[i-1]:
            dp[i-1][j]

        If source[i-1] == target[j-1], also use source[i-1]:
            dp[i-1][j-1]

    T:
        row-major.

    B:
        dp[i][0] = 1
            Empty target appears once in any source prefix.

        dp[0][j] = 0 for j > 0.

    O:
        dp[n][m]

    Trap:
        This is counting. Do not use max.
    """
    n = len(source)
    m = len(target)
    dp = table(n + 1, m + 1, 0)

    for i in range(n + 1):
        dp[i][0] = 1

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = dp[i - 1][j]

            if source[i - 1] == target[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]

    return dp[n][m]


def distinct_subsequences_rolling(source: str, target: str) -> int:
    """
    1D rolling version.

    State:
        dp[j] = number of ways to form target[:j] using processed source.

    Critical order:
        j must go backward so source[i-1] is used at most once per row.
    """
    m = len(target)
    dp = [0] * (m + 1)
    dp[0] = 1

    for ch in source:
        for j in range(m, 0, -1):
            if ch == target[j - 1]:
                dp[j] += dp[j - 1]

    return dp[m]


# =============================================================================
# Level 4 — Interleaving / Consume From Either Sequence
# =============================================================================


def is_interleave(a: str, b: str, s: str) -> bool:
    """
    LeetCode:
        97. Interleaving String

    S:
        dp[i][j] = whether s[:i+j] can be formed by interleaving
                  a[:i] and b[:j].

    R:
        Take next char from a:
            dp[i-1][j] and a[i-1] == s[i+j-1]

        Take next char from b:
            dp[i][j-1] and b[j-1] == s[i+j-1]

    T:
        row-major.

    B:
        dp[0][0] = True

    O:
        dp[n][m]
    """
    n = len(a)
    m = len(b)

    if n + m != len(s):
        return False

    dp = table(n + 1, m + 1, False)
    dp[0][0] = True

    for i in range(n + 1):
        for j in range(m + 1):
            if i > 0 and dp[i - 1][j] and a[i - 1] == s[i + j - 1]:
                dp[i][j] = True

            if j > 0 and dp[i][j - 1] and b[j - 1] == s[i + j - 1]:
                dp[i][j] = True

    return dp[n][m]


# =============================================================================
# Level 5 — Shortest Common Supersequence
# =============================================================================


def shortest_common_supersequence(a: str, b: str) -> str:
    """
    LeetCode:
        1092. Shortest Common Supersequence

    Conceptual reduction:
        Build around the LCS.

    This version computes an LCS table, then reconstructs the SCS.

    S:
        dp[i][j] = LCS length of a[:i], b[:j].

    Reconstruction:
        Walk backward from (n, m).
        If chars match, include once.
        Otherwise include char from direction with larger LCS value.

    Trap:
        The DP table stores LCS length, but the output is a string.
    """
    n = len(a)
    m = len(b)
    dp = table(n + 1, m + 1, 0)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if same(a, b, i, j):
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    i = n
    j = m
    out: list[str] = []

    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            out.append(a[i - 1])
            i -= 1
        else:
            out.append(b[j - 1])
            j -= 1

    while i > 0:
        out.append(a[i - 1])
        i -= 1

    while j > 0:
        out.append(b[j - 1])
        j -= 1

    return "".join(reversed(out))


# =============================================================================
# Level 6 — Substring / Contiguous Match DP
# =============================================================================


def find_length_repeated_subarray(a: list[int], b: list[int]) -> int:
    """
    LeetCode:
        718. Maximum Length of Repeated Subarray

    This is NOT LCS.

    S:
        dp[i][j] = length of longest common suffix of a[:i], b[:j].
        Equivalently, length of repeated subarray ending at a[i-1], b[j-1].

    R:
        if a[i-1] == b[j-1]:
            dp[i][j] = 1 + dp[i-1][j-1]
        else:
            dp[i][j] = 0

    O:
        max over all dp[i][j], not dp[n][m].

    Trap:
        Contiguity forces reset to 0 on mismatch.
    """
    n = len(a)
    m = len(b)
    dp = table(n + 1, m + 1, 0)
    best = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
                best = max(best, dp[i][j])

    return best


def longest_common_substring_length(a: str, b: str) -> int:
    """
    Same contiguous-match primitive as Maximum Length of Repeated Subarray,
    but for strings.
    """
    n = len(a)
    m = len(b)
    prev = [0] * (m + 1)
    best = 0

    for i in range(1, n + 1):
        curr = [0] * (m + 1)

        for j in range(1, m + 1):
            if same(a, b, i, j):
                curr[j] = 1 + prev[j - 1]
                best = max(best, curr[j])

        prev = curr

    return best


# =============================================================================
# Level 7 — Minimum Window Subsequence
# =============================================================================


def min_window_subsequence(s: str, t: str) -> str:
    """
    LeetCode:
        727. Minimum Window Subsequence

    One DP interpretation:

    State:
        dp[j] = start index in s of a window ending at current s index
                that matches t[:j+1] as a subsequence.

    Iterate over s left-to-right.
    Update j backward so each s[i] is used once.

    If t[-1] is matched, dp[m-1] gives the start of a candidate window.

    Trap:
        This is subsequence inside a substring window.
    """
    m = len(t)
    starts = [-1] * m
    best_start = -1
    best_len = inf

    for i, ch in enumerate(s):
        for j in range(m - 1, -1, -1):
            if ch != t[j]:
                continue

            if j == 0:
                starts[j] = i
            elif starts[j - 1] != -1:
                starts[j] = starts[j - 1]

        if starts[-1] != -1:
            length = i - starts[-1] + 1

            if length < best_len:
                best_len = length
                best_start = starts[-1]

    return "" if best_start == -1 else s[best_start:best_start + best_len]


# =============================================================================
# Level 8 — Pattern Matching DP
# =============================================================================


def is_match_regex(s: str, p: str) -> bool:
    """
    LeetCode:
        10. Regular Expression Matching

    Pattern symbols:
        . matches any single character
        * means zero or more of the previous pattern element

    S:
        dp[i][j] = whether s[:i] matches p[:j].

    R:
        If p[j-1] is normal or '.':
            match current char and dp[i-1][j-1]

        If p[j-1] is '*':
            zero copies:
                dp[i][j-2]

            one or more copies if previous pattern char matches s[i-1]:
                dp[i-1][j]

    B:
        dp[0][0] = True
        Empty string can match patterns like a*, a*b*, etc.

    Trap:
        '*' refers to previous pattern character.
    """
    n = len(s)
    m = len(p)
    dp = table(n + 1, m + 1, False)
    dp[0][0] = True

    for j in range(2, m + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]

    def char_matches(i: int, j: int) -> bool:
        return p[j - 1] == "." or s[i - 1] == p[j - 1]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j - 1] == "*":
                dp[i][j] = dp[i][j - 2]

                if char_matches(i, j - 1):
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif char_matches(i, j):
                dp[i][j] = dp[i - 1][j - 1]

    return dp[n][m]


def is_match_wildcard(s: str, p: str) -> bool:
    """
    LeetCode:
        44. Wildcard Matching

    Pattern symbols:
        ? matches any single character
        * matches any sequence, including empty

    S:
        dp[i][j] = whether s[:i] matches p[:j].

    R:
        If p[j-1] is normal or '?':
            dp[i][j] = dp[i-1][j-1]

        If p[j-1] is '*':
            dp[i][j] = dp[i][j-1] or dp[i-1][j]
            zero chars       one more char consumed by *

    Trap:
        Wildcard '*' is not regex '*'.
        It does not refer to previous character.
    """
    n = len(s)
    m = len(p)
    dp = table(n + 1, m + 1, False)
    dp[0][0] = True

    for j in range(1, m + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 1]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j - 1] == "*":
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif p[j - 1] == "?" or s[i - 1] == p[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]

    return dp[n][m]


# =============================================================================
# Part 5 Problem Map
# =============================================================================


PART_5_PROBLEM_MAP = {
    "lcs_subsequence_optimization": [
        1143,
        1035,
        583,
        1092,
    ],
    "edit_distance_alignment_cost": [
        72,
        583,
        712,
    ],
    "counting_subsequences": [
        115,
        940,
    ],
    "consume_from_either_sequence": [
        97,
    ],
    "substring_contiguous_match": [
        718,
        1062,
    ],
    "minimum_window_subsequence": [
        727,
    ],
    "pattern_matching_dp": [
        10,
        44,
    ],
}


TWO_SEQUENCE_DP_DIAGNOSTIC_CHECKLIST = [
    "Does dp[i][j] mean prefixes a[:i], b[:j]?",
    "Is this subsequence or substring?",
    "Can characters be skipped from one or both sequences?",
    "Is the aggregation max, min, sum, or boolean OR?",
    "What does the empty row/column mean?",
    "Is the final answer dp[n][m] or max over all states?",
    "Does mismatch reset to 0? If yes, this is contiguous substring-style DP.",
    "Can space be rolled by rows?",
    "If rolling 1D, must j go forward or backward?",
    "Are pattern symbols like '*' regex-style or wildcard-style?",
]


if __name__ == "__main__":
    assert lcs_length("abcde", "ace") == 3
    assert lcs_length_rolling("abcde", "ace") == 3
    assert uncrossed_lines([1, 4, 2], [1, 2, 4]) == 2

    assert edit_distance("horse", "ros") == 3
    assert delete_operation_distance("sea", "eat") == 2
    assert delete_operation_distance_direct("sea", "eat") == 2
    assert minimum_delete_sum("sea", "eat") == 231

    assert distinct_subsequences("rabbbit", "rabbit") == 3
    assert distinct_subsequences_rolling("rabbbit", "rabbit") == 3

    assert is_interleave("aabcc", "dbbca", "aadbbcbcac")
    assert not is_interleave("aabcc", "dbbca", "aadbbbaccc")

    assert shortest_common_supersequence("abac", "cab") in {"cabac"}
    assert find_length_repeated_subarray([1, 2, 3, 2, 1], [3, 2, 1, 4, 7]) == 3
    assert longest_common_substring_length("abcdef", "zabcf") == 3
    assert min_window_subsequence("abcdebdde", "bde") == "bcde"

    assert is_match_regex("aab", "c*a*b")
    assert not is_match_regex("mississippi", "mis*is*p*.")
    assert is_match_wildcard("adceb", "*a*b")
    assert not is_match_wildcard("acdcb", "a*c?b")
