"""

Palindrome Linked List

Statement
Given the head of a linked list, your task is to check whether the linked list is a palindrome or not. Return TRUE if the linked list is a palindrome; otherwise, return FALSE.

Note: The input linked list prior to the checking process should be identical to the list after the checking process has been completed.

"""

from functools import reduce

class Node:
    def __init__(self, data, nxt=None):
        self.data, self.next = data, nxt

    def __iter__(self):
        self.curr = self
        while self.curr:
            yield self.curr
            self.curr = self.curr.next

    def set_next(self, node):
        self.next = node
        return self

    def __str__(self):
        return ' -> '.join(f'{node.data}' for node in self)

def list_to_node(vs):
    return reduce(lambda n, v: Node(v).set_next(n), reversed(vs), None)

def equal(l, r):
    if not l: return not r or not r.next
    if not r: return not l or not l.next
    return (l.data == r.data) and equal(l.next, r.next)


def reverse(l):
    if not l or not l.next: return l, l
    h, t = reverse(l.next)
    t.next = l; l.next = None
    return h, l


def mid(l):
    if not l: return l
    s, f = l, l
    while f.next and f.next.next:
        s = s.next
        f = f.next.next
    r = s.next; s.next = None
    return l, r

def palindrome(h):
    first, second = mid(h)
    return equal(first, reverse(second)[0])

if __name__ == '__main__':
    # vs = [12, 13, 11, 11, 13, 12]
    vs = [1, 2, 3, 2, 1]
    nvs = list_to_node(vs)
    # rnvs = reverse(nvs)
    # print(rnvs[0])


    # mnvs = mid(nvs)
    # print(mnvs[0])
    # print(mnvs[1])
    # rmnvs = reverse(mnvs[1])[0]
    # print(rmnvs)
    # print(f'equality {equal(rmnvs, mnvs[0])}')

    print(palindrome(nvs))
