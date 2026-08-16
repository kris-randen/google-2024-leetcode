"""
Greedy Algorithms — Part 2
Proof + Counterexample Toolkit

This file is intentionally not a full solution dump.

Purpose
-------
Greedy solutions are usually easy to code but hard to trust.

This toolkit gives you:
    1. proof patterns as reusable mental templates
    2. small brute-force validators
    3. counterexample harnesses
    4. a few canonical toy problems where greedy proof styles become visible

Core lesson
-----------
A greedy choice is not valid because it "looks best now."

A greedy choice is valid only when you can prove one of these:

    exchange argument:
        Any optimal solution can be transformed to include my choice.

    stays-ahead argument:
        After every step, my partial solution is at least as good as any other.

    dominance argument:
        Candidate A is never worse than candidate B, so B can be discarded.

    feasibility monotonicity:
        If target x is feasible, then all easier targets are feasible too.

    replacement argument:
        If the selected set becomes infeasible, removing the worst selected item
        preserves the best possible future.

    deferred-choice argument:
        I do not choose now. I collect feasible options and choose only when forced.
"""

from __future__ import annotations

from heapq import heappop, heappush
from itertools import combinations
from random import randint, seed
from typing import Callable, Iterable, Sequence, TypeVar


T = TypeVar("T")


# ---------------------------------------------------------------------
# Level 0 — Generic brute-force / validation helpers
# ---------------------------------------------------------------------

def all_subsequences(xs: Sequence[T]) -> Iterable[tuple[T, ...]]:
    """
    Emit every subsequence by index choice.

    Useful for checking:
        - interval scheduling
        - maximum compatible subset
        - choose k items
        - lexicographic subsequence problems on small inputs
    """
    n = len(xs)

    for r in range(n + 1):
        yield from combinations(xs, r)


def best_by_bruteforce(
    candidates: Iterable[T],
    feasible: Callable[[T], bool],
    score: Callable[[T], int | float | tuple],
) -> T | None:
    """
    Pick the best feasible candidate by exhaustive search.

    For small n only.

    This is not for production solutions.
    It is for testing whether a greedy idea is probably correct.
    """
    best = None
    best_score = None

    for x in candidates:
        if not feasible(x):
            continue

        s = score(x)

        if best is None or s > best_score:
            best = x
            best_score = s

    return best


def assert_matches_bruteforce(
    greedy: Callable[[T], int | float | tuple],
    brute: Callable[[T], int | float | tuple],
    gen_case: Callable[[], T],
    *,
    trials: int = 1000,
) -> None:
    """
    Randomized greedy validator.

    If this fails, it gives you a concrete counterexample.

    It does not prove correctness.
    It is a counterexample discovery tool.
    """
    for _ in range(trials):
        case = gen_case()
        g = greedy(case)
        b = brute(case)

        if g != b:
            raise AssertionError(
                f"Greedy failed.\ncase={case}\ngreedy={g}\nbrute={b}"
            )


# ---------------------------------------------------------------------
# Proof Pattern 1 — Exchange Argument
# ---------------------------------------------------------------------

def max_non_overlapping_intervals(intervals: list[tuple[int, int]]) -> int:
    """
    Greedy skeleton:
        sort by end
        take interval if compatible

    Proof style:
        exchange argument

    Why earliest end is safe:
        Let G be the interval with the earliest end.
        Take any optimal solution O.
        Let O_first be the first interval in O.
        Since G ends no later than O_first, replacing O_first with G
        cannot reduce room for the remaining intervals.
        Therefore some optimal solution starts with G.
    """
    end = float("-inf")
    count = 0

    for start, finish in sorted(intervals, key=lambda x: x[1]):
        if start >= end:
            count += 1
            end = finish

    return count


def brute_max_non_overlapping_intervals(intervals: list[tuple[int, int]]) -> int:
    def compatible(subset: tuple[tuple[int, int], ...]) -> bool:
        ordered = sorted(subset, key=lambda x: x[0])
        return all(a[1] <= b[0] for a, b in zip(ordered, ordered[1:]))

    return max(
        (len(subset) for subset in all_subsequences(intervals) if compatible(subset)),
        default=0,
    )


# ---------------------------------------------------------------------
# Proof Pattern 2 — Stays-Ahead Argument
# ---------------------------------------------------------------------

def can_reach_end(nums: list[int]) -> bool:
    """
    Greedy skeleton:
        scan left to right
        maintain farthest reachable index

    Proof style:
        stays-ahead

    Invariant:
        after processing index i, farthest is the farthest index reachable using
        jumps from positions <= i.

    If i ever exceeds farthest, no method can reach i.
    """
    farthest = 0

    for i, jump in enumerate(nums):
        if i > farthest:
            return False

        farthest = max(farthest, i + jump)

    return True


