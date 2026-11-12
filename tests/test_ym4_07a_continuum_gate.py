#!/usr/bin/env python3
"""YM4-07A exact-rational weak-coupling/continuum acceptance gate.

Never claims a new actual 4D SU2 continuum mass bound. It checks
physical-time scaling, all-beta Bessel-order finite sample evidence,
full-spectrum versus observable dark-state traps, and space-volume scaling.
"""
from math import gcd, factorial
from hashlib import sha256
from pathlib import Path
import sys

FAULTS = ('wrong_time_scale', 'ignore_dark_state', 'false_finite_box_infinite_volume',
          'bad_neutral_irrep', 'fake_Turan_reverse', 'false_static_ratio_continuum',
          'bad_Dobrushin_acceptance')
if len(sys.argv) > 2 or (len(sys.argv)==2 and sys.argv[1] not in FAULTS):
    raise SystemExit('usage: test_ym4_07a_continuum_gate.py [fault]')
fault = sys.argv[1] if len(sys.argv)==2 else ''

def check(value,name):
    if not value:
        print('YM4_07A_REJECT|check='+name+'|fault='+fault+'|json=0',flush=True)
        raise SystemExit(1)

def show(section, detail):
    print('YM4_07A|'+section+'|'+detail+'|json=0',flush=True)

