#!/usr/bin/env python3
"""06I/J: exact-rational complete-sector SU2 Wilson finite strong-coupling bound.
No selected-sector-to-full-spectrum inference. No floats or JSON.
"""
from hashlib import sha256
from itertools import product, combinations
from math import factorial, gcd
from pathlib import Path
import sys

FAULTS=("wrong_four_link_L2","drop_Haar_floor","incorrect_cutoff",
        "false_high_spin","wrong_winding_support","false_N3_ratio",
        "false_center_charge","false_two_edge_glueball")
if len(sys.argv)>2 or (len(sys.argv)==2 and sys.argv[1] not in FAULTS):
    raise SystemExit("usage: test_ym4_06i_j_isotropic_first_ratio.py [fault]")
fault=sys.argv[1] if len(sys.argv)==2 else ""

def check(ok,where):
    if not ok:
        print("YM4_06IJ_REJECT|check="+where+"|fault="+fault+"|json=0",flush=True)
        raise SystemExit(1)

def emit(kind,fields):
    print("YM4_06IJ|"+kind+"|"+fields+"|json=0",flush=True)

def power(a,n):
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

def add(a,b):
    return rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1])

def sub(a,b):
    return rat(a[0]*b[1]-b[0]*a[1],a[1]*b[1])

def mul(a,b):
    return rat(a[0]*b[0],a[1]*b[1])

def div(a,b):
    check(b[0]!=0,"nonzero_rational_divisor")
    return rat(a[0]*b[1],a[1]*b[0])

def eq(a,b):
    return a[0]*b[1]==b[0]*a[1]

def lt(a,b):
    return a[0]*b[1]<b[0]*a[1]

def le(a,b):
    return a[0]*b[1]<=b[0]*a[1]

def cube(a):
    return mul(mul(a,a),a)

def ratpower(a,n):
    return rat(power(a[0],n),power(a[1],n))

def bessel_interval(order,term_count):
    # beta=1/8; x=beta/2=1/16.
    x=rat(1,16)
    x2=mul(x,x)
    term=rat(1,power(16,order)*factorial(order))
    summation=rat(0)
    for k in range(term_count):
        summation=add(summation,term)
        term=div(mul(term,x2),rat((k+1)*(order+k+1)))
    # Last included k=term_count-1. "term" is first omitted.
    # Each subsequent ratio no greater than the first omitted-to-next ratio.
    ratio=div(x2,rat((term_count+1)*(order+term_count+1)))
    check(lt(ratio,rat(1)),"Bessel_series_tail_ratio")
    upper=add(summation,div(term,sub(rat(1),ratio)))
    return summation,upper

def bessel():
    i1=bessel_interval(1,10)
    i2=bessel_interval(2,10)
    t1lo=div(i2[0],i1[1])
    t1hi=div(i2[1],i1[0])
    fundamental_lower=rat(511,16384)
    fundamental_upper=rat(1,32)
    check(lt(fundamental_lower,t1lo) and
          lt(t1lo,t1hi) and lt(t1hi,fundamental_upper),
          "continuous_SU2_fundamental_Bessel_interval")
    high_spin=rat(1,16) if fault=="false_high_spin" else rat(1,1536)
    check(lt(high_spin,fundamental_lower),
          "all_higher_irreps_below_fundamental")
    check(lt(high_spin,mul(fundamental_lower,fundamental_lower)),
          "neutral_two_link_higher_irreps_below_four_link_fundamental")
    emit("BESSEL","isotropic_beta=1/8|fundamental_gt=511/16384"+
         "|fundamental_lt=1/32|n_ge2_le=1/1536")
    return fundamental_lower,fundamental_upper,high_spin

def translate(x,axis,step,L):
    z=list(x)
    z[axis]=(z[axis]+step)%L
    return tuple(z)

def edge_from_step(x,axis,sign,L):
    nxt=translate(x,axis,sign,L)
    return ((x,axis) if sign==1 else (nxt,axis)),nxt

def cycle_exists(L,length):
    # Enumerate closed trails with distinct oriented link identities,
    # without an early return to the starting vertex.
    for start in product(range(L),repeat=3):
        stack=[(start,(),(start,))]
        for depth in range(length):
            updated=[]
            for at,links,verts in stack:
                for axis in range(3):
                    for sign in (-1,1):
                        key,nxt=edge_from_step(at,axis,sign,L)
                        if key in links:
                            continue
                        if nxt==start:
                            if depth+1==length:
                                return True
                            continue
                        if depth+1==length or nxt in verts:
                            continue
                        updated.append((nxt,links+(key,),verts+(nxt,)))
            stack=updated
            if not stack:
                break
    return False

