from collections import namedtuple, deque

Pair = namedtuple('Pair', ['key', 'val'])
Range = namedtuple('Range', ['lo', 'hi'])

class Node:
    def __init__(self, key, val=0, left: 'Node' = None, right: 'Node' = None, count=1):
        self.key, self.val, self.count = key, val, count
        self.left, self.right = left, right

    @staticmethod
    def size(x):
        return 0 if not x else x.count

    @staticmethod
    def pair(x):
       return (
                Pair(key=None, val=None)
                if not x else
                Pair(key=x.key, val=x.val)
              )

    @staticmethod
    def get(x: 'Node', key) -> 'Node':
        match x:
            case Node(key=k, left=lt, right=rt):
                if key == k:
                    return x
                if key < k:
                    return Node.get(lt, key)
                if key > k:
                    return Node.get(rt, key)

    @staticmethod
    def getkv(x: 'Node', key) -> Pair:
        return Node.pair(Node.get(x, key))

    @staticmethod
    def set(x: 'Node', key, val):
        match Node.get(x, key):
            case node:
                old, node.val = node.val, val
                return old

    @staticmethod
    def update(x: 'Node'):
        x.count = 1 + \
                  Node.size(x.left) + \
                  Node.size(x.right)

    @staticmethod
    def put(x: 'Node', key, val):
        match x:
            case None:
                return Node(key, val)
            case Node(key=k, left=lt, right=rt):
                if key == k:
                    x.val = val
                if key < k:
                    x.left = Node.put(lt, key, val)
                if key > k:
                    x.right = Node.put(rt, key, val)
        Node.update(x)
        return x

    @staticmethod
    def floor(x: 'Node', key):
        match x:
            case Node(key=k, left=lt, right=rt):
                if key == k:
                    return x
                if key < k:
                    return Node.floor(lt, key)
                if key > k:
                    return Node.floor(rt, key) or x

    @staticmethod
    def floorkv(x: 'Node', key) -> Pair:
        return Node.pair(Node.floor(x, key))

    @staticmethod
    def ceil(x: 'Node', key):
        match x:
            case Node(key=k, left=lt, right=rt):
                if key == k:
                    return x
                if key < k:
                    return Node.ceil(lt, key) or x
                if key > k:
                    return Node.ceil(rt, key)

    @staticmethod
    def ceilkv(x: 'Node', key) -> Pair:
        return Node.pair(Node.ceil(x, key))

    @staticmethod
    def rank(x: 'Node', key):
        match x:
            case None:
                return 0
            case Node(key=k, left=lt, right=rt):
                if key < k:
                    return Node.rank(lt, key)
                if key == k:
                    return Node.size(lt)
                if key > k:
                    return 1 + Node.size(lt) + Node.rank(rt, key)

    @staticmethod
    def select(x: 'Node', rank):
        match x:
            case Node(left=lt, right=rt):
                r = Node.size(lt)
                if rank == r:
                    return x
                if rank < r:
                    return Node.select(lt, rank)
                if rank > r:
                    return Node.select(rt, rank - (1 + r))

    @staticmethod
    def selectkv(x: 'Node', rank):
        return Node.pair(Node.select(x, rank))

    @staticmethod
    def count(x: 'Node', lo, hi):
        return (
                Node.rank(x, hi) - Node.rank(x, lo) +
                (1 if Node.get(x, hi) else 0)
               )

    @staticmethod
    def inside(k, lo, hi):
        return lo <= k <= hi

    @staticmethod
    def range(x: 'Node', lo, hi):
        def impl(x: 'Node', lo, hi, dq: deque):
            match x:
                case Node(key=k, left=lt, right=rt):
                    if lo < k: impl(lt, lo, hi, dq)
                    if lo <= k <= hi: dq.append(x)
                    if hi > k: impl(rt, lo, hi, dq)
        impl(x, lo, hi, (dq := deque()))
        return dq

    @staticmethod
    def pairs(x: 'Node', lo, hi):
        return [Node.pair(y) for y in Node.range(x, lo, hi)]

    @staticmethod
    def keys(x: 'Node', lo, hi):
        return [y.key for y in Node.range(x, lo, hi)]

    @staticmethod
    def vals(x: 'Node', lo, hi):
        return [y.val for y in Node.range(x, lo, hi)]

    @staticmethod
    def min(x: 'Node'):
        match x:
            case Node(key=k, left=lt):
                return min(k, Node.min(lt))
            case None:
                return float('inf')

    @staticmethod
    def max(x: 'Node'):
        match x:
            case Node(key=k, right=rt):
                return max(k, Node.max(rt))
            case None:
                return float('-inf')

    @staticmethod
    def inorder(x: 'Node'):
        def impl(x: 'Node', dq: deque):
            match x:
                case Node(left=lt, right=rt):
                    impl(lt, dq)
                    dq.append(x)
                    impl(rt, dq)
        impl(x, (dq := deque()))
        return dq

    @staticmethod
    def preorder(x: 'Node'):
        def impl(x: 'Node', dq: deque):
            match x:
                case Node(left=lt, right=rt):
                    dq.append(x)
                    impl(lt, dq)
                    impl(rt, dq)
        impl(x, (dq := deque()))
        return dq

    @staticmethod
    def postorder(x: 'Node'):
        def impl(x: 'Node', dq: deque):
            match x:
                case Node(left=lt, right=rt):
                    impl(lt, dq)
                    impl(rt, dq)
                    dq.append(x)
        impl(x, (dq := deque()))
        return dq

    @staticmethod
    def levelorder(x: 'Node'):
        def impl(x: 'Node', dq: deque):

            pass

