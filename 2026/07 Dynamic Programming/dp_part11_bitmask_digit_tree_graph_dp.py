"""

Part 11 — Bitmask / Digit / Tree / Graph Dynamic Programming

Scope:
    Bitmask DP:
        847. Shortest Path Visiting All Nodes
        943. Find the Shortest Superstring
        1125. Smallest Sufficient Team
        1349. Maximum Students Taking Exam
        1799. Maximize Score After N Operations
        1879. Minimum XOR Sum of Two Arrays

    Digit DP:
        233. Number of Digit One
        357. Count Numbers with Unique Digits
        600. Non-negative Integers without Consecutive Ones
        902. Numbers At Most N Given Digit Set
        1012. Numbers With Repeated Digits

    Tree DP:
        124. Binary Tree Maximum Path Sum
        337. House Robber III
        834. Sum of Distances in Tree
        968. Binary Tree Cameras
        1372. Longest ZigZag Path in a Binary Tree

    Graph / DAG DP:
        329. Longest Increasing Path in a Matrix
        787. Cheapest Flights Within K Stops
        1548. The Most Similar Path in a Graph
        1857. Largest Color Value in a Directed Graph
        2050. Parallel Courses III

Core mental model:
    Earlier parts used states like:
        dp[i]
        dp[r][c]
        dp[l][r]

    This part expands the state vocabulary:

        dp[mask]
        dp[pos][tight][started][...]
        dfs(node) -> tuple
        dp[v]
        dp[step][v]
        dp[mask][last]

    The primitive is still SRTBOT:
        state
        recurrence
        topological order
        base cases
        answer extraction
        complexity









# Part 11 — Bitmask / Digit / Tree / Graph DP

Python file:

[Download Part 11 — Bitmask / Digit / Tree / Graph DP Python file](sandbox:/mnt/data/dp_part11_bitmask_digit_tree_graph_dp.py)

## What Part 11 covers

```text id="kx06ie"
Advanced DP state shapes
    -> Bitmask DP
    -> Digit DP
    -> Tree DP
    -> Graph / DAG DP
```

## 1. Bitmask DP

Core state:

```text id="rx8erz"
dp[mask]
dp[mask][last]
```

Use when the problem has a small set of items and a subset matters.

Representative problems:

```text id="4focau"
847. Shortest Path Visiting All Nodes
943. Find the Shortest Superstring
1125. Smallest Sufficient Team
1799. Maximize Score After N Operations
1879. Minimum XOR Sum of Two Arrays
```

Key patterns:

```text id="rc7jzy"
assignment:
    dp[mask] = best after assigning first popcount(mask) items

team cover:
    dp[skill_mask] = smallest team covering skill_mask

TSP/path:
    dp[mask][last] = best path using mask and ending at last

pairing game:
    dp[mask] = best score after using selected elements
```

Main trap:

```text id="4m916v"
Sometimes dp[mask] is insufficient.
Path problems usually need dp[mask][last].
```

---

## 2. Digit DP

Core state:

```text id="oq41pn"
dp[pos][tight][started][extra_state]
```

Use when counting numbers under an upper bound with digit constraints.

Representative problems:

```text id="igkl0u"
233. Number of Digit One
357. Count Numbers with Unique Digits
600. Non-negative Integers without Consecutive Ones
902. Numbers At Most N Given Digit Set
1012. Numbers With Repeated Digits
```

Common flags:

```text id="c2esve"
pos:
    current digit position

tight:
    whether prefix is equal to upper bound so far

started:
    whether we have placed a non-leading-zero digit

prev digit / prev_one:
    needed for adjacency constraints

used mask:
    needed for unique-digit constraints
```

Main trap:

```text id="68dfw5"
Leading zero handling changes the count.
```

---

## 3. Tree DP

Core state:

```text id="9f4as3"
dfs(node) -> value
dfs(node) -> tuple of values
```

Use when parent answers depend on child answers.

Representative problems:

```text id="lhrbkj"
124. Binary Tree Maximum Path Sum
337. House Robber III
834. Sum of Distances in Tree
968. Binary Tree Cameras
1372. Longest ZigZag Path in a Binary Tree
```

Important distinction:

```text id="zy7wok"
returned value to parent
vs
global answer
```

Example: Binary Tree Maximum Path Sum.

```text id="o47qnr"
return to parent:
    best downward path

global answer:
    best path passing through current node using both children
```

For rerooting DP:

```text id="vjpx5m"
postorder pass:
    compute subtree values

preorder pass:
    move root from parent to child
```

---

## 4. Graph / DAG DP

Core states:

```text id="qq44is"
dp[v]
dp[step][v]
dp[mask][v]
```

Use when the dependency graph is explicit.

Representative problems:

```text id="s6itac"
329. Longest Increasing Path in a Matrix
787. Cheapest Flights Within K Stops
1548. The Most Similar Path in a Graph
1857. Largest Color Value in a Directed Graph
2050. Parallel Courses III
```

Important distinction:

```text id="efho88"
DAG:
    topological DP works

cyclic graph:
    plain DFS memo may be invalid

bounded-step graph:
    dp[step][v] works

unit-cost state graph:
    BFS over DP states works
```

## Composition chains

```text id="yb64yo"
subset mask
+ popcount(mask) as progress
+ choose unused item
-> assignment bitmask DP
```

```text id="fxpaov"
mask
+ terminal last node
+ add one unvisited node
-> TSP / shortest superstring DP
```

```text id="awyuk6"
digit position
+ tight flag
+ started flag
+ previous digit / used mask
-> Digit DP
```

```text id="a3a4iq"
postorder DFS
+ tuple state per node
+ combine child states
-> Tree DP
```

```text id="vky59n"
DAG vertex state
+ topological order
+ edge relaxation
-> Graph DP
```

## Most important traps

```text id="q6p0b4"
1. Forgetting the last-node dimension in path bitmask DP.
2. Using bitmask DP when n is too large.
3. Mishandling leading zeros in Digit DP.
4. Memoizing tight digit states incorrectly.
5. Returning the wrong tree value to the parent.
6. Confusing tree global answer with returned subtree answer.
7. Applying DFS memo to cyclic graphs without cycle handling.
8. Updating bounded-step graph DP in-place and accidentally using too many steps.
9. Forgetting topological order for DAG DP.
```

Next natural step: **Part 12 — Advanced DP Optimizations**.

"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import cache
from math import gcd, inf
from typing import Optional


# =============================================================================
# Level 0 — Generic Helpers
# =============================================================================


def bit(i: int) -> int:
    return 1 << i


def has(mask: int, i: int) -> bool:
    return bool(mask & bit(i))


def add(mask: int, i: int) -> int:
    return mask | bit(i)


def remove(mask: int, i: int) -> int:
    return mask & ~bit(i)


def full_mask(n: int) -> int:
    return (1 << n) - 1


def iter_bits(mask: int):
    """
    Yield set bit indices in mask.
    """
    i = 0

    while mask:
        if mask & 1:
            yield i

        mask >>= 1
        i += 1


def popcount(mask: int) -> int:
    return mask.bit_count()


# =============================================================================
# Level 1 — Bitmask DP: Assignment / Matching
# =============================================================================


def minimum_xor_sum(nums1: list[int], nums2: list[int]) -> int:
    """
    LeetCode:
        1879. Minimum XOR Sum of Two Arrays

    S:
        dp[mask] = minimum XOR sum after assigning first popcount(mask)
                   nums1 values to selected nums2 indices in mask.

    R:
        worker/item index i = popcount(mask)
        choose an unused j from nums2.

    T:
        increasing mask.

    B:
        dp[0] = 0

    O:
        dp[(1 << n) - 1]

    Complexity:
        O(n * 2^n)
    """
    n = len(nums1)
    dp = [inf] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        i = popcount(mask)

        if i >= n:
            continue

        for j in range(n):
            if has(mask, j):
                continue

            nxt = add(mask, j)
            dp[nxt] = min(dp[nxt], dp[mask] + (nums1[i] ^ nums2[j]))

    return int(dp[-1])


def assignment_min_cost(cost: list[list[int]]) -> int:
    """
    Generic assignment bitmask DP.

    S:
        dp[mask] = min cost after assigning first popcount(mask) workers
                  to selected jobs in mask.

    This is the template behind many matching-style bitmask problems.
    """
    n = len(cost)
    dp = [inf] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        worker = popcount(mask)

        if worker >= n:
            continue

        for job in range(n):
            if not has(mask, job):
                nxt = add(mask, job)
                dp[nxt] = min(dp[nxt], dp[mask] + cost[worker][job])

    return int(dp[-1])


# =============================================================================
# Level 2 — Bitmask DP: Smallest Sufficient Team
# =============================================================================


def smallest_sufficient_team(req_skills: list[str], people: list[list[str]]) -> list[int]:
    """
    LeetCode:
        1125. Smallest Sufficient Team

    Convert each person's skills into a bitmask.

    S:
        dp[mask] = one minimum-size team covering skill mask.

    R:
        add person p:
            new_mask = mask | person_mask[p]

    T:
        iterate people; update dp.

    B:
        dp[0] = []

    O:
        dp[full_skill_mask]

    Complexity:
        O(people * 2^skills)
    """
    skill_id = {skill: i for i, skill in enumerate(req_skills)}
    target = full_mask(len(req_skills))

    person_masks = []

    for skills in people:
        mask = 0

        for skill in skills:
            if skill in skill_id:
                mask |= bit(skill_id[skill])

        person_masks.append(mask)

    dp: dict[int, list[int]] = {0: []}

    for person, pmask in enumerate(person_masks):
        if pmask == 0:
            continue

        snapshot = list(dp.items())

        for mask, team in snapshot:
            nxt = mask | pmask

            if nxt not in dp or len(team) + 1 < len(dp[nxt]):
                dp[nxt] = team + [person]

    return dp[target]


# =============================================================================
# Level 3 — Bitmask DP: Path / TSP Shape
# =============================================================================


def shortest_path_visiting_all_nodes(graph: list[list[int]]) -> int:
    """
    LeetCode:
        847. Shortest Path Visiting All Nodes

    This is BFS over a DP state graph.

    S:
        (node, mask) = currently at node, visited set mask.

    R:
        move to neighbor:
            (neighbor, mask | bit(neighbor))

    T:
        BFS layers because every edge has unit cost.

    B:
        all singleton states are sources.

    O:
        first state with full mask.

    Complexity:
        O(n * 2^n + edges * 2^n)
    """
    n = len(graph)
    target = full_mask(n)
    q = deque()
    seen = set()

    for node in range(n):
        mask = bit(node)
        q.append((node, mask, 0))
        seen.add((node, mask))

    while q:
        node, mask, dist = q.popleft()

        if mask == target:
            return dist

        for nei in graph[node]:
            nxt = (nei, mask | bit(nei))

            if nxt not in seen:
                seen.add(nxt)
                q.append((nei, nxt[1], dist + 1))

    return -1


def shortest_superstring(words: list[str]) -> str:
    """
    LeetCode:
        943. Find the Shortest Superstring

    TSP-like bitmask DP.

    Precompute overlap[i][j]:
        max suffix of words[i] matching prefix of words[j].

    S:
        dp[mask][last] = shortest superstring length using words in mask
                         and ending with word last.

    R:
        append next word.

    Reconstruction:
        parent[mask][last] stores previous last.

    Complexity:
        O(n^2 * 2^n + n^2 * L^2)
    """
    n = len(words)

    overlap = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            max_len = min(len(words[i]), len(words[j]))

            for k in range(max_len, -1, -1):
                if words[i].endswith(words[j][:k]):
                    overlap[i][j] = k
                    break

    size = 1 << n
    dp = [[inf] * n for _ in range(size)]
    parent = [[-1] * n for _ in range(size)]

    for i in range(n):
        dp[bit(i)][i] = len(words[i])

    for mask in range(size):
        for last in range(n):
            if dp[mask][last] == inf:
                continue

            for nxt in range(n):
                if has(mask, nxt):
                    continue

                new_mask = add(mask, nxt)
                cost = dp[mask][last] + len(words[nxt]) - overlap[last][nxt]

                if cost < dp[new_mask][nxt]:
                    dp[new_mask][nxt] = cost
                    parent[new_mask][nxt] = last

    mask = size - 1
    last = min(range(n), key=lambda i: dp[mask][i])

    order = []

    while last != -1:
        order.append(last)
        prev = parent[mask][last]
        mask = remove(mask, last)
        last = prev

    order.reverse()

    result = words[order[0]]

    for i in range(1, len(order)):
        a = order[i - 1]
        b = order[i]
        result += words[b][overlap[a][b]:]

    return result


# =============================================================================
# Level 4 — Bitmask DP: Game / Pairing
# =============================================================================


def max_score_after_n_operations(nums: list[int]) -> int:
    """
    LeetCode:
        1799. Maximize Score After N Operations

    S:
        dp[mask] = max score after choosing used numbers in mask.

    If used count is 2 * operation_index:
        next operation number = used_count // 2 + 1

    R:
        choose two unused indices i, j:
            score = op * gcd(nums[i], nums[j]) + dp[mask | i | j]

    T:
        top-down memo over masks.

    Complexity:
        O(n^2 * 2^n)
    """
    n = len(nums)

    @cache
    def dp(mask: int) -> int:
        used = popcount(mask)

        if used == n:
            return 0

        op = used // 2 + 1
        best = 0

        for i in range(n):
            if has(mask, i):
                continue

            for j in range(i + 1, n):
                if has(mask, j):
                    continue

                nxt = mask | bit(i) | bit(j)
                best = max(best, op * gcd(nums[i], nums[j]) + dp(nxt))

        return best

    return dp(0)


# =============================================================================
# Level 5 — Digit DP
# =============================================================================


def count_without_consecutive_ones(n: int) -> int:
    """
    LeetCode:
        600. Non-negative Integers without Consecutive Ones

    S:
        dp(pos, tight, prev_one) = count valid completions from binary digit pos.

    R:
        choose bit 0 or 1, respecting tight and no consecutive ones.

    B:
        pos == len(bits) -> 1

    O:
        dp(0, True, False)

    Complexity:
        O(number_of_bits * 2 * 2)
    """
    bits = bin(n)[2:]

    @cache
    def dp(pos: int, tight: bool, prev_one: bool) -> int:
        if pos == len(bits):
            return 1

        limit = int(bits[pos]) if tight else 1
        total = 0

        for b in range(limit + 1):
            if prev_one and b == 1:
                continue

            total += dp(
                pos + 1,
                tight and b == limit,
                b == 1,
            )

        return total

    return dp(0, True, False)


def at_most_n_given_digit_set(digits: list[str], n: int) -> int:
    """
    LeetCode:
        902. Numbers At Most N Given Digit Set

    Count positive integers <= n using only the given digit set.

    S:
        dp(pos, tight, started) = count valid numbers from current decimal pos.

    R:
        choose to skip leading position if not started,
        or place one allowed digit.

    O:
        subtract 1 if empty number was counted.
    """
    chars = str(n)

    @cache
    def dp(pos: int, tight: bool, started: bool) -> int:
        if pos == len(chars):
            return 1 if started else 0

        total = 0
        limit = chars[pos] if tight else "9"

        if not started:
            total += dp(pos + 1, False, False)

        for d in digits:
            if d > limit:
                continue

            total += dp(
                pos + 1,
                tight and d == limit,
                True,
            )

        return total

    return dp(0, True, False)


def count_numbers_with_unique_digits(n: int) -> int:
    """
    LeetCode:
        357. Count Numbers with Unique Digits

    Counts x where 0 <= x < 10^n.

    This can be combinatorics, but it is also a digit-mask DP.

    S:
        dp(pos, used_mask, started)

    Since upper bound is 10^n - 1, tight is unnecessary.
    """
    if n == 0:
        return 1

    @cache
    def dp(pos: int, used: int, started: bool) -> int:
        if pos == n:
            return 1

        total = 0

        if not started:
            total += dp(pos + 1, used, False)

        for d in range(10):
            if not started and d == 0:
                continue

            if has(used, d):
                continue

            total += dp(pos + 1, add(used, d), True)

        return total

    return dp(0, 0, False)


def num_dup_digits_at_most_n(n: int) -> int:
    """
    LeetCode:
        1012. Numbers With Repeated Digits

    Easier reduction:
        repeated_digits_count = n - count_unique_positive_numbers_up_to_n

    Digit DP counts positive numbers <= n with all unique digits.
    """
    digits = str(n)

    @cache
    def unique(pos: int, tight: bool, started: bool, used: int) -> int:
        if pos == len(digits):
            return 1 if started else 0

        total = 0
        limit = int(digits[pos]) if tight else 9

        if not started:
            total += unique(pos + 1, False, False, used)

        for d in range(0, limit + 1):
            if not started and d == 0:
                continue

            if has(used, d):
                continue

            total += unique(
                pos + 1,
                tight and d == limit,
                True,
                add(used, d),
            )

        return total

    return n - unique(0, True, False, 0)


def count_digit_one(n: int) -> int:
    """
    LeetCode:
        233. Number of Digit One

    Digit DP version.

    S:
        dp(pos, tight, count_so_far)

    For simplicity, return total count of ones across all valid numbers.
    A more optimized mathematical solution exists.
    """
    digits = str(n)

    @cache
    def dp(pos: int, tight: bool, ones: int) -> int:
        if pos == len(digits):
            return ones

        limit = int(digits[pos]) if tight else 9
        total = 0

        for d in range(limit + 1):
            total += dp(
                pos + 1,
                tight and d == limit,
                ones + (1 if d == 1 else 0),
            )

        return total

    return dp(0, True, 0)


# =============================================================================
# Level 6 — Tree DP
# =============================================================================


@dataclass
class TreeNode:
    val: int = 0
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def rob_tree(root: Optional[TreeNode]) -> int:
    """
    LeetCode:
        337. House Robber III

    S:
        dfs(node) -> (skip, take)

    R:
        take node:
            node.val + left.skip + right.skip

        skip node:
            max(left) + max(right)

    T:
        postorder.
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


