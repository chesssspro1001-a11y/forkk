import sys, random, math
"""
Efficient integer factorization utilities combining:
1. Linear sieve (up to 1_000_000+9) for smallest prime factors (SPF) and quick trial division.
2. Deterministic Miller–Rabin primality test valid for all 64‑bit unsigned integers.
3. Pollard’s Rho algorithm (Brent-style cycle detection variant via tortoise–hare) for splitting large composite factors.
Key components:
- _sieve(): Precomputes smallest prime factors (SPF) for all numbers < 1e6+9. This enables O(log n) factor extraction per reduced number in that range and accelerates trial division.
- _is_prime(n): Deterministic Miller–Rabin for n < 2^64 using a proven sufficient base set (2, 325, 9375, 28178, 450775, 9780504, 1795265022).
- _pollard_rho(n): Randomized Pollard Rho using polynomial f(x)=x^2 + c (mod n) with randomly chosen c and seeds; finds a non-trivial factor with expected time about O(n^{1/4}) for semiprimes of balanced size.
- _factor(n, out): Recursive decomposition combining the above; accumulates prime factors (with multiplicity) into 'out'.
- factorize(n): Public helper returning an (unsorted) list of prime factors with multiplicity.

Algorithmic notes (Pollard Rho brief theory):
Pollard’s Rho exploits the birthday paradox on the sequence x_{i+1} = f(x_i) mod n in the ring Z/nZ. For a composite n = p*q, the sequence projected modulo p cycles earlier; gcd(|x_i - x_j|, n) eventually reveals p (or q). Expected time to find a factor roughly ~ O(p^{1/2}) where p is the smaller prime factor; for balanced semiprimes ~ O(n^{1/4}). Random restarts mitigate rare pathological cycles.
Determinism & randomness:
While Miller–Rabin here is deterministic for 64-bit, Pollard Rho uses randomness for seeds and constants; worst-case behavior is not guaranteed but practically very fast for typical competitive programming constraints.
Complexity summary:
- Sieve preprocessing: O(N log log N) with N ≈ 1e6.
- Each factorization:
    * Fast for n < sieve limit (O(log n)).
    * Otherwise dominated by Pollard Rho splits plus primality tests: empirically sub-millisecond for 64-bit inputs.
Limitations:
- Designed for 64-bit integers (n < 2^64). Larger integers would need an expanded Miller–Rabin base set or a different strategy.
- Uses Python's random module (not cryptographically secure).
- Output formatting includes a trailing space per line (may need adjustment for strict judges).
Usage example (conceptual):
    factors = factorize(360)  # Might yield [2,2,2,3,3,5]
    sorted_factors = sorted(factors)
"""

_small_primes = []
_spf_limit = 10**6 + 9
_spf = [0] * _spf_limit

def _sieve():
    global _small_primes
    for i in range(2, _spf_limit):
        if _spf[i] == 0:
            _spf[i] = i
            _small_primes.append(i)
        j = 0
        while j < len(_small_primes):
            p = _small_primes[j]
            k = i * p
            if k >= _spf_limit: break
            _spf[k] = p
            if p == _spf[i]: break
            j += 1

_sieve()

# Deterministic Miller-Rabin for 64-bit
def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < _spf_limit:
        return _spf[n] == n
    # quick trial by small primes
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n - 1
    s = 0
    while d & 1 == 0:
        d >>= 1
        s += 1
    # bases sufficient for 64-bit
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def _pollard_rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    while True:
        c = random.randrange(1, n)
        f = lambda x: (pow(x, 2, n) + c) % n
        x = random.randrange(0, n)
        y = x
        d = 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d

def _factor(n: int, out: list):
    if n == 1:
        return
    if n < _spf_limit:
        while n > 1:
            p = _spf[n]
            out.append(p)
            n //= p
        return
    if _is_prime(n):
        out.append(n)
        return
    d = _pollard_rho(n)
    _factor(d, out)
    _factor(n // d, out)

def factorize(n: int):
    res = []
    _factor(n, res)
    return res

def main():
    data = sys.stdin.read().strip().split()
    if not data: 
        return
    it = iter(data)
    t = int(next(it))
    out_lines = []
    for _ in range(t):
        n = int(next(it))
        if n == 1:
            out_lines.append("0 ")
            continue
        f = factorize(n)
        f.sort()
        line = [str(len(f))] + [str(x) for x in f]
        out_lines.append(" ".join(line) + " ")
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()