class Tree:
    def __init__(self, root=None):
        self.root = root

    def get(self, key):
        return Node.getkv(self.root, key).key

    def __getitem__(self, key):
        return self.get(key)

    def set(self, key, val):
        return Node.set(self.root, key, val)

    def __setitem__(self, key, val):
        return self.set(key, val)

    def size(self):
        return Node.size(self.root)

    def put(self, key, val):
        self.root = Node.put(self.root, key, val)

    def floor(self, key):
        return Node.floorkv(self.root, key).key

    def ceil(self, key):
        return Node.ceilkv(self.root, key).key

    def rank(self, key):
        return Node.rank(self.root, key)

    def select(self, rank):
        return Node.selectkv(self.root, rank).key

    def count(self, lo, hi):
        return Node.count(self.root, lo, hi)

    def lh(self, lo, hi):
        return lo if lo else self.min(), hi if hi else self.max()

    def pairs(self, lo, hi):
        lo, hi = self.lh(lo, hi)
        return Node.pairs(self.root, lo, hi)

    def keys(self, lo=None, hi=None):
        lo, hi = self.lh(lo, hi)
        return [p.key for p in self.pairs(lo, hi)]

    def vals(self, lo=None, hi=None):
        lo, hi = self.lh(lo, hi)
        return [p.val for p in self.pairs(lo, hi)]

    def min(self):
        return Node.min(self.root)

    def max(self):
        return Node.max(self.root)

    def inorder(self):
        return [y.key for y in Node.inorder(self.root)]

    def preorder(self):
        return [y.key for y in Node.preorder(self.root)]

    def postorder(self):
        return Node.postorder(self.root)



if __name__ == '__main__':
    vs = [2, 3, 5, 7, 9]
    root = Node(5)
    root.left = Node(3)
    root.right = Node(7)
    root.left.left = Node(2)
    root.right.right = Node(9)
    tree = Tree(root)
    print(tree.inorder())
    print(tree.preorder())
    root = Node(3)
    root.left = Node(2)
    root.right = Node(5)
    root.right.right = Node(9)
    root.right.right.left = Node(7)
    tree = Tree(root)
    print(tree.inorder())
    root = Node(9)
    root.left = Node(7)
    root.left.left = Node(5)
    root.left.left.left = Node(3)
    root.left.left.left.left = Node(2)
    tree = Tree(root)
    print(tree.inorder())
    print(tree[5])
    print(Node.getkv(None, 5))