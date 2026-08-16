# Linked List
# Level 0 | Traversal and Testing Primitives
from functools import reduce


class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val, self.next = val, nxt

    def __iter__(self):
        node = self

        while node:
            nxt = node.nxt
            yield node
            node = nxt


def iter_nodes(head):
    return iter(head) if head else iter(())

def iter_values(head):
    return (node.val for node in iter_nodes(head))

def list_nodes(head):
    return list(iter_nodes(head))

def list_values(head):
    return list(iter_values(head))

def cons(node, nxt):
    node.nxt = nxt
    return node

def chain(nodes):
    return reduce(
        lambda nxt, node: cons(node, nxt),
        reversed(nodes),
        None
    )

def link(values):
    return chain([ListNode(v) for v in values])

# Level 1 | Pointer Atoms

def detach_front(head):
    target = head.next
    head.next = None
    return head, target

def attach_after(tail, node):
    tail.next = node
    return node

def delete_after(prev):

    pass
