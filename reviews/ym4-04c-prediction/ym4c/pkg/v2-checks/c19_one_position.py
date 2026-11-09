#!/usr/bin/env python3
"""YM4-04C v2 repair lane: C10's line channel and the one_position_support fault, as exact integer counts.

Scale-k lattice (Z/L)^4, L = 8; next-coarse lattice (Z/4)^4. Coarse link (x',mu) = fine links (2x',mu) [position 0]
and (2x'+e_mu,mu) [position 1]. Input: one Y per coarse plaquette P'' = (x',mu<nu), Y = the 8 fine links of the
2x2 loop, R(Y) = s*chi_1/2(loop), sup|R| = 2|s|. Output: R(dP'') = s*chi_1/2(V_P''), sup 2|s|, on the 4 coarse links.
Norm = max_l sum_{Y containing l} e^{kappa #Y} sup|R(Y)|; every Y has one size, so ratio = (count_out/count_in) e^{kappa(#Y_out-#Y_in)}.
"""
from fractions import Fraction as Fr
import itertools
L = 8; Lc = L // 2
def e(mu): return tuple(1 if i == mu else 0 for i in range(4))
def add(x, y): return tuple((a + b) % L for a, b in zip(x, y))
def fine_links_of_coarse(xc, mu):
    x0 = tuple(2 * c for c in xc)
    return [((x0, mu), 0), ((add(x0, e(mu)), mu), 1)]
def coarse_add(x, y): return tuple((a + b) % Lc for a, b in zip(x, y))

objs = []   # (set of (fine link, position)), coarse boundary
for xc in itertools.product(range(Lc), repeat=4):
    for mu, nu in itertools.combinations(range(4), 2):
        cl = [(xc, mu), (coarse_add(xc, e(mu)), nu), (coarse_add(xc, e(nu)), mu), (xc, nu)]
        fl = []
        for (y, d) in cl: fl += fine_links_of_coarse(y, d)
        objs.append((fl, cl))
in_count = {}; out_count = {}
size_all = set(); size_pos1 = set(); held_both = set(); held_one = set()
for fl, cl in objs:
    for (l, pos) in fl: in_count[l] = in_count.get(l, 0) + 1
    for c in cl: out_count[c] = out_count.get(c, 0) + 1
    size_all.add(len(fl)); size_pos1.add(sum(1 for (_, p) in fl if p == 1))
    pos_by_coarse = {}
    for (l, pos), c in zip(fl, [c for c in cl for _ in (0, 1)]):
        pos_by_coarse.setdefault(c, set()).add(pos)
    held_both.add(sum(1 for c in cl if pos_by_coarse[c] == {0, 1}))
    held_one.add(sum(1 for c in cl if len(pos_by_coarse[c]) >= 1))
cin = max(in_count.values()); cout = max(out_count.values())
print(f"objects: {len(objs)} (= 6 x 4^4); fine links in some Y: {len(in_count)} of {4*L**4}; max Y per fine link: {cin}; max P'' per coarse link: {cout}")
print(f"#Y over all links: {sorted(size_all)}; #Y counting position-1 links only: {sorted(size_pos1)}")
print(f"#Y'' (coarse links held at both positions): {sorted(held_both)}; #Y'' (held from at least one position): {sorted(held_one)}")
for kap in (Fr(1, 4), Fr(0)):
    for rule, yin in (("correct #Y=all links", min(size_all)), ("fault #Y=position-1 links", min(size_pos1))):
        for orule, yout in (("Y''=both positions", min(held_both)), ("Y''=one position (draft fault)", min(held_one))):
            ex = kap * (yout - yin)
            print(f"kappa={kap}: {rule}, {orule}: fine norm = {cin*2}|s| e^({kap*yin}), coarse norm = {cout*2}|s| e^({kap*yout}), ratio = ({Fr(cout, cin)}) * e^({ex})")
