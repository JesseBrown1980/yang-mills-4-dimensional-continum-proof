# Lane L2-sec3-part2: exact integer checks of note Lemmas 3.15, 3.16, 3.17 and Proposition 3.18
# on small abstract polymer systems (the section 3.6 setting). Evidence only; the proofs are the derivations.
import itertools, sys
from qint import q, add, sub, mul, div, le, lt, ZERO, ONE, factorial, exp_lo_hi, dec, ip, sgn

out = []
def say(s):
    out.append(s); print(s)

# ---------- graph helpers ----------
def edges_of(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]

def connected(n, E):
    if n == 0:
        return True
    adj = {i: [] for i in range(n)}
    for (i, j) in E:
        adj[i].append(j); adj[j].append(i)
    seen = {0}; st = [0]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); st.append(v)
    return len(seen) == n

def conn_sum(n, H):
    # sum over connected spanning subgraphs G of H of (-1)^{#edges(G)}
    H = list(H); tot = 0
    for mask in range(1 << len(H)):
        G = [H[k] for k in range(len(H)) if (mask >> k) & 1]
        if connected(n, G):
            tot += -1 if (len(G) % 2) else 1
    return tot

def spanning_trees(n, H):
    H = list(H); res = []
    for G in itertools.combinations(H, n - 1):
        if connected(n, G):
            res.append(frozenset(G))
    return res

def penrose_count(n, H):
    # #{tau spanning tree of H : R(tau) = tau}; vertex 0 here is the note's vertex 1
    Hs = set(H); cnt = 0
    for tau in spanning_trees(n, H):
        adj = {i: [] for i in range(n)}
        for (i, j) in tau:
            adj[i].append(j); adj[j].append(i)
        d = {0: 0}; par = {}; st = [0]
        while st:
            u = st.pop()
            for v in adj[u]:
                if v not in d:
                    d[v] = d[u] + 1; par[v] = u; st.append(v)
        R = set(tau)
        for (i, j) in Hs:
            if d[i] == d[j]:
                R.add((i, j))
            for (a, b) in ((i, j), (j, i)):   # a shallower, b deeper by one
                if d[b] == d[a] + 1 and a > par[b]:
                    R.add((i, j))
        if R == set(tau):
            cnt += 1
    return cnt

# ---------- Part A: Lemma 3.16 (Penrose partition) ----------
ok = True; ngraphs = 0
for n in range(1, 6):
    E = edges_of(n)
    for mask in range(1 << len(E)):
        H = [E[k] for k in range(len(E)) if (mask >> k) & 1]
        if not connected(n, H):
            continue
        ngraphs += 1
        lhs = conn_sum(n, H)
        rhs = sgn(n - 1) * penrose_count(n, H)
        nt = len(spanning_trees(n, H))
        if lhs != rhs or abs(lhs) > nt:
            ok = False; say("A_FAIL n=%d H=%s lhs=%d rhs=%d trees=%d" % (n, H, lhs, rhs, nt))
seed = 20261109; n6 = 0
E6 = edges_of(6)
while n6 < 150:
    seed = (seed * 6364136223846793005 + 1442695040888963407) % (1 << 64)
    mask = seed >> 49  # 15 bits
    H = [E6[k] for k in range(15) if (mask >> k) & 1]
    if len(H) > 11 or not connected(6, H):
        continue
    n6 += 1; ngraphs += 1
    lhs = conn_sum(6, H); rhs = -penrose_count(6, H); nt = len(spanning_trees(6, H))
    if lhs != rhs or abs(lhs) > nt:
        ok = False; say("A_FAIL n=6 H=%s lhs=%d rhs=%d" % (H, lhs, rhs))
say("PART_A|lemma=3.16|graphs_checked=%d|all_connected_graphs_n<=5_plus_%d_at_n=6|identity_holds=%d|abs_phiT<=spanning_trees=%d|tag=MEASURED" % (ngraphs, n6, int(ok), int(ok)))

# ---------- abstract polymer system: ground links 1..4, elements with off-sets ----------
GAM = {"a": {1}, "b": {1, 2}, "c": {2, 3}, "d": {4}, "e": {3, 4}}
names = sorted(GAM)
def inc(x, y):
    return len(GAM[x] & GAM[y]) > 0

phi_cache = {}
def phiT(X):
    n = len(X)
    I = tuple((i, j) for (i, j) in edges_of(n) if inc(X[i], X[j]))
    key = (n, I)
    if key not in phi_cache:
        phi_cache[key] = conn_sum(n, I) if connected(n, I) else 0
    return phi_cache[key]

# ---------- Part B: Lemma 3.15 (Mayer expansion), truncated multivariate series ----------
DEG = 5
def mono(X):
    return tuple(sorted(X))
