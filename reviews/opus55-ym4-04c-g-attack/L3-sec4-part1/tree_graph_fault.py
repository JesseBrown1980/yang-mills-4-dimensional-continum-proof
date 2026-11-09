#!/usr/bin/env python3
# Planted fault for tree_graph_exact.py: choose the activities so that only
# sum_{o ni e} nu_o <= t holds (the (1+t)^{s(o)} factor of (T) dropped), and show
# the instrument then reports item-1 violations T(e) > t.  Integer only.
import random, sys
sys.path.insert(0, "/mnt/c/tmp/opus55/ym4-04c-gattack/work/L3-sec4-part1")
from tree_graph_exact import components, polymers, instance

def run(rng, kind, t_num, t_den):
    n_off = rng.randint(5, 8); n_line = 3; nobj = rng.randint(8, 10)
    offl, linel, objs = instance(rng, n_off, n_line, nobj, kind)
    off = [o[0] for o in objs]
    a = [rng.randint(1, 50) for _ in objs]
    need = 0
    for e in offl:
        lhs = t_den * sum(a[i] for i in range(nobj) if e in off[i])
        need = max(need, -(-lhs // t_num))
    Dn = max(need, 1)
    P = polymers(nobj, off)
    DEN = Dn ** nobj
    viol = 0
    for e in offl:
        T = 0
        for G in P:
            if any(e in off[i] for i in G):
                v = 1
                for i in G: v *= a[i]
                T += v * Dn ** (nobj - len(G))
        if T * t_den > t_num * DEN: viol += 1
    return viol, n_off

rng = random.Random(7)
tot = 0
for rep in range(8):
    kind = ["fat", "star"][rep % 2]
    v, n = run(rng, kind, 1, 1)
    tot += v
    print("L3_TREEGRAPH_FAULT|rep=%d|kind=%s|t=1|off_links=%d|item1_violations=%d|json=0" % (rep, kind, n, v))
print("L3_TREEGRAPH_FAULT_END|total_violations=%d|expected=positive|tag=MEASURED|json=0" % tot)
