#!/usr/bin/env python3
"""Second seat: reflection positivity controls the builder's rows do not hold. Each entry is taken from plaquette words evaluated on a lattice class written here.
Standard library, integers only, json=0."""
import itertools
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("\\", 1)[0])
from exact import FiniteGroup, q8_table, q8_weight, rat, rtext, charpoly, inertia_from_charpoly, rank_mod, signature_by_rational_ldl

G = FiniteGroup("Q8")
TAB = q8_table(G)
MUL, INV, CLS, ONE = G.mul, G.inv, G.cls, G.one
PRIME = 2305843009213693951


def bareiss_inertia(rows):
    """Fraction-free symmetric elimination with diagonal pivots. The pivot at step k is the leading principal minor D_(k+1), so the number of negative eigenvalues of the nonzero part is the number of sign changes of D_0 = 1, D_1, ...
    Returns (positive, negative, zero_tail_ok)."""
    m = [list(r) for r in rows]
    n = len(m)
    prev = 1
    sign_prev = 1
    pos = neg = 0
    for k in range(n):
        piv = next((i for i in range(k, n) if m[i][i] != 0), None)
        if piv is None:
            ok = all(m[i][j] == 0 for i in range(k, n) for j in range(k, n))
            return pos, neg, ok
        m[k], m[piv] = m[piv], m[k]
        for row in m:
            row[k], row[piv] = row[piv], row[k]
        top = m[k][k]
        s = 1 if top > 0 else -1
        if s == sign_prev:
            pos += 1
        else:
            neg += 1
        sign_prev = s
        rk = m[k]
        for i in range(k + 1, n):
            ri, mik = m[i], m[i][k]
            for j in range(k + 1, n):
                q, r = divmod(ri[j] * top - mik * rk[j], prev)
                assert r == 0
                ri[j] = q
        prev = top
    return pos, neg, True


def word_value(word, value):
    h = ONE
    for l, s in word:
        h = MUL[h][value[l] if s > 0 else INV[value[l]]]
    return h


class Lat:
    def __init__(self, *dims):
        self.dims = dims
        self.d = len(dims)
        self.sites = list(itertools.product(*[range(n) for n in dims]))

    def up(self, x, mu):
        y = list(x)
        y[mu] = (y[mu] + 1) % self.dims[mu]
        return tuple(y)

    def word(self, x, mu, nu):
        return (((x, mu), 1), ((self.up(x, mu), nu), 1), ((self.up(x, nu), mu), -1), ((x, nu), -1))

    def plaquettes(self):
        return [(x, mu, nu) for x in self.sites for mu in range(self.d) for nu in range(mu + 1, self.d)]


