"""WG06: exact original continuous SU(2) rank-42 Haar Gram and magnetic slope.

The original physical L=2 SU2 neutral four-fundamental spin-network
basis is built directly from the WG04 24-plaquette and 18 double-winding
support classes. The orthonormal Haar Gram is identity by Peter-Weyl
orthogonality, verified independently by original link supports.

The first variation of the ORIGINAL 24-plaquette magnetic multiplier,
 B(beta)=exp(-24beta)*exp(beta*sum_p W_p),
has E42-compressed matrix M_ij=<phi_i,(sum_p W_p)phi_j>_Haar.
The nonzero entries are exactly 1/8, evaluated by an exact SU2 Haar
quadratic cubature on every link: uniform quaternion Q8 has the same
degree <=2 coordinate moments as normalized Haar S3. No floating point.

This is the electric-band first magnetic derivative, not yet a
Feshbach-isolated *interacting* six-mode spectral projector.
Also derives true interacting original Wilson C2,C4 positive lower
bounds from WG05's >1/5 actual physical rank42 spectral weight.
"""
from itertools import combinations, product
from ym4_su2_wilson_local_transfer import R, require
from ym4_su2_neutral_42_band import (
    canonical_neutral_basis_supports, spatial_link_lookup,
)
from ym4_su2_first_centre_energy_order import original_spatial_links
from ym4_su2_center_flux_projectors import winding_word
from ym4_4d_wilson_cylinder_moments import plaquette_word
from ym4_su2_wilson_42band_positive_weight import (
    original_physical_wilson_42band_weight,
)


def loops_and_masks():
    """Full original 42 physical electric basis, each as trace-loop words."""
    lookup=spatial_link_lookup()
    def mask(word):
        value=0
        for site,axis,sign in word:
            key=(site,axis)
            require(key in lookup,"original_spatial_word_outside_source")
            bit=1<<lookup[key]
            require(not (value&bit),"repeated_link_in_basis_word")
            value|=bit
        return value
    entries=[]
    for x,y,z in product((0,1),repeat=3):
        site=(x,y,z,0)
        for mu,nu in combinations((0,1,2),2):
            word=plaquette_word(site,mu,nu)
            entries.append(("P",(tuple(word),),mask(word)))
    for axis in range(3):
        loops=[]
        other=[d for d in range(3) if d!=axis]
        for transverse in product((0,1),repeat=2):
            coord=[0,0,0,0]
            for d,v in zip(other,transverse):
                coord[d]=v
            word=winding_word(axis,tuple(coord))
            loops.append((tuple(word),mask(word)))
        for left,right in combinations(loops,2):
            a,ma=left
            b,mb=right
            require(ma&mb==0,"winding_loop_pair_shared_link")
            entries.append(("D",(a,b),ma|mb))
    require(len(entries)==42 and len(set(e[2] for e in entries))==42,
            "original_neutral_42_basis_mismatch")
    parent=canonical_neutral_basis_supports()
    require(set(e[2] for e in entries)==set(parent["neutral"]),
            "wrong_original_SU2_42_spin_network_basis")
    return tuple(entries)


def q_mul(x,y):
    """Exact Q8 unit-quaternion multiplication; values (sign,index)."""
    sx,ix=x
    sy,iy=y
    require(sx in (-1,1) and sy in (-1,1)
            and ix in (0,1,2,3) and iy in (0,1,2,3),
            "invalid_exact_quaternion_element")
    if ix==0:
        return (sx*sy,iy)
    if iy==0:
        return (sx*sy,ix)
    if ix==iy:
        return (-sx*sy,0)
    if (ix,iy) in ((1,2),(2,3),(3,1)):
        return (sx*sy,6-ix-iy)
    return (-sx*sy,6-ix-iy)


def q_inverse(x):
    sx,ix=x
    require(sx in (-1,1) and ix in (0,1,2,3),
            "invalid_quaternion_inverse_argument")
    return (sx if ix==0 else -sx,ix)


def q_character(word, values, lookup):
    val=(1,0)
    for site,axis,orientation in word:
        require(orientation in (-1,1),"nonSU2_link_orientation")
        edge=lookup[(site,axis)]
        q=(1,values[edge])
        val=q_mul(val,q if orientation==1 else q_inverse(q))
    return 2*val[0] if val[1]==0 else 0


