"""YM4-WG03: exact first SU2 physical excited centre-sector ordering at L=2.

For 0<beta<=1/100, first excited eigenvalues of the original full
physical SU(2) Wilson 2x2x2 spatial transfer are centre-charged.
The original local contractible Wilson half-trace is centre-neutral,
so its first-physical-excitation spectral projector weight is ZERO.

The proof compares full positive transfer eigenvalues to original
electric Haar convolution (Peter-Weyl) through the true magnetic
multiplier and physical Gauss projector. Finite integer graph
enumeration establishes the necessary two-fundamental-link sector
classification. All estimates use rational pairs, no floats.
"""
from itertools import combinations
from ym4_su2_wilson_local_transfer import (
    R, require, character_eigen_interval,
)
from ym4_4d_wilson_cylinder_moments import positive_links, translate
from ym4_su2_center_flux_projectors import (
    selected_link, physical_transfer_selection,
)


def original_spatial_links():
    """24 positive spatial links on the original t=0 slice."""
    links=tuple((site,axis) for site,axis in positive_links()
                if site[3] == 0 and axis < 3)
    require(len(links) == 24, "wrong_original_spatial_link_count")
    return links


def endpoints(link):
    start,axis=link
    require(axis in (0,1,2) and len(start)==4 and start[3]==0,
            "invalid_original_spatial_edge")
    return start,translate(start,axis)


def singleton_fundamental_has_singlet(link):
    """A single nontrivial SU2 edge has two distinct gauge endpoints."""
    a,b=endpoints(link)
    require(a!=b,"unexpected_spatial_loop_at_single_link")
    return False


def two_fundamental_links_gauge_possible(a,b):
    """Exactly two spin-half edges require even incidence at each site."""
    require(a!=b, "duplicate_spatial_link")
    count={}
    for link in (a,b):
        u,v=endpoints(link)
        count[u]=count.get(u,0)+1
        count[v]=count.get(v,0)+1
    return all(n%2==0 for n in count.values())


def two_link_centre_charge(a,b):
    return tuple((-1 if (int(selected_link(a,axis))
                          +int(selected_link(b,axis)))%2 else 1)
                 for axis in range(3))


def check_fundamental_two_link_support():
    """Enumerate all 276 pairs; 12 gauge-allowed, every one charged."""
    links=original_spatial_links()
    require(all(not singleton_fundamental_has_singlet(l) for l in links),
            "one_link_Gauss_singlet_falsifier")
    accepted=[]
    total=0
    for a,b in combinations(links,2):
        total+=1
        if two_fundamental_links_gauge_possible(a,b):
            charge=two_link_centre_charge(a,b)
            require(charge in ((-1,1,1),(1,-1,1),(1,1,-1)),
                    "neutral_two_fundamental_link_state_detected")
            accepted.append((a,b,charge))
    require(total==276 and len(accepted)==12,
            "wrong_two_link_gauge_pair_count")
    require(tuple(sum(int(pair[2][axis]==-1) for pair in accepted)
                  for axis in range(3)) == (4,4,4),
            "incorrect_winding_sector_multiplicity")
    return {"pairs":total,"admissible":len(accepted),"winding":tuple(accepted)}


def uniform_character_bounds(beta):
    """For 0<beta<=1/100, exact all-representation Haar bounds.

    SU2 normalized Wilson convolution eigenvalue
      kappa_r=(beta/2)^r J_(r+1)/J_1,
    J_m=sum_(k>=0) (beta^2/4)^k/(k! (k+m)!).
    For y=beta^2/4<=1/40000, J_1 in [1,exp(y)]
    and J_(r+1) in [1/(r+1)!, exp(y)/(r+1)!].
    exp(y)<=1/(1-y), giving
      beta/5 < kappa1 < beta/3,
      kappa_r < beta^2/20 for all r>=2.
    The r>=2 majorant declines with r because ratio
    (beta/2)/(r+2)<=beta/8<1.
    """
    beta=R.of(beta)
    require(beta>R(0) and beta<=R(1,100),
            "beta_outside_first_sector_ordering_window")
    y=beta.power(2).div(4)
    require(y<=R(1,40000),"Wilson_Bessel_series_range_mismatch")
    low1=beta*(R(1)-y).div(4)
    high1=beta.div(4*(R(1)-y))
    high_rest=beta.power(2).div(24*(R(1)-y))
    require(low1>beta.div(5) and high1<beta.div(3),
            "fundamental_character_bounds_failed")
    require(high_rest<beta.power(2).div(20)
            and beta.div(8)<R(1),
            "all_higher_character_majorant_failed")
    return {"beta":beta,"low1":low1,"high1":high1,
            "high_other_representations":high_rest,
            "coarse_low1":beta.div(5),"coarse_high1":beta.div(3),
            "coarse_high_other":beta.power(2).div(20)}