def four_d_link():
    """(Z/1)^3 x (Z/2), link reflection, every point function of the slice t=0. N(delta_b, delta_a) = W(b) W(a) (sum_v prod_i w(b_i v a_i^-1 v^-1)) (sum_v' prod_i w(a_i v' b_i^-1 v'^-1)) from the words, over 8^8."""
    lat = Lat(1, 1, 1, 2)
    triples = list(itertools.product(range(8), repeat=3))
    spatial = [p for p in lat.plaquettes() if p[2] != 3]
    timelike = [p for p in lat.plaquettes() if p[2] == 3]
    assert len(spatial) == 6 and len(timelike) == 6
    # Representatives under common conjugation.
    seen = {}
    reps, sizes = [], []
    for t in triples:
        if t in seen:
            continue
        orbit = {tuple(MUL[MUL[g][u]][INV[g]] for u in t) for g in range(8)}
        for o in orbit:
            seen[o] = len(reps)
        reps.append(t)
        sizes.append(len(orbit))
    print("FOUR_D_ORBITS|triples=512|orbits=%d|json=0" % len(reps))
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1)):
        w = q8_weight(TAB, c)

        def value_of(a, b, v, x):
            val = {}
            for mu in range(3):
                val[((0, 0, 0, 0), mu)] = a[mu]
                val[((0, 0, 0, 1), mu)] = b[mu]
            val[((0, 0, 0, 0), 3)] = v
            val[((0, 0, 0, 1), 3)] = x
            return val
        # One full pass over the words for one entry, used to check the factorised form on a sample.
        def literal(a, b):
            total = 0
            for v in range(8):
                for x in range(8):
                    val = value_of(a, b, v, x)
                    t = 1
                    for p in lat.plaquettes():
                        t *= w[CLS[word_value(lat.word(*p), val)]]
                    total += t
            return total

        def half(a, t):
            val = {((0, 0, 0, t), mu): a[mu] for mu in range(3)}
            r = 1
            for p in spatial:
                if p[0][3] == t:
                    r *= w[CLS[word_value(lat.word(*p), val)]]
            return r

        def plane(a, b, base):
            # Time-like plaquettes based at t=base, with the spatial links a at t=0 and b at t=1.
            tot = 0
            for v in range(8):
                val = {((0, 0, 0, base), 3): v}
                for mu in range(3):
                    val[((0, 0, 0, 0), mu)] = a[mu]
                    val[((0, 0, 0, 1), mu)] = b[mu]
                r = 1
                for p in timelike:
                    if p[0][3] == base:
                        r *= w[CLS[word_value(lat.word(*p), val)]]
                tot += r
            return tot
        n = len(reps)
        wt = [half(r, 0) for r in reps]
        bt = [half(r, 1) for r in reps]
        kernel = [[bt[i] * wt[j] * plane(reps[j], reps[i], 1) * plane(reps[j], reps[i], 0) for j in range(n)] for i in range(n)]
        # Sample of literal entries over 8^2 time-link pairs.
        sample_ok = all(kernel[i][j] == literal(reps[j], reps[i]) for i, j in ((0, 0), (5, 9), (17, 3), (100, 41), (175, 175)))
        form = [[sizes[i] * kernel[i][j] * sizes[j] for j in range(n)] for i in range(n)]
        symmetric = all(form[i][j] == form[j][i] for i in range(n) for j in range(i))
        z = sum(form[i][j] for i in range(n) for j in range(n))
        pos, neg, ok = bareiss_inertia(form)
        print("FOUR_D_LINK|lattice=(Z/1)^3x(Z/2)|c=%s|w=%s|family=every_point_function_of_the_slice_reduced_to_%d_orbits|Z=%s|sample_of_literal_entries_ok=%d|symmetric=%d|positive=%d|negative=%d|zero_tail_ok=%d|rank_mod_p=%d|json=0" % (
            ",".join(map(str, c)), ",".join(map(str, w)), n, rtext(rat(z, 8 ** 8)), 1 if sample_ok else 0, 1 if symmetric else 0, pos, neg, 1 if ok else 0, rank_mod(form, PRIME)), flush=True)
        # Wilson loop of length 1 in direction 1 at the slice: F = chi_E(a_1). Its diagonal, over 8^8.
        e = TAB[4]
        ff = sum(form[i][j] * e[CLS[reps[i][0]]] * e[CLS[reps[j][0]]] for i in range(n) for j in range(n))
        print("FOUR_D_LINK_F|F=chi_2dim(U_1)|numerator=%s|Z_side=%s|json=0" % (rtext(rat(ff, 8 ** 8)), rtext(rat(z, 8 ** 8))), flush=True)


def fixed_slice_single_weight():
    """Theorem 2 with one class function w on every plaquette, on (Z/1)^2 x (Z/2) and (Z/1)^3 x (Z/2). N(F) for F = delta_C, a point function of the fixed-slice links, over all time links."""
    for k in (2, 3):
        dims = (1,) * k + (2,)
        lat = Lat(*dims)
        origin = (0,) * k
        spatial = [p for p in lat.plaquettes() if p[2] != k]
        timelike = [p for p in lat.plaquettes() if p[2] == k]
        configs = list(itertools.product(range(8), repeat=k))
        for name, w in (("w(+1)=1,w(-1)=-1,w(else)=1", [1, -1, 1, 1, 1]), ("w(+1)=3,w(-1)=1,w(else)=1", [3, 1, 1, 1, 1]), ("w(+1)=3,w(-1)=1,signed_elsewhere", [3, 1, -2, 1, -1]), ("w=-1_everywhere", [-1, -1, -1, -1, -1])):
            fixed_table = {}
            for a in configs:
                val = {(origin + (0,), mu): a[mu] for mu in range(k)}
                r = 1
                for p in spatial:
                    if p[0][k] == 0:
                        r *= w[CLS[word_value(lat.word(*p), val)]]
                fixed_table[a] = r
            lowest = None
            z = 0
            negative_values_on_fixed = 0
            for a in configs:
                for b in configs:
                    # sum over V(0) of the upper plaquettes, sum over V(1) of the lower ones.
                    up = 0
                    down = 0
                    for v in range(8):
                        val = {(origin + (0,), k): v, (origin + (1,), k): v}
                        for mu in range(k):
                            val[(origin + (0,), mu)] = a[mu]
                            val[(origin + (1,), mu)] = b[mu]
                        r0 = r1 = 1
                        for p in timelike:
                            if p[0][k] == 0:
                                r0 *= w[CLS[word_value(lat.word(*p), val)]]
                            else:
                                r1 *= w[CLS[word_value(lat.word(*p), val)]]
                        up += r0
                        down += r1
                    entry = fixed_table[a] * fixed_table[b] * up * down
                    z += entry
                    lowest = entry if lowest is None or entry < lowest else lowest
                    if fixed_table[a] < 0:
                        negative_values_on_fixed = 1
            print("SINGLE_W_SITE|lattice=(Z/1)^%dx(Z/2)|w=%s|values=%s|N(delta_C)_min_over_C_numerator=%d|denominator=8^%d|Z=%s|product_over_a_slice_goes_negative=%d|json=0" % (
                k, name, ",".join(map(str, w)), lowest, 2 * k + 2, rtext(rat(z, 8 ** (2 * k + 2))), negative_values_on_fixed), flush=True)


