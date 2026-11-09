# Lane L2-sec3-part2, check T3 at step 0: the tail beyond the head (Lemma 3.11, Corollary 3.12),
# the closed tail 6F(49)x^49/(1 - mu x) with the pole test (Lemmas 3.29, 3.30), mu's bracket, and the
# C19 missing_tail planted-fault reads at 1/40 and 0.02248 (alpha = 2^-22), with the C04 pole guard.
# Integers only: rationals as (num, den) pairs, outward dyadic rounding at P bits.
import sys
from qint import q, add, sub, mul, div, le, lt, ZERO, ONE, up, down, dec, iroot_floor, exp_lo_hi, F, comb, factorial, ip, sgn

out = []
def say(s):
    out.append(s); print(s)
P = 1400   # bits; 2^-1400 is far below 6F(n)x^n relative precision needs (F(49) ~ 1.9e80)
MU = q(20 ** 20, 19 ** 19)          # exact mu = 20^20/19^19
ok_all = True
def need(flag, label):
    global ok_all
    if not flag:
        ok_all = False
        say("FAIL|" + label)

# ---- 1. mu bracket (Lemma 3.11's integer inequality) ----
b1 = 5300068 * 19 ** 19 <= 100000 * 20 ** 20 <= 5300069 * 19 ** 19
need(b1, "mu_bracket")
say("MU|5300068*19^19<=100000*20^20<=5300069*19^19:%d|mu_in=[%s,%s]|tag=MEASURED" % (int(b1), dec(MU, 8), dec(MU, 8, "ceil")))

# ---- 2. Lemma 3.11 product formula, strict increase, strictly below mu, n = 0..400 ----
ok2 = True; prev = None
for n in range(0, 401):
    Fn, Fn1 = F(n), F(n + 1)
    num = 20; den = 1
    for j in range(1, 20):
        num *= 20 * n + j; den *= 19 * n + j + 1
    if Fn1 * den != Fn * num: ok2 = False
    r = q(Fn1, Fn)
    if not (Fn1 * 19 ** 19 < Fn * 20 ** 20): ok2 = False
    if prev is not None and not lt(prev, r): ok2 = False
    prev = r
need(ok2, "lemma_3.11_ratio")
f49 = F(49)
say("LEMMA_3.11|product_formula_exact_n=0..400:%d|strictly_increasing:%d|strictly_below_mu:%d|F(49)=%d|tag=MEASURED" % (int(ok2), int(ok2), int(ok2), f49))

# ---- 3. closed-tail domination sum_{n>=49}6F(n)y^n <= 6F(49)y^49/(1-mu y), partial sums at y with mu*y in {1/2, 99/100} ----
ok3 = True
for frac in (q(1, 2), q(99, 100)):
    y = div(frac, MU)
    closed = div(mul(q(6 * f49), (y[0] ** 49, y[1] ** 49)), sub(ONE, mul(MU, y)))
    part = ZERO; yn = (y[0] ** 49, y[1] ** 49)
    for n in range(49, 49 + 301):
        part = add(part, mul(q(6 * F(n)), yn))
        yn = mul(yn, y)
        if not le(part, closed): ok3 = False
    say("CLOSED_TAIL|mu*y=%s|partial_sum_n=49..349<=closed_form:%d|partial/closed>=%s|tag=MEASURED" % (dec(frac, 2), int(le(part, closed)), dec(div(part, closed), 6)))
need(ok3, "closed_tail")

# ---- 4. eps_6 enclosures ----
def c0_enclosure(x, M=40):
    # c_0(x) = sum_m (x/2)^{2m}/(m!(m+1)!), x >= 0 small; tail after m = M is at most 2 x the first omitted term
    s = ZERO; xx = mul(x, x)
    t = ONE   # m = 0 term
    for m in range(0, M + 1):
        s = add(s, t)
        t = div(mul(t, xx), q(4 * (m + 1) * (m + 2)))
    return s, add(s, mul(q(2), t))
