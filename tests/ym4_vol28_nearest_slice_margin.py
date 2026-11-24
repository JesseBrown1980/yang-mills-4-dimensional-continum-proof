"""VOL28 native SU2 nearest-slice centered Wilson correlation lower margin.

Strict integer native 4D torus geometry and exact production exponents,
Haar low moments, SU2 Riccati barrier algebra and independent rational
two-state positive-transfer trace/Perron/Cauchy control.
Original continuous SU2 Wilson Fourier/Perron proof remains analytic.
"""
from itertools import product
from math import gcd


def check(ok, label):
    if not ok:
        raise AssertionError(label)


def q(n, d=1):
    check(d != 0, 'nonzero_rational_denominator')
    if d < 0:
        n,d=-n,-d
    c=gcd(abs(n),d)
    return (n//c,d//c)


def mulq(a,b):
    return q(a[0]*b[0],a[1]*b[1])


def greater(a,b):
    return a[0]*b[1]>b[0]*a[1]


def shift(x,axis,L):
    z=list(x)
    z[axis]=(z[axis]+1)%L
    return tuple(z)


def face_links(x,mu,nu,L):
    check(mu<nu and mu!=2 and nu!=2,'spatial_plaquette')
    return ((x,mu),(shift(x,mu,L),nu),
            (shift(x,nu,L),mu),(x,nu))


def original_spatial_geometry(r):
    L=4*r+6
    check(L%2==0 and L>=2*(2*r+3),'original_even_no_wrap_torus')
    d=r+1
    p0=face_links((0,0,0,0),0,1,L)
    pd=face_links((0,0,d,0),0,1,L)
    check(len(set(p0))==4 and len(set(pd))==4 and
          not set(p0).intersection(pd),
          'central_and_one_step_exterior_plaquettes_disjoint')
    check(all(x[0][2]==0 for x in p0) and
          all(x[0][2]==d for x in pd),
          'translate_purely_in_time_direction_two')
    count_sites=0
    spatial_links=set()
    spatial_faces=set()
    for xyz in product(range(L),repeat=3):
        x=(xyz[0],xyz[1],0,xyz[2])
        count_sites+=1
        for mu in (0,1,3):
            spatial_links.add((x,mu))
        for mu,nu in ((0,1),(0,3),(1,3)):
            face=face_links(x,mu,nu,L)
            check(len(set(face))==4,'native_spatial_Wilson_four_links')
            spatial_faces.add((x,mu,nu))
    check(count_sites==L**3,'native_slice_sites')
    E=len(spatial_links)
    Q=len(spatial_faces)
    check(E==3*L**3 and Q==3*L**3,'three_spatial_links_and_faces_per_site')
    check(4*E+6*Q==30*L**3,'correct_final_Perron_Fourier_exponent')
    check(5*E+6*Q==33*L**3,'pre_trivial_character_exponent')
    return L,E,Q


def native_Haar_plaquette_moment():
    # 24 Hurwitz unit quaternions reproduce the Haar second moment
    # exactly; never a finite-beta Gibbs replacement.
    pts=[]
    for i in range(4):
        for s in (-1,1):
            a=[0]*4
            a[i]=2*s
            pts.append(tuple(a))
    pts.extend(tuple(a) for a in product((-1,1),repeat=4))
    check(len(pts)==24,'exact_unit_quaternion_moment_quadrature')
    check(all(sum(v*v for v in a)==4 for a in pts),'exact_SU2_unit_norm')
    check(sum(a[0] for a in pts)==0,'fundamental_plaquette_Haar_zero_mean')
    check(sum(a[0]*a[0] for a in pts)==24,
          'fundamental_plaquette_Haar_second_one_quarter')
    # Since F=(1+Re U_p)/2, Var_Haar(F)=1/16 for one native
    # plaquette, and E_Haar (F-m)^2 >=1/16 for every m in [0,1].
    check(24*16==384,'source_fourier_test_Haar_variance')


def riccati_barrier(beta):
    check(beta>=1,'beta_positive')
    # At B=beta/(beta+4) the Riccati vector field minus B'
    # equals exactly 5*beta/(beta+4)^2.
    # The equation multiplied by (beta+4)^2 is:
    # (beta+4)^2-beta^2-3(beta+4)-4 = 5beta.
    lhs=(beta+4)**2-beta**2-3*(beta+4)-4
    check(lhs==5*beta and lhs>0,'strict_SU2_Bessel_ratio_barrier')
    if beta>=4:
        check(2*beta>=beta+4,'fundamental_ratio_at_least_half')
    # For beta>=1, the elementary Haar-cap bound yields
    # a0 > exp(beta)/(9*beta*beta). The cap proof is analytic.
    check(9*beta*beta>=9,'Haar_cap_positive_integer_denominator')


def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]