def binary_tree_max_path_sum(root: Optional[TreeNode]) -> int:
    """
    LeetCode:
        124. Binary Tree Maximum Path Sum

    Key split:
        return value to parent:
            best downward path starting at node

        global answer:
            best path passing through node using both children

    S:
        dfs(node) returns downward_gain.

    R:
        downward_gain = node.val + max(left_gain, right_gain, 0)

    Global:
        node.val + max(0,left) + max(0,right)
    """
    best = -10**18

    def dfs(node: Optional[TreeNode]) -> int:
        nonlocal best

        if node is None:
            return 0

        left = max(0, dfs(node.left))
        right = max(0, dfs(node.right))

        best = max(best, node.val + left + right)

        return node.val + max(left, right)

    dfs(root)
    return best


def min_camera_cover(root: Optional[TreeNode]) -> int:
    """
    LeetCode:
        968. Binary Tree Cameras

    Tree DP with three states.

    States returned:
        has_camera:
            minimum cameras if this node has a camera.

        covered:
            minimum cameras if this node is covered but has no camera.

        needs_camera:
            minimum cameras if this node is not covered and needs parent camera.

    R:
        has_camera = 1 + min(left states) + min(right states)

        covered = min(
            left has camera + right covered/has_camera,
            right has camera + left covered/has_camera
        )

        needs_camera = left.covered + right.covered

    O:
        min(root.has_camera, root.covered)
    """
    INF = 10**9

    def dfs(node: Optional[TreeNode]) -> tuple[int, int, int]:
        if node is None:
            return INF, 0, 0

        lh, lc, ln = dfs(node.left)
        rh, rc, rn = dfs(node.right)

        has_camera = 1 + min(lh, lc, ln) + min(rh, rc, rn)
        covered = min(
            lh + min(rh, rc),
            rh + min(lh, lc),
        )
        needs_camera = lc + rc

        return has_camera, covered, needs_camera

    has_camera, covered, _ = dfs(root)
    return min(has_camera, covered)


