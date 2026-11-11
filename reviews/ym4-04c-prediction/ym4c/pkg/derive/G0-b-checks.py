#!/usr/bin/env python3
"""Scratch checks for note section 3, route B (Theorem G0). Integers and Fractions only.

Not an engine and not evidence. Each block checks one fact the written proof derives:
A Fuss-Catalan values, mu, and the product formula for F(n+1)/F(n);
B a rational lower bound on pi and 8/(3 pi) <= 8489/10000;
C local geometry of the b = 2 lines on fine (Z/8)^4;
D the closed sets holding the boundary of one coarse plaquette, up to 8 plaquettes;
E connected sets through one off link, n <= 4, against 6 F_20(n);
F the crude certificate at beta = 1/100 and 1/64, theta = 1/4: brackets on the least root.
"""
import itertools
import sys
from fractions import Fraction as Fr
from math import comb, factorial

OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s, flush=True)


# ---------------- A: Fuss-Catalan ----------------
def F(n, D=20):
    return comb(D * n, n) // ((D - 1) * n + 1)


MU = Fr(20**20, 19**19)
draft = [20540, 784245, 31763004, 1340246340, 58281448940, 2593593086150,
         117544525178080, 5406686759963586, 251754316822792420]
say("A F_20(4..12) equal to draft:", [F(n) for n in range(4, 13)] == draft)
say("A mu in [53.00068,53.00069]:", Fr(5300068, 100000) <= MU <= Fr(5300069, 100000))
ok_formula = True
ok_mono = True
ok_below = True
prev = None
for n in range(0, 121):
    r = Fr(F(n + 1), F(n))
    prod = Fr(20)
    for j in range(1, 20):
        prod *= Fr(20 * n + j, 19 * n + j + 1)
    ok_formula &= (r == prod)
    ok_below &= (r < MU)
    if prev is not None:
        ok_mono &= (prev < r)
    prev = r
say("A F(n+1)/F(n) = 20 prod_{j=1..19}(20n+j)/(19n+j+1) for n=0..120:", ok_formula)
say("A strictly increasing n=0..120:", ok_mono, "; below mu:", ok_below)
say("A F(1),F(2),F(3) =", F(1), F(2), F(3))

# ---------------- B: pi ----------------
def atan_lower(x, terms):
    # alternating series, truncated after an odd number of terms ending with a minus: lower bound
    s = Fr(0)
    for k in range(terms):
        s += Fr((-1) ** k) * x ** (2 * k + 1) / (2 * k + 1)
    return s


def atan_upper(x, terms):
    s = Fr(0)
    for k in range(terms):
        s += Fr((-1) ** k) * x ** (2 * k + 1) / (2 * k + 1)
    return s


# Machin: pi = 16 atan(1/5) - 4 atan(1/239). An even number of terms of the alternating series
# for atan is a lower bound; an odd number an upper bound (0 < x < 1, terms decreasing).
pi_lo = 16 * atan_lower(Fr(1, 5), 4) - 4 * atan_upper(Fr(1, 239), 1)
pi_hi = 16 * atan_upper(Fr(1, 5), 5) - 4 * atan_lower(Fr(1, 239), 2)
say("B pi in [%s, %s] (decimal %.9f, %.9f)" % (pi_lo, pi_hi, float(pi_lo), float(pi_hi)))
say("B 8/(3 pi_lo) <= 8489/10000:", Fr(8) / (3 * pi_lo) <= Fr(8489, 10000),
    " 8/(3 pi) in [%.7f, %.7f]" % (float(Fr(8) / (3 * pi_hi)), float(Fr(8) / (3 * pi_lo))))

# ---------------- C: local geometry on fine (Z/8)^4 ----------------
L = 8
d = 4


def add(x, mu, s=1):
    y = list(x)
    y[mu] = (y[mu] + s) % L
    return tuple(y)


def is_line(link):
    x, mu = link
    return all(x[n] % 2 == 0 for n in range(d) if n != mu)


