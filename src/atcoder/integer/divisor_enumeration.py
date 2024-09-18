"""約数列挙"""
def enum_divisors(n: int) -> list[int]:
    """約数列挙 O(√n)

    Args:
        n (int): 整数

    Returns:
        list[int]: `n`の約数のリスト
    """
    divisors: list[int] = []
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if n // i != i:
                divisors.append(n // i)
    divisors.sort()
    return divisors

if __name__ == "__main__":
    n = 625
    print(enum_divisors(n))
