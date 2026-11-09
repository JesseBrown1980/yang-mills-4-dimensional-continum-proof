#!/usr/bin/env python3
"""YM4-04C v2: C10c brackets at the quoted digits (same arithmetic as c10c_constants.py, nmax = 150)."""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/v2-checks")
from c10c_constants import E, c_of, K, EABS_HI
from kp_exact import up, dn
EABS_LO = Fr(8, 3) / Fr(31416, 10000)       # 8/(3 pi) >= 8/(3*3.1416)
def br(lo, hi, d):
    import math
    sc = 10**d
    return f"[{math.floor(lo*sc)/sc:.{d}f},{math.ceil(hi*sc)/sc:.{d}f}]"
lead = (E(Fr(-3, 2))[0] / 4, E(Fr(-3, 2))[1] / 4)
print("e^{-3/2}/4 in", br(*lead, 8))
for s in (Fr(1, 8192), Fr(1, 65536)):
    e10 = E(10 * K); din = (dn(24 * s * e10[0]), up(24 * s * e10[1]))
    (clo, chi), (t2lo, t2hi) = c_of(*din, nmax=150)
    e1 = E(1)
    rnat = (6 * e1[0] * (s - 4 * s * s) / din[1], 6 * e1[1] * (s + 4 * s * s) / din[0])
    lb = (6 * e1[0] * (s / 2 - 4 * s * s * EABS_HI) / EABS_HI, 6 * e1[1] * (s / 2 + 4 * s * s * EABS_HI) / EABS_LO)
    rlb = (lb[0] / din[1], lb[1] / din[0])
    q = (rlb[0] / chi, rlb[1] / clo)
    print(f"s={s}: delta_in {br(*din,7)} 2delta' {br(t2lo,t2hi,7)} C_k_MET={t2hi <= K/2} c {br(clo,chi,7)}")
    print(f"   natural ratio {br(*rnat,7)}  lower-bound/delta_in {br(*rlb,7)}  lower-bound/(c*delta_in) {br(*q,5)}  slack_nat {br(clo/rnat[1], chi/rnat[0], 3)} slack_lb {br(1/q[1], 1/q[0], 2)}")
