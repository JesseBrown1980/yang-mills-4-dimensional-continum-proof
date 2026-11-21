"""Full finite 4D SU(2) Wilson cylinder: exact Haar/Taylor C0,C2,C4 bounds.

Original 2x2x2x10 periodic Wilson plaquette action, all 480 coupled
plaquettes. Rational bounds on finite-periodic Euclidean connected Wilson
correlators; does not evaluate the infinite-time vacuum spectral moments.

The exact SU(2) Haar facts are the source identities in YM4-02a.
Only integer-rational arithmetic and exact Z2 link-incidence enumeration.
"""
from itertools import product
from ym4_su2_wilson_local_transfer import R, require

L = 2
T = 10
DIMS = (L, L, L, T)
SITE_COUNT = 80
LINK_COUNT = 320
PLAQUETTE_COUNT = 480


def sites():
    return tuple(product(*(range(size) for size in DIMS)))


def translate(site, mu, delta=1):
    require(type(mu) is int and 0 <= mu < 4, "invalid_direction")
    out = list(site)
    out[mu] = (out[mu] + delta) % DIMS[mu]
    return tuple(out)


def positive_links():
    return tuple((site, mu) for site in sites() for mu in range(4))


def plaquette_word(site, mu, nu):
    """Ordered plaquette word: +mu,+nu,-mu,-nu, as in PROBLEM.md."""
    require(type(mu) is int and type(nu) is int
            and 0 <= mu < nu < 4, "invalid_plaquette_plane")
    return ((site, mu, 1),
            (translate(site, mu), nu, 1),
            (translate(site, nu), mu, -1),
            (site, nu, -1))


def plaquettes():
    return tuple((site, mu, nu, plaquette_word(site, mu, nu))
                 for site in sites()
                 for mu in range(4) for nu in range(mu + 1, 4))


def verify_closed_word(word):
    require(len(word) == 4, "plaquette_word_length")
    start = word[0][0] if word[0][2] == 1 else translate(word[0][0], word[0][1])
    here = start
    for base, mu, sign in word:
        require(sign in (-1, 1), "invalid_edge_orientation")
        edge_start = base if sign == 1 else translate(base, mu)
        edge_end = translate(base, mu) if sign == 1 else base
        require(here == edge_start, "plaquette_path_discontinuous")
        here = edge_end
    require(here == start, "plaquette_path_not_closed")
    require(len({(base, mu) for base, mu, sign in word}) == 4,
            "non_distinct_plaquette_links")
    return True


def geometry():
    links = positive_links()
    pls = plaquettes()
    require(len(sites()) == SITE_COUNT and len(links) == LINK_COUNT,
            "source_site_link_count_mismatch")
    require(len(pls) == PLAQUETTE_COUNT, "source_plaquette_count_mismatch")
    link_id = {link: i for i, link in enumerate(links)}
    incidences = {link: 0 for link in links}
    masks = []
    spatial = 0
    timelike = 0
    for site, mu, nu, word in pls:
        verify_closed_word(word)
        mask = 0
        for base, axis, sign in word:
            key = (base, axis)
            incidences[key] += 1
            mask |= 1 << link_id[key]
        require(mask.bit_count() == 4, "plaquette_support_wrong")
        masks.append(mask)
        if nu == 3:
            timelike += 1
        else:
            spatial += 1
    require(spatial == 240 and timelike == 240,
            "missing_spatial_or_timelike_plaquettes")
    require(all(v == 6 for v in incidences.values()),
            "link_six_staple_incidence_failure")
    require(len(set(masks)) == PLAQUETTE_COUNT,
            "duplicate_plaquette_support")
    return pls, tuple(masks)


def parity_coefficient_counts(masks, target):
    """Count ordered (p,q) satisfying support(p) XOR support(q)=target.

    Nonzero target is a necessary condition for a nonvanishing Haar
    monomial; for the specific accepted cases the remaining factors
    are evaluated by exclusive Haar links and Catalan moments.
    """
    lookup = {mask: i for i, mask in enumerate(masks)}
    require(len(lookup) == len(masks), "duplicate_plaquette_support")
    return sum(int((target ^ p) in lookup) for p in masks)


