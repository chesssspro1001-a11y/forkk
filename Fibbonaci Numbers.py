"""
Properties
----------
Fibonacci numbers (F_n) possess numerous notable identities and number-theoretic properties.

1. Cassini's Identity:
    F_{n-1} * F_{n+1} - F_n^2 = (-1)^n
    This can be proved by induction. A succinct proof (attributed to Knuth) arises from taking
    the determinant of the 2x2 matrix representation of Fibonacci recurrence:
         |F_{n+1}  F_n    |
         |F_n      F_{n-1}|

2. Addition Rule:
    F_{n+k} = F_k * F_{n+1} + F_{k-1} * F_n
    Special case (k = n):
    F_{2n} = F_n * (F_{n+1} + F_{n-1})

3. Divisibility:
    From the addition rule and induction: for any positive integer k, F_{nk} is a multiple of F_n.
    The converse also holds:
      If F_m is a multiple of F_n, then m is a multiple of n.

4. GCD Identity:
    GCD(F_m, F_n) = F_{GCD(m, n)}
    This identity shows the Fibonacci sequence aligns structurally with the Euclidean algorithm.

5. Algorithmic Note:
    Consecutive Fibonacci numbers form the worst-case input sequence for the Euclidean algorithm
    (Lame's theorem), maximizing the number of modulo steps for a given magnitude of inputs.

6. Closed Form (Binet's Formula):
    F_n = ( ( (1 + √5)/2 )^n - ( (1 - √5)/2 )^n ) / √5
    Let φ = (1 + √5)/2 and ψ = (1 - √5)/2. Then F_n = (φ^n - ψ^n)/√5.
    For n ≥ 0, rounding (φ^n / √5) to nearest integer yields F_n due to |ψ| < 1.

7. Pisano Period:
    For a modulus m ≥ 2, the Fibonacci sequence reduced modulo m is purely periodic:
        F_0 ≡ 0, F_1 ≡ 1, ...
    There exists the least positive integer π(m) (the Pisano period) such that:
        (F_{π(m)}, F_{π(m)+1}) ≡ (0, 1) (mod m)
    Hence F_{n + π(m)} ≡ F_n (mod m) for all n ≥ 0.

"""

from math import sqrt

_phi = (1 + sqrt(5)) / 2
_psi = (1 - sqrt(5)) / 2
_sqrt5 = sqrt(5)

def fib_binet(n: int) -> int:
    """Return F_n using Binet's formula (accurate for n >= 0 within integer rounding)."""
    return int(round((_phi**n - _psi**n) / _sqrt5))

def fib_fast_doubling(n: int) -> int:
    """Return F_n using fast doubling (O(log n)), exact for large n."""
    if n < 0:
        raise ValueError("n must be non-negative")
    def _fd(k):
        if k == 0:
            return (0, 1)
        a, b = _fd(k // 2)
        c = a * (2 * b - a)
        d = a * a + b * b
        if k % 2 == 0:
            return (c, d)
        else:
            return (d, c + d)
    return _fd(n)[0]

def fib_matrix(n: int) -> int:
    """Return F_n using 2x2 matrix exponentiation (O(log n))."""
    # Identity matrix and Fibonacci Q-matrix
    res = (1, 0, 0, 1)      # (a b; c d)
    base = (1, 1, 1, 0)
    k = n
    while k:
        if k & 1:
            # res = res * base
            r00 = res[0] * base[0] + res[1] * base[2]
            r01 = res[0] * base[1] + res[1] * base[3]
            r10 = res[2] * base[0] + res[3] * base[2]
            r11 = res[2] * base[1] + res[3] * base[3]
            res = (r00, r01, r10, r11)
        # base = base * base
        b00 = base[0] * base[0] + base[1] * base[2]
        b01 = base[0] * base[1] + base[1] * base[3]
        b10 = base[2] * base[0] + base[3] * base[2]
        b11 = base[2] * base[1] + base[3] * base[3]
        base = (b00, b01, b10, b11)
        k >>= 1
    return res[1]


#best is to calculate using phi feild (CSES Fibo)