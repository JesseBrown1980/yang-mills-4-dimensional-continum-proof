"""Orbits of the closed sets holding a class-1 link w under the stabilizer of w (scratch, not evidence).
Shows that the C03 numbers count sets, not symmetry classes."""
import importlib.util, os, sys, itertools
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cc", os.path.join(here, "G0-count-checks.py"))
cc = importlib.util.module_from_spec(spec); sys.argv = [sys.argv[0], "1", "1"]; spec.loader.exec_module(cc)
N = 8
G = cc.build(N)
links, link_id, plaqs = G["links"], G["link_id"], G["plaqs"]
pid = {(x, m, n): i for i, (x, m, n, _) in enumerate(plaqs)}
w = cc.first_link_of_class(G, 1)
found, _ = cc.closed_search(G, G["link_plaqs"][w], 8)
def link_key(x, m):
    return (x, m)
def img_link(g, l):
    perm, sg, t = g
    x, m = links[l]
    y = [0]*4
    for r in range(4):
        y[perm[r]] = (sg[r]*x[r] + t[perm[r]]) % N
    m2 = perm[m]
    if sg[m] < 0:
        y[m2] = (y[m2] - 1) % N
    return link_id[(tuple(y), m2)]
def img_plaq(g, p):
    ls = plaqs[p][3]
    s = frozenset(img_link(g, l) for l in ls)
    return s
plaq_by_links = {frozenset(ls): i for i, (_, _, _, ls) in enumerate(plaqs)}
x0, m0 = links[w]
stab = []
for perm in itertools.permutations(range(4)):
    for sg in itertools.product((1, -1), repeat=4):
        # choose the even translation that sends w's image back onto w, if any
        g0 = (perm, sg, (0, 0, 0, 0))
        l = img_link(g0, w)
        y, m = links[l]
        if m != m0: continue
        t = tuple((x0[r] - y[r]) % N for r in range(4))
        if any(c % 2 for c in t): continue
        g = (perm, sg, t)
        if img_link(g, w) == w: stab.append(g)
print("stabilizer order of a class-1 link:", len(stab))
for n in (4, 6, 8):
    sets = found.get(n, set())
    rem = set(sets); orbits = 0
    while rem:
        S = rem.pop(); orbits += 1
        for g in stab:
            T = frozenset(plaq_by_links[img_plaq(g, p)] for p in S)
            rem.discard(T)
    print(f"n={n}: {len(sets)} sets holding w, {orbits} orbits under the stabilizer of w")
