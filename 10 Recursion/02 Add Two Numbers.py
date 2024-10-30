"""

2. Add Two Numbers
Solved
Medium
Topics
Companies
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example 1:
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.

Example 2:
Input: l1 = [0], l2 = [0]
Output: [0]

Example 3:
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]


Constraints:

The number of nodes in each linked list is in the range [1, 100].
0 <= Node.val <= 9
It is guaranteed that the list represents a number that does not have leading zeros.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
4.8M
Submissions
11M
Acceptance Rate
43.7%

Runtime 49 ms Beats 85.69%
Memory 16.61 MB Beats 23.73%

"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def adds(l1, l2, carry):
    if not l1 and not l2: return None if not carry else ListNode(carry)
    l1v, l2v = (0 if not l1 else l1.val), (0 if not l2 else l2.val)
    nl1, nl2 = (None if not l1 else l1.next), (None if not l2 else l2.next)
    val = l1v + l2v + carry
    node = ListNode(val % 10)
    node.next = adds(nl1, nl2, val // 10)
    return node

# Approach below is preferable as it has a nice symmetry doesn't involve optional checking of values for each list.

def add_nn(u, v, carry):
    def add_dd(p, q):
        return (p + q) % 10, (p + q) // 10

    def add_dn(d, v):
        if not v: return None if not d else ListNode(d)
        d, carry = add_dd(d, v.val); nd = ListNode(d)
        nd.next = add_dn(carry, v.next)
        return nd

    if not u: return add_dn(carry, v)
    if not v: return add_dn(carry, u)
    d, carry = add_dd(u.val + v.val, carry); nd = ListNode(d)
    nd.next = add_nn(u.next, v.next, carry)
    return nd




# Now let's do add for numbers expressed as strings
# First we reverse the strings and convert them into a list of digits
# We reverse because it's easy and more natural to iteratre forward
# Finally we reverse the result and join it as a string and return it
# So first we just define addition on a lists of digits

# def add_ll(ul, vl, carry):
#     def add_dd(p, q, *argv):
#         rsum = p + q + sum(argv)
#         return rsum % 10, rsum // 10
#
#     def add_dl(d, vl):
#         if not vl: return [] if not d else [d]
#         d, carry = add_dd(d, vl[0])
#         return [d] + add_dl(carry, vl[1:])
#
#     if not ul: return add_dl(carry, vl)
#     if not vl: return add_dl(carry, ul)
#     d, carry = add_dd(ul[0], vl[0], carry)
#     return [d] + add_ll(ul[1:], vl[1:], carry)

# Notice the almost complete similarity of the above with that of addition of numbers using a linked list. The only difference is instead of None we return the empty list and instead of node.next we do list concatenation instead

# Now the strings part is easy. First reverse the strings. Convert them to lists add the lists and then convert the result to a string and reverse the string before returning

# We don't need a separate function for reversing a list we can say s[::-1] and that will give us the reversed string

# def sl(s):
#     return [int(n) for n in s]
#
# def ls(l):
#     return ''.join([str(n) for n in l])
#
# def add_ss(us, vs, carry):
#     return ls(add_ll(sl(us[::-1]), sl(vs[::-1]), carry))[::-1]

# Now let's do multiplication. Note the following 2 things:
# 1. We will need to split the multiplication into similar chunks like we did for addition:
 # a. Multiply two digits with a carry along
 # b. Multiply a digit with a list of digits
 # c. Finally use the two above to multiply two lists of digits
# 2. The addition functions we wrote can be reused as is for doing the additions. But we'll rewrite them anyway for practice

# The algorithm we use for multiplication is the one taught most commonly in schools. You start from the end and start multiply the last digit of second number with the first. Then the second last but we add a zero at the end because now this is a second digit which means it's a mutliple of 10. And similarly go forward adding subsequent zeros at the end as the digits are multiples of higher powers of 10.

# So notice it's extremely useful again to have the two number lists reversed for easier compute. We have to remember to eventually reverse the result before returning

from functools import reduce
from collections import namedtuple

Sum = namedtuple('sum', ['d', 'carry'])
LDigit = namedtuple('listdigit', ['carry', 'vl', 'l'])


def add(p, q, *args):
    rsum = p + q + sum(args)
    return Sum(rsum % 10, rsum // 10)

def add_dl(c, vl):
    if not vl: return [] if not c else [c]
    d, carry = add(c, vl[0])
    return [d] + add_dl(carry, vl[1:])


def add_ll(ul, vl, c):
    if not ul: return add_dl(c, vl)
    if not vl: return add_dl(c, ul)
    d, carry = add(ul[0], vl[0], c)
    return [d] + add_ll(ul[1:], vl[1:], carry)


def add_ss(us, vs):
    def sl(vs): return [int(v) for v in vs]
    def ls(vl): return ''.join([str(v) for v in vl])
    return ls(add_ll(sl(us)[::-1], sl(vs)[::-1], 0)[::-1])


def add_lls(vls):
    def add_llc(ul, vl, carry):
        def add_dl(d, vl):
            if not vl: return [] if not d else [d]
            rsum = add(d, vl[0])
            return [rsum.d] + add_dl(rsum.carry, vl[1:])

        if not ul: return add_dl(carry, vl)
        if not vl: return add_dl(carry, ul)
        d, carry = add(ul[0] + vl[0], carry)
        return [d] + add_llc(ul[1:], vl[1:], carry)

    def add_ll(ul, vl): return add_llc(ul, vl, 0)

    return reduce(add_ll, vls)

# Neither of the lists can be empty because that would be absurd and we leave that exception checking to the caller. But either of the numbers can be zero. And zero could be [0] or [0, 0, ..] any length of a sequence of zeros would represent zero. Let's add a small helper function to check this

# We'll collect a list of number lists through this process and add all of them. So let's write the addition functions above that can add two lists but also reduce a collection / list of lists and add them all. And by similarity of convention we take the second number vl to iterate the digits.

# Also let's try to write the for loop using a map / comprehension instead

def mult_lls(vls):
    def mult_ll(ul, vl):
        def mult_dd(p, q, carry):
            return ((p * q) + carry) % 10, ((p * q) + carry) // 10

        def mult_dl(d, vl, carry):
            if not vl: return [] if not carry else [carry]
            p, carry = mult_dd(d, vl[0], carry)
            return [p] + mult_dl(d, vl[1:], carry)

        return add_lls(
            [
                [0] * i + mult_dl(v, ul, 0)
                for i, v in enumerate(vl)
            ]
        )

    def zero(vls):
        def zero(vl):
            def zero(v): return v == 0
            return all(map(zero, vl))
        return any(map(zero, vls))

    if zero(vls): return [0]

    return reduce(mult_ll, vls)

# Now let's take a list of numbers given to us in string form and multiply them all. For each number we first reverse it convert it to a list of digits (ints). Multiply all those list numbers and then take the result and reverse it before returning

def mult_sss(vss):
    def sl(vs): return [int(v) for v in vs]

    def ls(vl): return ''.join([str(v) for v in vl])

    return ls(mult_lls([sl(vs[::-1]) for vs in vss])[::-1])


if __name__ == '__main__':
    us = '123'
    vs = '2345'
    ws = '1'
    print(add_ss(us, vs))