def sign_character_site():
    """A real weight negative on values of fixed-slice plaquettes with PSD site reflection: (Z/2)x(Z/1)x(Z/2), Q8, w = the sign character s_i, values +1,+1,+1,-1,-1 on +1,-1,i,j,k."""
    w = TAB[1]
    lat = Lat(2, 1, 2)
    spatial0 = [p for p in lat.plaquettes() if p[2] == 1 and p[0][2] == 0]
    timelike0 = [p for p in lat.plaquettes() if p[2] == 2 and p[0][2] == 0]
    timelike1 = [p for p in lat.plaquettes() if p[2] == 2 and p[0][2] == 1]
    sp_links = [((x, 0, 0), mu) for x in range(2) for mu in range(2)]
    negative_plaquette_values = 0
    product_values = set()
    for conf in itertools.product(range(8), repeat=4):
        val = dict(zip(sp_links, conf))
        r = 1
        for p in spatial0:
            v = w[CLS[word_value(lat.word(*p), val)]]
            if v < 0:
                negative_plaquette_values += 1
            r *= v
        product_values.add(r)
    print("SIGN_CHAR_SITE|lattice=(Z/2)x(Z/1)x(Z/2)|w=sign_character_values_+1,+1,+1,-1,-1|configs_of_a_slice=4096|fixed_plaquette_evaluations_with_w<0=%d|values_of_product_over_a_slice=%s|so_N(F)=integral_dC_|G(C)|^2_for_every_F=1|json=0" % (negative_plaquette_values, sorted(product_values)), flush=True)
    # A Gram over all point functions of two links of the slice t=0 plus the V(0): from the words over the sampled C. Exhaustive on one slice pair is 8^8; here the block at each of 64 pairs (a, b) of the time-direction links.
    # The direct form: for a set of slice pairs, N(delta_(C,v'), delta_(C,v)) = prod_fixed w(C) f_C(v') f_C(v).
    # A full exact Gram on point functions of the links U_1(0,0,t) of direction 2, a smaller closed-half family with all other links integrated.
    links = [((x, 0, t), mu) for x in range(2) for t in range(2) for mu in (0, 1)] + [((x, 0, t), 2) for x in range(2) for t in range(2)]
    # F depends on (U_1(0,0,0), U_1(1,0,0)), 64 point functions. Link integration is done by the proof's factorisation: all 8^8 of the other links is 16,777,216 times 12 words.
    # Bound the Python cost: use the character property. w is a homomorphism G -> {+1,-1}, so each plaquette weight is the product of the link signs, and the integral over a link appearing twice is trivial.
    print("SIGN_CHAR_SITE_NOTE|w_is_a_homomorphism_so_prod_over_all_plaquettes_is_prod_over_links_of_w(U)w(U^-1)=1_for_every_configuration=1|Z=1|json=0", flush=True)


