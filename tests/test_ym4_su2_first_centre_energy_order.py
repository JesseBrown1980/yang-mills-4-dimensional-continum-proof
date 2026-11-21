"""Independent exact SU2 Peter-Weyl / centre first-state spectral ordering."""
from itertools import combinations, product
import unittest

import ym4_su2_first_centre_energy_order as M
from ym4_su2_wilson_local_transfer import (
    R, character_eigen_interval,
)
from ym4_su2_center_flux_projectors import physical_transfer_selection


def independent_graph():
    """Construct undirected incidence without producer geometry helpers."""
    vertices=tuple(product((0,1),repeat=3))
    links=tuple(((x,y,z),axis)
                for x,y,z in vertices for axis in range(3))
    ends={}
    for start,axis in links:
        tgt=list(start)
        tgt[axis]=(tgt[axis]+1)%2
        ends[(start,axis)]=(start,tuple(tgt))
    good=[]
    for a,b in combinations(links,2):
        degrees={}
        for edge in (a,b):
            u,v=ends[edge]
            degrees[u]=degrees.get(u,0)+1
            degrees[v]=degrees.get(v,0)+1
        if all(n%2==0 for n in degrees.values()):
            good.append((a,b))
    return links, good


def independent_pair_charge(pair):
    return tuple(
        -1 if sum(int(edge[1]==axis and edge[0][axis]==0)
                  for edge in pair)%2 else 1
        for axis in range(3)
    )


class OriginalSU2FirstEnergyOrderingTests(unittest.TestCase):
    def test_independent_24_spatial_edges_and_12_winding_pairs(self):
        links,pairs=independent_graph()
        self.assertEqual(len(links),24)
        self.assertEqual(len(pairs),12)
        self.assertEqual(M.check_fundamental_two_link_support()["pairs"],276)
        self.assertEqual(M.check_fundamental_two_link_support()["admissible"],12)
        charges=tuple(independent_pair_charge(p) for p in pairs)
        self.assertEqual(charges.count((-1,1,1)),4)
        self.assertEqual(charges.count((1,-1,1)),4)
        self.assertEqual(charges.count((1,1,-1)),4)
        self.assertNotIn((1,1,1),charges)

    def test_original_one_link_no_Gauss_invariant_excitation(self):
        for link in M.original_spatial_links():
            a,b=M.endpoints(link)
            self.assertNotEqual(a,b)
            self.assertFalse(M.singleton_fundamental_has_singlet(link))
        with self.assertRaisesRegex(ValueError,"duplicate_spatial_link"):
            link=M.original_spatial_links()[0]
            M.two_fundamental_links_gauge_possible(link,link)

    def test_rational_Wilson_character_bounds_all_sample_couplings(self):
        for beta in (R(1,100),R(1,1000),R(1,10000),R(1,100000)):
            r=M.uniform_character_bounds(beta)
            self.assertGreater(r["low1"],beta.div(5))
            self.assertLess(r["high1"],beta.div(3))
            self.assertLess(r["high_other_representations"],
                            beta.power(2).div(20))
            for index in range(1,9):
                lo,hi=character_eigen_interval(index,beta)
                if index==1:
                    self.assertLess(r["low1"],lo)
                    self.assertLess(hi,r["high1"])
                else:
                    self.assertLess(hi,r["high_other_representations"])

    def test_uniform_beta_interval_energy_order(self):
        for beta in (R(1,100),R(1,200),R(1,1000),
                     R(1,10000),R(1,100000)):
            s=M.original_first_sector_energy_bounds(beta)
            self.assertGreater(s["magnetic_floor"],R(0))
            self.assertGreaterEqual(s["magnetic_floor"],R(13,25))
            self.assertEqual(s["charged_lower"],R(13,625)*beta.power(2))
            self.assertEqual(s["neutral_upper"],beta.power(3).div(27))
            self.assertGreater(s["charged_lower"],s["neutral_upper"])
            self.assertGreater(s["ratio_lower"],R(56))
            self.assertTrue(s["physical_first_eigenspace_centre_charged"])
            self.assertEqual(s["local_contractible_Wilson_first_weight"],R(0))

    def test_exact_frozen_beta_values(self):
        a=M.original_first_sector_energy_bounds(R(1,10000))
        self.assertEqual(a["charged_lower"],R(13,62500000000))
        self.assertEqual(a["neutral_upper"],R(1,27000000000000))
        b=M.original_first_sector_energy_bounds(R(1,100000))
        self.assertEqual(b["charged_lower"],R(13,6250000000000))
        self.assertEqual(b["neutral_upper"],R(1,27000000000000000))

    def test_original_full_centre_and_Gauss_source_binding(self):
        s=physical_transfer_selection()
        self.assertEqual(s["sectors"],8)
        self.assertEqual(s["source_charge"],(1,1,1))
        self.assertTrue(s["charged_Wilson_overlap_exact_zero"])
        self.assertEqual(s["first_excited_sector_order"],"OPEN")
        # WG03 proves the order by the independent electric-operator
        # comparison; WG02 alone proves only centre-charge selection.
        actual=M.original_first_sector_energy_bounds(R(1,10000))
        self.assertTrue(actual["physical_first_eigenspace_centre_charged"])

    def test_exact_three_level_minmax_sanity_example(self):
        beta=R(1,10000)
        a=M.original_first_sector_energy_bounds(beta)
        # A diagonal positive electric operator with 1 vacuum,
        # a charged two-fundamental winding, and a neutral excitation.
        electric=(R(1),beta.power(2).div(25),beta.power(3).div(27))
        magnetic=(a["magnetic_floor"],a["magnetic_floor"],R(1))
        transfer=tuple(x*y for x,y in zip(electric,magnetic))
        self.assertGreater(transfer[0],transfer[1])
        self.assertGreater(transfer[1],transfer[2])
        self.assertGreater(transfer[1],a["neutral_upper"])

    def test_centre_neutral_two_fundamental_sabotage(self):
        links,pairs=independent_graph()
        for pair in pairs:
            self.assertNotEqual(independent_pair_charge(pair),(1,1,1))
        # A purported neutral pair uses two edges at distinct endpoints.
        fake=(links[0],links[1])
        self.assertFalse(M.two_fundamental_links_gauge_possible(
            ((fake[0][0][0],fake[0][0][1],fake[0][0][2],0),fake[0][1]),
            ((fake[1][0][0],fake[1][0][1],fake[1][0][2],0),fake[1][1])))

    def test_invalid_beta_and_wrong_graph_inputs_rejected(self):
        for beta in (R(0),R(-1),R(1,99),R(1,2)):
            with self.assertRaisesRegex(ValueError,
                                        "beta_outside_first_sector_ordering_window"):
                M.uniform_character_bounds(beta)
        with self.assertRaisesRegex(ValueError,"invalid_original_spatial_edge"):
            M.endpoints(((0,0,0,0),3))

    def test_receipt_reproducible_and_quantitative(self):
        text=M.receipt()
        self.assertEqual(text,M.receipt())
        self.assertIn("two_link_Gauss_admissible_winding_pairs=12",text)
        self.assertIn("lambda_charged_lower_gt=13/62500000000",text)
        self.assertIn("lambda_neutral_second_upper_lt=1/27000000000000",text)
        self.assertIn("EXACT_ZERO_FOR_ALL_BETA_LE_1OVER100",text)
        self.assertIn("centre_neutral_first_visible_mode=OPEN",text)
        self.assertIn("continuum_gap=OPEN",text)


if __name__=="__main__":
    unittest.main()
