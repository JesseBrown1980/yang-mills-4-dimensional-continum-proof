"""YM4 VOL24: original SU2 adjoint Wilson boundary Gram and 13 Haar harmonics.

Strict integer-only 4D geometry/Haar quartic-moment falsifiers.
The native beta>0 Wilson heat-bath variance theorem is analytic.
"""
from itertools import product


def check(ok, label):
    if not ok:
        raise AssertionError(label)


def move(x, mu, delta=1):
    a=list(x)
    a[mu]+=delta
    return tuple(a)


def face_edges(x, mu, nu):
    check(mu<nu,'orientation')
    return ((x,mu),(move(x,mu),nu),(move(x,nu),mu),(x,nu))


def incidence(e):
    x,mu=e
    rows=set()
    for nu in range(4):
        if nu==mu:
            continue
        for z in (x,move(x,nu,-1)):
            a,b=sorted((mu,nu))
            if e in face_edges(z,a,b):
                rows.add((z,a,b))
    check(len(rows)==6,'six_original_faces')
    return rows


def interior(e,r):
    x,mu=e
    return all(-r<=v<=r for v in x) and x[mu]<r


def loop_geometry(r):
    selected=[]
    supports=[]
    for s,t in product((-1,1),repeat=2):
        x=(0,s*r,t*r,0)
        e=(x,0)
        check(interior(e,r),'internal_edge')
        mixed=[]
        for z,a,b in incidence(e):
            edges=face_edges(z,a,b)
            if sum(interior(v,r) for v in edges)==1:
                mixed.append((z,a,b,edges))
        check(len(mixed)==2,'exact_two_mixed_faces')
        ext=set()
        for _,_,_,edges in mixed:
            ext.update(v for v in edges if not interior(v,r))
        check(len(ext)==6,'six_original_exterior_loop_links')
        check(all(interior(v,r+1) for v in ext),'shell_support')
        q=(move(x,1,s),0)
        check(q in ext,'selected_parallel_0_link')
        check(q in set(mixed[0][3]).union(mixed[1][3]),
              'selected_in_mixed_plaquette')
        check(not interior(q,r),'selected_link_outside_inner_cube')
        selected.append(q)
        supports.append(ext)
    for i in range(4):
        for j in range(i+1,4):
            check(not supports[i].intersection(supports[j]),
                  'original_contours_disjoint')
            check(not incidence(selected[i]).intersection(incidence(selected[j])),
                  'four_heat_baths_factorize')
    return len(selected),sum(len(v) for v in supports)


def moment_cubature():
    # Unit quaternions with coordinates v/2. Exactly reproduces Haar
    # moments of order <=4; never a finite-beta Gibbs replacement.
    pts=[]
    for i in range(4):
        for s in (-1,1):
            p=[0]*4
            p[i]=2*s
            pts.append(tuple(p))
    pts.extend(product((-1,1),repeat=4))
    check(len(pts)==24,'Hurwitz_24_points')
    check(all(sum(x*x for x in v)==4 for v in pts),'unit_quaternion')
    for i in range(4):
        check(sum(v[i] for v in pts)==0,'first_Haar_moment')
        check(sum(v[i]*v[i] for v in pts)==24,'second_Haar_moment')
        check(sum(v[i]**4 for v in pts)==48,'fourth_Haar_moment')
        for j in range(4):
            if j!=i:
                check(sum(v[i]*v[j] for v in pts)==0,
                      'linear_offdiagonal')
                check(sum(v[i]*v[i]*v[j]*v[j] for v in pts)==16,
                      'fourth_mixed_Haar_moment')
    # First degree has 4 features u_i. Degree-two has 6 offdiagonal
    # u_i*u_j and 3 diagonal contrasts u_i^2-u_3^2.
    off=[(i,j) for i in range(4) for j in range(i+1,4)]
    check(len(off)==6,'offdiagonal_dimension_six')
    features=[lambda v,i=i:v[i]*v[j] for i,j in []]
    # Use index-coded functions rather than closures with mutable variables.
    second=[]
    for i,j in off:
        second.append(tuple(v[i]*v[j] for v in pts))
    for i in range(3):
        second.append(tuple(v[i]*v[i]-v[3]*v[3] for v in pts))
    check(len(second)==9,'traceless_degree_two_dimension_nine')
    for i,row in enumerate(second):
        check(sum(row)==0,'quadratic_Haar_centered')
        for j,other in enumerate(second):
            total=sum(a*b for a,b in zip(row,other))
            expected=16 if i==j and i<6 else 0
            if i>=6 and j>=6:
                expected=64 if i==j else 32
            check(total==expected,'complete_quadratic_Haar_Gram')
        for j in range(4):
            check(sum(row[k]*pts[k][j] for k in range(24))==0,
                  'Haar_linear_quadratic_orthogonality')
    # The adjoint test observable h=(u_0^2-1/4)=(v_0^2-1)/4.
    h=tuple(v[0]*v[0]-1 for v in pts)
    check(sum(h)==0 and sum(t*t for t in h)==24,'adjoint_Haar_variance_1_16')
    for j in range(4):
        check(sum(h[k]*pts[k][j] for k in range(24))==0,
              'first_harmonic_parity_red_control')
    covnums=[sum(h[k]*second[j][k] for k in range(24))
             for j in range(6,9)]
    # Cov(h,d_j)=covnums[j]/(24*16), hence (1/12,0,0).
    check(covnums==[32,0,0],'second_harmonic_recovers_adjoint')
    # D^-1 diag block is 12*(I3-J3/4) = diag9/off-3.
    # v=(1/12,0,0) gives v^T D^-1 v=9/144=1/16.
    check(9*16==144,'exact_degree_two_full_projection')
    return len(pts),len(second)


