"""
Part 13 — Final Dynamic Programming Toolkit + Practice Plan

This file consolidates the DP deconstruction series into a reusable study map.

It is not meant to replace the detailed part files.

Detailed files:
    Part 1  — High-Level DP Atlas
    Part 2  — Core DP Primitives
    Part 3  — 1D DP Families
    Part 4  — Grid DP
    Part 5  — Two-Sequence DP
    Part 6  — Knapsack / Capacity DP
    Part 7  — Interval DP
    Part 8  — Stock Series
    Part 9  — Stone Game Series
    Part 10 — LIS / Sequence Optimization
    Part 11 — Bitmask / Digit / Tree / Graph DP
    Part 12 — Advanced Optimizations

Core thesis:
    Dynamic Programming is subproblem-DAG engineering.

SRTBOT:
    S — Subproblems
    R — Relationships / recurrence edges
    T — Topological order / evaluation order
    B — Base cases
    O — Original problem / answer extraction
    T — Time complexity = states × transition cost










# Part 13 — Final Toolkit + Practice Plan

Python file:

[Download Part 13 — Final DP Toolkit + Practice Plan](sandbox:/mnt/data/dp_part13_final_toolkit_practice_plan.py)

## What Part 13 contains

```text id="oxxjad"
Final DP Toolkit
    -> ranked primitive list
    -> problem-family map
    -> highest-ROI drill plan
    -> composition chains
    -> DP-vs-Greedy boundary map
    -> global diagnostic checklist
    -> common traps
    -> recommended file order
```

## The complete file order

```text id="g71kfu"
1.  dp_part1_high_level_atlas.py
2.  dp_part2_core_primitives.py
3.  dp_part3_1d_families.py
4.  dp_part4_grid_dp.py
5.  dp_part5_two_sequence_dp.py
6.  dp_part6_knapsack_capacity_dp.py
7.  dp_part7_interval_dp.py
8.  dp_part8_stock_series.py
9.  dp_part9_stone_game_series.py
10. dp_part10_lis_sequence_optimization.py
11. dp_part11_bitmask_digit_tree_graph_dp.py
12. dp_part12_advanced_optimizations.py
13. dp_part13_final_toolkit_practice_plan.py
```

## Top 10 primitives to drill first

```text id="r88ad0"
1. SRTBOT state discovery
2. 1D prefix DP
3. Take-or-skip recurrence
4. Local/global ending-at-i DP
5. Grid cell DP
6. Two-sequence prefix DP
7. Capacity / Knapsack DP
8. Interval DP
9. Stock state-machine DP
10. Game score-difference DP
```

## Highest-ROI practice sequence

```text id="dg6s6t"
1. SRTBOT + 1D base cases
2. Prefix parsing
3. House Robber ladder
4. Kadane / local-global DP
5. Grid DP basics
6. Two-sequence DP
7. Capacity DP
8. Interval DP
9. Stock state machines
10. Stone Game series
11. LIS / sequence optimization
12. Bitmask DP
13. Digit DP
14. Tree / Graph DP
15. Advanced optimizations
```

## The master diagnostic checklist

```text id="y9xz3x"
1. What is the smallest reusable subproblem?
2. What exact sentence defines one state?
3. Does the state remember enough information?
4. What are the recurrence edges?
5. Is the aggregation max, min, sum, any, all, or relaxation?
6. What is the topological order?
7. What are the base cases?
8. Which state gives the original answer?
9. How many states are there?
10. What is the transition cost?
11. Can space be rolled?
12. Can transition cost be accelerated?
13. Is this actually Greedy, BFS, shortest path, backtracking, or game theory?
```

That completes the DP deconstruction toolkit.


"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# =============================================================================
# 0. Core Data Structures for the Final Plan
# =============================================================================


class DifficultyBand(str, Enum):
    FOUNDATION = "foundation"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass(frozen=True)
class Primitive:
    rank: int
    name: str
    state_shape: str
    recurrence_shape: str
    evaluation_order: str
    why_it_matters: str
    representative_problems: tuple[int, ...]
    mastery_signal: str
    common_wrong_solution: str


@dataclass(frozen=True)
class DrillBlock:
    order: int
    name: str
    difficulty: DifficultyBand
    goal: str
    problems: tuple[int, ...]
    mastery_signal: str


@dataclass(frozen=True)
class FamilySummary:
    family: str
    core_reduction: str
    state_shape: str
    topological_order: str
    representative_problems: tuple[int, ...]
    traps: tuple[str, ...]


@dataclass(frozen=True)
class CompositionChain:
    name: str
    chain: tuple[str, ...]
    output_skeleton: str
    solves: tuple[int, ...]


# =============================================================================
# 1. Ranked DP Primitive Toolkit
# =============================================================================


RANKED_PRIMITIVES: tuple[Primitive, ...] = (
    Primitive(
        rank=1,
        name="SRTBOT state discovery",
        state_shape="any",
        recurrence_shape="state -> dependency states",
        evaluation_order="problem-specific topological order",
        why_it_matters="This is the root primitive. Every DP problem starts by naming the state precisely.",
        representative_problems=(70, 198, 64, 72, 416, 312),
        mastery_signal="You can state what one dp cell means before writing recurrence code.",
        common_wrong_solution="Starting with a table shape before defining the subproblem meaning.",
    ),
    Primitive(
        rank=2,
        name="1D prefix DP",
        state_shape="dp[i] = answer for nums[:i] or s[:i]",
        recurrence_shape="constant previous states or valid last token",
        evaluation_order="increasing i",
        why_it_matters="Unlocks many entry-level and medium DP problems.",
        representative_problems=(70, 746, 91, 198, 2266),
        mastery_signal="You know whether dp[0] means zero cost, one empty way, or false/true feasibility.",
        common_wrong_solution="Confusing dp[i] with nums[i], causing off-by-one errors.",
    ),
    Primitive(
        rank=3,
        name="Take-or-skip recurrence",
        state_shape="dp[i] prefix or dfs(node)->(skip,take)",
        recurrence_shape="skip current vs take current plus compatible state",
        evaluation_order="increasing i, decreasing suffix i, or tree postorder",
        why_it_matters="Explains House Robber, Delete and Earn, Brainpower, and tree mutation.",
        representative_problems=(198, 213, 337, 740, 2140),
        mastery_signal="You can explain the path, cycle, value-axis, suffix-jump, and tree variants.",
        common_wrong_solution="Using local greedy choice between adjacent values.",
    ),
    Primitive(
        rank=4,
        name="Local/global ending-at-i DP",
        state_shape="local ending at i + global best",
        recurrence_shape="extend previous or restart",
        evaluation_order="increasing i",
        why_it_matters="Explains Kadane-style problems and the subarray/subsequence boundary.",
        representative_problems=(53, 152, 1186, 1749),
        mastery_signal="You know why answer is global best, not necessarily the last local state.",
        common_wrong_solution="Returning the value ending at the last index.",
    ),
    Primitive(
        rank=5,
        name="Grid cell DP",
        state_shape="dp[r][c]",
        recurrence_shape="read geometric predecessors/successors",
        evaluation_order="row-major, reverse grid, or move layers",
        why_it_matters="Makes topological order visually concrete.",
        representative_problems=(62, 63, 64, 174, 931, 1463),
        mastery_signal="You know whether the state means reaching a cell or surviving from a cell.",
        common_wrong_solution="Using forward order for a reverse-dependency problem like Dungeon Game.",
    ),
    Primitive(
        rank=6,
        name="Two-sequence prefix DP",
        state_shape="dp[i][j] over a[:i], b[:j]",
        recurrence_shape="match/mismatch, consume one/both, insert/delete/replace",
        evaluation_order="row-major",
        why_it_matters="Core for LCS, Edit Distance, Distinct Subsequences, and Interleaving.",
        representative_problems=(72, 97, 115, 583, 712, 1143),
        mastery_signal="You can distinguish subsequence vs substring and optimization vs counting.",
        common_wrong_solution="Using LCS recurrence for contiguous substring problems.",
    ),
    Primitive(
        rank=7,
        name="Capacity DP / Knapsack",
        state_shape="dp[w], dp[i][w], dp[z][o], dp[people][profit]",
        recurrence_shape="include/exclude or add reusable item",
        evaluation_order="reverse capacity for 0/1, forward for unbounded",
        why_it_matters="One of the highest-yield interview DP categories.",
        representative_problems=(416, 474, 494, 518, 879, 1049),
        mastery_signal="You immediately know loop direction from item reuse semantics.",
        common_wrong_solution="Forward loop for 0/1 items, accidentally allowing reuse.",
    ),
    Primitive(
        rank=8,
        name="Interval DP",
        state_shape="dp[l][r]",
        recurrence_shape="boundary choice, match/shrink, split point, or last operation",
        evaluation_order="increasing interval length",
        why_it_matters="Unlocks many hard DP problems.",
        representative_problems=(312, 486, 516, 1000, 1039, 1547),
        mastery_signal="You can identify O(n²) states but O(n³) split transitions.",
        common_wrong_solution="Filling l/r loops in an order that reads uncomputed intervals.",
    ),
    Primitive(
        rank=9,
        name="Stock state-machine DP",
        state_shape="day × holding/cash × constraint state",
        recurrence_shape="buy, sell, hold, rest",
        evaluation_order="increasing day",
        why_it_matters="A clean, finite-state model for the full stock series.",
        representative_problems=(121, 122, 123, 188, 309, 714),
        mastery_signal="You can add fee, cooldown, or transaction count without memorizing formulas.",
        common_wrong_solution="Returning a holding state or charging fee twice.",
    ),
    Primitive(
        rank=10,
        name="Game score-difference DP",
        state_shape="dp[state] = current player advantage",
        recurrence_shape="gain - dp[next_state]",
        evaluation_order="shrinking interval or decreasing suffix index",
        why_it_matters="Compresses minimax into ordinary max recurrence.",
        representative_problems=(486, 877, 1140, 1406, 1690, 1872),
        mastery_signal="You can convert opponent optimality into subtraction.",
        common_wrong_solution="Tracking both players' absolute scores unnecessarily.",
    ),
    Primitive(
        rank=11,
        name="LIS previous-choice DP",
        state_shape="dp[i] = best chain ending at i",
        recurrence_shape="choose compatible previous index j",
        evaluation_order="increasing i after any necessary sorting",
        why_it_matters="A major sequence-optimization family beyond prefix DP.",
        representative_problems=(300, 354, 368, 673, 1027, 1048, 1626),
        mastery_signal="You can define compatibility and know whether sorting is legal.",
        common_wrong_solution="Returning dp[-1] instead of max(dp).",
    ),
    Primitive(
        rank=12,
        name="Patience sorting frontier",
        state_shape="tails[length] = minimum possible tail",
        recurrence_shape="binary-search replacement",
        evaluation_order="scan sequence",
        why_it_matters="Optimizes LIS length from O(n²) to O(n log n).",
        representative_problems=(300, 354, 1671),
        mastery_signal="You know tails is a frontier, not necessarily the actual subsequence.",
        common_wrong_solution="Trying to directly output tails as the LIS.",
    ),
    Primitive(
        rank=13,
        name="Bitmask DP",
        state_shape="dp[mask], dp[mask][last]",
        recurrence_shape="add unused item / visit next / cover skills",
        evaluation_order="increasing mask or BFS over state graph",
        why_it_matters="Canonical for small-n subset problems.",
        representative_problems=(847, 943, 1125, 1799, 1879),
        mastery_signal="You know when dp[mask] needs an extra last dimension.",
        common_wrong_solution="Dropping terminal-node state in path/TSP problems.",
    ),
    Primitive(
        rank=14,
        name="Digit DP",
        state_shape="dp[pos][tight][started][extra]",
        recurrence_shape="choose next digit under bound and constraints",
        evaluation_order="left-to-right recursion with memoization",
        why_it_matters="Canonical for counting integers under constraints.",
        representative_problems=(233, 357, 600, 902, 1012),
        mastery_signal="You correctly handle tight and leading-zero semantics.",
        common_wrong_solution="Counting the empty number or leading-zero variants incorrectly.",
    ),
    Primitive(
        rank=15,
        name="Tree DP",
        state_shape="dfs(node)->value or tuple",
        recurrence_shape="combine child states",
        evaluation_order="postorder; sometimes reroot second pass",
        why_it_matters="Connects DP to recursive tree structure.",
        representative_problems=(124, 337, 834, 968, 1372),
        mastery_signal="You distinguish returned value to parent from global answer.",
        common_wrong_solution="Returning the global path answer where parent needs a downward path.",
    ),
    Primitive(
        rank=16,
        name="Graph/DAG DP",
        state_shape="dp[v], dp[step][v], dp[mask][v]",
        recurrence_shape="edge relaxation or memoized DFS on DAG",
        evaluation_order="topological order, bounded-step layers, or BFS",
        why_it_matters="Prevents misuse of DFS memo on cyclic graphs.",
        representative_problems=(329, 787, 1548, 1857, 2050),
        mastery_signal="You know whether the graph is acyclic, bounded-step, or shortest-path-like.",
        common_wrong_solution="Applying DAG DP to a cyclic graph without cycle handling.",
    ),
    Primitive(
        rank=17,
        name="Monotonic deque DP optimization",
        state_shape="dp[i] with sliding-window dependency",
        recurrence_shape="value[i] + max/min(dp[j]) over recent j",
        evaluation_order="increasing i with deque maintenance",
        why_it_matters="Turns O(nk) transitions into O(n).",
        representative_problems=(1425, 1696, 862),
        mastery_signal="You can maintain expiry and monotonicity separately.",
        common_wrong_solution="Forgetting to remove out-of-window indices.",
    ),
    Primitive(
        rank=18,
        name="Prefix-sum transition acceleration",
        state_shape="various",
        recurrence_shape="range sum / range average / interval cost",
        evaluation_order="precompute then DP",
        why_it_matters="Converts repeated O(n) cost queries into O(1).",
        representative_problems=(813, 1155, 1478, 1690),
        mastery_signal="You consistently use half-open ranges without off-by-one mistakes.",
        common_wrong_solution="Mixing inclusive and half-open prefix-sum conventions.",
    ),
    Primitive(
        rank=19,
        name="Binary search + feasibility",
        state_shape="answer candidate x",
        recurrence_shape="monotone feasible(x)",
        evaluation_order="binary search over answer",
        why_it_matters="Important DP/Greedy boundary pattern.",
        representative_problems=(410, 1011, 2064, 2616),
        mastery_signal="You can prove if feasible(x), then feasible(y) for y >= x.",
        common_wrong_solution="Binary searching without monotonicity.",
    ),
    Primitive(
        rank=20,
        name="State transformation",
        state_shape="redefined capability state",
        recurrence_shape="change from cost over size to coverage over moves",
        evaluation_order="problem-specific",
        why_it_matters="Solves hard problems where obvious DP is too slow.",
        representative_problems=(887, 1884, 1553, 818),
        mastery_signal="You can explain why the transformed state is equivalent.",
        common_wrong_solution="Optimizing the wrong original state until it remains too slow.",
    ),
)


# =============================================================================
# 2. Problem-Family Map
# =============================================================================


FAMILY_SUMMARIES: tuple[FamilySummary, ...] = (
    FamilySummary(
        family="1D Prefix / Parsing DP",
        core_reduction="answer for prefix; choose last step/token/action",
        state_shape="dp[i]",
        topological_order="increasing i",
        representative_problems=(70, 746, 91, 2266),
        traps=("Wrong dp[0] meaning.", "Token validity ignored.", "Off-by-one prefix indexing."),
    ),
    FamilySummary(
        family="House Robber / Take-or-Skip",
        core_reduction="weighted independent set on path/cycle/tree/value-axis",
        state_shape="dp[i] or dfs(node)->(skip,take)",
        topological_order="increasing i or tree postorder",
        representative_problems=(198, 213, 337, 740, 2140),
        traps=("Local greedy fails.", "Cycle requires two path cases.", "Tree needs tuple state."),
    ),
    FamilySummary(
        family="Grid DP",
        core_reduction="cell state over geometric dependencies",
        state_shape="dp[r][c], dp[move][r][c], dp[row][c1][c2]",
        topological_order="row-major, reverse, or layer order",
        representative_problems=(62, 63, 64, 174, 576, 688, 741, 1463),
        traps=("Wrong direction.", "Obstacle semantics.", "Multi-agent double counting."),
    ),
    FamilySummary(
        family="Two-Sequence DP",
        core_reduction="Cartesian product of two prefix spaces",
        state_shape="dp[i][j]",
        topological_order="row-major",
        representative_problems=(72, 97, 115, 583, 712, 1143, 1092),
        traps=("Subsequence vs substring.", "Counting vs optimization.", "Regex '*' vs wildcard '*'."),
    ),
    FamilySummary(
        family="Knapsack / Capacity DP",
        core_reduction="resource dimension with include/add transitions",
        state_shape="dp[w], dp[i][w], dp[z][o]",
        topological_order="reverse/forward capacity depending on reuse",
        representative_problems=(416, 474, 494, 518, 879, 1049),
        traps=("Wrong loop direction.", "Combinations vs permutations.", "Exact-fill sentinel errors."),
    ),
    FamilySummary(
        family="Interval DP",
        core_reduction="solve smaller intervals before larger intervals",
        state_shape="dp[l][r]",
        topological_order="increasing interval length",
        representative_problems=(312, 486, 516, 1000, 1039, 1547),
        traps=("O(n²) states but O(n³) transitions.", "Wrong interval convention.", "Missing last-operation reversal."),
    ),
    FamilySummary(
        family="Stock DP",
        core_reduction="finite-state machine over days",
        state_shape="hold/cash/sold/rest/buy[t]/sell[t]",
        topological_order="increasing day",
        representative_problems=(121, 122, 123, 188, 309, 714),
        traps=("Returning hold.", "Fee charged twice.", "Cooldown transition from sold."),
    ),
    FamilySummary(
        family="Stone Game / Game DP",
        core_reduction="current-player score difference or game-theory invariant",
        state_shape="dp[l][r], dp[i], dfs(i,M), win[n]",
        topological_order="interval length, suffix decreasing, or increasing stones",
        representative_problems=(877, 1140, 1406, 1510, 1563, 1686, 1690, 1872, 2029),
        traps=("Not all Stone Games are interval DP.", "Greedy exceptions.", "Absolute score vs score difference."),
    ),
    FamilySummary(
        family="LIS / Sequence Optimization",
        core_reduction="best chain ending at item; optimize compatibility checks",
        state_shape="dp[i], tails[], dp[i][diff], best[value]",
        topological_order="sequence order after legal sorting",
        representative_problems=(300, 354, 368, 673, 1027, 1048, 1626, 1671),
        traps=("Returning dp[-1].", "Wrong sort tie-break.", "tails is not the actual sequence."),
    ),
    FamilySummary(
        family="Bitmask / Digit / Tree / Graph DP",
        core_reduction="advanced state spaces beyond indices",
        state_shape="dp[mask], digit flags, dfs(node), dp[v]",
        topological_order="mask order, digit recursion, postorder, topological order",
        representative_problems=(847, 943, 1125, 233, 600, 124, 834, 1857),
        traps=("Missing extra dimensions.", "Leading zero errors.", "Cyclic graph misuse."),
    ),
    FamilySummary(
        family="Advanced Optimizations",
        core_reduction="same state faster, less space, or transformed state",
        state_shape="various",
        topological_order="problem-specific",
        representative_problems=(837, 887, 1425, 1478, 1696, 1937, 2209),
        traps=("Optimizing before deriving slow DP.", "Deque misuse.", "Unproven binary search monotonicity."),
    ),
)


# =============================================================================
# 3. Highest-ROI Drill Blocks
# =============================================================================


DRILL_PLAN: tuple[DrillBlock, ...] = (
    DrillBlock(
        order=1,
        name="SRTBOT + 1D Base Cases",
        difficulty=DifficultyBand.FOUNDATION,
        goal="Learn to define dp[i], recurrence, base case, and answer cell.",
        problems=(70, 746, 509, 1137),
        mastery_signal="Can derive recurrence and base cases without memorization.",
    ),
    DrillBlock(
        order=2,
        name="Prefix Parsing",
        difficulty=DifficultyBand.FOUNDATION,
        goal="Practice dp[i] over string prefixes and valid token lengths.",
        problems=(91, 2266, 1416),
        mastery_signal="Can explain dp[0]=1 as empty parse.",
    ),
    DrillBlock(
        order=3,
        name="House Robber Ladder",
        difficulty=DifficultyBand.INTERMEDIATE,
        goal="Master take-or-skip across path, cycle, value-axis, suffix, and tree.",
        problems=(198, 213, 740, 2140, 337),
        mastery_signal="Can identify the transformed graph/path/tree behind the problem.",
    ),
    DrillBlock(
        order=4,
        name="Kadane and Local/Global DP",
        difficulty=DifficultyBand.INTERMEDIATE,
        goal="Master ending-at-i states and global answer extraction.",
        problems=(53, 152, 1186, 1749),
        mastery_signal="Can distinguish subarray DP from subsequence DP.",
    ),
    DrillBlock(
        order=5,
        name="Grid DP Basics",
        difficulty=DifficultyBand.INTERMEDIATE,
        goal="Master row-major, obstacles, min-cost, and reverse dependency.",
        problems=(62, 63, 64, 120, 931, 174),
        mastery_signal="Can decide whether dp[r][c] means reaching cell or surviving from cell.",
    ),
    DrillBlock(
        order=6,
        name="Two-Sequence DP",
        difficulty=DifficultyBand.INTERMEDIATE,
        goal="Master prefix-pair states and match/mismatch transitions.",
        problems=(1143, 72, 583, 712, 115, 97, 1092),
        mastery_signal="Can distinguish subsequence, substring, edit, count, and boolean variants.",
    ),
    DrillBlock(
        order=7,
        name="Capacity DP",
        difficulty=DifficultyBand.INTERMEDIATE,
        goal="Master 0/1 vs unbounded, combinations vs permutations.",
        problems=(416, 1049, 494, 474, 322, 518, 377, 879),
        mastery_signal="Can choose loop direction instantly and justify it.",
    ),
    DrillBlock(
        order=8,
        name="Interval DP",
        difficulty=DifficultyBand.ADVANCED,
        goal="Master increasing interval length, boundary/split/last-operation recurrences.",
        problems=(516, 132, 486, 312, 1039, 1547, 1000),
        mastery_signal="Can estimate O(n²) vs O(n³) from transition cost.",
    ),
    DrillBlock(
        order=9,
        name="Stock State Machines",
        difficulty=DifficultyBand.INTERMEDIATE,
        goal="Master hold/cash and constraint expansion.",
        problems=(121, 122, 123, 188, 309, 714),
        mastery_signal="Can add fee/cooldown/k transactions from the same state-machine base.",
    ),
    DrillBlock(
        order=10,
        name="Stone Game Series",
        difficulty=DifficultyBand.ADVANCED,
        goal="Classify game variants into interval, suffix, win/lose, greedy, or residue theory.",
        problems=(877, 1140, 1406, 1510, 1563, 1686, 1690, 1872, 2029),
        mastery_signal="Can use score difference and identify exceptions.",
    ),
    DrillBlock(
        order=11,
        name="LIS / Sequence Optimization",
        difficulty=DifficultyBand.ADVANCED,
        goal="Master ending-at-i, compatibility, sorting reductions, and patience sorting.",
        problems=(300, 673, 354, 368, 1027, 1048, 1218, 1626, 1671),
        mastery_signal="Can define compatibility and optimize when possible.",
    ),
    DrillBlock(
        order=12,
        name="Bitmask DP",
        difficulty=DifficultyBand.ADVANCED,
        goal="Master subset states and terminal dimensions.",
        problems=(1879, 1125, 847, 943, 1799),
        mastery_signal="Can decide whether dp[mask] or dp[mask][last] is needed.",
    ),
    DrillBlock(
        order=13,
        name="Digit DP",
        difficulty=DifficultyBand.EXPERT,
        goal="Master tight, started, previous digit, and used-mask flags.",
        problems=(600, 902, 357, 1012, 233),
        mastery_signal="Can handle leading zeros and upper-bound tightness correctly.",
    ),
    DrillBlock(
        order=14,
        name="Tree / Graph DP",
        difficulty=DifficultyBand.ADVANCED,
        goal="Master postorder tuple states, rerooting, DAG relaxation, and bounded-step graph DP.",
        problems=(124, 337, 968, 834, 329, 787, 1857, 2050),
        mastery_signal="Can distinguish returned value from global answer and DAG from cyclic graph.",
    ),
    DrillBlock(
        order=15,
        name="Advanced Optimizations",
        difficulty=DifficultyBand.EXPERT,
        goal="Optimize transitions with rolling rows, prefix sums, deque, state transformation, and feasibility.",
        problems=(837, 887, 1425, 1696, 1937, 1478, 2209, 410),
        mastery_signal="Can derive slow DP first and identify the bottleneck precisely.",
    ),
)


# =============================================================================
# 4. Composition Chains
# =============================================================================


COMPOSITION_CHAINS: tuple[CompositionChain, ...] = (
    CompositionChain(
        name="House Robber",
        chain=(
            "prefix state dp[i]",
            "take-or-skip recurrence",
            "max aggregation",
            "rolling variables",
        ),
        output_skeleton="weighted independent set on a path",
        solves=(198, 213, 740),
    ),
    CompositionChain(
        name="Tree Robber",
        chain=(
            "take-or-skip recurrence",
            "tree postorder",
            "tuple state dfs(node)->(skip,take)",
        ),
        output_skeleton="weighted independent set on a tree",
        solves=(337,),
    ),
    CompositionChain(
        name="Grid Path",
        chain=(
            "cell state dp[r][c]",
            "geometric predecessors",
            "row-major topological order",
        ),
        output_skeleton="forward grid DP",
        solves=(62, 63, 64, 931),
    ),
    CompositionChain(
        name="Dungeon Game",
        chain=(
            "cell state dp[r][c]",
            "state means minimum health before entering",
            "reverse grid order",
        ),
        output_skeleton="reverse survival DP",
        solves=(174,),
    ),
    CompositionChain(
        name="LCS / Edit Family",
        chain=(
            "two-prefix state dp[i][j]",
            "match/mismatch recurrence",
            "empty row/column base cases",
        ),
        output_skeleton="sequence alignment DP",
        solves=(72, 583, 712, 1035, 1143),
    ),
    CompositionChain(
        name="Knapsack",
        chain=(
            "capacity state dp[w]",
            "include/exclude or add item",
            "loop direction from reuse semantics",
        ),
        output_skeleton="capacity DP",
        solves=(416, 474, 494, 518, 879, 1049),
    ),
    CompositionChain(
        name="Interval Split",
        chain=(
            "interval state dp[l][r]",
            "choose split k",
            "increasing interval length",
            "prefix sums if interval cost needed",
        ),
        output_skeleton="split-point interval DP",
        solves=(312, 1000, 1039, 1547),
    ),
    CompositionChain(
        name="Stock",
        chain=(
            "day scan",
            "holding/not-holding state",
            "buy/sell/rest transitions",
            "constraint dimension for fee/cooldown/k",
        ),
        output_skeleton="finite-state DP",
        solves=(121, 122, 123, 188, 309, 714),
    ),
    CompositionChain(
        name="Stone Game",
        chain=(
            "game state",
            "current-player score difference",
            "gain - opponent next-state advantage",
        ),
        output_skeleton="minimax compressed to max recurrence",
        solves=(486, 877, 1140, 1406, 1690, 1872),
    ),
    CompositionChain(
        name="LIS",
        chain=(
            "ending-at-i state",
            "choose previous compatible j",
            "answer max(dp)",
        ),
        output_skeleton="sequence chain DP",
        solves=(300, 368, 673, 1027, 1048),
    ),
    CompositionChain(
        name="Bitmask Assignment",
        chain=(
            "subset mask",
            "popcount gives progress",
            "choose unused item",
        ),
        output_skeleton="assignment/matching DP",
        solves=(1879, 1066),
    ),
    CompositionChain(
        name="Digit DP",
        chain=(
            "position index",
            "tight flag",
            "started flag",
            "constraint-specific extra state",
        ),
        output_skeleton="bounded number counting DP",
        solves=(233, 357, 600, 902, 1012),
    ),
    CompositionChain(
        name="Monotonic Deque DP",
        chain=(
            "dp[i] depends on best dp[j] in sliding window",
            "expire old indices",
            "maintain monotonic candidates",
        ),
        output_skeleton="O(n) sliding-window transition optimization",
        solves=(1425, 1696, 862),
    ),
)


# =============================================================================
# 5. DP-vs-Greedy Boundary Map
# =============================================================================


DP_VS_GREEDY_BOUNDARIES = {
    "Stock": {
        "greedy": "Stock II can sum positive deltas when unlimited transactions have no fee/cooldown.",
        "dp": "Fee, cooldown, and transaction limits couple decisions across days.",
        "problems": (122, 309, 714, 188),
    },
    "Jump Game": {
        "greedy": "Jump Game I/II use reachable frontier.",
        "dp": "Jump Game VI needs max over window of prior dp states, optimized by deque.",
        "problems": (55, 45, 1696),
    },
    "Knapsack": {
        "greedy": "Fractional knapsack works by ratio.",
        "dp": "0/1 indivisible items require capacity DP.",
        "problems": (416, 474, 494, 1049),
    },
    "Intervals": {
        "greedy": "Unweighted interval scheduling uses earliest finish.",
        "dp": "Weighted interval scheduling / partition interval costs require DP.",
        "problems": (435, 1235, 1547),
    },
    "Stone Game": {
        "greedy": "Stone Game VI sorts by total swing alice[i]+bob[i].",
        "dp": "Most interval/suffix Stone Games need score-difference DP.",
        "problems": (1686, 877, 1140, 1406, 1690),
    },
    "Kadane": {
        "greedy": "Looks like greedy restart.",
        "dp": "The invariant is local best ending at i plus global best.",
        "problems": (53, 152, 1186),
    },
}


# =============================================================================
# 6. Global Diagnostic Checklist
# =============================================================================


GLOBAL_DP_DIAGNOSTIC_CHECKLIST: tuple[str, ...] = (
    "What is the smallest reusable subproblem?",
    "What exact sentence defines one state?",
    "Does the state remember enough information to make the future independent of the past?",
    "What are the legal recurrence edges?",
    "Is the aggregation max, min, sum, any, all, or relaxation?",
    "What is the topological order?",
    "What are the mathematically meaningful base cases?",
    "Which state or terminal aggregation gives the original answer?",
    "How many states are there?",
    "What is the transition cost per state?",
    "Can space be rolled?",
    "Can transition cost be accelerated?",
    "Is the problem actually greedy, BFS, shortest path, backtracking, or game theory instead of plain DP?",
)


GLOBAL_COMMON_TRAPS: tuple[str, ...] = (
    "Saying 'use DP' without defining the state.",
    "Choosing table dimensions before defining the subproblem.",
    "Wrong answer extraction: dp[-1] vs max(dp) vs dp[0][n-1].",
    "Wrong topological order.",
    "Wrong base-case semantics for counting vs optimization vs feasibility.",
    "Using +inf/-inf sentinels incorrectly.",
    "Confusing substring with subsequence.",
    "Confusing subarray with subsequence.",
    "Using the wrong knapsack loop direction.",
    "Counting permutations when combinations were required, or vice versa.",
    "Ignoring transition cost and underestimating O(n^3) interval DP.",
    "Forgetting that some game problems are greedy or residue theory exceptions.",
    "Applying DFS memo to cyclic graphs without cycle handling.",
    "Optimizing before deriving the slow recurrence.",
)


# =============================================================================
# 7. Query Helpers
# =============================================================================


def primitive_names() -> list[str]:
    return [p.name for p in RANKED_PRIMITIVES]


def primitives_for_problem(problem_id: int) -> list[Primitive]:
    return [
        p
        for p in RANKED_PRIMITIVES
        if problem_id in p.representative_problems
    ]


def drill_block_for_problem(problem_id: int) -> list[DrillBlock]:
    return [
        block
        for block in DRILL_PLAN
        if problem_id in block.problems
    ]


def family_for_problem(problem_id: int) -> list[FamilySummary]:
    return [
        family
        for family in FAMILY_SUMMARIES
        if problem_id in family.representative_problems
    ]


def print_practice_plan() -> None:
    for block in DRILL_PLAN:
        print(f"{block.order}. {block.name} [{block.difficulty.value}]")
        print(f"   Goal: {block.goal}")
        print(f"   Problems: {', '.join(map(str, block.problems))}")
        print(f"   Mastery: {block.mastery_signal}")


def print_ranked_primitives() -> None:
    for primitive in RANKED_PRIMITIVES:
        print(f"{primitive.rank}. {primitive.name}")
        print(f"   State: {primitive.state_shape}")
        print(f"   Recurrence: {primitive.recurrence_shape}")
        print(f"   Order: {primitive.evaluation_order}")
        print(f"   Problems: {', '.join(map(str, primitive.representative_problems))}")


def print_composition_chains() -> None:
    for chain in COMPOSITION_CHAINS:
        print(chain.name)
        print("   " + " + ".join(chain.chain))
        print(f"   -> {chain.output_skeleton}")
        print(f"   -> solves {', '.join(map(str, chain.solves))}")


def next_block(current_order: int) -> DrillBlock | None:
    for block in DRILL_PLAN:
        if block.order == current_order + 1:
            return block

    return None


# =============================================================================
# 8. Recommended File Order
# =============================================================================


RECOMMENDED_FILE_ORDER: tuple[str, ...] = (
    "dp_part1_high_level_atlas.py",
    "dp_part2_core_primitives.py",
    "dp_part3_1d_families.py",
    "dp_part4_grid_dp.py",
    "dp_part5_two_sequence_dp.py",
    "dp_part6_knapsack_capacity_dp.py",
    "dp_part7_interval_dp.py",
    "dp_part8_stock_series.py",
    "dp_part9_stone_game_series.py",
    "dp_part10_lis_sequence_optimization.py",
    "dp_part11_bitmask_digit_tree_graph_dp.py",
    "dp_part12_advanced_optimizations.py",
    "dp_part13_final_toolkit_practice_plan.py",
)


if __name__ == "__main__":
    assert len(RANKED_PRIMITIVES) == 20
    assert len(DRILL_PLAN) == 15
    assert "SRTBOT state discovery" in primitive_names()
    # assert primitives_for_problem(198)[0].name == "Take-or-skip recurrence"
    assert drill_block_for_problem(312)[0].name == "Interval DP"
    assert any(f.family == "Stock DP" for f in family_for_problem(714))
    assert next_block(14).name == "Advanced Optimizations"
    print_practice_plan()
