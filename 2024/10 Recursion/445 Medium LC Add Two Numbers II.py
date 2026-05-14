"""

445. Add Two Numbers II
Medium
Topics
Companies
You are given two non-empty linked lists representing two non-negative integers. The most significant digit comes first and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.



Example 1:


Input: l1 = [7,2,4,3], l2 = [5,6,4]
Output: [7,8,0,7]
Example 2:

Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [8,0,7]
Example 3:

Input: l1 = [0], l2 = [0]
Output: [0]

"""

# from functools import reduce
# from collections import deque

class ListNode:
    def __init__(self, val=0, succ=None):
        self.val = val
        self.next = succ

    def set_next(self, node):
        self.next = node
        return self

    def __iter__(self):
        self.curr = self
        while self.curr:
            yield self.curr
            self.curr = self.curr.next

    def __str__(self):
        # ss = []
        # for node in self: ss += [f'{node.val}']
        # return ' -> '.join(ss)
        return ' -> '.join(str(node.val) for node in self)


def ne(node: ListNode):
    return [] if not node else [node.val]


def nodes_to_list(node):
    return reduce(lambda l, n: l + [n.val], node, [])


def list_to_nodes(vs):
    return reduce(lambda n, v: ListNode(v).set_next(n), reversed(vs), None)




# def add(d1, d2, *args):
#     rsum = d1 + d2 + sum(args)
#     return rsum % 10, rsum // 10

# def add_dl(vl, c):
#     if not vl: return [] if not c else [c]
#     d, carry = add(c, v := vl.popleft())
#     return [d] + add_dl(vl, carry)
#
# def add_llc(ul, vl, c):
#     if not ul: return add_dl(vl, c)
#     if not vl: return add_dl(ul, c)
#     d, carry = add(ul[0], vl[0], c)
#     return [d] + add_llc(ul[1:], vl[1:], carry)
#
# def add_ll(ul, vl): return add_llc(ul, vl, 0)
#
# def add_lls(vls): return reduce(add_ll, vls)
#
# def sl(vs): return [int(v) for v in vs]
# def ls(vl): return ''.join([str(v) for v in vl])
#
# def add_lss(vss):
#     return ls(
#         add_lls(
#             [sl(vs)[::-1] for vs in vss]
#         )
#     )[::-1]

from functools import reduce
from collections import deque

def add(d1, d2, *args):
    rsum = d1 + d2 + sum(args)
    return rsum % 10, rsum // 10

def add_dl(vl, c):
    if not vl: return deque() if not c else deque([c])
    d, carry = add(c, vl.pop())
    (res := add_dl(vl, carry)).append(d)
    return res

def add_llc(ul, vl, c):
    if not ul: return add_dl(vl, c)
    if not vl: return add_dl(ul, c)
    d, carry = add(ul.pop(), vl.pop(), c)
    (res := add_llc(ul, vl, carry)).append(d)
    return res

def add_ll(ul, vl): return add_llc(ul, vl, 0)
def add_lls(vls): return reduce(add_ll, vls)
def sd(vs): return deque(int(v) for v in vs)
def ds(vl): return ''.join(str(v) for v in vl)

def add_lss(vss):
    return ds(
                add_lls(
                            (sd(vs) for vs in vss)
                       )
             )


if __name__ == '__main__':
    vs = [2, 3, 4]
    ws = [5, 6, 2, 11, 3, 6, 2, 9, 8, 7, 7, 9, 4, 4, 9]
    nvs = list_to_nodes(vs)
    nws = list_to_nodes(ws)
    print(nvs)
    print(nws)
    # str(nvs)
    # for n in nvs: print(n.val)
    # us = nodes_to_list(nvs)
    # print(us)
    # vss = deque([2, 5, 7])
    # print(add(2, v := vss.popleft()))
    # print(vss)
    # print(uss := deque(1 for _ in range(5)))
    # print(ds(uss))
    # kss = ['123', '0']
    # print(add_lss(kss))