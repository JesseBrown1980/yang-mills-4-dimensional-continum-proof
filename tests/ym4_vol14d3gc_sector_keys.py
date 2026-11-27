#!/usr/bin/env python3
"""Cantor sector addresses and integer nearby-stationarity inequalities."""
from itertools import product
from pathlib import Path
from hashlib import sha256

PER=(4,2,4,4)
GROUP=tuple(product(*(range(n) for n in PER)))
FIXTURE='305b5acbac5f7636908a2081754122fb79b4b7661fde44cb4fb5f4bfc028ec54'


def req(ok,why):
    if not ok:
        raise ValueError(why)


def opposite(k):
    return tuple((-v)%n for v,n in zip(k,PER))


def cantor(i):
    a=0
    for j in range(8):
        a=3*a+2*((i>>(7-j))&1)
    return a


def key_test():
    f=Path(__file__).resolve().parent.parent/'docs/certificate-atlas/FIXTURE-YM4-VOL14D3F-RATIONAL-STAGGERED-20261126.txt'
    req(sha256(f.read_bytes()).hexdigest()==FIXTURE,'source')
    reps=[(0,k) for k in GROUP if k<=opposite(k)]+[(1,k) for k in GROUP]
    cover={}
    seen=set()
    addresses=[]
    for i,(c,k) in enumerate(reps):
        a=cantor(i)
        mate=(-c,opposite(k))
        # Include source and basis domain in the address, not only the digit word.
        key=(FIXTURE,'tree-zero-transported-Z',c,k,a)
        req(key not in seen,'key_collision')
        seen.add(key);addresses.append(a)
        for s in {(c,k),mate}:
            req(s not in cover,'sector_double_count')
            cover[s]=key
    req(len(reps)==200 and len(cover)==384 and len(set(addresses))==200,'coverage')
    req(all(0<=a<6561 for a in addresses),'cantor_span')
    req(len([k for c,k in reps if c==0])==72,'neutral')
    req(all(cover[c,k]==cover[-c,opposite(k)] for c,k in cover),'conjugate')
    for a in addresses:
        for unused in range(8):
            req(a%3 in (0,2),'cantor_digits');a//=3
    # Full graded threshold schedule: threshold is an extra parameter, not a new mode.
    grades=((1,3),(1,2),(2,3))
    req(len({(key,n,d) for key in seen for n,d in grades})==600,'graded_keys')
    req(len({(delta,key,n,d) for delta in (30,36) for key in seen for n,d in grades})==1200,'fixture_separation')
    print('YM4_VOL14D3GC|cantor_depth=8|address_span=6561|representatives=200|covered_sectors=384|neutral=72|charged=128|grades=3|fixture_keys=1200|json=0')


def enclosure():
    # D3F deficits and D3GA curl bound are premises, replayed separately.
    # 1-cos(t) >= t^2/2-t^4/24 for t=1/d-1/100000.
    for d,v in ((36,385412410),(30,554965836)):
        a=100000-d;b=100000*d
        req((12*a*a*b*b-a**4)*10**12>24*b**4*v,'angle_slack')
    req(56*100000<10**7,'angle_ball')
    req(11*8*10**7<=13*(7*10**7-88),'repair_angle')
    # |P/V-P0/V0| <=154*(8/7+64/49)*r <400r.
    req(154*(56+64)<400*49,'ratio_lipschitz')
    req(162*56*8+2*400*7<12000*7,'multiplier_lipschitz')
    req(10**7+1000*8*400<2*10**7,'E_ball')
    req(10**7+30*64*(5*12000+6*400)<13*10**7,'signed_ball')
    req(2*(1799-780)*125**2>1800*128**2,'relative_half')
    req(26**2>648 and 26*16*210*10**7<10**12,'inward_gradient')
    print('YM4_VOL14D3GC|chart_radius=1/10000000|angle_slack_gt=1/100000|relative_neutral_floor_gt=1/2|primitive_nearby_stationary=DERIVED|charged_floor=OPEN|global_minimizer=OPEN|json=0')


if __name__=='__main__':
    key_test();enclosure()
