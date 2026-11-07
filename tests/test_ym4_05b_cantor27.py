#!/usr/bin/env python3
"""YM4-05B: 27 Cantor-spaced nonlinear 4D-local SU2 measurements.

CAUTION: 3^4 torus with Q8-valued SU2 links and deliberately chosen nonlinear
gauge-covariant PLAQUETTE feedback. This is NOT Yang-Mills dynamics, full SU2
Haar gauge-field sampling, RG or a mass gap calculation. Its one-link
Wilson conditional Haar integral IS genuine continuous SU2, separately.

This *attempts* a shortcut before any claimed observable closure. The scalar
Q -> next Q reduction fails on actual pairs. Full-state periodicity *on this
single finite orbit* is then independently certified, allowing a conditional
3^40 time jump by cycle arithmetic. This cannot be exported to 4D YM.

All numbers exact integers/rationals, no JSON, no floating point.
"""
import hashlib
import itertools
import math
import sys
from pathlib import Path

FAULTS=("wrong_Cantor_digit","missing_inverse","broken_gauge_covariance",
        "false_Q_closure","false_cycle","incorrect_ternary_jump",
        "claim_physical_mass_gap")
fault=""
if len(sys.argv)>2 or (len(sys.argv)==2 and
    (not sys.argv[1].startswith("sabotage=") or
     sys.argv[1][9:] not in FAULTS)):
    print("usage: test_ym4_05b_cantor27.py [sabotage=NAME]")
    sys.exit(2)
if len(sys.argv)==2:
    fault=sys.argv[1][9:]


def check(ok,name):
    if not ok:
        print("FAILED|check="+name+"|json=0",flush=True)
        sys.exit(1)


def emit(tag,**kwargs):
    print(tag+"|"+"|".join(str(k)+"="+str(v) for k,v in kwargs.items())
          +"|json=0",flush=True)


def integer_power(a,n):
    check(isinstance(a,int) and isinstance(n,int) and n>=0,
          "nonnegative_integer_exponent")
    out=1
    while n:
        if n&1:
            out*=a
        n//=2
        if n:
            a*=a
    return out


