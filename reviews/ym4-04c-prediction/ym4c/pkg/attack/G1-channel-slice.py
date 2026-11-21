# Add-on reads for the G1 channel attack: m >= 1 sharpening at the KP edge; slack of C10b and C10c under the slice bound.
# Fractions with outward-rounded exp enclosures, imported from G1-channel-checks.py's functions by exec of its header.
from fractions import Fraction as F
src = open("G1-channel-checks.py").read().split("out = []")[0]
exec(src)
K = KAPPA
for d in [F(1117801, 10**7), F(11178, 10**5)]:
    d1, d2 = dprime(d)
    print("delta", float(d), "2d' upper", float(2 * d2), "<= 1/4:", 2 * d2 <= K)
    if 2 * d2 < K:
        lo, hi, arg, ts = cstar_A(d, mmin=1)
        print("   c*_(m>=1) in [%.8f, %.8f], argf %s" % (float(lo), float(hi), arg))
# at 2d' = kappa exactly the m>=1 entry tends to e^{delta - kappa/2}; delta there is <= 0.111780108
print("e^{0.111780108 - 1/8} <=", float(ehi(F(111780108, 10**9) - K / 2)))

# C10b at s = 1/2000 and 1/4096: delta_in = 12 s e^{6k}; delta_out = 3 e^{4k} log c_0(4s) (the slice bound equals it)
def logc0_iv(x):
    # c_0(x) = sum_m (x/2)^{2m}/(m!(m+1)!) ; y := c_0 - 1 in [x^2/8, x^2/8 + x^4/192 * 2]; log(1+y) in [y - y^2/2, y]
    ylo = x * x / 8
    yhi = x * x / 8 + 2 * x**4 / 192
    return ylo - ylo * ylo / 2, yhi
for s in [F(1, 2000), F(1, 4096)]:
    din = (rdown(12 * s * elo(6 * K)), rup(12 * s * ehi(6 * K)))
    lc = logc0_iv(4 * s)
    dout = (rdown(3 * elo(4 * K) * lc[0]), rup(3 * ehi(4 * K) * lc[1]))
    cf = frozen_c(din[1])[1]; cfl = frozen_c(din[0])[0]
    ca = cstar_A(din[0])[0]
    cs = csharp_B(din[0])[0]
    print(f"C10b s={s}: delta_in [{float(din[0]):.10f},{float(din[1]):.10f}] delta_out [{float(dout[0]):.6e},{float(dout[1]):.6e}]")
    print(f"   slack c*delta_in/delta_out: frozen >= {float(cfl*din[0]/dout[1]):.1f}, route A >= {float(ca*din[0]/dout[1]):.1f}, route B c_sharp >= {float(cs*din[0]/dout[1]):.1f}")
# C10c: delta_in = 24 s e^{10k}; delta_out^nat <= 6 e^{4k} (s + 4 s^2) (the v2 row's bracket); the slice bound equals delta_out^nat
for s in [F(1, 8192), F(1, 65536)]:
    din = (rdown(24 * s * elo(10 * K)), rup(24 * s * ehi(10 * K)))
    doutU = rup(6 * ehi(4 * K) * (s + 4 * s * s))
    doutL = rdown(6 * elo(4 * K) * (s - 4 * s * s))
    cfl = frozen_c(din[0])[0]; cfh = frozen_c(din[1])[1]
    ca = cstar_A(din[0])[0]
    cs = csharp_B(din[0])[0]
    print(f"C10c s={s}: delta_in [{float(din[0]):.8f},{float(din[1]):.8f}] frozen c [{float(cfl):.7f},{float(cfh):.7f}] c*_A >= {float(ca):.7f} c_sharp >= {float(cs):.7f}")
    print(f"   slack against every decomposition (slice bound = natural): frozen >= {float(cfl*din[0]/doutU):.3f}, route A >= {float(ca*din[0]/doutU):.3f}, route B c_sharp >= {float(cs*din[0]/doutU):.3f}")
