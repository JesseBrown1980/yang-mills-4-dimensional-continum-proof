"""YM4-WG08: exact SU2 first-six fully symmetric rank-one Wilson eigenmode.

The original full continuous-SU2 Wilson theory on spatial 2x2x2 is
invariant under the 48 spatial translations/coordinate permutations
G=(Z2)^3 semidirect S3. WG06's six K4,2 positive-slope blocks form
one transitive permutation orbit under G, so its fully G-invariant
electric positive-slope subspace has exact rank one.

WG07's actual full physical interacting six-eigenspace projector
commutes with G and differs from that electric six-slope projector by
<23250 beta in operator norm for beta<=1/1000000. Orthogonal
projection ranks are stable below distance one: the G-invariant
component of the *actual interacting* rank-six band is therefore
exactly one-dimensional and an exact physical transfer eigenvector.

The original true-vacuum centered local Wilson plaquette has strictly
positive squared overlap >1/289 with this identified rank-one mode.
Relative energy ordering of this symmetric mode among neutral levels
2 through 7 is still OPEN, as is the continuum gap.
"""
from itertools import permutations, product
from ym4_su2_wilson_local_transfer import R, require
from ym4_su2_wilson_first_magnetic_42gram import (
    loops_and_masks, exact_graph_spectral_certificate,
)
from ym4_su2_neutral_42_band import spatial_link_lookup
from ym4_su2_first_centre_energy_order import original_spatial_links
from ym4_su2_wilson_six_feshbach import (
    original_interacting_six_Wilson_weight,
)


SYMMETRY_BETA_MAX=R(1,1000000)


def exact_original_spatial_symmetries():
    """Original spatial affine 48-element symmetry G=(Z2)^3 : S3.

    Each spatial link (site,axis) has site time coordinate zero.
    A spatial site transforms as new[i]=old[perm[i]] XOR shift[i],
    while positive old axis d becomes new axis perm.index(d).
    The original SU2 gauge field is transported by relabeling
    these positive links; all original Wilson trace loops map to
    equal traces (plaquette orientation reversal uses Tr U^-1=Tr U).
    """
    group=tuple((shift,perm)
                for shift in product((0,1),repeat=3)
                for perm in permutations((0,1,2)))
    require(len(group)==48 and len(set(group))==48,
            "wrong_original_spatial_affine_group")
    return group


def spatial_link_image(link, symmetry):
    site,axis=link
    shift,perm=symmetry
    require(site[3]==0 and axis in (0,1,2),
            "invalid_original_spatial_link")
    newsite=tuple(site[perm[i]]^shift[i] for i in range(3))+(0,)
    newaxis=perm.index(axis)
    return newsite,newaxis


def transformed_mask(mask, symmetry, links, lookup):
    result=0
    for i,link in enumerate(links):
        if mask&(1<<i):
            mapped=spatial_link_image(link,symmetry)
            require(mapped in lookup,"spatial_symmetry_lost_original_link")
            result|=1<<lookup[mapped]
    require(result.bit_count()==mask.bit_count(),
            "original_spatial_symmetry_not_link_bijection")
    return result


def exact_42_space_spatial_action():
    """Return 48 exact permutation actions on all 42 Haar spin networks."""
    basis=loops_and_masks()
    lookup=spatial_link_lookup()
    links=original_spatial_links()
    mask_to_index={entry[2]:i for i,entry in enumerate(basis)}
    require(len(mask_to_index)==42 and len(links)==24,
            "original_SU2_42basis_not_complete")
    group=exact_original_spatial_symmetries()
    actions=[]
    for symmetry in group:
        idx=[]
        for _,words,mask in basis:
            mapped=transformed_mask(mask,symmetry,links,lookup)
            require(mapped in mask_to_index,
                    "spatial_symmetry_not_closed_on_42basis")
            idx.append(mask_to_index[mapped])
        require(len(set(idx))==42,
                "original_SU2_group_not_unitary_permutation")
        actions.append(tuple(idx))
    require(len(set(actions))==48,
            "spatial_symmetry_group_action_not_faithful")
    return tuple(actions)


