#!/usr/bin/env python3
"""Second-seat scratch checks for the KP lens of G0 (not an engine, not evidence).

Integers and Fractions only, with outward dyadic rounding at P bits. Floats appear only in display.
Route differs from G0-a-kp.py and G0-b-checks.py: alpha_- is bracketed by a monotone lower iteration
and an exact upper certificate; NOT_MET of the admissibility test is certified by convexity
(g(a0) > 0 and g'(a0) < 0 with directed enclosures), not by a search read.
Run: python3 -I G0-kp-checks.py
"""
from fractions import Fraction as Fr
from math import comb
import itertools, sys

P = 320
ONE = Fr(1)
KAPPA = Fr(1, 4)
MU = Fr(20**20, 19**19)


def dn(x):
    x = Fr(x)
    return Fr((x.numerator << P) // x.denominator, 1 << P)


def up(x):
    x = Fr(x)
    return Fr(-((-x.numerator << P) // x.denominator), 1 << P)


def F20(n):
    return comb(20 * n, n) // (19 * n + 1)


FN = {n: F20(n) for n in range(1, 80)}

# ---------- exp enclosures ----------

def exp_enc(y):
    """[lo, hi] with lo <= e^y <= hi, y rational."""
    y = Fr(y)
    neg = y < 0
    t = -y if neg else y
    # Taylor at t >= 0; t <= 8 in every use here
    s = Fr(0); term = Fr(1); j = 0
    while True:
        s += term
        j += 1
        term = term * t / j
        if term < Fr(1, 1 << (P + 40)) and t / (j + 1) < Fr(1, 2):
            lo, hi = s, s + 2 * term
            break
    lo, hi = dn(lo), up(hi)
    if neg:
        return dn(1 / hi), up(1 / lo)
    return lo, hi


# ---------- c_0 and eps_6 ----------

def c0_enc(x):
    x = Fr(x)
    s = Fr(0); m = 0; term = Fr(1)
    q = (x / 2) ** 2
    while True:
        s += term
        nxt = term * q / ((m + 1) * (m + 2))
        m += 1
        term = nxt
        if term < Fr(1, 1 << (P + 60)):
            return dn(s), up(s + 2 * term)


def eps6_enc(beta):
    beta = Fr(beta)
    lo_c, hi_c = c0_enc(beta)
    lo = Fr(0); hi = Fr(0)
    for k in range(7):
        ck = c0_enc(k * beta) if k else (ONE, ONE)
        # q_k = c0(k beta) / c0(beta)^k
        qlo = dn(ck[0] / hi_c ** k)
        qhi = up(ck[1] / lo_c ** k)
        w = comb(6, k) * (-1) ** (6 - k)
        if w > 0:
            lo += w * qlo; hi += w * qhi
        else:
            lo += w * qhi; hi += w * qlo
    assert lo > 0
    # sixth root by bisection
    def root6(v, upper):
        a, b = Fr(0), Fr(1)
        for _ in range(P):
            m = (a + b) / 2
            m = Fr((m.numerator << 0), m.denominator)
            if m ** 6 <= v:
                a = m
            else:
                b = m
        return b if upper else a
    return root6(lo, False), root6(hi, True)


# ---------- the certificate series ----------
HEAD_C03 = {4: 1, 5: 0, 6: 12, 7: 0, 8: 32, 9: 32, 10: 304}
HEAD_FREE = {n: 0 for n in range(4, 11)}
HEAD_CRUDE = {n: 6 * FN[n] for n in range(4, 11)}


def S_exact(x, head):
    x = Fr(x)
    assert MU * x < 1
    s = Fr(0)
    xn = x ** 4
    for n in range(4, 49):
        c = head[n] if n <= 10 else 6 * FN[n]
        s += c * xn
        xn *= x
    s += 6 * FN[49] * xn / (1 - MU * x)  # xn = x^49
    return s


def dS_exact(x, head):
    """x S'(x)."""
    x = Fr(x)
    s = Fr(0)
    for n in range(4, 49):
        c = head[n] if n <= 10 else 6 * FN[n]
        s += c * n * x ** n
    t = 6 * FN[49] * x ** 49
    # d/dx [x^49/(1-mu x)] * x = 49 x^49/(1-mu x) + mu x^50/(1-mu x)^2
    s += t * 49 / (1 - MU * x) + t * MU * x / (1 - MU * x) ** 2
    return s


def x_enc(eps, alpha, theta):
    lo, hi = exp_enc(2 * Fr(alpha) + Fr(theta))
    return dn(eps[0] * lo), up(eps[1] * hi)


def alpha_bracket(eps, head, theta=KAPPA, iters=200):
    """Lower: iterate a <- S^-(x^-(a)) from 0 (monotone, stays below alpha_-).
    Upper: smallest of a few candidates a with S^+(x^+(a)) <= a, checked exactly."""
    a = Fr(0)
    for _ in range(iters):
        xl, _ = x_enc(eps, a, theta)
        if MU * xl >= 1:
            return None
        b = dn(S_exact(xl, head))
        if b <= a:
            break
        if b - a < Fr(1, 1 << (P - 40)):
            a = b
            break
        a = b
        if a > Fr(1, 4):
            return None
    lo = a
    for rel in (Fr(1, 10**12), Fr(1, 10**10), Fr(1, 10**8), Fr(1, 10**6)):
        cand = up(lo * (1 + rel))
        _, xh = x_enc(eps, cand, theta)
        if MU * xh < 1 and up(S_exact(xh, head)) <= cand:
            return lo, cand
    return lo, None


def certify_alpha_minus_above(eps, head, a0, theta=KAPPA):
    """True if alpha_-(theta) > a0 is certified: g(a0) > 0 and g'(a0) < 0, with g convex."""
    xl, xh = x_enc(eps, a0, theta)
    if MU * xh >= 1:
        return False
    g_lo = dn(S_exact(xl, head)) - a0
    dg_hi = 2 * up(dS_exact(xh, head)) - 1
    return g_lo > 0 and dg_hi < 0


# ---------- G1's frozen c(delta), used only to locate delta_crit ----------

def c_enc(delta):
    """[lo, hi] of c(delta) = e^delta [e^{-4kappa} + max_{n>=4}(e^{-(kappa/2-2d')n} - e^{-kappa n/2})]."""
    delta = Fr(delta)
    ed = exp_enc(delta)
    dp_lo, dp_hi = dn(delta * ed[0]), up(delta * ed[1])
    a_lo = KAPPA / 2 - 2 * dp_hi   # smaller decay rate gives the larger first term
    a_hi = KAPPA / 2 - 2 * dp_lo
    best_lo = Fr(0); best_hi = Fr(0)
    for n in range(4, 61):
        t1 = exp_enc(-a_hi * n); t1h = exp_enc(-a_lo * n)
        t2 = exp_enc(-KAPPA * n / 2)
        hlo = t1[0] - t2[1]
        hhi = t1h[1] - t2[0]
        best_lo = max(best_lo, hlo); best_hi = max(best_hi, hhi)
    # h(n) = e^{-a n} - e^{-b n} is unimodal in real n; for n >= 60 it is below e^{-a_lo*60} < best_lo
    assert exp_enc(-a_lo * 60)[1] < best_lo
    e1 = exp_enc(-4 * KAPPA)
    return dn(ed[0] * (e1[0] + best_lo)), up(ed[1] * (e1[1] + best_hi))


def show(x, d=12):
    return f"{float(x):.{d}g}"


def main():
    out = []
    pr = lambda *a: (print(*a), out.append(" ".join(str(t) for t in a)))

    # ===== A. geometry of the test sets on fine (Z/8)^4 =====
    N = 8
    dims = range(4)
    def add(x, mu, s=1):
        y = list(x); y[mu] = (y[mu] + s) % N; return tuple(y)
    def link(x, mu):
        return (x, mu)
    def is_line(l):
        x, mu = l
        return all(x[v] % 2 == 0 for v in dims if v != mu)
    def plaq_links(x, mu, nu):
        return [link(x, mu), link(add(x, mu), nu), link(add(x, nu), mu), link(x, nu)]
    sites = list(itertools.product(range(N), repeat=4))
    plaqs = [(x, mu, nu) for x in sites for mu in dims for nu in dims if mu < nu]
    through = {}
    for p in plaqs:
        for l in plaq_links(*p):
            through.setdefault(l, []).append(p)
    def off(p):
        return [l for l in plaq_links(*p) if not is_line(l)]
    def filling(s, mu, nu):
        # the 4 plaquettes of plane (mu,nu) with corner s
        return [(s, mu, nu), (add(s, mu, -1), mu, nu), (add(s, nu, -1), mu, nu),
                (add(add(s, mu, -1), nu, -1), mu, nu)]
    ok_W = ok_Wp = ok_disj = ok_fill = True
    ncoarse = 0
    for xc in itertools.product(range(0, N, 2), repeat=4):
        for mu in dims:
            ncoarse += 1
            e0 = link(xc, mu)
            m = add(xc, mu)
            e1 = link(m, mu)
            Wp = set()
            for nu in dims:
                if nu != mu:
                    Wp.add(link(m, nu)); Wp.add(link(add(m, nu, -1), nu))
            assert len(Wp) == 6 and all(not is_line(l) for l in Wp)
            P0 = through[e0]; P1 = through[e1]
            W = set(l for p in P0 for l in off(p))
            ok_W &= (len(W) == 12) and all(len(off(p)) == 2 and set(off(p)) <= W for p in P0)
            ok_Wp &= all(len(set(off(p)) & Wp) == 1 for p in P0 + P1)
            pairs = [frozenset(off(p)) for p in P0]
            ok_disj &= all(not (a & b) for a, b in itertools.combinations(pairs, 2))
            # the 6 fillings through l: each holds both positions, exactly 2 links of W, exactly 1 of W'
            for nu in dims:
                if nu == mu:
                    continue
                for s in (+1, -1):
                    ctr = add(m, nu, s)
                    a, b = (mu, nu) if mu < nu else (nu, mu)
                    F = filling(ctr, a, b)
                    links = set(l for p in F for l in plaq_links(*p))
                    offF = set(l for p in F for l in off(p))
                    ok_fill &= (e0 in links and e1 in links and len(offF & W) == 2 and len(offF & Wp) == 1)
    pr("A coarse links on fine 8^4:", ncoarse)
    pr("A #W(e0)=12 and both off links of each plaquette through e0 in W(e0):", ok_W)
    pr("A each of the 12 plaquettes through e0 or e1 has exactly one off link in W'(l) (6 links at m_l):", ok_Wp)
    pr("A the 6 off-link pairs of the plaquettes through e0 are pairwise disjoint:", ok_disj)
    pr("A each filling through l holds e0,e1, exactly 2 links of W(e0) and exactly 1 of W'(l):", ok_fill)

    # ===== B. the factor 2 is exact on the fillings-only gas =====
    # Fillings have pairwise disjoint internal links, so in the gas of fillings alone every cluster is
    # {F^m}, Phi = (-1)^{m-1} z^m / m. With z = 1/1000 at each of the 6 fillings through l:
    z = Fr(1, 1000)
    # sum over clusters through l of |Phi| = 6 * sum_m z^m/m ; the 12-link union bound counts each twice
    M = 60
    true_sum = 6 * sum(z ** m / m for m in range(1, M + 1))
    union12 = 12 * sum(z ** m / m for m in range(1, M + 1))
    pr("B fillings-only gas: union bound over W(e0) / true holding-cluster sum =", union12 / true_sum)

    # ===== C. the KP certificate at the rows G0's tables touch =====
    res = {}
    for beta, name in [(Fr(1, 100), "1/100"), (Fr(1, 64), "1/64"), (Fr(1, 50), "1/50")]:
        eps = eps6_enc(beta)
        pr(f"C beta={name} eps6 in [{show(eps[0], 13)}, {show(eps[1], 13)}]")
        for hname, head in [("crude", HEAD_CRUDE), ("C03", HEAD_C03), ("headfree", HEAD_FREE)]:
            br = alpha_bracket(eps, head)
            if br is None or br[1] is None:
                pr(f"C   {hname}: no certificate")
                continue
            lo, hi = br
            res[(name, hname)] = (lo, hi)
            d12 = (12 * lo, 12 * hi); d6 = (6 * lo, 6 * hi)
            e6 = exp_enc(d6[1])
            c1_6 = up(2 * d6[1] * e6[1])
            e12 = exp_enc(d12[0])
            c1_12 = dn(2 * d12[0] * e12[0])
            pr(f"C   {hname}: alpha_- in [{show(lo)}, {show(hi)}]; 12 alpha in [{show(d12[0])}, {show(d12[1])}];"
               f" 6 alpha in [{show(d6[0])}, {show(d6[1])}]; 2d'(6) <= {show(c1_6, 7)}; 2d'(12) >= {show(c1_12, 7)}")

    # ===== D. delta_crit from G1's frozen c(delta) =====
    a, b = Fr(49, 1000), Fr(50, 1000)
    assert c_enc(a)[1] < 1 and c_enc(b)[0] > 1
    for _ in range(40):
        m = (a + b) / 2
        clo, chi = c_enc(m)
        if chi < 1:
            a = m
        elif clo > 1:
            b = m
        else:
            break
    pr(f"D delta_crit in [{show(a, 12)}, {show(b, 12)}] (c(a)<1<c(b) certified)")
    dc_grid = Fr(int(a * 10**9), 10**9)
    assert c_enc(dc_grid)[1] < 1
    pr(f"D delta_crit^- on the 1e-9 grid = {dc_grid} ; C13 bracket lower end 0.0496174")
    pr(f"D c(49/1000) in [{show(c_enc(Fr(49,1000))[0],7)}, {show(c_enc(Fr(49,1000))[1],7)}];"
       f" c(1/20) in [{show(c_enc(Fr(1,20))[0],7)}, {show(c_enc(Fr(1,20))[1],7)}]")

    # ===== E. the admissibility edges, both factors, both delta_crit^- readings =====
    for factor in (12, 6):
        for hname, head, pair in [("crude", HEAD_CRUDE, (Fr(1369, 100000), Fr(1370, 100000)) if factor == 12 else (Fr(1556, 100000), Fr(1557, 100000))),
                                  ("C03", HEAD_C03, (Fr(1959, 100000), Fr(1960, 100000)) if factor == 12 else (Fr(2029, 100000), Fr(2030, 100000))),
                                  ("headfree", HEAD_FREE, (Fr(1959, 100000), Fr(1960, 100000)) if factor == 12 else (Fr(2029, 100000), Fr(2030, 100000)))]:
            for dcm, dcname in [(Fr(496174, 10**7), "0.0496174"), (dc_grid, "grid")]:
                met_b, not_b = pair
                eps = eps6_enc(met_b)
                br = alpha_bracket(eps, head)
                met = br is not None and br[1] is not None and factor * br[1] < dcm
                eps2 = eps6_enc(not_b)
                notmet = certify_alpha_minus_above(eps2, head, dcm / factor)
                br2 = alpha_bracket(eps2, head)
                v2 = factor * br2[0] if br2 else None
                pr(f"E factor {factor} {hname} dcrit^-={dcname}: MET certified at {float(met_b)}: {met}"
                   f" (factor*alpha <= {show(factor*br[1], 10) if br and br[1] else None});"
                   f" NOT_MET certified at {float(not_b)}: {notmet} (factor*alpha_- >= {show(v2, 10) if v2 else None})")

    with open(__file__.replace(".py", ".out"), "w") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
