"""ランレングス圧縮"""

def run_length_encoding(s: str) -> list[tuple[str, int]]:
    """ランレングス圧縮

    Args:
        s (str): 圧縮する文字列

    Returns:
        list[tuple[str, int]]: (文字, 文字数)のリスト
    """
    res = []
    cnt = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            cnt += 1
        else:
            res.append((s[i - 1], cnt))
            cnt = 1
        if i == len(s) - 1:
            res.append((s[i], cnt))
    return res

s = "AAAAAAABBBBCCDEEEEEAAA"

print(run_length_encoding(s))
