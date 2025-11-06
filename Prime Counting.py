import sys

# Prime Counting (pi(n)) using Lehmer's algorithm for n up to about 1e16 comfortably.
# Adjust sieve limit if needed; must be >= n^(2/3) for target max n.
_SIEVE_LIMIT = 5_000_000  # covers n up to roughly (5e6)^(3/2) ~= 3.5e10; with Lehmer still OK beyond.
_is_comp = bytearray(_SIEVE_LIMIT + 1)
primes = []
pi = [0] * (_SIEVE_LIMIT + 1)

def _sieve():
    for i in range(2, _SIEVE_LIMIT + 1):
        if not _is_comp[i]:
            primes.append(i)
        pi[i] = pi[i-1] + (0 if _is_comp[i] else 1)
        for p in primes:
            k = i * p
            if k > _SIEVE_LIMIT:
                break
            _is_comp[k] = 1
            if i % p == 0:
                break

_sieve()

# Cache for phi(x, s) for small s to speed up Lehmer
_phi_cache = {}
_SMALL_S_LIMIT = 7  # cache only for small s to save memory

def phi(x: int, s: int) -> int:
    if s == 0:
        return x
    if s == 1:
        return x - x // 2
    if s == 2:
        return x - x // 2 - x // 3 + x // 6
    if s == 3:
        return x - x//2 - x//3 - x//5 + x//6 + x//10 + x//15 - x//30  # inclusion-exclusion for primes[0..2]=2,3,5
    if s < 0:
        return 0
    if x == 0:
        return 0
    if s <= _SMALL_S_LIMIT and x < (1 << 50):
        key = (x, s)
        if key in _phi_cache:
            return _phi_cache[key]
        res = phi(x, s - 1) - phi(x // primes[s - 1], s - 1)
        _phi_cache[key] = res
        return res
    return phi(x, s - 1) - phi(x // primes[s - 1], s - 1)

def lehmer_pi(n: int) -> int:
    if n <= _SIEVE_LIMIT:
        return pi[n]
    # Parameter decomposition
    a = lehmer_pi(int(n ** (1/4)))
    b = lehmer_pi(int(n ** 0.5))
    c = lehmer_pi(int(n ** (1/3)))
    # First part
    res = phi(n, a) + (b + a - 2) * (b - a + 1) // 2
    # Main correction loop
    for i in range(a + 1, b + 1):
        p = primes[i - 1]
        w = n // p
        res -= lehmer_pi(w)
        if i <= c:
            lim = lehmer_pi(int(w ** 0.5))
            for j in range(i, lim + 1):
                res -= lehmer_pi(w // primes[j - 1]) - (j - 1)
    return res

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    q = int(data[0])
    out = []
    for i in range(1, q + 1):
        n = int(data[i])
        out.append(str(lehmer_pi(n)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()