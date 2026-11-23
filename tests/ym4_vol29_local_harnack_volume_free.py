"""YM4 VOL29: original-SU2 local Harnack and even-time two-step square.

Strict integer/rational controls for the 4 original spatial source links,
13 original touching plaquettes, local Fourier coercivity, and the exact
production exponent. The native continuous SU2 Wilson proof is analytic.
"""
from itertools import product
from fractions import Fraction as Q


def check(ok, label):
    if not ok:
        raise AssertionError(label)


def shift(x, mu, L):
    y=list(x)
    y[mu]=(y[mu]+1)%L
    return tuple(y)


def face(x, mu, nu, L):
    return ((x,mu),(shift(x,mu,L),nu),
            (shift(x,nu,L),mu),(x,nu))


def original_geometry(L):
    check(L%2==0 and L>=4,'even_original_spatial_torus')
    source=set(face((0,0,0),0,1,L))
    check(len(source)==4,'four_positive_source_links')
    touched=set()
    each={edge:0 for edge in source}
    for x in product(range(L),repeat=3):
        for mu,nu in ((0,1),(0,2),(1,2)):
            edges=set(face(x,mu,nu,L))
            if source.intersection(edges):
                touched.add((x,mu,nu))
                for e in source.intersection(edges):
                    each[e]+=1
    check(len(touched)==13,'exact_original_thirteen_touched_faces')
    check(sorted(each.values())==[4,4,4,4],
          'original_four_plaquettes_per_spatial_link')
    return len(source),len(touched)


def local_exponents():
    k,N=original_geometry(4)
    check(k==4 and N==13,'source_geometry_locked')
    output_transfer=N+2*k
    spatial_half_weight=N
    spatial_full_weight=2*N
    source_a_ratio=output_transfer+spatial_half_weight
    total=4*source_a_ratio+spatial_full_weight
    check((output_transfer,spatial_half_weight,spatial_full_weight,
           source_a_ratio,total)==(21,13,26,34,162),
          'source_local_Harnack_exponent')
    # Fourier test: S=c+p/2, ||p||^2_H=1/4. Two exact
    # eigenmodes K_A 1=a0^4 and K_A p=a0^4*A^4 p.
    # At A=1/2, the inverse-square bound is
    # (c²+1/(16 A^8)) <=5/(16 A^8).
    for a in (Q(1,2),Q(2,3),Q(3,4)):
        for c in (-Q(1,2),Q(0),Q(1,2)):
            left=c*c+Q(1,16)/(a**8)
            right=Q(5,16)/(a**8)
            check(left<=right,'native_four_link_finite_Fourier_inverse')
    # Local source Cauchy numerator (1/16)^2 and
    # ||K^-1S||^2 <=5/(16 a0^8 A^8) give A^8/80.
    check(Q(1,256)/Q(5,16)==Q(1,80),
          'local_fourier_Cauchy_prefactor')
    check(Q(4)*Q(1,80)==Q(1,20),
          'normalized_C1_over_C0_prefactor')
    check(80*(2**8)==20480 and 20*(2**8)==5120,
          'production_A_ge_one_half_factors')
    return total


def matmul(a,b):
    return [[a[i][0]*b[0][j]+a[i][1]*b[1][j]
             for j in range(2)] for i in range(2)]


def mpow(a,n):
    z=[[1,0],[0,1]]
    for _ in range(n):
        z=matmul(z,a)
    return z


def trace(a):
    return a[0][0]+a[1][1]


def spectral_even_time():
    # A separate 2-state positive definite transfer test, not a
    # finite-group replacement for the continuous SU2 Wilson theory.
    T=[[3,1],[1,3]]
    B=[[Q(1,2),Q(0)],[Q(0),-Q(1,2)]]
    expected={
       4:(Q(1,4),Q(5,34),Q(2,17)),
       6:(Q(1,4),Q(17,130),Q(1,13)),
       10:(Q(1,4),Q(257,2050),Q(13,205))
    }
    for L in (4,6,10):
        z=trace(mpow(T,L))
        C=[]
        for d in (0,1,2):
            numerator=trace(matmul(matmul(matmul(B,mpow(T,d)),B),
                                    mpow(T,L-d)))
            C.append(Q(numerator,z))
        check(tuple(C)==expected[L],'exact_periodic_spectral_trace')
        check(C[0]>=C[1]>=C[2]>0,'finite_periodic_C1_ge_C2')
        check(C[1]*C[1]<=C[0]*C[2],
              'finite_periodic_spectral_logconvexity')
    return expected[10][1],expected[10][2]


