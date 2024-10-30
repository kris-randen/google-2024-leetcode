from collections.abc import Iterable, Sequence
from typing import Optional, TypeVar, Generic, Union, Tuple, Iterator
from collections import deque
from functools import reduce

T = TypeVar('T')

class fudeq(Sequence, Generic[T]):
    """
    A custom double-ended queue (deque) implementation that supports efficient
    append and appendleft operations, pattern matching, and more.

    Attributes:
        __data (deque): Internal deque to store elements of the fudeq.
    """

    def __init__(self, data: Optional[Iterable[T]] = None):
        """
        Initializes the fudeq with an optional iterable of data.

        Args:
            data (Optional[Iterable[T]]): Initial data to populate the fudeq. Defaults to None.
        """
        self.__data = deque(data) if data else deque()

    def __getitem__(self, index: int) -> T:
        """
        Prevents direct retrieval by index, raises an error.

        Args:
            index (int): Index to access.

        Raises:
            NotImplementedError: Always raised to prevent direct access by index.
        """
        raise NotImplementedError("Direct indexing is not supported for fudeq.")

    def __setitem__(self, index: int, value: T) -> None:
        """
        Prevents direct setting of value by index, raises an error.

        Args:
            index (int): Index of the item to set.
            value (T): Value to set at the index.

        Raises:
            NotImplementedError: Always raised to prevent setting value by index.
        """
        raise NotImplementedError("Direct indexing for setting values is not supported for fudeq.")

    def __iter__(self) -> Iterator[T]:
        """
        Returns an iterator over the fudeq.

        Returns:
            Iterator[T]: Iterator over the fudeq.
        """
        return iter(self.__data)

    def __len__(self) -> int:
        """
        Returns the length of the fudeq.

        Returns:
            int: Length of the fudeq.
        """
        return len(self.__data)

    def __add__(self, other: 'fudeq[T]') -> 'fudeq[T]':
        """
        Concatenates two fudeqs.

        Args:
            other (fudeq[T]): The fudeq to concatenate with.

        Returns:
            fudeq[T]: A new fudeq with the combined elements.
        """
        return fudeq(self.__data + other.__data)

    def appendleft(self, item: T) -> None:
        """
        Inserts an item at the beginning of the fudeq.

        Args:
            item (T): The item to insert.
        """
        self.__data.appendleft(item)

    def append(self, item: T) -> None:
        """
        Appends an item to the end of the fudeq.

        Args:
            item (T): The item to append.
        """
        self.__data.append(item)

    def unc(self) -> Tuple[Optional[T], 'fudeq[T]']:
        """
        Uncons (extracts) the first element and the rest of the fudeq.

        Returns:
            Tuple[Optional[T], fudeq[T]]: The first element and the rest of the fudeq.
        """
        if not self.__data:
            return None, fudeq()
        first = self.__data.popleft()
        return first, self

    def uns(self) -> Tuple['fudeq[T]', Optional[T]]:
        """
        Unsnocs (extracts) the last element and the rest of the fudeq.

        Returns:
            Tuple[fudeq[T], Optional[T]]: The rest of the fudeq and the last element.
        """
        if not self.__data:
            return fudeq(), None
        last = self.__data.pop()
        return self, last

    def pr(self) -> Optional[T]:
        """
        Pops and returns the last element of the fudeq.

        Returns:
            Optional[T]: The last element of the fudeq, or None if fudeq is empty.
        """
        return self.__data.pop() if self.__data else None

    def pl(self) -> Optional[T]:
        """
        Pops and returns the first element of the fudeq.

        Returns:
            Optional[T]: The first element of the fudeq, or None if fudeq is empty.
        """
        return self.__data.popleft() if self.__data else None

    def __pos__(self) -> Tuple[Optional[T], 'fudeq[T]']:
        """
        Overloads the unary `+` operator to perform the `unc` operation.

        Returns:
            Tuple[Optional[T], fudeq[T]]: The first element and the rest of the fudeq.
        """
        return self.unc()

    def __neg__(self) -> Tuple['fudeq[T]', Optional[T]]:
        """
        Overloads the unary `-` operator to perform the `uns` operation.

        Returns:
            Tuple[fudeq[T], Optional[T]]: The rest of the fudeq and the last element.
        """
        return self.uns()

    def __truediv__(self, other: T) -> 'fudeq[T]':
        """
        Overloads the `/` operator to prepend an item to the fudeq using appendleft.

        Args:
            other (T): The item to prepend.

        Returns:
            fudeq[T]: The fudeq with the item prepended.
        """
        self.append(other)
        return self

    def __rtruediv__(self, other: T) -> 'fudeq[T]':
        """
        Overloads the `/` operator to prepend an item to the fudeq using appendleft.

        Args:
            other (T): The item to prepend.

        Returns:
            fudeq[T]: The fudeq with the item prepended.
        """
        self.appendleft(other)
        return self

    def __repr__(self) -> str:
        """
        Returns a string representation of the fudeq.

        Returns:
            str: String representation of the fudeq.
        """
        return f"fudeq({list(self.__data)})"

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the fudeq.

        Returns:
            str: String representation of the fudeq.
        """
        return str(list(self.__data))

    def __eq__(self, other: object) -> bool:
        """
        Compares this fudeq with another for equality.

        Args:
            other (object): The other fudeq to compare with.

        Returns:
            bool: True if both fudeqs are equal, False otherwise.
        """
        if isinstance(other, fudeq):
            return self.__data == other.__data
        return False

    def __delitem__(self, index: int) -> None:
        """
        Raises an error if an attempt is made to delete an item from the fudeq.

        Args:
            index (int): Index of the item to delete.

        Raises:
            NotImplementedError: Always raised to prevent deletion.
        """
        raise NotImplementedError("Item deletion is not supported for fudeq.")

    def __contains__(self, item: T) -> bool:
        """
        Checks if an item is contained in the fudeq.

        Args:
            item (T): The item to check for.

        Returns:
            bool: True if the item is in the fudeq, False otherwise.
        """
        return item in self.__data

    def __reversed__(self) -> 'fudeq[T]':
        """
        Returns a reversed version of the fudeq.

        Returns:
            fudeq[T]: A new fudeq with elements in reverse order.
        """
        return fudeq(reversed(self.__data))

def add(p, q, c=0):
    rsum = p + q + c
    return rsum % 10, rsum // 10

def add_df(vf, d):
    match (vf, d):
        case ([], 0): return fudeq()
        case ([], d): return fudeq([d])
        case _:
            d, c = add(vf.pr(), d)
            return add_df(vf, c) / d

def add_ffc(uf, vf, d):
    match (uf, vf):
        case ([], _): return add_df(vf, d)
        case (_, []): return add_df(uf, d)
        case _:
            d, c = add(uf.pr(), vf.pr(), d)
            return add_ffc(uf, vf, c) / d

def add_ff(uf, vf):
    return add_ffc(uf, vf, 0)
def add_ffs(vfs):
    return reduce(add_ff, vfs)
def sf(vs):
    return fudeq(int(v) for v in vs)
def fs(vf):
    return ''.join(str(v) for v in vf)
def add_fss(vss):
    return fs(add_ffs(sf(vs) for vs in vss))

if __name__ == '__main__':
    uf = fudeq([2, 3, 5, 1])
    print(uf)
    vf = uf / 17
    print(vf)
    wf = 23 / uf
    print(wf)
    vss = ['1234', '23']
    print(add_fss(vss))
