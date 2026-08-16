"""
Part 9 — Stone Game Series

Scope:
    877. Stone Game
    1140. Stone Game II
    1406. Stone Game III
    1510. Stone Game IV
    1563. Stone Game V
    1686. Stone Game VI
    1690. Stone Game VII
    1872. Stone Game VIII
    2029. Stone Game IX

Core mental model:
    "Stone Game" is not one pattern.

    The series splits into several different families:

        1. Interval score-difference DP
            Stone Game I
            Stone Game VII
            Predict the Winner

        2. Suffix take-k game DP
            Stone Game II
            Stone Game III
            Stone Game VIII

        3. Win/lose impartial game DP
            Stone Game IV

        4. Split-point interval DP
            Stone Game V

        5. Greedy/game-theory exceptions
            Stone Game VI
            Stone Game IX

Most reusable game-DP primitive:
    dp[state] = maximum score difference current player can force
                from this state.

Why score difference is powerful:
    It absorbs the opponent's optimal play by subtraction.

        choose move:
            gain_from_move - dp[next_state]

SRTBOT:
    S — game state
    R — legal moves from state
    T — smaller interval / later suffix / smaller pile count
    B — terminal positions
    O — initial state
    T — states × legal moves








# Part 9 — Stone Game Series

Python file:

[Download Part 9 — Stone Game Series Python file](sandbox:/mnt/data/dp_part9_stone_game_series.py)

## What Part 9 covers

```text id="9xvpm5"
Stone Game Series
    -> 877. Stone Game
    -> 1140. Stone Game II
    -> 1406. Stone Game III
    -> 1510. Stone Game IV
    -> 1563. Stone Game V
    -> 1686. Stone Game VI
    -> 1690. Stone Game VII
    -> 1872. Stone Game VIII
    -> 2029. Stone Game IX
```

## Core mental model

“Stone Game” is not one DP pattern.

It splits into:

```text id="ipyqov"
1. Interval score-difference DP
2. Suffix take-k game DP
3. Win/lose impartial game DP
4. Split-point interval DP
5. Greedy/game-theory exceptions
```

The most reusable primitive is:

```text id="tzi31j"
dp[state] = maximum score difference current player can force from this state
```

Why score difference works:

```text id="xihh60"
current player chooses a move

candidate =
    immediate_gain - opponent_best_difference_from_next_state
```

So the opponent’s optimal play is absorbed by subtraction.

---

## Series map

### Stone Game I — 877

Family:

```text id="8xyw3z"
interval score-difference DP
```

State:

```text id="dp9dd7"
dp[l][r] = max score difference current player can force from piles[l:r+1]
```

Transition:

```text id="a6wegg"
max(
    piles[l] - dp[l+1][r],
    piles[r] - dp[l][r-1]
)
```

LeetCode 877 also has a parity-strategy shortcut where Alice always wins under the original constraints, but the interval DP is the reusable primitive.

---

### Stone Game II — 1140

Family:

```text id="7g2jhu"
suffix DP with expanding M
```

State:

```text id="3spo6k"
dfs(i, M) = max stones current player can collect from piles[i:] with current M
```

Transition:

```text id="iwm7lk"
take X piles, where 1 <= X <= 2M

candidate =
    suffix[i] - dfs(i + X, max(M, X))
```

---

### Stone Game III — 1406

Family:

```text id="3zvsf3"
suffix take-k score-difference DP
```

State:

```text id="sww7fw"
dp[i] = max score difference current player can force from stoneValue[i:]
```

Transition:

```text id="2fxkkn"
take 1, 2, or 3 stones

candidate =
    gain - dp[i + x]
```

Answer:

```text id="10pwok"
dp[0] > 0  -> Alice
dp[0] < 0  -> Bob
dp[0] == 0 -> Tie
```

---

### Stone Game IV — 1510

Family:

```text id="615t06"
win/lose impartial game DP
```

State:

```text id="4xacbv"
win[n] = whether current player wins with n stones
```

Transition:

```text id="qg4fj8"
win[n] = any(not win[n - square])
```

This is not score maximization. It is boolean game DP.

---

### Stone Game V — 1563

Family:

```text id="tx8tbh"
split-point interval DP
```

State:

```text id="l2p7nk"
dp[l][r] = max score Alice can obtain from stoneValue[l:r+1]
```

Transition:

```text id="sk29zb"
choose split k

left_sum = sum(l..k)
right_sum = sum(k+1..r)

if left_sum < right_sum:
    score = left_sum + dp[l][k]

if left_sum > right_sum:
    score = right_sum + dp[k+1][r]

if equal:
    score = left_sum + max(dp[l][k], dp[k+1][r])
```

This is interval DP, but not the simple left/right boundary game.

---

### Stone Game VI — 1686

Family:

```text id="b57j1i"
greedy total-swing sorting
```

Key insight:

```text id="q199mh"
If Alice takes stone i:
    Alice gains alice[i]
    Bob is denied bob[i]

Total swing:
    alice[i] + bob[i]
```

So sort by:

```text id="srj0ia"
alice[i] + bob[i]
```

descending, then alternate picks.

This is a major exception: it is not DP.

---

### Stone Game VII — 1690

Family:

```text id="o4n4t1"
interval score-difference DP with prefix sums
```

State:

```text id="4sud23"
dp[l][r] = max score difference current player can force from stones[l:r+1]
```

Transition:

```text id="q7fhyk"
remove left:
    sum(l+1..r) - dp[l+1][r]

remove right:
    sum(l..r-1) - dp[l][r-1]
```

Prefix sums make remaining-sum queries O(1).

---

### Stone Game VIII — 1872

Family:

```text id="i8lm52"
suffix score-difference DP over prefix sums
```

Core optimized recurrence:

```text id="kk5fdo"
best = prefix[n-1]

for i from n-2 down to 1:
    best = max(best, prefix[i] - best)
```

This is one of those cases where the final code looks cryptic unless the score-difference DP is understood first.

---

### Stone Game IX — 2029

Family:

```text id="imk4sr"
modulo-count game theory
```

Only residues modulo 3 matter.

Criterion:

```text id="omagsu"
c0, c1, c2 = counts of stones mod 3

if c0 is even:
    Alice wins iff c1 > 0 and c2 > 0

if c0 is odd:
    Alice wins iff abs(c1 - c2) > 2
```

This is not table DP.

---

## Composition chains

```text id="xgu5nt"
interval state dp[l][r]
+ choose left/right
+ score-difference invariant
-> Stone Game I / Predict the Winner
```

```text id="hlrju4"
suffix state dp[i]
+ take 1..k stones
+ gain - dp[next]
-> Stone Game III
```

```text id="tdg5yl"
state dfs(i, M)
+ suffix sums
+ take X in 1..2M
-> Stone Game II
```

```text id="t21k65"
interval state dp[l][r]
+ prefix sums
+ choose split k
-> Stone Game V
```

```text id="n84lni"
value-to-Alice + value-to-Bob
+ total swing sorting
-> Stone Game VI
```

## Most important traps

```text id="eoe6p7"
1. Treating all Stone Games as interval DP.
2. Treating all Stone Games as minimax recursion without score-difference compression.
3. Forgetting that Stone Game VI is greedy.
4. Forgetting that Stone Game IX is residue game theory.
5. Confusing Alice's absolute score with score difference.
6. Missing prefix/suffix sums for O(1) interval or suffix gains.
7. In Stone Game II, forgetting that M changes to max(M, X).
8. In Stone Game V, using boundary choice instead of split point.
```

Next natural step: **Part 10 — LIS / Sequence Optimization**.


"""

