# G1 channel attack: exact checks. Fractions only; exp by Taylor with a remainder bound,
# outward-rounded to dyadics of denominator 2^PREC. Floats appear only in print formatting.
from fractions import Fraction as F
import itertools, sys

PREC = 160
ONE = F(1)
KAPPA = F(1, 4)


def rdown(x):
    d = 1 << PREC
    n = (x.numerator * d) // x.denominator
    return F(n, d)


def rup(x):
    d = 1 << PREC
    n = -((-x.numerator * d) // x.denominator)
    return F(n, d)


def exp_iv(x):
    """Return (lo, hi) with lo <= e^x <= hi, x a Fraction."""
    if x < 0:
        lo, hi = exp_iv(-x)
        return rdown(ONE / hi), rup(ONE / lo)
    j = 0
    y = x
    while y > F(1, 64):
        y /= 2
        j += 1
    s = F(0)
    term = F(1)
    k = 0
    while True:
        s += term
        k += 1
        term = term * y / k
        if term < F(1, 1 << (PREC + 20)):
            break
    # remainder <= term * 1/(1 - y/(k+1)) <= 2*term
    lo, hi = rdown(s), rup(s + 2 * term)
    for _ in range(j):
        lo, hi = rdown(lo * lo), rup(hi * hi)
    return lo, hi


def elo(x):
    return exp_iv(x)[0]


def ehi(x):
    return exp_iv(x)[1]


def dprime(d):
    lo, hi = exp_iv(d)
    return rdown(d * lo), rup(d * hi)


def fmt(x, n=10):
    return f"{float(x):.{n}f}"


# ---------- frozen c(delta) ----------
def frozen_c(d, k=KAPPA):
    """Enclosure of e^d [e^{-4k} + max_{n>=4}(e^{-(k/2-2d')n} - e^{-kn/2})], d rational, C_k strict."""
    d1, d2 = dprime(d)
    u1, u2 = k / 2 - 2 * d1, k / 2 - 2 * d2   # u2 <= u1
    assert u2 > 0, "C_k strict needed"
    # certified tail start N: f(.;d2) decreasing for n >= N iff e^{2 d2 N} * u2 >= k/2
    N = 4
    while elo(2 * d2 * N) * u2 < k / 2:
        N += 1
    best_hi, best_lo, arg = F(0), F(0), None
    for n in range(4, N + 1):
        hi = ehi(-u2 * n) - elo(-k * n / 2)
        lo = elo(-u1 * n) - ehi(-k * n / 2)
        if hi > best_hi:
            best_hi = hi
        if lo > best_lo:
            best_lo, arg = lo, n
    e4lo, e4hi = exp_iv(-4 * k)
    edlo, edhi = exp_iv(d)
    return rdown(edlo * (e4lo + best_lo)), rup(edhi * (e4hi + best_hi)), arg, N


# ---------- route A: c*(delta) closed form (Lemma 4.16), and brute-force Q ----------
def cstar_A(d, k=KAPPA, mmin=0):
    """max{e^{-4k}, e^{d+2d'-5k}, e^d e^{-k*mmin/2} sup_{f>=4} g(f)}; mmin=1 is the root-holds-e_0 sharpening."""
    d1, d2 = dprime(d)
    v1, v2 = k - 2 * d1, k - 2 * d2
    assert v2 > 0
    N = 4
    while elo(2 * d2 * N) * v2 < k:
        N += 1
    best_hi, best_lo, arg = F(0), F(0), None
    for f in range(4, N + 1):
        hi = ehi(-v2 * f) - elo(-k * f)
        lo = elo(-v1 * f) - ehi(-k * f)
        best_hi = max(best_hi, hi)
        if lo > best_lo:
            best_lo, arg = lo, f
    edlo, edhi = exp_iv(d)
    emlo, emhi = exp_iv(-k * mmin / 2)
    t3 = (rdown(edlo * emlo * best_lo), rup(edhi * emhi * best_hi))
    t2 = (elo(d + 2 * d1 - 5 * k), ehi(d + 2 * d2 - 5 * k))
    t1 = exp_iv(-4 * k)
    lo = max(t1[0], t2[0], t3[0])
    hi = max(t1[1], t2[1], t3[1])
    return lo, hi, arg, (t1, t2, t3)


def Q_brute_A(d, k=KAPPA, fmax=80, mmax=80, mmin=0):
    """sup over 1<=f<=fmax, mmin<=m<=mmax, f+m>=4 of q(f,m) (upper enclosure), for a check of Lemma 4.16."""
    d1, d2 = dprime(d)
    best = F(0)
    arg = None
    for f in range(1, fmax + 1):
        A = ehi(2 * d2 * f) - 1
        for m in range(mmin, mmax + 1):
            if f + m < 4:
                continue
            single = ehi(-k * (m % 2) / 2) if m >= 8 else F(0)
            q = ehi(-k * (f + m) + k * m / 2) * (single + A)
            if q > best:
                best, arg = q, (f, m)
    return best, arg


# ---------- route B: c_B and c_sharp ----------
def cB(d, k=KAPPA):
    d1, d2 = dprime(d)
    return elo(d + 16 * d1 - 4 * k), ehi(d + 16 * d2 - 4 * k)


def csharp_B(d, k=KAPPA, sm1=False):
    """max{e^{-4k}, e^d max_{n>=4} [f(n) + 1[n>=9]e^{-k(n+1)/2}]}; sm1: use s <= n-1 (root holds l_0)."""
    d1, d2 = dprime(d)
    u1, u2 = k / 2 - 2 * d1, k / 2 - 2 * d2
    assert u2 > 0
    N = 4
    while elo(2 * d2 * N) * u2 < k / 2:
        N += 1
    N += 2
    best_hi, best_lo, arg = F(0), F(0), None
    for n in range(4, N + 1):
        s = n - 1 if sm1 else n
        # e^{-kn/2}(e^{2d's}-1)
        hi = ehi(-k * n / 2) * (ehi(2 * d2 * s) - 1)
        lo = elo(-k * n / 2) * (elo(2 * d1 * s) - 1)
        if n >= 9:
            hi += ehi(-k * (n + 1) / 2)
            lo += elo(-k * (n + 1) / 2)
        best_hi = max(best_hi, hi)
        if lo > best_lo:
            best_lo, arg = lo, n
    edlo, edhi = exp_iv(d)
    e4 = exp_iv(-4 * k)
    return max(e4[0], rdown(edlo * best_lo)), max(e4[1], rup(edhi * best_hi)), arg


def leaves(fun, a, b, target_hi, steps=40, grid=F(1, 10**10)):
    """Bisection: largest grid point x in [a,b] with upper(fun(x)) <= target_hi (fun nondecreasing)."""
    lo, hi = a, b
    for _ in range(steps):
        mid = F(((lo + hi) / 2 / grid).__floor__()) * grid
        if mid <= lo:
            break
        if fun(mid) <= target_hi:
            lo = mid
        else:
            hi = mid
    return lo, hi


out = []


def P(*a):
    s = " ".join(str(x) for x in a)
    out.append(s)
    print(s)
    sys.stdout.flush()


e1 = exp_iv(F(-1))
P("e^-1 in", fmt(e1[0], 12), fmt(e1[1], 12))

# ---------- 1. the draft's points ----------
pts = [
    ("C07 crude 1/100", F(11044, 10**6), F(11045, 10**6), (F(44504, 10**5), F(44505, 10**5)), (F(2233, 10**5), F(2234, 10**5))),
    ("C08 refined 1/100", F(942, 10**8), F(945, 10**8), (F(36793, 10**5), F(36795, 10**5)), None),
    ("C10b s=1/2000", F(26890, 10**6), F(26891, 10**6), (F(5950, 10**4), F(5951, 10**4)), (F(5524, 10**5), F(5525, 10**5))),
    ("C10b s=1/4096", F(13129, 10**6), F(13131, 10**6), (F(4617, 10**4), F(4618, 10**4)), None),
    ("C14 refined 1/64", F(20347, 10**7), F(20348, 10**7), (F(38085, 10**5), F(38086, 10**5)), None),
    ("C13 49/1000", F(49, 1000), F(49, 1000), (F(98248, 10**5), F(98249, 10**5)), None),
    ("C13 1/20", F(1, 20), F(1, 20), (F(10110, 10**4), F(10111, 10**4)), None),
]
P("\n== 1. frozen c and 2d' over each draft delta bracket, against the draft's output brackets ==")
for name, a, b, cbr, dbr in pts:
    ca = frozen_c(a)
    cb = frozen_c(b)
    inside = (cbr[0] <= ca[0]) and (cb[1] <= cbr[1])
    P(f"{name}: delta in [{fmt(a,8)},{fmt(b,8)}]  c in [{fmt(ca[0],8)}, {fmt(cb[1],8)}]  argmax n={ca[2]},{cb[2]}  draft [{fmt(cbr[0],5)},{fmt(cbr[1],5)}]  image_inside={inside}")
    if dbr:
        da, db = dprime(a), dprime(b)
        P(f"   2d' in [{fmt(2*da[0],8)}, {fmt(2*db[1],8)}] draft [{fmt(dbr[0],5)},{fmt(dbr[1],5)}] image_inside={dbr[0] <= 2*da[0] and 2*db[1] <= dbr[1]}")

# C11 2d' image
a, b = F(10165, 10**5), F(10166, 10**5)
da, db = dprime(a), dprime(b)
P(f"C11 crude 1/64: 2d' in [{fmt(2*da[0],8)}, {fmt(2*db[1],8)}] draft [0.22505,0.22507] image_inside={F(22505,10**5) <= 2*da[0] and 2*db[1] <= F(22507,10**5)}")
# where the draft's upper ends are crossed
def frozen_hi(d):
    return frozen_c(d)[1]
x, y = leaves(frozen_hi, F(11044, 10**6), F(11045, 10**6), F(44505, 10**5), grid=F(1, 10**11))
P(f"C07: upper(c) <= 0.44505 for delta <= {fmt(x,11)}; the critic's delta_1 = 0.0110444507 -> c in [{fmt(frozen_c(F(110444507,10**10))[0],8)}, {fmt(frozen_c(F(110444507,10**10))[1],8)}]")
x, y = leaves(frozen_hi, F(26890, 10**6), F(26891, 10**6), F(5951, 10**4), grid=F(1, 10**11))
din = F(12, 2000) * 1  # times e^{6k}
dlo, dhi = rdown(F(12, 2000) * elo(6 * KAPPA)), rup(F(12, 2000) * ehi(6 * KAPPA))
P(f"C10b s=1/2000: upper(c) <= 0.5951 for delta <= {fmt(x,11)}; exact delta_in = 12 s e^(3/2) in [{fmt(dlo,11)},{fmt(dhi,11)}] -> c <= {fmt(frozen_c(dhi)[1],8)}")
dlo4, dhi4 = rdown(F(12, 4096) * elo(6 * KAPPA)), rup(F(12, 4096) * ehi(6 * KAPPA))
P(f"C10b s=1/4096: exact delta_in in [{fmt(dlo4,11)},{fmt(dhi4,11)}] -> c in [{fmt(frozen_c(dlo4)[0],8)},{fmt(frozen_c(dhi4)[1],8)}]")
x, y = leaves(lambda d: 2 * dprime(d)[1], F(10165, 10**5), F(10166, 10**5), F(22507, 10**5), grid=F(1, 10**11))
P(f"C11: upper(2d') <= 0.22507 for delta <= {fmt(x,11)}")

# ---------- 2. route A ----------
P("\n== 2. route A: c* closed form vs brute-force Q, thresholds ==")
for d in [F(1, 1000), F(11045, 10**6), F(26891, 10**6), F(5, 100), F(72094, 10**6), F(72095, 10**6), F(10, 100), F(10166, 10**5)]:
    lo, hi, arg, ts = cstar_A(d)
    Qb, qarg = Q_brute_A(d)
    edhi_ = ehi(d)
    P(f"d={fmt(d,6)}: c* in [{fmt(lo,10)},{fmt(hi,10)}] argf={arg}; brute e^d*Qmax_hi={fmt(rup(edhi_*Qb),10)} at (f,m)={qarg}; t2_hi={fmt(ts[1][1],8)} t3=[{fmt(ts[2][0],8)},{fmt(ts[2][1],8)}]")

a0, a1 = F(72094, 10**6), F(72095, 10**6)
P(f"route A: t3_hi(0.072094) = {fmt(cstar_A(a0)[3][2][1],10)} vs e^-1_lo {fmt(e1[0],10)}; t3_lo(0.072095) = {fmt(cstar_A(a1)[3][2][0],10)}")
P(f"route A c* at C12 head-free [0.072645,0.072646]: [{fmt(cstar_A(F(72645,10**6))[0],8)}, {fmt(cstar_A(F(72646,10**6))[1],8)}]")
P(f"route A c* at C11 crude [0.10165,0.10166]: [{fmt(cstar_A(F(10165,10**5))[0],8)}, {fmt(cstar_A(F(10166,10**5))[1],8)}]")
for d in [F(109530694, 10**9), F(109530695, 10**9)]:
    lo, hi, arg, _ = cstar_A(d)
    P(f"route A delta_crit*: c*({fmt(d,9)}) in [{fmt(lo,10)},{fmt(hi,10)}] argf={arg}")

# sharpened route A: the root at e_0 holds e_0, so m >= 1
P("-- route A with m >= 1 (the root holds the line link e_0): --")
for d in [F(72095, 10**6), F(8, 100), F(9, 100), F(10, 100)]:
    lo, hi, arg, ts = cstar_A(d, mmin=1)
    Qb, qarg = Q_brute_A(d, mmin=1)
    P(f"d={fmt(d,6)}: c*_(m>=1) in [{fmt(lo,10)},{fmt(hi,10)}]; brute e^d*Qmax_hi={fmt(rup(ehi(d)*Qb),10)} at {qarg}")
x, y = leaves(lambda d: cstar_A(d, mmin=1)[1], F(72094, 10**6), F(11, 100), e1[1], grid=F(1, 10**9))
P(f"route A with m>=1: c* = e^-1 (upper enclosure <= e^-1_hi) up to delta = {fmt(x,9)} (next grid point {fmt(y,9)})")
xx, yy = leaves(lambda d: cstar_A(d, mmin=1)[1], F(10, 100), F(111780, 10**6), F(1) - F(1, 10**12), grid=F(1, 10**9))
P(f"route A with m>=1: c* < 1 up to delta = {fmt(xx,9)} (2d' <= 1/4 ends at 0.111780108)")

# ---------- 3. route B ----------
P("\n== 3. route B: c_B, c_sharp, delta_eq, thresholds, delta_crit ==")
for name, a, b, _, _ in pts:
    A_, B_ = cB(a), cB(b)
    S_a, S_b = csharp_B(a), csharp_B(b)
    P(f"{name}: c_B in [{fmt(A_[0],8)},{fmt(B_[1],8)}]  c_sharp in [{fmt(S_a[0],8)},{fmt(S_b[1],8)}] argn={S_a[2]},{S_b[2]}")

def f8f9(d, k=KAPPA):
    d1, d2 = dprime(d)
    u1, u2 = k / 2 - 2 * d1, k / 2 - 2 * d2
    # f(8)-f(9) = e^{-8u}(1-e^{-u}) - e^{-4k}(1-e^{-k/2}); return (lo, hi)
    hi = ehi(-8 * u2) * (1 - elo(-u2)) - elo(-4 * k) * (1 - ehi(-k / 2))
    lo = elo(-8 * u1) * (1 - ehi(-u1)) - ehi(-4 * k) * (1 - elo(-k / 2))
    return lo, hi
for d in [F(70256343, 10**10), F(70256344, 10**10)]:
    lo, hi = f8f9(d)
    P(f"f(8)-f(9) at {fmt(d,10)}: [{lo.numerator/lo.denominator:.3e}, {hi.numerator/hi.denominator:.3e}]")
for d in [F(116995481, 10**10), F(116995482, 10**10)]:
    lo, hi, arg = csharp_B(d)
    P(f"c_sharp({fmt(d,10)}) in [{fmt(lo,12)},{fmt(hi,12)}] argn={arg}  (e^-1 = [{fmt(e1[0],12)},{fmt(e1[1],12)}])")
for d in [F(558087801, 10**10), F(558087802, 10**10)]:
    lo, hi = cB(d)
    P(f"c_B({fmt(d,10)}) in [{fmt(lo,12)},{fmt(hi,12)}]")
for d in [F(577661141, 10**10), F(577661142, 10**10)]:
    lo, hi, arg = csharp_B(d)
    P(f"c_sharp({fmt(d,10)}) in [{fmt(lo,12)},{fmt(hi,12)}] argn={arg}")
for d in [F(49617491, 10**9), F(49617492, 10**9)]:
    lo, hi, arg, N = frozen_c(d)
    P(f"frozen c({fmt(d,9)}) in [{fmt(lo,12)},{fmt(hi,12)}] argn={arg}")
# sharpened route B: s <= n - 1
x, y = leaves(lambda d: csharp_B(d, sm1=True)[1], F(116995481, 10**10), F(5, 100), e1[1], grid=F(1, 10**10))
P(f"route B with s<=n-1: c_sharp = e^-1 up to delta = {fmt(x,10)}")

# ---------- 4. c >= proved, on a grid of delta in (0, C_k edge) ----------
P("\n== 4. ordering checks on a grid: c*_A <= c_sharp? c_sharp <= c_B <= c; c*_A < c ==")
bad = []
for i in range(1, 59):
    d = F(i, 1000)
    c = frozen_c(d)
    A_ = cstar_A(d)
    Bc = cB(d)
    Bs = csharp_B(d)
    if not (A_[1] < c[0]): bad.append(("c*A<c", i))
    if not (Bs[1] <= Bc[1] + F(1, 10**30) and Bc[0] <= c[1]): bad.append(("B order", i))
    if not (Bc[1] <= c[1] + F(1, 10**30)): bad.append(("cB<=c", i))
P("violations:", bad if bad else "none", "(58 grid points, delta = i/1000)")

open("/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/attack/G1-channel-checks.out", "w").write("\n".join(out) + "\n")
