"""

92. Reverse Linked List II
Medium

Given the head of a singly linked list and two integers left and right where left <= right, reverse the nodes of the list from position left to position right, and return the reversed list.

Example 1:


Input: head = [1,2,3,4,5], left = 2, right = 4
Output: [1,4,3,2,5]
Example 2:

Input: head = [5], left = 1, right = 1
Output: [5]


Follow up: Could you do it in one pass?

"""

class ListNode:
    def __init__(self, val=0, node=None):
        self.val = val; self.next = node

    def __iter__(self):
        self.cur = self
        while self.cur:
            yield self.cur
            self.cur = self.cur.next

def rev_k(n, k):
    def base(n, k): return not n or not n.next or not k or k == 1
    def rev_kr(n, k):
        if base(n, k): return n, n
        h, t = rev_kr(n.next, k - 1)
        n.next = t.next; t.next = n
        return h, n
    return rev_kr(n, k)[0]

def get(n, i):
    if not n or i == 1: return n
    return get(n.next, i - 1)

def rev_lr(n, l, r):
    if l == 1: return rev_k(n, r - l + 1)
    ln = get(n, l - 1)
    ln.next = rev_k(ln.next, r - l + 1)
    return n