def longest_zigzag(root: Optional[TreeNode]) -> int:
    """
    LeetCode:
        1372. Longest ZigZag Path in a Binary Tree

    S:
        dfs(node) -> (left_start, right_start)

        left_start:
            longest zigzag starting at node by first moving left.

        right_start:
            longest zigzag starting at node by first moving right.

    R:
        left_start = 1 + child's right_start
        right_start = 1 + child's left_start

    Answer:
        global max edges.
    """
    best = 0

    def dfs(node: Optional[TreeNode]) -> tuple[int, int]:
        nonlocal best

        if node is None:
            return -1, -1

        left_l, left_r = dfs(node.left)
        right_l, right_r = dfs(node.right)

        go_left = 1 + left_r
        go_right = 1 + right_l

        best = max(best, go_left, go_right)

        return go_left, go_right

    dfs(root)
    return best


def sum_of_distances_in_tree(n: int, edges: list[list[int]]) -> list[int]:
    """
    LeetCode:
        834. Sum of Distances in Tree

    Rerooting DP.

    First pass postorder:
        count[v] = subtree size
        ans[0] = sum distances from root 0 to all nodes

    Second pass preorder reroot:
        When moving root from v to child:
            nodes in child's subtree get 1 closer: count[child]
            all other nodes get 1 farther: n - count[child]

        ans[child] = ans[v] - count[child] + (n - count[child])
    """
    g = [[] for _ in range(n)]

    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    count = [1] * n
    ans = [0] * n

    def post(v: int, parent: int) -> None:
        for w in g[v]:
            if w == parent:
                continue

            post(w, v)
            count[v] += count[w]
            ans[v] += ans[w] + count[w]

    def reroot(v: int, parent: int) -> None:
        for w in g[v]:
            if w == parent:
                continue

            ans[w] = ans[v] - count[w] + (n - count[w])
            reroot(w, v)

    post(0, -1)
    reroot(0, -1)

    return ans


