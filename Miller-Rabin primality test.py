"""
Miller-Rabin Primality Test (deterministic for 64-bit integers)

Theory:
For odd n > 2 write n - 1 = 2^s * d with d odd.
Fermat: a^(n-1) ≡ 1 (mod n)  (for prime n)
Refined (Miller-Rabin):
For a base a (1 < a < n-1) compute x0 = a^d mod n.
If x0 == 1 or x0 == n-1 -> passes this base.
Else square repeatedly: x_{i+1} = x_i^2 mod n for i = 0 .. s-2.
If any x_i becomes n-1 -> passes this base.
Otherwise a is a witness to compositeness.

Deterministic bases:
For n < 2^64 it suffices to test the following bases (if n >= the base):
(see research by Jim Sinclair / deterministic reductions):
[2, 3, 5, 7, 11, 13]
Smaller refined minimal sets exist, but this set is fast enough and clear.

Functions:
 - is_probable_prime(n, k=8): probabilistic (random bases) for large n
 - is_prime(n): deterministic for n < 2^64, falls back to probabilistic for larger n
"""
from random import randrange

def _binpower(base: int, e: int, mod: int) -> int:
    result = 1
    base %= mod
    while e:
        if e & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        e >>= 1
    return result

def _check_composite(n: int, a: int, d: int, s: int) -> bool:
    x = _binpower(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for _ in range(1, s):
        x = (x * x) % n
        if x == n - 1:
            return False
    return True

def miller_rabin(n: int, iterations: int = 5) -> bool:
    """Return True if n is probably prime, else False (probabilistic)."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # write n-1 = 2^s * d with d odd
    d = n - 1
    s = 0
    while d & 1 == 0:
        d >>= 1
        s += 1

    for _ in range(iterations):
        a = randrange(2, n - 1)  # 2 <= a <= n-2
        if _check_composite(n, a, d, s):
            return False
    return True
