"""YM4 VOL12: closed-cube chessboard route to an unconditional bad-star cluster bound.

Integer-only checker for the finite, combinatorial and arithmetic parts of
NOTE-YM4-VOL12-CHESSBOARD-BAD-STAR-CLUSTERS-20261124.md:

  rows 01-03  closed unit blocks, the 24 face orbits and their multiplicity 4,
              link and plaquette incidence, link-graph degree 18 (L = 4, 6)
  row 04      reflection covariance: theta_{mu,k} o tau_s = tau_{theta s}
  row 05      every unit block lies in exactly one closed half
  row 06      odd side: block transport by parity is inconsistent (rejected)
  rows 07-08  rooted connected link sets N_1..N_4 and the m = 3 falsifier
              of an 18^(m-1) count
  row 09      the adjacent-label inequality used in the chessboard proof
  rows 10-14  integer certificates for rho_star at the beta = 9^k fixtures

The analytic steps (reflection positivity, the chessboard theorem, the
partition-function bound) are proved in the note and are not re-proved here.
"""
from itertools import product


def require(ok, name):
    if not ok:
        raise ValueError(name)


def power(base, exponent):
    require(isinstance(base, int) and isinstance(exponent, int)
            and 0 <= exponent <= 5000, "bounded_nonfloating_power")
    p = 1
    for unused in range(exponent):
        p *= base
    return p


def emit(*fields):
    print("|".join(("YM4_VOL12",) + fields + ("json=0",)))


# ---------------------------------------------------------------- geometry

def sites(L):
    return list(product(range(L), repeat=4))


def step(x, mu, L):
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)


def plaquette_sites(x, mu, nu, L):
    return frozenset((x, step(x, mu, L), step(x, nu, L), step(step(x, mu, L), nu, L)))


def plaquette_links(x, mu, nu, L):
    return frozenset(((x, mu), (step(x, mu, L), nu), (step(x, nu, L), mu), (x, nu)))


def all_plaquettes(L):
    out = {}
    for x in sites(L):
        for mu in range(4):
            for nu in range(mu + 1, 4):
                out[(x, mu, nu)] = (plaquette_sites(x, mu, nu, L), plaquette_links(x, mu, nu, L))
    return out


CORNERS = list(product((0, 1), repeat=4))


def tau(t, y, L):
    """Transport corner y of the base block C_0 to block C_t by reflections."""
    out = []
    for mu in range(4):
        if t[mu] % 2 == 0:
            out.append((t[mu] + y[mu]) % L)
        else:
            out.append((t[mu] + 1 - y[mu]) % L)
    return tuple(out)


def base_faces():
    faces = []
    for mu in range(4):
        for nu in range(mu + 1, 4):
            others = [r for r in range(4) if r not in (mu, nu)]
            for a in product((0, 1), repeat=2):
                corners = []
                for y in CORNERS:
                    if y[others[0]] == a[0] and y[others[1]] == a[1]:
                        corners.append(y)
                faces.append(((mu, nu, a), corners))
    return faces


