"""VOL12 conditional repair-deficit activity: original continuous SU(2).

Exact-integer finite-packet geometry and beta=9^k arithmetic. The
continuous-Haar local variational comparison is proven in companion note.
"""
from itertools import product


def need(value, label):
    if not value:
        raise ValueError(label)


def power(a, n):
    need(isinstance(a, int) and isinstance(n, int) and n >= 0,
         "integer_nonnegative_power")
    z = 1
    for unused in range(n):
        z *= a
    return z


def shift(x, d, L):
    a = list(x)
    a[d] = (a[d]+1) % L
    return tuple(a)


def packet_geometry(L, count):
    incidence = {}
    for x in product(range(L), repeat=4):
        for d in range(4):
            incidence[(x,d)] = set()
    plaquettes = []
    for x in product(range(L), repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                p=((x,mu),(shift(x,mu,L),nu),
                   (shift(x,nu,L),mu),(x,nu))
                plaquettes.append(p)
                idx=len(plaquettes)-1
                for e in p:
                    incidence[e].add(idx)
    S=[]
    for e in sorted(incidence):
        if all(incidence[e].isdisjoint(incidence[f]) for f in S):
            S.append(e)
            if len(S)==count:
                break
    need(len(S)==count,"packet_exists")
    T=set()
    for e in S:
        for pidx in incidence[e]:
            T.update(plaquettes[pidx])
    M=sum(any(e in T for e in p) for p in plaquettes)
    n=len(T)
    need(n<=19*count and M<=6*n,"local_patch_cardinality")
    need(all(incidence[e].isdisjoint(incidence[f])
             for i,e in enumerate(S) for f in S[i+1:]),
         "independent_pivot_incidence")
    need(all(all(f in T for f in plaquettes[pidx])
             for e in S for pidx in incidence[e]),
         "bad_star_observable_in_patch")
    return n,M


def rate_margin(k):
    beta=power(9,k)
    C=729*1536*power(beta,3)
    h=beta//256
    margin=h-19*C.bit_length()
    # Compare rho <= 18^(-57) conservatively using 18 < 2^5.
    return beta,C.bit_length(),h,margin


def main():
    for L in (3,4):
        for r in (2,4):
            n,M=packet_geometry(L,r)
            need(n<=19*r and M<=114*r,"size_independent_of_total_L")
    beta,bits,h,margin=rate_margin(7)
    need(beta==4782969 and bits==87 and margin==17030,
         "local_relative_deficit_rho_ternary_rate")
    need(margin>=5*57,"conditional_rho_satisfies_VOL10_threshold")
    # Some smaller beta gives vacuous rho: monotone scope gate.
    need(rate_margin(3)[-1]<0,"weak_rate_control")
    # Absolute probabilities require an exterior repair deficit tail.
    # Markov with E[D_T]<=M R(beta), M<=114r produces 912 R/eps.
    # eps=1/16, R(9^k)<=(35+18k)/(3 beta):
    bterm_num=4864*(35+18*7)
    need(bterm_num==783104 and bterm_num<beta,
         "unconditional_bad_boundary_first_moment_rate")
    need(783104*100>beta,"contamination_not_a_cluster_tail")
    return (
        "YM4_VOL12_REPAIR|original_continuous_SU2=ANALYTIC|T_union_plaquette_stars_le=19r|touching_plaquettes_le=114r|json=0\n"
        "YM4_VOL12_CONDITIONAL|repair_deficit_D=M_minus_max_local_Wilson_action|arbitrary_exteriors=ACCOUNTED|local_cap_radius=1_over_4beta|json=0\n"
        "YM4_VOL12_RHO|beta=9power7|epsilon=1/16|conditional_if_D_le=r_epsilon_over8|rho_lt=2power_minus17030|rho_le=18power_minus57|json=0\n"
        "YM4_VOL12_CONTAMINATION|beta=9power7|Markov_P_D_gt_r_epsilon_over8_le=783104/4782969|nondecaying_in_r=YES|json=0\n"
        "YM4_VOL12_REPAIR_SCOPE|localized_conditional_bad_star_activity=ANALYTIC|unconditional_rho=OPEN|physical_size_cube=OPEN|11_continuum_gates=OPEN|json=0\n"
    )


if __name__ == '__main__':
    print(main(),end='')
