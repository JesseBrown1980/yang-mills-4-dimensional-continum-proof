#!/usr/bin/env python3
"""Exact finite 4D SU(2) gauge-covariance controls using rational quaternions.

This proves and checks only a finite-lattice algebraic lemma, NOT continuum
existence or a physical mass gap. Requires Python >= 3.10, stdlib only.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import product
from random import Random

ONE = (Q(1), Q(0), Q(0), Q(0))
SIDE = 2
D = 4
SITES = list(product(range(SIDE), repeat=D))


def multiply(p, q):
    a, b, c, d = p
    e, f, g, h = q
    return (
        a*e - b*f - c*g - d*h,
        a*f + b*e + c*h - d*g,
        a*g - b*h + c*e + d*f,
        a*h + b*g - c*f + d*e,
    )


def inverse(p):
    a, b, c, d = p
    return (a, -b, -c, -d)


def norm_sq(p):
    return sum(z*z for z in p)


def shift(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % SIDE
    return tuple(y)


# Independent noncommuting SU(2) elements, not merely a finite subgroup.
A = (Q(3, 5), Q(4, 5), Q(0), Q(0))
B = (Q(5, 13), Q(0), Q(12, 13), Q(0))
C = (Q(8, 17), Q(0), Q(0), Q(15, 17))
PALETTE = [
    ONE, A, B, C, inverse(A), inverse(B), inverse(C),
    multiply(A, B), multiply(B, C), multiply(C, A),
]


def links_and_gauge(seed):
    rng = Random(seed)
    U = {(x, mu): PALETTE[rng.randrange(len(PALETTE))] for x in SITES for mu in range(D)}
    g = {x: PALETTE[rng.randrange(len(PALETTE))] for x in SITES}
    return U, g


def gauge_transform(U, g, bad=False):
    # bad=True implements intentionally incorrect missing inverse.
    return {
        (x, mu): multiply(
            multiply(g[x], U[(x, mu)]),
            (g[shift(x, mu)] if bad else inverse(g[shift(x, mu)])),
        )
        for x in SITES for mu in range(D)
    }


def plaquette(U, x, mu, nu):
    return multiply(
        multiply(
            multiply(U[(x, mu)], U[(shift(x, mu), nu)]),
            inverse(U[(shift(x, nu), mu)]),
        ),
        inverse(U[(x, nu)]),
    )


def all_plaquettes(U):
    return {
        (x, mu, nu): plaquette(U, x, mu, nu)
        for x in SITES for mu in range(D) for nu in range(mu+1, D)
    }


def wilson_action(plaquettes, beta=Q(3, 2)):
    # For unit quaternions Re Tr U = 2*q.scalar.
    return beta * sum((Q(1) - p[0] for p in plaquettes.values()), Q(0))


def assert_raises_assertion(fn):
    try:
        fn()
    except AssertionError:
        return
    raise AssertionError("fault control did not fail")


def assert_equal(left, right):
    assert left == right, "mismatch"


def check_seed(seed):
    U, g = links_and_gauge(seed)
    assert len(U) == 64 and len(g) == 16
    assert all(norm_sq(p) == 1 for p in (*U.values(), *g.values()))
    assert multiply(A, B) != multiply(B, A)
    for p in (*U.values(), *g.values()):
        assert multiply(p, inverse(p)) == ONE
    P = all_plaquettes(U)
    transformed = gauge_transform(U, g)
    Pt = all_plaquettes(transformed)
    assert len(P) == 96 and len(Pt) == 96
    assert all(norm_sq(v) == 1 for v in Pt.values())
    assert any(v[0] != 1 for v in P.values())  # Non-pure-gauge sample
    for (x, mu, nu), value in P.items():
        # Wilson loop has exact conjugation covariance, not matrix equality.
        expected = multiply(multiply(g[x], value), inverse(g[x]))
        assert Pt[(x, mu, nu)] == expected
        assert Pt[(x, mu, nu)][0] == value[0]
    assert wilson_action(P) == wilson_action(Pt)
    # Fault #1: alter one observed plaquette trace by one rational unit.
    first = next(iter(P))
    assert_raises_assertion(
        lambda: assert_equal(P[first][0], Pt[first][0] + Q(1, 10**6))
    )
    # Fault #2: remove the endpoint inverse in the gauge law.
    wrong = all_plaquettes(gauge_transform(U, g, bad=True))
    assert_raises_assertion(
        lambda: assert_equal(
            [P[k][0] for k in sorted(P)],
            [wrong[k][0] for k in sorted(P)],
        )
    )
    return wilson_action(P)


def main():
    seeds = (20261103, 1729, 314159, 271828)
    results = [check_seed(s) for s in seeds]
    assert len(set(results)) > 1
    print(
        "EXACT_SU2_4D|sites=16|links=64|plaquettes=96|seeds=4|"
        "gauge_covariance=PASS|wilson_action=PASS|fault_controls=2/2|"
        "failures=0|json=0"
    )
    print(
        "SCOPE|finite_periodic_lattice_only=1|continuum_existence=OPEN|"
        "physical_mass_gap=OPEN|json=0"
    )


if __name__ == "__main__":
    main()
