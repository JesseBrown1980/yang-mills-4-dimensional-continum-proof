"""Independent 24-link original SU2 neutral 42-band falsification tests."""
from itertools import combinations, product
import unittest

import ym4_su2_neutral_42_band as W
from ym4_su2_wilson_local_transfer import R, character_eigen_interval
from ym4_su2_first_centre_energy_order import original_spatial_links


def independent_spatial_graph():
    """Build all 24 original 3D links without producer geometry helpers."""
    return tuple((site, direction)
                 for site in product((0, 1), repeat=3)
                 for direction in (0, 1, 2))


def independent_endpoints(link):
    s, direction = link
    t = list(s)
    t[direction] ^= 1
    return s, tuple(t)


def independent_neutral_four_supports():
    edges = independent_spatial_graph()
    valid = []
    neutral = set()
    charged = []
    degree_four = 0
    count = 0
    for ids in combinations(range(24), 4):
        count += 1
        degrees = {v: 0 for v in product((0, 1), repeat=3)}
        for i in ids:
            a, b = independent_endpoints(edges[i])
            degrees[a] += 1
            degrees[b] += 1
        if any(v % 2 for v in degrees.values()):
            continue
        charge = tuple(
            -1 if sum(int(edges[i][1] == direction and
                          edges[i][0][direction] == 0)
                      for i in ids) % 2 else 1
            for direction in (0, 1, 2))
        valid.append((ids, charge))
        if 4 in degrees.values():
            degree_four += 1
        if charge == (1, 1, 1):
            neutral.add(frozenset(edges[i] for i in ids))
            assert 4 not in degrees.values()
        else:
            charged.append(charge)
    return count, valid, neutral, charged, degree_four