def original_symmetric_six_electric_source():
    """Exact 48-group average on WG06 first positive magnetic eigenspace.

    The six K4,2 components form a *transitive* orbit under G.
    Each positive Perron eigenvector is uniquely chosen with all
    positive coefficients. The symmetry permutations transport it
    with positive sign, so the invariant subspace of the six
    positive-slope eigenvectors has dimension one.

    Original W=phi0/2 has a 24-plaquette orbit, each image appearing
    twice in the 48-element group. Thus
       P_G W=(1/48) sum_{p=0}^{23} phi_p.
    The exact top-positive-slope projector is
       Pplus=(A^2+sqrt8 A)/16, A=8M, A^3=8A.
    The averaged source has only plaquette entries, so
    <P_G W, A P_G W>=0, and its positive-slope weight is
       <P_G W,A^2 P_G W>/16 =1/192.
    """
    graph=exact_graph_spectral_certificate()
    A=graph["A"]
    actions=exact_42_space_spatial_action()
    require(len(actions)==48,
            "wrong_true_spatial_symmetry_group_size")
    require(all(A[i][j]==A[g[i]][g[j]]
                for g in actions for i in range(42) for j in range(42)),
            "SU2_magnetic_42Gram_breaks_spatial_symmetry")
    source_orbit=[g[0] for g in actions]
    require(set(source_orbit)==set(range(24)),
            "original_local_Wilson_plaquette_orbit_incomplete")
    counts=[source_orbit.count(i) for i in range(42)]
    require(counts[:24]==[2]*24 and counts[24:]==[0]*18,
            "wrong_original_Wilson_symmetry_averaging")
    components=graph["components"]
    six=[c for c in components if len(c)==6]
    require(len(six)==6,"original_WG06_six_components_missing")
    by_index={i:block for block,comp in enumerate(six)
              for i in comp}
    require(len(by_index)==36,"wrong_six_magnetic_blocks")
    block_orbit={by_index[g[0]] for g in actions}
    require(len(block_orbit)==6,
            "SU2_six_component_group_orbit_not_transitive")
    require(all(sorted(len([g for g in actions
                            if by_index[g[0]]==b]) for b in range(6))
                ==[8]*6 for _ in (0,)),
            "SU2_six_positive_modes_not_permutation_orbit")
    A2=tuple(tuple(sum(A[i][k]*A[k][j] for k in range(42))
                   for j in range(42)) for i in range(42))
    numerator=sum(counts[i]*A2[i][j]*counts[j]
                  for i in range(42) for j in range(42))
    require(numerator==768 and numerator//4==192,
            "symmetric_original_SU2_A2_source_numerator")
    require(all(A[i][j]==0 for i in range(24) for j in range(24)),
            "plaquette_to_plaquette_first_order_symmetry_negative")
    weight=R(numerator,16*(2*len(actions))**2)
    require(weight==R(1,192),
            "fully_symmetric_SU2_slope_source_weight_mismatch")
    return {"actions":actions,"components":six,
            "source_orbit_count":24,"source_group_image_multiplicity":2,
            "positive_slope_symmetric_rank":1,
            "positive_slope_symmetric_weight":weight,
            "A2_source_numerator":numerator}


