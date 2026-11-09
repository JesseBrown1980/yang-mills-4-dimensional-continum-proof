# n7_precision_recheck.py -- the same reads at a second working precision (P = 480 instead of 640; at P = 320 the fixed-point powers x^49 keep only about 36 bits and the root certification declines, rigorously),
# and E3 at the flat-range end written out by hand at f = 7, as a consistency check of this lane's code.
import sys
sys.path.insert(0, '/mnt/c/tmp/opus55/ym4-04c-gattack/work/L5-numbers')
import ilib as L
L.setP(480)
from ilib import rat, add, sub, mul, muli, neg, exp_iv, exp_point, fmti, inside
import g1lib as G
import polylib as PL

for (p, q) in [(78733761, 10 ** 9), (78733762, 10 ** 9), (114846768, 10 ** 9)]:
    d = rat(p, q)
    c, E2, E3, fa, un, fs = G.cfin(d)
    dp, lm = G.lam_iv(d)
    g7 = sub(exp_iv(muli(neg(sub(rat(1, 4), lm)), 7)), exp_point(-(7 << (L.P - 2))))
    E3_7 = mul(exp_iv(sub(d, rat(1, 8))), g7)
    print('RECHECK|delta=' + str(p) + '/' + str(q) + '|cfin=' + fmti(c, 12) + '|E3=' + fmti(E3, 12) + '|argmax=' + str(fa) + '|E3_at_f7=' + fmti(E3_7, 12) + '|P=480|json=0')
for (b, head) in [((2074, 100000), 'C03'), ((2075, 100000), 'C03'), ((1767, 100000), 'crude'), ((1768, 100000), 'crude'), ((1, 64), 'crude'), ((1, 100), 'crude')]:
    A = PL.A_of(PL.eps6(*b), 0)
    rt = PL.least_root(A, PL.coef_list(PL.HEADS[head]))
    print('RECHECK|beta=' + str(b[0]) + '/' + str(b[1]) + '|head=' + head + '|delta1=' + fmti((6 * rt[0], 6 * rt[1]), 12) + '|P=480|json=0')
