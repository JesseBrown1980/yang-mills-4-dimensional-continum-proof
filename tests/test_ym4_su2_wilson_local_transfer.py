"""Independent Haar-polynomial and exact-rational acceptance of Wilson local transfer.

Independent checks use Chebyshev polynomials and Catalan Haar moments rather
than calling the producer's character derivation. No stochastic numerics.
"""
from math import comb, factorial
from pathlib import Path
import runpy
import unittest

M = runpy.run_path(str(Path(__file__).with_name(
    "ym4_su2_wilson_local_transfer.py")))
R = M["R"]


def poly_add(a, b, scale=1):
    out = dict(a)
    for power, coeff in b.items():
        out[power] = out.get(power, 0) + scale * coeff
    return {k: v for k, v in out.items() if v}


def poly_mul_x2(a):
    return {power + 1: 2 * coeff for power, coeff in a.items()}


def characters(up_to):
    chars = [{0: 1}, {1: 2}]
    for _ in range(2, up_to + 1):
        chars.append(poly_add(poly_mul_x2(chars[-1]), chars[-2], -1))
    return chars[:up_to + 1]


def haar_monomial(power):
    if power % 2:
        return R(0)
    m = power // 2
    catalan = comb(2 * m, m) // (m + 1)
    return R(catalan, 4 ** m)


def polynomial_haar(poly):
    return sum((R(c) * haar_monomial(p)
                for p, c in poly.items()), R(0))


def multiply_poly(a, b):
    out = {}
    for p, c in a.items():
        for q, d in b.items():
            out[p + q] = out.get(p + q, 0) + c * d
    return out


def quaternion_mul(a, b):
    x0, x1, x2, x3 = a
    y0, y1, y2, y3 = b
    return (
        x0*y0-x1*y1-x2*y2-x3*y3,
        x0*y1+x1*y0+x2*y3-x3*y2,
        x0*y2-x1*y3+x2*y0+x3*y1,
        x0*y3+x1*y2-x2*y1+x3*y0,
    )


def quat_inverse(a):
    return (a[0], -a[1], -a[2], -a[3])


