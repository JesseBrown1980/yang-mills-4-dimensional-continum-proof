#!/usr/bin/env python3
# L3-sec4-part1: exact integer checks of note Lemma 4.11 (root decomposition is
# injective) and Lemma 4.12 items 1 and 2 (the (1+t)^{s(o)} tree-graph bound), on
# random and adversarial hypergraphs of "objects" over off and line links.
# Integer only: every rational is an integer pair compared by cross-multiplication.
# No float, no fractions module, no decimal.  Seeded, deterministic.
import random, itertools, sys

def components(objs, off):
    # components of a set of object ids under "share an off link"
    objs = list(objs); seen = set(); comps = []
    for s in objs:
        if s in seen: continue
        stack = [s]; comp = set([s]); seen.add(s)
        while stack:
            a = stack.pop()
            for b in objs:
                if b not in seen and off[a] & off[b]:
                    seen.add(b); comp.add(b); stack.append(b)
        comps.append(frozenset(comp))
    return comps

def polymers(nobj, off):
    out = []
    for mask in range(1, 1 << nobj):
        S = [i for i in range(nobj) if mask >> i & 1]
        if len(components(S, off)) == 1:
            out.append(frozenset(S))
    return out

def instance(rng, n_off, n_line, nobj, kind):
    offl = list(range(n_off)); linel = list(range(n_off, n_off + n_line))
    objs = []
    for i in range(nobj):
        if kind == "star":      # every object holds off link 0: worst attachment pile-up
            f = set([0]) | set(rng.sample(offl[1:], rng.randint(0, 2)))
        elif kind == "chain":   # path-like overlaps
            f = set([i % n_off, (i + 1) % n_off])
        elif kind == "fat":     # few objects with many off links (the m=0, large f regime)
            f = set(rng.sample(offl, rng.randint(max(1, n_off // 2), n_off)))
        else:
            f = set(rng.sample(offl, rng.randint(1, min(4, n_off))))
        m = set(rng.sample(linel, rng.randint(0, min(3, n_line))))
        objs.append((frozenset(f), frozenset(m)))
    return offl, linel, objs

def check(rng, n_off, n_line, nobj, kind, t_num, t_den):
    offl, linel, objs = instance(rng, n_off, n_line, nobj, kind)
    off = [o[0] for o in objs]; supp = [o[0] | o[1] for o in objs]
    s = [len(f) for f in off]
    smax = max(s)
    # choose integer a_o >= 0, then the common denominator Dn so that (T) holds:
    # sum_{o ni e} (a_o/Dn) ((t_den+t_num)/t_den)^{s(o)} <= t_num/t_den at every off link e.
    a = [rng.randint(1, 50) for _ in objs]
    # need: t_den * sum a_o (t_den+t_num)^{s} t_den^{smax-s}  <=  t_num * Dn * t_den^{smax}
    need = 0
    for e in offl:
        lhs = sum(a[i] * (t_den + t_num) ** s[i] * t_den ** (smax - s[i]) for i in range(nobj) if e in off[i])
        lhs *= t_den
        rhs_unit = t_num * t_den ** smax
        need = max(need, -(-lhs // rhs_unit))
    Dn = max(need, 1)
    # (T) verified exactly, and record how tight it is at the worst link
    for e in offl:
        lhs = t_den * sum(a[i] * (t_den + t_num) ** s[i] * t_den ** (smax - s[i]) for i in range(nobj) if e in off[i])
        assert lhs <= t_num * Dn * t_den ** smax
    P = polymers(nobj, off)
    # nu(Gamma) = prod a_o / Dn^{#Gamma}; compare against t with common denominator Dn^nobj
    def num(G):  # numerator over Dn^nobj
        v = 1
        for i in G: v *= a[i]
        return v * Dn ** (nobj - len(G))
    DEN = Dn ** nobj
    worst1 = (0, 1)
    # Lemma 4.12 item 1 at every off link
    for e in offl:
        T = sum(num(G) for G in P if any(e in off[i] for i in G))
        # T/DEN <= t_num/t_den
        assert T * t_den <= t_num * DEN, ("item1 fails", e)
        if T * worst1[1] > worst1[0] * DEN * 1:  # track max T/DEN as pair (T, DEN)
            pass
        if worst1 == (0, 1) or T * worst1[1] > worst1[0] * DEN:
            worst1 = (T, DEN)
    # Lemma 4.11 injectivity and Lemma 4.12 item 2 at every link (off or line) and object o
    order = list(range(nobj))  # total order on objects = index
    allinks = offl + linel
    n_item2 = 0
    for e in allinks:
        seen = {}
        for G in P:
            holders = [i for i in G if e in supp[i]]
            if not holders: continue
            o = min(holders)
            rest = [i for i in G if i != o]
            key = None
            if rest:
                comps = components(rest, off)
                idx = {}
                for C in comps:
                    shared = sorted(off[o] & set().union(*[off[i] for i in C]))
                    assert shared, "component not attached to root through an off link"
                    eC = shared[0]
                    assert eC not in idx, "C -> e_C not injective"
                    idx[eC] = C
                key = (o, tuple(sorted((k, tuple(sorted(v))) for k, v in idx.items())))
            else:
                key = (o, ())
            assert key not in seen, "root decomposition not injective"
            seen[key] = G
        for o in range(nobj):
            if e not in supp[o]: continue
            lhs = sum(num(G) for G in P if len(G) >= 2 and o in G and min(i for i in G if e in supp[i]) == o)
            # rhs = (a_o/Dn) * ((1+t)^{s(o)} - 1); compare lhs/DEN <= a_o((t_den+t_num)^s - t_den^s)/(Dn t_den^s)
            so = s[o]
            assert lhs * Dn * t_den ** so <= a[o] * ((t_den + t_num) ** so - t_den ** so) * DEN, ("item2 fails", e, o)
            n_item2 += 1
    # ratio max_e T(e)/t as an integer pair, printed to 6 digits by integer division
    T, DENm = worst1
    r6 = (T * t_den * 10 ** 6) // (t_num * DENm)
    return len(P), n_item2, r6

def main():
    rng = random.Random(20261109)
    rows = []
    kinds = ["random", "star", "chain", "fat"]
    for rep in range(24):
        kind = kinds[rep % 4]
        t_num, t_den = [(1, 10), (1, 4), (85, 1000), (1, 1)][rep % 4]
        n_off = rng.randint(5, 9); n_line = rng.randint(2, 5); nobj = rng.randint(7, 11)
        npoly, n2, r6 = check(rng, n_off, n_line, nobj, kind, t_num, t_den)
        rows.append((rep, kind, f"{t_num}/{t_den}", n_off, n_line, nobj, npoly, n2, r6))
    for r in rows:
        print("L3_TREEGRAPH|rep=%d|kind=%s|t=%s|off=%d|line=%d|objects=%d|polymers=%d|item2_checks=%d|max_T_over_t_x1e6=%d|item1=PASS|item2=PASS|injective=PASS|json=0" % r)
    print("L3_TREEGRAPH_END|instances=%d|failed=0|tag=MEASURED|json=0" % len(rows))

if __name__ == "__main__":
    main()
