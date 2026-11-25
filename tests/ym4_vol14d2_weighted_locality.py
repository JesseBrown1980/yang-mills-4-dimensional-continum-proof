#!/usr/bin/env python3
"""Integer stencil reconstruction and weighted locality bounds at b=3."""
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


def conjugation(H,p,q):
    require(p>q>0,"weight")
    # cosh(l log(p/q))-1 for l=1 or 2, common denominator 2*p*p*q*q.
    w1=(p-q)*(p-q)*p*q
    w2=(p*p-q*q)*(p*p-q*q)
    den=2*p*p*q*q*D*D
    mat=[{} for unused in LINKS]
    for (a,i,j),v in H.items():
        dist=sum(map(abs,a))
        if dist:
            inc(mat[i],j,abs(v)*(w1 if dist==1 else w2))
    require(all(mat[j].get(i,0)==v for i,row in enumerate(mat)
                for j,v in row.items()),"symmetric_majorant")
    w=[1]*324
    for unused in range(12):
        u=[sum(a*w[j] for j,a in row.items()) for row in mat]
        w=next_weight(u)
    u=[sum(a*w[j] for j,a in row.items()) for row in mat]
    # 1/105 - 1/220 = 23/4620.
    return all(4620*x<=23*den*y for x,y in zip(u,w))


def emit(s):
    print("YM4_VOL14D2|"+s+"|json=0")


def main():
    T,K=build()
    tb=gram_bounds(fold(T),D)
    kb=gram_bounds(fold(K),D)
    require(tb[:3]==[22,13,13] and tb[-1]==13,"T_norm")
    require(kb[:3]==[76,59,57] and kb[-1]==57,"K_norm")
    H=hessian(K)
    emit("T_norm_sq_le=13|H_norm_le=57|offsets=33|range_l1=2|H_integer_entries=525780")
    require(conjugation(H,65,64),"weighted_accretivity")
    require(not conjugation(H,33,32),"oversized_weight_rejected_by_this_test")
    emit("H_floor=1/105|weight=65/64|accretive_floor=1/220|larger_weight_test=REJECTED")
    require(220*13*65*65<3000*64*64,"covariance_prefactor")
    require(57*105<79*79,"chebyshev_ratio")
    emit("C_xy_le=3000*(64/65)^r|strip_linf=log(65/64)|chebyshev_ratio_lt=39/40")
    emit("nonflat_background=OPEN|sharp_Bloch_strip=OPEN|physical_mass_gap=OPEN")


if __name__=="__main__":
    main()
