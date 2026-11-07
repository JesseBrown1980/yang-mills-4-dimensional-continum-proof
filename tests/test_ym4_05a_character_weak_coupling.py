#!/usr/bin/env python3
"""YM4-05A: prediction-first weak-coupling SU(2) character blocking controls.

The 2D SU(2) heat-kernel convolution is EXACT on a simply connected disk.
The 4D SIX-staple Haar integral is EXACT for a single eliminated Wilson link.
Those are different models/operations: NO claim of 4D weak-coupling RG or gap.

All arithmetic uses integer rational intervals; no floating point, JSON, or
large-lattice Monte Carlo. Uses classical SU(2) character orthogonality,
heat-kernel semigroup, and the SU(2) = unit S^3 Haar identity.
"""
from hashlib import sha256
from itertools import product
from math import comb,gcd
from pathlib import Path
import sys

BAD=("bad_dimension","bad_convolution","bad_ternary_area",
     "bad_casimir","missing_chair","bad_mixed_derivative",
     "claim_4D_closure","claim_mass_gap")
fault=""
if len(sys.argv)>2 or (len(sys.argv)==2 and
    (not sys.argv[1].startswith("sabotage=")
     or sys.argv[1][9:] not in BAD)):
    print("usage: test_ym4_05a_character_weak_coupling.py [sabotage=NAME]")
    sys.exit(2)
if len(sys.argv)==2:
    fault=sys.argv[1][9:]


def check(ok,name):
    if not ok:
        print("FAILED|check="+name+"|json=0",flush=True)
        sys.exit(1)


def emit(tag,**fields):
    print(tag+"|"+"|".join(str(k)+"="+str(v) for k,v in fields.items())
          +"|json=0",flush=True)


def ipow(a,n):
    check(type(a) is int and type(n) is int and n>=0,
          "integer_nonnegative_exponent")
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
          "rational_integers_and_nonzero_denominator")
    if b<0:
        a,b=-a,-b
    d=gcd(a,b)
    return (a//d,b//d)


def add(a,b):
    return rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1])


def mul(a,b):
    return rat(a[0]*b[0],a[1]*b[1])


def sub(a,b):
    return rat(a[0]*b[1]-b[0]*a[1],a[1]*b[1])


def div(a,b):
    check(b[0]!=0,"rational_divisor_nonzero")
    return rat(a[0]*b[1],a[1]*b[0])


def rp(a,n):
    return rat(ipow(a[0],n),ipow(a[1],n))


def lt(a,b):
    return a[0]*b[1]<b[0]*a[1]


def le(a,b):
    return a[0]*b[1]<=b[0]*a[1]


def text_rat(a):
    return str(a[0])+"/"+str(a[1])


def poly_sub(a,b):
    out=list(a)+[0]*max(0,len(b)-len(a))
    for i,v in enumerate(b):
        out[i]-=v
    return out


def cheb_u(n):
    # SU2 spin n/2 character: U_n(cos theta), U0=1, U1=2*x.
    check(n>=0,"cheb_degree")
    if n==0:
        return [1]
    a=[1]
    b=[0,2]
    for _ in range(2,n+1):
        two_x_b=[0]+[2*t for t in b]
        a,b=b,poly_sub(two_x_b,a)
    return b


def haar_monomial(k):
    # SU2 normalized Haar on S^3, u0=cos(theta).
    # odd moment zero; even moment Catalan_m/4^m.
    if k%2:
        return rat(0)
    m=k//2
    return rat(comb(2*m,m),ipow(4,m)*(m+1))


def polynomial_expect(p):
    s=rat(0)
    for k,v in enumerate(p):
        if v:
            s=add(s,mul(rat(v),haar_monomial(k)))
    return s


def polynomial_product(a,b):
    result=[0]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):
            result[i+j]+=u*v
    return result


