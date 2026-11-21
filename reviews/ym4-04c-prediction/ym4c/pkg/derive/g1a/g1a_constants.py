#!/usr/bin/env python3
"""Scratch arithmetic for G1-a.md (not an engine, not evidence).

Exact rationals with outward rounding of exp to 2^-200. Floats only to choose a scan length and
for display. Computes the frozen c(delta) and the proved c_star(delta) of G1-a.md section 4.9,
their enclosures at the deltas the draft rows quote, delta_crit for both, and the C16 product.
"""
from fractions import Fraction as Fr
import math
import sys

KAP = Fr(1, 4)
PREC = 200  # outward rounding grid 2^-PREC


def _floor(x):
    return Fr(math.floor(x * 2**PREC), 2**PREC)


def _ceil(x):
    return Fr(math.ceil(x * 2**PREC), 2**PREC)


def _exp_series(y):
    """[lo, hi] for e^y, 0 <= y <= 1/2, Taylor with a geometric remainder."""
    s = Fr(0); t = Fr(1); j = 0
    while True:
        s += t
        j += 1
        t = t * y / j
        if t < Fr(1, 2**(PREC + 30)):
            # remainder sum_{i>=j} y^i/i! <= t / (1 - y/(j+1))
            return s, s + t / (1 - y / (j + 1))


def exp_enc(y):
    """[lo, hi] for e^y, y rational of either sign; range reduction by halving."""
    y = Fr(y)
    neg = y < 0
    a = -y if neg else y
    k = 0
    while a > Fr(1, 2):
        a /= 2
        k += 1
    lo, hi = _exp_series(a)
    for _ in range(k):
        lo, hi = _floor(lo * lo), _ceil(hi * hi)
    if neg:
        lo, hi = _floor(1 / hi), _ceil(1 / lo)
    return _floor(lo), _ceil(hi)


def elo(y):
    return exp_enc(y)[0]


def ehi(y):
    return exp_enc(y)[1]


def dprime(d):
    return d * elo(d), d * ehi(d)


def unimodal_max(r_lo, r_hi, rate, nmin, upper):
    """max over integers n >= nmin of e^{-r n} - e^{-rate n}, over r in [r_lo, r_hi] (0 < r < rate).
    upper=True: an upper enclosure (r = r_lo side); else a lower one (r = r_hi side).
    The real maximiser n*(r) = ln(rate/r)/(rate - r) decreases in r; the scan stops at an N
    certified to satisfy e^{(rate - r_lo) N} >= rate / r_lo, so N >= n*(r) for every r in range."""
    nstar = math.log(float(rate / r_lo)) / float(rate - r_lo)
    N = max(nmin + 1, int(math.ceil(nstar)) + 2)
    while elo((rate - r_lo) * N) < rate / r_lo:
        N += 1
    best = None
    for n in range(nmin, N + 1):
        if upper:
            v = ehi(-r_lo * n) - elo(-rate * n)
        else:
            v = elo(-r_hi * n) - ehi(-rate * n)
        if best is None or v > best[0]:
            best = (v, n)
    return best


def c_frozen(d, upper=True):
    """Frozen: e^d [e^{-4k} + max_{n>=4}(e^{-(k/2 - 2d')n} - e^{-k n/2})], defined while 2d' < k/2."""
    dlo, dhi = dprime(d)
    r_lo, r_hi = KAP / 2 - 2 * dhi, KAP / 2 - 2 * dlo
    if r_lo <= 0:
        return None
    m, n = unimodal_max(r_lo, r_hi, KAP / 2, 4, upper)
    if upper:
        return ehi(d) * (ehi(-4 * KAP) + m), n
    return elo(d) * (elo(-4 * KAP) + m), n


def c_star(d, upper=True):
    """Proved (G1-a 4.9): max{ e^{-4k}, e^d * max( e^{-5k + 2d'}, max_{f>=4}(e^{-(k - 2d')f} - e^{-k f}) ) },
    defined while 2d' < k."""
    dlo, dhi = dprime(d)
    r_lo, r_hi = KAP - 2 * dhi, KAP - 2 * dlo
    if r_lo <= 0:
        return None
    m, f = unimodal_max(r_lo, r_hi, KAP, 4, upper)
    if upper:
        inner = max(ehi(-5 * KAP + 2 * dhi), m)
        return max(ehi(-4 * KAP), ehi(d) * inner), f
    inner = max(elo(-5 * KAP + 2 * dlo), m)
    return max(elo(-4 * KAP), elo(d) * inner), f


