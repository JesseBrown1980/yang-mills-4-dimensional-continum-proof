# G1 structure-lens scratch check. Exact Fractions, outward dyadic rounding at 2^-P.
# Not an engine, not evidence. Floats only in fmt() for display.
from fractions import Fraction as F
import math
P = 220
SC = F(1, 2**P)
def dn(x):  # round down to dyadic
    return F(math.floor(x * 2**P), 2**P)
def up(x):
    return F(math.ceil(x * 2**P), 2**P)
class I:
    __slots__ = ("lo", "hi")
    def __init__(s, lo, hi=None):
        if hi is None: hi = lo
        assert lo <= hi, (lo, hi)
        s.lo, s.hi = F(lo), F(hi)
    def __add__(a, b):
        b = b if isinstance(b, I) else I(b); return I(dn(a.lo + b.lo), up(a.hi + b.hi))
    __radd__ = __add__
    def __neg__(a): return I(-a.hi, -a.lo)
    def __sub__(a, b):
        b = b if isinstance(b, I) else I(b); return a + (-b)
    def __rsub__(a, b): return I(b) - a
    def __mul__(a, b):
        b = b if isinstance(b, I) else I(b)
        ps = [a.lo*b.lo, a.lo*b.hi, a.hi*b.lo, a.hi*b.hi]
        return I(dn(min(ps)), up(max(ps)))
    __rmul__ = __mul__
    def __truediv__(a, b):
        b = b if isinstance(b, I) else I(b)
        assert b.lo > 0 or b.hi < 0
        return a * I(dn(1/b.hi) if b.hi > 0 else dn(1/b.hi), up(1/b.lo)) if b.lo > 0 else NotImplemented
def exp_q(x):
    """enclosure of e^x for rational x"""
    x = F(x); k = 0
    while abs(x) > F(1, 64): x /= 2; k += 1
    s = F(0); t = F(1); n = 0
    while True:
        s += t; n += 1; t = t * x / n
        if abs(t) < SC / 2**40: break
    rem = abs(t) * 2  # |y|<=1/64: tail <= |t|/(1-|y|) < 2|t|
    lo, hi = dn(s - rem), up(s + rem)
    for _ in range(k):
        lo, hi = dn(lo*lo), up(hi*hi)
    return I(lo, hi)
def exp_i(x):
    return I(exp_q(x.lo).lo, exp_q(x.hi).hi)
kap = F(1, 4)
EM1 = exp_q(-1)
def dprime(d):  # d interval
    return d * exp_i(d)
def fmt(x, nd=10):
    return "[%.*g, %.*g]" % (nd, float(x.lo), nd, float(x.hi))
def maxscan(term, decay_rate, best_needed=None, n0=4):
    """max over integer n>=n0 of term(n) (interval), with term(n) <= e^{-decay_rate.lo*n} as tail cap."""
    best = None; n = n0; arg = None
    while True:
        t = term(n)
        if best is None or t.lo > best.lo: best_lo = t.lo
        if best is None:
            best = I(t.lo, t.hi); arg = n
        else:
            if t.hi > best.hi or t.lo > best.lo:
                if t.lo > best.lo: arg = n
                best = I(max(best.lo, t.lo), max(best.hi, t.hi))
        cap = exp_q(-decay_rate.lo * (n + 1)).hi if decay_rate.lo > 0 else F(10)
        if decay_rate.lo > 0 and cap < best.lo and n > 8:
            return best, arg
        n += 1
        if n > 4000: raise RuntimeError("scan")
def c_frozen(d):
    dp = dprime(d)
    r = I(kap/2) - 2*dp
    assert r.lo > 0
    term = lambda n: exp_i(-(r*n)) - exp_q(-kap*n/2)
    m, arg = maxscan(term, r)
    return exp_i(d) * (EM1 + m), arg
def c_star(d):  # route A, kappa<=1/4, 2d'<=kappa
    dp = dprime(d)
    r = I(kap) - 2*dp
    assert r.lo > 0
    e2 = exp_i(d + 2*dp - F(5, 4))
    term = lambda f: exp_i(-(r*f)) - exp_q(-kap*f)
    m, arg = maxscan(term, r)
    e3 = exp_i(d) * m
    lo = max(EM1.lo, e2.lo, e3.lo); hi = max(EM1.hi, e2.hi, e3.hi)
    return I(lo, hi), arg
