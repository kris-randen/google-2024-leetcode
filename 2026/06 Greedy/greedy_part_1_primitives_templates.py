"""
Greedy primitives toolkit templates.

These are not full LeetCode solutions for every problem. They are reusable
skeletons that compose into the major Greedy-tagged families:
interval scheduling, coverage expansion, jump frontier, deferred heap choice,
replacement heap, delta sorting, pair extremes, frequency construction,
lexicographic monotonic deletion, and binary-search-on-answer feasibility.


Done. I created:

1. [Greedy problem catalogue CSV — 460 rows](sandbox:/mnt/data/leetcode_greedy_problem_catalog.csv)
2. [Greedy family summary CSV](sandbox:/mnt/data/leetcode_greedy_family_summary.csv)
3. [Greedy primitive code templates Python file](sandbox:/mnt/data/greedy_primitives_templates.py)

I used the attached LeetCode Greedy list, which contains **460 questions** with difficulty and acceptance data, as the source catalogue.  The attached prompt explicitly asks for the primitive → skeleton → recipe style, proof machinery, series ladders, Greedy-vs-DP boundary, and code templates.

## Part 1 — Greedy Toolkit Map

### A. Executive Summary

Greedy is not “pick the locally best thing.”

Greedy is:

```text
Find an ordering or state invariant where one local choice becomes globally safe.
```


The highest-value Greedy primitives are:


| Rank | Primitive                        | Why it matters                                              |
| ---: | -------------------------------- | ----------------------------------------------------------- |
|    1 | Sort by safe commit key          | Turns messy choice into deterministic order                 |
|    2 | Earliest finishing interval      | Unlocks interval scheduling/stabbing                        |
|    3 | Reachable frontier               | Jump Game, coverage, patching                               |
|    4 | Deferred heap choice             | IPO, refueling, furthest building                           |
|    5 | Replacement heap                 | Course Schedule III, max performance/team selection         |
|    6 | Delta sorting                    | Two City, Mice and Cheese, opportunity-cost problems        |
|    7 | Pair extremes                    | Boats, cookies, matching, minimizing max pair               |
|    8 | Monotonic lexicographic deletion | Remove K Digits, Duplicate Letters, Competitive Subsequence |
|    9 | Frequency/cooldown construction  | Reorganize String, Task Scheduler variants                  |
|   10 | Greedy feasibility predicate     | Binary-search-on-answer problems                            |

---

### B. Greedy Mental Model

A Greedy problem usually reduces to one of these statements:

```text
1. I can safely commit the earliest-ending / smallest / largest candidate.
2. I cannot decide yet, so I defer the choice in a heap.
3. I can sort by opportunity cost and take the top k deltas.
4. I can maintain a frontier and always extend it as far as possible.
5. I can repair local violations without harming previous optimality.
6. I can binary-search the answer and use greedy only as feasibility check.
7. I can choose lexicographically smaller now if future feasibility is preserved.

```

The proof style is the real primitive. For each greedy idea, ask:

```text
Can I exchange an optimal solution's first choice with mine?
Does my frontier stay at least as far as any other method?
Does this local repair preserve all previous constraints?
Is the answer monotone so greedy can be used only inside binary search?
```

---

### C. Ranked Toolkit of Primitives

| Rank | Primitive                                | Skeletons unlocked              | Representative problems |
| ---: | ---------------------------------------- | ------------------------------- | ----------------------- |
|    1 | `sort_by_end + keep last_end`            | Interval scheduling             | 435, 452, 646           |
|    2 | `coverage_frontier + farthest_extension` | Coverage expansion              | 1024, 1326, 330, 2952   |
|    3 | `reachable_frontier`                     | Jump reachability               | 55, 45                  |
|    4 | `available_candidates_heap`              | Deferred choice                 | 502, 871, 1642          |
|    5 | `replacement_heap`                       | Keep best feasible selected set | 630, 857, 1383, 2542    |
|    6 | `delta_sorting`                          | Opportunity-cost allocation     | 1029, 2611              |
|    7 | `pair_extremes`                          | Matching / capacity             | 881, 1877               |
|    8 | `smallest_sufficient_resource`           | Matching                        | 455, 2410               |
|    9 | `monotonic_delete_stack`                 | Lexicographic deletion          | 402, 316, 1081, 1673    |
|   10 | `frequency_heap + cooldown`              | Rearrangement/scheduling        | 621, 767, 358           |
|   11 | `running_surplus_reset`                  | Circular feasibility            | 134                     |
|   12 | `prefix/suffix repair`                   | Local constraints               | 135, 2366               |
|   13 | `residue/parity invariant`               | Game/count feasibility          | 2029, 1262              |
|   14 | `greedy_feasible(x)`                     | Binary search on answer         | 410, 2064, 2616, 2528   |
|   15 | `marginal_gain_heap`                     | Diminishing returns             | 1792, 2208, 2233        |

---

### D. Layered Arsenal

```text
Level 0 — Testing / Counterexample Utilities
    brute force validator
    small random case generator
    greedy-vs-brute checker
    adversarial examples

Level 1 — Atomic Greedy Moves
    choose min
    choose max
    choose earliest end
    choose farthest extension
    choose smallest sufficient resource
    choose largest marginal gain
    choose best delta
    replace current worst
    defer decision until forced

Level 2 — State / Invariant Primitives
    reachable frontier
    coverage interval
    running surplus
    active interval heap
    selected set heap
    available candidates heap
    monotonic chosen subsequence
    remaining frequency map
    cooldown queue
    parity/residue counts
    feasibility predicate

Level 3 — Composition Skeletons
    interval scheduling
    interval stabbing
    coverage expansion
    jump frontier
    refueling/deferred gain
    deadline scheduling
    replacement heap scheduling
    top-k under bottleneck
    lexicographic deletion
    pair extremes
    delta allocation
    binary-search + greedy check

Level 4 — Problem Recipes
    solve only by composing Level 1–3 primitives
```

---

### E. Composition Chains

```text
sort by end
+ keep last chosen end
+ exchange argument
-> interval scheduling
-> 435, 646
```

```text
sort by interval start
+ maintain current coverage
+ choose farthest reachable end
+ stays-ahead proof
-> coverage expansion
-> 1024, 1326
```

```text
scan array
+ current_end as layer boundary
+ farthest as next frontier
+ BFS-layer mental model
-> minimum jumps
-> 45
```

```text
sort by unlock condition
+ max-heap of available gains
+ choose best only among currently feasible choices
-> deferred greedy
-> 502, 871
```

```text
sort by deadline
+ max-heap of selected durations
+ if infeasible, remove longest selected duration
-> replacement heap scheduling
-> 630
```

```text
sort by bottleneck descending
+ min-heap of selected additive values
+ evaluate score at each bottleneck threshold
-> top-k under bottleneck
-> 1383, 2542
```

```text
remaining counts
+ monotonic stack
+ pop only if future feasibility survives
-> lexicographic deletion
-> 316, 1081, 402, 1673
```

---

### F. Problem-Family Map

| Family                        | Core reduction                                 | Key primitives              | Examples              |
| ----------------------------- | ---------------------------------------------- | --------------------------- | --------------------- |
| Interval scheduling           | Keep earliest-ending compatible item           | sort by end, last_end       | 435, 646              |
| Interval stabbing             | Place point at earliest end                    | sort by end, stabbing point | 452, 757              |
| Active interval heap          | Count or group overlaps                        | min-heap of end times       | 253, 2406             |
| Coverage expansion            | Extend covered region maximally                | farthest extension          | 1024, 1326            |
| Patching / constructible sums | Maintain `[1, miss)` coverage                  | coverage frontier           | 330, 1798, 2952       |
| Jump frontier                 | Maintain farthest reachable index              | current_end, farthest       | 55, 45                |
| Deferred heap choice          | Use best past option only when needed          | max-heap gains              | 502, 871, 1642        |
| Replacement heap              | Keep best feasible selected set                | remove worst selected       | 630, 857, 1383, 2542  |
| Delta sorting                 | Choose by opportunity cost                     | sort by delta               | 1029, 2611            |
| Pairing/matching              | Match extremes or smallest sufficient          | two pointers                | 455, 870, 881, 2410   |
| Lexicographic greedy          | Improve current prefix while preserving future | monotonic stack             | 316, 402, 1081, 1673  |
| Frequency scheduling          | Choose high-frequency item under constraints   | heap, cooldown              | 621, 767, 358         |
| Binary search + greedy        | Greedy is only the feasibility check           | monotone predicate          | 410, 2064, 2616, 2528 |
| Game/count invariant          | Optimal play reduces to counts/parity/order    | residue, combined score     | 1686, 2029            |

---

### G. Series Evolution Ladders

#### 1. Jump Game

```text
55 Jump Game
    frontier feasibility

45 Jump Game II
    frontier layers = minimum jumps

1024 Video Stitching / 1326 Taps
    jump frontier generalized to interval coverage

330 Patching Array / 2952 Coins
    coverage frontier generalized to constructible sums
```

Core primitive:

```text
current covered region + farthest extension
```

---

#### 2. Stock

```text
122 Stock II
    pure greedy: sum positive deltas

714 Stock with Fee
    compressed 2-state DP / greedy-DP boundary

Cooldown / at most k transactions
    not pure greedy; becomes DP
```

Core lesson:

```text
Unlimited independent transactions -> greedy.
Transaction constraints coupling decisions across time -> DP.
```

---

#### 3. Stone Game

```text
Stone Game VI
    greedy by combined value Alice[i] + Bob[i]

Stone Game IX
    residue-count game theory, not local greedy

Other Stone Game variants
    often minimax / interval DP
```

Core lesson:

```text
If both players value the same choice differently, sort by total swing.
If future state depends on interval choices, expect DP/game theory.
```

---

#### 4. Knapsack / Selection

```text
Fractional knapsack
    greedy by value/weight ratio

0/1 knapsack
    ratio greedy fails; DP needed

Top-k with bottleneck
    sort bottleneck + heap selected values

Worker/team variants
    857, 1383, 2542
```

Core lesson:

```text
Divisible items -> ratio greedy.
Indivisible items with capacity interactions -> DP/heap hybrid.
```

---

#### 5. Interval Series

```text
435 Non-overlapping Intervals
    choose earliest end

452 Arrows
    choose stabbing point at earliest end

253 Meeting Rooms II / 2406 Groups
    active interval heap

1024 Video Stitching / 1326 Taps
    coverage expansion

2589 Minimum Time to Complete Tasks
    latest feasible time slots inside intervals
```

---

### H. Greedy vs DP Boundary

| Looks greedy                    | Actually                                         |
| ------------------------------- | ------------------------------------------------ |
| Stock II                        | Pure greedy                                      |
| Stock with fee                  | Greedy-DP compression                            |
| Stock cooldown / k transactions | DP                                               |
| Fractional knapsack             | Pure greedy                                      |
| 0/1 knapsack                    | DP                                               |
| Stone Game VI                   | Greedy game scoring                              |
| Most Stone Games                | Game DP                                          |
| Split Array Largest Sum         | Binary search + greedy check                     |
| House Robber IV                 | Binary search + greedy feasibility / DP boundary |
| Wildcard Matching               | DP or special greedy-backtracking                |

---

### I. Highest-ROI Practice Order

1. 435 Non-overlapping Intervals
2. 452 Minimum Number of Arrows
3. 55 Jump Game
4. 45 Jump Game II
5. 1024 Video Stitching
6. 330 Patching Array
7. 502 IPO
8. 871 Minimum Refueling Stops
9. 630 Course Schedule III
10. 1642 Furthest Building
11. 1029 Two City Scheduling
12. 455 Assign Cookies
13. 881 Boats to Save People
14. 402 Remove K Digits
15. 316 Remove Duplicate Letters
16. 1673 Most Competitive Subsequence
17. 621 Task Scheduler
18. 767 Reorganize String
19. 410 Split Array Largest Sum
20. 2542 Maximum Subsequence Score

---

### J. Common Traps

```text
1. Sorting by start instead of end in interval scheduling.
2. Choosing current largest gain too early instead of deferring with heap.
3. Confusing reachability frontier with jump-count frontier.
4. Using greedy for 0/1 knapsack.
5. Using greedy for constrained stock problems that need DP.
6. Popping from monotonic stack without proving future availability.
7. Forgetting closed vs half-open interval boundaries.
8. Applying “take max” when the true key is delta/opportunity cost.
9. Treating all Stone Games as greedy.
10. Forgetting that binary-search problems use greedy only as a check.
```

The CSV catalogue has an inferred `classification_confidence` column. Rows marked `manual-high` are the important/high-confidence anchors; rows marked `heuristic` are title-inferred and should be refined as we expand each family.


"""

