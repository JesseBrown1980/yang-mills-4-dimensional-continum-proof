#!/usr/bin/env python3
"""Scratch sanity check (not evidence) of Lemma 4.12 of G1-a.md on random small hypergraphs.

Links 0..L-1, the first L_line of them 'line', the rest 'off'. Objects are random subsets.
Weights nu_o are scaled (exact Fractions) so that the hypothesis
sum_{o contains e} nu_o (1+t)^{#off(o)} <= t holds at every off link e (a hypothesis slightly
stronger than the e^{t #off} form only in that (1+t)^n <= e^{tn}; we use the e-form via a rational
upper bound of e^t). Every off-link-connected set of objects is enumerated, and
T(e) = sum over sets holding e as an off link of prod nu is compared with t, exactly; item 2 too.
"""
from fractions import Fraction as Fr
import itertools
import random

def e_up(t):
    # rational upper bound of e^t, 0 <= t <= 1: Taylor to 30 terms plus a geometric tail
    s = Fr(0); term = Fr(1)
    for j in range(30):
        s += term
        term = term * t / (j + 1)
    return s + term * 2

def run(seed, L=14, L_line=5, n_obj=11, t=Fr(1, 10)):
    rnd = random.Random(seed)
    line = set(range(L_line))
    objs = []
    while len(objs) < n_obj:
        k = rnd.randint(3, 6)
        o = frozenset(rnd.sample(range(L), k))
        if any(x not in line for x in o) and o not in objs:
            objs.append(o)
    off = lambda o: [x for x in o if x not in line]
    et = e_up(t)
    raw = [Fr(rnd.randint(1, 100), 100) for _ in objs]
    # scale so the hypothesis holds with equality at the worst off link
    worst = max(sum(raw[i] * et ** len(off(o)) for i, o in enumerate(objs) if e in o)
                for e in range(L_line, L) if any(e in o for o in objs))
    nu = [r * t / worst for r in raw]
    for e in range(L_line, L):
        assert sum(nu[i] * et ** len(off(o)) for i, o in enumerate(objs) if e in o) <= t
    # enumerate off-link-connected subsets
    adj = {i: {j for j in range(n_obj) if j != i and set(off(objs[i])) & set(off(objs[j]))} for i in range(n_obj)}
    def connected(S):
        S = list(S); seen = {S[0]}; stack = [S[0]]
        while stack:
            a = stack.pop()
            for b in adj[a]:
                if b in S and b not in seen:
                    seen.add(b); stack.append(b)
        return len(seen) == len(S)
    polys = [S for r in range(1, n_obj + 1) for S in itertools.combinations(range(n_obj), r) if connected(S)]
    worst_ratio = Fr(0)
    for e in range(L_line, L):
        T = Fr(0)
        for S in polys:
            if any(e in off(objs[i]) for i in S):
                p = Fr(1)
                for i in S:
                    p *= nu[i]
                T += p
        assert T <= t, (seed, e, float(T))
        worst_ratio = max(worst_ratio, T / t)
    # item 2 at every link (line or off)
    for e in range(L):
        lhs = Fr(0)
        for S in polys:
            if len(S) >= 2 and any(e in objs[i] for i in S):
                p = Fr(1)
                for i in S:
                    p *= nu[i]
                lhs += p
        rhs = sum(nu[i] * ((1 + t) ** len(off(o)) - 1) for i, o in enumerate(objs) if e in o)
        assert lhs <= rhs, (seed, e)
    return len(polys), worst_ratio

if __name__ == "__main__":
    for seed in range(12):
        n, r = run(seed)
        print(f"seed {seed}: {n} connected sets; max T(e)/t = {float(r):.4f} <= 1; item 2 holds at every link")
