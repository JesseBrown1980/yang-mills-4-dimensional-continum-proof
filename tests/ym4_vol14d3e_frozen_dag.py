#!/usr/bin/env python3
"""Exact mixed quaternion jets: memoized connectors, signed factorization, frozen pencil."""
from itertools import product, permutations
from math import factorial

B=tuple(product((-1,0,1),repeat=4))
Z=(0,)*4
ONE=(1,0,0,0)
ZERO=(0,)*4
JONE=(ONE,ZERO,ZERO,ZERO)
JZERO=(ZERO,)*4


def require(ok,name):
    if not ok:
        raise ValueError(name)


def add(*vs):
    return tuple(sum(xs) for xs in zip(*vs))


def scale(v,n):
    return tuple(n*x for x in v)


def mul(a,b):
    w,x,y,z=a
    t,i,j,k=b
    return (w*t-x*i-y*j-z*k,w*i+x*t+y*k-z*j,
            w*j-x*k+y*t+z*i,w*k+x*j-y*i+z*t)


def conj(a):
    return (a[0],-a[1],-a[2],-a[3])


def ja(a,b):
    return tuple(add(x,y) for x,y in zip(a,b))


def js(a,n):
    return tuple(scale(x,n) for x in a)


def jc(a):
    return tuple(conj(x) for x in a)


def jp(a,b):
    v,x,y,h=a
    w,r,s,k=b
    return (mul(v,w),add(mul(x,w),mul(v,r)),
            add(mul(y,w),mul(v,s)),
            add(mul(h,w),mul(x,s),mul(y,r),mul(v,k)))


def step(x,i,s=1):
    return tuple(a+s if j==i else a for j,a in enumerate(x))


def edge(x,i):
    h=sum((j+1)*a for j,a in enumerate(x))+3*i
    k=h%3+1
    q=tuple(3 if j==0 else ((-1 if h%2 else 1)*4 if j==k else 0)
            for j in range(4))
    a=(0,)+tuple((h+j*j+2*j)%5-2 for j in range(1,4))
    b=(0,)+tuple((2*h+j*j+j)%7-3 for j in range(1,4))
    require(mul(q,conj(q))==(25,0,0,0),"unit_link")
    mix=(-sum(u*v for u,v in zip(a,b)),0,0,0)
    return (q,mul(q,a),mul(q,b),mul(q,mix))


def word(z):
    return tuple((i,1 if a>0 else -1) for i,a in enumerate(z) if a)


def travel(root,w):
    a=JONE
    x=root
    for i,s in w:
        y=step(x,i,s)
        f=edge(x if s>0 else y,i)
        a=jp(a,f if s>0 else jc(f))
        x=y
    return a


def depth(z):
    return sum(a!=0 for a in z)


def connectors(root):
    cache={Z:JONE}
    transitions=0
    direct=0
    ordered={Z:[JONE]}
    for z in sorted(B,key=depth)[1:]:
        raw=JZERO
        for i,s in word(z):
            p=step(z,i,-s)
            x=add(root,p)
            f=edge(x if s>0 else step(x,i,s),i)
            raw=ja(raw,jp(cache[p],f if s>0 else jc(f)))
            transitions+=1
        cache[z]=raw
        paths=[travel(root,w) for w in permutations(word(z))]
        ordered[z]=paths
        check=JZERO
        for a in paths:
            check=ja(check,a)
        require(raw==check,"all_endpoint_jets")
        direct+=len(paths)*depth(z)
    require(transitions==216 and direct==2216,"operation_counts")
    return cache,ordered


def emit(s):
    print("YM4_VOL14D3E|"+s+"|json=0")


def dag_test():
    src,sp=connectors(Z)
    # common denominator for all paths is 81*24^2*5^11.
    frozen=[]
    bad_order=False
    bad_mixed=False
    for m in range(4):
        y=step(Z,m,3)
        tar,tp=connectors(y)
        fast=JZERO
        slow=JZERO
        count=0
        for z in B:
            k=depth(z)
            middle=travel(z,((m,1),)*3)
            weight=(5**8,5**6,5**4,5**2,1)[k]*(24//factorial(k))**2
            v=jp(jp(src[z],middle),jc(tar[z]))
            fast=ja(fast,js(v,weight))
            for a in sp[z]:
                for b in tp[z]:
                    slow=ja(slow,js(jp(jp(a,middle),jc(b)),weight))
                    count+=1
            bad_order=bad_order or v!=jp(jp(middle,src[z]),jc(tar[z]))
            # Removing the mixed cross term from the first join.
            a=src[z]
            b=middle
            dropped=jp(a,b)
            dropped=dropped[:3]+(add(dropped[3],scale(mul(a[1],b[2]),-1)),)
            bad_mixed=bad_mixed or v!=jp(dropped,jc(tar[z]))
        require(count==10473 and fast==slow,"full_face_jet")
        frozen.append(fast)
    require(bad_order and bad_mixed,"negative_controls")
    require(2*4*2216==17728,"naive_connector_count")
    emit("centres=5|endpoint_jets=405|connector_products_direct=2216|connector_products_dag=216|four_face_naive=17728|shared_per_centre=216")
    emit("directions=4|pairs_per_face=10473|factorized_offsets=81|full_mixed_jets=PASS|order_mutation=REJECTED|mixed_mutation=REJECTED")


def transpose(a):
    return tuple(zip(*a))


def mm(a,b):
    return tuple(tuple(sum(x*y for x,y in zip(row,col)) for col in zip(*b)) for row in a)


def ms(a,n):
    return tuple(scale(row,n) for row in a)


def ma(*args):
    return tuple(add(*rows) for rows in zip(*args))


def gram(a,b):
    return mm(transpose(a),b)


def pencil_test():
    H=((9,-2,1),(-2,7,-3),(1,-3,8))
    M=((4,1,0),(1,3,-1),(0,-1,5))
    Y=((2,-1),(1,3),(-2,1))
    A=mm(H,Y)
    Bm=mm(M,Y)
    G0=gram(A,A)
    G1=ma(gram(A,Bm),gram(Bm,A))
    G2=gram(Bm,Bm)
    wrong=False
    for n,d in ((0,1),(1,4),(1,2),(3,4),(1,1),(5,4)):
        R=mm(ma(ms(H,d),ms(M,-n)),Y)
        fast=ma(ms(G0,d*d),ms(G1,-d*n),ms(G2,n*n))
        require(R==ma(ms(A,d),ms(Bm,-n)) and gram(R,R)==fast,"pencil_replay")
        wrong=wrong or fast!=ma(ms(G0,d*d),ms(G1,d*n),ms(G2,n*n))
    require(wrong,"pencil_sign_mutation")
    emit("fixed_pencil_thresholds=6|anchor_passes=2|residual_gram_replay=PASS|sign_mutation=REJECTED")


def main():
    dag_test()
    pencil_test()
    emit("full_nonflat_uniform_floor=OPEN|review11_adversarial_reproduction=OPEN|continuum=OPEN")


if __name__=="__main__":
    main()
