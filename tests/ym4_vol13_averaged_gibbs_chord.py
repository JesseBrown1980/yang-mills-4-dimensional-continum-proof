"""Exact original 4D SU2 coordinate-tree Gibbs averaged rooted-chord certificate.

Integer-only geometry/Q8 controls; continuous Haar/Gibbs bounds are
analytically proved in the companion certificate note, not approximated here.
"""
from itertools import product

ONE=(1,0,0,0)
I=(0,1,0,0)
J=(0,0,1,0)
K=(0,0,0,1)
Q8=(ONE,I,J,K,(-1,0,0,0),(0,-1,0,0),(0,0,-1,0),(0,0,0,-1))

def require(ok,label):
    if not ok:
        raise ValueError(label)

def mul(u,v):
    a,b,c,d=u
    e,f,g,h=v
    return (a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)

def inv(u):
    return (u[0],-u[1],-u[2],-u[3])

def step(x,mu,sgn=1):
    z=list(x)
    z[mu]+=sgn
    return tuple(z)

def cube_links(b):
    for x in product(range(b),repeat=4):
        for mu in range(4):
            if x[mu]+1<b:
                yield (x,mu)

def path_to(x):
    path=[]
    p=(0,0,0,0)
    for mu in range(4):
        for unused in range(x[mu]):
            path.append((p,mu,1))
            p=step(p,mu)
    require(p==x,'canonical_original_path_endpoint')
    return path

def path_product(U,path):
    out=ONE
    for x,mu,sign in path:
        e=(x,mu) if sign==1 else (step(x,mu,-1),mu)
        val=U[e]
        out=mul(out,val if sign==1 else inv(val))
    return out

def plaquette(U,x,mu,nu):
    return mul(mul(mul(U[(x,mu)],U[(step(x,mu),nu)]),
                   inv(U[(step(x,nu),mu)])),inv(U[(x,nu)]))

def field(b):
    U={}
    for x,mu in cube_links(b):
        key=(x[0]+3*x[1]+5*x[2]+7*x[3]+2*mu+x[mu]*mu)%8
        U[(x,mu)]=Q8[key]
    return U

def cycle(U,e):
    x,mu=e
    y=step(x,mu)
    return mul(mul(path_product(U,path_to(x)),U[e]),
               inv(path_product(U,path_to(y))))

def conjugated_reduced(U,e):
    x,mu=e
    prefix=tuple(x[k] if k<=mu else 0 for k in range(4))
    z=prefix
    red=[]
    for nu in range(mu+1,4):
        for unused in range(x[nu]):
            red.append((z,nu,1))
            z=step(z,nu)
    require(z==x,'reduced_strip_first_half')
    red.append((z,mu,1))
    z=step(z,mu)
    for nu in range(3,mu,-1):
        for unused in range(x[nu]):
            red.append((z,nu,-1))
            z=step(z,nu,-1)
    require(z==step(prefix,mu),'reduced_strip_second_half')
    red.append((z,mu,-1))
    require(len(red)==2*sum(x[nu] for nu in range(mu+1,4))+2,
            'exact_reduced_cycle_length')
    h=path_product(U,path_to(prefix))
    return mul(mul(h,path_product(U,red)),inv(h)),red

def verify_strip(U,e):
    x,mu=e
    first=path_to(x)+[(x,mu,1)]
    desired=path_to(step(x,mu))
    dirs=[p[1] for p in first]
    n=sum(x[nu] for nu in range(mu+1,4))
    cursor=len(dirs)-1
    nontrivial=0
    for unused in range(n):
        require(cursor>0 and dirs[cursor]==mu and dirs[cursor-1]>mu,
                'mu_moves_past_later_direction')
        nu=dirs[cursor-1]
        z=[0,0,0,0]
        for d in dirs[:cursor-1]:
            z[d]+=1
        z=tuple(z)
        if plaquette(U,z,mu,nu)!=ONE:
            nontrivial+=1
        dirs[cursor-1],dirs[cursor]=dirs[cursor],dirs[cursor-1]
        cursor-=1
    require(dirs==[v[1] for v in desired],
            'exact_original_coordinate_tree_direction_swaps')
    a,red=conjugated_reduced(U,e)
    require(a==cycle(U,e),'exact_nonabelian_reduced_cycle')
    dist2=sum((a[j]-ONE[j])**2 for j in range(4))
    require(dist2<=4*nontrivial*nontrivial,
            'nonabelian_plaquette_telescope_triangle')
    if n==0:
        require(a==ONE and not nontrivial,'tree_edge_cycle_identity')
    return n

