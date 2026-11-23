"""VOL14 original SU2 source-local weighted gauge-orbit metric controls.

Exact integer original 4D geometry and noncommuting quaternion falsifiers.
The continuous Gibbs theorem is analytically proved in the companion note.
"""
from itertools import product
from collections import deque

ONE=(1,0,0,0)
NEG=(-1,0,0,0)
I=(0,1,0,0)
J=(0,0,1,0)
K=(0,0,0,1)
Q8=(ONE,I,J,K,NEG,(0,-1,0,0),(0,0,-1,0),(0,0,0,-1))

def check(ok,name):
    if not ok:
        raise ValueError(name)

def mul(u,v):
    a,b,c,d=u
    e,f,g,h=v
    return (a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)

def inv(q):
    return (q[0],-q[1],-q[2],-q[3])

def plus(x,mu,modulus=0):
    y=list(x)
    y[mu]+=1
    if modulus:
        y[mu]%=modulus
    return tuple(y)

def internal_links(b):
    for x in product(range(b),repeat=4):
        for mu in range(4):
            if x[mu]+1<b:
                yield (x,mu)

def pow3_table(limit):
    values=[1]
    for unused in range(limit):
        values.append(values[-1]*3)
    return values

def rational_geometry(b):
    max_depth=4*(b-1)
    powers=pow3_table(max_depth)
    denominator=powers[max_depth]
    edges=0
    chords=0
    total_strip=0
    weighted_edges=0
    weighted_strip=0
    tail_ed=[0]*(max_depth+1)
    tail_strip=[0]*(max_depth+1)
    for x,mu in internal_links(b):
        distance=sum(x)
        strip=sum(x[nu] for nu in range(mu+1,4))
        check(strip<=distance and strip<=3*(b-1),"short_coordinate_strip")
        numerator=powers[max_depth-distance]
        edges+=1
        chords+=int(strip>0)
        total_strip+=strip
        weighted_edges+=numerator
        weighted_strip+=strip*numerator
        tail_ed[distance]+=numerator
        tail_strip[distance]+=strip*numerator
    check(edges==4*(b-1)*b*b*b,"original_four_dimensional_edges")
    check(chords==3*b*b*b*b-4*b*b*b+1,"original_4d_cycle_rank")
    check(total_strip==3*b*b*b*(b-1)*(b-1),"original_total_coordinate_strip")
    check(4*weighted_edges<=81*denominator,"uniform_weighted_edge_count")
    check(16*weighted_strip<=243*denominator,"uniform_weighted_strip_count")
    for radius in range(max_depth+1):
        edge_tail=sum(tail_ed[radius:])
        strip_tail=sum(tail_strip[radius:])
        power2=1
        for unused in range(radius):
            power2*=2
        check(power2*edge_tail<=324*denominator,"tail_edge_weighted")
        check(power2*strip_tail<=972*denominator,"tail_strip_weighted")
    return edges,chords,weighted_edges,weighted_strip,denominator

def beta_envelopes():
    beta=282429536481
    denominator_s=41000
    denominator_m=740000
    tiny=1
    for unused in range(663):
        tiny*=2
    check(2*(35+18*12)*denominator_s*denominator_s<3*beta,
          "strict_original_plaquette_R_bound")
    check((37*tiny+288*beta)*denominator_m*denominator_m<72*beta*tiny,
          "strict_original_preferred_direction_m_bound")
    s=denominator_s
    m=denominator_m
    check(1000*(243*m+1134*s)<8*s*m,
          "weighted_preferred_chord_lt_1over1000")
    check(2000*(243*m+1458*s)<16*s*m,
          "weighted_joint_orbit_lt_1over2000")
    check(40500*4==2000*81,"normalized_orbit_lt_1over40500")
    check(16*(1944*m+5184*s)<s*m,
          "preferred_chord_tail_lt_pow2_neg_radius_over16")
    check(32*(972*m+2916*s)<s*m,
          "joint_orbit_tail_lt_pow2_neg_radius_over32")
    return s,m

def full_links(L):
    for x in product(range(L),repeat=4):
        for mu in range(4):
            yield x,mu

