# Exact group sums and Haar integrals on only the multisets the plain degree argument cannot settle, on one-side-1 lattices in d >= 3. Every other multiset has each link at degree <= t and agrees by the degree argument. Uses the filed tool's functions. Integers only, json=0.
import itertools
import sys

args = sys.argv[1:]
sys.argv = sys.argv[:1]
sys.path.insert(0, "C:/tmp/opus55/confirm-4d-20261104/ym4-02b-last/winrun")
import multiset_check as mc  # noqa: E402

T = {"Q8": 3, "2T": 5, "2O": 7, "2I": 11}
for arg in args:
    s, g = arg.split(":")
    t = T[g]
    sides = tuple(int(v) for v in s.split("x"))
    lat = mc.Lat(sides)
    seen = {}
    worst = 0
    for k in range(1, t + 1):
        for combo in itertools.combinations_with_replacement(range(len(lat.faces)), k):
            deg = {}
            for i in combo:
                for l in lat.faces[i]:
                    deg[l] = deg.get(l, 0) + 1
            if any(v % 2 for v in deg.values()) or max(deg.values()) <= t:
                continue
            plist = [lat.faces[i] for i in combo]
            key = mc.canonical(plist)
            if key in seen:
                continue
            seen[key] = 1
            ge = mc.group_expect(lat, plist, g)
            he = mc.haar_expect(plist)
            same = 1 if ge == he else 0
            if not same:
                worst += 1
            print("OVER|sides=%s|group=%s|t=%d|k=%d|top_degree=%d|G=%d/%d|Haar=%d/%d|same=%d|json=0" % (s, g, t, k, max(deg.values()), ge[0], ge[1], he[0], he[1], same))
            sys.stdout.flush()
    print("OVER_CELL|sides=%s|group=%s|t=%d|patterns=%d|differ=%d|json=0" % (s, g, t, len(seen), worst))
    sys.stdout.flush()
print("OVER_DONE|json=0")