from __future__ import annotations

from collections import Counter, deque
from heapq import heappop, heappush, heapify
from itertools import combinations
from typing import Callable, Iterable, Iterator, Optional, Sequence, TypeVar

T = TypeVar("T")


# -----------------------------------------------------------------------------
# Level 0: small testing / validation helpers
# -----------------------------------------------------------------------------


def argmax(items: Iterable[T], key: Callable[[T], int | float]) -> Optional[T]:
    best = None
    for item in items:
        if best is None or key(item) > key(best):
            best = item
    return best


def argmin(items: Iterable[T], key: Callable[[T], int | float]) -> Optional[T]:
    best = None
    for item in items:
        if best is None or key(item) < key(best):
            best = item
    return best


def check_against_bruteforce(
    cases: Iterable[T],
    greedy: Callable[[T], object],
    brute: Callable[[T], object],
) -> None:
    for case in cases:
        g = greedy(case)
        b = brute(case)
        assert g == b, (case, g, b)


# -----------------------------------------------------------------------------
# Interval scheduling / stabbing / active-set primitives
# -----------------------------------------------------------------------------


def max_non_overlapping_intervals(intervals: list[tuple[int, int]]) -> int:
    """
    Primitive:
        Sort by end time, keep earliest-ending compatible interval.

    Solves skeletons like:
        435 Non-overlapping Intervals
        646 Maximum Length of Pair Chain
    """
    last_end = float("-inf")
    count = 0

    for start, end in sorted(intervals, key=lambda x: x[1]):
        if start >= last_end:
            count += 1
            last_end = end

    return count


