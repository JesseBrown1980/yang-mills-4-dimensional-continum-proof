#!/usr/bin/env python3
# L3-sec4-part1: brute-force integer check of note Lemma 4.1 items 1-5 (and the
# site facts Lemmas 4.2/4.3 use) on fine (Z/M)^4, coarse (Z/(M/2))^4.
# Integer only: no float, no fractions module, no decimal.
import itertools, sys

def run(M):
    L = M // 2
    D = 4
    sites = list(itertools.product(range(M), repeat=D))
    def add(x, mu, s=1):
        y = list(x); y[mu] = (y[mu] + s) % M; return tuple(y)
    def O(x):
        return frozenset(i for i in range(D) if x[i] % 2 == 1)
    links = [(x, mu) for x in sites for mu in range(D)]
    # item 1: line link iff every non-mu coordinate even; position of exactly one coarse link
    def is_line(l):
        x, mu = l
        return all(x[i] % 2 == 0 for i in range(D) if i != mu)
    pos = {}  # fine line link -> (coarse link, position index)
    for xp in itertools.product(range(L), repeat=D):
        for mu in range(D):
            b = tuple(2 * c for c in xp)
            e0 = (b, mu); e1 = (add(b, mu), mu)
            for idx, e in ((0, e0), (1, e1)):
                assert e not in pos, ("two coarse links share a position", e)
                pos[e] = ((xp, mu), idx)
    nline = sum(1 for l in links if is_line(l))
    assert nline == len(pos) == 2 * D * L ** D
    for l in links:
        assert is_line(l) == (l in pos)
    # item 2: a fine plaquette holds 0 or 2 line links
    cnt = {}
    for x in sites:
        for mu in range(D):
            for nu in range(mu + 1, D):
                pl = [(x, mu), (add(x, mu), nu), (add(x, nu), mu), (x, nu)]
                k = sum(1 for l in pl if is_line(l))
                cnt[k] = cnt.get(k, 0) + 1
    assert set(cnt) <= {0, 2}, cnt
    # item 3: line links touch only #O<=1; O={mu} sites are midpoints of exactly one coarse
    # link; such a site touches exactly e0, e1 of it as line links, and 6 off links
    def links_at(x):
        out = []
        for nu in range(D):
            out.append((x, nu)); out.append((add(x, nu, -1), nu))
        return out
    mid_of = {}
    for xp in itertools.product(range(L), repeat=D):
        for mu in range(D):
            b = tuple(2 * c for c in xp)
            m = add(b, mu)
            assert m not in mid_of
            mid_of[m] = (xp, mu)
    bad = 0; nmid = 0; ncoarse = 0
    for x in sites:
        o = O(x)
        at = links_at(x)
        assert len(set(at)) == 8
        lines_here = [l for l in at if is_line(l)]
        if len(o) >= 2:
            if lines_here: bad += 1
        elif len(o) == 0:
            ncoarse += 1
            assert x not in mid_of
        else:
            nmid += 1
            (mu,) = tuple(o)
            cl = mid_of[x]
            assert cl[1] == mu
            b = tuple(2 * c for c in cl[0])
            assert set(lines_here) == {(b, mu), (x, mu)}, (x, lines_here)
            assert pos[(b, mu)] == (cl, 0) and pos[(x, mu)] == (cl, 1)
            assert len(at) - len(lines_here) == 6
    assert bad == 0 and nmid == D * L ** D and ncoarse == L ** D
    # two midpoints are never adjacent (each off link touches at most one midpoint)
    for x in mid_of:
        for nu in range(D):
            for s in (1, -1):
                assert add(x, nu, s) not in mid_of
    # the line-link graph is exactly the subdivision of the coarse torus graph:
    # every line link joins a coarse site and a midpoint, and m_l's two line links
    # end at 2x' and 2(x'+e_mu).  Cycles of a subdivision correspond 1-1 to cycles of
    # the graph, with the both-position rule; this is item 5's mechanism.
    for e, (cl, idx) in pos.items():
        y, mu = e
        a, b2 = y, add(y, mu)
        ends = sorted([len(O(a)), len(O(b2))])
        assert ends == [0, 1]
    for m, (xp, mu) in mid_of.items():
        nb = sorted([add(m, mu, -1), add(m, mu, 1)])
        want = sorted([tuple(2 * c for c in xp), tuple(2 * ((xp[i] + (1 if i == mu else 0)) % L) for i in range(D))])
        assert nb == want
    # item 4: coarse torus (Z/L)^4 has no self loops, no double links, no triangles
    csites = list(itertools.product(range(L), repeat=D))
    def cadd(x, mu, s=1):
        y = list(x); y[mu] = (y[mu] + s) % L; return tuple(y)
    nbr = {x: [] for x in csites}
    for x in csites:
        for mu in range(D):
            y = cadd(x, mu)
            assert y != x
            nbr[x].append(y); nbr[y].append(x)
    dbl = sum(1 for x in csites if len(nbr[x]) != len(set(nbr[x])))
    tri = 0
    for x in csites:
        sx = set(nbr[x])
        for y in sx:
            if sx & set(nbr[y]): tri += 1
    assert dbl == 0 and tri == 0
    return dict(M=M, L=L, line_links=nline, plaquette_line_counts=dict(sorted(cnt.items())),
                midpoints=nmid, coarse_sites=ncoarse, double_links=dbl, triangles=tri)

if __name__ == "__main__":
    for M in (8, 12):
        r = run(M)
        print("L3_LEMMA41|" + "|".join(f"{k}={v}" for k, v in r.items()) + "|all_asserts=PASS|json=0")
