#!/usr/bin/env python3
# Lane L1-sec3-part1: Lemma 3.14 at its size edge n <= 2N - 1, tested on the small even torus N = 4 (outside G0's N >= 8,
# used only to exercise the lifting / injectivity mechanism where winding first becomes possible, n = 2N = 8),
# against N = 8. Counts closed connected plaquette sets that hold one off link. Integer arithmetic only.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from poly_enum import build, enum

def winds(G, S):
    # a set winds when its plaquettes cover every lambda-slab [c, c+1] mod N for some lambda
    N = G["N"]; plaqs = G["plaqs"]
    for lam in range(4):
        cs = {plaqs[p][0][lam] for p in S if lam in (plaqs[p][1], plaqs[p][2])}
        if len(cs) == N:
            return True
    return False

if __name__ == "__main__":
    nmax = int(sys.argv[1])
    Ns = [int(a) for a in sys.argv[2].split(",")]
    which = sys.argv[3] if len(sys.argv) > 3 else "c1"
    for N in Ns:
        G = build(N)
        lid = G["lid"]
        w = {"c1": lid((0, 1, 0, 0), 0), "c2": lid((0, 1, 1, 0), 0), "c3": lid((0, 1, 1, 1), 0)}[which]
        roots = list(G["link_pl"][w])
        _, closed = enum(G, roots, nmax, True, True)
        byn = [0] * (nmax + 1)
        wind = [0] * (nmax + 1)
        for S in closed:
            byn[len(S)] += 1
            if winds(G, S):
                wind[len(S)] += 1
        print("EDGE314|N=%d|w=%s|class=%d|N_w(n)_n1..%d=%s|winding_n1..%d=%s|dup=%d" % (
            N, which, G["lclass"][w], nmax, ",".join(str(byn[n]) for n in range(1, nmax + 1)), nmax,
            ",".join(str(wind[n]) for n in range(1, nmax + 1)), int(len(closed) != len(set(closed)))))
    print("EDGE314_END|tag=MEASURED|json=0")
