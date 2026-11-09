#!/usr/bin/env python3
"""Scratch sanity checks for G0-a.md (not an engine, not evidence). Integers and Fractions only.

Part 1: Fuss-Catalan values, mu, the ratio monotonicity (cross-check of the all-n proof), pi lower bound.
Part 2: b = 2 geometry on fine (Z/8)^4: link classes, quarters, fillings, the midpoint test set W'(l).
Part 3: closed sets of at most 8 plaquettes holding all 8 line links of a coarse boundary dP.
"""
from fractions import Fraction as Fr
from itertools import combinations
from math import comb
import sys

D = 20


def F(n):
    return comb(D * n, n) // ((D - 1) * n + 1)


def part1():
    mu = Fr(D**D, (D - 1) ** (D - 1))
    print("F_20(4..12)", [F(n) for n in range(4, 13)])
    assert all(comb(D * n, n) % ((D - 1) * n + 1) == 0 for n in range(1, 400))
    lo, hi = Fr(5300068, 100000), Fr(5300069, 100000)
    print("mu in [53.00068,53.00069]:", lo <= mu <= hi)
    r = [Fr(F(n + 1), F(n)) for n in range(0, 400)]
    print("ratio strictly increasing n=0..399:", all(r[i] < r[i + 1] for i in range(len(r) - 1)),
          "all < mu:", all(x < mu for x in r))
    # pi > lower bound from Machin: pi = 16 atan(1/5) - 4 atan(1/239); atan partial sums alternate
    def atan_lo(x, terms):  # odd number of terms after the first -> lower bound when ending on a minus
        s = Fr(0)
        for k in range(terms):
            s += Fr((-1) ** k, 2 * k + 1) * x ** (2 * k + 1)
        return s
    def atan_hi(x, terms):
        return atan_lo(x, terms)
    # atan(x) partial sums: even count of terms -> lower bound; odd count -> upper bound (0<x<1)
    pi_lo = 16 * atan_lo(Fr(1, 5), 10) - 4 * atan_hi(Fr(1, 239), 9)
    print("pi_lo > 333/106:", pi_lo > Fr(333, 106), " 8/(3*pi_lo) <= 8489/10000:", Fr(8, 3) / pi_lo <= Fr(8489, 10000))
    print("848/999 < 8489/10000:", Fr(848, 999) < Fr(8489, 10000))


L = 8
DIM = 4


def sid(x):
    i = 0
    for c in x:
        i = i * L + (c % L)
    return i


def norm(x):
    return tuple(c % L for c in x)


def odd(x):
    return frozenset(i for i in range(DIM) if x[i] % 2)


