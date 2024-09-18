"""進数の変換"""


def basechanger(n: int, from_base: int, to_base: int) -> list[int]:
    """整数`n`の進数を`from_base`から`to_base`に変換

    Args:
        n (int): 整数`n`
        from_base (int): 元の進数
        to_base (int): 変換後の進数

    Returns:
        list[int]: to_base進数での表現
    """
    if n == 0:
        return [0]
    s = str(n)
    base10 = 0
    for i in range(len(s)):
        base10 += int(s[i]) * from_base ** (len(s) - i - 1)
    ret = []
    while base10 >= 1:
        tmp = base10 % to_base
        base10 //= to_base
        ret.append(tmp)
    ret.reverse()
    return ret
