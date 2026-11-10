#!/usr/bin/env python3
"""Machine check of the combinatorial step of NOTE section 4 (own code, integers only).
Dual multigraph: vertices = cubes, edges = faces (face P_mn(x) joins cube x and cube x - r, r the third axis).
For every lattice with sides in {2,3,4,5} (sorted triples), enumerate EVERY nonempty face set F with |F| <= 3
and no dual vertex of degree exactly 1 (necessary, from the cube identity), up to translation (one face at the origin).
Classify them. Locality argument for sides >= 4 (written in REFUTE note): a closed walk of <= 3 unit steps in the
periodic lattice with every side >= 4 lifts to a closed walk in Z^3, which is bipartite, so has no 2- or 3-cycle
with distinct edges; hence sides >= 4 add nothing new and {2,3,4,5} covers every equivalence class.
"""
import itertools


def run(dims):
    sites = list(itertools.product(*[range(n) for n in dims]))
    sid = {s: i for i, s in enumerate(sites)}
    faces = []
    for s in sites:
        for mu, nu in ((0, 1), (0, 2), (1, 2)):
            r = 3 - mu - nu
            t = list(s)
            t[r] = (t[r] - 1) % dims[r]
            faces.append((sid[s], sid[tuple(t)], s, mu, nu))
    nf = len(faces)

    def ok(F):
        deg = {}
        for f in F:
            a, b = faces[f][0], faces[f][1]
            deg[a] = deg.get(a, 0) + 1
            deg[b] = deg.get(b, 0) + 1
        return all(v != 1 for v in deg.values())
    found = {1: 0, 2: 0, 3: 0}
    kinds = set()
    for k in (1, 2, 3):
        for first in range(3):  # a face at the origin
            for rest in itertools.combinations(range(nf), k - 1):
                if first in rest:
                    continue
                F = (first,) + rest
                if len(set(F)) != k or not ok(F):
                    continue
                found[k] += 1
                axes = sorted(set(3 - faces[f][3] - faces[f][4] for f in F))
                planes = sorted(set((faces[f][3], faces[f][4]) for f in F))
                straight = len(planes) == 1 and len(set(tuple(c for i, c in enumerate(faces[f][2]) if i != axes[0]) for f in F)) == 1
                kinds.add("k%d_axis%s_side%s_straight%d" % (k, axes[0] if len(axes) == 1 else "mixed",
                                                             dims[axes[0]] if len(axes) == 1 else "-", straight))
    lmin = min(dims)
    predicted = sorted(set(["k2_axis%d_side2_straight1" % a for a in range(3) if dims[a] == 2] +
                           ["k3_axis%d_side3_straight1" % a for a in range(3) if dims[a] == 3]))
    agree = sorted(kinds) == predicted
    print("SUPPORT_LEMMA|lattice=%dx%dx%d|L_min=%d|admissible_by_size=1:%d,2:%d,3:%d|kinds=%s|predicted=%s|agree=%d|json=0"
          % (dims + (lmin, found[1], found[2], found[3], ";".join(sorted(kinds)) or "none", ";".join(predicted) or "none", agree)))
    return agree


def main():
    allok = True
    for dims in itertools.combinations_with_replacement((2, 3, 4, 5), 3):
        allok = run(dims) and allok
    print("SUPPORT_LEMMA_DONE|all_agree=%d|json=0" % allok)


if __name__ == "__main__":
    main()
