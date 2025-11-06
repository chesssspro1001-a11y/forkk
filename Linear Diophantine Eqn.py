import sys
from math import gcd

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def find_any_solution(a, b, c):
    if a == 0 and b == 0:
        if c == 0:
            return True, 0, 0, 0  # infinite grid (handled outside)
        return False, 0, 0, 0
    g, x, y = extended_gcd(abs(a), abs(b))
    if c % g != 0:
        return False, 0, 0, g
    x *= c // g
    y *= c // g
    if a < 0: x = -x
    if b < 0: y = -y
    return True, x, y, g

def shift_solution(x, y, a, b, k):
    return x + k * b, y - k * a

def count_solutions(a, b, c, x1, x2, y1, y2):
    ok, x0, y0, g = find_any_solution(a, b, c)
    if not ok: 
        return 0
    if a == 0 and b == 0:
        # c == 0 here
        return (x2 - x1 + 1) * (y2 - y1 + 1)
    if a == 0:
        # b y = c
        if c % b: return 0
        y = c // b
        return (x2 - x1 + 1) if y1 <= y <= y2 else 0
    if b == 0:
        # a x = c
        if c % a: return 0
        x = c // a
        return (y2 - y1 + 1) if x1 <= x <= x2 else 0

    a_div = a // g
    b_div = b // g

    # General solution: x = x0 + k * b_div, y = y0 - k * a_div
    # Constrain x
    def floor_div(a, b):
        return a // b if a * b >= 0 else -((-a) // b)
    def ceil_div(a, b):
        return a // b if a * b > 0 and a % b == 0 else floor_div(a + b - 1 if b > 0 else a + b + 1, b)

    # For x in [x1,x2]:
    # x1 <= x0 + k*b_div <= x2
    if b_div > 0:
        kx_low = (x1 - x0 + b_div - 1) // b_div
        kx_high = (x2 - x0) // b_div
    else:
        kx_low = (x0 - x2 + (-b_div) - 1) // (-b_div)
        kx_high = (x0 - x1) // (-b_div)

    # For y in [y1,y2]:
    # y1 <= y0 - k*a_div <= y2  ->  y0 - y2 <= k*a_div <= y0 - y1
    if a_div > 0:
        ky_low = (y0 - y2 + a_div - 1) // a_div
        ky_high = (y0 - y1) // a_div
    else:
        ky_low = (y0 - y1 + (-a_div) - 1) // (-a_div)
        ky_high = (y0 - y2) // (-a_div)

    k_low = max(kx_low, ky_low)
    k_high = min(kx_high, ky_high)
    if k_low > k_high:
        return 0
    return k_high - k_low + 1

