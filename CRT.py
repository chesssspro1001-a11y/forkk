from typing import List, Tuple

"""
Chinese Remainder Theorem (weak form and generalized form)

Theory (concise):
Given congruences:
    x ≡ a_i (mod m_i), for i = 1..k

Weak form (classic CRT):
- If all moduli m_i are pairwise coprime, there exists a unique solution modulo M = Π m_i.

Generalized form:
- Let g = gcd(m_i, m_j). A necessary and sufficient condition for a solution to exist is:
      a_i ≡ a_j (mod g)  for every pair.
- When merging two congruences:
      x ≡ a1 (mod m1)
      x ≡ a2 (mod m2)
  Let g = gcd(m1, m2).
  If (a2 - a1) % g != 0 → no solution.
  Otherwise reduce the system to one congruence:
      x = a1 + m1 * t
      m1 * t ≡ (a2 - a1) (mod m2)
      Divide by g:
          (m1/g) * t ≡ (a2 - a1)/g (mod m2/g)
      Since m1/g and m2/g are coprime, invert m1/g modulo m2/g.
  New modulus = lcm(m1, m2) = m1//g * m2.

This implementation:
- chinese_remainder_pair merges two congruences (possibly non-coprime moduli)
- chinese_remainder takes arrays A (remainders) and M (moduli)
- Returns (x, L) where x is the smallest non-negative solution modulo L
- Returns (-1, -1) if invalid or no solution
"""


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Return (g,x,y) such that g = gcd(a,b) and ax + by = g."""
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def mod_inverse(a: int, mod: int) -> int:
    """Return inverse of a modulo mod; assumes gcd(a,mod)=1."""
    g, x, _ = extended_gcd(a, mod)
    if g != 1:
        raise ValueError("Inverse does not exist")
    return x % mod

def chinese_remainder_pair(a1: int, m1: int, a2: int, m2: int) -> Tuple[int, int]:
    """
    Merge:
        x ≡ a1 (mod m1)
        x ≡ a2 (mod m2)
    Return (x, lcm) or (-1, -1) if no solution.
    """
    if m1 <= 0 or m2 <= 0:
        return (-1, -1)
    g, p, q = extended_gcd(m1, m2)
    diff = a2 - a1
    if diff % g != 0:
        return (-1, -1)  # Inconsistent
    # Solve m1 * t ≡ diff (mod m2)
    m2_reduced = m2 // g
    t = (diff // g) * (p % m2_reduced) % m2_reduced
    x = a1 + m1 * t
    mod = m1 // g * m2
    x %= mod
    return (x, mod)

def chinese_remainder(A: List[int], M: List[int]) -> Tuple[int, int]:
    """
    Generalized CRT over lists.
    Return (x, L) with x the unique solution modulo L (product/lcm of moduli),
    or (-1, -1) if invalid input or no solution.
    """
    if len(A) != len(M) or not A:
        return (-1, -1)
    x = A[0] % M[0]
    mod = M[0]
    if mod <= 0:
        return (-1, -1)
    for a, m in zip(A[1:], M[1:]):
        res_x, res_m = chinese_remainder_pair(x, mod, a % m, m)
        if res_x == -1:
            return (-1, -1)
        x, mod = res_x, res_m
    return (x, mod)

# Weak form (pairwise coprime) faster merge (optional)
def chinese_remainder_coprime(A: List[int], M: List[int]) -> Tuple[int, int]:
    """
    Assumes M are pairwise coprime.
    Return (x, product) or (-1,-1) if invalid.
    """
    if len(A) != len(M) or not A:
        return (-1, -1)
    x = 0
    prod = 1
    for a, m in zip(A, M):
        if m <= 0:
            return (-1, -1)
        inv = mod_inverse(prod % m, m)  # Since gcd(prod, m)=1
        # Combine: x ≡ current x (mod prod), x ≡ a (mod m)
        x = (a - x) % m * inv % m * prod + x
        prod *= m
    return (x % prod, prod)