def c_B(d):
    dp = dprime(d)
    return exp_i(d + 16*dp - 1)
def c_sharp(d):
    dp = dprime(d)
    r = I(kap/2) - 2*dp
    def g(n):
        v = exp_i(-(r*n)) - exp_q(-kap*n/2)
        if n >= 9: v = v + exp_q(-kap*(n+1)/2)
        return v
    m, arg = maxscan(g, r)
    e = exp_i(d) * m
    return I(max(EM1.lo, e.lo), max(EM1.hi, e.hi)), arg
def hull(f, a, b):
    """f nondecreasing in d: enclosure over [a,b]"""
    x, _ = f(I(a)) if isinstance(f(I(a)), tuple) else (f(I(a)), None)
    y = f(I(b)); y = y[0] if isinstance(y, tuple) else y
    return I(x.lo, y.hi)
def first(v): return v[0] if isinstance(v, tuple) else v
Q = lambda s: F(s)
print("e^-1", fmt(EM1, 12))
e15 = exp_q(F(3, 2)); e25 = exp_q(F(5, 2))
pts = {
  "C07 crude 1/100 bracket": (Q("0.011044"), Q("0.011045")),
  "C07 point 0.0110444507": (Q("0.0110444507"), Q("0.0110444507")),
  "C08 refined 1/100": (Q("9.42e-6"), Q("9.45e-6")),
  "C10b s=1/2000 (12e^{3/2}/2000)": ((12*e15/2000).lo, (12*e15/2000).hi),
  "C10b s=1/4096": ((12*e15/4096).lo, (12*e15/4096).hi),
  "C10c s=1/8192 (24e^{5/2}/8192)": ((24*e25/8192).lo, (24*e25/8192).hi),
  "C10c s=1/65536": ((24*e25/65536).lo, (24*e25/65536).hi),
  "C13 49/1000": (Q("0.049"), Q("0.049")),
  "C13 1/20": (Q("0.05"), Q("0.05")),
  "C14 refined 1/64": (Q("2.0347e-3"), Q("2.0348e-3")),
}
for name, (a, b) in pts.items():
    dA = I(a, b)
    tp = 2*dprime(dA)
    cf = I(first(c_frozen(I(a))).lo, first(c_frozen(I(b))).hi)
    cs = I(first(c_star(I(a))).lo, first(c_star(I(b))).hi)
    cb = I(c_B(I(a)).lo, c_B(I(b)).hi)
    ch = I(first(c_sharp(I(a))).lo, first(c_sharp(I(b))).hi)
    print(name, "| delta", fmt(dA, 9), "| 2d'", fmt(tp, 8), "| c", fmt(cf, 8), "| c*", fmt(cs, 8), "| c_B", fmt(cb, 8), "| c#", fmt(ch, 8))
for name, (a, b) in {"C11 crude 1/64": (Q("0.10165"), Q("0.10166")), "C12 head-free 1/50": (Q("0.072645"), Q("0.072646"))}.items():
    tp = 2*dprime(I(a, b))
    cs = I(first(c_star(I(a))).lo, first(c_star(I(b))).hi)
    print(name, "| 2d'", fmt(tp, 8), "| c*", fmt(cs, 8), "(frozen c undefined: 2d'>1/8)")
# edges on the stated grids
def edge(name, pred_hold, a, b):
    print(name, a, "holds:", pred_hold(a), "|", b, "holds:", pred_hold(b))