def min_jumps(nums: list[int]) -> int:
    """
    Greedy skeleton:
        current_end = end of current BFS layer
        farthest = farthest reachable from current layer
        when i reaches current_end, commit one jump

    Proof style:
        stays-ahead / BFS frontier

    Assumption:
        end is reachable.
    """
    if len(nums) <= 1:
        return 0

    jumps = 0
    current_end = 0
    farthest = 0

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])

        if i == current_end:
            jumps += 1
            current_end = farthest

    return jumps


# ---------------------------------------------------------------------
# Proof Pattern 3 — Coverage Frontier
# ---------------------------------------------------------------------

def min_patches(nums: list[int], n: int) -> int:
    """
    Greedy skeleton:
        maintain coverage [1, miss)
        if next num <= miss, extend coverage
        else patch with miss

    Proof style:
        stays-ahead / coverage invariant

    Invariant:
        all sums in [1, miss) are constructible.

    If nums[i] <= miss:
        adding nums[i] extends coverage to [1, miss + nums[i])

    If nums[i] > miss:
        miss itself is impossible unless we add a new number <= miss.
        Adding miss is optimal because it maximally extends coverage.
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


# ---------------------------------------------------------------------
# Proof Pattern 4 — Deferred Choice With Heap
# ---------------------------------------------------------------------

def min_refuel_stops(
    target: int,
    start_fuel: int,
    stations: list[tuple[int, int]],
) -> int:
    """
    Greedy skeleton:
        travel forward
        push fuels of stations already reachable
        when stuck, use the largest previous fuel

    Proof style:
        deferred choice

    Key idea:
        Do not choose a station when first seen.
        Choosing early is unnecessary.
        When fuel is insufficient, choose the best among all reachable stations.

    This is safer than:
        "always refuel at the biggest station ahead"
        or
        "always refuel as soon as possible"
    """
    stations = stations + [(target, 0)]
    fuel = start_fuel
    prev = 0
    stops = 0
    available: list[int] = []

    for pos, gain in stations:
        fuel -= pos - prev

        while fuel < 0 and available:
            fuel += -heappop(available)
            stops += 1

        if fuel < 0:
            return -1

        heappush(available, -gain)
        prev = pos

    return stops


# ---------------------------------------------------------------------
# Proof Pattern 5 — Replacement Heap
# ---------------------------------------------------------------------

def max_courses(courses: list[tuple[int, int]]) -> int:
    """
    Each course is:
        duration, deadline

    Greedy skeleton:
        sort by deadline
        tentatively take each course
        if total time exceeds deadline, remove longest selected duration

    Proof style:
        replacement argument

    Invariant:
        Among courses considered so far, the heap stores a feasible selected set
        with minimum possible total duration for its size.

    If infeasible:
        Removing the longest selected duration gives the most time back and keeps
        the largest number of courses.
    """
    total = 0
    selected: list[int] = []

    for duration, deadline in sorted(courses, key=lambda x: x[1]):
        total += duration
        heappush(selected, -duration)

        if total > deadline:
            total += heappop(selected)

    return len(selected)


# ---------------------------------------------------------------------
# Proof Pattern 6 — Delta Sorting / Opportunity Cost
# ---------------------------------------------------------------------

def two_city_cost(costs: list[tuple[int, int]]) -> int:
    """
    Greedy skeleton:
        send everyone to A initially
        choose n people to switch to B by smallest B - A delta

    Proof style:
        exchange / opportunity cost

    Equivalent:
        Sort by how much cheaper B is relative to A.
    """
    n = len(costs) // 2
    base = sum(a for a, _ in costs)
    deltas = sorted(b - a for a, b in costs)

    return base + sum(deltas[:n])


# ---------------------------------------------------------------------
# Proof Pattern 7 — Pair Extremes
# ---------------------------------------------------------------------

def boats_needed(people: list[int], limit: int) -> int:
    """
    Greedy skeleton:
        sort weights
        always place heaviest remaining person
        pair with lightest if possible

    Proof style:
        dominance / exchange

    Why heaviest must be handled now:
        The heaviest remaining person must go in some boat.
        If they can pair with the lightest, that pairing is safe because the
        lightest is the easiest possible partner.
        If they cannot pair with the lightest, they cannot pair with anyone.
    """
    people.sort()
    lo, hi = 0, len(people) - 1
    boats = 0

    while lo <= hi:
        if people[lo] + people[hi] <= limit:
            lo += 1

        hi -= 1
        boats += 1

    return boats


# ---------------------------------------------------------------------
# Proof Pattern 8 — Monotonic Lexicographic Deletion
# ---------------------------------------------------------------------

def remove_k_digits(num: str, k: int) -> str:
    """
    Greedy skeleton:
        maintain increasing stack
        remove previous larger digit if current digit is smaller

    Proof style:
        lexicographic exchange

    Why popping is safe:
        If previous digit d > current digit c, then putting c earlier makes the
        number lexicographically smaller, as long as we still have deletion budget.
    """
    stack: list[str] = []

    for digit in num:
        while k and stack and stack[-1] > digit:
            stack.pop()
            k -= 1

        stack.append(digit)

    if k:
        stack = stack[:-k]

    ans = "".join(stack).lstrip("0")
    return ans or "0"


def smallest_subsequence_distinct(s: str) -> str:
    """
    Greedy skeleton:
        monotonic stack
        each char used once
        pop only if popped char appears again later

    Proof style:
        lexicographic exchange + future feasibility

    Extra invariant beyond remove_k_digits:
        A character can be popped only if it can be recovered later.
    """
    remaining = {ch: s.count(ch) for ch in set(s)}
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


# ---------------------------------------------------------------------
# Proof Pattern 9 — Greedy Feasibility Predicate
# ---------------------------------------------------------------------

def can_split_with_largest_sum(nums: list[int], max_allowed: int, parts: int) -> bool:
    """
    Greedy feasibility check for Split Array Largest Sum.

    Predicate:
        Can nums be split into at most parts subarrays such that each sum <= max_allowed?

    Proof style:
        feasibility monotonicity

    If max_allowed works:
        any larger value also works.

    Greedy inside predicate:
        fill the current subarray until adding the next value would exceed max_allowed.
        This uses the fewest possible subarrays for this max_allowed.
    """
    used = 1
    current = 0

    for x in nums:
        if x > max_allowed:
            return False

        if current + x <= max_allowed:
            current += x
        else:
            used += 1
            current = x

    return used <= parts


def min_largest_split_sum(nums: list[int], parts: int) -> int:
    lo, hi = max(nums), sum(nums)

    while lo < hi:
        mid = (lo + hi) // 2

        if can_split_with_largest_sum(nums, mid, parts):
            hi = mid
        else:
            lo = mid + 1

    return lo


# ---------------------------------------------------------------------
# Counterexample utilities
# ---------------------------------------------------------------------

def random_intervals(
    *,
    n: int = 8,
    max_start: int = 10,
    max_len: int = 5,
) -> list[tuple[int, int]]:
    intervals = []

    for _ in range(n):
        start = randint(0, max_start)
        end = start + randint(1, max_len)
        intervals.append((start, end))

    return intervals


def validate_interval_scheduling(trials: int = 1000) -> None:
    """
    Example validator:
        greedy earliest-end interval scheduling vs brute force.

    If this passes, it does not prove correctness.
    But if it fails, your greedy idea is wrong.
    """
    assert_matches_bruteforce(
        max_non_overlapping_intervals,
        brute_max_non_overlapping_intervals,
        random_intervals,
        trials=trials,
    )


def wrong_interval_greedy_by_shortest_length(intervals: list[tuple[int, int]]) -> int:
    """
    Deliberately suspicious greedy:
        choose shortest interval first.

    This looks plausible but is not the canonical safe key.
    Use validators/counterexamples to distrust such ideas.
    """
    chosen: list[tuple[int, int]] = []

    for interval in sorted(intervals, key=lambda x: x[1] - x[0]):
        if all(interval[1] <= a or b <= interval[0] for a, b in chosen):
            chosen.append(interval)

    return len(chosen)


def find_counterexample_for_wrong_interval_greedy(
    *,
    trials: int = 10000,
) -> list[tuple[int, int]] | None:
    for _ in range(trials):
        case = random_intervals(n=7, max_start=8, max_len=6)

        wrong = wrong_interval_greedy_by_shortest_length(case)
        brute = brute_max_non_overlapping_intervals(case)

        if wrong != brute:
            return case

    return None


if __name__ == "__main__":
    seed(0)

    validate_interval_scheduling(1000)

    case = find_counterexample_for_wrong_interval_greedy()

    if case:
        print("Counterexample found:")
        print(case)
        print("wrong:", wrong_interval_greedy_by_shortest_length(case))
        print("brute:", brute_max_non_overlapping_intervals(case))
    else:
        print("No counterexample found in this run.")
