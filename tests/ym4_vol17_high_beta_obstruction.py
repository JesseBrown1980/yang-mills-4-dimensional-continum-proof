"""YM4 VOL17 original 4D SU2 high-beta actual link influence obstruction.

Strict integer/rational SU2 quaternions; analytic Haar TV lower bound
is separately derived in the companion theorem, not numerically simulated.
"""
from itertools import product
from math import gcd

ONE=(1,0,0,0,1)
MINUS=(-1,0,0,0,1)
Q2=(-1,1,1,1,2)
Q3=(-1,-1,-1,-1,2)
I=(0,1,0,0,1)
MINUS_I=(0,-1,0,0,1)
FIVE=(ONE,Q2,Q3,I,MINUS_I)

def require(ok,name):
    if not ok:
        raise ValueError(name)

def norm(q):
    return sum(x*x for x in q[:4])==q[4]*q[4]

def reduce_q(q):
    vals=list(q)
    g=vals[4]
    for x in vals[:4]:
        g=gcd(g,abs(x))
    return tuple(x//g for x in vals)

def mul(u,v):
    a,b,c,d,z=u
    e,f,g,h,w=v
    return reduce_q((a*e-b*f-c*g-d*h,
                     a*f+b*e+c*h-d*g,
                     a*g-b*h+c*e+d*f,
                     a*h+b*g-c*f+d*e,z*w))

def inv(q):
    return (q[0],-q[1],-q[2],-q[3],q[4])

def added_resultant(staples):
    result=[]
    for j in range(4):
        top=0
        for q in staples:
            require(2*q[j]%q[4]==0,"rational_resultant_double_scale")
            top+=2*q[j]//q[4]
        require(top%2==0,"actual_integral_resultant")
        result.append(top//2)
    return tuple(result)+(1,)

def shifted(x,nu,L,sgn=1):
    z=list(x)
    z[nu]=(z[nu]+sgn)%L
    return tuple(z)

def six_opposite_links(L):
    x=(0,0,0,0)
    out=[]
    for nu in (1,2,3):
        out.append((shifted(x,nu,L),0))
        out.append((shifted(x,nu,L,-1),0))
    require(len(set(out))==6,"six_distinct_actual_original_opposite_links")
    return out

def original_six_staples(U,L):
    x=(0,0,0,0)
    y=shifted(x,0,L)
    out=[]
    for nu in (1,2,3):
        xp=shifted(x,nu,L)
        xm=shifted(x,nu,L,-1)
        ym=shifted(y,nu,L,-1)
        plus=mul(mul(U[(x,nu)],U[(xp,0)]),inv(U[(y,nu)]))
        minus=mul(mul(inv(U[(xm,nu)]),U[(xm,0)]),U[(ym,nu)])
        out.extend((plus,minus))
    return tuple(out)

def original_link_fields(L,selected,sign):
    positions=six_opposite_links(L)
    target=[]
    remaining=list(FIVE)
    for j in range(6):
        target.append((ONE if sign==1 else MINUS)
                      if j==selected else remaining.pop(0))
    require(not remaining,"every_other_staple_assigned")
    U={(x,mu):ONE for x in product(range(L),repeat=4) for mu in range(4)}
    for e,q in zip(positions,target):
        U[e]=q
    return U,target

def high_beta_witness():
    L=6
    require(all(norm(q) for q in FIVE+(MINUS,)),
            "all_true_continuous_SU2_norm_one_rational_staples")
    require(added_resultant(FIVE)==(0,0,0,0,1),
            "five_noncommuting_SU2_staples_sum_exactly_zero")
    require(mul(Q2,I)!=mul(I,Q2),
            "noncommuting_SU2_rational_quaternion_control")
    positions=six_opposite_links(L)
    for j,f in enumerate(positions):
        plus,plus_target=original_link_fields(L,j,1)
        minus,minus_target=original_link_fields(L,j,-1)
        require(plus[f]==ONE and minus[f]==MINUS,
                "single_opposite_SU2_link_flipped")
        require(all(plus[e]==minus[e] for e in plus if e!=f),
                "entire_original_periodic_link_environments_differ_only_one_neighbor")
        require(original_six_staples(plus,L)==tuple(plus_target),
                "exact_original_4d_six_SU2_plaquette_staples_plus")
        require(original_six_staples(minus,L)==tuple(minus_target),
                "exact_original_4d_six_SU2_plaquette_staples_minus")
        require(added_resultant(original_six_staples(plus,L))==ONE,
                "SU2_one_link_conditional_resultant_plusI")
        require(added_resultant(original_six_staples(minus,L))==MINUS,
                "SU2_one_link_conditional_resultant_minusI")
        # Every f is an INTERNAL original positive link of the centered
        # b=3 cube, as is the distinguished link e=(0,0,0,0),mu=0.
        x,mu=f
        centered=tuple(v if v<=L//2 else v-L for v in x)
        require(mu==0 and centered[0]==0
                and all(-1<=c<=1 for c in centered),
                "changed_neighbor_is_internal_to_centered_b3_SU2_cube")
    # Haar is true full SU2 S3. With x=Re(U), mass of [1/2,3/4]
    # exceeds 1/16 from density (2/pi)*sqrt(1-x^2).
    # For beta>=36, e^(beta/2)>1+18+18^2/2=181.
    cap_exp_lower=1+18+18*18//2
    require(cap_exp_lower==181,
            "strict_positive_exponential_Taylor_lower_181")
    tv_num=cap_exp_lower-16
    require(tv_num==165 and 6*tv_num>cap_exp_lower,
            "six_actual_influence_coefficients_force_row_sum_gt_one")
    production_beta=282429536481
    require(production_beta>36,
            "production_beta_exceeds_high_beta_obstruction_threshold")

def main():
    high_beta_witness()
    return (
      'YM4_VOL17_EXACT_SU2|original_periodic_L6=PASS|rational_unit_quaternions=PASS|noncommuting_staples=PASS|json=0\n'
      'YM4_VOL17_SIX_NEIGHBORS|all_six_original_staples_independently_realizable=PASS|one_actual_neighbor_change_per_pair=PASS|json=0\n'
      'YM4_VOL17_RESULTANT|five_staples_sum_exact_zero=PASS|sixth_neighbor_flip_yields_H_plusI_vs_minusI=PASS|json=0\n'
      'YM4_VOL17_HAAR_TV|full_continuous_SU2_Haar=ANALYTIC|beta_ge36_TV_gt_165over181=ANALYTIC|json=0\n'
      'YM4_VOL17_DOBRUSHIN|six_coefficients_gt_165over181|row_sum_gt_990over181_gt_one|beta9power12=REJECTED|json=0\n'
      'YM4_VOL17_SCOPE|unprojected_worst_environment_TV_contraction=OBSTRUCTED|gauge_invariant_typical_region_coupling=OPEN|json=0\n'
      'YM4_VOL17_NEXT|interpolating_boundary_good_region_activity=OPEN|physical_Wilson_covariance_decay=OPEN|11_continuum_gates=OPEN|json=0\n'
    )

if __name__=="__main__":
    print(main(),end="")