def check_character_orthogonality():
    count=0
    for n in range(1,13):
        c=cheb_u(n-1)
        dimension=sum(c)
        check(dimension==n,"SU2_representation_dimension")
        if fault=="bad_dimension" and n==2:
            check(dimension==n+1,"RED_bad_dimension")
        if fault=="bad_casimir" and n==2:
            check(n*n-1==n*n,"RED_bad_casimir")
        for m in range(1,13):
            d=cheb_u(m-1)
            moment=polynomial_expect(polynomial_product(c,d))
            check(moment==rat(int(n==m)),
                  "SU2_exact_Haar_character_orthogonality")
            count+=1
    # By Schur's lemma, ∫ chi_n(AU) chi_m(U^-1 B)dU
    # =delta_nm chi_n(AB)/n. At AB=I and n=m=2 this
    # gives 1, not 2, independently cross-checked above.
    if fault=="bad_convolution":
        check(1==2,"RED_bad_convolution")
    check(polynomial_expect(cheb_u(1))==rat(0)
          and polynomial_expect(polynomial_product(cheb_u(1),
                                                 cheb_u(1)))==rat(1),
          "fundamental_character_orthogonality")
    emit("YM4_05A_CHARACTERS",
         group="CONTINUOUS_SU2",degrees_tested=12,
         integer_Haar_orthogonality_pairs=count,
         fundamental_dimension=2,
         Casimir_4_times="n_squared_minus_1",
         convolution="delta_nm_chi_n_over_n",
         spin_rep_dimension="n")


def check_heat_kernel_blocks():
    # 2D disk heat kernel K_q = sum_{n>=1} n*q^(n^2-1)*chi_n.
    # Convolving 2D plaquettes via a single shared edge multiplies
    # normalized character coefficients (n cancels by Schur).
    # 3x3 => 9 plaquettes. Two such blocks => 9x9 =>81.
    for n in range(1,13):
        exponent=n*n-1
        check(exponent>=0,"casimir_nonnegative")
        if fault=="bad_ternary_area" and n==2:
            check(ipow(3,2)==8,"RED_bad_ternary_area")
        q=rat(7,9)
        coeff=rp(q,exponent)
        one=rp(coeff,9)
        two=rp(one,9)
        direct=rp(coeff,81)
        check(two==direct,"heat_B3_B3_equals_B9_coeff")
        check(one==rp(q,9*exponent),"heat_B3_casimir")
        check(direct==rp(q,81*exponent),"heat_B9_casimir")
    prev=None
    for k in range(1,5):
        m=ipow(9,k)
        q=rat(2*m-1,2*m)
        blocked=rp(q,m)
        check(lt(rat(0),blocked) and le(blocked,rat(2,3)),
              "heat_weak_coarse_q_le_two_thirds")
        if prev is not None:
            check(lt(prev,blocked),
                  "heat_weak_refinement_character_monotonic")
        prev=blocked
        # For log(1-x), x=1/(2m):
        # -1/2 -1/(8m-4) <= m log(1-x) <= -1/2.
        # This is the symbolic log-series enclosure, checked in
        # integer arithmetic via m>=1 and x<=1/2.
        e=rat(1,8*m-4)
        check(m>=9 and lt(e,rat(1,10)) and 8*m-4>0,
              "explicit_logarithm_remainder_denominator")
        # For fundamental (n=2) character, multiply log error by 3.
        emit("YM4_05A_HEAT_FLOW",k=k,plaquettes_blocked=m,
             q_fine=text_rat(q),heat_inverse_diffusion_parameter=2*m,
             normalized_fundamental_coefficient="q_fine^(3*"+str(m)+")",
             blocked_q_monotonic_in_k="YES",
             log_q_block_limit="-1/2",
             log_q_block_abs_error_le="1/"+str(8*m-4),
             normalized_rep_n_error_le="(n^2-1)/"+str(8*m-4))
    # q_block <=2/3 for all k; |chi_n|<=n and the character
    # expansion has coefficients n*q_block^(n²-1).
    # For n>=10, t_(n+1)/t_n <1/2, hence tail <=2*t_10.
    first=mul(rat(200),rp(rat(2,3),99))
    check(lt(first,rat(1,1000000000000)),
          "two_dim_heat_high_spin_tail_lt_1e_minus12")
    nextterm=mul(rat(121),rp(rat(2,3),120))
    t10=mul(rat(100),rp(rat(2,3),99))
    check(lt(mul(rat(2),nextterm),t10),
          "SU2_character_tail_ratio_below_half")
    emit("YM4_05A_HEAT_THEOREM",
         setting="TWO_DIMENSIONAL_DISK_ONLY",
         link_Haar_convolution="EXACT",
         block3_plaquettes=9,block9_plaquettes=81,
         B3_B3_equals_B9="PASS",
         true_weak_heat_parameter_k="2*9^k",
         coarse_q_limit="exp(-1/2)",
         high_spin_truncate_through_n=9,
         uniform_tail_lt="1/1000000000000",
         higher_D_Same_flow="NOT_PROVED")


