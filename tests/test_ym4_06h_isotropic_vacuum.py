#!/usr/bin/env python3
"""YM4-06H exact integer/rational controls of actual isotropic SU2 spatial Haar
moment structure and Fourier-cutoff vacuum normalization. No float or JSON.
Analytic Haar and signed exponential arguments are in the accompanying note.
"""
from hashlib import sha256
from itertools import product, combinations
from math import factorial, gcd
from pathlib import Path
import sys

FAULTS=("wrong_census", "cross_moment", "wrong_variance",
        "false_exp_bound", "claim_N19_enough", "nonorthonormal_Gram")
if len(sys.argv)>2 or (len(sys.argv)==2 and sys.argv[1] not in FAULTS):
    raise SystemExit("usage: test_ym4_06h_isotropic_vacuum.py [fault]")
fault=sys.argv[1] if len(sys.argv)==2 else ""

def check(ok,name):
    if not ok:
        print("YM4_06H_REJECT|check="+name+"|fault="+fault+"|json=0",flush=True)
        raise SystemExit(1)

def emit(kind,detail):
    print("YM4_06H|"+kind+"|"+detail+"|json=0",flush=True)

def ipow(base,exponent):
    check(type(base) is int and type(exponent) is int and exponent>=0,"integer_power_input")
    out=1
    while exponent:
        if exponent&1:
            out*=base
        exponent//=2
        if exponent:
            base*=base
    return out

def rat(n,d=1):
    check(type(n) is int and type(d) is int and d!=0,"integer_fraction")
    if d<0:
        n,d=-n,-d
    g=gcd(n,d)
    return (n//g,d//g)

def add(a,b):
    return rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1])

def mul(a,b):
    return rat(a[0]*b[0],a[1]*b[1])

def sub(a,b):
    return rat(a[0]*b[1]-b[0]*a[1],a[1]*b[1])

def lt(a,b):
    return a[0]*b[1]<b[0]*a[1]

def eq(a,b):
    return a[0]*b[1]==b[0]*a[1]

def shift(x,axis,L):
    y=list(x)
    y[axis]=(y[axis]+1)%L
    return tuple(y)

def incidence(L):
    faces=[]
    for x in product(range(L),repeat=3):
        for i,j in combinations(range(3),2):
            edges=( (x,i),(shift(x,i,L),j),
                    (shift(x,j,L),i),(x,j) )
            check(len(set(edges))==4,"four_distinct_links_per_plaquette")
            faces.append(frozenset(edges))
    actual=len(faces)
    predicted=3*ipow(L,3)
    if fault=="wrong_census" and L==2:
        predicted+=1
    check(actual==predicted and len(set(faces))==actual,
          "complete_distinct_spatial_plaquette_census")
    seen={0:0,1:0,2:0}
    for p,q in combinations(faces,2):
        overlap=len(p&q)
        check(overlap<4,"distinct_plaquettes_not_same_link_support")
        check(overlap <= (2 if L==2 else 1),
              "no_pair_spatial_plaquettes_shares_every_link")
        check(len(p-q)>0 and len(q-p)>0,"Haar_unpaired_link_exists")
        seen[overlap]+=1
    check(sum(seen.values())==actual*(actual-1)//2,
          "exhaustive_cross_plaquette_pair_enumeration")
    if L==2:
        check(seen[2]==24 and seen[1]==96 and seen[0]==156,
              "independent_L2_overlap_census")
    if L==3:
        check(seen[2]==0 and seen[1]==486 and seen[0]==2754,
              "independent_L3_overlap_census")
    if L==4:
        check(seen[2]==0 and seen[1]==1152 and seen[0]==17184,
              "independent_L4_overlap_census")
    emit("GEOMETRY","L="+str(L)+"|plaquettes="+str(actual)+
         "|max_common_links="+str(2 if L==2 else 1)+
         "|distinct_supports=YES|unpaired_Haar_link_each_pair=YES")
    return actual,seen

def moments(Ns):
    # SU2 Haar fundamental character squared integral equals 1.
    # a_p=(1/2) chi_1, so each exact Haar variance is 1/4.
    ap_second=rat(1,3) if fault=="wrong_variance" else rat(1,4)
    check(eq(ap_second,rat(1,4)),"Haar_fundamental_character_orthogonality")
    cross=rat(1,4) if fault=="cross_moment" else rat(0)
    check(eq(cross,rat(0)),"unpaired_link_Haar_cross_correlation")
    E_X2=add(mul(rat(Ns),ap_second),
             mul(rat(Ns*(Ns-1)),cross))
    check(eq(E_X2,rat(Ns,4)),"exact_total_spatial_trace_variance")
    return E_X2

