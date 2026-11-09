# n1_constants.py -- L5-numbers lane: mu, F_20, pi bounds, e_chi, the beta_k bound,
# delta_crit and its fallback, c_fin (own scan with a certified tail cut), the flat range,
# c_fin at delta_crit^-, and C10c. Integer only; imports only ilib (own code).
import sys
sys.path.insert(0, '/mnt/c/tmp/opus55/ym4-04c-gattack/work/L5-numbers')
import ilib as L
from ilib import rat, add, sub, mul, div, muli, divi, neg, exp_iv, exp_point, ln1p_iv, imax, fmti, inside, dec, ge_rat, le_rat, lt_rat, gt_rat, scii

FAILS = []


def row(name, ok, **kv):
    s = 'NUM|id=' + name + '|' + '|'.join(k + '=' + str(v) for k, v in kv.items()) + '|ok=' + ('1' if ok else '0') + '|json=0'
    print(s)
    if not ok:
        FAILS.append(name)


def comb(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r


# ------------------------------------------------------------------ mu and F_20
MU_N, MU_D = 20 ** 20, 19 ** 19
ok_mu = (5300068 * MU_D <= 100000 * MU_N) and (100000 * MU_N <= 5300069 * MU_D)
ok_mu_strict = (5300068 * MU_D < 100000 * MU_N) and (100000 * MU_N < 5300069 * MU_D)
row('mu_bracket', ok_mu and ok_mu_strict, mu='20^20/19^19', enclosure=fmti(rat(MU_N, MU_D), 12), claim='[53.00068,53.00069]')


def F(n):
    num = comb(20 * n, n)
    assert num % (19 * n + 1) == 0
    v = num // (19 * n + 1)
    if n >= 1:
        assert comb(20 * n, n - 1) % n == 0 and comb(20 * n, n - 1) // n == v
    return v


FROZEN_F = [20540, 784245, 31763004, 1340246340, 58281448940, 2593593086150, 117544525178080, 5406686759963586, 251754316822792420]
mine = [F(n) for n in range(4, 13)]
row('F20_4_12', mine == FROZEN_F, values=','.join(str(v) for v in mine))
row('6F20_1_5', [6 * F(n) for n in range(1, 6)] == [6, 120, 3540, 123240, 4705470], values=','.join(str(6 * F(n)) for n in range(1, 6)))
row('F20_2_vs_F19_2', F(2) == 20 and comb(38, 2) // 37 == 19, F20_2=F(2), F19_2=comb(38, 2) // 37)
# ratio strictly increasing and strictly below mu, n = 0..400 (exact cross-multiplication)
okr = True
prev = None
for n in range(0, 401):
    a, b = F(n + 1), F(n)          # ratio a/b
    if not (a * MU_D < MU_N * b):
        okr = False
    # product formula 20*prod_{j=1}^{19}(20n+j)/(19n+j+1)
    pn, pd = 20, 1
    for j in range(1, 20):
        pn *= (20 * n + j)
        pd *= (19 * n + j + 1)
    if a * pd != b * pn:
        okr = False
    if prev is not None and not (prev[0] * b < a * prev[1]):
        okr = False
    prev = (a, b)
row('F20_ratio_increasing_below_mu_n0_400', okr)
# F(n+2)/F(n) > 2000 only from n = 8
r2 = [(n, F(n + 2) * 100 // F(n)) for n in range(4, 11)]
row('F20_two_step_ratio', all((F(n + 2) > 2000 * F(n)) == (n >= 8) for n in range(4, 11)), hundredths=';'.join(str(n) + ':' + str(v) for n, v in r2))

# ------------------------------------------------------------------ pi, Machin, e_chi
re_, im_ = 5, 1
z = (1, 0)
for _ in range(4):
    z = (z[0] * re_ - z[1] * im_, z[0] * im_ + z[1] * re_)
z = (z[0] * 239 + z[1] * 1, z[1] * 239 - z[0] * 1)
row('machin_identity', z == (114244, 114244), product=str(z))
# the lower bound 16(1/5-1/375+1/15625-1/546875)-4/239 as an exact integer pair
num = 16 * (328125 - 4375 + 105 - 3) * 239 - 4 * 1640625
den = 1640625 * 239
row('machin_lower_bound_exact', num == 1231847548 and den == 392109375, num=num, den=den)
PI = L.pi_iv()
row('pi_enclosure', ge_rat(PI[0], (1231847548, 392109375)), pi=fmti(PI, 25), piL_le_pi=1)
row('piL_gt_333_106_gt_80000_25467', 1231847548 * 106 > 333 * 392109375 and 333 * 25467 > 80000 * 106)
ECHI = div(L.const(8), muli(PI, 3))
row('e_chi_enclosure', inside(ECHI, '0.8488263', '0.8488264'), e_chi=fmti(ECHI, 13))
row('e_chi_lt_848_999_lt_8489_10000', 848 * 10000 < 8489 * 999 and 8 * 106 * 999 == 848 * 3 * 333,
    note='8/(3pi)<8*106/(3*333)=848/999_from_pi>333/106')
EM1 = exp_point(-L.ONE)
row('e_minus_1', inside(EM1, '0.3678794411714', '0.3678794411715'), e_m1=fmti(EM1, 16))
# beta_k: (16/(3pi)) e^-1
BK = mul(div(L.const(16), muli(PI, 3)), EM1)
row('betak_true_factor', lt_rat(BK[1], dec('0.62454')), value=fmti(BK, 12))
BK_L = mul(rat(16 * 392109375, 3 * 1231847548), EM1)
row('betak_with_piL', le_rat(BK_L[1], dec('0.6245318')) and lt_rat(BK_L[1], dec('0.62454')), bound=fmti(BK_L, 12))
BK_333 = mul(rat(1696, 999), EM1)
row('betak_with_333_106', lt_rat(BK_333[1], dec('0.6245481')) and gt_rat(BK_333[0], dec('0.62454')), bound=fmti(BK_333, 12),
    reads='below_0.6245481_and_above_0.62454')
BK_8489 = mul(rat(2 * 8489, 10000), EM1)
row('betak_with_8489', lt_rat(BK_8489[1], dec('0.62459')) and gt_rat(BK_8489[0], dec('0.62454')), bound=fmti(BK_8489, 12),
    reads='below_0.62459_and_above_0.62454')

# ------------------------------------------------------------------ G1: lambda, delta_crit
K4 = rat(1, 4)


def lam_iv(d):
    dp = mul(d, exp_iv(d))
    return dp, add(dp, ln1p_iv(dp))


def lam_rat(p, q):
    return lam_iv(rat(p, q))


dp_a, lm_a = lam_rat(114846768, 10 ** 9)
dp_b, lm_b = lam_rat(114846769, 10 ** 9)
row('delta_crit_bracket', le_rat(lm_a[1], (1, 4)) and gt_rat(lm_b[0], (1, 4)),
    lambda_at_0_114846768=fmti(lm_a, 14), lambda_at_0_114846769=fmti(lm_b, 14))
# bisection for delta_crit itself
lo, hi = (114846768, 10 ** 9), (114846769, 10 ** 9)
# work on a dyadic grid: delta = m / 2^80
SH = 80
mlo = (114846768 << SH) // 10 ** 9
mhi = L.cdiv(114846769 << SH, 10 ** 9)
for _ in range(60):
    mm = (mlo + mhi) // 2
    _, lmm = lam_rat(mm, 1 << SH)
    if le_rat(lmm[1], (1, 4)):
        mlo = mm
    elif gt_rat(lmm[0], (1, 4)):
        mhi = mm
    else:
        break
DCRIT = (rat(mlo, 1 << SH)[0], rat(mhi, 1 << SH)[1])
row('delta_crit_tight', True, delta_crit=fmti(DCRIT, 20))
# 2 delta' at the edge
row('two_dprime_at_edge', inside(muli(dp_a, 2), '0.2576475939', '0.2576475964') and inside(muli(dp_b, 2), '0.2576475939', '0.2576475964'),
    two_dprime=fmti(muli(dp_a, 2), 12) + '..' + fmti(muli(dp_b, 2), 12))
# fallback 2 delta' <= kappa
fa, _ = lam_rat(111780108, 10 ** 9)
fb, _ = lam_rat(111780109, 10 ** 9)
row('delta_crit_fallback_bracket', le_rat(muli(fa, 2)[1], (1, 4)) and gt_rat(muli(fb, 2)[0], (1, 4)),
    two_dprime_at_0_111780108=fmti(muli(fa, 2), 14), two_dprime_at_0_111780109=fmti(muli(fb, 2), 14))
# frozen C_k edge 2 delta' <= kappa/2
ga, _ = lam_rat(58923670, 10 ** 9)
gb, _ = lam_rat(58923671, 10 ** 9)
row('frozen_Ck_edge', le_rat(muli(ga, 2)[1], (1, 8)) and gt_rat(muli(gb, 2)[0], (1, 8)))


# ------------------------------------------------------------------ c_fin
def cfin(d, fallback=False):
    """c_fin(delta) at kappa = 1/4 for an interval delta; returns (c, E2, E3, fmax, unique, fstop).
    fallback=True replaces lambda by 2 delta' (route A's bookkeeping with m >= 1)."""
    dp, lm = lam_iv(d)
    if fallback:
        lm = muli(dp, 2)
    E2 = exp_iv(sub(add(d, lm), rat(5, 4)))
    a = sub(K4, lm)
    assert a[0] > 0, 'lambda not below kappa'
    best_lo = -1
    best_hi = -1
    farg = None
    gs = {}
    f = 4
    while True:
        eu = exp_iv(muli(neg(a), f))
        ev = exp_point(-(f << (L.P - 2)))
        g = sub(eu, ev)
        gs[f] = g
        if g[0] > best_lo:
            best_lo = g[0]
            farg = f
        if g[1] > best_hi:
            best_hi = g[1]
        if eu[1] <= best_lo:
            break
        f += 1
    unique = all(gs[h][1] < gs[farg][0] for h in gs if h != farg)
    E3 = mul(exp_iv(sub(d, rat(1, 8))), (best_lo, best_hi))
    c = imax(imax((EM1[0], EM1[1]), E2), E3)
    return c, E2, E3, farg, unique, f


def is_e1(c, E2, E3):
    # c_fin = e^-1 exactly when both other entries are at most e^-1
    return E2[1] <= EM1[0] and E3[1] <= EM1[0]


for (p, q, lo_s, hi_s, fexp) in [(1, 10, '0.611173', '0.611174', 9), (11, 100, '0.811310', '0.811311', 13)]:
    c, E2, E3, fa_, un, fs = cfin(rat(p, q))
    row('cfin_' + str(p) + '_' + str(q), inside(c, lo_s, hi_s) and fa_ == fexp and un and E3[0] > EM1[1] and E3[0] > E2[1],
        cfin=fmti(c, 10), argmax_f=fa_, unique=int(un), E2=fmti(E2, 10), scan_stop_f=fs)
for (p, q) in [(49, 1000), (1, 20)]:
    c, E2, E3, fa_, un, fs = cfin(rat(p, q))
    row('cfin_' + str(p) + '_' + str(q) + '_is_e^-1', is_e1(c, E2, E3), E3=fmti(E3, 12), E2=fmti(E2, 12))
# the flat range end
c, E2, E3, fa_, un, fs = cfin(rat(78733761, 10 ** 9))
row('cfin_flat_end_0_078733761', is_e1(c, E2, E3), E3=fmti(E3, 12), E2=fmti(E2, 12), argmax_f=fa_, e_m1_lo=L.fmt(EM1[0], 12, False))
c2, E22, E32, fa2, un2, fs2 = cfin(rat(78733762, 10 ** 9))
row('cfin_leaves_e^-1_at_0_078733762', E32[0] > EM1[1] and fa2 == 7 and un2, E3=fmti(E32, 12), argmax_f=fa2)
# own sampling below the flat end (support only; the interval claim rests on Lemma 4.19)
okflat = True
for k in range(1, 79):
    cc, e2, e3, _, _, _ = cfin(rat(k, 1000))
    if not is_e1(cc, e2, e3):
        okflat = False
row('cfin_e^-1_at_k_over_1000_k1_78', okflat)
# fallback flat end 0.077320139
c, E2, E3, fa_, un, fs = cfin(rat(77320139, 10 ** 9), fallback=True)
c2, E22, E32, fa2, un2, fs2 = cfin(rat(77320140, 10 ** 9), fallback=True)
row('fallback_flat_end_0_077320139', is_e1(c, E2, E3) and E32[0] > EM1[1], E3_at_end=fmti(E3, 12), E3_next=fmti(E32, 12), argmax_next=fa2)
# c_fin at delta_crit^- = 0.114846768
c, E2, E3, fa_, un, fs = cfin(rat(114846768, 10 ** 9))
dp_c, lm_c = lam_rat(114846768, 10 ** 9)
gap = sub(K4, lm_c)
row('cfin_at_delta_crit_minus', inside(c, '0.989898', '0.989899'), cfin=fmti(c, 12), argmax_f=fa_, unique=int(un), scan_stop_f=fs,
    kappa_minus_lambda=scii(gap, 8), E2=fmti(E2, 8))
EB = exp_iv(sub(rat(114846769, 10 ** 9), rat(1, 8)))
row('lemma_4_17_bound_at_0_114846769', inside(EB, '0.9898981390', '0.9898981391'), e_pow=fmti(EB, 12),
    note='the_canonical_middle_step_<=0.989898139_is_false_as_written;assembly_note_correct')
EB2 = exp_iv(sub(rat(1148467681, 10 ** 10), rat(1, 8)))
_, lm_x = lam_rat(1148467681, 10 ** 10)
row('lemma_4_17_end_bound', gt_rat(lm_x[0], (1, 4)) and le_rat(EB2[1], dec('0.989898139')), e_pow=fmti(EB2, 12))


# Lemma 4.16 closed form against a brute-force sup of q(f,m), 1<=f<=60, 1<=m<=40
def qfm(f, m, lm):
    # q(f,m) = e^{-k(f+m)} e^{km/2} [e^{-k (m mod 2)/2} 1[m>=8] + e^{lambda f} - 1], k = 1/4
    base = exp_point(-((f + m) << (L.P - 2)) + (m << (L.P - 3)))
    br = sub(exp_iv(muli(lm, f)), L.const(1))
    if m >= 8:
        br = add(br, exp_point(-((m % 2) << (L.P - 3))))
    return mul(base, br)


okq = True
for (p, q) in [(1, 100), (3, 100), (5, 100), (7, 100), (8, 100), (11, 100)]:
    d = rat(p, q)
    dp, lm = lam_iv(d)
    best = (-1, -1)
    for f in range(1, 61):
        for m in range(1, 41):
            if f + m < 4:
                continue
            v = qfm(f, m, lm)
            best = imax(best, v)
    cbr = imax((EM1[0], EM1[1]), mul(exp_iv(d), best))
    cc, _, _, _, _, _ = cfin(d)
    # the closed form must be at least the brute-force sup and agree to many digits
    agree = cc[1] >= cbr[0] and (cc[0] - cbr[1]) <= (1 << (L.P - 300))
    if not agree:
        okq = False
row('lemma_4_16_closed_form_vs_bruteforce', okq, deltas='0.01,0.03,0.05,0.07,0.08,0.11')

# ------------------------------------------------------------------ C10c
E32 = exp_point(-(3 << (L.P - 1)))
row('C10c_e^-3/2/4', inside(divi(E32, 4), '0.05578254', '0.05578255'), value=fmti(divi(E32, 4), 12))
E1 = exp_point(L.ONE)
E52 = exp_point(5 << (L.P - 1))
for (sd, claims) in [(65536, dict(din=('0.0044613', '0.0044614'), lam=('0.0089526', '0.0089527'), ratio=('0.0557791', '0.0557860'),
                                  slice=('0.151623', '0.151642'), slack=('6.5944', '6.5953'), pr=('4.0902', '4.0908'), proj=('0.0328523', '0.0328622'))),
                     (8192, dict(din=('0.0356909', '0.0356910'), lam=('0.0733078', '0.0733079'), ratio=('0.0557553', '0.0558098'),
                                 slice=('0.15155', '0.15171'), slack=('6.591', '6.599'), pr=('4.7975', '4.8023'), proj=('0.0328285', '0.0328860')))]:
    s = rat(1, sd)
    din = mul(muli(s, 24), (E52[0], E52[1]))
    dp, lm = lam_iv(din)
    c, E2, E3, _, _, _ = cfin(din)
    c_is_e1 = is_e1(c, E2, E3)
    s2 = mul(s, s)
    nat = mul(muli((E1[0], E1[1]), 6), (sub(s, muli(s2, 4))[0], add(s, muli(s2, 4))[1]))     # 6e[s-4s^2, s+4s^2]
    nat_lo = mul(muli((E1[0], E1[1]), 6), sub(s, muli(s2, 4)))
    nat_hi = mul(muli((E1[0], E1[1]), 6), add(s, muli(s2, 4)))
    NAT = (nat_lo[0], nat_hi[1])
    PR = mul(exp_iv(add(sub(din, rat(3, 2)), muli(lm, 2))), din)                            # e^{delta-6k+2lambda} delta_in
    ratio = div(NAT, din)
    slice_ = div(NAT, mul((EM1[0], EM1[1]), din))
    slack = div(mul((EM1[0], EM1[1]), din), NAT)
    prr = div(PR, NAT)
    # projection bound 6e^{4k}|c_P|/e_chi with c_P in [s/2 - 4s^2 e_chi, s/2 + 4s^2 e_chi]
    cP = (sub(divi(s, 2), mul(muli(s2, 4), ECHI))[0], add(divi(s, 2), mul(muli(s2, 4), ECHI))[1])
    proj = div(mul(muli((E1[0], E1[1]), 6), div(cP, ECHI)), din)
    okc = (inside(din, *claims['din']) and inside(lm, *claims['lam']) and lt_rat(lm[1], (1, 4)) and c_is_e1 and inside(ratio, *claims['ratio'])
           and inside(slice_, *claims['slice']) and inside(slack, *claims['slack']) and inside(prr, *claims['pr']) and inside(proj, *claims['proj']))
    row('C10c_s_1_' + str(sd), okc, delta_in=fmti(din, 10), lam=fmti(lm, 10), cfin_is_e1=int(c_is_e1), nat_over_din=fmti(ratio, 9),
        nat_over_cfin_din=fmti(slice_, 9), slice_slack=fmti(slack, 7), perroot_over_nat=fmti(prr, 7), proj_over_din=fmti(proj, 9))

print('NUM_N1_END|fails=' + str(len(FAILS)) + '|' + ','.join(FAILS) + '|json=0')