# =============================================================================
# Level 7 — Graph / DAG DP
# =============================================================================


def longest_increasing_path(matrix: list[list[int]]) -> int:
    """
    LeetCode:
        329. Longest Increasing Path in a Matrix

    Treat each cell as a DAG vertex.
    Edge from cell to larger-valued neighbor.

    S:
        dfs(r,c) = longest increasing path starting at cell.

    R:
        1 + max(dfs(larger neighbor))

    T:
        DFS memo over acyclic value-increasing graph.

    Complexity:
        O(rows * cols)
    """
    rows = len(matrix)
    cols = len(matrix[0])

    @cache
    def dfs(r: int, c: int) -> int:
        best = 1

        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr = r + dr
            nc = c + dc

            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))

        return best

    return max(dfs(r, c) for r in range(rows) for c in range(cols))


def cheapest_flight_with_k_stops(
    n: int,
    flights: list[list[int]],
    src: int,
    dst: int,
    k: int,
) -> int:
    """
    LeetCode:
        787. Cheapest Flights Within K Stops

    This is bounded-edge shortest path DP.

    S:
        dist[v] after using at most step edges.

    R:
        relax all flights from previous layer only.

    T:
        increasing number of edges from 0 to k+1.

    B:
        dist[src] = 0

    O:
        dist[dst] after k+1 edges.

    Trap:
        Must use a copy per layer; in-place relaxation allows too many stops.
    """
    dist = [inf] * n
    dist[src] = 0

    for _ in range(k + 1):
        nxt = dist[:]

        for u, v, price in flights:
            if dist[u] != inf:
                nxt[v] = min(nxt[v], dist[u] + price)

        dist = nxt

    return -1 if dist[dst] == inf else int(dist[dst])