from __future__ import annotations

from functools import cache
from math import isqrt


# =============================================================================
# Level 0 — Utilities
# =============================================================================


def prefix_sums(nums: list[int]) -> list[int]:
    ps = [0]

    for x in nums:
        ps.append(ps[-1] + x)

    return ps


def range_sum(ps: list[int], l: int, r: int) -> int:
    """
    Half-open interval sum:
        sum(nums[l:r])
    """
    return ps[r] - ps[l]


def suffix_sums(nums: list[int]) -> list[int]:
    """
    suffix[i] = sum(nums[i:])
    suffix[n] = 0
    """
    n = len(nums)
    suffix = [0] * (n + 1)

    for i in range(n - 1, -1, -1):
        suffix[i] = nums[i] + suffix[i + 1]

    return suffix


def inclusive_intervals(n: int):
    for length in range(1, n + 1):
        for l in range(0, n - length + 1):
            r = l + length - 1
            yield l, r, length


# =============================================================================
# Level 1 — Core Game DP Primitives
# =============================================================================


def interval_score_difference(nums: list[int]) -> int:
    """
    Generic boundary-choice interval game.

    S:
        dp[l][r] = maximum score difference current player can force
                  over opponent from nums[l:r+1].

    R:
        take left:
            nums[l] - dp[l+1][r]

        take right:
            nums[r] - dp[l][r-1]

    T:
        increasing interval length.

    B:
        dp[i][i] = nums[i]

    O:
        dp[0][n-1]

    Complexity:
        O(n^2)
    """
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for l, r, length in inclusive_intervals(n):
        if length == 1:
            dp[l][r] = nums[l]
        else:
            dp[l][r] = max(
                nums[l] - dp[l + 1][r],
                nums[r] - dp[l][r - 1],
            )

    return dp[0][n - 1]


