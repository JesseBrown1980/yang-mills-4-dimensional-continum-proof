#!/usr/bin/env python3
# Lane L1-sec3-part1: note Lemma 3.2 items 1-5 as exact integer / integer-pair rational checks.
# No float, no fractions module, no decimal, no true division: a rational is a reduced pair (num, den), den > 0.
from math import comb, factorial, gcd

def q(n, d=1):
    if d < 0: n, d = -n, -d
    g = gcd(n, d)
    return (n // g, d // g)
def qa(x, y): return q(x[0] * y[1] + y[0] * x[1], x[1] * y[1])
def qs(x, y): return q(x[0] * y[1] - y[0] * x[1], x[1] * y[1])
def qm(x, y): return q(x[0] * y[0], x[1] * y[1])
def qd(x, y): return q(x[0] * y[1], x[1] * y[0])
def qlt(x, y): return x[0] * y[1] < y[0] * x[1]
def qle(x, y): return x[0] * y[1] <= y[0] * x[1]
Z = (0, 1); ONE = (1, 1)

out = []
allok = True
def chk(name, ok, detail=""):
    global allok
    allok = allok and ok
    out.append("HAAR|%s|ok=%d%s" % (name, 1 if ok else 0, ("|" + detail) if detail else ""))

M = 60
# ---- item 1 / item 2: E[a^{2m}] three ways
# (i) Weyl density (2/pi) sin^2 phi, Wallis: int_0^pi cos^{2k} = pi C(2k,k)/4^k, sin^2 = 1 - cos^2
def mom_weyl(m):
    return qm((2, 1), qs(q(comb(2 * m, m), 4 ** m), q(comb(2 * m + 2, m + 1), 4 ** (m + 1))))
# (ii) uniform measure on S^3 subset R^4 (SU(2) = unit quaternions, a = x_0): prod_{i<m} (2i+1)/(4+2i)
def mom_s3(m):
    r = ONE
    for i in range(m):
        r = qm(r, q(2 * i + 1, 4 + 2 * i))
    return r
# (iii) the note's closed form 4^{-m}(2m)!/(m!(m+1)!)
def mom_note(m):
    return q(factorial(2 * m), 4 ** m * factorial(m) * factorial(m + 1))
ok = all(mom_weyl(m) == mom_s3(m) == mom_note(m) for m in range(0, M + 1))
cat = all(qm(mom_note(m), (4 ** m, 1)) == (comb(2 * m, m) // (m + 1), 1) for m in range(0, M + 1))
chk("item1_2_even_moments_weyl_eq_S3_eq_note_closed_form_m0..60", ok)
chk("item2_4^m_E[a^2m]_is_Catalan_m0..60", cat)
def mom(k):
    return Z if k % 2 else mom_note(k // 2)

# Chebyshev U_m (integer coefficient lists, low degree first)
def chebU(mmax):
    U = [[1], [0, 2]]
    for m in range(1, mmax):
        a = [0] + [2 * c for c in U[m]]
        b = U[m - 1] + [0] * (len(a) - len(U[m - 1]))
        U.append([x - y for x, y in zip(a, b)])
    return U
U = chebU(40)
def E_poly(p):
    r = Z
    for i, c in enumerate(p):
        if c:
            r = qa(r, qm((c, 1), mom(i)))
    return r
def pmul(p, r):
    o = [0] * (len(p) + len(r) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(r):
            o[i + j] += x * y
    return o
# item 1: characters chi_j = U_{2j}(cos phi) orthonormal under the density; |chi_j| <= 2j+1 is U_m(1) = m+1
ok = all(E_poly(pmul(U[m], U[k])) == (ONE if m == k else Z) for m in range(0, 21) for k in range(0, 21))
chk("item1_chebyshevU_orthonormal_under_weyl_moments_m,k<=20", ok)
chk("item1_U_m(1)=m+1", all(sum(U[m]) == m + 1 for m in range(0, 40)))

# ---- item 2: c_0 series coefficients
ok = all(qm(mom_note(m), q(1, factorial(2 * m))) == q(1, 4 ** m * factorial(m) * factorial(m + 1)) for m in range(0, 41))
chk("item2_c0_coefficients_(beta/2)^2m/(m!(m+1)!)", ok)

# ---- item 3: E[chi_{(n-1)/2} e^{beta a}] = (2n/beta) I_n(beta), coefficientwise
# Fourier coefficient (1/pi) int_0^pi cos^k phi cos(n phi) dphi, two independent routes:
def fourier_binom(k, n):
    if k < n or (k - n) % 2: return Z
    return q(comb(k, (k - n) // 2), 2 ** k)
def chebT(nmax):
    T = [[1], [0, 1]]
    for m in range(1, nmax):
        a = [0] + [2 * c for c in T[m]]
        b = T[m - 1] + [0] * (len(a) - len(T[m - 1]))
        T.append([x - y for x, y in zip(a, b)])
    return T
T = chebT(40)
def arcsine_mom(k):
    # (1/pi) int_0^pi cos^k phi dphi = C(k, k/2)/2^k for k even, 0 for k odd
    return Z if k % 2 else q(comb(k, k // 2), 2 ** k)
def fourier_cheb(k, n):
    r = Z
    for i, c in enumerate(T[n]):
        if c:
            r = qa(r, qm((c, 1), arcsine_mom(k + i)))
    return r
ok_f = all(fourier_binom(k, n) == fourier_cheb(k, n) for k in range(0, 41) for n in range(0, 16))
chk("item3_fourier_coefficient_two_routes_k<=40_n<=15", ok_f)
ok = True
for n in range(1, 16):
    for k in range(0, 40):
        lhs = qm(E_poly(pmul(U[n - 1], [0] * k + [1])), q(1, factorial(k)))
        # coefficient of beta^k in (2n/beta) I_n(beta) = 2n * [beta^{k+1}] I_n = 2n * fourier(k+1, n)/(k+1)!
        rhs = qm((2 * n, 1), qm(fourier_binom(k + 1, n), q(1, factorial(k + 1))))
        if lhs != rhs:
            ok = False
chk("item3_E[chi e^{beta a}]=(2n/beta)I_n_coefficientwise_n1..15_k<40", ok)
# n = 1: c_0 = 2 I_1 / beta, so t_1 = 1; vanishing below order n-1
ok = all(E_poly(pmul(U[n - 1], [0] * k + [1])) == Z for n in range(1, 16) for k in range(0, n - 1))
chk("item3_E[chi_{(n-1)/2} a^k]=0_for_k<n-1", ok)
# bound |n t_n| <= 2n beta^{n-1} e^beta/n!: coefficientwise for n t_n c_0 (nonneg series), and c_0 >= 1
ok = True
for n in range(1, 16):
    for j in range(0, 31):
        c_lhs = q(2 * n, 2 ** (2 * j + n) * factorial(j) * factorial(j + n))
        c_rhs = q(2 * n, factorial(n) * factorial(2 * j))
        if not qle(c_lhs, c_rhs):
            ok = False
chk("item3_coefficientwise_bound_ntn_c0<=2n_beta^{n-1}e^beta/n!", ok)

# ---- item 4: eps_6^6 = E K^6 = sum_k C(6,k)(-1)^{6-k} c_0(k beta)/c_0(beta)^k, as power series to beta^16
P = 17
def c0_series(scale):
    s = [Z] * P
    for m in range(0, (P + 1) // 2):
        if 2 * m < P:
            s[2 * m] = qm(q(scale ** (2 * m), 1), q(1, 4 ** m * factorial(m) * factorial(m + 1)))
    return s
def smul(a, b):
    o = [Z] * P
    for i in range(P):
        if a[i] == Z: continue
        for j in range(P - i):
            if b[j] != Z:
                o[i + j] = qa(o[i + j], qm(a[i], b[j]))
    return o
def sinv(a):
    o = [Z] * P
    o[0] = qd(ONE, a[0])
    for n in range(1, P):
        s = Z
        for i in range(1, n + 1):
            s = qa(s, qm(a[i], o[n - i]))
        o[n] = qd(qs(Z, s), a[0])
    return o
c0 = c0_series(1)
ic0 = sinv(c0)
rhs = [Z] * P
for k in range(0, 7):
    term = c0_series(k) if k > 0 else [ONE] + [Z] * (P - 1)
    pw = [ONE] + [Z] * (P - 1)
    for _ in range(k):
        pw = smul(pw, ic0)
    term = smul(term, pw)
    sgn = 1 if (6 - k) % 2 == 0 else -1
    rhs = [qa(r, qm((sgn * comb(6, k), 1), t)) for r, t in zip(rhs, term)]
# lhs: f(a, beta) = e^{beta a}/c_0 - 1 as series in beta with polynomial-in-a coefficients (lists of rationals)
def poly_add(p, r):
    n = max(len(p), len(r)); p = p + [Z] * (n - len(p)); r = r + [Z] * (n - len(r))
    return [qa(x, y) for x, y in zip(p, r)]
def poly_mul(p, r):
    o = [Z] * (len(p) + len(r) - 1)
    for i, x in enumerate(p):
        if x == Z: continue
        for j, y in enumerate(r):
            if y != Z:
                o[i + j] = qa(o[i + j], qm(x, y))
    return o
f = []
for n in range(P):
    # coefficient of beta^n: sum_{i+j=n} (a^i/i!) ic0[j], minus 1 at n = 0
    p = [Z]
    for i in range(n + 1):
        mono = [Z] * i + [q(1, factorial(i))]
        p = poly_add(p, poly_mul(mono, [ic0[n - i]]))
    if n == 0:
        p = poly_add(p, [q(-1, 1)])
    f.append(p)
def bmul(A, B):
    o = [[Z] for _ in range(P)]
    for i in range(P):
        for j in range(P - i):
            o[i + j] = poly_add(o[i + j], poly_mul(A[i], B[j]))
    return o
f6 = [[ONE]] + [[Z] for _ in range(P - 1)]
for _ in range(6):
    f6 = bmul(f6, f)
def E_qpoly(p):
    r = Z
    for i, c in enumerate(p):
        if c != Z:
            r = qa(r, qm(c, mom(i)))
    return r
lhs = [E_qpoly(p) for p in f6]
ok = lhs == rhs and all(x == Z for x in lhs[:6]) and lhs[6] == q(5, 64)
chk("item4_eps6^6_binomial_formula_eq_E[K^6]_series_to_beta^16", ok, "beta^6_coeff=%d/%d|beta^8_coeff=%d/%d" % (lhs[6] + lhs[8]))

# ---- item 5
# E|chi_1/2| = (8/pi) int_0^{pi/2} cos sin^2 = 8/(3 pi): int_0^{pi/2} cos sin^2 = [sin^3/3] = 1/3 (exact antiderivative)
# Machin identity (5+i)^4 (239-i) = 114244 (1+i) in Gaussian integers
def gm(x, y): return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])
g = (1, 0)
for _ in range(4): g = gm(g, (5, 1))
g = gm(g, (239, -1))
chk("item5_machin_gaussian_identity", g == (114244, 114244), "(5+i)^4(239-i)=%d+%di" % g)
# branch: 0 < 4 arctan(1/5) - arctan(1/239) < pi/2 since 0 < arctan(1/239) < arctan(1/5) < 1/5 and 4/5 < pi/2 (pi/2 > 3/2)
lo_a5 = qa(qs(qa(q(1, 5), q(1, 15625)), q(1, 375)), q(-1, 546875))   # 1/5 - 1/375 + 1/15625 - 1/546875
hi_a239 = q(1, 239)
pi_lo = qs(qm((16, 1), lo_a5), qm((4, 1), hi_a239))
chk("item5_pi_lower_equals_frozen_1231847548/392109375", pi_lo == (1231847548, 392109375), "%d/%d" % pi_lo)
# alternating-series terms: x^{2k+1}/(2k+1) at x = 1/5: 1/5, 1/375, 1/15625, 1/546875 (decreasing)
chk("item5_series_terms", [q(1, 5 ** (2 * k + 1) * (2 * k + 1)) for k in range(4)] == [q(1, 5), q(1, 375), q(1, 15625), q(1, 546875)])
chk("item5_pi_lower>333/106", qlt(q(333, 106), pi_lo))
chk("item5_8/(3pi)<848/999_iff_pi>333/106", q(8 * 999, 3 * 848) == q(333, 106))
chk("item5_848/999<8489/10000", qlt(q(848, 999), q(8489, 10000)))
# outward enclosure 8/(3pi) in [0.8488263, 0.8488264] (a remark after the proof): item 5's own lower bound
# pi >= 1231847548/392109375 = 3.1415916745... is too weak for the upper end 0.8488264, so the remark is checked
# with longer alternating Machin partial sums (lower: stop after a negative term; upper: stop after a positive term)
def atan_partial(x, K):
    s = Z
    for k in range(K + 1):
        s = qa(s, qm(q((-1) ** k, 2 * k + 1), (x[0] ** (2 * k + 1), x[1] ** (2 * k + 1))))
    return s
pi_lo_long = qs(qm((16, 1), atan_partial((1, 5), 13)), qm((4, 1), atan_partial((1, 239), 4)))
pi_hi_long = qs(qm((16, 1), atan_partial((1, 5), 12)), qm((4, 1), atan_partial((1, 239), 5)))
ok_br = qlt(pi_lo_long, pi_hi_long) and qle(pi_lo, pi_lo_long)
# 8/(3 pi) >= 0.8488263  <=>  pi <= 8*10^7/(3*8488263)
e_lo_ok = qle(pi_hi_long, q(8 * 10 ** 7, 3 * 8488263))
# 8/(3 pi) <= 0.8488264  <=>  pi >= 8*10^7/(3*8488264)
e_hi_ok = qle(q(8 * 10 ** 7, 3 * 8488264), pi_lo_long)
chk("item5_remark_enclosure_8/(3pi)_in_[0.8488263,0.8488264]_with_long_machin", ok_br and e_lo_ok and e_hi_ok)
chk("item5_remark_item5_lower_bound_alone_does_not_give_upper_end_0.8488264", not qle(q(8 * 10 ** 7, 3 * 8488264), pi_lo),
    "pi_lo_item5=%d/%d" % pi_lo)
# route B's [0.8488264, 0.8488266] misses the true value: 8/(3pi) < 0.8488264
chk("item5_remark_routeB_display_misses", qlt(q(8 * 10 ** 7, 3 * 8488264), pi_lo_long))

# ---- note for check T4 (Lemma 4.22 uses item 5): (16/(3pi)) e^{-1} against 0.62454, 0.6245481, 0.62459
def einv_partial(K):
    s = Z
    for k in range(K + 1):
        s = qa(s, q((-1) ** k, factorial(k)))
    return s
einv_hi = einv_partial(24)  # even K: upper bound
einv_lo = einv_partial(25)  # odd K: lower bound
b_machin = qm(qd((16, 1), qm((3, 1), pi_lo)), einv_hi)
b_333 = qm(qd((16, 1), qm((3, 1), q(333, 106))), einv_hi)
b_333_lo = qm(qd((16, 1), qm((3, 1), q(333, 106))), einv_lo)
b_8489 = qm(qm((2, 1), q(8489, 10000)), einv_hi)
b_8489_lo = qm(qm((2, 1), q(8489, 10000)), einv_lo)
t4 = [
    ("T4note_machin_bound_gives_<0.62454", qlt(b_machin, q(62454, 100000))),
    ("T4note_pi>333/106_gives_<0.6245481", qlt(b_333, q(6245481, 10000000))),
    ("T4note_pi>333/106_does_not_give_0.62454", qle(q(62454, 100000), b_333_lo)),
    ("T4note_8489/10000_gives_<0.62459", qlt(b_8489, q(62459, 100000))),
    ("T4note_8489/10000_does_not_give_0.62454", qle(q(62454, 100000), b_8489_lo)),
]
for name, okk in t4:
    chk(name, okk)
for line in out:
    print(line)
print("HAAR_SUMMARY|all_ok=%d|tag=MEASURED|json=0" % int(allok))