def padd(P, Q):
    R = dict(P)
    for k, v in Q.items():
        R[k] = add(R.get(k, ZERO), v)
        if R[k][0] == 0:
            del R[k]
    return R
def pmul(P, Q):
    R = {}
    for k1, v1 in P.items():
        for k2, v2 in Q.items():
            k = mono(k1 + k2)
            if len(k) > DEG:
                continue
            R[k] = add(R.get(k, ZERO), mul(v1, v2))
    return {k: v for k, v in R.items() if v[0] != 0}
def pscale(c, P):
    R = {}
    for k, v in P.items():
        m = mul(c, v)
        if m[0] != 0:
            R[k] = m
    return R
Xi1 = {}
for r in range(1, len(names) + 1):
    for A in itertools.combinations(names, r):
        if all(not inc(x, y) for x, y in itertools.combinations(A, 2)) and len(A) <= DEG:
            Xi1[mono(A)] = add(Xi1.get(mono(A), ZERO), ONE)
logXi = {}; Pk = {(): ONE}
for k in range(1, DEG + 1):
    Pk = pmul(Pk, Xi1)
    logXi = padd(logXi, pscale(q(sgn(k + 1), k), Pk))
clus = {}
for n in range(1, DEG + 1):
    for X in itertools.product(names, repeat=n):
        p = phiT(X)
        if p == 0:
            continue
        k = mono(X)
        clus[k] = add(clus.get(k, ZERO), q(p, factorial(n)))
clus = {k: v for k, v in clus.items() if v[0] != 0}
okB = (clus == logXi)
say("PART_B|lemma=3.15|system=5_elements_on_4_links|degree<=%d|monomials_compared=%d|log_Xi_equals_cluster_series=%d|tag=MEASURED" % (DEG, len(set(clus) | set(logXi)), int(okB)))

# ---------- Part C: Lemma 3.17 (rooted-tree recursion), truncated series in s ----------
cw = {"a": 2, "b": 1, "c": 3, "d": 1, "e": 2}   # omega(g) = s * cw[g]
NMAX = 6
def pruefer_trees(n):
    if n == 1:
        yield []
        return
    if n == 2:
        yield [(0, 1)]
        return
    for seq in itertools.product(range(n), repeat=n - 2):
        deg = [1] * n
        for x in seq:
            deg[x] += 1
        T = []
        for x in seq:
            leaf = min(i for i in range(n) if deg[i] == 1)
            T.append((min(leaf, x), max(leaf, x))); deg[leaf] -= 1; deg[x] -= 1
        u, v = [i for i in range(n) if deg[i] == 1]
        T.append((u, v))
        yield T
def depth_from0(n, T):
    adj = {i: [] for i in range(n)}
    for (i, j) in T:
        adj[i].append(j); adj[j].append(i)
    d = {0: 0}; st = [0]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in d:
                d[v] = d[u] + 1; st.append(v)
    return max(d.values())
TREES = {n: [(T, depth_from0(n, T)) for T in pruefer_trees(n)] for n in range(1, NMAX + 1)}
cayley_ok = all(len(TREES[n]) == (ip(n, n - 2) if n >= 2 else 1) for n in range(1, NMAX + 1))
MB = {}
def M_brute(g, h):
    if (g, h) in MB:
        return MB[(g, h)]
    coeffs = [ZERO] * NMAX
    for n in range(1, NMAX + 1):
        tot = 0
        for (T, dep) in TREES[n]:
            if dep > h:
                continue
            for rest in itertools.product(names, repeat=n - 1):
                X = (g,) + rest
                if all(inc(X[i], X[j]) for (i, j) in T):
                    w = 1
                    for x in rest:
                        w *= cw[x]
                    tot += w
        coeffs[n - 1] = q(tot, factorial(n - 1))
    MB[(g, h)] = coeffs
    return coeffs
def s_mul(A, B):
    C = [ZERO] * NMAX
    for i in range(NMAX):
        if A[i][0] == 0:
            continue
        for j in range(NMAX - i):
            C[i + j] = add(C[i + j], mul(A[i], B[j]))
    return C
def s_exp(A):
    assert A[0][0] == 0
    R = [ONE] + [ZERO] * (NMAX - 1); P = [ONE] + [ZERO] * (NMAX - 1)
    for k in range(1, NMAX):
        P = s_mul(P, A); P = [div(c, q(k)) for c in P]
        R = [add(x, y) for x, y in zip(R, P)]
    return R
okC = cayley_ok
for g in names:
    if M_brute(g, 0) != [ONE] + [ZERO] * (NMAX - 1):
        okC = False
for h in range(0, 4):
    for g in names:
        lhs = M_brute(g, h + 1)
        inner = [ZERO] * NMAX
        for gp in names:
            if inc(g, gp):
                Mh = M_brute(gp, h)
                shifted = [ZERO] + [mul(q(cw[gp]), c) for c in Mh[:NMAX - 1]]
                inner = [add(x, y) for x, y in zip(inner, shifted)]
        rhs = s_exp(inner)
        if lhs != rhs:
            okC = False; say("C_FAIL g=%s h=%d" % (g, h))