def check_orbits(L):
    plaqs = all_plaquettes(L)
    by_sites = {}
    for key, (ps, unused) in plaqs.items():
        require(ps not in by_sites, "plaquette_sites_determine_plaquette")
        by_sites[ps] = key
    faces = base_faces()
    require(len(faces) == 24, "face_types_24")
    covered = {}
    blocks = sites(L)
    for (fid, corners) in faces:
        hits = {}
        for t in blocks:
            image = frozenset(tau(t, y, L) for y in corners)
            require(image in by_sites, "image_is_a_plaquette")
            key = by_sites[image]
            hits[key] = hits.get(key, 0) + 1
        require(all(v == 4 for v in hits.values()), "multiplicity_4")
        require(len(hits) * 4 == power(L, 4), "orbit_size_L4_over_4")
        for key in hits:
            require(key not in covered, "orbits_disjoint")
            covered[key] = fid
    require(len(covered) == len(plaqs) == 6 * power(L, 4), "orbits_cover_all_plaquettes")
    # Independent recount: plaquettes whose four sites lie in a block's 16 sites,
    # found from the block's own site set rather than from the face transport.
    cube_count = {}
    for t in blocks:
        block = frozenset(tau(t, y, L) for y in CORNERS)
        require(len(block) == 16, "block_has_16_sites")
        inside = set()
        for x in block:
            for mu in range(4):
                for nu in range(mu + 1, 4):
                    ps = plaquette_sites(x, mu, nu, L)
                    if ps <= block:
                        inside.add(by_sites[ps])
        require(len(inside) == 24, "block_contains_24_plaquettes")
        for key in inside:
            cube_count[key] = cube_count.get(key, 0) + 1
    require(len(cube_count) == len(plaqs) and set(cube_count.values()) == {4},
            "closed_cubes_per_plaquette_4")
    per_link = {}
    for key, (unused, pl) in plaqs.items():
        require(len(pl) == 4, "links_per_plaquette_4")
        for e in pl:
            per_link[e] = per_link.get(e, 0) + 1
    require(len(per_link) == 4 * power(L, 4) and set(per_link.values()) == {6}, "plaquettes_per_link_6")
    nbr = {}
    for key, (unused, pl) in plaqs.items():
        for e in pl:
            nbr.setdefault(e, set()).update(pl - {e})
    require({len(v) for v in nbr.values()} == {18}, "link_graph_degree_18")
    emit("row=0" + ("1" if L == 4 else "2"), "L=" + str(L), "blocks=" + str(len(blocks)),
         "links=" + str(len(per_link)), "plaquettes=" + str(len(plaqs)), "face_types=24",
         "orbit_size_each=" + str(power(L, 4) // 4), "orbits_disjoint_and_cover=YES")
    return plaqs, nbr


def check_reflections(L):
    blocks = sites(L)
    half = L // 2
    for mu in range(4):
        for k in range(L):
            for s in blocks:
                sp = list(s)
                sp[mu] = (2 * k - s[mu] - 1) % L
                sp = tuple(sp)
                for y in CORNERS:
                    x = tau(s, y, L)
                    rx = list(x)
                    rx[mu] = (2 * k - x[mu]) % L
                    require(tuple(rx) == tau(sp, y, L), "reflection_covariance")
                plus = all(((tau(s, y, L)[mu] - k) % L) <= half for y in CORNERS)
                minus = all(((k - tau(s, y, L)[mu]) % L) <= half for y in CORNERS)
                require(plus != minus, "block_in_exactly_one_closed_half")
    return True


def check_odd_side(L):
    """With L odd, t and t + L name the same block but have opposite parity."""
    conflicts = 0
    for t in sites(L):
        t2 = tuple(c + L if i == 0 else c for i, c in enumerate(t))
        for y in CORNERS:
            if tau(t, y, L) != tau(t2, y, L):
                conflicts += 1
    return conflicts


# ---------------------------------------------------------- rooted animals

def rooted_counts(nbr, root, mmax):
    level = {frozenset([root])}
    counts = [len(level)]
    for unused in range(mmax - 1):
        nxt = set()
        for s in level:
            frontier = set()
            for e in s:
                frontier |= nbr[e]
            for c in frontier - s:
                nxt.add(s | {c})
        level = nxt
        counts.append(len(level))
    return counts


# ------------------------------------------------- chessboard proof step

def lcg(state):
    return (state * 6364136223846793005 + 1442695040888963407) % (1 << 64)


def adjacency_pairs(L):
    pairs = []
    for s in sites(L):
        for nu in range(4):
            pairs.append((s, step(s, nu, L), nu))
    return pairs


def equal_pairs(labels, pairs):
    return sum(1 for (a, b, unused) in pairs if labels[a] == labels[b])


def check_label_step(L, samples, nlabels):
    pairs = adjacency_pairs(L)
    blocks = sites(L)
    half = L // 2
    state = 20261124
    tested = 0
    for unused in range(samples):
        labels = {}
        for s in blocks:
            state = lcg(state)
            labels[s] = (state >> 33) % nlabels
        for mu in range(4):
            for k in range(L):
                inplus = {s: ((s[mu] - k) % L) < half for s in blocks}

                def mirror(s):
                    r = list(s)
                    r[mu] = (2 * k - s[mu] - 1) % L
                    return tuple(r)
                a1 = {s: (labels[s] if inplus[s] else labels[mirror(s)]) for s in blocks}
                a2 = {s: (labels[mirror(s)] if inplus[s] else labels[s]) for s in blocks}
                e_plus = sum(1 for (a, b, unused2) in pairs
                             if inplus[a] and inplus[b] and labels[a] == labels[b])
                e_minus = sum(1 for (a, b, unused2) in pairs
                              if not inplus[a] and not inplus[b] and labels[a] == labels[b])
                straddle = [(a, b) for (a, b, unused2) in pairs if inplus[a] != inplus[b]]
                require(len(straddle) == 2 * power(L, 3), "straddling_pairs_2L3")
                require(equal_pairs(a1, pairs) == 2 * e_plus + 2 * power(L, 3), "E_a1_identity")
                require(equal_pairs(a2, pairs) == 2 * e_minus + 2 * power(L, 3), "E_a2_identity")
                if any(labels[a] != labels[b] for (a, b) in straddle):
                    e = equal_pairs(labels, pairs)
                    require(equal_pairs(a1, pairs) + equal_pairs(a2, pairs) >= 2 * e + 2,
                            "reflection_increases_agreement")
                    tested += 1
    return tested


# ------------------------------------------------------ integer fixtures
# rho_star = 6 * 1536 * e^(3/4) * beta^(3/2) * e^(-beta*eps/64), beta = 9^k.
# Upper certificate: e^(3/4) < 3, beta^(3/2) = 3^(3k), e^(-x) <= 2^(-floor x).
# Lower certificate: e^(3/4) >= 1, e^(-x) >= 3^(-ceil x) since e < 3.

def floor_ceil_x(k, en, ed, scale):
    num = (power(9, k)) * en
    den = scale * ed
    fl = num // den
    ce = fl if fl * den == num else fl + 1
    return fl, ce


def star_upper_le(k, en, ed, j):
    """True if rho_star <= 18^(-j) is certified."""
    fl, unused = floor_ceil_x(k, en, ed, 64)
    return 6 * 1536 * power(3, (3 * k + 1)) * power(18, j) <= power(2, fl)


def star_lower_gt(k, en, ed, j):
    """True if rho_star > 18^(-j) is certified."""
    unused, ce = floor_ceil_x(k, en, ed, 64)
    return 6 * 1536 * power(3, (3 * k)) * power(18, j) > power(3, ce)


def star_log2_ceiling(k, en, ed):
    fl, unused = floor_ceil_x(k, en, ed, 64)
    return (6 * 1536 * power(3, (3 * k + 1))).bit_length() - fl


def plaquette_log2_ceiling(k, en, ed):
    fl, unused = floor_ceil_x(k, en, ed, 16)
    return (power(1536, 4) * 27 * power(3, (12 * k))).bit_length() - fl


def main():
    nbr = None
    for L in (4, 6):
        unused, graph = check_orbits(L)
        check_reflections(L)
        if L == 6:
            nbr = graph
    emit("row=03", "L=4_and_6", "closed_unit_cubes_per_plaquette=4", "plaquettes_per_link=6",
         "links_per_plaquette=4", "link_graph_degree=18")
    emit("row=04", "L=4_and_6", "reflection_covariance=PASS")
    emit("row=05", "L=4_and_6", "every_unit_block_in_exactly_one_closed_half=YES")

    conflicts = check_odd_side(5)
    require(conflicts > 0, "odd_side_must_conflict")
    require(check_odd_side(4) == 0 and check_odd_side(6) == 0, "even_side_consistent")
    emit("row=06", "L=5", "transport_conflicts=" + str(conflicts), "odd_side=REJECTED")

    root = ((0, 0, 0, 0), 0)
    counts = rooted_counts(nbr, root, 4)
    require(counts == [1, 18, 375, 8364], "rooted_counts_match_prediction")
    for m, n in enumerate(counts, 1):
        require(n <= power(18, (2 * (m - 1))), "count_le_18_pow_2m_minus_2")
        require(n <= power(72, (m - 1)), "count_le_72_pow_m_minus_1")
    emit("row=07", "L=6", "N1=1", "N2=18", "N3=375", "N4=8364",
         "bound_18_pow_2m_minus_2=HOLDS", "bound_72_pow_m_minus_1=HOLDS")
    require(counts[2] > power(18, 2), "too_strong_count_must_fail")
    emit("row=08", "too_strong_count_18_pow_m_minus_1", "falsified_at_m=3", "375_gt_324=YES")

    tested = check_label_step(4, 12, 3)
    require(tested > 0, "label_step_exercised")
    emit("row=09", "L=4", "configurations_with_a_differing_straddle=" + str(tested),
         "E(a1)+E(a2)_ge_2E(a)+2=PASS")

    require(not star_upper_le(4, 1, 16, 0) and star_lower_gt(4, 1, 16, 0), "row10")
    emit("row=10", "beta=9^4", "eps=1/16", "rho_star_gt_1=CERTIFIED", "verdict=NO_INFORMATION")
    require(star_upper_le(5, 1, 16, 3), "row11a")
    require(star_lower_gt(5, 1, 16, 57), "row11b")
    emit("row=11", "beta=9^5", "eps=1/16", "rho_star_le_18^-3=CERTIFIED",
         "rho_star_gt_18^-57=CERTIFIED", "VOL10_criterion=FAILS", "VOL12_criterion=PASSES",
         "rho_star_lt_2^" + str(star_log2_ceiling(5, 1, 16)))
    require(6 * 1536 * power(3, 19) * power(18, 57) < power(2, 518), "row12_witness")
    require(star_upper_le(6, 1, 16, 3) and star_upper_le(6, 1, 16, 57), "row12")
    emit("row=12", "beta=9^6", "eps=1/16", "rho_star_le_18^-3=CERTIFIED",
         "rho_star_le_18^-57=CERTIFIED", "integer_witness=6*1536*3^19*18^57_lt_2^518",
         "rho_star_lt_2^" + str(star_log2_ceiling(6, 1, 16)),
         "rho_D_lt_2^" + str(plaquette_log2_ceiling(6, 1, 16)))
    require(star_upper_le(5, 1, 2, 57), "row13")
    emit("row=13", "beta=9^5", "eps=1/2", "rho_star_le_18^-57=CERTIFIED",
         "rho_star_lt_2^" + str(star_log2_ceiling(5, 1, 2)))
    require(6 * 1536 > 1, "row14")
    emit("row=14", "eps=0", "rho_star_ge_6*1536", "verdict=NO_INFORMATION")
    print("YM4_VOL12_VERDICT|rows=14|geometry=PASS|chessboard_label_step=PASS|fixtures=PASS"
          "|theorem_status=PROOF_WRITTEN_PENDING_HUMAN_REVIEW|odd_L=OPEN|multiscale=OPEN|json=0")


if __name__ == "__main__":
    main()
