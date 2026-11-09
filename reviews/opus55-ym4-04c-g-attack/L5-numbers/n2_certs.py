# n2_certs.py -- L5-numbers lane: eps_6, the C_0 least roots and delta_1 of C07, C08, C11, C12, C14,
# the self-map edge reads of C13 and C14 (and their fallback and the C19 surrogate), C16, and the
# C19 missing_tail reads. Own code, integer only.
import sys
sys.path.insert(0, '/mnt/c/tmp/opus55/ym4-04c-gattack/work/L5-numbers')
import ilib as L
from ilib import rat, add, sub, mul, div, muli, divi, exp_iv, exp_point, fmti, inside, dec, le_rat, lt_rat, gt_rat, ge_rat, scii, cdiv
import polylib as PL
import g1lib as G

FAILS = []


def row(name, ok, **kv):
    print('NUM|id=' + name + '|' + '|'.join(k + '=' + str(v) for k, v in kv.items()) + '|ok=' + ('1' if ok else '0') + '|json=0')
    sys.stdout.flush()
    if not ok:
        FAILS.append(name)


EM1 = exp_point(-L.ONE)

# ---------------------------------------------------------------- eps_6 against C02
C02 = [((1, 1000), '6.53830e-4', '6.53831e-4'), ((1, 100), '6.538419e-3', '6.538420e-3'), ((1, 64), '1.0216544e-2', '1.0216545e-2'),
       ((1, 50), '1.3077541e-2', '1.3077542e-2'), ((1, 45), '1.4530846e-2', '1.4530847e-2'), ((1, 40), '1.6347585e-2', '1.6347586e-2'),
       ((1, 10), '6.5499695e-2', '6.5499696e-2'), ((1, 1), '0.740642074', '0.740642075'), ((4, 1), '4.29699629', '4.29699630')]
EPS = {}
for (b, lo_s, hi_s) in C02:
    e = PL.eps6(*b)
    EPS[b] = e
    row('eps6_' + str(b[0]) + '_' + str(b[1]), inside(e, lo_s, hi_s), eps6=scii(e, 12), width_bits=(e[1] - e[0]).bit_length())


def eps(b):
    if b not in EPS:
        EPS[b] = PL.eps6(*b)
    return EPS[b]


def delta1(b, head):
    """delta_1 = 6 alpha_-(1/4) for coupling b = (p, q) and a head name"""
    A = PL.A_of(eps(b), 0)
    rt = PL.least_root(A, PL.coef_list(PL.HEADS[head]))
    if rt is None:
        return None
    return (6 * rt[0], 6 * rt[1])


def chain(name, D, d1_lo, d1_hi, lam_lo, lam_hi, d2_s, sum_s, extra_end=None):
    dp, lm = G.lam_iv(D)
    c, E2, E3, _, _, _ = G.cfin(D)
    e1 = G.is_e1(E2, E3)
    d2 = mul(EM1, D)
    sm = div(D, sub(L.const(1), EM1))
    ok = inside(D, d1_lo, d1_hi) and (lam_lo is None or inside(lm, lam_lo, lam_hi)) and lt_rat(lm[1], (1, 4)) and e1 \
        and le_rat(d2[1], dec(d2_s)) and le_rat(sm[1], dec(sum_s))
    kv = dict(delta1=scii(D, 12), lam=scii(lm, 10), cfin_is_e1=int(e1), delta2=scii(d2, 8), sum=scii(sm, 8))
    # the engine's certified delta_1^+ = 6 alpha^+ with alpha^+ on the 2^-48 grid: test at delta_1^+ + 6*2^-48
    Dp = (D[0], D[1] + (6 << (L.P - 48)))
    d2p = mul(EM1, Dp)
    smp = div(Dp, sub(L.const(1), EM1))
    kv['at_delta1_plus_6x2^-48'] = str(int(le_rat(d2p[1], dec(d2_s)) and le_rat(smp[1], dec(sum_s))))
    if extra_end is not None:
        De = rat(*dec(d1_hi))
        d2e = mul(EM1, De)
        sme = div(De, sub(L.const(1), EM1))
        kv['at_bracket_end'] = str(int(le_rat(d2e[1], dec(d2_s)) and le_rat(sme[1], dec(sum_s))))
    row(name, ok, **kv)
    return D


