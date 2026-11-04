# Weight with zeros: w = 1, -1 on the central elements and 0 elsewhere, used on EVERY plaquette of the closed half.
# Reads f(C) and W_plus(C, A) of Lemma 0004 Theorem 2 directly, on lattices the note leaves out: k = 2, an odd side, sides of 1.
# Claim under test (DERIVED by the second seat): f(C) < 0 forces W_plus(C, .) to vanish, so site reflection positivity holds on every lattice.
# Integers only. json=0.
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep import *

q8 = Q8_mat()
MINUS = next(i for i in range(8) if i and q8.tab[i][i] == 0)
T, INV = q8.tab, q8.inv


def w(g):
    return 1 if g == 0 else (-1 if g == MINUS else 0)


def slice_g(lat, cfg):
    g = 1
    for word in lat.words:
        g *= w(hol(q8, cfg, word))
        if g == 0:
            return 0
    return g


def timelike_word_values(lat, C0, C1, V):
    """U_i(x,0) V(x+i) U_i(x,1)^-1 V(x)^-1 for each spatial link, using the repository's convention with time after space."""
    out = []
    for l, (x, mu) in enumerate(lat.links):
        vx = V[lat.sites.index(x)]
        vy = V[lat.sites.index(lat.step(x, mu))]
        out.append(T[T[T[C0[l]][vy]][INV[C1[l]]]][INV[vx]])
    return out


def all_slices(lat):
    return list(itertools.product(range(8), repeat=len(lat.links)))


# ---- Direct brute force on T = 2 for the smallest lattices: every C and every A.
for dims in ((1, 1),):
    lat = Lat(*dims)
    slices = all_slices(lat)
    gv = [slice_g(lat, c) for c in slices]
    neg = [c for c, g in zip(slices, gv) if g < 0]
    pos = [c for c, g in zip(slices, gv) if g > 0]
    nV = 8 ** len(lat.sites)
    Vs = list(itertools.product(range(8), repeat=len(lat.sites)))
    negative_f = 2 * len(neg) * len(pos)
    with_support = 0
    pairs_read = 0
    for a, b in itertools.chain(((n, p) for n in neg for p in pos), ((p, n) for n in neg for p in pos)):
        pairs_read += 1
        alive = False
        for V in Vs:
            if all(w(x) != 0 for x in timelike_word_values(lat, a, b, V)):
                alive = True
                break
        if alive:
            with_support += 1
    print("IND_ZERO_SRP_DIRECT|lattice=%sxT2|group=Q8|slices=%d|slice_g_-1=%d|slice_g_+1=%d|C_with_f<0=%d|of_those_with_W_plus_not_identically_0=%d|A_per_C=%d|json=0" % ("x".join(map(str, dims)), len(slices), len(neg), len(pos), negative_f, with_support, nV))
    sys.stdout.flush()


# ---- Exhaustive through the same statement read the other way, on T = 2: fix C0 with g != 0 and V, list all C1 with every time-like plaquette central
# (C1 link = +-V(x)^-1 C0 link V(x+i), which is every solution), and read g(C1) against g(C0).
def reachable_check(dims, cap_c0=None, cap_v=None, seed=1):
    lat = Lat(*dims)
    L = len(lat.links)
    pos = {x: i for i, x in enumerate(lat.sites)}
    ends = [(pos[x], pos[lat.step(x, mu)]) for x, mu in lat.links]
    rng = RNG(seed)
    # central slices: sample or enumerate
    read = differ = dead = 0
    negative_seen = positive_seen = 0
    total_slices = 8 ** L
    if total_slices <= 4096 * 16:
        c0s = (c for c in itertools.product(range(8), repeat=L))
    else:
        # build central slices from a flat V4 field on Z/2 lifts by rejection-free method: gauge transform of a twisted or trivial base, plus central signs
        def gen():
            while True:
                yield random_central(lat, rng)
        c0s = gen()
    count = 0
    n_sites = len(lat.sites)
    for c0 in c0s:
        g0 = slice_g(lat, c0)
        if g0 == 0:
            continue
        count += 1
        if cap_c0 and count > cap_c0:
            break
        negative_seen += 1 if g0 < 0 else 0
        positive_seen += 1 if g0 > 0 else 0
        if 8 ** n_sites <= (cap_v or 8 ** n_sites):
            vs = itertools.product(range(8), repeat=n_sites)
        else:
            vs = (tuple(rng.below(8) for _ in range(n_sites)) for _ in range(cap_v))
        for V in vs:
            base = [T[T[INV[V[a]]][c0[l]]][V[b]] for l, (a, b) in enumerate(ends)]
            # all sign choices when small, a sample when large
            if L <= 4:
                choices = itertools.product((0, 1), repeat=L)
            else:
                choices = (tuple(rng.below(2) for _ in range(L)) for _ in range(32))
            for flips in choices:
                c1 = [T[MINUS][x] if f else x for x, f in zip(base, flips)]
                assert all(w(y) != 0 for y in timelike_word_values(lat, c0, c1, V))
                g1 = slice_g(lat, c1)
                read += 1
                if g1 == 0:
                    dead += 1
                elif g1 != g0:
                    differ += 1
    print("IND_ZERO_SRP_REACHABLE|lattice=%sxT2|group=Q8|C0_read=%d|with_g_-1=%d|with_g_+1=%d|C1_read_with_every_time_like_plaquette_central=%d|g(C1)=0_on=%d|g(C1)_opposite_g(C0)_on=%d|json=0" % ("x".join(map(str, dims)), min(count, cap_c0 or count), negative_seen, positive_seen, read, dead, differ))
    sys.stdout.flush()


