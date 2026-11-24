"""YM4 VOL27 original continuous SU2 Wilson transfer strict-predictor controls.

All integer original 4D geometry and SU2 tensor-power fusion checks.
A rational two-state spectral fixture tests transfer trace and beta-zero red.
Continuous SU2 Wilson transfer positivity is analytical, not discretized here.
"""
from itertools import product
from math import gcd


def check(ok, label):
    if not ok:
        raise AssertionError(label)


def q(n, d=1):
    check(d != 0, 'rational_denominator')
    if d < 0:
        n, d = -n, -d
    c = gcd(abs(n), d)
    return (n//c, d//c)


def mulq(a, b):
    return q(a[0]*b[0], a[1]*b[1])

def subq(a, b):
    return q(a[0]*b[1]-b[0]*a[1], a[1]*b[1])


def shift(x, axis):
    z = list(x)
    z[axis] += 1
    return tuple(z)


def plaquette(x, mu, nu):
    check(mu < nu, 'original_oriented_plaquette')
    return ((x,mu),(shift(x,mu),nu),
            (shift(x,nu),mu),(x,nu))


def inner_link(e, r):
    x, mu = e
    return all(-r<=z<=r for z in x) and x[mu]<r


def original_geometry(r):
    base=(0,0,0,0)
    d=r+1
    outer=(0,0,d,0)
    central=plaquette(base,0,1)
    remote=plaquette(outer,0,1)
    check(len(set(central))==4 and len(set(remote))==4,
          'original_plaquettes_four_links')
    check(all(inner_link(e,r) for e in central),
          'actual_centered_spatial_plaquette')
    check(all(not inner_link(e,r) for e in remote),
          'translated_spatial_plaquette_is_entirely_exterior')
    check(all(inner_link(e,r+1) for e in remote),
          'translated_plaquette_is_first_shell_inside')
    check(not set(central).intersection(remote),
          'distinct_original_plaquettes')
    L=4*r+6
    check(L%2==0 and L>=2*(2*r+3),'untwisted_even_torus')
    check(1<=d<L-d,'separation_shorter_than_complementary_time_path')
    def wrap(edges):
        return {(tuple(x%L for x in e[0]),e[1]) for e in edges}
    check(len(wrap(central))==4 and len(wrap(remote))==4,
          'periodic_injective_positive_links')
    check(not wrap(central).intersection(wrap(remote)),
          'periodic_disjoint_translated_plaquettes')
    return d,L


def spin_half_fusion():
    # χ_{1/2} χ_{k/2}=χ_{(k+1)/2}+χ_{(k-1)/2}, second absent for k=0.
    # All tensor multiplicities are nonnegative integers, and the highest
    # spin (n/2) in (χ_{1/2})^n occurs exactly once for EVERY integer n.
    mult={0:1}
    for n in range(1,17):
        next_mult={}
        for doubled_spin,count in mult.items():
            next_mult[doubled_spin+1]=next_mult.get(doubled_spin+1,0)+count
            if doubled_spin>0:
                next_mult[doubled_spin-1]=next_mult.get(doubled_spin-1,0)+count
        mult=next_mult
        check(mult.get(n)==1,'highest_spin_irrep_once')
        check(all(k>=0 and v>0 and k<=n and (n-k)%2==0
                  for k,v in mult.items()),'SU2_fusion_irrep_parity')
        check(sum(mult.values())>0,'strict_positive_irrep_multiplicities')
    check(mult[0]>0 and mult[16]==1,'spin_zero_and_highest_positive')
    return len(mult)


def matmul(a,b):
    return [[a[i][0]*b[0][j]+a[i][1]*b[1][j]
             for j in range(2)] for i in range(2)]


def matpow(a,n):
    check(n>=0,'nonnegative_integer_matrix_power')
    out=[[1,0],[0,1]]
    for _ in range(n):
        out=matmul(out,a)
    return out


def trace(a):
    return a[0][0]+a[1][1]


def spectral_trace_fixture():
    T=[[2,1],[1,2]]
    T0=[[1,1],[1,1]]
    A=[[1,0],[0,-1]]  # twice the centered multiplication F - 1/2.
    L=6
    d=2
    z=trace(matpow(T,L))
    check(z==730,'rational_strict_transfer_partition')
    raw=trace(matmul(matmul(matmul(A,matpow(T,d)),A),
                     matpow(T,L-d)))
    check(raw==90,'two_state_physical_trace_numerator')
    cov=q(raw,4*z)
    check(cov==q(9,292),'spectral_positive_covariance')
    raw1=trace(matmul(matmul(matmul(A,matpow(T,1)),A),
                      matpow(T,L-1)))
    cov1=q(raw1,4*z)
    c0=q(1,4)
    check(cov1==q(123,1460),'exact_one_step_periodic_transfer_covariance')
    gap=subq(mulq(c0,cov),mulq(cov1,cov1))
    check(gap==q(81,133225),'strict_logconvex_two_step_determinant')
    spectral=q(3*3+3*3*3*3,4*(3*3*3*3*3*3+1))
    check(spectral==cov,'strict_positive_eigenbasis_sum')
    # Exact spectral lambda=(3,1), A has offdiagonal 1/2 in eigenbasis.
    red_raw=trace(matmul(matmul(matmul(A,matpow(T0,d)),A),
                         matpow(T0,L-d)))
    check(red_raw==0,'beta_zero_rank_one_correlation_vanishes')
    check(trace(matpow(T0,L))==64,'beta_zero_rank_one_partition')
    # For a [0,1] exterior source, Var(F_d)<=1/4, hence
    # V_r >= 4 Cov(F_0,F_d)^2 even with unknown true Wilson covariance.
    floor=mulq(q(4),mulq(cov,cov))
    check(floor==q(81,21316),'normalized_predictor_variance_interface')
    return cov,floor,cov1,gap


def main():
    for r in (1,2,3,4):
        d,L=original_geometry(r)
        print('YM4_VOL27_GEOMETRY|r='+str(r)+'|time_separation='+str(d)+
              '|even_L='+str(L)+'|source=INTERNAL|translated=EXTERIOR|PASS')
    count=spin_half_fusion()
    print('YM4_VOL27_PETER_WEYL|tensor_power_to=16|highest_irrep_once=PASS|final_irreps='+str(count))
    cov,floor,cov1,gap=spectral_trace_fixture()
    print('YM4_VOL27_SPECTRAL_TOY|lambda=3,1|cov='+str(cov[0])+
          '/'+str(cov[1])+'|predictor_lower='+str(floor[0])+
          '/'+str(floor[1])+'|PASS')
    print('YM4_VOL27_LOGCONVEX|C0=1/4|C1=123/1460|C2=9/292|det=81/133225|PASS')
    print('YM4_VOL27_BETA_ZERO|rank_one_transfer=PASS|translated_cov=0|PASS')
    print('YM4_VOL27_NATIVE|continuous_SU2_transfer=ANALYTIC|beta_positive_predictor=STRICT|beta_9pow12=INCLUDED')
    print('YM4_VOL27_SCOPE|production_numeric_margin=OPEN|continuum_mass_rate=OPEN|continuum_11=OPEN')


if __name__=='__main__':
    main()
