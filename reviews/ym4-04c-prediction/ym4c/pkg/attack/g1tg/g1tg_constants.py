# Second-seat attack on G1 (tree-graph / KP lens): independent exact enclosures.
# Fractions only; e^y by Taylor series with a rigorous remainder; outward dyadic rounding.
# Floats appear only in print formatting. Not an engine; not evidence.
from fractions import Fraction as F
import math

PREC = 220
SCALE = 1 << PREC

def rdn(x):  # round down to a dyadic of denominator 2^PREC
    return F(math.floor(x * SCALE), SCALE)

def rup(x):
    return F(math.ceil(x * SCALE), SCALE)

def exp_iv(q):
    """Enclosure [lo, hi] of e^q for rational q, |q| <= 16."""
    q = F(q)
    j = 0
    y = q
    while abs(y) > F(1, 16):
        y /= 2
        j += 1
    s = F(0); term = F(1); n = 0
    N = 30
    for n in range(N + 1):
        s += term
        term = term * y / (n + 1)
    # remainder <= |y|^{N+1}/(N+1)! * 1/(1-|y|)
    rem = abs(term) / (1 - abs(y))
    lo, hi = rdn(s - rem), rup(s + rem)
    for _ in range(j):
        lo, hi = rdn(lo * lo), rup(hi * hi)
    return lo, hi

def iv_mul(a, b):
    ps = [a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1]]
    return rdn(min(ps)), rup(max(ps))

def exp_of_iv(a):  # e^x over x in [a0,a1]
    return exp_iv(a[0])[0], exp_iv(a[1])[1]

KAPPA = F(1, 4)
EM1 = exp_iv(-1)

def dprime(delta):
    e = exp_iv(delta)
    return rdn(delta * e[0]), rup(delta * e[1])

def powers_scan(A, B, n0, extra=None, nmax=4000):
    """max over n>=n0 of A^n - B^n (+ extra(n)), A,B intervals in (0,1). Returns (lo,hi,argmax).
    Tail certificate: for n > N, value <= A_hi^n + extra_hi(n) which must fall below the running lo."""
    Ap = (F(1), F(1)); Bp = (F(1), F(1))
    for _ in range(n0):
        Ap = (rdn(Ap[0]*A[0]), rup(Ap[1]*A[1])); Bp = (rdn(Bp[0]*B[0]), rup(Bp[1]*B[1]))
    best_lo = None; best_hi = None; arg = None
    n = n0
    while n <= nmax:
        lo = Ap[0] - Bp[1]; hi = Ap[1] - Bp[0]
        if extra is not None:
            el, eh = extra(n); lo += el; hi += eh
        if best_lo is None or lo > best_lo:
            best_lo = lo; arg = n
        if best_hi is None or hi > best_hi:
            best_hi = hi
        # tail: any m>n has value <= A_hi^m + extra_hi(m) <= A_hi^{n+1} + extra_hi(n+1) (extra decreasing)
        nxt = Ap[1]*A[1] + (extra(n+1)[1] if extra is not None else 0)
        if n > n0 + 2 and nxt <= best_lo:
            return best_lo, best_hi, arg
        Ap = (rdn(Ap[0]*A[0]), rup(Ap[1]*A[1])); Bp = (rdn(Bp[0]*B[0]), rup(Bp[1]*B[1]))
        n += 1
    raise RuntimeError("scan did not certify the tail")

def c_frozen(delta):
    dp = dprime(delta)
    if 2*dp[1] > KAPPA/2:
        return None
    r = (KAPPA/2 - 2*dp[1], KAPPA/2 - 2*dp[0])
    A = exp_of_iv((-r[1], -r[0]))
    B = exp_iv(-KAPPA/2)
    mlo, mhi, arg = powers_scan(A, B, 4)
    ed = exp_iv(delta)
    return rdn(ed[0]*(EM1[0] + mlo)), rup(ed[1]*(EM1[1] + mhi)), arg

def c_star_A(delta, m_ge_1=False):
    """G1-a's c*: max{e^{-4k}, e^{d+2d'-5k}, e^d sup_{f>=4}(e^{-(k-2d')f}-e^{-kf})}.
    With m_ge_1=True, the third entry uses roots holding >= 1 line link: e^{d-k/2} sup_{f>=3} g(f)."""
    dp = dprime(delta)
    if 2*dp[1] > KAPPA:
        return None
    r = (KAPPA - 2*dp[1], KAPPA - 2*dp[0])
    A = exp_of_iv((-r[1], -r[0]))
    B = exp_iv(-KAPPA)
    ed = exp_iv(delta)
    e2 = exp_of_iv((delta + 2*dp[0] - 5*KAPPA, delta + 2*dp[1] - 5*KAPPA))
    if m_ge_1:
        mlo, mhi, arg = powers_scan(A, B, 3)
        h = exp_iv(-KAPPA/2)
        third = (rdn(ed[0]*h[0]*mlo), rup(ed[1]*h[1]*mhi))
    else:
        mlo, mhi, arg = powers_scan(A, B, 4)
        third = (rdn(ed[0]*mlo), rup(ed[1]*mhi))
    lo = max(EM1[0], e2[0], third[0]); hi = max(EM1[1], e2[1], third[1])
    return lo, hi, arg, e2, third

