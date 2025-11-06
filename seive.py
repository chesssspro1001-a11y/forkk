from math import isqrt
# Sieve templates: classic sieve, linear sieve (with SPF), factorization helper.

def sieve_bool(n: int): #time complexity O(n log log n)
    """
    Returns:
        is_prime: list[bool] where is_prime[i] is True iff i is prime (0..n)
    """
    if n < 1:
        return [False] * (n + 1)
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    if n >= 1:
        is_prime[1] = False
    limit = isqrt(n)
    for p in range(2, limit + 1):
        if is_prime[p]:
            step = p
            start = p * p
            is_prime[start:n + 1:step] = [False] * ((n - start) // step + 1)
    return is_prime

def sieve_primes(n: int): 
    """
    Returns:
        primes: list of primes <= n
    """
    is_prime = sieve_bool(n)
    return [i for i, v in enumerate(is_prime) if v]

def linear_sieve(n: int): #time complexity O(n)
    """
    Returns:
        primes: list of primes <= n (in order)
        spf: smallest prime factor for each number 0..n (spf[1]=1)
    Complexity: O(n)
    ensures that every composite number is marked exactly once
    """
    spf = [0] * (n + 1)
    primes = []
    if n >= 1:
        spf[1] = 1
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        for p in primes:
            if p > spf[i] or p * i > n:
                break
            spf[p * i] = p
    return primes, spf

def factorize_with_spf(x: int, spf: list[int]): #time complexity O(log x)
    """
    Factorizes x using precomputed smallest prime factors.
    Returns list of (prime, exponent).
    """
    if x <= 1:
        return []
    res = []
    while x > 1:
        p = spf[x]
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
        res.append((p, cnt))
    return res


def segmented_sieve(l: int, r: int): #time complexity O((r-l+1) log log sqrt(r))
    """
    Returns list of primes in the inclusive range [l, r] using a segmented sieve.
    Handles ranges starting below 2.
    """
    if r < 2 or r < l:
        return []
    if l < 2:
        l = 2
    limit = isqrt(r)
    base_primes = sieve_primes(limit)
    size = r - l + 1
    is_prime_seg = [True] * size
    for p in base_primes:
        start = max(p * p, ((l + p - 1) // p) * p)
        for multiple in range(start, r + 1, p):
            is_prime_seg[multiple - l] = False
    return [l + i for i, flag in enumerate(is_prime_seg) if flag]