def most_similar_path(
    n: int,
    roads: list[list[int]],
    names: list[str],
    target_path: list[str],
) -> list[int]:
    """
    LeetCode:
        1548. The Most Similar Path in a Graph

    S:
        dp[i][v] = min edit distance for target_path[:i+1]
                  ending at city v at position i.

    R:
        dp[i][v] = cost(v at i) + min(dp[i-1][u] for u adjacent to v)

    T:
        increasing path index i.

    B:
        dp[0][v] = mismatch cost at first target.

    O:
        min_v dp[m-1][v], reconstruct path with parent.
    """
    g = [[] for _ in range(n)]

    for a, b in roads:
        g[a].append(b)
        g[b].append(a)

    m = len(target_path)
    dp = [[inf] * n for _ in range(m)]
    parent = [[-1] * n for _ in range(m)]

    for v in range(n):
        dp[0][v] = 0 if names[v] == target_path[0] else 1

    for i in range(1, m):
        for v in range(n):
            cost = 0 if names[v] == target_path[i] else 1

            for u in g[v]:
                candidate = dp[i - 1][u] + cost

                if candidate < dp[i][v]:
                    dp[i][v] = candidate
                    parent[i][v] = u

    end = min(range(n), key=lambda v: dp[m - 1][v])
    path = []

    for i in range(m - 1, -1, -1):
        path.append(end)
        end = parent[i][end]

    path.reverse()
    return path


