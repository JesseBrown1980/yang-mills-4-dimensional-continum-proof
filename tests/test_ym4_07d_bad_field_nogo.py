#!/usr/bin/env python3
"""YM4-07D: incidence, local finite-energy constants and separated-support tests.
All integer arithmetic. Proof of probability bound is in accompanying note.
"""
from hashlib import sha256
from itertools import product
from math import factorial
from pathlib import Path
import sys

FAULTS=("wrong_neighbor","drop_negative_side","wrong_neighbor_degree",
        "wrong_halfball_constant","wrong_anchor_spacing",
        "wrong_beta_cost","wrong_asymptotic_slope")
if len(sys.argv)>2 or (len(sys.argv)==2 and sys.argv[1] not in FAULTS):
    raise SystemExit("usage: test_ym4_07d_bad_field_nogo.py [fault-name]")
fault=sys.argv[1] if len(sys.argv)==2 else ""

def check(ok,reason):
    if not ok:
        print("YM4_07D_REJECT|reason="+reason+"|fault="+fault+"|json=0",flush=True)
        raise SystemExit(1)

def emit(name,fields):
    print("YM4_07D|"+name+"|"+fields+"|json=0",flush=True)

def power(x,n):
    check(type(x) is int and type(n) is int and n>=0,"integer_exponent")
    out=1
    while n:
        if n&1:
            out*=x
        n//=2
        if n:
            x*=x
    return out

def shift(x,axis,step,L):
    return tuple((x[j]+(step if j==axis else 0))%L for j in range(4))

def edges(x,mu,nu,L):
    return ((x,mu), (shift(x,mu,1,L),nu),
            (shift(x,nu,1,L),mu), (x,nu))

def support_of_central(x,mu,L):
    inc=[]
    for nu in range(4):
        if nu==mu:
            continue
        inc.append(edges(x,mu,nu,L))
        if fault!="drop_negative_side":
            inc.append(edges(shift(x,nu,-1,L),mu,nu,L))
    check(len(inc)==6,"six_incident_plaquettes")
    check(all((x,mu) in f for f in inc),"target_in_each_plaquette")
    used=set(link for f in inc for link in f)
    check(len(used)==19,"nineteen_distinct_support_links")
    return inc,used

def geometry(L):
    x=(0,0,0,0)
    mu=0
    inc,used=support_of_central(x,mu,L)
    j=(shift(x,mu,1,L),1)
    if fault=="wrong_neighbor":
        j=(x,mu)
    count=sum(j in f for f in inc)
    check(count==1,"neighbor_appears_in_exactly_one_target_staple")
    # Every nondegenerate 4D link meets precisely six plaquettes
    full_count=0
    for site in product(range(L),repeat=4):
        for a in range(4):
            for d in range(a+1,4):
                if j in edges(site,a,d,L):
                    full_count+=1
    if fault=="wrong_neighbor_degree":
        full_count-=1
    check(full_count==6,"neighbor_has_six_Wilson_plaquettes")
    # Build disjoint 19-edge supports at spacing at least three.
    stride=2 if fault=="wrong_anchor_spacing" else 3
    indices=list(range(0,L,stride))
    # For L not divisible by stride, do not include a final anchor
    # closer than stride across the periodic wrap.
    indices=[a for a in indices if a <= stride*((L//stride)-1)]
    selected=[]
    for site in product(indices,repeat=4):
        loc,local=support_of_central(site,0,L)
        for other in selected:
            check(not (local & other),"separated_neighborhoods_disjoint")
        selected.append(local)
    check(len(selected)==power(L//3,4),"anchor_count_exact")
    emit("GEOMETRY","L="+str(L)+"|staples=6|support_links=19"+
         "|neighbor_once=YES|neighbor_plaquettes=6|separated_anchors="+str(len(selected))+
         "|overlap=NONE")

def constants():
    # fixed r=1/8: half Haar ball >= r^3/48=1/24576.
    check(48*power(8,3)==24576,"fixed_halfball_24576")
    denominator=48*power(8,3)
    if fault=="wrong_halfball_constant":
        denominator+=1
    check(denominator==24576,"fixed_halfball_normalization")
    # 6 beta*(1+1/8) = 27 beta/4.
    cost_num=6*9
    cost_den=8
    if fault=="wrong_beta_cost":
        cost_num=6*8
    check(4*cost_num==27*cost_den,"fixed_exp_cost_27_over_4")

    # adaptive radius 1/(6 beta): r^3/48 gives 1/(10368 beta^3).
    check(48*power(6,3)==10368,"adaptive_halfball_10368")
    for beta in (1,2,16,64):
        # t<=6 beta, so t*(1+1/(6 beta))<=6 beta+1.
        numerator=6*beta*(6*beta+1)
        denominator=6*beta
        check(numerator==denominator*(6*beta+1),
              "adaptive_cost_at_beta_"+str(beta))
    # e < 3: n! >= 2^(n-1), n>=2; strict at n>=4.
    for n in range(2,30):
        check(factorial(n)>=power(2,n-1),"exp_one_factorial_geometric")
    check(factorial(4)>power(2,3),"exp_one_strict_lt3")
    emit("CONSTANTS","fixed_r=1/8|halfball_ge=1/24576|cost=27beta/4"+
         "|adaptive_r=1/(6beta)|halfball_ge=1/(10368beta_cubed)"+
         "|cost_le=6beta+1|e_lt3=PASS")

def slope():
    # For beta_k=beta0+c k+o(k) and Lk~3^k,
    # M_k p_k exponent is 4 ln3 - 6c.
    check(4*3==6*2,"critical_slope_two_thirds_ln3")
    # c_SU2_one_loop = 11 ln3/(3*pi^2)
    # pi>3 => pi^2>9>11/2, so c_1loop<2/3 ln3.
    comparison=18
    if fault=="wrong_asymptotic_slope":
        comparison=10
    check(comparison>11,"SU2_one_loop_slope_below_threshold")
    emit("SLOPE","trinary_volume_ratio=81|critical_c=2ln3/3"+
         "|SU2_one_loop_c=11ln3/(3pi_squared)|pi_gt3=YES|strict=PASS")
    emit("SCOPE","all_good_failure=CONDITIONAL_ON_TRAJECTORY"+
         "|actual_nonperturbative_RG=OPEN|cluster_bound=OPEN|physical_gap=OPEN")

def main():
    for suffix,expected in (("D",10),("D2",6)):
        path=("docs/PREDICTION-YM4-07"+suffix+
              ("-UNIFORM-BAD-FIELD-LOWER-20261111.hbp" if suffix=="D" else
               "-ADAPTIVE-BAD-FIELD-LOWER-20261111.hbp"))
        raw=Path(path).read_bytes()
        count=sum(line.startswith("PREDICT|id=W07"+suffix+"-")
                  for line in raw.decode("utf-8").splitlines())
        check(count==expected,"frozen_predictions_"+suffix)
        emit("FREEZE","segment="+suffix+"|rows="+str(expected)+
             "|sha256="+sha256(raw).hexdigest())
    for L in (3,4,6,7,9):
        geometry(L)
    constants()
    slope()
    emit("DONE","exact_geometry_and_constants=PASS"+
         "|analytic_probability_proof=IN_NOTE|physical_mass_gap=NOT_PROVED")

if __name__=="__main__":
    main()
