# Step 3 orientation read on finite groups, the five Q8 counts by my own gauge fixing, and class-sign bands on SU(2) at side 1 with exact rationals. Integers only. json=0.
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep import *
import su2_lib as Q


# ---- Step 3: s(U_p) = s(u x_i) needs both the class property and w(g^-1) = w(g). F21 has classes that inversion swaps.
def read_step3(G, dims, seed, draws):
    lat = Lat(*dims)
    rng = RNG(seed)
    same_conj = same_merged = total = 0
    for _ in range(draws):
        cfg = [rng.below(G.n) for _ in lat.links]
        for l in range(len(lat.links)):
            for w in lat.words:
                pos = [i for i, (a, e) in enumerate(w) if a == l]
                if not pos:
                    continue
                i = pos[0]
                word = list(w[i:]) + list(w[:i])
                if word[0][1] < 0:
                    word = [(a, -e) for a, e in reversed(word)]
                    j = [t for t, (a, e) in enumerate(word) if a == l and e > 0][0]
                    word = word[j:] + word[:j]
                u = cfg[l]
                x = 0
                for a, e in word[1:]:
                    x = G.tab[x][cfg[a] if e > 0 else G.inv[cfg[a]]]
                value = G.tab[u][x]
                original = hol(G, cfg, w)
                total += 1
                same_conj += 1 if G.conj_of[value] == G.conj_of[original] else 0
                same_merged += 1 if G.mc_of[value] == G.mc_of[original] else 0
    print("IND_STEP3|group=%s|lattice=%s|reads=%d|u_x_i_in_the_same_conjugacy_class=%d|u_x_i_in_the_same_inversion_closed_class=%d|json=0" % (G.name, "x".join(map(str, dims)), total, same_conj, same_merged))


read_step3(Q8_mat(), (2, 2), 1, 200)
read_step3(F21(), (2, 2), 2, 200)
read_step3(SL23(), (2, 2, 2), 3, 40)
read_step3(S(3), (2, 3), 4, 100)

# ---- The five Q8 weights over 8^5 gauge-fixed configurations on (Z/2)x(Z/2), with my tree. Q8 from matrices, so name the classes by element order and centrality.
q8 = Q8_mat()
minus = next(i for i in range(8) if i and q8.tab[i][i] == 0)
others = sorted(set(q8.mc_of[i] for i in range(8)) - {q8.mc_of[0], q8.mc_of[minus]})
# Each of the three noncentral classes plays i, j, k. The counts for the two off-rule weights are invariant under permuting them, by Aut(Q8) acting as S3.
w_list = ((3, 2, 1, -1, -2), (1, 1, 1, -1, -1), (-1, -1, -1, -1, -1), (3, 2, 1, -1, 2), (1, -1, 1, 1, 1))
order = [q8.mc_of[0], q8.mc_of[minus]] + others
lat = Lat(2, 2)
ex, nf = exhaustive_parities(q8, lat)
for w in w_list:
    mask = sum(1 << order[c] for c, v in enumerate(w) if v < 0)
    negative = sum(n for p, n in ex.items() if popcount(mask & p) & 1)
    print("IND_FIVE|w=%s|lattice=2x2|configs=%d|negative=%d|json=0" % (",".join(map(str, w)), sum(ex.values()), negative))


# ---- SU(2): class signs from real-part bands, on the side-1 slices, against exact rational configurations. Each pattern is a sign of the real part on a union of bands.
def sign_on_real(q, cuts):
    """+1 or -1 by how many cuts (numerator, denominator) sit at or below the real part a/den. None exactly on a cut."""
    a, den = q[0], q[4]
    count = 0
    for cn, cd in cuts:
        left, right = a * cd, cn * den
        if left == right:
            return 0
        if left > right:
            count += 1
    return -1 if count % 2 else 1


patterns = [[(0, 1)], [(1, 2)], [(-1, 2)], [(3, 4)], [(-3, 4)], [(9, 10)], [(-9, 10)], [(-1, 2), (1, 2)], [(1, 4), (3, 4)], [(-3, 4), (-1, 4)], [(-9, 10), (9, 10)], [(-1, 2), (0, 1), (1, 2)], [(-3, 4), (-1, 2), (-1, 4), (1, 4), (1, 2), (3, 4)], [(99, 100)], [(-99, 100)]]
for dims, seed in (((2, 1), 701), ((1, 1), 702), ((3, 1), 703), ((2, 1, 1), 704), ((1, 1, 1), 705)):
    lat = Lat(*dims)
    rng = RNG(seed)
    both = 0
    for cuts in patterns:
        vals = {}
        draws = 0
        while len(vals) < 2 and draws < 30000:
            draws += 1
            cfg = [Q.random_unit(rng) for _ in lat.links]
            s = 1
            for w in lat.words:
                s *= sign_on_real(Q.word_value(cfg, w), cuts)
                if s == 0:
                    break
            if s:
                vals[s] = 1
        both += 1 if len(vals) == 2 else 0
    print("IND_SU2_BANDS|lattice=%s|real_part_band_patterns=%d|patterns_showing_both_values_of_S=%d|json=0" % ("x".join(map(str, dims)), len(patterns), both))
    sys.stdout.flush()
print("IND_EXTRA_DONE|json=0")
