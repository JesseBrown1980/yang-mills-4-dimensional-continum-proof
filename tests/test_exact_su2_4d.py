#!/usr/bin/env python3
"""Exact finite 4D SU(2) gauge-covariance controls using integer-tuple quaternions.

A quaternion is five ints (a, b, c, d, den), meaning (a, b, c, d) / den, reduced with den > 0.
This checks a finite-lattice algebraic lemma, proved in Lemma 0001, on one lattice.
Requires Python >= 3.10, stdlib only, integers only.
"""
from __future__ import annotations

from itertools import product
from math import gcd
from random import Random

SIDE = 2
D = 4
SITES = list(product(range(SIDE), repeat=D))
CONTROLS = set()


def quat(a, b, c, d, den=1):
    assert den > 0
    g = gcd(gcd(gcd(gcd(a, b), c), d), den)
    return (a // g, b // g, c // g, d // g, den // g)


ONE = quat(1, 0, 0, 0)


def multiply(p, q):
    a, b, c, d, m = p
    e, f, g, h, n = q
    return quat(
        a*e - b*f - c*g - d*h,
        a*f + b*e + c*h - d*g,
        a*g - b*h + c*e + d*f,
        a*h + b*g - c*f + d*e,
        m*n,
    )


def inverse(p):
    a, b, c, d, den = p
    return (a, -b, -c, -d, den)


def is_unit(p):
    a, b, c, d, den = p
    return a*a + b*b + c*c + d*d == den*den


def shift(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % SIDE
    return tuple(y)


# Independent noncommuting SU(2) elements of infinite order.
A = quat(3, 4, 0, 0, 5)
B = quat(5, 0, 12, 0, 13)
C = quat(8, 0, 0, 15, 17)
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


def half_trace(p):
    # For unit quaternions Re Tr U = 2*scalar. Returned reduced, as an integer pair.
    g = gcd(p[0], p[4])
    return (p[0] // g, p[4] // g)


def wilson_action(plaquettes, beta=(3, 2)):
    # beta * sum over plaquettes of (1 - half trace), as a reduced integer pair.
    top, bottom = 0, 1
    for p in plaquettes.values():
        n, d = half_trace(p)
        top, bottom = top*d + (d - n)*bottom, bottom*d
    g = gcd(beta[0]*top, beta[1]*bottom)
    return (beta[0]*top // g, beta[1]*bottom // g)


def covariance_holds(P, Pt, g):
    # Each Wilson loop transforms by conjugation at its base site.
    return all(
        Pt[(x, mu, nu)] == multiply(multiply(g[x], value), inverse(g[x]))
        for (x, mu, nu), value in P.items()
    )


WILSON = {
    20261103: (449929987986, 3508004825),
    1729: (193195378719, 1349232625),
    314159: (185342826929127, 1490902050625),
    271828: (2969866827969, 22936954625),
}


def known_answers():
    # The product order, and one plaquette by hand.
    assert multiply(A, B) == (15, 20, 36, 48, 65)
    # The unit test answers both ways.
    assert is_unit(A) and not is_unit((1, 1, 0, 0, 1))
    # One link A, every other link ONE: exactly its six plaquettes move, each with half trace 3/5.
    U = {(x, mu): ONE for x in SITES for mu in range(D)}
    origin = SITES[0]
    U[(origin, 0)] = A
    P = all_plaquettes(U)
    six = {(origin, 0, nu) for nu in (1, 2, 3)} | {(shift(origin, nu), 0, nu) for nu in (1, 2, 3)}
    assert {k for k, v in P.items() if v != ONE} == six
    assert all(half_trace(P[k]) == (3, 5) for k in six)
    # (3/2) * 6 * (1 - 3/5) = 18/5
    assert wilson_action(P) == (18, 5)


def wrong_matrix_same_trace(v):
    # A change of the plaquette matrix that keeps the trace when v is not central.
    for h in (A, B):
        w = multiply(multiply(h, v), inverse(h))
        if w != v:
            return w
    return multiply(v, A)


def checker_controls(P, Pt, g):
    # The covariance check must see one wrong plaquette anywhere. The wrong matrix keeps the trace, apart from an
    # identity plaquette, the only SU(2) element with half trace 1. Both counts come from the checks themselves.
    seen = kept = 0
    for k in P:
        wrong = dict(Pt)
        wrong[k] = wrong_matrix_same_trace(Pt[k])
        seen += 0 if covariance_holds(P, wrong, g) else 1
        kept += 1 if half_trace(wrong[k]) == half_trace(Pt[k]) else 0
    return seen, kept


def check_seed(seed):
    U, g = links_and_gauge(seed)
    assert len(U) == 64 and len(g) == 16
    assert all(is_unit(p) for p in (*U.values(), *g.values()))
    assert multiply(A, B) != multiply(B, A)
    for p in (*U.values(), *g.values()):
        assert multiply(p, inverse(p)) == ONE
    P = all_plaquettes(U)
    transformed = gauge_transform(U, g)
    Pt = all_plaquettes(transformed)
    assert len(P) == 96 and len(Pt) == 96
    assert all(is_unit(v) for v in Pt.values())
    assert any(half_trace(v) != (1, 1) for v in P.values())  # A sample with curvature
    assert covariance_holds(P, Pt, g)
    detected = checker_controls(P, Pt, g)
    assert all(half_trace(Pt[k]) == half_trace(P[k]) for k in P)
    assert wilson_action(P) == wilson_action(Pt)
    assert wilson_action(P) == WILSON[seed]
    # Fault #1: corrupt one link of the transformed field. The covariance check must fail.
    corrupted = dict(transformed)
    first = next(iter(corrupted))
    corrupted[first] = multiply(corrupted[first], A)
    if not covariance_holds(P, all_plaquettes(corrupted), g):
        CONTROLS.add((seed, "corrupted_link"))
    # Fault #2: remove the endpoint inverse in the gauge law. The traces must move.
    wrong = all_plaquettes(gauge_transform(U, g, bad=True))
    if [half_trace(P[k]) for k in sorted(P)] != [half_trace(wrong[k]) for k in sorted(P)]:
        CONTROLS.add((seed, "endpoint_inverse"))
    return wilson_action(P), detected


def main():
    if not __debug__:
        raise SystemExit("assertions are off: run without -O")
    known_answers()
    seeds = (20261103, 1729, 314159, 271828)
    results = [check_seed(s) for s in seeds]
    actions = [r[0] for r in results]
    assert len(set(actions)) > 1
    seen = sum(r[1][0] for r in results)
    kept = sum(r[1][1] for r in results)
    assert seen == 96 * len(seeds) and kept == 372 and len(CONTROLS) == 2 * len(seeds)
    print(
        "EXACT_SU2_4D|sites=16|links=64|plaquettes=96|seeds=4|"
        "gauge_covariance=PASS|wilson_action=PASS|fault_controls=%d/2|"
        "failures=0|json=0" % (len(CONTROLS) // len(seeds))
    )
    for seed, action in zip(seeds, actions):
        print("EXACT_SU2_4D_VALUE|seed=%d|S_W=%d/%d|json=0" % (seed, action[0], action[1]))
    print(
        "EXACT_SU2_4D_CHECKER|one_link_fixture_S_W=18/5|"
        "wrong_plaquettes_detected=%d/%d|kept_the_trace=%d|json=0" % (seen, 96 * len(seeds), kept)
    )
    print(
        "SCOPE|finite_periodic_lattice_only=1|continuum_existence=OPEN|"
        "physical_mass_gap=OPEN|json=0"
    )


if __name__ == "__main__":
    main()
