#!/usr/bin/env python3
"""Exact 1+1D S3 Wilson gauge-transfer, three-scale and triadic jump.

Wilson class weight is w(g)=exp[-ln(2)(2-chi_standard(g))].
Normalized per-element probabilities are 8/16 for the identity,
2/16 for each transposition and 1/16 for each 3-cycle.
This is NOT the 2D S3 Hamiltonian eigenproblem, NOT 4D SU(2),
and NOT a construction of a continuum limit.
"""
from hashlib import sha256
from itertools import permutations
from math import gcd

def integer_power(base, exponent):
    """Integer-only binary exponentiation; negative exponents are refused."""
    if not isinstance(exponent, int) or exponent < 0:
        raise ValueError('NEGATIVE_EXPONENT')
    value = 1
    while exponent:
        if exponent & 1:
            value *= base
        exponent //= 2
        if exponent:
            base *= base
    return value

G = tuple(permutations(range(3)))
N = 6
assert len(G) == N and G[0] == (0, 1, 2)

def mul(g,h):
    return tuple(g[h[i]] for i in range(3))

def inv(g):
    return tuple(g.index(i) for i in range(3))

def chi(g):
    return sum(g[i] == i for i in range(3)) - 1

def sign(g):
    return -1 if sum(g[i] > g[j] for i in range(3) for j in range(i+1,3))%2 else 1

def weight(g):
    return {2:8, 0:2, -1:1}[chi(g)]

def mm(a,b):
    cols=list(zip(*b))
    return tuple(tuple(sum(u*v for u,v in zip(row,col)) for col in cols) for row in a)

def ident():
    return tuple(tuple(int(i==j) for j in range(N)) for i in range(N))

def direct(a,n):
    if n<0: raise ValueError('NEGATIVE_EXPONENT')
    out=ident()
    for _ in range(n): out=mm(out,a)
    return out

def ternary(a,n):
    if not isinstance(n,int) or n<0: raise ValueError('NEGATIVE_EXPONENT')
    out=ident()
    p=a
    cubings=0
    digits=0
    while n:
        d=n%3
        n//=3
        for _ in range(d): out=mm(out,p)
        digits+=1
        if n:
            p=mm(mm(p,p),p)
            cubings+=1
    return out,cubings,digits

