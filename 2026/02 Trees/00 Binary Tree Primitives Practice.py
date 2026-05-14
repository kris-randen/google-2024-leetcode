

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def is_leaf(node):
    return \
        (
            node is not None and
            node.left is None and
            node.right is None
        )

def children(node):
    if node.left:
        yield node.left
    if node.right:
        yield node.right

def preorder_nodes(root):
    if root is None:
        return

    yield root
    yield from preorder_nodes(root.left)
    yield from preorder_nodes(root.right)

def inorder_nodes(root):
    if root is None:
        return

    yield from inorder_nodes(root.left)
    yield root
    yield from inorder_nodes(root.right)

def postorder_nodes(root):
    if root is None:
        return

    yield from postorder_nodes(root.left)
    yield from postorder_nodes(root.right)
    yield root


def preorder_values(root):
    return (node.val for node in preorder_nodes(root))

