"""YM4 VOL20 strict Fraction source-Fisher and nested Gibbs-shell controls.

An exact rational probability-space falsifier for analytic Wilson/SU2 identities.
The 16 states below are a toy measure, not a continuous SU(2) simulation.
"""
from fractions import Fraction as Q
from itertools import product


def require(ok, label):
    if not ok:
        raise AssertionError(label)


# A and C are two exterior shells; Z is the binary Wilson-source analogue.
# A fair independent +/-1 variable V plays an abstract gauge-nuisance direction.
ROWS = []
for a, c, z, v in product((0, 1), (0, 1), (0, 1), (-1, 1)):
    success = Q(2 + a + 2*c, 8)
    weight = Q(1, 8) * (success if z else 1 - success)
    ROWS.append((a, c, z, v, weight))
require(sum(row[4] for row in ROWS) == 1, 'normalized_measure')


def mean(func):
    return sum(w * Q(func(a, c, z, v)) for a, c, z, v, w in ROWS)


def variance(func):
    m = mean(func)
    return mean(lambda a, c, z, v: (Q(func(a, c, z, v)) - m) ** 2)


def projected_score(func, feature):
    bins = {}
    for a, c, z, v, weight in ROWS:
        k = feature(a, c, z, v)
        mass, total = bins.get(k, (Q(0), Q(0)))
        bins[k] = (mass + weight, total + weight * Q(func(a, c, z, v)))
    values = {k: total / mass for k, (mass, total) in bins.items()}
    avg = mean(func)
    pv = sum(mass * (values[k] - avg)**2 for k, (mass, total) in bins.items())
    return pv, values, bins


def covariance(f, g):
    return mean(lambda a, c, z, v: Q(f(a, c, z, v)) * Q(g(a, c, z, v))) - mean(f)*mean(g)


def source_fisher():
    score = lambda a, c, z, v: 2*a + c
    tangent = lambda a, c, z, v: v
    source = lambda a, c, z, v: z
    source_rescaled = lambda a, c, z, v: 1000*z+17
    extension = lambda a, c, z, v: (z, c)
    constant = lambda a, c, z, v: 0
    fisher, cond, bins = projected_score(score, source)
    fisher_rescaled, _, _ = projected_score(score, source_rescaled)
    extended, _, _ = projected_score(score, extension)
    trivial, _, _ = projected_score(score, constant)
    nuisance, _, _ = projected_score(tangent, source)
    require(variance(score) == Q(5, 4), 'raw_score_variance')
    require(fisher == Q(4, 63), 'source_fisher_exact')
    require(cond == {1: Q(25, 14), 0: Q(23, 18)}, 'conditional_source_score')
    require(fisher == fisher_rescaled, 'source_affine_rescaling_invariant')
    require(trivial == 0 and fisher <= extended <= variance(score), 'data_processing')
    require(nuisance == 0 and variance(tangent) == 1, 'nuisance_projected_null')
    require(mean(score) == Q(3, 2), 'mean_score')
    # Differentiate the normalized finite exponential tilt at t=0.
    for z, (mass, total) in bins.items():
        tangent_mass = total - mass * mean(score)
        require(tangent_mass == mass * (cond[z] - mean(score)), 'pushed_score_derivative')
    require(covariance(source, score) == Q(1, 8), 'source_score_covariance')
    require(covariance(source, score)**2 == variance(source)*fisher,
            'sharp_source_CS')
    return fisher


def shell_replica():
    source = lambda a, c, z, v: z
    m0 = lambda a, c, z, v: Q(2+a+2*c, 8)
    m1 = lambda a, c, z, v: Q(5+4*c, 16)
    m2 = lambda a, c, z, v: Q(7, 16)
    v0, v1, v2 = variance(m0), variance(m1), variance(m2)
    require(mean(source) == Q(7,16) and variance(source) == Q(63,256), 'source_variance')
    require(v0 == Q(5,256) and v1 == Q(1,64) and v2 == 0, 'shell_variance')
    drop = mean(lambda a, c, z, v: (m0(a,c,z,v) - m1(a,c,z,v))**2)
    require(drop == Q(1,256) and v0 == v1 + drop, 'orthogonal_shell_drop')
    require(drop / v0 == Q(1,5), 'shell_relative_dissipation')
    require(v0/variance(source) == Q(5,63), 'near_normalized_exterior_response')
    require(v1/variance(source) == Q(4,63), 'far_normalized_exterior_response')
    require(variance(lambda a,c,z,v: 17+1000*z) == 1000000*variance(source),
            'physical_affine_rescale')
    require(variance(lambda a,c,z,v: 17+1000*m0(a,c,z,v)) == 1000000*v0,
            'conditional_variance_rescale')
    values = [Q(2+a+2*c,8) for a,c in product((0,1),(0,1))]
    replica = sum((u-v)**2 for u in values for v in values) / 16
    require(replica == Q(5,128) == 2*v0, 'replica_variance_identity')
    return v0, v1, drop


def main():
    fisher = source_fisher()
    v0,v1,drop = shell_replica()
    print('YM4_VOL20_FISHER|source_score='+str(fisher)+'|affine_invariance=PASS|data_processing=PASS')
    print('YM4_VOL20_WARD|nuisance_raw_variance=1|source_projected=0|PASS')
    print('YM4_VOL20_REPLICA|variance='+str(v0)+'|two_replica='+str(2*v0)+'|PASS')
    print('YM4_VOL20_SHELL|near='+str(v0)+'|far='+str(v1)+'|drop='+str(drop)+'|kappa=1/5|PASS')
    print('YM4_VOL20_SCALING|source_variance_normalized=PASS|rescale_x1000=PASS')
    print('YM4_VOL20_SCOPE|continuous_SU2=ANALYTIC|toy_Fraction=PASS|high_beta_physical_decay=OPEN|continuum_11=OPEN')


if __name__=='__main__':
    main()
