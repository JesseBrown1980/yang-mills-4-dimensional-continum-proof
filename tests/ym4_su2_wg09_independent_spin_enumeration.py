"""WG09 clean-room exact low-spin SU2 Gauss singlet enumeration.

Independently enumerates physical spin labels of sum r_e<=5,
with r_e twice the SU2 spin and exact SU2 vertex fusion
(sum r even, maximum r <= sum of other incident r).
The original 2x2x2 periodic spatial cubic lattice is bipartite.
No original WG04/GW09 basis or producer code is imported.
"""
from itertools import combinations, product
from collections import Counter


SITES=tuple(product((0,1),repeat=3))
LINKS=tuple((site,axis) for site in SITES for axis in range(3))


def shifted(site,axis):
    return tuple(site[d] ^ int(d==axis) for d in range(3))


def compositions(total,parts):
    if parts==1:
        yield (total,)
    else:
        for first in range(1,total-parts+2):
            for tail in compositions(total-first,parts-1):
                yield (first,)+tail


def local_singlet(spins):
    return sum(spins)%2==0 and 2*max(spins,default=0)<=sum(spins)


def gauge_invariant(assignment):
    at={site:[] for site in SITES}
    for i,r in assignment.items():
        site,axis=LINKS[i]
        at[site].append(r)
        at[shifted(site,axis)].append(r)
    return all(local_singlet(v) for v in at.values())


def spatial_charge(assignment):
    return tuple(sum(r for i,r in assignment.items()
                     if LINKS[i][1]==d and LINKS[i][0][d]==0)%2
                 for d in range(3))


def exact_counts():
    out={}
    for total in (2,3,4,5):
        neutral=Counter()
        charged=0
        for occupied in range(1,total+1):
            for edges in combinations(range(24),occupied):
                for values in compositions(total,occupied):
                    assignment=dict(zip(edges,values))
                    if not gauge_invariant(assignment):
                        continue
                    if spatial_charge(assignment)==(0,0,0):
                        neutral[tuple(sorted(values))]+=1
                    else:
                        charged+=1
        out[total]=(dict(neutral),charged)
    assert out[2]==({},12)
    assert out[3]==({},0)
    assert out[4][0]=={(1,1,1,1):42,(2,2):12}
    assert out[4][1]==120
    assert out[5]==({},0)
    return out


def receipt():
    exact_counts()
    return (
        "YM4_WG09_SPIN_ENUM|original_SU2_links=24"
        "|S2_neutral=0|S2_charged=12|S3_neutral=0"
        "|S4_neutral_fundamental=42|S4_neutral_spinone_two_link=12"
        "|S4_charged_assignments=120|S5_neutral=0|json=0\n"
        "YM4_WG09_SPIN_ENUM_VERDICT|neutral_nonvacuum_except_E42_R12"
        "_spin_index_ge6=EXACT|json=0\n"
    )


if __name__=="__main__":
    print(receipt(),end="")
