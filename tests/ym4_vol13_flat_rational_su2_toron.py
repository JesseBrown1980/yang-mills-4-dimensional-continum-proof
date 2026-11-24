"""VOL13 exact continuous-centre-adjacent flat SU2 toron scope controls.

Uses the unit-circle SU2 subgroup {(a+bi) : a*a+b*b=1}, represented
as exact rational Gaussian integers. All full L4 and L6 original 4D
plaquettes/staple products are checked; no floating point.
"""
from functools import reduce
from itertools import product
from math import gcd

def require(ok,label):
    if not ok:
        raise ValueError(label)

def rational_pair(a,b,d):
    require(d>0,'denominator_positive')
    g=gcd(gcd(abs(a),abs(b)),d)
    require(g>0,'normalization_nonzero')
    return (a//g,b//g,d//g)

ONE=(1,0,1)
Q=(3,4,5)

def mul(a,b):
    x,y,d=a
    u,v,e=b
    return rational_pair(x*u-y*v,x*v+y*u,d*e)

def inv(a):
    x,y,d=a
    return (x,-y,d)

def is_unit(a):
    x,y,d=a
    return x*x+y*y==d*d

def step(x,mu,L,k=1):
    y=list(x)
    y[mu]=(y[mu]+k)%L
    return tuple(y)

def sites(L):
    return product(range(L),repeat=4)

def construct(L,q):
    return {(x,mu):(q if mu==0 else ONE) for x in sites(L) for mu in range(4)}

def plaq(L,U,x,mu,nu):
    # q_mu q_nu q_mu^{-1} q_nu^{-1} in original directed plaquette.
    return mul(mul(mul(U[(x,mu)],U[(step(x,mu,L),nu)]),
                   inv(U[(step(x,nu,L),mu)])),inv(U[(x,nu)]))

def staples(L,U,x,mu):
    y=step(x,mu,L)
    vals=[]
    for nu in range(4):
        if nu==mu:
            continue
        xp=step(x,nu,L)
        xm=step(x,nu,L,-1)
        ym=step(xm,mu,L)
        # Products from source x to target x+mu
        vals.append(mul(mul(U[(x,nu)],U[(xp,mu)]),
                        inv(U[(y,nu)])))
        vals.append(mul(mul(inv(U[(xm,nu)]),U[(xm,mu)]),
                        U[(ym,nu)]))
    return vals

def winding(L,U,mu):
    x=(0,0,0,0)
    acc=ONE
    for unused in range(L):
        acc=mul(acc,U[(x,mu)])
        x=step(x,mu,L)
    require(x==(0,0,0,0),'closed_periodic_path')
    return acc

def certify(L):
    require(L in (4,6),'even_original_volumes')
    U=construct(L,Q)
    faces=0
    stars=0
    for x in sites(L):
        for mu in range(4):
            S=staples(L,U,x,mu)
            require(len(S)==6 and all(s==U[(x,mu)] for s in S),
                    'all_six_exact_staples_equal_original_link')
            for i in range(6):
                for j in range(i+1,6):
                    require(S[i]==S[j],'all_fifteen_double_staple_loops_good')
                    stars+=1
            for nu in range(mu+1,4):
                require(plaq(L,U,x,mu,nu)==ONE,'original_SU2_plaquette_flat')
                faces+=1
    require(faces==6*L**4 and stars==4*L**4*15,
            'all_original_4D_plaquettes_and_stars')
    h=winding(L,U,0)
    expected=rational_pair(-527,-336,625) if L==4 else rational_pair(11753,-10296,15625)
    require(h==expected and is_unit(h),'exact_rational_SU2_winding')
    require(h!=ONE and h!=(-1,0,1),'noncentral_nontrivial_winding')
    # All contractible plaquette Wilson traces identically +1, while
    # Polyakov Wilson trace is 2*h[0]/h[2] and differs from both +/-2.
    require(abs(h[0])<h[2],'noncentral_normalized_polyakov_trace')
    # The full one-parameter family q_theta=cos theta+i sin theta
    # has identical flat plaquettes for all theta by commutativity.
    return h

def main():
    require(is_unit(Q) and mul(Q,inv(Q))==ONE,'genuine_unit_SU2_rational_quaternion')
    a=certify(4)
    b=certify(6)
    require(a==(-527,-336,625) and b==(11753,-10296,15625),
            'full_rational_polyakov_holonomy_pins')
    return (
        'YM4_VOL13_TORON|SU2_real_quaternion_continuous_U1_subgroup=EXACT_RATIONAL|L4_L6=PASS|json=0\n'
        'YM4_VOL13_TORON_PLAQ|all_original_4d_plaquettes_equal_identity=PASS|all_six_staples_per_link_identical=PASS|all_15_pairs_good=PASS|json=0\n'
        'YM4_VOL13_TORON_W4|normalized_Polyakov_real=-527/625|imag=-336/625|noncentral=PASS|json=0\n'
        'YM4_VOL13_TORON_W6|normalized_Polyakov_real=11753/15625|imag=-10296/15625|noncentral=PASS|json=0\n'
        'YM4_VOL13_TORON_SCOPE|flat_SU2_moduli_continuous=ANALYTIC|local_contractible_Wilson_plaquettes=IDENTICAL|global_winding_unequal=YES|json=0\n'
        'YM4_VOL13_NEXT|local_contractible_observable_coupling=OPEN|nonabelian_chord_average=OPEN|all_sector_holonomy_transport=OPEN|11_continuum_gates=OPEN|json=0\n'
    )

if __name__=='__main__':
    print(main(),end='')
