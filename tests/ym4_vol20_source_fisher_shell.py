"""YM4 VOL20 strict integer-pair source-Fisher and Gibbs-shell controls.

Sixteen exact abstract probability atoms, no floating arithmetic or libraries.
The continuous SU2 Haar and Wilson probability theorem is analytic.
"""
from math import gcd
from itertools import product


def require(ok, label):
    if not ok:
        raise AssertionError(label)


def q(n, d=1):
    if isinstance(n, tuple):
        require(d == 1 and len(n) == 2, 'canonical pair input')
        return n
    require(d != 0, 'nonzero denominator')
    if d < 0:
        n = -n
        d = -d
    c = gcd(abs(n), d)
    return (n//c, d//c)


def add(x, y):
    return q(x[0]*y[1]+y[0]*x[1], x[1]*y[1])


def neg(x):
    return (-x[0], x[1])


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    return q(x[0]*y[0], x[1]*y[1])


def ratio(x, y):
    require(y[0] != 0, 'nonzero ratio divisor')
    return q(x[0]*y[1], x[1]*y[0])


def square(x):
    return mul(x, x)


def total(xs):
    s = q(0)
    for x in xs:
        s = add(s, x)
    return s


def render(x):
    if x[1] == 1:
        return str(x[0])
    return str(x[0]) + '/' + str(x[1])


# A,C are exterior shells, Z is a binary Wilson-source analogue and V
# an independent nuisance sign. All weights are integer numerator-pairs.
ROWS=[]
for a,c,z,v in product((0,1),(0,1),(0,1),(-1,1)):
    success=q(2+a+2*c,8)
    mass=mul(q(1,8), success if z else sub(q(1),success))
    ROWS.append((a,c,z,v,mass))
require(total([w for a,c,z,v,w in ROWS])==q(1),'normalized measure')


def mean(func):
    return total([mul(w,q(func(a,c,z,v))) for a,c,z,v,w in ROWS])


def variance(func):
    m=mean(func)
    return mean(lambda a,c,z,v:square(sub(q(func(a,c,z,v)),m)))


def projected_score(func, feature):
    bins={}
    for a,c,z,v,w in ROWS:
        k=feature(a,c,z,v)
        mass, weighted=bins.get(k,(q(0),q(0)))
        bins[k]=(add(mass,w), add(weighted,mul(w,q(func(a,c,z,v)))))
    values={k:ratio(weighted,mass) for k,(mass,weighted) in bins.items()}
    avg=mean(func)
    pv=total([mul(mass,square(sub(values[k],avg)))
              for k,(mass,weighted) in bins.items()])
    return pv,values,bins


def covariance(f,g):
    pair=mean(lambda a,c,z,v:mul(q(f(a,c,z,v)),q(g(a,c,z,v))))
    return sub(pair,mul(mean(f),mean(g)))


def source_fisher():
    score=lambda a,c,z,v:2*a+c
    tangent=lambda a,c,z,v:v
    source=lambda a,c,z,v:z
    rescaled=lambda a,c,z,v:1000*z+17
    enlarged=lambda a,c,z,v:(z,c)
    constant=lambda a,c,z,v:0
    fisher,cond,bins=projected_score(score,source)
    other,_,_=projected_score(score,rescaled)
    larger,_,_=projected_score(score,enlarged)
    trivial,_,_=projected_score(score,constant)
    nuisance,_,_=projected_score(tangent,source)
    require(variance(score)==q(5,4),'raw score variance')
    require(fisher==q(4,63),'source Fisher')
    require(cond=={1:q(25,14),0:q(23,18)},'source score conditionals')
    require(fisher==other,'affine source normalization')
    require(trivial==q(0),'constant source zero score')
    # Nonnegative integer cross-products compare the reduced fractions.
    require(fisher[0]*larger[1]<=larger[0]*fisher[1], 'source inclusion 1')
    raw=variance(score)
    require(larger[0]*raw[1]<=raw[0]*larger[1], 'source inclusion 2')
    require(nuisance==q(0) and variance(tangent)==q(1),'projected nuisance null')
    require(mean(score)==q(3,2),'score mean')
    for z,(mass,weighted) in bins.items():
        slope=sub(weighted,mul(mass,mean(score)))
        require(slope==mul(mass,sub(cond[z],mean(score))), 'finite tilted source derivative')
    cov=covariance(source,score)
    require(cov==q(1,8),'source score covariance')
    require(square(cov)==mul(variance(source),fisher),'sharp source Cauchy-Schwarz')
    return fisher


def shell_replica():
    source=lambda a,c,z,v:z
    m0=lambda a,c,z,v:q(2+a+2*c,8)
    m1=lambda a,c,z,v:q(5+4*c,16)
    m2=lambda a,c,z,v:q(7,16)
    v0,v1,v2=variance(m0),variance(m1),variance(m2)
    require(mean(source)==q(7,16) and variance(source)==q(63,256),'source variance')
    require(v0==q(5,256) and v1==q(1,64) and v2==q(0),'shell variance')
    drop=mean(lambda a,c,z,v:square(sub(m0(a,c,z,v),m1(a,c,z,v))))
    require(drop==q(1,256) and v0==add(v1,drop),'orthogonal shell drop')
    require(ratio(drop,v0)==q(1,5),'shell relative dissipation')
    require(ratio(v0,variance(source))==q(5,63),'normalized near response')
    require(ratio(v1,variance(source))==q(4,63),'normalized far response')
    ren=lambda a,c,z,v:17+1000*z
    rencond=lambda a,c,z,v:add(q(17),mul(q(1000),m0(a,c,z,v)))
    require(variance(ren)==mul(q(1000000),variance(source)),'source rescaling')
    require(variance(rencond)==mul(q(1000000),v0),'conditional rescaling')
    values=[q(2+a+2*c,8) for a,c in product((0,1),(0,1))]
    replica=mul(q(1,16), total([square(sub(u,v)) for u in values for v in values]))
    require(replica==q(5,128) and replica==mul(q(2),v0),'two Gibbs replicas')
    return v0,v1,drop


def main():
    fisher=source_fisher()
    v0,v1,drop=shell_replica()
    print('YM4_VOL20_FISHER|source_score='+render(fisher)+'|affine_invariance=PASS|data_processing=PASS')
    print('YM4_VOL20_WARD|nuisance_raw_variance=1|source_projected=0|PASS')
    print('YM4_VOL20_REPLICA|variance='+render(v0)+'|two_replica='+render(mul(q(2),v0))+'|PASS')
    print('YM4_VOL20_SHELL|near='+render(v0)+'|far='+render(v1)+'|drop='+render(drop)+'|kappa=1/5|PASS')
    print('YM4_VOL20_SCALING|source_variance_normalized=PASS|rescale_x1000=PASS')
    print('YM4_VOL20_SCOPE|continuous_SU2=ANALYTIC|toy_integer_pairs=PASS|high_beta_physical_decay=OPEN|continuum_11=OPEN')

if __name__=='__main__':
    main()
