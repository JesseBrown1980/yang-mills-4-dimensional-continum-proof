#!/usr/bin/env python3
"""YM4-04C v2 repair lane: exact W-lane rechecks (integers and Fractions only; floats only in display).

A(b,d) = b^-2 * sum_{n in Z_b^(d-1), n != 0} 1/khat^2(2 pi n/b) - (1 - b^-2)/12, khat^2(k) = sum_i 4 sin^2(k_i/2).
For b in {2,4,8}, 4 sin^2(pi m/b) lies in Q(sqrt2), so A(b,d) = p + q*sqrt2 exactly.
"""
from fractions import Fraction as Fr
import itertools

class Q2:
    """p + q*sqrt2 with p, q rational."""
    __slots__ = ("p", "q")
    def __init__(self, p, q=0): self.p, self.q = Fr(p), Fr(q)
    def __add__(s, o): o = o if isinstance(o, Q2) else Q2(o); return Q2(s.p + o.p, s.q + o.q)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, Q2) else Q2(o); return Q2(s.p - o.p, s.q - o.q)
    def __mul__(s, o): o = o if isinstance(o, Q2) else Q2(o); return Q2(s.p*o.p + 2*s.q*o.q, s.p*o.q + s.q*o.p)
    __rmul__ = __mul__
    def inv(s):
        n = s.p*s.p - 2*s.q*s.q
        assert n != 0
        return Q2(s.p/n, -s.q/n)
    def __truediv__(s, o): o = o if isinstance(o, Q2) else Q2(o); return s * o.inv()
    def __eq__(s, o): o = o if isinstance(o, Q2) else Q2(o); return s.p == o.p and s.q == o.q
    def sign(s):
        """exact sign of p + q sqrt2"""
        p, q = s.p, s.q
        if q == 0: return (p > 0) - (p < 0)
        if p == 0: return (q > 0) - (q < 0)
        if p > 0 and q > 0: return 1
        if p < 0 and q < 0: return -1
        # opposite signs: compare p^2 with 2 q^2
        if p > 0: return 1 if p*p > 2*q*q else -1
        return 1 if 2*q*q > p*p else -1
    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0

def s2tab(b):
    """4 sin^2(pi m/b) for m = 0..b-1, exactly in Q(sqrt2), b in {2,4,8}."""
    if b == 2: return [Q2(0), Q2(4)]
    if b == 4: return [Q2(0), Q2(2), Q2(4), Q2(2)]
    if b == 8:
        # 4 sin^2(pi m/8) = 2 - 2 cos(pi m/4); cos(pi m/4) = 1, 1/sqrt2, 0, -1/sqrt2, -1, ...
        c = [Q2(1), Q2(0, Fr(1, 2)), Q2(0), Q2(0, Fr(-1, 2)), Q2(-1), Q2(0, Fr(-1, 2)), Q2(0), Q2(0, Fr(1, 2))]
        return [Q2(2) - 2*x for x in c]
    raise ValueError(b)

def A(b, d):
    t = s2tab(b); tot = Q2(0)
    for n in itertools.product(range(b), repeat=d - 1):
        if any(n):
            den = Q2(0)
            for m in n: den = den + t[m]
            tot = tot + den.inv()
    return tot * Fr(1, b*b) - (1 - Fr(1, b*b)) / 12

def enclose(x, den):
    """[lo, hi] on the grid 1/den with lo <= x < hi, decided by exact sign tests."""
    # x = p + q sqrt2; find integer k with k/den <= x < (k+1)/den by bisection
    lo, hi = -10**6 * den, 10**6 * den
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if Q2(Fr(mid, den)) <= x: lo = mid
        else: hi = mid
    return Fr(lo, den), Fr(hi, den)

def show(name, x, den=10**10):
    lo, hi = enclose(x, den)
    print(f"{name} = {x.p} + ({x.q})*sqrt2 ; in [{float(lo):.10f}, {float(hi):.10f}] (grid 1/{den})")
    return lo, hi

