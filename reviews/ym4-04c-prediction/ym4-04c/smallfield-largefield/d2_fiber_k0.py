"""Derivation check: k'=0 Bloch sector of the linearized b=2 line-map fiber on the fine 2^4 cell.

Physical fiber vectors v = tau + h(tau), tau transverse on (Z/2)^4, h harmonic with B v = 0.
Per direction mu the B-coupled transverse modes are q in {0,pi}^4, q_mu=0, q!=0, polarization e_mu,
with eigenvalue 4 n(q) of d^T d; Rayleigh = sum lam a^2 / (sum a^2 + (sum a)^2).
Lowest generalized eigenvalue solves lam * sum_q 1/(lam_q - lam) = 1.
Also brute-force check: build the 64x64 problem exactly and count inertia.
"""
from fractions import Fraction as Fr
import itertools


def secular(lam):
    return lam * (Fr(3) / (4 - lam) + Fr(3) / (8 - lam) + Fr(1) / (12 - lam)) - 1


lo, hi = Fr(0), Fr(4)
lo, hi = Fr(1, 100), Fr(399, 100)
for _ in range(80):
    m = (lo + hi) / 2
    if secular(m) < 0:
        lo = m
    else:
        hi = m
print("secular root in [%.12f, %.12f]" % (lo.numerator / lo.denominator, hi.numerator / hi.denominator))
# cubic: (4-l)(8-l)(12-l) = l[3(8-l)(12-l)+3(4-l)(12-l)+(4-l)(8-l)]

# brute force on (Z/2)^4: links (x,mu), x in {0,1}^4
sites = list(itertools.product((0, 1), repeat=4))
idx = {}
for x in sites:
    for mu in range(4):
        idx[(x, mu)] = len(idx)
N = len(idx)


def add(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % 2
    return tuple(y)


# d: plaquettes (x,mu<nu): A_mu(x)+A_nu(x+mu)-A_mu(x+nu)-A_nu(x)
rows = []
for x in sites:
    for mu in range(4):
        for nu in range(mu + 1, 4):
            r = [0] * N
            r[idx[(x, mu)]] += 1
            r[idx[(add(x, mu), nu)]] += 1
            r[idx[(add(x, nu), mu)]] -= 1
            r[idx[(x, nu)]] -= 1
            rows.append(r)
K = [[sum(r[i] * r[j] for r in rows) for j in range(N)] for i in range(N)]
# B: coarse link mu = A_mu(0)+A_mu(e_mu)
z = (0, 0, 0, 0)
Brows = []
for mu in range(4):
    r = [0] * N
    r[idx[(z, mu)]] += 1
    r[idx[(add(z, mu), mu)]] += 1
    Brows.append(r)
# gauge directions: d lambda for lambda at each site (all gauge directions lie in ker B here)
G = []
for s in sites:
    r = [0] * N
    for mu in range(4):
        # A_mu(x) = lam(x+mu) - lam(x)
        for x in sites:
            if add(x, mu) == s:
                r[idx[(x, mu)]] += 1
            if x == s:
                r[idx[(x, mu)]] -= 1
    G.append(r)


def nullspace(M, n):
    """Rational basis of {v : M v = 0} for rows M of length n."""
    M = [[Fr(a) for a in r] for r in M]
    piv = []
    rI = 0
    for c in range(n):
        p = None
        for i in range(rI, len(M)):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[rI], M[p] = M[p], M[rI]
        pv = M[rI][c]
        M[rI] = [a / pv for a in M[rI]]
        for i in range(len(M)):
            if i != rI and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[rI])]
        piv.append(c)
        rI += 1
        if rI == len(M):
            break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [Fr(0)] * n
        v[f] = Fr(1)
        for i, c in enumerate(piv):
            v[c] = -M[i][f]
        basis.append(v)
    return basis


# physical fiber = {v : B v = 0, <g, v> = 0 for all gauge g}
phys = nullspace(Brows + G, N)
print("physical fiber dim", len(phys))


def quad(M, u, v):
    return sum(u[i] * sum(M[i][j] * v[j] for j in range(N) if M[i][j]) for i in range(N))


Kp = [[quad(K, a, b) for b in phys] for a in phys]
Gp = [[sum(x * y for x, y in zip(a, b)) for b in phys] for a in phys]


def count_below(lam):
    """Number of eigenvalues of (Kp, Gp) below lam, by LDL inertia of Kp - lam Gp."""
    n = len(Kp)
    A = [[Kp[i][j] - lam * Gp[i][j] for j in range(n)] for i in range(n)]
    neg = 0
    for k in range(n):
        p = A[k][k]
        if p == 0:
            raise ValueError("zero pivot")
        if p < 0:
            neg += 1
        for i in range(k + 1, n):
            if A[i][k] != 0:
                f = A[i][k] / p
                for j in range(k + 1, n):
                    if A[k][j] != 0:
                        A[i][j] -= f * A[k][j]
    return neg


for lam in (Fr(70, 100), Fr(71, 100), Fr(1, 2), Fr(4, 1), Fr(401, 100)):
    print("eigenvalues below", lam, ":", count_below(lam))