def c_B(delta):
    dp = dprime(delta)
    return exp_iv(delta + 16*dp[0] - 1)[0], exp_iv(delta + 16*dp[1] - 1)[1]

def c_sharp_B(delta):
    dp = dprime(delta)
    if 2*dp[1] > KAPPA/2:
        return None
    r = (KAPPA/2 - 2*dp[1], KAPPA/2 - 2*dp[0])
    A = exp_of_iv((-r[1], -r[0]))
    B = exp_iv(-KAPPA/2)
    def extra(n):
        if n < 9:
            return (F(0), F(0))
        v = exp_iv(-KAPPA*(n+1)/2)
        return v
    mlo, mhi, arg = powers_scan(A, B, 4, extra=extra)
    ed = exp_iv(delta)
    third = (rdn(ed[0]*mlo), rup(ed[1]*mhi))
    return max(EM1[0], third[0]), max(EM1[1], third[1]), arg, third

def fmt(x, d=10):
    return f"{float(x):.{d}g}"

def show(name, iv):
    print(f"{name}: [{fmt(iv[0])}, {fmt(iv[1])}]")

print("e^-1 in", fmt(EM1[0], 12), fmt(EM1[1], 12))

# ---- frozen c at the rows' points (point reads and bracket ends)
pts = {
 "C07 crude 1/100 delta_1=0.0110444507 (critic's read)": F(110444507, 10**10),
 "C07 lo 0.011044": F(11044, 10**6), "C07 hi 0.011045": F(11045, 10**6),
 "C08 lo 9.42e-6": F(942, 10**8), "C08 hi 9.45e-6": F(945, 10**8),
 "C13 49/1000": F(49, 1000), "C13 1/20": F(1, 20),
 "C14 1/64 lo 2.0347e-3": F(20347, 10**7), "C14 1/64 hi 2.0348e-3": F(20348, 10**7),
}
for k, d in pts.items():
    c = c_frozen(d); dp = dprime(d)
    print(f"{k}: 2d'=[{fmt(2*dp[0])},{fmt(2*dp[1])}] c_frozen=[{fmt(c[0])},{fmt(c[1])}] argmax_n={c[2]}")

# C10b / C10c inputs from s: delta_in = 12 s e^{6k}, 24 s e^{10k}
e15 = exp_iv(F(3, 2)); e25 = exp_iv(F(5, 2))
for s in [F(1, 2000), F(1, 4096)]:
    din = (rdn(12*s*e15[0]), rup(12*s*e15[1]))
    clo = c_frozen(din[0]); chi = c_frozen(din[1])
    ca_lo = c_star_A(din[0]); ca_hi = c_star_A(din[1])
    cs_lo = c_sharp_B(din[0]); cs_hi = c_sharp_B(din[1])
    print(f"C10b s=1/{1/s}: delta_in=[{fmt(din[0])},{fmt(din[1])}] c_frozen=[{fmt(clo[0])},{fmt(chi[1])}] "
          f"c*_A=[{fmt(ca_lo[0])},{fmt(ca_hi[1])}] c#_B=[{fmt(cs_lo[0])},{fmt(cs_hi[1])}] c_B=[{fmt(c_B(din[0])[0])},{fmt(c_B(din[1])[1])}]")
for s in [F(1, 8192), F(1, 65536)]:
    din = (rdn(24*s*e25[0]), rup(24*s*e25[1]))
    dp0 = dprime(din[0]); dp1 = dprime(din[1])
    clo = c_frozen(din[0]); chi = c_frozen(din[1])
    ca_lo = c_star_A(din[0]); ca_hi = c_star_A(din[1])
    cs_lo = c_sharp_B(din[0]); cs_hi = c_sharp_B(din[1])
    print(f"C10c s=1/{1/s}: delta_in=[{fmt(din[0])},{fmt(din[1])}] 2d'=[{fmt(2*dp0[0])},{fmt(2*dp1[1])}] c_frozen=[{fmt(clo[0])},{fmt(chi[1])}] "
          f"c*_A=[{fmt(ca_lo[0])},{fmt(ca_hi[1])}] c#_B=[{fmt(cs_lo[0])},{fmt(cs_hi[1])}] c_B=[{fmt(c_B(din[0])[0])},{fmt(c_B(din[1])[1])}]")

# ---- thresholds claimed in the derivations
def check(name, cond_lo_point, cond_hi_point):
    print(f"{name}: at lower grid point -> {cond_lo_point}; at upper grid point -> {cond_hi_point}")

