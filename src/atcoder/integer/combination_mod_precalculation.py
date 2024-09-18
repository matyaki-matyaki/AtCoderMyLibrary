"""N以下のnについて、組み合わせnCk (mod MOD) = n!/(k!(n-k)!) (mod MOD)を前計算することでO(1)で計算"""
import numpy as np

MOD = 998244353
N = 10000

def prepare(N: int, MOD: int) -> tuple[list[int], list[int]]:
    """`N`以下の自然数`i`の階乗`i! (mod MOD)`とその逆元を計算 O(n)

    Args:
        N (int): 計算する必要のある最大の自然数
        MOD (int): modulo

    Returns:
        tuple[list[int], list[int]]: 階乗のリストとその逆元のリスト
    """
    nrt = int(N ** 0.5) + 1
    nsq = nrt * nrt
    facts = np.arange(nsq, dtype=np.int64).reshape(nrt, nrt)
    facts[0, 0] = 1
    for i in range(1, nrt):
        facts[:, i] = facts[:, i] * facts[:, i - 1] % MOD
    for i in range(1, nrt):
        facts[i] = facts[i] * facts[i - 1, -1] % MOD
    facts_list = facts.ravel().tolist()

    invs = np.arange(1, nsq + 1, dtype=np.int64).reshape(nrt, nrt)
    invs[-1, -1] = pow(facts[-1], MOD - 2, MOD)
    for i in range(nrt - 2, -1, -1):
        invs[:, i] = invs[:, i] * invs[:, i + 1] % MOD
    for i in range(nrt - 2, -1, -1):
        invs[i] = invs[i] * invs[i + 1, 0] % MOD
    invs_list = invs.ravel().tolist()

    return facts_list, invs_list

facts, invs = prepare(N, MOD)

def cmb_mod(n: int, k: int) -> int:
    """`prepare`で用意されたテーブルを用いてnCk (mod MOD)を計算 O(1)"""
    if n < k:
        return 0
    if n == 0:
        return 0
    return facts[n] * invs[n - k] % MOD * invs[k] % MOD
