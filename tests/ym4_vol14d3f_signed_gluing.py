#!/usr/bin/env python3
"""D2 pinned stencil replay, with exact signed window gluing and KKT inertia tests."""
from itertools import product, permutations

B = tuple(product((-1, 0, 1), repeat=4))
Z = (0,)*4
D = 1944
LINKS = [(x,m) for x in B for m in range(4)]
LIDX = {l:i for i,l in enumerate(LINKS)}
PLAQ = [(x,m,n) for x in B for m in range(4) for n in range(m+1,4)]


def require(ok, name):
    if not ok:
        raise ValueError(name)


def add(x,y):
    return tuple(a+b for a,b in zip(x,y))


def sub(x,y):
    return tuple(a-b for a,b in zip(x,y))


def unit(m,s=1):
    return tuple(s if i==m else 0 for i in range(4))


def canon(x):
    k=tuple((a+1)//3 for a in x)
    return k,tuple(a-3*b for a,b in zip(x,k))


def path(z):
    return tuple((i,1 if v>0 else -1) for i,v in enumerate(z)
                 for unused in range(abs(v)))


def inc(d,k,v):
    d[k]=d.get(k,0)+v
    if not d[k]:
        del d[k]


def walk(t,x,steps,w):
    for m,s in steps:
        y=add(x,unit(m,s))
        inc(t,(x if s>0 else y,m),s*w)
        x=y
    return t


def build():
    tree=set()
    for z in B:
        tree.update(walk({},Z,path(z),1))
    require(len(tree)==80,"tree")
    L=[]
    for m in range(4):
        r={}
        y=unit(m,3)
        for z in B:
            ps=set(permutations(path(z)))
            require(24%len(ps)==0,"connector_weight")
            walk(r,z,((m,1),)*3,24)
            for p in ps:
                walk(r,Z,p,24//len(ps))
                walk(r,y,p,-24//len(ps))
        require(len(r)==459 and sum(v*v for v in r.values())*729==277*D*D,"L_row")
        cross=[(x,i,v) for (x,i),v in r.items() if canon(x)[1][i]==1]
        require(len(cross)==27 and all(i==m and x[m]==1 and 27*v==D for x,i,v in cross),"L_cross")
        L.append(r)
    # T P_Z on the ambient block link space, with denominator D.
    # P_Z kills tree links and subtracts each crossing mean.
    # L's crossing coefficients are constant on its sole crossing face,
    # so L P_Z keeps precisely the non-tree internal coefficients.
    T=[]
    for x,m in LINKS:
        r={}
        if (x,m) not in tree:
            r[x,m]=D
            if x[m]==1:
                for y in B:
                    if y[m]==1:
                        inc(r,(y,m),-(D//27))
                for (y,i),v in L[m].items():
                    unused,loc=canon(y)
                    if loc[i]!=1 and (loc,i) not in tree:
                        inc(r,(y,i),-v)
        require(all(sum(map(abs,canon(y)[0]))<=1 for y,i in r),"T_range")
        T.append(r)
    K=[]
    for x,m,n in PLAQ:
        r={}
        for y,i,sg in ((x,m,1),(add(x,unit(m)),n,1),
                       (add(x,unit(n)),m,-1),(x,n,-1)):
            a,loc=canon(y)
            shift=tuple(3*v for v in a)
            for (s,j),v in T[LIDX[loc,i]].items():
                inc(r,(add(s,shift),j),sg*v)
        allowed={Z,unit(m),unit(n),add(unit(m),unit(n))}
        require(all(canon(s)[0] in allowed for s,j in r),"K_range")
        K.append(r)
    return T,K


def fold(rows):
    out=[]
    for row in rows:
        r={}
        for (x,m),v in row.items():
            inc(r,LIDX[canon(x)[1],m],abs(v))
        out.append(r)
    return out


def next_weight(u):
    top=max(u)
    require(top>0,"nonzero_matrix")
    return [max(1,(x*1048576+top-1)//top) for x in u]


def gram_bounds(rows,den):
    w=[1]*324
    bs=[]
    for unused in range(12):
        v=[sum(a*w[j] for j,a in r.items()) for r in rows]
        u=[0]*324
        for r,t in zip(rows,v):
            for j,a in r.items():
                u[j]+=a*t
        b=max((x+den*den*y-1)//(den*den*y) for x,y in zip(u,w))
        require(all(x<=b*den*den*y for x,y in zip(u,w)),"gram_positive_weight")
        bs.append(b)
        w=next_weight(u)
    return bs


def hessian(K):
    H={}
    for r in K:
        a=[(q,LIDX[x,m],v) for (s,m),v in r.items() for q,x in (canon(s),)]
        for q,i,v in a:
            for q2,j,w in a:
                inc(H,(sub(q2,q),i,j),v*w)
    require(all(H.get((tuple(-x for x in a),j,i),0)==v
                for (a,i,j),v in H.items()),"H_adjoint")
    offsets={a for a,i,j in H}
    require(len(offsets)==33 and max(sum(map(abs,a)) for a in offsets)==2,"H_offsets")
    require(len(H)==525780,"H_integer_entries")
    return H



def tent(r,x):
    return max(0,r-abs(x))


def radius_test():
    T,K=build()
    H=hessian(K)
    mats=[[{} for unused in LINKS] for unused in range(2)]
    for (a,i,j),v in H.items():
        l=sum(map(abs,a))
        require(all(abs(x)<=1 for x in a),"stencil_coordinate_range")
        if l:
            inc(mats[l-1][i],j,abs(v))
    def apply(mat,w):
        return [sum(v*w[j] for j,v in row.items()) for row in mat]
    w=[1]*324
    for unused in range(12):
        a,b=(apply(mat,w) for mat in mats)
        w=next_weight([4160*x+16641*y for x,y in zip(a,b)])
    a,b=(apply(mat,w) for mat in mats)
    def test(r):
        s=r*(2*r*r+1)//3
        t=s-r
        require(s==sum(tent(r,x)**2 for x in range(1-r,r)),"tent_norm")
        require(t==sum(tent(r,x)*tent(r,x+1) for x in range(1-r,r)),"tent_overlap")
        return all(4620*(r*t*x+(s*s-t*t)*y)<=23*D*D*t*t*z for x,y,z in zip(a,b,w))
    require(test(99) and not test(98),"radius_witness")
    print("YM4_VOL14D3F|flat_offsets=33|entries=525780|tent_radius=99|side=197|preceding_radius=REJECTED_BY_FIXED_WITNESS|compensation_norm_le=23/4620|flat_patch_floor=1/220|json=0")


def signed_window():
    points=tuple(product(range(2),repeat=4))
    off=tuple(a for a in B if sum(map(abs,a))<=2)
    def wrap(x):
        return tuple(v%2 for v in x)
    def value(x):
        return 1+sum((i+1)*v for i,v in enumerate(x))
    def coeff(x,a):
        y=wrap(add(x,a))
        l=sum(map(abs,a))
        return 300+sum(x) if not l else sum((i+1)*(v+w) for i,(v,w) in enumerate(zip(x,y)))%7-3
    def w(x):
        p=1
        for v in x:
            p*=tent(2,v)
        return p
    direct=sum(coeff(x,a)*value(x)*value(wrap(add(x,a))) for x in points for a in off)
    out=0
    bad=0
    require(16*300>32*36*3,"strict_local_diagonal_dominance")
    for c in points:
        for z in B:
            x=wrap(add(c,z))
            for a in off:
                l=sum(map(abs,a))
                v=coeff(x,a)*value(x)*value(wrap(add(x,a)))*w(z)*w(add(z,a))
                out+=(16,24,36)[l]*v
                bad+=16*v
    require(out==16*6**4*direct,"signed_wrapped_glue")
    require(bad!=out,"omitted_compensation")


def inertia(m):
    a=[list(row) for row in m]
    p=n=0
    while a:
        k=next((i for i,r in enumerate(a) if r[i]),None)
        require(k is not None,"fixture_nonzero_pivot")
        a[0],a[k]=a[k],a[0]
        for row in a:
            row[0],row[k]=row[k],row[0]
        d=a[0][0]
        sg=1 if d>0 else -1
        p+=int(d>0)
        n+=int(d<0)
        a=[[sg*(d*a[i][j]-a[i][0]*a[0][j]) for j in range(1,len(a))] for i in range(1,len(a))]
    return p,n


def kkt_test():
    a=[[4,1,0],[1,3,-1],[0,-1,2]]
    c=[[2,-1],[0,3],[-2,2]]
    d=[[-5,2],[2,-3]]
    def kkt(a):
        return [a[i]+c[i]+[0,0] for i in range(3)]+[
            [c[j][i] for j in range(3)]+d[i]+[int(i==j) for j in range(2)] for i in range(2)]+[
            [0,0,0]+[int(i==j) for j in range(2)]+[0,0] for i in range(2)]
    require(inertia(a)==(3,0) and inertia(kkt(a))==(5,2),"KKT_inertia")
    a[0][0]=-4
    require(inertia(a)==(2,1) and inertia(kkt(a))==(4,3),"negative_tangent")


def main():
    radius_test()
    signed_window()
    kkt_test()
    print("YM4_VOL14D3F|signed_wrapped_window_identity=PASS|omitted_compensation=REJECTED|KKT_inertia=PASS|negative_tangent=REJECTED|json=0")
    print("YM4_VOL14D3F|exact_stationarity=OPEN|augmented_relative_floor=OPEN|uniform_minimizer_angle=OPEN|continuum=OPEN|json=0")


if __name__=="__main__":
    main()
