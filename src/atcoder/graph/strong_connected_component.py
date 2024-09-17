"""強連結成分分解"""
import sys

sys.setrecursionlimit(10**9)

# import pypyjit
# pypyjit.set_param('max_unroll_recursion=-1')

def scc(N: int, edges: list[tuple[int, int]]) -> list[list[int]]:  # noqa: C901, PLR0915
    """有向グラフを強連結成分分解し、トポロジカルソートしたものを返す`O(N + M)`

    Args:
        N (int): 頂点数
        edges (list[tuple[int, int]]): 辺のリスト[(始点, 終点)] (0-indexed)

    Returns:
        list[list[int]]: 各強連結成分に含まれる頂点のリスト(0-indexed)
    """
    M = len(edges)
    start = [0] * (N + 1)
    elist = [0] * M
    for e in edges:
        start[e[0] + 1] += 1
    for i in range(1, N + 1):
        start[i] += start[i - 1]
    counter = start[:]
    for e in edges:
        elist[counter[e[0]]] = e[1]
        counter[e[0]] += 1
    visited = []
    low = [0] * N
    Ord = [-1] * N
    ids = [0] * N
    NG = [0, 0]

    def dfs(v: int) -> None:
        stack = [(v, -1, 0), (v, -1, 1)]
        while stack:
            v, bef, t = stack.pop()
            if t:
                if bef != -1 and Ord[v] != -1:
                    low[bef] = min(low[bef], Ord[v])
                    continue
                low[v] = NG[0]
                Ord[v] = NG[0]
                NG[0] += 1
                visited.append(v)
                for i in range(start[v], start[v + 1]):
                    to = elist[i]
                    if Ord[to] == -1:
                        stack.append((to, v, 0))
                        stack.append((to, v, 1))
                    else:
                        low[v] = min(low[v], Ord[to])
            else:
                if low[v] == Ord[v]:
                    while True:
                        u = visited.pop()
                        Ord[u] = N  # SCCの訪問順は意味がないため、Nで上書き
                        ids[u] = NG[1]
                        if u == v:
                            break
                    NG[1] += 1
                if bef != -1:  # befが有効な場合のみlowを更新
                    low[bef] = min(low[bef], low[v])

    for i in range(N):
        if Ord[i] == -1:
            dfs(i)

    for i in range(N):
        ids[i] = NG[1] - 1 - ids[i]

    group_num = NG[1]
    counts = [0] * group_num
    for x in ids:
        counts[x] += 1

    groups: list[list[int]] = [[] for i in range(group_num)]
    for i in range(N):
        groups[ids[i]].append(i)

    return groups

if __name__ == "__main__":
    """動作確認"""
    # https://atcoder.jp/contests/practice2/tasks/practice2_g
    N, M = map(int, input().split())
    edges: list[tuple[int, int]] = []
    for _ in range(M):
        a, b = map(int, input().split())
        edges.append((a, b))

    groups = scc(N, edges)
    print(len(groups))
    for g in groups:
        print(len(g), *g)
