#!/usr/bin/env python3
"""L4-sec4-part2 extra reads: more digits of the object channel at the flat-range edge, C19's surrogate edge with factor 6,
the wall crossing mu e^{1/4} eps_6 = 1, and the head-free lower limit at 0.02074 against the C03 head. Integer only."""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ival import ONE, rat, mul, iexp, dec, ds, self_check
import l4p2_checks as L

nb = self_check(os.path.abspath(__file__))
print("L4P2X_NO_FLOAT|bad=%d|tag=MEASURED|json=0" % sum(nb))
for n in (78733761, 78733762):
    c, e1, e2, e3, arg, fstop = L.cfin(rat(n, 10 ** 9))
    print("L4P2X_ENTRY3|delta=%d/1000000000|entry3=%s|e^-1=%s|tag=MEASURED|json=0" % (n, ds(e3, 14), ds(L.EM1, 14)))
# C19 surrogate: crude head, delta_1 <= 49/1000 in place of delta_1 <= delta_crit^-
em, _ = L.eps6(1552, 10 ** 5)
en, _ = L.eps6(1553, 10 ** 5)
okm, _ = L.met_read("crude", em, (49, 6000))
okn, _ = L.notmet_read("crude", en, (49, 6000))
print("L4P2X_C19_SURROGATE|MET_at_0.01552=%d|NOT_MET_at_0.01553=%d|tag=MEASURED|json=0" % (int(okm), int(okn)))
# the wall: mu e^{1/4} eps_6(beta) crosses 1 in [0.02247, 0.02248]
for b in (2247, 2248):
    e6, _ = L.eps6(b, 10 ** 5)
    w = mul(mul(L.MU, iexp(rat(1, 4))), e6)
    print("L4P2X_WALL|beta=0.%05d|mu*e^{1/4}*eps6=%s|below_1=%d|at_or_above_1=%d|tag=MEASURED|json=0" % (
        b, ds(w, 8), int(w[1] < ONE), int(w[0] >= ONE)))
