"""Design-lane derivation check (not an engine): strong-coupling one-step couplings from the merged YM4-03C table.

Integers and Fractions only. Reads nothing from the repo; the coefficients are typed from NOTE-YM4-03C section 13.1.
"""
from fractions import Fraction as F

# log rho coefficients (c_F), d = 4, from S_eff = -log rho: c = -S coefficient
c_half = {4: F(1, 128), 6: F(-1, 768), 8: F(1, 1536), 10: F(-467, 2211840)}
c_one = {8: F(-19, 884736), 10: F(7, 884736)}
c_chair = {10: F(3, 524288)}
c_half_d3 = {4: F(1, 128), 6: F(-1, 768), 8: F(5, 12288), 10: F(-1013, 8847360)}
# d = 2 planar: c_half = series of 2 t_2^4, c_one = series of 3 t_3^4 - 2 t_2^8
c_half_d2 = {4: F(1, 128), 6: F(-1, 768), 8: F(1, 6144), 10: F(-79, 4423680)}


def series_mul(a, b, top=12):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            if i + j <= top:
                out[i + j] = out.get(i + j, 0) + x * y
    return out


# check the planar series from t_n: t2 = b/4 - b^3/96 + b^5/1536 - b^7/23040 + 13 b^9/4423680
t2 = {1: F(1, 4), 3: F(-1, 96), 5: F(1, 1536), 7: F(-1, 23040), 9: F(13, 4423680)}
t3 = {2: F(1, 24), 4: F(-1, 384), 6: F(1, 5760), 8: F(-13, 1105920)}
t2_4 = series_mul(series_mul(t2, t2), series_mul(t2, t2))
t3_4 = series_mul(series_mul(t3, t3), series_mul(t3, t3))
t2_8 = series_mul(t2_4, t2_4)
planar_half = {k: 2 * v for k, v in t2_4.items() if k <= 10}
planar_one = {k: 3 * t3_4.get(k, 0) - 2 * t2_8.get(k, 0) for k in (8, 10)}
print("planar 2t2^4 =", planar_half)
print("planar 3t3^4-2t2^8 =", planar_one)
assert planar_half == c_half_d2
assert planar_one == c_one


def beta_S(ch):
    return {k: 2 * v for k, v in ch.items()}


def beta_q(ch, d):
    chairs_per_plaquette = 8 * (d - 2)
    out = {}
    for k in (4, 6, 8, 10):
        v = 2 * ch.get(k, 0) + 8 * c_one.get(k, 0) + 2 * chairs_per_plaquette * c_chair.get(k, 0)
        out[k] = v
    return out


for d, ch in ((2, c_half_d2), (3, c_half_d3), (4, c_half)):
    print("d=%d beta'_S =" % d, beta_S(ch))
    print("d=%d beta'_q(p->0, axis p) =" % d, beta_q(ch, d))
    diff = {k: beta_q(ch, d)[k] - beta_S(ch).get(k, 0) for k in (4, 6, 8, 10)}
    print("d=%d beta'_q - beta'_S =" % d, diff)

# the 2D exact small-field formula expanded: (1/3) sum n^2(n^2-1) t_n^4 / sum n^2 t_n^4 = 4t2^4 + 24 t3^4 - 16 t2^8 + O(b^12)
two_d = {k: 4 * t2_4.get(k, 0) + 24 * t3_4.get(k, 0) - 16 * t2_8.get(k, 0) for k in (4, 6, 8, 10)}
print("d=2 exact-formula expansion =", two_d)
assert two_d == beta_q(c_half_d2, 2)

# beta^12 split between character matching and action projection: 2 c_half c_one
print("beta'_chi - beta'_S at beta^12 =", 2 * c_half[4] * c_one[8])

# Wilson-only proxy of YM4-04A at b = 2: 4 (beta/4)^4 = beta^4/64; deviation of beta'_q at beta^6
print("proxy deviation at beta^6 =", beta_q(c_half, 4)[6])
