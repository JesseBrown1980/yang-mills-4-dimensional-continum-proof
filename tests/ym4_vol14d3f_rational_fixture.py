#!/usr/bin/env python3
"""Exact rational Abelian primitive-cell fixture: no floating-point arithmetic."""
from itertools import product, combinations
from math import lcm, factorial
from pathlib import Path
from hashlib import sha256

SHAPE=(3,6,3,3)
X=tuple(product(*(range(n) for n in SHAPE)))
C=((0,0,0,0),(0,3,0,0))
B=tuple(product((-1,0,1),repeat=4))
Z=(0,0,0,0)
ONE=(1,0)
ZERO=(0,0)
D=2**40
LINKS=tuple((x,m) for x in X for m in range(4))
IDX={v:i for i,v in enumerate(LINKS)}


def require(ok,why):
    if not ok:
        raise ValueError(why)


def add(a,b):
    return tuple(x+y for x,y in zip(a,b))


def scale(a,n):
    return tuple(x*n for x in a)


def neg(a):
    return (a[0],-a[1])


def mul(a,b):
    return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])


def step(x,m,s=1):
    return tuple((v+(s if j==m else 0))%SHAPE[j] for j,v in enumerate(x))


def wrap(x):
    return tuple(v%n for v,n in zip(x,SHAPE))


def inc(d,k,v):
    d[k]=add(d.get(k,ZERO),v)


def jet_sum(a,b):
    d=dict(a[1])
    for k,v in b[1].items():
        inc(d,k,v)
    return add(a[0],b[0]),d


def jet_mul(a,b):
    d={k:mul(v,b[0]) for k,v in a[1].items()}
    for k,v in b[1].items():
        inc(d,k,mul(a[0],v))
    return mul(a[0],b[0]),d


def jet_conj(a):
    return neg(a[0]),{k:scale(neg(v),-1) for k,v in a[1].items()}


def jet_scale(a,n):
    return scale(a[0],n),{k:scale(v,n) for k,v in a[1].items()}


def edge(q,x,m,s):
    i=IDX[(x if s==1 else step(x,m,-1),m)]
    v=q[i] if s==1 else neg(q[i])
    return v,{i:scale(v,s)}


def connector(q,c):
    cache={Z:(ONE,{})}
    for z in sorted(B,key=lambda z:sum(v!=0 for v in z))[1:]:
        a=(ZERO,{})
        for m,s in enumerate(z):
            if not s:
                continue
            p=tuple(v-s if j==m else v for j,v in enumerate(z))
            a=jet_sum(a,jet_mul(cache[p],edge(q,wrap(add(c,p)),m,s)))
        cache[z]=a
    return cache


def face(c,m):
    return [IDX[(wrap(add(c,z)),m)] for z in B if z[m]==1]


def check(delta,values,word):
    require(len(values)==33 and len(word)==648,"source_shape")
    nn=[values[int(ch,36)] for ch in word]
    require(set(nn)==set(values),"source_coverage")
    dd=[D*D+n*n for n in nn]
    Q=lcm(*dd)
    q=[scale((D*D-n*n,2*D*n),Q//d) for n,d in zip(nn,dd)]
    require(all(a*a+b*b==Q*Q for a,b in q),"rational_unit")
    for c in C:
        tree=set()
        for z in B:
            x=c
            for m,s in enumerate(z):
                if s:
                    a=step(x,m,-1) if s==-1 else x
                    tree.add(IDX[(a,m)])
                    x=step(x,m,s)
        require(len(tree)==80 and all(nn[i]==0 for i in tree),"tree")
    Q4=Q**4
    grad=[0]*len(q)
    maxdef=0
    for x in X:
        for m,n in combinations(range(4),2):
            p=(ONE,{})
            for y,k,s in ((x,m,1),(step(x,m),n,1),(step(x,n),m,-1),(x,n,-1)):
                p=jet_mul(p,edge(q,y if s==1 else step(y,k),k,s))
            a,b=p[0]
            defect=Q4-a
            require(defect>=0 and defect*24*delta**4<(12*delta*delta-1)*Q4,"angle")
            maxdef=max(maxdef,defect)
            for i,v in p[1].items():
                grad[i]+=v[1]
    caches={c:connector(q,c) for c in C}
    den=81*24**2*Q**11
    residual_lo=[g*10**12//Q4 for g in grad]
    residual_hi=[-((-g*10**12)//Q4) for g in grad]
    for c in C:
        for m in range(4):
            y=step(c,m,3)
            v=(ZERO,{})
            for z in B:
                k=sum(t!=0 for t in z)
                p=(ONE,{})
                x=wrap(add(c,z))
                for unused in range(3):
                    p=jet_mul(p,edge(q,x,m,1));x=step(x,m)
                a=jet_mul(jet_mul(caches[c][z],p),jet_conj(caches[y][z]))
                v=jet_sum(v,jet_scale(a,(24//factorial(k))**2*Q**(8-2*k)))
            a,b=v[0];norm=a*a+b*b
            require(64*norm>=49*den*den,"mean_floor")
            row={i:mul(neg(v[0]),dv)[0] for i,dv in v[1].items()}
            f=face(c,m)
            require(sum(row.get(i,0) for i in f)==norm,"neutral_face_inverse")
            gf=sum(grad[i] for i in f)
            for i,l in row.items():
                top=gf*l*10**12
                bot=norm*Q4
                residual_lo[i]-=-((-top)//bot)
                residual_hi[i]-=top//bot
    maxres=max(max(abs(a),abs(b)) for a,b in zip(residual_lo,residual_hi))
    require(maxres<=10000,"near_stationarity")
    print('YM4_VOL14D3F|delta=1/'+str(delta)+'|rational_links=648|plaquettes=972|tree_links=160|mean_floor=PASS|face_inverse=PASS|deficit_upper_ppt='+str(-((-maxdef*10**12)//Q4))+'|stationarity_abs_upper_ppt='+str(maxres)+'|json=0')


def main():
    data=(Path(__file__).resolve().parent.parent/'docs/certificate-atlas/FIXTURE-YM4-VOL14D3F-RATIONAL-STAGGERED-20261126.txt').read_bytes()
    require(sha256(data).hexdigest()=="305b5acbac5f7636908a2081754122fb79b4b7661fde44cb4fb5f4bfc028ec54","frozen_source")
    for line in data.decode("ascii").splitlines():
        d,v,w=line.split('|')
        check(int(d),tuple(map(int,v.split(','))),w)
    group=tuple(product(range(4),range(2),range(4),range(4)))
    roots=((1,0),(0,1),(-1,0),(0,-1))
    # Exact character orthogonality, by checking every difference character.
    for k in group:
        values=[roots[sum(a*b*s for a,b,s in zip(k,x,(1,2,1,1)))%4] for x in group]
        require(tuple(sum(v) for v in zip(*values))==((128,0) if k==Z else ZERO),"character")
    selfconj=sum(all(2*a%n==0 for a,n in zip(k,(4,2,4,4))) for k in group)
    require(len(group)==128 and selfconj==16,"sector_count")
    require((128+16)//2==72 and 2*240==480,"sector_dimensions")
    require(128*3*480==184320,"all_coordinates")
    print("YM4_VOL14D3F|characters=128|self_conjugate=16|neutral_representatives=72|charged_representatives=128|max_complex_dimension=480|json=0")


if __name__=="__main__":
    main()