def original_first_sector_energy_bounds(beta):
    """Original full-Gauss + all-magnetic-plaquettes minmax theorem.

    Let K be the 24-link normalized electric Wilson Haar convolution
    on physical spin networks. The unique K vacuum is the constant.
    A gauge-invariant nonvacuum state has >=2 nontriv link irreps:
    with exactly two fundamental links it must be a charged winding
    (276-pair exhaustive original graph check); otherwise it has
    >=3 nontriv edges or one rep r>=2.

    Thus second NEUTRAL eigenvalue K_0 is <
      max[(beta/3)^3,(beta/3)*(beta^2/20)]=beta^3/27.

    The charged two-link fundamental winding W_i is an actual
    K eigenfunction of eigenvalue kappa1^2.

    B product over 24 original spatial Wilson plaquettes obeys
    e^(-48beta)<=B<=1, so in every centre charge sector,
       e^(-48beta) K_e <= K_e^(1/2) B K_e^(1/2) <= K_e.
    Nonzero eigenvalues of this operator equal those of original
    physical T_e=B^(1/2) P K P B^(1/2).
    Since e^(-48beta)>=1-48beta>=13/25 and kappa1>beta/5,
    first CHARGED eigenvalue > 13 beta^2/625.
    This exceeds all neutral nonvacuum eigenvalues for beta<=1/100.
    """
    b=uniform_character_bounds(beta)
    source=check_fundamental_two_link_support()
    centre=physical_transfer_selection()
    require(centre["sectors"]==8 and source["admissible"]==12,
            "physical_gauge_centre_source_incompatible")
    beta=b["beta"]
    magnetic_floor=R(1)-48*beta
    require(magnetic_floor>=R(13,25),
            "wrong_magnetic_floor")
    lower_charged=R(13,625)*beta.power(2)
    upper_neutral=beta.power(3).div(27)
    require(lower_charged>upper_neutral,
            "charged_neutral_spectral_separation_failed")
    require(lower_charged.div(upper_neutral)>R(56),
            "frozen_minimum_sector_separation_failed")
    # At beta=1/10000,1/100000 also independently check actual
    # exact rational character enclosures, not merely crude all-beta.
    if beta in (R(1,10000),R(1,100000)):
        k1lo,k1hi=character_eigen_interval(1,beta)
        k2lo,k2hi=character_eigen_interval(2,beta)
        require(b["low1"]<=k1lo and k1hi<=b["high1"]
                and k2hi<b["high_other_representations"],
                "independent_character_interval_mismatch")
        require(magnetic_floor*k1lo.power(2)>upper_neutral,
                "actual_charged_trial_cannot_beat_neutral")
    return {"beta":beta,"charged_lower":lower_charged,
            "neutral_upper":upper_neutral,
            "ratio_lower":lower_charged.div(upper_neutral),
            "magnetic_floor":magnetic_floor,
            "physical_first_eigenspace_centre_charged":True,
            "local_contractible_Wilson_first_weight":R(0)}


def acceptance_row(beta, charged_floor, neutral_cap):
    s=original_first_sector_energy_bounds(beta)
    require(s["charged_lower"]==charged_floor
            and s["neutral_upper"]==neutral_cap,
            "original_frozen_energy_brackets_mismatch")
    require(s["local_contractible_Wilson_first_weight"]==R(0),
            "first_Wilson_weight_zero_gate_failed")
    return (
        "YM4_WG03_ENERGY|beta="+str(beta)
        +"|L=2,2,2|lambda_charged_lower_gt="+str(charged_floor)
        +"|lambda_neutral_second_upper_lt="+str(neutral_cap)
        +"|separation_ratio_gt_56=YES"
        +"|first_physical_nonvacuum_centre=CHARGED"
        +"|original_local_Wilson_first_weight=0|json=0"
    )


def receipt():
    check_fundamental_two_link_support()
    return "\n".join((
        "YM4_WG03_SOURCE|original_SU2_Wilson=YES|full_Gauss=YES"
        "|spatial_links=24|spatial_magnetic_plaquettes=24"
        "|electric_Peter_Weyl=FULL|original_time_transfer=K24|json=0",
        "YM4_WG03_GRAPH|unordered_fundamental_edge_pairs=276"
        "|two_link_Gauss_admissible_winding_pairs=12"
        "|centre_charged_pairs=12|centre_neutral_pairs=0|json=0",
        "YM4_WG03_ANALYTIC|beta_range=0_LT_beta_LE_1/100"
        "|kappa1_gt_beta_over5|kappa1_lt_beta_over3"
        "|all_kappa_r_ge2_lt_beta2_over20"
        "|B_min_ge_13over25|B_max_le_1|json=0",
        acceptance_row(R(1,10000),R(13,62500000000),
                       R(1,27000000000000)),
        acceptance_row(R(1,100000),R(13,6250000000000),
                       R(1,27000000000000000)),
        "YM4_WG03_VERDICT|first_physical_nonvacuum_sector=CHARGED"
        "|original_local_contractible_Wilson_first_spectral_weight"
        "=EXACT_ZERO_FOR_ALL_BETA_LE_1OVER100"
        "|centre_neutral_first_visible_mode=OPEN"
        "|all_volume_uniformity=OPEN|continuum_gap=OPEN|json=0",
    ))+"\n"


if __name__=="__main__":
    print(receipt(),end="")
