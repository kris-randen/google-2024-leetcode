"""

2471. Minimum Number of Operations to Sort a Binary Tree by Level
Solved
Medium
Topics
Companies
Hint
You are given the root of a binary tree with unique values.

In one operation, you can choose any two nodes at the same level and swap their values.

Return the minimum number of operations needed to make the values at each level sorted in a strictly increasing order.

The level of a node is the number of edges along the path between it and the root node.



Example 1:


Input: root = [1,4,3,7,6,8,5,null,null,null,null,9,null,10]
Output: 3
Explanation:
- Swap 4 and 3. The 2nd level becomes [3,4].
- Swap 7 and 5. The 3rd level becomes [5,6,8,7].
- Swap 8 and 7. The 3rd level becomes [5,6,7,8].
We used 3 operations so return 3.
It can be proven that 3 is the minimum number of operations needed.
Example 2:


Input: root = [1,3,2,7,6,5,4]
Output: 3
Explanation:
- Swap 3 and 2. The 2nd level becomes [2,3].
- Swap 7 and 4. The 3rd level becomes [4,6,5,7].
- Swap 6 and 5. The 3rd level becomes [4,5,6,7].
We used 3 operations so return 3.
It can be proven that 3 is the minimum number of operations needed.
Example 3:


Input: root = [1,2,3,4,5,6]
Output: 0
Explanation: Each level is already sorted in increasing order so return 0.


Constraints:

The number of nodes in the tree is in the range [1, 105].
1 <= Node.val <= 105
All the values of the tree are unique.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
23.3K
Submissions
37.4K
Acceptance Rate
62.3%

"""

from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def vmap(vs):
    return {v: i for i, v in enumerate(sorted(vs))}


def rvmap(vs, vm):
    return [vm[v] for v in vs]


def swaps(rv):
    c = 0
    for i, r in enumerate(rv):
        if not i == r: rv[i], rv[r] = rv[r], rv[i]; c += 1
    return c


def misp(rve):
    return any([not i == r for i, r in rve])


def vops(vs):
    rv = rvmap(vs, vmap(vs)); c = 0
    while misp(enumerate(rv)): c += swaps(rv)
    return c


def vopsc(vs):
    rv = rvmap(vs, vmap(vs))
    visited = [False] * len(rv)
    swap_count = 0

    for i in range(len(rv)):
        if visited[i] or rv[i] == i:
            continue

        cycle_length = 0
        j = i
        while not visited[j]:
            visited[j] = True
            j = rv[j]
            cycle_length += 1

        if cycle_length > 1:
            swap_count += cycle_length - 1

    return swap_count


def bfs(node):
    frontier = [[node]]
    for nds in frontier:
        nxt = [
                child for nd in nds
                for child in (nd.left, nd.right)
                if child
              ]
        if nxt: frontier.append(nxt)
    return [[nd.val for nd in nds] for nds in frontier]


def tops(node):
    return sum(vops(vs) for vs in bfs(node))


class Solution:
    def minimumOperations(self, root: Optional[TreeNode]) -> int:
        if not root: return 0
        return tops(root)
