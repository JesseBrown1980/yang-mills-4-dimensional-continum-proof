#!/usr/bin/env python3
"""YM4-04C v2 repair lane: C10c constants from the analytic leading order only (no SU(2) integral is computed).

Input: one Y per next-coarse plaquette P'', R(Y) = s chi(rect_b) chi(rect_t), #Y = 10 (8 line links, 2 arm links).
delta_in = 24 s e^{10 kappa} (sup|R| = 4s, 6 Y per line link). X := chi(A pi) chi(pi^-1 B) in [-4,4], pi Haar on the arm.
Leading order (Schur): E_pi[X] = chi(V_P'')/2.  f(chi) := log E_pi[e^{sX}] in [s E X, s E X + 8 s^2] (Jensen, Hoeffding's lemma).
Natural output R(dP'') = f - (max f + min f)/2: delta_out^nat = 6 e^{4 kappa} osc(f)/2 in 6e[s - 4s^2, s + 4s^2].
Every decomposition: delta_out >= 6 e^{4 kappa} |c_P| / E|chi|, c_P = E[f chi] in [s/2 - 4 s^2 E|chi|, s/2 + 4 s^2 E|chi|].
G1's c(delta) = e^delta [e^{-4 kappa} + max_{n>=4} (e^{-(kappa/2 - 2 delta') n} - e^{-kappa n/2})], delta' = delta e^delta.
"""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/v2-checks")
from kp_exact import exp_lo, exp_hi, up, dn
K = Fr(1, 4)
def E(y): return (exp_lo(y), exp_hi(y))          # (lo, hi) of e^y, 160-bit outward dyadic rounding
def mul(a, b):
    c = [a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1]]; return (min(c), max(c))
EABS_HI = Fr(8489, 10000)   # E|chi_1/2| = 8/(3 pi) <= 8489/10000 (pi >= 3.1416 > 8/(3*0.8489))
assert Fr(8, 3) / EABS_HI < Fr(31416, 10000)
def c_of(dlo, dhi, nmax=400):
    """enclosure of c(delta) for delta in [dlo, dhi]; h(n) = e^{-u n} - e^{-v n} with u = kappa/2 - 2 delta'."""
    dplo = dn(dlo * E(dlo)[0]); dphi = up(dhi * E(dhi)[1])
    ulo = K/2 - 2*dphi; uhi = K/2 - 2*dplo
    assert ulo > 0
    hlo = max(E(-uhi*n)[0] - E(-K*n/2)[1] for n in range(4, nmax + 1))
    hhi = max(E(-ulo*n)[1] - E(-K*n/2)[0] for n in range(4, nmax + 1))
    # beyond nmax: h(n) <= e^{-ulo n} <= e^{-ulo nmax}, far below the max (checked)
    assert E(-ulo*nmax)[1] < hlo
    em1 = E(-4*K)
    return (E(dlo)[0]*(em1[0] + hlo), E(dhi)[1]*(em1[1] + hhi)), (2*dplo, 2*dphi)
def f(x, d=7): return f"{float(x):.{d}e}"
if __name__ == "__main__":
    r = E(Fr(-3, 2)); lead = (r[0]/4, r[1]/4)
    print("leading ratio e^{-3/2}/4 in [", f(lead[0], 9), ",", f(lead[1], 9), "]")
    for s in (Fr(1, 8192), Fr(1, 65536)):
        e10 = E(10*K); din = (dn(24*s*e10[0]), up(24*s*e10[1]))
        (clo, chi), (t2lo, t2hi) = c_of(*din)
        Ck = t2hi <= K/2
        e1 = E(1)
        nat = (6*e1[0]*(s - 4*s*s), 6*e1[1]*(s + 4*s*s))
        ratio_nat = (nat[0]/din[1], nat[1]/din[0])
        cP_lo = s/2 - 4*s*s*EABS_HI
        lb = 6*e1[0]*cP_lo/EABS_HI          # valid lower bound (E|chi| <= EABS_HI)
        cdin = (clo*din[0], chi*din[1])
        print(f"s={s}: delta_in in [{f(din[0])},{f(din[1])}]; 2delta' in [{f(t2lo)},{f(t2hi)}]; C_k MET={Ck}; c(delta_in) in [{f(clo)},{f(chi)}]")
        print(f"    natural delta_out in [{f(nat[0])},{f(nat[1])}]; delta_out^nat/delta_in in [{f(ratio_nat[0])},{f(ratio_nat[1])}]")
        print(f"    (e^-1.5/4)(1-4s) = {f(lead[0]*(1-4*s),9)}, (e^-1.5/4)(1+4s) = {f(lead[1]*(1+4*s),9)}")
        print(f"    every-decomposition lower bound >= {f(lb)}; lower bound/delta_in >= {f(lb/din[1])}; lower bound/(c delta_in) <= {f(6*e1[1]*(s/2+4*s*s*EABS_HI)/(Fr(8,3)/Fr(31416,10000))/cdin[0])} (upper side uses E|chi| >= 8/(3*3.1416))")
        print(f"    slack c/(natural ratio) in [{f(clo/ratio_nat[1],4)},{f(chi/ratio_nat[0],4)}]; slack c*delta_in/lower_bound <= {f(cdin[1]/lb,4)}")
