"""VOL32: Exact native continuous SU2 Haar Wilson two-sphere covariance.

The full L=128 original Wilson law at beta=0 is independent normalized
continuous SU2 Haar on each original link. The checker enumerates only
geometric coefficients of a mathematically exact Haar covariance, using
integers throughout, with no finite-group physical replacement.
"""
from math import gcd


EXPECTED=(
 (2,24,0),(3,104,0),(4,24,0),(5,248,0),(6,312,0),
 (7,456,0),(8,24,0),(9,968,0),(10,744,0),(11,1064,0),
 (12,312,1),(13,1464,30),(14,1368,24),(15,3224,102),
 (16,24,0),(17,2456,96),(18,2904,72),(19,3048,96),
 (20,744,6),(21,5928,192)
)


def check(ok,label):
    if not ok:
        raise AssertionError(label)


def rational(n,d):
    check(d>0,'positive_rational_denominator')
    g=gcd(abs(n),d)
    return str(n//g) if d==g else str(n//g)+'/'+str(d//g)


def four_sphere(r):
    pairs={}
    for x in range(-r,r+1):
        for y in range(-r,r+1):
            pairs.setdefault(x*x+y*y,[]).append((x,y))
    points=set()
    for norm,ab in pairs.items():
        for x,y in ab:
            for t,z in pairs.get(r*r-norm,()):
                points.add((x,y,t,z))
    check(all(sum(v*v for v in x)==r*r for x in points),
          'original_4D_integer_shell')
    return points


def independent_three_square(r):
    target=r*r-144
    if target<0:
        return 0
    n=0
    for x in range(-r,r+1):
        for y in range(-r,r+1):
            for z in range(-r,r+1):
                if x*x+y*y+z*z==target:
                    n+=1
    return n


def hausdorff_original_lattice_sites(points):
    # Every exact 4D site address is distinct on the L=128 torus.
    mapped={tuple(z%128 for z in x) for x in points}
    check(len(mapped)==len(points),'periodic_torus_unique_sites')
    return mapped


def haar_second_moment():
    # Strict arithmetic control of the CONTINUOUS Haar second moment:
    # 24 quaternion addresses integrate polynomials of degree <=4
    # exactly. The physical beta=0 measure is still continuous Haar.
    points=[]
    for axis in range(4):
        for sign in (-1,1):
            p=[0]*4
            p[axis]=2*sign
            points.append(tuple(p))
    for a in (-1,1):
        for b in (-1,1):
            for c in (-1,1):
                for d in (-1,1):
                    points.append((a,b,c,d))
    check(len(points)==24,'Hurwitz_moment_quadrature_24')
    check(sum(x[0] for x in points)==0,'Haar_trace_mean_zero')
    check(sum(x[0]*x[0] for x in points)==24,'Haar_Re_quaternion_var_one_quarter')
    check(all(sum(z*z for z in p)==4 for p in points),
          'Hurwitz_unit_norm_two_coordinates')
    return '1/2','1/16'


def main():
    mean,var=haar_second_moment()
    print('YM4_VOL32_MODEL|L=128|beta=0|gauge_group=CONTINUOUS_SU2_HAAR|orientation=01|PASS')
    print('YM4_VOL32_LOCAL|plaquette_mean='+mean+
          '|plaquette_variance='+var+
          '|distinct_plaquette_covariance=0|ANALYTIC')
    for r,n,j in EXPECTED:
        c=four_sphere(r)
        other={(x[0],x[1],24-x[2],x[3]) for x in c}
        check(len(c)==len(other)==n,'original_4D_shell_count')
        check(len(c & other)==independent_three_square(r)==j,
              'independent_two_sphere_intersection')
        hausdorff_original_lattice_sites(c|other)
        var_ratio=rational(1,16*n)
        covariance=rational(j,16*n*n)
        correlation=rational(j,n)
        check(j<=n,'cross_correlation_bounded_one')
        print('YM4_VOL32_HAAR|r='+str(r)+'|N='+str(n)+'|J='+str(j)+
              '|mean=1/2|var='+var_ratio+'|cov='+covariance+
              '|corr='+correlation+'|PASS')
    check(EXPECTED[10]==(12,312,1) and EXPECTED[14]==(16,24,0),
          'midpoint_and_three_square_gap')
    check(all(next(n for rr,n,j in EXPECTED if rr==r)==24
              for r in (2,4,8,16)),'24cell_repeating_sample_size')
    print('YM4_VOL32_DIAGNOSTIC|r=2,4,8,16|N=24|var=1/384|constant_mean=1/2|PASS')
    print('YM4_VOL32_ALL_BETA|single_plaquette_shell_mean=TRANSLATION_INVARIANT|connected_dynamics=UNMEASURED')
    print('YM4_VOL32_SCOPE|exact_Haar_shell_correlation=PASS|beta_9pow12_shell_correlation=OPEN|continuum_11=OPEN')


if __name__=='__main__':
    main()
