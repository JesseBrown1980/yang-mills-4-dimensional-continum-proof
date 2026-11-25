#!/usr/bin/env python3
"""Exact local reconstruction on the b=3 linearized tree-gauge slice."""
from itertools import product, permutations

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


def emit(s):
    print("YM4_VOL14D1|"+s+"|json=0")


def main():
    rows={}
    columns={}
    rmax=0
    for mu in range(4):
        l=constraint_row(mu)
        root2=tuple(3 if i==mu else 0 for i in range(4))
        require(len(l)==459 and sum(v*v for v in l.values())*729==277*D*D,
                "L_row_norm")
        require(sum(abs(v) for v in l.values())*27==205*D,"L_row_l1")
        require(all(sum(v for (x,i),v in l.items() if i==j)==
                    (3*D if j==mu else 0) for j in range(4)),"constant_field")
        cross={(x,i):v for (x,i),v in l.items() if x[mu]==1 and i==mu}
        require(len(cross)==27 and set(cross.values())=={D//27},"cross_weight")
        total={}
        for (x,i),v in l.items():
            if (x,i) in cross:
                q=crossing_difference(x,mu)
            else:
                q=internal(root2 if x[mu]>=2 else Z,x,i)
            accum(total,q,v)
        tree=set()
        for root in (Z,root2):
            for z in B:
                x=root
                for s in path(z):
                    k,sg=edge(x,s)
                    tree.add(k)
                    x=step(x,s)
        require(len(tree)==160,"two_block_trees")
        for x in B:
            if x[mu]<1:
                q={k:D*v for k,v in internal(Z,x,mu).items()}
                kind="internal"
            else:
                q={k:D*v for k,v in crossing_difference(x,mu).items()}
                accum(q,total,-1)
                kind="cross"
            lhs={}
            for (a,i,j),v in q.items():
                for e,n in (((a,i),1),((step(a,i+1),j),1),
                            ((step(a,j+1),i),-1),((a,j),-1)):
                    inc(lhs,e,n*v)
            inc(lhs,(x,mu),-D)
            if kind=="cross":
                accum(lhs,l,1)
            require(set(lhs)<=tree,"exact_identity_mod_tree_L")
            # Negative control: dropping a crossing reconstruction coefficient
            # must be rejected for the central crossing row.
            if kind=="cross" and x==step(Z,mu+1):
                mutant=dict(lhs)
                inc(mutant,(x,mu),D)
                require(not set(mutant)<=tree,"missing_crossing_rejected")
            rows[x,mu]=q
            rmax=max(rmax,sum(abs(v) for v in q.values()))
            for (a,i,j),v in q.items():
                inc(columns,(fold(a),i,j),abs(v))
    require(len(rows)==324 and sum(not q for q in rows.values())==80,
            "tree_zero_rows")
    require(sum(x[mu]<1 for x,mu in rows)==216,"internal_count")
    require(sum(x[mu]==1 for x,mu in rows)==108,"cross_count")
    require(81*rmax==1138*D and max(columns.values())==37*D,"Schur_norm")
    emit("b=3|L_row_nnz=459|L_row_norm_sq=277/729|crossing_count=27|crossing_weight=1/27")
    emit("rows=324|tree_zero_rows=80|internal=216|crossing=108|identity_mod_tree_L=PASS")
    emit("S_row_max=1138/81|S_col_max=37|unweighted_norm_sq_le=42106/81")
    # Fold absolute convolution coefficients into a finite nonnegative matrix.
    mat=[]
    for q in rows.values():
        folded={}
        for (a,i,j),v in q.items():
            inc(folded,(fold(a),i,j),abs(v))
        mat.append(folded)
    cols=set(columns)
    w={k:1 for k in cols}
    bounds=[]
    for unused in range(8):
        mw=[sum(v*w[k] for k,v in a.items()) for a in mat]
        ww={k:0 for k in cols}
        for a,t in zip(mat,mw):
            for k,v in a.items():
                ww[k]+=v*t
        n=max((ww[k]+D*D*w[k]-1)//(D*D*w[k]) for k in cols)
        require(all(ww[k]<=n*D*D*w[k] for k in cols),"positive_weight_bound")
        bounds.append(n)
        top=max(ww.values())
        w={k:max(1,(v*1048576+top-1)//top) for k,v in ww.items()}
    require(bounds==[291,118,109,107,106,105,105,105],"weighted_bound")
    emit("weighted_norm_sq_ceiling_sequence="+",".join(str(v) for v in bounds))
    require(8*277<4*729,"L_operator_norm")
    require(16*(1+27*4)<2048,"H_upper")
    require(2048*105*1*1<511*511,"Chebyshev_ratio")
    emit("coercivity=1/105|H_norm_le=2048|chebyshev_ratio_lt=255/256")
    emit("nonflat_background=OPEN|sharp_Bloch_strip=OPEN|continuum_mass_gap=OPEN")


if __name__=="__main__":
    main()
