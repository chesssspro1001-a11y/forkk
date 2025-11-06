from typing import List, Tuple
from math import gcd

# Linear Congruence Solver: Solve a * x ≡ b (mod m)
# Theory:
# A linear congruence a x ≡ b (mod m) has solutions iff gcd(a, m) | b.
# Let g = gcd(a, m). If g ∤ b -> no solution.
# Otherwise divide: a' = a / g, b' = b / g, m' = m / g.
# Then a' and m' are coprime, so the unique solution modulo m' is:
#    x0 ≡ (a')^{-1} * b' (mod m')
# All solutions modulo m are:
#    x = x0 + k * m'  for k = 0 .. g-1
# (they are distinct modulo m and there are exactly g of them)
#
# We implement:
# - extended_gcd: returns (g, x, y) with ax + by = g
# - mod_inverse: inverse of a modulo m (assuming gcd(a,m)=1)
# - solve_linear_congruence: returns sorted list of all solutions or empty list
#
# Complexity: O(log min(a, m))


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def mod_inverse(a: int, m: int) -> int:
    a %= m
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return -1
    return x % m

def solve_linear_congruence(a: int, b: int, m: int) -> List[int]:
    a %= m
    b %= m
    g = gcd(a, m)
    if b % g != 0:
        return []
    if g == 1:
        inv = mod_inverse(a, m)
        return [ (inv * b) % m ]
    # Reduce
    a_ = a // g
    b_ = b // g
    m_ = m // g
    inv = mod_inverse(a_, m_)
    x0 = (inv * b_) % m_
    # Generate all g solutions modulo m
    sols = [ (x0 + k * m_) % m for k in range(g) ]
    sols.sort()
    return sols