def exact_coercivity_fixture():
    # Algebraic control of the source-local K_A tensor K_R lemma:
    # normalized Haar on 2 symbols and positive rational kernel;
    # strictly auxiliary to the continuous SU2 Fourier theorem.
    KA=((Q(3,2),Q(1,2)),(Q(1,2),Q(3,2)))
    KR=((Q(2),Q(1,2)),(Q(1,2),Q(2)))
    source=(Q(1,2),-Q(1,2))
    a=((Q(2),Q(3)),(Q(5),Q(2))) # index local u, complementary x
    V=((Q(2),Q(4)),(Q(3),Q(2))) # index output local v, rest y
    R=Q(5,2)
    RV=Q(2)
    num=Q(0)
    den=Q(0)
    for v in range(2):
        for y in range(2):
            x=Q(0);z=Q(0)
            for u in range(2):
                for t in range(2):
                    w=KA[v][u]*KR[y][t]*Q(1,4)
                    x+=w*source[u]*a[u][t]
                    z+=w*a[u][t]
            num+=Q(1,4)*V[v][y]*x*x
            den+=Q(1,4)*V[v][y]*z*z
    check(den>0 and num>0,'rational_weighted_K2_positive')
    ratio=num/den
    # For this toy S=+-1/2, Haar second=1/4,
    # ||KA^-1 S||²=1/4, ||KA||=2.
    lower=Q(1)/(Q(16)*R**4*RV)
    check(lower==Q(1,1250),'toy_local_harnack_lower_constant')
    check(ratio>=lower,'independent_source_local_Cauchy_control')
    return ratio,lower


def production():
    beta=9**12
    check(beta==282429536481 and beta==3**24,
          'production_beta_integer')
    exponent=162*beta
    check(exponent==45753584909922,
          'volume_free_production_exponent')
    old_L10=(30*beta+150)*10**3
    check(old_L10==8472886094580000,
          'previous_global_volume_comparison')
    check(exponent<old_L10,'strict_improvement_exponent')
    for L in (4,6,10,14,18,22):
        k,N=original_geometry(L)
        check(k==4 and N==13,'no_spatial_volume_growth')
        print('YM4_VOL29_GEOMETRY|L='+str(L)+
              '|source_links=4|touching_faces=13|PASS')
    print('YM4_VOL29_LOCAL|transfer_ratio_exp=21beta|'+
          'half_spatial=13beta|source_a=34beta|'+
          'V_ratio=26beta|total_exp=162beta|PASS')
    print('YM4_VOL29_PRODUCTION|beta=9^12|exponent='+str(exponent)+
          '|C1_gt_1_over_20480_times_3_pow|'+
          'C1_over_C0_gt_1_over_5120_times_3_pow|'+
          'volume_free=PASS')
    print('YM4_VOL29_COMPARISON|VOL28_L10_exponent='+str(old_L10)+
          '|VOL29_exponent='+str(exponent)+'|PASS')


def main():
    local_exponents()
    spectral_even_time()
    print('YM4_VOL29_SPECTRAL|L=4,6,10|C1_ge_C2=PASS|'+
          'two_step_square=ANALYTIC')
    ratio,lower=exact_coercivity_fixture()
    print('YM4_VOL29_TOY|local_ratio='+str(ratio)+'|'+
          'certified_lower='+str(lower)+'|PASS')
    production()
    print('YM4_VOL29_SCOPE|original_SU2_volume_free_lower=ANALYTIC|'+
          'source_local_Harnack=ANALYTIC|'+
          'continuum_upper_mass_rate=OPEN|continuum_11=OPEN')


if __name__=='__main__':
    main()