say("PART_C|lemma=3.17|M_0=1_and_M_(h+1)=exp(sum_(g2_incompatible_with_g)omega(g2)M_h(g2))_coefficientwise_through_s^%d|h=0..3|elements=5|cayley_counts_ok=%d|holds=%d|tag=MEASURED" % (NMAX - 1, int(cayley_ok), int(okC)))

# ---------- Part D: Proposition 3.18 items 1 and 3, truncated sums against the bounds ----------
alpha = q(1, 5)
expo = {k: exp_lo_hi(mul(alpha, q(k))) for k in range(1, 4)}
omega = {"a": q(1, 40), "b": q(1, 60), "c": q(1, 45), "d": q(1, 30), "e": q(1, 50)}
links = sorted(set().union(*GAM.values()))
kp_ok = True; kp_max = ZERO
for w in links:
    s = ZERO
    for g in names:
        if w in GAM[g]:
            s = add(s, mul(omega[g], expo[len(GAM[g])][1]))
    if lt(kp_max, s):
        kp_max = s
    if not le(s, alpha):
        kp_ok = False
say("PART_D_HYP|KP_w_with_alpha=1/5|max_over_w_of_left_side_upper=%s|holds=%d" % (dec(kp_max, 8, "ceil"), int(kp_ok)))
ND = 6
item1_ok = True
for g in names:
    tot = ZERO; trees_tot = ZERO
    for n in range(1, ND + 1):
        acc = ZERO; acc_tree = ZERO
        for rest in itertools.product(names, repeat=n - 1):
            X = (g,) + rest
            p = abs(phiT(X))
            w = ONE
            for x in rest:
                w = mul(w, omega[x])
            nt = sum(1 for (T, dep) in TREES[n] if all(inc(X[i], X[j]) for (i, j) in T))
            if p:
                acc = add(acc, mul(q(p), w))
            if nt:
                acc_tree = add(acc_tree, mul(q(nt), w))
            if p > nt:
                item1_ok = False
        tot = add(tot, div(acc, q(factorial(n - 1))))
        trees_tot = add(trees_tot, div(acc_tree, q(factorial(n - 1))))
    bound_lo = expo[len(GAM[g])][0]
    if not le(trees_tot, bound_lo):
        item1_ok = False
    say("PART_D_ITEM1|gamma=%s|#off=%d|truncated_n<=%d_abs_phiT_sum<=%s|truncated_tree_sum<=%s|e^(alpha#off)>=%s" % (g, len(GAM[g]), ND, dec(tot, 10, "ceil"), dec(trees_tot, 10, "ceil"), dec(bound_lo, 10)))
item3_ok = True
for w in links:
    tot = ZERO
    for n in range(1, ND):
        acc = ZERO
        for X in itertools.product(names, repeat=n):
            if not any(w in GAM[x] for x in X):
                continue
            p = abs(phiT(X))
            if not p:
                continue
            wt = ONE
            for x in X:
                wt = mul(wt, omega[x])
            acc = add(acc, mul(q(p), wt))
        tot = add(tot, div(acc, q(factorial(n))))
    mid = ZERO
    for g in names:
        if w in GAM[g]:
            mid = add(mid, mul(omega[g], expo[len(GAM[g])][0]))
    if not le(tot, mid):
        item3_ok = False
    say("PART_D_ITEM3|w=%d|truncated_n<=%d_cluster_sum<=%s|sum_(gamma_holding_w)omega*e^(alpha#off)>=%s|alpha=1/5" % (w, ND - 1, dec(tot, 10, "ceil"), dec(mid, 10)))
say("PART_D|prop=3.18|item1_truncated_below_bound=%d|abs_phiT<=trees_pointwise=%d|item3_truncated_below_middle_term=%d|tag=MEASURED_(finite_truncations,evidence_only)" % (int(item1_ok), int(item1_ok), int(item3_ok)))

# ---------- Part E: hard-core single element ----------
okE = True
for n in range(1, 7):
    if conn_sum(n, edges_of(n)) != sgn(n - 1) * factorial(n - 1):
        okE = False
say("PART_E|phiT(K_n)=(-1)^(n-1)(n-1)!_for_n=1..6:%d|tag=MEASURED" % int(okE))
allok = ok and okB and okC and kp_ok and item1_ok and item3_ok and okE
say("SUMMARY|cluster_combinatorics_all_pass=%d|json=0" % int(allok))
open("/mnt/c/tmp/opus55/ym4-04c-gattack/work/L2-sec3-part2/cluster_combinatorics.out", "w").write("\n".join(out) + "\n")
sys.exit(0 if allok else 1)
