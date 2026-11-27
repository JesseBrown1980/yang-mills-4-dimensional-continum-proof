#!/usr/bin/env python3
"""Distinct full-sector keys; conjugate equivalence only for computation."""
from itertools import product
from pathlib import Path
from hashlib import sha256

PER=(4,2,4,4)
G=tuple(product(*(range(n) for n in PER)))
SOURCE='305b5acbac5f7636908a2081754122fb79b4b7661fde44cb4fb5f4bfc028ec54'


def require(ok,why):
    if not ok:
        raise ValueError(why)


def mate(s):
    c,k=s
    return -c,tuple((-v)%n for v,n in zip(k,PER))


def rep(s):
    c,k=s
    if c==0:
        return min(s,mate(s))
    return s if c==1 else mate(s)


def cantor(i):
    out=0
    for j in range(9):
        out=3*out+2*((i>>(8-j))&1)
    return out


def main():
    path=Path(__file__).resolve().parent.parent/'docs/certificate-atlas/FIXTURE-YM4-VOL14D3F-RATIONAL-STAGGERED-20261126.txt'
    require(sha256(path.read_bytes()).hexdigest()==SOURCE,'source')
    sectors=tuple((c,k) for c in (0,1,-1) for k in G)
    addresses={s:cantor(i) for i,s in enumerate(sectors)}
    require(len(addresses)==384 and len(set(addresses.values()))==384,'sector_unique')
    require(all(0<=a<19683 for a in addresses.values()),'span')
    for a in addresses.values():
        for unused in range(9):
            require(a%3 in (0,2),'digits');a//=3
    grades=((1,3),(1,2),(2,3))
    keys={(SOURCE,d,'tree-zero-transported-Z',s,a) for d in (30,36) for s,a in addresses.items()}
    require(len(keys)==768,'fixture_unique')
    require(len({(key,g) for key in keys for g in grades})==2304,'grade_unique')
    reps={rep(s) for s in sectors}
    require(len(reps)==200 and all(rep(s)==rep(mate(s)) for s in sectors),'reuse')
    require(all(addresses[s]!=addresses[mate(s)] for s in sectors if s!=mate(s)),'conjugate_not_same_key')
    require(sum(s==mate(s) for s in sectors)==16,'self_conjugate')
    print('YM4_VOL14D3GC|full_sector_cantor_depth=9|address_span=19683|distinct_sector_keys_per_fixture=384|computation_representatives=200|fixture_sector_keys=768|graded_sector_keys=2304|conjugate_keys_distinct=PASS|json=0')


if __name__=='__main__':
    main()
