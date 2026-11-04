# Claim 7: lattice-level reading of the first-difference rows on the 2x2 periodic torus, for all four groups, with exact group histograms against the exact Haar series.
# Haar: on a closed surface with F faces and Euler characteristic chi, Z = z^F sum_j d_j^chi t_j^F with t_j = I_{2j+1}/I_1. Here F=4, chi=0, so Z = z^4 sum_j t_j^4.
# Integers only.
import math

ORDER = 15


def red(n, d):
    assert d != 0
    if d < 0:
        n, d = -n, -d
    g = math.gcd(n, d) or 1
    return n // g, d // g


def qa(a, b):
    return red(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def qs(a, b):
    return red(a[0] * b[1] - b[0] * a[1], a[1] * b[1])


def qm(a, b):
    return red(a[0] * b[0], a[1] * b[1])


def smul(a, b):
    out = [(0, 1)] * ORDER
    for i, x in enumerate(a):
        if x[0]:
            for j, y in enumerate(b):
                if i + j >= ORDER:
                    break
                if y[0]:
                    out[i + j] = qa(out[i + j], qm(x, y))
    return out


def sdiv(a, b):
    assert b[0] == (1, 1)
    out = []
    for n in range(ORDER):
        acc = a[n]
        for j in range(n):
            acc = qs(acc, qm(out[j], b[n - j]))
        out.append(acc)
    return out


def spow(a, n):
    out = [(1, 1)] + [(0, 1)] * (ORDER - 1)
    for _ in range(n):
        out = smul(out, a)
    return out


def bessel_I(nu):
    """I_nu(beta) divided by (beta/2)^nu ... returned as a series in beta with the factor beta^nu kept, integers only."""
    s = [(0, 1)] * ORDER
    k = 0
    while nu + 2 * k < ORDER:
        s[nu + 2 * k] = red(1, 2 ** (nu + 2 * k) * math.factorial(k) * math.factorial(k + nu))
        k += 1
    return s


def ratio(nu):
    # t = I_nu / I_1 as a series: both divisible by beta, so divide num and den by beta first (ORDER shrinks by one at the top only).
    num = bessel_I(nu)[1:] + [(0, 1)]
    den = bessel_I(1)[1:] + [(0, 1)]
    lead = den[0]
    den = [qm(x, (lead[1], lead[0])) for x in den]
    num = [qm(x, (lead[1], lead[0])) for x in num]
    return sdiv(num, den)


# z = (2/beta) I_1
z = [qm(x, (2, 1)) for x in (bessel_I(1)[1:] + [(0, 1)])]
ts = {nu: ratio(nu) for nu in range(2, 7)}  # nu=2j+1: nu=2 is j=1/2
total = [(1, 1)] + [(0, 1)] * (ORDER - 1)
for nu, t in ts.items():
    total = [qa(a, b) for a, b in zip(total, spow(t, 4))]
Z = smul(spow(z, 4), total)
haar = {k: qm(Z[k], (math.factorial(k), 1)) for k in range(0, 14)}
print("HAAR_T2|E_X2=%d/%d|E_X4=%d/%d|E_X6=%d/%d|E_X8=%d/%d|E_X12=%d/%d|hand_E_X4=91/32|json=0" % (haar[2] + haar[4] + haar[6] + haar[8] + haar[12]))
assert haar[4] == (91, 32)

WRING = {"Q8": (0, 0), "2T": (0, 0), "2O": (0, 2), "2I": (1, 1)}
EXPECT_T = {"Q8": 3, "2T": 5, "2O": 7, "2I": 11}
DIM_INV = {"Q8": 2, "2T": 1, "2O": 1, "2I": 1}
for name in ("Q8", "2T", "2O", "2I"):
    line = open("hist_%s.txt" % name, encoding="utf8").read().strip().split("|")
    assert "sum_ok=1" in line
    configs = int([x for x in line if x.startswith("configs=")][0].split("=")[1])
    hist = {}
    for x in line:
        if ":" in x and "," in x:
            pair, c = x.split(":")
            a, b = pair.split(",")
            hist[(int(a), int(b))] = int(c)
    p, q = WRING[name]

    def rmul(x, y):
        return (x[0] * y[0] + x[1] * y[1] * q, x[0] * y[1] + x[1] * y[0] + x[1] * y[1] * p)
    moments = {}
    for k in range(0, 14):
        S = (0, 0)
        for key, c in hist.items():
            v = (1, 0)
            for _ in range(k):
                v = rmul(v, key)
            S = (S[0] + c * v[0], S[1] + c * v[1])
        assert S[1] == 0, (name, k, S)
        moments[k] = red(S[0], configs * 2 ** k)  # the histogram is of 2X, the sum of traces
    t = EXPECT_T[name]
    diffs = {k: qs(moments[k], haar[k]) for k in range(0, 14)}
    first = next(k for k in range(0, 14) if diffs[k][0])
    want = red(4 * DIM_INV[name], 2 ** (t + 1))
    # plaquette series difference at beta^t: (1/N_p) (t+1) * delta_E / (t+1)! = delta_E / (N_p t!)
    delta_plaq = qm(diffs[first], red(1, 4 * math.factorial(first - 1)))
    print("T2_FIRST_DIFF|group=%s|t=%d|moments_agree_through_k=%d|E_G_X^%d-E_H_X^%d=%d/%d|predicted_N_p*dimInv/2^(t+1)=%d/%d|plaquette_series_delta_at_beta^%d=%d/%d|json=0" % ((name, t, first - 1, first, first) + diffs[first] + want + (first - 1,) + delta_plaq))
    assert first == t + 1 and diffs[first] == want
print("FIRST_DIFF_T2_DONE|json=0")
