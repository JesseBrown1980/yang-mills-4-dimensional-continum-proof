#!/usr/bin/env python3
"""YM4-06F exact rational controls for the full physical Wilson Fourier tail.
The analytic 4D SU2 argument is in the note, not inferred from toy matrices.
"""
from hashlib import sha256
from math import factorial,gcd
from pathlib import Path
import sys

FAULTS=("drop_tail","wrong_volume_factor","wrong_cutoff_condition",
        "false_rank","false_lambda","false_bessel_ratio",
        "broken_end_gauge","false_loewner")
if len(sys.argv)>2 or (len(sys.argv)==2 and sys.argv[1] not in FAULTS):
    raise SystemExit("usage: test_ym4_06f_full_wilson_fourier.py [fault]")
fault=sys.argv[1] if len(sys.argv)==2 else ""

def check(ok,why):
    if not ok:
        print("YM4_06F_REJECT|check="+why+"|fault="+fault+"|json=0",flush=True)
        raise SystemExit(1)

def emit(kind,fields):
    print("YM4_06F|"+kind+"|"+fields+"|json=0",flush=True)

def ipow(a,n):
    check(type(a) is int and type(n) is int and n>=0,"integer_power")
    out=1
    while n:
        if n&1:
            out*=a
        n//=2
        if n:
            a*=a
    return out

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

def div(x,y):
    check(y[0]!=0,"nonzero_rational_divisor")
    return rat(x[0]*y[1],x[1]*y[0])

def lt(x,y):
    return x[0]*y[1]<y[0]*x[1]

def le(x,y):
    return x[0]*y[1]<=y[0]*x[1]

def equal(x,y):
    return x[0]*y[1]==y[0]*x[1]

def sum_rat(items):
    total=rat(0)
    for item in items:
        total=add(total,item)
    return total

def bessel_interval(beta,order,terms=48):
    # Positive exact factorial series, with a decreasing-ratio tail.
    x=rat(beta,2)
    x2=mul(x,x)
    value=rat(ipow(beta,order),ipow(2,order)*factorial(order))
    total=value
    for k in range(terms):
        value=div(mul(value,x2),rat((k+1)*(order+k+1)))
        total=add(total,value)
    omitted=div(mul(value,x2),rat((terms+1)*(order+terms+1)))
    ratio=div(x2,rat((terms+2)*(order+terms+2)))
    check(lt(ratio,rat(1)),"Bessel_positive_geometric_tail")
    upper=add(total,div(omitted,sub(rat(1),ratio)))
    return total,upper

def ratio_interval(beta):
    first=bessel_interval(beta,1)
    second=bessel_interval(beta,2)
    return div(second[0],first[1]),div(second[1],first[0])

def cutoff(beta,N,limit):
    if fault=="wrong_cutoff_condition" and beta==8:
        N=0
    check(2*(N+3)>=beta,"Fourier_tail_cutoff_criterion")
    delta=rat(ipow(beta,N+1),ipow(2,N+1)*factorial(N+2))
    if fault=="drop_tail" and beta==2:
        delta=rat(0)
    check(lt(rat(0),delta),"Fourier_tail_positive")
    check(lt(delta,rat(1,ipow(10,limit))),"Fourier_tail_decimal_limit")
    if beta==2:
        check(equal(delta,rat(1,3628800)),"beta2_exact")
    if beta==4:
        check(equal(delta,rat(4,42567525)),"beta4_exact")
    if beta==8:
        check(equal(delta,rat(8388608,2143861251406875)),"beta8_exact")
    emit("TAIL","beta="+str(beta)+"|N="+str(N)+"|delta="+
         str(delta[0])+"/"+str(delta[1])+
         "|strict_lt_10powminus="+str(limit))

def test_character():
    for beta,lo,hi in ((2,rat(43,100),rat(44,100)),
                       (4,rat(65,100),rat(66,100)),
                       (8,rat(81,100),rat(83,100))):
        left,right=ratio_interval(beta)
        if fault=="false_bessel_ratio" and beta==4:
            left=add(left,rat(1,10))
        check(lt(lo,left) and lt(left,right) and lt(right,hi),
              "exact_positive_Bessel_ratio_"+str(beta))
        emit("BESSEL","beta="+str(beta)+"|I2_over_I1_between="+
             str(lo[0])+"/"+str(lo[1])+":"+
             str(hi[0])+"/"+str(hi[1])+"|rational=PASS")
    for N in (0,1,2,8,12,20):
        dim=sum(ipow(n+1,2) for n in range(N+1))
        if fault=="false_rank" and N==2:
            dim+=1
        check(dim==(N+1)*(N+2)*(2*N+3)//6,
              "complete_matrix_coefficients_rank")
    emit("RANK","SU2_irreps=all_matrix_coefficients"+
         "|rank_per_link=sum_nplus1_squared|global_rank=EXPONENTIAL")
    cutoff(2,8,6)
    cutoff(4,12,7)
    cutoff(8,20,8)
    cutoff(16,40,13)

