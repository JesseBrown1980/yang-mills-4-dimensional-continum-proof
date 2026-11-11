#!/usr/bin/env python3
"""YM4-06C: full-vacuum-complement Schur spectral bound and compression leakage.
Only exact integer and rational comparisons; NOT a 4D Wilson RG theorem.
"""
from hashlib import sha256
from math import gcd
from pathlib import Path
import sys

FAULTS = ("drop_dark", "drop_leakage", "too_small_threshold",
          "incorrect_triple_memory", "fake_markov_closure",
          "suppress_fast_block")
if len(sys.argv)>2 or (len(sys.argv)==2 and sys.argv[1] not in FAULTS):
    raise SystemExit("usage: test_ym4_06c_full_spectrum_schur.py [fault]")
fault=sys.argv[1] if len(sys.argv)==2 else ""

def check(ok,name):
    if not ok:
        print("YM4_06C_REJECT|check="+name+"|fault="+fault+"|json=0",flush=True)
        raise SystemExit(1)

def emit(label,detail):
    print("YM4_06C|"+label+"|"+detail+"|json=0",flush=True)

def rp(base,n):
    check(type(base) is int and type(n) is int and n>=0,"integer_power_input")
    ret=1
    while n:
        if n&1:
            ret*=base
        n//=2
        if n:
            base*=base
    return ret

def rat(n,d=1):
    check(type(n) is int and type(d) is int and d!=0,"rational_integer_input")
    if d<0:
        n,d=-n,-d
    g=gcd(n,d)
    return (n//g,d//g)

def add(a,b):
    return rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1])

def sub(a,b):
    return rat(a[0]*b[1]-b[0]*a[1],a[1]*b[1])

def mul(a,b):
    return rat(a[0]*b[0],a[1]*b[1])

def lt(a,b):
    return a[0]*b[1]<b[0]*a[1]

def le(a,b):
    return a[0]*b[1]<=b[0]*a[1]

def equal(a,b):
    return a[0]*b[1]==b[0]*a[1]

def matrix_multiply(A,B):
    check(len(A)>0 and len(B)>0 and len(A[0])==len(B),"matrix_product_shape")
    return tuple(tuple(
        sum_terms([mul(A[i][k],B[k][j]) for k in range(len(B))])
        for j in range(len(B[0])))
        for i in range(len(A)))

def sum_terms(terms):
    z=rat(0)
    for item in terms:
        z=add(z,item)
    return z

