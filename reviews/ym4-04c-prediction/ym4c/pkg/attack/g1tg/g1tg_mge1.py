# G1-a's c* with roots restricted to m >= 1 line links: where it leaves e^{-1} (search read on the 1e-9 grid).
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from fractions import Fraction as F
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from g1tg_constants import c_star_A, EM1, fmt
lo, hi = F(72094, 10**6), F(111780108, 10**9)
def at_em1(d):
    a = c_star_A(d, m_ge_1=True)
    return a is not None and max(a[3][1], a[4][1]) <= EM1[0]
assert at_em1(lo)
for _ in range(40):
    mid = (lo + hi) / 2
    if at_em1(mid): lo = mid
    else: hi = mid
g = F(int(lo * 10**9), 10**9)
print("m>=1 roots: e^d Q^+ <= e^-1 at", fmt(g, 12), ":", at_em1(g), "; at", fmt(g + F(1, 10**9), 12), ":", at_em1(g + F(1, 10**9)))
a = c_star_A(F(111780108, 10**9), m_ge_1=True)
print("m>=1 roots at the condition edge 0.111780108: c*^+ =", fmt(a[1], 10), "argmax f =", a[2])
