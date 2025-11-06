import math
from collections import defaultdict

# Generates (a, b, c) with a^2 + b^2 = c^2
def generate_pythagorean_triples(max_c: int, include_multiples: bool = True):
    """
    Generate Pythagorean triples with c <= max_c.
    If include_multiples is True, include non-primitive multiples as in the C++ code.
    """
    triples_by_c = defaultdict(list)

    # Upper bound for m: since c = m^2 + n^2 <= max_c  =>  m^2 < max_c
    m_limit = int(math.isqrt(max_c)) + 1

    for m in range(1, m_limit):
        for n in range(1, m):
            if (m - n) % 2 == 0:  # same parity, skip
                continue
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            if c > max_c:
                break
            if math.gcd(a, b) != 1:  # ensure primitive
                continue

            if include_multiples:
                k = 1
                while k * c <= max_c:
                    triples_by_c[k * c].append((a * k, b * k))
                    k += 1
            else:
                triples_by_c[c].append((a, b))
    return triples_by_c