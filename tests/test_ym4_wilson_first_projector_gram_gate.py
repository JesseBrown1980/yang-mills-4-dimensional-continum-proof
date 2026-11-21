"""Independent exact source, Gram positivity and projector isolation falsifiers."""
import unittest

import ym4_wilson_first_projector_gram_gate as G
from ym4_su2_wilson_local_transfer import R
from ym4_wilson_vacuum_trace_bridge import vacuum_wilson_intervals
from ym4_4d_wilson_cylinder_moments import ceil_scaled


class WilsonProjectorGramTests(unittest.TestCase):
    def test_full_physical_original_source(self):
        for beta in (R(1, 10000), R(1, 100000)):
            s = G.sharpen_physical_source(beta)
            parent = vacuum_wilson_intervals(beta)
            self.assertEqual(s["q"], 24 * beta)
            self.assertEqual(s["C0_lower"], parent["vacuum_C0_lower"])
            self.assertEqual(s["C0_upper"], parent["vacuum_C0_upper"])
            self.assertGreater(s["C0_lower"], R(0))
            self.assertEqual(parent["trace"]["nonvacuum_eigenratio_upper"],
                             s["q"])
            self.assertEqual(s["C2_upper"], s["q"].power(2)*s["C0_upper"])
            self.assertEqual(s["C4_upper"], s["q"].power(4)*s["C0_upper"])

    def test_frozen_new_scaled_upper_intervals(self):
        expected = (
            (R(1,10000), R(3,1250), 1440139406097, 8295202979114),
            (R(1,100000), R(3,12500), 14400001334, 829440077),
        )
        for beta,q,c2,c4 in expected:
            s = G.sharpen_physical_source(beta)
            self.assertEqual(q,s["q"])
            self.assertEqual(ceil_scaled(s["C2_upper"],10**18),c2)
            self.assertEqual(ceil_scaled(s["C4_upper"],10**24),c4)
            # The original preimplementation targets are conservative ceilings.
            self.assertLessEqual(c2, 1440139406101 if beta == R(1,10000) else 14400001334)
            self.assertLessEqual(c4, 8295202979139 if beta == R(1,10000) else 829440077)
            self.assertLess(s["C4_upper"],s["old_C4_upper"])
            self.assertLess(s["C2_upper"],s["old_C2_upper"])

    def test_independent_even_Gram_variance_inequality(self):
        # For a positive measure, G_even=[[C0,C2],[C2,C4]]
        # is the Gram of {u,R^2u}. Independently compute its determinant.
        for beta in (R(1,10000),R(1,100000)):
            pair = G.adversarial_spectral_pair(beta)
            c0,c2,c4=pair["even_moments"]
            q=24*beta
            self.assertEqual(c0,R(1,4))
            self.assertEqual(c2,R(61,1728)*q.power(2))
            self.assertEqual(c4,R(1633,248832)*q.power(4))
            self.assertEqual(c0*c4-c2.power(2),
                             R(589,1492992)*q.power(4))
            self.assertGreater(c0*c4-c2.power(2),R(0))
            self.assertLessEqual(c2,q.power(2)*c0)
            self.assertLessEqual(c4,q.power(2)*c2)

    def test_pair_same_moments_but_different_first_weight(self):
        for beta in (R(1,10000),R(1,100000)):
            pair=G.adversarial_spectral_pair(beta)
            self.assertEqual(pair["weights_no_first"][0],R(0))
            self.assertEqual(pair["weights_with_first"][0],R(21,4000))
            self.assertEqual(
                tuple(G.moment_power(pair["values"],
                                     pair["weights_no_first"],n)
                      for n in (0,2,4)),
                tuple(G.moment_power(pair["values"],
                                     pair["weights_with_first"],n)
                      for n in (0,2,4)))
            self.assertEqual(len(pair["values"]),4)
            self.assertGreater(pair["values"][0],pair["values"][1])
            self.assertGreater(pair["values"][1],pair["values"][2])
            self.assertGreater(pair["values"][2],pair["values"][3])

    def test_positive_source_can_have_first_eigenstate_zero_weight(self):
        beta=R(1,10000)
        pair=G.adversarial_spectral_pair(beta)
        self.assertGreater(pair["even_moments"][0],R(0))
        self.assertGreater(pair["even_moments"][1],R(0))
        self.assertGreater(pair["even_moments"][2],R(0))
        self.assertEqual(pair["first_weight_no"],R(0))
        self.assertEqual(pair["first_weight_yes"],R(21,4000))
        self.assertGreater(pair["first_weight_yes"],R(0))

    def test_both_fixture_spectra_respect_full_trace(self):
        for beta in (R(1,10000),R(1,100000)):
            pair=G.adversarial_spectral_pair(beta)
            actual=sum((t.power(2) for t in pair["values"]),R(0))
            original=vacuum_wilson_intervals(beta)
            self.assertEqual(actual,pair["trace2"])
            self.assertLess(actual, original["trace"]["excited_normalized_trace2_upper"])
            self.assertLess(pair["values"][0], 24*beta)

    def test_conditional_exact_isolation_fixture(self):
        for beta in (R(1,10000),R(1,100000)):
            v=G.independently_checked_isolation_fixture(beta)
            self.assertEqual(v["C0"],R(1,4))
            self.assertEqual(v["C2"],R(5,64)*(24*beta).power(2))
            self.assertEqual(v["lower"],R(1,20))
            self.assertLess(v["lower"],R(1,8))

    def test_denominator_and_ordering_falsifiers(self):
        with self.assertRaisesRegex(ValueError,"unordered_spectral_isolation"):
            G.isolated_first_weight_dual(R(1,4),R(0),R(1,2),R(1,2))
        with self.assertRaisesRegex(ValueError,"unordered_spectral_isolation"):
            G.isolated_first_weight_dual(R(1,4),R(0),R(1,4),R(1,2))
        with self.assertRaisesRegex(ValueError,"invalid_physical_source_intervals"):
            G.isolated_first_weight_dual(R(0),R(0),R(1,2),R(1,4))
        with self.assertRaisesRegex(ValueError,"invalid_physical_source_intervals"):
            G.isolated_first_weight_dual(R(1,4),R(-1),R(1,2),R(1,4))
        with self.assertRaisesRegex(ValueError,"infeasible_isolated_first_data"):
            G.isolated_first_weight_dual(R(1,4),R(1),R(1,2),R(1,4))

    def test_held_original_even_if_hypothetical_isolation_supplied(self):
        for beta in (R(1,10000),R(1,100000)):
            label,lower=G.original_first_projector_gate(beta)
            self.assertEqual(label,"HOLD")
            self.assertEqual(lower,R(0))
            original=vacuum_wilson_intervals(beta)
            # Numerical lower is zero: no positive first-weight dual
            # even if one were to posit a spectral gap without evidence.
            self.assertEqual(original["vacuum_C2_lower"], R(0))

    def test_spectral_falsifier_negative_inputs(self):
        with self.assertRaisesRegex(ValueError,"beta_not_in_frozen_original_source"):
            G.q_for_beta(R(1,100))
        with self.assertRaisesRegex(ValueError,"invalid_moment_order"):
            G.moment_power((R(1,2),),(R(1),),-2)
        with self.assertRaisesRegex(ValueError,"negative_spectral_weight"):
            G.moment_power((R(1,2),),(R(-1),),2)
        with self.assertRaisesRegex(ValueError,"invalid_excited_spectrum"):
            G.moment_power((R(1),),(R(1),),2)
        with self.assertRaisesRegex(ValueError,"invalid_spectral_measure_shape"):
            G.moment_power((R(1,2),),(R(1),R(0)),2)

    def test_point_mass_and_cauchy_controls(self):
        t=R(1,7)
        vals=(t,)
        masses=(R(1,4),)
        c0=G.moment_power(vals,masses,0)
        c2=G.moment_power(vals,masses,2)
        c4=G.moment_power(vals,masses,4)
        self.assertEqual(c0*c4,c2.power(2))
        self.assertEqual(c0,R(1,4))
        self.assertEqual(c2,R(1,196))
        self.assertEqual(c4,R(1,9604))

    def test_strict_positive_source_injective_transfer_requires_more_than_two_moments(self):
        # When T is positive injective, ||T u||^2=C2>0 if u!=0.
        # The original proof uses the exact positive Wilson transfer
        # and C0_lower>0, but has no effective numerical C2 lower.
        s=G.sharpen_physical_source(R(1,10000))
        self.assertTrue(s["strict_C2_positive"])
        self.assertTrue(s["strict_C4_positive"])
        self.assertEqual(s["C2_lower"],R(0))
        self.assertEqual(s["C4_lower"],R(0))

    def test_replay_and_explicit_status(self):
        x=G.receipt()
        self.assertEqual(x,G.receipt())
        self.assertIn("C4_upper_1e24=8295202979139",x)
        self.assertIn("C4_upper_1e24=829440077",x)
        self.assertIn("same_C0_C2_C4=PASS",x)
        self.assertIn("first_eigenprojector=HOLD",x)
        self.assertIn("first_excited_Wilson_weight=HOLD",x)
        self.assertIn("continuum_uniform_mass_gap=OPEN",x)


if __name__=="__main__":
    unittest.main()