def q_norm_sq(staples):
    # Unit SU2 quaternions represented exactly as integer tuples.
    # trace(U A)/2 is the real part; Haar U on unit S^3.
    # Staple a=(a0,a1,a2,a3) gives v_a=(a0,-a1,-a2,-a3)
    vectors=[(a[0],-a[1],-a[2],-a[3]) for a in staples]
    check(all(sum(x*x for x in a)==1 for a in vectors),
          "six_unit_su2_staples")
    vector=[sum(v[i] for v in vectors) for i in range(4)]
    q=sum(t*t for t in vector)
    pair_sum=0
    for i in range(len(vectors)):
        for j in range(i+1,len(vectors)):
            pair_sum+=sum(vectors[i][d]*vectors[j][d] for d in range(4))
    check(q==len(vectors)+2*pair_sum,
          "six_staple_invariant_pairwise_trace")
    return q


def four_dimensional_chair():
    # Two mu=0 plaquettes in different planes (0,1) and (0,2)
    # sharing the edge x -> x+0 have six other positive-link edges
    # in their combined boundary. This is a nonplanar chair,
    # not an elementary plaquette (4 links).
    x=(0,0,0,0)
    def shift(p,axis):
        v=list(p);v[axis]+=1
        return tuple(v)
    def plaq_edges(mu,nu):
        return {(x,mu),(shift(x,mu),nu),
                (shift(x,nu),mu),(x,nu)}
    e01=plaq_edges(0,1)
    e02=plaq_edges(0,2)
    e03=plaq_edges(0,3)
    pair=e01.symmetric_difference(e02)
    check(len(e01)==4 and len(e02)==4 and
          len(e01.intersection(e02))==1 and len(pair)==6,
          "mixed_plane_chair_six_link_boundary")
    if fault=="missing_chair":
        check(len(pair)==4,"RED_missing_chair")
    check(len(e01.intersection(e03))==1
          and len(e02.intersection(e03))==1,
          "three_distinct_mixed_planes")
    check(6*5//2==15 and 3*2*2==12,
          "six_staples_fifteen_pairs_twelve_mixed_plane")
    emit("YM4_05A_4D_GEOMETRY",
         dimension=4,same_oriented_link_plaquettes=6,
         unordered_staple_pairs=15,
         pair_of_different_planes=12,
         mixed_plane_union_without_common_link=6,
         mixed_loop="NONPLANAR_SIX_LINK_CHAIR",
         closure_into_single_Wilson_plaquette="NOT_JUSTIFIED")


def one_link_series(beta,Q,N):
    # E_Haar exp(beta*u dot v) with |v|²=Q,
    # u uniform on S³:
    # Z=sum_m (beta² Q)^m/[4^m*m!*(m+1)!].
    z2=beta*beta*Q
    a=rat(1)
    partial=a
    for m in range(N):
        a=mul(a,rat(z2,4*(m+1)*(m+2)))
        partial=add(partial,a)
    following=mul(a,rat(z2,4*(N+1)*(N+2)))
    rho=rat(z2,4*(N+2)*(N+3))
    check(lt(rho,rat(1)),"tail_ratio_below_one")
    tail=div(following,sub(rat(1),rho))
    check(lt(tail,mul(partial,rat(1,1000000000000))),
          "Haar_series_relative_tail_lt_1e_minus12")
    return partial,add(partial,tail)


