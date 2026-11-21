#!/usr/bin/env python3
# YM4-04C final-critic fix pass: exact reads behind B2, fix 6, fix 7 and fix 9. Scratch arithmetic, not an engine
# and not evidence. Integers and Fractions only; every enclosure is outward (the up/down/ex helpers of
# pkg/recompute/final_s_lane.py at 256 bits, loaded from its definitions block, which prints nothing).
# Floats appear only inside fmt(), for display. Run from anywhere: python3 -I -B fix_checks.py > fix_checks.out
import os
import sys
import itertools
from fractions import Fraction as Q

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'recompute', 'final_s_lane.py')
text = open(SRC, encoding='utf-8').read()
R = {'__name__': 'final_s_lane_defs', '__file__': SRC}
exec(compile(text.split("\nSECTIONS = ")[0], SRC, 'exec'), R)
up, down, ex, fmt, K, MU, EM1 = R['up'], R['down'], R['ex'], R['fmt'], R['K'], R['MU'], R['EM1']


def P(*a):
    print(' '.join(str(t) for t in a), flush=True)


def dec(s):
    return Q(s)


P('YM4-04C fix pass checks. e^{-1} in [%s, %s]' % (fmt(EM1[0], 14), fmt(EM1[1], 14)))

# ---------------- fix 6: chains at the certified delta_1 and at the upper end of the frozen bracket ----------------
P('== fix 6: chain bounds at the certified delta_1^+ = 6 alpha^+ and at the bracket end')
ROWS = [
    ('C07', Q(1, 100), 'crude', dec('0.0055222'), dec('0.0055223'), dec('2.0316e-3'), dec('8.737e-3')),
    ('C08', Q(1, 100), 'C03', dec('4.7159e-6'), dec('4.7160e-6'), dec('1.7350e-6'), dec('7.461e-6')),
    ('C11', Q(1, 64), 'crude', dec('0.0508265'), dec('0.0508266'), dec('1.8699e-2'), dec('8.041e-2')),
    ('C14', Q(1, 64), 'C03', dec('1.01738e-3'), dec('1.01739e-3'), dec('3.7428e-4'), dec('1.6095e-3')),
    ('C12', Q(1, 50), 'C03', dec('0.0363235'), dec('0.0363236'), dec('1.3363e-2'), dec('5.7463e-2')),
]
ENGINE_SLACK = Q(6, 2 ** 48)        # the engine's least root is a dyadic of denominator 2^48: delta_1 shifts by <= 6*2^-48
D1 = {}
for label, beta, head, blo, bhi, d2b, smb in ROWS:
    a_lo, a_up, ok = R['alpha_root'](beta, head)
    assert ok
    d_lo, d_hi = 6 * a_lo, 6 * a_up
    D1[label] = (d_lo, d_hi)
    inside = blo <= d_lo and d_hi <= bhi
    c_lo, c_hi, info = R['cfin'](d_lo, d_hi)
    flat = info['off_hi'] <= EM1[0]
    d2 = up(c_hi * d_hi)
    sm = up(d_hi / (1 - c_hi))
    # at the engine's resolution
    de = d_hi + ENGINE_SLACK
    ce = R['cfin'](de)[1]
    d2e, sme = up(ce * de), up(de / (1 - ce))
    # at the upper end of the frozen bracket: lower enclosures decide a failure, upper ones a pass
    cb_lo, cb_hi, _ = R['cfin'](bhi)
    d2b_lo, d2b_hi = down(cb_lo * bhi), up(cb_hi * bhi)
    smb_lo, smb_hi = down(bhi / (1 - cb_lo)), up(bhi / (1 - cb_hi))
    def verdict(lo, hi, bound):
        return 'holds' if hi <= bound else ('FAILS' if lo > bound else 'undecided')
    P('%s beta_0=%s head=%s: delta_1 in [%s, %s] inside the frozen [%s, %s]: %s; c_fin = e^{-1}: %s' % (
        label, beta, head, fmt(d_lo, 12), fmt(d_hi, 12), fmt(blo, 8), fmt(bhi, 8), inside, flat))
    P('   at the certified delta_1^+: delta_2 <= %s (bound %s: %s); sum_k delta_k <= %s (bound %s: %s); margins %s and %s' % (
        fmt(d2, 10), fmt(d2b, 6), d2 <= d2b, fmt(sm, 10), fmt(smb, 6), sm <= smb, fmt(d2b - d2, 4), fmt(smb - sm, 4)))
    P('   at delta_1^+ + 6*2^-48: delta_2 <= %s (%s); sum <= %s (%s)' % (fmt(d2e, 10), d2e <= d2b, fmt(sme, 10), sme <= smb))
    P('   at the bracket end %s: delta_2 in [%s, %s] (%s); sum in [%s, %s] (%s)' % (
        fmt(bhi, 8), fmt(d2b_lo, 10), fmt(d2b_hi, 10), verdict(d2b_lo, d2b_hi, d2b), fmt(smb_lo, 10), fmt(smb_hi, 10),
        verdict(smb_lo, smb_hi, smb)))

