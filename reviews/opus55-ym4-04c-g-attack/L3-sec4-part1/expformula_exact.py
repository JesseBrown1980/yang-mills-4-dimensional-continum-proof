#!/usr/bin/env python3
# L3-sec4-part1, check G1b: the identity of note Lemma 3.15 (log Xi = Ursell series,
# the REPORTED exponential formula for connected graphs) as G1 uses it, checked
# coefficient by coefficient in exact integer-pair rationals up to total degree DEG,
# on small abstract gases with off-link incompatibility (reflexive, symmetric), as in
# note section 3.6 / Theorem 4.9.  Also checks the multiset regrouping phi(X) =
# phi^T / prod m_X! used in the proof of Theorem 4.9, and Corollary 4.10 (a)/(b) and
# Proposition 3.18 item 3 as truncated (lower-bound) sums at a weight that meets
# (KP_w) with EQUALITY at its worst link (the window-boundary analogue lambda = kappa).
# Integer only: rationals are (num, den) integer pairs; no float/fractions/decimal.
import itertools, math, sys

def rn(a, b=1):
    if b < 0: a, b = -a, -b
    g = math.gcd(a, b); return (a // g, b // g)
def radd(x, y): return rn(x[0] * y[1] + y[0] * x[1], x[1] * y[1])
def rmul(x, y): return rn(x[0] * y[0], x[1] * y[1])
def rneg(x): return (-x[0], x[1])
ZERO = (0, 1); ONE = (1, 1)

def padd(P, Q):
    R = dict(P)
    for k, v in Q.items():
        R[k] = radd(R.get(k, ZERO), v)
        if R[k][0] == 0: del R[k]
    return R
def pmul(P, Q, deg):
    R = {}
    for k1, v1 in P.items():
        for k2, v2 in Q.items():
            k = tuple(a + b for a, b in zip(k1, k2))
            if sum(k) > deg: continue
            R[k] = radd(R.get(k, ZERO), rmul(v1, v2))
    return {k: v for k, v in R.items() if v[0] != 0}
def pscale(P, c): return {k: rmul(v, c) for k, v in P.items() if rmul(v, c)[0] != 0}

def formal_log_xi(off, deg):
    n = len(off)
    def inc(i, j): return bool(off[i] & off[j])
    P = {}
    for r in range(1, n + 1):
        for A in itertools.combinations(range(n), r):
            if all(not inc(i, j) for i, j in itertools.combinations(A, 2)):
                if r <= deg:
                    k = tuple(1 if i in A else 0 for i in range(n))
                    P[k] = radd(P.get(k, ZERO), ONE)
    # log(1+P) = sum_{k>=1} (-1)^{k+1} P^k / k ; P has no constant term
    L = {}; Pk = {tuple([0] * n): ONE}
    for k in range(1, deg + 1):
        Pk = pmul(Pk, P, deg)
        L = padd(L, pscale(Pk, rn((-1) ** (k + 1), k)))
    return L

def connected(nv, edges):
    if nv == 1: return True
    adj = {i: [] for i in range(nv)}
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    seen = {0}; st = [0]
    while st:
        a = st.pop()
        for b in adj[a]:
            if b not in seen: seen.add(b); st.append(b)
    return len(seen) == nv

def phiT(seq, off):
    nv = len(seq)
    E = [(i, j) for i, j in itertools.combinations(range(nv), 2) if off[seq[i]] & off[seq[j]]]
    tot = 0
    for mask in range(1 << len(E)):
        sub = [E[b] for b in range(len(E)) if mask >> b & 1]
        if connected(nv, sub): tot += (-1) ** len(sub)
    return tot

def ursell_series(off, deg):
    n = len(off); U = {}
    cache = {}
    for m in range(1, deg + 1):
        for seq in itertools.product(range(n), repeat=m):
            key = tuple(sorted(seq))
            if key not in cache: cache[key] = phiT(list(key), off)   # phi^T is symmetric
            v = cache[key]
            if v == 0: continue
            k = [0] * n
            for g in seq: k[g] += 1
            k = tuple(k)
            U[k] = radd(U.get(k, ZERO), rn(v, math.factorial(m)))
    U = {k: v for k, v in U.items() if v[0] != 0}
    # multiset form: phi(X) = phi^T(any realization)/prod m!  ->  coefficient of zeta^m
    mult_ok = True
    for k, v in U.items():
        seq = [g for g in range(n) for _ in range(k[g])]
        pm = 1
        for x in k: pm *= math.factorial(x)
        if v != rn(cache[tuple(sorted(seq))], pm): mult_ok = False
    return U, cache, mult_ok

SYSTEMS = {
    "path4": [{0}, {0, 1}, {1, 2}, {2}],
    "star4": [{0}, {0}, {0, 1}, {0, 2}],
    "triangle_pendant": [{0, 1}, {1, 2}, {0, 2}, {2, 3}],
    "two_blocks": [{0}, {0}, {1}, {1, 2}],
}

def exp_lo(x_num, x_den, terms=30):
    # lower bound of e^{x}, x = x_num/x_den >= 0: Taylor partial sum (integer pair)
    s = ZERO; t = ONE
    for k in range(terms):
        s = radd(s, t); t = rmul(t, rn(x_num, x_den * (k + 1)))
    return s

def main(deg=5):
    allok = True
    for name, off in SYSTEMS.items():
        off = [frozenset(o) for o in off]
        L = formal_log_xi(off, deg)
        U, cache, mult_ok = ursell_series(off, deg)
        same = (L == U)
        allok &= same and mult_ok
        print("L3_EXPFORMULA|system=%s|polymers=%d|degree<=%d|monomials_logXi=%d|monomials_ursell=%d|coefficients_equal=%s|multiset_phi_eq_phiT_over_prod_m!=%s|json=0"
              % (name, len(off), deg, len(L), len(U), int(same), int(mult_ok)))
        # Corollary 4.10(a) and Prop 3.18 item 3, truncated at deg (so the left side is a LOWER
        # bound of the full sum): weight omega(g) = c, alpha = 1/2, chosen so that (KP_w) holds
        # with equality at the worst link: max_w sum_{g ni w} c e^{alpha #off(g)} = alpha.
        # e^{alpha s} is bracketed by integer pairs: lower = partial sum, upper = lower + tail.
        alpha = (1, 2)
        links = sorted(set().union(*off))
        # use the upper bracket of e^{alpha s} to choose c (so (KP_w) truly holds), integer pairs
        def eup(s):
            lo = exp_lo(alpha[0] * s, alpha[1], 40)
            return radd(lo, rn(1, 10 ** 30))
        worst = ZERO
        for w in links:
            acc = ZERO
            for g in range(len(off)):
                if w in off[g]: acc = radd(acc, eup(len(off[g])))
            if acc[0] * worst[1] > worst[0] * acc[1]: worst = acc
        c = rmul(alpha, (worst[1], worst[0]))  # c = alpha / worst  -> (KP_w) equality up to the tail
        # truncated cluster sums with weight omega = c (z = omega, d = 0)
        okA = True; ok3 = True
        for g in range(len(off)):
            lhs = ZERO
            for k, v in U.items():
                if k[g] >= 1:
                    # |Phi(X;omega)| = |phi(X)| c^{n}: |v| is |phi^T|/prod m!; with 1/n! *n!/prod m! regrouping
                    n = sum(k)
                    pm = 1
                    for x in k: pm *= math.factorial(x)
                    seq = [h for h in range(len(off)) for _ in range(k[h])]
                    ph = abs(cache[tuple(sorted(seq))])
                    term = rn(ph * c[0] ** n, pm * c[1] ** n)
                    lhs = radd(lhs, term)
            rhs = rmul(c, exp_lo(alpha[0] * len(off[g]), alpha[1], 40))  # LOWER bracket of the right side
            # truncated left <= lower bracket of right: a strictly stronger test than needed
            if lhs[0] * rhs[1] > rhs[0] * lhs[1]: okA = False
        for w in links:
            lhs = ZERO
            for k, v in U.items():
                if any(k[h] >= 1 and w in off[h] for h in range(len(off))):
                    n = sum(k); pm = 1
                    for x in k: pm *= math.factorial(x)
                    seq = [h for h in range(len(off)) for _ in range(k[h])]
                    lhs = radd(lhs, rn(abs(cache[tuple(sorted(seq))]) * c[0] ** n, pm * c[1] ** n))
            if lhs[0] * alpha[1] > alpha[0] * lhs[1]: ok3 = False
        allok &= okA and ok3
        print("L3_KP_TRUNCATED|system=%s|alpha=1/2|KPw_worst_link=equality_up_to_1e-30|cor4.10a_truncated_le_rhs=%d|prop3.18_item3_truncated_le_alpha=%d|json=0"
              % (name, int(okA), int(ok3)))
    print("L3_EXPFORMULA_END|systems=%d|all_ok=%d|tag=MEASURED|json=0" % (len(SYSTEMS), int(allok)))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