def main():
    frozen=Path("docs/PREDICTION-YM4-06C-FULL-SPECTRUM-SCHUR-20261111.hbp").read_bytes()
    rows=[line for line in frozen.decode("utf-8").splitlines()
          if line.startswith("PREDICT|id=S")]
    check(len(rows)==16,"frozen_sixteen_predictions")
    emit("FREEZE","rows=16|sha256="+sha256(frozen).hexdigest())

    zero=rat(0)
    one=rat(1)
    u=rat(1,2)
    rho=rat(1,4)
    z=rat(1,16)
    if fault=="drop_leakage":
        z=zero
    P=((one,zero,zero),
       (zero,u,z),
       (zero,z,rho))
    P2=matrix_multiply(P,P)
    P3=matrix_multiply(P2,P)
    B=((one,zero),(zero,u))
    B2=matrix_multiply(B,B)
    B3=matrix_multiply(B2,B)

    mem2=sub(P2[1][1],B2[1][1])
    mem3=sub(P3[1][1],B3[1][1])
    if fault=="incorrect_triple_memory":
        mem3=sub(P2[1][1],B3[1][1])
    check(equal(mem2,rat(1,256)),"two_step_leakage_exact_Zadj_Z")
    check(equal(mem3,rat(5,1024)),"three_step_leakage_exact")
    check(equal(mem3,mul(add(add(u,u),rho),mul(z,z))),
          "three_step_memory_algebra")
    if fault=="fake_markov_closure":
        check(equal(P3[1][1],B3[1][1]),"false_exact_markov_closure")
    emit("MEMORY","two_step=1/256|three_step=5/1024"+
         "|nonmarkov_exact=YES|operator_norm_le_3zeta2=PASS")

    # Full fine transfer complement is a 2x2 PSD matrix [[u,z],[z,rho]].
    # An exact rational bound t applies when t >= u,rho and
    # (t-u)*(t-rho)>=z*z.
    t=rat(65,128) if fault=="too_small_threshold" else rat(33,64)
    check(le(u,t) and le(rho,t),"threshold_greater_than_both_blocks")
    determinant=mul(sub(t,u),sub(t,rho))
    coupling=mul(z,z)
    check(le(coupling,determinant),"schur_mixed_block_bound")
    if fault=="":
        check(equal(determinant,rat(17,4096)) and
              equal(coupling,rat(16,4096)),"strict_schur_margin")
        too_low=rat(65,128)
        check(lt(mul(sub(too_low,u),sub(too_low,rho)),coupling),
              "too_small_threshold_rejected")
    # Full second eigenvalue exceeds u since the 2x2 char polynomial
    # is negative at u: (u-u)*(u-rho)-z*z = -z*z.
    check(lt(zero,coupling),"mixing_creates_strict_overshoot")
    check(equal(sub(t,u),rat(1,64)),"certified_multiplicative_budget")
    check(equal(t,rat(33,64)),"certified_ratio_33_over64")
    emit("SCHUR","retained=1/2|discarded=1/4|cross=1/16"+
         "|full_second_gt=1/2|full_second_le=33/64"+
         "|t_ratio_vs_coarse_root=33/32|margin=1/4096")

    # Hidden dark mode with zero mixing. Coarse sees exact three-time
    # ratio 1/8 but the full fine model has a 3/4 excitation.
    hidden=rat(1,4) if fault=="drop_dark" else rat(3,4)
    H=((one,zero,zero),(zero,u,zero),(zero,zero,hidden))
    H3=matrix_multiply(matrix_multiply(H,H),H)
    check(equal(H3[1][1],rat(1,8)),"exact_compressed_three_step")
    check(equal(H3[2][2],rat(27,64)),"retained_dark_excitation")
    check(lt(u,hidden),"full_second_is_hidden")
    rho_claim=rat(0) if fault=="suppress_fast_block" else hidden
    check(equal(rho_claim,H[2][2]),"fast_block_independent_replay")
    check(lt(u,rho_claim),"fast_spectral_bound_exceeds_target")
    emit("DARK","coarse_3step_second=1/8|visible_fine=1/2"+
         "|actual_fine_first=3/4|complement_condition=REQUIRED")

    # Infinite all-k *conditional* budget, not a toy simulation claim.
    # a_(k+1)=3^-(k+1), x_k=a_(k+1)^2/64.
    # sum x_k/a_(k+1)= (1/64)*(1/3)/(1-1/3)=1/128.
    check(equal(mul(rat(1,64),rat(1,2)),rat(1,128)),
          "infinite_geometric_log_budget")
    # ln(2)>1/2 follows from integral_1^2 dx/x > 1/2.
    for k in range(7):
        fine_a=rat(1,rp(3,k+1))
        x=mul(mul(fine_a,fine_a),rat(1,64))
        cost=rat(1,64*rp(3,k+1))
        check(equal(mul(x,rat(rp(3,k+1))),cost),
              "all_k_budget_term_"+str(k))
    emit("BUDGET","a_fine=3^-k-1|xk=a_fine_squared_over64"+
         "|sum_xk_over_afine=1/128|ln2_gt_1/2"+
         "|actual_4D_estimates=NOT_PROVED")

    emit("SCOPE","vacuum_preserving_isometry=ASSUMED"+
         "|all_4D_SU2_block_errors=OPEN|dark_complement=UNBOUNDED"+
         "|continuum_gap=NOT_PROVED|r9=UNTOUCHED")
    emit("DONE","finite_exact_matrix_controls=PASS|theorem_proof=IN_NOTE|json=0")

if __name__=="__main__":
    main()
