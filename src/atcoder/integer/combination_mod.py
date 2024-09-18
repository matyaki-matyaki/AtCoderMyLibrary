"""nCk (mod MOD)を計算"""
def cmb_mod(n: int, k: int, MOD: int) -> int:
    """NCk (mod MOD)"""
    if k < 0 or n < k:
        return 0
    a = 1
    b = 1
    for i in range(k):
        a *= n - i
        a %= MOD
        b *= i + 1
        b %= MOD
    return (a * pow(b, MOD - 2, MOD)) % MOD