def largest_path_value(colors: str, edges: list[list[int]]) -> int:
    """
    LeetCode:
        1857. Largest Color Value in a Directed Graph

    Need:
        Detect cycle. If cycle exists, return -1.

    DAG DP:
        dp[v][color] = max count of color on any path ending at v.

    T:
        Kahn topological order.

    R:
        propagate dp[v] to neighbors.
    """
    n = len(colors)
    g = [[] for _ in range(n)]
    indeg = [0] * n

    for a, b in edges:
        g[a].append(b)
        indeg[b] += 1

    q = deque(i for i in range(n) if indeg[i] == 0)
    dp = [[0] * 26 for _ in range(n)]
    seen = 0
    best = 0

    while q:
        v = q.popleft()
        seen += 1

        color = ord(colors[v]) - ord("a")
        dp[v][color] += 1
        best = max(best, dp[v][color])

        for w in g[v]:
            for c in range(26):
                dp[w][c] = max(dp[w][c], dp[v][c])

            indeg[w] -= 1

            if indeg[w] == 0:
                q.append(w)

    return best if seen == n else -1


def minimum_time_parallel_courses(n: int, relations: list[list[int]], time: list[int]) -> int:
    """
    LeetCode:
        2050. Parallel Courses III

    DAG longest path.

    S:
        finish[v] = earliest finish time of course v.

    R:
        finish[next] = max(finish[next], finish[v] + time[next])

    T:
        topological order.

    B:
        source courses finish at own duration.

    O:
        max(finish)
    """
    g = [[] for _ in range(n)]
    indeg = [0] * n

    for prev, nxt in relations:
        prev -= 1
        nxt -= 1
        g[prev].append(nxt)
        indeg[nxt] += 1

    finish = time[:]
    q = deque(i for i in range(n) if indeg[i] == 0)

    while q:
        v = q.popleft()

        for w in g[v]:
            finish[w] = max(finish[w], finish[v] + time[w])
            indeg[w] -= 1

            if indeg[w] == 0:
                q.append(w)

    return max(finish)