def actual_full_physical_symmetric_eigenmode(beta):
    """One genuine G-invariant physical eigenvector among neutral levels 2-7.

    Full interacting WG07 physical P6(beta) commutes with all original
    spatial translations/axis permutations because B,K,Gauss do.
    Original electric Pplus also commutes with G. Their operator
    norm distance is <=23250beta <1. The corresponding G-invariant
    orthogonal projections therefore have equal rank. Electric
    invariant Pplus has rank one by the transitive orbit above,
    so the actual interacting physical P6 contains a rank-ONE
    invariant subspace. T acts on it as one scalar: a genuine
    symmetry-resolved original SU2 physical eigenvector.

    W's electric symmetric slope weight is exactly 1/192, hence
       ||P_G Pplus W||=sqrt(1/192)>1/14.
    WG07 physical projector distance <=23250beta,
    WG05 correct centered source ||u-W||<=148beta, ||W||=1/2:
       ||P_G P6 u|| >1/14-11773beta>1/17
    for 0<beta<=1/1000000.
    Actual single-eigenvector source weight >1/289.
    """
    beta=R.of(beta)
    require(R(0)<beta<=SYMMETRY_BETA_MAX,
            "beta_outside_symmetric_rankone_source_window")
    s=original_symmetric_six_electric_source()
    parent=original_interacting_six_Wilson_weight(beta)
    require(parent["rank"]==6 and parent["weight_lower"]==R(9,400),
            "actual_Su2_six_physical_projector_not_authenticated")
    require(parent["projector_distance_upper"]==23250*beta
            and parent["source_distance_upper"]==148*beta,
            "true_full_physical_Wilson_source_angle_not_pinned")
    require(s["positive_slope_symmetric_rank"]==1
            and s["positive_slope_symmetric_weight"]==R(1,192),
            "electric_spatial_invariant_rankone_source_failed")
    require(R(1,192)>R(1,196),
            "positive_original_SU2_symmetry_source_norm")
    require(23250*beta<R(1),
            "symmetric_rankone_projection_not_stable")
    normlower=R(1,14)-parent["projector_distance_upper"].div(2)
    normlower-=parent["source_distance_upper"]
    require(normlower==R(1,14)-11773*beta
            and normlower>R(1,17),
            "original_physical_symmetric_rankone_Wilson_HOLD")
    return {"beta":beta,"physical_symmetric_eigenmode_rank":1,
            "physical_neutral_band_rank":6,
            "individual_symmetric_mode_Wilson_weight_lower":R(1,289),
            "norm_lower":normlower,
            "energy_position_among_neutral_2_to_7":"OPEN",
            "individual_first_neutral_eigenvalue_weight":"OPEN"}


def receipt():
    s=original_symmetric_six_electric_source()
    require(s["positive_slope_symmetric_weight"]==R(1,192),
            "original_SU2_symmetric_source_fixture_failed")
    rows=[
        "YM4_WG08_SOURCE|original_continuous_SU2=YES"
        "|full_4D_Wilson_physical_Gauss=YES|spatial_L=2"
        "|24_magnetic_plaquettes=YES|full_Peter_Weyl=YES|json=0",
        "YM4_WG08_GROUP|translations=8|axis_permutations=6"
        "|original_spatial_group_order=48|42_network_action=PERMUTED"
        "|magnetic_A_invariant=EXACT|json=0",
        "YM4_WG08_ELECTRIC|six_K4_2_positive_slope_blocks=TRANSITIVE"
        "|fully_spatial_symmetric_slope_rank=1"
        "|original_local_Wilson_orbit_24_each_count2=YES"
        "|A2_group_source_numerator=768"
        "|symmetric_first_slope_weight=1/192|json=0",
        "YM4_WG08_PHYSICAL|WG07_full_interacting_six_cluster=PASS"
        "|commuting_spatial_symmetry_projector=YES"
        "|physical_six_symmetric_invariant_rank=1"
        "|one_actual_SU2_physical_neutral_eigenvector=ISOLATED_BY_SYMMETRY"
        "|json=0",
    ]
    for den in (1000000,10000000):
        beta=R(1,den)
        v=actual_full_physical_symmetric_eigenmode(beta)
        require(v["physical_symmetric_eigenmode_rank"]==1
                and v["individual_symmetric_mode_Wilson_weight_lower"]==
                R(1,289),"actual_symmetric_source_cert_not_reproduced")
        rows.append(
            "YM4_WG08_WILSON|beta="+str(beta)
            +"|true_original_interacting_vacuum_centered=YES"
            +"|single_symmetric_physical_eigenvector_weight_gt=1/289"
            +"|energy_order_within_six=OPEN|json=0")
    rows.append(
        "YM4_WG08_VERDICT|original_SU2_first_six_neutral_symmetry_rank1=PASS"
        "|first_identified_single_neutral_eigenvector_Wilson_weight"
        "=CERTIFIED_POSITIVE"
        "|individual_first_neutral_energy_order=OPEN"
        "|full_second_order_six_split=OPEN"
        "|large_volume_weak_coupling_continuum_gap=OPEN|json=0")
    return "\n".join(rows)+"\n"


if __name__=="__main__":
    print(receipt(),end="")