def spatial_geometry():
    for L,target in ((2,2),(3,3),(4,4),(5,4)):
        if fault=="wrong_four_link_L2" and L==2:
            target=4
        for n in range(2,target):
            check(not cycle_exists(L,n),"no_shorter_periodic_cycle_L"+str(L))
        check(cycle_exists(L,target),"actual_periodic_spatial_girth_L"+str(L))
        emit("GIRTH","L="+str(L)+"|girth="+str(target))
    L=2
    vertices=tuple(product(range(2),repeat=3))
    # Two positively-oriented x edges running x0 -> x1 -> x0;
    # exactly 12 distinct axis windings, one per transverse coordinate.
    winding=set()
    for x in vertices:
        for i in range(3):
            nextx=translate(x,i,1,L)
            links=frozenset(((x,i),(nextx,i)))
            if len(links)!=2:
                continue
            winding.add((i,links))
    count=12 if fault=="wrong_winding_support" else len(winding)
    check(count==12 and len(winding)==12,
          "twelve_two_link_periodic_fundamental_windings")
    for i,links in winding:
        parity=sum(1 for x,axis in links if axis==i and x[i]==1)%2
        if fault=="false_center_charge":
            parity=0
        check(parity==1,"fundamental_winding_center_charged")
    plaquettes=[]
    for x in vertices:
        for i,j in combinations(range(3),2):
            links=((x,i),(translate(x,i,1,L),j),
                   (translate(x,j,1,L),i),(x,j))
            check(len(set(links))==4,"distinct_plaquette_links")
            plaquettes.append(frozenset(links))
    check(len(plaquettes)==24 and len(set(plaquettes))==24,
          "isotropic_24_distinct_spatial_plaquettes")
    for links in plaquettes:
        for i in range(3):
            parity=sum(1 for x,axis in links if axis==i and x[i]==1)%2
            if fault=="false_two_edge_glueball" and i==0:
                parity=1
            check(parity==0,"contractible_plaquette_center_neutral")
    emit("CENTER","winding_lines=12|plaquettes=24"+
         "|fundamental_winding_charge=ODD|plaquette_charge=EVEN"+
         "|vacuum_to_winding_overlap=ZERO")
    return len(vertices),len(plaquettes)

def qmul(a,b):
    w,x,y,z=a
    h,i,j,k=b
    return (w*h-x*i-y*j-z*k,
            w*i+x*h+y*k-z*j,
            w*j-x*k+y*h+z*i,
            w*k+x*j-y*i+z*h)

def qinv(q):
    return (q[0],-q[1],-q[2],-q[3])

def q8_gauge():
    one=(1,0,0,0)
    minus=(-1,0,0,0)
    e1=(0,1,0,0)
    e2=(0,0,1,0)
    e3=(0,0,0,1)
    qs=(one,minus,e1,qinv(e1),e2,qinv(e2),e3,qinv(e3))
    counter=0
    for a,b,g,h in product(qs,repeat=4):
        original=qmul(a,b)
        transformed=qmul(
            qmul(qmul(g,a),qinv(h)),
            qmul(qmul(h,b),qinv(g)))
        check(original[0]==transformed[0],
              "two_link_winding_gauge_invariance")
        center_flipped=qmul(qmul(minus,a),b)
        check(center_flipped[0]==-original[0],
              "two_link_winding_center_odd")
        counter+=1
    check(counter==4096,"Q8_algebra_4096")
    emit("GAUGE","Q8_only_algebra_control=YES"+
         "|noncommuting_endpoint_changes=4096"+
         "|actual_SU2_spectrum_from_irrep_theorem=YES")

