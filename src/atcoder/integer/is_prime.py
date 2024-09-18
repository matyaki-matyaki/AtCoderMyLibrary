"""素数判定"""
def is_prime(n: int) -> bool:
    """素数の判定

    Args:
        n (int): 整数

    Returns:
        bool: `n`が素数かどうか
    """
    if n == 1:
        return True
    return all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))

