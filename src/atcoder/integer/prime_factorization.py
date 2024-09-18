"""素因数分解"""
from collections import Counter


def prime_factorize(n: int) -> Counter:
    """素因数分解 O(log n)

    Args:
        n (int): 素因数分解される整数

    Returns:
        Counter: key: 素数, value: keyの数
    """
    a = []
    while n % 2 == 0:
        a.append(2)
        n //= 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            a.append(f)
            n //= f
        else:
            f += 2
    if n != 1:
        a.append(n)

    return Counter(a)

if __name__ == "__main__":
    n = 12
    counter = prime_factorize(n)
    for key, value in counter.items():
        print(f"{key=}, {value=}")
