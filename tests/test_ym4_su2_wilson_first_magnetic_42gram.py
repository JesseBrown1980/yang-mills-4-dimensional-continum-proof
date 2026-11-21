"""Independent original SU2 Wilson magnetic 42x42 first-order Gram audit."""
from itertools import combinations, product
from math import isqrt
import unittest

import ym4_su2_wilson_first_magnetic_42gram as M
from ym4_su2_wilson_local_transfer import R
from ym4_su2_wilson_42band_positive_weight import (
    original_physical_wilson_42band_weight,
)


def independent_42_masks():
    """Rebuild original 24 spatial L2 edges and cycles from coordinates."""
    vertices=tuple(product((0,1),repeat=3))
    edges=tuple((v,d) for v in vertices for d in range(3))
    lookup={edge:i for i,edge in enumerate(edges)}
    def flip(v,d):
        vals=list(v)
        vals[d]^=1
        return tuple(vals)
    plaquettes=[]
    for v in vertices:
        for a,b in combinations(range(3),2):
            keys=((v,a),(flip(v,a),b),(flip(v,b),a),(v,b))
            plaquettes.append(sum(1<<lookup[e] for e in keys))
    pair_masks=[]
    for axis in range(3):
        trans=tuple(i for i in range(3) if i!=axis)
        paths=[]
        for bits in product((0,1),repeat=2):
            vertex=[0,0,0]
            for d,bit in zip(trans,bits):
                vertex[d]=bit
            v=tuple(vertex)
            paths.append((1<<lookup[(v,axis)]) |
                         (1<<lookup[(flip(v,axis),axis)]))
        for x,y in combinations(paths,2):
            assert x&y==0
            pair_masks.append(x|y)
    assert len(plaquettes)==24 and len(pair_masks)==18
    return tuple(plaquettes+pair_masks),set(plaquettes)


def independent_adjacency():
    masks,plaq=independent_42_masks()
    return tuple(tuple(int(i!=j and (masks[i]^masks[j]) in plaq)
                       for j in range(42)) for i in range(42))


def independent_components(A):
    unseen=set(range(42))
    result=[]
    while unseen:
        root=min(unseen)
        unseen.remove(root)
        stack=[root]
        for k in stack:
            for j in tuple(sorted(unseen)):
                if A[k][j]:
                    unseen.remove(j)
                    stack.append(j)
        result.append(stack)
    return result