# ---------------------------------------------------------------- C07, C08, C11, C14 at 1/64, C12
D07 = delta1((1, 100), 'crude')
chain('C07_chain_1/100_crude', D07, '0.0055222', '0.0055223', '0.0110902', '0.0110903', '2.0316e-3', '8.737e-3', extra_end=1)
dp07, _ = G.lam_iv(D07)
row('C07_two_dprime', inside(muli(dp07, 2), '0.0111056', '0.0111057'), two_dprime=fmti(muli(dp07, 2), 10))
D08 = delta1((1, 100), 'C03')
chain('C08_chain_1/100_C03', D08, '4.7159e-6', '4.7160e-6', '9.4320e-6', '9.4321e-6', '1.7350e-6', '7.461e-6', extra_end=1)
D08h = delta1((1, 100), 'headfree')
row('C08_headfree_lower_limit', inside(D08h, '4.6861e-6', '4.6862e-6') and D08h[1] < D08[0], delta1_headfree=scii(D08h, 12))
R = div(D07, D08)
row('C08_crude_over_refined', inside(R, '1170', '1172'), ratio=fmti(R, 6))
# P_10(1/100) and 12 e P_10
b = (1, 100)


def P10(p, q):
    # beta^4/128 - beta^6/768 + beta^8/1536 - 467 beta^10/2211840, exact integer pair
    num = (p ** 4) * (q ** 6) * 17280 - (p ** 6) * (q ** 4) * 2880 + (p ** 8) * (q ** 2) * 1440 - 467 * (p ** 10)
    den = 2211840 * q ** 10
    # check the common denominator: 2211840/128 = 17280, /768 = 2880, /1536 = 1440
    assert 2211840 == 128 * 17280 == 768 * 2880 == 1536 * 1440
    return (num, den)


pn, pd = P10(1, 100)
E1 = exp_point(L.ONE)
W12 = mul(muli(E1, 12), rat(pn, pd))
row('C08_12e_P10', inside(W12, '2.548e-9', '2.549e-9'), value=scii(W12, 10))
RW = div(D08, W12)
row('C08_delta1_over_12eP10', inside(RW, '1850', '1851'), ratio=fmti(RW, 4))

D11 = delta1((1, 64), 'crude')
chain('C11_chain_1/64_crude', D11, '0.0508265', '0.0508266', '0.1055724', '0.1055725', '1.8699e-2', '8.041e-2', extra_end=1)
dp11, _ = G.lam_iv(D11)
row('C11_two_dprime', inside(muli(dp11, 2), '0.1069532', '0.1069533') and le_rat(muli(dp11, 2)[1], (1, 8)), two_dprime=fmti(muli(dp11, 2), 10))
D14 = delta1((1, 64), 'C03')
chain('C14_chain_1/64_C03', D14, '1.01738e-3', '1.01739e-3', '2.0363e-3', '2.0364e-3', '3.7428e-4', '1.6095e-3', extra_end=1)
D12 = delta1((1, 50), 'C03')
chain('C12_chain_1/50_C03', D12, '0.0363235', '0.0363236', '0.0746422', '0.0746423', '1.3363e-2', '5.7463e-2', extra_end=1)
row('C12_certified_delta1', inside(D12, '0.0363235365', '0.0363235366'), delta1=fmti(D12, 13))
D12h = delta1((1, 50), 'headfree')
row('C12_headfree', inside(D12h, '0.0363229', '0.0363230'), delta1=fmti(D12h, 12))

# ---------------------------------------------------------------- C16
D20 = mul(exp_point(-(19 << L.P)), D07)
OSC = mul(mul(L.const(512), exp_point(-L.ONE)), D20)
D20p = mul(exp_point(-(19 << L.P)), (D07[0], D07[1] + (6 << (L.P - 48))))
END = mul(exp_point(-(19 << L.P)), rat(*dec('0.0055223')))
row('C16_delta20', le_rat(D20[1], dec('3.093991e-11')) and le_rat(D20[1], dec('3.0940e-11')) and le_rat(D20p[1], dec('3.0940e-11'))
    and gt_rat(END[0], dec('3.094032e-11')), delta20=scii(D20, 10), at_bracket_end=scii(END, 10))
row('C16_osc', le_rat(OSC[1], dec('5.828e-9')), osc=scii(OSC, 10), osc_from_3_0940em11=scii(mul(mul(L.const(512), exp_point(-L.ONE)), rat(30940, 10 ** 15)), 8))

# ---------------------------------------------------------------- edge reads
DCm = (114846768, 6 * 10 ** 9)
DCp = (114846769, 6 * 10 ** 9)
FBm = (111780108, 6 * 10 ** 9)
FBp = (111780109, 6 * 10 ** 9)
SUR = (49, 6000)