def rational(a,b=1):
    check(isinstance(a,int) and isinstance(b,int) and b!=0,
          "rational_input_integral")
    if b<0:
        a,b=-a,-b
    g=math.gcd(a,b)
    return (a//g,b//g)


def plus(a,b):
    return rational(a[0]*b[1]+b[0]*a[1],a[1]*b[1])


def times(a,b):
    return rational(a[0]*b[0],a[1]*b[1])


def divided(a,b):
    check(b[0]!=0,"nonzero_rational_divisor")
    return rational(a[0]*b[1],a[1]*b[0])


def less(a,b):
    return a[0]*b[1]<b[0]*a[1]


def original_haar(beta,Q,N):
    """Independent original term-by-term rational reference from YM4-05A."""
    x=beta*beta*Q
    term=rational(1)
    sm=term
    for j in range(N):
        term=times(term,rational(x,4*(j+1)*(j+2)))
        sm=plus(sm,term)
    nextterm=times(term,rational(x,4*(N+1)*(N+2)))
    rho=rational(x,4*(N+2)*(N+3))
    check(less(rho,rational(1)),"reference_haar_tail_ratio")
    bound=divided(nextterm,rational(rho[1]-rho[0],rho[1]))
    return sm,plus(sm,bound)


def fast_haar(beta,Q,N):
    """Common-denominator Horner, identical rational endpoints to original."""
    check(beta>=0 and 0<=Q<=36 and N>=0,"Haar_input_domain")
    x=beta*beta*Q
    denominator=1
    numerator=1
    for j in range(N,0,-1):
        denominator*=4*j*(j+1)
        numerator=x*numerator+denominator
    lo=rational(numerator,denominator)
    if x==0:
        return lo,lo
    a=4*(N+1)*(N+2)
    b=4*(N+2)*(N+3)
    check(x<b,"Haar_positive_geometric_tail")
    upper=rational(numerator*a*(b-x)+integer_power(x,N+1)*b,
                   denominator*a*(b-x))
    check(less(lo,upper),"positive_haar_truncation_tail")
    return lo,upper


def check_six_staple_Gram_Pascal():
    # Exact 64 signed SU2 inputs compress to four Gram norms.
    histogram={0:0,4:0,16:0,36:0}
    for signs in itertools.product((-1,1),repeat=6):
        sum_signs=sum(signs)
        q=sum_signs*sum_signs
        paired=6+2*sum(signs[i]*signs[j]
                       for i in range(6) for j in range(i+1,6))
        check(q==paired,"signed_six_staple_Gram_pair_identity")
        histogram[q]+=1
    check(histogram=={0:20,4:30,16:12,36:2},
          "six_staple_Pascal_64_to_four")
    emit("CANTOR_FAST_GRAM",signed_Q8_inputs=64,
         Gram_matrix_pairs=15,unique_invariants=4,
         histogram="Q0:20,Q4:30,Q16:12,Q36:2",
         method="PASCAL_AND_PAIRWISE_GRAM")


def check_original_haar():
    expected=((1365888,1365889),(1512545,1512546),
              (1533420,1533421),(1538087,1538088))
    total=0
    for beta,(a,b) in zip((1,4,16,64),expected):
        N=max(40,6*beta)
        Z={}
        for Q in (0,4,16,36):
            quick=fast_haar(beta,Q,N)
            check(quick==original_haar(beta,Q,N),
                  "exact_fast_Haar_equals_original_fraction_oracle")
            Z[Q]=quick
            total+=1
        low=divided(times(Z[36][0],Z[4][0]),
                    times(Z[16][1],Z[16][1]))
        high=divided(times(Z[36][1],Z[4][1]),
                     times(Z[16][0],Z[16][0]))
        ppm_lo=low[0]*1000000//low[1]
        ppm_hi=high[0]*1000000//high[1]+1
        check((ppm_lo,ppm_hi)==(a,b),
              "pin_original_four_4D_Wilson_Haar_intervals")
        emit("CANTOR_FAST_HAAR",beta=beta,terms=N,
             rational_replays=4,
             mixed_ratio_ppm=str(a)+":"+str(b),
             method="INTEGER_HORNER",
             independent_original="EXACT_MATCH")
    check(total==16,"original_Haar_sixteen_checked")


QUATS=((1,0,0,0),(-1,0,0,0),(0,1,0,0),(0,-1,0,0),
       (0,0,1,0),(0,0,-1,0),(0,0,0,1),(0,0,0,-1))
QI={q:i for i,q in enumerate(QUATS)}
E=0


def quat_mul(a,b):
    x,y,z,w=a
    p,q,r,s=b
    return (x*p-y*q-z*r-w*s,x*q+y*p+z*s-w*r,
            x*r-y*s+z*p+w*q,x*s+y*r-z*q+w*p)


MUL=[[QI[quat_mul(a,b)] for b in QUATS] for a in QUATS]
INV=[QI[(v[0],-v[1],-v[2],-v[3])] for v in QUATS]

def mult(a,b):
    return MUL[a][b]


SIZE=3
VERTS=tuple(itertools.product(range(SIZE),repeat=4))
EDGES=tuple((x,mu) for x in VERTS for mu in range(4))
EDGE_ID={v:i for i,v in enumerate(EDGES)}


def move(x,mu,steps=1):
    y=list(x)
    y[mu]=(y[mu]+steps)%SIZE
    return tuple(y)


def plaq_edges(x,mu,nu):
    return (EDGE_ID[x,mu],
            EDGE_ID[move(x,mu),nu],
            EDGE_ID[move(x,nu),mu],
            EDGE_ID[x,nu])


PLAQ={(x,mu,nu):plaq_edges(x,mu,nu)
      for x in VERTS for mu in range(4) for nu in range(4)
      if mu!=nu}
POS_PLAQ=tuple(PLAQ[x,mu,nu] for x in VERTS
               for mu in range(4) for nu in range(mu+1,4))


def plaq(U,indices):
    a,b,c,d=indices
    return mult(mult(mult(U[a],U[b]),INV[U[c]]),INV[U[d]])


def update(U):
    # Gauge covariant because P_mu,nu(x) transforms by conjugation at x.
    # One fixed plaquette per link: nonlinear and noncommuting, NOT
    # heat-bath evolution or Wilson gradient flow.
    out=[0]*len(U)
    for pos,(x,mu) in enumerate(EDGES):
        nu=(mu+1)%4
        P=plaq(U,PLAQ[x,mu,nu])
        out[pos]=mult(P,U[pos])
    return bytes(out)


def start_state():
    # Stable seed without an external RNG; Python tuple spelling is
    # pinned as part of this test. All entries exactly in SU2's Q8 subset.
    return bytes(hashlib.sha256(
        ("1:"+str((x,mu))).encode("ascii")).digest()[0]%8
        for x,mu in EDGES)


def negative_plaquette(U,x,mu,nu):
    # Based loop x -> x+mu -> x+mu-nu -> x-nu -> x.
    a=U[EDGE_ID[x,mu]]
    b=U[EDGE_ID[move(move(x,mu),nu,-1),nu]]
    c=U[EDGE_ID[move(x,nu,-1),mu]]
    d=U[EDGE_ID[move(x,nu,-1),nu]]
    return mult(mult(mult(a,INV[b]),INV[c]),d)


def wilson_and_Q(U):
    # A local normalized trace over all positive plaquettes, and the
    # exact norm squared of six SU2 staples around the origin 0-link.
    W=sum(QUATS[plaq(U,p)][0] for p in POS_PLAQ)
    x=(0,0,0,0)
    mu=0
    ui=U[EDGE_ID[x,mu]]
    staples=[]
    for nu in (1,2,3):
        for sign in (-1,1):
            P=(plaq(U,PLAQ[x,mu,nu]) if sign==1
               else negative_plaquette(U,x,mu,nu))
            staples.append(mult(INV[ui],P))
    vector=[sum(QUATS[q][j] for q in staples) for j in range(4)]
    Q=sum(z*z for z in vector)
    gram=6+2*sum(
        sum(QUATS[staples[i]][k]*QUATS[staples[j]][k]
            for k in range(4))
        for i in range(6) for j in range(i+1,6))
    check(Q==gram and 0<=Q<=36,
          "SU2_six_staple_Gram_equals_direct_norm")
    return W,Q


def cantor_times():
    # 27 *rank-spaced* endpoints selected from all 32 exact
    # fifth-generation middle-third Cantor digits 0/2.
    out=[]
    for i in range(27):
        rank=i*31//26
        pos=sum(2*((rank>>j)&1)*integer_power(3,j)
                for j in range(5))
        out.append(pos)
    check(len(out)==27 and out==sorted(set(out))
          and out[0]==0 and out[-1]==242,
          "twenty_seven_Cantor_ranks")
    for t in out:
        q=t
        for _ in range(5):
            check(q%3 in (0,2),"Cantor_only_zero_or_two_digits")
            q//=3
        check(q==0,"Cantor_five_digits_only")
    if fault=="wrong_Cantor_digit":
        check(1 in out,"RED_wrong_Cantor_digit")
    return out


def gauge_transform(U,G):
    return bytes(mult(mult(G[x],U[i]),INV[G[move(x,mu)]])
                 for i,(x,mu) in enumerate(EDGES))


def gauge_check(U):
    G={x:hashlib.sha256(("g:"+str(x)).encode("ascii")
                      ).digest()[0]%8 for x in VERTS}
    gaugeU=gauge_transform(U,G)
    check(wilson_and_Q(gaugeU)==wilson_and_Q(U),
          "nonlinear_4D_gauge_invariant_observables")
    check(update(gaugeU)==gauge_transform(update(U),G),
          "nonlinear_4D_gauge_covariant_one_step")
    if fault=="broken_gauge_covariance":
        check(update(gaugeU)==update(U),
              "RED_broken_gauge_covariance")


def explore():
    check(len(VERTS)==81 and len(EDGES)==324 and
          len(POS_PLAQ)==486 and
          mult(2,4)!=mult(4,2),
          "noncommutative_4D_finite_geometry")
    if fault=="missing_inverse":
        check(INV[2]==2,"RED_missing_inverse")
    sample=cantor_times()
    states=[start_state()]
    for t in range(243):
        states.append(update(states[-1]))
    check(len(states)==244,"243_exact_sequential_4D_updates")
    unique={}
    repeat=None
    for t,U in enumerate(states):
        if U in unique:
            repeat=(unique[U],t)
            break
        unique[U]=t
    check(repeat==(4,172) and len(unique)==172,
          "nonlinear_full_state_first_cycle_certification")
    check(states[4]==states[172]
          and all(update(states[t])==states[t+1]
                  for t in (0,3,4,53,54,170,171,172,241,242)),
          "independently_replay_selected_cycle_and_endpoints")
    if fault=="false_cycle":
        check(states[4]==states[171],"RED_false_cycle")
    for t in (0,54,242):
        gauge_check(states[t])
    obs=[wilson_and_Q(U) for U in states]
    qnext={}
    conflicts=0
    count_distinct=set()
    Qdistinct=set()
    cache={}
    for slot,t in enumerate(sample):
        W,Q=obs[t]
        expected_next=obs[t+1][1]
        if Q in qnext and qnext[Q]!=expected_next:
            conflicts+=1
        else:
            qnext.setdefault(Q,expected_next)
        count_distinct.add((W,Q))
        Qdistinct.add(Q)
        if Q not in cache:
            bounds=fast_haar(16,Q,96)
            check(bounds==original_haar(16,Q,96),
                  "Cantor_27_exact_continuous_SU2_one_link_Haar")
            lo=bounds[0][0]*1000//bounds[0][1]
            hi=bounds[1][0]*1000//bounds[1][1]+1
            cache[Q]=(lo,hi)
        emit("CANTOR27",slot=slot,t=t,full_W=W,local_Q=Q,
             next_Q=expected_next,
             haar_Z_beta16_times1000_floor=cache[Q][0],
             haar_Z_beta16_times1000_ceil=cache[Q][1],
             full_state_SHA256=hashlib.sha256(states[t]).hexdigest()[:16])
    check(len(count_distinct)==23 and len(Qdistinct)==8,
          "twenty_seven_real_observations_nonconstant")
    check(conflicts==14,"Cantor_Q_scalar_next_step_collisions")
    if fault=="false_Q_closure":
        check(conflicts==0,"RED_false_Q_closure")
    # The full state repeats only after 168 steps from t=4. This is
    # an exact orbit-specific finite-map theorem: F deterministic and
    # states[4]==states[172] implies future recurrence by induction.
    # Test direct sequential states up to 243 before jumping.
    def jumped_at(n):
        return states[n] if n<4 else states[4+(n-4)%168]
    for t in (0,1,3,4,5,27,81,168,171,172,200,242,243):
        check(jumped_at(t)==states[t],
              "full_state_cycle_jump_vs_sequential_reference")
    huge=integer_power(3,40)
    recovered=jumped_at(huge)
    check(len(recovered)==324 and
          jumped_at(huge+168)==recovered and
          update(recovered)==jumped_at(huge+1),
          "nonlinear_full_state_exact_cycle_long_jump")
    if fault=="incorrect_ternary_jump":
        check(jumped_at(huge)==jumped_at(huge+1),
              "RED_incorrect_ternary_jump")
    emit("CANTOR27_ANALYSIS",
         samples=27,source="CLASSIC_MIDDLE_THIRD_LEVEL5_RANK_SUBSET",
         time_min=0,time_max=242,
         distinct_W_Q_pairs=len(count_distinct),
         local_Q_unique=len(Qdistinct),
         Q_to_next_Q_conflicts=conflicts,
         scalar_Q_Markov_reduction="REFUTED_FOR_THIS_UPDATE",
         gauge_covariance="EXACT_Q8_VALUED_SU2_INPUTS",
         full_states_replayed=243)
    emit("CANTOR27_CYCLE",
         first_repeat_time=172,
         repeats_state_at=4,cycle_length=168,
         exact_state_equality="YES",
         jump_target="3^40",
         jump_time=huge,
         target_reduced_time=4+(huge-4)%168,
         cycle_induction="VALID_ON_THIS_ONE_FINITE_ORBIT",
         physical_Yang_Mills_time_jump="NOT_CLAIMED")
    return states


def verify_matrix_law_scope():
    # Matrix Law Essentials: power-three cubing is valid for one FIXED
    # linear step. This local SU2 update is state dependent, so it does
    # not admit a fixed 1D Q transfer, as shown by sampled conflicts.
    P=1000081
    base=7*integer_power(9,P-2)%P
    check(base*9%P==7,"mod_prime_denominator_inverse")
    checks=0
    for n in range(1,10):
        x=integer_power(base,n*n-1)%P
        z=x
        for k in range(1,41):
            z=z*z%P*z%P
            if k in (1,3,9,20,40):
                check(z==pow(x,integer_power(3,k),P),
                      "fixed_diagonal_character_jump_matches_pow")
                checks+=1
    check(checks==45,"45_independent_ternary_jump_comparisons")
    emit("CANTOR27_MATRIX_LAW",
         modular_fixed_character_modes=9,
         exact_jump_comparisons=checks,
         cubings_to_3pow40=40,
         Pascal_mod3="REQUIRES_COMMUTING_MAP_OVER_CHARACTERISTIC_3",
         noncommuting_4D_SU2="NO_FROBENIUS_SHORTCUT",
         full_state_cycle_shortcut="ONLY_AFTER_EXACT_STATE_REPEAT_PROOF")


def main():
    root=Path(__file__).resolve().parents[1]
    for name,prefix,count in (
        ("PREDICT-YM4-05B-MATRIX-FAST-20261107.hbp",b"PREDICT|id=",14),
        ("PREDICT-YM4-05B-CANTOR27-NONLINEAR-20261107.hbp",
         b"PREDICT|cantor=",12)):
        raw=root.joinpath("docs",name).read_bytes()
        check(sum(int(row.startswith(prefix)) for row in raw.splitlines())==count,
              "prediction_freeze_"+name)
        emit("CANTOR27_FREEZE",artifact=name,rows=count,
             sha256=hashlib.sha256(raw).hexdigest())
    original=root.joinpath("tests",
        "YM4_05A_CHARACTER_WEAK_RECEIPT.hbp").read_bytes()
    check(original.count(b"YM4_05A_4D_HAAR|beta=")==4,
          "original_4D_Haar_receipt_pinned_exist")
    emit("CANTOR27_START",source="NONLINEAR_4D_GAUGE_COVARIANT_Q8_SURROGATE",
         exact_local_integral="ACTUAL_SU2_HAAR",
         4D_Wilson_transfer_operator="NOT_THIS_DYNAMICS",
         original_sha256=hashlib.sha256(original).hexdigest())
    check_six_staple_Gram_Pascal()
    check_original_haar()
    explore()
    verify_matrix_law_scope()
    if fault=="claim_physical_mass_gap":
        check("OPEN"=="PROVED","RED_claim_physical_mass_gap")
    emit("CANTOR27_DONE",status="PASS_WITH_SCALAR_REDUCTION_REFUTED",
         Cantor_measurements=27,
         inferred_Q_only_dynamics="FAIL",
         verified_full_state_cycle="PASS_SURROGATE_ONLY",
         nonlinear_jump_3pow40="VALID_AFTER_ORBIT_CERTIFICATION",
         actual_4D_SU2_Renormalized_reduction="OPEN",
         physical_YangMills_mass_gap="OPEN")


if __name__=="__main__":
    main()
