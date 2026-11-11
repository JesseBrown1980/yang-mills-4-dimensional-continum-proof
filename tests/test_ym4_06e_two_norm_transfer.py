#!/usr/bin/env python3
"""YM4-06E exact rational verification of alpha-free two-norm Schur criterion.
No actual 4D SU2 uniform leakage or dark-complement bound is inferred.
"""
from hashlib import sha256
from math import gcd
from pathlib import Path
import sys

FAULTS=("corrupt_memory","drop_fast","u_too_low",
        "ignore_coupling","too_small_tau","fake_zero_leakage")
if len(sys.argv)>2 or (len(sys.argv)==2 and sys.argv[1] not in FAULTS):
    raise SystemExit("usage: test_ym4_06e_two_norm_transfer.py [fault]")
fault=sys.argv[1] if len(sys.argv)==2 else ""

def check(ok,where):
    if not ok:
        print("YM4_06E_REJECT|check="+where+"|fault="+fault+"|json=0",flush=True)
        raise SystemExit(1)

def emit(name,details):
    print("YM4_06E|"+name+"|"+details+"|json=0",flush=True)

def power(n,k):
    check(type(n) is int and type(k) is int and k>=0,"integer_exponent")
    x=1
    while k:
        if k&1:
            x*=n
        k//=2
        if k:
            n*=n
    return x

def rat(n,d=1):
    check(type(n) is int and type(d) is int and d!=0,"integer_fraction")
    if d<0:
        n,d=-n,-d
    g=gcd(n,d)
    return (n//g,d//g)

def add(x,y):
    return rat(x[0]*y[1]+y[0]*x[1],x[1]*y[1])

def sub(x,y):
    return rat(x[0]*y[1]-y[0]*x[1],x[1]*y[1])

def mul(x,y):
    return rat(x[0]*y[0],x[1]*y[1])

def cube(x):
    return mul(mul(x,x),x)

def eq(x,y):
    return x[0]*y[1]==y[0]*x[1]

def lt(x,y):
    return x[0]*y[1]<y[0]*x[1]

def le(x,y):
    return x[0]*y[1]<=y[0]*x[1]

def matmul(A,B):
    check(len(A[0])==len(B),"matrix_dimensions")
    out=[]
    for i in range(len(A)):
        row=[]
        for j in range(len(B[0])):
            value=rat(0)
            for k in range(len(B)):
                value=add(value,mul(A[i][k],B[k][j]))
            row.append(value)
        out.append(tuple(row))
    return tuple(out)

def mixed():
    one=rat(1)
    zero=rat(0)
    u0=rat(1,2)
    z=rat(1,16)
    rho=rat(1,4)
    P=((one,zero,zero),(zero,u0,z),(zero,z,rho))
    P2=matmul(P,P)
    P3=matmul(P2,P)
    B=((one,zero),(zero,u0))
    B2=matmul(B,B)
    B3=matmul(B2,B)

    # The zeta-squared input is computed independently as the actual
    # two-tick compression difference on the complete coarse complement.
    memory=sub(P2[1][1],B2[1][1])
    if fault=="corrupt_memory":
        memory=add(memory,rat(1,1024))
    check(eq(memory,rat(1,256)),"independent_two_tick_memory")
    zeta2=rat(0) if fault=="ignore_coupling" else mul(P[2][1],P[2][1])
    check(eq(zeta2,memory),"zeta_squared_equals_two_tick_memory")

    rc=P3[1][1]
    check(eq(rc,rat(133,1024)),"actual_exact_induced_coarse_ratio")
    three_memory=sub(P3[1][1],B3[1][1])
    if fault=="fake_zero_leakage":
        check(eq(three_memory,rat(0)),"fake_three_tick_markov_closure")
    check(eq(three_memory,rat(5,1024)),"exact_three_tick_memory")
    check(le(three_memory,mul(rat(3),zeta2)),
          "memory_operator_norm_bound_3zeta2")

    full_retained_upper=add(rc,mul(rat(3),zeta2))
    check(eq(full_retained_upper,rat(145,1024)),"retained_cube_bound")
    u=rat(1,2) if fault=="u_too_low" else rat(17,32)
    check(le(full_retained_upper,cube(u)),"retained_cube_upper_enclosure")
    if fault=="":
        check(eq(cube(u),rat(4913,32768)),"cube_exact_4913")

    tau=rat(17,32) if fault=="too_small_tau" else rat(35,64)
    check(le(u,tau) and le(rho,tau),"Schur_positivity_diagonals")
    product=mul(sub(tau,u),sub(tau,rho))
    check(le(zeta2,product),"all_physical_modes_schur_gate")
    check(eq(product,rat(19,4096)) and
          eq(zeta2,rat(16,4096)),"exact_schur_margin")
    emit("INDUCED","r_coarse=133/1024|two_tick_leakage=1/256"+
         "|three_tick_memory=5/1024|retained_cube_cap=145/1024")
    emit("SCHUR","cube_u=4913/32768|u=17/32"+
         "|discarded_rho=1/4|zeta_squared=1/256"+
         "|tau=35/64|determinant=19/4096"+
         "|full_fine_second_ratio_le_tau=PASS")

def dark():
    one,zero=rat(1),rat(0)
    u,rho=rat(1,2),rat(3,4)
    if fault=="drop_fast":
        rho=rat(1,4)
    F=((one,zero,zero),(zero,u,zero),(zero,zero,rho))
    F3=matmul(matmul(F,F),F)
    rc=F3[1][1]
    check(eq(rc,rat(1,8)),"coarse_visible_three_step_exact")
    check(eq(F3[2][2],rat(27,64)),"independent_hidden_3quarter_eigen")
    ubar=rat(1,2)
    check(eq(cube(ubar),rc),"zero_leakage_retained_cube_exact")
    tau=rat(1,2)
    check(not le(rho,tau),"hidden_mode_must_block_false_gap")
    emit("DARK","coarse_r=1/8|zeta_squared=0"+
         "|fast_rho=3/4|false_tau=1/2|REJECTED=YES")

def main():
    raw=Path("docs/PREDICTION-YM4-06E-TWO-NORM-TRANSFER-20261111.hbp").read_bytes()
    rows=[line for line in raw.decode("utf-8").splitlines()
          if line.startswith("PREDICT|id=E")]
    check(len(rows)==14,"frozen_fourteen_predictions")
    emit("FREEZE","rows=14|sha256="+sha256(raw).hexdigest())
    mixed()
    dark()
    emit("SCOPE","induced_Wilson_isometry=ANALYTIC"+
         "|two_norm_sufficient_theorem=DERIVED"+
         "|all_scale_real_SU2_zeta_rho=OPEN|physical_continuum_gap=OPEN")
    emit("DONE","full_spectrum_two_norm_exact_control=PASS|json=0")

if __name__=="__main__":
    main()
