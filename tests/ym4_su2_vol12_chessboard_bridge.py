"""VOL12 chessboard bridge: exact original geometry and imported-theorem arithmetic.

IMPORTANT: This checks only the finite incidence and exact rate arithmetic,
NOT the imported Lean reflection-positivity theorem FoldMix.rarity_orient.
"""
from itertools import product


def require(value, label):
    if not value:
        raise ValueError(label)


def ipow(base, n):
    require(isinstance(base, int) and isinstance(n, int) and n >= 0,
            "integer_positive_exponent")
    out = 1
    for unused in range(n):
        out *= base
    return out


def shifted(x, axis, L):
    y = list(x)
    y[axis] = (y[axis] + 1) % L
    return tuple(y)


def original_link_plaquette_graph(L):
    vertices = list(product(range(L), repeat=4))
    links = [(x, d) for x in vertices for d in range(4)]
    incident = {e: [] for e in links}
    adjacent = {e: set() for e in links}
    plaquettes = []
    orientations = []
    for x in vertices:
        for mu in range(4):
            for nu in range(mu+1, 4):
                p = ((x, mu), (shifted(x, mu, L), nu),
                     (shifted(x, nu, L), mu), (x, nu))
                require(len(set(p)) == 4, "four_original_links_per_plaquette")
                idx = len(plaquettes)
                plaquettes.append(p)
                orientations.append((mu, nu))
                for e in p:
                    incident[e].append(idx)
                    for f in p:
                        if e != f:
                            adjacent[e].add(f)
    require(len(links) == 4*ipow(L, 4) and
            len(plaquettes) == 6*ipow(L, 4), "original_4D_counts")
    require(all(len(incident[e]) == 6 and len(adjacent[e]) == 18
                for e in links), "six_incident_and_eighteen_adjacent")
    return links, incident, adjacent, orientations


def validate_independent_choices(L, r):
    links, incident, adjacent, orientations = original_link_plaquette_graph(L)
    packet = []
    for e in links:
        if all(e not in adjacent[f] for f in packet):
            packet.append(e)
            if len(packet) == r:
                break
    require(len(packet) == r, "independent_packet_size")
    require(all(set(incident[e]).isdisjoint(incident[f])
                for j, e in enumerate(packet) for f in packet[j+1:]),
            "plaquette_disjoint_stars")
    # Each e has six incident original plaquettes; every marked choice set
    # has r distinct plaquettes and can be partitioned among six orientations.
    choose_first = [incident[e][0] for e in packet]
    choose_last = [incident[e][-1] for e in packet]
    for choices in (choose_first, choose_last):
        require(len(set(choices)) == r, "marked_defects_are_distinct")
        histogram = {o: 0 for o in sorted(set(orientations))}
        for idx in choices:
            histogram[orientations[idx]] += 1
        require(len(histogram) == 6 and sum(histogram.values()) == r,
                "six_original_plane_orientations")
        require(6*max(histogram.values()) >= r, "orientation_pigeonhole")
    return len(packet)


def integer_rate_at(k):
    beta = ipow(9,k)
    cap_denom = 1280
    A = ipow(24*ipow(cap_denom,3),4)
    N = (beta*1597)//204800
    margin = N - A.bit_length()
    # The imported theorem gives q <= A exp(-beta*1597/102400).
    # e^2>2 implies q < A / 2^N.
    return beta, A, N, margin


def main():
    # Even side L>=4 is an essential EXTERNAL premise, unlike the
    # original incidence math which also works for L3.
    require(validate_independent_choices(3,4) == 4,
            "odd_geometry_exists_but_chessboard_theorem_unavailable")
    for L in (4,6):
        for count in (2,4,20):
            require(validate_independent_choices(L,count) == count,
                    "even_original_graph_packet")
    beta,A,N,margin=integer_rate_at(6)
    require(beta == 531441 and A.bit_length() == 143 and
            N == 4144 and margin == 4001,
            "integer_Haar_cap_exponential_envelope")
    # If q<2^-4001, then rho=6 q^(1/6)<2^-663.
    # Since 18<2^5, 2^-663 < 18^-57.
    require(4001 >= 6*666 and 6<8 and 663>5*57,
            "rho_less_2_minus663_less_18_minus57")
    # An exact stronger direct inequality, avoiding roots and reals:
    # 6^6 * A * 18^342 < 2^N.
    threshold = ipow(6,6)*A*ipow(18,342)
    require(threshold < ipow(2,N),
            "rho_strictly_below_vol10_threshold")
    require(threshold.bit_length() == 1584 and N-threshold.bit_length() == 2560,
            "independently_visible_integer_margin")
    # k5 is not sufficient *with these conservative bounds*.
    beta5,A5,N5,margin5=integer_rate_at(5)
    require(beta5 == 59049 and margin5 > 0 and
            not (ipow(6,6)*A5*ipow(18,342) < ipow(2,N5)),
            "do_not_promote_k5")
    # No odd-side, twisted, conditioned boundary or continuum promotion.
    return (
        "YM4_VOL12_CHESSBOARD_IMPORT|source=computoergosum_22-01_FoldMix_rarity_orient|status=EXTERNAL_SOURCE_AUDIT_OPEN|json=0\n"
        "YM4_VOL12_CHESSBOARD_SCOPE|original_continuous_SU2_Wilson=REQUIRED|periodic_even_L_ge4=REQUIRED|same_orientation_external_rate=REQUIRED|odd_L=OPEN|json=0\n"
        "YM4_VOL12_GEOMETRY|independent_stars_share_no_plaquette=PASS|incident_plaquettes_per_star=6|plane_orientations=6|L3=NEGATIVE_SCOPE|L4_L6=PASS|json=0\n"
        "YM4_VOL12_JOINT|if_external_chessboard=ACCEPTED|unconditional_joint_bad_star_le=rho_power_r|rho=6_times_q_power_one_sixth|json=0\n"
        "YM4_VOL12_RATE|epsilon=1/16|y=1/64|a=1/1280|beta=9power6|beta_integer=531441|cap_A_bits=143|N=4144|rho_lt=2power_minus663|VOL10_rho_le_18power_minus57=CONDITIONAL_PASS|json=0\n"
        "YM4_VOL12_ISLAND|original_even_periodic_SU2_root_cluster_tail_le=18power_minus_m_minus2|status=CONDITIONAL_ON_EXTERNAL_ORIENT_CHESSBOARD|json=0\n"
        "YM4_VOL12_REDS|odd_L=REJECTED|arbitrary_exterior=REJECTED|blocked_scale=REJECTED|physical_cube=OPEN|11_continuum_gates=OPEN|json=0\n"
    )


if __name__ == '__main__':
    print(main(),end='')
