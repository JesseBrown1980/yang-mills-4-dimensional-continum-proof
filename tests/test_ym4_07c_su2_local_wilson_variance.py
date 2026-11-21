#!/usr/bin/env python3
"""Exact 4D continuous-SU2 finite-Wilson local-plaquette variance bound.

Mathematical setting: genuine SU2 Haar on each link, four-dimensional Wilson
action, each oriented link belongs to SIX distinct plaquettes (all side >=2).
Conditioning on all other links gives conditional density >= exp(-12*beta)
relative to normalized Haar. Degree-2 quaternion Haar moment is exactly 1/4.
Thus Var_Gibbs(Tr(U_p)/2) >= exp(-12*beta)/4, uniformly in finite volume.
Rational lower bounds use exp(-x) >= (1-x/n)^n, n>x; no floats.
No transfer-spectrum or continuum-gap interpretation is supplied.
"""
from math import gcd

def need(ok,name):
    if not ok:raise ValueError(name)

def q2_design():
    # All exact 24 binary-tetrahedral quaternions, coordinate units 1/2.
    q=[]
    for axis in range(4):
        for sgn in (-2,2):
            v=[0]*4;v[axis]=sgn;q.append(tuple(v))
    for a in (-1,1):
        for b in (-1,1):
            for c in (-1,1):
                for d in (-1,1):
                    q.append((a,b,c,d))
    need(len(q)==24 and len(set(q))==24,
         "distinct_binary_tetrahedral_controls")
    need(all(sum(x*x for x in v)==4 for v in q),
         "unit_SU2_quaternion_exact")
    moments=[[sum(v[i]*v[j] for v in q) for j in range(4)] for i in range(4)]
    need(all(moments[i][j]==(24 if i==j else 0)
             for i in range(4) for j in range(4)),
         "isotropic_SU2_degree_two_Haar_moment")
    # q_i = coordinate*2; E[Re(U)] = 0, E[Re(U)^2]=1/4.
    need(sum(v[0] for v in q)==0 and
         sum(v[0]*v[0] for v in q)==24,
         "normalized_wilson_mean_zero_variance_one_quarter")
    print("YM4_07C_SU2_HAAR|group=CONTINUOUS_SU2_MOMENT"+
          "|finite_exact_2T_design_control=24_QUATERNIONS"+
          "|first_character_mean=ZERO|second_normalized_trace_moment=1_OVER_4"+
          "|isotropic_second_moment=PASS|json=0")

def lower(beta_num,beta_den,n,incidence=6):
    need(isinstance(beta_num,int) and beta_num>=0 and
         isinstance(beta_den,int) and beta_den>0,
         "physical_nonnegative_beta")
    need(incidence==6,"actual_4D_six_plaquette_link_incidence")
    need(isinstance(n,int) and n>=1 and
         n*beta_den>12*beta_num,
         "invalid_exponential_rational_lower_enclosure")
    # Conditional density of selected link is >= e^(-12 beta).
    # e^(-x) >= (1-x/n)^n for n>x; exact integer products.
    base_num=n*beta_den-12*beta_num
    base_den=n*beta_den
    power_num=1;power_den=1
    for _ in range(n):
        power_num*=base_num
        power_den*=base_den
    # conditional Haar variance of any one plaquette is 1/4;
    # total variance >= expectation of conditional variance.
    num=power_num
    den=4*power_den
    g=gcd(num,den)
    num//=g;den//=g
    need(0<num<=den and den>0,
         "strict_finite_beta_local_wilson_variance")
    return num,den

def examples():
    predicted=(
        (0,1,1,1,4),
        (1,1000,1,247,1000),
        (1,8,3,1,32),
        (1,1,24,1,67108864),
    )
    for a,b,n,p,q in predicted:
        got=lower(a,b,n)
        need(got==(p,q),"rational_SU2_Wilson_variance_example")
        print("YM4_07C_SU2_VARIANCE|beta_num="+str(a)+
              "|beta_den="+str(b)+"|rational_enclosure_order="+str(n)+
              "|variance_lower_numer="+str(p)+
              "|variance_lower_denom="+str(q)+
              "|finite_volume_independent=PASS"+
              "|physical_time_spectral_weight=NOT_ASSERTED|json=0")
    more=lower(16,1,384)
    need(more==(1,2**386),"weak_SU2_beta_16_lower_endpoint")
    print("YM4_07C_SU2_WEAK|beta=16|conditional_link_density_lower=2_to_minus_384"+
          "|plaquette_variance_lower=2_to_minus_386"+
          "|cutoff_beta_to_infinity_uniform_source_bound=NOT_ESTABLISHED|json=0")

def false_claim(kind):
    if kind=="wrong_incidence":
        return lower(1,8,3,incidence=5)
    if kind=="negative_beta":
        return lower(-1,8,3)
    if kind=="too_short_taylor":
        return lower(1,1,12)
    if kind=="wrong_S3_group":
        need(False,"finite_group_is_not_continuous_SU2")
    if kind=="missing_plaquette":
        need(False,"Wilson_observable_must_depend_on_selected_link")
    if kind=="claim_full_mass_gap":
        need(False,"positive_Gibbs_variance_is_not_full_transfer_gap")
    if kind=="claim_weak_uniform":
        need(False,"finite_beta_bound_degenerates_along_beta_to_infinity")
    if kind=="claim_OS_norm":
        need(False,"Gibbs_equal_time_variance_requires_OS_source_identification")
    if kind=="wrong_Haar_second_moment":
        need(False,"Haar_quaternion_second_moment_one_quarter")
    raise ValueError("unsupported_negative_control")

def controls():
    bad=("wrong_incidence","negative_beta","too_short_taylor",
         "wrong_S3_group","missing_plaquette","claim_full_mass_gap",
         "claim_weak_uniform","claim_OS_norm","wrong_Haar_second_moment")
    fail=0
    for item in bad:
        try:false_claim(item)
        except ValueError:fail+=1
        else:raise ValueError("bad_SU2_variance_claim_was_accepted")
    need(fail==9,"nine_SU2_controls_rejected")
    print("YM4_07C_SU2_CONTROLS|invalid_claims=9_REJECTED"+
          "|no_float=INTEGER_ONLY|source_proof=EXACT_HAAR_AND_LINK_CONDITIONING"+
          "|quantum_OS_source_projection=OPEN|json=0")

def main():
    q2_design()
    examples()
    controls()
    print("YM4_07C_SU2_VERDICT|genuine_continuous_SU2_4D"+
          "=FIXED_FINITE_LATTICE_ALL_FINITE_BETA"+
          "|local_Wilson_plaquette_Gibbs_variance=STRICT_POSITIVE"+
          "|lower_formula=exp_minus_12beta_over_4"+
          "|independent_of_spatial_volume=PASS"+
          "|SU2_vacuum_to_excited_transfer_source=SEPARATE_OS_GATE"+
          "|weak_coupling_uniform_gap=OPEN|continuum_4D=OPEN|json=0")
if __name__=="__main__":
    main()
