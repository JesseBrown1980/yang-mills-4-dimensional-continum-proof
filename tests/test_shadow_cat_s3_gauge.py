#!/usr/bin/env python3
"""Candidate Shadow Cat Z3 holonomy inside S3: explicit gauge-invariance test.

This is a conjugacy test of S3, NOT an identification with the actual user's
full Shadow Cat physical model. Predict before code: be28b595.
All calculations are integer permutation algebra, no binary floating point.
"""
from hashlib import sha256
from itertools import permutations
from pathlib import Path
import sys

SABOTAGES=("claim_signed_label_is_gauge_invariant",
           "claim_trace_distinguishes_orientation",
           "claim_transposition_in_A3",
           "claim_gap_is_proved")
args=sys.argv[1:]
if len(args)>1 or (args and (not args[0].startswith("sabotage=")
                            or args[0][9:] not in SABOTAGES)):
    print("usage: test_shadow_cat_s3_gauge.py [sabotage=NAME]")
    sys.exit(2)
SABOTAGE=args[0][9:] if args else ""
FAIL=[]


def emit(tag,**vals):
    print(tag+"|"+"|".join(str(k)+"="+str(v) for k,v in vals.items())+"|json=0")


def check(name,yes):
    if not yes:
        FAIL.append(name)
        emit("FAILED",check=name)


def compose(a,b):
    return tuple(a[b[i]] for i in range(3))


def inverse(p):
    inv=[0]*3
    for i,j in enumerate(p):
        inv[j]=i
    return tuple(inv)


def conj(g,h):
    return compose(compose(g,h),inverse(g))


def chi(p):
    # Standard representation = 3D permutation representation minus trivial.
    return sum(int(p[i]==i) for i in range(3))-1


def gpower(x,n):
    assert n>=0
    result=(0,1,2)
    while n:
        if n%2:
            result=compose(result,x)
        n//=2
        if n:
            x=compose(x,x)
    return result


def power3(k):
    assert k>=0
    n=1
    for _ in range(k):
        n*=3
    return n


def main():
    root=Path(__file__).resolve().parents[1]
    data=(root/"docs/PREDICTION-YM4-SHADOW-CAT-S3-GAUGE-20261106.hbp").read_bytes()
    predictions=[x for x in data.splitlines() if x.startswith(b"PREDICT|id=")]
    assert len(predictions)==9
    identity=(0,1,2)
    cycle=(1,2,0)
    cycle2=compose(cycle,cycle)
    trans=(1,0,2)
    group=tuple(permutations(range(3)))
    A3=(identity,cycle,cycle2)
    label={identity:0,cycle:1,cycle2:2}
    check("S3_has_six",len(group)==6 and len(A3)==3 and
          len(set(group))==6)
    for g in group:
        for h in A3:
            check("A3_normal_subgroup",conj(g,h) in A3)
    flipped=conj(trans,cycle)
    check("signed_shadow_not_gauge_invariant",
          flipped==cycle2 and label[flipped]!=label[cycle]
          and (SABOTAGE!="claim_signed_label_is_gauge_invariant"
               or label[flipped]==label[cycle]))
    emit("SHADOW_S3_CONJUGATION",gauge_element="TRANS",
         loop_before="C1",loop_after="C2",
         raw_shadow_before=label[cycle],raw_shadow_after=label[flipped],
         signed_label_invariant="NO",
         conjugacy_class_invariant="YES")
    csign=chi(cycle)
    check("standard_character",chi(identity)==2 and chi(trans)==0 and
          chi(cycle)==-1 and chi(cycle2)==-1)
    check("character_cannot_distinguish_shadow_orientation",
          chi(cycle)==chi(cycle2) and
          (SABOTAGE!="claim_trace_distinguishes_orientation"
           or chi(cycle)!=chi(cycle2)))
    check("transposition_not_in_A3",
          trans not in A3 and
          (SABOTAGE!="claim_transposition_in_A3" or trans in A3))
    emit("SHADOW_S3_CHARACTER",chi_identity=chi(identity),
         chi_transposition=chi(trans),chi_cycle=chi(cycle),
         chi_inverse_cycle=chi(cycle2),character_is_gauge_invariant=1,
         orientation_information_lost=1)
    sweep=0
    checksum=sha256()
    # Explicit two-link periodic closed path: gauge transformations at
    # both endpoints must telescope to conjugation at the basepoint.
    for u in group:
        for v in group:
            h=compose(u,v)
            for g0 in group:
                for g1 in group:
                    up=compose(compose(g0,u),inverse(g1))
                    vp=compose(compose(g1,v),inverse(g0))
                    hp=compose(up,vp)
                    good=(hp==conj(g0,h) and
                          chi(hp)==chi(h) and
                          (hp in (cycle,cycle2))==(h in (cycle,cycle2)))
                    check("two_link_gauge_covariance",good)
                    checksum.update(bytes(hp))
                    sweep+=1
    check("complete_s3_two_link_sweep",sweep==1296)
    emit("SHADOW_S3_SWEEP",link_pairs=36,gauge_pairs=36,
         cases=sweep,all_character_checks=1296,
         digest=checksum.hexdigest(),status="PASS")
    for k in (1,2,3,4,8,16):
        n=power3(k)
        jumped=gpower(cycle,n)
        check("C1_order_three_jump",jumped==identity)
        emit("SHADOW_S3_JUMP",k=k,steps=n,cycle_power="IDENTITY",
             raw_signed_label_after_power="0",
             physical_time_evolution="NOT_MODELLED")
    # A permutation-group conjugacy fact is independent of a physical
    # transfer operator spectrum, so no proof of Yang-Mills mass gap.
    check("S3_conjugacy_not_clay_proof",
          SABOTAGE!="claim_gap_is_proved")
    emit("SHADOW_S3_SCOPE",raw_shadow_r="GAUGE_COVARIANT_ONLY",
         class_character="GAUGE_INVARIANT",
         physical_S3_Hamiltonian_first_gap="NOT_COMPUTED",
         SU2_continuum_4D="OPEN",quantum_cloning="NOT_TESTED",
         three_cycle_orientation="NOT_IN_WILSON_TRACE")
    if FAIL:
        emit("SHADOW_S3_VERIFY",status="FAIL",failed=len(FAIL),
             sabotage=SABOTAGE or "NONE",json_zero=1)
        sys.exit(1)
    emit("SHADOW_S3_VERIFY",status="PASS",predictions=9,
         group_elements=6,sweep_cases=sweep,
         signed_shadow_gauge_invariant=0,
         class_wilson_gauge_invariant=1,
         jumps_max=43046721,red_controls="RUN_SEPARATELY",
         Clay_gap="NOT_PROVED",json_zero=1)

if __name__=="__main__":
    main()
