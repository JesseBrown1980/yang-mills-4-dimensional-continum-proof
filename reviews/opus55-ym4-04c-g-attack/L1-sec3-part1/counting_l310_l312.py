#!/usr/bin/env python3
# Lane L1-sec3-part1: note Lemmas 3.10, 3.11 and Corollary 3.12 re-derived as exact integer checks.
# Integer arithmetic only (math.comb, //, %, ** with nonnegative exponents). No float, no fractions, no decimal.
import sys
from math import comb
from itertools import product

out = []
allok = True
def chk(name, ok, detail=""):
    global allok
    allok = allok and ok
    out.append("CNT|%s|ok=%d%s" % (name, 1 if ok else 0, ("|" + detail) if detail else ""))

def F(n, D=20):
    a = comb(D * n, n)
    b = (D - 1) * n + 1
    assert a % b == 0
    return a // b

# ---- Lemma 3.10: both closed forms agree, as exact integers, D = 2..25, n = 1..120
ok = True
for D in range(2, 26):
    for n in range(1, 121):
        a = comb(D * n, n)
        b = (D - 1) * n + 1
        c = comb(D * n, n - 1)
        if a % b != 0 or c % n != 0 or a // b != c // n:
            ok = False
chk("L310_two_closed_forms_equal_D2..25_n1..120", ok)

# ---- Lemma 3.10: t_D(n) from the functional equation T = y (1 + T)^D (root slot choice), integer power series
def tree_series(D, M):
    T = [0] * (M + 1)
    for _ in range(M + 1):
        # P = (1 + T)^D truncated at degree M - 1
        P = [0] * (M + 1); P[0] = 1
        base = T[:]; base[0] += 1
        for _k in range(D):
            Q = [0] * (M + 1)
            for i, x in enumerate(P):
                if x:
                    for j in range(0, M + 1 - i):
                        if base[j]:
                            Q[i + j] += x * base[j]
            P = Q
        T = [0] + P[:M]
    return T
ok = True
for D in (2, 3, 4, 5, 20):
    M = 40 if D == 20 else 30
    T = tree_series(D, M)
    for n in range(1, M + 1):
        if T[n] != F(n, D):
            ok = False
chk("L310_series_T=y(1+T)^D_matches_F_D(n)_D=2,3,4,5,20", ok, "n<=40_for_D=20")

# ---- brute-force subtrees of the complete D-ary tree containing the root (vertex = word over 1..D)
def brute_subtrees(D, nmax):
    level = {frozenset([()])}
    counts = [0, 1]
    for n in range(2, nmax + 1):
        nxt = set()
        for S in level:
            for v in S:
                for i in range(1, D + 1):
                    c = v + (i,)
                    if c not in S:
                        nxt.add(S | {c})
        level = nxt
        counts.append(len(level))
    return counts
ok = True
det = []
for D, nmax in ((2, 8), (3, 7), (4, 6), (20, 3)):
    c = brute_subtrees(D, nmax)
    det.append("D=%d:%s" % (D, ",".join(str(x) for x in c[1:])))
    if any(c[n] != F(n, D) for n in range(1, nmax + 1)):
        ok = False
chk("L310_brute_force_subtree_counts_equal_F_D(n)", ok, ";".join(det))

