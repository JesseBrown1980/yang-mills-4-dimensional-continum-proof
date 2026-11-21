"""Design-lane SANITY CHECK ONLY (floats, numpy; not evidence, not an engine).

Gauge-free constrained minimization of S = 1/2 sum_p theta_p^2 on the fine (Z/2L)^4 abelian lattice,
subject to the coarse data of a map M (line map or averaged map, b = 2), for the coarse plane wave
A'_mu(x') = (-1)^{x'_nu} (mu = 0, nu = 1).  Ratio r = S_min / S_W(A'), S_W = 1/2 sum_P theta'_P^2.
Expected (alias formula, d3_tree.py): line r = 15/28 = 0.5357142857, averaged r = 2.
"""
import itertools
import numpy as np

d, b = 4, 2
Lc = 2
Lf = b * Lc
sites = list(itertools.product(range(Lf), repeat=d))
idx = {}
for s in sites:
    for mu in range(d):
        idx[(s, mu)] = len(idx)
N = len(idx)


def sh(s, mu, k=1):
    t = list(s)
    t[mu] = (t[mu] + k) % Lf
    return tuple(t)


rows = []
for s in sites:
    for mu in range(d):
        for nu in range(mu + 1, d):
            r = np.zeros(N)
            r[idx[(s, mu)]] += 1
            r[idx[(sh(s, mu), nu)]] += 1
            r[idx[(sh(s, nu), mu)]] -= 1
            r[idx[(s, nu)]] -= 1
            rows.append(r)
P = np.array(rows)  # theta = P a
Q = P.T @ P  # S = 1/2 a^T Q a

csites = list(itertools.product(range(Lc), repeat=d))


def line_row(xc, mu):
    r = np.zeros(N)
    base = tuple(b * c for c in xc)
    for s in range(b):
        r[idx[(sh(base, mu, s), mu)]] += 1
    return r


def avg_row(xc, mu):
    r = np.zeros(N)
    base = tuple(b * c for c in xc)
    for y in itertools.product(range(b), repeat=d):
        start = tuple((base[i] + y[i]) % Lf for i in range(d))
        for s in range(b):
            r[idx[(sh(start, mu, s), mu)]] += 1.0 / b ** d
    return r


def coarse_target():
    v = []
    for xc in csites:
        for mu in range(d):
            v.append(float((-1) ** xc[1]) if mu == 0 else 0.0)
    return np.array(v)


def SW(Ap):
    # coarse plaquettes on (Z/Lc)^4
    cidx = {}
    for xc in csites:
        for mu in range(d):
            cidx[(xc, mu)] = len(cidx)
    tot = 0.0
    def csh(s, mu):
        t = list(s); t[mu] = (t[mu] + 1) % Lc; return tuple(t)
    for xc in csites:
        for mu in range(d):
            for nu in range(mu + 1, d):
                th = Ap[cidx[(xc, mu)]] + Ap[cidx[(csh(xc, mu), nu)]] - Ap[cidx[(csh(xc, nu), mu)]] - Ap[cidx[(xc, nu)]]
                tot += 0.5 * th * th
    return tot


Ap = coarse_target()
for name, rowf in (("line", line_row), ("averaged", avg_row)):
    C = np.array([rowf(xc, mu) for xc in csites for mu in range(d)])
    # minimize 1/2 a^T Q a subject to C a = Ap: KKT system, least-squares (Q singular on gauge modes)
    K = np.block([[Q, C.T], [C, np.zeros((C.shape[0], C.shape[0]))]])
    rhs = np.concatenate([np.zeros(N), Ap])
    sol, *_ = np.linalg.lstsq(K, rhs, rcond=None)
    a = sol[:N]
    resid = np.abs(C @ a - Ap).max()
    Smin = 0.5 * a @ Q @ a
    print("%s: S_min=%.10f S_W=%.10f r=%.10f constraint_resid=%.2e" % (name, Smin, SW(Ap), Smin / SW(Ap), resid))
