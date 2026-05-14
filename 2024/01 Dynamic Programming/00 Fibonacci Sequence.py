from functools import reduce
from itertools import islice


def fibs():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def elem(n, gen):
    pass


fib = lambda n: next(islice(fibs(), n, None))


def get_r(n, gen):
    reduce(lambda _, __: next(gen), range(n), 0)


def fibb(n, memo={0: 0, 1: 1}):
    if n in memo: return memo[n]
    memo[n] = fibb(n - 1) + fibb(n - 2)
    return memo[n]

if __name__ == '__main__':
    print(fibb(500))
