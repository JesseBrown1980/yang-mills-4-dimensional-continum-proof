#!/usr/bin/env python3
"""Exact suffix-transport word counts for the covariant crossing-face lift."""
from itertools import product, permutations

B=tuple(product((-1,0,1),repeat=4))
D=1944


def require(ok, why):
    if not ok:
        raise ValueError(why)


def walk(start, word):
    x=list(start)
    for i,s in word:
        x[i]+=s
        require(all(-1<=v<=1 for v in x),"path_outside_target_block")
    return tuple(x)


def swap(w,i,start):
    require(w[i][0]!=w[i+1][0],"perpendicular_swap")
    w[i],w[i+1]=w[i+1],w[i]
    require(walk(start,w)==(0,0,0,0),"swap_endpoint")


def check(mu):
    total=0
    worst=0
    count=0
    for z in B:
        base=tuple((i,1 if v>0 else -1) for i,v in enumerate(z) if v)
        ps=set(permutations(base))
        require(24%len(ps)==0,"weight")
        weight=24//len(ps)
        start=tuple(-1 if i==mu else v for i,v in enumerate(z))
        target=[(i,1 if v<0 else -1)
                for i,v in reversed(tuple(enumerate(start))) if v]
        for p in ps:
            w=[(mu,1)]*(1+z[mu])+[(i,-s) for i,s in reversed(p)]
            require(walk(start,w)==(0,0,0,0),"suffix_endpoint")
            n=0
            if z[mu]==1:
                j=w.index((mu,-1))
                while j>2:
                    swap(w,j-1,start)
                    j-=1
                    n+=1
                require(w[1:3]==[(mu,1),(mu,-1)],"cancellation")
                del w[1:3]
                require(walk(start,w)==(0,0,0,0),"cancel_endpoint")
            for j in range(1,len(w)):
                k=j
                while k>0 and w[k-1][0]<w[k][0]:
                    swap(w,k-1,start)
                    k-=1
                    n+=1
            require(w==target,"canonical_suffix")
            total+=weight*n
            count+=weight
            worst=max(worst,n)
    require(count==D,"normalized_weights")
    return worst,total


def emit(s):
    print("YM4_VOL14D3A|"+s+"|json=0")


def main():
    expected=((9,5184,8,3),(8,4320,20,9),
              (7,3456,16,9),(6,2592,4,3))
    for mu,(maximum,total,num,den) in enumerate(expected):
        require(check(mu)==(maximum,total),"suffix_counts")
        require(total*den==D*num,"weighted_mean")
        emit("axis="+str(mu)+"|suffix_swaps_max="+str(maximum)
             +"|weighted_mean="+str(num)+"/"+str(den))
    # (2 delta)/(7/8) * (8/3) = 64/315.
    require(2*8*8*315==64*30*7*3,"relative_error")
    require(315-64==251 and 315*3<251*4,"inverse_norm")
    emit("delta=1/30|V_floor=7/8|LR_error_le=64/315|LR_inverse_le=315/251")
    emit("curvature_form=OPEN|constrained_minimizer_hessian=OPEN|background_locality=OPEN")


if __name__=="__main__":
    main()
