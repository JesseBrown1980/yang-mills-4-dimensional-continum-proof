# n6_extra.py -- L5-numbers lane: two cross-reads by a second route.
# (a) W03's d = 3 corner at b = 8 by interval cosines (no Q(sqrt2) pairing);
# (b) C09's dyadic-resolution clause: 2^-48/alpha_-(theta_imin) at the six couplings.
import sys
sys.path.insert(0, '/mnt/c/tmp/opus55/ym4-04c-gattack/work/L5-numbers')
import ilib as L
from ilib import rat, add, sub, mul, div, muli, fmti, inside, dec, cos_iv, pi_iv, le_rat, scii
import polylib as PL

PI = pi_iv()
TWO_PI = muli(PI, 2)


def red(y):
    while y[0] > PI[1]:
        y = sub(y, TWO_PI)
    return y


for b in (2, 4, 8):
    Cp = (0, 0)
    for nn in range(b):
        u = sub(L.const(2), muli(cos_iv(red(div(add(PI, muli(TWO_PI, nn)), L.const(b)))), 2))
        for nr in range(b):
            v = sub(L.const(2), muli(cos_iv(red(div(muli(TWO_PI, nr), L.const(b)))), 2))
            Cp = add(Cp, div(L.const(1), add(u, v)))
    Cp = div(Cp, L.const(b))
    br = div(L.const(b), muli(Cp, 4))
    print('NUM|id=W03_corner_d3_by_cosines_b' + str(b) + '|b_times_r=' + fmti(br, 12) + '|json=0')
print('NUM|id=W03_corner_b8_exact_rational|value=' + fmti(rat(207812897, 453627584), 14) + '|json=0')

coef = PL.coef_list(PL.HEADS['C03'])
worst = None
for (b, i) in [((1, 4000), 194), ((1, 2000), 150), ((1, 1000), 105), ((1, 700), 83), ((1, 600), 73), ((1, 100), 0)]:
    eps = PL.eps6(*b)
    rt = PL.least_root(PL.A_of(eps, i), coef)
    res = div(rat(1, 1 << 48), (rt[0], rt[1]))
    ok = le_rat(res[1], dec('4.7e-6'))
    print('NUM|id=C09_dyadic_resolution_' + str(b[0]) + '_' + str(b[1]) + '|i=' + str(i) + '|alpha=' + scii((rt[0], rt[1]), 8) + '|2^-48/alpha=' + scii(res, 5) + '|ok=' + str(int(ok)) + '|json=0')
print('NUM|id=C09_four_times_4.7e-6|value=1.88e-5|le_1.9e-5=' + str(int(4 * 47 <= 190)) + '|json=0')
