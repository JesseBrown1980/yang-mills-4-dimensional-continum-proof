# G1 repair scratch checks. Integers and Fractions only, outward dyadic rounding.
# Not an engine and not evidence. Floats appear only in display (fmt).
# The final G1 constant c_1 (roots hold a line link, m >= 1), the KP edge 2 delta' <= kappa,
# reproduction of the frozen c, the row points, the beta edges, the slice-bound slacks, the F1 instance.
import sys
from fractions import Fraction as Q
from math import comb

B = 256


def up(x, b=B):
    x = Q(x)
    if x == 0:
        return x
    n, d = x.numerator, x.denominator
    s = max(0, b - (abs(n).bit_length() - d.bit_length()))
    return Q(-((-n << s) // d), 1 << s)


def down(x, b=B):
    x = Q(x)
    if x == 0:
        return x
    n, d = x.numerator, x.denominator
    s = max(0, b - (abs(n).bit_length() - d.bit_length()))
    return Q((n << s) // d, 1 << s)


def fmt(x, k=12):
    return format(x.numerator / x.denominator, '.%dg' % k)


_EXP = {}


def ex(y, M=50):
    """[lo, hi] with lo <= e^y <= hi for rational y."""
    y = Q(y)
    if y in _EXP:
        return _EXP[y]
    if y < 0:
        lo, hi = ex(-y, M)
        r = (down(1 / hi), up(1 / lo))
    elif y > Q(1, 4):
        lo, hi = ex(y / 2, M)
        r = (down(lo * lo), up(hi * hi))
    else:
        s, t = Q(0), Q(1)
        for m in range(M + 1):
            s += t
            t = t * y / (m + 1)
        r = (down(s), up(s + t / (1 - y / (M + 2))))
    _EXP[y] = r
    return r


K = Q(1, 4)
EM1 = ex(-1)
out = []


def P(*a):
    line = ' '.join(str(t) for t in a)
    out.append(line)
    print(line, flush=True)


def dprime(d):
    lo, hi = ex(d)
    return down(d * lo), up(d * hi)


# ---------- the final constant c_1 and the frozen c ----------
def g_sup(rate_lo, rate_hi, kap, fmin=4):
    """sup over integers f >= fmin of e^{-r f} - e^{-kap f}; returns (lower at r=rate_hi..., upper, argmax).
    Upper uses the smaller rate (rate_lo), lower the larger rate (rate_hi). Tail cut certified."""
    best_hi, arg, f = Q(0), None, fmin
    vals_lo = {}
    while True:
        tail = ex(-rate_lo * f)[1]
        if tail <= best_hi:
            break
        ghi = up(ex(-rate_lo * f)[1] - ex(-kap * f)[0])
        glo = down(ex(-rate_hi * f)[0] - ex(-kap * f)[1])
        vals_lo[f] = glo
        if ghi > best_hi:
            best_hi, arg = ghi, f
        f += 1
    best_lo = max(vals_lo.values())
    return best_lo, best_hi, arg, f


def c1(dlo, dhi=None):
    """[lo, hi] for c_1 over [dlo, dhi]; c_1 = max{e^{-4k}, e^{d+2d'-5k}, e^{d-k/2} sup_{f>=4} g(f)}, g(f)=e^{-(k-2d')f}-e^{-kf}.
    Needs 2 d'^+ < kappa at dhi. Monotone in d, so the ends suffice."""
    if dhi is None:
        dhi = dlo
    p_lo, p_hi = dprime(dlo)[0], dprime(dhi)[1]
    assert 2 * p_hi < K
    e1 = ex(-4 * K)
    e2 = (ex(dlo + 2 * p_lo - 5 * K)[0], ex(dhi + 2 * p_hi - 5 * K)[1])
    glo, ghi, arg, fstop = g_sup(K - 2 * p_hi, K - 2 * p_lo, K)
    e3 = (down(ex(dlo - K / 2)[0] * glo), up(ex(dhi - K / 2)[1] * ghi))
    lo = max(e1[0], e2[0], e3[0])
    hi = max(e1[1], e2[1], e3[1])
    return lo, hi, {'e2': e2, 'e3': e3, 'argf': arg, 'fstop': fstop, 'off_hi': max(e2[1], e3[1])}


def c_frozen(dlo, dhi=None):
    """[lo, hi] for the frozen c = e^d [e^{-4k} + max_{n>=4} (e^{-(k/2-2d')n} - e^{-kn/2})]; needs 2d'^+ < k/2."""
    if dhi is None:
        dhi = dlo
    p_lo, p_hi = dprime(dlo)[0], dprime(dhi)[1]
    assert 2 * p_hi < K / 2
    glo, ghi, arg, _ = g_sup(K / 2 - 2 * p_hi, K / 2 - 2 * p_lo, K / 2)
    lo = down(ex(dlo)[0] * (EM1[0] + glo))
    hi = up(ex(dhi)[1] * (EM1[1] + ghi))
    return lo, hi, arg


def cstarA(dlo, dhi=None):
    """route A's c* (roots with m >= 0): max{e^{-4k}, e^{d+2d'-5k}, e^d sup_{f>=4} g(f)}."""
    if dhi is None:
        dhi = dlo
    p_lo, p_hi = dprime(dlo)[0], dprime(dhi)[1]
    assert 2 * p_hi < K
    e2 = (ex(dlo + 2 * p_lo - 5 * K)[0], ex(dhi + 2 * p_hi - 5 * K)[1])
    glo, ghi, arg, _ = g_sup(K - 2 * p_hi, K - 2 * p_lo, K)
    e3 = (down(ex(dlo)[0] * glo), up(ex(dhi)[1] * ghi))
    return max(EM1[0], e2[0], e3[0]), max(EM1[1], e2[1], e3[1])


P('e^{-1} in [%s, %s]' % (fmt(EM1[0], 13), fmt(EM1[1], 13)))

# ---------- 1. the two scalar edges on the 1e-9 grid ----------
def edge_grid(test, lo, hi, scale=10 ** 9):
    lo, hi = int(lo * scale), int(hi * scale)
    assert test(Q(lo, scale)) and not test(Q(hi, scale))
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if test(Q(mid, scale)):
            lo = mid
        else:
            hi = mid
    return Q(lo, scale), Q(hi, scale)


kp_ok = lambda d: 2 * dprime(d)[1] <= K          # certified 2 d' <= kappa
kp_bad = lambda d: 2 * dprime(d)[0] > K          # certified 2 d' > kappa
a, b = edge_grid(kp_ok, Q(1, 10), Q(12, 100))
P('1 KP edge: 2d\'<=1/4 certified at', fmt(a, 12), '; 2d\'>1/4 certified at', fmt(b, 12), ':', kp_bad(b))
DKP_LO, DKP_HI = a, b
a2, b2 = edge_grid(lambda d: 2 * dprime(d)[1] <= K / 2, Q(5, 100), Q(6, 100))
P('1 frozen C_k edge: 2d\'<=1/8 certified at', fmt(a2, 12), '; 2d\'>1/8 certified at', fmt(b2, 12), ':',
  2 * dprime(b2)[0] > K / 2)

# c_1 < 1 on the whole KP domain: e^{d-k/2} at the KP edge (analytic bound c_1 <= max{e^{-4k}, e^{d-k/2}})
P('1 analytic bound at the KP edge: e^{d-1/8} at d=%s is <= %s < 1' % (fmt(DKP_HI, 12), fmt(ex(DKP_HI - K / 2)[1], 10)))
for d in [Q(1117801, 10 ** 7), Q(11178, 10 ** 5), Q(111, 1000), Q(11, 100)]:
    lo, hi, info = c1(d)
    P('1 c_1(%s) in [%s, %s], argmax f = %s' % (fmt(d, 10), fmt(lo, 10), fmt(hi, 10), info['argf']))

# ---------- 2. where c_1 leaves e^{-1} ----------
def c1_is_em1(d):
    return c1(d)[2]['off_hi'] <= EM1[0]


lo_e, hi_e = edge_grid(c1_is_em1, Q(7, 100), Q(8, 100))
_, _, inf_hi = c1(hi_e)
P('2 c_1 = e^{-1}: object channel upper <= e^{-1} lower at', fmt(lo_e, 12), '(upper', fmt(c1(lo_e)[2]['off_hi'], 10),
  '); at', fmt(hi_e, 12), 'object channel lower', fmt(max(inf_hi['e2'][0], inf_hi['e3'][0]), 10), '> e^{-1} upper:',
  max(inf_hi['e2'][0], inf_hi['e3'][0]) > EM1[1], 'argmax f =', inf_hi['argf'])
P('2 second entry e^{d+2d\'-5/4} at', fmt(lo_e, 12), 'is <=', fmt(c1(lo_e)[2]['e2'][1], 10))
for d in [Q(72094, 10 ** 6), Q(72095, 10 ** 6)]:
    P('2 route A c* (m>=0) at %s in [%s, %s]; c_1 upper %s' % (fmt(d, 8), fmt(cstarA(d)[0], 10), fmt(cstarA(d)[1], 10),
                                                              fmt(c1(d)[1], 10)))

# ---------- 3. the row points: frozen c reproduced, final c_1 ----------
pts = [
    ('C07 crude 1/100 bracket', Q(11044, 10 ** 6), Q(11045, 10 ** 6)),
    ('C07 point 0.0110444507', Q(110444507, 10 ** 10), Q(110444507, 10 ** 10)),
    ('C08 refined 1/100', Q(942, 10 ** 8), Q(945, 10 ** 8)),
    ('C10b s=1/2000', Q(26890, 10 ** 6), Q(26891, 10 ** 6)),
    ('C10b s=1/4096', Q(13129, 10 ** 6), Q(13131, 10 ** 6)),
    ('C10c s=1/8192', Q(356909, 10 ** 7), Q(356910, 10 ** 7)),
    ('C10c s=1/65536', Q(44613, 10 ** 7), Q(44614, 10 ** 7)),
    ('C13 49/1000', Q(49, 1000), Q(49, 1000)),
    ('C13 1/20', Q(1, 20), Q(1, 20)),
    ('C13 delta_1 at 0.01369 (upper)', Q(49603, 10 ** 6), Q(49603, 10 ** 6)),
    ('C14 delta_1 at 0.01959 (upper)', Q(49383, 10 ** 6), Q(49383, 10 ** 6)),
    ('C14 refined 1/64', Q(20347, 10 ** 7), Q(20348, 10 ** 7)),
    ('C12 head-free 1/50', Q(72645, 10 ** 6), Q(72646, 10 ** 6)),
    ('C12 refined 1/50', Q(72646, 10 ** 6), Q(72648, 10 ** 6)),
    ('C11 crude 1/64', Q(10165, 10 ** 5), Q(10166, 10 ** 5)),
]
for name, dlo, dhi in pts:
    p_lo, p_hi = dprime(dlo)[0], dprime(dhi)[1]
    s = '3 %s: 2d\' in [%s, %s]' % (name, fmt(2 * p_lo, 9), fmt(2 * p_hi, 9))
    if 2 * p_hi < K / 2:
        cf = c_frozen(dlo, dhi)
        s += '; frozen c in [%s, %s] (n=%s)' % (fmt(cf[0], 10), fmt(cf[1], 10), cf[2])
    else:
        s += '; frozen C_k NOT_MET (2d\' > 1/8: %s)' % (2 * p_lo > K / 2)
    lo, hi, info = c1(dlo, dhi)
    s += '; c_1 in [%s, %s]%s' % (fmt(lo, 10), fmt(hi, 10), ' = e^{-1}' if info['off_hi'] <= EM1[0] else ' (argmax f=%s)' % info['argf'])
    P(s)

# ---------- 4. chains with c_1 ----------
def chain(name, d1hi):
    lo, hi, info = c1(d1hi)
    d2 = up(hi * d1hi)
    sm = up(d1hi / (1 - hi))
    P('4 %s: c_1(delta_1) <= %s; delta_2 <= %s; sum_k delta_k <= %s' % (name, fmt(hi, 10), fmt(d2, 8), fmt(sm, 8)))
    return hi


h = chain('C07 crude 1/100', Q(11045, 10 ** 6))
chain('C08 refined 1/100', Q(945, 10 ** 8))
chain('C14 refined 1/64', Q(20348, 10 ** 7))
chain('C11 crude 1/64', Q(10166, 10 ** 5))
chain('C12 refined 1/50', Q(72648, 10 ** 6))
d20 = up(h ** 19 * Q(11045, 10 ** 6))
osc = up(512 * EM1[1] * d20)
P('4 C16: delta_20 <= c_1^19 delta_1 <=', fmt(d20, 8), '; osc_V log rho_20 <= (512/e) delta_20 <=', fmt(osc, 8))
cf = c_frozen(Q(11045, 10 ** 6))
d20f = up(cf[1] ** 19 * Q(11045, 10 ** 6))
P('4 C16 frozen reproduction: delta_20 <=', fmt(d20f, 8), '; osc <=', fmt(up(512 * EM1[1] * d20f), 8))
P('4 C07 frozen reproduction: delta_2 <=', fmt(up(cf[1] * Q(11045, 10 ** 6)), 8), '; sum <=',
  fmt(up(Q(11045, 10 ** 6) / (1 - cf[1])), 8))

# ---------- 5. C10, C10b, C10c against the slice bound and the per-root bound ----------
def c0(x, M=30):
    q = (x / 2) ** 2
    s, t = Q(0), Q(1)
    for m in range(M + 1):
        s += t
        t = t * q / ((m + 1) * (m + 2))
    return s, s + t / (1 - q / ((M + 2) * (M + 3)))


def log1p_enc(ylo, yhi):
    return ylo - ylo * ylo / 2, yhi


for s in [Q(1, 2000), Q(1, 4096)]:
    e6 = ex(6 * K)
    din = (down(12 * s * e6[0]), up(12 * s * e6[1]))
    c0lo, c0hi = c0(4 * s)
    lg = log1p_enc(c0lo - 1, c0hi - 1)
    e4 = ex(4 * K)
    dout = (down(3 * e4[0] * lg[0]), up(3 * e4[1] * lg[1]))
    c1lo, c1hi, info = c1(din[0], din[1])
    assert info['off_hi'] <= EM1[0]
    r_lo, r_hi = down(dout[0] / (EM1[1] * din[1])), up(dout[1] / (EM1[0] * din[0]))
    P('5 C10b s=%s: delta_in in [%s, %s]; slice bound = natural delta_out in [%s, %s]; c_1 = e^{-1}' % (
        s, fmt(din[0], 11), fmt(din[1], 11), fmt(dout[0], 8), fmt(dout[1], 8)))
    P('5   delta_out/(c_1 delta_in) in [%s, %s], slack in [%s, %s]' % (fmt(r_lo, 7), fmt(r_hi, 7), fmt(1 / r_hi, 7), fmt(1 / r_lo, 7)))
    # per-root bound: roots are rectangles with (f, m) = (2, 4): factor e^d e^{-k(6)} e^{2k}(e^{4d'}-1) = e^{d-4k}(e^{4d'}-1)
    p_lo, p_hi = dprime(din[0])[0], dprime(din[1])[1]
    pr_lo = down(ex(din[0] - 4 * K)[0] * (ex(4 * p_lo)[0] - 1))
    pr_hi = up(ex(din[1] - 4 * K)[1] * (ex(4 * p_hi)[1] - 1))
    P('5   per-root factor e^{d-4k}(e^{4d\'}-1) in [%s, %s]; per-root bound / natural delta_out in [%s, %s]' % (
        fmt(pr_lo, 8), fmt(pr_hi, 8), fmt(down(pr_lo * din[0] / dout[1]), 7), fmt(up(pr_hi * din[1] / dout[0]), 7)))
    if s == Q(1, 2000):
        pb = (Q(400, 10 ** 9), Q(401, 10 ** 9))
        P('5   frozen projection bound [4.00e-7, 4.01e-7] / (c_1 delta_in) in [%s, %s]; the frozen clause asks <= 3e-5' % (
            fmt(down(pb[0] / (EM1[1] * din[1])), 6), fmt(up(pb[1] / (EM1[0] * din[0])), 6)))

for s in [Q(1, 8192), Q(1, 65536)]:
    e10 = ex(10 * K)
    din = (down(24 * s * e10[0]), up(24 * s * e10[1]))
    e4 = ex(4 * K)
    dout = (down(6 * e4[0] * (s - 4 * s * s)), up(6 * e4[1] * (s + 4 * s * s)))
    c1lo, c1hi, info = c1(din[0], din[1])
    assert info['off_hi'] <= EM1[0]
    r_lo, r_hi = down(dout[0] / (EM1[1] * din[1])), up(dout[1] / (EM1[0] * din[0]))
    P('5 C10c s=%s: delta_in in [%s, %s]; slice bound = natural delta_out in [%s, %s]; c_1 = e^{-1}' % (
        s, fmt(din[0], 9), fmt(din[1], 9), fmt(dout[0], 8), fmt(dout[1], 8)))
    P('5   delta_out/(c_1 delta_in) in [%s, %s], slack in [%s, %s]' % (fmt(r_lo, 7), fmt(r_hi, 7), fmt(1 / r_hi, 7), fmt(1 / r_lo, 7)))
    # per-root bound: (f, m) = (2, 8): q = e^{-10k} e^{4k} [1 + e^{4d'} - 1] = e^{-6k+4d'}; times e^d
    p_lo, p_hi = dprime(din[0])[0], dprime(din[1])[1]
    pr_lo = ex(din[0] - 6 * K + 4 * p_lo)[0]
    pr_hi = ex(din[1] - 6 * K + 4 * p_hi)[1]
    P('5   per-root factor e^{d-6k+4d\'} in [%s, %s]; per-root bound / natural delta_out in [%s, %s]' % (
        fmt(pr_lo, 8), fmt(pr_hi, 8), fmt(down(pr_lo * din[0] / dout[1]), 7), fmt(up(pr_hi * din[1] / dout[0]), 7)))

# ---------- 6. the F1 instance under the final d = (k/2) #line(Gamma), a = d' #off(Gamma) ----------
d = Q(1, 100)
p_lo, p_hi = dprime(d)
R0 = Q(1, 10 ** 6)
RA = Q(36787, 10 ** 7) - Q(1, 10 ** 6)
w0 = (ex(R0)[0] - 1, ex(R0)[1] - 1)
wA = (ex(RA)[0] - 1, ex(RA)[1] - 1)
# off(p0) = 2, line(p0) = 2; off(pA) = off(pB) = 4, line = 0; pA, pB each share one off link with p0, none with each other
polys = [  # (omega upper, #off(union), #line(union))
    (w0[1], 2, 2), (wA[1], 4, 0), (wA[1], 4, 0),
    (w0[1] * wA[1], 5, 2), (w0[1] * wA[1], 5, 2), (w0[1] * wA[1] ** 2, 8, 2)]
lhs = sum(up(om * ex(p_hi * fo + K / 2 * ml)[1]) for om, fo, ml in polys)
P('6 F1 instance, final a and d: KP left side at {p_0} <=', fmt(lhs, 8), '; a({p_0}) = 2d\' >=', fmt(2 * p_lo, 8), ':', lhs <= 2 * p_lo)
norm_shared = up(ex(4 * K)[1] * (R0 + RA))
P('6 F1 instance: norm at a shared off link <=', fmt(norm_shared, 8), '<= 1/100:', norm_shared <= d)

# ---------- 8. the final form: lambda := d' + ln(1 + d') in place of 2d' (the (1+t)^f tree hypothesis) ----------
def ln1p(x, N=60):
    """[lo, hi] for ln(1+x), 0 < x < 1: alternating partial sums."""
    x = Q(x)
    s, t, lo, hi = Q(0), Q(1), None, None
    sums = []
    for j in range(1, N + 2):
        t = t * x
        s += (t if j % 2 else -t) / j
        sums.append(s)
    # sums[N-1] has N terms; even count -> lower, odd count -> upper
    a_, b_ = sums[-2], sums[-1]
    return down(min(a_, b_)), up(max(a_, b_))


def lam(d):
    p_lo, p_hi = dprime(d)
    return down(p_lo + ln1p(p_lo)[0]), up(p_hi + ln1p(p_hi)[1])


def cfin(dlo, dhi=None):
    """[lo, hi] for c_fin = max{e^{-4k}, e^{d+lam-5k}, e^{d-k/2} sup_{f>=4}(e^{-(k-lam)f}-e^{-kf})}, needs lam^+ < kappa."""
    if dhi is None:
        dhi = dlo
    l_lo, l_hi = lam(dlo)[0], lam(dhi)[1]
    assert l_hi < K
    e2 = (ex(dlo + l_lo - 5 * K)[0], ex(dhi + l_hi - 5 * K)[1])
    glo, ghi, arg, fstop = g_sup(K - l_hi, K - l_lo, K)
    e3 = (down(ex(dlo - K / 2)[0] * glo), up(ex(dhi - K / 2)[1] * ghi))
    return max(EM1[0], e2[0], e3[0]), max(EM1[1], e2[1], e3[1]), {'e2': e2, 'e3': e3, 'argf': arg, 'off_hi': max(e2[1], e3[1])}


la, lb = edge_grid(lambda d: lam(d)[1] <= K, Q(11, 100), Q(12, 100))
P("8 lambda edge: dp+ln(1+dp) <= 1/4 certified at", fmt(la, 12), '; > 1/4 certified at', fmt(lb, 12), ':', lam(lb)[0] > K)
DL_LO, DL_HI = la, lb
P("8 at the lambda edge: 2dp in [%s, %s] (> 1/4: %s); delta < 1/8: %s; e^{d-1/8} <= %s" % (
    fmt(2 * dprime(DL_LO)[0], 10), fmt(2 * dprime(DL_HI)[1], 10), 2 * dprime(DL_LO)[0] > K, DL_HI < K / 2,
    fmt(ex(DL_HI - K / 2)[1], 10)))
for d in [Q(1145, 10 ** 4), Q(114, 1000), Q(11178, 10 ** 5), Q(111, 1000), Q(11, 100)]:
    lo_, hi_, inf_ = cfin(d)
    P('8 c_fin(%s) in [%s, %s], argmax f = %s' % (fmt(d, 10), fmt(lo_, 10), fmt(hi_, 10), inf_['argf']))
lo_e, hi_e = edge_grid(lambda d: cfin(d)[2]['off_hi'] <= EM1[0], Q(7, 100), Q(8, 100))
inf_hi = cfin(hi_e)[2]
P('8 c_fin = e^{-1} through', fmt(lo_e, 12), '(object channel upper', fmt(cfin(lo_e)[2]['off_hi'], 10), '); at', fmt(hi_e, 12),
  'object channel lower', fmt(max(inf_hi['e2'][0], inf_hi['e3'][0]), 10), '> e^{-1}:', max(inf_hi['e2'][0], inf_hi['e3'][0]) > EM1[1],
  'argmax f =', inf_hi['argf'])
for name, dlo, dhi in pts:
    l_hi = lam(dhi)[1]
    lo_, hi_, inf_ = cfin(dlo, dhi)
    P('8 %s: lambda in [%s, %s]; c_fin in [%s, %s]%s' % (name, fmt(lam(dlo)[0], 9), fmt(l_hi, 9), fmt(lo_, 10), fmt(hi_, 10),
                                                         ' = e^{-1}' if inf_['off_hi'] <= EM1[0] else ' (argmax f=%s)' % inf_['argf']))
for name, d1 in [('C07', Q(11045, 10 ** 6)), ('C08', Q(945, 10 ** 8)), ('C14 1/64', Q(20348, 10 ** 7)),
                 ('C11', Q(10166, 10 ** 5)), ('C12 refined', Q(72648, 10 ** 6))]:
    hi_ = cfin(d1)[1]
    P('8 chain %s: c_fin <= %s; delta_2 <= %s; sum <= %s' % (name, fmt(hi_, 10), fmt(up(hi_ * d1), 8), fmt(up(d1 / (1 - hi_)), 8)))

# ---------- 9. closed form of Q_fin against a brute-force sup; per-root factors under lambda ----------
def q_enc(f, m, l_lo, l_hi):
    single = 1 if m >= 8 else 0
    sh = ex(-K * (m % 2) / 2)
    pre_lo, pre_hi = ex(-K * (f + m) + K * m / 2)
    lo = down(pre_lo * (single * sh[0] + ex(l_lo * f)[0] - 1))
    hi = up(pre_hi * (single * sh[1] + ex(l_hi * f)[1] - 1))
    return lo, hi


for d in [Q(1, 100), Q(5, 100), Q(7, 100), Q(8, 100), Q(10, 100), Q(11, 100)]:
    l_lo, l_hi = lam(d)
    best_lo, best_hi, arg = Q(0), Q(0), None
    for f in range(1, 61):
        for m in range(1, 41):
            if f + m < 4:
                continue
            a_, b_ = q_enc(f, m, l_lo, l_hi)
            if a_ > best_lo:
                best_lo, arg = a_, (f, m)
            best_hi = max(best_hi, b_)
    e2 = ex(l_hi - 5 * K)[1]
    glo, ghi, garg, _ = g_sup(K - l_hi, K - l_lo, K)
    closed_hi = max(e2, up(ex(-K / 2)[1] * ghi))
    closed_lo = max(ex(l_lo - 5 * K)[0], down(ex(-K / 2)[0] * glo))
    P('9 delta=%s: brute sup over 1<=f<=60, 1<=m<=40 in [%s, %s] at (f,m)=%s; closed form in [%s, %s]; enclosures overlap within 1e-50: %s' % (
        fmt(d, 4), fmt(best_lo, 10), fmt(best_hi, 10), arg, fmt(closed_lo, 10), fmt(closed_hi, 10),
        best_lo <= closed_hi and closed_lo <= best_hi and up(closed_hi - best_lo) < Q(1, 10 ** 50)))
for s_, f_, m_, lab in [(Q(1, 2000), 2, 4, 'C10b'), (Q(1, 4096), 2, 4, 'C10b'), (Q(1, 8192), 2, 8, 'C10c'), (Q(1, 65536), 2, 8, 'C10c')]:
    if lab == 'C10b':
        e6 = ex(6 * K)
        din = (down(12 * s_ * e6[0]), up(12 * s_ * e6[1]))
        c0lo, c0hi = c0(4 * s_)
        lg = log1p_enc(c0lo - 1, c0hi - 1)
        e4 = ex(4 * K)
        dout = (down(3 * e4[0] * lg[0]), up(3 * e4[1] * lg[1]))
    else:
        e10 = ex(10 * K)
        din = (down(24 * s_ * e10[0]), up(24 * s_ * e10[1]))
        e4 = ex(4 * K)
        dout = (down(6 * e4[0] * (s_ - 4 * s_ * s_)), up(6 * e4[1] * (s_ + 4 * s_ * s_)))
    l_lo, l_hi = lam(din[0])[0], lam(din[1])[1]
    qlo, qhi = q_enc(f_, m_, l_lo, l_hi)
    pr_lo, pr_hi = down(ex(din[0])[0] * qlo), up(ex(din[1])[1] * qhi)
    P('9 %s s=%s: per-root factor e^d q(%d,%d) under lambda in [%s, %s]; per-root bound / natural delta_out in [%s, %s]' % (
        lab, s_, f_, m_, fmt(pr_lo, 8), fmt(pr_hi, 8), fmt(down(pr_lo * din[0] / dout[1]), 7), fmt(up(pr_hi * din[1] / dout[0]), 7)))

# ---------- 7. beta edges: C_0 at theta = 1/4 with delta_1 = factor*alpha, against a threshold ----------
F = lambda n: comb(20 * n, n) // (19 * n + 1)
MU = Q(20 ** 20, 19 ** 19)
HEADS = {
    'crude': {n: 6 * F(n) for n in range(4, 11)},
    'C03': dict(zip(range(4, 11), [1, 0, 12, 0, 32, 32, 304])),
    'headfree': {n: 0 for n in range(4, 11)},
}
COEF = {h: [0] * 4 + [(HEADS[h][n] if n <= 10 else 6 * F(n)) for n in range(4, 49)] for h in HEADS}
F49 = 6 * F(49)


def S_and_dS(x, h):
    """S(x) and S'(x) exactly; None if mu x >= 1."""
    if MU * x >= 1:
        return None
    c = COEF[h]
    s, ds = Q(0), Q(0)
    p = x ** 3
    for n in range(4, 49):
        ds += n * c[n] * p
        p *= x
        s += c[n] * p
    # p = x^48 now
    den = 1 - MU * x
    s += F49 * p * x / den
    ds += F49 * (49 * p / den + MU * p * x / den ** 2)
    return s, ds


def c0e(x, M=40):
    q = (x / 2) ** 2
    s, t = Q(0), Q(1)
    for m in range(M + 1):
        s += t
        t = t * q / ((m + 1) * (m + 2))
    return s, s + t / (1 - q / ((M + 2) * (M + 3)))


def iroot(n, k):
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + n // x ** (k - 1)) // k
        if y >= x:
            break
        x = y
    while x ** k > n:
        x -= 1
    while (x + 1) ** k <= n:
        x += 1
    return x


_EPS = {}


def eps6(beta, bits=160):
    if beta in _EPS:
        return _EPS[beta]
    c1l, c1h = c0e(beta)
    lo = hi = Q(0)
    for k in range(7):
        ckl, ckh = c0e(k * beta)
        rl, rh = ckl / c1h ** k, ckh / c1l ** k
        sg = (-1) ** (6 - k) * comb(6, k)
        if sg > 0:
            lo += sg * rl
            hi += sg * rh
        else:
            lo += sg * rh
            hi += sg * rl
    lo, hi = down(lo), up(hi)
    n_lo = (lo.numerator << (6 * bits)) // lo.denominator
    n_hi = -((-hi.numerator << (6 * bits)) // hi.denominator)
    zl, zh = iroot(n_lo, 6), iroot(n_hi, 6)
    if zh ** 6 < n_hi:
        zh += 1
    r = (Q(zl, 1 << bits), Q(zh, 1 << bits))
    _EPS[beta] = r
    return r


def read(beta, h, factor, thr_met, thr_not):
    """MET: alpha_c = thr_met/factor certifies S^+(x^+) <= alpha_c. NOT_MET: at alpha_c = thr_not/factor,
    g^- > 0 and g'^+ < 0 (so the least root exceeds alpha_c), or S has no value (pole)."""
    el, eh = eps6(beta)
    th = Q(1, 4)
    am = thr_met / factor
    xh = up(eh * ex(2 * am + th)[1])
    r = S_and_dS(xh, h)
    met = r is not None and up(r[0]) <= am
    an = thr_not / factor
    xl = down(el * ex(2 * an + th)[0])
    xh2 = up(eh * ex(2 * an + th)[1])
    rl, rh = S_and_dS(xl, h), S_and_dS(xh2, h)
    if rl is None:
        notmet = True
    else:
        notmet = rl[0] > an and rh is not None and 2 * xh2 * rh[1] - 1 < 0
    return met, notmet


def find_edge(h, factor, thr_met, thr_not, start, step=1):
    """walk the 1e-5 grid from start (an index) to an adjacent MET / NOT_MET pair, each certified."""
    i = start
    m, n = read(Q(i, 10 ** 5), h, factor, thr_met, thr_not)
    if m:
        while True:
            m2, n2 = read(Q(i + 1, 10 ** 5), h, factor, thr_met, thr_not)
            if not m2:
                return i, (m, n), (m2, n2)
            i += 1
    else:
        while True:
            m2, n2 = read(Q(i - 1, 10 ** 5), h, factor, thr_met, thr_not)
            if m2:
                return i - 1, (m2, n2), (m, n)
            i -= 1


def c0_stop(h, start):
    """C_0 edge: MET read at alpha_c chosen as 1/4-safe search is not needed; reuse read with thr = factor*1/4."""
    return find_edge(h, 1, Q(1, 4), Q(1, 4), start)


DCF = (Q(496174, 10 ** 7), Q(496175, 10 ** 7))          # frozen delta_crit bracket (C13)
DCA = (Q(109530694, 10 ** 9), Q(109530695, 10 ** 9))    # route A delta_crit*
DC1 = (DKP_LO, DKP_HI)                                   # final: the KP edge
jobs = [
    ('frozen c, factor 12', 12, DCF, {'crude': 1369, 'C03': 1959, 'headfree': 1959}),
    ('route A c*, factor 12', 12, DCA, {'crude': 1582, 'C03': 2037, 'headfree': 2037}),
    ('c_1 (2d\' <= k), factor 12', 12, DC1, {'crude': 1586, 'C03': 2038, 'headfree': 2038}),
    ('c_1 (2d\' <= k), factor 6', 6, DC1, {'crude': 1760, 'C03': 2074, 'headfree': 2074}),
    ('final c_fin (lambda <= k), factor 12', 12, (DL_LO, DL_HI), {'crude': 1590, 'C03': 2039, 'headfree': 2039}),
    ('final c_fin (lambda <= k), factor 6', 6, (DL_LO, DL_HI), {'crude': 1765, 'C03': 2074, 'headfree': 2074}),
]
for label, fac, thr, starts in jobs:
    for h in ['crude', 'C03', 'headfree']:
        i, a_, b_ = find_edge(h, fac, thr[0], thr[1], starts[h])
        P('7 %s, %s: MET at %s (certified %s), NOT_MET at %s (certified %s)' % (
            label, h, fmt(Q(i, 10 ** 5), 6), a_[0], fmt(Q(i + 1, 10 ** 5), 6), b_[1]))

if len(sys.argv) > 1:
    # the C_0 stops themselves (any alpha <= 1/4); an alpha_c-only read is not a C_0 read, so this is display only
    pass

with open(__file__.replace('.py', '.out'), 'w') as f:
    f.write('\n'.join(out) + '\n')
