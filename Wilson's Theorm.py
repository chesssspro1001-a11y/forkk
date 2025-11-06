"""
Wilson's Theorem:
An integer p > 1 is prime  <=>  (p - 1)! ≡ -1 (mod p)  i.e. (p - 1)! % p == p - 1

This gives a primality test, but it is factorial-time (O(p)), so it's only practical for small p.
Included:
- is_prime_trial: a faster practical check (trial division) for comparison.
- is_prime_wilson: direct Wilson's theorem check.
- factorial_mod: computes (n!) % mod with early termination.
"""