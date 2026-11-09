#!/usr/bin/env python3
"""Copies the canonical sections repair/G0.md and repair/G1.md into note-src/, changing file paths only:
scratch paths become the committed copies under reviews/ym4-04c-prediction/ (ym4c/ for the package tree,
ym4-04c/ for the design-lane tree). Every replacement must apply exactly the stated number of times."""
import os
PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = "reviews/ym4-04c-prediction/ym4c/pkg/"
SCR = "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/"
FIX = {
    "G0.md": [
        ("`pkg/derive/G0-a.md`", "`" + R + "derive/G0-a.md`", 1),
        ("`pkg/derive/G0-b.md`", "`" + R + "derive/G0-b.md`", 1),
        ("`pkg/attack/G0-kp.md`", "`" + R + "attack/G0-kp.md`", 1),
        ("`pkg/attack/G0-count.md`", "`" + R + "attack/G0-count.md`", 1),
        ("`pkg/attack/G0-assembly.md`", "`" + R + "attack/G0-assembly.md`", 1),
        ("`ym4-04c/synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp`",
         "`reviews/ym4-04c-prediction/ym4-04c/synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp`", 1),
        ("`" + SCR + "repair/G0-repair-checks.py`", "`" + R + "repair/G0-repair-checks.py`", 1),
    ],
    "G1.md": [
        ("`pkg/derive/G1-a.md`", "`" + R + "derive/G1-a.md`", 1),
        ("`pkg/derive/G1-b.md`", "`" + R + "derive/G1-b.md`", 1),
        ("`pkg/attack/G1-treegraph.md`", "`" + R + "attack/G1-treegraph.md`", 1),
        ("`pkg/attack/G1-channel.md`", "`" + R + "attack/G1-channel.md`", 1),
        ("`pkg/attack/G1-structure.md`", "`" + R + "attack/G1-structure.md`", 1),
        ("(`attack/g1tg/g1tg_literal_d.py`)", "(`" + R + "attack/g1tg/g1tg_literal_d.py`)", 1),
        ("Read by `repair/G1-repair-checks.py`:", "Read by `" + R + "repair/G1-repair-checks.py`:", 1),
        ("(`repair/G0-repair-checks.out`)", "(`" + R + "repair/G0-repair-checks.out`)", 1),
        ("All are under `" + SCR + "repair/`.", "All are under `" + R + "repair/`.", 1),
        ("- This package: `derive/G1-a.md`", "- This package, under `" + R + "`: `derive/G1-a.md`", 1),
    ],
}
OUT = {"G0.md": "03-G0.md", "G1.md": "04-G1.md"}
for name, reps in FIX.items():
    s = open(os.path.join(PKG, "repair", name), encoding="utf-8").read()
    for a, b, n in reps:
        assert s.count(a) == n, (name, a, s.count(a))
        s = s.replace(a, b)
    assert SCR not in s and "`pkg/" not in s, name
    open(os.path.join(PKG, "assemble", "note-src", OUT[name]), "w", encoding="utf-8").write(s)
    print(name, "->", OUT[name], len(reps), "path fixes")
