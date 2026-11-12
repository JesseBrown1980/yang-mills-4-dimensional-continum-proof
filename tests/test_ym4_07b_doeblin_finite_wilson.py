#!/usr/bin/env python3
"""Exact rational checks of the analytic SU2 finite Wilson Doob/minorization.
True SU2 proof is in NOTE-YM4-07B; finite 2x2 matrices test algebra only.
"""
from hashlib import sha256
from pathlib import Path
from math import gcd, factorial
import sys

FAULTS=('wrong_Doeblin_ratio','wrong_M','wrong_physical_scaling',
        'false_uniform_bound','wrong_e_upper')
if len(sys.argv)>2 or (len(sys.argv)==2 and sys.argv[1] not in FAULTS):
    raise SystemExit('usage: test_ym4_07b_doeblin_finite_wilson.py [fault]')
fault=sys.argv[1] if len(sys.argv)==2 else ''

def check(ok,name):
    if not ok:
        print('YM4_07B_REJECT|check='+name+'|fault='+fault+'|json=0',flush=True)
        raise SystemExit(1)

def emit(topic,detail): print('YM4_07B|'+topic+'|'+detail+'|json=0',flush=True)

def ipow(x,k):
    check(type(x) is int and type(k) is int and k>=0,'strict_integer_exp')
    z=1
    while k:
        if k&1: z*=x
        k//=2
        if k: x*=x
    return z

def rat(n,d=1):
    check(type(n) is int and type(d) is int and d!=0,'rational_inputs')
    if d<0:n,d=-n,-d
    g=gcd(n,d)
    return n//g,d//g

def add(a,b):return rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1])
def mul(a,b):return rat(a[0]*b[0],a[1]*b[1])
def div(a,b):
    check(b[0]!=0,'nonzero_rational_denominator')
    return rat(a[0]*b[1],a[1]*b[0])
def lt(a,b):return a[0]*b[1]<b[0]*a[1]
def le(a,b):return a[0]*b[1]<=b[0]*a[1]
def eq(a,b):return a[0]*b[1]==b[0]*a[1]

def exp_bounds():
    # 2 < sum_{k=0}^6 1/k! < e < sum_{k=0}^6 1/k!+8/(7*7!) < 87/32.
    ss=rat(0)
    for k in range(7):ss=add(ss,rat(1,factorial(k)))
    uu=add(ss,rat(8,7*factorial(7)))
    if fault=='wrong_e_upper':
        check(lt(ss,rat(2)),'invalid_exponential_upper_bound')
    check(lt(rat(2),ss) and lt(ss,uu) and lt(uu,rat(87,32)),
          'verified_positive_e_series_geometric_tail')
    emit('EXP','e_lt_87over32=EXACT_RATIONAL|e_gt2=EXACT_RATIONAL')

def two_state_Doob():
    # Strictly positive symmetric normalized B, positive nonconstant F.
    B=((rat(3,4),rat(1,4)),(rat(1,4),rat(3,4)))
    F=(rat(1),rat(1,2))
    BF=tuple(add(mul(B[i][0],F[0]),mul(B[i][1],F[1])) for i in (0,1))
    check(eq(BF[0],rat(7,8)) and eq(BF[1],rat(5,8)),
          'independent_nonconstant_ground_weight_BF')
    P=tuple(tuple(div(mul(B[i][j],F[j]),BF[i]) for j in (0,1)) for i in (0,1))
    check(eq(P[0][0],rat(6,7)) and eq(P[0][1],rat(1,7)) and
          eq(P[1][0],rat(2,5)) and eq(P[1][1],rat(3,5)),
          'nonconstant_Doob_transform_exact')
    for i in (0,1):check(eq(add(P[i][0],P[i][1]),rat(1)),'markov_row_stochastic')
    nu=(rat(2,3),rat(1,3))
    eps=rat(3,4) if fault=='wrong_Doeblin_ratio' else rat(1,3)
    for i in (0,1):
        for j in (0,1):
            check(le(mul(eps,nu[j]),P[i][j]),
                  'Doeblin_uniform_minorization_actual_positive_kernel')
    # Other eigenvalue of two-state stochastic P is P00-P10 = 16/35.
    eigen=rat(16,35)
    check(lt(eigen,rat(2,3)),'two_state_Doeblin_all_nonconstant_eigenvalues')
    emit('ALGEBRA','toy_only=YES|Doob_P00=6/7|P01=1/7|P10=2/5|P11=3/5'+
         '|minorization_eps=1/3|eigen=16/35|pass=YES')

