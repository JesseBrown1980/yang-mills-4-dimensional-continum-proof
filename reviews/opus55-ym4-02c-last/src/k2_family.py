#!/usr/bin/env python3
"""(Z/1)x(Z/1)x(Z/T), T>=4, Q8. The grid weights with w(+1)=0, so that only non-commuting slices survive: at most 6 orbits, at most 36 pairs. c_0 > 0 only, since w and -w give one form. Integers only, json=0."""
import itertools, sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *
from k2_orbits import Slice, form, c8
S = Slice(1)
total = psd = 0
ex = []
for b, c1, c2, c3 in itertools.product(range(-3, 4), repeat=4):
    w = (0, b, c1, c2, c3)
    if b == 0:
        continue  # the slice plaquette has no allowed value: Z = 0
    cc = c8(w)
    if cc[0] <= 0 or min(cc) >= 0:
        continue
    total += 1
    nreps, pairs, rows, K = form(S, list(w))
    p, q, r = bareiss_inertia(rows)
    if q == 0:
        psd += 1
        ex.append((w, cc, nreps, len(pairs), p, q, r))
print("K2_FAMILY|lattice=(Z/1)x(Z/1)x(Z/T),T>=4|group=Q8|w(+1)=0|w(-1)!=0|others_in_-3..3|c_0>0|some_c_rho<0=%d|PSD=%d|json=0" % (total, psd))
for e in ex[:30]:
    print("K2_FAMILY_PSD|w=%s|c_times_8=%s|slice_orbits=%d|pairs=%d|positive=%d|negative=%d|rank=%d|json=0" % (",".join(map(str, e[0])), ",".join(map(str, e[1])), e[2], e[3], e[4], e[5], e[6]))