def suffix_take_k_score_difference(values: list[int], max_take: int) -> int:
    """
    Generic suffix game where current player may take 1..max_take items.

    S:
        dp[i] = maximum score difference current player can force
                from values[i:].

    R:
        take x items:
            gain = sum(values[i:i+x])
            candidate = gain - dp[i+x]

    T:
        decreasing i.

    B:
        dp[n] = 0

    O:
        dp[0]

    Complexity:
        O(n * max_take)
    """
    n = len(values)
    dp = [0] * (n + 1)

    for i in range(n - 1, -1, -1):
        gain = 0
        best = -10**18

        for x in range(1, max_take + 1):
            if i + x > n:
                break

            gain += values[i + x - 1]
            best = max(best, gain - dp[i + x])

        dp[i] = best

    return dp[0]


# =============================================================================
# Stone Game I
# =============================================================================


def stone_game_i(piles: list[int]) -> bool:
    """
    LeetCode:
        877. Stone Game

    Problem:
        Alice and Bob take stones from either end.
        Higher total wins.

    DP solution:
        Same as Predict the Winner:
            interval score-difference DP.

    For the original LeetCode constraints:
        even number of piles and odd total
        Alice can always win by parity strategy.

    But using DP keeps the primitive general.
    """
    return interval_score_difference(piles) > 0


def stone_game_i_math(piles: list[int]) -> bool:
    """
    Mathematical shortcut for LeetCode 877's original constraints.

    Alice can commit to either all even-indexed piles or all odd-indexed piles.
    Since one parity has larger sum, Alice can force that parity.

    This is not the general interval-game solution.
    """
    return True


# =============================================================================
# Stone Game II
# =============================================================================


def stone_game_ii(piles: list[int]) -> int:
    """
    LeetCode:
        1140. Stone Game II

    Rule:
        Starting with M = 1, current player can take X piles where:
            1 <= X <= 2M
        Then M becomes max(M, X).

    S:
        dfs(i, m) = maximum stones current player can collect from piles[i:]
                    given current M = m.

    R:
        If current player takes x piles:
            current gets suffix[i] - opponent_best_after_move

        opponent state:
            dfs(i + x, max(m, x))

        candidate:
            suffix[i] - dfs(i + x, max(m, x))

    T:
        top-down memo over i increasing through recursion.

    B:
        if 2m >= remaining piles, current player takes all.

    O:
        dfs(0, 1)

    Complexity:
        O(n^3) conservative, often described as O(n^2) states with transitions.
    """
    n = len(piles)
    suffix = suffix_sums(piles)

    @cache
    def dfs(i: int, m: int) -> int:
        if i >= n:
            return 0

        if 2 * m >= n - i:
            return suffix[i]

        best = 0

        for x in range(1, 2 * m + 1):
            best = max(best, suffix[i] - dfs(i + x, max(m, x)))

        return best

    return dfs(0, 1)


