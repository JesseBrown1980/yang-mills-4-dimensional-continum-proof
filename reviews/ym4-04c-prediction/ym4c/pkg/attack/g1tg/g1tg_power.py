# What the C10b and C10c reads test, compared with G1's multi-object part (exact enclosures; display floats).
import sys, io, contextlib
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from fractions import Fraction as F
with contextlib.redirect_stdout(io.StringIO()):
    from g1tg_constants import exp_iv, rdn, rup, dprime, c_frozen, c_star_A, EM1, fmt
e15 = exp_iv(F(3, 2)); e25 = exp_iv(F(5, 2))
# C10b, s = 1/2000: delta_in = 12 s e^{3/2}; frozen delta_out and projection bound brackets from the draft row
s = F(1, 2000)
din = (rdn(12*s*e15[0]), rup(12*s*e15[1]))
c = c_frozen(din[1]); ed = exp_iv(din[1])
multi_frozen = c[1] - ed[0]*EM1[0]          # e^d max_n f(n), the frozen multi-object part (upper)
dp = dprime(din[1])
# G1-a's per-root factor for C10b's roots (rectangles: f = 2 off, m = 4 line): e^{d} e^{-4k}(e^{4d'}-1)
qa = ed[1]*EM1[1]*(exp_iv(4*dp[1])[1] - 1)
out_nat = (F(4077, 10**9), F(4078, 10**9)); proj = (F(400, 10**9), F(401, 10**9))
print("C10b s=1/2000: delta_in =", fmt(din[1]))
print("  frozen c*delta_in / projection bound >=", fmt(c[0]*din[0]/proj[1]))
print("  frozen multi-object part e^d max f <=", fmt(multi_frozen), "; times delta_in / natural delta_out in [",
      fmt((c[0]-ed[1]*EM1[1])*din[0]/out_nat[1]), ",", fmt(multi_frozen*din[1]/out_nat[0]), "]; / projection bound <=", fmt(multi_frozen*din[1]/proj[0]))
print("  G1-a per-root factor for these roots <=", fmt(qa), "; times delta_in / natural delta_out <=", fmt(qa*din[1]/out_nat[0]),
      "; / projection bound <=", fmt(qa*din[1]/proj[0]))
# C10c: delta_in = 24 s e^{5/2}; v2 brackets bound/delta_in and natural/delta_in
for s, nat, bnd in [(F(1, 8192), (F(557553, 10**7), F(558098, 10**7)), (F(328285, 10**7), F(328860, 10**7))),
                    (F(1, 65536), (F(557791, 10**7), F(557860, 10**7)), (F(328523, 10**7), F(328622, 10**7)))]:
    din = (rdn(24*s*e25[0]), rup(24*s*e25[1]))
    cf = c_frozen(din[1]); ca = c_star_A(din[1]); ed = exp_iv(din[1]); dp = dprime(din[1])
    # G1-a's per-root factor for C10c's root (f = 2 off, m = 8 line): e^d q(2,8) = e^{d - 6k + 4d'}
    q28 = exp_iv(din[1] - F(3, 2) + 4*dp[1])[1]
    assert F(5,100) < nat[0] < F(6,100) and F(3,100) < bnd[0] < F(4,100)
    print(f"C10c s=1/{1/s}: slack every-decomp vs frozen c >= {fmt(cf[0]/bnd[1])}; vs G1-a c* >= {fmt(ca[0]/bnd[1])}; "
          f"vs G1-a per-root factor {fmt(q28)} >= {fmt(exp_iv(din[0]-F(3,2))[0]/bnd[1])}; natural vs per-root >= {fmt(exp_iv(din[0]-F(3,2))[0]/nat[1])}")
