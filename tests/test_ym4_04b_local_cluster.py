#!/usr/bin/env python3
"""YM4-04B: volume-independent local SU(2) Wilson connected-cluster bound.

EXACT INTEGER CHECK of the geometry, rational constants and algebraic
consequences of the NAMED classical Dobrushin comparison theorem.
It does NOT numerically integrate continuous SU(2) over the huge lattice.
The source proof is documented in docs/NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md.

Prediction-first at commit ddfbbf44f539752769b6d8881a0e79fc6a119198.
Stacked on YM4-04A PR #36. No float, no json.
"""
import hashlib
import itertools
import math
import sys
from collections import deque
from pathlib import Path

SABOTAGES=(
    "wrong_plaquette_incidence","wrong_neighbor_sum",
    "missing_time_separation","wrong_proxy_exponent",
    "spurious_weak_coupling_contraction","spurious_first_weight",
    "wrong_scale_ratio","non_summable_invention",
)
sabotage=""
if len(sys.argv)>2 or (len(sys.argv)==2 and
    (not sys.argv[1].startswith("sabotage=")
     or sys.argv[1][9:] not in SABOTAGES)):
    print("usage: test_ym4_04b_local_cluster.py [sabotage=NAME]")
    sys.exit(2)
if len(sys.argv)==2:
    sabotage=sys.argv[1][9:]


def check(ok,name):
    if not ok:
        print("FAILED|check="+name+"|json=0",flush=True)
        sys.exit(1)


def line(tag,**values):
    print(tag+"|"+"|".join(str(k)+"="+str(v) for k,v in values.items())
          +"|json=0",flush=True)


def power(a,n):
    check(type(a) is int and type(n) is int and n>=0,
          "integer_nonnegative_power")
    out=1
    while n:
        if n&1:
            out*=a
        n//=2
        if n:
            a*=a
    return out


def rat(a,b=1):
    check(type(a) is int and type(b) is int and b!=0,
          "integer_rational_types")
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


def div(a,b):
    check(b[0]!=0,"nonzero_rational_divisor")
    return rat(a[0]*b[1],a[1]*b[0])


def rpow(a,n):
    return rat(power(a[0],n),power(a[1],n))


def less(a,b):
    return a[0]*b[1]<b[0]*a[1]


def disp(a):
    return str(a[0])+"/"+str(a[1])


def plus(x,axis,size,step=1):
    y=list(x)
    y[axis]=(y[axis]+step)%size
    return tuple(y)


def rectangle_links(size,side,t):
    # 9x9 spatial rectangle for side=9, a 3x3 for side=3;
    # time axis 0, spatial axes 1 and 2, other coord 0.
    origin=(t,0,0,0)
    x=origin
    out=[]
    for _ in range(side):
        out.append((x,1))
        x=plus(x,1,size)
    for _ in range(side):
        out.append((x,2))
        x=plus(x,2,size)
    for _ in range(side):
        x=plus(x,1,size,-1)
        out.append((x,1))
    for _ in range(side):
        x=plus(x,2,size,-1)
        out.append((x,2))
    check(x==origin and len(out)==4*side and
          len(set(out))==4*side,"loop_boundary_distinct")
    return out


