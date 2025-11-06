from math import gcd
# Extended exponent reduction (non-coprime case):

# For general x, m, and n >= log2(m):
#     x^n ≡ x^{phi(m) + (n mod phi(m))} (mod m)
# This lets us reduce large exponents even when gcd(x, m) != 1.
# Practical rule used in implementations:
#   Let ph = phi(m).
#   If gcd(x, m) == 1: exponent -> n % ph
#   Else:
#       If n < ph: exponent -> n (cannot reduce safely yet)
#       Else:      exponent -> ph + (n % ph)

def pow_mod_general(a: int, e: int, m: int) -> int:
    """
    Compute a^e mod m using Euler reduction even when a and m are not coprime.
    Uses adjusted exponent: 
        if gcd(a,m)==1: e' = e % phi(m)
        else:           e' = e (if e < phi(m)) else phi(m) + (e % phi(m))
    Valid for m >= 1. Handles edge cases.
    """
    if m == 1:
        return 0
    if e == 0:
        return 1 % m
    ph = phi(m)
    if gcd(a, m) == 1:
        exp = e % ph
    else:
        exp = e if e < ph else ph + (e % ph)
    return pow(a % m, exp, m)


#multiplicative Function f(a*b) = f(a) * f(b)
def euler_theorem(a: int, m: int) -> int:
    """
    Euler's Theorem:
        a^{phi(m)} ≡ 1 (mod m) if gcd(a, m) = 1.
    Returns a^{phi(m)} mod m, guaranteeing 1 when gcd(a,m)=1 (except m=1 where result is 0).
    """
    if m == 1:
        return 0
    if gcd(a, m) != 1:
        raise ValueError("a and m must be coprime")
    return pow(a, phi(m), m)

def pow_mod_coprime(a: int, e: int, m: int) -> int:
    """
    Compute a^e mod m using Euler's theorem to reduce the exponent when gcd(a, m) = 1.
    If not coprime, falls back to direct pow.
    """
    if m == 1:
        return 0
    if gcd(a, m) == 1:
        e %= phi(m)
    return pow(a % m, e, m)


def phi(n: int) -> int:
    """
    Compute Euler's Totient (phi) of n.
    phi(n) = count of integers k in [1, n] such that gcd(k, n) = 1.
    Requires n >= 1.
    """
    result = n
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            result -= result // p
        p += 1 if p == 2 else 2  # check 2 then only odds
    if x > 1:
        result -= result // x
    return result


def phi_sieve(limit: int) -> list:
    """
    Compute phi(k) for all 1 <= k <= limit using a sieve in O(limit log log limit).
    Returns list phi where phi[k] = phi(k).
    """
    phi = list(range(limit + 1))
    for i in range(2, limit + 1):
        if phi[i] == i:  # i is prime
            step = i
            for j in range(i, limit + 1, step):
                phi[j] -= phi[j] // i
    return phi

print(phi(1337))