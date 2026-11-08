#!/usr/bin/env python3
"""
YM4-03C, gate G3: the first non-plaquette term, the chair, by route S, in code separate from the engine.

The operator's gate: "an independent recomputation of the first non-plaquette term (the chair) with its operator definition, sign, rational
coefficient and lattice-size conditions". This file shares no code with blocked_action_engine.rs. It works on plain fine coordinates of Z^d,
d = 4 and d = 3, with no doubled cells, no group, no Weingarten matrix and no projection.

Operator: chi_1/2 of the 6-link coarse loop around P = (0, 1) and Q = (0, 2) at the coarse site 0, which share l = (0, e_0), spin 0 on l.
Route S: a count of the fine surfaces H with the chair's fine boundary, each with its character integral.
  1. Every H with that boundary is F_P xor F_Q xor the boundary of a 3-chain C. Method A takes every chain of at most three unit cubes in a
     window around the chair; method B is the defect-repair walk from F_P xor F_Q. Both keep the sets of at most 10 plaquettes.
  2. Each set connected through off links is read for its topology: every off link in exactly two of its plaquettes, every line link of the
     loop in exactly one, its Euler characteristic V - E + F, and the positions of l it holds.
  3. A disk of F spin-1/2 plaquettes integrates to 2 t_2^F chi_1/2(boundary): F - E_int + V_int = 1, each internal link a factor 1/2 by
     int chi(AU) chi(U^-1 B) dU = chi(AB)/2, each internal vertex a closed loop of value 2. Holding one position of l or none, it has spin 0
     on l (Lemma A of the note).
  4. t_2 = I_2/I_1 by the Bessel series, a route apart from the engine's McKay powers; at order 10 a disk of 10 plaquettes enters with
     2 (1/4)^10.
  5. Integer-spin decorations at order 10 hold a half-integer set of 8 plaquettes and one spin-1 plaquette; each candidate is read for an
     invariant at every off link by Clebsch-Gordan counting. Fillings of P and Q share line links only, so they are compatible polymers and
     the logarithm holds no product of them.
Sign: +c in log rho, -c in S_10, by S_eff = -log rho + const.

Run as python3 -I -B -X utf8 route_s_chair.py. Integers and integer pairs only, the standard library only, json=0.
"""
import itertools
import sys
from math import gcd

OUT = []


def say(text):
    OUT.append(text)
    sys.stdout.write(text + "\n")


