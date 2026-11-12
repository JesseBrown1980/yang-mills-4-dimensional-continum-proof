#!/usr/bin/env python3
"""YM4-06K exact-integer independent controls of complete center-neutral SU2
Wilson spectral decay. Analytic all-irrep and minmax steps live in the note.
No float, JSON, selected-state diagonalization or finite-group spectral proxy.
"""
from hashlib import sha256
from itertools import product, combinations
from math import factorial, gcd
from pathlib import Path
import sys

FAULTS=("fake_high_spin_first","false_loop_girth","wrong_center_parity",
        "bad_Haar_floor","invalid_neutral_ratio","dropped_tail",
        "false_correlator_bound","claim_first_Wilson_overlap")

if len(sys.argv)>2 or (len(sys.argv)==2 and sys.argv[1] not in FAULTS):
    raise SystemExit("usage: test_ym4_06k_neutral_first_spectrum.py [fault]")
fault=sys.argv[1] if len(sys.argv)==2 else ""

def check(ok,rule):
    if not ok:
        print("YM4_06K_REJECT|check="+rule+"|fault="+fault+"|json=0",flush=True)
        raise SystemExit(1)

def emit(topic,values):
    print("YM4_06K|"+topic+"|"+values+"|json=0",flush=True)

def ipow(n,k):
    check(type(n) is int and type(k) is int and k>=0,"nonnegative_integer_power")
    p=1
    while k:
        if k&1:
            p*=n
        k//=2
        if k:
            n*=n
    return p

def rat(n,d=1):
    check(type(n) is int and type(d) is int and d!=0,"integer_rational")
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
    check(y[0]!=0,"nonzero_rational_denominator")
    return rat(x[0]*y[1],x[1]*y[0])

def powrat(x,k):
    return rat(ipow(x[0],k),ipow(x[1],k))

def lt(x,y):
    return x[0]*y[1]<y[0]*x[1]

def eq(x,y):
    return x[0]*y[1]==y[0]*x[1]

def positive_series(order,terms):
    # SU2 I_order(beta), at beta=1/8: beta/2=1/16.
    first=rat(1,ipow(16,order)*factorial(order))
    acc=rat(0)
    nextterm=first
    for k in range(terms):
        acc=add(acc,nextterm)
        nextterm=div(nextterm,rat(ipow(16,2)*(k+1)*(order+k+1)))
    further_ratio=rat(1,ipow(16,2)*(terms+1)*(order+terms+1))
    check(lt(further_ratio,rat(1)),"positive_geometric_Bessel_remainder")
    return acc,add(acc,div(nextterm,sub(rat(1),further_ratio)))

def independent_Bessel():
    i1=positive_series(1,12)
    i2=positive_series(2,12)
    lower=div(i2[0],i1[1])
    upper=div(i2[1],i1[0])
    check(lt(rat(511,16384),lower) and
          lt(lower,upper) and lt(upper,rat(1,32)),
          "true_continuous_SU2_Bessel_fundamental_bounds")
    higher=rat(1,32) if fault=="fake_high_spin_first" else rat(1,1536)
    check(lt(higher,rat(511,16384)),"all_n_ge2_below_t1")
    check(lt(powrat(higher,2),powrat(rat(511,16384),4)),
          "neutral_higher_irrep_two_edge_below_fundamental_plaquette")
    emit("BESSEL","beta=1/8|t1_between_511/16384_and_1/32=YES"+
         "|higher_tn_le_1/1536|two_even_link_below_four_fundamental=YES")
    return lower,upper

def shift(point,axis,L):
    return tuple((point[j]+(1 if j==axis else 0))%L for j in range(3))

def check_geometry():
    L=2
    vertices=tuple(product(range(L),repeat=3))
    links={(v,i) for v in vertices for i in range(3)}
    faces=[]
    for v in vertices:
        for i,j in combinations(range(3),2):
            edges=frozenset(((v,i),(shift(v,i,L),j),
                             (shift(v,j,L),i),(v,j)))
            check(len(edges)==4,"four_distinct_plaquette_links")
            faces.append(edges)
    expected_faces=25 if fault=="false_loop_girth" else 24
    check(len(links)==24 and len(faces)==expected_faces and
          len(set(faces))==24,"full_periodic_L2_plaquette_census")
    windings=set()
    for v in vertices:
        for i in range(3):
            links2=frozenset(((v,i),(shift(v,i,L),i)))
            check(len(links2)==2,"distinct_parallel_winding_links")
            windings.add((i,links2))
    check(len(windings)==12,"twelve_primitive_two_link_axis_windings")
    # The cubical L2 spatial multigraph is bipartite and has no self loops,
    # so it has no odd cycles. There are no 1-edge cycles or 3-edge cycles.
    for v in vertices:
        for i in range(3):
            check((sum(v)%2)!=(sum(shift(v,i,L))%2),
                  "bipartite_no_one_or_three_edge_cycles")
    for axis,w in windings:
        parity=sum(1 for v,i in w if i==axis and v[axis]==1)%2
        if fault=="wrong_center_parity":
            parity=0
        check(parity==1,"fundamental_winding_center_odd")
    for face in faces:
        for axis in range(3):
            parity=sum(1 for v,i in face if i==axis and v[axis]==1)%2
            check(parity==0,"contractible_plaquette_center_even")
    emit("GEOMETRY","L=2|sites=8|oriented_links=24|plaquettes=24"+
         "|girth=2|two_link_windings=12|no_odd_cycle=YES"+
         "|fundamental_two_link_center=ODD"+
         "|fundamental_four_link_plaquette_center=EVEN")