def show(x, k=10):
    return f"{float(x):.{k}g}"


def crit(cfun, cond_rate, lo, hi, den=10**9):
    """Largest j/den with the condition 2d' < cond_rate certified and c^+ < 1, and the next point,
    where c^- >= 1 or the condition fails (bisection only locates; the pair is read exactly)."""
    def ok(j):
        d = Fr(j, den)
        if 2 * dprime(d)[1] >= cond_rate:
            return False
        c = cfun(d, True)
        return c is not None and c[0] < 1

    def bad(j):
        d = Fr(j, den)
        if 2 * dprime(d)[0] >= cond_rate:
            return True
        c = cfun(d, False)
        return c is not None and c[0] >= 1
    assert ok(lo) and not ok(hi)
    while hi - lo > 1:
        m = (lo + hi) // 2
        if ok(m):
            lo = m
        else:
            hi = m
    return Fr(lo, den), Fr(hi, den), bad(hi)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "pts"
    if what == "pts":
        pts = [
            ("C07 delta_1 lo", Fr(11044, 10**6)), ("C07 delta_1 hi", Fr(11045, 10**6)),
            ("C07 delta_1 crit-read", Fr(110444507, 10**10)),
            ("C08 delta_1 lo", Fr(942, 10**8)), ("C08 delta_1 hi", Fr(945, 10**8)),
            ("C10b s=1/2000 lo", Fr(26890, 10**6)), ("C10b s=1/2000 hi", Fr(26891, 10**6)),
            ("C10b s=1/4096 lo", Fr(13129, 10**6)), ("C10b s=1/4096 hi", Fr(13131, 10**6)),
            ("C13 49/1000", Fr(49, 1000)), ("C13 1/20", Fr(1, 20)),
            ("C13 delta_1 at 0.01369 hi", Fr(49603, 10**6)), ("C13 delta_1 at 0.01370 lo", Fr(49788, 10**6)),
            ("C14 delta_1 at 0.01959 hi", Fr(49383, 10**6)),
            ("C14 1/64 refined lo", Fr(20347, 10**7)), ("C14 1/64 refined hi", Fr(20348, 10**7)),
            ("C12 head-free lo", Fr(72645, 10**6)), ("C12 head-free hi", Fr(72646, 10**6)),
            ("C11 crude lo", Fr(10165, 10**5)), ("C11 crude hi", Fr(10166, 10**5)),
        ]
        for name, d in pts:
            dl, dh = dprime(d)
            cf_hi = c_frozen(d, True); cf_lo = c_frozen(d, False)
            cs_hi = c_star(d, True); cs_lo = c_star(d, False)
            cf = "undefined(2d'>=k/2)" if cf_hi is None else f"[{show(cf_lo[0])},{show(cf_hi[0])}] n*={cf_hi[1]}"
            cs = "undefined(2d'>=k)" if cs_hi is None else f"[{show(cs_lo[0])},{show(cs_hi[0])}] f*={cs_hi[1]}"
            print(f"{name}: delta={show(d)} 2d' in [{show(2*dl)},{show(2*dh)}] "
                  f"frozenC_k(2d'<=1/8)={2*dh <= Fr(1,8)} provedC_k(2d'<=1/4)={2*dh <= Fr(1,4)} "
                  f"c_frozen={cf} c_star={cs}")
    elif what == "chain":
        # C07 / C08 / C16 / C14 chains with both constants, at the upper end of each delta_1 bracket
        for name, d1 in (("C07 crude 1/100", Fr(11045, 10**6)), ("C08 refined 1/100", Fr(945, 10**8)),
                         ("C14 refined 1/64", Fr(20348, 10**7))):
            for lab, cf in (("frozen", c_frozen), ("proved", c_star)):
                c = cf(d1, True)[0]
                d2 = c * d1
                tot = d1 / (1 - c)
                d20 = c**19 * d1
                osc = 512 * ehi(-1) * d20
                print(f"{name} [{lab}]: c(delta_1)<={show(c)} delta_2<={show(d2)} sum<={show(tot)} "
                      f"delta_20<={show(d20)} osc_20<={show(osc)}")
    elif what == "crit":
        lo, hi, b = crit(c_frozen, KAP / 2, 49000000, 50000000)
        print(f"frozen delta_crit: certified < 1 at {lo}, not at {hi} (c^- >= 1 or C_k fails there: {b})")
        lo, hi, b = crit(c_star, KAP, 60000000, 125000000)
        print(f"proved delta_crit*: certified < 1 at {lo}, not at {hi} (c^- >= 1 or condition fails there: {b})")
        d = lo
        print("at delta_crit*-:", "2d'=", show(2 * dprime(d)[1]), "c*=", show(c_star(d, True)[0]),
              "f*=", c_star(d, True)[1], "e^d e^{-5k+2d'}=", show(ehi(d) * ehi(-5 * KAP + 2 * dprime(d)[1])))
    elif what == "split":
        # where c_star leaves e^{-4k}: first delta on 10^-6 grid with e^d * inner > e^{-4k}
        lo, hi = 1, 120000
        def above(j):
            d = Fr(j, 10**6)
            dl, dh = dprime(d)
            m, f = unimodal_max(KAP - 2 * dh, KAP - 2 * dl, KAP, 4, True)
            return ehi(d) * max(ehi(-5 * KAP + 2 * dh), m) > elo(-4 * KAP)
        while hi - lo > 1:
            m = (lo + hi) // 2
            if above(m):
                hi = m
            else:
                lo = m
        print(f"c_star = e^-1 exactly (upper enclosure not above e^-1) for delta <= {lo}e-6; above from {hi}e-6")
        d = Fr(hi, 10**6)
        dl, dh = dprime(d)
        m, f = unimodal_max(KAP - 2 * dh, KAP - 2 * dl, KAP, 4, True)
        print("  there: e^d e^{-5k+2d'}=", show(ehi(d) * ehi(-5 * KAP + 2 * dh)), " e^d max_f g=", show(ehi(d) * m), "f=", f)


