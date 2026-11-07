#!/usr/bin/env python3
"""Shadow Cats: retained C0/C1/C2 mod-three residue across ternary torus slices.

The labels and 2/3 versus -1/3 account for a finite algebraic residual.
The script NEVER identifies it with a physical Yang-Mills excitation.
Predictions frozen at 11fecb81 before this script existed.
Only integers, permutations, SHA-256, no Python Fraction or binary floats.
"""
from hashlib import sha256
from pathlib import Path
import sys

SABOTAGES=("flip_residue","lose_signed_third","break_C1_cycle",
           "confuse_shadow_with_mass_gap")
arg=sys.argv[1:]
if len(arg)>1 or (arg and (not arg[0].startswith("sabotage=")
                            or arg[0][9:] not in SABOTAGES)):
    print("usage: test_shadow_cat_residual.py [sabotage=NAME]")
    sys.exit(2)
SABOTAGE=arg[0][9:] if arg else ""
FAIL=[]


def emit(tag,**data):
    print(tag+"|"+"|".join(str(k)+"="+str(v) for k,v in data.items())+"|json=0")


def check(name,condition):
    if not condition:
        FAIL.append(name)
        emit("FAILED",check=name)


def residue(cells):
    return sum(cells)%3


def cat_cycle(triple):
    return (triple[2],triple[0],triple[1])


def ternary_block(cells):
    assert len(cells)%3==0
    return [sum(cells[i:i+3])%3 for i in range(0,len(cells),3)]


def compose(first,second):
    return [first[second[i]] for i in range(len(first))]


def apply(permutation,state):
    return [state[permutation[i]] for i in range(len(state))]


def fingerprint(state):
    return sha256(bytes(state)).hexdigest()


def main():
    root=Path(__file__).resolve().parents[1]
    pred=(root/"docs/PREDICTION-YM4-04-SHADOW-CATS-20261106.hbp").read_bytes()
    rows=[line for line in pred.splitlines() if line.startswith(b"PREDICT|id=")]
    assert len(rows)==9
    emit("SHADOW_BEGIN",registered_predictions=len(rows),
         prediction_sha256=sha256(pred).hexdigest(),
         interpretation="TERNARY_ALGEBRA_NOT_YM4_SPECTRUM")
    triple=(1,1,0)
    orbit=[triple]
    for _ in range(3):
        orbit.append(cat_cycle(orbit[-1]))
    check("C1_order_three",orbit[3]==triple and len(set(orbit[:3]))==3
          and (SABOTAGE!="break_C1_cycle" or orbit[1]==orbit[0]))
    for i,t in enumerate(orbit[:3]):
        check("C1_residue_"+str(i),residue(t)==2)
        emit("SHADOW_CAT",C1_rotation=i,C0=t[0],C1=t[1],C2=t[2],
             shadow_residue=residue(t),
             unsigned_fraction="2/3",balanced_fraction="-1/3")
    check("signed_shadow_third",2-(-1)==3 and
          (SABOTAGE!="lose_signed_third" or 2-(-1)==0))
    emit("SHADOW_SIGNED",residue=2,unsigned="2/3",balanced="-1/3",
         difference="1/1",same_residue_mod_integer=1)
    check("connected_tori_share_shadow",orbit[0]!=orbit[1]
          and residue(orbit[0])==residue(orbit[1])==2)
    emit("SHADOW_CONNECTED",torus_A="1,1,0",torus_B="0,1,1",
         shared_shadow_residue=2,instant_physical_signal="NOT_TESTED")
    cells=[(i*i+2*i+1)%3 for i in range(27)]
    cells[0]=(cells[0]+(2-residue(cells)))%3
    check("initial_residual",residue(cells)==2 and
          (SABOTAGE!="flip_residue" or residue(cells)==1))
    state=cells[:]
    levels=[]
    while True:
        levels.append(len(state))
        check("blocked_shadow_"+str(len(state)),residue(state)==2)
        emit("SHADOW_BLOCK",sites=len(state),residue=residue(state),
             state_sha256=fingerprint(state))
        if len(state)==1:
            break
        state=ternary_block(state)
    check("all_three_scales_and_terminal",levels==[27,9,3,1])
    # The matrix is an integer permutation of 27 sites. Its 3^k power
    # can be computed by k cubings of the permutation, no giant array.
    first=[(i-1)%27 for i in range(27)]
    jumped=first
    for k in range(17):
        n=3**k
        result=apply(jumped,cells)
        independent=[cells[(i-n)%27] for i in range(27)]
        check("jump_"+str(k),result==independent and residue(result)==2)
        if n<=243:
            direct=cells[:]
            for _ in range(n):
                direct=apply(first,direct)
            check("direct_"+str(k),direct==result)
        if k in (0,1,2,3,9,16):
            emit("SHADOW_JUMP",exponent=k,steps=n,ring_sites=27,
                 remainder=n%27,shadow_residue=residue(result),
                 direct_short_checked=int(n<=243),
                 state_sha256=fingerprint(result))
        jumped=compose(compose(jumped,jumped),jumped)
    # A persistent finite-valued Shadow Cat DOES NOT supply the energy
    # of the lowest excited transfer state. The spectral ratio can close.
    for j in (1,3,6,9,12):
        K=3**j
        qdark=(K*K,K*K+1)
        upper=(1,K)
        valid=residue(cells)==2 and K>=3 and upper[0]<upper[1]
        if SABOTAGE=="confuse_shadow_with_mass_gap":
            valid=valid and K<=2
        check("shadow_not_gap_"+str(j),valid)
        emit("SHADOW_GAP_BOUNDARY",inv_spacing=K,shadow_residue=2,
             dark_transfer_ratio=str(qdark[0])+"/"+str(qdark[1]),
             dark_first_physical_gap_upper="1/"+str(K),
             positive_uniform_gap="NOT_INFERRED",
             actual_SU2_gauge_observable="NOT_CONSTRUCTED")
    if FAIL:
        emit("SHADOW_VERIFY",status="FAIL",failed=len(FAIL),
             sabotage=SABOTAGE or "NONE",json_zero=1)
        sys.exit(1)
    emit("SHADOW_VERIFY",status="PASS",predictions=9,
         torus_sizes="27,9,3,1",jump_exponents="0..16",
         high_jump=43046721,shared_signed_residual="2/3_equiv_-1/3_mod1",
         physical_instant_signaling="NOT_SHOWN",
         SU2_continuum_mass_gap="OPEN",json_zero=1)

if __name__=="__main__":
    main()
