# A derivation of the sign theorem from its statement alone

A fresh seat of the same model family as the second seat, on November 4, 2026, shown the statement and not the proof in [the note](../../docs/NOTE-YM4-02c-SITE-SIGN.md). A pencil proof, with nothing run. Its fields follow verbatim. It reached the same route as the note: one link at a time, independent staples, and the L2 matrix coefficient. Review from a different model family stays with GPT-6.

**Verdict:** TRUE_AS_STATED

## Proof

```text
STATUS: pencil proof, tag NAMED. Machine check NOT_MEASURED, because the task fixed this as pencil-only. Refutation attempt found no falsifier.
Notation: s=sign w, so s=+-1 a.e. and ||s||_2=1. Links are (x,i). (L_t s)(y)=s(ty). rho(t)=<s,L_t s>=int s(y)s(ty)dy.

STEP 0, incidence. Since all L_i>=2, the four links of a plaquette are distinct, so U_p is Haar and s(U_p)=+-1 a.e.
For each j!=i, link (x,i) lies in the plane {i,j} plaquettes based at x and at x-e_j, distinct since L_j>=2.
So each link lies in exactly m=2(k-1)>=2 plaquettes, once each. Their direction-j links are (x,j), (x+e_i,j),
(x-e_j,j), (x-e_j+e_i,j): four distinct links since L_i,L_j>=2.

STEP 1, (<=). Let s=eps*kappa a.e. Each U_p is Haar, so a.e. s(U_p)=eps*kappa(U_p) for all p. Since kappa is a
homomorphism to an abelian group with kappa(g^-1)=kappa(g), prod_p kappa(U_p)=prod_links kappa(link)^m=1, m even.
So sign g=eps^N a.e. (N plaquettes) and sign f=eps^(2N)=+1 a.e.

STEP 2, (=>) begins. g!=0 a.e. by Step 0. With A+={g>0}, A-={g<0}, independence gives P(f<0)=2P(A+)P(A-)=0.
So F:=prod_p s(U_p)=sign g equals one delta in {+1,-1} a.e.

STEP 3, cancel the far plaquettes. Fix link l0 with value a; C'=all other links. For a plaquette through l0, rotate
(class function) and invert if a occurs as a^-1 (w(g^-1)=w(g)): s(U_p)=s(a h_i), h_i=word in its other three links.
F=prod_i s(a h_i)*R(C'), R=product over plaquettes missing l0. Fubini: for a.e. (a,a',C') both prod_i s(a h_i)R=delta
and prod_i s(a' h_i)R=delta. Multiply, R^2=1: prod_{i=1..m} Psi(h_i)=1, where Psi(h)=Psi_{a,a'}(h)=s(ah)s(a'h).

STEP 4, staples are independent Haar. By Step 0 each h_i contains a direction-j link b_i, namely (x+e_i,j) or
(x-e_j+e_i,j), lying in no other staple. Given all links of C' except b_1..b_m, h_i=u_i b_i^(+-1) v_i with u_i,v_i
fixed, so (h_1..h_m) is Haar on G^m. At L_j=2 two staples share one direction-i link; the private b_i still give this.
So the Step 3 identity holds for a.e. (a,a',h_1..h_m) in G^(m+2) (measure-preserving map, null preimage => null).

STEP 5, two-point equation. For a.e. (a,a') and a.e. (h_2..h_m): Psi(h_1)=prod_{i>=2}Psi(h_i) for a.e. h_1 (m>=2).
So Psi is a.e. a constant +-1, equal to its integral int s(ah)s(a'h)dh=int s(y)s(a'a^-1 y)dy=rho(a'a^-1) (y=ah).
(a,a')->a'a^-1 pushes Haar to Haar, so |rho(t)|=1 for a.e. t.

STEP 6, homomorphism. t->L_t s is continuous into L^2(G), so rho is continuous; conull sets are dense (Haar has full
support), so |rho|=1 at every t. Cauchy-Schwarz equality with ||s||=||L_t s||=1 gives L_t s=rho(t)s in L^2 for
every t. L_t L_u s=L_{ut}s gives rho(ut)s=rho(u)rho(t)s; s!=0 in L^2, so rho(ut)=rho(u)rho(t) for all u,t.
kappa:=rho is a continuous homomorphism G->{+1,-1}.

STEP 7, identify s. r:=s*kappa has r(ty)=rho(t)s(y)kappa(t)kappa(y)=r(y) for a.e. y, each t. Fubini: for a.e. y,
r(y)=int r(ty)dt=int r=:eps. r=+-1 a.e. gives eps=+-1, so s=eps*kappa a.e. QED.

COROLLARY. G connected: kappa(G) is connected in discrete {+1,-1} and contains 1, so kappa=1, and the claim reads
s=eps a.e., i.e. w has one sign a.e. SU(2) is homeomorphic to S^3, so it is connected.

PENCIL CHECKS, k=2, L=(2,2), abelian G: u_1,u_2,u_3 free, u_4=-(u_1+u_2+u_3). Z/3, s(0)=+1, s(+-1)=-1: u=(0,0,0,0)
gives F=+1, u=(1,1,1,0) gives F=-1. (Z/2)^2, s=-1 only at (1,1): u=0 gives +1, u=((1,0),(0,1),0,(1,1)) gives -1.
FALSIFIER: one (G,w,k,L) meeting the hypotheses with F a.e. constant and s not eps*kappa. Steps 0 and 4 are the
only places lattice geometry enters, so an incidence error there is the first thing to attack.
```

