# Does each displayed bracket in G1-a 4.14 and G1-b 4.13/4.14 contain the exact enclosure over its delta bracket?
import os, io, contextlib, importlib.util
from fractions import Fraction as F
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("k", os.path.join(here, "g1st_constants.py"))
with contextlib.redirect_stdout(io.StringIO()):
    k = importlib.util.module_from_spec(spec); spec.loader.exec_module(k)
I, first, EM1 = k.I, k.first, k.EM1
def over(fn, a, b):
    lo = first(fn(I(F(a)))).lo; hi = first(fn(I(F(b)))).hi
    return lo, hi
tp = lambda d: 2 * k.dprime(d)
cf, cs, cb, ch = k.c_frozen, k.c_star, k.c_B, k.c_sharp
e15 = k.exp_q(F(3, 2))
rows = [
 # (source, quantity, fn, delta_lo, delta_hi, shown_lo, shown_hi)
 ("A", "C07 2d'", tp, "0.011044", "0.011045", "0.0223332", "0.0223354"),
 ("A", "C07 c", cf, "0.011044", "0.011045", "0.4450429", "0.4450509"),
 ("A", "C08 2d'", tp, "9.42e-6", "9.45e-6", "1.88401e-5", "1.89002e-5"),
 ("A", "C08 c", cf, "9.42e-6", "9.45e-6", "0.3679383", "0.3679386"),
 ("A", "C10b 1/2000 2d'", tp, "0.026890", "0.026891", "0.0552457", "0.0552479"),
 ("A", "C10b 1/2000 c", cf, "0.026890", "0.026891", "0.5950951", "0.5951069"),
 ("A", "C10b 1/4096 2d'", tp, "0.013129", "0.013131", "0.0266050", "0.0266092"),
 ("A", "C10b 1/4096 c", cf, "0.013129", "0.013131", "0.4617347", "0.4617511"),
 ("A", "C14 1/64 2d'", tp, "2.0347e-3", "2.0348e-3", "4.07768e-3", "4.07789e-3"),
 ("A", "C14 1/64 c", cf, "2.0347e-3", "2.0348e-3", "0.3808522", "0.3808529"),
 ("A", "C12 2d'", tp, "0.072645", "0.072646", "0.1562374", "0.1562398"),
 ("A", "C12 c*", cs, "0.072645", "0.072646", "0.3727262", "0.3727351"),
 ("A", "C11 2d'", tp, "0.10165", "0.10166", "0.2250522", "0.2250767"),
 ("A", "C11 c*", cs, "0.10165", "0.10166", "0.7717123", "0.7719306"),
 ("B", "C07 c", cf, "0.011044", "0.011045", "0.4450430", "0.4450509"),
 ("B", "C07 c_B", cb, "0.011044", "0.011045", "0.4447292", "0.4447370"),
 ("B", "C07 2d'", tp, "0.011044", "0.011045", "0.0223333", "0.0223353"),
 ("B", "C08 c=c_B", cb, "9.42e-6", "9.45e-6", "0.3679383", "0.3679386"),
 ("B", "C10b 1/2000 c", cf, "0.026890", "0.026891", "0.595095", "0.595107"),
 ("B", "C10b 1/2000 c_B", cb, "0.026890", "0.026891", "0.587932", "0.587943"),
 ("B", "C10b 1/2000 c#", ch, "0.026890", "0.026891", "0.509131", "0.509143"),
 ("B", "C10b 1/2000 2d'", tp, "0.026890", "0.026891", "0.0552458", "0.0552479"),
 ("B", "C10b 1/4096 c", cf, "0.013129", "0.013131", "0.461734", "0.461752"),
 ("B", "C10b 1/4096 c_B", cb, "0.013129", "0.013131", "0.461150", "0.461167"),
 ("B", "C10b 1/4096 c#", ch, "0.013129", "0.013131", "0.379284", "0.379301"),
 ("B", "C14 1/64 c_B", cb, "2.0347e-3", "2.0348e-3", "0.3808522", "0.3808529"),
]
bad = 0
for src, q, fn, a, b, sl, sh in rows:
    lo, hi = over(fn, a, b)
    ok = F(sl) <= lo and hi <= F(sh)
    if not ok: bad += 1
    print("%s %-18s exact [%.10f, %.10f] shown [%s, %s] %s" % (src, q, float(lo), float(hi), sl, sh, "contains" if ok else "DOES NOT CONTAIN"))
# route B prose: c_B - e^-1 over C08 in [5.892e-5, 5.912e-5]
lo = first(cb(I(F("9.42e-6")))).lo - EM1.hi; hi = first(cb(I(F("9.45e-6")))).hi - EM1.lo
ok = F("5.892e-5") <= lo and hi <= F("5.912e-5")
print("B c_B-e^-1 at C08 exact [%.9g, %.9g] shown [5.892e-5, 5.912e-5] %s" % (float(lo), float(hi), "contains" if ok else "DOES NOT CONTAIN"))
bad += (not ok)
print("brackets that do not contain the exact enclosure:", bad)