def min_stabbing_points(intervals: list[tuple[int, int]]) -> int:
    """
    Primitive:
        Sort by end time, place one point at current interval's end,
        consume every interval containing that point.

    Solves skeletons like:
        452 Minimum Number of Arrows to Burst Balloons
    """
    points = 0
    last_point = float("-inf")

    for start, end in sorted(intervals, key=lambda x: x[1]):
        if start > last_point:
            points += 1
            last_point = end

    return points


def min_active_groups(intervals: list[tuple[int, int]], *, closed: bool = True) -> int:
    """
    Primitive:
        Sort by start, keep active interval ends in a min-heap.

    closed=True means [start, end] intervals overlap when start <= previous_end.
    closed=False means [start, end) intervals do not overlap when start >= previous_end.

    Solves skeletons like:
        253 Meeting Rooms II
        2406 Divide Intervals Into Minimum Number of Groups
    """
    active: list[int] = []
    best = 0

    for start, end in sorted(intervals):
        while active and (active[0] < start if closed else active[0] <= start):
            heappop(active)

        heappush(active, end)
        best = max(best, len(active))

    return best


# -----------------------------------------------------------------------------
# Coverage expansion / jump frontier primitives
# -----------------------------------------------------------------------------


def min_intervals_to_cover(
    intervals: list[tuple[int, int]],
    target_start: int,
    target_end: int,
) -> int:
    """
    Primitive:
        Current coverage is [target_start, covered]. Among all intervals starting
        at or before covered, choose the one that extends farthest.

    Solves skeletons like:
        1024 Video Stitching
        1326 Minimum Number of Taps to Open to Water a Garden
    """
    intervals.sort()
    i = 0
    used = 0
    covered = target_start

    while covered < target_end:
        farthest = covered

        while i < len(intervals) and intervals[i][0] <= covered:
            farthest = max(farthest, intervals[i][1])
            i += 1

        if farthest == covered:
            return -1

        used += 1
        covered = farthest

    return used


