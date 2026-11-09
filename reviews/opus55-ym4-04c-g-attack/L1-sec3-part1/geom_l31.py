#!/usr/bin/env python3
# Lane L1-sec3-part1: exhaustive re-check of note Lemma 3.1 (items 1-8) and the Lemma 3.5 example
# on fine tori (Z/N)^4. Integer arithmetic only: no float, no fractions, no decimal, no true division.
import sys

def run(N):
    out = []
    ok_all = True
    def chk(name, ok, detail=""):
        nonlocal ok_all
        ok_all = ok_all and ok
        out.append("L31_N%d|%s|ok=%d%s" % (N, name, 1 if ok else 0, ("|" + detail) if detail else ""))
    L = N // 2
    D4 = (0, 1, 2, 3)
    def add(x, d, s=1):
        y = list(x); y[d] = (y[d] + s) % N; return tuple(y)
    def odd(x):
        return frozenset(d for d in D4 if x[d] % 2 == 1)
    sites = [(a, b, c, d) for a in range(N) for b in range(N) for c in range(N) for d in range(N)]
    def operp(link):
        return odd(link[0]) - {link[1]}
    # transverse odd set is the same at both ends
    same_ends = all(operp((x, l)) == (odd(add(x, l)) - {l}) for x in sites for l in D4)
    chk("operp_same_at_both_ends", same_ends)
    def lclass(link):
        return len(operp(link))
    plaqs = [(x, l, n) for x in sites for l in D4 for n in D4 if l < n]
    def plinks(p):
        x, l, n = p
        return [(x, l), (add(x, l), n), (add(x, n), l), (x, n)]
    def pcorners(p):
        x, l, n = p
        return [x, add(x, l), add(add(x, l), n), add(x, n)]
    def Op(p):
        x, l, n = p
        return odd(x) - {l, n}
    # O(p) same at all four corners
    chk("Op_same_at_all_corners", all(len({odd(c) - {p[1], p[2]} for c in pcorners(p)}) == 1 for p in plaqs))
    # ---- item 1
    link_pl = {}
    for p in plaqs:
        for e in plinks(p):
            link_pl.setdefault(e, []).append(p)
    nlinks = 4 * N ** 4
    chk("item1_link_count", len(link_pl) == nlinks, "links=%d" % len(link_pl))
    chk("item1_each_link_in_6_plaquettes", all(len(v) == 6 for v in link_pl.values()))
    chk("item1_plaquette_4_distinct_links", all(len(set(plinks(p))) == 4 for p in plaqs))
    share_ok = True
    for e, ps in link_pl.items():
        for i in range(len(ps)):
            si = set(plinks(ps[i]))
            for j in range(i + 1, len(ps)):
                if len(si & set(plinks(ps[j]))) != 1:
                    share_ok = False
    chk("item1_two_distinct_plaquettes_share_at_most_one_link", share_ok)
    # ---- item 2
    def is_line(e):
        return len(operp(e)) == 0
    def corner_of(e1, e2):
        a = {e1[0], add(e1[0], e1[1])}
        b = {e2[0], add(e2[0], e2[1])}
        c = a & b
        return c
    it2 = True
    nq = 0
    for p in plaqs:
        x, l, n = p
        ls = plinks(p)
        cl = sorted(lclass(e) for e in ls)
        t = len(Op(p))
        if t == 0:
            nq += 1
            lines = [e for e in ls if is_line(e)]
            offs = [e for e in ls if not is_line(e)]
            if cl != [0, 0, 1, 1]: it2 = False; continue
            if sorted(e[1] for e in lines) != sorted([l, n]): it2 = False
            c = corner_of(lines[0], lines[1])
            if len(c) != 1 or len(odd(next(iter(c)))) != 0: it2 = False
            c2 = corner_of(offs[0], offs[1])
            if len(c2) != 1 or odd(next(iter(c2))) != frozenset({l, n}): it2 = False
        else:
            if cl != sorted([t, t, t + 1, t + 1]): it2 = False
    chk("item2_quarters_and_classes", it2, "quarters=%d" % nq)
    chk("item2_quarter_count_6N4_over_4", nq * 4 == 6 * N ** 4)
    # ---- item 3: fillings
    fillings = {}  # (s, l, n) -> list of 4 plaquettes
    it3 = True
    quarter_fill_count = {}
    quarter_fill = {}
    def plaq_key(x, l, n):
        return (x, l, n)
    def coarse_of_line(e):
        # a line link (y, lam): position 0 of (y/2, lam) if y_lam even, else position 1 of ((y - e_lam)/2, lam)
        y, lam = e
        if y[lam] % 2 == 0:
            return (tuple(v // 2 for v in y), lam), 0
        yy = add(y, lam, -1)
        return (tuple(v // 2 for v in yy), lam), 1
    def cadd(x, d, s=1):
        y = list(x); y[d] = (y[d] + s) % L; return tuple(y)
    for s in sites:
        O = odd(s)
        if len(O) != 2:
            continue
        l, n = sorted(O)
        bases = [s, add(s, l, -1), add(s, n, -1), add(add(s, l, -1), n, -1)]
        F = [(b, l, n) for b in bases]
        if not all(len(Op(p)) == 0 for p in F): it3 = False
        cs = set()
        for p in F:
            cs.update(pcorners(p))
        if len(cs) != 9: it3 = False
        for c in cs:
            if c != s and len(odd(c)) == 0:
                pass
        far = [add(add(s, l, a), n, b) for a in (1, -1) for b in (1, -1)]
        if not all(len(odd(c)) == 0 for c in far): it3 = False
        internal = set()
        for p in F:
            for e in plinks(p):
                if not is_line(e):
                    internal.add(e)
        expect_int = {(s, l), (add(s, l, -1), l), (s, n), (add(s, n, -1), n)}
        if internal != expect_int: it3 = False
        # each internal link in exactly 2 quarters of F; 4-cycle
        for e in internal:
            if sum(1 for p in F if e in plinks(p)) != 2: it3 = False
        adj = {i: set() for i in range(4)}
        for i in range(4):
            for j in range(4):
                if i != j and set(plinks(F[i])) & set(plinks(F[j])) & internal:
                    adj[i].add(j)
        if not all(len(adj[i]) == 2 for i in range(4)): it3 = False
        # 8 line links = both positions of the 4 coarse links of dQ, Q with base (s - e_l - e_n)/2
        q = tuple(v // 2 for v in add(add(s, l, -1), n, -1))
        dQ = {(q, l), (cadd(q, n), l), (q, n), (cadd(q, l), n)}
        lines = set()
        for p in F:
            for e in plinks(p):
                if is_line(e):
                    lines.add(e)
        if len(lines) != 8: it3 = False
        cl = {}
        for e in lines:
            c, pos = coarse_of_line(e)
            cl.setdefault(c, set()).add(pos)
        if set(cl.keys()) != dQ or not all(v == {0, 1} for v in cl.values()): it3 = False
        # the quarter at a coarse corner c holds the two line links of dQ at c
        for p in F:
            ls = [e for e in plinks(p) if is_line(e)]
            cc = corner_of(ls[0], ls[1])
            if len(cc) != 1 or len(odd(next(iter(cc)))) != 0: it3 = False
        fillings[(s, l, n)] = F
        for p in F:
            quarter_fill_count[p] = quarter_fill_count.get(p, 0) + 1
            quarter_fill[p] = (s, l, n)
    chk("item3_fillings", it3, "fillings=%d" % len(fillings))
    chk("item3_every_quarter_in_exactly_one_filling", len(quarter_fill_count) == nq and all(v == 1 for v in quarter_fill_count.values()))
    # ---- item 4
    internal_of = {}
    for key, F in fillings.items():
        for p in F:
            for e in plinks(p):
                if not is_line(e):
                    internal_of.setdefault(e, set()).add(key)
    it4 = True
    n1 = n2 = n3 = 0
    for e, ps in link_pl.items():
        c = lclass(e)
        if c == 1:
            n1 += 1
            fs = internal_of.get(e, set())
            if len(fs) != 1: it4 = False; continue
            key = next(iter(fs))
            qs = [p for p in ps if len(Op(p)) == 0]
            o1 = [p for p in ps if len(Op(p)) == 1]
            if len(qs) != 2 or len(o1) != 4: it4 = False
            if not all(p in fillings[key] for p in qs): it4 = False
        elif c in (2, 3):
            if c == 2: n2 += 1
            else: n3 += 1
            if any(len(Op(p)) == 0 for p in ps): it4 = False
            if e in internal_of: it4 = False
    for p in plaqs:
        if len(Op(p)) == 1:
            c1 = [e for e in plinks(p) if lclass(e) == 1]
            if len(c1) != 2: it4 = False; continue
            planes = []
            for e in c1:
                fs = internal_of.get(e, set())
                if len(fs) != 1: it4 = False; break
                key = next(iter(fs))
                planes.append((key[1], key[2]))
            if len(planes) == 2 and planes[0] == planes[1]: it4 = False
    chk("item4_class1_links", it4, "class1=%d|class2=%d|class3=%d" % (n1, n2, n3))
    # ---- coarse lattice structures (item 8 and used in 5, 6)
    csites = [(a, b, c, d) for a in range(L) for b in range(L) for c in range(L) for d in range(L)]
    cplaqs = [(x, l, n) for x in csites for l in D4 for n in D4 if l < n]
    def cplinks(P):
        x, l, n = P
        return [(x, l), (cadd(x, l), n), (cadd(x, n), l), (x, n)]
    clink_pl = {}
    for P in cplaqs:
        for e in cplinks(P):
            clink_pl.setdefault(e, []).append(P)
    it8 = all(len(set(cplinks(P))) == 4 for P in cplaqs) and all(len(v) == 6 for v in clink_pl.values()) and len(clink_pl) == 4 * L ** 4
    # two perpendicular coarse links at a common site lie in exactly one coarse plaquette
    def cends(e):
        return {e[0], cadd(e[0], e[1])}
    perp_ok = True
    for x in csites:
        inc = []
        for d in D4:
            inc.append((x, d))
            inc.append((cadd(x, d, -1), d))
        for i in range(len(inc)):
            for j in range(i + 1, len(inc)):
                a, b = inc[i], inc[j]
                if a[1] == b[1]:
                    continue
                cnt = sum(1 for P in clink_pl[a] if b in cplinks(P))
                if cnt != 1:
                    perp_ok = False
    # girth of the coarse link graph: no multi-edges, shortest cycle length
    adjc = {x: [] for x in csites}
    for x in csites:
        for d in D4:
            y = cadd(x, d)
            adjc[x].append(y)
            adjc[y].append(x)
    multi = any(len(set(v)) != len(v) for v in adjc.values())
    girth = None
    for r in csites:
        dist = {r: 0}
        par = {r: None}
        frontier = [r]
        while frontier:
            nf = []
            for u in frontier:
                for v in adjc[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        par[v] = u
                        nf.append(v)
                    elif par[u] != v:
                        g = dist[u] + dist[v] + 1
                        if girth is None or g < girth:
                            girth = g
            frontier = nf
    chk("item8_coarse", it8 and perp_ok and (not multi) and girth == 4, "L=%d|perp_unique=%d|multi_edges=%d|girth=%s" % (L, int(perp_ok), int(multi), girth))
    # ---- item 5
    it5 = True
    for key, F in fillings.items():
        s, l, n = key
        q = tuple(v // 2 for v in add(add(s, l, -1), n, -1))
        Q = (q, l, n)
        for p in F:
            ls = [e for e in plinks(p) if is_line(e)]
            c0 = coarse_of_line(ls[0])[0]
            c1 = coarse_of_line(ls[1])[0]
            both = [P for P in clink_pl[c0] if c1 in cplinks(P)]
            if both != [Q]:
                it5 = False
    chk("item5_quarter_holds_at_most_one_line_link_of_other_dP", it5)
    # ---- item 6
    it6 = True
    for x1 in csites:
        for l in D4:
            ell = (x1, l)
            b = tuple(2 * v for v in x1)
            e0 = (b, l)
            m = add(b, l)
            e1 = (m, l)
            P6 = link_pl[e0]
            if len(P6) != 6 or not all(len(Op(p)) == 0 for p in P6): it6 = False; continue
            Qs = clink_pl[ell]
            offs = []
            atm = []
            keys = []
            for p in P6:
                if b not in pcorners(p): it6 = False
                o = [e for e in plinks(p) if not is_line(e)]
                offs.extend(o)
                key = [quarter_fill[p]] if p in quarter_fill else []
                if len(key) != 1: it6 = False; continue
                keys.append(key[0])
                s, l2, n2 = key[0]
                q = tuple(v // 2 for v in add(add(s, l2, -1), n2, -1))
                if (q, l2, n2) not in Qs: it6 = False
                am = [e for e in o if m in (e[0], add(e[0], e[1]))]
                if len(am) != 1: it6 = False
                atm.extend(am)
            if len(set(offs)) != 12: it6 = False
            for k in keys:
                if sum(1 for e in set(offs) if e in internal_of and k in internal_of[e]) != 2: it6 = False
            Wp = set()
            for d in D4:
                for e in ((m, d), (add(m, d, -1), d)):
                    if not is_line(e):
                        Wp.add(e)
            if len(Wp) != 6 or set(atm) != Wp: it6 = False
            # e1 side: same 6 fillings, same W'
            P6b = link_pl[e1]
            atm1 = []
            keys1 = []
            for p in P6b:
                keys1.append(quarter_fill[p])
                o = [e for e in plinks(p) if not is_line(e)]
                atm1.extend(e for e in o if m in (e[0], add(e[0], e[1])))
                if add(b, l, 2) not in pcorners(p): it6 = False
            if set(keys1) != set(keys) or set(atm1) != Wp: it6 = False
            # map filling -> its off link at m from both sides agrees
            if not all(lclass(e) == 1 for e in set(offs) | Wp): it6 = False
    chk("item6_W_e0_12_distinct_Wprime_6_class1", it6)
    # ---- item 7: degree = 5 * #off
    nbr = {}
    for e, ps in link_pl.items():
        if is_line(e):
            continue
        for p in ps:
            for q in ps:
                if p != q:
                    nbr.setdefault(p, set()).add(q)
    it7 = True
    degs = set()
    for p in plaqs:
        k = sum(1 for e in plinks(p) if not is_line(e))
        dg = len(nbr.get(p, ()))
        degs.add(dg)
        if dg != 5 * k: it7 = False
    chk("item7_degree_5k", it7 and max(degs) == 20 and min(degs) == 10, "degrees=%s" % sorted(degs))
    # ---- Lemma 3.5 example: the 6 faces of a unit cube with odd 4th coordinate
    x0 = (0, 0, 0, 1)
    cube = []
    for (a, bb) in ((0, 1), (0, 2), (1, 2)):
        c = 3 - a - bb
        cube.append((x0, a, bb))
        cube.append((add(x0, c), a, bb))
    cl = {}
    for p in cube:
        for e in plinks(p):
            cl[e] = cl.get(e, 0) + 1
    alloff = all(not is_line(e) for e in cl)
    closed = all(v >= 2 for e, v in cl.items() if not is_line(e))
    # connectivity via shared off links
    seen = {cube[0]}
    st = [cube[0]]
    while st:
        u = st.pop()
        for v in cube:
            if v not in seen and set(e for e in plinks(u) if not is_line(e)) & set(e for e in plinks(v) if not is_line(e)):
                seen.add(v); st.append(v)
    chk("lemma35_cube_example", alloff and closed and len(seen) == 6 and len(cl) == 12 and len(set(cube)) == 6,
        "plaquettes=6|off_links=%d|all_off=%d|closed=%d|connected=%d" % (len(cl), int(alloff), int(closed), int(len(seen) == 6)))
    return ok_all, out

if __name__ == "__main__":
    Ns = [int(a) for a in sys.argv[1:]] or [8, 10]
    allok = True
    for N in Ns:
        ok, out = run(N)
        allok = allok and ok
        for line in out:
            print(line)
    print("L31_SUMMARY|N=%s|all_ok=%d|tag=MEASURED|json=0" % (",".join(str(n) for n in Ns), int(allok)))