def test_complete_tensor():
    # Two Z2 temporal links, a finite spectral minmax control, NOT SU2.
    q=rat(1,8)
    k0=div(add(rat(1),q),rat(2))
    k1=div(sub(rat(1),q),rat(2))
    K=((k0,k1),(k1,k0))
    configs=((0,0),(0,1),(1,0),(1,1))
    B=tuple(tuple(mul(K[a][c],K[b][d]) for c,d in configs)
            for a,b in configs)
    P0=tuple(tuple(rat(1,4) for j in range(4)) for i in range(4))
    signs=((1,1,-1,-1),(1,-1,1,-1),(1,-1,-1,1))
    coeff=(q,q,mul(q,q))
    omitted=tuple(tuple(sum_rat(mul(coeff[k],rat(signs[k][i]*signs[k][j],4))
                                for k in range(3)) for j in range(4))
                   for i in range(4))
    check(all(equal(sub(B[i][j],P0[i][j]),omitted[i][j])
              for i in range(4) for j in range(4)),
          "complete_four_state_positive_tail")
    tail=(rat(0) if fault=="false_loewner" else
          (rat(1,128) if fault=="wrong_volume_factor" else q))
    check(le(mul(q,q),tail) and le(q,tail),
          "Loewner_complete_tensor_norm_bound")
    # A^1/2 is nonconstant: four rational weights.
    d=(rat(1),rat(1,2),rat(1,3),rat(1,4))
    T=tuple(tuple(mul(mul(d[i],B[i][j]),d[j]) for j in range(4))
            for i in range(4))
    T0=tuple(tuple(mul(mul(d[i],P0[i][j]),d[j]) for j in range(4))
             for i in range(4))
    check(all(equal(sub(T[i][j],T0[i][j]),
                    mul(mul(d[i],omitted[i][j]),d[j]))
              for i in range(4) for j in range(4)),
          "congruence_of_full_operator_tail")
    leading=mul(rat(1,4),sum_rat(mul(v,v) for v in d))
    if fault=="false_lambda":
        leading=rat(1,4)
    check(equal(leading,rat(205,576)),"truncated_rank_one_ground")
    check(equal(div(q,leading),rat(72,205)),
          "complete_first_excited_ratio_upper")
    emit("Z2_FULL","temporal_links=2|tail=1/8"+
         "|nonconstant_spatial_multiplier=YES|lambda0_N=205/576"+
         "|lambda1_all_states_le=1/8|ratio_le=72/205")

def qm(a,b):
    w,x,y,z=a
    h,i,j,k=b
    return (w*h-x*i-y*j-z*k,w*i+x*h+y*k-z*j,
            w*j-x*k+y*h+z*i,w*k+x*j-y*i+z*h)

def qc(a):
    return (a[0],-a[1],-a[2],-a[3])

def gauge():
    # SU2 fundamental coefficients transform in the same n=1 rep.
    qs=((1,0,0,0),(-1,0,0,0),(0,1,0,0),(0,-1,0,0),
        (0,0,1,0),(0,0,-1,0),(0,0,0,1),(0,0,0,-1))
    for left in qs:
        for right in qs:
            for v in qs:
                candidate=qm(qm(left,v),right if fault=="broken_end_gauge"
                             else qc(right))
                check(candidate==qm(left,qm(v,qc(right))),
                      "endpoint_gauge_representation")
                check(sum(x*x for x in candidate)==1,
                      "SU2_fundamental_quaternion_norm")
    emit("GAUGE","fundamental_SU2_matrix_coefficients_under_left_right"+
         "|Q8_512_exact_controls=PASS|all_n_invariance=ANALYTIC")

def main():
    raw=Path("docs/PREDICTION-YM4-06F-FULL-WILSON-FOURIER-20261111.hbp").read_bytes()
    rows=[line for line in raw.decode("utf-8").splitlines()
          if line.startswith("PREDICT|id=F")]
    check(len(rows)==22,"twenty_two_frozen_predictions")
    emit("FREEZE","rows=22|sha256="+sha256(raw).hexdigest())
    test_character()
    test_complete_tensor()
    gauge()
    emit("SCOPE","actual_finite_SU2_full_spectrum=ANALYTIC_PROOF"+
         "|absolute_temporal_tail_volume_independent=YES"+
         "|relative_gap_uniform=OPEN|continuum_gap=OPEN|r9=UNTOUCHED")
    emit("DONE","all_exact_rational_controls=PASS|physical_gap=NOT_PROVED")

if __name__=="__main__":
    main()
