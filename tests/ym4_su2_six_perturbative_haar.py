"""WG09 exact second and third order original continuous SU2 Haar six-mode pilot.
Uses integer quaternion multiplication and genuine SU2 2nd/4th Haar moments.
Finite-beta fourth-order spectral remainder is OPEN.
"""
from itertools import product, combinations, permutations
from functools import lru_cache
from fractions import Fraction as F
from collections import defaultdict, Counter

S=tuple(product((0,1),repeat=3))
L=tuple((s,d) for s in S for d in range(3))
I={e:i for i,e in enumerate(L)}
def sh(s,d):return tuple(s[k]^(k==d) for k in range(3))
def pl(s,a,b):return ((s,a,1),(sh(s,a),b,1),(sh(s,b),a,-1),(s,b,-1))
P=tuple(pl(s,a,b) for s in S for a,b in combinations(range(3),2))
def wind(s,d):return ((s,d,1),(sh(s,d),d,1))
D=[]
for d in range(3):
 other=[k for k in range(3) if k!=d]
 ws=[]
 for bits in product((0,1),repeat=2):
  s=tuple(dict(zip(other,bits)).get(k,0) for k in range(3))
  ws.append(wind(s,d))
 D.extend((a,b) for a,b in combinations(ws,2))
B=tuple((p,) for p in P)+tuple(D)
def mask(loops):return sum(1<<I[(s,d)] for loop in loops for s,d,_ in loop)
M=tuple(mask(loops) for loops in B)
PM=tuple(mask((p,)) for p in P)
A=tuple(tuple(int(i!=j and (M[i]^M[j]) in PM) for j in range(42)) for i in range(42))
seen=set();components=[]
for i in range(42):
 if i not in seen:
  queue=[i];seen.add(i)
  for v in queue:
   for w in range(42):
    if A[v][w] and w not in seen:seen.add(w);queue.append(w)
  components.append(tuple(sorted(queue)))
BLOCKS=tuple(c for c in components if len(c)==6)

@lru_cache(None)
def multiply(x,y):
 if x==0:return (1,y)
 if y==0:return (1,x)
 if x==y:return (-1,0)
 if (x,y) in ((1,2),(2,3),(3,1)):return (1,6-x-y)
 return (-1,6-x-y)

@lru_cache(None)
def trace_tensor(signs):
 out={}
 for letters in product(range(4),repeat=len(signs)):
  sign=1;state=0
  for letter,ori in zip(letters,signs):
   m,state=multiply(state,letter)
   sign*=m*(-1 if ori<0 and letter!=0 else 1)
  if state==0:out[letters]=2*sign
 return out

def contract(factors):
 while len(factors)>1:
  proposals=[]
  for a in range(len(factors)):
   for b in range(a+1,len(factors)):
    la,lb=factors[a][0],factors[b][0]
    common=set(la)&set(lb)
    free=(set(la)|set(lb))-common
    proposals.append(((len(free),-len(common),len(factors[a][1])*len(factors[b][1])),a,b))
  _,a,b=min(proposals)
  la,da=factors[a];lb,db=factors[b]
  common=tuple(v for v in la if v in lb)
  onlya=tuple((v,k) for k,v in enumerate(la) if v not in common)
  onlyb=tuple((v,k) for k,v in enumerate(lb) if v not in common)
  sa={v:k for k,v in enumerate(la)};sb={v:k for k,v in enumerate(lb)}
  bucket=defaultdict(list)
  for xb,vb in db.items():
   bucket[tuple(xb[sb[v]] for v in common)].append((xb,vb))
  result=defaultdict(int)
  for xa,va in da.items():
   for xb,vb in bucket.get(tuple(xa[sa[v]] for v in common),()):
    key=tuple(xa[k] for v,k in onlya)+tuple(xb[k] for v,k in onlyb)
    result[key]+=va*vb
  labels=tuple(v for v,k in onlya)+tuple(v for v,k in onlyb)
  for i in sorted((a,b),reverse=True):factors.pop(i)
  factors.append((labels,{k:v for k,v in result.items() if v}))
 assert factors[0][0]==()
 return factors[0][1].get((),0)