def r(n,d=1):
    check(type(n) is int and type(d) is int and d != 0,'integer_rational_inputs')
    if d < 0: n,d=-n,-d
    g = gcd(n,d)
    return (n//g,d//g)

def a(x,y): return r(x[0]*y[1]+y[0]*x[1],x[1]*y[1])
def s(x,y): return r(x[0]*y[1]-y[0]*x[1],x[1]*y[1])
def m(x,y): return r(x[0]*y[0],x[1]*y[1])
def d(x,y):
    check(y[0]!=0,'division_nonzero')
    return r(x[0]*y[1],x[1]*y[0])
def lt(x,y): return x[0]*y[1]<y[0]*x[1]
def le(x,y): return x[0]*y[1]<=y[0]*x[1]
def eq(x,y): return x[0]*y[1]==y[0]*x[1]
def ipow(base, exponent):
    check(type(base) is int and type(exponent) is int and exponent>=0,
          'strict_integer_exponent')
    value=1
    while exponent:
        if exponent&1:
            value*=base
        exponent//=2
        if exponent:
            base*=base
    return value

def power(x,n):
    check(type(n) is int and n>=0,'integer_exponent')
    return r(ipow(x[0],n),ipow(x[1],n))

def modified_Bessel_interval(beta,order,terms=42):
    # beta is an even positive integer in this control: x=beta/2 integer.
    x = beta//2
    check(beta>0 and beta%2==0 and type(order) is int and order>=0,
          'positive_even_beta_for_rational_Bessel')
    term=r(ipow(x,order),factorial(order))
    lower=r(0)
    for k in range(terms):
        lower=a(lower,term)
        term=d(m(term,r(x*x)),r((k+1)*(k+order+1)))
    ratio=r(x*x,(terms+1)*(terms+order+1))
    check(lt(ratio,r(1)),'strict_Bessel_tail_contraction')
    upper=a(lower,d(term,s(r(1),ratio)))
    return lower,upper

def checked_Bessel_order():
    for beta in (2,4,8,16):
        intervals={q:modified_Bessel_interval(beta,q) for q in range(1,15)}
        lo1,hi1=intervals[1]
        lo2,hi2=intervals[2]
        t1_lower=d(lo2,hi1)
        t1_upper=d(hi2,lo1)
        check(lt(r(0),t1_lower) and lt(t1_lower,t1_upper) and lt(t1_upper,r(1)),
              'normalized_fundamental_bessel_between_zero_and_one')
        for nu in range(2,14):
            lprev,uprev=intervals[nu-1]
            lcur,ucur=intervals[nu]
            lnext,unext=intervals[nu+1]
            wrong=(fault=='fake_Turan_reverse' and beta==8 and nu==2)
            if wrong:
                check(lt(power(lcur,2),m(uprev,unext)),
                      'false_reverse_Turan_inequality_rejected')
            else:
                check(lt(m(uprev,unext),power(lcur,2)),
                      'Bessel_Turan_positive_cross_products')
        for n in range(2,13):
            l,up=intervals[n+1]
            tn_upper=d(up,lo1)
            check(lt(tn_upper,power(t1_lower,n)),
                  'higher_temporal_irrep_strictly_below_fundamental_power')
        t1sq=power(t1_lower,2)
        t1four=power(t1_lower,4)
        t2upper=d(intervals[3][1],lo1)
        if fault=='bad_neutral_irrep' and beta==2:
            t2upper=t1sq
        check(lt(power(t2upper,2),t1four),
              'all_beta_adjoint_two_edge_winding_below_neutral_plaquette')
        if beta==2:
            # At the actual beta=2 isotropic interaction, the 06H floor
            # is (37/25) exp(-48), whereas the pure-electric neutral
            # upper is t1^4. It is provably larger than that floor:
            # exp(48)>1+48+48^2/2=1201 and t1>2/5.
            check(lt(r(2,5),t1_lower),'beta2_t1_gt_two_fifths')
            check(lt(r(37,25*1201),power(r(2,5),4)),
                  'beta2_existing_neutral_ratio_ceiling_is_vacuous')
            show('OBSTRUCTION','beta=2|spatial_isotropic=YES|old_ratio_upper_gt1=YES'+
                 '|true_interacting_neutral_second=NOT_COMPUTED')
        show('BESSEL', 'beta='+str(beta)+'|Turan_orders=2..13_PASS'+
             '|tn_lt_t1_power_n_orders=2..12_PASS'+
             '|pure_temporal_neutral_second=t1_power4'+
             '|interacting_neutral_second=NOT_COMPUTED')

def full_physical_time_scaling():
    # a_k=3^-k and unit physical-time transfer exponent 3^k.
    # A: ratio n/(n+1) -> physical mass 1.
    # B: ratio n*n/(n*n+1) -> physical mass 0, and is the hidden slow state.
    # C: constant ratio 1/2 -> infinite mass, vanishing complement for t>0.
    for k in range(0,8):
        n=ipow(3,k)
        steps=ipow(2,k) if (fault=='wrong_time_scale' and k==2) else n
        check(steps==n,'number_of_steps_per_fixed_physical_time')
        q_massive=r(n,n+1)
        q_massless=r(n*n,n*n+1)
        q_static=r(1,2)
        unit_massive=power(q_massive,steps)
        unit_massless=power(q_massless,steps)
        unit_static=power(q_static,steps)
        check(lt(r(1,3),unit_massive) and le(unit_massive,r(1,2)),
              'massive_time_one_bounded_away_zero_and_one')
        check(lt(unit_massless,r(1)),'massless_time_one_below_one')
        if n>1:
            check(lt(r(n-1,n),unit_massless),
                  'massless_time_one_approaches_one_from_below')
            check(lt(unit_massive,unit_massless),
                  'hidden_slow_mode_dominates_full_physical_spectrum')
        selected=q_massive if fault=='ignore_dark_state' else q_massless
        if n>1:
            check(eq(selected,q_massless),'full_spectrum_not_selected_observable')
        if fault=='false_static_ratio_continuum' and k==2:
            check(lt(r(1,3),unit_static),
                  'static_lattice_gap_cannot_survive_continuum_as_nontrivial')
        if k>=2:
            check(lt(unit_static,r(1,100)),'fixed_lattice_ratio_kills_time_one_complement')
        show('SCALE','k='+str(k)+'|a=1/3power'+str(k)+
             '|physical_time_steps='+str(steps)+
             '|massive_time_one_in_1/3_to_1/2=YES'+
             '|vanishing_mass_hidden_mode=YES|fixed_ratio_trivializes=YES')
    show('LIMIT','massive_m_k=n_log_1plus1overn_to_1'+
         '|massless_m_k=n_log_1plus1overn_squared_to_0'+
         '|static_m_k=n_log2_to_infinity'+
         '|full_spectrum_dark_counterexample=PASS')

def volume_and_Dobrushin_gate():
    # L(a)a stays at 2 for L=2*3^k; it tends to infinity for L=2*3^(2k).
    # beta_k=2+k is ONLY a rational monotone-growing proxy for AF beta(a).
    # Classical sufficient Dobrushin criterion from PR 57: alpha_UB=9 beta.
    for k in range(0,8):
        n=ipow(3,k)
        side_fixed=2*n
        physical_fixed=r(side_fixed,n)
        growing=2*n*n
        physical_growing=r(growing,n)
        check(eq(physical_fixed,r(2)) and eq(physical_growing,r(2*n)),
              'physical_box_length_from_lattice_side_times_spacing')
        if fault=='false_finite_box_infinite_volume' and k==2:
            check(lt(r(2),physical_fixed),
                  'constant_physical_box_is_not_infinite_volume')
        beta=2+k
        alpha_upper=9*beta
        if fault=='bad_Dobrushin_acceptance' and k==2:
            check(alpha_upper<1,'Dobrushin_sufficient_criterion_must_hold')
        check(alpha_upper>=18,'existing_strong_coupling_Dobrushin_bound_not_useful')
        Ns=3*ipow(growing,3)
        check(Ns==24*ipow(3,6*k),
              'growing_box_actual_spatial_plaquette_census')
        show('VOLUME','k='+str(k)+'|fixed_box_physical_length=2'+
             '|growing_box_physical_length='+str(2*n)+
             '|spatial_Ns_growing=24_times_3power'+str(6*k)+
             '|beta_proxy='+str(beta)+'|Dobrushin_sufficient_upper='+str(alpha_upper)+
             '|Dobrushin_test=NOT_MET')

def main():
    frozen=Path('docs/PREDICTION-YM4-07A-CONTINUUM-WEAK-GATE-20261112.hbp').read_bytes()
    rows=[x for x in frozen.decode('utf-8').splitlines() if x.startswith('PREDICT|id=W')]
    check(len(rows)==24,'frozen_twenty_four_predictions')
    show('FREEZE','rows=24|sha256='+sha256(frozen).hexdigest())
    checked_Bessel_order()
    full_physical_time_scaling()
    volume_and_Dobrushin_gate()
    show('BOUNDARY','weak_coupling_actual_interacting_full_spectrum=OPEN'+
         '|volume_uniform_physical_mass=OPEN|OS_continuum_construction=OPEN'+
         '|no_Clay_solution_claim=YES|r9=HOLD')
    show('DONE','exact_integer_controls_and_seven_falsifiers=PASS')

if __name__=='__main__': main()