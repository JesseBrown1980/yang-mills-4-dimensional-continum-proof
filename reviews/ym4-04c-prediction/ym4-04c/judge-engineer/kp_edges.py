import sys
sys.path.insert(0, '.')
from kp_check import *

def C0all(beta, counts):
    e = eps6(beta)
    out = []
    for i in range(129):
        b = Dd(1) / 4 + Dd(i) / 64
        a = Dd(0); ok = False
        for _ in range(400):
            x = e * (2 * a + b).exp()
            s = S(x, counts)
            if s is None or s > Dd(1) / 4: break
            if s <= a * (1 + Dd(10) ** -40): ok = True; break
            a = s
        if ok: out.append((a, b))
    return out

def met(beta, counts, dmax=None):
    o = C0all(beta, counts)
    if not o: return False
    if dmax is None: return True
    d1 = min(12 * a * (-4 * (b - KAP)).exp() for a, b in o)
    return d1 <= dmax

def edge(lo, hi, counts, dmax=None):
    # integer grid in units of 1e-5
    lo = int(lo * 100000); hi = int(hi * 100000)
    assert met(Dd(lo) / 100000, counts, dmax) and not met(Dd(hi) / 100000, counts, dmax)
    while hi - lo > 1:
        m = (lo + hi) // 2
        if met(Dd(m) / 100000, counts, dmax): lo = m
        else: hi = m
    return lo, hi

# wall
def bis(f, lo, hi, it=60):
    lo = Dd(lo); hi = Dd(hi)
    for _ in range(it):
        m = (lo + hi) / 2
        if f(m) < 1: lo = m
        else: hi = m
    return lo
print("beta_wall(1/4) ~", bis(lambda b: MU * Dd('0.25').exp() * eps6(b), '0.02', '0.025', 40))
print("mu eps6 = 1 at ~", bis(lambda b: MU * eps6(b), '0.025', '0.03', 40))
print("mu e^1/4 eps6 at 1/18:", MU * Dd('0.25').exp() * eps6(Dd(1) / 18))
print("crude edge (1e-5 units):", edge(0.018, 0.020, crude))
print("headfree edge:", edge(0.020, 0.022, headfree))
print("measured edge:", edge(0.020, 0.022, measured))
# delta_crit
lo, hi = Dd('0.049'), Dd('0.050')
print("c(0.049)", cfun(lo), "c(0.050)", cfun(hi))
for _ in range(40):
    m = (lo + hi) / 2
    if cfun(m) < 1: lo = m
    else: hi = m
print("delta_crit ~", lo)
print("crude induction edge (delta1<=49/1000):", edge(0.013, 0.015, crude, Dd(49) / 1000))
print("headfree induction edge (delta1<=49/1000):", edge(0.018, 0.0205, headfree, Dd(49) / 1000))
print("measured induction edge (delta1<=49/1000):", edge(0.018, 0.0205, measured, Dd(49) / 1000))
print("measured induction edge (delta1<delta_crit):", edge(0.018, 0.0205, measured, lo))
def P10(b):
    return b**4/128 - b**6/768 + b**8/1536 - 467*b**10/2211840
for beta in [Dd(1)/4000, Dd(1)/2000, Dd(1)/1000, Dd(1)/700, Dd(1)/100]:
    o = C0all(beta, measured)
    T = min(Dd('0.8489') * 12 * a * (-8 * b).exp() for a, b in o)
    print("C09 beta", beta, "T/P10 %.4e" % (T / P10(beta)))