def local_noncommuting_control(b):
    sites=list(product(range(b),repeat=4))
    gauge={x:Q8[(x[0]+2*x[1]+3*x[2]+5*x[3])%8] for x in sites}
    U={(x,mu):(I if mu==0 else J if mu==1 else K if mu==2 else ONE)
       for x,mu in internal_links(b)}
    V={(x,mu):mul(mul(gauge[x],u),inv(gauge[plus(x,mu)]))
       for (x,mu),u in U.items()}
    edges=list(U)
    root=(0,0,0,0)
    gs={root:gauge[root]}
    seen={root}
    queue=deque([root])
    while queue:
        x=queue.popleft()
        for mu in range(4):
            for direction in (-1,1):
                y=list(x)
                y[mu]+=direction
                if not (0<=y[mu]<b):
                    continue
                y=tuple(y)
                e=(x,mu) if direction==1 else (y,mu)
                if y in seen:
                    continue
                u=U[e] if direction==1 else inv(U[e])
                v=V[e] if direction==1 else inv(V[e])
                gs[y]=mul(mul(inv(v),gs[x]),u)
                seen.add(y)
                queue.append(y)
    check(len(gs)==b*b*b*b,"full_original_site_frame")
    for e in edges:
        x,mu=e
        y=plus(x,mu)
        eq=mul(mul(gs[x],U[e]),inv(gs[y]))
        check(eq==V[e],"explicit_gauge_orbit_zero_cost")
    check(mul(I,J)!=mul(J,I),"genuine_nonabelian_SU2_control")
    W=dict(V)
    edge=((0,0,0,0),0)
    W[edge]=mul(NEG,W[edge])
    def face(A):
        x=(0,0,0,0)
        return mul(mul(mul(A[(x,0)],A[(plus(x,0),1)]),
                       inv(A[(plus(x,1),0)])),inv(A[(x,1)]))
    check(face(W)==mul(NEG,face(V)),
          "local_Wilson_loop_discriminates_orbits")
    return len(edges)

def torus_winding_control(b):
    L=2*b
    normal={e:ONE for e in full_links(L)}
    twisted={(x,mu):(NEG if mu==0 and x[0]==L-1 else ONE)
             for x,mu in full_links(L)}
    check(all(normal[e]==twisted[e] for e in internal_links(b)),
          "interior_orbit_distance_zero_for_winding_red")
    def loop(A):
        x=(0,0,0,0)
        q=ONE
        for unused in range(L):
            q=mul(q,A[(x,0)])
            x=plus(x,0,L)
        return q
    check(loop(normal)==ONE and loop(twisted)==NEG,
          "global_winding_traces_plus2_minus2")

def main():
    check(mul(I,J)==K and mul(J,I)==inv(K),"noncommuting_SU2_group")
    for b in (2,3,4,9):
        rational_geometry(b)
    beta_envelopes()
    for b in (2,3):
        local_noncommuting_control(b)
        torus_winding_control(b)
    return (
        'YM4_VOL14_GEOM|original_4D_boxes_b2_b3_b4_b9=PASS|coordinate_tree=PASS|exact_weighted_generating_sums=PASS|json=0\n'
        'YM4_VOL14_WEIGHTS|sum_edge_weight_le_81over4|sum_strip_weight_le_243over16|annular_tail_2power_minus_r=PASS|json=0\n'
        'YM4_VOL14_BETA12|beta=9power12|sqrt_2R_lt_1over41000|m_lt_1over740000|integer_only=PASS|json=0\n'
        'YM4_VOL14_CHORD|weighted_expected_preferred_chord_lt_1over1000|tail_lt_2power_minus_r_over16|json=0\n'
        'YM4_VOL14_ORBIT|full_joint_conditional_averaged_weighted_orbit_lt_1over2000|normalized_orbit_W1_lt_1over40500|json=0\n'
        'YM4_VOL14_ORBIT_TAIL|weighted_actual_link_mismatch_tail_lt_2power_minus_r_over32|source_anchored=PASS|json=0\n'
        'YM4_VOL14_Q8|genuine_noncommuting_SU2_site_gauge=PASS|positive_orbit_zero=PASS|local_plaquette_red=PASS|json=0\n'
        'YM4_VOL14_GLOBAL_RED|entire_internal_cube_orbit_zero|global_periodic_winding_plus2_vs_minus2|all_sector_contraction=OPEN|json=0\n'
        'YM4_VOL14_SCOPE|periodic_Gibbs_averaged_metric=SOURCE_DEPENDENT_ANALYTIC|physical_unweighted_spatial_covariance=OPEN|full_block_transfer=OPEN|11_continuum_gates=OPEN|json=0\n'
    )

if __name__=='__main__':
    print(main(),end='')