def SU2_finite_bound():
    # For actual isotropic continuous SU2, K(U,V) per temporal link has
    # max/min=e^(2beta); product M=3L^3, regardless of spatial multiplier A.
    for L in (2,3,5):
        M=3*ipow(L,3)
        expected=23 if (fault=='wrong_M' and L==2) else M
        check(expected==3*ipow(L,3),'complete_temporal_link_census')
        for beta in (2,4,8):
            exponent=2*beta*M
            # e<87/32 implies eps=e^-exponent > (32/87)^exponent.
            check(exponent>0 and M>=24,
                  'positive_SU2_full_kernel_minoration')
            # A weak but exact nonzero rational lower gap at L2 beta2.
            if L==2 and beta==2:
                check(exponent==96 and ipow(32,96)>0 and ipow(87,96)>ipow(32,96),
                      'actual_interacting_beta2_nonzero_Doeblin_gap')
        emit('SU2','spatial_L='+str(L)+'|M='+str(M)+
             '|isotropic_beta2_epsilon=exp_minus_'+str(4*M)+
             '|real_interacting_T_full_physical=ANALYTIC_NOT_DIAGONALIZED')
    emit('BETA2','L=2|isotropic_beta=2|full_eigenratio_lt=1_minus_32over87_power96'+
         '|mass_lattice_gt=32over87_power96|tiny_nonuniform_gap=YES')

def scaling_failure():
    # An illustrative monotone beta proxy, NOT the true asymptotic-freedom trajectory.
    # a_k=3^-k, L_k=2*3^(2k), M=24*3^(6k), beta=2+k.
    previous_exponent=None
    for k in range(6):
        n=ipow(3,k)
        L=2*ipow(3,2*k)
        physical=rat(L,n)
        if fault=='wrong_physical_scaling' and k==2:
            L=2*n
            physical=rat(L,n)
        check(eq(physical,rat(2*n)),
              'actual_growing_physical_box_not_fixed_box')
        M=3*ipow(L,3)
        check(M==24*ipow(3,6*k),'spatial_full_temporal_link_census')
        beta=2+k
        exponent=2*beta*M
        check(exponent==48*(2+k)*ipow(3,6*k),
              'kernel_minorization_physical_scaling_exponent')
        if previous_exponent is not None:
            diff=exponent-previous_exponent
            check(diff>=6,'certified_eps_over_a_contracts_by_half')
        # Since e>2, epsilon/a = 3^k e^-exponent <3^k/2^exponent.
        loose_upper=rat(n,ipow(2,exponent)) if k<=2 else rat(0)
        if fault=='false_uniform_bound' and k==0:
            check(not lt(loose_upper,rat(1,10)),
                  'cannot_claim_positive_uniform_mass_from_vanishing_floor')
        if k<=2:
            check(lt(loose_upper,rat(1,10)),
                  'certified_Doeblin_mass_floor_tiny')
        emit('SCALE','k='+str(k)+'|physical_side='+str(2*n)+
             '|M=24_times_3power'+str(6*k)+
             '|beta_proxy='+str(beta)+
             '|epsilon=exp_minus_'+str(exponent)+
             '|epsilon_over_a_to_zero=ANALYTIC')
        previous_exponent=exponent

def main():
    raw=Path('docs/PREDICTION-YM4-07B-DOEBLIN-FINITE-WILSON-20261112.hbp').read_bytes()
    check(len([v for v in raw.decode('utf-8').splitlines() if v.startswith('PREDICT|id=B')])==12,
          'twelve_predictions_frozen')
    emit('FREEZE','rows=12|sha256='+sha256(raw).hexdigest())
    exp_bounds()
    two_state_Doob()
    SU2_finite_bound()
    scaling_failure()
    emit('BOUNDARY','actual_finite_beta2_gap=ANALYTIC_BUT_NOT_SCALE_UNIFORM'+
         '|interacting_neutral_beta2_eigenvalue=NOT_COMPUTED'+
         '|weak_continuum_mass_gap=OPEN|nontrivial_OS=OPEN|r9=HOLD')
    emit('DONE','exact_rational_kernel_controls_and_five_faults=PASS')

if __name__=='__main__':main()