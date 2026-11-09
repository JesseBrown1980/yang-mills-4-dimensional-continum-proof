#!/usr/bin/env python3
# Lane L1-sec3-part1: small-polymer enumeration on fine tori (Z/N)^4, for note Lemmas 3.5, 3.6, 3.9, 3.13, 3.14.
# Redelmeier enumeration of connected plaquette sets (graph: share an off link), with an exact closure prune.
# Integer arithmetic only.
import sys
sys.setrecursionlimit(10000)

def build(N):
    D4 = (0, 1, 2, 3)
    def sid(x):
        return ((x[0] * N + x[1]) * N + x[2]) * N + x[3]
    def add(x, d, s=1):
        y = list(x); y[d] = (y[d] + s) % N; return tuple(y)
    sites = [(a, b, c, d) for a in range(N) for b in range(N) for c in range(N) for d in range(N)]
    def lid(x, l):
        return sid(x) * 4 + l
    def odd(x):
        return frozenset(d for d in D4 if x[d] % 2 == 1)
    nl = 4 * N ** 4
    lclass = [0] * nl
    for x in sites:
        for l in D4:
            lclass[lid(x, l)] = len(odd(x) - {l})
    plaqs = []
    plinks = []
    for x in sites:
        for l in D4:
            for n in D4:
                if l < n:
                    plaqs.append((x, l, n))
                    plinks.append((lid(x, l), lid(add(x, l), n), lid(add(x, n), l), lid(x, n)))
    np_ = len(plaqs)
    poff = [tuple(e for e in plinks[i] if lclass[e] > 0) for i in range(np_)]
    link_pl = [[] for _ in range(nl)]
    for i in range(np_):
        for e in plinks[i]:
            link_pl[e].append(i)
    nbrs = [None] * np_
    for i in range(np_):
        s = []
        for e in poff[i]:
            for j in link_pl[e]:
                if j != i:
                    s.append(j)
        nbrs[i] = tuple(s)
    return dict(N=N, sites=sites, plaqs=plaqs, plinks=plinks, poff=poff, link_pl=link_pl, nbrs=nbrs,
                lclass=lclass, lid=lid, add=add, odd=odd)

def enum(G, roots, nmax, prune, collect_closed):
    """Enumerate connected plaquette sets S with root r in S and no root of smaller list position in S,
    for each r in roots (so each set meeting the roots is produced once). Returns counts by size of all
    produced sets (only meaningful when prune=False) and the list of closed sets."""
    nbrs = G["nbrs"]; poff = G["poff"]
    np_ = len(nbrs)
    seen = bytearray(np_)
    cnt = {}
    state = {"deficit": 0}
    counts = [0] * (nmax + 1)
    closed = []
    P = []
    def addp(v):
        d = 0
        for e in poff[v]:
            c = cnt.get(e, 0) + 1
            cnt[e] = c
            if c == 1: d += 1
            elif c == 2: d -= 1
        state["deficit"] += d
    def remp(v):
        d = 0
        for e in poff[v]:
            c = cnt[e] - 1
            if c == 0:
                del cnt[e]; d -= 1
            else:
                cnt[e] = c
                if c == 1: d += 1
        state["deficit"] += d
    def rec(untried, size):
        untried = list(untried)
        while untried:
            v = untried.pop()
            P.append(v); addp(v)
            s1 = size + 1
            counts[s1] += 1
            if state["deficit"] == 0 and collect_closed:
                closed.append(tuple(sorted(P)))
            if s1 < nmax and ((not prune) or state["deficit"] <= 4 * (nmax - s1)):
                new = []
                for u in nbrs[v]:
                    if not seen[u]:
                        seen[u] = 1
                        new.append(u)
                rec(untried + new, s1)
                for u in new:
                    seen[u] = 0
            remp(v); P.pop()
    for k, r in enumerate(roots):
        for q in roots[:k + 1]:
            seen[q] = 1
        rec([r], 0)
        for q in roots[:k + 1]:
            seen[q] = 0
    return counts, closed

def F20(n):
    from math import comb
    return comb(20 * n, n) // (19 * n + 1)

