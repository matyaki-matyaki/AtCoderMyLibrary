"""自由度の高いUnionFind"""
from collections import defaultdict
from typing import Generic, Self, TypeVar

# UnionFindFreeの要素のタイプ
T = TypeVar("T")
class UnionFindFree(Generic[T]):
    """自由度の高いUnionFind

    - 頂点数を予め指定しない
    - 集合の要素として文字列やtupleがok
    - 自由度が高い代償として、計算時間とメモリ消費が悪い
    - 出典：https://qiita.com/tomato1997/items/7c001c2a9a1e7f428241

    Attributes:
    ----------
        parents (dict[T, int]): {子要素: 親ID}のdict
        members_set (defaultdict[T, set[T]]): {根: 根に属する要素集合}のdefaultdict
        roots_set (set): 根の集合
        key2ID (dict): {要素: ID(int)}のdict
        ID2key (dict): {ID(int): 要素}のdict（key2IDの逆変換）
        cnt (int): IDのカウンター（今見ている要素数）

    """

    def __init__(self: Self) -> None:
        """Init."""
        self.parents: dict[T, int] = {}
        self.members_set: defaultdict[T, set[T]] = defaultdict(lambda : set())
        self.roots_set: set[T] = set()
        self.key2ID: dict[T, int] = {}
        self.ID2key: dict[int, T] = {}
        self.cnt = 0

    def dictf(self: Self, x: T) -> int:
        """要素名とIDをやり取りする"""
        if x in self.key2ID:
            return self.key2ID[x]
        self.cnt += 1
        self.key2ID[x] = self.cnt
        self.parents[x] = self.cnt
        self.ID2key[self.cnt] = x
        self.members_set[x].add(x)
        self.roots_set.add(x)
        return self.key2ID[x]

    def find_root(self: Self, x: T) -> T:
        """xが属するグループの根（いなければxが根）"""
        id_x = self.dictf(x)
        if self.parents[x] == id_x:
            return x
        self.parents[x] = self.key2ID[self.find_root(self.ID2key[self.parents[x]])]
        return self.ID2key[self.parents[x]]

    def union(self: Self, x: T, y: T) -> None:
        """xとyのグループを結合"""
        x = self.find_root(x)
        y = self.find_root(y)
        if self.parents[x] > self.parents[y]:
            x, y = y, x
        if x == y:
            return
        for i in self.members_set[y]:
            self.members_set[x].add(i)
        self.members_set[y] = set()
        self.roots_set.remove(y)
        self.parents[y] = self.key2ID[x]

    def size(self: Self, x: T) -> int:
        """xの属するグループのサイズ（要素数）"""
        return len(self.members_set[self.find_root(x)])

    def is_same(self: Self, x: T, y: T) -> bool:
        """xとyが同じグループに属するか"""
        return self.find_root(x) == self.find_root(y)

    def members(self: Self, x: T) -> set:
        """xが属するグループに属する要素"""
        return self.members_set[self.find_root(x)]

    def roots(self: Self) -> set:
        """すべての根"""
        return self.roots_set

    def group_count(self: Self) -> int:
        """連結成分の数"""
        return len(self.roots_set)

    def all_group_members(self: Self) -> dict:
        """{根: [そのグループに含まれる要素のリスト]}のdict"""
        return {r: self.members_set[r] for r in self.roots_set}

    def __str__(self: Self) -> str:
        """print用"""
        return "\n".join(f"{r}: {m}" for r, m in self.all_group_members().items())
