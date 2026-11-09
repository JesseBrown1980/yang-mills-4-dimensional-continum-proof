# n3_c09.py -- L5-numbers lane: C09's readout bound T = (8489/10000)*6*alpha*e^{-8 theta}, minimized
# over certified (alpha, theta) on the pinned grid theta = 1/4 + i/64, 0 <= i <= 320, with the C03 head;
# T/P_10, the minimizing index, the relative gap to the neighbours, the readout_grid_128 fault value,
# and the containment of P_10 in 2t_2^4 +- T. Own code, integer only.
import sys
sys.path.insert(0, '/mnt/c/tmp/opus55/ym4-04c-gattack/work/L5-numbers')
import ilib as L
from ilib import rat, add, sub, mul, div, muli, divi, exp_point, fmti, inside, dec, le_rat, lt_rat, gt_rat, ge_rat, scii, cdiv
import polylib as PL

FAILS = []


def row(name, ok, **kv):
    print('NUM|id=' + name + '|' + '|'.join(k + '=' + str(v) for k, v in kv.items()) + '|ok=' + ('1' if ok else '0') + '|json=0')
    sys.stdout.flush()
    if not ok:
        FAILS.append(name)


def P10(p, q):
    num = (p ** 4) * (q ** 6) * 17280 - (p ** 6) * (q ** 4) * 2880 + (p ** 8) * (q ** 2) * 1440 - 467 * (p ** 10)
    den = 2211840 * q ** 10
    return (num, den)


def In(n, p, q):
    """I_n(p/q) = sum_k (p/(2q))^{2k+n}/(k!(k+n)!), enclosure"""
    G = 64
    W = L.P + G
    one = 1 << W
    # first term (p/(2q))^n / n!
    fact = 1
    for j in range(1, n + 1):
        fact *= j
    t0n = p ** n
    t0d = (2 * q) ** n * fact
    lo_t = (one * t0n) // t0d
    hi_t = cdiv(one * t0n, t0d)
    a2 = p * p
    b2 = 4 * q * q
    s_lo, t = lo_t, lo_t
    k = 1
    while True:
        t = (t * a2) // (b2 * k * (k + n))
        if t == 0:
            break
        s_lo += t
        k += 1
    s_hi, t = hi_t, hi_t
    k = 1
    while True:
        t = cdiv(t * a2, b2 * k * (k + n))
        s_hi += t
        if t <= 1 and 2 * a2 <= b2 * (k + 1) * (k + 1 + n):
            break
        k += 1
    s_hi += 1
    return (s_lo >> G, cdiv(s_hi, 1 << G))


coef = PL.coef_list(PL.HEADS['C03'])
FROZEN = [((1, 4000), 194, '5.2e-4', '5.3e-4'), ((1, 2000), 150, '8.3e-3', '8.4e-3'), ((1, 1000), 105, '0.133', '0.134'),
          ((1, 700), 83, '0.557', '0.558'), ((1, 600), 73, '1.032', '1.033'), ((1, 100), 0, '6.9e3', '7.0e3')]
K = rat(8489 * 6, 10000)
for (b, iexp, lo_s, hi_s) in FROZEN:
    eps = PL.eps6(*b)
    pn, pd = P10(*b)
    PP = rat(pn, pd)
    Ts = {}
    for i in range(0, 321):
        A = PL.A_of(eps, i)
        rt = PL.least_root(A, coef)
        if rt is None:
            continue
        al = (rt[0], rt[1])
        e8 = exp_point(-((16 + i) << (L.P - 3)))
        T = mul(mul(K, al), e8)
        Ts[i] = div(T, PP)
    imin = None
    for i in Ts:
        if imin is None or Ts[i][1] < Ts[imin][0]:
            imin = i
    # certify the minimizer: every other index has a lower end above the minimizer's upper end
    unique = all(Ts[i][0] > Ts[imin][1] for i in Ts if i != imin)
    gaps = []
    for j in (imin - 1, imin + 1):
        if j in Ts:
            g = div(sub(Ts[j], Ts[imin]), Ts[imin])
            gaps.append(g)
    gmin = min(g[0] for g in gaps)
    # the indices without a certified root: any certified alpha there has alpha >= S(eps e^theta)
    # (S increases in alpha), so T/P_10 >= (8489/10000)*6*S^-(eps^- e^theta) e^{-8 theta}/P_10, or there is
    # no certified alpha at all when mu eps e^theta >= 1 (the pole at alpha = 0)
    excl_ok = True
    for i in range(0, 321):
        if i in Ts:
            continue
        A = PL.A_of(eps, i)
        r = PL.S_eval(A, coef)
        if not r.lo_finite:
            continue
        e8 = exp_point(-((16 + i) << (L.P - 3)))
        LB = div(mul(mul(K, (r.lo, r.lo)), e8), PP)
        if not LB[0] > Ts[imin][1]:
            excl_ok = False
    ok = imin == iexp and unique and inside(Ts[imin], lo_s, hi_s) and ge_rat(gmin, dec('1.9e-5')) and excl_ok
    row('C09_T_over_P10_' + str(b[0]) + '_' + str(b[1]), ok, i_min=imin, unique=int(unique), T_over_P10=scii(Ts[imin], 8),
        rel_gap_min=scii((gmin, gmin), 5), certified_i_count=len(Ts), i_range=str(min(Ts)) + '..' + str(max(Ts)),
        uncertified_i_excluded=int(excl_ok))
    if b == (1, 4000):
        i128 = None
        for i in Ts:
            if i <= 128 and (i128 is None or Ts[i][1] < Ts[i128][0]):
                i128 = i
        row('C19_readout_grid_128_1_4000', i128 == 128 and inside(Ts[i128], '1.47e-2', '1.48e-2'), i_min=i128, T_over_P10=scii(Ts[i128], 8))
    if b in ((1, 4000), (1, 2000), (1, 1000)):
        I1 = In(1, *b)
        I2 = In(2, *b)
        t2 = div(I2, I1)
        t24 = L.powi(t2, 4)
        two_t24 = muli(t24, 2)
        Tmin = mul(Ts[imin], PP)
        diff = sub(PP, two_t24)
        b8 = rat(b[0] ** 8, 2048 * b[1] ** 8)
        eta = sub(L.const(1), div(diff, b8))
        contain = (diff[1] <= Tmin[0]) and (-diff[0] <= Tmin[0])
        lowpow = div(Tmin, diff)
        row('C09_containment_' + str(b[0]) + '_' + str(b[1]), contain and ge_rat(eta[0], (0, 1)) and le_rat(eta[1], dec('4e-7')) and ge_rat(lowpow[0], dec('2.1e12')),
            P10_minus_2t2_4=scii(diff, 8), eta=scii(eta, 4) if eta[0] > 0 else fmti(eta, 12), T_over_diff=scii(lowpow, 4))

print('NUM_N3_END|fails=' + str(len(FAILS)) + '|' + ','.join(FAILS) + '|json=0')