# ---- cycle lemma, brute force: words (C_1..C_n), C_i subset of {1..D}, sum k_i = n - 1
ok = True
det = []
for D, n in ((2, 5), (3, 4), (3, 5), (2, 7), (4, 4)):
    subsets = list(range(1 << D))
    A = 0
    B = 0
    trees = set()
    bad_shift = 0
    for w in product(subsets, repeat=n):
        ks = [bin(c).count("1") for c in w]
        if sum(ks) != n - 1:
            continue
        A += 1
        P = [0]
        for k in ks:
            P.append(P[-1] + k - 1)
        valid = all(P[j] >= 0 for j in range(1, n)) and P[n] == -1
        # number of valid cyclic shifts
        nv = 0
        for r in range(n):
            ww = ks[r:] + ks[:r]
            Q = 0; good = True
            for j in range(n):
                Q += ww[j] - 1
                if j < n - 1 and Q < 0:
                    good = False; break
            if good:
                nv += 1
                # first minimizer rule
                fm = min(range(n), key=lambda m: (P[m], m))
                if fm != r:
                    bad_shift += 1
        if nv != 1:
            bad_shift += 1
        if valid:
            B += 1
            # decode preorder word into a subtree (set of root paths)
            stack = [()]
            verts = []
            it = iter(w)
            # depth-first preorder decoding
            def decode(path):
                c = next(it)
                verts.append(path)
                for i in range(D):
                    if c >> i & 1:
                        decode(path + (i + 1,))
            decode(())
            trees.add(frozenset(verts))
    good = (A == comb(D * n, n - 1)) and (A % n == 0) and (B == A // n) and (B == F(n, D)) and len(trees) == B and bad_shift == 0
    det.append("D=%d,n=%d:A=%d,B=%d,trees=%d" % (D, n, A, B, len(trees)))
    ok = ok and good
chk("L310_cycle_lemma_one_valid_shift_first_minimizer_and_decode_bijective", ok, ";".join(det))

# ---- frozen values F(4..12)
frozen = [20540, 784245, 31763004, 1340246340, 58281448940, 2593593086150, 117544525178080, 5406686759963586, 251754316822792420]
chk("L310_frozen_F20(4..12)", [F(n) for n in range(4, 13)] == frozen, ",".join(str(F(n)) for n in range(4, 13)))

# ---- Lemma 3.11: ratio identity, strict increase, below mu, factor gap identity, mu bracket
ok_id = ok_inc = ok_mu = ok_gap = True
NMAX = 400
for n in range(0, NMAX + 1):
    num = 20
    den = 1
    for j in range(1, 20):
        num *= (20 * n + j)
        den *= (19 * n + j + 1)
        # 20/19 - f_j = (j+20)/(19(19n+j+1)):  (20(19n+j+1) - 19(20n+j)) == j + 20
        if 20 * (19 * n + j + 1) - 19 * (20 * n + j) != j + 20:
            ok_gap = False
        # f_j increasing: f_j(n+1) > f_j(n)
        if (20 * (n + 1) + j) * (19 * n + j + 1) <= (20 * n + j) * (19 * (n + 1) + j + 1):
            ok_inc = False
    if F(n + 1) * den != F(n) * num:
        ok_id = False
    if not (F(n + 1) * 19 ** 19 < F(n) * 20 ** 20):
        ok_mu = False
    if n >= 1 and not (F(n + 1) * F(n - 1) > F(n) * F(n)):
        ok_inc = False
chk("L311_ratio_product_identity_n0..400", ok_id)
chk("L311_factors_and_ratio_strictly_increasing_n0..400", ok_inc)
chk("L311_ratio_below_mu_n0..400", ok_mu)
chk("L311_factor_gap_identity_j+20", ok_gap)
mu_lo = 5300068 * 19 ** 19 <= 100000 * 20 ** 20
mu_hi = 100000 * 20 ** 20 <= 5300069 * 19 ** 19
chk("L311_mu_in_[53.00068,53.00069]", mu_lo and mu_hi)
# mu = 20 (20/19)^19 = 20^20/19^19
chk("L311_mu_identity", 20 * 20 ** 19 == 20 ** 20)
# tends to mu: the ratio at n = 10^6 is within 10^-3 of mu (checked via the product bound of the gaps)
n = 10 ** 6
num = 20; den = 1
for j in range(1, 20):
    num *= (20 * n + j); den *= (19 * n + j + 1)
# mu - r < 1/1000  <=>  1000 (20^20 den - 19^19 num) < 19^19 den
chk("L311_ratio_close_to_mu_at_n=10^6", 1000 * (20 ** 20 * den - 19 ** 19 * num) < 19 ** 19 * den)

# ---- Corollary 3.12: tail ratio F(49+j) <= F(49) mu^j, j = 0..300
ok = all(F(49 + j) * 19 ** (19 * j) <= F(49) * 20 ** (20 * j) for j in range(0, 301))
chk("C312_F(49+j)<=F(49)mu^j_j0..300", ok)
# termwise domination at sample points: sum_{n=49}^{49+J} 6F(n) y^n <= 6F(49) y^49 / (1 - mu y) at y = p/q with mu y < 1
ok = True
for (p, q) in ((1, 60), (1, 54), (1, 100), (1, 1000)):
    if not (20 ** 20 * p < 19 ** 19 * q):
        continue
    J = 200
    # LHS * q^(49+J) as integer, RHS: 6F(49) p^49 / q^49 * 1/(1 - mu p/q) = 6F(49) p^49 q 19^19 / (q^49 (19^19 q - 20^20 p))
    lhs_num = sum(6 * F(n) * p ** n * q ** (49 + J - n) for n in range(49, 49 + J + 1))
    lhs_den = q ** (49 + J)
    rhs_num = 6 * F(49) * p ** 49 * q * 19 ** 19
    rhs_den = q ** 49 * (19 ** 19 * q - 20 ** 20 * p)
    if not (lhs_num * rhs_den <= rhs_num * lhs_den):
        ok = False
chk("C312_partial_tail_sums_below_closed_tail_at_y=1/60,1/54,1/100,1/1000", ok)
# S(y e^-s) <= e^{-4s} S(y): termwise, every term has degree >= 4 and the pole factor decreases; checked as monotone in the
# substitution y -> y t with 0 < t <= 1 rational: S(y t) <= t^4 S(y) at y = 1/60, t in {1/2, 9/10, 99/100}
def S_closed(p, q, head):
    # returns S(p/q) as an integer pair; head = dict n -> N(n) for n = 4..10
    terms = []
    num = 0
    den = 1
    def addq(a, b, c, d):
        return a * d + c * b, b * d
    for n in range(4, 11):
        num, den = addq(num, den, head[n] * p ** n, q ** n)
    for n in range(11, 49):
        num, den = addq(num, den, 6 * F(n) * p ** n, q ** n)
    # 6F(49) y^49 / (1 - mu y), mu y = 20^20 p / (19^19 q)
    tn = 6 * F(49) * p ** 49 * 19 ** 19 * q
    td = q ** 49 * (19 ** 19 * q - 20 ** 20 * p)
    num, den = addq(num, den, tn, td)
    return num, den
crude = {n: 6 * F(n) for n in range(4, 11)}
ok = True
for (tp, tq) in ((1, 2), (9, 10), (99, 100)):
    a, b = S_closed(1 * tp, 60 * tq, crude)
    c, d = S_closed(1, 60, crude)
    # a/b <= (tp/tq)^4 c/d
    if not (a * d * tq ** 4 <= tp ** 4 * c * b):
        ok = False
chk("C312_S(yt)<=t^4_S(y)_samples", ok)
# crude head validity rests on Lemma 3.9 + 3.10 (N_w(n) <= 6 t_20(n) = 6 F(n)); 6F(1..5)
chk("C312_6F20(1..5)", [6 * F(n) for n in range(1, 6)] == [6, 120, 3540, 123240, 4705470])

for line in out:
    print(line)
print("CNT_SUMMARY|all_ok=%d|tag=MEASURED|json=0" % int(allok))
