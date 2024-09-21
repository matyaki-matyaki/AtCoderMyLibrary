"""めぐる式二分探索（ある条件を満たすかどうかの二分探索）"""
from typing import Callable


def binary_search_meguru(ng: int, ok: int, is_ok: Callable[[int], bool]) -> int:
    """めぐる式二分探索

    Args:
        ng (int): 数が大きくなれば条件を満たす場合：取りうる値の最小値 - 1,\
            数が大きくなれば条件を満たす場合：取りうる値の最大値 + 1
        ok (int): 数が大きくなれば条件を満たす場合：取りうる値の最大値 + 1,\
            数が大きくなれば条件を満たす場合：取りうる値の最小値 - 1
        is_ok (Callable[[int], bool]): 条件

    Returns:
        int: is_okを満たすギリギリの値
    """
    while abs(ok - ng) > 1:
        mid = (ok + ng) // 2
        if is_ok(mid):
            ok = mid
        else:
            ng = mid
    return ok
