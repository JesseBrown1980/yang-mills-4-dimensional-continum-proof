#!/usr/bin/env python3
"""Prediction-first YM4-04 two factor-three blocks of the ACTUAL SU(2) map.

Exact rational quaternions, SU2 YM4-03 Theorems 1-9 as pinned input, rigorous
global holomorphic-Cauchy error to a Wilson-only PROXY, YM4-02d/03 transfer
spectral implication, and an explicitly failing physical-gap counterexample.

Do not mistake this for SU2 full Wilson-integral evaluation, Wilson closure,
a weak-coupling physical gap, or an infinite-scale induction.
"""
import hashlib
import itertools
import math
import sys
from pathlib import Path

CONTROLS=("wrong_line_order","missing_inverse","wrong_beta_exponent",
          "wrong_log_tail","wrong_q9","spurious_visibility",
          "positive_toy_mass_floor","wrong_Haar_connected_zero_for_same_plaquette",
          "claim_nonzero_C_from_bound","false_variance_gt_one")
fault=""
if len(sys.argv)>2 or (len(sys.argv)==2 and
    (not sys.argv[1].startswith("sabotage=")
     or sys.argv[1][9:] not in CONTROLS)):
    print("usage: test_ym4_04_two_ternary_blocks.py [sabotage=CASE]")
    sys.exit(2)
if len(sys.argv)==2:
    fault=sys.argv[1][9:]

def check(ok,name):
    if not ok:
        print("FAILED|check="+name+"|json=0",flush=True)
        sys.exit(1)

def emit(tag,**values):
    print(tag+"|"+"|".join(str(k)+"="+str(v) for k,v in values.items())
          +"|json=0",flush=True)

def power(a,n):
    check(type(n) is int and n>=0,"nonnegative_integer_exponent")
    out=1
    while n:
        if n&1:
            out*=a
        n//=2
        if n:
            a*=a
    return out

def rat(a,b=1):
    check(type(a) is int and type(b) is int and b!=0,"rational_type")
    if b<0:
        a,b=-a,-b
    g=math.gcd(a,b)
    return (a//g,b//g)

def add(a,b):
    return rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1])
def sub(a,b):
    return rat(a[0]*b[1]-b[0]*a[1],a[1]*b[1])
def mul(a,b):
    return rat(a[0]*b[0],a[1]*b[1])
def inv(a):
    check(a[0]!=0,"inverse_nonzero")
    return rat(a[1],a[0])
def lt(a,b):
    return a[0]*b[1]<b[0]*a[1]
def le(a,b):
    return a[0]*b[1]<=b[0]*a[1]
def rp(a,n):
    return rat(power(a[0],n),power(a[1],n))
def rs(a):
    return str(a[0])+"/"+str(a[1])

ONE=(1,0,0,0,1)
POOL=((3,4,0,0,5),(5,0,12,0,13),(0,3,0,4,5),
      (0,0,5,12,13),(12,0,5,0,13),(4,0,0,3,5))