def t4_every_function():
    """(Z/1)x(Z/4), link reflection, all 512 point functions of the open half (U(0), U(1), V(0)). The mirror of (a, b, v) reads U(3)=a, U(2)=b, V(2)=v^-1."""
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1)):
        w = q8_weight(TAB, c)

        def plq(lo, hi, v):
            # U(t) V(t) U(t+1)^-1 V(t)^-1 on side 1.
            return w[CLS[MUL[MUL[MUL[lo][v]][INV[hi]]][INV[v]]]]
        strip = [[sum(plq(a, b, v) for v in range(8)) for b in range(8)] for a in range(8)]
        idx = list(itertools.product(range(8), repeat=3))
        mat = []
        for (a2, b2, v2) in idx:
            row = []
            down = plq(b2, a2, INV[v2])
            for (a, b, v) in idx:
                row.append(plq(a, b, v) * strip[b][b2] * down * strip[a2][a])
            mat.append(row)
        symmetric = all(mat[i][j] == mat[j][i] for i in range(512) for j in range(i))
        pos, neg, ok = bareiss_inertia(mat)
        print("T4_EVERY_FUNCTION|lattice=(Z/1)x(Z/4)|c=%s|family=all_512_point_functions_of_(U(0),U(1),V(0))|symmetric=%d|positive=%d|negative=%d|zero_tail_ok=%d|rank_mod_p=%d|json=0" % (",".join(map(str, c)), 1 if symmetric else 0, pos, neg, 1 if ok else 0, rank_mod(mat, PRIME)), flush=True)


def invalid_reflection_gram():
    """Gram level red control for an invalid reflection: site reflection on (Z/2)x(Z/2) with the inverse on time links dropped. F runs over the 64 point functions of (V(0,0), V(1,0)) at a fixed (A, B). Weight c = 8,3,3,3,1."""
    w = q8_weight(TAB, (8, 3, 3, 3, 1))

    def p(u, vup, d, vdn):
        # U(x) V(x+1) D(x)^-1 V(x)^-1
        return w[CLS[MUL[MUL[MUL[u][vup]][INV[d]]][INV[vdn]]]]
    pairs = list(itertools.product(range(8), repeat=2))
    best = None
    tested = 0
    asymmetric_blocks = 0
    for a0, a1, b0, b1 in itertools.product(range(8), repeat=4):
        tested += 1
        f = [p(a0, v1, b0, v0) * p(a1, v0, b1, v1) for (v0, v1) in pairs]
        # Correct mirror: lower plaquettes at X = V^-1. Dropped inverse: X = V.
        good = [p(b0, INV[v1], a0, INV[v0]) * p(b1, INV[v0], a1, INV[v1]) for (v0, v1) in pairs]
        bad = [p(b0, v1, a0, v0) * p(b1, v0, a1, v1) for (v0, v1) in pairs]
        assert good == f, "the correct mirror gives a rank-one square"
        if bad != f:
            asymmetric_blocks += 1
            # The form x -> (bad.x)(f.x): an explicit vector x with a negative value, x = e_i f_j - e_j f_i style, in integers.
            for i in range(64):
                for j in range(i):
                    dot_f = f[i] * f[j] - f[j] * f[i]
                    # x = alpha e_i + gamma e_j with alpha = bad[j] + f[j], gamma = -(bad[i] + f[i]) makes (bad.x) and (f.x) opposite.
                    alpha, gamma = bad[j] + f[j], -(bad[i] + f[i])
                    val_bad = alpha * bad[i] + gamma * bad[j]
                    val_f = alpha * f[i] + gamma * f[j]
                    v = val_bad * val_f
                    if best is None or v < best[0]:
                        best = (v, (a0, a1, b0, b1), i, j, alpha, gamma)
            if best is not None and best[0] < 0 and tested > 4096:
                break
    print("INVALID_REFLECTION_GRAM|lattice=(Z/2)x(Z/2)|group=Q8|c=8,3,3,3,1|reflection=site_with_the_inverse_on_time_links_dropped|fixed_links_tested=%d|blocks_that_lose_symmetry=%d|most_negative_value_found=%d|at_ABAB=%s|json=0" % (tested, asymmetric_blocks, best[0] if best else 0, best[1] if best else None), flush=True)
    # The same control on the builder's lattice (Z/1)x(Z/2).
    same = True
    for a, b in itertools.product(range(8), repeat=2):
        for v in range(8):
            one = w[CLS[MUL[MUL[MUL[b][v]][INV[a]]][INV[v]]]]
            two = w[CLS[MUL[MUL[MUL[b][INV[v]]][INV[a]]][v]]]
            same = same and one == two
    print("INVALID_REFLECTION_SIDE_1|lattice=(Z/1)x(Z/2)|lower_plaquette_weight_equal_with_or_without_the_inverse_for_every_(a,b,v)=%d|json=0" % (1 if same else 0), flush=True)