if __name__ == "__main__":
    Ns = [int(a) for a in sys.argv[1].split(",")]
    nmax_closed = int(sys.argv[2])
    nmax_conn = int(sys.argv[3])
    from math import comb
    allok = True
    results = {}
    for N in Ns:
        G = build(N)
        lid, odd, add = G["lid"], G["odd"], G["add"]
        plinks, poff, lclass, link_pl = G["plinks"], G["poff"], G["lclass"], G["link_pl"]
        reps = {
            "c1_xlam_even": lid((0, 1, 0, 0), 0),
            "c1_xlam_odd": lid((1, 1, 0, 0), 0),
            "c2": lid((0, 1, 1, 0), 0),
            "c3": lid((0, 1, 1, 1), 0),
            "c1_dir3": lid((0, 0, 1, 0), 3),
        }
        for name, w in reps.items():
            roots = list(link_pl[w])
            assert len(roots) == 6
            # (i) connected sets holding w, unpruned, to nmax_conn: compare with 6 F_20(n) (Lemma 3.9); per-root counts vs F_20(n)
            cc, _ = enum(G, roots, nmax_conn, False, False)
            ok39 = all(cc[n] <= 6 * F20(n) for n in range(1, nmax_conn + 1))
            per_root = []
            for r in roots:
                c1, _ = enum(G, [r], nmax_conn, False, False)
                per_root.append(c1)
            ok39r = all(c1[n] <= F20(n) for c1 in per_root for n in range(1, nmax_conn + 1))
            allok = allok and ok39 and ok39r
            print("ENUM_N%d|%s|class=%d|connected_holding_w_n1..%d=%s|6F20=%s|per_root_max=%s|F20=%s|lemma39_bound_ok=%d" % (
                N, name, lclass[w], nmax_conn, ",".join(str(cc[n]) for n in range(1, nmax_conn + 1)),
                ",".join(str(6 * F20(n)) for n in range(1, nmax_conn + 1)),
                ",".join(str(max(c1[n] for c1 in per_root)) for n in range(1, nmax_conn + 1)),
                ",".join(str(F20(n)) for n in range(1, nmax_conn + 1)), int(ok39 and ok39r)))
            # (ii) closed connected sets holding w, pruned, to nmax_closed
            _, closed = enum(G, roots, nmax_closed, True, True)
            byn = [0] * (nmax_closed + 1)
            for S in closed:
                byn[len(S)] += 1
            # dedupe check
            dup = len(closed) != len(set(closed))
            # Lemma 3.5: #off <= 2#gamma ; Lemma 3.6: 4-sets are fillings (all quarters, one plane, common corner with O = plane)
            ok35 = True; ok36 = True; ok313 = True
            plaqs = G["plaqs"]
            for S in closed:
                offs = set()
                for p in S:
                    offs.update(poff[p])
                if len(offs) > 2 * len(S): ok35 = False
                if len(S) <= 3: ok36 = False
                if len(S) == 4:
                    pls = [plaqs[p] for p in S]
                    if not all(len(odd(x) - {l, n}) == 0 for (x, l, n) in pls): ok36 = False
                    if len({(l, n) for (x, l, n) in pls}) != 1: ok36 = False
                    l, n = pls[0][1], pls[0][2]
                    common = None
                    for (x, ll, nn) in pls:
                        cs = {x, add(x, ll), add(add(x, ll), nn), add(x, nn)}
                        common = cs if common is None else (common & cs)
                    if len(common) != 1 or odd(next(iter(common))) != frozenset({l, n}): ok36 = False
                # Lemma 3.13 on the torus: every lambda-extent [c,c+1] present appears at least twice
                for lam in range(4):
                    ext = {}
                    for p in S:
                        x, l, n = plaqs[p]
                        if lam in (l, n):
                            ext[x[lam]] = ext.get(x[lam], 0) + 1
                    if any(v < 2 for v in ext.values()): ok313 = False
            exp4 = 1 if lclass[w] == 1 else 0
            ok36 = ok36 and byn[1] == 0 and byn[2] == 0 and byn[3] == 0 and byn[4] == exp4
            allok = allok and ok35 and ok36 and ok313 and not dup
            results[(N, name)] = byn
            print("ENUM_N%d|%s|class=%d|closed_connected_holding_w_N_w(n)_n1..%d=%s|dup=%d|lemma35_ok=%d|lemma36_ok=%d|lemma313_ok=%d" % (
                N, name, lclass[w], nmax_closed, ",".join(str(byn[n]) for n in range(1, nmax_closed + 1)), int(dup), int(ok35), int(ok36), int(ok313)))
    # Lemma 3.14: counts by class equal across reps of the same class and across N
    classes = {}
    for (N, name), byn in results.items():
        c = 1 if name.startswith("c1") else int(name[1])
        classes.setdefault(c, set()).add(tuple(byn))
    ok314 = all(len(v) == 1 for v in classes.values())
    allok = allok and ok314
    print("ENUM_CLASS_RULE|N=%s|counts_equal_within_class_across_reps_and_N=%d|%s" % (
        ",".join(str(n) for n in Ns), int(ok314), "|".join("class%d=%s" % (c, ",".join(str(x) for x in next(iter(v)))) for c, v in sorted(classes.items()))))
    print("ENUM_SUMMARY|all_ok=%d|tag=MEASURED|json=0" % int(allok))
