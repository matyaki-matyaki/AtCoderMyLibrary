"""セグメントツリー"""
from typing import Callable, Generic, TypeVar

# SegmentTreeの要素のタイプ
T = TypeVar("T")
class SegmentTree(Generic[T]):
    """SegmentTree

    Attributes:
        _array: 元の配列
        _func: 演算
        _unit: 単位元
        _n: 元の配列の長さ
        _height: 木の深さ
        _n_leaf: 完全二分木の葉の数（= 葉以外の頂点数 - 1）
        _t: 完全二分木の要素(_d[0]は使わない)

    Note:
        - 参考：https://github.com/not522/ac-library-python/blob/master/atcoder/segtree.py#L18
        - 演算と単位元
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
    """
    def __init__(self, array: list[T], func: Callable[[T, T], T], unit: T) -> None:
        """Init. O(n)

        Args:
            array (list[T]): セグメントツリーに乗せるリスト
            func (Callable[[T, T], T]): 演算
            unit (T): 単位元
        """
        self._array = array
        self._func = func
        self._unit = unit
        self._n = len(self._array)
        self._height = (self._n - 1).bit_length()
        self._n_leaf = 1 << self._height
        self._t = [self._unit] * (self._n_leaf << 1) # 葉の数 x 2で完全二分木を構築できる (index 0は使わない)
        for i in range(self._n):
            self._t[self._n_leaf + i] = self._array[i] # 元の配列値を葉に格納
        for i in range(self._n_leaf - 1, 0, -1):
            self._update_value(i) # 深い方からセグメントツリーを構築

    def set_value(self, index: int, value: T) -> None:
        """`index`番目の値を`value`で更新 O(log n)"""
        assert 0 <= index < self._n
        index += self._n_leaf
        self._t[index] = value
        for i in range(1, self._height + 1):
            self._update_value(index >> i) # 深い方からセグメントツリーを更新

    def get_value(self, index: int) -> T:
        """`index`番目の値を取得 O(1)"""
        assert 0 <= index < self._n
        return self._t[index + self._n_leaf]

    def query(self, left: int, right: int) -> T:
        """`func([left, right))`の値を取得（左閉右開区間に注意） O(log n)"""
        assert 0 <= left <= right <= self._n
        from_left = self._unit
        from_right = self._unit
        left += self._n_leaf
        right += self._n_leaf
        while left < right:
            if left & 1: # leftが奇数のとき，頂点leftは右の子
                from_left = self._func(from_left, self._t[left])
                left += 1
            if right & 1: # rightが奇数のとき，頂点right-1は左の子
                from_right = self._func(self._t[right - 1], from_right)
                right -= 1
            left >>= 1
            right >>= 1
        return self._func(from_left, from_right)

    def query_all(self) -> T:
        """`func(array)`を計算 O(1)"""
        return self._t[1]

    def max_right(self, left: int, is_satisfied: Callable[[T], bool]) -> int:
        """次の条件を満たす`right`を返す（存在しないときは'n'を返す）

        `func(unit)`, `func([left, left + 1))`, ..., `func([left, right))`は`is_satisfied`を満たすが，\
        `func([left, right + 1))`は満たさないような`right`
        """
        assert 0 <= left <= self._n
        assert is_satisfied(self._unit)

        if left == self._n:
            return self._n

        left += self._n_leaf
        prod_true = self._unit # Trueとなることが確定した区間の総積

        first = True
        # 1回目でなく，かつleftが2べきになったら終了（2べきのときfunc([l, N]）を計算している）
        while first or (left & -left) != left:
            first = False
            while not (left & 1): # while left % 2 == 0
                left >>= 1 # 右の子になるまで親に登る
            if not is_satisfied(self._func(prod_true, self._t[left])): # このleftの子孫のどこかでFalseになる
                while left < self._n_leaf: # 葉に至る前まで
                    left <<= 1
                    if is_satisfied(self._func(prod_true, self._t[left])):
                        prod_true = self._func(prod_true, self._t[left])
                        left += 1 # 左の子まではTrueなので右の子（とその子孫を確認）
                return left - self._n_leaf
            prod_true = self._func(prod_true, self._t[left])
            left += 1
        return self._n

    def min_left(self, right: int, is_satisfied: Callable[[T], bool]) -> int:
        """次の条件を満たす`left`を返す（存在しないときは`0`を返す）

        `func(uint)`, `func([right - 1, right))`, ..., 'func([left, right))'は`is_satisfied`を満たすが，\
        `func([left - 1, right))`は満たさないような`left`
        """
        assert 0 <= right <= self._n
        assert is_satisfied(self._unit)

        if right == 0:
            return 0

        right += self._n_leaf
        prod_true = self._unit

        first = True
        while first or (right & -right) != right:
            first = False
            right -= 1
            while right > 1 and (right & 1):
                right >>= 1
            if not is_satisfied(self._func(self._t[right], prod_true)):
                while right < self._n_leaf:
                    right = (right << 1) + 1
                    if is_satisfied(self._func(self._t[right], prod_true)):
                        prod_true = self._func(self._t[right], prod_true)
                        right -= 1
                return right + 1 - self._n_leaf
            prod_true = self._func(self._t[right], prod_true)

        return 0

    def _update_value(self, index: int) -> None:
        """セグメントツリーの`index`番目の要素を子を用いて更新"""
        self._t[index] = self._func(self._t[index << 1], self._t[(index << 1) + 1])


if __name__ == "__main__":
    """動作確認"""
    # https://atcoder.jp/contests/practice2/tasks/practice2_j
    N, Q = map(int, input().split())
    A = list(map(int, input().split()))

    # SegmentTreeの構築
    segtree = SegmentTree(A, max, -1)

    for _ in range(Q):
        t, arg1, arg2 = map(int, input().split())
        match t:
            case 1:
                X, V = arg1 - 1, arg2
                segtree.set_value(X, V)
            case 2:
                L, R = arg1 - 1, arg2
                print(segtree.query(L, R))
            case 3:
                X, V = arg1 - 1, arg2
                def is_satisfied(seg_val: int, V: int = V) -> bool:
                    """条件式"""
                    return seg_val < V
                print(segtree.max_right(X, is_satisfied) + 1)
