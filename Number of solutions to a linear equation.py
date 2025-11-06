import sys
#number of solutions to a linear equation  with a1 + a2 + a3 + ...an = s given a1 < x1 < a2 < x2 < ... < an < xn
MOD = 10**9 + 7

def mod_pow(a, b):
    res = 1
    while b:
        if b & 1:
            res = res * a % MOD
        a = a * a % MOD
        b >>= 1
    return res

MAX_INV = 55
inv = [0] * MAX_INV
for i in range(1, MAX_INV):
    inv[i] = mod_pow(i, MOD - 2)

def nCr_largeN(N, r):
    if r < 0:
        return 0
    if r == 0:
        return 1
    if r > N - r:
        r = N - r
    if r < 0:
        return 0
    ans = 1
    for i in range(r):
        ans = ans * ((N - i) % MOD) % MOD
        ans = ans * inv[i + 1] % MOD
    return ans


data = sys.stdin.read().strip().split()

it = iter(data)
n = int(next(it))
s = int(next(it))
f = [int(next(it)) for _ in range(n)]

ans = 0
for mask in range(1 << n):
    x = s
    bits = 0
    m = mask
    i = 0
    while m:
        if m & 1:
            x -= f[i] + 1
            bits += 1
        m >>= 1
        i += 1

    if x < 0:
        continue
    temp = nCr_largeN(x + n - 1, n - 1)
    if bits & 1:
        temp = -temp
    ans = (ans + temp) % MOD

print(ans % MOD)