def extra():
    # C10b: projection lower bound [4.00e-7, 4.01e-7] against c * delta_in at s = 1/2000
    plo, phi = Fr(400, 10**9), Fr(401, 10**9)
    dlo, dhi = Fr(26890, 10**6), Fr(26891, 10**6)
    for lab, cf in (("frozen", c_frozen), ("proved", c_star)):
        lo = plo / (cf(dhi, True)[0] * dhi)
        hi = phi / (cf(dlo, False)[0] * dlo)
        print(f"C10b projection/(c*delta_in) [{lab}]: [{show(lo)},{show(hi)}]  slack 1/ratio in [{show(1/hi)},{show(1/lo)}]")
    # the proved condition 2 d e^d <= 1/4: its edge on the 10^-9 grid
    lo, hi = 100000000, 120000000
    while hi - lo > 1:
        m = (lo + hi) // 2
        if 2 * dprime(Fr(m, 10**9))[1] <= KAP:
            lo = m
        else:
            hi = m
    print(f"proved condition 2d'<=1/4: holds at {lo}e-9, fails at {hi}e-9 (lower side read)")
    lo, hi = 50000000, 70000000
    while hi - lo > 1:
        m = (lo + hi) // 2
        if 2 * dprime(Fr(m, 10**9))[1] <= KAP / 2:
            lo = m
        else:
            hi = m
    print(f"frozen condition 2d'<=1/8: holds at {lo}e-9, fails at {hi}e-9")
    # e^{-1} enclosure
    print("e^{-1} in", show(elo(-1), 12), show(ehi(-1), 12))
    # c_star and c_frozen at small delta, and their difference
    for d in (Fr(1, 10**4), Fr(1, 10**3), Fr(1, 100), Fr(5, 100), Fr(7, 100), Fr(8, 100), Fr(9, 100), Fr(10, 100), Fr(109, 1000)):
        cf = c_frozen(d, True)
        cs = c_star(d, True)
        print(f"delta={show(d)}: c_frozen^+={'undef' if cf is None else show(cf[0])} c_star^+={show(cs[0])} (f*={cs[1]})")


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "extra":
    extra()
