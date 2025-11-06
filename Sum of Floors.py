MOD = 10**9 + 7

def weighted_floor_sum(n: int, mod: int = MOD) -> int:
    """
    Computes S = sum_{i=1..n} i * floor(n / i) modulo mod.

    Theory:
    For fixed q = floor(n / i), the indices i form a contiguous interval:
        i in [L, R] where L = current i, R = n // q.
    Over that block, floor(n / i) = q is constant.
    So contribution = q * sum_{i=L}^{R} i = q * (R - L + 1)*(L + R)//2.
    Advancing by blocks gives O(sqrt n) complexity because q changes only ~2*sqrt(n) times.
    """
    total = 0
    i = 1
    while i <= n:
        q = n // i
        r = n // q
        block_sum = (r - i + 1) * (i + r) // 2
        total = (total + q * block_sum) % mod
        i = r + 1
    return total