def cls(link):
    x, mu = link
    return sum(1 for n in range(d) if n != mu and x[n] % 2 == 1)


sites = list(itertools.product(range(L), repeat=d))
plaqs = []
for x in sites:
    for mu in range(d):
        for nu in range(mu + 1, d):
            plaqs.append((x, mu, nu, ((x, mu), (add(x, mu), nu), (add(x, nu), mu), (x, nu))))
P_links = [p[3] for p in plaqs]
link_to_p = {}
for i, ls in enumerate(P_links):
    for l in ls:
        link_to_p.setdefault(l, []).append(i)
offl = [tuple(l for l in ls if not is_line(l)) for ls in P_links]
say("C plaquettes", len(plaqs), "links", len(link_to_p),
    "every link in 6 plaquettes:", all(len(v) == 6 for v in link_to_p.values()))
say("C off links per plaquette:", sorted(set(len(o) for o in offl)))
# off-link neighbours
nbr = []
for i in range(len(plaqs)):
    s = set()
    for l in offl[i]:
        for j in link_to_p[l]:
            if j != i:
                s.add(j)
    nbr.append(s)
say("C off-link degree max", max(len(s) for s in nbr), "min", min(len(s) for s in nbr))
# distinct plaquettes share at most one link
share_ok = True
for i in range(len(plaqs)):
    for j in nbr[i]:
        if len(set(P_links[i]) & set(P_links[j])) > 1:
            share_ok = False
say("C two distinct off-link neighbours share exactly one link:", share_ok)
from collections import Counter
say("C link classes (0 = line):", sorted(Counter(cls(l) for l in link_to_p).items()))
# plaquette types: line plaquettes have off links of class 1 only; type A: two class-1, two class-2;
# type B: two class-2, two class-3
types = Counter()
for i in range(len(plaqs)):
    types[tuple(sorted(cls(l) for l in P_links[i]))] += 1
say("C plaquette link-class patterns:", sorted(types.items()))


def center_of_line_plaquette(i):
    # the unique corner with exactly two odd coordinates
    x, mu, nu, _ = plaqs[i]
    corners = [x, add(x, mu), add(x, nu), add(add(x, mu), nu)]
    c2 = [c for c in corners if sum(v % 2 for v in c) == 2]
    return c2


line_plaqs = [i for i in range(len(plaqs)) if len(offl[i]) == 2]
okc = True
for i in line_plaqs:
    c2 = center_of_line_plaquette(i)
    if len(c2) != 1:
        okc = False
        continue
    c = c2[0]
    for l in offl[i]:
        a, mu = l
        if not (a == c or add(a, mu) == c):
            okc = False
say("C each line plaquette has one corner with two odd coordinates, and both its off links end there:", okc)
# fillings: the 4 line plaquettes around a centre c in the plane of c's odd directions
fillings = {}
for i in line_plaqs:
    c = center_of_line_plaquette(i)[0]
    fillings.setdefault(c, []).append(i)
say("C fillings: count", len(fillings), "each of 4 plaquettes:", all(len(v) == 4 for v in fillings.values()))
in_fill = Counter()
for c, ps in fillings.items():
    for l in set(l for i in ps for l in offl[i]):
        in_fill[l] += 1
say("C off links by number of fillings holding them, per class:",
    sorted(Counter((cls(l), in_fill[l]) for l in link_to_p if not is_line(l)).items()))
# W(e0) for every line link
wsz = set()
mult_ok = True
fill_split_ok = True
for l, ps in link_to_p.items():
    if not is_line(l):
        continue
    W = set()
    for i in ps:
        W.update(offl[i])
        if len(offl[i]) != 2:
            mult_ok = False
    wsz.add(len(W))
    # each W link in exactly one filling through the coarse link of l, each such filling holds 2
    cs = [center_of_line_plaquette(i)[0] for i in ps]
    hold = Counter()
    for c in cs:
        fl = set(m for j in fillings[c] for m in offl[j])
        hold[c] = len(fl & W)
    if sorted(hold.values()) != [2] * 6:
        fill_split_ok = False
