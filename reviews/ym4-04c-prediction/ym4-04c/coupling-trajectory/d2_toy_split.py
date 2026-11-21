"""Design-lane derivation check: one SU(2) plaquette variable with density exp(c_h chi_1/2 + c_1 chi_1).

<chi_1/2> by exact Haar moments (Catalan numbers), then the Wilson inversion 2 t_2(y) = y/2 - y^3/48 + ...,
compared with 2 c_h.  The beta^12 term of c_h is an arbitrary placeholder X, which must cancel.
Series in beta are dicts {power: Fraction}; truncation at beta^12.
"""
from fractions import Fraction as F
from math import comb

TOP = 12


def mul(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            if i + j <= TOP:
                out[i + j] = out.get(i + j, 0) + x * y
    return {k: v for k, v in out.items() if v != 0}


def add(*xs):
    out = {}
    for a in xs:
        for k, v in a.items():
            out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v != 0}


def scal(s, a):
    return {k: s * v for k, v in a.items()}


def catalan(m):
    return F(comb(2 * m, m), m + 1)


def moment(p):  # E_Haar[x^p], x = chi_1/2
    return catalan(p // 2) if p % 2 == 0 else F(0)


X = F(12345, 678910)  # placeholder beta^12 coefficient of c_h
c_h = {4: F(1, 128), 6: F(-1, 768), 8: F(1, 1536), 10: F(-467, 2211840), 12: X}
c_1 = {8: F(-19, 884736), 10: F(7, 884736)}

# f = c_h x + c_1 (x^2 - 1): represent polynomial in x with series coefficients: {deg: series}
f = {1: c_h, 2: c_1, 0: scal(-1, c_1)}


def pmul(p, q):
    out = {}
    for i, a in p.items():
        for j, b in q.items():
            s = mul(a, b)
            if s:
                out[i + j] = add(out.get(i + j, {}), s)
    return out


# e^f up to f^3 (f is O(beta^4); f^4 is O(beta^16))
one = {0: {0: F(1)}}
f2 = pmul(f, f)
f3 = pmul(f2, f)
ef = {}
for p, s in ((one, F(1)), (f, F(1)), (f2, F(1, 2)), (f3, F(1, 6))):
    for deg, ser in p.items():
        ef[deg] = add(ef.get(deg, {}), scal(s, ser))


def expect(poly):  # E_Haar of polynomial in x with series coefficients
    out = {}
    for deg, ser in poly.items():
        m = moment(deg)
        if m:
            out = add(out, scal(m, ser))
    return out


num = expect(pmul({1: {0: F(1)}}, ef))
den = expect(ef)
# 1/den as series: den = 1 + small
small = add(den, {0: F(-1)})
inv = {0: F(1)}
term = {0: F(1)}
for _ in range(4):
    term = scal(-1, mul(term, small))
    inv = add(inv, term)
mean = mul(num, inv)
print("<chi_1/2> =", mean)
y = scal(2, mean)
y = add(y, scal(F(1, 24), mul(mul(y, y), y)))
y = add(scal(2, mean), scal(F(1, 24), mul(mul(y, y), y)))
print("beta'_chi =", y)
diff = add(y, scal(-2, c_h))
print("beta'_chi - beta'_S =", diff)
assert diff == {12: F(-19, 56623104)}
print("OK: split is -19/56623104 beta^12 and the placeholder cancels")