# C16: delta_20 <= c_fin(delta_1)^19 delta_1 and osc <= (512/e) delta_20, from C07's delta_1
d_lo, d_hi = D1['C07']
c_hi = R['cfin'](d_lo, d_hi)[1]
B20, BOSC = dec('3.0940e-11'), dec('5.828e-9')
d20 = up(c_hi ** 19 * d_hi)
osc = up(512 * EM1[1] * d20)
de = d_hi + ENGINE_SLACK
d20e = up(R['cfin'](de)[1] ** 19 * de)
bhi = dec('0.0055223')
d20b_lo, d20b_hi = down(EM1[0] ** 19 * bhi), up(EM1[1] ** 19 * bhi)
oscb_lo = down(512 * EM1[0] * d20b_lo)
P('C16 from C07: delta_20 <= e^{-19} delta_1^+ <= %s (bound 3.0940e-11: %s, margin %s); osc <= %s (bound 5.828e-9: %s)' % (
    fmt(d20, 10), d20 <= B20, fmt(B20 - d20, 4), fmt(osc, 10), osc <= BOSC))
P('   at delta_1^+ + 6*2^-48: delta_20 <= %s (%s)' % (fmt(d20e, 10), d20e <= B20))
P('   at the bracket end 0.0055223: e^{-19}*0.0055223 in [%s, %s] (%s); osc >= %s (%s)' % (
    fmt(d20b_lo, 10), fmt(d20b_hi, 10), 'FAILS' if d20b_lo > B20 else ('holds' if d20b_hi <= B20 else 'undecided'),
    fmt(oscb_lo, 10), 'FAILS' if oscb_lo > BOSC else 'holds or undecided'))
c12 = D1['C12']
P('C12 certified delta_1 in [%s, %s] (10-digit grid: inside [0.0363235365, 0.0363235366]: %s)' % (
    fmt(c12[0], 13), fmt(c12[1], 13), dec('0.0363235365') <= c12[0] and c12[1] <= dec('0.0363235366')))
c07 = D1['C07']
P('C07 certified delta_1 in [%s, %s] (inside [0.0055222253, 0.0055222254]: %s)' % (
    fmt(c07[0], 13), fmt(c07[1], 13), dec('0.0055222253') <= c07[0] and c07[1] <= dec('0.0055222254')))

# ---------------- B2: missing_tail with and without the pole test ----------------
P('== B2: missing_tail (S -> the head-only sum_{n=4..10} N(n) x^n with the C03 head), theta = 1/4')
HEAD = R['HEADS']['C03']


def s_head(x):
    return sum(HEAD[n] * x ** n for n in range(4, 11))


