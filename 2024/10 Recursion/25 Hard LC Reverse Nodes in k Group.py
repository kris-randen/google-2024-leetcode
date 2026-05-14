"""

25. Reverse Nodes in k-Group
Solved
Hard
Topics
Companies
Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.



Example 1:


Input: head = [1,2,3,4,5], k = 2
Output: [2,1,4,3,5]
Example 2:


Input: head = [1,2,3,4,5], k = 3
Output: [3,2,1,4,5]


Constraints:

The number of nodes in the list is n.
1 <= k <= n <= 5000
0 <= Node.val <= 1000


Follow-up: Can you solve the problem in O(1) extra memory space?

Seen this question in a real interview before?
1/5
Yes
No
Accepted
993K
Submissions
1.7M
Acceptance Rate
59.9%

Runtime 828 ms Beats 5.31%
Memory 17.62 MB Beats 8.21%

"""

# def reverse_k_r(head, k):
#     def reverse_k_rr(node, k):
#         if not node or not node.next: return node, node
#         head, toe = reverse_k_rr(node.next, k - 1)
#         node.next = toe.next; toe.next = node
#         return head, node
#     # if k == 1 or k == 0: return head
#     if k == 1: return head
#     return reverse_k_rr(head, k)[0]


def length(head): return reduce(lambda l, n: 1 + l, head, 0)

def tail(node):
    if not node or not node.next: return node
    return tail(node.next)


def reverse_kk(head, k):
    def reverse_kk_rec(node, k):
        if k == 0: return node, node.toe
        if k == 1: return node, node.toe
        nhead, ntail = reverse_kk_rec(node.next, k - 1)
        node.next = ntail.next
        ntail.next = node
        return nhead, node
    return reverse_kk_rec(head, k)


def reverse_k_group(node, k):
    khead, ktail = reverse_kk(node, k)
    if length(node) <= k: return khead
    ktail.next = reverse_k_group(ktail.next, k)
    return khead


# def length(head): reduce(lambda l, n: 1 + l, head, 0)
def toel(head): return reduce(lambda p, q: q.next, head, None)

def list_to_nodes(vs):
    return reduce(lambda n, v: ListNode(v).set_next(n), reversed(vs), None)







from functools import reduce


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, node=None):
        self.val = val
        self.next = node

    def __iter__(self):
        self.curr = self
        while self.curr:
            yield self.curr
            self.curr = self.curr.next

    def set_next(self, node):
        self.next = node
        return self

    def __str__(self):
        return ' -> '.join(str(n.val) for n in self)

    def __repr__(self):
        return self.__str__()

    @property
    def length(self):
        return reduce(lambda l, n: 1 + l, self, 0)

    @property
    def toe(self):
        return reduce(lambda p, q: q, self, None)

def rev_k(head, k):
    def base(n, k):
        return not n or not n.next or not k or k == 1
    def rev_kr(n, k):
        if base(n, k):return n, n, k
        h, t, k = rev_kr(n.next, k - 1)
        n.next = t.next; t.next = n
        return h, n, k
    h, t, l = rev_kr(head, k)
    if l > 1: return rev_kr(h, length(h))[0]
    return h




if __name__ == '__main__':
    vs = [i + 1 for i in range(10)]
    lnvs = list_to_nodes(vs)

    rlnvs_5 = rev_k(lnvs, 5)
    print(f'rlnvs 5 = {rlnvs_5}')
    lnvs = list_to_nodes(vs)

    rlnvs_4 = rev_k(lnvs, 4)
    print(f'rlnvs 4 = {rlnvs_4}')
    lnvs = list_to_nodes(vs)

    rlnvs_0 = rev_k(lnvs, 0)
    print(f'rlnvs 0 = {rlnvs_0}')
    lnvs = list_to_nodes(vs)

    rlnvs_1 = rev_k(lnvs, 1)
    print(f'rlnvs 1 = {rlnvs_1}')
    lnvs = list_to_nodes(vs)

    rlnvs_16 = rev_k(lnvs, 16)
    print(f'rlnvs 16 = {rlnvs_16}')
    lnvs = list_to_nodes(vs)