def can_jump(nums: Sequence[int]) -> bool:
    """
    Primitive:
        Maintain farthest reachable index. If current index crosses the frontier,
        reachability has failed.

    Solves:
        55 Jump Game
    """
    farthest = 0

    for i, jump in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + jump)

    return True


def min_jumps(nums: Sequence[int]) -> int:
    """
    Primitive:
        BFS-level interpretation of array jumps.
        current_end is the end of the current jump layer.
        farthest is the next layer frontier.

    Solves:
        45 Jump Game II
    """
    jumps = 0
    current_end = 0
    farthest = 0

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])

        if i == current_end:
            jumps += 1
            current_end = farthest

    return jumps


def min_patches(nums: Sequence[int], n: int) -> int:
    """
    Primitive:
        Coverage invariant: all sums in [1, miss) are constructible.
        If next number <= miss, extend coverage.
        Otherwise patch exactly miss.

    Solves:
        330 Patching Array
        2952 Minimum Number of Coins to be Added
    """
    miss = 1
    i = 0
    patches = 0

    while miss <= n:
        if i < len(nums) and nums[i] <= miss:
            miss += nums[i]
            i += 1
        else:
            miss += miss
            patches += 1

    return patches


# -----------------------------------------------------------------------------
# Heap greedy / deferred choice / replacement heap primitives
# -----------------------------------------------------------------------------


