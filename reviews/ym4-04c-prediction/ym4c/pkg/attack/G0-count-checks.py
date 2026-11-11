"""Second-seat scratch checks for the counting lens of Theorem G0.

Integers and Fractions only. Not an engine, not evidence.
Blocks:
  A  Fuss-Catalan values, divisibility, mu bracket, ratio monotonicity, product formula, tail.
  B  b = 2 geometry on fine (Z/N)^4, N = 8 and N = 10.
  C  off-link-connected sets through a root plaquette and through an off link, n <= NMAX_CONN,
     by Redelmeier enumeration, against F_20(n) and 6 F_20(n).
  D  closed (Lemma-B) off-link-connected sets through an off link of each class, n <= NMAX_CLOSED,
     by closure-driven growth; N = 8 and N = 10 compared (locality).
  E  closed sets holding all 8 line links of a coarse plaquette, n <= 8.
  F  the filling-plus-cube set of C19's finner_exponent_2 fault.
"""
import sys
from fractions import Fraction
from math import comb

sys.setrecursionlimit(10000)
NMAX_CONN = int(sys.argv[1]) if len(sys.argv) > 1 else 5
NMAX_CLOSED = int(sys.argv[2]) if len(sys.argv) > 2 else 8


def out(*a):
    print(*a, flush=True)


# ---------------- A ----------------
def F(n, D=20):
    num = comb(D * n, n)
    den = (D - 1) * n + 1
    assert num % den == 0
    return num // den


out("A. Fuss-Catalan")
draft = [20540, 784245, 31763004, 1340246340, 58281448940, 2593593086150,
         117544525178080, 5406686759963586, 251754316822792420]