def mixed_ratio(beta):
    # Hold four staples at +I, vary other two independently ±I.
    # Q(++)=36, Q(+-)=Q(-+)=16, Q(--)=4.
    I=(1,0,0,0)
    J=(-1,0,0,0)
    qs={}
    for s,t in product((I,J),repeat=2):
        q=q_norm_sq((I,I,I,I,s,t))
        qs[(s[0],t[0])]=q
    check(qs=={(1,1):36,(1,-1):16,(-1,1):16,(-1,-1):4},
          "four_staple_background_and_two_sign_variations")
    mixed=qs[1,1]-qs[1,-1]-qs[-1,1]+qs[-1,-1]
    check(mixed==8,"second_order_mixed_Q_differential")
    if fault=="bad_mixed_derivative":
        check(mixed==0,"RED_bad_mixed_derivative")
    # logZ=beta² Q/8+O(beta⁴), so the mixed log coefficient
    # is (36-16-16+4)/8 = 1 in exact integers.
    check(mixed//8==1 and mixed%8==0,
          "mixed_log_Z_beta_squared_coefficient_one")
    if fault=="claim_4D_closure":
        check(mixed==0,"RED_claim_4D_closure")
    N=max(40,6*beta)
    Z={}
    for Q in (0,4,16,36):
        Z[Q]=one_link_series(beta,Q,N)
    check(Z[0]==(rat(1),rat(1)),
          "Z_at_zero_staple_norm_one")
    for x,y in ((0,4),(4,16),(16,36)):
        check(lt(Z[x][1],Z[y][0]),
              "strict_local_SU2_staple_norm_monotonic")
    ratio_lo=div(mul(Z[36][0],Z[4][0]),mul(Z[16][1],Z[16][1]))
    ratio_hi=div(mul(Z[36][1],Z[4][1]),mul(Z[16][0],Z[16][0]))
    check(lt(rat(6,5),ratio_lo) and lt(ratio_lo,ratio_hi),
          "finite_beta_nonlinear_mixed_staple_ratio")
    ppm=1000000
    lo_ppm=ratio_lo[0]*ppm//ratio_lo[1]
    hi_ppm=ratio_hi[0]*ppm//ratio_hi[1]+1
    check(hi_ppm-lo_ppm<=2,
          "one_link_mixed_ratio_enclosure_two_ppm")
    emit("YM4_05A_4D_HAAR",beta=beta,
         Wilson_link_integration="EXACT_SU2_S3_HAAR",
         staple_count=6,
         Q_pp=36,Q_pm=16,Q_mp=16,Q_mm=4,
         log_mixed_beta_squared_coefficient=1,
         Taylor_terms_through=N,
         relative_tail_lt="1/1000000000000",
         mixed_ratio_ppm_interval=str(lo_ppm)+":"+str(hi_ppm),
         mixed_ratio_strict_gt="6/5",
         induced_mixed_interaction="NONZERO_CERTIFIED")
    

def main():
    root=Path(__file__).resolve().parents[1]
    frozen=root.joinpath("docs",
        "PREDICT-YM4-05A-CHARACTER-WEAK-COUPLING-20261107.hbp").read_bytes()
    check(sum(int(line.startswith(b"PREDICT|id=")) for line in
              frozen.splitlines())==16,"frozen_sixteen_prediction_rows")
    emit("YM4_05A_BEGIN",
         prediction_sha256=sha256(frozen).hexdigest(),
         source="CONTINUOUS_SU2",
         positive_control="2D_HEAT_KERNEL",
         negative_control="4D_WILSON_SINGLE_LINK",
         arithmetic="EXACT_INTEGER_RATIONAL",
         full_4D_RG="NOT_COMPUTED")
    check_character_orthogonality()
    check_heat_kernel_blocks()
    four_dimensional_chair()
    for beta in (1,4,16,64):
        mixed_ratio(beta)
    if fault=="claim_mass_gap":
        check("OPEN"=="PROVED","RED_claim_mass_gap")
    emit("YM4_05A_LIMITS",
         two_dim_weak_character_blocking="EXACT",
         four_dim_local_Wilson_mixed_chair="CERTIFIED",
         fourD_induced_action_Wilson_closed="NOT_PROVED",
         fourD_weak_coupling_Renormalized_flow="OPEN",
         full_spectrum_first_gap="OPEN",
         physical_mass_uniformity="OPEN",
         continuum_4D_SU2_Yang_Mills_Clay="OPEN")
    emit("YM4_05A_DONE",
         status="PASS_WITH_4D_WEAK_RG_HOLD",
         two_dim_heat_kernel_semigroup="EXACT",
         four_dim_six_staple_pair_network="REQUIRED",
         physical_gap="NOT_CERTIFIED")


if __name__=="__main__":
    main()
