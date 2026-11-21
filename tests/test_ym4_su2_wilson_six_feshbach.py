"""Independent exact fourth SU2 Haar and six-state Feshbach acceptance tests."""
from itertools import product
from math import gcd
import unittest

import ym4_su2_wilson_six_feshbach as W
from ym4_su2_wilson_local_transfer import R
from ym4_su2_wilson_first_magnetic_42gram import exact_graph_spectral_certificate
from ym4_su2_wilson_42band_positive_weight import physical_vacuum_source_estimates


def rat(n,d=1):
    """Independent small rational kernel for endpoint scalar inequalities."""
    if d==0:
        raise ValueError("zero_denominator")
    if d<0:
        n,d=-n,-d
    k=gcd(n,d)
    return n//k,d//k


def add(a,b):
    return rat(a[0]*b[1]+a[1]*b[0],a[1]*b[1])


def neg(a):
    return -a[0],a[1]


def sub(a,b):
    return add(a,neg(b))


def mul(a,b):
    return rat(a[0]*b[0],a[1]*b[1])


def div(a,b):
    return rat(a[0]*b[1],a[1]*b[0])


def pow2(a):
    return mul(a,a)


def lt(a,b):
    return a[0]*b[1]<b[0]*a[1]


def independent_24_quaternions():
    # Independent design construction: 8 signed coordinate axes,
    # 16 vertices of the half-coordinate sign cube.
    axis=[]
    for i in range(4):
        v=[0]*4
        v[i]=2
        axis.append(tuple(v))
        v[i]=-2
        axis.append(tuple(v))
    cube=list(product((1,-1),repeat=4))
    return tuple(axis+cube)


def moment(indices):
    points=independent_24_quaternions()
    numerator=0
    for q in points:
        term=1
        for i in indices:
            term*=q[i]
        numerator+=term
    return rat(numerator,24*2**len(indices))