def part2():
    sites = [norm((a, b, c, d)) for a in range(L) for b in range(L) for c in range(L) for d in range(L)]
    def lk(x, mu):
        return (norm(x), mu)
    def cls(l):
        x, mu = l
        return len(odd(x) - {mu})
    plaqs = []
    for x in sites:
        for mu, nu in combinations(range(DIM), 2):
            xm = list(x); xm[mu] += 1
            xn = list(x); xn[nu] += 1
            ls = [lk(x, mu), lk(xm, nu), lk(xn, mu), lk(x, nu)]
            plaqs.append((x, mu, nu, ls))
    lp = {}
    for i, (_, _, _, ls) in enumerate(plaqs):
        for l in ls:
            lp.setdefault(l, []).append(i)
    print("links", len(lp), "every link in 6 plaquettes:", all(len(v) == 6 for v in lp.values()))
    share = all(len(set(plaqs[i][3]) & set(plaqs[j][3])) <= 1
                for v in lp.values() for i, j in combinations(v, 2))
    print("two distinct plaquettes share at most one link (pairs through a common link):", share)
    ok_T = True; quarters = []
    for i, (x, mu, nu, ls) in enumerate(plaqs):
        T = odd(x) - {mu, nu}
        cl = sorted(cls(l) for l in ls)
        if not T:
            ok_T &= cl == [0, 0, 1, 1]
            quarters.append(i)
        else:
            t = len(T); ok_T &= cl == [t, t, t + 1, t + 1]
    print("plaquette link classes {0,0,1,1} if T empty, else {t,t,t+1,t+1}:", ok_T)
    # fillings: center s with odd(s) = {mu,nu}; its 4 quarters; internal links
    fill_of = {}
    for i in quarters:
        x, mu, nu, ls = plaqs[i]
        offl = [l for l in ls if cls(l) == 1]
        # the corner where both off links meet
        ends = [set([l[0], norm(tuple(l[0][k] + (1 if k == l[1] else 0) for k in range(DIM)))]) for l in offl]
        s = (ends[0] & ends[1]).pop()
        ok = odd(s) == frozenset({mu, nu})
        if not ok:
            print("quarter corner parity FAIL"); sys.exit(1)
        fill_of.setdefault((s, mu, nu), []).append(i)
    print("fillings", len(fill_of), "each with 4 quarters:", all(len(v) == 4 for v in fill_of.values()))
    internal = {}
    for key, qs in fill_of.items():
        for i in qs:
            for l in plaqs[i][3]:
                if cls(l) == 1:
                    internal.setdefault(l, set()).add(key)
    c1 = [l for l in lp if cls(l) == 1]
    print("class-1 links internal to exactly one filling:", all(len(internal.get(l, ())) == 1 for l in c1),
          " class-2/3 links internal to none:", all(l not in internal for l in lp if cls(l) >= 2))
    qset = set(quarters)
    ok_split = all(sum(1 for i in lp[l] if i in qset) == 2 for l in c1)
    print("each class-1 link: 2 quarters (its filling) and 4 non-quarters:", ok_split)
    # degree census
    deg = []
    for i, (_, _, _, ls) in enumerate(plaqs):
        nb = set()
        for l in ls:
            if cls(l) >= 1:
                nb.update(j for j in lp[l] if j != i)
        deg.append(len(nb))
    print("off-link adjacency degree max", max(deg), "min", min(deg))
    # W(e0) and the midpoint test set W'(l)
    okW = True
    for x in sites:
        if odd(x):
            continue
        for mu in range(DIM):
            for pos in (0, 1):
                y = list(x); y[mu] += pos
                e = lk(y, mu)
                m = list(x); m[mu] += 1; m = norm(m)
                ps = lp[e]
                offs = [l for i in ps for l in plaqs[i][3] if cls(l) >= 1]
                at_m = []
                for i in ps:
                    am = [l for l in plaqs[i][3] if cls(l) >= 1 and
                          (l[0] == m or norm(tuple(l[0][k] + (1 if k == l[1] else 0) for k in range(DIM))) == m)]
                    at_m.append(len(am))
                    okW &= len(am) == 1
                mid_offs = set()
                for nu in range(DIM):
                    if nu == mu:
                        continue
                    mid_offs.add(lk(m, nu))
                    mm = list(m); mm[nu] -= 1; mid_offs.add(lk(mm, nu))
                covered = set(l for i in ps for l in plaqs[i][3] if l in mid_offs)
                okW &= len(ps) == 6 and len(set(offs)) == 12 and len(offs) == 12 and covered == mid_offs
    print("every line link: 6 plaquettes, 12 distinct off links, exactly 1 per plaquette at the midpoint,"
          " covering the 6 off links there:", okW)
    return plaqs, lp, cls


def part3(plaqs, lp, cls, NMAX=8):
    # coarse plaquette P at the origin in plane (0,1); its 8 line links; seeds = 6 off links at m_l, l=(0,0)
    def lk(x, mu):
        return (norm(x), mu)
    dP = [lk((0, 0, 0, 0), 0), lk((1, 0, 0, 0), 0), lk((0, 2, 0, 0), 0), lk((1, 2, 0, 0), 0),
          lk((0, 0, 0, 0), 1), lk((0, 1, 0, 0), 1), lk((2, 0, 0, 0), 1), lk((2, 1, 0, 0), 1)]
    assert all(cls(l) == 0 for l in dP)
    m = (1, 0, 0, 0)
    seeds = []
    for nu in (1, 2, 3):
        seeds.append(lk(m, nu))
        mm = list(m); mm[nu] -= 1; seeds.append(lk(mm, nu))
    poff = [tuple(l for l in ls if cls(l) >= 1) for (_, _, _, ls) in plaqs]
    found = {}
    for seed in seeds:
        start = [frozenset([p]) for p in lp[seed]]
        seen = set(start); frontier = list(start)
        while frontier:
            S = frontier.pop()
            mult = {}
            for p in S:
                for e in poff[p]:
                    mult[e] = mult.get(e, 0) + 1
            openl = [e for e, c in mult.items() if c == 1]
            n = len(S)
            if not openl:
                held = set(l for p in S for l in plaqs[p][3])
                if all(l in held for l in dP):
                    found[S] = n
                if n < NMAX:
                    for e in mult:
                        for q in lp[e]:
                            if q not in S:
                                T = S | {q}
                                if T not in seen:
                                    seen.add(T); frontier.append(T)
                continue
            rem = NMAX - n
            if rem <= 0 or len(openl) > 4 * rem:
                continue
            e0 = min(openl)
            for q in lp[e0]:
                if q not in S:
                    T = S | {q}
                    if T not in seen:
                        seen.add(T); frontier.append(T)
    hist = {}
    for S, n in found.items():
        hist[n] = hist.get(n, 0) + 1
    print("closed off-link-connected sets of <=", NMAX, "plaquettes holding all of dP at both positions, by size:",
          dict(sorted(hist.items())))


if __name__ == "__main__":
    part1()
    plaqs, lp, cls = part2()
    part3(plaqs, lp, cls)
