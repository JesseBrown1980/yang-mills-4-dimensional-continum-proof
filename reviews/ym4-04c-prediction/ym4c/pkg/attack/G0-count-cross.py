"""Cross-checks for G0-count-checks.py (scratch, integers only, not evidence).

1. Off-link-connected sets holding a class-1 off link, n <= 5, by brute-force extension with set dedup
   (a route independent of the Redelmeier recursion).
2. Closed-set counts N_w(n), n <= 8, at several off links of each class (different directions,
   both parities of the coordinate along the link): the counts should depend on the class only.
"""
import importlib.util
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cc", os.path.join(here, "G0-count-checks.py"))
cc = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0], "1", "1"]
spec.loader.exec_module(cc)

G = cc.build(8)
adj, poff, link_plaqs, links, lclass = G["adj"], G["poff"], G["link_plaqs"], G["links"], G["lclass"]

w = cc.first_link_of_class(G, 1)
layer = {frozenset([p]) for p in link_plaqs[w]}
counts = [len(layer)]
for n in range(2, 6):
    nxt = set()
    for S in layer:
        for p in S:
            for q in adj[p]:
                if q not in S:
                    nxt.add(S | {q})
    layer = nxt
    counts.append(len(layer))
print("1. brute force, sets holding a class-1 off link, n=1..5:", counts, flush=True)

print("2. closed counts N_w(1..8) at several links per class", flush=True)
for c in (1, 2, 3):
    picks = []
    seen_types = set()
    for l, cl in enumerate(lclass):
        if cl != c:
            continue
        x, m = links[l]
        odd = tuple(r for r in range(4) if r != m and x[r] % 2)
        key = (m, odd, x[m] % 2)
        if key not in seen_types:
            seen_types.add(key)
            picks.append(l)
    res = set()
    for l in picks[:8]:
        found, _ = cc.closed_search(G, link_plaqs[l], 8)
        res.add(tuple(len(found.get(n, ())) for n in range(1, 9)))
    print(f"  class {c}: {len(picks[:8])} link types tried, distinct count vectors: {sorted(res)}", flush=True)