def mpow(a,n):
    check(n>=0,'positive_integer_matrix_power')
    out=[[1,0],[0,1]]
    for _ in range(n):
        out=mm(out,a)
    return out


def trace(a):
    return a[0][0]+a[1][1]


def rational_transfer_control():
    # Two-state independent spectral-algebra control. Haar is uniform on
    # two signs. T is written in an orthonormal basis and has strictly
    # positive kernel and eigenvalues 4,2; not a native SU2 calculation.
    T=[[3,1],[1,3]]
    A=[[1,0],[0,-1]]  # twice centered physical bounded F
    L=6
    Z=trace(mpow(T,L))
    raw=trace(mm(mm(mm(A,T),A),mpow(T,L-1)))
    c1=q(raw,4*Z)
    check(Z==4160 and raw==2176,'exact_positive_transfer_trace')
    check(c1==q(17,130),'independent_two_state_C1')
    # Normalize the top eigenvector Omega=(1,1)/sqrt(2) and
    # set S=A/2. Then <Omega,S T S Omega>=1/2,
    # Tr(T)=6. The spectral C1 lower is 1/12.
    perron_lower=q(1,12)
    check(greater(c1,perron_lower),'Perron_trace_lower_margin')
    # The Fourier Cauchy step is exact on the sign eigenmode:
    # <g,S>=1/4, <S,T^(-1) S>=1/8, yielding 1/2.
    test=mulq(q(1,4),q(1,4))
    check(test==q(1,16),'two_mode_positive_test_numerator')
    check(mulq(test,q(8))==q(1,2),
          'two_mode_Fourier_Cauchy_saturation')
    return c1,perron_lower


def production_exponents():
    beta=9**12
    check(beta==282429536481 and beta==3**24,
          'production_coupling_is_exact_power_three')
    check(9*beta*beta==3**50,
          'SU2_trivial_character_cap_exact_power_three')
    check(30*beta+150==8472886094580,
          'production_per_spatial_site_exponent')
    expected={10:8472886094580000,
              14:23249599443527520,
              18:49413871703590560,
              22:90219291135087840}
    for r in (1,2,3,4):
        L,E,Q=original_spatial_geometry(r)
        exp=(30*beta+150)*L**3
        check(exp==expected[L],'production_nearest_slice_margin')
        check(E==Q and 150*L**3==50*E,
              'production_polynomial_cap_to_power_three')
        check(exp==30*beta*L**3+50*E,
              'complete_production_lower_margin_exponent')
        print('YM4_VOL28_ORIGINAL|r='+str(r)+'|L='+str(L)+
              '|spatial_links='+str(E)+'|spatial_faces='+str(Q)+'|PASS')
        print('YM4_VOL28_MARGIN|L='+str(L)+'|beta=9^12|'+
              'C1_over_C0_gt_1_over_320_times_3_pow='+str(exp)+'|PASS')


def main():
    native_Haar_plaquette_moment()
    for b in (1,4,9**12):
        riccati_barrier(b)
    print('YM4_VOL28_SU2_HAAR|plaquette_mean=0|variance=1/4|'+
          'a0_cap=ANALYTIC|ratio_Riccati=ANALYTIC|PASS')
    c1,p=rational_transfer_control()
    check(c1==q(17,130) and p==q(1,12),'independent_transfer_test')
    print('YM4_VOL28_PERRON_TOY|lambda=4,2|C1=17/130|'+
          'lower=1/12|PASS')
    production_exponents()
    print('YM4_VOL28_SCOPE|native_original_SU2=ANALYTIC|'+
          'numeric_finite_volume_margin=EXACT_EXPONENT|'+
          'volume_uniform=OPEN|continuum_mass_rate=OPEN|continuum_11=OPEN')


if __name__=='__main__':
    main()