# =============================================================================
# Part 11 Maps and Diagnostic Checklist
# =============================================================================


PART_11_PROBLEM_MAP = {
    "bitmask_assignment_dp": [
        1879,
        1066,
    ],
    "bitmask_team_cover_dp": [
        1125,
    ],
    "bitmask_path_tsp_dp": [
        847,
        943,
    ],
    "bitmask_pairing_game_dp": [
        1799,
    ],
    "digit_dp": [
        233,
        357,
        600,
        902,
        1012,
    ],
    "tree_dp": [
        124,
        337,
        834,
        968,
        1372,
    ],
    "graph_dag_dp": [
        329,
        787,
        1548,
        1857,
        2050,
    ],
}


ADVANCED_STATE_DIAGNOSTIC_CHECKLIST = [
    "Is the state an index, mask, digit position, tree node, graph vertex, or step-layer?",
    "For bitmask DP, does dp[mask] need a terminal dimension like last?",
    "For digit DP, do we need tight, started, previous digit, used mask, or count state?",
    "For tree DP, what value must be returned to the parent?",
    "Is there also a global answer separate from the returned value?",
    "For rerooting, is one postorder pass enough, or do we need a preorder pass?",
    "For graph DP, is the graph acyclic? If not, is there a bounded step dimension or shortest-path algorithm?",
    "What is the topological order: mask increasing, digit position, postorder, Kahn order, or BFS layer?",
    "What are the terminal states and answer extraction rules?",
    "Is the complexity exponential, pseudo-polynomial, or linear in edges/states?",
]


