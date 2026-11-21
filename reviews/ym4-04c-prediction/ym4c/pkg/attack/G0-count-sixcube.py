"""Three unit cubes around one class-1 off link: a closed off-link-connected polymer in which that
link lies in all 6 of its plaquettes, so a common Finner exponent below 6 is not allowed (scratch)."""
import importlib.util, os, sys
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cc", os.path.join(here, "G0-count-checks.py"))
cc = importlib.util.module_from_spec(spec); sys.argv = [sys.argv[0], "1", "1"]; spec.loader.exec_module(cc)
N = 8
G = cc.build(N)
plaqs, link_id, poff, lclass = G["plaqs"], G["link_id"], G["poff"], G["lclass"]
pid = {(x, m, n): i for i, (x, m, n, _) in enumerate(plaqs)}
def sh(x, v): return tuple((a + b) % N for a, b in zip(x, v))
def cube(base, dirs):
    out = []
    a, b, c = dirs
    for (m, n, k) in ((a, b, c), (a, c, b), (b, c, a)):
        for t in (0, 1):
            v = [0, 0, 0, 0]; v[k] = t
            mm, nn = min(m, n), max(m, n)
            out.append(pid[(sh(base, tuple(v)), mm, nn)])
    return out
# e = ((0,1,0,0), 0): direction 0, odd transverse {1}: class 1
e = link_id[((0, 1, 0, 0), 0)]
assert lclass[e] == 1
o = (0, 1, 0, 0)
A = cube(o, (0, 2, 3))                      # +2, +3 sides
B = cube(sh(o, (0, 0, -1, 0)), (0, 2, 1))   # -2 side, +1 side
C = cube(sh(o, (0, -1, 0, -1)), (0, 1, 3))  # -1 side, -3 side
gam = set(A) | set(B) | set(C)
cnt = {}
for p in gam:
    for l in poff[p]:
        cnt[l] = cnt.get(l, 0) + 1
seen = {next(iter(gam))}; st = list(seen)
while st:
    p = st.pop()
    for q in G["adj"][p]:
        if q in gam and q not in seen: seen.add(q); st.append(q)
print("three cubes around e: size", len(gam), "closed", all(k >= 2 for k in cnt.values()),
      "connected", seen == gam, "incidence at e", cnt[e], "max incidence", max(cnt.values()))
