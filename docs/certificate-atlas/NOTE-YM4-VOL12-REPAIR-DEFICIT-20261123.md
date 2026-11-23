# YM4-VOL12 local repair-deficit theorem — original continuous SU(2) Wilson packets

**23 November 2026 — analytic conditional theorem, original continuous Haar; independent mathematical referee OPEN.** Companion to the [unconditional finite-volume pilot](NOTE-YM4-VOL12-FINITE-PACKET-PILOT-20261123.md). This local comparison isolates the exact exterior frustration quantity which must be controlled to obtain a volume-uniform bad-island activity. The unconditional input for VOL10 and all 11 continuum obligations remain OPEN.

## 1. Gauge-invariant packet geometry

Use the original periodic 4D Wilson measure from VOL09–VOL11: beta>=1, positive original links and all four-edge plaquettes, W_p=halftrace U_p. Choose r original positive links S with no shared incident plaquette. For each e in S, include e and the other links of all six incident plaquettes. Call their union T. The original degree-18 link graph gives

- n=|T| <= 19r original links;
- P(T) = the set of original Wilson plaquettes touching at least one link in T; M=|P(T)| <= 6n <= 114r;
- every bad-star event B_e is measurable from U_T alone, and bad stars in S force r **distinct** plaquette deficits greater than epsilon/4 within P(T).

No assumption that the patches surrounding different e are disjoint is needed beyond no *shared incident plaquette*. Their expanded T sets are allowed to overlap.

Fix any exterior links b=U_(T^c). Define the **gauge-invariant local repair deficit**

\[
D_T(b)=M-\max_{u_T\in\mathrm{SU}(2)^T}
   \sum_{p\in P(T)}W_p(u_T,b)\in[0,2M].
\]

The maximum exists by compactness. It quantifies the best local Wilson completion compatible with the actual exterior; D=0 exactly when all touched plaquettes can be made flat. The supremum is invariant under the induced endpoint gauge action on b.

## 2. Boundary-conditional SU(2) variational Haar-cap lemma

Let u_T^* maximize the touched-plaquette action for the fixed exterior. Place each original interior link within SU(2) geodesic distance a=1/(4 beta) of its respective u_e^*. Normalized continuous Haar mass per cap is at least a^3/24=1/(1536 beta^3), by the VOL09 cap inequality (a<=1/4).

Every touched original plaquette changes at most four links; bi-invariance and the triangle inequality bound the holonomy geodesic displacement by 4a<=1/beta. Since W=cos(theta) is 1-Lipschitz in the geodesic angle, the touched-plaquette Wilson action drops by at most M/beta. Thus the **local conditional partition function** satisfies

\[
Z_T(b)\ge
(1536\beta^3)^{-n}
\exp\{\beta[M-D_T(b)]-M\}.
\tag{12.3}
\]

On E_S = all r selected bad stars, r distinct touched plaquettes have W_p<1-epsilon/4, and every other W_p<=1. The constrained numerator is at most exp{beta(M-r epsilon/4)}. Division gives the rigorous **arbitrary-exterior inequality**

\[
\boxed{\mu_{\beta,L}(E_S\mid U_{T^c}=b)
\le\min\{1,(1536\beta^3)^n
\exp[M-\beta(r\epsilon/4-D_T(b))]\}.}
\tag{12.4}
\]

There is no worst-case-mixing assumption: the bound displays the exact boundary penalty D_T(b).

## 3. Conditional local exponential packet activity

If D_T(b)<=r epsilon/8, then M<=6n and e<3 imply

\[
\mu_{\beta,L}(E_S\mid b)
\le [729\cdot1536\beta^3]^{19r}
e^{-\beta r\epsilon/8}.
\tag{12.5}
\]

For epsilon=1/16, beta=9^k, define the exact-rational rate

\[
\rho_k=\min\left\{1,\frac{(729\cdot1536\cdot9^{3k})^{19}}
{2^{\lfloor9^k/256\rfloor}}\right\}.
\tag{12.6}
\]

Using e^2>2, floor(rx)>=r floor(x), and (12.5),

\[
\boxed{\mu_{9^k,L}(E_S\ \cap\ \{D_T(U_{T^c})\le r/128\})
\le\rho_k^r.}
\tag{12.7}
\]

The condition is a **local boundary repair cost**, not the earlier VOL11 individual good-star exterior event. This joint good-boundary result holds for every periodic L>=3 and every plaquette-separated S. At k=7, beta=4,782,969, the integer base (729*1536*beta^3) has 87 bits and

\[
\rho_7<2^{-17030}<18^{-57}.
\]

Thus the VOL10 numerical threshold is met **inside this explicitly restricted repairable-exterior sector**. The full original Gibbs bad-island theorem still requires a bound on the complementary repair-deficit event.

## 4. Actual original Gibbs contamination and its present cost

Taking the original Gibbs expectation over exterior b yields

\[
\boxed{\mu(E_S)\le\rho_k^r+
\mu[D_T(U_{T^c})>r\epsilon/8].}\tag{12.8}
\]

For any sampled interior u_T, its touched plaquette action is no greater than the maximum, so configuration-wise

\[
D_T(U_{T^c})\le\sum_{p\in P(T)}(1-W_p(U)).
\]

Using periodic equilibrium translation/rotation symmetry, VOL09's mean plaquette deficit R(beta), and M<=114r, Markov gives

\[
\boxed{\mu[D_T>r\epsilon/8]
\le\min\{1,912R(\beta)/\epsilon\}.}\tag{12.9}
\]

At epsilon=1/16 and beta=9^7, the exact rational allowance is 783104/4782969 (~0.164). Its lack of decay with r is the **remaining joint bad-boundary obstacle**. This one-point/first-moment estimate is weaker than the existing VOL11 marginal, so the best unconditional bound should take the minimum of all available estimates.

## 5. Verification and acceptance boundary

The integer-only [repair checker](../../tests/ym4_su2_vol12_repair_packet.py) rebuilds the original L=3,4 packet supports, verifies 19r and 114r geometry, reproduces the 87-bit base, checks rho threshold using exact arithmetic, freezes [HBP](YM4-VOL12-REPAIR-PACKET-20261123.hbp), and rejects extending the conditional activity to unconditional cluster control.

- **Analytic local theorem:** (12.3)–(12.9), continuous SU2 Haar. Independent external proof review OPEN.
- **Exact integer replay:** local; hosted CI PENDING.
- **Original unconditioned independent-star rho:** OPEN; requires quantitative joint tail of D_T for growing packets (or an equivalent multiscale block condition).
- **Physical-size cube / all-sector Wilson transfer / 11 continuum construction gates:** OPEN.

The next independent acceptance target is a **joint repair-deficit tail** under the original Gibbs distribution, with scale-dependent blocks and exterior geometry. Source comparison: [Bhattacharjee et al. v7](https://hexagonmath.org/2610.00341v7) develops averaged block conditions and bad-block clusters. No first-in-literature priority claim is made.
