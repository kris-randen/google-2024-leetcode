
"""
Greedy Algorithms — Part 3
Interval Greedy Family

This file is a reusable interval-greedy toolkit.

It is intentionally written as primitives + recipes, not as a dump of unrelated
LeetCode solutions.

Core interval-greedy idea
-------------------------
Most interval greedy problems become simple after you identify the correct
"commit key":

    earliest end:
        choose the interval/point that leaves maximum room for future choices

    active end heap:
        track currently open intervals/resources

    closed interval stabbing:
        place a point at the earliest possible end that still covers current interval

    latest feasible slot:
        when a task needs slots inside [start, end], fill from the right side
        so earlier slots remain available for tighter future tasks

Important boundary convention
-----------------------------
There are two common interval models:

    half-open intervals: [start, end)
        compatible if previous_end <= current_start
        common for meeting rooms

    closed intervals: [start, end]
        compatible/non-overlapping if previous_end < current_start
        common for arrows / integer interval stabbing

Do not mix these.
"""

from __future__ import annotations

from heapq import heappop, heappush
from typing import Iterable, Sequence


Interval = tuple[int, int]
Task = tuple[int, int, int]


# ---------------------------------------------------------------------
# Level 0 — Representation / boundary predicates
# ---------------------------------------------------------------------

def start(interval: Interval) -> int:
    return interval[0]


def end(interval: Interval) -> int:
    return interval[1]


def sorted_by_end(intervals: Iterable[Interval]) -> list[Interval]:
    """
    Standard ordering for interval scheduling.

    Commit key:
        earliest finish time
    """
    return sorted(intervals, key=lambda x: x[1])


def sorted_by_start(intervals: Iterable[Interval]) -> list[Interval]:
    """
    Standard ordering for sweep-line / active-heap problems.
    """
    return sorted(intervals, key=lambda x: x[0])


def compatible_half_open(prev: Interval, curr: Interval) -> bool:
    """
    For [start, end) intervals.

    [1, 3) and [3, 5) do not overlap.
    """
    return end(prev) <= start(curr)


def disjoint_closed(prev: Interval, curr: Interval) -> bool:
    """
    For [start, end] intervals.

    [1, 3] and [3, 5] overlap at point 3.
    """
    return end(prev) < start(curr)


# ---------------------------------------------------------------------
# Level 1 — Earliest-end commit primitive
# ---------------------------------------------------------------------

def select_non_overlapping_half_open(intervals: Sequence[Interval]) -> list[Interval]:
    """
    Select the maximum number of non-overlapping half-open intervals.

    Primitive:
        sort by end
        take interval if start >= last_end

    Proof:
        exchange argument

    Why earliest end is safe:
        replacing the first interval of any optimal solution with the earliest
        ending compatible interval leaves at least as much room for the future.
    """
    chosen: list[Interval] = []
    last_end = float("-inf")

    for l, r in sorted_by_end(intervals):
        if l >= last_end:
            chosen.append((l, r))
            last_end = r

    return chosen


def max_non_overlapping_half_open(intervals: Sequence[Interval]) -> int:
    """
    Recipe:
        435 style, if interpreted as half-open compatibility.
    """
    return len(select_non_overlapping_half_open(intervals))


def erase_overlap_intervals(intervals: Sequence[Interval]) -> int:
    """
    LeetCode 435 — Non-overlapping Intervals.

    Keep as many compatible intervals as possible.
    Remove the rest.

    LeetCode's examples behave like:
        compatible if current_start >= previous_end
    """
    return len(intervals) - max_non_overlapping_half_open(intervals)


# ---------------------------------------------------------------------
# Level 2 — Closed interval stabbing primitive
# ---------------------------------------------------------------------

def min_stabbing_points_closed(intervals: Sequence[Interval]) -> int:
    """
    Minimum number of points needed to stab all closed intervals.

    Primitive:
        sort by end
        place point at current interval's end when current interval is uncovered

    Equivalent to:
        452. Minimum Number of Arrows to Burst Balloons

    Boundary:
        If current_start <= arrow_position, current interval is already stabbed.
        Need new point only when current_start > arrow_position.
    """
    points = 0
    arrow = float("-inf")

    for l, r in sorted_by_end(intervals):
        if l > arrow:
            points += 1
            arrow = r

    return points


def find_min_arrow_shots(points: Sequence[Interval]) -> int:
    """
    LeetCode 452 — Minimum Number of Arrows to Burst Balloons.
    """
    return min_stabbing_points_closed(points)


# ---------------------------------------------------------------------
# Level 3 — Strict pair-chain primitive
# ---------------------------------------------------------------------

def find_longest_chain(pairs: Sequence[Interval]) -> int:
    """
    LeetCode 646 — Maximum Length of Pair Chain.

    Pair chain condition:
        previous_end < current_start

    This is closed/strict compatibility, not half-open meeting compatibility.
    """
    count = 0
    last_end = float("-inf")

    for l, r in sorted_by_end(pairs):
        if l > last_end:
            count += 1
            last_end = r

    return count


# ---------------------------------------------------------------------
# Level 4 — Active interval heap primitive
# ---------------------------------------------------------------------

def min_rooms_half_open(intervals: Sequence[Interval]) -> int:
    """
    Meeting rooms for half-open intervals [start, end).

    Primitive:
        sort by start
        min-heap of active end times

    Reuse condition:
        earliest ending meeting can be reused if earliest_end <= current_start.
    """
    active: list[int] = []

    for l, r in sorted_by_start(intervals):
        if active and active[0] <= l:
            heappop(active)

        heappush(active, r)

    return len(active)


