"""最長増加部分列"""
from bisect import bisect_left


def lis(li: list) -> list[int]:
    """最長部分増加列（`bisect_left`を`bisect_right`に変えれば、最長部分広義増加列となる）O(n log n)

    Args:
        li (list): 数列

    Returns:
        list[int]: 最長増加部分列
    """
    # STEP1: LIS長パート with 使用位置
    n = len(li)
    lisDP = [float("inf")] * n # 通常のLIS用リスト
    index_list: list[int] = [-1] * n # lの[i]文字目が使われた場所を記録する
    for i in range(n):
        # 通常のLISを求め、indexListに使った場所を記録する
        ind = bisect_left(lisDP, li[i])
        lisDP[ind] = li[i]
        index_list[i] = ind
    # STEP2: LIS復元パート by 元配列の使用した位置
    # 後ろから見ていくので、まずは、LIS長目(targetIndex)のindexListを探したいとする
    targetIndex = max(index_list)
    ans = [0] * (targetIndex + 1) # 復元結果(indexListは0-indexedなのでlen=4ならmax=3で格納されているので+1する)
    # 後ろから見ていく
    for i in range(n - 1, -1, -1):
        # もし、一番最後に出てきているtargetIndexなら
        if index_list[i] == targetIndex:
            ans[targetIndex] = li[i] # ansのtargetIndexを確定
            targetIndex -= 1
    return ans


if __name__ == "__main__":
    N = int(input())
    A = list(map(int, input().split()))

    ans = lis(A)
    print(len(ans))
