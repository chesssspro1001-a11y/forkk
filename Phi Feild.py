MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

class Field:
    # represents a + b * sqrt(5)
    __slots__ = ("a", "b")
    def __init__(self, a=0, b=0):
        self.a = a % MOD
        self.b = b % MOD
    def __add__(self, o):
        return Field(self.a + o.a, self.b + o.b)
    def __sub__(self, o):
        return Field(self.a - o.a, self.b - o.b)
    def __mul__(self, o):
        if isinstance(o, Field):
            # (a1 + b1√5)(a2 + b2√5) = (a1a2 + 5 b1b2) + (a1b2 + a2b1)√5
            return Field(self.a * o.a + 5 * self.b * o.b,
                         self.a * o.b + self.b * o.a)
        else:
            return Field(self.a * o, self.b * o)
    def inv(self):
        # 1 / (a + b√5) = (a - b√5) / (a^2 - 5 b^2)
        denom = (self.a * self.a - 5 * self.b * self.b) % MOD
        invd = modinv(denom)
        return Field(self.a * invd, (-self.b) * invd)
    def __truediv__(self, o):
        if isinstance(o, Field):
            return self * o.inv()
        else:
            invo = modinv(o)
            return Field(self.a * invo, self.b * invo)
    def pow(self, e):
        r = Field(1, 0)
        b = self
        while e:
            if e & 1:
                r = r * b
            b = b * b
            e >>= 1
        return r

# phi = (1 + sqrt(5)) / 2  => coefficients (1/2, 1/2)
inv2 = (MOD + 1) // 2
phi = Field(inv2, inv2)

def fib(n: int):
    if n == 0:
        return 0
    a = phi.pow(n)
    b = (Field(1, 0) - phi).pow(n)
    num = a - b  # (phi^n - (1 - phi)^n)
    res = num / Field(0, 1)  # divide by sqrt(5)
    # result should be purely real
    assert res.b % MOD == 0
    return res.a % MOD