def q(n, d=1):
    if d < 0:
        n, d = -n, -d
    g = gcd(n, d) or 1
    return (n // g, d // g)


def qadd(a, b):
    return q(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def qmul(a, b):
    return q(a[0] * b[0], a[1] * b[1])


def qs(a):
    if a[1] == 1:
        return str(a[0])
    return str(a[0]) + "/" + str(a[1])


TOP = 12


def ser_mul(a, b):
    out = [(0, 1)] * (TOP + 1)
    for i in range(TOP + 1):
        if a[i][0] == 0:
            continue
        for k in range(TOP + 1 - i):
            if b[k][0]:
                out[i + k] = qadd(out[i + k], qmul(a[i], b[k]))
    return out


def ser_inv(a):
    out = [(0, 1)] * (TOP + 1)
    out[0] = q(a[0][1], a[0][0])
    for k in range(1, TOP + 1):
        s = (0, 1)
        for i in range(1, k + 1):
            s = qadd(s, qmul(a[i], out[k - i]))
        out[k] = qmul(q(-s[0], s[1]), out[0])
    return out


def factorial(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r


def bessel(n):
    """I_n(beta) = sum_k (beta/2)^(2k+n) / (k! (k+n)!), as exact coefficients through beta^TOP."""
    out = [(0, 1)] * (TOP + 1)
    k = 0
    while 2 * k + n <= TOP:
        e = 2 * k + n
        out[e] = q(1, (1 << e) * factorial(k) * factorial(k + n))
        k += 1
    return out


def t2():
    i1 = bessel(1)
    i2 = bessel(2)
    b1 = i1[1:] + [(0, 1)]  # I_1 / beta
    b2 = i2[1:] + [(0, 1)]  # I_2 / beta
    return ser_mul(b2, ser_inv(b1))


# ---- the fine lattice Z^d

def vadd(x, y):
    return tuple(a + b for a, b in zip(x, y))


def unit(d, k):
    return tuple(1 if i == k else 0 for i in range(d))


def plaq(x, mu, nu):
    return (x, mu, nu) if mu < nu else (x, nu, mu)


def plaq_edges(d, p):
    x, mu, nu = p
    return [(x, mu), (vadd(x, unit(d, mu)), nu), (vadd(x, unit(d, nu)), mu), (x, nu)]


def plaq_vertices(d, p):
    x, mu, nu = p
    return [x, vadd(x, unit(d, mu)), vadd(x, unit(d, nu)), vadd(vadd(x, unit(d, mu)), unit(d, nu))]


def is_line(d, e):
    x, mu = e
    return all(x[k] % 2 == 0 for k in range(d) if k != mu)


def cube_faces(d, x, dirs):
    out = []
    for k in dirs:
        i, j = [m for m in dirs if m != k]
        out.append(plaq(x, i, j))
        out.append(plaq(vadd(x, unit(d, k)), i, j))
    return frozenset(out)


def filling(d, mu, nu):
    out = set()
    for s in (0, 1):
        for r in (0, 1):
            x = [0] * d
            x[mu] = s
            x[nu] = r
            out.add(plaq(tuple(x), mu, nu))
    return frozenset(out)


def boundary(d, H):
    odd = set()
    for p in H:
        for e in plaq_edges(d, p):
            odd ^= {e}
    return frozenset(odd)


def window_cubes(d, lo, hi):
    out = []
    for dirs in itertools.combinations(range(d), 3):
        ranges = [range(lo, hi) for _ in range(d)]
        for x in itertools.product(*ranges):
            out.append((tuple(x), dirs))
    return out


def method_a(d, F, budget):
    """Chains of at most three cubes in the window [-2, 3)^d; a third cube is tried when it can bring the size within the budget."""
    cubes = window_cubes(d, -2, 3)
    faces = [cube_faces(d, x, dirs) for x, dirs in cubes]
    owners = {}
    for index, fs in enumerate(faces):
        for f in fs:
            owners.setdefault(f, []).append(index)
    found = set()
    if len(F) <= budget:
        found.add(F)
    n = len(cubes)
    # one and two cubes over the whole window, then a third cube sharing faces with the running set
    for i in range(n):
        Hi = F ^ faces[i]
        if len(Hi) <= budget:
            found.add(Hi)
        for j in range(i + 1, n):
            Hij = Hi ^ faces[j]
            if len(Hij) <= budget:
                found.add(Hij)
            need = len(Hij) + 6 - budget
            if need > 12:
                continue
            counts = {}
            for f in Hij:
                for k in owners.get(f, ()):
                    if k > j:
                        counts[k] = counts.get(k, 0) + 1
            for k, shared in counts.items():
                if 2 * shared >= need:
                    Hk = Hij ^ faces[k]
                    if len(Hk) <= budget:
                        found.add(Hk)
    return found, len(cubes)


def method_b(d, F, budget):
    """The defect-repair walk of tests/test_one_scale_blocking.py, written again here: from the empty set, add a plaquette on the lowest
    edge of the defect, the difference between the set's boundary and the chair's, until the defect closes; a set stops when its defect
    holds more than four edges per plaquette left in the budget."""
    target = boundary(d, F)
    seen = set()
    found = set()
    stack = [(frozenset(), target)]
    while stack:
        H, defect = stack.pop()
        if H in seen:
            continue
        seen.add(H)
        if not defect:
            found.add(H)
            continue
        remaining = budget - len(H)
        if remaining <= 0 or len(defect) > 4 * remaining:
            continue
        x, mu = min(defect)
        for nu in range(d):
            if nu == mu:
                continue
            for s in (0, -1):
                base = list(x)
                base[nu] += s
                p = plaq(tuple(base), mu, nu)
                if p in H:
                    continue
                moved = set(defect)
                for e in plaq_edges(d, p):
                    moved ^= {e}
                stack.append((H | {p}, frozenset(moved)))
    return found


def read_set(d, H, positions):
    plist = sorted(H)
    by_edge = {}
    for p in plist:
        for e in plaq_edges(d, p):
            by_edge.setdefault(e, []).append(p)
    parent = {p: p for p in plist}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for e, ps in by_edge.items():
        if not is_line(d, e):
            for p in ps[1:]:
                parent[find(ps[0])] = find(p)
    connected = len({find(p) for p in plist}) == 1
    off_two = all(len(ps) == 2 for e, ps in by_edge.items() if not is_line(d, e))
    vertices = set()
    for p in plist:
        vertices.update(plaq_vertices(d, p))
    euler = len(vertices) - len(by_edge) + len(plist)
    held = tuple(k for k, e in enumerate(positions) if e in by_edge)
    span = max(max(x[k] for x in vertices) - min(x[k] for x in vertices) for k in range(d))
    return connected, off_two, euler, held, span


def invariants(spins):
    mult = {0: 1}
    for n in spins:
        nxt = {}
        for j, c in mult.items():
            k = abs(j - n)
            while k <= j + n:
                nxt[k] = nxt.get(k, 0) + c
                k += 2
        mult = nxt
    return mult.get(0, 0)


def decorations(d, H8):
    """One spin-1 plaquette q beside a half-integer set of 8 at spin 1/2: count the q for which every off link admits an invariant."""
    passing = 0
    tried = 0
    for base in itertools.product(range(-2, 4), repeat=d):
        for mu in range(d):
            for nu in range(mu + 1, d):
                qd = plaq(tuple(base), mu, nu)
                if qd in H8:
                    continue
                tried += 1
                spins = {}
                for p in list(H8) + [qd]:
                    for e in plaq_edges(d, p):
                        if not is_line(d, e):
                            spins.setdefault(e, []).append(2 if p == qd else 1)
                if all(invariants(v) > 0 for v in spins.values()):
                    passing += 1
    return passing, tried


def run(d):
    label = "d" + str(d)
    FP = filling(d, 0, 1)
    FQ = filling(d, 0, 2)
    F = FP ^ FQ
    target = boundary(d, F)
    positions = [(tuple([0] * d), 0), (unit(d, 0), 0)]
    budget = 10
    seta, ncubes = method_a(d, F, budget)
    setb = method_b(d, F, budget)
    for H in seta | setb:
        assert boundary(d, H) == target
    rows = {}
    disks = []
    for H in sorted(seta | setb, key=lambda s: (len(s), sorted(s))):
        connected, off_two, euler, held, span = read_set(d, H, positions)
        key = (len(H), connected, off_two, euler)
        rows[key] = rows.get(key, 0) + 1
        if connected and off_two and euler == 1 and len(H) <= budget:
            disks.append((H, held, span, H in seta, H in setb))
    t = t2()
    # the leading term of t_2, read from the Bessel series: a disk of 10 plaquettes enters at beta^10 with 2 t_2^10's leading term
    lead = t[1]
    w = (2, 1)
    for _ in range(10):
        w = qmul(w, lead)
    coef = (0, 1)
    held_list = []
    spans = []
    both = 0
    for H, held, span, ina, inb in disks:
        if len(H) == 10:
            coef = qadd(coef, w)
            held_list.append("(" + ",".join(str(h) for h in held) + ")")
            spans.append(span)
            both += 1 if (ina and inb) else 0
        assert len(held) <= 1, "a disk holding both positions of l"
    eight = [H for H in seta | setb if len(H) == 8]
    passing = 0
    tried = 0
    for H8 in eight:
        p, tr = decorations(d, H8)
        passing += p
        tried += tr
    by = ",".join(str(k[0]) + ":" + ("connected" if k[1] else "split") + ":" + ("off_links_in_two" if k[2] else "off_links_not_in_two") + ":euler=" + str(k[3]) + "=" + str(v) for k, v in sorted(rows.items()))
    say("ROUTE_S_SETS|" + label + "|boundary=the_chair's_12_line_links|method_a_chains_of_<=3_cubes_in_window_[-2,3)^d=" + str(len(seta)) + "|cubes_in_window=" + str(ncubes) + "|method_b_defect_repair_walk=" + str(len(setb)) + "|in_both=" + str(len(seta & setb)) + "|by_size_connection_valence_euler=" + by + "|tag=MEASURED|json=0")
    say("ROUTE_S_DISKS|" + label + "|disks_of_10=" + str(len(held_list)) + "|positions_of_l_held=" + ",".join(sorted(held_list)) + "|found_by_both_methods=" + str(both) + "|largest_fine_span=" + str(max(spans) if spans else 0) + "|so_it_embeds_in_fine_6^d,coarse_sides>=3|tag=MEASURED|json=0")
    say("ROUTE_S_DECORATIONS|" + label + "|half-integer_sets_of_8=" + str(len(eight)) + "|spin-1_plaquettes_tried_in_window=" + str(tried) + "|with_an_invariant_at_every_off_link=" + str(passing) + "|tag=MEASURED|json=0")
    say("ROUTE_S_T2|route=Bessel_I_2/I_1|t_2=" + ",".join("b" + str(k) + ":" + qs(t[k]) for k in range(1, 10) if t[k][0]) + "|tag=MEASURED|json=0")
    s10 = q(-coef[0], coef[1])
    say("ROUTE_S_CHAIR|" + label + "|operator=chi_1/2_of_the_6-link_loop_around_P=(0,1)_and_Q=(0,2)_at_x'=0,spin_0_on_l=(0,e_0)|b10_log_rho=" + qs(coef) + "|S_10_coefficient=" + qs(s10) + "|sign=+c_in_log_rho,-c_in_S_eff|clusters=none,F_P_and_F_Q_share_line_links_only|decorations=" + str(passing) + "|lattice=coarse_sides>=3|tag=MEASURED|json=0")
    return coef, passing


def main():
    results = []
    for d in (4, 3):
        coef, passing = run(d)
        results.append((coef, passing))
    ok = all(c == (3, 524288) and p == 0 for c, p in results)
    say("ROUTE_S_DONE|d4=" + qs(results[0][0]) + "|d3=" + qs(results[1][0]) + "|frozen=3/524288|result=" + ("MET" if ok else "MISS") + "|json=0")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
