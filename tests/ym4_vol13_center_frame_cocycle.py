"""Original 4D periodic SU2 centre frame coherence controls (all exact integers).

Flat centre link-ratio cocycles admit periodic site gauges exactly when
all fundamental winding products are +1. Finite 4D witnesses and BFS.
"""
from collections import deque
from itertools import product


def require(ok, label):
    if not ok:
        raise ValueError(label)


def shift(x, mu, L, step=1):
    a=list(x)
    a[mu]=(a[mu]+step)%L
    return tuple(a)


def site_gauge(L):
    return {x:(-1 if (x[0]+2*x[1]+3*x[2]+5*x[3])%3==0 else 1)
            for x in product(range(L),repeat=4)}


def link_ratio(L, case):
    g=site_gauge(L)
    ratio={}
    for x in product(range(L),repeat=4):
        for mu in range(4):
            if case=='pure':
                r=g[x]*g[shift(x,mu,L)]
            elif case=='winding':
                r=(-1 if mu==0 and x[0]==L-1 else 1)
            else:
                r=(-1 if x==(0,0,0,0) and mu==0 else 1)
            ratio[(x,mu)]=r
    return ratio


def plaquette_fluxes(L,ratio):
    products=[]
    for x in product(range(L),repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                p=(ratio[(x,mu)]*ratio[(shift(x,mu,L),nu)]*
                   ratio[(shift(x,nu,L),mu)]*ratio[(x,nu)])
                products.append(p)
    require(len(products)==6*L*L*L*L,'original_4D_plaquette_count')
    return products


def winding(L,ratio):
    loops=[]
    for mu in range(4):
        x=(0,0,0,0)
        h=1
        for unused in range(L):
            h*=ratio[(x,mu)]
            x=shift(x,mu,L)
        require(x==(0,0,0,0),'closed_periodic_winding_loop')
        loops.append(h)
    return loops


def periodic_gauge_reconstruct(L,ratio):
    root=(0,0,0,0)
    gauges={root:1}
    queue=deque((root,))
    while queue:
        x=queue.popleft()
        for mu in range(4):
            for sign in (-1,1):
                y=shift(x,mu,L,sign)
                edge=(x,mu) if sign==1 else (y,mu)
                desired=gauges[x]*ratio[edge]
                if y not in gauges:
                    gauges[y]=desired
                    queue.append(y)
                elif gauges[y]!=desired:
                    return False,len(gauges)
    require(len(gauges)==L*L*L*L,'all_sites_reached')
    require(all(ratio[(x,mu)]==gauges[x]*gauges[shift(x,mu,L)]
                for x in gauges for mu in range(4)),
            'verified_periodic_site_gauge_witness')
    return True,len(gauges)


def main():
    for L in (4,6):
        pure=link_ratio(L,'pure')
        wind=link_ratio(L,'winding')
        local=link_ratio(L,'local_defect')
        require(all(p==1 for p in plaquette_fluxes(L,pure)),
                'pure_site_gauge_has_flat_link_ratios')
        require(all(x==1 for x in winding(L,pure)),
                'pure_site_gauge_trivial_global_winding')
        require(periodic_gauge_reconstruct(L,pure)==(True,L*L*L*L),
                'positive_explicit_gauge_frame_reconstruction')
        require(all(p==1 for p in plaquette_fluxes(L,wind)),
                'winding_cocycle_is_locally_flat')
        require(winding(L,wind)==[-1,1,1,1],
                'flat_but_globally_nontrivial_cocycle')
        require(periodic_gauge_reconstruct(L,wind)[0] is False,
                'winding_blocks_periodic_frame')
        require(any(p==-1 for p in plaquette_fluxes(L,local)),
                'local_frustration_red_control')
        require(periodic_gauge_reconstruct(L,local)[0] is False,
                'local_flux_blocks_periodic_frame')
    return (
        'YM4_VOL13_CENTER_FRAME|original_4D_SU2_centre=EXACT|L4_L6=PASS|gauge_transform_frame_BFS=PASS|json=0\n'
        'YM4_VOL13_COCYCLE|pure_frame=FLAT_WITH_TRIVIAL_WINDING|periodic_gauge_exists=YES|json=0\n'
        'YM4_VOL13_WINDING|all_plaquette_fluxes=plus1|Polyakov_ratio_direction0=minus1|periodic_gauge_exists=NO|json=0\n'
        'YM4_VOL13_LOCAL_RED|plaquette_flux=minus1_exists|periodic_gauge_exists=NO|json=0\n'
        'YM4_VOL13_SCOPE|centre_subgroup_cocycle=EXACT|full_SU2_nonabelian_frame=OPEN|multi_link_good_region_coupling=OPEN|11_continuum_gates=OPEN|json=0\n'
    )


if __name__=='__main__':
    print(main(),end='')