def rectangle_source(U,b):
    for width in range(1,b):
        for height in range(1,b):
            z=(0,0,0,0)
            path=[]
            for mu,sign,count in ((0,1,width),(1,1,height),(0,-1,width),(1,-1,height)):
                for unused in range(count):
                    path.append((z,mu,sign))
                    z=step(z,mu,sign)
            require(z==(0,0,0,0),'source_loop_closed')
            hol=path_product(U,path)
            lhs=sum((hol[k]-ONE[k])**2 for k in range(4))
            area=width*height
            rhs=0
            for x0 in range(width):
                for x1 in range(height):
                    h=plaquette(U,(x0,x1,0,0),0,1)
                    rhs+=sum((h[k]-ONE[k])**2 for k in range(4))
            require(lhs<=area*rhs,'original_nonabelian_Wilson_source_filling_Cauchy')

def geometry(b):
    U=field(b)
    rectangle_source(U,b)
    fill_count=0
    chord_count=0
    for e in cube_links(b):
        n=verify_strip(U,e)
        fill_count+=n
        chord_count+=int(n>0)
    vertices=b**4
    links=4*(b-1)*b**3
    require(chord_count==links-vertices+1,
            'exact_original_four_dimensional_tree_cycle_rank')
    require(fill_count==3*b**3*(b-1)**2,
            'exact_four_dimensional_total_strip_area')

def rational_bounds(k,Sden,Mden):
    # Strict accepted exact ternary-beta fixtures; avoids runtime negative exponents.
    beta={6:531441,9:387420489,12:282429536481}[k]
    R_num=35+18*k
    require(2*R_num*Sden*Sden<3*beta,
            'strict_integer_sqrt_two_R_envelope')
    # E||U-v||^2 <=37/(72beta)+4/2^663.
    pscale=2**663
    require((37*pscale+288*beta)*Mden*Mden<72*beta*pscale,
            'strict_integer_staple_direction_displacement')

def beta_cube_fixture(b,k,Sden,Mden):
    rational_bounds(k,Sden,Mden)
    n=3*(b-1)
    # Expected preferred-field root chord <= 2n*S+2(2n+2)*M.
    den=Sden*Mden
    D_num=2*n*Mden+2*(2*n+2)*Sden
    if b==81 and k==12:
        require(36*D_num<den,'strict_b81_beta12_averaged_chord_lt_1over36')
        pscale=2**663
        # 18*(1/24 + D/2 + 2/2^663)<1 (all exact integers).
        require(18*(den*pscale+12*D_num*pscale+48*den)
                <24*den*pscale,
                'strict_18_neighbor_averaged_one_link_kernel_budget')
    else:
        require(36*D_num>=den,'negative_averaged_geometry_budget')

def main():
    require(mul(I,J)==K and mul(J,I)==inv(K),
            'genuine_noncommuting_SU2_quaternion_fixture')
    for b in (2,3,4):
        geometry(b)
    for b,k,s,m in ((3,6,74,1000),(9,6,74,1000),
                    (27,9,1700,27000),(81,12,40000,700000)):
        beta_cube_fixture(b,k,s,m)
    return (
        'YM4_VOL13_AVERAGE|original_continuous_SU2_periodic_Gibbs=ANALYTIC|vol09_R_beta=IMPORTED|json=0\n'
        'YM4_VOL13_COORD_TREE|internal_box_b2_b3_b4=PASS|nonabelian_Q8_swap=PASS|strip_face_count=sum_later_coordinates|json=0\n'
        'YM4_VOL13_COUNT|chords=3b4minus4b3plus1|total_strip_area=3b3_times_bminus1_squared|json=0\n'
        'YM4_VOL13_WILSON_SOURCE|nonabelian_Q8_rectangles=PASS|loop_deficit_le_A_times_plaquette_deficits=PASS|original_SU2_averaged_W1_le_A2_R=ANALYTIC|json=0\n'
        'YM4_VOL13_GIBBS|actual_link_chord_mean_le=2n_sqrt_2R|preferred_link_chord_mean_le=2n_sqrt_2R_plus_2_times_2nplus2_m|json=0\n'
        'YM4_VOL13_PREF_M|m_squared_le=37_over_72beta_plus_4_over_2power663|even_periodic_L_ge4|beta_ge9power6|json=0\n'
        'YM4_VOL13_RATIONAL|k6_s_lt_1over74_m_lt_1over1000|k9_s_lt_1over1700_m_lt_1over27000|k12_s_lt_1over40000_m_lt_1over700000|json=0\n'
        'YM4_VOL13_BUDGET|b81_beta9power12_expected_chord_lt_1over36=PASS|b27_beta9power9=HOLD|json=0\n'
        'YM4_VOL13_SCOPE|joint_Gibbs_preferred_chord_marginals=BOUNDED|gauge_covariant_multilink_conditional_coupling=OPEN|physical_scaling=OPEN|11_continuum_gates=OPEN|json=0\n'
    )

if __name__=='__main__':
    print(main(),end='')