def source_haar_data():
    pls, masks = geometry()
    lookup = {key: i for i, key in enumerate((site, mu, nu)
                                              for site, mu, nu, word in pls)}
    # One spatial Wilson plaquette based at (0,0,0,t), in the (0,1) plane.
    base = (0, 0, 0, 0)
    w0 = masks[lookup[(base, 0, 1)]]
    w2 = masks[lookup[((0, 0, 0, 2), 0, 1)]]
    w4 = masks[lookup[((0, 0, 0, 4), 0, 1)]]
    require((w0 & w2) == 0 and (w0 & w4) == 0
            and (w2 & w4) == 0,
            "time_separated_Wilson_support_not_disjoint")
    require(sum(int(p == w0) for p in masks) == 1,
            "original_Wilson_plaquette_not_unique")
    require(parity_coefficient_counts(masks, 0) == PLAQUETTE_COUNT,
            "Haar_A2_parity_unexpected")
    require(parity_coefficient_counts(masks, w0) == 0,
            "Haar_WA2_did_not_vanish")
    for wt in (w2, w4):
        require(sum(int(p == (w0 ^ wt)) for p in masks) == 0,
                "Haar_W0WtA_did_not_vanish")
        require(parity_coefficient_counts(masks, w0 ^ wt) == 2,
                "Haar_W0WtA2_pair_count_wrong")
        require(sum(int(p == wt) for p in masks) == 1,
                "nonunique_shifted_Wilson_loop")
    # E0[A_p^2]=1/4; for distinct p,q an exclusive edge kills E0[A_p A_q].
    # E0[W^4]=1/8 and E0[W^2 A_p^2]=1/16 for p!=W.
    # E0[W0 Wt A_p A_q]=1/16 for (p,q)=(W0,Wt) or (Wt,W0).
    return {"sites": SITE_COUNT, "links": LINK_COUNT,
            "plaquettes": PLAQUETTE_COUNT, "spatial": 240,
            "timelike": 240, "mean_A": R(0), "A2": R(120),
            "mean_W": R(0), "W2": R(1, 4),
            "WA": R(1, 4), "W2A": R(0),
            "WA2": R(0), "W2A2": R(481, 16),
            "WWt": R(0), "WWtA": R(0), "WWtA2": R(1, 8),
            "parity_t2": 2, "parity_t4": 2}


def floor_scaled(x, scale):
    x = R.of(x)
    require(type(scale) is int and scale > 0, "invalid_fixed_grid")
    return x.n * scale // x.d