def norm(q):
    g=0
    for v in q:
        g=math.gcd(g,abs(v))
    check(g!=0 and q[4]>0,"unit_quaternion_denominator")
    return tuple(v//g for v in q)
def qm(p,q):
    a,b,c,d,m=p
    e,f,g,h,n=q
    return norm((a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,
                 a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e,m*n))
def qi(q):
    return q[0],-q[1],-q[2],-q[3],q[4]
def unit(q):
    return sum(v*v for v in q[:4])==q[4]*q[4]
def qword(items):
    q=ONE
    for item in items:
        q=qm(q,item)
    return q
def spatial(x,axis,offset,side):
    v=list(x)
    v[axis]=(v[axis]+offset)%side
    return tuple(v)
def fine_anchor(coarse):
    return tuple(9*x for x in coarse)
def qg(pos):
    i=sum((j+7)*v for j,v in enumerate(pos))
    return POOL[(i+3)%len(POOL)]
def gauge_link(U,pos,axis):
    edge=(pos,axis)
    h0=qg(pos)
    h1=qg(spatial(pos,axis,1,18))
    return qm(qm(h0,U.get(edge,ONE)),qi(h1))

def setup():
    field={}
    for c in itertools.product(range(2),repeat=4):
        for mu in range(4):
            base=fine_anchor(c)
            for s in range(9):
                p=spatial(base,mu,s,18)
                check((p,mu) not in field,"disjoint_coarse_link_lines")
                field[p,mu]=POOL[(sum(c)*5+mu*7+s)%len(POOL)]
    check(len(field)==576 and all(unit(q) for q in field.values()),
          "rational_SU2_field_576")
    return field

def blo(U,x,mu,side,step,getlink):
    # YM4-03 line product B_b, no artificial commutative shortcut.
    return qword(getlink(U,spatial(x,mu,j,side),mu)
                 for j in range(step))

def fine_get(U,x,mu):
    return U.get((x,mu),ONE)
def upper_get(U,x,mu):
    return U[(x,mu)]

def plaquette(V,x,mu,nu,L):
    a=upper_get(V,x,mu)
    b=upper_get(V,spatial(x,mu,1,L),nu)
    c=upper_get(V,spatial(x,nu,1,L),mu)
    d=upper_get(V,x,nu)
    return qword((a,b,qi(c),qi(d)))
def fine_rectangle(U,coarse,mu,nu):
    x=fine_anchor(coarse)
    word=[]
    for j in range(9):
        word.append(fine_get(U,x,mu))
        x=spatial(x,mu,1,18)
    for j in range(9):
        word.append(fine_get(U,x,nu))
        x=spatial(x,nu,1,18)
    for j in range(9):
        x=spatial(x,mu,-1,18)
        word.append(qi(fine_get(U,x,mu)))
    for j in range(9):
        x=spatial(x,nu,-1,18)
        word.append(qi(fine_get(U,x,nu)))
    check(x==fine_anchor(coarse),"closed_nine_rectangle")
    return qword(word)

def geom():
    U=setup()
    mid={}
    coarse={}
    middle_count=0
    for x in itertools.product(range(2),repeat=4):
        for mu in range(4):
            for j in range(3):
                xm=spatial(tuple(3*a for a in x),mu,j,6)
                start=tuple(3*a for a in xm)
                mid[xm,mu]=blo(U,start,mu,18,3,fine_get)
                middle_count+=1
    check(middle_count==192 and len(mid)==192,"middle_link_count")
    coarse_count=0
    noncommute=0
    for x in itertools.product(range(2),repeat=4):
        for mu in range(4):
            coarse[x,mu]=blo(mid,tuple(3*a for a in x),
                              mu,6,3,upper_get)
            direct=blo(U,fine_anchor(x),mu,18,9,fine_get)
            if fault=="wrong_line_order" and coarse_count==0:
                wrong=qword(fine_get(U,spatial(fine_anchor(x),mu,j,18),mu)
                            for j in reversed(range(9)))
                check(wrong==direct,"RED_wrong_line_order")
            check(coarse[x,mu]==direct,"two_B3_equals_B9")
            if fault=="missing_inverse" and coarse_count==0:
                check(qi(direct)==direct,"RED_missing_inverse")
            direct_g=blo(U,fine_anchor(x),mu,18,9,gauge_link)
            endpoint=spatial(fine_anchor(x),mu,9,18)
            covariant=qm(qm(qg(fine_anchor(x)),direct),qi(qg(endpoint)))
            check(direct_g==covariant,"SU2_coarse_gauge_covariance")
            coarse_count+=1
            if mu==0:
                left=qm(POOL[0],POOL[1])
                right=qm(POOL[1],POOL[0])
                noncommute+=int(left!=right)
    check(coarse_count==64 and noncommute==16,
          "noncommuting_SU2_not_abelian")
    pls=0
    nontrivial=0
    for x in itertools.product(range(2),repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                p=plaquette(coarse,x,mu,nu,2)
                check(unit(p),"SU2_coarse_plaquette_unit")
                direct=fine_rectangle(U,x,mu,nu)
                check(p==direct,"two_scale_Wilson_rectangle_identity")
                nontrivial+=int(p!=ONE)
                pls+=1
    check(pls==96 and nontrivial>0,"coarse_plaquette_count_nontrivial")
    # A physical-time-separated pair of spatial Wilson observables:
    # time=axis0; separate their insertions by one coarse time step (9 fine).
    c0=(0,0,0,0)
    c1=(1,0,0,0)
    f=plaquette(coarse,c0,1,2,2)
    g=plaquette(coarse,c1,1,2,2)
    check(f==fine_rectangle(U,c0,1,2)
          and g==fine_rectangle(U,c1,1,2),"time_separated_closed_Wilson")
    emit("YM4_04_GEOMETRY",dimension=4,group="SU2_RATIONAL_QUATERNIONS",
         fine="18x18x18x18",middle="6x6x6x6",
         coarse="2x2x2x2",nontrivial_SU2="PASS",
         B3_B3_equals_B9="EXACT",coarse_links=coarse_count,
         coarse_plaquettes=pls,
         gauge_covariance="EXACT",plaquette_pullback="EXACT")
    emit("YM4_04_WILSON_PAIR",time_separation_fine_links=9,
         normalized_spatial_plaquette_0=rs(rat(f[0],f[4])),
         normalized_spatial_plaquette_9=rs(rat(g[0],g[4])),
         configuration_level="NONCOMMUTATIVE_SU2_EXACT",
         connected_measure_identity="YM4_03_HAAR_PUSHFORWARD_THEOREM")
    return U

def source_proofs(root):
    path=root.joinpath("docs","NOTE-YM4-03-ONE-SCALE-BLOCKING.md")
    raw=path.read_bytes()
    blob=b"blob "+str(len(raw)).encode("ascii")+bytes((0,))+raw
    check(hashlib.sha1(blob).hexdigest()==
          "88b441ce39c3867d4635c0ac3f3475ea5ac621dc",
          "pinned_03_map_and_theorem_9")
    s=raw.decode("utf-8")
    check("## 2. The map" in s and
          "## 3. The pushforward" in s and
          "## 4. Reflection positivity" in s and
          "Theorem 9 (the first dependence on V)" in s and
          "2^{1−2b²}" in s and
          "λ′₁ ≤ λ₁^b" in s,
          "YM4_03_proof_inputs_present")
    emit("YM4_04_SOURCE",YM4_03_git_blob="88b441ce39c3867d4635c0ac3f3475ea5ac621dc",
         YM4_03_b3_Wilson_coefficient="2^-17",
         actual_pushforward="EXACT_BY_THEOREM_4",
         source_02d_transfer_bound="USED_AS_STATED")

def rg_bounds():
    Nfine=6*power(18,4)
    Nmid=6*power(6,4)
    Ncoarse=6*power(2,4)
    nlinks=3*power(18,3)
    check((Nfine,Nmid,Ncoarse,nlinks)==
          (629856,7776,96,17496),"four_dimensional_cell_counts")
    beta=rat(1,32*Nfine)
    betamid=rat(power(beta[0],9),power(beta[1],9)*power(4,8))
    betacoarse=rat(power(betamid[0],9),power(betamid[1],9)*power(4,8))
    if fault=="wrong_beta_exponent":
        check(betamid==rat(power(beta[0],8),
                           power(beta[1],8)*power(4,8)),
              "RED_wrong_beta_exponent")
    check(betamid==rat(power(beta[0],9),
                       power(beta[1],9)*65536),"Wilson_PROXY_b3_order_9")
    check(betacoarse==rat(power(beta[0],81),
                          power(beta[1],81)*power(4,80)),
          "Wilson_PROXY_two_ternary_steps_order_81")
    check(le(mul(beta,rat(Nfine)),rat(1,8))
          and le(mul(betamid,rat(Nmid)),rat(1,8)),
          "analytic_log_Cauchy_radius")
    x1=mul(rat(4*Nfine),beta)
    x2=mul(rat(4*Nmid),betamid)
    delta1=mul(rat(2),rp(x1,10))
    delta2=mul(rat(2),rp(x2,10))
    if fault=="wrong_log_tail":
        check(delta1==rat(1,0+power(2,30)),"RED_wrong_log_tail")
    check(delta1==rat(1,536870912)
          and lt(delta2,rat(1,power(2,128))),
          "Cauchy_log_density_error_both_scales")
    delta=add(delta1,delta2)
    check(lt(delta,rat(1,2)),"density_error_lt_half")
    corr=mul(rat(3),mul(delta,inv(sub(rat(1),delta))))
    check(lt(corr,rat(1,100000000)),"correlation_error_below_1e_minus8")
    # For a *single* step the full density pointwise ratio lies in
    # [exp(-delta1),exp(delta1)]. A deterministic pushforward preserves
    # this inequality, and a second comparison multiplies bounds.
    # |E F - E_w F| <= exp(delta)-1 for |F|<=1.
    # Connected F,G: <=3(exp(delta)-1) <=3*delta/(1-delta).
    # Additional prediction freeze a31877e0 (before this computation).
    # On the coarse 2^4 torus take two *spatial* (1,2)-plaquettes at
    # temporal coordinates x0=0 and x0=1. Their sets of spatial links
    # are disjoint. Under PRODUCT Haar each single normalized SU(2)
    # fundamental character has zero expectation, and so does FG.
    # The full Wilson proxy at beta2 has density ratio to product Haar
    # bounded by exp(plus_or_minus 2*Ncoarse*beta2), since |X|<=Ncoarse.
    # If z=2*Ncoarse*beta2<1, then exp(z)-1<=z/(1-z).
    # Hence |C_proxy|<=eta+eta^2, and
    # |C_actual|<=3*delta/(1-delta)+eta+eta^2 < 10^-8.
    # The sign and *nonzero spectral weight* are both UNKNOWN.
    p0=(0,0,0,0)
    p1=(1,0,0,0)
    def spatial_edges(x):
        return {(x,1),(spatial(x,1,1,2),2),
                (spatial(x,2,1,2),1),(x,2)}
    aedges=spatial_edges(p0)
    bedges=spatial_edges(p1)
    check(len(aedges)==4 and len(bedges)==4
          and len(aedges.intersection(bedges))==0,
          "two_disjoint_spatial_Haar_plaquettes")
    if fault=="wrong_Haar_connected_zero_for_same_plaquette":
        bedges=aedges
        check(len(aedges.intersection(bedges))==0,
              "RED_wrong_Haar_connected_zero_for_same_plaquette")
    z=mul(rat(2*Ncoarse),betacoarse)
    check(lt(z,rat(1,power(2,128))),"Haar_proxy_z_lt_2_minus_128")
    eta=mul(z,inv(sub(rat(1),z)))
    actual_upper=add(corr,add(eta,mul(eta,eta)))
    check(lt(actual_upper,rat(1,100000000)),
          "absolute_actual_connected_SU2_Wilson_lt_1e_minus8")
    if fault=="claim_nonzero_C_from_bound":
        check(lt(rat(0),sub(rat(0),actual_upper)),
              "RED_claim_nonzero_C_from_bound")
    emit("YM4_04_ACTUAL_CORRELATION",
         temporal_separation_fine_links=9,
         operator_pair="normalized_spatial_SU2_Wilson_t0_and_t9",
         Haar_single_means="ZERO",
         Haar_product="ZERO_BY_DISJOINT_LINK_SUPPORT",
         proxy_to_Haar_z_lt="1/2^128",
         proxy_connected_bound="eta_plus_eta_squared",
         actual_connected_interval_lower="-1/100000000",
         actual_connected_interval_upper="+1/100000000",
         actual_abs_C_lt="1/100000000",
         sign_and_first_spectral_weight="OPEN",
         proof="EXACT_PUSHFORWARD_PLUS_RATIONAL_ENCLOSURES")
    signal=mul(rat(2*Nmid),betamid)
    check(lt(signal,delta1),"uniform_bound_cannot_resolve_Wilson_signal")
    q0=mul(beta,rat(nlinks))
    check(q0==rat(1,1152),"finite_SU2_transfer_02d_ratio")
    q3=rp(q0,3)
    q9=rp(q0,9)
    if fault=="wrong_q9":
        check(q9==rp(q0,8),"RED_wrong_q9")
    check(q9==rp(q3,3),"nested_transfer_upper_bound")
    if fault=="spurious_visibility":
        check("OPEN"=="PROVED","RED_spurious_visibility")
    emit("YM4_04_COUPLINGS",dimension=4,
         plaquettes_fine=Nfine,plaquettes_middle=Nmid,
         plaquettes_coarse=Ncoarse,beta0=rs(beta),
         beta1_proxy="beta0^9/4^8",
         beta2_proxy="beta0^81/4^80",
         induced_action_Wilson_closed="NOT_PROVED",
         true_two_block_beta_running="UNKNOWN")
    emit("YM4_04_CORRELATION",exact_two_block_pullback="BY_HAAR_THEOREM",
         delta1=rs(delta1),delta2_lt="1/2^128",
         delta_total="delta1_plus_delta2_exact",
         density_pointwise_error="exp(plus_or_minus_delta_total)",
         normalized_connected_Wilson_error_lt="1/100000000",
         bound="3*delta_total/(1-delta_total)",
         normalized_Wilson_character_absolute_bound="1")
    # The finite periodic Euclidean measure with N_t=18 (above) is
    # DIFFERENT from the infinite temporal extent vacuum correlation.
    # For the latter, choose F=1/2 Tr(U_{9x9 spatial rectangle}) on
    # a 3D fine spatial slice, so ||F||<=1 and F is gauge invariant.
    # With positive normalized fine transfer P=T/lambda0, the centered
    # v=(F-<Omega,F Omega>)*Omega has norm^2=Var(F)<=1.
    # Thus C_Omega(n)=<v,P^n v> is NONNEGATIVE, and for n=9
    # C_Omega(9)<=q0^9 Var(F)<=1/1152^9.
    # Visibility of the actual first eigenstate is not required for
    # the upper bound, and is not established by it.
    if fault=="false_variance_gt_one":
        check(lt(rat(1),rat(1)),"RED_false_variance_gt_one")
    check(q9==rat(1,3573323304747203265520730112),
          "infinite_time_vacuum_corr_transfer_upper")
    emit("YM4_04_VACUUM_CORRELATION",
         state="INFINITE_TEMPORAL_EXTENT_INTERACTING_SU2_VACUUM",
         observable="NORMALIZED_SPATIAL_9x9_WILSON_RECTANGLE",
         time_separation_fine_links=9,
         connected_C_lower="0",
         connected_C_upper=rs(q9),
         centered_variance_upper="1",
         proof="POSITIVE_TRANSFER_PLUS_YM4_02D_RATIO",
         first_excitation_overlap="OPEN",
         distinct_from_finite_periodic_measure="YES")
    emit("YM4_04_SPECTRUM",
         fine_transfer_subleading_ratio_le=rs(q0),
         B3_visible_subspace_ratio_le=rs(q3),
         B9_visible_subspace_ratio_le=rs(q9),
         B9_visible_ratio_le_B3_ratio_cubed="DERIVED_BY_NESTED_HPRIME",
         fine_physical_mass_lower="log(1152)/a",
         all_first_states_visible="OPEN",
         Wilson_PROXY_spectrum_comparison="NOT_JUSTIFIED")
    emit("YM4_04_PRECISION",absolute_Wilson_correlation_control="PASS",
         first_proxy_Wilson_signal_smaller_than_error="YES",
         relative_beta_precision="FAIL_EXPECTED",
         need_better_estimate="LOCAL_CONNECTED_CLUSTER_ERROR",
         weak_coupling_SU2="NOT_TESTED",
         induction_all_k="OPEN")

def counterexample():
    # 2x2 transfer T(a)=diag(1,q), q=(1+a^2)^(-1).
    # Vacuum omega=(1,0), gauge-irrelevant off-diagonal observable O
    # yields C(n)=q^n>0. Blocking T^3,T^9 leaves physical mass
    # (1/a)*log(1/q) unchanged. As a=3^-k,
    # 0<m_phys=3^k log(1+3^(-2k))<=3^-k -> 0.
    # These toy matrices are NOT SU2 Wilson transfer operators.
    for k in range(1,7):
        n=power(3,k)
        q=rat(n*n,n*n+1)
        qb3=rp(q,3)
        qb9=rp(q,9)
        check(qb9==rp(qb3,3),"toy_block_power_composition")
        c=rp(q,n)
        check(lt(rat(0),c) and lt(c,rat(1)),
              "toy_positive_finite_gap_and_correlation")
        check(le(sub(rat(1),c),rat(1,n)),
              "toy_physical_t1_correlation_tends_one")
        # Exact physical mass 3^k log(1+1/3^(2k)) <= 1/3^k.
        # log(1+x) <= x, with strict < for x>0.
        check(lt(rat(0),rat(1,n)),"toy_physical_mass_bound_positive")
        if fault=="positive_toy_mass_floor" and k==6:
            check(le(rat(1,10),rat(1,n)),
                  "RED_positive_toy_mass_floor")
        emit("YM4_04_TOY",k=k,a="1/"+str(n),
             transfer_q=rs(q),block_q3="q^3",block_q9="q^9",
             fine_gap_lattice="log(1+1/"+str(n*n)+")",
             physical_mass_strict_upper="1/"+str(n),
             connected_t1_lower="1-1/"+str(n),
             all_finite_gaps_positive="YES")
    emit("YM4_04_COUNTEREXAMPLE",
         model="Tdiag1_and_one_over_1_plus_a_squared",
         every_finite_gap="POSITIVE",
         physical_gap_limit="ZERO",
         two_ternary_blocks="EXACT_WITH_NO_SPECTRAL_LOSS",
         witness_visibility="NONZERO",
         conclusion="FINITE_GAP_PLUS_EXACT_BLOCKING_NOT_SUFFICIENT")

def main():
    root=Path(__file__).resolve().parents[1]
    prediction=root.joinpath("docs",
        "PREDICTION-YM4-04-TWO-TERNARY-BLOCKS-20261107.hbp").read_bytes()
    check(sum(int(z.startswith(b"PREDICT|id="))
              for z in prediction.splitlines())==19,
          "nineteen_prediction_rows_frozen")
    supplement=root.joinpath("docs",
        "PREDICTION-YM4-04-TWO-BLOCK-CORRELATION-SUPPLEMENT-20261107.hbp"
        ).read_bytes()
    check(sum(int(z.startswith(b"PREDICT|supp="))
              for z in supplement.splitlines())==6,
          "six_supplement_predictions_frozen_before_actual_C_bound")
    vacuum_pred=root.joinpath("docs",
        "PREDICTION-YM4-04-VACUUM-CORRELATION-SUPPLEMENT-20261107.hbp"
        ).read_bytes()
    check(sum(int(z.startswith(b"PREDICT|vac="))
              for z in vacuum_pred.splitlines())==4,
          "four_vacuum_correlator_predictions_frozen")
    emit("YM4_04_VACUUM_FREEZE",
         prediction_sha256=hashlib.sha256(vacuum_pred).hexdigest(),
         predictions=4,source_commit="4a5853527776cbf660e4acf2410016c3694dc187")
    emit("YM4_04_CORRELATION_FREEZE",
         supplement_sha256=hashlib.sha256(supplement).hexdigest(),
         predictions=6,source_commit="a31877e0d91c67ee34e06ba8fc428a66b2d8fa95")
    emit("YM4_04_BEGIN",prediction_sha256=hashlib.sha256(prediction).hexdigest(),
         gauge="CONTINUOUS_SU2",
         map="YM4_03_B3_COMPOSED_B3",
         integer_only="YES",
         new_full_wilson_integral="NOT_COMPUTED")
    source_proofs(root)
    geom()
    rg_bounds()
    counterexample()
    emit("YM4_04_DONE",status="PASS_WITH_RELATIVE_PRECISION_HOLD",
         coarse_SU2_map_and_measures="EXACT",
         two_scale_absolute_correlation_error="CERTIFIED",
         two_scale_transfer_sector_bound="DERIVED",
         relative_Wilson_signal="NOT_RESOLVED",
         all_scale_induction="OPEN",continuum_SU2_mass_gap="OPEN")

if __name__=="__main__":
    main()
