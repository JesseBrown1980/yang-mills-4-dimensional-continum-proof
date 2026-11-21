"""Independent exact original 48-spatial-symmetry SU2 rank-one Wilson audit."""
from itertools import permutations, product
from math import gcd
import unittest

import ym4_su2_wilson_symmetric_rankone as W
from ym4_su2_wilson_local_transfer import R
from ym4_su2_wilson_first_magnetic_42gram import (
    loops_and_masks, exact_graph_spectral_certificate,
)
from ym4_su2_wilson_six_feshbach import original_interacting_six_Wilson_weight


def independent_original_edges():
    return tuple((tuple(v)+(0,),d)
                 for v in product((0,1),repeat=3) for d in range(3))


def independent_action(shift, perm):
    edges=independent_original_edges()
    lookup={edge:i for i,edge in enumerate(edges)}
    basis=loops_and_masks()
    mask_to_idx={row[2]:i for i,row in enumerate(basis)}
    mapping=[]
    for row in basis:
        mask=0
        for i,(v,axis) in enumerate(edges):
            if row[2]&(1<<i):
                newcoord=tuple(v[perm[j]]^shift[j] for j in range(3))+(0,)
                newaxis=perm.index(axis)
                mask|=1<<lookup[(newcoord,newaxis)]
        mapping.append(mask_to_idx[mask])
    return tuple(mapping)


def gcd_fraction(n,d):
    k=gcd(n,d)
    return (n//k,d//k)


class SymmetricPhysicalWilsonRankOneTests(unittest.TestCase):
    def test_independent_all_48_original_SU2_spatial_permutations(self):
        group=tuple((shift,perm)
                    for perm in permutations((0,1,2))
                    for shift in product((0,1),repeat=3))
        self.assertEqual(len(group),48)
        actions=set(independent_action(shift,perm) for shift,perm in group)
        self.assertEqual(len(actions),48)
        self.assertEqual(actions,set(W.exact_42_space_spatial_action()))
        for action in actions:
            self.assertEqual(set(action),set(range(42)))

    def test_full_original_magnetic_42_network_equivariance(self):
        A=exact_graph_spectral_certificate()["A"]
        for shift in product((0,1),repeat=3):
            for perm in permutations((0,1,2)):
                g=independent_action(shift,perm)
                for i in range(42):
                    for j in range(42):
                        self.assertEqual(A[i][j],A[g[i]][g[j]])

    def test_six_positive_slope_blocks_form_one_transitive_orbit(self):
        A=exact_graph_spectral_certificate()["A"]
        unseen=set(range(42))
        components=[]
        while unseen:
            start=min(unseen)
            unseen.remove(start)
            queue=[start]
            for i in queue:
                for j in tuple(unseen):
                    if A[i][j]:
                        unseen.remove(j)
                        queue.append(j)
            components.append(tuple(queue))
        blocks=[c for c in components if len(c)==6]
        self.assertEqual(len(blocks),6)
        self.assertEqual(len([c for c in components if len(c)==1]),6)
        block_by_vertex={i:j for j,b in enumerate(blocks) for i in b}
        orbit={block_by_vertex[g[0]]
               for g in W.exact_42_space_spatial_action()}
        self.assertEqual(len(orbit),6)

    def test_original_Wilson_24_plaquette_orbit_uniform(self):
        actions=W.exact_42_space_spatial_action()
        multiplicities=[sum(int(g[0]==j) for g in actions)
                        for j in range(42)]
        self.assertEqual(multiplicities[:24],[2]*24)
        self.assertEqual(multiplicities[24:],[0]*18)
        self.assertEqual(len(actions),48)

    def test_independent_exact_symmetric_positive_slope_source(self):
        A=exact_graph_spectral_certificate()["A"]
        # The G-average of local W=phi0/2 is sum(phi_p)/48.
        # For a plaquette-only vector the odd-A term vanishes, so
        # Pplus=(A²+sqrt8 A)/16 yields an exact rational norm:
        # sum_{plaquette p,q} (A²)_pq / (48²*16).
        tally=0
        for i in range(24):
            for j in range(24):
                tally+=sum(A[i][k]*A[k][j] for k in range(42))
        self.assertEqual(tally,192)
        self.assertEqual(gcd_fraction(tally,48*48*16),(1,192))
        expected=W.original_symmetric_six_electric_source()
        self.assertEqual(expected["positive_slope_symmetric_rank"],1)
        self.assertEqual(expected["positive_slope_symmetric_weight"],R(1,192))
        self.assertEqual(expected["A2_source_numerator"],768)
        self.assertEqual(expected["source_orbit_count"],24)

    def test_actual_true_physical_rank_one_and_positive_source(self):
        for den in (1000000,10000000):
            beta=R(1,den)
            parent=original_interacting_six_Wilson_weight(beta)
            s=W.actual_full_physical_symmetric_eigenmode(beta)
            self.assertEqual(s["physical_symmetric_eigenmode_rank"],1)
            self.assertEqual(s["physical_neutral_band_rank"],6)
            self.assertEqual(s["individual_symmetric_mode_Wilson_weight_lower"],
                             R(1,289))
            self.assertGreater(s["norm_lower"],R(1,17))
            self.assertLess(parent["projector_distance_upper"],R(1))
            self.assertEqual(s["energy_position_among_neutral_2_to_7"],"OPEN")
            self.assertEqual(s["individual_first_neutral_eigenvalue_weight"],
                             "OPEN")

    def test_independent_positive_endpoint_inequality(self):
        # Direct integer numerator cross-check:
        # at beta=1e-6, 1/14 -11773 beta >1/17
        b=R(1,1000000)
        a=R(1,14)-11773*b
        self.assertEqual(a,R(1,14)-R(11773,1000000))
        self.assertGreater(a,R(1,17))
        self.assertGreater(a.power(2),R(1,289))
        self.assertGreater(R(1,192),R(1,196))
        self.assertLess(23250*b,R(1))

    def test_negative_beta_and_source_promotion(self):
        for beta in (R(0),R(-1),R(1,999999),R(1,10000)):
            with self.assertRaisesRegex(ValueError,
                "beta_outside_symmetric_rankone_source_window"):
                W.actual_full_physical_symmetric_eigenmode(beta)
        with self.assertRaisesRegex(ValueError,"invalid_original_spatial_link"):
            W.spatial_link_image(((0,0,0,0),3),
                                 ((0,0,0),(0,1,2)))

    def test_canonical_receipt_and_precise_scope(self):
        text=W.receipt()
        self.assertEqual(text,W.receipt())
        for marker in (
            "original_spatial_group_order=48",
            "fully_spatial_symmetric_slope_rank=1",
            "symmetric_first_slope_weight=1/192",
            "physical_six_symmetric_invariant_rank=1",
            "one_actual_SU2_physical_neutral_eigenvector=ISOLATED_BY_SYMMETRY",
            "single_symmetric_physical_eigenvector_weight_gt=1/289",
            "individual_first_neutral_energy_order=OPEN",
            "large_volume_weak_coupling_continuum_gap=OPEN"
        ):
            self.assertIn(marker,text)


if __name__=="__main__":
    unittest.main()
