"""Normal UnionFind"""
from collections import defaultdict


class UnionFind:
    """UnionFind

    Attributes:
        _n (int): 頂点数
        _parents (list): 各要素の親要素のインデックスを格納するリストで、要素が根の場合は-(そのグループの要素数)を格納

    Note:
    - 頂点数nは事前に指定
    - 頂点：`0` ~ `n-1`までの整数
    - 参考：https://note.nkmk.me/python-union-find/
    """
    def __init__(self, n: int) -> None:
        """Init.

        Args:
            n (int): 頂点数
        """
        self._n = n
        self._parents = [-1] * n

    def find_root(self, x: int) -> int:
        """頂点xが属するグループの根（いなければxが根）"""
        if self._parents[x] < 0:
            return x
        self._parents[x] = self.find_root(self._parents[x]) # 経路圧縮
        return self._parents[x]

    def union(self, x: int, y: int) -> None:
        """頂点xと頂点yのグループを結合"""
        x = self.find_root(x)
        y = self.find_root(y)
        if x == y: # 元々同じグループの場合
            return

        if self._parents[x] > self._parents[y]: # 要素数の少ない方を多い方に結合
            x, y = y, x

        # x: 要素数が多い方のグループの根, y: 少ない方のグループの根

        self._parents[x] += self._parents[y]
        self._parents[y] = x

    def size(self, x: int) -> int:
        """頂点xの属するグループのサイズ（要素数）"""
        return -self._parents[self.find_root(x)]

    def is_same_group(self, x: int, y: int) -> bool:
        """頂点xと頂点yが同じグループに属するか"""
        return self.find_root(x) == self.find_root(y)

    def members(self, x: int) -> list:
        """頂点xが属するグループに属する要素"""
        root = self.find_root(x)
        return [i for i in range(self._n) if self.find_root(i) == root]

    def roots(self) -> list:
        """すべての根"""
        return [i for i, x in enumerate(self._parents) if x < 0]

    def group_count(self) -> int:
        """連結成分の数"""
        return len(self.roots())

    def all_group_members(self) -> defaultdict:
        """{根: [そのグループに含まれる要素のリスト]}のdefaultdict"""
        group_members = defaultdict(list)
        for member in range(self._n):
            group_members[self.find_root(member)].append(member)
        return group_members

    def __str__(self) -> str:
        """print用"""
        return "\n".join(f"{r}: {m}" for r, m in self.all_group_members().items())

if __name__ == "__main__":
    """動作確認"""
    # https://atcoder.jp/contests/atc001/tasks/unionfind_a
    N, Q = map(int, input().split())

    # UnionFindの構築
    uf = UnionFind(N)

    for _ in range(Q):
        P, A, B = map(int, input().split())
        A -= 1
        B -= 1
        if P == 0:
            uf.union(A, B)
        elif uf.is_same_group(A, B):
            print("Yes")
        else:
            print("No")

    print("uf=\n", uf)
