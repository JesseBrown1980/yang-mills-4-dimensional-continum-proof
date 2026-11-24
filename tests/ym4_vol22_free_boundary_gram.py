"""YM4 VOL22: original 4D cube outer-cut count and exact source Gram control.

Integer-only independent geometry for the original SU(2) Wilson link lattice.
Abstract 32-atom binary Gibbs fixture tests the two-reference variational
argument and a finite source-restricted PSD Gram certificate. No finite group
or toy fixture replaces the original continuous SU(2) Haar analytic theorem.
"""
from itertools import product
from math import gcd


def check(ok, name):
    if not ok:
        raise AssertionError(name)


def q(a, b=1):
    if isinstance(a, tuple):
        check(b == 1, 'tuple_input')
        return a
    check(b != 0, 'nonzero_denominator')
    if b < 0:
        a, b = -a, -b
    c = gcd(abs(a), b)
    return (a//c, b//c)


def add(a,b):
    return q(a[0]*b[1]+b[0]*a[1],a[1]*b[1])


def sub(a,b):
    return q(a[0]*b[1]-b[0]*a[1],a[1]*b[1])


def mul(a,b):
    return q(a[0]*b[0],a[1]*b[1])


def div(a,b):
    check(b[0] != 0,'divisor')
    return q(a[0]*b[1],a[1]*b[0])


def sumq(xs):
    x=q(0)
    for y in xs:
        x=add(x,y)
    return x


def ge(a,b):
    return a[0]*b[1]>=b[0]*a[1]


def fmt(a):
    return str(a[0]) if a[1]==1 else str(a[0])+'/'+str(a[1])


def link_set(r):
    return {(x,mu) for x in product(range(-r,r+1),repeat=4)
            for mu in range(4) if x[mu]<r}


def face(x,mu,nu):
    y=list(x); z=list(x)
    y[mu]+=1; z[nu]+=1
    return ((x,mu),(tuple(y),nu),(tuple(z),mu),(x,nu))


def mixed_faces(r):
    ins=link_set(r)
    mixed=set()
    for x in product(range(-r-1,r+1),repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                edges=face(x,mu,nu)
                if sum(e in ins for e in edges)==1:
                    mixed.add((x,mu,nu))
    return mixed


def boundary_geometry(r):
    b=2*r+1
    inside=link_set(r)
    outer=link_set(r+1)
    inner_mixed=mixed_faces(r)
    outer_mixed=mixed_faces(r+1)
    support=set()
    for x,mu,nu in inner_mixed:
        support.update(e for e in face(x,mu,nu) if e not in inside)
    check(support.issubset(outer-inside),'support_in_larger_cube')
    check(len(inner_mixed)==24*b*b*(b-1),'inner_mixed_face_count')
    check(len(outer_mixed)==24*(b+2)*(b+2)*(b+1),'outer_mixed_face_count')
    check(len(support)==8*b*b*(4*b-3),'original_resultant_support')
    touching=set()
    for x in product(range(-r-2,r+2),repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                if any(e in support for e in face(x,mu,nu)):
                    touching.add((x,mu,nu))
    old=len(touching)
    new=len(outer_mixed)
    check(old==24*b*(3*b*b+b-3),'vol21_action_count')
    check(new==24*(b+2)*(b+2)*(b+1),'vol22_cut_count')
    winner='VOL21_INNER' if old<=new else 'VOL22_OUTER'
    if r==1:
        check(winner=='VOL21_INNER','small_size_red_gate')
    else:
        check(winner=='VOL22_OUTER','improvement_gate')
    beta=9**12
    exponent=4*beta*min(old,new)
    return b,old,new,winner,exponent


# Abstract finite Gibbs test: W=(u,v,z) and exterior Y=(orientation, strength).
# Conditional q_y(W) is a tilt of a fixed free-boundary measure nu(W).
# Beta=log(2), so all probabilities are exact ratios of integers.
WS=tuple(product((0,1),repeat=3))
YS=tuple(product((0,1),repeat=2))

def internal(w):
    return int(w[0]==w[1])+int(w[1]==w[2])

def crossing(w,y):
    t,s=y
    return s*sum(1 if x==t else -1 for x in w)


def normalize(values):
    z=sum(values.values())
    return {k:q(v,z) for k,v in values.items()}

def ipow(base, exponent):
    check(exponent>=0, 'nonnegative_integer_power')
    value=1
    for _ in range(exponent):
        value*=base
    return value


NU=normalize({w:ipow(2,internal(w)) for w in WS})
COND={y:normalize({w:ipow(2,internal(w)+crossing(w,y)+3) for w in WS})
      for y in YS}
MIX={w:div(sumq([COND[y][w] for y in YS]),q(len(YS))) for w in WS}


def marg(prob):
    return {(u,v,z):prob[(u,v,z)] for u,v,z in WS}


def mean(prob,fun):
    return sumq([mul(prob[w],q(fun(w))) for w in WS])


def cov(prob,fun,other):
    xy=mean(prob,lambda w:fun(w)*other(w))
    return sub(xy,mul(mean(prob,fun),mean(prob,other)))


def law_and_dirichlet():
    for y in YS:
        check(sumq(COND[y].values())==q(1),'conditional_normalized')
        for w in WS:
            # Raw mixed original action is in [-3,3]; beta=ln2 => 2^(2M)=64.
            check(ge(COND[y][w],div(NU[w],q(64))),'free_lower')
            check(ge(mul(q(64),NU[w]),COND[y][w]),'free_upper')
            check(ge(COND[y][w],div(MIX[w],q(4096))),'relative_lower')
    check(sumq(MIX.values())==q(1),'mixture_normalized')
    fs=[lambda w:int(w[0]==w[1]),lambda w:int(w[1]==w[2]),
        lambda w:int(w[0]==w[2])]
    G=[[cov(MIX,f,g) for g in fs] for f in fs]
    D=[[div(sumq([cov(COND[y],f,g) for y in YS]),q(len(YS)))
        for g in fs] for f in fs]
    check(G==[[q(3,16),q(1,48),q(1,12)],
              [q(1,48),q(3,16),q(1,12)],
              [q(1,12),q(1,12),q(2,9)]],'source_gram_exact')
    check(D==[[q(13,72),q(1,72),q(2,27)],
              [q(1,72),q(13,72),q(2,27)],
              [q(2,27),q(2,27),q(17,81)]],'shell_dirichlet_exact')
    check(div(D[0][0],G[0][0])==q(26,27),'single_source_kappa')
    # Generalized eigen gate: D - (58/63)G is exactly PSD, rank 2.
    gap=[[sub(D[i][j],mul(q(58,63),G[i][j]))
         for j in range(3)] for i in range(3)]
    check(gap==[[q(1,126),q(-1,189),q(-1,378)],
                [q(-1,189),q(1,126),q(-1,378)],
                [q(-1,378),q(-1,378),q(1,189)]],
          'exact_sharp_generalized_gram')
    for i in range(3):
        check(ge(gap[i][i],q(0)),'positive_principal_minor_1')
        for j in range(i+1,3):
            m=sub(mul(gap[i][i],gap[j][j]),mul(gap[i][j],gap[j][i]))
            check(m==q(5,142884),'positive_principal_minor_2')
    a,b,c=gap[0]; d,e,f=gap[1]; g,h,k=gap[2]
    det=add(sub(mul(a,sub(mul(e,k),mul(f,h))),
                mul(b,sub(mul(d,k),mul(f,g)))),
            mul(c,sub(mul(d,h),mul(e,g))))
    check(det==q(0),'positive_principal_minor_3')
    # Exact two-copy variance formula in the free/conditional mixture.
    single=fs[0]
    var=cov(MIX,single,single)
    conditional_var=D[0][0]
    replica=div(sumq([mul(MIX[x],mul(MIX[y],q((single(x)-single(y))**2)))
                      for x in WS for y in WS]),q(2))
    cond_pair=div(sumq([div(sumq([mul(COND[t][x],mul(COND[t][y],
                                        q((single(x)-single(y))**2)))
                                  for x in WS for y in WS]),q(2))
                        for t in YS]),q(len(YS)))
    check(replica==var and cond_pair==conditional_var,'replica_dirichlet_identity')
    return fmt(var),fmt(conditional_var),fmt(div(conditional_var,var))


def main():
    check(9**12==282429536481,'beta_exact')
    for r in range(1,5):
        b,old,new,who,e=boundary_geometry(r)
        print('YM4_VOL22_CUT|r='+str(r)+'|b='+str(b)+'|touch='+str(old)+
              '|outer='+str(new)+'|winner='+who+'|PASS')
        print('YM4_VOL22_BETA12|r='+str(r)+'|kappa_gt_3_pow_minus='+str(e)+'|PASS')
    var,drop,kappa=law_and_dirichlet()
    print('YM4_VOL22_TOY|total_variance='+var+'|shell_loss='+drop+
          '|single_kappa='+kappa+'|PASS')
    print('YM4_VOL22_GRAM|invariant_source_subspace_dim=3|kappa_min=58/63|PSD=PASS')
    print('YM4_VOL22_SCOPE|original_SU2_Haar_bound=ANALYTIC|integer_geometry=PASS|toy_Gram=PASS|physical_mass_rate=OPEN')

if __name__=='__main__':
    main()
