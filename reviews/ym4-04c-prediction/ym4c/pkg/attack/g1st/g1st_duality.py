# Finding S3 arithmetic: the six-plaquette duality floor, and what it does to C10b/C10c power.
# Exact Fractions with the interval exp of g1st_constants.py. Not an engine.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("k", os.path.join(os.path.dirname(os.path.abspath(__file__)), "g1st_constants.py"))
from fractions import Fraction as F
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    k = importlib.util.module_from_spec(spec); spec.loader.exec_module(k)
I, exp_q, fmt, EM1 = k.I, k.exp_q, k.fmt, k.EM1
kap = F(1, 4)
# (a) j e^{4 kappa} <= e^{kappa (3j+1)} for j=1..6 at kappa=1/4, i.e. e^{3(j-1)/4} >= j
for j in range(1, 7):
    lhs = exp_q(F(3 * (j - 1), 4))
    print("j=%d: e^{3(j-1)/4} lower %.6f >= %d: %s" % (j, float(lhs.lo), j, lhs.lo >= j))
# smallest kappa for which the j=2 inequality holds: e^{3 kappa} >= 2  <=> kappa >= ln2/3
print("j=2 needs kappa >= ln(2)/3 ~ %.6f (display only)" % (0.6931471805599453 / 3))
# (b) C10: every-representation floor = natural norm 12|s| e^{4kappa}; ratio e^{-4kappa}
# (c) C10b: natural delta_out/delta_in in v2 bracket [1.516e-4, 1.517e-4]; ratio to c(delta_in) at s=1/2000
e15 = exp_q(F(3, 2)); din = 12 * e15 / 2000
c_fr = k.first(k.c_frozen(din)); c_st = k.first(k.c_star(din)); c_sh = k.first(k.c_sharp(din))
r = I(F("1.516e-4"), F("1.517e-4"))
for nm, c in (("frozen c", c_fr), ("route A c*", c_st), ("route B c#", c_sh)):
    q = I(r.lo / c.hi, r.hi / c.lo)
    print("C10b s=1/2000 natural/(c delta_in) with %s: %s, slack %s" % (nm, fmt(q, 6), fmt(I(1 / q.hi, 1 / q.lo), 6)))
pl = I(F("4.00e-7"), F("4.01e-7")); q = I(pl.lo / (c_fr.hi * din.hi), pl.hi / (c_fr.lo * din.lo))
print("C10b frozen projection bound/(c delta_in): %s, slack %s" % (fmt(q, 6), fmt(I(1 / q.hi, 1 / q.lo), 6)))
# (d) C10c: v2 brackets for delta_out^nat/delta_in
e25 = exp_q(F(5, 2))
for s, br in ((8192, (F("0.0557553"), F("0.0558098"))), (65536, (F("0.0557791"), F("0.0557860")))):
    din = 24 * e25 / s
    for nm, c in (("frozen c", k.first(k.c_frozen(din))), ("route A c*", k.first(k.c_star(din))), ("route B c#", k.first(k.c_sharp(din)))):
        q = I(br[0] / c.hi, br[1] / c.lo)
        print("C10c s=1/%d natural/(c delta_in) with %s: %s, slack %s" % (s, nm, fmt(q, 6), fmt(I(1 / q.hi, 1 / q.lo), 6)))
