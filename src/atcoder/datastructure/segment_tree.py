"""セグ木"""
import math
import operator
from typing import Callable, Literal, Self


class SegmentTree:
    """SegmentTree.

    - 計算量
        - 構築：O(n log n)
        - 値の更新：O(log n)
        - 区間積取得：O(log n)
    - 演算と関連する関数、単位元
        演算          |python関数              |単位元
        --------------------------------------------------
        和            operator.add             0
        積            operator.mul             1
        最小値         min                      float('inf')
        最大値         max                      -float('inf')
        最大公約数      math.gcd                 0
        最小公倍数      x * y // math.gcd(x, y)  1
        AND           operator.and_            1
        OR            operator.or_             0
        XOR           operator.xor             0
    - すべて0-indexed
    """
    def __init__(  # noqa: C901, PLR0915
        self: Self,
        array: list[int],
        method: Literal["ADD", "MUL", "MIN", "MAX", "GCD", "LCM", "AND", "OR", "XOR"] | None,
        func: Callable[[int, int], int] | None = None,
        unit: int | None = None,
    ) -> None:
        """Init.

        Args:
            array (list[T]): セグ木に乗せる配列
            method (Literal["ADD", "MUL", "MIN", "MAX", "GCD", "LCM", "AND", "OR", "XOR"] | None): 演算
            func (Callable[[T, T], T] | None, optional): 演算に用いる関数. Defaults to None.
            unit (T | None, optional): 単位元. Defaults to None.
        """
        self.array = array
        if method is None:
            assert func is not None
            assert unit is not None
        else:
            match method:
                case "ADD":
                    func = operator.add
                    unit = 0
                case "MUL":
                    func = operator.mul
                    unit = 1
                case "MIN":
                    func = min
                    unit = max(self.array)
                case "MAX":
                    func = max
                    unit = min(self.array)
                case "GCD":
                    func = math.gcd
                    unit = 0
                case "LCM":
                    def func(x: int, y: int) -> int:
                        return x * y // math.gcd(x, y)
                    unit = 1
                case "AND":
                    func = operator.and_
                    unit = 1
                case "OR":
                    func = operator.or_
                    unit = 0
                case "XOR":
                    func = operator.xor
                    unit = 0
                case _:
                    msg = f"Unknown method: {method}."
                    raise ValueError(msg)
        self.func, self.unit = self.parse(method, func, unit)
        self.n = len(self.array)
        self.func = func
        self.unit = unit
        self.log = (self.n - 1).bit_length()
        self.size = 1 << self.log
        self.d = [self.unit for i in range(2 * self.size)]
        for i in range(self.n):
            self.d[self.size + i] = array[i]
        for i in range(self.size - 1, 0, -1):
            self.update(i)

        def parse(
            self: self.Self,
            method: str | None,
            func: Callable[[int, int], int] | None,
            unit: int | None,
        ) -> tuple[Callable[[int, int], int], int]:
            if method is None:
                assert func is not None
                assert unit is not None
            else:
                match method:
                    case "ADD":
                        func = operator.add
                        unit = 0
                    case "MUL":
                        func = operator.mul
                        unit = 1
                    case "MIN":
                        func = min
                        unit = max(self.array)
                    case "MAX":
                        func = max
                        unit = min(self.array)
                    case "GCD":
                        func = math.gcd
                        unit = 0
                    case "LCM":
                        def func(x: int, y: int) -> int:
                            return x * y // math.gcd(x, y)
                        unit = 1
                    case "AND":
                        func = operator.and_
                        unit = 1
                    case "OR":
                        func = operator.or_
                        unit = 0
                    case "XOR":
                        func = operator.xor
                        unit = 0
                    case _:
                        msg = f"Unknown method: {method}."
                        raise ValueError(msg)
            return func, unit


        def set(self: Self, index: int, value: float) -> None:
            """`index`番目(0-indexed)の値を`value`で更新"""
            assert 0 <= index < self.n
            index += self.size
            self.d[index] = value
            for i in range(1, self.log + 1):
                self.update(index >> i)

        def get(self: Self, index: int) -> float:
            """`index`番目(0-indexed)の値を取得"""
            assert 0 <= index < self.n
            return self.d[index + self.size]

        def query(self: Self, left: int, right: int) -> float:
            assert 0 <= left <= right <= self.n
            sml = self.unit
            smr = self.unit
            left += self.size
            right += self.size
            while left < right:
                if left & 1:
                    sml = self.func(sml, self.d[left])
                    left += 1
                if right & 1:
                    smr = self.func(self.d[right - 1], smr)
                    right -= 1
                left >>= 1
                right >>= 1
            return self.func(sml, smr)
