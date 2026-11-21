#!/usr/bin/env python3
"""Scratch (not evidence): where the C19 fault delta_crit_surrogate (delta_1 <= 49/1000 in place of
delta_1 < delta_crit^-) stops, with the frozen factor 12 and with the proved factor 6, crude head.
Exact enclosures from G0-kp-checks.py. Run: python3 -I G0-kp-surrogate.py"""
import importlib.util
from fractions import Fraction as Fr
spec = importlib.util.spec_from_file_location("k", __file__.replace("G0-kp-surrogate.py", "G0-kp-checks.py"))
k = importlib.util.module_from_spec(spec); spec.loader.exec_module(k)
SUR = Fr(49, 1000)
out = []
for factor, grid in ((12, range(1364, 1368)), (6, range(1550, 1557))):
    for g in grid:
        beta = Fr(g, 100000)
        eps = k.eps6_enc(beta)
        br = k.alpha_bracket(eps, k.HEAD_CRUDE)
        met = br is not None and br[1] is not None and factor * br[1] <= SUR
        notmet = k.certify_alpha_minus_above(eps, k.HEAD_CRUDE, SUR / factor)
        line = f"factor {factor} beta {g/100000:.5f}: surrogate MET certified {met}, NOT_MET certified {notmet}, factor*alpha in [{float(factor*br[0]):.9f}, {float(factor*br[1]):.9f}]"
        print(line); out.append(line)
open(__file__.replace(".py", ".out"), "w").write("\n".join(out) + "\n")