if __name__ == "__main__":
    assert minimum_xor_sum([1, 2], [2, 3]) == 2
    assert assignment_min_cost([[1, 2], [2, 1]]) == 2

    team = smallest_sufficient_team(
        ["java", "nodejs", "reactjs"],
        [["java"], ["nodejs"], ["nodejs", "reactjs"]],
    )
    assert set(team) == {0, 2}

    assert shortest_path_visiting_all_nodes([[1, 2, 3], [0], [0], [0]]) == 4
    assert shortest_superstring(["alex", "loves", "leetcode"]) in {
        "alexlovesleetcode",
        "leetcodelovesalex",
        "lovesalexleetcode",
        "alexleetcodeloves",
        "leetcodealexloves",
        "lovesleetcodealex",
    }

    assert max_score_after_n_operations([1, 2]) == 1

    assert count_without_consecutive_ones(5) == 5
    assert at_most_n_given_digit_set(["1", "3", "5", "7"], 100) == 20
    assert count_numbers_with_unique_digits(2) == 91
    assert num_dup_digits_at_most_n(20) == 1
    assert count_digit_one(13) == 6

    root = TreeNode(3, TreeNode(2, None, TreeNode(3)), TreeNode(3, None, TreeNode(1)))
    assert rob_tree(root) == 7

    max_path_root = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert binary_tree_max_path_sum(max_path_root) == 42

    assert min_camera_cover(TreeNode(0, TreeNode(0, TreeNode(0), TreeNode(0)))) == 1
    assert longest_zigzag(TreeNode(1, None, TreeNode(1, TreeNode(1), TreeNode(1)))) == 2
    assert sum_of_distances_in_tree(6, [[0, 1], [0, 2], [2, 3], [2, 4], [2, 5]]) == [8, 12, 6, 10, 10, 10]

    assert longest_increasing_path([[9, 9, 4], [6, 6, 8], [2, 1, 1]]) == 4
    assert cheapest_flight_with_k_stops(
        4,
        [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]],
        0,
        3,
        1,
    ) == 700

    path = most_similar_path(
        5,
        [[0, 2], [0, 3], [1, 2], [1, 3], [1, 4], [2, 4]],
        ["ATL", "PEK", "LAX", "DXB", "HND"],
        ["ATL", "DXB", "HND", "LAX"],
    )
    assert len(path) == 4

    assert largest_path_value("abaca", [[0, 1], [0, 2], [2, 3], [3, 4]]) == 3
    assert largest_path_value("a", [[0, 0]]) == -1
    assert minimum_time_parallel_courses(3, [[1, 3], [2, 3]], [3, 2, 5]) == 8
