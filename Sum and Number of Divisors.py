# Number theory utilities: count and sum of divisors.
# both are multiplicative functions f(a*b) = f(a) * f(b)

def number_of_divisors(n: int) -> int:
    """
    Returns the number of positive divisors of n.
    """
    if n == 1:
        return 1

    count = 1
    # Factor 2
    exp = 0
    while n % 2 == 0:
        n //= 2
        exp += 1
    if exp:
        count *= (exp + 1)

    p = 3
    while p * p <= n:
        if n % p == 0:
            exp = 0
            while n % p == 0:
                n //= p
                exp += 1
            count *= (exp + 1)
        p += 2

    if n > 1:
        count *= 2  # remaining prime factor
    return count


def sum_of_divisors(n: int) -> int:
    """
    Returns the sum of positive divisors of n.
    """
    if n == 1:
        return 1

    total = 1
    # Factor 2
    if n % 2 == 0:
        exp = 0
        pow2 = 1
        sum2 = 1
        while n % 2 == 0:
            n //= 2
            exp += 1
            pow2 <<= 1  # multiply by 2
            sum2 += pow2
        total *= sum2

    p = 3
    while p * p <= n:
        if n % p == 0:
            pow_p = 1
            sum_p = 1
            while n % p == 0:
                n //= p
                pow_p *= p
                sum_p += pow_p
            total *= sum_p
        p += 2

    if n > 1:
        total *= (1 + n)  # remaining prime factor
    return total



def sum_of_div_MOD(n):
    n = int(input().strip())
    MOD = 10**9 + 7
    
    ans = 0
    l = 1
    
    while l <= n:
        t = n // l
        r = n // t
    
        cnt_sum = (l + r) * (r - l + 1) // 2
        ans = (ans + (cnt_sum % MOD) * (t % MOD)) % MOD
        l = r + 1
    
    print(ans)