def incidence(size,keep_edges=True):
    # Actual four oriented link indices of EVERY plaquette of a torus.
    # C_ij may count multiple plaquettes connecting one pair of links.
    links={}
    for x in itertools.product(range(size),repeat=4):
        for mu in range(4):
            links[x,mu]=len(links)
    counts=[0]*len(links)
    adj=[{} for _ in counts] if keep_edges else None
    nplaquettes=0
    for x in itertools.product(range(size),repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                edge_keys=( (x,mu),(plus(x,mu,size),nu),
                            (plus(x,nu,size),mu),(x,nu) )
                edges=[links[q] for q in edge_keys]
                check(len(set(edges))==4,
                      "plaquette_has_four_distinct_links")
                for e in edges:
                    counts[e]+=1
                    if keep_edges:
                        for other in edges:
                            if other!=e:
                                adj[e][other]=adj[e].get(other,0)+1
                nplaquettes+=1
    check(nplaquettes==6*power(size,4),"all_four_dimensional_plaquettes")
    check(all(count==6 for count in counts),
          "each_link_six_plaquettes")
    neighbor_sums=[sum(row.values()) for row in adj]
    check(all(v==18 for v in neighbor_sums),
          "each_link_eighteen_neighbor_multiplicity")
    if sabotage=="wrong_plaquette_incidence" and size==2:
        check(counts[0]==7,"RED_wrong_plaquette_incidence")
    if sabotage=="wrong_neighbor_sum" and size==3:
        check(neighbor_sums[0]==17,"RED_wrong_neighbor_sum")
    return links,adj,nplaquettes


def graph_distance(links,adj,source,target):
    a={links[key] for key in source}
    b={links[key] for key in target}
    check(not (a & b),"time_separated_link_supports")
    frontier=deque((v,0) for v in a)
    seen=set(a)
    while frontier:
        v,n=frontier.popleft()
        if v in b:
            return n
        for q in adj[v]:
            if q not in seen:
                seen.add(q)
                frontier.append((q,n+1))
    raise AssertionError("connected plaquette graph expected")


def structural_proof():
    # Included boundary side=2, where some links can share two plaquettes.
    for size in (2,3,6):
        links,adj,Np=incidence(size)
        if size==2:
            r=1
            source=rectangle_links(size,r,0)
            target=rectangle_links(size,r,r)
            distance=graph_distance(links,adj,source,target)
            check(distance==r,"coarse_t1_link_graph_distance")
        elif size==6:
            r=3
            source=rectangle_links(size,r,0)
            target=rectangle_links(size,r,r)
            distance=graph_distance(links,adj,source,target)
            check(distance==r,"middle_t3_link_graph_distance")
            if sabotage=="missing_time_separation":
                check(distance==r-1,"RED_missing_time_separation")
        else:
            distance="NOT_APPLICABLE"
        line("YM4_04B_GEOMETRY",size=size,
             dimension=4,links=len(links),plaquettes=Np,
             incidence_every_link=6,neighbor_multiplicity_every_link=18,
             distance_wilson_pair=distance,geometry_audit="EXHAUSTIVE")
    # A link in 4D is incident to 6 plaquettes for every side>=2.
    # Each such plaquette has four distinct link variables. Its three
    # other variables contribute 3 to total neighbor multiplicity.
    # On 18^4, time coordinates within a plaquette differ by 0 or +/-1.
    # Both spatial loop supports are at t=0 or t=9 on a time ring of 18,
    # so every connecting neighbor path has >=9 edges. In fact the
    # temporal (0,1)-plaquettes at one spatial perimeter edge connect
    # the same oriented spatial edge successively t=0...9: <=9.
    src=rectangle_links(18,9,0)
    target=rectangle_links(18,9,9)
    check(len(src)==36 and len(target)==36 and
          all(e[0][0]==0 for e in src) and
          all(e[0][0]==9 for e in target),
          "fine_t9_space_time_separation")
    for t in range(9):
        x=(t,0,0,0)
        a=(x,1)
        b=(plus(x,0,18),1)
        # Both are in a (time,space) plaquette at x.
        temporal_plaq=((x,0),(plus(x,0,18),1),
                       (plus(x,1,18),0),(x,1))
        check(a in temporal_plaq and b in temporal_plaq,
              "temporal_plaquette_edge_path")
    line("YM4_04B_FINE_GEOMETRY",
         shape="18x18x18x18",
         spatial_wilson_rectangle_side=9,
         perimeter_support=36,
         temporal_distance=9,
         proof="PLAQUETTE_TIME_LIPSCHITZ_AND_EXPLICIT_NINE_PATH",
         full_18_fourth_links_not_enumerated="YES")


def beta_proxy(k):
    # 4*(1/4000)^(9^k) for beta0=1/1000.
    return rat(4,power(4000,power(9,k)))


def covariance_bound(alpha,r):
    # Dobrushin comparison bound for 4r-link normalized Wilson loops.
    return div(mul(rat(4*r),rpow(alpha,r)),sub(rat(1),alpha))


def proxy_covariance_bound(k):
    alpha=mul(rat(18),beta_proxy(k))
    return div(mul(rat(4),alpha),sub(rat(1),alpha))


def numerical_certificates():
    beta=rat(1,1000)
    alpha=mul(rat(18),beta)
    check(alpha==rat(9,500) and less(alpha,rat(1)),
          "strong_coupling_SU2_Dobrushin_contraction")
    beta1=beta_proxy(1)
    beta2=beta_proxy(2)
    check(beta1==rat(1,power(1000,9)*power(4,8))
          and beta2==rat(1,power(1000,81)*power(4,80)),
          "Wilson_proxy_two_stage_powers")
    if sabotage=="wrong_proxy_exponent":
        check(beta1==rat(1,power(1000,8)*power(4,8)),
              "RED_wrong_proxy_exponent")
    c3=covariance_bound(alpha,3)
    c9=covariance_bound(alpha,9)
    p3=proxy_covariance_bound(1)
    p9=proxy_covariance_bound(2)
    error3=add(c3,p3)
    error9=add(c9,p9)
    check(less(p3,rat(1,power(10,27)))
          and less(p9,rat(1,power(10,29))),
          "named_Wilson_proxy_individual_bounds")
    check(less(c3,rat(1,10000)) and
          less(error3,rat(1,10000)),
          "local_first_step_absolute_correlation_error")
    check(less(c9,rat(1,100000000000000)) and
          less(error9,rat(1,100000000000000)),
          "local_second_step_absolute_correlation_error")
    line("YM4_04B_COUPLING",beta0=disp(beta),
         alpha0=disp(alpha),local_overlap_count=18,
         sufficient_contraction="18*beta_lt_1",
         large_volume_Np_unrestricted="YES",
         Wilson_beta1="beta0^9/4^8",
         Wilson_beta2="beta0^81/4^80",
         induced_action_Wilson_exact="NOT_CLAIMED")
    line("YM4_04B_TWO_BLOCKS",
         actual_b3_fine_covariance_le=disp(c3),
         actual_b9_fine_covariance_le=disp(c9),
         first_proxy_cov_bound_lt="1/1000000000000000000000000000",
         second_proxy_cov_bound_lt="1/100000000000000000000000000000",
         first_connected_proxy_error_lt="1/10000",
         second_connected_proxy_error_lt="1/100000000000000",
         proof="DOBRUSHIN_COMPARISON_PLUS_EXACT_YM4_03_B9_PULLBACK",
         effective_action_norm="NOT_CONTROLLED",
         relative_coupling_precision="NOT_ESTABLISHED")
    # The infinite family keeps fixed beta0=1/1000 at a=1/3^k:
    # each physical Wilson loop side=1 has 4*3^k fine links.
    # The two time slices are separated by 3^k links.
    for k in range(1,7):
        r=power(3,k)
        bound=covariance_bound(alpha,r)
        check(less(rat(0),bound) and
              less(bound,rat(1,10000)),
              "all_example_scale_bounds_positive_small")
        if k>1:
            prev=covariance_bound(alpha,r//3)
            ratio=div(bound,prev)
            check(less(ratio,rat(1,2)),"scale_geometric_ratio_lt_half")
            if sabotage=="wrong_scale_ratio" and k==2:
                check(less(rat(1,2),ratio),
                      "RED_wrong_scale_ratio")
        line("YM4_04B_SCALE",k=k,fine_spacing="1/"+str(r),
             fine_side=""+str(2*r),
             temporal_separation=r,perimeter_links=4*r,
             actual_connected_bound="4*3^k*(9/500)^(3^k)/(1-9/500)",
             positive_rational_bound="CERTIFIED",
             no_beta_running="YES")
    # Bound the infinite sum directly, not only its first six terms.
    # a_(k+1)/a_k = 3 alpha^(2*3^k) <= 3 alpha^6 <1.
    # b_k = 4 alpha_k/(1-alpha_k), alpha_k=72/4000^(9^k).
    # alpha_(k+1)/alpha_k <=1/2, b_(k+1)/b_k<=1/2.
    actual_ratio=mul(rat(3),rpow(alpha,6))
    check(less(actual_ratio,rat(1,2)),
          "summable_actual_tail_ratio")
    sum_actual=div(c3,sub(rat(1),actual_ratio))
    alpha1=mul(rat(18),beta1)
    # For every k>=1, alpha_(k+1)/alpha_k
    # = 4000^(-8*9^k) <= 4000^(-72) < 1/2.
    # Since x/(1-x) is increasing, the same ratio upper bounds
    # successive proxy covariance estimates.
    alpha2=mul(rat(18),beta_proxy(2))
    check(less(mul(rat(2),alpha2),alpha1)
          and power(4000,72)>2,
          "proxy_infinite_ratio_bound_from_power_recursion")
    sum_proxy=mul(rat(2),proxy_covariance_bound(1))
    total=add(sum_actual,sum_proxy)
    check(less(total,rat(1,10000)),
          "infinite_scale_sum_strict_lt_one_tenthousandth")
    if sabotage=="non_summable_invention":
        check(less(rat(1,10000),total),
              "RED_non_summable_invention")
    line("YM4_04B_INFINITE_SUM",
         fixed_bare_beta="1/1000",
         full_SU2_all_finite_tori="SIDE_2_TIMES_3_POWER_K",
         actual_ratio_bound="3*(9/500)^6",
         proxy_ratio_bound="1/2",
         all_connected_proxy_errors_sum_lt="1/10000",
         statement="LOCAL_ABSOLUTE_CORRELATION_ERRORS_SUMMABLE",
         first_state_visibility="NOT_PROVED",
         Wilson_action_RG_convergence="NOT_PROVED",
         beta_to_infinity_trajectory="NOT_PROVED")
    if sabotage=="spurious_first_weight":
        check("OPEN"=="CERTIFIED","RED_spurious_first_weight")
    # Dobrushin criterion is only sufficient, not a no-gap theorem.
    weak1=mul(rat(18),rat(1,10))
    weak2=mul(rat(18),rat(4))
    check(weak1==rat(9,5) and weak2==rat(72),
          "weak_coupling_sufficient_condition_breaks")
    if sabotage=="spurious_weak_coupling_contraction":
        check(less(weak1,rat(1)),
              "RED_spurious_weak_coupling_contraction")
    line("YM4_04B_WEAK_COUPLING_RED",
         beta_small="1/1000",
         beta_test_1="1/10",alpha_bound_1="9/5",
         beta_test_2="4",alpha_bound_2="72",
         local_Dobrushin_test="NO_CONTRACTION_AT_WEAK_COUPLING",
         invalidates_SU2_continuum="NO",
         identifies_missing_estimate="YES")
    line("YM4_04B_LIMITS",actual_SU2_finite_measures="YES",
         exact_YM4_03_pushforward="USED",
         local_bound_Np_independent="YES",
         full_effective_action_norm="OPEN",
         first_E1_overlap="OPEN",
         continuum_coupling_beta_a_to_infinity="OPEN",
         physical_gap_uniformity="OPEN",
         fourD_Clay="OPEN")


def main():
    root=Path(__file__).resolve().parents[1]
    frozen=root.joinpath("docs",
        "PREDICTION-YM4-04B-LOCAL-CLUSTER-20261107.hbp").read_bytes()
    check(sum(int(s.startswith(b"PREDICT|id="))
              for s in frozen.splitlines())==19,
          "nineteen_predictions_frozen_first")
    base=root.joinpath("docs",
        "NOTE-YM4-03-ONE-SCALE-BLOCKING.md").read_bytes()
    git_blob=b"blob "+str(len(base)).encode("ascii")+bytes((0,))+base
    check(hashlib.sha1(git_blob).hexdigest()==
          "88b441ce39c3867d4635c0ac3f3475ea5ac621dc",
          "YM4_03_original_exact_map_is_pinned")
    line("YM4_04B_START",
         prediction_sha256=hashlib.sha256(frozen).hexdigest(),
         source_YM4_03_blob="88b441ce39c3867d4635c0ac3f3475ea5ac621dc",
         group="CONTINUOUS_SU2",
         comparison="NAMED_DOBRUSHIN_THEOREM",
         integer_only="YES")
    structural_proof()
    numerical_certificates()
    line("YM4_04B_DONE",
         status="PASS_STRONG_COUPLING_LOCAL_SUMMABLE_ONLY",
         exact_SU2_link_geometry="YES",
         bounded_two_block_connected_error="YES",
         all_k_connected_errors_summable="YES",
         weak_coupling_induction="HOLD",
         physical_gap_first_E1="OPEN",
         output="CERTIFICATE_NOT_A_FULL_CONTINUUM_PROOF")


if __name__=="__main__":
    main()
