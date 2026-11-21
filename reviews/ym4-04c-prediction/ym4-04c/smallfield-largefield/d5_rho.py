"""Derivation check: Gaussian line-map coarse transverse precision ratio rho_d(S), S = sin^2(kappa/2), k' = kappa e_1, polarization e_2."""
from fractions import Fraction as Fr
def rho4(S): return 4 / (4 + 24*S/(S+8) + 20*S/(S+24))
def rho3(S): return 2 / (4 + 12*S/(S+8))
def rho2(S): return Fr(1, 4)
prev = None
for t in (Fr(1,16), Fr(1,8), Fr(1,4), Fr(1,2), Fr(1)):
    S = t*t/(1+t*t)
    r = rho4(S)
    line = "t=%s S=%s rho4=%s (%.9f) 1-rho4=%.9f rho3=%s (%.6f)" % (t, S, r, r.numerator/r.denominator, 1-r.numerator/r.denominator, rho3(S), rho3(S).numerator/rho3(S).denominator)
    if prev is not None:
        line += " dev(t)/dev(2t)=%.6f" % ((1-r)/(1-prev[1])).__float__()
    print(line)
    prev = (t, r)
for S in (Fr(1,2), Fr(1)):
    print("S=%s rho4=%s rho3=%s" % (S, rho4(S), rho3(S)))
