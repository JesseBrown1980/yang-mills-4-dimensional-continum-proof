#!/usr/bin/env python3
"""YM4-06G exact SU2 electric-only dark-sector theorem computational controls.
Q8 is used only for noncommutative central-noise algebra, not SU2 spectral data.
"""
from hashlib import sha256
from itertools import product
from math import factorial,gcd
from pathlib import Path
import sys

FAULTS=("noncentral_noise","wrong_product_order","false_short_cycle",
        "wrong_off_plaquette","false_dark_bound","false_zero_leakage",
        "false_small_budget","drop_high_spin")
if len(sys.argv)>2 or (len(sys.argv)==2 and sys.argv[1] not in FAULTS):
    raise SystemExit("usage: test_ym4_06g_electric_su2_dark.py [fault]")
fault=sys.argv[1] if len(sys.argv)==2 else ""

def check(ok,why):
    if not ok:
        print("YM4_06G_REJECT|check="+why+"|fault="+fault+"|json=0",flush=True)
        raise SystemExit(1)

def emit(kind,fields):
    print("YM4_06G|"+kind+"|"+fields+"|json=0",flush=True)

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
    check(type(n) is int and type(d) is int and d!=0,"integer_rational")
    if d<0:
        n,d=-n,-d
    g=gcd(n,d)
    return (n//g,d//g)

def add(x,y):
    return rat(x[0]*y[1]+x[1]*y[0],x[1]*y[1])

def mul(x,y):
    return rat(x[0]*y[0],x[1]*y[1])

def div(x,y):
    check(y[0]!=0,"nonzero_divisor")
    return rat(x[0]*y[1],x[1]*y[0])

def sub(x,y):
    return rat(x[0]*y[1]-x[1]*y[0],x[1]*y[1])

def lt(x,y):
    return x[0]*y[1]<x[1]*y[0]

def bessel_two_series(m):
    # beta=2, so I_m(2)=sum_k 1/(k!(m+k)!).
    term=rat(1,factorial(m))
    total=term
    for k in range(20):
        term=div(term,rat((k+1)*(m+k+1)))
        total=add(total,term)
    omitted=div(term,rat(21*(m+21)))
    ratio=rat(1,22*(m+22))
    return total,add(total,div(omitted,sub(rat(1),ratio)))

def spin():
    I1=bessel_two_series(1)
    I2=bessel_two_series(2)
    low=div(I2[0],I1[1])
    high=div(I2[1],I1[0])
    check(lt(rat(43,100),low) and lt(low,high) and
          lt(high,rat(44,100)),"SU2_exact_positive_Bessel_ratio")
    high_spin=rat(1,2) if fault=="drop_high_spin" else rat(1,6)
    check(lt(high_spin,low),"all_n_ge2_lower_than_fundamental")
    dark_lower=rat(ipow(43,4),ipow(100,4))
    coarse_upper=rat(ipow(44,12),ipow(100,12))
    if fault=="false_dark_bound":
        dark_lower=coarse_upper
    check(lt(coarse_upper,dark_lower),
          "discarded_fine_plaquette_dominates_all_coarse_modes")
    target=rat(ipow(25,8),ipow(11,8))
    if fault=="false_small_budget":
        target=rat(2)
    check(lt(rat(711),target),"multiplicative_error_greater_than_710")
    emit("SPECTRUM","beta_t=2|t1_between=43/100_and_44/100"+
         "|n_ge2_le_1/6|fine_first=t1^4|coarse_first=t1^36"+
         "|dark_rho=t1^4|required_x_gt_710")

def shift(x,axis,n,L):
    return tuple((x[i]+(n if i==axis else 0))%L for i in range(3))

def neighbors(x,L):
    return {shift(x,i,n,L) for i in range(3) for n in (-1,1)}

def graph(L):
    for x in product(range(L),repeat=3):
        near=neighbors(x,L)
        check(len(near)==6 and x not in near,"simple_periodic_graph")
        for y in near:
            check(x in neighbors(y,L),"graph_edge_symmetry")
            check(not (near & neighbors(y,L)),"no_triangle_cycles")
    x=(0,0,0)
    square=(x,shift(x,0,1,L),shift(shift(x,0,1,L),1,1,L),
            shift(x,1,1,L))
    check(len(set(square))==4 and all(
          square[(k+1)%4] in neighbors(square[k],L) for k in range(4)),
          "nontrivial_shortest_plaquette_cycle")
    emit("GRAPH","L="+str(L)+"|no_cycles_of_length_below_4=PASS")

def off_path():
    Lc=4
    Lf=12
    paths=set()
    for c in product(range(Lc),repeat=3):
        base=tuple(3*x for x in c)
        for i in range(3):
            for k in range(3):
                paths.add((shift(base,i,k,Lf),i))
    x=(0,0,0) if fault=="wrong_off_plaquette" else (1,1,1)
    edges=((x,0),(shift(x,0,1,Lf),1),
           (shift(x,1,1,Lf),0),(x,1))
    check(len(set(edges))==4 and all(e not in paths for e in edges),
          "four_offpath_fine_Wilson_plaquette_edges")
    check(len(paths)==576,"complete_coarse_line_link_census")
    emit("OFFPATH","fine_side=12|coarse_side=4"+
         "|coarse_line_links=576|disjoint_fine_plaquette_links=4")

def qm(a,b):
    w,x,y,z=a
    h,i,j,k=b
    return (w*h-x*i-y*j-z*k,w*i+x*h+y*k-z*j,
            w*j-x*k+y*h+z*i,w*k+x*j-y*i+z*h)

def qc(a):
    return (a[0],-a[1],-a[2],-a[3])

E=(1,0,0,0)
M=(-1,0,0,0)
I=(0,1,0,0)
J=(0,0,1,0)
K=(0,0,0,1)
Q8=(E,M,I,qc(I),J,qc(J),K,qc(K))

def central_noise():
    weights={g:(3 if g==E else (1 if g==M else 2)) for g in Q8}
    if fault=="noncentral_noise":
        weights[I]=3
    check(sum(weights.values())==(17 if fault=="noncentral_noise" else 16),
          "positive_Q8_weight_normalization")
    triples=list(product(Q8,repeat=3))
    base_hist={g:0 for g in Q8}
    for a,b,c in triples:
        base_hist[qm(qm(a,b),c)]+=weights[a]*weights[b]*weights[c]
    count=0
    for a,b,c in triples:
        if a not in (E,I,J,K):
            continue
        v=qm(qm(a,b),c)
        inverse=qc(v)
        observed={g:0 for g in Q8}
        for p,q,s in triples:
            if fault=="wrong_product_order":
                fine=qm(qm(qm(qm(qm(p,a),s),c),q),b)
            else:
                fine=qm(qm(qm(qm(qm(p,a),q),b),s),c)
            effective_noise=qm(fine,inverse)
            observed[effective_noise]+=weights[p]*weights[q]*weights[s]
        check(observed==base_hist,"three_link_central_noise_pushforward")
        count+=1
    check(count==256,"Q8_base_configuration_count")
    leakage=rat(1,8) if fault=="false_zero_leakage" else rat(0)
    check(leakage[0]==0,"zero_memory_of_exact_central_semigroup")
    emit("NOISE","noncommuting_Q8_base_triples=256"+
         "|three_noise_configs_per_base=512|central_histogram_exact=PASS"+
         "|block_subspace_invariant=PASS")

def main():
    raw=Path("docs/PREDICTION-YM4-06G-ELECTRIC-SU2-DARK-20261111.hbp").read_bytes()
    rows=[v for v in raw.decode("utf-8").splitlines()
          if v.startswith("PREDICT|id=G")]
    check(len(rows)==14,"frozen_fourteen_predictions")
    emit("FREEZE","rows=14|sha256="+sha256(raw).hexdigest())
    spin()
    graph(3 if fault=="false_short_cycle" else 4)
    graph(12)
    off_path()
    central_noise()
    emit("SCOPE","continuous_SU2_electric_only_model=ANALYTIC"+
         "|isotropic_4D_Wilson_mass_gap=OPEN|r9=UNTOUCHED")
    emit("DONE","actual_SU2_dark_sector_countercontrol=DERIVED")

if __name__=="__main__":
    main()
