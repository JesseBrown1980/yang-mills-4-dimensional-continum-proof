# c05_c06_edges.py -- G_attack filing, second seat (local Opus 5.5 seat, pid 8467a937cba309f7).
# Reproduces the C_0 reads of the reviewers' edge file ym4-04c/final-check/edges.py (PR #45 head
# dfe0859, sha256 c2f4f7bb...afa85) that no lane had certified: the C05 crude edge 0.01904/0.01905
# and the C06 NOT_MET at 0.02076 (C03 head and head-free), plus the 1/50 reads of C05 and C06.
# Integer only. Reuses the L5-numbers lane library (ilib, polylib): outward-rounded dyadic
# intervals at P = 640 bits, the frozen closed form S with exact mu, pole test first.
# MET read: S^+(x^+(alpha)) <= alpha at a dyadic alpha with the pole test passed (Lemma 3.30).
# NOT_MET proof (convex tangent bound, Lemmas 3.30/3.31): at theta = kappa = 1/4 (enough by
# Lemma 3.31 item 2), points c < c' = c + h with g'^+(c) <= 0, g'^-(c') >= 0, g^-(c) + g'^-(c) h > 0
# and g^-(c') > 0 give g > 0 on [0, pole); beyond the pole no read is possible.
import sys
sys.path.insert(0, '/mnt/c/tmp/opus55/ym4-04c-gattack/work/L5-numbers')
import ilib as L
from ilib import cdiv, scii
import polylib as PL

FAILS = []


def row(name, ok, **kv):
    print('FILING_EDGE|id=' + name + '|' + '|'.join(k + '=' + str(v) for k, v in kv.items())
          + '|ok=' + ('1' if ok else '0') + '|tag=MEASURED|json=0')
    sys.stdout.flush()
    if not ok:
        FAILS.append(name)


def g_at(A, coef, a):
    """enclosures of g = S(x(a)) - a and g' = 2 x S'(x) - 1 at an exact dyadic a >= 0"""
    x = PL.x_at(A, a)
    r = PL.S_eval(x, coef, deriv=True, tail=True)
    if not r.pole_ok:
        return None
    glo = r.lo - a
    ghi = r.hi - a
    gplo = ((2 * x[0] * r.dlo) >> L.P) - L.ONE
    gphi = cdiv(2 * x[1] * r.dhi, L.ONE) - L.ONE
    return glo, ghi, gplo, gphi


def met(b, head):
    A = PL.A_of(PL.eps6(*b), 0)
    coef = PL.coef_list(PL.HEADS[head])
    rt = PL.least_root(A, coef)
    if rt is None:
        return False, None
    return PL.certify_upper(A, coef, rt[1]), rt


def notmet(b, head):
    A = PL.A_of(PL.eps6(*b), 0)
    coef = PL.coef_list(PL.HEADS[head])
    # bisection for the sign change of g' on [0, pole), using point values; out-of-domain counts as g' > 0
    lo, hi = 0, L.ONE >> 2
    r0 = g_at(A, coef, 0)
    if r0 is not None and r0[2] >= 0:
        # g nondecreasing from 0: g >= g(0)
        return r0[0] > 0, dict(case='g_prime_at_0_nonneg', g0_lo=scii((r0[0], r0[1]), 8))
    for _ in range(200):
        m = (lo + hi) >> 1
        r = g_at(A, coef, m)
        if r is None or (r[2] + r[3]) > 0:
            hi = m
        else:
            lo = m
        if hi - lo <= (1 << (L.P - 60)):
            break
    for hs in (40, 34, 30, 26, 22):
        h = 1 << (L.P - hs)
        c = max(0, lo - h)
        c2 = c + 2 * h
        rc = g_at(A, coef, c)
        rc2 = g_at(A, coef, c2)
        if rc is None or rc2 is None:
            continue
        glo_c, _, gplo_c, gphi_c = rc
        glo_c2, _, gplo_c2, _ = rc2
        ok_left = gphi_c <= 0
        ok_right = gplo_c2 >= 0
        mid_lb = glo_c + ((gplo_c * (c2 - c)) >> L.P)
        if ok_left and ok_right and mid_lb > 0 and glo_c2 > 0:
            return True, dict(h_bits=hs, alpha_star=scii((c, c2), 10), g_min_lb=scii((mid_lb, mid_lb), 8),
                              g_c2_lb=scii((glo_c2, glo_c2), 8))
    return False, dict(alpha_star=scii((lo, hi), 10))


# C05: crude head, MET at 0.01903 and 0.01904, NOT_MET at 0.01905 and at 1/50
for j in (1903, 1904):
    ok, rt = met((j, 100000), 'crude')
    row('C05_crude_MET_' + str(j), ok, alpha_minus=None if rt is None else scii(rt, 11))
for b in ((1905, 100000), (1, 50)):
    ok, info = notmet(b, 'crude')
    row('C05_crude_NOT_MET_' + str(b[0]) + '_' + str(b[1]), ok, **info)
# C06: C03 head and head-free, MET at 0.02075, NOT_MET at 0.02076; C03 MET at 1/50
for head in ('C03', 'headfree'):
    ok, rt = met((2075, 100000), head)
    row('C06_' + head + '_MET_2075', ok, alpha_minus=None if rt is None else scii(rt, 11))
    ok, info = notmet((2076, 100000), head)
    row('C06_' + head + '_NOT_MET_2076', ok, **info)
ok, rt = met((1, 50), 'C03')
row('C06_C03_MET_1_50', ok, alpha_minus=None if rt is None else scii(rt, 11))
print('FILING_EDGE_END|fails=' + str(len(FAILS)) + '|' + ','.join(FAILS) + '|json=0')
