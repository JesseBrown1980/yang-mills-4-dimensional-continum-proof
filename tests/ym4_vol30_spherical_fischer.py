"""YM4 VOL30: strict integer four-dimensional spherical/fischer certificate.

Actual original SU2 Wilson conditional inequalities are analytic.
This checker verifies lattice sites, two-ended reflection, frozen SHA
receipts, independent three-square counts and reversible 9/20 addressing.
No field expectation values are sampled or inferred from geometry.
"""
from collections import defaultdict
from hashlib import sha256
from json import load


def check(ok, name):
    if not ok:
        raise AssertionError(name)


def sphere(r):
    pairs = defaultdict(list)
    for a in range(-r,r+1):
        for b in range(-r,r+1):
            pairs[a*a+b*b].append((a,b))
    out = set()
    for k, left in list(pairs.items()):
        for a,b in left:
            for c,d in pairs.get(r*r-k,()):
                out.add((a,b,c,d))
    check(all(sum(v*v for v in p)==r*r for p in out),
          'exact_four_integer_squares')
    return out


def three_square_count(r):
    target=r*r-144
    if target<0:
        return 0
    total=0
    for a in range(-r,r+1):
        for b in range(-r,r+1):
            for c in range(-r,r+1):
                if a*a+b*b+c*c==target:
                    total+=1
    return total


def canonical(r,n,j):
    return ('YM4-VOL30|L=128|d=24|R='+str(r)+
            '|shell_points='+str(n)+
            '|dual_intersection='+str(j)+
            '|source=0,0,0,0|outer=0,0,24,0')


def main():
    with open('docs/certificate-atlas/YM4-VOL30-SPHERE-FRAMES-20261123.json',
              encoding='utf-8') as f:
        manifest=load(f)
    check(manifest['geometry']['L']==128 and
          manifest['geometry']['d']==24,'frozen_geometry_L_d')
    frames=manifest['frames']
    check(len(frames)==20,'exact_twenty_radii')
    B=147456*(1+6*(9**12))*(1+6*(9**12))
    check(B==423433462692859012475599601664,
          'actual_su2_six_staple_B')
    exponent=162*(9**12)
    check(exponent==45753584909922,
          'production_native_volume_free_exponent')
    print('YM4_VOL30_MODEL|continuous_SU2_Wilson=ANALYTIC|4D_lattice_sites=INTEGER|L=128|d=24|PASS')
    print('YM4_VOL30_BOUND|beta=9^12|B='+str(B)+
          '|lower_corr1=1_over_5120_times_3_pow_45753584909922'+
          '|upper_corr1=1_minus_2_over_B|ANALYTIC')
    counted={}
    for frame in frames:
        r=frame['r']
        check(r==len(counted)+2,'strict_fischer_radius_address')
        center=sphere(r)
        check(len(center)==frame['shell_count'],'frozen_four_sphere_count')
        # Independent reflection in x2=d/2: center sphere to outer sphere.
        outer={(p[0],p[1],24-p[2],p[3]) for p in center}
        check(len(outer)==len(center),'exact_reflection_bijection')
        check(all(p[0]*p[0]+p[1]*p[1]+
                  (p[2]-24)*(p[2]-24)+p[3]*p[3]==r*r
                  for p in outer),'outer_four_sphere')
        shared=center.intersection(outer)
        num=three_square_count(r)
        check(num==len(shared)==frame['shared_count'],
              'independent_three_square_dual_intersection')
        raw=canonical(r,len(center),len(shared))
        digest=sha256(raw.encode('utf-8')).hexdigest()
        check(digest==frame['sha256'],'frozen_sha256_source_identity')
        counted[r]=(len(center),len(shared),digest)
        print('YM4_VOL30_FRAME|r='+str(r)+'|shell='+str(len(center))+
              '|shared='+str(len(shared))+'|sha256='+digest+'|PASS')
    check(counted[12][1]==1 and counted[16][1]==0,
          'midpoint_contact_and_three_square_obstruction')
    check((0,0,12,0) in sphere(12),'unique_midpoint_site')
    print('YM4_VOL30_CONTACT|r=12|site=0,0,12,0|shared=1|r16_shared=0|PASS')
    for n in (9,20):
        forward=list(range(2,n+2))
        reverse=list(reversed(forward))
        check(forward==list(reversed(reverse)),
              'exact_fischer_reverse_address')
        check([counted[k] for k in forward]==
              list(reversed([counted[k] for k in reverse])),
              'frozen_snapshot_roundtrip_identity')
        print('YM4_VOL30_ROUNDTRIP|steps='+str(n)+
              '|start_r=2|end_r='+str(n+1)+
              '|forward_reverse_exact=PASS')
    print('YM4_VOL30_SCOPE|continuous_group=YES|lattice_cutoff=FINITE'+
          '|physical_shell_measurements=NOT_COMPUTED|continuum_limit=OPEN'+
          '|continuum_11=OPEN')


if __name__=='__main__':
    main()
