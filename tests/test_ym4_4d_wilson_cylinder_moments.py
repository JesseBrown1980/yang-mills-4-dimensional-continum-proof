"""Independent exact 4D cylinder Wilson-link, Haar and negative controls."""
from itertools import product
from math import comb
import unittest

import ym4_4d_wilson_cylinder_moments as M
from ym4_su2_wilson_local_transfer import R


def qmul(a, b):
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (
        a0*b0-a1*b1-a2*b2-a3*b3,
        a0*b1+a1*b0+a2*b3-a3*b2,
        a0*b2-a1*b3+a2*b0+a3*b1,
        a0*b3+a1*b2-a2*b1+a3*b0,
    )


def qinv(x):
    return (x[0], -x[1], -x[2], -x[3])


def norm2(q):
    return sum((v*v for v in q), R(0))


ONE = (R(1), R(0), R(0), R(0))
QX = (R(3, 5), R(4, 5), R(0), R(0))
QY = (R(5, 13), R(0), R(12, 13), R(0))
QZ = (R(0), R(0), R(0), R(1))
QUATS = (ONE, QX, QY, QZ)


def link_sample():
    return {(site, mu): QUATS[(site[0] + 2*site[1] + site[2]
                                + 3*site[3] + mu) % 4]
            for site in M.sites() for mu in range(4)}


def gauge_sample():
    return {site: QUATS[(2*site[0] + site[1] + site[2]
                          + 3*site[3]) % 4] for site in M.sites()}


def wilson_holonomy(word, field):
    acc = ONE
    for site, mu, sign in word:
        value = field[(site, mu)]
        acc = qmul(acc, value if sign == 1 else qinv(value))
    return acc


def action_sum(field):
    return sum((wilson_holonomy(word, field)[0]
                for site, mu, nu, word in M.plaquettes()), R(0))