def eps6_enclosure(beta):
    c = {k: c0_enclosure(mul(q(k), beta)) for k in range(1, 7)}
    c[0] = (ONE, ONE)
    lo1, hi1 = c[1]
    nlo = ZERO; nhi = ZERO
    for k in range(0, 7):
        coef = comb(6, k) * sgn(6 - k)
        plo = mul(c[k][0], (ip(lo1[0], 6 - k), ip(lo1[1], 6 - k)))
        phi_ = mul(c[k][1], (ip(hi1[0], 6 - k), ip(hi1[1], 6 - k)))
        if coef > 0:
            nlo = add(nlo, mul(q(coef), plo)); nhi = add(nhi, mul(q(coef), phi_))
        else:
            nlo = add(nlo, mul(q(coef), phi_)); nhi = add(nhi, mul(q(coef), plo))
    assert lt(ZERO, nlo)
    dlo = (lo1[0] ** 6, lo1[1] ** 6); dhi = (hi1[0] ** 6, hi1[1] ** 6)
    e6lo = div(nlo, dhi); e6hi = div(nhi, dlo)
    K = 300
    t_lo = (e6lo[0] << (6 * K)) // e6lo[1]
    t_hi = -((-(e6hi[0] << (6 * K))) // e6hi[1])
    plo = iroot_floor(t_lo, 6)
    phi2 = iroot_floor(t_hi, 6)
    if phi2 ** 6 < t_hi: phi2 += 1
    return q(plo, 1 << K), q(phi2, 1 << K)
BETAS = {"1/40": q(1, 40), "0.02248": q(2248, 100000), "0.02076": q(2076, 100000), "0.02075": q(2075, 100000)}
EPS = {k: eps6_enclosure(b) for k, b in BETAS.items()}
for k in BETAS:
    say("EPS6|beta=%s|eps6_in=[%s,%s]|tag=MEASURED" % (k, dec(EPS[k][0], 12), dec(EPS[k][1], 12, "ceil")))
c02_ok = le(q(16347585, 10 ** 9), EPS["1/40"][0]) and le(EPS["1/40"][1], q(16347586, 10 ** 9))
need(c02_ok, "C02_bracket_1/40")
say("EPS6_C02|beta=1/40_inside_[1.6347585e-2,1.6347586e-2]:%d" % int(c02_ok))

QUART = q(1, 4)
E14 = exp_lo_hi(QUART)
# ---- 5. pole guard (C04): mu * e^{1/4} * eps6^- ----
for k, lim in (("1/40", q(11125, 10000)), ("0.02248", q(100035, 100000))):
    wq = mul(mul(MU, E14[0]), EPS[k][0])
    flag = le(lim, wq)
    need(flag, "pole_guard_" + k)
    say("POLE_GUARD|beta=%s|mu*e^(1/4)*eps6^->=%s|>=%s:%d|so_mu*x>1_for_every_alpha>0,theta>=1/4:honest_C_0_NOT_MET_by_the_pole|tag=MEASURED" % (k, dec(wq, 7), dec(lim, 5), int(flag)))

HEADS = {"C03": {4: 1, 5: 0, 6: 12, 7: 0, 8: 32, 9: 32, 10: 304},
         "crude": {n: 6 * F(n) for n in range(4, 11)},
         "headfree": {n: 0 for n in range(4, 11)}}

def xs(eps, alpha, theta, mode):
    r = add(mul(q(2), alpha), theta)
    lo, hi = exp_lo_hi(r)
    return up(mul(eps[1], hi), P) if mode == "up" else down(mul(eps[0], lo), P)

def S_poly(head, x, nlo, nhi, mode):
    # sum_{n=nlo}^{nhi} c_n x^n with c_n = head (n<=10) or 6F(n) (n>=11); every product rounded in `mode`
    rnd = up if mode == "up" else down
    s = ZERO; xn = ONE
    for n in range(1, nhi + 1):
        xn = rnd(mul(xn, x), P)
        if n < nlo: continue
        c = head[n] if n <= 10 else 6 * F(n)
        if c: s = rnd(add(s, mul(q(c), xn)), P)
    return s

def S_full_up(head, x):
    # Lemma 3.30 reading rule: pole test first, then 1 - mu^+ x^+ in the denominator, every other op upward
    mx = up(mul(MU, x), P)
    if not lt(mx, ONE): return None
    s = S_poly(head, x, 4, 48, "up")
    x49 = ONE
    for n in range(49): x49 = up(mul(x49, x), P)
    tail = up(div(mul(q(6 * F(49)), x49), down(sub(ONE, mx), P)), P)
    return up(add(s, tail), P)

ALPHA = q(1, 1 << 22)
# ---- 6. C19 missing_tail: head-only C03 polynomial, pole test removed ----
for k, lim in (("1/40", q(196, 10 ** 9)), ("0.02248", q(128, 10 ** 9))):
    x = xs(EPS[k], ALPHA, QUART, "up")
    s = S_poly(HEADS["C03"], x, 4, 10, "up")
    flag = le(s, lim) and le(s, ALPHA)
    need(flag, "missing_tail_" + k)
    say("MISSING_TAIL|beta=%s|alpha=2^-22|x^+=%s|S_head_only^+=%s|<=%s:%d|<=alpha=%s:%d|faulted_read_MET,honest_read_NOT_MET_by_pole,so_the_C04_guard_fires|tag=MEASURED" % (k, dec(x, 10, "ceil"), dec(s, 12, "ceil"), dec(lim, 9), int(le(s, lim)), dec(ALPHA, 12), int(le(s, ALPHA))))

# ---- 7. variant: missing_tail with the pole test kept, at 0.02076 ----
x = xs(EPS["0.02076"], ALPHA, QUART, "up")
mx = up(mul(MU, x), P)
s = S_poly(HEADS["C03"], x, 4, 10, "up")
flag = lt(mx, ONE) and le(s, q(927, 10 ** 10)) and le(s, ALPHA)
need(flag, "variant_pole_kept_0.02076")
say("VARIANT_POLE_KEPT|beta=0.02076|mu*x^+=%s<1:%d|S_head_only^+=%s<=9.27e-8:%d|so_that_variant_passes_C04_and_misses_later_(C06)|tag=MEASURED" % (dec(mx, 7, "ceil"), int(lt(mx, ONE)), dec(s, 12, "ceil"), int(le(s, q(927, 10 ** 10)))))

# ---- 8. variants that would not fire: NOT_MET proofs for every alpha in [0,1/4] at theta = 1/4 ----
def notmet_proof(head, nlo, nhi, eps):
    # a_0 = 0; a_{i+1} := S^-(x^-(a_i)); S increases in alpha, so S(x(alpha)) >= a_{i+1} > alpha on [a_i, a_{i+1})
    a = ZERO; steps = 0
    while lt(a, QUART) or a == QUART:
        x = xs(eps, a, QUART, "down")
        nxt = S_poly(head, x, nlo, nhi, "down")
        steps += 1
        if not lt(a, nxt): return False, steps, a
        a = nxt
        if steps > 200: return False, steps, a
    return True, steps, a
for k in ("1/40", "0.02248"):
    r1 = notmet_proof(HEADS["crude"], 4, 10, EPS[k])
    r2 = notmet_proof(HEADS["headfree"], 4, 48, EPS[k])
    need(r1[0] and r2[0], "variants_not_fire_" + k)
    say("VARIANTS_NOT_FIRE|beta=%s|crude_head_cut_at_10:NOT_MET_proved=%d(steps=%d)|any_head_cut_at_48(headfree_is_least):NOT_MET_proved=%d(steps=%d)|tag=MEASURED" % (k, int(r1[0]), r1[1], int(r2[0]), r2[1]))

# ---- 9. edge read with the full S (tail and pole test): C03 head at 0.02075 (MET) and 0.02076 (NOT_MET) ----
def g_up(head, eps, alpha):
    x = xs(eps, alpha, QUART, "up")
    s = S_full_up(head, x)
    return None if s is None else sub(s, alpha)
def find_cert(head, eps):
    lo, hi = 0, 1 << 46   # alpha = k / 2^48 in [0, 1/4]
    D = 1 << 48
    for _ in range(90):
        if hi - lo < 3: break
        m1 = lo + (hi - lo) // 3; m2 = hi - (hi - lo) // 3
        g1 = g_up(head, eps, q(m1, D)); g2 = g_up(head, eps, q(m2, D))
        if g1 is None: hi = m1; continue
        if g2 is None: hi = m2; continue
        if lt(g1, g2): hi = m2
        else: lo = m1
    best = None
    for kk in range(lo, hi + 1):
        g = g_up(head, eps, q(kk, D))
        if g is not None and (best is None or lt(g, best[1])): best = (kk, g)
    return best
for k, head in (("0.02075", "C03"), ("0.02075", "headfree")):
    b = find_cert(HEADS[head], EPS[k])
    met = b is not None and le(b[1], ZERO)
    say("EDGE_FULL_S|beta=%s|head=%s|min_g^+_over_dyadic_alpha=%s_at_alpha=%s|C_0_MET:%d|tag=MEASURED" % (k, head, dec(b[1], 14, "ceil") if b else "pole", dec(q(b[0], 1 << 48), 10) if b else "-", int(met)))
for k, head in (("0.02076", "C03"), ("0.02076", "headfree")):
    b = find_cert(HEADS[head], EPS[k])
    met = b is not None and le(b[1], ZERO)
    say("EDGE_FULL_S|beta=%s|head=%s|min_g^+_over_dyadic_alpha=%s|C_0_MET_at_any_dyadic_alpha:%d|(a_MET_read_would_contradict_C06;NOT_MET_needs_the_lower-enclosure_proof_of_the_CERTIFICATES_row)|tag=MEASURED" % (k, head, dec(b[1], 14, "ceil") if b else "pole", int(met)))

say("SUMMARY|tail_step0_all_pass=%d|json=0" % int(ok_all))
open("/mnt/c/tmp/opus55/ym4-04c-gattack/work/L2-sec3-part2/tail_step0.out", "w").write("\n".join(out) + "\n")
sys.exit(0 if ok_all else 1)