class OriginalWilsonMagneticFirstGramTests(unittest.TestCase):
    def test_original_42_supports_independently_build(self):
        masks,plaq=independent_42_masks()
        self.assertEqual(len(set(masks)),42)
        self.assertEqual(len(plaq),24)
        basis=M.loops_and_masks()
        self.assertEqual(tuple(x[2] for x in basis),masks)
        self.assertEqual([x[0] for x in basis[:24]],["P"]*24)
        self.assertEqual([x[0] for x in basis[24:]],["D"]*18)

    def test_quaternion_quadratic_design_exact_second_Haar_moment(self):
        # 8 signed axis quaternions: mean q_a=0, covariance delta_ab/4.
        values=tuple((s,i) for i in range(4) for s in (-1,1))
        self.assertEqual(len(values),8)
        for d in range(4):
            self.assertEqual(sum(s if i==d else 0 for s,i in values),0)
            for e in range(4):
                numerator=sum((s if i==d else 0)*
                              (s if i==e else 0) for s,i in values)
                self.assertEqual(R(numerator,8),R(1,4) if d==e else R(0))
        for v in values:
            self.assertEqual(M.q_mul(v,M.q_inverse(v)),(1,0))
            self.assertEqual(M.q_mul(M.q_inverse(v),v),(1,0))
        # The normalized Haar on the unit S3 quaternion sphere has
        # exactly these coordinate moments, so the cubature is exact
        # for every polynomial with per-link coordinate degree <=2.

    def test_independent_first_magnetic_graph_and_source_block(self):
        expected=independent_adjacency()
        self.assertEqual(expected,M.original_first_magnetic_matrix())
        self.assertEqual(sum(sum(row) for row in expected)//2,48)
        comps=independent_components(expected)
        self.assertEqual(sorted(len(c) for c in comps),[1]*6+[6]*6)
        for comp in comps:
            if len(comp)==6:
                left=[i for i in comp if i<24]
                right=[i for i in comp if i>=24]
                self.assertEqual((len(left),len(right)),(4,2))
                self.assertEqual(sum(expected[a][b]
                                     for a in left for b in right),8)
            else:
                self.assertTrue(comp[0]>=24)
        self.assertEqual(sum(expected[0]),2)

    def test_all_48_original_SU2_Haar_couplings_exact_one_eighth(self):
        basis=M.loops_and_masks()
        plaq={x[2]:x for x in basis[:24]}
        checked=0
        for i,j in combinations(range(42),2):
            diff=basis[i][2]^basis[j][2]
            if diff in plaq:
                actual=M.exact_Haar_triple(basis[i],basis[j],plaq[diff])
                self.assertEqual(actual,R(1,8))
                checked+=1
        self.assertEqual(checked,48)
        # A single unallowed swap, or all diagonal triples, must be
        # exactly zero by independent per-link SU2 central parity.
        self.assertEqual(M.exact_Haar_triple(basis[0],basis[0],basis[0]),R(0))
        self.assertEqual(M.exact_Haar_triple(basis[0],basis[1],basis[0]),R(0))

    def test_matrix_cubic_identity_and_sixfold_top_degeneracy(self):
        g=M.exact_graph_spectral_certificate()
        A=g["A"]
        A2=tuple(tuple(sum(A[i][k]*A[k][j] for k in range(42))
                       for j in range(42)) for i in range(42))
        self.assertEqual(sum(A2[i][i] for i in range(42)),96)
        self.assertEqual(isqrt(8)**2,4)
        self.assertEqual(g["top6_multiplicity"],6)
        self.assertEqual(g["bottom6_multiplicity"],6)
        self.assertEqual(g["zero_multiplicity"],30)
        self.assertEqual(g["source_positive6_weight"],R(1,32))
        for i in range(42):
            for j in range(42):
                self.assertEqual(sum(A2[i][k]*A[k][j]
                                     for k in range(42)),8*A[i][j])
        # Squared projection onto +/- six-mode space at source:
        # ||P_pair e0||² = (A²)_00/8 = 1/4; bipartite symmetry splits
        # equally, yielding 1/8 for unit phi0 and 1/32 for W=phi0/2.
        self.assertEqual(R(A2[0][0],8),R(1,4))

    def test_actual_vacuum_Wilson_moments_positive_with_correct_scale(self):
        for den in (10000,100000):
            beta=R(1,den)
            s=original_physical_wilson_42band_weight(beta)
            self.assertGreater(s["weight_lower"],R(1,5))
            for even_time in (2,4):
                expected=R(1,5*(500*den**4)**even_time)
                got=M.true_original_Wilson_moment_lower(beta,even_time)
                self.assertEqual(got,expected)
                self.assertGreater(got,R(0))

    def test_wrong_beta_moment_is_not_promoted(self):
        with self.assertRaisesRegex(ValueError,"beta_outside_source_weight_window"):
            M.true_original_Wilson_moment_lower(R(1,1000),2)
        with self.assertRaisesRegex(ValueError,"moment_requires_original_even_time"):
            M.true_original_Wilson_moment_lower(R(1,10000),3)

    def test_negative_quaternion_controls(self):
        with self.assertRaisesRegex(ValueError,"invalid_exact_quaternion_element"):
            M.q_mul((1,5),(1,0))
        with self.assertRaisesRegex(ValueError,"invalid_quaternion_inverse_argument"):
            M.q_inverse((2,0))

    def test_deterministic_hbp_and_no_first_mode_promotion(self):
        a=M.receipt()
        self.assertEqual(a,M.receipt())
        for t in ("components_K4_2=6","exact_each_nonzero_Mij=1/8",
                  "first_magnetic_order_top6_cluster_weight=1/32",
                  "original_normalized_Wilson_C2_C4_lower=POSITIVE",
                  "true_interacting_top6_Feshbach_projector=OPEN",
                  "first_neutral_eigenvalue_Wilson_weight=OPEN"):
            self.assertIn(t,a)


if __name__=="__main__":
    unittest.main()