def exact_Haar_triple(entry_i,entry_j,plaquette_entry):
    """Return <phi_i,W_p phi_j> exactly, with SU2 Haar not Q8 surrogate.

    Each link appears 0 or 2 times in a nonvanishing triple.
    Every SU2 fundamental trace is polynomial of degree <=2 in
    the four real quaternion coordinates per link. Q8's positive
    8-point uniform measure has coordinate mean zero, covariance
    delta_ab/4, exactly equal to normalized Haar on S3.
    Because every edge appears twice, integrand is invariant under
    q_edge -> -q_edge. Average over the four positive coordinate
    basis quaternions suffices and is *exact* for Haar.
    """
    all_loops=entry_i[1]+entry_j[1]+plaquette_entry[1]
    counts={}
    for word in all_loops:
        for s,d,orientation in word:
            key=(s,d)
            counts[key]=counts.get(key,0)+1
    if any(n%2 for n in counts.values()):
        return R(0)
    require(all(n==2 for n in counts.values()) and len(counts)==6,
            "triple_trace_requires_quadratic_edge_cubature")
    links=tuple(sorted(counts))
    lookup={edge:i for i,edge in enumerate(links)}
    total=0
    # Each local coordinate-basis quaternion stands for both its
    # signs, because the degree-two integrand is even per link.
    for values in product(range(4),repeat=6):
        out=1
        for word in all_loops:
            out*=q_character(word,values,lookup)
            if not out:
                break
        total+=out
    # last observable is normalized W_p=chi_p/2.
    return R(total,2*4**6)


def original_first_magnetic_matrix():
    """A=8 * E42(sum_p W_p)E42: exact integer 42x42 adjacency."""
    basis=loops_and_masks()
    plaquettes=basis[:24]
    support_to_plaquette={entry[2]:entry for entry in plaquettes}
    require(len(support_to_plaquette)==24,
            "incorrect_original_spatial_plaquette_enumeration")
    matrix=[[0]*42 for _ in range(42)]
    computed=0
    for i,j in combinations(range(42),2):
        diff=basis[i][2]^basis[j][2]
        if diff not in support_to_plaquette:
            continue
        entry_p=support_to_plaquette[diff]
        coefficient=exact_Haar_triple(basis[i],basis[j],entry_p)
        require(coefficient==R(1,8),
                "unexpected_original_SU2_magnetic_Haar_coefficient")
        matrix[i][j]=matrix[j][i]=8*coefficient.n//coefficient.d
        computed+=1
    require(computed==48,"wrong_original_SU2_magnetic_support_count")
    require(all(matrix[i][i]==0 for i in range(42)),
            "magnetic_first_order_diagonal_should_vanish")
    return tuple(tuple(row) for row in matrix)


def exact_graph_spectral_certificate():
    """Six K4,2 components, six isolates; A^3=8A and source top6."""
    A=original_first_magnetic_matrix()
    degrees=[sum(row) for row in A]
    require(degrees[:24]==[2]*24 and
            degrees[24:].count(4)==12 and
            degrees[24:].count(0)==6,
            "first_magnetic_42_graph_wrong_degrees")
    seen=set()
    components=[]
    for i in range(42):
        if i in seen:
            continue
        q=[i]
        seen.add(i)
        for node in q:
            for j in range(42):
                if A[node][j] and j not in seen:
                    seen.add(j)
                    q.append(j)
        components.append(tuple(q))
    sizes=sorted(len(c) for c in components)
    require(sizes==[1]*6+[6]*6,
            "incorrect_magnetic_first_order_connected_blocks")
    for comp in components:
        if len(comp)==1:
            require(comp[0]>=24,"isolated_plaquette_basis_invalid")
            continue
        p=[k for k in comp if k<24]
        d=[k for k in comp if k>=24]
        require(len(p)==4 and len(d)==2 and
                all(A[x][y]==1 for x in p for y in d) and
                all(A[x][y]==0 for x,y in combinations(p,2)) and
                A[d[0]][d[1]]==0,
                "six_block_not_exact_K4_2")
    # A^2, A^3 checked by integer arithmetic: minimal polynomial
    # x(x^2-8), and 12 nonzero eigenvalues +/-sqrt(8).
    A2=tuple(tuple(sum(A[i][k]*A[k][j] for k in range(42))
                   for j in range(42)) for i in range(42))
    require(sum(A2[i][i] for i in range(42))==96,
            "magnetic_A_squared_trace_mismatch")
    require(all(sum(A2[i][k]*A[k][j] for k in range(42))
                ==8*A[i][j] for i in range(42) for j in range(42)),
            "magnetic_first_order_cubic_minimal_polynomial_failure")
    # Original local plaquette W=phi_0/2 has squared orthogonal
    # first-order *positive-six cluster* weight:
    # +/- spectral projectors share diagonal A2[0][0]/16=1/8
    # from bipartiteness, then W amplitude factor (1/2)^2.
    require(A2[0][0]==2,
            "source_not_degree_two_in_magnetic_42_graph")
    top6_source_weight=R(A2[0][0],64)
    require(top6_source_weight==R(1,32),
            "incorrect_first_order_top6_Wilson_source_weight")
    return {"A":A,"components":tuple(components),
            "edge_count":48,"source_positive6_weight":top6_source_weight,
            "top6_multiplicity":6,"bottom6_multiplicity":6,
            "zero_multiplicity":30}