vals = [F(n) for n in range(4, 13)]
out("  F_20(1..3) =", [F(n) for n in (1, 2, 3)])
out("  F_20(4..12) equal draft C01:", vals == draft)
# alternate form C(Dn, n-1)/n
assert all(comb(20 * n, n - 1) % n == 0 and comb(20 * n, n - 1) // n == F(n) for n in range(1, 300))
out("  F_D(n) = C(Dn,n-1)/n for n=1..299: True")
mu = Fraction(20 ** 20, 19 ** 19)
out("  mu bracket 5300068*19^19 <= 100000*20^20 <= 5300069*19^19:",
    5300068 * 19 ** 19 <= 100000 * 20 ** 20 <= 5300069 * 19 ** 19)
NR = 1500
prev = None
mono = True
below = True
for n in range(0, NR + 1):
    r = Fraction(F(n + 1), F(n))
    if prev is not None and not (prev < r):
        mono = False
    if not (r < mu):
        below = False
    prev = r
out(f"  F(n+1)/F(n) strictly increasing and < mu for n=0..{NR}:", mono and below)
ok = True
for n in range(0, 201):
    pf = Fraction(20)
    for j in range(1, 20):
        pf *= Fraction(20 * n + j, 19 * n + j + 1)
    ok &= (pf == Fraction(F(n + 1), F(n)))
out("  product formula 20*prod_{j=1}^{19}(20n+j)/(19n+j+1) = F(n+1)/F(n), n=0..200:", ok)
# tail: F(n) <= F(49) mu^(n-49) as integers, n = 49..1200
ok = all(F(n) * 19 ** (19 * (n - 49)) <= F(49) * 20 ** (20 * (n - 49)) for n in range(49, 1201))
out("  F(n) <= F(49) mu^(n-49) for n=49..1200:", ok)
# where F(n+2)/F(n) > 2000 holds
first = [n for n in range(1, 30) if F(n + 2) > 2000 * F(n)]
out("  F(n+2)/F(n) > 2000 first holds at n =", first[0], "; values n=4..9:",
    [round(F(n + 2) / F(n), 2) for n in range(4, 10)])
# C03 counting gaps
Nc = {8: 32, 10: 304, 12: 2326}
for n, c in Nc.items():
    g = Fraction(6 * F(n), c)
    out(f"  counting gap 6F(n)/N(n) at n={n}: {float(g):.6e}")
out("  N(10)/N(8) =", Fraction(304, 32), "; N(12)/N(10) =", Fraction(2326, 304), "=", float(Fraction(2326, 304)))


# ---------------- B ----------------
def build(N):
    sites = [(a, b, c, d) for a in range(N) for b in range(N) for c in range(N) for d in range(N)]

    def add(x, mu, s=1):
        y = list(x)
        y[mu] = (y[mu] + s) % N
        return tuple(y)

    link_id = {}
    links = []
    for x in sites:
        for m in range(4):
            link_id[(x, m)] = len(links)
            links.append((x, m))
    lclass = [sum(1 for r in range(4) if r != m and x[r] % 2 == 1) for (x, m) in links]
    plaqs = []
    for x in sites:
        for m in range(4):
            for n in range(m + 1, 4):
                ls = (link_id[(x, m)], link_id[(add(x, m), n)], link_id[(add(x, n), m)], link_id[(x, n)])
                plaqs.append((x, m, n, ls))
    link_plaqs = [[] for _ in links]
    for pi, (_, _, _, ls) in enumerate(plaqs):
        for l in ls:
            link_plaqs[l].append(pi)
    poff = [tuple(l for l in ls if lclass[l] > 0) for (_, _, _, ls) in plaqs]
    adj = []
    for pi, offs in enumerate(poff):
        nb = []
        for l in offs:
            for q in link_plaqs[l]:
                if q != pi:
                    nb.append(q)
        adj.append(nb)
    return dict(N=N, sites=sites, add=add, link_id=link_id, links=links, lclass=lclass,
                plaqs=plaqs, link_plaqs=link_plaqs, poff=poff, adj=adj)


def geometry(G):
    N = G["N"]
    links, lclass, plaqs, link_plaqs, poff, adj = (G[k] for k in ("links", "lclass", "plaqs", "link_plaqs", "poff", "adj"))
    out(f"B. geometry on fine (Z/{N})^4: {len(plaqs)} plaquettes, {len(links)} links")
    out("  every link in exactly 6 plaquettes:", all(len(v) == 6 for v in link_plaqs))
    out("  every plaquette has 4 distinct links:", all(len(set(ls)) == 4 for (_, _, _, ls) in plaqs))
    # share at most one link
    pair = {}
    for l, ps in enumerate(link_plaqs):
        for i in range(6):
            for j in range(i + 1, 6):
                k = (ps[i], ps[j])
                pair[k] = pair.get(k, 0) + 1
    out("  two distinct plaquettes share at most one link:", max(pair.values()) == 1)
    cc = [0, 0, 0, 0]
    for c in lclass:
        cc[c] += 1
    out("  link classes 0,1,2,3:", cc)
    out("  off links per plaquette:", sorted(set(len(o) for o in poff)))
    degs = [len(a) for a in adj]
    out("  off-link degree min, max:", min(degs), max(degs),
        "; neighbours distinct:", all(len(set(a)) == len(a) for a in adj),
        "; degree = 5*#off:", all(len(adj[i]) == 5 * len(poff[i]) for i in range(len(adj))))
    # quarters and fillings
    quarters = [i for i, o in enumerate(poff) if len(o) == 2]
    centers = {}
    for i in quarters:
        x, m, n, ls = plaqs[i]
        offs = poff[i]
        # common endpoint of the two off links
        def ends(l):
            y, d = links[l]
            return {y, G["add"](y, d)}
        c = ends(offs[0]) & ends(offs[1])
        assert len(c) == 1
        c = c.pop()
        centers.setdefault((c, m, n), []).append(i)
    out("  fillings:", len(centers), "; all of size 4:", all(len(v) == 4 for v in centers.values()))
    # class-1 links in exactly one filling, others none
    inf = [0] * len(links)
    for v in centers.values():
        s = set()
        for i in v:
            s |= set(poff[i])
        assert len(s) == 4
        for l in s:
            inf[l] += 1
    out("  filling membership by class:",
        {c: sorted(set(inf[l] for l in range(len(links)) if lclass[l] == c)) for c in range(1, 4)})
    # W(e0), W'(l)
    okW = True
    okWp = True
    for l in range(len(links)):
        if lclass[l] != 0:
            continue
        ps = link_plaqs[l]
        W = set()
        for p in ps:
            W |= set(poff[p])
        okW &= (len(W) == 12) and all(len(poff[p]) == 2 for p in ps)
        # midpoint: the endpoint of l that is not coarse
        y, d = links[l]
        ends = [y, G["add"](y, d)]
        mid = [e for e in ends if any(c % 2 for c in e)]
        assert len(mid) == 1
        mid = mid[0]
        for p in ps:
            at_mid = [o for o in poff[p] if mid in (links[o][0], G["add"](links[o][0], links[o][1]))]
            okWp &= (len(at_mid) == 1)
    out("  #W(e_0) = 12 at every line link, its 6 plaquettes quarters:", okW)
    out("  each plaquette through a line link has exactly one off link at the midpoint (W'(l) = 6):", okWp)
    return quarters, centers


# ---------------- C ----------------
def redelmeier(adj, root, forbidden, nmax):
    counts = [0] * (nmax + 1)
    seen = set(forbidden)
    seen.add(root)

    def rec(untried, size):
        untried = list(untried)
        while untried:
            v = untried.pop()
            counts[size + 1] += 1
            if size + 1 < nmax:
                new = []
                for u in adj[v]:
                    if u not in seen:
                        seen.add(u)
                        new.append(u)
                rec(untried + new, size + 1)
                for u in new:
                    seen.discard(u)

    rec([root], 0)
    return counts


def first_link_of_class(G, c):
    for l, cl in enumerate(G["lclass"]):
        if cl == c:
            return l


def conn_counts(G, nmax):
    adj, poff, link_plaqs = G["adj"], G["poff"], G["link_plaqs"]
    out(f"C. off-link-connected sets on (Z/{G['N']})^4, n <= {nmax}")
    bound1 = [F(n) for n in range(1, nmax + 1)]
    for name, cond in (("quarter", 2), ("non-quarter", 4)):
        root = next(i for i, o in enumerate(poff) if len(o) == cond)
        cts = redelmeier(adj, root, [], nmax)[1:]
        out(f"  through a {name} plaquette: {cts}  F_20: {bound1}  ok: {all(a <= b for a, b in zip(cts, bound1))}")
    bound6 = [6 * F(n) for n in range(1, nmax + 1)]
    for c in (1, 2, 3):
        w = first_link_of_class(G, c)
        ps = link_plaqs[w]
        tot = [0] * nmax
        for i, p in enumerate(ps):
            cts = redelmeier(adj, p, ps[:i], nmax)[1:]
            tot = [a + b for a, b in zip(tot, cts)]
        out(f"  holding a class-{c} off link: {tot}  6F_20: {bound6}  ok: {all(a <= b for a, b in zip(tot, bound6))}")


# ---------------- D ----------------
def closed_search(G, seeds, nmax, target=None):
    poff, link_plaqs = G["poff"], G["link_plaqs"]
    visited = set()
    found = {}
    stack = [frozenset([s]) for s in seeds]

    def open_links(S):
        cnt = {}
        for p in S:
            for l in poff[p]:
                cnt[l] = cnt.get(l, 0) + 1
        return sorted(l for l, k in cnt.items() if k == 1)

    while stack:
        S = stack.pop()
        if S in visited:
            continue
        visited.add(S)
        op = open_links(S)
        rem = nmax - len(S)
        if len(op) > 4 * rem:
            continue
        if not op:
            if target is None or target(S):
                found.setdefault(len(S), set()).add(S)
            if rem == 0:
                continue
            nbrs = set()
            for p in S:
                for l in poff[p]:
                    for q in link_plaqs[l]:
                        if q not in S:
                            nbrs.add(q)
            for q in nbrs:
                T = S | {q}
                if T not in visited:
                    stack.append(T)
        else:
            if rem == 0:
                continue
            f = op[0]
            for q in link_plaqs[f]:
                if q not in S:
                    T = S | {q}
                    if T not in visited:
                        stack.append(T)
    return found, len(visited)


def closed_counts(G, nmax):
    out(f"D. Lemma-B-closed off-link-connected sets holding a given off link on (Z/{G['N']})^4, n <= {nmax}")
    res = {}
    for c in (1, 2, 3):
        w = first_link_of_class(G, c)
        found, nst = closed_search(G, G["link_plaqs"][w], nmax)
        cts = [len(found.get(n, ())) for n in range(1, nmax + 1)]
        # sanity: every found set is closed, connected, holds w
        res[c] = cts
        out(f"  class {c}: N_c(1..{nmax}) = {cts}   ({nst} states)")
    return res


# ---------------- E ----------------
def readout(G, nmax=8):
    links, link_id, add, poff, link_plaqs, plaqs = (G[k] for k in ("links", "link_id", "add", "poff", "link_plaqs", "plaqs"))
    # coarse plaquette with base 0 in plane (0,1): line links of its boundary
    o = (0, 0, 0, 0)
    e0 = (1, 0, 0, 0)
    e1 = (0, 1, 0, 0)
    def lk(x, m):
        return link_id[(x, m)]
    def sh(x, v):
        return tuple((a + b) % G["N"] for a, b in zip(x, v))
    bd = set()
    for m, base_shift in ((0, (0, 0, 0, 0)), (0, (0, 2, 0, 0)), (1, (0, 0, 0, 0)), (1, (2, 0, 0, 0))):
        b = sh(o, base_shift)
        u = [0, 0, 0, 0]
        u[m] = 1
        bd.add(lk(b, m))
        bd.add(lk(sh(b, tuple(u)), m))
    assert len(bd) == 8 and all(G["lclass"][l] == 0 for l in bd)
    held = lambda S: bd <= {l for p in S for l in plaqs[p][3]}
    seeds = link_plaqs[lk(o, 0)]
    found, nst = closed_search(G, seeds, nmax, target=held)
    out(f"E. closed sets holding all 8 line links of a coarse plaquette, n <= {nmax}:",
        {n: len(v) for n, v in sorted(found.items())}, f"({nst} states)")


# ---------------- F ----------------
def filling_plus_cube(G):
    # filling centered at s = (1,1,0,0) in plane (0,1); internal link e from s along -e_0: ((0,1,0,0), 0), class 1, O_perp={1}
    N = G["N"]
    link_id, poff, plaqs, link_plaqs = G["link_id"], G["poff"], G["plaqs"], G["link_plaqs"]
    pid = {(x, m, n): i for i, (x, m, n, _) in enumerate(plaqs)}
    def sh(x, v):
        return tuple((a + b) % N for a, b in zip(x, v))
    s = (1, 1, 0, 0)
    fill = [pid[(sh(s, (dx, dy, 0, 0)), 0, 1)] for dx in (0, -1) for dy in (0, -1)]
    e = link_id[((0, 1, 0, 0), 0)]
    assert all(len(poff[p]) == 2 for p in fill)
    # unit cube in directions 0,2,3 at x_1 = 1 (odd), containing e: base (0,1,0,0)
    b = (0, 1, 0, 0)
    cube = []
    for (m, n, k) in ((0, 2, 3), (0, 3, 2), (2, 3, 0)):
        for t in (0, 1):
            v = [0, 0, 0, 0]
            v[k] = t
            cube.append(pid[(sh(b, tuple(v)), m, n)])
    gam = set(fill) | set(cube)
    cnt = {}
    for p in gam:
        for l in poff[p]:
            cnt[l] = cnt.get(l, 0) + 1
    closed = all(k >= 2 for k in cnt.values())
    # connectivity
    seen = {next(iter(gam))}
    st = list(seen)
    while st:
        p = st.pop()
        for q in G["adj"][p]:
            if q in gam and q not in seen:
                seen.add(q)
                st.append(q)
    out("F. filling + cube: size", len(gam), "closed", closed, "connected", seen == gam,
        "; plaquettes of the set through e:", cnt[e], "; max incidence:", max(cnt.values()),
        "; cube edges all off links:", all(G["lclass"][l] > 0 for p in cube for l in plaqs[p][3]))


if __name__ == "__main__":
    for N in (8, 10):
        G = build(N)
        geometry(G)
        if N == 8:
            filling_plus_cube(G)
            conn_counts(G, NMAX_CONN)
            readout(G, 8)
        res = closed_counts(G, NMAX_CLOSED)
    out("draft C03: class1 N_1(4..8) = 1,0,12,0,32; class2 0,0,12,0,12; class3 0,0,12,0,0")
