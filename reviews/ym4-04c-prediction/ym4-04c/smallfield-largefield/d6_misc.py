import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from ri import I, log_i, dec
import d1_chessboard as d1
# D1 aligned tile: ratio (1 - T4(1-eps))/eps
def T4(x): return 8*x**4 - 8*x**2 + 1
for c in (Fr(63,65), Fr(255,257), Fr(1023,1025)):
    e = 1 - c
    r = (1 - T4(c)) / e
    print("cos=%s eps=%s ratio=%s = %s ; 16-40e+32e^2-8e^3=%s" % (c, e, r, dec(r,8), 16-40*e+32*e*e-8*e**3))
L4 = log_i(I(4))
for L in (4, 8):
    for beta in (16, 64, 256, 1024, 4096):
        Nf, t, h, v = d1.phi0(L, beta)
        es = v / beta
        ec = 16 * (v + L4) / beta
        ecc = 64 * v / beta
        print("L=%d beta=%d eps*=Phi0/beta=%s  eps'_union=16(Phi0+log4)/beta=%s  eps'_chess=64Phi0/beta=%s  ratio_union=%s" % (L, beta, es, ec, ecc, ec/es))