class SU2WilsonSixFeshbachTests(unittest.TestCase):
    def test_true_continuous_SU2_fourth_tensor_design(self):
        p=independent_24_quaternions()
        self.assertEqual(len(p),24)
        self.assertEqual(len(set(p)),24)
        self.assertTrue(W.verify_fourth_Haar_tensor())
        for indices in product(range(4),repeat=4):
            i,j,k,l=indices
            expected=rat(int(i==j and k==l)
                         +int(i==k and j==l)
                         +int(i==l and j==k),24)
            self.assertEqual(moment(indices),expected)
            actual=W.exact_Haar_coordinate_monomial(indices)
            self.assertEqual((actual.n,actual.d),expected)
        self.assertEqual(moment((0,0,0,0)),rat(1,8))
        self.assertEqual(moment((0,0,1,1)),rat(1,24))
        self.assertEqual(W.exact_Haar_coordinate_monomial((0,0,0,0))*4,
                         R(1,2))

    def test_Q8_is_not_valid_for_original_fourth_order_Haar(self):
        # Q8 signed axes get E[q0^4]=1/4 rather than Haar=1/8.
        axes=[v for v in independent_24_quaternions()
              if sum(int(x!=0) for x in v)==1]
        self.assertEqual(len(axes),8)
        numerator=sum(v[0]**4 for v in axes)
        self.assertEqual(rat(numerator,8*16),rat(1,4))
        self.assertNotEqual(rat(1,4),moment((0,0,0,0)))
        with self.assertRaisesRegex(ValueError,"invalid_S3_Haar_monomial"):
            W.exact_Haar_coordinate_monomial((4,))

    def test_independent_integer_schur_end_point(self):
        b=rat(1,10000)
        z=mul(rat(24),b)
        e=mul(rat(25),b)
        self.assertTrue(lt(div(z,sub(rat(1),z)),e))
        r=div(rat(288),sub(rat(1),z))
        self.assertTrue(lt(r,rat(289)))
        t=mul(rat(100,99),rat(625))
        correction=add(rat(289),t)
        temp=add(rat(1),mul(rat(100,99),e))
        correction=add(correction,mul(rat(9,10),
                                      mul(rat(625),pow2(temp))))
        self.assertTrue(lt(correction,rat(1500)))
        self.assertTrue(lt(mul(rat(1500),b),rat(1,6)))
        self.assertEqual((W.six_cluster_schur_certificate(R(1,10000))
                          ["Schur_error_coefficient"].n,
                          W.six_cluster_schur_certificate(R(1,10000))
                          ["Schur_error_coefficient"].d),
                         correction)

    def test_complete_electric_tail_ratio_gap(self):
        for den in (10000,100000,1000000,10000000):
            s=W.six_cluster_schur_certificate(R(1,den))
            self.assertLess(s["relative_tail"],R(9,20))
            self.assertLess(s["Schur_error_rel_upper"],
                            R(1,den).div(6))
            self.assertEqual(s["physical_neutral_top_six_rank"],6)
            self.assertEqual(s["physical_neutral_top_six_indices"],
                             (2,3,4,5,6,7))
            self.assertEqual(s["individual_first_eigenstate_weight"],"OPEN")

    def test_all_Schur_blocks_are_required(self):
        beta=R(1,10000)
        s=W.six_cluster_schur_certificate(beta)
        # Demonstrate that the vacuum/tail terms are present and positive:
        eps=25*beta
        vac=R(100,99)*eps.power(2)
        tail=R(9,10)*eps.power(2)*(
            R(1)+R(100,99)*eps).power(2)
        second=289*beta.power(2)
        self.assertGreater(vac,R(0))
        self.assertGreater(tail,R(0))
        self.assertGreater(second,R(0))
        self.assertGreater(s["Schur_error_coefficient"]*beta.power(2),
                           vac+second)
        self.assertLess(s["Schur_error_coefficient"],R(1500))

    def test_first_magnetic_graph_is_exactly_six_positive_modes(self):
        g=exact_graph_spectral_certificate()
        self.assertEqual(len(g["A"]),42)
        self.assertEqual(g["top6_multiplicity"],6)
        self.assertEqual(g["bottom6_multiplicity"],6)
        self.assertEqual(g["zero_multiplicity"],30)
        self.assertEqual(g["source_positive6_weight"],R(1,32))
        self.assertLess(R(1,3).power(2),R(1,8))
        self.assertGreater(R(1,32),R(1,36))

    def test_uniform_six_source_projector_and_true_vacuum(self):
        for den in (1000000,2000000,10000000):
            beta=R(1,den)
            s=W.original_interacting_six_Wilson_weight(beta)
            self.assertEqual(s["rank"],6)
            self.assertEqual(s["weight_lower"],R(9,400))
            self.assertEqual(s["one_true_eigenmode_lower"],R(3,800))
            self.assertEqual(s["projector_distance_upper"],23250*beta)
            self.assertEqual(s["source_distance_upper"],148*beta)
            self.assertGreater(s["norm_lower"],R(3,20))
            self.assertEqual(s["individual_first_neutral_weight"],"OPEN")
            parent=physical_vacuum_source_estimates(beta)
            self.assertLess(parent["D"],148*beta)

    def test_endpoint_source_margin_independent_integer_pair(self):
        beta=rat(1,1000000)
        normlo=sub(rat(1,6),mul(rat(11773),beta))
        self.assertTrue(lt(rat(3,20),normlo))
        self.assertTrue(lt(rat(9,400),pow2(normlo)))
        self.assertEqual(normlo,rat(464681,3000000))
        self.assertTrue(lt(mul(rat(23250),beta),rat(1,20)))

    def test_invalid_parameter_cannot_promote_a_first_neutral_claim(self):
        for beta in (R(0),R(-1),R(1,9999),R(1,100)):
            with self.assertRaisesRegex(ValueError,
                                        "beta_outside_full_six_cluster_window"):
                W.six_cluster_schur_certificate(beta)
        for beta in (R(0),R(1,999999),R(1,10000)):
            with self.assertRaisesRegex(ValueError,
                                        "beta_outside_positive_six_source_window"):
                W.original_interacting_six_Wilson_weight(beta)

    def test_exact_replay_and_status_boundaries(self):
        text=W.receipt()
        self.assertEqual(text,W.receipt())
        for marker in (
            "24_point_Hurwitz_quaternion_fourth_tensor=EXACT",
            "effective_42_Schur_norm_le=1500beta2_times_t",
            "actual_interacting_six_projector=PASS",
            "actual_interacting_six_spectral_weight_gt=9/400",
            "one_eigenmode_of_six_weight_gt=3/800",
            "individual_first_neutral_Wilson_overlap=OPEN",
            "full_42by42_second_derivative_matrix=OPEN",
            "large_volume_weak_coupling_continuum_gap=OPEN",
        ):
            self.assertIn(marker,text)


if __name__=="__main__":
    unittest.main()
