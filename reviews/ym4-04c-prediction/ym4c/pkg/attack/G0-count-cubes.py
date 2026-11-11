"""Check that the 12 closed 6-plaquette sets holding an off link are the 12 unit cubes through it (scratch)."""
import importlib.util, os, sys
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cc", os.path.join(here, "G0-count-checks.py"))
cc = importlib.util.module_from_spec(spec); sys.argv = [sys.argv[0], "1", "1"]; spec.loader.exec_module(cc)
N = 8
G = cc.build(N)
plaqs = G["plaqs"]
def is_cube(S):
    planes = set((m, n) for (_, m, n, _) in (plaqs[p] for p in S))
    dirs = set(d for pl in planes for d in pl)
    if len(dirs) != 3 or len(planes) != 3: return False
    sites = set()
    for p in S:
        x, m, n, _ = plaqs[p]
        for a in (0, 1):
            for b in (0, 1):
                y = list(x); y[m] = (y[m] + a) % N; y[n] = (y[n] + b) % N; sites.add(tuple(y))
    return len(sites) == 8
for c in (1, 2, 3):
    w = cc.first_link_of_class(G, c)
    found, _ = cc.closed_search(G, G["link_plaqs"][w], 6)
    six = found.get(6, set())
    print(f"class {c}: {len(six)} closed 6-sets, all unit cubes: {all(is_cube(S) for S in six)}")
