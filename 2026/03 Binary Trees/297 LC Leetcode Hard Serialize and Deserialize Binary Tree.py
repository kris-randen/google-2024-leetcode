"""

297. Serialize and Deserialize Binary Tree
Hard

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

Clarification: The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.



Example 1:


Input: root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]
Example 2:

Input: root = []
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 104].
-1000 <= Node.val <= 1000

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,199,475/2M
Acceptance Rate
60.7%

"""

from typing import Optional, Iterator, List, Iterable


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


NULL = "#"
SEP = ","

def preorder_tokens(root: Optional[TreeNode]) -> Iterator[str]:
    if root is None:
        yield NULL
        return

    yield str(root.val)
    yield from preorder_tokens(root.left)
    yield from preorder_tokens(root.right)

def tree_from_tokens(tokens: Iterator[str]) -> Optional[TreeNode]:
    token = next(tokens)

    if token == NULL:
        return None

    root = TreeNode(int(token))
    root.left = tree_from_tokens(tokens)
    root.right = tree_from_tokens(tokens)
    return root

def encode(tokens: Iterator[str]) -> str:
    return SEP.join(tokens)

def decode(data: str) -> Iterator[str]:
    return iter(data.split(SEP))

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        return encode(preorder_tokens(root))



    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        return tree_from_tokens(decode(data))

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))

