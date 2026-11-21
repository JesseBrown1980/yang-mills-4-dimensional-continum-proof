"""Independent exact rational physical SU2 Wilson 42-band weight tests."""
from math import gcd
import unittest

import ym4_su2_wilson_42band_positive_weight as S
from ym4_su2_wilson_local_transfer import R
from ym4_su2_neutral_42_band import physical_neutral_band
from ym4_su2_first_centre_energy_order import original_first_sector_energy_bounds
from ym4_wilson_vacuum_trace_bridge import vacuum_wilson_intervals


class OriginalSU2Physical42BandWeightTests(unittest.TestCase):
    def test_uniform_envelope_independently_as_python_integers(self):
        # Independent exact-rational integer-pair kernel with all four
        # operations separately authored, rather than importing producer R.
        def p(n, d=1):
            g=gcd(n,d)
            return (n//g,d//g)
        def add(a,b):
            return p(a[0]*b[1]+b[0]*a[1],a[1]*b[1])
        def neg(a):
            return (-a[0],a[1])
        def sub(a,b):
            return add(a,neg(b))
        def mul(a,b):
            return p(a[0]*b[0],a[1]*b[1])
        def div(a,b):
            return p(a[0]*b[1],a[1]*b[0])
        def fourth(a):
            square=mul(a,a)
            return mul(square,square)
        def greater(a,b):
            return a[0]*b[1]>b[0]*a[1]
        q=p(1,10000)
        y=div(mul(q,q),p(4))
        om=sub(p(1),y)
        b=sub(p(1),mul(p(48),q))
        d=div(sub(p(1),b),b)
        k1upper=div(q,mul(p(4),om))
        e=div(mul(k1upper,k1upper),b)
        D=add(mul(p(6),e),mul(p(3),d))
        C0upper=add(p(1,4),add(mul(p(4),e),mul(p(2),d)))
        half_minus=sub(p(1,2),D)
        ray_coeff=div(mul(fourth(om),mul(half_minus,half_minus)),p(256))
        tail_coeff=div(C0upper,mul(p(576),mul(om,om)))
        numerator=sub(ray_coeff,tail_coeff)
        denom=sub(div(p(1),mul(p(256),fourth(om))),p(1,576))
        self.assertEqual(b,p(622,625))
        self.assertEqual(d,p(3,622))
        self.assertTrue(greater(numerator,p(0)))
        self.assertTrue(greater(denom,p(0)))
        self.assertTrue(greater(div(numerator,denom),p(1,5)))
        w=S.uniformly_frozen_positive_witness()
        self.assertEqual((w["weight_lower"].n,w["weight_lower"].d),
                         div(numerator,denom))

    def test_true_vacuum_rank_one_error_and_variance(self):
        for beta in (R(1,10000),R(1,100000)):
            a=S.physical_vacuum_source_estimates(beta)
            self.assertEqual(a["b"], R(1)-48*beta)
            self.assertEqual(a["d"],(48*beta).div(a["b"]))
            self.assertEqual(a["e"],
                a["electric_excited_norm"].div(a["b"]))
            self.assertEqual(a["D"],6*a["e"]+3*a["d"])
            self.assertEqual(a["C0_upper"],R(1,4)+4*a["e"]+2*a["d"])
            self.assertLess(a["D"],R(1,2))
            self.assertGreater(a["C0_upper"],R(1,4))
            self.assertEqual(a["Haar_W_norm_square"],R(1,4))
            self.assertEqual(a["band"]["band_rank"],42)
            self.assertEqual(a["band"]["neutral_band_source_weight_status"],
                             "OPEN")

    def test_original_physical_band_positive_exact_source(self):
        for beta in (R(1,10000),R(1,100000)):
            a=S.original_physical_wilson_42band_weight(beta)
            c=S.physical_vacuum_source_estimates(beta)
            self.assertEqual(a["rank"],42)
            self.assertGreater(a["weight_lower"],R(1,5))
            self.assertLess(a["weight_lower"],a["source_C0_upper"])
            self.assertEqual(a["source_C0_upper"],c["C0_upper"])
            self.assertEqual(a["one_eigenmode_weight_lower"],
                             a["weight_lower"].div(42))
            self.assertGreater(a["one_eigenmode_weight_lower"],R(1,210))
            self.assertEqual(a["first_neutral_individual_weight"],"OPEN")
            self.assertGreater(a["band_eigenvalue_upper"],
                               a["tail_eigenvalue_upper"])
            self.assertGreater(a["Rayleigh_lower"],
                               a["tail_eigenvalue_upper"]*
                               a["source_C0_upper"])

    def test_two_stronger_frozen_original_su2_couplings(self):
        a=S.original_physical_wilson_42band_weight(R(1,10000))
        b=S.original_physical_wilson_42band_weight(R(1,100000))
        self.assertGreater(a["weight_lower"],R(21,100))
        self.assertGreater(b["weight_lower"],R(24,100))
        self.assertGreater(a["one_eigenmode_weight_lower"],R(1,200))
        self.assertGreater(b["one_eigenmode_weight_lower"],R(1,175))
        self.assertGreater(b["weight_lower"],a["weight_lower"])

    def test_independent_fixed_lattice_original_WV01_parent_source(self):
        # Our new source-bound proof uses its own vacuum perturbation
        # envelope; the earlier original full 4D Wilson positive-vacuum
        # source gives a separately derived sharper C0 interval.
        for beta in (R(1,10000),R(1,100000)):
            a=S.original_physical_wilson_42band_weight(beta)
            v=vacuum_wilson_intervals(beta)
            self.assertLess(v["vacuum_C0_upper"],a["source_C0_upper"])
            self.assertGreater(v["vacuum_C0_lower"],R(0))
            self.assertLess(a["weight_lower"],v["vacuum_C0_upper"])
            self.assertEqual(v["trace"]["nonvacuum_eigenratio_upper"],
                             24*beta)

    def test_physical_first_charged_overlap_stays_zero(self):
        for beta in (R(1,10000),R(1,100000)):
            first=original_first_sector_energy_bounds(beta)
            self.assertEqual(first["local_contractible_Wilson_first_weight"],
                             R(0))
            a=S.original_physical_wilson_42band_weight(beta)
            self.assertGreater(a["one_eigenmode_weight_lower"],R(1,210))
            self.assertEqual(a["first_neutral_individual_weight"],"OPEN")

    def test_independent_diagonal_physical_spectral_fixture(self):
        # Explicit 44-dimensional positive compact fixture:
        # vacuum=one, rank-42 isolated band, one tail. W couples
        # true vacuum to one of the band vectors with amplitude 1/2.
        beta=R(1,10000)
        band=physical_neutral_band(beta)
        spectrum=(R(1),) + (band["band_lower"],)*42 + (
            band["tail_upper"].div(2),)
        self.assertEqual(len(spectrum),44)
        self.assertGreater(spectrum[0],R(1,2))
        self.assertGreater(spectrum[1],spectrum[43])
        source_coeff=(R(0),R(1,2))+(R(0),)*42
        self.assertEqual(len(source_coeff),44)
        weights=tuple(v.power(2) for v in source_coeff)
        self.assertEqual(sum(weights,R(0)),R(1,4))
        self.assertEqual(sum(weights[1:43],R(0)),R(1,4))
        self.assertGreater(sum(weights[1:43],R(0)),R(1,5))

    def test_frozen_predicted_output_and_deterministic_receipt(self):
        result=S.receipt()
        self.assertEqual(result,S.receipt())
        self.assertIn("physical_Wilson_42band_weight_gt=1/5",result)
        self.assertIn("some_individual_neutral_Wilson_eigenmode_weight_gt=1/210",
                      result)
        self.assertIn("source_weight_whole_42band_gt_one_fifth=PASS",result)
        self.assertIn("individual_first_neutral_Wilson_weight=OPEN",result)
        self.assertIn("continuum_mass_gap=OPEN",result)
        self.assertEqual(result.count("YM4_WG05_ORIGINAL|beta="),2)

    def test_invalid_beta_cannot_promote_positive_Wilson_weight(self):
        for beta in (R(0),R(-1),R(1,9999),R(1,1000),R(1,100)):
            with self.assertRaisesRegex(
                    ValueError,"beta_outside_source_weight_window"):
                S.original_physical_wilson_42band_weight(beta)

    def test_rational_floor_output_is_conservative(self):
        r=S.original_physical_wilson_42band_weight(R(1,10000))
        cap=S.floor_scaled(r["weight_lower"],10**12)
        self.assertLessEqual(R(cap,10**12),r["weight_lower"])
        self.assertGreater(R(cap,10**12),R(21,100))


if __name__=="__main__":
    unittest.main()