@lru_cache(100000)
def haar(i,j,plaquettes):
 loops=((B[i] if i is not None else ())+
        (B[j] if j is not None else ())+tuple(P[p] for p in plaquettes))
 occ={}
 for il,loop in enumerate(loops):
  for k,(s,d,ori) in enumerate(loop):
   occ.setdefault((s,d),[]).append((il,k))
 if any(len(v)%2 for v in occ.values()):return F(0)
 assert all(len(v) in (2,4) for v in occ.values())
 denominator=1;n4=0
 for v in occ.values():
  denominator*=4 if len(v)==2 else 24
  if len(v)==4:n4+=1
 pairings=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
 total=0
 for choice in product(range(3),repeat=n4):
  labels={};next_label=0;k4=0
  for v in occ.values():
   if len(v)==2:
    for x in v:labels[x]=next_label
    next_label+=1
   else:
    for pair in pairings[choice[k4]]:
     for idx in pair:labels[v[idx]]=next_label
     next_label+=1
    k4+=1
  factors=[]
  for il,loop in enumerate(loops):
   factors.append((tuple(labels[(il,k)] for k in range(len(loop))),
                   trace_tensor(tuple(o for _,_,o in loop))))
  total+=contract(factors)
 return F(total,denominator*2**len(plaquettes))

def orbitals():
 index={m:i for i,m in enumerate(M)}
 blockof={i:b for b,c in enumerate(BLOCKS) for i in c}
 actions=[]
 for bits in product((0,1),repeat=3):
  for perm in permutations(range(3)):
   g=[]
   for mask0 in M:
    new=0
    for i,(s,d) in enumerate(L):
     if mask0&(1<<i):
      ns=tuple(s[perm[k]]^bits[k] for k in range(3))
      new|=1<<I[(ns,perm.index(d))]
    g.append(index[new])
   assert all(A[i][j]==A[g[i]][g[j]] for i in range(42) for j in range(42))
   actions.append(tuple(blockof[g[c[0]]] for c in BLOCKS))
 assert len(set(actions))==48
 groups=[];seen=set()
 for j in range(6):
  if (0,j) not in seen:
   o={(g[0],g[j]) for g in actions}
   groups.append(o);seen.update(o)
 assert sorted(map(len,groups))==[6,6,24]
 opposite=next(o for o in groups if len(o)==6 and any(i!=j for i,j in o))
 opp=next(j for i,j in opposite if i==0)
 cross=next(j for j in range(1,6) if j!=opp)
 return opp,cross

def block_v2(a,b):
 parts=defaultdict(F)
 for i in BLOCKS[a]:
  for j in BLOCKS[b]:
   for p in range(24):
    for q in range(24):
     if M[i]^M[j]==PM[p]^PM[q]:
      z=haar(i,j,(p,q))
      if a!=b:assert z==F(1,4)
      key=('P' if i<24 else 'D')+('P' if j<24 else 'D')
      parts[key]+=z
 assert parts['PD']==parts['DP']==0
 return parts['PP']/8+parts['DD']/4,parts

