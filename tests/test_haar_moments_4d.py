#!/usr/bin/env python3
"""YM4-02a: exact SU(2) Haar-moment consequences on the 2^4 Wilson lattice.

This *structural* checker derives the first two plaquette-trace cumulants from
the standard continuum SU(2) Haar identities:
    E_Haar[(1/2)Tr(U)] = 0,
    E_Haar[((1/2)Tr(U))^2] = 1/4.
It exhaustively checks the link-incidence hypotheses that eliminate all
off-diagonal plaquette covariances. Haar orthogonality is its input. Reflection
positivity and the continuum limit are later rows of the ledger.
Python standard library, integers only.
"""
from collections import Counter
from itertools import combinations, product

DIM, SIDE = 4, 2
SITES = tuple(product(range(SIDE), repeat=DIM))


def step(x, direction):
    result = list(x)
    result[direction] = (result[direction] + 1) % SIDE
    return tuple(result)


def all_plaquettes():
    # Every entry is a positively-directed link id (x, mu).
    return {
        (x, mu, nu): (
            (x, mu),
            (step(x, mu), nu),
            (step(x, nu), mu),
            (x, nu),
        )
        for x in SITES
        for mu in range(DIM)
        for nu in range(mu + 1, DIM)
    }


def check_geometry(plaquettes):
    assert len(plaquettes) == len(SITES) * DIM * (DIM - 1) // 2 == 96
    link_set = set()
    for links in plaquettes.values():
        assert len(links) == 4, "plaquette lost an edge"
        assert len(set(links)) == 4, "repeated edge inside plaquette"
        link_set.update(links)
    assert len(link_set) == 64, "wrong number of positively-directed links"
    incidence = Counter(link for links in plaquettes.values() for link in links)
    assert all(m == 2 * (DIM - 1) for m in incidence.values())
    overlap = Counter()
    for p, q in combinations(plaquettes.values(), 2):
        common = len(set(p) & set(q))
        overlap[common] += 1
        assert common <= 2, "different plaquettes lack exclusive links"
    assert sum(overlap.values()) == 96 * 95 // 2
    return overlap


def must_reject_bad_geometry(bad):
    try:
        check_geometry(bad)
    except AssertionError:
        return True
    raise AssertionError("negative geometry control incorrectly accepted")


def exact_haar_consequences():
    # Non-numerical input from SU(2) Haar symmetry / character orthogonality:
    # χ_{1/2}(U) = Tr(U) = 2a, where uniform q=(a,b,c,d) is on S^3.
    # E[a]=0 and E[a²]=1/4; the latter follows from rotational symmetry
    # and E[a²+b²+c²+d²]=1.
    n = 96
    mean_a = 0
    # E[a^2] = 1/4, carried as the integer quotient of n by 4.
    assert n % 4 == 0
    # Distinct plaquettes each have an exclusive Haar link. Integrating that
    # link first makes their covariance exactly zero.
    mean_sum = n * mean_a
    var_sum = n // 4 - n * mean_a * mean_a
    # Z(β)=exp(-βn) E_Haar exp(β sum_p a_p).
    # Derivatives of log Z at β=0 are -n+mean_sum and var_sum.
    log_z_first = -n + mean_sum
    log_z_second = var_sum
    z_first = log_z_first
    z_second = log_z_second + log_z_first * log_z_first
    assert (mean_sum, var_sum) == (0, 24)
    assert (log_z_first, log_z_second) == (-96, 24)
    assert (z_first, z_second) == (-96, 9240)
    # E S_W(β) = 96 β, Var S_W(β) = 24 β² under PRODUCT HAAR;
    # these are expectations under product Haar.
    return (int(log_z_first), int(log_z_second), int(z_second))


def main():
    p = all_plaquettes()
    overlap = check_geometry(p)
    # Distinct 4D plaquettes share 0, 1, or 2 positive links.
    assert overlap == Counter({0: 3696, 1: 768, 2: 96}), overlap
    controls = 0
    # Fault A: duplicate all four links of a different plaquette.
    first, second = list(p)[:2]
    faulty = dict(p)
    faulty[second] = faulty[first]
    controls += must_reject_bad_geometry(faulty)
    # Fault B: delete one link from one plaquette.
    faulty = dict(p)
    faulty[first] = faulty[first][:3]
    controls += must_reject_bad_geometry(faulty)
    d1, d2, z2 = exact_haar_consequences()
    assert controls == 2
    print(
        "HAAR_MOMENT_4D|sites=16|positive_links=64|plaquettes=96|"
        "pairs=4560|overlap0=3696|overlap1=768|overlap2=96|"
        f"logZ_prime_0={d1}|logZ_second_0={d2}|Z_second_0={z2}|"
        f"fault_controls={controls}/2|failed=0|json=0"
    )
    print(
        "SCOPE|standard_Haar_orthogonality_used=1|"
        "four_dimensional_finite_cutoff=1|reflection_positivity=OPEN|"
        "continuum_existence=OPEN|physical_mass_gap=OPEN|json=0"
    )


if __name__ == "__main__":
    main()
