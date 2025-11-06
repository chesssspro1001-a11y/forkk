"""
Compute the Möbius function μ(n).

Theory
-------
The Möbius function μ(n) is defined for every positive integer n by:
    μ(1) = 1
    μ(n) = 0 if n is divisible by the square of any prime (i.e. n is not square-free)
    μ(n) = (-1)^k if n is the product of k distinct primes (i.e. n is square-free)

Equivalently, μ(n) is the sum of the primitive n-th roots of unity and therefore always lies in {-1, 0, 1}.

Interpretation:
    - μ(n) = 1  : n is square-free and has an even number of distinct prime factors (including n = 1, where k = 0).
    - μ(n) = -1 : n is square-free and has an odd number of distinct prime factors.
    - μ(n) = 0  : n has at least one squared prime factor.

Number-theoretic role:
    - μ is multiplicative: if gcd(a, b) = 1 then μ(ab) = μ(a) * μ(b).
    - It inverts Dirichlet convolution with the constant-1 function: For arithmetic functions f, g,
                g(n) = Σ_{d|n} f(d)    ⇔    f(n) = Σ_{d|n} μ(d) * g(n/d)
        (Möbius inversion formula).
    - Relation with Euler's totient: Σ_{d|n} μ(d) * (n / d) = φ(n).
    - Summatory function M(x) = Σ_{n ≤ x} μ(n) is connected to the Riemann Hypothesis.

Algorithmic Notes
-----------------
A typical implementation:
    1. Factor n (trial division up to sqrt(n) for small inputs or a sieve / fast factoring for ranges).
    2. Track whether any prime factor appears with exponent > 1 (then return 0).
    3. Count distinct prime factors; return 1 if count is even, else -1.

Time Complexity
---------------
    - Single evaluation via trial division: O(sqrt(n)) in worst case.
    - With a precomputed smallest-prime-factor (SPF) sieve up to N: amortized near O(log n) per query.

Edge Cases
----------
    - n = 1 must return 1.
    - Perfect squares of primes (e.g., 4, 9, 25) return 0.
    - Large n with repeated factors should short-circuit early once a squared prime is found.
"""