say("C |W(e0)| over all line links:", sorted(wsz),
    "; each plaquette through e0 has 2 off links, both in W(e0):", mult_ok)
say("C the 6 fillings through the coarse link each hold exactly 2 links of W(e0):", fill_split_ok)

# ---------------- D: closed sets holding dP, up to 8 plaquettes ----------------
pidx = {(p[0], p[1], p[2]): i for i, p in enumerate(plaqs)}
O = (0, 0, 0, 0)
mu0, nu0 = 0, 1
# coarse plaquette P at coarse site 0 in plane (0,1); its 4 coarse links and their 8 line links
def coarse_link_positions(xc, m):
    x0 = tuple(2 * v % L for v in xc)
    return [(x0, m), (add(x0, m), m)]


dP = [((0, 0, 0, 0), mu0), ((0, 0, 0, 0), nu0), ((0, 1, 0, 0), mu0), ((1, 0, 0, 0), nu0)]
dP_line = [pos for (xc, m) in dP for pos in coarse_link_positions(xc, m)]
FP = set(fillings[(1, 1, 0, 0)])
seeds = link_to_p[((0, 0, 0, 0), mu0)]
NMAX = 8


def Ypp(S):
    held = set(l for i in S for l in P_links[i] if is_line(l))
    return held


found = {}
seen = set()
stack = [frozenset([s]) for s in seeds]
states = 0
while stack:
    S = stack.pop()
    if S in seen:
        continue
    seen.add(S)
    states += 1
    cnt = Counter(l for i in S for l in offl[i])
    open_ = sorted(l for l, c in cnt.items() if c == 1)
    if len(open_) > 4 * (NMAX - len(S)):
        continue
    if not open_:
        found[S] = True
        if len(S) < NMAX:
            for l in cnt:
                for q in link_to_p[l]:
                    if q not in S:
                        stack.append(S | {q})
        continue
    if len(S) >= NMAX:
        continue
    e = open_[0]
    for q in link_to_p[e]:
        if q not in S:
            stack.append(S | {q})
hold_dP = Counter()
holders8 = []
for S in found:
    h = Ypp(S)
    if all(l in h for l in dP_line):
        hold_dP[len(S)] += 1
        if len(S) == 8:
            holders8.append(S)
say("D search states", states, "; closed sets through a plaquette of e0, up to 8:", len(found))
say("D closed sets holding all 8 line links of dP, by size:", sorted(hold_dP.items()))
say("D the size-4 one is F_P:", any(set(S) == FP for S in found if len(S) == 4 and all(l in Ypp(S) for l in dP_line)))
# how many quadrants of F_P each size-8 holder keeps
say("D size-8 holders by number of F_P quadrants kept:", sorted(Counter(len(set(S) & FP) for S in holders8).items()))

# ---------------- E: connected sets through one off link, n <= 4 ----------------
def connected_sets_through(link, nmax):
    roots = link_to_p[link]
    res = Counter()
    seenE = set()
    frontier = [frozenset([r]) for r in roots]
    for S in frontier:
        seenE.add(S)
    level = frontier
    res[1] = len(level)
    for n in range(2, nmax + 1):
        nxt = set()
        for S in level:
            for i in S:
                for q in nbr[i]:
                    if q not in S:
                        T = S | {q}
                        if T not in seenE:
                            nxt.add(T)
        seenE.update(nxt)
        level = list(nxt)
        res[n] = len(level)
    return res


for c in (1, 2, 3):
    l = next(l for l in link_to_p if not is_line(l) and cls(l) == c)
    r = connected_sets_through(l, 4)
    say("E class", c, "connected sets through the link, n=1..4:", [r[n] for n in range(1, 5)],
        "; 6F_20(n):", [6 * F(n) for n in range(1, 5)],
        "; all below:", all(r[n] <= 6 * F(n) for n in range(1, 5)))

