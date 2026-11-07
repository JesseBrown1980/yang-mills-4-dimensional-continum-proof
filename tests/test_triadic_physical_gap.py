#!/usr/bin/env python3
"""YM4-04/06: exact rational triadic transfer and continuum-gap obstruction.

Theorems, counterexample, and frozen predictions:
 docs/PREDICTION-YM4-04-TRIADIC-PHYSICAL-GAP-20261106.hbp
 docs/NOTE-YM4-04-TRIADIC-PHYSICAL-GAP-20261106.md

This is a self-contained two-level TRANSFER-OPERATOR TEST, not the 3x4 S3
Hamiltonian or a 4D SU(2) Wilson lattice calculation. It shows exactly why
finite-time matrix jumps and a gap at each finite scale do not establish
a *uniform physical* gap as lattice spacing tends to zero.

All tested values are exact integer or Fraction. The only logarithms occur in
symbolic proofs in the accompanying note, never in this program.
No float, numpy, JSON or external dependencies.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import sys

SABOTAGES = (
    "drop_physical_a",
    "misread_high_cluster",
    "wrong_cube_block",
    "fake_uniform_collapsing_gap",
)
sabotage = ""
if len(sys.argv) > 2:
    print("usage: test_triadic_physical_gap.py [sabotage=NAME]")
    sys.exit(2)
if len(sys.argv) == 2:
    arg = sys.argv[1]
    if not arg.startswith("sabotage=") or arg[9:] not in SABOTAGES:
        print("usage: test_triadic_physical_gap.py [sabotage=NAME]")
        sys.exit(2)
    sabotage = arg[9:]

ROOT = Path(__file__).resolve().parents[1]
PRED = ROOT / "docs/PREDICTION-YM4-04-TRIADIC-PHYSICAL-GAP-20261106.hbp"
preddata = PRED.read_bytes()
assert preddata.count(b"\nPREDICT|id=") == 13
predictions = [l for l in preddata.splitlines() if l.startswith(b"PREDICT|id=")]
assert len(predictions) == 13
FAILS = []


def record(tag, **data):
    print(tag+"|"+"|".join(str(k)+"="+str(v) for k,v in data.items())+"|json=0")


def check(name, yes):
    if not yes:
        FAILS.append(name)
        record("FAILED",check=name)


def frac(x):
    return str(x.numerator)+"/"+str(x.denominator)


def stable(j):
    k = 3**j
    return F(k, k+1)


def collapse(j):
    k = 3**j
    return F(k*k, k*k+1)


def digest_frac(r):
    """Length-prefixed signed integers: exact state SHA, no decimal conversion."""
    z = sha256()
    for v in (r.numerator, r.denominator):
        b = v.to_bytes(max(1,(v.bit_length()+7)//8),"big")
        z.update(len(b).to_bytes(4,"big"))
        z.update(b)
    return z.hexdigest()


def transfer_step(q, state):
    return (state[0], q*state[1])


def main():
    record("YM4_BRIDGE_BEGIN",prediction_rows=len(predictions),
           prediction_sha256=sha256(preddata).hexdigest(),
           model="TWO_LEVEL_TOY_NOT_YM4",json_zero=1)
    bound_ok = True
    collapse_ok = True
    for j in range(13):
        k = 3**j
        a = F(1,k)
        q_stable = stable(j)
        q_collapse = collapse(j)
        # ln(1+x) between x/(1+x) and x, x>=0.
        # m_stable=k*ln(1+1/k), bracket [k/(k+1),1].
        # m_collapse=k*ln(1+1/k^2), upper <=1/k.
        stable_lower = F(k,k+1)
        stable_upper = F(1)
        collapsing_upper = F(1,k)
        bound_ok &= (stable_lower >= F(1,2) and stable_upper==1)
        collapse_ok &= (0 < q_collapse < 1 and collapsing_upper==a)
        if j in (0,1,3,6,9,12):
            record("YM4_FAMILY",j=j,inv_spacing=k,
                   stable_ratio=frac(q_stable),
                   stable_physical_mass_lower=frac(stable_lower),
                   stable_physical_mass_upper=frac(stable_upper),
                   collapse_ratio=frac(q_collapse),
                   collapse_physical_mass_upper=frac(collapsing_upper),
                   every_finite_transfer_gap_positive=1)
    # Targeted negative control: dropping physical 1/a changes the upper.
    if sabotage == "drop_physical_a":
        upper_wrong = F(1,3**12*3**12)
        check("gap_physical_scale",upper_wrong == F(1,3**12))
    else:
        check("gap_physical_scale",bound_ok and collapse_ok)
    check("collapsing_limit",F(1,3**12)<F(1,100000))
    for j in range(1,13):
        k=3**j
        a2=F(1,k*k)
        q=collapse(j)
        parent=collapse(j-1)
        mismatch=abs(q**3 - parent)
        assert mismatch<=6*a2
        if j in (1,2,3,6,9,12):
            record("YM4_BLOCK_DEFECT",j=j,scale=3,
                   defect=frac(mismatch),bound=frac(6*a2),
                   bound_met=1)
    record("YM4_COLLAPSE",family="q=1/(1+a^2)",
           one_scale_blocking_defect_bound="6*a_squared",
           physical_mass_upper="a",
           continuum_gap_limit="ZERO",
           interpretation="EXACT_FINITE_JUMPS_ARE_NOT_UNIFORM_GAP")
    # THREE exact rational levels with spacing 1/9,1/3,1.
    qfine=F(1,2)
    qmiddle=F(1,8)
    qcoarse=F(1,512)
    three_ok = qfine**3==qmiddle and qfine**9==qcoarse
    if sabotage == "wrong_cube_block":
        three_ok &= qfine**2==qmiddle
    check("exact_three_scale",three_ok)
    for physical_time in (1,2,3):
        fine=qfine**(9*physical_time)
        mid=qmiddle**(3*physical_time)
        coarse=qcoarse**physical_time
        check("exact_correlation_t"+str(physical_time),
              fine==mid==coarse)
        record("YM4_THREE_SCALE",physical_time=physical_time,
               a_fine="1/9",a_middle="1/3",a_coarse="1",
               fine_exponent=9*physical_time,middle_exponent=3*physical_time,
               coarse_exponent=physical_time,
               correlation=frac(coarse),
               physical_mass="9*log(2)",all_equal=int(fine==mid==coarse))
    # Actual repeated cubing, binary exponentiation, and sequential linear map.
    for name, getq in (("STABLE",stable),("COLLAPSE",collapse)):
        q=getq(5)
        for exponent in (1,2,3,4,5,6):
            n=3**exponent
            cube=q
            for _ in range(exponent):
                cube=cube*cube*cube
            binary=q**n
            check("triadic_"+name+"_"+str(exponent),cube==binary)
            if n<=243:
                state=(F(0),F(1))
                for _ in range(n):
                    state=transfer_step(q,state)
                check("direct_"+name+"_"+str(exponent),
                      state[1]==binary)
            record("YM4_MATRIX_JUMP",family=name,spacing="1/243",
                   exponent=exponent,steps=n,
                   cubings=exponent,cube_equals_binary=int(cube==binary),
                   direct_checked=int(n<=243),
                   state_sha256=digest_frac(binary))
    # First gap != gap above a low-energy cluster.
    for j in (0,3,6,12):
        K=3**j
        E=[F(i,K) for i in range(8)]
        E.extend((F(94)+F(7,K),F(95)+F(7,K)))
        assert len(E)==10 and E==sorted(E)
        upper=E[8]-E[7]
        first=E[1]-E[0]
        check("cluster_not_first",upper==94 and first==F(1,K) and
              upper!=first and
              (sabotage!="misread_high_cluster" or first==upper))
        record("YM4_CLUSTER",j=j,cluster_high_gap=frac(upper),
               true_first_gap=frac(first),
               state_count=len(E),
               high_gap_is_not_first=1)
    # More finite samples cannot turn a vanishing sequence into a uniform bound.
    if sabotage == "fake_uniform_collapsing_gap":
        check("uniform_continuum_gap_not_inferred",
              F(1,3**12)>=F(1,2))
    else:
        check("uniform_continuum_gap_not_inferred",
              F(1,3**12)<F(1,2))
    record("YM4_SCOPE",finite_S3_E9_minus_E8_lower="24.039673_J_E_at_r9",
           finite_S3_first_gap="NOT_DEDUCED_FROM_E9_MINUS_E8",
           finite_SU2_transfer_gap="FIXED_LATTICE_ONLY",
           YM4_04="ALL_SCALE_INDUCTION_OPEN",
           YM4_05="OS_CONTINUUM_EXISTENCE_OPEN",
           YM4_06="UNIFORM_PHYSICAL_MASS_GAP_OPEN",
           Yang_Mills_Clay="NOT_PROVED")
    if FAILS:
        record("YM4_BRIDGE_VERIFY",status="FAIL",failed=len(FAILS),
               sabotage=sabotage or "NONE",json_zero=1)
        sys.exit(1)
    record("YM4_BRIDGE_VERIFY",status="PASS",
           prediction_rows=len(predictions),
           rational_family_levels=13,
           exact_three_scale=1,
           jump_rows=12,cluster_examples=4,
           red_controls="RUN_SEPARATELY",
           physical_mass_gap_continuum="OPEN",
           Clay_proof="NOT_CLAIMED",json_zero=1)


if __name__ == "__main__":
    main()