# =============================================================================
# Stone Game III
# =============================================================================


def stone_game_iii(stone_value: list[int]) -> str:
    """
    LeetCode:
        1406. Stone Game III

    Rule:
        Current player may take 1, 2, or 3 stones from the front.

    S:
        dp[i] = maximum score difference current player can force
                from stone_value[i:].

    R:
        take x in {1,2,3}:
            gain = sum(stone_value[i:i+x])
            candidate = gain - dp[i+x]

    T:
        decreasing i.

    B:
        dp[n] = 0

    O:
        sign of dp[0].
    """
    diff = suffix_take_k_score_difference(stone_value, 3)

    if diff > 0:
        return "Alice"

    if diff < 0:
        return "Bob"

    return "Tie"


# =============================================================================
# Stone Game IV
# =============================================================================


def winner_square_game(n: int) -> bool:
    """
    LeetCode:
        1510. Stone Game IV

    Rule:
        Players remove a non-zero square number of stones.
        Player unable to move loses.

    This is win/lose impartial game DP.

    S:
        win[i] = whether current player wins with i stones.

    R:
        win[i] = any(not win[i - square] for square <= i)

    T:
        increasing i.

    B:
        win[0] = False

    O:
        win[n]

    Complexity:
        O(n * sqrt(n))
    """
    win = [False] * (n + 1)

    for stones in range(1, n + 1):
        root = isqrt(stones)

        for x in range(1, root + 1):
            if not win[stones - x * x]:
                win[stones] = True
                break

    return win[n]


# =============================================================================
# Stone Game V
# =============================================================================


def stone_game_v(stone_value: list[int]) -> int:
    """
    LeetCode:
        1563. Stone Game V

    Rule:
        Alice splits stones into left and right non-empty parts.
        Bob discards the part with larger sum.
        Alice scores the remaining part's sum.
        If equal, Alice chooses which part remains.

    S:
        dp[l][r] = max score Alice can obtain from stone_value[l:r+1].

    R:
        choose split k:
            left_sum = sum(l..k)
            right_sum = sum(k+1..r)

            if left_sum < right_sum:
                score = left_sum + dp[l][k]

            if left_sum > right_sum:
                score = right_sum + dp[k+1][r]

            if equal:
                score = left_sum + max(dp[l][k], dp[k+1][r])

    T:
        increasing interval length.

    B:
        singleton interval = 0 because no split possible.

    Complexity:
        O(n^3)
    """
    n = len(stone_value)
    ps = prefix_sums(stone_value)
    dp = [[0] * n for _ in range(n)]

    for l, r, length in inclusive_intervals(n):
        if length == 1:
            dp[l][r] = 0
            continue

        best = 0

        for k in range(l, r):
            left = range_sum(ps, l, k + 1)
            right = range_sum(ps, k + 1, r + 1)

            if left < right:
                best = max(best, left + dp[l][k])
            elif left > right:
                best = max(best, right + dp[k + 1][r])
            else:
                best = max(best, left + max(dp[l][k], dp[k + 1][r]))

        dp[l][r] = best

    return dp[0][n - 1]


# =============================================================================
# Stone Game VI
# =============================================================================


