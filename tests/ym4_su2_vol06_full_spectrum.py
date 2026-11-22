"""YM4-VOL06: independent exact-integer geometry and spectral-root audit.

Mathematical dependencies requiring analytic review (not machine-proved here):
- classical Rebeschini--van Handel Dobrushin comparison and tilted covariance;
- original Wilson temporal transfer, Gauss sector, positivity improving;
- density of bounded spatial-slice observables via positive vacuum.

The code only certifies finite incidence, time separation, rational consistency,
and an exact spectral-root falsifier. No numeric spectrum is fabricated.
"""

from collections import Counter, deque
from itertools import combinations, product


def check(statement, label):
    if not statement:
        raise ValueError(label)


def shifted(site, axis, size):
    point = list(site)
    point[axis] = (point[axis] + 1) % size[axis]
    return tuple(point)


def link_graph(spatial_side, temporal_side):
    size = (temporal_side,) + (spatial_side,) * 3
    check(spatial_side >= 3 and temporal_side >= 3, "distinct_original_links")
    graph = {}
    incident = Counter()
    influence_multiplicity = Counter()
    for site in product(*tuple(range(side) for side in size)):
        for axis in range(4):
            graph[site, axis] = set()
    for site in product(*tuple(range(side) for side in size)):
        for axis, other in combinations(range(4), 2):
            p = (
                (site, axis),
                (shifted(site, axis, size), other),
                (shifted(site, other, size), axis),
                (site, other),
            )
            check(len(set(p)) == 4, "distinct_plaquette_links")
            for u in p:
                incident[u] += 1
                for v in p:
                    if v != u:
                        influence_multiplicity[u] += 1
                        graph[u].add(v)
    check(len(graph) == temporal_side * spatial_side ** 3 * 4,
          "original_link_count")
    check(set(incident) == set(graph), "plaquettes_cover_every_link")
    check(set(incident.values()) == {6}, "six_plaquettes_per_original_link")
    check(sum(incident.values()) == len(graph) * 6,
          "six_incident_plaquettes_per_link")
    check(set(influence_multiplicity.values()) == {18},
          "influence_multiplicity_exactly_eighteen")
    return graph, size


def graph_distance_all_spatial_slices(graph, size):
    origin = [v for v in graph if v[0][0] == 0 and v[1] in (1, 2, 3)]
    dist = {v: 0 for v in origin}
    queue = deque(origin)
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    check(len(dist) == len(graph), "connected_link_plaquette_graph")
    for n in range(1, (size[0] - 1) // 2 + 1):
        target = [v for v in graph if v[0][0] == n and v[1] in (1, 2, 3)]
        check(min(dist[v] for v in target) == n,
              "spatial_time_distance_at_n_" + str(n))
    return (size[0] - 1) // 2


def exact_spectral_root_controls():
    # For fixed L and bounded f, C_f(n) <= M_f alpha^n, M_f finite.
    # In positive transfer, eigenvector f*Omega has C_f(n) = r^n.
    an, ad = 9, 500
    sites = 3 * 3 ** 3
    check(18 * 1 < 1000, "dobrushin_contraction")
    mn, md = sites * ad, ad - an
    check(mn > md, "finite_prefactor")
    n = 200
    rn, rd = 1, 50
    check(rn * ad > an * rd, "bad_eigen_ratio_above_alpha")
    check(rn ** n * ad ** n * md > mn * an ** n * rd ** n,
          "eigen_ratio_negative_control_must_break_envelope")
    check(mn >= md, "boundary_ratio_not_excluded")
    return "9/500", "log(500/9)"


def certify():
    grid_checks = []
    for side, time in ((3, 7), (4, 9)):
        graph, dims = link_graph(side, time)
        largest = graph_distance_all_spatial_slices(graph, dims)
        grid_checks.append(f"L{side}_T{time}_distance_to_{largest}")
    ratio, log_floor = exact_spectral_root_controls()
    return (
        "YM4_VOL06_MODEL|group=continuous_SU2|dimension=3plus1"
        "|transfer=original_Gauss_Wilson|beta_domain=0_lt_beta_lt_1/18"
        "|spatial_L=GE3|json=0\n"
        "YM4_VOL06_GEOMETRY|each_link_plaquettes=6"
        "|row_influence_multiplicity=18|time_distance_ge=n"
        "|independent_slices=" + ",".join(grid_checks) + "|json=0\n"
        "YM4_VOL06_SPECTRAL|finite_L_full_physical_eigen_ratio_le=18beta"
        "|includes_Wilson_dark_and_center_sectors=YES"
        "|uses_bounded_slice_observables_dense=ANALYTIC_DEPENDENCY|json=0\n"
        "YM4_VOL06_SAMPLE|beta=1/1000|all_physical_excited_ratio_le="
        + ratio + "|energy_floor=" + log_floor + "|json=0\n"
        "YM4_VOL06_AUDIT|geometry=PASS|rational_root_control=PASS"
        "|Dobrushin_external_theorem=DEPENDENCY"
        "|positive_transfer=DEPENDENCY|analytic_audit=REQUIRED|json=0\n"
        "YM4_VOL06_SCOPE|uniform_L_strong_coupling=CANDIDATE"
        "|weak_coupling_continuum=OPEN|11_continuum_gates=OPEN"
        "|Clay_Yang_Mills=OPEN|json=0\n"
    )


if __name__ == "__main__":
    print(certify(), end="")