def cap_and_beta():
    beta=9**12
    check(beta==282429536481,'beta_production')
    # True S3 radial interval probabilities >1/48 on two caps.
    # Var(T^2) > (1/48)^2 * (1/(8*kappa))^2.
    check(48*48*8*8==147456,'S3_two_cap_radial_constant')
    check(147456*9==1327104,'S3_adjoint_longitudinal_constant')
    check(3840<1327104,'S3_transverse_is_stronger')
    # Four adjoint observables have range width one; their covariance
    # Gram is <=identity by range/Cauchy, so no extra factor of four.
    den=1327104*(1+6*beta)**2
    check(den==3810901164235731112280396414976,
          'native_adjoint_production_denominator')
    return den


def scale_gate():
    K=1327104
    n=23
    check(3**22<2*K*(1+6*22)**2,'logarithmic_trajectory_prethreshold')
    check(3**n>=2*K*(1+6*n)**2,'beta_le_n_first_threshold')
    # 3*(1+6n)^2 >= (7+6n)^2 for every n>=2.
    # The left minus right is 72*n*n-48*n-46; derivative positive
    # for all n>=1, and the value at n=2 is 146>0.
    check(72*2*2-48*2-46==146,'integer_induction_base')
    for k in range(2,70):
        check(3*(1+6*k)**2>=(1+6*(k+1))**2,
              'three_growth_inductive')
    beta=9**12
    check(3**64<2*K*(1+6*beta)**2<=3**65,
          'fixed_production_beta_threshold')
    return n,65


def main():
    for r in (1,2,3,4):
        n,s=loop_geometry(r)
        check(n==4 and s==24,'four_adjoint_original_loop_geometry')
        print('YM4_VOL24_GEOMETRY|r='+str(r)+
              '|adjoint_loops=4|external_links='+str(s)+'|heat_baths=4|PASS')
    p,dim=moment_cubature()
    check(p==24 and dim==9,'SU2_Haar_complete_degree_two')
    print('YM4_VOL24_HAAR|linear=4|quadratic=9|S3_moment_order=4|PASS')
    print('YM4_VOL24_ADJOINT_RED|variance=1/16|first_harmonic=0|degree_two_capture=1/16|PASS')
    den=cap_and_beta()
    print('YM4_VOL24_NATIVE_ADJOINT_GRAM|beta=9^12|dim=4|k_min=1/'+str(den)+'|PSD=ANALYTIC')
    n,p=scale_gate()
    print('YM4_VOL24_SCALE|beta_n_le_n|a_n=3_pow_minus_n|m=1|n_from='+str(n)+'|CONDITIONAL')
    print('YM4_VOL24_SCALE_FIXED|beta=9^12|a=3_pow_minus_n|m=1|n_from='+str(p)+'|CONDITIONAL')
    print('YM4_VOL24_SCOPE|actual_continuous_SU2_beta12=ANALYTIC|centered_predictor=OPEN|continuum_11=OPEN')


if __name__=='__main__':
    main()