def max_capital_after_projects(
    k: int,
    capital: int,
    projects: list[tuple[int, int]],
) -> int:
    """
    projects: list of (required_capital, profit)

    Primitive:
        Sort by required capital. Push profits of all currently affordable
        projects. Pick max profit among available projects.

    Solves skeletons like:
        502 IPO
    """
    projects.sort()
    available: list[int] = []
    i = 0

    for _ in range(k):
        while i < len(projects) and projects[i][0] <= capital:
            heappush(available, -projects[i][1])
            i += 1

        if not available:
            break

        capital -= heappop(available)

    return capital


def min_refuels(target: int, start_fuel: int, stations: list[tuple[int, int]]) -> int:
    """
    stations: list of (position, fuel)

    Primitive:
        Defer refueling until forced. When forced, use the largest fuel among
        stations already passed.

    Solves:
        871 Minimum Number of Refueling Stops
    """
    stations = stations + [(target, 0)]
    fuel = start_fuel
    prev = 0
    stops = 0
    passed: list[int] = []

    for pos, gain in stations:
        fuel -= pos - prev

        while fuel < 0 and passed:
            fuel -= heappop(passed)
            stops += 1

        if fuel < 0:
            return -1

        heappush(passed, -gain)
        prev = pos

    return stops


def max_count_with_deadlines(courses: list[tuple[int, int]]) -> int:
    """
    courses: list of (duration, deadline)

    Primitive:
        Sort by deadline. Keep selected durations. If total time exceeds current
        deadline, remove the longest selected duration.

    Solves:
        630 Course Schedule III
    """
    total = 0
    chosen: list[int] = []

    for duration, deadline in sorted(courses, key=lambda x: x[1]):
        total += duration
        heappush(chosen, -duration)

        if total > deadline:
            total += heappop(chosen)

    return len(chosen)


def top_k_under_bottleneck(
    items: list[tuple[int, int]],
    k: int,
    score: Callable[[int, int], int],
) -> int:
    """
    items: list of (bottleneck_value, additive_value)

    Primitive:
        Sort by bottleneck descending. Keep k largest additive values among the
        current threshold. Evaluate score(sum_additive, current_bottleneck).

    Solves skeletons like:
        1383 Maximum Performance of a Team
        2542 Maximum Subsequence Score
    """
    best = 0
    total = 0
    selected: list[int] = []

    for bottleneck, additive in sorted(items, reverse=True):
        heappush(selected, additive)
        total += additive

        if len(selected) > k:
            total -= heappop(selected)

        if len(selected) == k:
            best = max(best, score(total, bottleneck))

    return best


# -----------------------------------------------------------------------------
# Pairing / matching / delta sorting primitives
# -----------------------------------------------------------------------------


def count_smallest_sufficient(demands: Sequence[int], resources: Sequence[int]) -> int:
    """
    Primitive:
        Sort demands and resources. Give the smallest sufficient resource to the
        smallest remaining demand.

    Solves skeletons like:
        455 Assign Cookies
        2410 Maximum Matching of Players With Trainers
    """
    ds = sorted(demands)
    rs = sorted(resources)
    i = 0

    for r in rs:
        if i < len(ds) and r >= ds[i]:
            i += 1

    return i


def boats_by_pairing_extremes(weights: Sequence[int], limit: int) -> int:
    """
    Primitive:
        Decide the heaviest remaining item. Pair it with the lightest if possible;
        otherwise send it alone.

    Solves:
        881 Boats to Save People
    """
    ws = sorted(weights)
    lo, hi = 0, len(ws) - 1
    boats = 0

    while lo <= hi:
        if ws[lo] + ws[hi] <= limit:
            lo += 1
        hi -= 1
        boats += 1

    return boats


