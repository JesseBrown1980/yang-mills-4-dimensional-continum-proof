"""Independent original SU2 Wilson centre-charge and projector acceptance."""
from itertools import product
import unittest

import ym4_su2_center_flux_projectors as M
from ym4_4d_wilson_cylinder_moments import (
    sites, positive_links, plaquettes, translate, geometry,
)
from ym4_su2_wilson_local_transfer import R


def quaternion_mul(a, b):
    a0,a1,a2,a3=a
    b0,b1,b2,b3=b
    return (
        a0*b0-a1*b1-a2*b2-a3*b3,
        a0*b1+a1*b0+a2*b3-a3*b2,
        a0*b2-a1*b3+a2*b0+a3*b1,
        a0*b3+a1*b2-a2*b1+a3*b0,
    )


def quaternion_inverse(q):
    return (q[0], -q[1], -q[2], -q[3])


IDENTITY=(R(1),R(0),R(0),R(0))
X=(R(3,5),R(4,5),R(0),R(0))
Y=(R(5,13),R(0),R(12,13),R(0))
Z=(R(0),R(0),R(0),R(1))
QUATS=(IDENTITY,X,Y,Z)


def field_sample():
    return {
        (s,axis):QUATS[(s[0]+2*s[1]+3*s[2]+5*s[3]+axis)%4]
        for s in sites() for axis in range(4)
    }


def gauge_sample():
    return {
        s:QUATS[(3*s[0]+s[1]+2*s[2]+s[3])%4] for s in sites()
    }


def minus_quaternion(q):
    return tuple(-x for x in q)


def centre_field(field, axis):
    return {key:(minus_quaternion(q)
                 if key[1]==axis and key[0][axis]==0 else q)
            for key,q in field.items()}


def gauge_field(field, gauge):
    return {(site,axis):
            quaternion_mul(
                quaternion_mul(gauge[site],value),
                quaternion_inverse(gauge[translate(site,axis)]))
            for (site,axis),value in field.items()}


def word_value(word, field):
    value=IDENTITY
    for s,d,orientation in word:
        q=field[(s,d)]
        value=quaternion_mul(
            value,q if orientation==1 else quaternion_inverse(q))
    return value