def random_central(lat, rng):
    """A random configuration with all plaquettes central: projected flat field on Q8/{+-1} from a gauge term and holonomy, lifted at random.
    Holonomies per direction, i on direction-a links at coordinate 0 and j on direction-b links at coordinate 0 with random a, b gives the twist."""
    I, J = 1, 2
    # find i and j as two noncommuting elements of order 4
    els = [x for x in range(8) if x not in (0, MINUS)]
    i = els[0]
    j = next(y for y in els if T[i][y] != T[y][i])
    cfg = [0] * len(lat.links)
    k = lat.k
    # choose for each direction a value in the Klein quotient, realized on coordinate 0 of that direction
    vals = [0, i, j, T[i][j]]
    pick = [vals[rng.below(4)] for _ in range(k)]
    for l, (x, mu) in enumerate(lat.links):
        cfg[l] = pick[mu] if x[mu] == 0 else 0
    # gauge transform
    g = [rng.below(8) for _ in lat.sites]
    pos = {x: n for n, x in enumerate(lat.sites)}
    for l, (x, mu) in enumerate(lat.links):
        cfg[l] = T[T[g[pos[x]]][cfg[l]]][INV[g[pos[lat.step(x, mu)]]]]
    # central lifts
    for l in range(len(cfg)):
        if rng.below(2):
            cfg[l] = T[MINUS][cfg[l]]
    return tuple(cfg)


reachable_check((1, 1))
reachable_check((3, 1), cap_c0=400, cap_v=16)
reachable_check((2, 2), cap_c0=400, cap_v=16)
reachable_check((3, 3), cap_c0=200, cap_v=16)
reachable_check((2, 2, 2), cap_c0=120, cap_v=16)
reachable_check((2, 2, 3), cap_c0=120, cap_v=16)
reachable_check((1, 1, 1), cap_c0=None)
reachable_check((3, 3, 3), cap_c0=40, cap_v=8)


# ---- T = 4, the smallest closed half with a slice inside: (Z/1)x(Z/1)xZ/4. Every C = (C0, C2), every A = (V0, V1, C1).
lat = Lat(1, 1)
slices = all_slices(lat)
gv = {c: slice_g(lat, c) for c in slices}
neg = [c for c in slices if gv[c] < 0]
pos = [c for c in slices if gv[c] > 0]
mid = [c for c in slices if gv[c] != 0]
central_neighbours = {}
for c in mid:
    pass
# reach[c] = set of slices reachable through one layer, with every time-like plaquette central
reach = {}
for c0 in mid:
    out = set()
    for v in range(8):
        for f in itertools.product((0, 1), repeat=2):
            c1 = tuple(T[T[INV[v]][c0[l]]][v] if not f[l] else T[MINUS][T[T[INV[v]][c0[l]]][v]] for l in range(2))
            out.add(c1)
    reach[c0] = out
two_layer_opposite = 0
for c0 in mid:
    for c1 in reach[c0]:
        if gv[c1] == 0:
            continue
        for c2 in reach[c1]:
            if gv[c2] != 0 and gv[c2] != gv[c0]:
                two_layer_opposite += 1
print("IND_ZERO_SRP_T4|lattice=1x1xT4|group=Q8|slices_with_g_nonzero=%d|paths_C0_C1_C2_with_every_plaquette_central_and_g(C2)_opposite_g(C0)=%d|json=0" % (len(mid), two_layer_opposite))


# ---- N_w(F) itself on (Z/1)x(Z/1)xZ/2, in integers, against the plaquette-dependent control of Lemma 0004.
# Numbers are scaled by the group orders, so they stay integers. N(F) carries 8^(number of links) in the denominator.
lat = Lat(1, 1)
slices = all_slices(lat)
sign = {c: slice_g(lat, c) for c in slices}
s_of = {}
for c in slices:
    # commutator sign
    v = hol(q8, c, lat.words[0])
    s_of[c] = 1 if v == 0 else -1
# (a) the Lemma's control, w on fixed slices and 1 on time-like plaquettes: F = indicator(s0=-1, s1=+1). N(F) = -15/64.
num = 0
for a in slices:
    for b in slices:
        if s_of[a] == -1 and s_of[b] == 1:
            num += s_of[a] * s_of[b]
print("IND_LEMMA_CONTROL|lattice=1x1xT2|time_like_weight=1|fixed_weight=1,-1|N(F)=%d/%d|reduced_expected=-15/64|json=0" % (num, 8 ** 4))
# (b) the same F with the one weight on every plaquette. G(C) = sum_V F W_plus.
Vs = range(8)
num_one_weight = 0
low = None
negatives = 0
for a in slices:
    for b in slices:
        f = sign[a] * sign[b]
        G = 0
        for v in Vs:
            wp = 1
            for l in range(2):
                wp *= w(T[T[T[a[l]][v]][INV[b[l]]]][INV[v]])
            G += wp
        val = f * G * G
        if s_of[a] == -1 and s_of[b] == 1 and f != 0:
            num_one_weight += val
        if low is None or val < low:
            low = val
        if val < 0:
            negatives += 1
print("IND_ONE_WEIGHT|lattice=1x1xT2|w=1,-1,0,0,0_on_every_plaquette|F=indicator(s0=-1,s1=+1)|N(F)_times_8^4_times_8^2=%d|lowest_N(delta_C)_scaled=%d|C_with_N(delta_C)<0=%d_of_%d|json=0" % (num_one_weight, low, negatives, len(slices) ** 2))
print("IND_ZERO_DONE|json=0")
