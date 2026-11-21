#!/usr/bin/env python3
"""YM4-04C v2 repair lane: pin C19 missing_tail (cut point and head) and demonstrate the corrected X3 route."""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/v2-checks")
from kp_exact import *

TH = Fr(1, 4)
HEADS = {"C03": {4: 1, 5: 0, 6: 12, 7: 0, 8: 32, 9: 32, 10: 304}, "headfree": {n: 0 for n in range(4, 11)}, "crude": {}}

def wall_quantity_lower(beta):
    eL, eU = eps6_bounds(beta)
    return MU * eL * exp_lo(TH)

if __name__ == "__main__":
    which = sys.argv[1]
    if which == "missing_tail":
        for beta in (Fr(1, 40), Fr(2248, 100000)):
            eL, eU = eps6_bounds(beta)
            print(f"beta={beta}: mu*e^(1/4)*eps6^- = {float(wall_quantity_lower(beta)):.8f} (>=1 means the pinned S^+ is undefined at every alpha>=0, theta>=1/4)")
            # pinned certificate (tail kept, cut 48): NOT_MET by the pole
            c = coeffs(HEADS["C03"], 48)
            ok, info = not_met_certificate(eL, eU, TH, c, 48, True)
            print(f"   pinned refined certificate (n<=48 + tail): NOT_MET proved={ok} {info}")
            for hname in ("C03", "headfree", "crude"):
                for ncut in (10, 48):
                    c = coeffs(HEADS[hname], ncut)
                    # try to certify MET with the no-tail series at a few rational alpha
                    met = None
                    for k in range(1, 400):
                        alpha = Fr(k, 2**22) if k < 200 else Fr(k - 199, 800)
                        okm, s = met_at(eU, alpha, TH, c, ncut, False)
                        if okm: met = (alpha, s); break
                    if hname == "headfree" and ncut == 10:
                        okm, s = met_at(eU, Fr(0), TH, c, ncut, False); met = (Fr(0), s) if okm else met
                    if met:
                        print(f"   no-tail cut={ncut} head={hname}: MET, S^+={float(met[1]):.4e} <= alpha={met[0]} ({float(met[0]):.4e})")
                    else:
                        ok, info = not_met_certificate(eL, eU, TH, c, ncut, False)
                        print(f"   no-tail cut={ncut} head={hname}: NOT_MET proved={ok} {[(float(v) if isinstance(v, Fr) else v) for v in (info if isinstance(info, tuple) else (info,))]}")
    elif which == "x3":
        c = coeffs(HEADS["crude"], 48)
        for j in (1904, 1905):
            beta = Fr(j, 100000); eL, eU = eps6_bounds(beta)
            a = newton_from_zero(eU, TH, c, 48, True)
            if a is not None:
                for h in (Fr(1, 2**30),):
                    ok, s = met_at(eU, a + h, TH, c, 48, True)
                    print(f"crude beta={j}e-5: Newton-from-0 iterate alpha_N={float(a):.12e}; read at alpha_N+2^-30: MET={ok} (S^+={float(s):.12e})")
            else:
                print(f"crude beta={j}e-5: Newton-from-0 stops (g'>=0 or alpha>1/4 or pole): no proposal")
            ok, info = not_met_certificate(eL, eU, TH, c, 48, True)
            print(f"   convex tangent NOT_MET certificate at theta=1/4: proved={ok} {[(float(v) if isinstance(v, Fr) else v) for v in (info if isinstance(info, tuple) else (info,))]}")