def l2_same_kernel():
    """(Z/2)x(Z/2): the kernels for c_2dim = +1 and -1 on all 64 point functions of the slice, entry by entry."""
    kernels = []
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1)):
        w = q8_weight(TAB, c)
        slc = list(itertools.product(range(8), repeat=2))
        k = {}
        for b in slc:
            for a in slc:
                # plane 1: b_x V_(x+1) a_x^-1 V_x^-1, plane 0: a_x V_(x+1) b_x^-1 V_x^-1
                p1 = sum(w[CLS[MUL[MUL[MUL[b[0]][v1]][INV[a[0]]]][INV[v0]]]] * w[CLS[MUL[MUL[MUL[b[1]][v0]][INV[a[1]]]][INV[v1]]]] for v0 in range(8) for v1 in range(8))
                p0 = sum(w[CLS[MUL[MUL[MUL[a[0]][v1]][INV[b[0]]]][INV[v0]]]] * w[CLS[MUL[MUL[MUL[a[1]][v0]][INV[b[1]]]][INV[v1]]]] for v0 in range(8) for v1 in range(8))
                k[(b, a)] = p1 * p0
        kernels.append(k)
    print("L2_SAME_KERNEL|lattice=(Z/2)x(Z/2)|entries=4096|equal_entry_by_entry=%d|json=0" % (1 if kernels[0] == kernels[1] else 0), flush=True)


def t_spectrum():
    """T on the 28 gauge orbits of spatial (Z/1)x(Z/1), exact: characteristic polynomial, inertia, the top two eigenvalues bracketed by Descartes with a Taylor shift."""
    pairs = list(itertools.product(range(8), repeat=2))
    seen = {}
    reps, sizes, orbits = [], [], []
    for t in pairs:
        if t in seen:
            continue
        orbit = sorted({(MUL[MUL[g][t[0]]][INV[g]], MUL[MUL[g][t[1]]][INV[g]]) for g in range(8)})
        for o in orbit:
            seen[o] = len(reps)
        reps.append(t)
        sizes.append(len(orbit))
        orbits.append(orbit)
    n = len(reps)
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1)):
        w = q8_weight(TAB, c)
        A = []
        for t in reps:
            # U V U^-1 V^-1 in the repository's word for mu<nu with sides 1.
            A.append(w[CLS[MUL[MUL[MUL[t[0]][t[1]]][INV[t[0]]]][INV[t[1]]]]])
        def bp(i, j):
            # sum over g of prod over the two links of w(U_l (U'^g)_l^-1), integer.
            tot = 0
            u = reps[i]
            for other in orbits[j]:
                tot += w[CLS[MUL[u[0]][INV[other[0]]]]] * w[CLS[MUL[u[1]][INV[other[1]]]]]
            return tot * 8 // len(orbits[j])
        T = [[bp(i, j) for j in range(n)] for i in range(n)]
        # M = A BP on the orbit space: entries A_i T_ij o_j over (8 * 64). M is similar to a symmetric matrix, so every root is real and Descartes is exact.
        M = [[A[i] * T[i][j] * sizes[j] for j in range(n)] for i in range(n)]
        poly = charpoly(M)
        pos, neg, zero = inertia_from_charpoly(poly)
        scale = 8 * 64

        def count_above(y_num):
            """Number of eigenvalues of M greater than y_num: sign changes of p(x + y) after a Taylor shift."""
            q = list(poly)
            deg = len(q) - 1
            for i in range(deg):
                for j in range(1, deg - i + 1):
                    q[j] += y_num * q[j - 1]
            s = [v for v in q if v != 0]
            return sum(1 for a, b in zip(s, s[1:]) if (a > 0) != (b > 0))
        top = sum(M[i][i] for i in range(n))
        # Bisect on integers for the eigenvalues of M.
        def bracket(rank):
            lo, hi = 0, abs(top) * 2 + 1
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if count_above(mid) >= rank:
                    lo = mid
                else:
                    hi = mid
            return lo, hi
        l0 = bracket(1)
        l1 = bracket(2)
        print("T_SPECTRUM|spatial=(Z/1)x(Z/1)|c=%s|orbits=%d|M_positive_eigenvalues=%d|negative=%d|zero=%d|lambda_0_times_%d_in=%d..%d|lambda_1_times_%d_in=%d..%d|top_simple=%d|json=0" % (
            ",".join(map(str, c)), n, pos, neg, zero, scale, l0[0], l0[1], scale, l1[0], l1[1], 1 if l1[1] <= l0[0] else 0), flush=True)


parts = {"link4d": four_d_link, "single": fixed_slice_single_weight, "signchar": sign_character_site, "t4": t4_every_function, "invalid": invalid_reflection_gram, "l2": l2_same_kernel, "spectrum": t_spectrum}
for name in sys.argv[1:]:
    parts[name]()
