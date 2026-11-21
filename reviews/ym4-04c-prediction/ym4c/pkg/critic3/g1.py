import sys
sys.path.insert(0, ".")
from spot import *
K = Fr(1, 4)
a, b = Fr(114846768, 10**9), Fr(114846769, 10**9)
print("delta_crit: lambda^+(a) <= 1/4:", lam_iv(a)[1] <= K, "; lambda^-(b) > 1/4:", lam_iv(b)[0] > K)
def twodp(d):
    e = exp_iv(d); return D(2*d*e[0]), U(2*d*e[1])
fa, fb = Fr(111780108, 10**9), Fr(111780109, 10**9)
print("fallback: 2d'^+(a) <= 1/4:", twodp(fa)[1] <= K, "; 2d'^-(b) > 1/4:", twodp(fb)[0] > K)
e1 = exp_iv(-1)
for d, lo, hi, farg in [(Fr(1,10), "0.611173", "0.611174", 9), (Fr(11,100), "0.811310", "0.811311", 13),
                        (a, "0.989898", "0.989899", None)]:
    l, h, arg, parts = cfin_iv(d)
    show(f"c_fin({float(d)}) argmax f={arg} (frozen f={farg})", (l, h), Fr(lo), Fr(hi))
for d in (Fr(49,1000), Fr(1,20), Fr(78733761, 10**9)):
    l, h, arg, parts = cfin_iv(d)
    print(f"c_fin({float(d)}): [{float(l):.12f}, {float(h):.12f}], object channel upper {float(max(parts[1][1], parts[2][1])):.10f} <= e^-1 lower {float(e1[0]):.10f}: {max(parts[1][1], parts[2][1]) <= e1[0]}")
d = Fr(78733762, 10**9)
l, h, arg, parts = cfin_iv(d)
print(f"c_fin(0.078733762): object channel lower {float(max(parts[1][0], parts[2][0])):.10f} > e^-1 upper {float(e1[1]):.10f}: {max(parts[1][0], parts[2][0]) > e1[1]} at f={arg}")
# fallback factor edge 0.077320139 under 2d' <= kappa: entries with lambda replaced by 2d'
def cfin_fb(d):
    ll, lh = twodp(d)
    best_l = Fr(0); best_h = Fr(0); f = 4
    while True:
        gl = exp_iv(-(K - ll) * f)[0] - exp_iv(-K * f)[1]; gh = exp_iv(-(K - lh) * f)[1] - exp_iv(-K * f)[0]
        best_l = max(best_l, gl); best_h = max(best_h, gh)
        if exp_iv(-(K - lh) * f)[1] <= best_l: break
        f += 1
    pre = exp_iv(d - K/2)
    t2 = (exp_iv(d + ll - 5*K)[0], exp_iv(d + lh - 5*K)[1])
    return max(t2[0], D(pre[0]*best_l)), max(t2[1], U(pre[1]*best_h))
for d in (Fr(77320139, 10**9), Fr(77320140, 10**9)):
    l, h = cfin_fb(d)
    print(f"fallback object channel at {float(d)}: [{float(l):.10f}, {float(h):.10f}] vs e^-1 [{float(e1[0]):.10f},{float(e1[1]):.10f}]")
# C16
d1p = Fr(55223, 10**7)
e19 = exp_iv(-19)
d20 = U(e19[1] * d1p)
osc = U(512 * e1[1] * d20)
print(f"C16: delta_20 <= {float(d20):.6e} (frozen <= 3.0940e-11): {d20 <= Fr(30940, 10**15)}; osc <= {float(osc):.6e} (frozen <= 5.828e-9): {osc <= Fr(5828, 10**12)}")
# Lemma 4.22 constant and the coupling cap
c = U(16 * e1[1] / (3 * PI[0]))
print(f"(16/(3pi))e^-1 <= {float(c):.8f} < 0.62454: {c < Fr(62454, 10**5)}; times delta_crit^+: {float(U(c*b)):.8f} < 0.07173: {U(c*b) < Fr(7173,10**5)}")
# C10b
for s, lo, hi in [(Fr(1,2000), "4.077e-6", "4.078e-6")]:
    c0 = c0_iv(4*s); lc = ln1p_iv(c0[0]-1)[0], ln1p_iv(c0[1]-1)[1]
    e = exp_iv(1)
    dout = (D(3*e[0]*lc[0]), U(3*e[1]*lc[1]))
    show(f"C10b delta_out s={s}", dout, Fr(lo), Fr(hi))
    e15 = exp_iv(Fr(3,2)); din = (D(12*s*e15[0]), U(12*s*e15[1]))
    show("C10b delta_in", din, Fr(26890, 10**6), Fr(26891, 10**6))
    r = (D(dout[0]/din[1]), U(dout[1]/din[0]))
    show("C10b delta_out/delta_in", r, Fr(1516, 10**7), Fr(1517, 10**7))
    sl = (D(e1[0]*din[0]/dout[1]), U(e1[1]*din[1]/dout[0]))
    show("C10b slice slack", sl, Fr(24261, 10), Fr(24262, 10))
    ll = lam_iv(din[0])[0], lam_iv(din[1])[1]
    pr = (D(exp_iv(din[0]-1)[0]*(exp_iv(2*ll[0])[0]-1)*din[0]/dout[1]), U(exp_iv(din[1]-1)[1]*(exp_iv(2*ll[1])[1]-1)*din[1]/dout[0]))
    show("C10b per-root/delta_out", pr, Fr(28907, 100), Fr(28908, 100))
# C10c per-root factor at s = 1/65536
s = Fr(1, 65536)
e25 = exp_iv(Fr(5,2)); din = (D(24*s*e25[0]), U(24*s*e25[1]))
show("C10c delta_in s=1/65536", din, Fr(44613, 10**7), Fr(44614, 10**7))
ll = lam_iv(din[0])[0], lam_iv(din[1])[1]
show("C10c lambda", ll, Fr(89526, 10**7), Fr(89527, 10**7))
prf = (exp_iv(din[0] - Fr(3,2) + 2*ll[0])[0], exp_iv(din[1] - Fr(3,2) + 2*ll[1])[1])
e = exp_iv(1)
nat = (D(6*e[0]*(s - 4*s*s)), U(6*e[1]*(s + 4*s*s)))
pr = (D(prf[0]*din[0]/nat[1]), U(prf[1]*din[1]/nat[0]))
show("C10c per-root/natural (from the DERIVED natural bracket)", pr, Fr(40902, 10**4), Fr(40908, 10**4))
sl = (D(e1[0]*din[0]/nat[1]), U(e1[1]*din[1]/nat[0]))
show("C10c slice slack", sl, Fr(65944, 10**4), Fr(65953, 10**4))