ALPHA = Q(1, 2 ** 22)
for beta, role in ((Q(1, 40), 'C04 guard'), (Q(2248, 100000), 'C04 guard'), (Q(2076, 100000), 'C06 NOT_MET point')):
    el, eh = R['eps6'](beta)
    wall_lo, wall_hi = down(MU * el * ex(K)[0]), up(MU * eh * ex(K)[1])
    xp = up(eh * ex(2 * ALPHA + K)[1])
    pole_pass = up(MU * xp) < 1          # the read's first step: mu^+ x^+ < 1 (mu is exact here)
    sp = up(s_head(xp))
    met_no_pole = sp <= ALPHA
    P('%s (%s): mu e^{1/4} eps_6 in [%s, %s]; at alpha = 2^-22: mu^+ x^+ < 1: %s; S_head^+ = %s <= alpha: %s' % (
        beta, role, fmt(wall_lo, 9), fmt(wall_hi, 9), pole_pass, fmt(sp, 6), met_no_pole))
    if wall_lo >= 1:
        P('   pole test kept: mu x >= mu eps_6^- e^{1/4} >= 1 at every alpha >= 0 and theta >= 1/4, so the read is NOT_MET'
          ' by the pole and the fault does not fire here; pole test removed with the tail: MET at alpha = 2^-22')
    else:
        P('   pole test kept: it passes, and the head-only S reads MET at alpha = 2^-22: %s' % (pole_pass and met_no_pole))

# ---------------- fix 7: one_position_support, and the variant that also counts the coarse Y ----------------
P('== fix 7: C10 line channel on fine (Z/8)^4 -> coarse (Z/4)^4 -> next blocking (Z/2)^4')
L, LC = 8, 4


def e(mu):
    return tuple(1 if i == mu else 0 for i in range(4))


def addc(x, y, m):
    return tuple((a + b) % m for a, b in zip(x, y))


def pos1(link):
    """1 if the coarse link (y, d) is position 1 of a link of the next blocking: y_d odd, every other coordinate even."""
    y, d = link
    return int(y[d] % 2 == 1 and all(y[j] % 2 == 0 for j in range(4) if j != d))


fine_in, fine_y_all, fine_y_pos1, coarse_in, n_of = {}, set(), set(), {}, {}
for xc in itertools.product(range(LC), repeat=4):
    for mu, nu in itertools.combinations(range(4), 2):
        cl = [(xc, mu), (addc(xc, e(mu), LC), nu), (addc(xc, e(nu), LC), mu), (xc, nu)]
        fl = []
        for (y, d) in cl:
            x0 = tuple(2 * c for c in y)
            fl += [((x0, d), 0), ((addc(x0, e(d), L), d), 1)]
        for (l, p) in fl:
            fine_in[l] = fine_in.get(l, 0) + 1
        fine_y_all.add(len(fl))
        fine_y_pos1.add(sum(1 for (_, p) in fl if p == 1))
        n = sum(pos1(c) for c in cl)
        for c in cl:
            coarse_in.setdefault(c, []).append(n)
        n_of[(xc, mu, nu)] = n
cnt = max(fine_in.values())
P('fine: max Y per fine line link %d; #Y = %s; #Y at position 1 = %s; coarse: P\'\' per coarse link %s' % (
    cnt, sorted(fine_y_all), sorted(fine_y_pos1), sorted(set(len(v) for v in coarse_in.values()))))
