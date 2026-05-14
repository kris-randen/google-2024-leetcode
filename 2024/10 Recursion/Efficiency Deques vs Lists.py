
import random
import timeit

from functools import reduce
from collections import deque
from memory_profiler import profile

import sys

# Increase recursion limit
sys.setrecursionlimit(2300)

def generate_test_data(size, length):
    """Generate a list of random strings, each representing a number with 'length' digits."""
    return [''.join(random.choices('0123456789', k=length)) for _ in range(size)]


@profile
def memory_test_lss():
    test_data = generate_test_data(size=50, length=50)  # Smaller data size
    add_lss(test_data)


@profile
def memory_test_qss():
    test_data = generate_test_data(size=50, length=50)  # Smaller data size
    add_qss(test_data)


def test_efficiency():
    # Generate test data
    size = 1000  # Larger number of numbers
    length = 2000  # Larger number of digits in each number

    # Timing add_lss (list-based)
    list_time = timeit.timeit(
        stmt="add_lss(data)",
        setup="from __main__ import add_lss, generate_test_data; data = generate_test_data({}, {})".format(size, length),
        globals=globals(),
        number=10
    )

    # Timing add_qss (deque-based)
    deque_time = timeit.timeit(
        stmt="add_qss(data)",
        setup="from __main__ import add_qss, generate_test_data; data = generate_test_data({}, {})".format(size, length),
        globals=globals(),
        number=10
    )

    print(f"Time taken by add_lss (using lists): {list_time} seconds")
    print(f"Time taken by add_qss (using deques): {deque_time} seconds")

def add(d1, d2, *args):
    rsum = d1 + d2 + sum(args)
    return rsum % 10, rsum // 10

def add_dq(vq, c):
    if not vq: return deque() if not c else deque([c])
    d, carry = add(c, vq.pop())
    (res := add_dq(vq, carry)).append(d)
    return res

def add_qqc(uq, vq, c):
    if not uq: return add_dq(vq, c)
    if not vq: return add_dq(uq, c)
    d, carry = add(uq.pop(), vq.pop(), c)
    (res := add_qqc(uq, vq, carry)).append(d)
    return res

def add_qq(uq, vq): return add_qqc(uq, vq, 0)
def add_qqs(vqs): return reduce(add_qq, vqs)
def sd(vs): return deque(int(v) for v in vs)
def ds(vq): return ''.join(str(v) for v in vq)

def add_qss(vss):
    return ds(
                add_qqs(
                            (sd(vs) for vs in vss)
                       )
             )


def add_dl(vl, c):
    if not vl: return [] if not c else [c]
    d, carry = add(c, vl[0])
    return [d] + add_dl(vl[1:], carry)

def add_llc(ul, vl, c):
    if not ul: return add_dl(vl, c)
    if not vl: return add_dl(ul, c)
    d, carry = add(ul[0], vl[0], c)
    return [d] + add_llc(ul[1:], vl[1:], carry)

def add_ll(ul, vl): return add_llc(ul, vl, 0)

def add_lls(vls): return reduce(add_ll, vls)

def sl(vs): return [int(v) for v in vs]
def ls(vl): return ''.join([str(v) for v in vl])

def add_lss(vss):
    return ls(
                add_lls(
                            [sl(vs)[::-1] for vs in vss]
                       )
             )[::-1]


if __name__ == '__main__':
    test_efficiency()
    memory_test_lss()
    memory_test_qss()