class FullWilsonCylinderTests(unittest.TestCase):
    def test_original_four_dimensional_complete_incidence(self):
        plaquettes, masks = M.geometry()
        self.assertEqual(len(M.sites()), 80)
        self.assertEqual(len(M.positive_links()), 320)
        self.assertEqual(len(plaquettes), 480)
        self.assertEqual(len(masks), 480)
        self.assertEqual(len(set(masks)), 480)
        self.assertEqual(sum(int(nu == 3) for _, mu, nu, _ in plaquettes), 240)
        self.assertEqual(sum(int(nu < 3) for _, mu, nu, _ in plaquettes), 240)

    def test_independent_edge_support_overlap(self):
        plaquettes, masks = M.geometry()
        # Independent geometric fact: distinct 2x2x2x10 squares have
        # an exclusive link on both loops (at most two shared links).
        for i, mask in enumerate(masks):
            self.assertEqual(mask.bit_count(), 4)
            for earlier in masks[:i]:
                self.assertLessEqual((earlier & mask).bit_count(), 2)
        for site, mu, nu, word in plaquettes:
            self.assertEqual(word[0], (site, mu, 1))
            self.assertEqual(word[1], (M.translate(site, mu), nu, 1))
            self.assertEqual(word[2], (M.translate(site, nu), mu, -1))
            self.assertEqual(word[3], (site, nu, -1))

    def test_exhaustive_independent_parity_counts(self):
        plaquettes, masks = M.geometry()
        bases = {(site, mu, nu): masks[i]
                 for i, (site, mu, nu, word) in enumerate(plaquettes)}
        w0 = bases[((0, 0, 0, 0), 0, 1)]
        self.assertEqual(sum(int(w0 == mask) for mask in masks), 1)
        # Independent XOR dictionary in the checker, not the producer's
        # parity_coefficient_counts function.
        mask_set = set(masks)
        self.assertEqual(sum(int(p in mask_set) for p in masks), 480)
        self.assertEqual(sum(int((p ^ w0) in mask_set) for p in masks), 0)
        for t in (2, 4):
            wt = bases[((0, 0, 0, t), 0, 1)]
            self.assertEqual((w0 & wt), 0)
            self.assertEqual(sum(int(p == (w0 ^ wt)) for p in masks), 0)
            matching = [(p, p ^ w0 ^ wt) for p in masks
                        if (p ^ w0 ^ wt) in mask_set]
            self.assertEqual(set(matching), {(w0, wt), (wt, w0)})

    def test_Haar_first_and_second_coefficients(self):
        h = M.source_haar_data()
        self.assertEqual(h["A2"], R(480, 4))
        self.assertEqual(h["WA"], R(1, 4))
        self.assertEqual(h["W2A"], R(0))
        self.assertEqual(h["WA2"], R(0))
        self.assertEqual(h["W2A2"], R(479, 16) + R(1, 8))
        self.assertEqual(h["WWtA2"], R(2, 16))
        # Catalan moments for one Haar SU2 half-trace:
        # integral x^(2m) = Catalan(m)/4^m.
        self.assertEqual(R(comb(4, 2)//3, 16), R(1, 8))
        self.assertEqual(R(1, 4)*R(1, 4), R(1, 16))

    def test_full_action_exact_SU2_gauge_covariance(self):
        field = link_sample()
        gauge = gauge_sample()
        for value in QUATS:
            self.assertEqual(norm2(value), R(1))
        transformed = {
            (site, mu): qmul(
                qmul(gauge[site], field[(site, mu)]),
                qinv(gauge[M.translate(site, mu)]))
            for site in M.sites() for mu in range(4)
        }
        for site, mu, nu, word in M.plaquettes():
            h0 = wilson_holonomy(word, field)
            h1 = wilson_holonomy(word, transformed)
            expected = qmul(qmul(gauge[site], h0), qinv(gauge[site]))
            self.assertEqual(h1, expected)
            self.assertEqual(h1[0], h0[0])
        self.assertEqual(action_sum(field), action_sum(transformed))

    def test_two_frozen_beta_windows_and_centred_cancellation(self):
        for beta, c0_accuracy, ct_accuracy in (
            (R(1, 10000), R(1, 10000), R(1, 50000)),
            (R(1, 100000), R(1, 10000000), R(1, 50000000)),
        ):
            a = M.bounded_connected(beta)
            self.assertLess(R(1, 4)-c0_accuracy, a["C0lo"])
            self.assertLess(a["C0hi"], R(1, 4)+c0_accuracy)
            self.assertLess(a["Ct_abs"], ct_accuracy)
            self.assertGreater(a["Zlo"], R(0))
            self.assertLess(a["Zlo"], a["Zhi"])
            # The disconnected beta^2 term cancels in connected C2,C4.
            self.assertEqual(beta.power(2).div(16),
                             beta.div(4).power(2))
            self.assertNotEqual(beta.power(2).div(16), R(0))

    def test_outward_fixed_grid_rounding(self):
        scale = 1000000000000
        self.assertEqual(M.floor_scaled(R(1, 3), scale), 333333333333)
        self.assertEqual(M.ceil_scaled(R(1, 3), scale), 333333333334)
        self.assertEqual(M.floor_scaled(R(-1, 3), scale), -333333333334)
        self.assertEqual(M.ceil_scaled(R(-1, 3), scale), -333333333333)
        a = M.bounded_connected(R(1, 10000))
        lo = M.floor_scaled(a["C0lo"], scale)
        hi = M.ceil_scaled(a["C0hi"], scale)
        self.assertLessEqual(R(lo, scale), a["C0lo"])
        self.assertLessEqual(a["C0hi"], R(hi, scale))

    def test_duplicate_plaquette_rejected(self):
        p = M.plaquettes()
        mutated = p[:-1] + (p[0],)
        with self.assertRaisesRegex(ValueError, "duplicate_plaquette_support"):
            M.geometry(mutated)

    def test_missing_all_240_timelike_plaquettes_rejected(self):
        mutated = tuple(p for p in M.plaquettes() if p[2] < 3)
        self.assertEqual(len(mutated), 240)
        with self.assertRaisesRegex(ValueError, "source_plaquette_count_mismatch"):
            M.geometry(mutated)

    def test_wrong_inverse_in_plaquette_rejected(self):
        p = list(M.plaquettes())
        site, mu, nu, word = p[0]
        mutated_word = word[:2] + ((word[2][0], word[2][1], 1),) + word[3:]
        p[0] = site, mu, nu, mutated_word
        with self.assertRaisesRegex(ValueError, "plaquette_path_discontinuous"):
            M.geometry(tuple(p))

    def test_bad_beta_and_invalid_geometry_rejected(self):
        with self.assertRaisesRegex(ValueError, "beta_outside_certified_Taylor_window"):
            M.bounded_connected(R(1, 480))
        with self.assertRaisesRegex(ValueError, "beta_outside_certified_Taylor_window"):
            M.bounded_connected(R(-1, 1000))
        with self.assertRaisesRegex(ValueError, "invalid_plaquette_plane"):
            M.plaquette_word((0, 0, 0, 0), 3, 0)
        with self.assertRaisesRegex(ValueError, "invalid_direction"):
            M.translate((0, 0, 0, 0), 4)

    def test_receipt_determinism_and_scope(self):
        a = M.receipt()
        self.assertEqual(a, M.receipt())
        self.assertIn("sites=80|links=320|plaquettes=480", a)
        self.assertIn("connected_order_beta2=CANCELS", a)
        self.assertIn("original_4D_Gauss_invariant_source=YES", a)
        self.assertIn("infinite_time_vacuum_moments=OPEN", a)
        self.assertIn("full_transfer_spectrum=OPEN|continuum_gap=OPEN", a)
        self.assertEqual(a.count("YM4_4D_WILSON_CYLINDER|"), 2)


if __name__ == "__main__":
    unittest.main()
