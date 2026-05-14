"""

2476. Closest Nodes Queries in a Binary Search Tree
Attempted
Medium

You are given the root of a binary search tree and an array queries of size n consisting of positive integers.

Find a 2D array answer of size n where answer[i] = [mini, maxi]:

mini is the largest value in the tree that is smaller than or equal to queries[i]. If a such value does not exist, add -1 instead.
maxi is the smallest value in the tree that is greater than or equal to queries[i]. If a such value does not exist, add -1 instead.
Return the array answer.



Example 1:


Input: root = [6,2,13,1,4,9,15,null,null,null,null,null,null,14], queries = [2,5,16]
Output: [[2,2],[4,6],[15,-1]]
Explanation: We answer the queries in the following way:
- The largest number that is smaller or equal than 2 in the tree is 2, and the smallest number that is greater or equal than 2 is still 2. So the answer for the first query is [2,2].
- The largest number that is smaller or equal than 5 in the tree is 4, and the smallest number that is greater or equal than 5 is 6. So the answer for the second query is [4,6].
- The largest number that is smaller or equal than 16 in the tree is 15, and the smallest number that is greater or equal than 16 does not exist. So the answer for the third query is [15,-1].
Example 2:


Input: root = [4,null,9], queries = [3]
Output: [[-1,4]]
Explanation: The largest number that is smaller or equal to 3 in the tree does not exist, and the smallest number that is greater or equal to 3 is 4. So the answer for the query is [-1,4].


Constraints:

The number of nodes in the tree is in the range [2, 105].
1 <= Node.val <= 106
n == queries.length
1 <= n <= 105
1 <= queries[i] <= 106

Seen this question in a real interview before?
1/6
Yes
No
Accepted
39,438/88.7K
Acceptance Rate
44.4%

"""
from bisect import *
from typing import List, Optional, Iterable, Iterator


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def partition(queries: List[int], val: int):
    less, equal, more = [], [], []

    for i, q in queries:
        if q < val: less.append((i, q))
        if q == val: equal.append((i, q))
        if q > val: more.append((i, q))
    return less, equal, more

def floors_tree(root: Optional[TreeNode], queries: List[int]) -> List[tuple[int, TreeNode]]:
    if root is None:
        return [(i, None) for i, q in queries]

    less, equal, more = partition(queries, root.val)

    left, here, right = \
    (
        floors_tree(root.left, less),
        [(i, root) for i, _ in equal],
        floors_tree(root.right, more)
    )

    right = [(i, better or root) for i, better in right]

    return left + here + right

def ceils_tree(root: Optional[TreeNode], queries: List[int]) -> List[tuple[int, TreeNode]]:
    if root is None:
        return [(i, None) for i, q in queries]

    less, equal, more = partition(queries, root.val)

    left, here, right = \
    (
        ceils_tree(root.left, less),
        [(i, root) for i, _ in equal],
        ceils_tree(root.right, more)
    )

    left = [(i, better or root) for i, better in left]

    return left + here + right


def ivalues(inodes: Iterable[TreeNode]) -> List[tuple[int, int]]:
    return [((i, node.val) if node else (i, -1)) for i, node in inodes]

def closest_inodes(root: Optional[TreeNode], queries: List[int]) -> List[List[int]]:
    fs = sorted(ivalues(floors_tree(root, enumerate(queries))))
    cs = sorted(ivalues(ceils_tree(root, enumerate(queries))))

    return [[u[1], v[1]] for u, v in zip(fs, cs)]


def inorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return

    yield from inorder(root.left)
    yield root
    yield from inorder(root.right)

def values(nodes: Iterable[TreeNode]):
    return [node.val for node in nodes]

def floor(vals: List[int], q: int):
    i = bisect_right(vals, q) - 1
    return vals[i] if i >= 0 else -1

def ceil(vals: List[int], q: int):
    i = bisect_left(vals, q)
    return vals[i] if i < len(vals) else -1


def floors(vals: List[int], qs: List[int]):
    return [floor(vals, q) for q in qs]

def ceils(vals: List[int], qs: List[int]):
    return [ceil(vals, q) for q in qs]

def closest(root: Optional[TreeNode], qs: List[int]):
    vals = values(inorder(root))
    return [[lo, hi] for lo, hi in zip(floors(vals, qs), ceils(vals, qs))]

class Solution:
    def closestNodes(self, root: Optional[TreeNode], queries: List[int]) -> List[List[int]]:
        return closest(root, queries)