d1, d2 = F(49617491, 10**9), F(49617492, 10**9)
check("frozen delta_crit (c^+<1 / c^->=1)", c_frozen(d1)[1] < 1, c_frozen(d2)[0] >= 1)

d1, d2 = F(58923670, 10**9), F(58923671, 10**9)
check("frozen C_k 2d'<=1/8 (holds / fails)", 2*dprime(d1)[1] <= F(1, 8), 2*dprime(d2)[0] > F(1, 8))
d1, d2 = F(111780108, 10**9), F(111780109, 10**9)
check("G1-a condition 2d'<=1/4 (holds / fails)", 2*dprime(d1)[1] <= F(1, 4), 2*dprime(d2)[0] > F(1, 4))

d1, d2 = F(72094, 10**6), F(72095, 10**6)
a1 = c_star_A(d1); a2 = c_star_A(d2)
check("G1-a c*=e^-1 edge (e^d Q upper <= e^-1 / lower > e^-1)",
      max(a1[3][1], a1[4][1]) <= EM1[0], max(a2[3][0], a2[4][0]) > EM1[1])
print("   at 0.072094: e^{d+2d'-5k}^+ =", fmt(a1[3][1]), " third^+ =", fmt(a1[4][1]), " argmax f =", a1[2])
print("   at 0.072095: third^- =", fmt(a2[4][0]), " argmax f =", a2[2])

d1, d2 = F(109530694, 10**9), F(109530695, 10**9)
a1 = c_star_A(d1); a2 = c_star_A(d2)
check("G1-a delta_crit* (c*^+<1 / c*^->=1)", a1[1] < 1, a2[0] >= 1)
print("   argmax f at delta_crit* =", a1[2], " c*^+ =", fmt(a1[1], 12))

# G1-b
def f89(delta):
    dp = dprime(delta)
    r = (KAPPA/2 - 2*dp[1], KAPPA/2 - 2*dp[0])
    A = exp_of_iv((-r[1], -r[0])); B = exp_iv(-KAPPA/2)
    A8 = (A[0]**8, A[1]**8); B8 = (B[0]**8, B[1]**8)
    lo = A8[0]*(1-A[1]) - B8[1]*(1-B[0]); hi = A8[1]*(1-A[0]) - B8[0]*(1-B[1])
    return lo, hi
d1, d2 = F(70256343, 10**10), F(70256344, 10**10)
check("G1-b delta_eq (f(8)-f(9) >0 / <0)", f89(d1)[0] > 0, f89(d2)[1] < 0)

d1, d2 = F(116995481, 10**10), F(116995482, 10**10)
b1 = c_sharp_B(d1); b2 = c_sharp_B(d2)
check("G1-b c#=e^-1 edge (third^+<=e^-1 / third^->e^-1)", b1[3][1] <= EM1[0], b2[3][0] > EM1[1])
print("   argmax n at the edge =", b1[2])

d1, d2 = F(558087801, 10**10), F(558087802, 10**10)
check("G1-b delta_crit(c_B) (c_B^+<1 / c_B^->=1)", c_B(d1)[1] < 1, c_B(d2)[0] >= 1)
d1, d2 = F(577661141, 10**10), F(577661142, 10**10)
check("G1-b delta_crit(c#) (c#^+<1 / c#^->=1)", c_sharp_B(d1)[1] < 1, c_sharp_B(d2)[0] >= 1)

# ---- chain values of C07 / C16 at the upper end of the delta_1 bracket
d = F(11045, 10**6)
c = c_frozen(d)[1]
print("C07 delta_2 <=", fmt(c*d), " sum <=", fmt(d/(1-c)), "  C16 delta_20 <=", fmt(c**19*d), " osc_20 <=", fmt(F(512)*c**19*d*EM1[1]))
d = F(110444507, 10**10)
c = c_frozen(d)
print("C16 at the critic's delta_1: delta_20 in [", fmt(c[0]**19*d), ",", fmt(c[1]**19*d), "]")

# ---- slack left in G1-a: roots at e_0 always hold the line link e_0 (m >= 1)
for d in [F(72095, 10**6), F(9, 100), F(1, 10)]:
    a = c_star_A(d); am = c_star_A(d, m_ge_1=True)
    print(f"G1-a c* at {fmt(d)}: as written [{fmt(a[0])},{fmt(a[1])}]; with m>=1 roots [{fmt(am[0])},{fmt(am[1])}]")
lo, hi = F(109530694, 10**9), F(111780108, 10**9)
for _ in range(34):
    mid = (lo + hi) / 2
    v = c_star_A(mid, m_ge_1=True)
    if v is not None and v[1] < 1:
        lo = mid
    else:
        hi = mid
print("G1-a with m>=1 roots: c*^+ < 1 up to delta >=", fmt(lo, 12), "(or the condition 2d'<=1/4 binds first)")