def certify():
 assert len(B)==42 and len(set(M))==42
 assert sum(map(sum,A))==96
 assert sorted(map(len,components))==[1]*6+[6]*6
 assert haar(0,0,(0,0))==F(1,2)
 opp,cross=orbitals()
 diag,parts=block_v2(0,0)
 bv,_=block_v2(0,opp)
 cv,_=block_v2(0,cross)
 assert diag==F(445,64) and bv==cv==F(1)
 assert parts['PP']==F(251,8) and parts['DD']==F(97,8)
 assert diag/2-F(1,2)==F(381,128)
 assert bv/2-F(1,2)==cv/2-F(1,2)==0

 spinone=[]
 for d in range(3):
  other=[k for k in range(3) if k!=d]
  for bits in product((0,1),repeat=2):
   s=tuple(dict(zip(other,bits)).get(k,0) for k in range(3))
   spinone.append(mask((wind(s,d),)))
 assert len(set(spinone))==12 and all(m.bit_count()==2 for m in spinone)
 parity=[(i,p) for i in range(42) for p in range(24) if M[i]^PM[p]==0]
 assert len(parity)==24 and all(i==p for i,p in parity)

 pairs=defaultdict(list)
 for p in range(24):
  for q in range(24):pairs[PM[p]^PM[q]].append((p,q))
 V2=[[sum((haar(i,j,pq) for pq in pairs.get(M[i]^M[j],())),F())
      for j in range(42)] for i in range(42)]
 v=[F(1,2) if i<24 else F() for i in range(42)]
 H2=[[V2[i][j]/2-v[i]*v[j] for j in range(42)] for i in range(42)]
 A2=[[sum(A[i][k]*A[k][j] for k in range(42)) for j in range(42)]
     for i in range(42)]
 h0=[];h1=[]
 for block in BLOCKS:
  ps=[j for j in block if j<24];ds=[j for j in block if j>=24]
  assert len(ps)==4 and len(ds)==2
  h0.append([sum(H2[k][j] for j in ds)/2 for k in range(42)])
  h1.append([sum(H2[k][j] for j in ps)/4 for k in range(42)])

 def quad(a,b,X):
  a0,a1=h0[a],h1[a];b0,b1=h0[b],h1[b]
  x0=[sum(X[i][j]*b0[j] for j in range(42)) for i in range(42)]
  x1=[sum(X[i][j]*b1[j] for j in range(42)) for i in range(42)]
  return (sum(a0[i]*x0[i]+2*a1[i]*x1[i] for i in range(42)),
          sum(a0[i]*x1[i]+a1[i]*x0[i] for i in range(42)))
 R=[[2*int(i==j)-F(3,16)*A2[i][j] for j in range(42)] for i in range(42)]
 mix={}
 for a,b in ((0,0),(0,opp),(0,cross)):
  r0,r1=quad(a,b,R);s0,s1=quad(a,b,A)
  assert 2*r1-s0/4==0
  mix[(a,b)]=r0-s1/4
 assert mix[(0,0)]==F(561,16384)
 assert mix[(0,opp)]==F(1,32)
 assert mix[(0,cross)]==F(1,64)

 triples=defaultdict(list)
 for p in range(24):
  for q in range(24):
   for r in range(24):triples[PM[p]^PM[q]^PM[r]].append((p,q,r))
 third={}
 for a,b in ((0,0),(0,opp),(0,cross)):
  parts=defaultdict(F)
  for i in BLOCKS[a]:
   for j in BLOCKS[b]:
    for pqr in triples.get(M[i]^M[j],()):
     tag=('P' if i<24 else 'D')+('P' if j<24 else 'D')
     parts[tag]+=haar(i,j,pqr)
  assert parts['PP']==parts['DD']==0
  val=parts['PD']+parts['DP']
  assert val==(F(40) if a==b else F(6))
  third[(a,b)]=val/8

 w2=[sum((haar(i,None,pq) for pq in pairs.get(M[i],())),F()) for i in range(42)]
 assert all(x==0 for x in w2[:24])
 assert Counter(w2[24:])=={F(1,4):12,F():6}
 coeff={pair:third[pair]/6-F(1,8)+mix[pair] for pair in ((0,0),(0,opp),(0,cross))}
 assert coeff[(0,0)]==F(36499,49152)
 assert coeff[(0,opp)]==F(1,32)
 assert coeff[(0,cross)]==F(1,64)
 assert coeff[(0,cross)]>0 and coeff[(0,opp)]+2*coeff[(0,cross)]>0
 return (
  "YM4_WG09_HAAR|continuous_SU2_link_fourth_moments=EXACT|chi_W2_chi_fixture=1/2|source_G42=42|json=0\n"
  "YM4_WG09_SECOND|projected_V2_diagonal=445/64|offdiagonal=1|vacuum_rankone=1/2_J6|Schur_beta2=381/128_I6|json=0\n"
  "YM4_WG09_TAIL|leading_two_link_spinone_neutral=12|E_to_spinone_V=ZERO_BY_SELECTION|higher_tail_relative=O_beta2|json=0\n"
  "YM4_WG09_THIRD|V3_PD_plus_DP_diagonal=40|offdiagonal=6|H2_internal_mixing_opposite=1/32_sqrt2|other=1/64_sqrt2|json=0\n"
  "YM4_WG09_THIRD_SPLIT|matrix=sqrt2_(36499/49152_I+1/32_O+1/64_X)|symmetric_minus_even=3sqrt2/32|symmetric_minus_odd=sqrt2/8|json=0\n"
  "YM4_WG09_VERDICT|third_order_signs=POSITIVE|full_finite_beta_order_remainder=OPEN|continuum_mass_gap=OPEN|json=0\n"
 )
if __name__=="__main__":
 print(certify(),end="")