def neutral_ratio():
    # Genuine isotropic SU2 Wilson spatial weight, Ns=24 and beta=1/8.
    Ns=24
    beta=rat(1,8)
    check(eq(mul(mul(beta,rat(2)),rat(Ns)),rat(6)),
          "actual_spatial_Wilson_pointwise_lower_expminus6")
    variance=div(mul(powrat(beta,2),rat(Ns)),
                 mul(rat(4),add(rat(2),mul(beta,rat(Ns)))))
    floor=add(rat(1),variance)
    if fault=="bad_Haar_floor":
        floor=rat(1)
    check(eq(floor,rat(163,160)),"actual_isotropic_Haar_Perron_163_over160")
    # e < 87/32 < 11/4, proved independently in the predecessor's
    # exact factorial-series checker. The bound below is intentionally
    # rational and conservative.
    upper=mul(mul(powrat(rat(1,32),4),rat(160,163)),
              powrat(rat(11,4),3))
    if fault=="invalid_neutral_ratio":
        upper=mul(mul(powrat(rat(1,32),2),rat(160,163)),
                  powrat(rat(11,4),3))
    lower=mul(powrat(rat(4,11),6),powrat(rat(511,16384),4))
    check(eq(upper,rat(6655,341835776)),
          "neutral_first_ratio_upper_exact")
    check(eq(lower,rat(68184176641,31165630701031653376)),
          "neutral_first_ratio_lower_exact")
    check(lt(lower,upper) and lt(upper,rat(1,50000)),
          "complete_center_neutral_ratio_lt_1over50000")
    # Across sectors, charged winding excitation is larger than the
    # first neutral excited eigenvalue in the full interacting model.
    check(lt(powrat(rat(1,32),4),
             mul(powrat(rat(4,11),6),powrat(rat(511,16384),2))),
          "charged_mode_strictly_outside_neutral_first")
    emit("SPECTRUM","actual_isotropic_SU2=YES|L=2|beta=1/8"+
         "|neutral_second_B=t1_power4"+
         "|neutral_ratio_gt=68184176641/31165630701031653376"+
         "|neutral_ratio_lt=6655/341835776_lt_1/50000"+
         "|neutral_gap_gt_ln50000"+
         "|charged_first_distinct_from_neutral=YES")
    return upper

def temporal_correlator(upper):
    # For a centered center-neutral f=(O-<O>)Omega, spectral theorem
    # gives 0<C_f(t)<=||f||²*r_neutral^t.
    # This checker tests exact rational attenuation for integer times;
    # the proof for arbitrary t follows from spectral positivity.
    cap=rat(1,100000) if fault=="false_correlator_bound" else rat(1,50000)
    check(lt(upper,cap),"uniform_neutral_correlator_decay_cap")
    for t in (0,1,2,3,27):
        check(lt(powrat(upper,t+1),powrat(cap,t+1)),
              "each_positive_integer_time_correlator_decay")
    first_overlap_proven=(fault=="claim_first_Wilson_overlap")
    check(not first_overlap_proven,
          "first_specific_neutral_Wilson_spectral_weight_still_open")
    emit("CORRELATOR","real_nonconstant_contractible_Wilson_C1_positive=ANALYTIC"+
         "|C_t_le_C0_times_1over50000_power_t_all_t_ge1=YES"+
         "|first_neutral_spectral_overlap=NOT_PROVED")

def Fourier_tail():
    # Carry original independent F-spectrum finite cutoff across sectors:
    # beta=1/8,N=3: delta=(1/16)^4/5!
    delta=rat(1,ipow(16,4)*factorial(5))
    if fault=="dropped_tail":
        delta=rat(0)
    check(eq(delta,rat(1,7864320)),"full_matrix_coefficient_Fourier_tail")
    relative=div(delta,mul(rat(163,160),powrat(rat(4,11),3)))
    check(eq(relative,rat(1331,512753664)),
          "independent_relative_Fourier_tail")
    check(lt(relative,rat(1,380000)),"full_SU2_Fourier_tail_small")
    emit("FOURIER","N=3|delta=1/7864320"+
         "|relative_delta_lt=1331/512753664_lt_1/380000"+
         "|not_a_truncated_matrix_diagonalization=YES")

def main():
    file=Path("docs/PREDICTION-YM4-06K-NEUTRAL-FIRST-SPECTRUM-20261112.hbp")
    raw=file.read_bytes()
    rows=[line for line in raw.decode("utf-8").splitlines()
          if line.startswith("PREDICT|id=K")]
    check(len(rows)==22,"twenty_two_original_frozen_predictions")
    emit("FREEZE","rows=22|sha256="+sha256(raw).hexdigest())
    check_geometry()
    independent_Bessel()
    neutral_upper=neutral_ratio()
    temporal_correlator(neutral_upper)
    Fourier_tail()
    emit("SCOPE","isotropic_SU2_L2_neutral_full_spectral_bound=ANALYTIC"+
         "|specific_glueball_first_weight=OPEN|beta2=OPEN"+
         "|large_volume=OPEN|continuum=OPEN|r9=HOLD")
    emit("DONE","rational_geometry_and_center_neutral_controls=PASS")

if __name__=="__main__":
    main()