def ceil_scaled(x, scale):
    x = R.of(x)
    require(type(scale) is int and scale > 0, "invalid_fixed_grid")
    return -((-x.n * scale) // x.d)


def bounded_connected(beta):
    """Rigorous, true finite-T original Wilson C0,C2,C4 enclosures.

    Set A=sum_p halfTr(U_p), |A|<=480. Cancel exp(-beta*Np) from
    the original Boltzmann weight; normalize against product Haar.
    R3<=x^3/[6(1-x)], x=480*beta<1.

    First three Haar coefficients are computed analytically from exact
    link incidences. The bound uses full interaction A, not decoupled
    timelike or magnetic factors.
    """
    beta = R.of(beta)
    require(beta > R(0) and beta * PLAQUETTE_COUNT < R(1),
            "beta_outside_certified_Taylor_window")
    h = source_haar_data()
    require(h["A2"] == R(120) and h["W2A2"] == R(481, 16)
            and h["WWtA2"] == R(1, 8),
            "Haar_source_coefficient_failed")
    b2 = beta.power(2)
    x = beta * PLAQUETTE_COUNT
    rem = x.power(3).div(6 * (R(1) - x))
    z_nom = R(1) + b2 * R(60)
    z_lo, z_hi = z_nom - rem, z_nom + rem
    require(z_lo > R(0), "partition_lower_bound_nonpositive")
    one_nom = beta.div(4)
    square_nom = R(1, 4) + b2 * R(481, 32)
    pair_nom = b2.div(16)
    mu_abs = (one_nom + rem).div(z_lo)
    c0_lo = (square_nom - rem).div(z_hi) - mu_abs.power(2)
    c0_hi = (square_nom + rem).div(z_lo)
    # C_t=(N_W0Wt*Z - N_W^2)/Z^2.
    # Exact cancellation at order beta^2: pair_nom=one_nom^2.
    require(pair_nom == one_nom.power(2), "connected_beta2_no_cancellation")
    absolute_numer = (pair_nom * (z_nom - R(1))
                      + rem * z_hi + pair_nom * rem
                      + 2 * one_nom * rem + rem.power(2))
    bound_t = absolute_numer.div(z_lo.power(2))
    require(c0_lo > R(0) and c0_lo < c0_hi and bound_t > R(0),
            "Wilson_bounds_invalid")
    return {"beta": beta, "x": x, "remainder": rem,
            "Zlo": z_lo, "Zhi": z_hi, "C0lo": c0_lo,
            "C0hi": c0_hi, "Ct_abs": bound_t}


def predict_acceptance(beta, c0_deviation, time_bound):
    a = bounded_connected(beta)
    require(a["C0lo"] > R(1, 4) - c0_deviation
            and a["C0hi"] < R(1, 4) + c0_deviation,
            "frozen_C0_enclosure_failure")
    require(a["Ct_abs"] < time_bound,
            "frozen_Ct_enclosure_failure")
    scale = 10 ** 12
    return (
        "YM4_4D_WILSON_CYLINDER|L=2,2,2|T=10|beta=" + str(beta)
        + "|plaquettes=480|C0_lower_1e12=" + str(floor_scaled(a["C0lo"], scale))
        + "|C0_upper_1e12=" + str(ceil_scaled(a["C0hi"], scale))
        + "|abs_C2_upper_1e12=" + str(ceil_scaled(a["Ct_abs"], scale))
        + "|abs_C4_upper_1e12=" + str(ceil_scaled(a["Ct_abs"], scale))
        + "|taylor_order=2|remainder3=EXACT_RATIONAL"
        + "|full_spatial_magnetic_action=INCLUDED"
        + "|all_temporal_plaquettes=INCLUDED"
        + "|thermal_periodic_correlators=BOUNDED"
        + "|vacuum_infinite_time=OPEN|json=0"
    )


def receipt():
    h = source_haar_data()
    rows = [
        "YM4_4D_WILSON_SOURCE|continuous_SU2=YES|sites=80|links=320"
        "|plaquettes=480|spatial=240|temporal=240"
        "|each_link_six_staples=PASS|json=0",
        "YM4_4D_WILSON_HAAR|E_A=0|E_A2=120|E_W=0|E_W2=1/4"
        "|E_WA=1/4|E_W2A=0|E_WA2=0"
        "|E_W2A2=481/16|E_W0WtA2=1/8"
        "|t2_pair_count=2|t4_pair_count=2|json=0",
        predict_acceptance(R(1, 10000), R(1, 10000), R(1, 50000)),
        predict_acceptance(R(1, 100000), R(1, 10000000),
                           R(1, 50000000)),
        "YM4_4D_WILSON_VERDICT|finite_periodic_Wilson_C0_C2_C4"
        "=EXACT_RATIONAL_INTERVALS|connected_order_beta2=CANCELS"
        "|original_4D_Gauss_invariant_source=YES"
        "|infinite_time_vacuum_moments=OPEN"
        "|full_transfer_spectrum=OPEN|continuum_gap=OPEN|json=0",
    ]
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    print(receipt(), end="")
