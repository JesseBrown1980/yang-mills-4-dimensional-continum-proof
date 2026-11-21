"""Independent exact rational controls of physical SU2 transfer trace bridge."""
import unittest

import ym4_wilson_vacuum_trace_bridge as V
import ym4_su2_wilson_local_transfer as W
import ym4_4d_wilson_cylinder_moments as C

R = W.R


class SU2VacuumTraceBridgeTests(unittest.TestCase):
    def test_full_physical_source_gate(self):
        self.assertTrue(V.match_original_source())
        h = C.source_haar_data()
        self.assertEqual((h["sites"], h["links"], h["plaquettes"]),
                         (80, 320, 480))
        self.assertEqual(h["spatial"], h["timelike"])
        self.assertEqual(V.SPATIAL_LINKS, 3*8)
        self.assertEqual(V.SPATIAL_PLAQUETTES, 3*8)

    def test_wrong_physical_counts_rejected(self):
        with self.assertRaisesRegex(ValueError, "wrong_physical_spatial_link_count"):
            V.match_original_source(23)
        with self.assertRaisesRegex(ValueError, "wrong_magnetic_plaquette_count"):
            V.match_original_source(24, 23)
        with self.assertRaisesRegex(ValueError, "wrong_periodic_trace_circumference"):
            V.match_original_source(24, 24, 8)

    def test_single_link_HS_character_multiplicity(self):
        for beta in (R(1, 10000), R(1, 100000)):
            certified = V.single_link_hilbert_schmidt_bound(beta)
            self.assertGreater(certified, R(1))
            partial_lower = R(1)
            for r in range(1, 9):
                lo, hi = W.character_eigen_interval(r, beta, last_k=6)
                d = r+1
                partial_lower += d*d*lo.power(2)
            self.assertLess(partial_lower, certified)
            # The regular L2(SU2) matrix-coefficient multiplicity
            # of fundamental spin-1/2 is 2^2=4, rather than 2.
            lo, hi = W.character_eigen_interval(1, beta)
            self.assertEqual(4*lo.power(2), 2*(2*lo.power(2)))
            self.assertNotEqual(4*lo.power(2), 2*lo.power(2))

    def test_positive_Wilson_trace_operator_enclosure(self):
        for beta, Ecap in ((R(1, 10000), R(1, 100)),
                           (R(1, 100000), R(1, 1000))):
            v = V.physical_transfer_trace_data(beta)
            self.assertEqual(v["vacuum_lambda0_lower"], R(1)-48*beta)
            self.assertEqual(v["nonvacuum_eigenratio_upper"], 24*beta)
            self.assertEqual(v["full_unprojected_HS"],
                             v["one_link_HS"].power(24))
            self.assertEqual(v["normalized_physical_trace2_upper"],
                v["full_unprojected_HS"].div((R(1)-48*beta).power(2)))
            self.assertEqual(v["excited_normalized_trace2_upper"],
                             v["normalized_physical_trace2_upper"]-R(1))
            self.assertLess(v["excited_normalized_trace2_upper"], Ecap)

    def test_trace_tail_falls_by_each_power(self):
        for beta in (R(1, 10000), R(1, 100000)):
            t = V.physical_transfer_trace_data(beta)
            q = 24*beta
            self.assertEqual(V.excited_trace_power_bound(t, 2),
                             t["excited_normalized_trace2_upper"])
            for k in range(3, 13):
                self.assertEqual(
                    V.excited_trace_power_bound(t, k),
                    V.excited_trace_power_bound(t, k-1)*q)

    def test_validated_vacuum_source_bounds(self):
        for beta, c0_cap, n_cap in (
            (R(1, 10000), R(1, 10000), R(1, 50000)),
            (R(1, 100000), R(1, 10000000), R(1, 50000000)),
        ):
            output = V.vacuum_wilson_intervals(beta)
            periodic = C.bounded_connected(beta)
            self.assertEqual(output["vacuum_C0_lower"],
                periodic["C0lo"]-output["errors"][0])
            self.assertEqual(output["vacuum_C0_upper"],
                periodic["C0hi"]+output["errors"][0])
            self.assertEqual(output["vacuum_C2_lower"], R(0))
            self.assertEqual(output["vacuum_C4_lower"], R(0))
            self.assertEqual(output["vacuum_C2_upper"],
                periodic["Ct_abs"]+output["errors"][2])
            self.assertEqual(output["vacuum_C4_upper"],
                periodic["Ct_abs"]+output["errors"][4])
            self.assertGreater(output["vacuum_C0_lower"], R(1,4)-c0_cap)
            self.assertLess(output["vacuum_C0_upper"], R(1,4)+c0_cap)
            self.assertLess(output["vacuum_C2_upper"], n_cap)
            self.assertLess(output["vacuum_C4_upper"], n_cap)

    def test_frozen_trace_error_gates(self):
        a = V.vacuum_wilson_intervals(R(1, 10000))
        self.assertLess(a["errors"][0], R(1, 100000000000000000000))
        self.assertLess(a["errors"][4], R(1, 1000000000000))
        b = V.vacuum_wilson_intervals(R(1, 100000))
        self.assertLess(b["errors"][0], R(1, 100000000000000000000000000000))
        self.assertLess(b["errors"][4], R(1, 100000000000000000))

    def test_time_window_and_beta_violations_rejected(self):
        a = V.physical_transfer_trace_data(R(1, 10000))
        with self.assertRaisesRegex(ValueError, "trace_power_requires_at_least_two"):
            V.excited_trace_power_bound(a, 1)
        with self.assertRaisesRegex(ValueError, "insufficient_time_for_trace_tail"):
            V.thermal_to_vacuum_connected_error(a, 9)
        with self.assertRaisesRegex(ValueError, "wrong_periodic_trace_circumference"):
            V.thermal_to_vacuum_connected_error(a, 4, circumference=8)
        with self.assertRaisesRegex(ValueError, "physical_trace_bound_outside_beta_range"):
            V.physical_transfer_trace_data(R(1, 24))
        with self.assertRaisesRegex(ValueError, "invalid_Wilson_beta"):
            V.single_link_hilbert_schmidt_bound(R(-1))

    def test_generic_trace_comparison_on_small_positive_spectrum(self):
        # Construct an unrelated 3-eigenvalue positive trace-class example,
        # to independently challenge the trace-to-vacuum inequality itself.
        a, b = R(1, 6), R(1, 9)
        eigen = (R(1), a, b)
        op = ((R(1, 2), R(1, 8), R(0)),
              (R(1, 8), R(1, 4), R(0)),
              (R(0), R(0), R(-1, 3)))
        # Max absolute row sum <= 5/8, hence operator norm <= 1.
        self.assertLessEqual(sum((abs_rat(x) for x in op[0]),R(0)),R(1))
        Tcirc, separation = 10, 4
        z = sum((v.power(Tcirc) for v in eigen), R(0))
        thermal_mean = (sum((eigen[i].power(Tcirc)*op[i][i]
                             for i in range(3)), R(0))).div(z)
        raw_pair = R(0)
        for i in range(3):
            for j in range(3):
                raw_pair += (eigen[i].power(Tcirc-separation)
                             *eigen[j].power(separation)*op[i][j]*op[j][i])
        raw_pair = raw_pair.div(z)
        connected_thermal = raw_pair-thermal_mean.power(2)
        m_vac = op[0][0]
        raw_vac = sum((op[0][j]*eigen[j].power(separation)*op[j][0]
                       for j in range(3)), R(0))
        connected_vac = raw_vac-m_vac.power(2)
        e = a.power(2)+b.power(2)
        q = a
        delta_n = e*q.power(Tcirc-separation-2)
        delta_T = e*q.power(Tcirc-2)
        error_bound = delta_n+5*delta_T
        self.assertLessEqual(abs_rat(connected_thermal-connected_vac),
                             error_bound)
        self.assertGreaterEqual(connected_vac, R(0))

    def test_second_order_parent_source_is_unmodified(self):
        s = C.receipt()
        self.assertIn("E_W2A2=481/16", s)
        self.assertIn("E_W0WtA2=1/8", s)
        self.assertIn("infinite_time_vacuum_moments=OPEN", s)
        # New output carries the vacuum trace correction.
        h = V.receipt()
        self.assertIn("original_4D_fixed_lattice_vacuum_Wilson_C0_C2_C4", h)
        self.assertIn("thermal_to_vacuum_control=PASS", h)
        self.assertIn("first_excited_Wilson_overlap=OPEN", h)
        self.assertEqual(h, V.receipt())


def abs_rat(r):
    return r if r >= R(0) else -r


if __name__ == "__main__":
    unittest.main()
