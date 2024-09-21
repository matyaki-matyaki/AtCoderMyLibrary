"""2次元累積和による部分和"""
def compute_2d_cumulative_sum(matrix: list[list[int]]) -> list[list[int]]:
    """2次元累積和の作成

    Args:
        matrix (list[list[int]]): 2次元リスト

    Returns:
        list[list[int]]: 2次元累積和
    """
    height = len(matrix)
    width = len(matrix[0])
    cumulative_sum = [[0] * width for _ in range(height)]
    cumulative_sum[0][0] = matrix[0][0]

    for i in range(1, width):
        cumulative_sum[0][i] = cumulative_sum[0][i - 1] + matrix[0][i]

    for i in range(1, height):
        row_sum = 0
        for j in range(width):
            row_sum += matrix[i][j]
            cumulative_sum[i][j] = cumulative_sum[i - 1][j] + row_sum

    return cumulative_sum

def get_submatrix_sum(cumulative_sum: list[list[int]], x1: int, y1: int, x2: int, y2: int) -> int:
    """部分行列（長方形部分）の和(sum(matrix[x1: x2 + 1, y1: y2 + 1]))

    Args:
        cumulative_sum (list[list[int]]): 上で作った2次元累積和
        x1 (int): 開始行
        y1 (int): 終了行
        x2 (int): 開始列
        y2 (int): 終了列

    Returns:
        int: 長方形部分の和
    """
    # 指定された (x1, y1) から (x2, y2) の範囲の和を計算する（0-indexed）

    if x1 == 0 and y1 == 0:
        return cumulative_sum[x2][y2]
    if x1 == 0:
        return cumulative_sum[x2][y2] - cumulative_sum[x2][y1 - 1]
    if y1 == 0:
        return cumulative_sum[x2][y2] - cumulative_sum[x1 - 1][y2]

    return (cumulative_sum[x2][y2]
            - cumulative_sum[x1 - 1][y2]
            - cumulative_sum[x2][y1 - 1]
            + cumulative_sum[x1 - 1][y1 - 1])
