"""Design-lane derivation check: exact tree-level values that the prediction freezes (Fractions only).

Line map, d = 4, polarization mu, momentum kappa e_nu:
  corner kappa = pi, b = 4: the sqrt(2) parts cancel between n_nu and b-1-n_nu, so r is rational.
  small-p slope A_b(0) = b^(2-d) sum_{n != 0} 1/khat^2(2 pi n/b) - (1 - 1/b^2)/12, rational for b = 2, 4.
Averaged map: r_avg(pi; b) = 3 b^2/(b^2 + 2) and A_avg(0; b) = -(1 - 1/b^2)/6 (checked here at b = 2 by the
finite-difference of the alias formula in Decimal; see d3_tree.py for the csc^4 identity).
"""
from fractions import Fraction as F
import itertools

# 4 sin^2(pi m / 4) for m = 0..3
s4 = [F(0), F(2), F(4), F(2)]
# corner b = 4: pair (2 - sqrt2 + t) and (2 + sqrt2 + t): sum = (4 + 2t)/((2 + t)^2 - 2), two such pairs over n_nu
S = F(0)
for m1, m2 in itertools.product(range(4), repeat=2):
    t = s4[m1] + s4[m2]
    S += 2 * (4 + 2 * t) / ((2 + t) ** 2 - 2)
C = S / 16  # b^(2-d) = 1/16
r4 = F(1, 4) / C
print("b=4 corner: S =", S, " r_line(pi;4) =", r4, "=", float(r4))
print("b=2 corner r =", F(15, 28), " b*r:", 2 * F(15, 28), 4 * r4)

for b, sv in ((2, [F(0), F(4)]), (4, s4)):
    tot = F(0)
    for n in itertools.product(range(b), repeat=3):
        if n == (0, 0, 0):
            continue
        tot += 1 / sum(sv[m] for m in n)
    A = F(1, b * b) * tot - (1 - F(1, b * b)) / 12
    print("line A_%d(0) = %s = %.12f" % (b, A, float(A)))

for b in (2, 4, 8):
    print("avg b=%d: r(pi) = %s, A(0) = %s" % (b, F(3 * b * b, b * b + 2), -(1 - F(1, b * b)) / 6))