def min_groups_closed(intervals: Sequence[Interval]) -> int:
    """
    LeetCode 2406 — Divide Intervals Into Minimum Number of Groups.

    Closed interval grouping:
        [1, 3] and [3, 5] overlap at 3, so they cannot share a group.

    Reuse condition:
        earliest_end < current_start
    """
    active: list[int] = []

    for l, r in sorted_by_start(intervals):
        if active and active[0] < l:
            heappop(active)

        heappush(active, r)

    return len(active)


# ---------------------------------------------------------------------
# Level 5 — Attend maximum events primitive
# ---------------------------------------------------------------------

def max_events_attended(events: Sequence[Interval]) -> int:
    """
    LeetCode 1353 — Maximum Number of Events That Can Be Attended.

    Primitive:
        process days in increasing order
        add all events starting today
        remove expired events
        attend the event that ends earliest

    Proof:
        exchange argument

    Why earliest-ending active event is safe:
        If we attend a later-ending event instead, the earlier-ending event has
        fewer future chances. Swapping preserves feasibility and cannot hurt.
    """
    events = sorted_by_start(events)
    i = 0
    day = 0
    attended = 0
    active_ends: list[int] = []

    while i < len(events) or active_ends:
        if not active_ends:
            day = max(day, events[i][0])

        while i < len(events) and events[i][0] <= day:
            heappush(active_ends, events[i][1])
            i += 1

        while active_ends and active_ends[0] < day:
            heappop(active_ends)

        if active_ends:
            heappop(active_ends)
            attended += 1
            day += 1

    return attended


# ---------------------------------------------------------------------
# Level 6 — At least two stabbing points per interval
# ---------------------------------------------------------------------

def intersection_size_at_least_two(intervals: Sequence[Interval]) -> int:
    """
    LeetCode 757 — Set Intersection Size At Least Two.

    Problem:
        Choose the smallest set S such that every closed interval [l, r]
        contains at least two points from S.

    Primitive:
        sort by end asc, start desc
        maintain the two largest selected points a < b relevant to current end
        add as few new points as needed, as far right as possible

    Why choose rightmost points?
        They satisfy the current interval and maximize chance of satisfying
        future intervals.
    """
    intervals = sorted(intervals, key=lambda x: (x[1], -x[0]))

    a = b = float("-inf")
    ans = 0

    for l, r in intervals:
        if l > b:
            ans += 2
            a, b = r - 1, r
        elif l > a:
            ans += 1
            a, b = b, r

    return ans


# ---------------------------------------------------------------------
# Level 7 — Latest feasible slot filling
# ---------------------------------------------------------------------

def minimum_time_to_complete_tasks(tasks: Sequence[Task]) -> int:
    """
    LeetCode 2589 — Minimum Time to Complete All Tasks.

    Each task is:
        start, end, duration

    Primitive:
        sort by end
        count already used slots inside [start, end]
        if more slots are needed, fill from end backward

    Proof:
        exchange / latest-slot argument

    Why fill from the right?
        Later slots are less useful to earlier-ending tasks already processed,
        and more likely to help the current/future intervals.
    """
    if not tasks:
        return 0

    max_end = max(r for _, r, _ in tasks)
    used = [False] * (max_end + 1)

    for l, r, duration in sorted(tasks, key=lambda x: x[1]):
        already = sum(used[t] for t in range(l, r + 1))
        need = duration - already

        t = r
        while need > 0:
            if not used[t]:
                used[t] = True
                need -= 1

            t -= 1

    return sum(used)


# ---------------------------------------------------------------------
# Composition summary helpers
# ---------------------------------------------------------------------

def interval_family_map() -> list[dict[str, str]]:
    """
    Compact catalogue for this interval family.
    """
    return [
        {
            "family": "interval scheduling",
            "primitive": "sort by end + take compatible",
            "proof": "exchange",
            "problems": "435, 646",
        },
        {
            "family": "interval stabbing",
            "primitive": "sort by end + place point at end",
            "proof": "exchange",
            "problems": "452",
        },
        {
            "family": "active interval grouping",
            "primitive": "sort by start + min-heap of active ends",
            "proof": "sweep-line resource invariant",
            "problems": "253, 2406",
        },
        {
            "family": "maximum event attendance",
            "primitive": "active end heap + attend earliest-ending event",
            "proof": "exchange",
            "problems": "1353",
        },
        {
            "family": "two-point interval stabbing",
            "primitive": "keep two rightmost selected points",
            "proof": "rightmost dominance",
            "problems": "757",
        },
        {
            "family": "latest feasible slot filling",
            "primitive": "sort by end + fill missing slots from right",
            "proof": "latest-slot exchange",
            "problems": "2589",
        },
    ]


if __name__ == "__main__":
    assert erase_overlap_intervals([(1, 2), (2, 3), (3, 4), (1, 3)]) == 1
    assert find_min_arrow_shots([(10, 16), (2, 8), (1, 6), (7, 12)]) == 2
    assert find_longest_chain([(1, 2), (2, 3), (3, 4)]) == 2
    assert min_rooms_half_open([(0, 30), (5, 10), (15, 20)]) == 2
    assert min_groups_closed([(5, 10), (6, 8), (1, 5), (2, 3), (1, 10)]) == 3
    assert max_events_attended([(1, 2), (2, 3), (3, 4)]) == 3
    assert intersection_size_at_least_two([(1, 3), (1, 4), (2, 5), (3, 5)]) == 3
    assert minimum_time_to_complete_tasks([(2, 3, 1), (4, 5, 1), (1, 5, 2)]) == 2