def true_original_Wilson_moment_lower(beta,even_time):
    """Positive original full-interacting normalized physical Wilson moments.

    WG05: physical true-vacuum Wilson band spectral mass >1/5.
    WG04: each physical *unnormalized* band eigenvalue > beta^4/500.
    Physical vacuum eigenvalue <=1 as B<=I and normalized electric
    transfer K<=I, hence normalized excited t=λ/λ0 > beta^4/500.
    Thus C_n > (1/5)(beta^4/500)^n, for all positive even n.
    """
    require(type(even_time) is int and even_time in (2,4),
            "moment_requires_original_even_time")
    result=original_physical_wilson_42band_weight(beta)
    require(result["weight_lower"]>R(1,5),
            "original_physical_Wilson_weight_not_positive")
    beta=R.of(beta)
    return (beta.power(4).div(500)).power(even_time).div(5)


def receipt():
    g=exact_graph_spectral_certificate()
    require(g["source_positive6_weight"]==R(1,32),
            "frozen_original_magnetic_source_weight_mismatch")
    rows=[
        "YM4_WG06_SOURCE|continuous_SU2=YES|original_4D_Wilson=YES"
        "|original_Gauss=YES|spatial_L=2"
        "|electric_basis_rank=42|24_plaquette_plus_18_double_winding=YES|json=0",
        "YM4_WG06_GRAM|original_Haar_G42=IDENTITY_BY_PETER_WEYL"
        "|magnetic_potential=sum_24_Wp"
        "|exact_each_nonzero_Mij=1/8|offdiagonal_undirected_edges=48|json=0",
        "YM4_WG06_GRAPH|components_K4_2=6|isolated_vertices=6"
        "|plaquette_degree2=24|double_winding_degree4=12"
        "|double_winding_degree0=6|json=0",
        "YM4_WG06_MATRIX|A=8M|trace_A_squared=96|A_cubed=8A"
        "|positive_eigenvalue=sqrt8_multiplicity6"
        "|negative_eigenvalue=minus_sqrt8_multiplicity6"
        "|zero_eigenvalue=multiplicity30|json=0",
        "YM4_WG06_SOURCE_PROJECTION|local_plaquette_W_halftrace=YES"
        "|first_magnetic_order_top6_cluster_weight=1/32"
        "|first_order_top6_degeneracy=6"
        "|true_interacting_top6_projector_weight=OPEN|json=0",
    ]
    for den in (10000,100000):
        beta=R(1,den)
        rows.append(
            "YM4_WG06_TRUE_VACUUM|beta="+str(beta)
            +"|original_Wilson_C2_lower_gt="+str(true_original_Wilson_moment_lower(beta,2))
            +"|original_Wilson_C4_lower_gt="+str(true_original_Wilson_moment_lower(beta,4))
            +"|positive_original_full_interacting_Wilson_moments=YES|json=0"
        )
    rows.append(
        "YM4_WG06_VERDICT|exact_42_Haar_Gram_and_first_magnetic_slope=PASS"
        "|first_magnetic_top6_rank6=PASS"
        "|original_normalized_Wilson_C2_C4_lower=POSITIVE"
        "|true_interacting_top6_Feshbach_projector=OPEN"
        "|first_neutral_eigenvalue_Wilson_weight=OPEN"
        "|continuum_mass_gap=OPEN|json=0"
    )
    return "\n".join(rows)+"\n"


if __name__=="__main__":
    print(receipt(),end="")
