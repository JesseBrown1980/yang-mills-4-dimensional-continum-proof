#!/usr/bin/env python3
"""Scratch: induction windows (step-0 delta_1 <= 49/1000, where c(delta) < 1) under count models."""
from fractions import Fraction as Fr
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4-04c/polymer-norm")
from window2 import window, CRUDE, SMALL, FREE
from derive_estimates import dec
D = Fr(49, 1000)
for name, head in (("crude", CRUDE), ("small_counts", SMALL), ("head_free", FREE)):
    wi = window(head, D)
    print(name, "induction_window(delta1<=0.049)", dec(wi[0]), dec(wi[1]), flush=True)
