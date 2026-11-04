# Which lattices with a side of 1 keep the conclusion? Independent. Integers only. json=0.
# The rule patterns are constant on every lattice (Step 2 uses only even link use, counted with multiplicity), so sampling gives the upper bound
# and the rule gives the lower bound. Where sampling leaves more than the rule, the small cases are read exhaustively.
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep import *


def bitlog(n):
    return n.bit_length() - 1


q8 = Q8_mat()
# The four numbers on (Z/2)x(Z/1) by direct read, all 4096
lat = Lat(2, 1)
pairs = {}
inverse = same = upto = both = diff = 0
minus = next(i for i in range(8) if i and q8.tab[i][i] == 0)
central = {0, minus}
mc = q8.mc_of
assert len(lat.words) == 2
for cfg in itertools.product(range(8), repeat=4):
    p0 = hol(q8, cfg, lat.words[0])
    p1 = hol(q8, cfg, lat.words[1])
    pairs[(mc[p0], mc[p1])] = pairs.get((mc[p0], mc[p1]), 0) + 1
    inverse += 1 if p1 == q8.inv[p0] else 0
    same += 1 if mc[p0] == mc[p1] else 0
    upto += 1 if mc[p0] == mc[p1] or mc[q8.tab[minus][p1]] == mc[p0] else 0
    if p0 in central and p1 in central:
        both += 1
        diff += 1 if p0 != p1 else 0
name = {mc[0]: "+1", mc[minus]: "-1"}
print("IND_Q8_2x1|configs=4096|second_is_inverse=%d|same_class=%d|same_up_to_centre=%d|both_central=%d|central_with_different_sign=%d|json=0" % (inverse, same, upto, both, diff))
print("IND_Q8_2x1_PAIRS|%s|json=0" % "|".join("%s,%s=%d" % (name.get(a, "c%d" % a), name.get(b, "c%d" % b), n) for (a, b), n in sorted(pairs.items())))
ps = set()
for (a, b), n in pairs.items():
    ps.add((1 << a) ^ (1 << b))
print("IND_Q8_2x1_CONSTANT|patterns=%d|constant=%d|rule=%d|json=0" % (1 << q8.nmc, len(constant_masks(q8.nmc, ps)), len(q8.rule)))

groups = [cyclic(2), cyclic(3), cyclic(4), direct(cyclic(2), cyclic(2)), S(3), D(4), Q8_mat(), D(5), A4(), Dic3(), F21(), S(4), SL23(), GL23(), TwoO(), A5(), SL25()]
family = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (1, 1, 1), (2, 1, 1), (3, 1, 1), (2, 2, 1), (2, 1, 2), (1, 2, 2), (3, 2, 1), (1, 1, 1, 1), (2, 1, 1, 1), (3, 1, 1, 1), (2, 2, 1, 1)]
for G in groups:
    for dims in family:
        lat = Lat(*dims)
        target = G.nmc - bitlog(len(G.rule))
        ps, rank, draws = sampled_parities(G, lat, target, G.n * 7919 + dims[0] * 97 + len(dims) * 13 + sum(dims), 4096)
        method = "witness_draws_%d" % draws
        # exact when the free-link count is small
        tr = set(lat.tree())
        nfree = len(lat.links) - len(tr)
        if rank < target and G.n ** nfree <= 3000000:
            ex, nf = exhaustive_parities(G, lat)
            ps = set(ex)
            method = "exhaustive_%d^%d" % (G.n, nf)
        const = constant_masks(G.nmc, ps)
        rule_inside = all(m in const for m in G.rule)
        status = "equal_rule" if const == G.rule else ("above_rule_exact" if method.startswith("exh") else "above_rule_by_samples")
        print("IND_SIDE1|group=%s|order=%d|lattice=%s|plaquettes=%d|patterns=%d|rule=%d|constant=%d|rule_inside=%d|status=%s|method=%s|json=0" % (
            G.name, G.n, "x".join(map(str, dims)), len(lat.words), 1 << G.nmc, len(G.rule), len(const), 1 if rule_inside else 0, status, method))
        sys.stdout.flush()
print("IND_SIDE1_DONE|json=0")
