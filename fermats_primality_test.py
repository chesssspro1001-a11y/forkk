#probabilistic (not deterministic)
#fermats little theorem : a**(p-1) ≡ 1 (mod p) for prime p
#but it can also hold for a composite number so we need to be careful 
#very fast and Carmichael numbers are very rare (only 646 in <= 1e9)
#Carmichael Numbers ; 561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341 , ...


import random
def fermat_primality_test(n: int, iterations: int = 5) -> bool:
    if n < 4:
        return n in (2, 3)
    for _ in range(iterations):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True
