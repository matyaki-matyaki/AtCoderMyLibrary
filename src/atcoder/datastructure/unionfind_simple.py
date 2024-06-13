"""Normal UnionFind"""
from collections import defaultdict
from typing import Self


class UnionFindSimple:
    """単純なUnionFind

    - 頂点数nは事前に指定
    - 頂点：0 ~ n-1までの整数
    - 出典：https://note.nkmk.me/python-union-find/

    Attributes:
    ----------
        n (int): 頂点数
        parents (list): 各要素の親要素の番号を格納するリストで、要素が根の場合は-(そのグループの要素数)を格納

    """

    def __init__(self: Self, n: int) -> None:
        """Init.

        Args:
            n (int): 頂点数
        """
        self.n = n
        self.parents = [-1] * n

    def find_root(self: Self, x: int) -> int:
        """頂点xが属するグループの根（いなければxが根）"""
        if self.parents[x] < 0:
            return x
        self.parents[x] = self.find_root(self.parents[x])
        return self.parents[x]

    def union(self: Self, x: int, y: int) -> None:
        """頂点xと頂点yのグループを結合"""
        x = self.find_root(x)
        y = self.find_root(y)
        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def size(self: Self, x: int) -> int:
        """頂点xの属するグループのサイズ（要素数）"""
        return -self.parents[self.find_root(x)]

    def is_same(self: Self, x: int, y: int) -> bool:
        """頂点xと頂点yが同じグループに属するか"""
        return self.find_root(x) == self.find_root(y)

    def members(self: Self, x: int) -> list:
        """頂点xが属するグループに属する要素"""
        root = self.find_root(x)
        return [i for i in range(self.n) if self.find_root(i) == root]

    def roots(self: Self) -> list:
        """すべての根"""
        return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self: Self) -> int:
        """連結成分の数"""
        return len(self.roots())

    def all_group_members(self: Self) -> defaultdict:
        """{根: [そのグループに含まれる要素のリスト]}のdefaultdict"""
        group_members = defaultdict(list)
        for member in range(self.n):
            group_members[self.find_root(member)].append(member)
        return group_members

    def __str__(self: Self) -> str:
        """print用"""
        return "\n".join(f"{r}: {m}" for r, m in self.all_group_members().items())