def exponential_floor():
    # All-real-t inequality proven analytically:
    # exp(t)>=1+t+t^2/(2+abs(t)).
    # For t=-u, g(u)=(u+2)exp(-u)-(2-u),
    # g'(u)=1-(u+1)exp(-u)>=0 for u>=0.
    # The checker verifies the derived exact rational Haar consequences.
    Ns,_=incidence(2)
    check(eq(moments(Ns),rat(6)),"L2_X_variance_six")
    beta=2
    factor=add(rat(1),rat(beta*beta*Ns,4*(2+beta*Ns)))
    check(eq(factor,rat(37,25)),"isotropic_Wilson_variance_floor_37_over_25")
    check(beta*Ns==48 and 2*beta*Ns==96,
          "isotropic_Jensen_vs_crude_Perron_exponents")
    emit("ISOTROPIC","L=2|beta=2|Ns=24|E_X=0|E_X_squared=6"+
         "|old_floor=exp_minus96|Jensen_floor=exp_minus48"+
         "|Haar_variance_floor=37/25_times_exp_minus48")

    e_partial=rat(0)
    for k in range(7):
        e_partial=add(e_partial,rat(1,factorial(k)))
    e_series_bound=add(e_partial,rat(8,7*factorial(7)))
    false_limit=rat(2) if fault=="false_exp_bound" else rat(87,32)
    check(lt(e_series_bound,false_limit),"exponential_factorial_upper_87over32")
    check(lt(e_partial,e_series_bound),"exponential_tail_positive")
    emit("EXP","e_series_partial_k0_to6_plus_geometric_tail_lt_87over32=PASS")

    rational_lower=mul(factor,rat(ipow(32,48),ipow(87,48)))
    delta20=rat(1,factorial(22))
    delta19=rat(1,factorial(21))
    check(lt(delta20,rational_lower),"Fourier_delta_N20_below_certified_Perron_floor")
    claimed_upper=delta19 if fault=="claim_N19_enough" else delta20
    check(lt(claimed_upper,rational_lower),
          "selected_fourier_cutoff_has_proved_normalization")
    check(lt(rational_lower,delta19),
          "N19_not_certified_by_this_elementary_floor")
    dims=21*22*43//6
    check(dims==3311 and Ns==24 and ipow(3311,24)>ipow(10,80),
          "infeasible_full_tensor_rank")
    emit("CUT","L=2|beta=2|N=20|delta=1/22factorial"+
         "|rational_Perron_lower=37/25_times_32over87_power48"+
         "|strict_delta_lt_lower=PASS|N19_cutoff_not_certified=YES"+
         "|matrix_coeff_rank_per_link=3311|total_links=24")

def orthonormal_G():
    # Non-orthonormal basis f1=e1,f2=e1+e2.
    # True selfadjoint T=diag(1,1/2) in orthonormal standard basis.
    # Matrix entries in f basis: G=[[1,1],[1,3/2]]
    # Gram of basis: S=[[1,1],[1,2]].
    # Physical generalized det(G-lambda S) vanishes at 1 and 1/2.
    # Ordinary eigenvalues of G are NOT {1,1/2}.
    G=((rat(1),rat(1)),(rat(1),rat(3,2)))
    S=((rat(1),rat(1)),(rat(1),rat(2)))
    if fault=="nonorthonormal_Gram":
        S=((rat(1),rat(0)),(rat(0),rat(1)))
    def det_shift(lam,Gram):
        a=sub(G[0][0],mul(lam,Gram[0][0]))
        b=sub(G[0][1],mul(lam,Gram[0][1]))
        c=sub(G[1][0],mul(lam,Gram[1][0]))
        d=sub(G[1][1],mul(lam,Gram[1][1]))
        return sub(mul(a,d),mul(b,c))
    check(eq(det_shift(rat(1),S),rat(0)) and
          eq(det_shift(rat(1,2),S),rat(0)),
          "nonorthonormal_basis_requires_generalized_eigenproblem")
    check(not eq(det_shift(rat(1),
                           ((rat(1),rat(0)),(rat(0),rat(1)))),rat(0)),
          "ordinary_Gram_eigenvalues_invalid_if_basis_not_orthonormal")
    emit("F12","basis_orthonormal=REQUIRED"+
         "|nonorthonormal_uses_generalized_eigenproblem=PASS")

def main():
    raw=Path("docs/PREDICTION-YM4-06H-ISOTROPIC-VACUUM-20261111.hbp").read_bytes()
    rows=[v for v in raw.decode("utf-8").splitlines() if v.startswith("PREDICT|id=J")]
    check(len(rows)==16,"sixteen_prediction_rows")
    emit("FREEZE","rows=16|sha256="+sha256(raw).hexdigest())
    for L in (3,4):
        Ns,_=incidence(L)
        check(eq(moments(Ns),rat(Ns,4)),
              "all_L_Haar_variance")
    exponential_floor()
    orthonormal_G()
    emit("SCOPE","actual_isotropic_SU2_analytic_Haar_moments=DERIVED"+
         "|actual_isotropic_full_spectrum=NOT_COMPUTED"+
         "|physical_gap=OPEN|r9_launch=UNTOUCHED")
    emit("DONE","exact_rational_census_and_cutoff_control=PASS|json=0")

if __name__=="__main__":
    main()