def stone_game_vi(alice_values: list[int], bob_values: list[int]) -> int:
    """
    LeetCode:
        1686. Stone Game VI

    This is the major greedy exception.

    Each stone has:
        value to Alice = alice_values[i]
        value to Bob   = bob_values[i]

    If Alice takes stone i:
        Alice gains alice[i]
        Bob is denied bob[i]

    Total swing of taking stone i:
        alice[i] + bob[i]

    Greedy:
        Sort stones descending by alice[i] + bob[i].
        Players take turns.

    O:
        return:
            1 if Alice wins
           -1 if Bob wins
            0 if tie

    This is not interval DP.
    """
    order = sorted(
        range(len(alice_values)),
        key=lambda i: alice_values[i] + bob_values[i],
        reverse=True,
    )

    alice = 0
    bob = 0

    for turn, i in enumerate(order):
        if turn % 2 == 0:
            alice += alice_values[i]
        else:
            bob += bob_values[i]

    if alice > bob:
        return 1

    if alice < bob:
        return -1

    return 0


# =============================================================================
# Stone Game VII
# =============================================================================


def stone_game_vii(stones: list[int]) -> int:
    """
    LeetCode:
        1690. Stone Game VII

    Rule:
        Current player removes one stone from either end.
        Score gained is sum of remaining stones.

    S:
        dp[l][r] = max score difference current player can force
                  from stones[l:r+1].

    R:
        remove left:
            sum(l+1..r) - dp[l+1][r]

        remove right:
            sum(l..r-1) - dp[l][r-1]

    T:
        increasing interval length.

    B:
        singleton = 0, because removing last stone gains 0.

    Complexity:
        O(n^2)
    """
    n = len(stones)
    ps = prefix_sums(stones)
    dp = [[0] * n for _ in range(n)]

    for l, r, length in inclusive_intervals(n):
        if length == 1:
            dp[l][r] = 0
            continue

        remove_left = range_sum(ps, l + 1, r + 1) - dp[l + 1][r]
        remove_right = range_sum(ps, l, r) - dp[l][r - 1]
        dp[l][r] = max(remove_left, remove_right)

    return dp[0][n - 1]


# =============================================================================
# Stone Game VIII
# =============================================================================


def stone_game_viii(stones: list[int]) -> int:
    """
    LeetCode:
        1872. Stone Game VIII

    Rule:
        On each move, remove x > 1 stones from the beginning.
        Add their sum to current player's score.
        Replace those stones with one stone equal to their sum.

    Standard transformation:
        Work with prefix sums.

    Let prefix[i] = sum(stones[:i+1]).

    DP idea:
        Once a prefix up to i is collapsed, future game is represented by i.

    Optimized recurrence:
        best = prefix[n-1]
        for i from n-2 down to 1:
            best = max(best, prefix[i] - best)

    O:
        best

    This is suffix score-difference DP compressed to O(1).
    """
    prefix = stones[:]

    for i in range(1, len(prefix)):
        prefix[i] += prefix[i - 1]

    best = prefix[-1]

    for i in range(len(stones) - 2, 0, -1):
        best = max(best, prefix[i] - best)

    return best


# =============================================================================
# Stone Game IX
# =============================================================================


def stone_game_ix(stones: list[int]) -> bool:
    """
    LeetCode:
        2029. Stone Game IX

    Rule:
        Players remove stones.
        If after a move, total sum is divisible by 3, that player loses.
        If no stones remain and nobody lost, Bob wins.

    This is a game-theory / residue-count exception.

    Only residues modulo 3 matter.

    Known criterion:
        let c0, c1, c2 be counts by residue.

        If c0 is even:
            Alice wins iff c1 > 0 and c2 > 0.

        If c0 is odd:
            Alice wins iff abs(c1 - c2) > 2.

    This is not interval DP.
    """
    count = [0, 0, 0]

    for x in stones:
        count[x % 3] += 1

    c0, c1, c2 = count

    if c0 % 2 == 0:
        return c1 > 0 and c2 > 0

    return abs(c1 - c2) > 2


# =============================================================================
# Series Family Map
# =============================================================================


