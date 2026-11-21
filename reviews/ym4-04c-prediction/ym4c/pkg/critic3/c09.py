import sys
sys.path.insert(0, ".")
from spot import *
c = coef(HEADS["C03"])
def root_small(eps, theta):
    xl, xh = x_iv(eps, 0, theta)
    s0, _ = S_dS(xh, c, True)
    hi = 2 * s0
    while not met(eps, hi, theta, c): hi *= 2
    lo = Fr(0)
    for _ in range(70):
        m = (lo + hi) / 2
        if met(eps, m, theta, c): hi = m
        else: lo = m
    gl, gph = g_lo_gp_hi(eps, lo, theta, c)
    assert gl > 0 and gph < 0
    return lo, hi
def P10(b): return b**4/128 - b**6/768 + b**8/1536 - 467*b**10/2211840
for beta, istar, lo, hi in [(Fr(1,4000), 194, "5.2e-4", "5.3e-4"), (Fr(1,1000), 105, "0.133", "0.134")]:
    eps = eps6_iv(beta)
    vals = {}
    for i in (istar - 2, istar - 1, istar, istar + 1, istar + 2):
        th = Fr(1, 4) + Fr(i, 64)
        a = root_small(eps, th)
        e8 = exp_iv(-8 * th)
        T = (D(Fr(8489, 10000) * 6 * a[0] * e8[0]), U(Fr(8489, 10000) * 6 * a[1] * e8[1]))
        vals[i] = (T[0] / P10(beta), T[1] / P10(beta))
    show(f"C09 T/P_10 at beta={beta}, i={istar}", vals[istar], Fr(lo), Fr(hi))
    for i, v in vals.items():
        print(f"   i={i}: T/P_10 = {float(v[0]):.10g}  rel to i*: {float(v[0]/vals[istar][1]-1):.3e}")
