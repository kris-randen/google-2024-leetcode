from collections import namedtuple

class Node:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

    @staticmethod
    def getn(x: 'Node', k):
        match x:
            case Node(val=key, left=l, right=r):
                if k == key:
                    return x
                elif k < key:
                    return Node.getn(x.left, k)
                else:
                    return Node.getn(x.right, k)

    @staticmethod
    def set(x: 'Node', k):
        match x:
            case None:
                x = Node(k)
            case Node(val=key, left=l, right=r):
                if k == key: x.val = k
                elif k < key:
                    x.left = Node.set(x.left, k)
                else:
                    x.right = Node.set(x.right, k)
        return x

    @staticmethod
    def floor(x: 'Node', k):

        pass