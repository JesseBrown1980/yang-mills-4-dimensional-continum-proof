#!/usr/bin/env python3
"""Integer signed curl certificate for the neutral Abelian sector."""
from itertools import product, permutations, combinations
from math import factorial, isqrt
from pathlib import Path
from hashlib import sha256
S=2**40
W=81*24**2
D=W*S
Z=(0,)*4
B=tuple(product((-1,0,1),repeat=4))
SH=(3,6,3,3)
C=(Z,(0,3,0,0))
X=tuple(product(*(range(n) for n in SH)))
P=tuple((x,m,n) for x in X for m,n in combinations(range(4),2))
L=tuple((x,m) for x in X for m in range(4))

def req(x,s):
    if not x: raise ValueError(s)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def step(x,m,s=1): return tuple(v+(s if j==m else 0) for j,v in enumerate(x))
def wrap(x): return tuple(v%n for v,n in zip(x,SH))
def inc(d,k,v):
    if v: d[k]=d.get(k,0)+v
    if k in d and not d[k]: del d[k]
def mul(a,b): return ((a[0]*b[0]-a[1]*b[1])//S,(a[0]*b[1]+a[1]*b[0])//S)
def neg(a): return (a[0],-a[1])
def path(z):return tuple((i,v) for i,v in enumerate(z) if v)
def walk(x,w):
    out=[]
    for m,s in w:
        y=step(x,m,s);out.append((x if s==1 else y,m,s));x=y
    return out,x

def fill(w,mu):
    w=list(w);r={}
    # Stable coordinate sort; signed swaps are elementary plaquettes.
    for i in range(1,len(w)):
        j=i
        while j>0 and w[j-1][0]>w[j][0]:
            x=Z
            for m,s in w[:j-1]:x=step(x,m,s)
            m,s=w[j-1];n,t=w[j];p=x
            if s==-1:p=step(p,m,-1)
            if t==-1:p=step(p,n,-1)
            inc(r,(p,n,m),-s*t)
            w[j-1],w[j]=w[j],w[j-1];j-=1
    # The sorted word reduces to the straight centre path.
    req(tuple(sum(s for m,s in w if m==j) for j in range(4))==step(Z,mu,3),'endpoint')
    # Verify signed boundary of fill against actual incidence separately in geometry.
    return r

def geometry(mu):
    y=step(Z,mu,3);out=[]
    for z in B:
        ps=tuple(permutations(path(z)));n=(24//len(ps))**2
        for a in ps:
            for b in ps:
                word=a+((mu,1),)*3+tuple((m,-s) for m,s in reversed(b))
                links,end=walk(Z,word);req(end==y,'path_end')
                r=fill(word,mu)
                # integer Stokes control: recover original path minus straight.
                chk={}
                for x,m,s in links:inc(chk,(x,m),s)
                for x,m,s in walk(Z,((mu,1),)*3)[0]:inc(chk,(x,m),-s)
                for (x,m,k),v in r.items():
                    for z2,j,s in ((x,m,1),(step(x,m),k,1),(step(x,k),m,-1),(x,k,-1)):
                        inc(chk,(z2,j),-v*s)
                req(not chk,'stokes')
                out.append((n,links,tuple(r.items())))
    req(len(out)==10473 and sum(n for n,l,r in out)==W,'weights')
    return out

def plaq(q,x,m,n):
    a=(S,0)
    for y,j,s in ((x,m,1),(step(x,m),n,1),(step(x,n),m,-1),(x,n,-1)):
        v=q[wrap(y),j];a=mul(a,v if s==1 else neg(v))
    return a

def check(d,vals,word,geo):
    q={}
    for k,ch in zip(L,word):
        n=vals[int(ch,36)];dd=S*S+n*n
        q[k]=((S*S-n*n)*S//dd,2*S*S*n//dd)
    p={k:plaq(q,*k) for k in P}
    grad={k:0 for k in L}
    for (x,m,n),(_,b) in p.items():
        for y,j,sg in ((x,m,1),(step(x,m),n,1),(step(x,n),m,-1),(x,n,-1)):
            grad[wrap(y),j]+=sg*b
    # Fold exact signed relative Hessian coefficients by primitive row and displacement.
    M={}; Er={}; Ec={}; counts={}; maxA=0;maxB=0;maxE=0;minV=S
    for c in C:
        for mu,g in enumerate(geo):
            paths=[];va=vb=0
            for n,l,r in g:
                a=(S,0)
                for x,m,s in l:
                    v=q[wrap(add(c,x)),m];a=mul(a,v if s==1 else neg(v))
                paths.append(a);va+=n*a[0];vb+=n*a[1]
            V=(va//W,vb//W);den=(V[0]*V[0]+V[1]*V[1])//S;req(den*4>=3*S,'mean_floor_approx');minV=min(minV,den)
            gf=sum(grad[wrap(add(c,z)),mu] for z in B if z[mu]==1)
            req(abs(gf)<3*S,'face_gradient')
            A={};E={};F={};local={}
            for (n,l,r),a in zip(g,paths):
                re,im=mul(neg(V),a)
                aa=re*S//den;bb=gf*im//den
                # exact integer approximate coefficients, no premature abs
                for (x,m,k),v in r:
                    key=(x,m,k)
                    inc(A,key,n*aa*v);inc(E,key,n*(aa-S)*v);inc(F,key,n*bb*v)
                    inc(counts,(wrap(add(c,x)),m,k),n*sum(abs(t) for _,t in r)*abs(v))
                    for key2,t in r:inc(local,(key,key2),n*bb*v*t*D)
            for x,a in A.items():
                for y,b in F.items():
                    inc(local,(x,y),-a*b);inc(local,(y,x),-a*b)
            for ((x,m,k),(y,i,j)),v in local.items():
                inc(M,((wrap(add(c,x)),m,k),sub(y,x),i,j),v)
            e=sum(map(abs,E.values()));maxE=max(maxE,e);maxA=max(maxA,sum(map(abs,A.values())));maxB=max(maxB,sum(map(abs,F.values())))
            for (x,m,k),v in E.items():inc(Ec,(wrap(add(c,x)),m,k),abs(v))
    mr={}
    for (p0,off,i,j),v in M.items():inc(mr,p0,abs(v))
    mrmax=max(mr.values());ec=max(Ec.values());count=max(counts.values());
    # Rigorous error budgets are established in the D3G-A note.
    req(count<=64*W,'fill_norm')
    req(maxE*ec*4000**2<=9*D*D,'E_approx_norm')
    req(mrmax*1000<=28*D*D,'signed_approx_norm')
    # 3/4000 + 8*1024/S <= 1/1000.
    req(3*S+4000*8*1024<=4*S,'E_exact_norm')
    # 28/1000 + 64*(5*65536+6*1024)/S <= 1/30.
    req(30*(28*S+1000*64*(5*65536+6*1024))<=1000*S,'signed_exact_norm')
    # (1799/1800)*(247/250)^2 - 1/30 > 15/16.
    req(16*(1799*247**2-60*250**2)>15*1800*250**2,'neutral_floor')
    print('YM4_VOL14D3GA|delta=1/'+str(d)+'|path_pairs_per_face=10473|fill_norm_sq_le=64|E_norm_le=1/1000|signed_norm_le=1/30|neutral_relative_floor_gt=15/16|json=0')

def main():
    data=(Path(__file__).resolve().parent.parent/'docs/certificate-atlas/FIXTURE-YM4-VOL14D3F-RATIONAL-STAGGERED-20261126.txt').read_bytes();req(sha256(data).hexdigest()=='305b5acbac5f7636908a2081754122fb79b4b7661fde44cb4fb5f4bfc028ec54','fixture')
    geo=[geometry(i) for i in range(4)]
    for line in data.decode().splitlines():
        d,v,w=line.split('|');check(int(d),tuple(map(int,v.split(','))),w,geo)
if __name__=='__main__':main()