def choose_by_delta(
    items: Sequence[T],
    k: int,
    delta: Callable[[T], int],
) -> list[T]:
    """
    Primitive:
        Choose k items with the largest opportunity-cost delta.

    Solves skeletons like:
        1029 Two City Scheduling
        2611 Mice and Cheese
    """
    return sorted(items, key=delta, reverse=True)[:k]


# -----------------------------------------------------------------------------
# Frequency / cooldown / construction primitives
# -----------------------------------------------------------------------------


def reorganize_without_adjacent_equal(chars: str) -> str:
    """
    Primitive:
        Always pick the currently highest-frequency character that is not cooling
        down from the previous step.

    Solves skeletons like:
        767 Reorganize String
        1054 Distant Barcodes
    """
    heap = [(-cnt, ch) for ch, cnt in Counter(chars).items()]
    heapify(heap)
    prev: Optional[tuple[int, str]] = None
    out = []

    while heap or prev:
        if not heap:
            return ""

        cnt, ch = heappop(heap)
        out.append(ch)
        cnt += 1

        if prev:
            heappush(heap, prev)
            prev = None

        if cnt < 0:
            prev = (cnt, ch)

    return "".join(out)


def split_into_consecutive_runs(nums: Sequence[int], k: int) -> bool:
    """
    Primitive:
        Process smallest remaining value and consume a full consecutive run.

    Solves skeletons like:
        846 Hand of Straights
        1296 Divide Array in Sets of K Consecutive Numbers
    """
    count = Counter(nums)

    for x in sorted(count):
        need = count[x]
        if need == 0:
            continue

        for y in range(x, x + k):
            if count[y] < need:
                return False
            count[y] -= need

    return True


# -----------------------------------------------------------------------------
# Lexicographic monotonic deletion / subsequence primitives
# -----------------------------------------------------------------------------


def remove_k_for_smallest(seq: Sequence[str], k: int) -> list[str]:
    """
    Primitive:
        While the previous chosen value is larger than current value, delete it
        if deletion budget remains.

    Solves:
        402 Remove K Digits
    """
    stack: list[str] = []

    for x in seq:
        while k and stack and stack[-1] > x:
            stack.pop()
            k -= 1
        stack.append(x)

    if k:
        del stack[-k:]

    return stack


def smallest_distinct_subsequence(s: str) -> str:
    """
    Primitive:
        Monotonic stack with future availability. Pop larger previous character
        only if it appears again later.

    Solves:
        316 Remove Duplicate Letters
        1081 Smallest Subsequence of Distinct Characters
    """
    remaining = Counter(s)
    used = set()
    stack: list[str] = []

    for ch in s:
        remaining[ch] -= 1

        if ch in used:
            continue

        while stack and stack[-1] > ch and remaining[stack[-1]] > 0:
            used.remove(stack.pop())

        stack.append(ch)
        used.add(ch)

    return "".join(stack)


def most_competitive_subsequence(nums: Sequence[int], k: int) -> list[int]:
    """
    Primitive:
        Monotonic stack with fixed output length. Pop larger previous value only
        if enough remaining elements exist to still fill length k.

    Solves:
        1673 Find the Most Competitive Subsequence
    """
    stack: list[int] = []
    n = len(nums)

    for i, x in enumerate(nums):
        while stack and stack[-1] > x and len(stack) - 1 + (n - i) >= k:
            stack.pop()

        if len(stack) < k:
            stack.append(x)

    return stack


# -----------------------------------------------------------------------------
# Binary-search-on-answer + greedy feasibility primitive
# -----------------------------------------------------------------------------


def first_true(lo: int, hi: int, feasible: Callable[[int], bool]) -> int:
    """
    Primitive:
        Find the smallest value in [lo, hi] for which feasible(value) is true.
    """
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def split_count_needed(nums: Sequence[int], max_sum: int) -> int:
    """
    Greedy feasibility helper:
        Given a max allowed subarray sum, count how many subarrays are needed.

    Solves check for:
        410 Split Array Largest Sum
    """
    groups = 1
    curr = 0

    for x in nums:
        if x > max_sum:
            return 10**18

        if curr + x <= max_sum:
            curr += x
        else:
            groups += 1
            curr = x

    return groups


def minimize_largest_split_sum(nums: Sequence[int], k: int) -> int:
    return first_true(
        max(nums),
        sum(nums),
        feasible=lambda cap: split_count_needed(nums, cap) <= k,
    )
