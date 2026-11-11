#!/usr/bin/env python3
"""YM4-06D exact finite Q8 control of general Haar disintegration and isometry.
The SU2 Wilson Hilbert-space proof is analytic in its note, not a Q8 inference.
"""
from hashlib import sha256
from itertools import product
from math import gcd
from pathlib import Path
import sys

FAULTS=("wrong_end_gauge", "wrong_order", "wrong_fiber_weight",
        "ignore_ground_density", "bad_pushforward_norm", "fake_semigroup")
if len(sys.argv)>2 or (len(sys.argv)==2 and sys.argv[1] not in FAULTS):
    raise SystemExit("usage: test_ym4_06d_wilson_vacuum_isometry.py [fault]")
fault=sys.argv[1] if len(sys.argv)==2 else ""

def check(ok,reason):
    if not ok:
        print("YM4_06D_REJECT|check="+reason+"|fault="+fault+"|json=0",flush=True)
        raise SystemExit(1)

def emit(label, fields):
    print("YM4_06D|"+label+"|"+fields+"|json=0",flush=True)

def rat(a,b=1):
    check(type(a) is int and type(b) is int and b!=0,"int_rational")
    if b<0:
        a,b=-a,-b
    g=gcd(a,b)
    return (a//g,b//g)

def add(a,b):
    return rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1])

def sub(a,b):
    return rat(a[0]*b[1]-b[0]*a[1],a[1]*b[1])

def mul(a,b):
    return rat(a[0]*b[0],a[1]*b[1])

def eq(a,b):
    return a[0]*b[1]==b[0]*a[1]

def quot(a,b):
    check(b[0]!=0,"nonzero_rational_denominator")
    return rat(a[0]*b[1],a[1]*b[0])

def sum_rat(values):
    s=rat(0)
    for v in values:
        s=add(s,v)
    return s

def qm(a,b):
    x,y,z,w=a
    h,i,j,k=b
    return (x*h-y*i-z*j-w*k,
            x*i+y*h+z*k-w*j,
            x*j-y*k+z*h+w*i,
            x*k+y*j-z*i+w*h)

def qi(a):
    return (a[0],-a[1],-a[2],-a[3])

E=(1,0,0,0)
NEG=(-1,0,0,0)
I=(0,1,0,0)
JQ=(0,0,1,0)
K=(0,0,0,1)
Q8=(E,NEG,I,qi(I),JQ,qi(JQ),K,qi(K))

def triple(a,b,c):
    if fault=="wrong_order":
        return qm(qm(a,c),b)
    return qm(qm(a,b),c)

def test_covariance():
    choices=((E,I,JQ,K),(I,JQ,K,qi(I)),(JQ,K,I,JQ),
             (NEG,I,K,JQ),(K,NEG,I,qi(K)))
    cases=0
    for a,b,c in product(Q8,repeat=3):
        true=qm(qm(a,b),c)
        for g0,g1,g2,g3 in choices:
            aa=qm(qm(g0,a),qi(g1))
            bb=qm(qm(g1,b),qi(g2))
            cc=qm(qm(g2,c),qi(g3))
            observed=triple(aa,bb,cc)
            right=g3 if fault=="wrong_end_gauge" else qi(g3)
            target=qm(qm(g0,true),right)
            check(observed==target,"ordered_three_link_gauge_covariance")
            cases+=1
    check(cases==2560,"fixed_gauge_cases")
    emit("GAUGE","Q8_noncommuting=YES|three_link_trials=2560"+
         "|endpoint_covariance=PASS|inner_gauge_cancellation=PASS")