class OriginalSU2CentreProjectorTests(unittest.TestCase):
    def test_exact_4D_centre_plaquette_incidence(self):
        p,masks=geometry()
        self.assertEqual(len(p),480)
        self.assertEqual(len(masks),480)
        self.assertEqual(M.original_full_action_centre_checks(),
                         ((40,360,120,0),)*3)
        for axis in range(3):
            self.assertEqual(
                sum(int(l[1]==axis and l[0][axis]==0)
                    for l in positive_links()),40)
            self.assertEqual(
                sum(int(M.flip_count(word,axis)==2)
                    for s,mu,nu,word in p),120)
            self.assertTrue(
                all(M.flip_count(word,axis) in (0,2)
                    for s,mu,nu,word in p))

    def test_centre_group_eight_projectors(self):
        self.assertTrue(M.check_projector_group_algebra())
        self.assertEqual(len(M.CHARGES),8)
        self.assertEqual(len(M.GROUP),8)
        for e in M.CHARGES:
            for f in M.CHARGES:
                s=sum(M.projector_numerator(e,g)*M.character(f,g)
                      for g in M.GROUP)
                self.assertEqual(s,8 if e==f else 0)

    def test_all_original_spatial_source_plaquettes_neutral(self):
        for site,mu,nu,word in plaquettes():
            self.assertEqual(M.word_charge(word),(1,1,1))
        local,winding=M.spatial_source_selection()
        self.assertEqual(M.word_charge(local),(1,1,1))
        self.assertEqual(winding,((-1,1,1),(1,-1,1),(1,1,-1)))

    def test_all_eight_sector_winding_products(self):
        chars=set()
        for bits in M.GROUP:
            e=[]
            for axis in range(3):
                e.append(-1 if bits[axis] else 1)
            e=tuple(e)
            self.assertIn(e,M.CHARGES)
            chars.add(e)
        self.assertEqual(chars,set(M.CHARGES))
        for axis in range(3):
            w=M.winding_word(axis)
            self.assertEqual(len(w),2)
            self.assertEqual(w[0][2],1)
            self.assertEqual(w[1][2],1)
            self.assertEqual(M.flip_count(w,axis),1)

    def test_full_SU2_Wilson_action_exact_rational_centre_symmetry(self):
        field=field_sample()
        p=plaquettes()
        original=tuple(word_value(word,field)[0] for _,_,_,word in p)
        for axis in range(3):
            transformed=centre_field(field,axis)
            self.assertEqual(centre_field(transformed,axis),field)
            self.assertEqual(
                tuple(word_value(word,transformed)[0]
                      for _,_,_,word in p),
                original)
        self.assertEqual(sum(original,R(0)),
                         sum((word_value(w,field)[0]
                              for *_,w in p),R(0)))

    def test_spatial_Wilson_source_and_winding_actual_quaternions(self):
        field={key:IDENTITY for key in positive_links()}
        local=M.spatial_source_selection()[0]
        self.assertEqual(word_value(local,field)[0],R(1))
        for axis in range(3):
            new=centre_field(field,axis)
            self.assertEqual(word_value(local,new)[0],R(1))
            for direction in range(3):
                w=M.winding_word(direction)
                self.assertEqual(word_value(w,field)[0],R(1))
                self.assertEqual(word_value(w,new)[0],
                    R(-1) if direction==axis else R(1))

    def test_original_local_Gauss_and_global_centre_commute(self):
        field=field_sample()
        gauge=gauge_sample()
        for axis in range(3):
            lhs=gauge_field(centre_field(field,axis),gauge)
            rhs=centre_field(gauge_field(field,gauge),axis)
            self.assertEqual(lhs,rhs)
        # Both original Wilson plaquette holonomy traces remain invariant
        # under local SU2 gauge transforms and each global centre action.
        p=plaquettes()
        action_before=sum((word_value(word,field)[0]
                           for *_,word in p),R(0))
        action_after=sum((word_value(word,gauge_field(field,gauge))[0]
                          for *_,word in p),R(0))
        self.assertEqual(action_before,action_after)

    def test_transfer_and_source_selection_scope(self):
        result=M.physical_transfer_selection()
        self.assertEqual(result["sectors"],8)
        self.assertEqual(result["source_charge"],(1,1,1))
        self.assertTrue(result["charged_Wilson_overlap_exact_zero"])
        self.assertEqual(result["first_excited_sector_order"],"OPEN")

    def test_odd_link_support_mutant_rejected(self):
        p=list(plaquettes())
        site,mu,nu,word=p[0]
        # A nonclosed three-edge chain containing one centre-crossing
        # is not the original gauge-invariant Wilson plaquette.
        mutant=word[:3]
        self.assertTrue(any(M.flip_count(mutant,axis)%2
                            for axis in range(3)))
        p[0]=(site,mu,nu,mutant)
        with self.assertRaisesRegex(ValueError,"plaquette_word_length"):
            M.original_full_action_centre_checks(tuple(p))

    def test_wrong_direction_and_group_inputs_rejected(self):
        with self.assertRaisesRegex(ValueError,"invalid_centre_direction"):
            M.selected_link(((0,0,0,0),1),3)
        with self.assertRaisesRegex(ValueError,"invalid_winding_direction"):
            M.winding_word(3)
        with self.assertRaisesRegex(ValueError,"invalid_centre_character"):
            M.character((0,1,1),(0,0,0))
        with self.assertRaisesRegex(ValueError,"invalid_centre_group_element"):
            M.xor3((0,0,0),(2,0,0))
        with self.assertRaisesRegex(ValueError,"invalid_loop_word"):
            M.flip_count([],0)

    def test_hbp_exact_and_no_first_state_promotion(self):
        s=M.receipt()
        self.assertEqual(s,M.receipt())
        self.assertIn("sector_projectors=8",s)
        self.assertIn("all_charged_sectors_local_Wilson_overlap=EXACT_ZERO",s)
        self.assertIn("first_eigenstate_sector_order=OPEN",s)
        self.assertIn("neutral_first_excitation_isolation=OPEN",s)
        self.assertIn("continuum_gap=OPEN",s)


if __name__=="__main__":
    unittest.main()