class NeutralSU2BandTests(unittest.TestCase):
    def test_independent_24_links_10626_four_subsets_and_42_neutral(self):
        count, valid, neutral, charged, deg4 = independent_neutral_four_supports()
        self.assertEqual(len(original_spatial_links()), 24)
        self.assertEqual(len(independent_spatial_graph()), 24)
        self.assertEqual(count, 10626)
        self.assertEqual(len(valid), 162)
        self.assertEqual(len(neutral), 42)
        self.assertEqual(len(charged), 120)
        self.assertEqual(deg4, 24)
        self.assertEqual(charged.count((-1, 1, 1)), 16)
        self.assertEqual(charged.count((1, -1, 1)), 16)
        self.assertEqual(charged.count((1, 1, -1)), 16)
        self.assertEqual(charged.count((-1, -1, 1)), 24)
        self.assertEqual(charged.count((-1, 1, -1)), 24)
        self.assertEqual(charged.count((1, -1, -1)), 24)
        self.assertEqual(charged.count((-1, -1, -1)), 0)

    def test_producer_neutral_basis_equals_independent_cycle_supports(self):
        basis = W.canonical_neutral_basis_supports()
        links = independent_spatial_graph()
        mapped = { (tuple(list(site) + [0]), direction): i
                   for i, (site, direction) in enumerate(links)}
        expected = set()
        for support in independent_neutral_four_supports()[2]:
            mask = sum(1 << mapped[(tuple(list(s) + [0]), d)]
                       for s, d in support)
            expected.add(mask)
        self.assertEqual(set(basis["neutral"]), expected)
        self.assertEqual(len(basis["plaquettes"]), 24)
        self.assertEqual(len(basis["double_winding"]), 18)
        self.assertEqual(set(basis["plaquettes"]) |
                         set(basis["double_winding"]), expected)
        self.assertEqual(basis["source_Haar_norm_square"], R(1,4))
        self.assertIn(basis["source_mask"], basis["plaquettes"])

    def test_nontrivial_three_edge_gauge_singlet_is_impossible(self):
        edges = independent_spatial_graph()
        admissible = 0
        for triple in combinations(edges, 3):
            degrees = {}
            for edge in triple:
                a, b = independent_endpoints(edge)
                degrees[a] = degrees.get(a, 0) + 1
                degrees[b] = degrees.get(b, 0) + 1
            if all(deg >= 2 for deg in degrees.values()):
                admissible += 1
        self.assertEqual(admissible, 0)
        self.assertEqual(W.check_no_three_link_physical_singlet(),
                         {"candidates":2024,"min_degree_two":0})

    def test_full_SU2_irrep_tail_no_cutoff(self):
        for beta in (R(1,100),R(1,1000),R(1,10000),R(1,100000)):
            s = W.neutral_tail_character_envelope(beta)
            self.assertLess(s["kappa2_upper"],
                            s["kappa1_lower"].power(2))
            self.assertLess(s["kappa1_upper"].power(5),
                            s["kappa2_upper"].power(2))
            self.assertLess(s["electric_neutral_tail_upper"],
                            beta.power(4).div(550))
            for irrep in range(1,13):
                lo,hi=character_eigen_interval(irrep,beta,last_k=8)
                if irrep==1:
                    self.assertGreaterEqual(lo,s["kappa1_lower"])
                    self.assertLessEqual(hi,s["kappa1_upper"])
                else:
                    self.assertLess(hi,s["kappa2_upper"])

    def test_all_42_original_magnetic_band_bounded(self):
        for beta in (R(1,100),R(1,200),R(1,1000),
                     R(1,10000),R(1,100000)):
            s=W.physical_neutral_band(beta)
            self.assertEqual(s["band_rank"],42)
            self.assertEqual(s["electric_plaquette_rank"],24)
            self.assertEqual(s["electric_double_winding_rank"],18)
            self.assertGreater(s["neutral_vacuum_lower"],R(1,2))
            self.assertGreater(s["band_lower"],beta.power(4).div(500))
            self.assertLess(s["tail_upper"],beta.power(4).div(550))
            self.assertGreater(s["band_lower"],s["tail_upper"])
            self.assertEqual(s["physical_interacting_band_projector_rank"],42)
            self.assertEqual(s["neutral_band_source_weight_status"],"OPEN")

    def test_frozen_original_beta_denominators(self):
        for den in (100,10000,100000):
            s=W.physical_neutral_band(R(1,den))
            self.assertEqual(s["frozen_band_lower"],R(1,500*den**4))
            self.assertEqual(s["frozen_tail_upper"],R(1,550*den**4))
            self.assertEqual(s["frozen_band_lower"]-
                             s["frozen_tail_upper"],R(1,5500*den**4))

    def test_Peter_Weyl_basis_contains_source_but_no_physical_overlap_claim(self):
        s=W.canonical_neutral_basis_supports()
        self.assertEqual(s["source_Haar_norm_square"],R(1,4))
        self.assertIn(s["source_mask"],s["neutral"])
        p=W.physical_neutral_band(R(1,10000))
        self.assertEqual(p["neutral_band_source_weight_status"],"OPEN")
        self.assertTrue(p["physical_interacting_band_projector_rank"]==42)

    def test_replay_and_scope_controls(self):
        s=W.receipt()
        self.assertEqual(s,W.receipt())
        self.assertIn("neutral_electric_Wilson_band_rank=42",s)
        self.assertIn("42_dimensional_neutral_projector=EXACT_BY_MINMAX",s)
        self.assertIn("physical_band_Wilson_overlap=OPEN",s)
        self.assertIn("continuum_mass_gap=OPEN",s)
        self.assertIn("beta=1/10000|42_eigenvalues_band_gt=1/5000000000000000000",s)

    def test_bad_source_inputs_falsify(self):
        for beta in (R(0),R(-1),R(1,99),R(1,2)):
            with self.assertRaisesRegex(ValueError,
                "beta_outside_first_sector_ordering_window"):
                W.physical_neutral_band(beta)
        original=W.original_spatial_links()[0]
        with self.assertRaisesRegex(ValueError,
            "duplicate_original_spatial_link"):
            W.support_mask((original,original),W.spatial_link_lookup())
        with self.assertRaisesRegex(ValueError,
            "link_outside_original_spatial_source"):
            W.support_mask((((2,0,0,0),0),),W.spatial_link_lookup())

    def test_diagonal_minmax_fixture_with_42_dimensional_band(self):
        beta=R(1,10000)
        s=W.physical_neutral_band(beta)
        k=s["band_lower"]
        t=s["tail_upper"]
        # Two independent diagonal positive examples between b*K and K:
        # vacuum, 42 band eigenvalues and two smaller neutral values.
        for multiplier in (R(1),s["magnetic_floor"]):
            eigen=(multiplier,)+(multiplier*k,)*42+(multiplier*t,)*2
            self.assertEqual(len(eigen),45)
            self.assertGreater(eigen[0],R(1,2))
            self.assertGreater(eigen[1],eigen[43])
            self.assertGreater(eigen[42],eigen[43])
            self.assertLess(eigen[43],beta.power(4).div(550))

if __name__=="__main__":
    unittest.main()
