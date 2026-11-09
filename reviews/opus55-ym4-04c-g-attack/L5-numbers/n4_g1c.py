# n4_g1c.py -- L5-numbers lane, check G1c part 1: C10's norms under the unfaulted count, the pinned
# one_position_support fault, and C19's variant_that_fires_with_another_ratio, by exact enumeration.
# Scale-k lattice (Z/16)^4 -> scale k+1 lattice (Z/8)^4 -> the next blocking to (Z/4)^4.
# A norm is a polynomial in E = e^kappa: sum over the Y containing a link of E^{count(Y)} * sup|R(Y)|,
# with sup|R(Y)| = 2|s| for every Y here (sup|chi_1/2| = 2). Integer only.
import sys
sys.path.insert(0, '/mnt/c/tmp/opus55/ym4-04c-gattack/work/L5-numbers')
import itertools
import ilib as L
from ilib import rat, add, sub, mul, div, exp_point, fmti, inside, dec, lt_rat, gt_rat

FAILS = []


def row(name, ok, **kv):
    print('NUM|id=' + name + '|' + '|'.join(k + '=' + str(v) for k, v in kv.items()) + '|ok=' + ('1' if ok else '0') + '|json=0')
    if not ok:
        FAILS.append(name)


def links_of_plaquette(x, mu, nu, n):
    """the 4 links (base, direction) of the plaquette at x in the (mu, nu) plane on (Z/n)^4"""
    def sh(y, d):
        z = list(y)
        z[d] = (z[d] + 1) % n
        return tuple(z)
    return [(x, mu), (sh(x, mu), nu), (sh(x, nu), mu), (x, nu)]


def is_line(link):
    y, mu = link
    return all(y[d] % 2 == 0 for d in range(4) if d != mu)


def position(link):
    """0 or 1 for a line link: the parity of its coordinate along its direction"""
    y, mu = link
    return y[mu] % 2


def fine_positions(clink, n_coarse):
    """the two fine line links e_0, e_1 of a coarse link (x', mu) on (Z/(2 n_coarse))^4"""
    x, mu = clink
    b = tuple(2 * c for c in x)
    b1 = list(b)
    b1[mu] = (b1[mu] + 1) % (2 * n_coarse)
    return [(b, mu), (tuple(b1), mu)]


NC = 8     # scale k+1 side
NF = 16    # scale k side
planes = [(m, v) for m in range(4) for v in range(4) if m < v]

# coarse plaquettes P'' of scale k+1 and their Y (8 fine line links)
fine_norm_unf = {}    # fine link -> polynomial dict exponent->count (unfaulted: exponent #Y = 8)
fine_norm_flt = {}    # faulted: exponent = number of links of Y at position 1
coarse_norm_unf = {}  # coarse link -> polynomial (exponent #Y'' = 4)
coarse_norm_var = {}  # the variant: exponent = number of links of boundary P'' at position 1 for the next blocking
count_hist = {}
pos1_per_Y = set()
for x in itertools.product(range(NC), repeat=4):
    for (mu, nu) in planes:
        cl = links_of_plaquette(x, mu, nu, NC)
        Y = []
        for c in cl:
            Y.extend(fine_positions(c, NC))
        assert len(set(Y)) == 8 and all(is_line(f) for f in Y)
        npos1 = sum(1 for f in Y if position(f) == 1)
        pos1_per_Y.add(npos1)
        for f in Y:
            d = fine_norm_unf.setdefault(f, {})
            d[8] = d.get(8, 0) + 1
            d = fine_norm_flt.setdefault(f, {})
            d[npos1] = d.get(npos1, 0) + 1
        cnt = sum(1 for c in cl if is_line(c) and position(c) == 1)
        count_hist[cnt] = count_hist.get(cnt, 0) + 1
        for c in cl:
            d = coarse_norm_unf.setdefault(c, {})
            d[4] = d.get(4, 0) + 1
            d = coarse_norm_var.setdefault(c, {})
            d[cnt] = d.get(cnt, 0) + 1


def polys(dct):
    return sorted(set(tuple(sorted(v.items())) for v in dct.values()))


row('C10_fine_unfaulted_polys', polys(fine_norm_unf) == [((8, 6),)], polys=str(polys(fine_norm_unf)))
row('C10_fine_faulted_polys', polys(fine_norm_flt) == [((4, 6),)] and pos1_per_Y == {4}, polys=str(polys(fine_norm_flt)))
row('C10_coarse_unfaulted_polys', polys(coarse_norm_unf) == [((4, 6),)], polys=str(polys(coarse_norm_unf)))
pv = polys(coarse_norm_var)
row('C19_variant_count_histogram', sorted(count_hist) == [0, 1, 2], hist=str(sorted(count_hist.items())), coarse_polys=str(pv))

# evaluate at kappa = 1/4 (E = e^{1/4}) and kappa = 0; the norm of each link is 2|s| * poly(E)
E = exp_point(1 << (L.P - 2))


def ev(poly, Ev):
    s = (0, 0)
    for (e, c) in poly:
        p = (L.ONE, L.ONE)
        for _ in range(e):
            p = mul(p, Ev)
        s = add(s, L.muli(p, c))
    return s


vals = [(p, ev(p, E)) for p in pv]
best = vals[0]
for v in vals[1:]:
    if v[1][0] > best[1][1]:
        best = v
dominates = all(best[0] == v[0] or v[1][1] < best[1][0] for v in vals)
row('C19_variant_max_link', best[0] == ((1, 3), (2, 3)) and dominates, max_poly=str(best[0]), value_over_2s=fmti(best[1], 10))
fine_flt = ev(((4, 6),), E)
ratio = div(best[1], fine_flt)
# the closed form (e^{-3k} + e^{-2k})/2 at k = 1/4
cf = L.divi(add(exp_point(-(3 << (L.P - 2))), exp_point(-(1 << (L.P - 1)))), 2)
em1 = exp_point(-L.ONE)
em14 = exp_point(-(1 << (L.P - 2)))
row('C19_variant_ratio', inside(ratio, '0.5394486', '0.5394487') and inside(cf, '0.5394486062268', '0.5394486062269') and
    ratio[0] <= cf[1] and cf[0] <= ratio[1] and ratio[0] > em1[1] and ratio[1] < em14[0] and ratio[1] < L.ONE,
    ratio=fmti(ratio, 13), closed_form=fmti(cf, 13), e_m1=fmti(em1, 8), e_m1over4=fmti(em14, 8),
    reads='strictly_between_e^-1_and_1_and_below_e^-kappa')
# kappa = 0: every poly evaluates to its count sum
one = (L.ONE, L.ONE)
r0 = div(ev(best[0], one), ev(((4, 6),), one))
row('C19_variant_ratio_kappa0', r0 == (L.ONE, L.ONE), ratio=fmti(r0, 6))
# the unfaulted C10 ratio e^{-4k} and the pinned fault ratio 1
r_unf = div(ev(((4, 6),), E), ev(((8, 6),), E))
r_flt = div(ev(((4, 6),), E), ev(((4, 6),), E))
row('C10_ratios', r_unf[0] <= em1[1] and em1[0] <= r_unf[1] and r_flt[0] <= L.ONE <= r_flt[1], unfaulted=fmti(r_unf, 12), pinned_fault=fmti(r_flt, 6))
print('NUM_N4_END|fails=' + str(len(FAILS)) + '|' + ','.join(FAILS) + '|json=0')
