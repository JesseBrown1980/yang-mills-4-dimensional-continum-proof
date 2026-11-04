# Theorem check on many finite groups and lattices with every side at least 2. Emits HBP rows. json=0.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep import *


def bitlog(n):
    return n.bit_length() - 1


groups = [cyclic(2), cyclic(3), cyclic(4), cyclic(5), cyclic(6), direct(cyclic(2), cyclic(2)), direct(direct(cyclic(2), cyclic(2)), cyclic(2)), direct(cyclic(2), cyclic(4)),
          S(3), D(4), Q8_mat(), D(5), D(6), A4(), Dic3(), F20(), F21(), S(4), SL23(), GL23(), TwoO(), A5(), SL25()]
print("IND_GROUPS|%s|json=0" % ",".join("%s:%d:mc%d:homs%d" % (G.name, G.n, G.nmc, len(G.hom_vals)) for G in groups))
lat2 = [(2, 2), (2, 3), (3, 3), (2, 4), (3, 4), (2, 2, 2), (2, 2, 3), (2, 3, 3), (2, 2, 2, 2)]
bad = 0
for G in groups:
    for dims in lat2:
        lat = Lat(*dims)
        target = G.nmc - bitlog(len(G.rule))
        small = dims == (2, 2) and G.n <= 12
        if small:
            ex, nfree = exhaustive_parities(G, lat)
            ps = set(ex)
            method = "exhaustive_%d^%d" % (G.n, nfree)
        else:
            ps, rank, draws = sampled_parities(G, lat, target, G.n * 1009 + sum(dims) * 31 + len(dims), 200000)
            method = "witness_draws_%d_rank_%d_target_%d" % (draws, rank, target)
        const = constant_masks(G.nmc, ps)
        ok = const == G.rule
        bad += 0 if ok else 1
        F = len(lat.words)
        ok2 = True
        for m in G.rule:
            eps_minus = (m >> G.mc_of[0]) & 1
            want = 1 if (eps_minus and F % 2) else 0
            vals = {popcount(m & p) & 1 for p in ps}
            ok2 = ok2 and vals == {want}
        print("IND_RULE|group=%s|order=%d|lattice=%s|F=%d|classes=%d|patterns=%d|rule=%d|constant_found=%d|equal_rule=%d|rule_S_equals_eps^F=%d|method=%s|json=0" % (
            G.name, G.n, "x".join(map(str, dims)), F, G.nmc, 1 << G.nmc, len(G.rule), len(const), 1 if ok else 0, 1 if ok2 else 0, method))
        sys.stdout.flush()
print("IND_RULE_DONE|mismatches=%d|json=0" % bad)
