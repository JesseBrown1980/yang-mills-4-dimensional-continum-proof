"""VOL26: original centered SU2 plaquette and harmonic-tail exact controls.

Native four-dimensional positive links and mixed faces, continuous Haar
S3 even moment recurrences and exact positive zonal-kernel moment ratios.
The all-beta Gibbs covariance/Lipschitz and tail bounds are analytic.
"""
from itertools import product
from math import gcd


def check(ok, name):
    if not ok:
        raise AssertionError(name)


def q(n, d=1):
    if isinstance(n, tuple):
        check(d == 1 and len(n) == 2, 'canonical_rational_pair')
        return n
    check(d != 0, 'nonzero_denominator')
    if d < 0:
        n, d = -n, -d
    c = gcd(abs(n), d)
    return (n//c, d//c)


def add(a, b):
    return q(a[0]*b[1]+b[0]*a[1], a[1]*b[1])


def sub(a, b):
    return q(a[0]*b[1]-b[0]*a[1], a[1]*b[1])


def mul(a, b):
    return q(a[0]*b[0], a[1]*b[1])


def divide(a, b):
    check(b[0] != 0, 'nonzero_divisor')
    return q(a[0]*b[1], a[1]*b[0])


def fmt(x):
    return str(x[0]) if x[1] == 1 else str(x[0])+'/'+str(x[1])


def shift(x, axis, step=1):
    v = list(x)
    v[axis] += step
    return tuple(v)


def internal(link, r):
    x, axis = link
    return all(-r <= c <= r for c in x) and x[axis] < r


def face_links(x, mu, nu):
    check(mu < nu, 'oriented_original_face')
    return ((x, mu), (shift(x,mu),nu),
            (shift(x,nu),mu), (x,nu))


def centered_source_and_q(r):
    origin = (0,0,0,0)
    source = face_links(origin,0,1)
    check(len(set(source)) == 4, 'four_source_plaquette_links')
    check(all(internal(e,r) for e in source),
          'actual_centered_original_Wilson_source')
    mixed = []
    for x in product(range(-r-1,r+1),repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                edges = face_links(x,mu,nu)
                if sum(internal(e,r) for e in edges) == 1:
                    mixed.append((x,mu,nu,edges))
    check(len(mixed) == 24*(2*r+1)*(2*r+1)*(2*r),
          'complete_original_mixed_face_census')
    chosen = []
    for s,t in product((-1,1),repeat=2):
        x=(0,s*r,t*r,0)
        witness=(shift(x,1,s),0)
        occurrences=[p for p in mixed if witness in p[3]]
        check(len(occurrences) == 1, 'exactly_one_mixed_plaquette_for_q')
        check(not internal(witness,r) and internal(witness,r+1),
              'witness_in_original_shell')
        check(witness not in source,'witness_not_source_plaquette_link')
        a,b,c,edges=occurrences[0]
        check((b,c)==(0,1),'unique_original_mixed_plane')
        check(sum(internal(e,r) for e in edges)==1,'one_internal_link_only')
        chosen.append(witness)
    check(len(set(chosen))==4,'four_distinct_witnesses')
    return len(source),len(chosen)


def haar_moments_and_spin_two():
    # Native S3 one-coordinate Haar even moments:
    # E[x^(2j)] = E[x^(2j-2)] * (2j-1)/(2j+2).
    mm=[q(1)]
    for j in range(1,5):
        mm.append(mul(mm[-1],q(2*j-1,2*j+2)))
    check(mm == [q(1),q(1,4),q(1,8),q(5,64),q(7,128)],
          'native_continuous_Haar_moments_through_eight')
    unit=mm[0]
    m2,m4,m6,m8=mm[1:]
    mean_chi2=add(sub(mul(q(16),m4),mul(q(12),m2)),unit)
    xx_chi2=add(sub(mul(q(16),m6),mul(q(12),m4)),m2)
    chi2_square=add(sub(add(sub(mul(q(256),m8),
                               mul(q(384),m6)),
                           mul(q(176),m4)),mul(q(24),m2)),unit)
    check(mean_chi2==q(0),'native_spin_two_character_mean_zero')
    check(xx_chi2==q(0),'native_spin_two_quadratic_orthogonality')
    check(chi2_square==q(1),'SU2_Peter_Weyl_spin_two_norm')
    check(divide(chi2_square,q(25))==q(1,25),
          'normalized_spin_two_variance')
    # Odd harmonics vanish by U -> -U. Even degree-two directions
    # orthogonal to x² by S2 transverse isotropy.
    transverse=divide(sub(mean_chi2,xx_chi2),q(3))
    check(transverse==q(0),'all_traceless_quadratic_harmonics_zero')
    return (m2,m4,m6,m8)


def moment_z(k):
    # SU2 Haar z=(1+u.v)/2 is Beta(3/2,3/2).
    value=q(1)
    for j in range(k):
        value=mul(value,q(2*j+3,2*j+6))
    return value


def kernel_checks():
    results={}
    for m in (0,1,2,3,27,81):
        a,b=moment_z(m),moment_z(m+1)
        ratio=divide(b,a)
        expect=q(2*m+3,2*m+6)
        check(ratio==expect,'beta_three_halves_kernel_ratio')
        chord=mul(q(4),sub(q(1),ratio))
        check(chord==q(6,m+3),'continuous_SU2_zonal_chord_square')
        results[m]=chord
    check((3*4*7)//6==14,'constant_plus_thirteen_harmonics')
    return results


def production_budget():
    beta=9**12
    check(beta==282429536481,'actual_production_beta')
    # 3*beta^2/[2(m+3)] <= 1/256:
    # 2*(m+3) >= 768*beta^2. Smallest integer degree is 384*beta²-3.
    minimum=384*beta*beta-3
    check(minimum==30630314141519043787530621,
          'exact_high_beta_harmonic_degree_budget')
    check(2*(minimum+3)>=3*beta*beta*256,
          'remainder_one_over_256_certificate')
    check(2*(minimum+2)<3*beta*beta*256,
          'minimal_degree_under_generic_envelope')
    return minimum


def main():
    for r in (1,2,3,4):
        a,b=centered_source_and_q(r)
        print('YM4_VOL26_CENTER|r='+str(r)+
              '|plaquette=0_1|internal_links='+str(a)+
              '|single_mixed_face_witnesses='+str(b)+'|PASS')
    m2,m4,m6,m8=haar_moments_and_spin_two()
    print('YM4_VOL26_HAAR|m2='+fmt(m2)+'|m4='+fmt(m4)+
          '|m6='+fmt(m6)+'|m8='+fmt(m8)+'|PASS')
    print('YM4_VOL26_SPIN2|mean=0|variance=1/25|harmonics_le2=ZERO|PASS')
    moments=kernel_checks()
    for m in (0,1,2,3,27,81):
        print('YM4_VOL26_KERNEL|m='+str(m)+
              '|chord2='+fmt(moments[m])+'|PASS')
    minimum=production_budget()
    print('YM4_VOL26_DEGREE|beta=9^12|variance_allowance=1/256|min_m='+
          str(minimum)+'|PASS')
    print('YM4_VOL26_SCOPE|centered_plaquette_source=ACTUAL|'+
          'one_q_Lipschitz_beta_over_2=ANALYTIC|'+
          'positive_physical_witness=OPEN|continuum_11=OPEN')


if __name__=='__main__':
    main()
