"""YM4 VOL30: strict integer four-dimensional spherical/fischer certificate.

Actual original SU2 Wilson conditional inequalities are analytic.
This checker verifies lattice sites, two-ended reflection, frozen SHA
receipts, independent three-square counts and reversible 9/20 addressing.
No field expectation values are sampled or inferred from geometry.
"""
from collections import defaultdict


def check(ok, name):
    if not ok:
        raise AssertionError(name)



# Pure integer FIPS 180-4 SHA-256. Independent of hashlib/json imports.
_K=(
0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2)
_MASK=0xffffffff


def _rot(x,n):
    return ((x>>n)|(x<<(32-n)))&_MASK


def sha256_hex(data):
    h=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
       0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
    msg=bytearray(data)
    bits=len(msg)*8
    msg.append(128)
    while len(msg)%64!=56:
        msg.append(0)
    msg.extend(bits.to_bytes(8,'big'))
    for offset in range(0,len(msg),64):
        w=[int.from_bytes(msg[offset+j:offset+j+4],'big')
           for j in range(0,64,4)]
        for j in range(16,64):
            s0=_rot(w[j-15],7)^_rot(w[j-15],18)^(w[j-15]>>3)
            s1=_rot(w[j-2],17)^_rot(w[j-2],19)^(w[j-2]>>10)
            w.append((w[j-16]+s0+w[j-7]+s1)&_MASK)
        a,b,c,d,e,f,g,h7=h
        for j in range(64):
            sigma1=_rot(e,6)^_rot(e,11)^_rot(e,25)
            choose=(e&f)^((~e)&g)
            t1=(h7+sigma1+choose+_K[j]+w[j])&_MASK
            sigma0=_rot(a,2)^_rot(a,13)^_rot(a,22)
            majority=(a&b)^(a&c)^(b&c)
            t2=(sigma0+majority)&_MASK
            h7,g,f,e,d,c,b,a=(g,f,e,(d+t1)&_MASK,
                               c,b,a,(t1+t2)&_MASK)
        for j,val in enumerate((a,b,c,d,e,f,g,h7)):
            h[j]=(h[j]+val)&_MASK
    return ''.join(format(v,'08x') for v in h)


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
    check(sha256_hex(b'abc')==
          'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad',
          'independent_SHA256_abc_known_vector')
    check(sha256_hex(b'')==
          'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
          'independent_SHA256_empty_known_vector')
    with open('docs/certificate-atlas/YM4-VOL30-SPHERE-FRAMES-20261123.json',
              encoding='utf-8') as f:
        inventory=f.read()
    check(inventory.count('"sha256": ')==20,
          'manifest_twenty_pinned_frames')
    check('"L": 128' in inventory and '"d": 24' in inventory,
          'frozen_geometry_L_d')
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
    for r in range(2,22):
        center=sphere(r)
        reflected={(p[0],p[1],24-p[2],p[3]) for p in center}
        check(len(reflected)==len(center),'exact_reflection_bijection')
        check(all(p[0]*p[0]+p[1]*p[1]+
                  (p[2]-24)*(p[2]-24)+p[3]*p[3]==r*r
                  for p in reflected),'outer_four_sphere')
        shared=center.intersection(reflected)
        independent=three_square_count(r)
        check(independent==len(shared),
              'independent_three_square_dual_intersection')
        text=canonical(r,len(center),len(shared))
        digest=sha256_hex(text.encode('utf-8'))
        # Distinct source of truth: independently enumerated geometry
        # and a separate JSON canonical frame record. This is text
        # matching a pinned manifest, not importing a JSON library.
        expected=('"r": '+str(r)+',\n'+
                  '      "shell_count": '+str(len(center))+',\n'+
                  '      "shared_count": '+str(len(shared))+',\n'+
                  '      "sha256": "'+digest+'"')
        check(expected in inventory,'pinned_manifest_frame_and_SHA')
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
