"""

1490. Clone N-ary Tree
Solved
Medium

Given a root of an N-ary tree, return a deep copy (clone) of the tree.

Each node in the n-ary tree contains a val (int) and a list (List[Node]) of its children.

class Node {
    public int val;
    public List<Node> children;
}
Nary-Tree input serialization is represented in their level order traversal, each group of children is separated by the null value (See examples).



Example 1:



Input: root = [1,null,3,2,4,null,5,6]
Output: [1,null,3,2,4,null,5,6]
Example 2:



Input: root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]
Output: [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]


Constraints:

The depth of the n-ary tree is less than or equal to 1000.
The total number of nodes is between [0, 104].


Follow up: Can your solution work for the graph problem?

"""

from __future__ import annotations
from typing import Optional, List

# Definition for a Node.
class Node:
    def __init__(self, val: Optional[int] = None, children: Optional[List['Node']] = None):
        self.val = val
        self.children = children if children is not None else []


def clone_tree(root: Optional[Node]) -> Optional[Node]:
    if not root:
        return None

    clone = {None: None}

    def dfs(p: Optional[Node]) -> Optional[Node]:
        if p in clone:
            return clone[p]

        copy = Node(p.val)
        clone[p] = copy

        for child in p.children:
            copy.children.append(dfs(child))

        return copy

    dfs(root)
    return clone[root]


class Solution:
    def cloneTree(self, root: Optional[Node]) -> Optional[Node]:
        return clone_tree(root)