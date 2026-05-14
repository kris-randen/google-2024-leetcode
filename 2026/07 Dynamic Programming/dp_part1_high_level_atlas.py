"""
Part 1 — Dynamic Programming High-Level Atlas

This file is not a solution file.

It is a structured map of the DP universe:
    family taxonomy
    state-shape taxonomy
    SRTBOT cards
    composition chains
    recommended expansion order

Use this as the index layer before drilling the concrete primitive files:
    Part 2 — Core DP Primitives
    Part 3 — 1D DP Families
    Part 4 — Grid DP
    ...



Here’s the full roadmap we’re following.

## Part 0 — Catalogue + Atlas

Purpose: create the map before drilling.

Outputs:

```text
leetcode_dp_problem_catalog.csv
leetcode_dp_family_summary.csv
dp_high_level_atlas.md
dp_primitives_templates.py
```

This is the 651-problem classification layer.

---

## Part 1 — High-Level DP Atlas

Purpose: understand the whole DP universe.

Covers:

```text
1D DP
Grid DP
Two-sequence DP
Knapsack / capacity DP
Interval DP
Stock DP
Stone Game / minimax DP
LIS / sequence optimization
Bitmask DP
Digit DP
Tree DP
Graph/DAG DP
Advanced optimized DP
DP-vs-Greedy boundaries
```

---

## Part 2 — Core DP Primitives

Purpose: build the reusable vocabulary.

Covers:

```text
state
recurrence
aggregation operator
sentinel / neutral value
topological order
base case
answer extraction
complexity = states × transition cost
```

This is the “DP grammar.”

Python file:

```text
dp_part2_core_primitives.py
```

---

## Part 3 — 1D DP Families

Purpose: first real family.

Covers:

```text
Fibonacci / stair-step
Decode Ways / prefix parsing
House Robber I
House Robber II
Delete and Earn
House Robber III
Suffix jump DP
Kadane / local-global DP
Tiny state-machine DP
```

Python file:

```text
dp_part3_1d_families.py
```

---

## Part 4 — Grid DP

Purpose: move from `dp[i]` to `dp[r][c]`.

Will cover:

```text
Unique Paths
Unique Paths II
Minimum Path Sum
Triangle
Minimum Falling Path Sum
Dungeon Game
Out of Boundary Paths
Knight Probability
Cherry Pickup I
Cherry Pickup II
Paths With Max Score
```

Main primitives:

```text
cell state
row-major order
reverse grid order
rolling row
multi-agent grid state
probability distribution over grid
```

---

## Part 5 — Two-Sequence DP

Purpose: alignment-style DP.

Will cover:

```text
LCS
Edit Distance
Delete Operation for Two Strings
Minimum ASCII Delete Sum
Distinct Subsequences
Interleaving String
Uncrossed Lines
Shortest Common Supersequence
Longest Repeated Subarray
Minimum Window Subsequence
```

Main primitive:

```text
dp[i][j] = answer for a[:i], b[:j]
```

---

## Part 6 — Knapsack / Capacity DP

Purpose: understand pseudo-polynomial DP.

Will cover:

```text
Subset Sum
Partition Equal Subset Sum
Target Sum
Last Stone Weight II
0/1 Knapsack
Unbounded Knapsack
Coin Change
Coin Change II
Combination Sum IV
Ones and Zeroes
Profitable Schemes
```

Most important trap:

```text
0/1 knapsack       -> reverse capacity loop
unbounded knapsack -> forward capacity loop
combinations       -> item outer loop
permutations       -> target outer loop
```

---

## Part 7 — Interval DP

Purpose: `dp[l][r]`.

Will cover:

```text
Longest Palindromic Subsequence
Palindrome Partitioning variants
Predict the Winner
Burst Balloons
Minimum Score Triangulation
Minimum Cost to Cut a Stick
Minimum Cost to Merge Stones
Strange Printer
Remove Boxes
```

Main primitives:

```text
choose boundary
choose split point
increasing interval length
prefix sums for interval cost
score-difference game state
```

---

## Part 8 — Stock Series

Purpose: fully deconstruct stock DP.

Will cover:

```text
121. Stock I
122. Stock II
123. Stock III
188. Stock IV
309. Cooldown
714. Transaction Fee
```

Main primitive:

```text
day × holding-status × transaction/cooldown/fee state
```

Evolution:

```text
one transaction
-> unlimited transactions
-> at most two
-> at most k
-> cooldown
-> fee
```

---

## Part 9 — Stone Game Series

Purpose: fully deconstruct game DP.

Will cover:

```text
Stone Game I
Stone Game II
Stone Game III
Stone Game IV
Stone Game V
Stone Game VI
Stone Game VII
Stone Game VIII
Stone Game IX
```

Main categories:

```text
interval minimax DP
score-difference DP
suffix/prefix-sum game DP
take-k game DP
game theory / greedy exceptions
```

---

## Part 10 — LIS / Sequence Optimization

Purpose: sequence DP beyond simple prefix.

Will cover:

```text
LIS O(n²)
LIS O(n log n)
Number of LIS
Russian Doll Envelopes
Largest Divisible Subset
Longest Arithmetic Subsequence
Longest Fibonacci-like Subsequence
Longest String Chain
Best Team With No Conflicts
```

Main primitives:

```text
dp[i] = best ending at i
choose previous index
patience sorting tails[]
coordinate/order reduction
```

---

## Part 11 — Bitmask / Digit / Tree / Graph DP

Purpose: advanced state shapes.

Covers:

```text
Bitmask DP:
    assignment
    shortest path visiting all nodes
    smallest sufficient team
    TSP-like DP

Digit DP:
    tight flag
    started flag
    previous digit constraints

Tree DP:
    postorder tuple states
    rerooting DP
    subtree combine

Graph/DAG DP:
    longest path in DAG
    shortest-path-like DP
    bounded-step graph DP
```

---

## Part 12 — Advanced Optimizations

Purpose: making slow DP fast.

Covers:

```text
rolling arrays
prefix-sum acceleration
monotonic deque optimization
binary-search optimization / LIS
state compression
sparse memoization
convexity / divide-and-conquer optimization, if useful
Knuth-style optimization, if useful
```

Representative problems:

```text
1425. Constrained Subsequence Sum
1696. Jump Game VI
887. Super Egg Drop
410. Split Array Largest Sum
1478. Allocate Mailboxes
```

---

## Part 13 — Final Toolkit + Practice Plan

Purpose: consolidate everything.

Outputs:

```text
final ranked primitive list
family map
problem ladder
study order
drill plan
code template file
common traps
DP-vs-Greedy boundary map
```

The next part is **Part 4 — Grid DP**.


"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


# =============================================================================
# Core Taxonomy
# =============================================================================


class StateShape(str, Enum):
    INDEX = "dp[i]"
    PREFIX = "dp[i] over nums[:i]"
    SUFFIX = "dp[i] over nums[i:]"
    ENDING_AT_INDEX = "dp[i] = best ending exactly at i"
    GRID_CELL = "dp[r][c]"
    TWO_SEQUENCE = "dp[i][j] over a[:i], b[:j]"
    INTERVAL = "dp[l][r]"
    CAPACITY = "dp[w] or dp[i][w]"
    STATE_MACHINE = "dp[i][state]"
    BITMASK = "dp[mask]"
    DIGIT = "dp[pos][tight][started][...]"
    TREE_TUPLE = "dfs(node) -> tuple"
    DAG_VERTEX = "dp[v]"
    PROBABILITY = "distribution over state space"


class Aggregation(str, Enum):
    MAX = "max"
    MIN = "min"
    SUM = "sum"
    ANY = "any / boolean OR"
    ALL = "all / boolean AND"
    RELAX = "edge relaxation"


class EvaluationOrder(str, Enum):
    INCREASING_I = "increasing i"
    DECREASING_I = "decreasing i"
    ROW_MAJOR = "row-major grid order"
    REVERSE_GRID = "reverse grid order"
    INCREASING_INTERVAL_LENGTH = "increasing interval length"
    REVERSE_CAPACITY = "capacity decreasing"
    FORWARD_CAPACITY = "capacity increasing"
    MASK_INCREASING = "mask increasing"
    POSTORDER_TREE = "postorder tree traversal"
    TOPOLOGICAL_DAG = "topological order on DAG"
    LEFT_TO_RIGHT_DIGITS = "left-to-right digit order"


@dataclass(frozen=True)
class SRTBOT:
    """
    A compact description of a DP family using the SRTBOT frame.

    S — Subproblems
    R — Relationships
    T — Topological order
    B — Base cases
    O — Original problem / answer extraction
    T — Time complexity
    """

    subproblems: str
    relationships: str
    topological_order: str
    base_cases: str
    original_answer: str
    time_complexity: str


@dataclass(frozen=True)
class DPFamily:
    name: str
    state_shape: StateShape
    aggregation: Aggregation
    evaluation_order: EvaluationOrder
    representative_problems: tuple[int, ...]
    mental_model: str
    srtbot: SRTBOT
    common_traps: tuple[str, ...]


@dataclass(frozen=True)
class CompositionChain:
    name: str
    chain: tuple[str, ...]
    skeleton: str
    solves: tuple[int, ...]


# =============================================================================
# Family Atlas
# =============================================================================


DP_FAMILIES: tuple[DPFamily, ...] = (
    DPFamily(
        name="Fibonacci / Stair-Step DP",
        state_shape=StateShape.INDEX,
        aggregation=Aggregation.SUM,
        evaluation_order=EvaluationOrder.INCREASING_I,
        representative_problems=(509, 70, 746, 1137, 790),
        mental_model="A size-i state depends on a constant number of previous sizes.",
        srtbot=SRTBOT(
            subproblems="dp[i] = answer for size/step i.",
            relationships="Usually dp[i-1], dp[i-2], sometimes dp[i-3].",
            topological_order="Increasing i.",
            base_cases="Smallest sizes such as dp[0], dp[1].",
            original_answer="dp[n].",
            time_complexity="O(n) states × O(1) transition.",
        ),
        common_traps=(
            "Confusing dp[0] as impossible instead of empty way.",
            "Returning the last physical stair instead of the virtual top.",
        ),
    ),
    DPFamily(
        name="1D Prefix Parsing DP",
        state_shape=StateShape.PREFIX,
        aggregation=Aggregation.SUM,
        evaluation_order=EvaluationOrder.INCREASING_I,
        representative_problems=(91, 639, 1416, 2266),
        mental_model="Parse the prefix by choosing the last valid token.",
        srtbot=SRTBOT(
            subproblems="dp[i] = number of ways to parse s[:i].",
            relationships="Sum over valid last token lengths.",
            topological_order="Increasing prefix length.",
            base_cases="dp[0] = 1 for the empty parse.",
            original_answer="dp[n].",
            time_complexity="O(n × max_token_length).",
        ),
        common_traps=(
            "Treating invalid tokens like '0' or leading-zero numbers as valid.",
            "Using Fibonacci blindly without checking token validity.",
        ),
    ),
    DPFamily(
        name="Take-or-Skip / House Robber",
        state_shape=StateShape.PREFIX,
        aggregation=Aggregation.MAX,
        evaluation_order=EvaluationOrder.INCREASING_I,
        representative_problems=(198, 213, 337, 740, 2140),
        mental_model="At each item, either skip it or take it and jump over conflicting items.",
        srtbot=SRTBOT(
            subproblems="dp[i] = best value from first i items, or suffix dp[i] for jump variants.",
            relationships="skip current vs take current plus compatible previous/future state.",
            topological_order="Increasing i for prefix; decreasing i for suffix jump variants.",
            base_cases="Empty prefix/suffix has value 0.",
            original_answer="dp[n] for prefix or dp[0] for suffix.",
            time_complexity="O(n) when transition target is O(1).",
        ),
        common_traps=(
            "Applying local greedy choices to adjacent conflicts.",
            "Missing that Delete and Earn is House Robber over value-axis, not input index.",
            "For tree mutation, using dp[i] instead of dfs(node)->(skip,take).",
        ),
    ),
    DPFamily(
        name="Kadane / Local-Global DP",
        state_shape=StateShape.ENDING_AT_INDEX,
        aggregation=Aggregation.MAX,
        evaluation_order=EvaluationOrder.INCREASING_I,
        representative_problems=(53, 152, 918, 1186, 1567, 1746, 1749),
        mental_model="Maintain best structure ending here plus best seen globally.",
        srtbot=SRTBOT(
            subproblems="local[i] = best answer ending exactly at i.",
            relationships="extend previous local state or restart at current item.",
            topological_order="Increasing i.",
            base_cases="local at first element.",
            original_answer="max over local states, tracked as best.",
            time_complexity="O(n).",
        ),
        common_traps=(
            "Returning dp[-1] when the answer is max(dp).",
            "Confusing subarray with subsequence.",
            "For product, forgetting both min and max local products.",
        ),
    ),
    DPFamily(
        name="Grid Path DP",
        state_shape=StateShape.GRID_CELL,
        aggregation=Aggregation.MIN,
        evaluation_order=EvaluationOrder.ROW_MAJOR,
        representative_problems=(62, 63, 64, 120, 174, 931, 1289, 1463),
        mental_model="Each grid cell is a state whose predecessors are geometric neighbors.",
        srtbot=SRTBOT(
            subproblems="dp[r][c] = answer ending at or starting from cell (r,c).",
            relationships="Read allowed predecessor/successor cells.",
            topological_order="Row-major, reverse row-major, or layer order depending on dependency direction.",
            base_cases="Start cell, boundary row/column, or terminal cell.",
            original_answer="Usually dp[-1][-1], dp[0][0], or best over final row.",
            time_complexity="O(rows × cols × transition_cost).",
        ),
        common_traps=(
            "Using row-major order when recurrence depends on future cells.",
            "Not distinguishing obstacle cells from high-cost cells.",
            "For Dungeon Game, using forward min path instead of reverse health requirement.",
        ),
    ),
    DPFamily(
        name="Two-Sequence Alignment DP",
        state_shape=StateShape.TWO_SEQUENCE,
        aggregation=Aggregation.MIN,
        evaluation_order=EvaluationOrder.ROW_MAJOR,
        representative_problems=(72, 97, 115, 583, 712, 1035, 1143, 1092),
        mental_model="A 2D table over prefixes of two sequences.",
        srtbot=SRTBOT(
            subproblems="dp[i][j] = answer for a[:i] and b[:j].",
            relationships="match/mismatch, delete/insert/replace, or consume from one/both strings.",
            topological_order="Increasing i and j.",
            base_cases="Empty prefix row/column.",
            original_answer="dp[n][m].",
            time_complexity="O(nm × transition_cost).",
        ),
        common_traps=(
            "Off-by-one confusion between dp index and string index.",
            "Using substring logic for subsequence problems.",
            "For counting, overwriting instead of accumulating.",
        ),
    ),
    DPFamily(
        name="Knapsack / Capacity DP",
        state_shape=StateShape.CAPACITY,
        aggregation=Aggregation.MAX,
        evaluation_order=EvaluationOrder.REVERSE_CAPACITY,
        representative_problems=(416, 474, 494, 518, 879, 1049, 1155, 1449),
        mental_model="Capacity or target becomes a pseudo-polynomial state dimension.",
        srtbot=SRTBOT(
            subproblems="dp[w] or dp[i][w] = best/count/possible value at capacity or sum w.",
            relationships="include/exclude item, add coin, or transition from previous sum.",
            topological_order="Reverse capacity for 0/1; forward capacity for unbounded.",
            base_cases="dp[0] = neutral value: True, 0, or 1 depending on aggregation.",
            original_answer="dp[target] or best over capacities.",
            time_complexity="O(number_of_items × capacity × transition_cost).",
        ),
        common_traps=(
            "Using forward loop for 0/1 and accidentally reusing items.",
            "Using reverse loop for unbounded and preventing reuse.",
            "Confusing combinations with permutations in counting problems.",
        ),
    ),
    DPFamily(
        name="Interval DP",
        state_shape=StateShape.INTERVAL,
        aggregation=Aggregation.MIN,
        evaluation_order=EvaluationOrder.INCREASING_INTERVAL_LENGTH,
        representative_problems=(312, 375, 486, 516, 877, 1000, 1039, 1547),
        mental_model="Solve all smaller intervals before larger intervals.",
        srtbot=SRTBOT(
            subproblems="dp[l][r] = answer for interval from l to r.",
            relationships="Choose boundary action or split point k.",
            topological_order="Increasing interval length.",
            base_cases="Empty or singleton intervals.",
            original_answer="dp[0][n-1].",
            time_complexity="Usually O(n^2) states × O(1 or n) transition.",
        ),
        common_traps=(
            "Filling by l/r loops that violate interval dependency order.",
            "For split DP, forgetting O(n) transition cost.",
            "Confusing inclusive [l,r] with half-open [l,r).",
        ),
    ),
    DPFamily(
        name="Stock State-Machine DP",
        state_shape=StateShape.STATE_MACHINE,
        aggregation=Aggregation.MAX,
        evaluation_order=EvaluationOrder.INCREASING_I,
        representative_problems=(121, 122, 123, 188, 309, 714),
        mental_model="Each day transitions between holding/not-holding and constraint states.",
        srtbot=SRTBOT(
            subproblems="dp[day][state] = best profit after day in trading state.",
            relationships="buy, sell, hold, rest transitions.",
            topological_order="Increasing day.",
            base_cases="Before trading: cash=0, hold=-inf.",
            original_answer="Best non-holding terminal state.",
            time_complexity="O(days × number_of_states).",
        ),
        common_traps=(
            "Returning a holding state as final answer.",
            "Updating states in-place without preserving old values when needed.",
            "Ambiguous transaction count: before buy vs after sell.",
        ),
    ),
    DPFamily(
        name="Bitmask DP",
        state_shape=StateShape.BITMASK,
        aggregation=Aggregation.MIN,
        evaluation_order=EvaluationOrder.MASK_INCREASING,
        representative_problems=(847, 943, 1125, 1349, 1434, 1799, 1879),
        mental_model="A subset of chosen/visited elements is encoded as an integer mask.",
        srtbot=SRTBOT(
            subproblems="dp[mask] or dp[mask][last] = best answer for selected subset.",
            relationships="Add one unused element or transition from previous mask.",
            topological_order="Increasing mask or increasing popcount.",
            base_cases="Empty mask or singleton masks.",
            original_answer="Full mask or best over full-mask terminal states.",
            time_complexity="O(2^n × transition_cost).",
        ),
        common_traps=(
            "Forgetting terminal dimension like last node in path problems.",
            "Using bitmask DP when n is too large.",
            "Confusing set membership with ordering.",
        ),
    ),
    DPFamily(
        name="Digit DP",
        state_shape=StateShape.DIGIT,
        aggregation=Aggregation.SUM,
        evaluation_order=EvaluationOrder.LEFT_TO_RIGHT_DIGITS,
        representative_problems=(233, 357, 600, 902, 1012, 1067, 1397),
        mental_model="Count valid numbers digit by digit under a tight upper-bound constraint.",
        srtbot=SRTBOT(
            subproblems="dp[pos][tight][started][extra_state] = count from current digit position.",
            relationships="Try each allowed digit and update flags.",
            topological_order="Left-to-right recursion with memoization over non-tight states.",
            base_cases="pos == len(digits).",
            original_answer="dp(0, tight=True, started=False, ...).",
            time_complexity="O(num_digits × flag_states × digit_choices).",
        ),
        common_traps=(
            "Memoizing tight states incorrectly when bound-specific.",
            "Mishandling leading zeros.",
            "Forgetting whether 0 should be counted.",
        ),
    ),
    DPFamily(
        name="Tree DP",
        state_shape=StateShape.TREE_TUPLE,
        aggregation=Aggregation.MAX,
        evaluation_order=EvaluationOrder.POSTORDER_TREE,
        representative_problems=(124, 337, 834, 968, 1373, 1372),
        mental_model="Parent state is computed from child states.",
        srtbot=SRTBOT(
            subproblems="dfs(node) returns one or more values for subtree rooted at node.",
            relationships="Combine left and right child states.",
            topological_order="Postorder traversal.",
            base_cases="Null node or leaf node.",
            original_answer="dfs(root) or global value updated during DFS.",
            time_complexity="O(number_of_nodes × combine_cost).",
        ),
        common_traps=(
            "Returning the global answer instead of the value parent needs.",
            "Not separating downward path from through-node path.",
            "For rerooting, missing second pass.",
        ),
    ),
    DPFamily(
        name="Graph / DAG DP",
        state_shape=StateShape.DAG_VERTEX,
        aggregation=Aggregation.RELAX,
        evaluation_order=EvaluationOrder.TOPOLOGICAL_DAG,
        representative_problems=(329, 787, 847, 1548, 1857, 1928, 1976, 2050),
        mental_model="When the dependency graph is explicit, DP becomes graph relaxation.",
        srtbot=SRTBOT(
            subproblems="dp[v] or dp[steps][v] = best value reaching/starting at vertex v.",
            relationships="Relax along edges.",
            topological_order="Topological order if DAG; otherwise bounded steps or shortest-path algorithm.",
            base_cases="Source/target vertices or step 0.",
            original_answer="Target state or best over terminal vertices.",
            time_complexity="O(states × outgoing_degree).",
        ),
        common_traps=(
            "Assuming arbitrary graph has acyclic DP order.",
            "Using DFS memo on graphs with cycles without cycle handling.",
            "Confusing shortest path with DP over a DAG.",
        ),
    ),
)


# =============================================================================
# Composition Chains
# =============================================================================


COMPOSITION_CHAINS: tuple[CompositionChain, ...] = (
    CompositionChain(
        name="House Robber Path",
        chain=(
            "prefix state dp[i]",
            "take-or-skip transition",
            "max aggregation",
            "rolling two-variable compression",
        ),
        skeleton="weighted independent set on a path",
        solves=(198, 213, 740),
    ),
    CompositionChain(
        name="Stock State Machine",
        chain=(
            "day index",
            "holding/not-holding status",
            "buy/sell/rest transitions",
            "terminal answer must be non-holding",
        ),
        skeleton="finite-state DP over days",
        solves=(121, 122, 123, 188, 309, 714),
    ),
    CompositionChain(
        name="Knapsack Capacity DP",
        chain=(
            "capacity state dp[w]",
            "include/exclude transition",
            "reverse loop for 0/1 or forward loop for unbounded",
            "aggregation: max, min, sum, or boolean OR",
        ),
        skeleton="capacity-indexed pseudo-polynomial DP",
        solves=(416, 474, 494, 518, 879, 1049),
    ),
    CompositionChain(
        name="Two-Sequence Alignment",
        chain=(
            "two-prefix state dp[i][j]",
            "match/mismatch transition",
            "empty prefix base row/column",
            "row-major evaluation order",
        ),
        skeleton="alignment table",
        solves=(72, 97, 115, 583, 712, 1035, 1143, 1092),
    ),
    CompositionChain(
        name="Interval DP",
        chain=(
            "interval state dp[l][r]",
            "boundary choice or split point",
            "increasing interval length",
            "answer at dp[0][n-1]",
        ),
        skeleton="shorter intervals before larger intervals",
        solves=(312, 375, 486, 516, 877, 1000, 1039, 1547),
    ),
    CompositionChain(
        name="LIS Previous-Choice DP",
        chain=(
            "ending-at-i state",
            "choose previous compatible index",
            "max over candidates",
            "answer is max(dp), not dp[-1]",
        ),
        skeleton="best chain ending at each item",
        solves=(300, 354, 368, 673, 1027, 1048, 1626),
    ),
)


# =============================================================================
# Expansion Plan
# =============================================================================


PART_EXPANSION_ORDER: tuple[str, ...] = (
    "Part 0 — Catalogue CSV + family summary",
    "Part 1 — High-Level DP Atlas",
    "Part 2 — Core DP Primitives",
    "Part 3 — 1D DP Families",
    "Part 4 — Grid DP",
    "Part 5 — Two-Sequence DP",
    "Part 6 — Knapsack / Capacity DP",
    "Part 7 — Interval DP",
    "Part 8 — Stock Series",
    "Part 9 — Stone Game Series",
    "Part 10 — LIS / Sequence Optimization",
    "Part 11 — Bitmask / Digit / Tree / Graph DP",
    "Part 12 — Advanced DP Optimizations",
    "Part 13 — Final Toolkit + Practice Plan",
)


# =============================================================================
# Query Helpers
# =============================================================================


def family_names() -> list[str]:
    return [family.name for family in DP_FAMILIES]


def find_family(name_fragment: str) -> DPFamily:
    fragment = name_fragment.lower()

    for family in DP_FAMILIES:
        if fragment in family.name.lower():
            return family

    raise ValueError(f"No DP family found for fragment: {name_fragment!r}")


def families_by_state_shape(shape: StateShape) -> list[DPFamily]:
    return [family for family in DP_FAMILIES if family.state_shape == shape]


def representative_problem_ids() -> set[int]:
    ids: set[int] = set()

    for family in DP_FAMILIES:
        ids.update(family.representative_problems)

    return ids


def problems_to_families(problem_id: int) -> list[str]:
    return [
        family.name
        for family in DP_FAMILIES
        if problem_id in family.representative_problems
    ]


def print_srtbot(family: DPFamily) -> None:
    card = family.srtbot

    print(f"{family.name}")
    print(f"S: {card.subproblems}")
    print(f"R: {card.relationships}")
    print(f"T: {card.topological_order}")
    print(f"B: {card.base_cases}")
    print(f"O: {card.original_answer}")
    print(f"T: {card.time_complexity}")


def print_composition_chains(chains: Iterable[CompositionChain] = COMPOSITION_CHAINS) -> None:
    for chain in chains:
        print(chain.name)
        print("  " + " + ".join(chain.chain))
        print(f"  -> {chain.skeleton}")
        print(f"  -> solves {', '.join(map(str, chain.solves))}")


# =============================================================================
# Core Diagnostic Questions
# =============================================================================


DP_ATLAS_DIAGNOSTIC_QUESTIONS: tuple[str, ...] = (
    "What state shape does this problem naturally want?",
    "Is the state a prefix, suffix, interval, capacity, tree, mask, digit, or graph state?",
    "What does one cell/state mean in one precise sentence?",
    "What are the recurrence edges?",
    "What aggregation operator is being used?",
    "What topological order makes the recurrence legal?",
    "What are the mathematically meaningful base cases?",
    "Which state or terminal aggregation gives the original answer?",
    "How many states exist?",
    "How expensive is each transition?",
    "Can the table be rolled or compressed?",
    "Is the problem actually greedy, BFS, shortest path, or backtracking instead of DP?",
)


if __name__ == "__main__":
    assert len(DP_FAMILIES) >= 10
    assert "Take-or-Skip / House Robber" in family_names()
    assert 198 in representative_problem_ids()
    assert "Stock State-Machine DP" in problems_to_families(121)
    assert find_family("interval").state_shape == StateShape.INTERVAL
    assert families_by_state_shape(StateShape.CAPACITY)[0].name == "Knapsack / Capacity DP"
    print_srtbot(find_family("house robber"))
    print()
    print_composition_chains()