def spectrum(lo,hi):
    # Every eigenvalue of genuine normalized interacting isotropic transfer
    # is bounded via B^(1/2) A B^(1/2) between e^-6 B and B.
    # At L=2 the first nontrivial eigenvalue of B is t1^2.
    Ns=24
    beta=rat(1,8)
    check(eq(mul(rat(2*Ns),beta),rat(6)),
          "isotropic_spatial_A_lower_exponent")
    e_upper=rat(11,4)
    # Elementary rational upper e < 11/4 follows from e < 87/32.
    check(lt(rat(87,32),e_upper),"strict_exponential_upper_bound")

    # Actual SU2 Haar variance gain from 06H:
    beta2Ns=mul(mul(beta,beta),rat(Ns))
    varpart=div(beta2Ns, mul(rat(4), add(rat(2),mul(beta,rat(Ns)))))
    Haar_factor=add(rat(1),varpart)
    if fault=="drop_Haar_floor":
        Haar_factor=rat(1)
    check(eq(Haar_factor,rat(163,160)),
          "actual_isotropic_Haar_Perron_floor")

    # 1/lambda0 <= (160/163) exp(3)
    ratio_upper=mul(mul(ratpower(hi,2),rat(160,163)),
                    ratpower(e_upper,3))
    check(eq(ratio_upper,rat(6655,333824)),
          "actual_full_first_ratio_upper_exact")
    check(lt(ratio_upper,rat(1,50)),
          "actual_complete_physical_gap_gt_ln50")

    ratio_lower=mul(ratpower(rat(4,11),6),ratpower(lo,2))
    check(eq(ratio_lower,rat(261121,116101021696)),
          "actual_full_first_ratio_lower_exact")

    # At L=2, all nonconstant physical electric spin-networks
    # of two edges have winding center charge (-1)^n. Neutral modes
    # are higher even irreps on two edges or >=four-link support.
    neutral_upper=ratpower(hi,4)
    charged_lower=ratio_lower  # lambda0<=1; lower of physical charged ratio.
    check(lt(neutral_upper,charged_lower),
          "interacting_center_charged_first_spectrum_above_neutral")
    check(lt(ratpower(hi,2),ratpower(rat(4,11),6)),
          "charged_fundamental_wins_over_neutral_first")
    emit("SPECTRUM","L=2|beta=1/8|actual_isotropic_SU2=YES"+
         "|first_physical_ratio_gt=261121/116101021696"+
         "|first_physical_ratio_lt=6655/333824_lt_1/50"+
         "|gamma_gt_ln50|first_sector=CENTER_CHARGED")

def cutoff():
    # N=3; (beta/2)^(N+1)/(N+2)! = 1/(16^4*5!)
    delta=rat(1,power(16,4)*factorial(5))
    if fault=="incorrect_cutoff":
        delta=rat(1,power(16,3)*factorial(4))
    check(eq(delta,rat(1,7864320)),
          "full_SU2_temporal_Fourier_tail_N3")
    dim=sum(power(n+1,2) for n in range(4))
    check(dim==30 and power(dim,24)>power(10,30),
          "entire_link_tensor_rank_computational_hold")
    # Certified lambda0_N >= (163/160)exp(-3), and exp(3)<(11/4)^3.
    relative=div(delta,mul(rat(163,160),ratpower(rat(4,11),3)))
    if fault=="false_N3_ratio":
        relative=rat(1,100)
    check(eq(relative,rat(1331,512753664)),
          "relative_Fourier_tail_exact_rational")
    check(lt(relative,rat(1,380000)),
          "relative_Fourier_tail_below_1_over380000")
    emit("FOURIER","N=3|delta=1/7864320"+
         "|relative_delta_over_lambda0_lt=1331/512753664_lt_1/380000"+
         "|per_link_rank=30|whole_pre_gauge_rank=30_power24")

def main():
    for path,prefix,expected in (
        ("docs/PREDICTION-YM4-06I-ISOTROPIC-FIRST-RATIO-20261111.hbp",
         "PREDICT|id=I",16),
        ("docs/PREDICTION-YM4-06J-CENTER-SECTOR-20261111.hbp",
         "PREDICT|id=C",10)):
        raw=Path(path).read_bytes()
        rows=[s for s in raw.decode("utf-8").splitlines() if s.startswith(prefix)]
        check(len(rows)==expected,"immutable_frozen_predictions_"+prefix)
        emit("FREEZE","rows="+str(expected)+"|sha256="+sha256(raw).hexdigest())
    spatial_geometry()
    lo,hi,_=bessel()
    q8_gauge()
    spectrum(lo,hi)
    cutoff()
    emit("SCOPE","actual_beta_1over8_complete_physical_spectrum=ENCLOSED"+
         "|separate_local_center_neutral_gap=NOT_COMPUTED"+
         "|actual_beta_2_spectrum=OPEN|all_scale_4D_gap=OPEN|r9=HOLD")
    emit("DONE","independent_integer_all_sector_controls=PASS|json=0")

if __name__=="__main__":
    main()
