#!/usr/bin/env python3
"""Exact signed curvature comparison on the flat-reference tree-gauge slice."""
from itertools import product, permutations, combinations

Z=(0,)*4
B=tuple(product((-1,0,1),repeat=4))
D=1944


def require(ok, why):
    if not ok:
        raise ValueError(why)


def step(x,s):
    return tuple(a+(1 if s>0 else -1) if j==abs(s)-1 else a
                 for j,a in enumerate(x))


def sub(x,y):
    return tuple(a-b for a,b in zip(x,y))


def path(z):
    return tuple((i+1)*(1 if v>0 else -1) for i,v in enumerate(z)
                 for unused in range(abs(v)))


def inc(t,k,v):
    t[k]=t.get(k,0)+v
    if not t[k]:
        del t[k]


def accum(t,s,n=1):
    for k,v in s.items():
        inc(t,k,n*v)


def edge(x,s):
    y=step(x,s)
    return (x if s>0 else y,abs(s)-1),1 if s>0 else -1


def walk(t,x,w,n):
    for s in w:
        k,sg=edge(x,s)
        inc(t,k,sg*n)
        x=step(x,s)


def swap(x,a,b):
    i,j=abs(a)-1,abs(b)-1
    require(i!=j,"perpendicular")
    y=step(step(x,a),b)
    base=tuple(min(v,w) for v,w in zip(x,y))
    sg=(1 if a*b>0 else -1)*(1 if i<j else -1)
    return (base,min(i,j),max(i,j)),sg


def internal(root,x,mu):
    v=sub(x,root)
    w=list(path(v))+[mu+1]
    p=len(w)-1
    out={}
    require(all(-1<=a<=1 for a in v) and v[mu]<1,"internal_edge")
    while p>0 and abs(w[p-1])>mu+1:
        u=root
        for a in w[:p-1]:
            u=step(u,a)
        k,sg=swap(u,w[p-1],w[p])
        inc(out,k,sg)
        w[p-1],w[p]=w[p],w[p-1]
        p-=1
    return out


def internal_signed(root,x,s):
    k,sg=edge(x,s)
    a,mu=k
    return {k:sg*v for k,v in internal(root,a,mu).items()}


def crossing_difference(x,mu):
    root2=step(step(step(Z,mu+1),mu+1),mu+1)
    u=step(Z,mu+1)
    out={}
    for a in path(tuple(v if j!=mu else 0 for j,v in enumerate(x))):
        k,sg=swap(u,a,mu+1)
        inc(out,k,sg)
        accum(out,internal_signed(Z,u,a),-1)
        accum(out,internal_signed(root2,step(u,mu+1),a),1)
        u=step(u,a)
    require(u==x,"cross_endpoint")
    return out


def constraint_row(mu):
    t={}
    y=step(step(step(Z,mu+1),mu+1),mu+1)
    for z in B:
        ps=set(permutations(path(z)))
        require(24%len(ps)==0,"connector_weight")
        walk(t,z,(mu+1,)*3,24)
        for p in ps:
            walk(t,Z,p,24//len(ps))
            walk(t,y,p,-24//len(ps))
    return t


def fold(a):
    return tuple((v+1)%3-1 for v in a)



def build():
    rows={}
    for mu in range(4):
        l=constraint_row(mu)
        root2=tuple(3 if i==mu else 0 for i in range(4))
        total={}
        for (x,i),v in l.items():
            q=crossing_difference(x,mu) if x[mu]==1 and i==mu else internal(root2 if x[mu]>=2 else Z,x,i)
            accum(total,q,v)
        for x in B:
            if x[mu]<1:
                q={k:D*v for k,v in internal(Z,x,mu).items()}
            else:
                q={k:D*v for k,v in crossing_difference(x,mu).items()}
                accum(q,total,-1)
            rows[x,mu]=q
    require(len(rows)==324 and sum(not q for q in rows.values())==80,"reconstruction")
    return rows


def actual(rows,x,mu,sg):
    a=fold(x)
    shift=sub(x,a)
    return {(tuple(t+w for t,w in zip(y,shift)),i,j):sg*v
            for (y,i,j),v in rows[a,mu].items()}


def typ(k):
    a,i,j=k
    return fold(a),i,j


def emit(s):
    print("YM4_VOL14D3B|"+s+"|json=0")


def main():
    rows=build()
    types=[(x,i,j) for x in B for i,j in combinations(range(4),2)]
    idx={k:i for i,k in enumerate(types)}
    mat=[[0]*len(types) for k in types]
    counts=0
    active={}
    for x,i,j in types:
        a=[actual(rows,x,i,1),actual(rows,step(x,i+1),j,1),
           actual(rows,step(x,j+1),i,-1),actual(rows,x,j,-1)]
        n=sum(bool(r) for r in a)
        active[n]=active.get(n,0)+1
        keys=sorted(set().union(*a))
        t=[idx[typ(k)] for k in keys]
        vals=list(zip(*[[r.get(k,0) for k in keys] for r in a]))
        for h,(f0,f1,f2,f3) in enumerate(vals):
            c0=-(f1+f2+f3)
            c1=f0-f2-f3
            c2=f0+f1-f3
            c3=f0+f1+f2
            i0=t[h]
            row=mat[i0]
            for k in range(h+1,len(keys)):
                g0,g1,g2,g3=vals[k]
                v=abs(c0*g0+c1*g1+c2*g2+c3*g3)
                if v:
                    j0=t[k]
                    row[j0]+=v
                    mat[j0][i0]+=v
                    counts+=1
    require(active=={4:282,2:132,1:72} and counts==9530764,"signed_counts")
    require(all(mat[i][j]==mat[j][i] for i in range(len(types))
                for j in range(len(types))),"symmetry")
    emit("plaquette_types=486|active1=72|active2=132|active4=282|signed_pairs=9530764")
    w=[1]*len(types)
    bs=[]
    for unused in range(12):
        u=[sum(a*b for a,b in zip(row,w)) for row in mat]
        b=max((a+D*D*v-1)//(D*D*v) for a,v in zip(u,w))
        require(all(a<=b*D*D*v for a,v in zip(u,w)),"weight")
        bs.append(b)
        top=max(u)
        w=[max(1,(a*1048576+top-1)//top) for a in u]
    require(bs==[1929,715,661,659,659,658,658,658,658,658,658,658],"weighted_ceilings")
    emit("weighted_ceilings="+",".join(str(v) for v in bs))
    require(2*658>30,"half_budget_fails")
    emit("relative_constant_le=658|delta=1/30|half_budget=FAIL")
    # 27 face links, 6 incident plaquettes, sin(delta)<=delta,
    # D3A inverse factor 315/251: 27*6*315/(30*251)=1701/251.
    require(27*6*315==1701*30,"multiplier_bound")
    emit("multiplier_norm_le=1701/251|stationary_gauge_Ward_identity=ANALYTIC|nonflat_bound=OPEN|continuum=OPEN")


if __name__=="__main__":
    main()