STONE_GAME_SERIES_LADDER = {
    "877_stone_game_i": {
        "family": "interval score-difference DP / parity-strategy shortcut",
        "state": "dp[l][r]",
        "transition": "choose left or right",
    },
    "1140_stone_game_ii": {
        "family": "suffix game DP with expanding M",
        "state": "dfs(i, M)",
        "transition": "take X in 1..2M",
    },
    "1406_stone_game_iii": {
        "family": "suffix take-k score-difference DP",
        "state": "dp[i]",
        "transition": "take 1, 2, or 3",
    },
    "1510_stone_game_iv": {
        "family": "win/lose impartial game DP",
        "state": "win[n]",
        "transition": "remove square number",
    },
    "1563_stone_game_v": {
        "family": "split-point interval DP",
        "state": "dp[l][r]",
        "transition": "choose split k",
    },
    "1686_stone_game_vi": {
        "family": "greedy total-swing sorting",
        "state": "sorted by alice[i] + bob[i]",
        "transition": "alternate picking",
    },
    "1690_stone_game_vii": {
        "family": "interval score-difference with prefix sums",
        "state": "dp[l][r]",
        "transition": "remove left/right and score remaining sum",
    },
    "1872_stone_game_viii": {
        "family": "suffix score-difference DP over prefix sums",
        "state": "best from collapsed prefix index",
        "transition": "continue or stop at prefix i",
    },
    "2029_stone_game_ix": {
        "family": "modulo-count game theory",
        "state": "counts of residues mod 3",
        "transition": "criterion, not table DP",
    },
}


STONE_GAME_DIAGNOSTIC_CHECKLIST = [
    "Is the game state an interval, suffix, pile count, or residue count?",
    "Is the score best represented as absolute score or score difference?",
    "Does the current player's gain become opponent's loss through subtraction?",
    "What are the legal moves from the state?",
    "Does each move shrink the interval or advance the suffix?",
    "Can prefix/suffix sums make move gains O(1)?",
    "Is this actually a greedy/game-theory exception?",
    "What is the terminal state?",
    "Does the problem ask for winner, score, score difference, or Alice's absolute score?",
    "Can the recurrence be compressed from table to rolling/scalar form?",
]


PART_9_PROBLEM_MAP = {
    "interval_score_difference": [
        486,
        877,
        1690,
    ],
    "suffix_take_k_game_dp": [
        1140,
        1406,
        1872,
    ],
    "win_loss_impartial_game": [
        1510,
    ],
    "split_interval_game_dp": [
        1563,
    ],
    "greedy_total_swing": [
        1686,
    ],
    "modulo_game_theory": [
        2029,
    ],
}


if __name__ == "__main__":
    assert stone_game_i([5, 3, 4, 5]) is True
    assert stone_game_i_math([5, 3, 4, 5]) is True

    assert stone_game_ii([2, 7, 9, 4, 4]) == 10

    assert stone_game_iii([1, 2, 3, 7]) == "Bob"
    assert stone_game_iii([1, 2, 3, -9]) == "Alice"
    assert stone_game_iii([1, 2, 3, 6]) == "Tie"

    assert winner_square_game(1) is True
    assert winner_square_game(2) is False
    assert winner_square_game(4) is True

    assert stone_game_v([6, 2, 3, 4, 5, 5]) == 18

    assert stone_game_vi([1, 3], [2, 1]) == 1
    assert stone_game_vi([1, 2], [3, 1]) == 0
    assert stone_game_vi([2, 4, 3], [1, 6, 7]) == -1

    assert stone_game_vii([5, 3, 1, 4, 2]) == 6

    assert stone_game_viii([-1, 2, -3, 4, -5]) == 5
    assert stone_game_viii([7, -6, 5, 10, 5, -2, -6]) == 13

    assert stone_game_ix([2, 1]) is True
    assert stone_game_ix([2]) is False
    assert stone_game_ix([5, 1, 2, 4, 3]) is False
