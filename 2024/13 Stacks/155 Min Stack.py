
from collections import deque

class MinStack:

    def __init__(self):
        self.dq, self.min = deque(), float('inf')

    def push(self, val: int) -> None:
        self.min = min(val, self.min)
        self.dq.append((val, self.min))

    def pop(self) -> None:
        self.dq.pop()
        if self.dq:
            self.min = self.topm
        else:
            self.min = float('inf')

    @property
    def topp(self) -> (int, int):
        return self.dq[-1]

    @property
    def topv(self) -> int:
        return self.topp[0]

    @property
    def topm(self) -> int:
        return self.topp[1]

    def top(self) -> int:
        return self.topp[0]

    def getMin(self) -> int:
        return self.topm








    