#!/usr/bin/env python3
"""Scratch sanity check (not evidence, not a proof) of the tree-graph lemma in its (1+t)^f form:
if sum_{o contains e} nu_o (1+t)^{#off(o)} <= t at every off link e, then
T(e) = sum over off-link-connected sets holding e as an off link of prod nu <= t, and the per-root
item 2 holds at every link. Weights are scaled to EQUALITY in the (1+t) hypothesis, so the e^{t f}
form of the hypothesis fails at the worst link. Exact Fractions; random hypergraphs as in route A's toy."""
from fractions import Fraction as Fr
import itertools
import random


def run(seed, L=14, L_line=5, n_obj=11, t=Fr(1, 10)):
    rnd = random.Random(1000 + seed)
    line = set(range(L_line))
    objs = []
    while len(objs) < n_obj:
        k = rnd.randint(3, 6)
        o = frozenset(rnd.sample(range(L), k))
        if any(x not in line for x in o) and o not in objs:
            objs.append(o)
    off = lambda o: [x for x in o if x not in line]
    raw = [Fr(rnd.randint(1, 100), 100) for _ in objs]
    worst = max(sum(raw[i] * (1 + t) ** len(off(o)) for i, o in enumerate(objs) if e in o)
                for e in range(L_line, L) if any(e in o for o in objs))
    nu = [r * t / worst for r in raw]
    hyp = [sum(nu[i] * (1 + t) ** len(off(o)) for i, o in enumerate(objs) if e in o) for e in range(L_line, L)]
    assert max(hyp) == t
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
    lines = []
    for seed in range(12):
        n, r = run(seed)
        lines.append(f"seed {seed}: {n} connected sets; hypothesis (1+t)^f at equality; max T(e)/t = {float(r):.4f} <= 1; item 2 holds at every link")
        print(lines[-1])
    open(__file__.replace('.py', '.out'), 'w').write('\n'.join(lines) + '\n')
