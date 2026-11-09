#!/usr/bin/env python3
# Lane L1-sec3-part1: (a) note Lemma 3.14 item 2, the class rule: the maps x -> sigma(x) + t (sigma a signed coordinate
# permutation, t even) preserve classes and plaquettes and act transitively on the off links of each class;
# (b) note Lemma 3.9, the BFS injection tau, run literally on the plaquette graph and tested for injectivity.
# Integer arithmetic only.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from poly_enum import build, enum

def classrule(N):
    D4 = (0, 1, 2, 3)
    def norm(a, b):
        # unordered unit edge {a, b} -> (base, dir)
        for d in D4:
            y = list(a); y[d] = (y[d] + 1) % N
            if tuple(y) == b:
                return (a, d)
            y = list(b); y[d] = (y[d] + 1) % N
            if tuple(y) == a:
                return (b, d)
        raise ValueError
    def ends(e):
        x, d = e
        y = list(x); y[d] = (y[d] + 1) % N
        return x, tuple(y)
    def odd(x):
        return frozenset(d for d in D4 if x[d] % 2 == 1)
    def cls(e):
        return len(odd(e[0]) - {e[1]})
    gens = []
    for i in D4:
        for j in D4:
            if i < j:
                def g(x, i=i, j=j):
                    y = list(x); y[i], y[j] = y[j], y[i]; return tuple(y)
                gens.append(g)
    gens.append(lambda x: (((-x[0]) % N),) + x[1:])
    for d in D4:
        def g(x, d=d):
            y = list(x); y[d] = (y[d] + 2) % N; return tuple(y)
        gens.append(g)
    sites = [(a, b, c, d) for a in range(N) for b in range(N) for c in range(N) for d in range(N)]
    links = [(x, d) for x in sites for d in D4]
    def plinks(x, l, n):
        def add(x, d):
            y = list(x); y[d] = (y[d] + 1) % N; return tuple(y)
        return {(x, l), (add(x, l), n), (add(x, n), l), (x, n)}
    plaq_sets = {frozenset(plinks(x, l, n)) for x in sites for l in D4 for n in D4 if l < n}
    ok_pres = True
    for g in gens:
        for e in links:
            a, b = ends(e)
            f = norm(g(a), g(b))
            if cls(f) != cls(e):
                ok_pres = False
        for P in list(plaq_sets)[:: max(1, len(plaq_sets) // 3000)]:
            img = set()
            for e in P:
                a, b = ends(e)
                img.add(norm(g(a), g(b)))
            if frozenset(img) not in plaq_sets:
                ok_pres = False
    res = []
    ok_tr = True
    for c, seed in ((1, ((0, 1, 0, 0), 0)), (2, ((0, 1, 1, 0), 0)), (3, ((0, 1, 1, 1), 0))):
        orbit = {seed}
        st = [seed]
        while st:
            e = st.pop()
            a, b = ends(e)
            for g in gens:
                f = norm(g(a), g(b))
                if f not in orbit:
                    orbit.add(f); st.append(f)
        allc = {e for e in links if cls(e) == c}
        res.append("class%d_orbit=%d_of_%d" % (c, len(orbit), len(allc)))
        if orbit != allc:
            ok_tr = False
    return ok_pres, ok_tr, res

def bfs_tau(G, root, nmax):
    """tau(A) for every connected A containing root with #A <= nmax; labelling lambda_u = position in nbrs[u]."""
    nbrs = G["nbrs"]
    lab = [{v: i + 1 for i, v in enumerate(nbrs[u])} for u in range(len(nbrs))]
    # enumerate connected sets containing root (Redelmeier), collect them
    sets = []
    np_ = len(nbrs)
    seen = bytearray(np_)
    P = []
    def rec(untried, size):
        untried = list(untried)
        while untried:
            v = untried.pop()
            P.append(v)
            sets.append(frozenset(P))
            if size + 1 < nmax:
                new = []
                for u in nbrs[v]:
                    if not seen[u]:
                        seen[u] = 1; new.append(u)
                rec(untried + new, size + 1)
                for u in new:
                    seen[u] = 0
            P.pop()
    seen[root] = 1
    rec([root], 0)
    images = {}
    ok = True
    for A in sets:
        # BFS inside A, FIFO; tree node = path of slot labels from the root
        node_of = {root: ()}
        queue = [root]
        qi = 0
        while qi < len(queue):
            u = queue[qi]; qi += 1
            for i in range(1, 21):
                # neighbour with label i, if any
                pass
            for v in nbrs[u]:
                pass
            inv = {lab[u][v]: v for v in nbrs[u]}
            for i in range(1, 21):
                v = inv.get(i)
                if v is not None and v in A and v not in node_of:
                    node_of[v] = node_of[u] + (i,)
                    queue.append(v)
        if len(node_of) != len(A):
            ok = False
        tau = frozenset(node_of.values())
        # subtree containing the root: prefix closed
        if not all(t[:-1] in tau for t in tau if t):
            ok = False
        # rebuild A from tau alone
        rebuilt = {(): root}
        for t in sorted(tau, key=len):
            if t:
                u = rebuilt[t[:-1]]
                inv = {lab[u][v]: v for v in nbrs[u]}
                rebuilt[t] = inv[t[-1]]
        if frozenset(rebuilt.values()) != A:
            ok = False
        if tau in images:
            ok = False
        images[tau] = A
    return ok, len(sets)

if __name__ == "__main__":
    allok = True
    for N in (8, 10):
        ok_pres, ok_tr, res = classrule(N)
        allok = allok and ok_pres and ok_tr
        print("CLASSRULE|N=%d|maps_preserve_class_and_plaquettes=%d|transitive_on_each_class=%d|%s" % (N, int(ok_pres), int(ok_tr), "|".join(res)))
    G = build(8)
    for name, x, l in (("quarter_root", None, None), ("nonquarter_root", None, None)):
        pass
    # a quarter (O(p) empty) and a plaquette with #O(p) = 1 as roots
    plaqs = G["plaqs"]
    odd = G["odd"]
    rq = next(i for i, (x, l, n) in enumerate(plaqs) if len(odd(x) - {l, n}) == 0)
    rn = next(i for i, (x, l, n) in enumerate(plaqs) if len(odd(x) - {l, n}) == 1)
    for name, r in (("quarter_root", rq), ("O1_root", rn)):
        ok, nsets = bfs_tau(G, r, 4)
        allok = allok and ok
        print("BFS_TAU|N=8|%s|connected_sets_size<=4=%d|tau_valid_subtree_rebuilds_A_injective=%d" % (name, nsets, int(ok)))
    print("CR_BFS_SUMMARY|all_ok=%d|tag=MEASURED|json=0" % int(allok))