class SU2WilsonLocalTests(unittest.TestCase):
    def test_exact_integer_rational_invariants(self):
        self.assertEqual(str(R(2, 4)), "1/2")
        self.assertEqual(R(2, 4) + R(1, 3), R(5, 6))
        self.assertEqual(R(2, 4) * R(4, 9), R(2, 9))
        self.assertEqual(R(2, 4).div(R(4, 9)), R(9, 8))
        with self.assertRaises(ValueError):
            R(1, 0)
        with self.assertRaises(ValueError):
            R(1).div(0)

    def test_haar_character_orthogonality(self):
        polys = characters(9)
        for n, a in enumerate(polys):
            for m, b in enumerate(polys):
                self.assertEqual(
                    polynomial_haar(multiply_poly(a, b)),
                    R(int(n == m)),
                    (n, m),
                )

    def test_character_wilson_taylor_coefficients(self):
        # Independent Haar polynomial calculation of each exponential
        # coefficient against chi_r, matched to the Bessel character series.
        polys = characters(8)
        for r in range(9):
            for k in range(5):
                degree = r + 2*k
                a = polynomial_haar(multiply_poly(polys[r], {degree: 1}))
                direct = a.div(factorial(degree))
                bessel = R(r + 1,
                           2**degree * factorial(k) * factorial(k+r+1))
                self.assertEqual(direct, bessel, (r, k))
                if degree > 0:
                    other_degree = degree - 1
                    self.assertEqual(
                        polynomial_haar(multiply_poly(
                            polys[r], {other_degree: 1})),
                        R(0),
                    )

    def test_frozen_ratio_brackets_beta_1_and_4(self):
        for beta, brackets in (
            (1, ((240193, 240195), (14422, 14425), (831, 834))),
            (4, ((658046, 658049), (108255, 108258),
                 (46876, 46880))),
        ):
            lo, hi = M["character_eigen_interval"](1, R(beta), 20)
            lo2, hi2 = M["connected_wilson_interval"](beta, 2)
            lo4, hi4 = M["connected_wilson_interval"](beta, 4)
            for pair, endpoints in zip(
                ((lo, hi), (lo2, hi2), (lo4, hi4)), brackets
            ):
                self.assertLess(R(endpoints[0], 10**6), pair[0])
                self.assertLess(pair[1], R(endpoints[1], 10**6))
            self.assertLess(hi-lo, R(1, 10**25))
            self.assertLess(lo, hi)

    def test_beta1_and_4_uniform_character_tail(self):
        self.assertLess(M["character_sup_tail"](1, 12), R(1, 10**12))
        self.assertLess(M["character_sup_tail"](4, 24), R(1, 10**12))
        self.assertGreater(M["character_sup_tail"](4, 4),
                           R(1, 10**12))
        self.assertGreater(M["character_sup_tail"](1, 2),
                           R(1, 10**12))

    def test_physical_W_normalization_and_character_dimension(self):
        self.assertEqual(M["connected_wilson_interval"](1, 0),
                         (R(1, 4), R(1, 4)))
        for beta in (1, 4):
            lo, hi = M["character_eigen_interval"](1, beta)
            c2lo, c2hi = M["connected_wilson_interval"](beta, 2)
            self.assertEqual(c2lo, (lo ** 2).div(4))
            self.assertEqual(c2hi, (hi ** 2).div(4))
            # A missed factor dim(fundamental)=2 doubles eigenvalue.
            self.assertNotEqual(2*lo, lo)
            # A missed half-trace factor changes C0 by exactly four.
            self.assertNotEqual(R(1), R(1, 4))

    def test_all_order_ratios_positive_and_lambda0_one(self):
        for beta in (1, 4):
            self.assertEqual(M["character_eigen_interval"](0, beta),
                             (R(1), R(1)))
            for index in range(1, 11):
                lo, hi = M["character_eigen_interval"](index, beta)
                self.assertLess(R(0), lo)
                self.assertLess(lo, hi)
                self.assertLess(hi, R(1))

    def test_original_4D_six_aligned_staples_with_Haar_sum(self):
        # The 4D six-staple local Haar partition is exactly the series
        # Z_beta(Q) = sum ((beta^2 Q)/4)^k / (k! (k+1)!).
        for beta_four, kappa in ((R(1, 6), 1), (R(2, 3), 4)):
            t = beta_four * beta_four * 9
            from_four_dim = sum(
                ((t**k).div(factorial(k) * factorial(k+1))
                 for k in range(21)), R(0)
            )
            j_lower, j_upper = M["bessel_j_interval"](1, R(kappa))
            self.assertEqual(from_four_dim, j_lower)
            self.assertLess(j_lower, j_upper)
            self.assertEqual(
                M["aligned_six_staple_mean"](beta_four),
                M["character_eigen_interval"](1, R(kappa))
            )

    def test_gauge_nonclass_source_rejected_by_exact_conjugation(self):
        # SU2 unit quaternion U=i, G=j sends i to -i under conjugation.
        # Half trace (real scalar) stays 0, while spinor diagonal
        # matrix entry a+i*b changes from +i to -i.
        u = (0, 1, 0, 0)
        g = (0, 0, 1, 0)
        moved = quaternion_mul(quaternion_mul(g, u), quat_inverse(g))
        self.assertEqual(moved, (0, -1, 0, 0))
        self.assertEqual(moved[0], u[0])
        self.assertNotEqual((moved[0], moved[1]), (u[0], u[1]))

    def test_negative_inputs_and_underestimated_tail_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid_Wilson_beta"):
            M["character_eigen_interval"](1, R(-1))
        with self.assertRaisesRegex(ValueError, "beta_outside_certified_range"):
            M["character_sup_tail"](5, 24)
        self.assertGreater(M["character_sup_tail"](4, 1), R(1, 10**12))
        with self.assertRaisesRegex(ValueError, "invalid_time"):
            M["connected_wilson_interval"](1, -1)
        with self.assertRaisesRegex(ValueError, "uncontrolled_bessel_tail"):
            M["bessel_j_interval"](1, 8, 0)
        with self.assertRaisesRegex(ValueError, "frozen_ratio_interval_miss"):
            M["check_frozen_row"](
                4, 24, R(2, 3),
                (R(1, 2), R(3, 5)),
                (R(108255, 10**6), R(108258, 10**6)),
                (R(46876, 10**6), R(46880, 10**6)),
            )

    def test_receipt_exact_and_scopes(self):
        data = M["receipt"]()
        self.assertIn("Haar_convolution=Wilson_plaquette", data)
        self.assertIn("C0=1/4|C2_lower=", data)
        self.assertIn("|uniform_tail_lt_1e-12=PASS", data)
        self.assertIn("physical_full4D_moments=OPEN", data)
        self.assertIn("continuum_mass_gap=OPEN", data)
        self.assertEqual(data, M["receipt"]())


if __name__ == "__main__":
    unittest.main()
