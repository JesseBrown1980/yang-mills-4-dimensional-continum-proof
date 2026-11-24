"""YM4 VOL21: exact original 4D SU2 shell-staple support and noise floor.

Strict integer-only combinatorial verifier; continuous Haar Gibbs minorization
and shell conditional-variance inequality are analytic, not finite-Q8 proof.
"""
from itertools import product


def require(ok, name):
    if not ok:
        raise AssertionError(name)


def internal_links(r):
    return {(x, mu) for x in product(range(-r, r+1), repeat=4)
            for mu in range(4) if x[mu] < r}


def face_links(x, mu, nu):
    y = list(x)
    z = list(x)
    y[mu] += 1
    z[nu] += 1
    return ((x, mu), (tuple(y), nu), (tuple(z), mu), (x, nu))


def is_support_link(e, r):
    x, mu = e
    crossing = (x[mu] == -r-1 or x[mu] == r) and all(
        -r <= x[nu] <= r for nu in range(4) if nu != mu)
    if crossing:
        return True
    if -r <= x[mu] < r:
        outer = sum(abs(x[nu]) == r+1 for nu in range(4) if nu != mu)
        interior = all(abs(x[nu]) <= r+1 for nu in range(4) if nu != mu)
        return interior and outer == 1
    return False


def fixture(r):
    b = 2*r+1
    inside = internal_links(r)
    outer = internal_links(r+1)
    support = set()
    mixed = 0
    # Complete local original (mu,nu) face census, including mixed faces.
    for x in product(range(-r-1,r+1),repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                face = face_links(x,mu,nu)
                if sum(e in inside for e in face) == 1:
                    mixed += 1
                    support.update(e for e in face if e not in inside)
    require(mixed == 24*b*b*(b-1), 'original_mixed_faces')
    require(support.issubset(outer - inside),'boundary_resultants_one_shell')
    require(all(is_support_link(e,r) for e in support),'support_positive_class')
    predicted = {e for e in outer-inside if is_support_link(e,r)}
    require(support == predicted,'complete_support_classification')
    s = len(support)
    require(s == 8*b*b*(4*b-3),'exact_staple_support_count')
    crossing = sum((x[mu] == -r-1 or x[mu] == r)
                   for x,mu in support)
    parallel = s-crossing
    require(crossing == 8*b*b*b,'crossing_links')
    require(parallel == 24*(b-1)*b*b,'outer_parallel_links')
    require(len(inside) == 4*(b-1)*b*b*b,'interior_original_links')
    require(len(outer-inside)==4*((b+1)*(b+2)*(b+2)*(b+2)
                                   -(b-1)*b*b*b),'one_shell_total_links')

    touch = 0
    by_orientation = {}
    transv = [0, 0, 0]
    # Every face touching support is contained in this coordinate window.
    for x in product(range(-r-2,r+2),repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                if any(e in support for e in face_links(x,mu,nu)):
                    touch += 1
                    by_orientation[(mu,nu)] = by_orientation.get((mu,nu),0)+1
                    others=[w for w in range(4) if w!=mu and w!=nu]
                    k=sum(abs(x[w])==r+1 for w in others)
                    require(all(abs(x[w])<=r+1 for w in others),
                            'two_orthogonal_coordinates_in_window')
                    transv[k]+=1
    m = 24*b*(3*b*b+b-3)
    require(touch == m,'exact_touching_plaquette_count')
    require(len(by_orientation) == 6,'all_six_orientations')
    require(all(z == 4*b*(3*b*b+b-3)
                for z in by_orientation.values()), 'orientation_symmetry')
    require(transv[0] == 6*b*b*(8*b-4),'two_interior_transverses')
    require(transv[1] == 6*4*b*(b-1)*(b+3),'one_outer_transverse')
    require(transv[2] == 0,'two_outer_transverse_rejected')
    require(touch <= 6*s,'each_original_link_six_faces')
    # Local geometry is embedded injectively in this original periodic torus.
    L=2*(b+2)
    require(len({(tuple(v % L for v in x),mu) for x,mu in support}) == s,
            'periodic_no_link_collision')
    # The strict all-beta universal floor is kappa >= exp(-4*beta*m).
    # Since e < 3, integer production beta certifies kappa > 3^(-E).
    beta=9**12
    exponent=4*beta*m
    require(exponent > 0 and exponent > 4*beta*b*b,
            'finite_beta_positive_but_weak_floor')
    return b,s,m,exponent


def main():
    require(9**12 == 282429536481,'production_beta')
    results = [fixture(r) for r in range(1,5)]
    for r,(b,s,m,exponent) in enumerate(results,1):
        print('YM4_VOL21_GEOMETRY|r='+str(r)+'|b='+str(b)+
              '|staple_support='+str(s)+'|touch_faces='+str(m)+'|PASS')
        print('YM4_VOL21_BETA12|r='+str(r)+
              '|kappa_gt_3_pow_minus='+str(exponent)+'|CONDITIONAL_ON_V_positive')
    print('YM4_VOL21_NOISE|finite_beta_Haar_density_lower=ANALYTIC|shell_variance_floor=ANALYTIC')
    print('YM4_VOL21_SCOPE|original_SU2_4D=ANALYTIC|physical_uniform_rate=OPEN|continuum_11=OPEN')


if __name__ == '__main__':
    main()
