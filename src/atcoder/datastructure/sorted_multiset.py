"""Sorted Multiset"""
# https://github.com/tatyam-prime/SortedSet/blob/main/SortedMultiset.py
import math
from bisect import bisect_left, bisect_right
from typing import Generic, Iterable, Iterator, Protocol, TypeVar


class Comparable(Protocol):
    """`T`が比較可能であることを示すためのクラス (mypy用)"""
    def __lt__(self: "T", other: "T") -> bool:
        """`self` < `other`"""
        ...
    def __gt__(self: "T", other: "T") -> bool:
        """`self` > `other`"""
        ...
    def __le__(self: "T", other: "T") -> bool:
        """`self` <= `other`"""
        ...
    def __ge__(self: "T", other: "T") -> bool:
        """`self` >= `other`"""
        ...

T = TypeVar("T", bound=Comparable)

class SortedMultiset(Generic[T]):
    """Sorted Multiset

    Attributes:
        array: 元の配列
        _sizes: 配列のサイズ

    Notes:
        - 参考：https://github.com/tatyam-prime/SortedSet/blob/main/SortedMultiset.py
        - Pypy可
    """
    BUCKET_RATIO = 16
    SPLIT_RATIO = 24

    def __init__(self, array: Iterable[T] = []) -> None:
        """Make a new SortedMultiset from iterable. / O(N) if sorted / O(N log N)"""
        array = list(array)
        n = self._size = len(array)
        if any(array[i] > array[i + 1] for i in range(n - 1)):
            array.sort()
        num_bucket = int(math.ceil(math.sqrt(n / self.BUCKET_RATIO)))
        self.array = [array[n * i // num_bucket : n * (i + 1) // num_bucket] for i in range(num_bucket)]

    def __iter__(self) -> Iterator[T]:
        """Iter."""
        for i in self.array:
            yield from i

    def __reversed__(self) -> Iterator[T]:
        """Reversed."""
        for i in reversed(self.array):
            yield from reversed(i)

    def __eq__(self, other) -> bool:  # noqa: ANN001
        """Eq."""
        return list(self) == list(other)

    def __len__(self) -> int:
        """Len."""
        return self._size

    def __repr__(self) -> str:
        """Repr."""
        return "SortedMultiset" + str(self.array)

    def __str__(self) -> str:
        """Str."""
        s = str(list(self))
        return "{" + s[1 : len(s) - 1] + "}"

    def _position(self, x: T) -> tuple[list[T], int, int]:
        """Return the bucket, index of the bucket and position in which x should be. self must not be empty."""
        for i, a in enumerate(self.array):  # noqa: B007
            if x <= a[-1]:
                break
        return (a, i, bisect_left(a, x))

    def __contains__(self, x: T) -> bool:
        """Contains."""
        if self._size == 0:
            return False
        a, _, i = self._position(x)
        return i != len(a) and a[i] == x

    def count(self, x: T) -> int:
        """要素`x`の個数数える O(√N)"""
        return self.index_right(x) - self.index(x)

    def add(self, x: T) -> None:
        """`x`を追加 O(√N)"""
        if self._size == 0:
            self.array = [[x]]
            self._size = 1
            return
        a, b, i = self._position(x)
        a.insert(i, x)
        self._size += 1
        if len(a) > len(self.array) * self.SPLIT_RATIO:
            mid = len(a) >> 1
            self.array[b:b+1] = [a[:mid], a[mid:]]

    def _pop(self, a: list[T], b: int, i: int) -> T:
        ans = a.pop(i)
        self._size -= 1
        if not a:
            del self.array[b]
        return ans

    def discard(self, x: T) -> bool:
        """要素`x`を除去（除去されたら`True`を返す） O(√N)"""
        if self._size == 0:
            return False
        a, b, i = self._position(x)
        if i == len(a) or a[i] != x:
            return False
        self._pop(a, b, i)
        return True

    def lt(self, x: T) -> T | None:
        """`x`未満で最大の要素を返す（存在しないときは`None`） O(√N)"""
        for a in reversed(self.array):
            if a[0] < x:
                return a[bisect_left(a, x) - 1]
        return None

    def le(self, x: T) -> T | None:
        """`x`以下で最大の要素を返す（存在しないときは`None`） O(√N)"""
        for a in reversed(self.array):
            if a[0] <= x:
                return a[bisect_right(a, x) - 1]
        return None

    def gt(self, x: T) -> T | None:
        """`x`より真に大きい最小の要素を返す（存在しないときは`None`） O(√N)"""
        for a in self.array:
            if a[-1] > x:
                return a[bisect_right(a, x)]
        return None

    def ge(self, x: T) -> T | None:
        """`x`以上で最小の要素を返す（存在しないときは`None`） O(√N)"""
        for a in self.array:
            if a[-1] >= x:
                return a[bisect_left(a, x)]
        return None

    def __getitem__(self, i: int) -> T:
        """Return the i-th element."""
        if i < 0:
            for a in reversed(self.array):
                i += len(a)
                if i >= 0:
                    return a[i]
        else:
            for a in self.array:
                if i < len(a):
                    return a[i]
                i -= len(a)
        raise IndexError

    def pop(self, i: int = -1) -> T:
        """`index`番目(0-indexed)の要素をpop & return  O(√N)"""
        if i < 0:
            for b, a in enumerate(reversed(self.array)):
                i += len(a)
                if i >= 0:
                    return self._pop(a, ~b, i)
        else:
            for b, a in enumerate(self.array):
                if i < len(a):
                    return self._pop(a, b, i)
                i -= len(a)
        raise IndexError

    def index(self, x: T) -> int:
        """`x`未満の要素数を返す（`x`を挿入するなら`x`のindexは？同じなら左に） O(√N)"""
        ans = 0
        for a in self.array:
            if a[-1] >= x:
                return ans + bisect_left(a, x)
            ans += len(a)
        return ans

    def index_right(self, x: T) -> int:
        """`x`以下の要素数を返す（`x`を挿入するなら`x`のindexは？同じなら右に） O(√N)"""
        ans = 0
        for a in self.array:
            if a[-1] > x:
                return ans + bisect_right(a, x)
            ans += len(a)
        return ans