P('position-1 counts of the coarse Y = boundary of P\'\' for the next blocking: %s' % sorted(set(n_of.values())))
multisets = sorted(set(tuple(sorted(v)) for v in coarse_in.values()))
P('multisets of these counts over the 6 P\'\' through a coarse link: %s' % multisets)
for kap in (Q(1, 4), Q(0)):
    E = ex(kap)
    best = None
    for ms in multisets:
        lo = sum(down(E[0] ** k) for k in ms)
        hi = sum(up(E[1] ** k) for k in ms)
        if best is None or lo > best[2]:
            best = (ms, lo, hi)
    ms, lo, hi = best
    assert all(sum(up(E[1] ** k) for k in m) <= lo for m in multisets if m != ms), 'maximizer not certified'
    fine_lo, fine_hi = 6 * down(E[0] ** 4), 6 * up(E[1] ** 4)      # faulted fine norm / (2|s|): 6 e^{4 kappa}
    r_lo, r_hi = down(lo / fine_hi), up(hi / fine_lo)
    P('kappa=%s: variant coarse norm / (2|s|) = sum over %s of e^{kappa n} in [%s, %s]; faulted fine norm / (2|s|) = 6e^{4kappa};'
      ' variant ratio in [%s, %s]' % (kap, ms, fmt(lo, 10), fmt(hi, 10), fmt(r_lo, 10), fmt(r_hi, 10)))
    if kap == Q(1, 4):
        cf_lo = down((ex(Q(-3, 4))[0] + ex(Q(-1, 2))[0]) / 2)
        cf_hi = up((ex(Q(-3, 4))[1] + ex(Q(-1, 2))[1]) / 2)
        P('   closed form (e^{-3kappa} + e^{-2kappa})/2 in [%s, %s]; strictly between e^{-1} and 1: %s; above e^{-kappa} = %s: %s' % (
            fmt(cf_lo, 10), fmt(cf_hi, 10), EM1[1] < cf_lo and cf_hi < 1, fmt(ex(-K)[0], 10), cf_lo > ex(-K)[1]))
P('pinned fault (fine-norm routine only, coarse #Y\'\' = 4): ratio = e^{kappa(4-4)} = 1; correct: e^{kappa(4-8)} = e^{-1}')

# ---------------- fix 9: W01's 2^k r_k ----------------
P('== fix 9: W01 corners')
r1, r2 = Q(15, 28), Q(25823, 98640)
r3 = (dec('0.1274530942'), dec('0.1274530943'))
P('2 r_1 = %s; 4 r_2 = %s; 8 r_3 in [%s, %s] inside [1.0196247, 1.0196248]: %s; strictly decreasing: %s' % (
    2 * r1, 4 * r2, 8 * r3[0], 8 * r3[1], dec('1.0196247') <= 8 * r3[0] and 8 * r3[1] <= dec('1.0196248'),
    2 * r1 > 4 * r2 > 8 * r3[1]))

# ---------------- the exact statements the rows quote ----------------
P('== exact statements quoted in the rows')
lo12 = D1['C12'][1]
c_hi12 = R['cfin'](D1['C12'][0], lo12)[1]
P('C12: sum at the certified delta_1^+ <= 5.7463e-2: %s; at 0.0363236 the lower enclosure of 0.0363236/(1-e^{-1}) is above 0.05746308: %s' % (
    up(lo12 / (1 - c_hi12)) <= dec('5.7463e-2'), down(dec('0.0363236') / (1 - EM1[0])) > dec('0.05746308')))
P('C16: e^{-19} delta_1^+ <= 3.093991e-11: %s; e^{-19}*0.0055223 is above 3.094032e-11: %s' % (
    d20 <= dec('3.093991e-11'), d20b_lo > dec('3.094032e-11')))
cf_lo = down((ex(Q(-3, 4))[0] + ex(Q(-1, 2))[0]) / 2)
cf_hi = up((ex(Q(-3, 4))[1] + ex(Q(-1, 2))[1]) / 2)
P('fix 7 variant ratio (e^{-3/4} + e^{-1/2})/2 inside [0.5394486, 0.5394487]: %s' % (
    dec('0.5394486') <= cf_lo and cf_hi <= dec('0.5394487')))
el, eh = R['eps6'](Q(2076, 100000))
xp = up(eh * ex(2 * ALPHA + K)[1])
P('B2 variant at 0.02076: mu^+ x^+ < 1 at alpha = 2^-22: %s; S_head^+ <= 9.27e-8 <= alpha: %s' % (
    up(MU * xp) < 1, up(s_head(xp)) <= dec('9.27e-8') <= ALPHA))