edge("C_k 2d'<=1/8", lambda d: (2*dprime(I(Q(d)))).hi <= F(1, 8), "0.058923670", "0.058923671")
edge("2d'<=1/4", lambda d: (2*dprime(I(Q(d)))).hi <= F(1, 4), "0.111780108", "0.111780109")
edge("delta_crit frozen c<1 (upper)", lambda d: first(c_frozen(I(Q(d)))).hi < 1, "0.049617491", "0.049617492")
print("   c lower at 0.049617492 >= 1:", first(c_frozen(I(Q("0.049617492")))).lo >= 1)
edge("delta_crit* c*<1 (upper)", lambda d: first(c_star(I(Q(d)))).hi < 1, "0.109530694", "0.109530695")
print("   c* lower at 0.109530695 >= 1:", first(c_star(I(Q("0.109530695")))).lo >= 1, "argmax f", c_star(I(Q("0.109530695")))[1])
x = c_star(I(Q("0.072094"))); y = c_star(I(Q("0.072095")))
dA = I(Q("0.072094")); eQ = exp_i(dA)  # recompute the off channel alone
def offchan(d):
    dp = dprime(d); r = I(kap) - 2*dp
    e2 = exp_i(d + 2*dp - F(5, 4))
    m, arg = maxscan(lambda f: exp_i(-(r*f)) - exp_q(-kap*f), r)
    e3 = exp_i(d) * m
    return I(max(e2.lo, e3.lo), max(e2.hi, e3.hi)), arg
oa = offchan(I(Q("0.072094"))); ob = offchan(I(Q("0.072095")))
print("c* = e^-1 edge: off channel e^d Q at 0.072094", fmt(oa[0], 10), "<= e^-1:", oa[0].hi < EM1.lo, "| at 0.072095", fmt(ob[0], 10), "> e^-1:", ob[0].lo > EM1.hi, "argmax f", ob[1])
edge("delta_crit(c_B) c_B<1", lambda d: c_B(I(Q(d))).hi < 1, "0.0558087801", "0.0558087802")
print("   c_B lower at ...802 >= 1:", c_B(I(Q("0.0558087802"))).lo >= 1)
edge("delta_crit(c#) c#<1", lambda d: first(c_sharp(I(Q(d)))).hi < 1, "0.0577661141", "0.0577661142")
print("   c# lower at ...142 >= 1:", first(c_sharp(I(Q("0.0577661142")))).lo >= 1)
edge("c# = e^-1 (upper <= e^-1 hi)", lambda d: first(c_sharp(I(Q(d)))).hi <= EM1.hi, "0.0116995481", "0.0116995482")
def f89(d):
    dp = dprime(I(Q(d))); r = I(kap/2) - 2*dp
    f8 = exp_i(-(r*8)) - exp_q(-4*kap); f9 = exp_i(-(r*9)) - exp_q(-kap*9/2)
    return f8 - f9
print("delta_eq: f(8)-f(9) at 0.0070256343", fmt(f89("0.0070256343"), 6), "at 0.0070256344", fmt(f89("0.0070256344"), 6))
# C16 delta_20 with frozen c at the upper end of C07
d1 = I(Q("0.011045")); cc = first(c_frozen(d1))
d20 = I(dn(cc.lo**19 * d1.lo), up(cc.hi**19 * d1.hi))
pi_lo, pi_hi = F(314159265358979, 10**14), F(314159265358980, 10**14)
print("C16 delta_20 <= c^19 delta_1 at delta_1=0.011045:", fmt(d20, 7), "osc<=(512/e)delta_20:", "%.6g" % float(up(512 * EM1.hi * d20.hi)))
# Lemma 4.22 constant and the existence floor of finding S4
c422 = I(dn(F(16)/(3*pi_hi) * EM1.lo), up(F(16)/(3*pi_lo) * EM1.hi))
print("(16/(3pi)) e^-1 =", fmt(c422, 8), "< 0.62454:", c422.hi < F("0.62454"))
floor = I(dn(3*pi_lo/16 * EM1.lo), up(3*pi_hi/16 * EM1.hi))
print("existence floor (3pi/16) e^-4kappa =", fmt(floor, 8))
# Wilson objects' route-A per-root factors at C07's upper delta (route A section 4.12)
dp = dprime(I(Q("0.011045")))
q22 = exp_q(-F(3,4)) * (exp_i(4*dp) - 1); q40 = EM1 * (exp_i(8*dp) - 1)
print("Wilson q(2,2), q(4,0) at delta=0.011045:", fmt(q22, 6), fmt(q40, 6))
# route-B multi-object share at C08
cbs = I(c_B(I(Q("9.42e-6"))).lo - EM1.hi, c_B(I(Q("9.45e-6"))).hi - EM1.lo)
print("c_B - e^-1 over C08 bracket:", fmt(cbs, 6))
