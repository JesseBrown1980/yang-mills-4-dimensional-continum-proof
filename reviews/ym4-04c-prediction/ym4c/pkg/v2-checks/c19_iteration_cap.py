#!/usr/bin/env python3
"""YM4-04C v2 repair lane: pin C19's iteration_cap_400 fault by exact computation.

Exact Fractions with upward dyadic rounding at 160 bits (delta_scan3.up/eup), eps_6 upper enclosure on the
1e-12 grid (derive_estimates.norms + root_bracket), S^+ = window2.S (the pinned crude series to n = 48 plus
the n = 49 geometric tail). KP pair renamed (alpha, theta); theta = 1/4 unless stated.
Variants of the planted iteration, all starting at alpha_0 = 0 and capped at 400 evaluations of S^+:
  J: alpha <- s,                 accept when s <= alpha*(1 + 10^-40)      (the judge's variant)
  W: alpha <- up(s*10001/10000), accept when s <= alpha                  (window2.least_a)
  P: alpha <- s,                 accept when s <= alpha                  (plain, no tolerance)
s := S^+(up(eps^+ * eup(2 alpha + theta))); NOT_MET when s is undefined (mu x >= 1) or s > 1/4, or at the cap.
"""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4-04c/polymer-norm")
from delta_scan3 import up, eup, KAPPA
from derive_estimates import norms, root_bracket
import window2

TOL = Fr(1, 10**40)
CAP = 400

def eps6_up(beta, den=10**12):
    _, _, (k6lo, k6hi) = norms(beta)
    return up(root_bracket(k6hi, 6, den)[1])

def run(eps, theta, variant, head=None):
    head = {} if head is None else head
    a = Fr(0)
    for j in range(1, CAP + 1):
        s = window2.S(up(eps * eup(2 * a + theta)), head)
        if s is None or s > Fr(1, 4):
            return ("NOT_MET", j, "s_undefined_or_above_1/4")
        if variant == "J":
            if s <= a * (1 + TOL): return ("MET", j, a)
            a = s
        elif variant == "W":
            if s <= a: return ("MET", j, a)
            a = up(s * Fr(10001, 10000))
        elif variant == "P":
            if s <= a: return ("MET", j, a)
            a = s
    return ("NOT_MET", CAP, "cap_reached")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "theta14"
    if mode == "theta14":
        for j in range(1900, 1906):
            beta = Fr(j, 100000); eps = eps6_up(beta)
            out = [f"beta={j}e-5"]
            for v in ("J", "W", "P"):
                r = run(eps, KAPPA, v)
                tag = r[0] + f"@{r[1]}"
                if r[0] == "MET": tag += f"(alpha~{float(r[2]):.6e})"
                else: tag += f"({r[2]})"
                out.append(f"{v}:{tag}")
            print(" ".join(out), flush=True)
    elif mode == "alltheta":
        # variant J at every grid theta = 1/4 + i/64, i = 0..320
        for j in map(int, sys.argv[2].split(",")):
            beta = Fr(j, 100000); eps = eps6_up(beta)
            mets = []; reasons = {}
            for i in range(0, 321):
                r = run(eps, KAPPA + Fr(i, 64), "J")
                if r[0] == "MET": mets.append(i)
                reasons[r[2] if r[0] == "NOT_MET" else "MET"] = reasons.get(r[2] if r[0] == "NOT_MET" else "MET", 0) + 1
            print(f"beta={j}e-5 variant J over 321 grid theta: MET at i={mets} ; outcomes={reasons}", flush=True)