def edge(name, bm, bp, head, am, ap, d_m=None, d_p=None):
    cf = PL.coef_list(PL.HEADS[head])
    Am = PL.A_of(eps(bm), 0)
    Ap = PL.A_of(eps(bp), 0)
    met, rm, _ = PL.met_read(Am, cf, rat(*am))
    nmet, rp, _ = PL.notmet_read(Ap, cf, rat(*ap))
    kv = dict(MET_at=str(bm[0]) + '/' + str(bm[1]), MET=int(met), NOTMET_at=str(bp[0]) + '/' + str(bp[1]), NOTMET=int(nmet))
    ok = met and nmet
    if d_m is not None:
        Dm = delta1(bm, head)
        Dp = delta1(bp, head)
        kv['delta1_m'] = fmti(Dm, 10)
        kv['delta1_p'] = fmti(Dp, 10)
        ok = ok and inside(Dm, *d_m) and inside(Dp, *d_p)
    row(name, ok, **kv)


edge('C14_edge_C03', (2074, 100000), (2075, 100000), 'C03', DCm, DCp, ('0.1088558', '0.1088559'), ('0.1158911', '0.1158912'))
edge('C14_edge_headfree', (2074, 100000), (2075, 100000), 'headfree', DCm, DCp, ('0.1088527', '0.1088528'), ('0.1158861', '0.1158862'))
edge('C14_edge_C03_fallback', (2074, 100000), (2075, 100000), 'C03', FBm, FBp)
edge('C14_edge_headfree_fallback', (2074, 100000), (2075, 100000), 'headfree', FBm, FBp)
edge('C13_edge_crude', (1767, 100000), (1768, 100000), 'crude', DCm, DCp, ('0.1145675', '0.1145676'), ('0.1150830', '0.1150831'))
edge('C13_edge_crude_fallback', (1761, 100000), (1762, 100000), 'crude', FBm, FBp)
edge('C19_surrogate_edge_crude', (1552, 100000), (1553, 100000), 'crude', SUR, SUR)
# the refined C_0 is MET at 0.02075 (C06 says so; read here only as a root existing)
A = PL.A_of(eps((2075, 100000)), 0)
rt = PL.least_root(A, PL.coef_list(PL.HEADS['C03']))
row('C06_refined_C0_MET_at_0_02075', rt is not None)

# ---------------------------------------------------------------- C19 missing_tail and the C04 guard
a22 = (1 << (L.P - 22), 1 << (L.P - 22))
for (b, bound) in [((1, 40), '1.96e-7'), ((2248, 100000), '1.28e-7'), ((2076, 100000), '9.27e-8')]:
    A = PL.A_of(eps(b), 0)
    x = PL.x_at_iv(A, a22)
    r = PL.S_eval(x, PL.coef_list(PL.HEADS['C03'])[:11] + [0] * 38, tail=False)
    mux_lo = (x[0] * PL.MU_N) // PL.MU_D
    row('C19_missing_tail_' + str(b[0]) + '_' + str(b[1]), le_rat(r.hi, dec(bound)) and r.hi <= a22[0],
        S_hi=scii((r.lo, r.hi), 8), MET_at_alpha_2pow_m22=int(r.hi <= a22[0]), pole_mu_x=fmti((mux_lo, cdiv(x[1] * PL.MU_N, PL.MU_D)), 8))
E14 = exp_point(1 << (L.P - 2))
for (b, lo_s) in [((1, 40), '1.1125'), ((2248, 100000), '1.00035')]:
    wq = mul(mul(eps(b), E14), rat(PL.MU_N, PL.MU_D))
    row('C04_guard_wall_' + str(b[0]) + '_' + str(b[1]), ge_rat(wq[0], dec(lo_s)), mu_e14_eps=fmti(wq, 8))
for (b, lo_s, hi_s) in [((1, 40), '1.1125', '1.1126'), ((1, 45), '0.9888', '0.9889')]:
    wq = mul(mul(eps(b), E14), rat(PL.MU_N, PL.MU_D))
    row('C15_wall_' + str(b[0]) + '_' + str(b[1]), inside(wq, lo_s, hi_s), mu_e14_eps=fmti(wq, 8))

print('NUM_N2_END|fails=' + str(len(FAILS)) + '|' + ','.join(FAILS) + '|json=0')
