from fractions import Fraction as Fr
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4-04c/polymer-norm")
from window2 import least_a, SMALL
from delta_scan3 import up, elo, KAPPA
from derive_estimates import eps6_upper

def bestT(beta, head, imax):
    eps = up(eps6_upper(beta)); bestv = None
    for i in range(0, imax+1):
        b = KAPPA + Fr(i, 64)
        a = least_a(eps, b, head)
        if a is None:
            if bestv is not None: break
            continue
        T = Fr(8489, 10000) * 12 * a / elo(8 * b)
        if bestv is None or T < bestv[0]:
            bestv = (T, a, b)
    return bestv
for beta in (Fr(1,4000), Fr(1,2000), Fr(1,1000), Fr(1,700)):
    c = beta**4/128 - beta**6/768 + beta**8/1536 - Fr(467,2211840)*beta**10
    for imax in (128, 320):
        r = bestT(beta, SMALL, imax)
        print(beta, imax, float(r[0]/c), r[2])