# ---------------- F: crude certificate at theta = 1/4 ----------------
def c0_bounds(x, M=40):
    x = Fr(x)
    q = (x / 2) ** 2
    s = Fr(0)
    t = Fr(1)
    for m in range(M):
        s += t
        t = t * q / ((m + 1) * (m + 2))
    # remaining terms: t, t*q/((M+1)(M+2)), ... ratio <= q/((M+1)(M+2)) < 1/2
    return s, s + 2 * t


def exp_bounds(y, M=60):
    y = Fr(y)
    assert 0 <= y < 1
    s = Fr(0)
    t = Fr(1)
    for k in range(M):
        s += t
        t = t * y / (k + 1)
    return s, s + 2 * t


def dyadic_down(v, bits=200):
    return Fr((v.numerator << bits) // v.denominator, 1 << bits)


def dyadic_up(v, bits=200):
    return Fr(-((-v.numerator << bits) // v.denominator), 1 << bits)


def eps6_bracket(beta):
    beta = Fr(beta)
    lo = Fr(0)
    hi = Fr(0)
    cb = c0_bounds(beta)
    for k in range(7):
        ck = c0_bounds(k * beta) if k else (Fr(1), Fr(1))
        coef = comb(6, k) * (-1) ** (6 - k)
        tlo = ck[0] / cb[1] ** k
        thi = ck[1] / cb[0] ** k
        if coef > 0:
            lo += coef * tlo
            hi += coef * thi
        else:
            lo += coef * thi
            hi += coef * tlo
    lo, hi = dyadic_down(lo), dyadic_up(hi)
    # sixth roots by bisection on dyadics
    def root(v, up):
        a, b = Fr(0), Fr(1)
        for _ in range(140):
            m = (a + b) / 2
            if m ** 6 <= v:
                a = m
            else:
                b = m
        return b if up else a
    return root(lo, False), root(hi, True)


def S_crude(x):
    s = Fr(0)
    for n in range(4, 49):
        s += 6 * F(n) * x ** n
    assert MU * x < 1
    return s + 6 * F(49) * x ** 49 / (1 - MU * x)


def least_root_bracket(beta, theta=Fr(1, 4)):
    elo, ehi = eps6_bracket(beta)
    # lower bound: monotone iteration from 0 with lower-rounded data
    a = Fr(0)
    for _ in range(14):
        x = dyadic_down(elo * exp_bounds(2 * a + theta)[0])
        a = dyadic_down(S_crude(x))
    alo = a
    # upper bound: a value with S(x_hi) <= a, found from the lower iterate plus a small step
    step = Fr(1, 10**12)
    ahi = alo
    while True:
        ahi = ahi + step
        x = dyadic_up(ehi * exp_bounds(2 * ahi + theta)[1])
        if S_crude(x) <= ahi:
            break
        step *= 2
    return (elo, ehi), alo, ahi


for beta, lab, br in ((Fr(1, 100), "C07", (Fr(11044, 10**6), Fr(11045, 10**6))),
                      (Fr(1, 64), "C11", (Fr(10165, 10**5), Fr(10166, 10**5)))):
    (elo, ehi), alo, ahi = least_root_bracket(beta)
    say("F beta=%s eps6 in [%.12e, %.12e]" % (beta, float(elo), float(ehi)))
    say("F beta=%s least root alpha_- in [%.10e, %.10e]" % (beta, float(alo), float(ahi)))
    say("F %s draft 12*alpha_- inside [%s, %s]:" % (lab, float(br[0]), float(br[1])),
        br[0] <= 12 * alo and 12 * ahi <= br[1],
        "; proved 6*alpha_- in [%.10f, %.10f]" % (float(6 * alo), float(6 * ahi)))
    d = 6 * ahi
    ehi_d = exp_bounds(d)[1]
    say("F %s proved 2*delta_1*e^delta_1 <= %.6f (draft 12-form: %.6f); 1/8 = 0.125"
        % (lab, float(2 * d * ehi_d), float(2 * (12 * ahi) * exp_bounds(12 * ahi)[1])))

with open(__file__.replace(".py", ".out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")


# ---------------- G: consequences of the factor 2 (scratch; conditional on G1 as drafted) ----------------
# delta_1(proved) = 6 alpha_-(theta=1/4); admissible iff C_0 MET and 6 alpha_- < delta_crit^- .
# delta_crit^- := 496174/10^7, the lower end of the draft's C13 bracket (a G1 quantity, not rechecked here).
DCRIT_LO = Fr(496174, 10**7)
HEADS = {"crude": {n: 6 * F(n) for n in range(4, 11)},
         "headfree": {n: 0 for n in range(4, 11)},
         "C03": {4: 1, 5: 0, 6: 12, 7: 0, 8: 32, 9: 32, 10: 304}}


def S_head(x, head):
    s = Fr(0)
    for n in range(4, 11):
        s += head[n] * x ** n
    for n in range(11, 49):
        s += 6 * F(n) * x ** n
    if MU * x >= 1:
        return None
    return s + 6 * F(49) * x ** 49 / (1 - MU * x)


def admissible(beta, head, factor=6, theta=Fr(1, 4), cap=None):
    """True/False: C_0 MET with factor*alpha_- < DCRIT_LO, decided with exact brackets."""
    cap = DCRIT_LO / factor if cap is None else cap
    elo, ehi = eps6_bracket(beta)
    a = Fr(0)
    for _ in range(400):
        x = dyadic_down(elo * exp_bounds(2 * a + theta)[0])
        s = S_head(x, head)
        if s is None:
            return False, a
        s = dyadic_down(s)
        if s >= cap:
            return False, s
        if s - a < Fr(1, 10**30):
            a = s
            break
        a = s
    ahi = a + Fr(1, 10**25)
    x = dyadic_up(ehi * exp_bounds(2 * ahi + theta)[1])
    s = S_head(x, head)
    if s is not None and s <= ahi and ahi < cap:
        return True, ahi
    raise RuntimeError("undecided at beta=%s" % beta)


def edge(head, lo, hi, factor=6):
    # lo admissible, hi not; integers in units of 10^-5
    assert admissible(Fr(lo, 10**5), head, factor)[0] and not admissible(Fr(hi, 10**5), head, factor)[0]
    while hi - lo > 1:
        m = (lo + hi) // 2
        if admissible(Fr(m, 10**5), head, factor)[0]:
            lo = m
        else:
            hi = m
    return lo, hi


# reproduce the draft's edges with factor 12, then read them with factor 6
for name, lo, hi in (("crude", 1300, 1500), ("C03", 1900, 2000)):
    e12 = edge(HEADS[name], lo, hi, factor=12)
    say("G %s self-map edge with the draft's factor 12: MET at %.5f, NOT_MET at %.5f" % (name, e12[0] / 1e5, e12[1] / 1e5))
for name, lo, hi in (("crude", 1369, 1563), ("C03", 1959, 2076), ("headfree", 1959, 2076)):
    try:
        e6 = edge(HEADS[name], lo, hi, factor=6)
        say("G %s self-map edge with the proved factor 6: MET at %.5f, NOT_MET at %.5f" % (name, e6[0] / 1e5, e6[1] / 1e5))
    except AssertionError:
        say("G %s: the bracket [%s, %s] does not straddle the factor-6 edge" % (name, lo, hi))
for name in ("headfree", "C03"):
    ok, a = admissible(Fr(1, 50), HEADS[name], 6)
    (elo, ehi), = [eps6_bracket(Fr(1, 50))]
    say("G beta=1/50 %s: factor-6 admissible %s; 6*alpha_- <= %.8f" % (name, ok, float(6 * a)))

with open(__file__.replace(".py", ".out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
