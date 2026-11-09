#!/usr/bin/env python3
"""Scratch (not an engine, not evidence): the self-map edges of C13/C14 with the proved G1 constant.

delta_1(beta) comes from the G0 lane's scratch certify() (G0-a-kp.py, theta = kappa, exact
upward-rounded KP inequality); the frozen output is 12*alpha, the G0-a proved output 6*S.
The G1 test is delta_1 < delta_crit*^- = 54765347/500000000 (g1a_constants.py crit).
Bisection only locates; each read is the certified pair.
"""
import importlib.util
import sys
from fractions import Fraction as Fr

G0 = "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/derive/G0-a-kp.py"
spec = importlib.util.spec_from_file_location("g0kp", G0)
g0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g0)

DCRIT_STAR = Fr(54765347, 500000000)
DCRIT_FROZEN = Fr(496174, 10**7)


def delta1(j, head, which, den=100000):
    eps, a = g0.certify(Fr(j, den), g0.HEADS[head])
    if a is None:
        return None
    if which == "frozen":
        return 12 * a
    return 6 * g0.S_up(g0.up(eps * g0.exp_up(2 * a + g0.KAPPA)), g0.HEADS[head])


def edge(head, which, dcrit, lo, hi, den=100000):
    def ok(j):
        d = delta1(j, head, which, den)
        return d is not None and d < dcrit
    assert ok(lo), ("lo", lo)
    assert not ok(hi), ("hi", hi)
    while hi - lo > 1:
        m = (lo + hi) // 2
        if ok(m):
            lo = m
        else:
            hi = m
    dlo = delta1(lo, head, which, den)
    dhi = delta1(hi, head, which, den)
    print(f"{head} / delta_1 {which} / dcrit {float(dcrit):.9f}: MET at {lo}/{den} (delta_1={float(dlo):.7g}); "
          f"not at {hi}/{den} (delta_1={'none: C_0 not certified' if dhi is None else f'{float(dhi):.7g}'})")


if __name__ == "__main__":
    w = sys.argv[1]
    if w == "crude":
        edge("crude", "frozen", DCRIT_STAR, 1560, 1910)
    elif w == "crude-g0a":
        edge("crude", "proved", DCRIT_STAR, 1560, 1910)
    elif w == "refined":
        edge("refined(C03)", "frozen", DCRIT_STAR, 1959, 2080)
    elif w == "headfree":
        edge("head-free", "frozen", DCRIT_STAR, 1959, 2080)
    elif w == "refined-g0a":
        edge("refined(C03)", "proved", DCRIT_STAR, 1959, 2080)
    elif w == "pts":
        for j, head in ((1563, "crude"), (1904, "crude"), (1905, "crude"), (2075, "refined(C03)"),
                        (2076, "refined(C03)"), (2075, "head-free"), (2076, "head-free"), (2000, "head-free")):
            print(j, head, delta1(j, head, "frozen"), "frozen 12a ->",
                  None if delta1(j, head, "frozen") is None else float(delta1(j, head, "frozen")))