## Where each hypothesis is used

```text
Compact: finite bi-invariant, inversion-invariant Haar (Steps 4-5); s in L^2; full support and continuity of t->L_t s (Step 6).
Second-countable: Borel sets of products are product-measurable, so multiplication is measurable and Fubini applies (Steps 2-5, 7).
k>=2: gives m=2(k-1)>=2, the two factors Step 5 needs. At k=1 there are no plaquettes, g=1, f=1 for every s, and (=>) fails.
L_i>=2: distinct links per plaquette, U_p Haar, exact incidence m, private links b_i (Steps 0, 1, 3, 4).
  Sharpness at L=(1,1): U=[a,b], G=Q8, s=-1 on {+-k} and +1 elsewhere. Commutators are +-1, so F=1 everywhere,
  while s is not eps*kappa because s(i)s(j)=+1 and s(ij)=-1.
Periodic boundary: every link has the same even incidence m, which gives (<=) in Step 1.
Class function: rotates a to the front of each plaquette (Step 3).
w(g^-1)=w(g): turns a^-1 into a (Step 3); it serves (=>).
Measurable: s is measurable, so all a.e. statements and Fubini apply. Bounded: the sign argument leaves it unused.
w!=0 a.e.: s=+-1 a.e., ||s||_2=1, g!=0 a.e. (Step 2), s nonzero in L^2 (Step 6).
Independent slices, f=g(C_0)g(C_m): Step 2, and eps^(2N) in Step 1. With eps=-1 and N odd, g<0 a.e. and f>0 a.e.
Connected G: only in the corollary.
```

## How the homomorphism arises

```text
Input from Step 5: |rho(t)|=1 for a.e. t, where rho(t)=<s,L_t s> is a matrix coefficient of the left regular representation.
(i) rho is continuous on all of G and conull sets are dense, so |rho|=1 at every t. The exceptional set ends here.
(ii) Equality in Cauchy-Schwarz gives L_t s=rho(t)s in L^2 for every t, so the line R*s is invariant under left translation.
(iii) L_{ut}s=L_t L_u s and s!=0 in L^2 give rho(ut)=rho(u)rho(t) for every u,t.
So kappa=rho is continuous and multiplicative everywhere by construction, with no a.e. cocycle left to correct.
(iv) s*kappa is left-invariant in L^2, hence a.e. the constant eps.
Separate theorem needed: none. Tools used: continuity of translation on L^2(G) (C(G) dense, uniform continuity),
Cauchy-Schwarz, Fubini. Automatic continuity of measurable homomorphisms and a.e.-homomorphism rigidity go unused.
```

## What it read

I read no file about this claim. The seat preload required C:/asolaria-acer/claims-gate/AGENT-DISCIPLINE.md and C:/asolaria-acer/claims-gate/GITHUB-3D-VIEWER-BUILD.md; I read both, and they contain general discipline and viewer build instructions with nothing on this claim. The harness auto-injected C:/Users/acer/CLAUDE.md and the MEMORY.md index. The index has one-line pointers to Yang-Mills repositories, gives nothing on this claim, and I opened no topic file. I searched no repository or memory, ran nothing, and did not see the other seat's proof.