if __name__ == "__main__":
    print("== W03 (d = 3) ==")
    A2, A4, A8 = A(2, 3), A(4, 3), A(8, 3)
    print("A(2,3) =", A2.p, "q =", A2.q, " expected 3/32:", A2 == Q2(Fr(3, 32)))
    print("A(4,3) =", A4.p, "q =", A4.q, " expected 73/384:", A4 == Q2(Fr(73, 384)))
    show("A(8,3)", A8)
    inc1 = A4 - A2
    print("increment A(4,3)-A(2,3) =", inc1.p, "(37/384:", inc1 == Q2(Fr(37, 384)), ")")
    inc2 = A8 - A4
    show("increment A(8,3)-A(4,3)", inc2)
    lo, hi = Fr(1071592, 10**7), Fr(1071593, 10**7)
    print("new bracket [0.1071592, 0.1071593] contains it:", Q2(lo) <= inc2 and inc2 <= Q2(hi), "(strict:", Q2(lo) < inc2 and inc2 < Q2(hi), ")")
    print("old bracket [0.10716, 0.10717] contains it:", Q2(Fr(10716, 10**5)) <= inc2 and inc2 <= Q2(Fr(10717, 10**5)))
    print("both increments inside [0.09, 0.12]:", Q2(Fr(9, 100)) <= inc1 and inc1 <= Q2(Fr(12, 100)) and Q2(Fr(9, 100)) <= inc2 and inc2 <= Q2(Fr(12, 100)))
    print("== W01 (d = 4) ==")
    B2, B4, B8 = A(2, 4), A(4, 4), A(8, 4)
    print("A_1 = A(2,4) =", B2.p, " (23/96:", B2 == Q2(Fr(23, 96)), ")")
    print("A_2 = A(4,4) =", B4.p, " (1367/1920:", B4 == Q2(Fr(1367, 1920)), ")")
    a3lo, a3hi = show("A_3 = A(8,4)", B8)
    print("A_3 in [1.7148137531, 1.7148137532]:", Q2(Fr(17148137531, 10**10)) <= B8 and B8 <= Q2(Fr(17148137532, 10**10)))
    print("A_1/2 =", B2.p / 2, "=", f"{float(B2.p/2):.6f}", "; A_2/4 =", B4.p / 4, "=", f"{float(B4.p/4):.6f}")
    show("A_3/8", B8 * Fr(1, 8))
    q1, q2, q3 = B2 * Fr(1, 2), B4 * Fr(1, 4), B8 * Fr(1, 8)
    print("A_k/2^k strictly increasing:", q1 < q2 and q2 < q3)
    # Watson's G_3(0) is REPORTED; the inequality uses only its lower bound 0.2527
    print("A_3/8 < 0.2527:", q3 < Q2(Fr(2527, 10000)))
    print("== W07 aligned-tile polynomial ==")
    for c in (Fr(63, 65), Fr(255, 257), Fr(1023, 1025)):
        eps = 1 - c
        cos4 = 8*c**4 - 8*c**2 + 1
        ratio = (1 - cos4) / eps
        poly = 16 - 40*eps + 32*eps**2 - 8*eps**3
        print(f"cos theta = {c}: (1-cos4theta)/eps = {ratio} ; 16-40eps+32eps^2-8eps^3 = {poly} ; equal: {ratio == poly} ; < 16: {ratio < 16}")
    print("== drop_alias_terms corner (b=2, d=4, q=pi, keep n=0 only) ==")
    # khat^2 at k = (pi/2) e_nu is 2; C' = b^(2-d) * (1/2) = 1/8; C'_W = 1/(4 sin^2(pi/2)) = 1/4
    print("r_1 with only n = 0 kept:", Fr(1, 4) / (Fr(1, 4) * Fr(1, 2)), "; full alias sum r_1 = 15/28 (W01)")
