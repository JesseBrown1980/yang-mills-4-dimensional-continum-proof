from fractions import Fraction as Fr
from itertools import product
class Q2:
    """u + v*sqrt2 with rational u, v."""
    def __init__(s, u, v=0): s.u, s.v = Fr(u), Fr(v)
    def __add__(s, o): o = o if isinstance(o, Q2) else Q2(o); return Q2(s.u + o.u, s.v + o.v)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, Q2) else Q2(o); return Q2(s.u - o.u, s.v - o.v)
    def __mul__(s, o): o = o if isinstance(o, Q2) else Q2(o); return Q2(s.u*o.u + 2*s.v*o.v, s.u*o.v + s.v*o.u)
    __rmul__ = __mul__
    def inv(s): n = s.u*s.u - 2*s.v*s.v; return Q2(s.u/n, -s.v/n)
    def __repr__(s): return f"{s.u} + ({s.v})sqrt2"
def four_sin2(n, b):
    """4 sin^2(pi n / b) for b in {2,4,8}, exactly in Q(sqrt2)."""
    n %= b
    # cos(2 pi n / b): 4 sin^2(x/2) = 2 - 2cos(x), x = 2 pi n/b
    cos8 = {0: Q2(1), 1: Q2(0, Fr(1, 2)), 2: Q2(0), 3: Q2(0, Fr(-1, 2)), 4: Q2(-1), 5: Q2(0, Fr(-1, 2)), 6: Q2(0), 7: Q2(0, Fr(1, 2))}
    return Q2(2) - 2 * cos8[n * (8 // b)]
def A(b, d):
    s = Q2(0)
    for n in product(range(b), repeat=d - 1):
        if all(x == 0 for x in n): continue
        k2 = Q2(0)
        for x in n: k2 = k2 + four_sin2(x, b)
        s = s + k2.inv()
    return s * Fr(1, b * b) - Fr(1, 12) * (1 - Fr(1, b * b))
for b in (2, 4, 8):
    print(f"d=4 A({b}) =", A(b, 4), "  d=3 A({b}) =", A(b, 3))
a3 = A(8, 4)
print("A_3 == 113360987/66106880:", a3.u == Fr(113360987, 66106880) and a3.v == 0)
a83 = A(8, 3)
print("A(8,3) == 54335/182784:", a83.u == Fr(54335, 182784) and a83.v == 0)
print("increments d=3:", A(4, 3).u - A(2, 3).u, a83.u - A(4, 3).u, "==6529/60928:", a83.u - A(4, 3).u == Fr(6529, 60928))
inc = a83.u - A(4, 3).u
print("increment in [0.1071592, 0.1071593]:", Fr(1071592, 10**7) <= inc <= Fr(1071593, 10**7))
print("A_k/2^k:", A(2,4).u/2, A(4,4).u/4, a3.u/8, " A_3/8 in [0.2143517,0.2143518]:", Fr(2143517,10**7) <= a3.u/8 <= Fr(2143518,10**7))
print("A_3 in [1.7148137531, 1.7148137532]:", Fr(17148137531, 10**10) <= a3.u <= Fr(17148137532, 10**10))
