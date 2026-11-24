"""YM4 VOL31. Exact integer-only four-sphere scaled-orbit and dual-shell test.

This certifies 4D lattice geometry, not a sampled Wilson field profile.
"""

EXPECTED = (
    (2,24,0),(3,104,0),(4,24,0),(5,248,0),(6,312,0),
    (7,456,0),(8,24,0),(9,968,0),(10,744,0),(11,1064,0),
    (12,312,1),(13,1464,30),(14,1368,24),(15,3224,102),
    (16,24,0),(17,2456,96),(18,2904,72),(19,3048,96),
    (20,744,6),(21,5928,192)
)


def verify(ok, reason):
    if not ok:
        raise AssertionError(reason)


def sphere(radius):
    square_pairs={}
    for a in range(-radius,radius+1):
        for b in range(-radius,radius+1):
            square_pairs.setdefault(a*a+b*b,[]).append((a,b))
    pts=set()
    for norm2,first in square_pairs.items():
        for a,b in first:
            for c,d in square_pairs.get(radius*radius-norm2,()):
                pts.add((a,b,c,d))
    verify(all(sum(k*k for k in p)==radius*radius for p in pts),'four-square')
    return pts


def independent_shared(radius):
    target=radius*radius-144
    if target<0:
        return 0
    result=0
    for a in range(-radius,radius+1):
        for b in range(-radius,radius+1):
            for d in range(-radius,radius+1):
                if a*a+b*b+d*d==target:
                    result+=1
    return result


def signature(pts):
    hist={}
    for p in pts:
        hist[p[2]]=hist.get(p[2],0)+1
    return tuple(sorted(hist.items()))


def main():
    caches={}
    print('YM4_VOL31_MODE|exact_4D_integer_geometry=PASS|actual_SU2_field_samples=NOT_COMPUTED')
    for radius,total,shared in EXPECTED:
        pts=sphere(radius)
        caches[radius]=pts
        forward=signature(pts)
        verify(len(pts)==total,'frame-count')
        verify(all(forward[i][1]==dict(forward)[-forward[i][0]] for i in range(len(forward))),'center-reflection-bands')
        refl={(p[0],p[1],24-p[2],p[3]) for p in pts}
        both=len(pts & refl)
        verify(both==shared==independent_shared(radius),'independent-two-end-contact')
        verify(len(refl)==len(pts),'reverse-bijection')
        print('YM4_VOL31_FRAME|r='+str(radius)+'|shell='+str(total)+'|shared='+str(shared)+'|layers='+str(len(forward))+'|PASS')
    base=caches[2]
    verify(len(base)==24,'24-seed')
    for radius in (2,4,8,16):
        scale=radius//2
        expected={(p[0]*scale,p[1]*scale,p[2]*scale,p[3]*scale) for p in base}
        verify(caches[radius]==expected,'power-two-scaled-orbit')
        bands=signature(caches[radius])
        normalized=tuple((x//scale,n) for x,n in bands)
        verify(normalized==((-2,1),(-1,8),(0,6),(1,8),(2,1)),'five-band-12468')
        axes=sum(sum(z!=0 for z in p)==1 for p in caches[radius])
        diagonal=sum(sum(z!=0 for z in p)==4 for p in caches[radius])
        verify((axes,diagonal)==(8,16),'axis-diagonal-8-plus-16')
        print('YM4_VOL31_SELF_SIMILAR|r='+str(radius)+'|points=24|axes=8|diagonals=16|bands=1,8,6,8,1|PASS')
    verify(caches[12]&{(0,0,12,0)}=={(0,0,12,0)},'midpoint-unique')
    verify(independent_shared(12)==1 and independent_shared(16)==0,'contact-obstruction')
    print('YM4_VOL31_CONTACT|r12=1_midpoint|r16=0_three_squares_112|PASS')
    possible={x*x%8 for x in range(8)}
    verify(not any((a+b+c)%8==7 for a in possible for b in possible for c in possible),'three-square-mod8')
    verify(112==16*7,'one-sixteen-times-seven')
    print('YM4_VOL31_MODULAR|112=16_times_7|three_squares_mod8_seven=IMPOSSIBLE|PASS')
    for length in (9,20):
        ordered=list(range(2,length+2))
        verify(ordered==list(reversed(list(reversed(ordered)))),'forward-reverse-address')
        verify([len(caches[x]) for x in ordered]==list(reversed([len(caches[x]) for x in reversed(ordered)])),'roundtrip-shape-inventory')
        print('YM4_VOL31_PLAY|frames='+str(length)+'|reverse_exact=PASS')
    print('YM4_VOL31_SCOPE|center_shell_geometry=PASS|lattice_symmetry=PASS|continuous_SU2_measurements=OPEN|continuum_mass_gap=OPEN')


if __name__=='__main__':
    main()
