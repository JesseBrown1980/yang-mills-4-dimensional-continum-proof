#!/usr/bin/env python3
"""Integer suffix transport geometry and rational lift constants."""
from itertools import product, permutations
from collections import Counter


def check(ok, why):
    if not ok:
        raise ValueError(why)


def walk(w, target):
    x=[0]*4
    for j,s in w:
        x[j]+=s
        check(all(-1<=a<=1 for a in x),"suffix_inside_block")
    check(tuple(x)==target,"suffix_endpoint")


def main():
    hist=Counter()
    for mu in range(4):
        order={j:i for i,j in enumerate([j for j in range(4) if j!=mu]+[mu])}
        for z in product((-1,0,1),repeat=4):
            c=tuple((j,v) for j,v in enumerate(z) if v)
            t=tuple(-1 if j==mu else v for j,v in enumerate(z))
            for p in set(permutations(c)):
                w=list(p)+[(mu,-1)]*(z[mu]+1)
                walk(w,t)
                swaps=0
                for j in range(1,len(w)):
                    k=j
                    while k and order[w[k-1][0]]>order[w[k][0]]:
                        w[k-1],w[k]=w[k],w[k-1]
                        swaps+=1
                        walk(w,t)
                        k-=1
                reduced=[]
                for a in w:
                    if reduced and reduced[-1]==(a[0],-a[1]):
                        reduced.pop()
                    else:
                        reduced.append(a)
                ref=[(j,t[j]) for j in sorted(range(4),key=lambda j:order[j]) if t[j]]
                check(reduced==ref,"reference_path")
                walk(reduced,t)
                hist[swaps]+=1
    check([hist[i] for i in range(7)]==[324,544,576,512,320,192,64],"hist")
    check(sum(hist.values())==2532 and max(hist)==6,"max_swap")
    # (12/30)*(8/7)=16/35; 1-16/35=19/35.
    check(12*8*35==16*30*7 and 35-16==19,"lift")
    check(105*23*44==23*4620,"identity_cost")
    print("YM4_VOL14D3A|suffix_cases=2532|max_swaps=6|hist=324,544,576,512,320,192,64|json=0")
    print("YM4_VOL14D3A|delta=1/30|norm_floor=7/8|LR_error_le=16/35|sigma_min_ge=19/35|inverse_norm_le=35/19|json=0")
    print("YM4_VOL14D3A|identity_weight_relative_cost_le=23/44|nonflat_Hessian=OPEN|multiplier=OPEN|json=0")


if __name__=="__main__":
    main()