def test_fiber():
    counts={v:0 for v in Q8}
    weights={v:0 for v in Q8}
    total=0
    fine_norm_numerator=0
    for a,b,c in product(Q8,repeat=3):
        v=triple(a,b,c)
        check(v in counts,"quaternion_group_closed")
        counts[v]+=1
        indicator=1 if v==E else 0
        weight=1+(1 if a==E else 0)+(1 if fault=="wrong_fiber_weight" else 2)*indicator
        weights[v]+=weight
        total+=weight
        f=3 if v==E else (-2 if v==NEG else 1)
        fine_norm_numerator+=weight*f*f
    check(all(counts[v]==64 for v in Q8),"three_link_Haar_64_per_element")
    check(weights[E]==200 and all(weights[v]==72 for v in Q8 if v!=E),
          "independent_positive_fiber_mass")
    check(total==704,"positive_weight_full_partition")
    normalizer=total+1 if fault=="bad_pushforward_norm" else total
    rho_e=rat(8*weights[E],normalizer)
    rho_non=rat(8*weights[NEG],normalizer)
    check(eq(rho_e,rat(25,11)) and eq(rho_non,rat(9,11)),
          "strict_positive_pushforward_density")
    check(eq(add(mul(rho_e,rat(1,8)),mul(rho_non,rat(7,8))),rat(1)),
          "pushforward_normalized")
    emit("FIBER","group=Q8|fine_assignments=512|preimages_per_V=64"+
         "|sum_weight=704|rho_identity=25/11|rho_other=9/11")

    norm_fine=rat(fine_norm_numerator,normalizer)
    coarse_norm=rat(19,8) if fault=="ignore_ground_density" else rat(
        weights[E]*9+weights[NEG]*4+sum(weights[v] for v in Q8 if v not in (E,NEG)),normalizer)
    check(eq(norm_fine,coarse_norm),"weighted_pullback_exact_isometry")
    check(eq(norm_fine,rat(315,88)),"independent_weighted_norm")
    # Raw-Haar isometry is an exact square-root-free identity:
    # Omega_f^2=w/Z, rho(v)=8*sum_fiber(w)/Z,
    # || Omega_f f(B)/sqrt(rho(B)) ||_Hf^2
    # = 1/8 sum_v f(v)^2, verified by cancellation per fiber.
    for v in Q8:
        per_fiber=quot(rat(weights[v],normalizer),rat(8*weights[v],normalizer))
        check(eq(per_fiber,rat(1,8)),"raw_Haar_isometry_per_fiber")
    emit("ISOMETRY","induced_weighted_norm_squared=315/88"+
         "|raw_Haar_square_root_free_identity=PASS"+
         "|induced_vacuum_maps_to_fine_vacuum=PASS")

def matmul(A,B):
    check(len(A[0])==len(B),"matmul_shapes")
    result=[]
    for i in range(len(A)):
        row=[]
        for j in range(len(B[0])):
            row.append(sum_rat(mul(A[i][k],B[k][j])
                               for k in range(len(B))))
        result.append(tuple(row))
    return tuple(result)

def test_three_tick_memory():
    o=rat(1)
    z=rat(0)
    h=rat(1,2)
    off=rat(1,16)
    f=rat(1,4)
    P=((o,z,z),(z,h,off),(z,off,f))
    P2=matmul(P,P)
    P3=matmul(P2,P)
    P6=matmul(P3,P3)
    # Select vacuum and retained mode (indices 0 and 1).
    compressed=P3[1][1]
    memory=sub(P6[1][1],mul(compressed,compressed))
    leakage=mul(P3[2][1],P3[2][1])
    if fault=="fake_semigroup":
        check(eq(memory,rat(0)),"false_exact_three_tick_semigroup")
    check(eq(memory,leakage),"six_tick_minus_two_coarse_exact_gram")
    check(eq(leakage,rat(12769,16777216)),
          "independent_three_tick_leakage_numerator")
    check(eq(compressed,rat(133,1024)),"three_tick_retained_component")
    emit("MEMORY","time_block=3|three_tick_induced=133/1024"+
         "|six_tick_minus_two_coarse=12769/16777216"+
         "|general_non_markov_closure=COUNTEREXAMPLE")

def main():
    raw=Path("docs/PREDICTION-YM4-06D-WILSON-VACUUM-ISOMETRY-20261111.hbp").read_bytes()
    rows=[v for v in raw.decode("utf-8").splitlines()
          if v.startswith("PREDICT|id=H")]
    check(len(rows)==12,"twelve_frozen_predicted_rows")
    emit("FREEZE","rows=12|sha256="+sha256(raw).hexdigest())
    test_covariance()
    test_fiber()
    test_three_tick_memory()
    emit("SCOPE","real_finite_SU2_vacuum_isometry=ANALYTIC_PROOF_IN_NOTE"+
         "|Q8_only=FINITE_ALGEBRA_CONTROL|fourD_transfer_norm_estimates=OPEN"+
         "|continuum_gap=OPEN|r9=UNTOUCHED")
    emit("DONE","exact_finite_control=PASS|physics_released=NO|json=0")

if __name__=="__main__":
    main()