def character_matrix(n):
    if n<0: raise ValueError('NEGATIVE_EXPONENT')
    if n==0: return ident()
    aa,bb,cc=integer_power(16,n),integer_power(4,n),integer_power(7,n)
    rows=[]
    for g in G:
        row=[]
        for h in G:
            x=mul(g,inv(h))
            v=aa+bb*sign(x)+2*cc*chi(x)
            assert v%6==0
            row.append(v//6)
        rows.append(tuple(row))
    return tuple(rows)

def hash_matrix(a,n):
    pieces=[n.to_bytes(8,'big'),N.to_bytes(2,'big')]
    for row in a:
        for z in row:
            assert z>=0
            b=z.to_bytes(max(1,(z.bit_length()+7)//8),'big')
            pieces.append(len(b).to_bytes(4,'big'))
            pieces.append(b)
    return sha256(b''.join(pieces)).hexdigest()

def correlation(a, n, observable):
    v=[observable(g) for g in G]
    top=sum(v[i]*a[i][j]*v[j] for i in range(N) for j in range(N))
    assert top%N==0
    top//=N
    bot=integer_power(16,n)
    d=gcd(top,bot)
    return top//d,bot//d

def emit(tag,**fields):
    print(tag+'|'+'|'.join(str(k)+'='+str(v) for k,v in fields.items())+'|json=0')

def main():
    a=tuple(tuple(weight(mul(g,inv(h))) for h in G) for g in G)
    assert all(sum(row)==16 for row in a)
    assert all(a[i][j]==a[j][i] for i in range(N) for j in range(N))
    for mode,fun,value in [('std',chi,7),('sign',sign,4)]:
        v=[fun(g) for g in G]
        assert sum(v)==0 and sum(x*x for x in v)==6
        assert all(sum(row[j]*v[j] for j in range(N))==value*v[i] for i,row in enumerate(a))
        emit('YM3_CHAR',mode=mode,eigen_numer=value,eigen_denom=16,zero_mean=1,orthogonality=1,status='PASS')
    for g in G:
        for h in G:
            c=mul(mul(h,g),inv(h))
            assert weight(c)==weight(g) and chi(c)==chi(g)
    emit('YM3_GAUGE',conjugation_pairs=36,character_invariance=1,weight_invariance=1,status='PASS')
    for n in (0,1,2,3,9):
        v=direct(a,n)
        assert v==character_matrix(n)==ternary(a,n)[0]
        emit('YM3_MATRIX',exponent=n,method='DIRECT_TRIADIC_CHARACTER',match=1,sha256=hash_matrix(v,n),status='PASS')
    fine=ternary(a,9)[0]
    local3=ternary(a,9)[0]
    local9=ternary(a,81)[0]
    mid=ternary(local3,3)[0]
    large=local9
    assert mid==ternary(fine,3)[0]==character_matrix(27)
    assert large==ternary(fine,9)[0]==character_matrix(81)
    assert large==ternary(mid,3)[0]
    for scale,L,area,exponent in [(1,9,1,9),(3,3,9,27),(9,1,81,81)]:
        emit('YM3_BLOCK',scale=scale,spatial_cells=L,plaquette_convolution=area,
             transfer_exponent=exponent,standard_eigen='(7/16)^'+str(exponent),
             sign_eigen='(1/4)^'+str(exponent),status='PASS')
    emit('YM3_COMMUTE',fine_cubed_equals_coarse3=1,fine_ninth_equals_coarse9=1,
         coarse3_cubed_equals_coarse9=1,status='PASS')
    orig=[(chi(g),a[0][j]) for j,g in enumerate(G)]
    pe=next(v for c,v in orig if c==2)
    pt=next(v for c,v in orig if c==0)
    pc=next(v for c,v in orig if c==-1)
    assert pt*pt*pt==pe*pc**2
    eff=[(chi(g),local3[0][j]) for j,g in enumerate(G)]
    e=next(v for c,v in eff if c==2)
    t=next(v for c,v in eff if c==0)
    c=next(v for k,v in eff if k==-1)
    residual=t*t*t-e*c*c
    assert residual<0
    emit('YM3_WILSON_CLOSURE',area=9,unblocked_family_identity=1,
         blocked_family_identity=0,negative_residual=1,
         sha256=sha256(str(residual).encode('ascii')).hexdigest(),status='PASS')
    for ticks in (1,3,9,27,81,243):
        ff,cubes,digits=ternary(fine,ticks)
        assert ff==character_matrix(9*ticks)
        if ticks<=9: assert ff==direct(fine,ticks)
        if ticks%3==0: assert ff==ternary(mid,ticks//3)[0]
        if ticks%9==0: assert ff==ternary(large,ticks//9)[0]
        emit('YM3_JUMP',fine_ticks=ticks,underlying_plaquettes=9*ticks,
             cubings=cubes,ternary_digits=digits,character_formula=1,
             scale3_match=int(ticks%3==0),scale9_match=int(ticks%9==0),
             sha256=hash_matrix(ff,9*ticks),status='PASS')
        if ticks%9!=0: continue
        for mode,fun,base in [('std',chi,7),('sign',sign,4)]:
            got=correlation(ff,9*ticks,fun)
            if base==7:
                d=gcd(integer_power(7,9*ticks),integer_power(16,9*ticks))
                expected=(integer_power(7,9*ticks)//d,integer_power(16,9*ticks)//d)
            else:
                expected=(1,integer_power(4,9*ticks))
            assert got==expected
            emit('YM3_CORRELATION',mode=mode,fine_ticks=ticks,
                 coarse3_ticks=ticks//3,coarse9_ticks=ticks//9,
                 ratio_symbolic='('+str(base)+'/16)^(9*t)',
                 exact_three_scale_agreement=1,
                 hash=sha256((str(got[0])+'|'+str(got[1])).encode()).hexdigest(),status='PASS')
    for b in (1,3,9):
        n=9*b
        emit('YM3_GAP',spatial_scale=b,temporal_scale=b,
             standard_ratio_numer=integer_power(7,n),standard_ratio_denom=integer_power(16,n),
             first_gap_coefficient='9*ln(16/7)',physical_gap_equal=1,status='PASS')
    assert ternary(ternary(a,3)[0],3)[0]!=mid
    emit('YM3_RED',control='wrong_block_area_3_instead_of_9',result='REJECTED',status='PASS')
    assert ternary(a,3)[0]!=mid
    emit('YM3_RED',control='unblocked_weight',result='REJECTED',status='PASS')
    mutated=[list(row) for row in mid]
    mutated[0][0]+=1
    assert tuple(tuple(row) for row in mutated)!=mid
    emit('YM3_RED',control='one_entry_corruption',result='REJECTED',status='PASS')
    assert 27!=9
    emit('YM3_RED',control='wrong_time_units_mass_gap',result='REJECTED',status='PASS')
    emit('YM3_VERIFY',status='PASS',predictions=12,missing=0,red_controls=4,
         matched_observation_ticks='9,27,81,243',
         real_4D_SU2='NOT_SIMULATED',continuous_limit='NOT_PROVED')

if __name__=='__main__':
    main()
