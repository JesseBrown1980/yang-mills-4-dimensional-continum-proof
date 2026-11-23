"""YM4 VOL12: original 4D SU2 periodic box bad-star crossing geometry.

Exact integer realization of the graph and conditional consequence of
published even-torus chessboard theorem and VOL10 root island estimate.
This script does NOT compile the external Lean proof or prove a
boundary-conditioned physical-size Wilson Dobrushin-Shlosman cube.
"""
from itertools import product


def require(ok, name):
    if not ok:
        raise ValueError(name)


def ipow(base, n):
    require(isinstance(base, int) and isinstance(n, int) and n >= 0,
            "nonnegative_integer_power")
    out = 1
    for unused in range(n):
        out *= base
    return out


def next_site(x, mu, L):
    a = list(x)
    a[mu] = (a[mu]+1) % L
    return tuple(a)


def link_graph(L):
    require(L in (4, 6), "tested_even_original_periodic_tori")
    vertices = list(product(range(L), repeat=4))
    links = [(x, mu) for x in vertices for mu in range(4)]
    neighbors = {e: set() for e in links}
    plaquettes = 0
    for x in vertices:
        for mu in range(4):
            for nu in range(mu+1, 4):
                p = ((x, mu), (next_site(x, mu, L), nu),
                     (next_site(x, nu, L), mu), (x, nu))
                require(len(set(p)) == 4, "four_distinct_links")
                plaquettes += 1
                for e in p:
                    for f in p:
                        if f != e:
                            neighbors[e].add(f)
    require(len(links) == 4*ipow(L, 4) and
            plaquettes == 6*ipow(L, 4),
            "original_SU2_4d_geometry")
    require(all(len(s) == 18 for s in neighbors.values()),
            "original_plaquette_sharing_degree18")
    for e, fs in neighbors.items():
        for f in fs:
            for axis in range(4):
                delta = (e[0][axis]-f[0][axis]) % L
                require(delta in (0, 1, L-1),
                        "neighbors_move_one_site_per_axis")
    return neighbors


def box_crossing_min_steps(L, b):
    require(L >= 2*b and 2 <= b, "avoid_periodic_wraparound")
    neighbors = link_graph(L)
    # Select one direction and sample one shortest route using
    # breadth-first expansion inside the based-link box Q_b.
    subset = {e for e in neighbors if all(x < b for x in e[0])}
    sources = [e for e in subset if e[0][0] == 0]
    targets = {e for e in subset if e[0][0] == b-1}
    visited = set(sources)
    frontier = set(sources)
    distance = 0
    while not (frontier & targets):
        more = set()
        for e in frontier:
            more.update(neighbors[e] & subset)
        frontier = more-visited
        visited.update(frontier)
        distance += 1
        require(frontier and distance <= 2*b,
                "connected_original_link_box")
    require(distance >= b-1,
            "crossing_requires_b_bad_vertices")
    return distance, len(sources)


def strict_power_of_two_exponent(b):
    require(isinstance(b, int) and b >= 2, "cube_side_b_ge2")
    numerator = 16*ipow(b,3)
    denominator = ipow(18,b+2)
    require(numerator < denominator, "probability_crossing_nontrivial")
    t = 0
    while 2*numerator*ipow(2,t) < denominator:
        t += 1
    require(numerator*ipow(2,t) < denominator,
            "strict_power_two_upper")
    return t


def certify():
    a = box_crossing_min_steps(4,2)
    c = box_crossing_min_steps(6,3)
    require(a == (1, 4*ipow(2,3)) and
            c == (2, 4*ipow(3,3)),
            "original_geometry_exact_face_roots")
    table = [(b,strict_power_of_two_exponent(b))
             for b in (2,3,9,27,81)]
    require(table == [(2,9),(3,12),(9,32),(27,102),(81,323)],
            "exact_integer_crossing_table")
    # For b>=2, (b+1)^3 / b^3 <= 27/8 <18.
    require(27 < 8*18, "crossing_bound_monotone")
    # Red gates: arbitrary exterior / twisted / odd-L / block measure
    # are absent from the imported theorem's hypotheses.
    return (
        "YM4_VOL12_CROSSING|premise=FOLDMIX_EVEN_TORUS_SOURCE_DEPENDENT|original_continuous_SU2=YES|json=0\n"
        "YM4_VOL12_CROSSING_GRAPH|L4_and_L6_degree18=PASS|neighbor_coordinate_step_le1=PASS|L_ge_2b=REQUIRED|json=0\n"
        "YM4_VOL12_CROSSING_THEOREM|all_four_axis_box_crossings_le=16_b_cubed_over_18_power_bplus2|root_cluster_tail=IMPORTED_VIA_VOL10|json=0\n"
        "YM4_VOL12_CROSSING_INTEGER|b2_lt_2power_minus9|b3_lt_2power_minus12|b9_lt_2power_minus32|b27_lt_2power_minus102|b81_lt_2power_minus323|json=0\n"
        "YM4_VOL12_CROSSING_SCOPE|physical_width_bad_star_crossing=CONDITIONAL_BOUND|arbitrary_boundary_cube_contraction=OPEN|all_sector_transfer=OPEN|11_continuum_gates=OPEN|json=0\n"
    )


if __name__ == '__main__':
    print(certify(),end='')
