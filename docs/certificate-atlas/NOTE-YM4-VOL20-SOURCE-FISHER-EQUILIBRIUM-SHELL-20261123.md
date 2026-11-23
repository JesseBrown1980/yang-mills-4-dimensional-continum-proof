# YM4 VOL20 — Wilson-source Fisher quotient and equilibrium shell-variance criterion

**23 November 2026 · research candidate · original finite-volume continuous SU(2) Wilson theory.** This note continues VOL15–VOL19 and gives two exact source-normalization-invariant interfaces for the high-coupling physical boundary problem in issue #116. The statements below are finite-volume identities or *conditional* spatial-decay criteria. No high-beta shell contraction or continuum mass gap is asserted.

## 1. Original conditional SU(2) setup

Let `T_h` be all original positive internal links of the centered cube `Q_h={-h,...,h}^4` embedded in an even periodic original Wilson torus of side `L>=2(2h+1)`. Let `J_h` be the boundary-affected interior links identified in VOL15 and write the actual conditional Haar Gibbs law

\[
\mu_B(dU_T)=Z_B^{-1}\exp\{\beta A_{\mathrm{int}}(U_T)+\beta\langle X(U_T),B\rangle\}\,dH_T(U_T),\qquad X=(U_e)_{e\in J_h}\in\mathbb R^{4|J_h|}.
\tag{20.1}
\]

The `B_e` are the original cyclic-order sums of at most three external SU(2) staples. For the interpolation and differentiation argument, allow arbitrary finite real quaternion `B_e`, including convex combinations not realized by a single exterior. The SU(2) links in `X` remain actual continuous unit quaternions, and the interior plaquette action is unchanged. The parameter `beta` in this note is the coefficient of `Re U_p` in the original Wilson action.

Choose a finite vector `Z(U_T)` of bounded **gauge-invariant Wilson source observables**, supported strictly in the centered interior. Set `A_S=sigma(Z)` and `Pi_B=Z_# mu_B`. VOL18 proves the source law is invariant under the left-right cube-site SU(2) action on `B`.

## 2. Exact source-law score and Fisher matrix for every finite beta

Fix a real direction `D` in the boundary-resultant vector space and set `A_D(U_T)=<X(U_T),D>`. Along `B_t=B+tD`, compactness and strictly positive Haar Gibbs densities justify differentiation under the integral. A common dominating reference for source laws is `Pi_0`, because all finite-volume Gibbs measures in (20.1) have strictly positive densities bounded above and below relative to the same finite Haar product. The source-law score is therefore, `Pi_B`-almost surely,

\[
\boxed{\partial_D\log\frac{d\Pi_B}{d\Pi_0}(z)
=\beta\left(\mathbb E_{\mu_B}[A_D\mid Z=z]-\mathbb E_{\mu_B}A_D\right).}
\tag{20.2}
\]

Define `Y_B=E_mu_B[X|A_S]` and `K_{B,S}=Cov_mu_B(Y_B)`, the positive-semidefinite VOL19 matrix. Taking the source-law expectation of the squared score gives the **exact identity**

\[
\boxed{I_{B,S}(D)=\beta^2\,D^\top K_{B,S}D.}
\tag{20.3}
\]

Thus `K` is precisely the source-law Fisher-information quadratic form (divided by `beta^2`), rather than only an upper bound for an individual source covariance. The all-beta VOL18 gauge Ward identity implies `K_{B,S}J_B=0`, so every cube-site gauge-tangent direction is a null direction of this Fisher form. At `beta=0`, the original product Haar law gives `K=0` directly.

**Source normalization invariance.** If `Z' = MZ+c` with any invertible finite real matrix `M` and deterministic `c`, then `sigma(Z')=sigma(Z)` and therefore `K_{B,S}` and `I_{B,S}` are exactly unchanged at every finite beta. This includes any nonzero finite-lattice multiplicative renormalization or additive subtraction of a Wilson source. More generally, replacing `Z` by a measurable function of `Z` decreases `K` in positive-semidefinite order by the conditional-expectation projection theorem. Consequently bare source amplitude collapse is not a substitute for small *source-law* Fisher information.

For any piecewise `C^1` curve of resultant parameters `B_t`, the square-root densities of the source laws obey

\[
\left\|\partial_t\sqrt{d\Pi_{B_t}/d\Pi_0}\right\|_{L^2(\Pi_0)}
=\tfrac12\sqrt{I_{B_t,S}(\dot B_t)}.
\]

Hence, using the Hellinger path length and the total-variation bound,

\[
\boxed{\|\Pi_{B_1}-\Pi_{B_0}\|_{\rm TV}
\le \min\left\{1,\frac\beta2\int_0^1
\sqrt{\dot B_t^\top K_{B_t,S}\dot B_t}\,dt\right\}.}
\tag{20.4}
\]

Optimizing over paths and over admissible cube-site gauges gives a **source-law metric on boundary-resultant gauge orbits**; the metric may have additional zero directions when the source law cannot distinguish the corresponding boundary parameters. The straight, gauge-aligned path recovers VOL19's bound but (20.4) controls the *entire joint source law*, not just the expectation of one `F`.

Equation (20.4) is an exact sensitivity theorem. It supplies no uniform decay with source-to-boundary distance until its Fisher length is bounded at the tuned `beta(a)`.

## 3. An original-Gibbs equilibrium route that bypasses interpolated exteriors

Let `mu=mu_{beta,L}` be the original **periodic** full Wilson measure. For a centered source `F=f(Z)` in `L^2(mu)`, let `E_h=sigma(eta_h)` be the full exterior-link sigma-algebra outside `T_h`, and `lambda_h` its true Gibbs marginal. The Gibbs Markov property and VOL15's boundary sufficient statistics give

\[
M_h(\eta_h):=\mathbb E_\mu[F\mid E_h](\eta_h)
=\Phi_F(B(\eta_h)).
\tag{20.5}
\]

Take two **independent actual Gibbs exteriors** `eta_h,eta_h'` drawn from `lambda_h`. Elementary replica algebra gives the exact, unconditional identity

\[
\boxed{\mathbb E_{\lambda_h\otimes\lambda_h}
|\Phi_F(B(\eta_h))-\Phi_F(B(\eta_h'))|^2
=2\,\operatorname{Var}_\mu(M_h).}
\tag{20.6}
\]

There are no artificial intermediate boundary fields in (20.6). Every conditional expectation is under an actual Gibbs exterior, and global winding holonomies can be retained in the full exterior sigma-algebra. This is an *observable-specific equilibrium comparison*, not a theorem about arbitrary-boundary uniform mixing.

Define the normalized exterior predictability of every nonconstant source `F` by

\[
\boxed{\Gamma_h(F):=
\frac{\operatorname{Var}_\mu(\mathbb E[F\mid E_h])}
{\operatorname{Var}_\mu(F)}\in[0,1].}
\tag{20.7}
\]

This ratio is invariant under **all nonzero affine source renormalizations**. For any exterior `G in L^2(E_h)`, conditional expectation and Cauchy–Schwarz give the physical, amplitude-normalized covariance inequality

\[
\boxed{\frac{|\operatorname{Cov}_\mu(F,G)|}
{\sqrt{\operatorname{Var}_\mu(F)\operatorname{Var}_\mu(G)}}
\le\sqrt{\Gamma_h(F)}.}
\tag{20.8}
\]

For the full source algebra, define `Lambda_h(S)=sup_{F in L^2(A_S), Var(F)>0} Gamma_h(F)`. It is the squared operator norm of the conditional-expectation map from centered source functions to exterior functions and is again invariant under invertible linear reparametrization of the source observables. Uniform physical-source mixing would follow from a bound such as `Lambda_h(S) <= C exp[-2m a(h-r0)]` with constants compatible with the original continuum source and transfer requirements.

## 4. Exact shell-variance identity and a sufficient *physical* decay gate

For integers `r>=r0`, let `T_r` be the internal links of the centered cube `Q_r` and let `E_r=sigma(links outside T_r)`. The sigma-algebras are nested: `E_{r+1} subset E_r`. For any `F` supported inside `T_{r0}`, write `M_r=E_mu[F|E_r]` and `V_r=Var_mu(M_r)`. The tower property plus orthogonality of conditional expectation prove the exact identity

\[
\boxed{V_r-V_{r+1}=
\mathbb E_\mu\!\left[(M_r-M_{r+1})^2\right]\ge0.}
\tag{20.9}
\]

For `V_r>0`, put `kappa_r(F)=(V_r-V_{r+1})/V_r in [0,1]`. With zero variance all later variances also vanish. For positive values, (20.9) gives the exact product

\[
\boxed{\Gamma_h(F)=\Gamma_{r0}(F)
\prod_{r=r0}^{h-1}(1-\kappa_r(F)).}
\tag{20.10}
\]

**Sufficient continuum-distance acceptance:** on a trajectory `beta=beta(a)`, for a fixed positive physical mass `m` and every shell in the chosen physical collar, prove

\[
\kappa_r(F)\ge 1-e^{-2ma},
\tag{20.11}
\]

uniformly over required volumes, source families, and sectors (or prove the corresponding summed logarithmic criterion). Then (20.8)–(20.10) yield

\[
\boxed{\frac{|\operatorname{Cov}_\mu(F,G)|}
{\sqrt{\operatorname{Var}_\mu(F)\operatorname{Var}_\mu(G)}}
\le e^{-ma(h-r0)}}
\tag{20.12}
\]

for every exterior `G` with nonzero variance. Here `a(h-r0)` is an actual source-to-boundary physical distance. Equation (20.11) is a **hypothesis to certify**, rather than a result inferred from VOL12 bad-star rarity or VOL18 Ward-null directions. The stronger version uniform over source functions is the required input for `Lambda_h(S)`; a fixed `F` yields only its own covariance estimate.

The per-shell requirement is quantitatively mild in the continuum scaling sense (`1-e^{-2ma}` approaches `2ma` as `a` decreases), but proving any positive lower bound for `kappa_r` along high-beta 4D Wilson measures requires controlling how much local Wilson information is lost across each physical shell. The project has not established that lower bound.

## 5. Independent strict integer-pair control and adverse checks

The verifier `tests/ym4_vol20_source_fisher_shell.py` is a **16-atom abstract exact-rational integer-pair probability-space control**, deliberately separate from a native continuous-SU(2) numerical integration. It constructs two nested exterior bits, a binary source, and an independent nuisance sign. Its exact results are:

- The source-projected score Fisher quadratic form is `4/63`, compared with the raw score variance `5/4`. The nuisance direction has raw variance `1` and projected source Fisher variance `0`. This tests the algebraic Ward-null mechanism, not an SU(2) Ward theorem.
- Invertible source rescaling by `1000` leaves the projected Fisher value unchanged. Source coarsening decreases projected information; adding an observed source feature increases it.
- For the original toy source, `Var(F)=63/256`, `V_near=5/256`, `V_far=1/64`, and the shell drop is `1/256`. The exact relative loss is `kappa=1/5`. The independent two-replica mean-square difference is `5/128=2V_near`.
- The exact normalized predictability is `Gamma_near=5/63` and `Gamma_far=4/63`, even after `F -> 17+1000F`. Thus shrinking or inflating the raw source amplitude cannot manufacture the physical mixing criterion.

The fixture uses integer numerator/denominator pairs with exact integer cross-products for all calculations, and tests both variance projection and sharp source Cauchy–Schwarz equality. It also has a strict no-floating-point and optimized-replay gate. A successful fixture cannot certify (20.11) for the 4D SU(2) measure; that remains a separate analytic or rigorously enclosed computational task.

## 6. Next accepted research workflow and safeguards

1. **Physical source:** specify one contractible Wilson source family `Z_a` (and its actual renormalization) with a nondegenerate continuum observable target, plus a separate winding-sector inventory.
2. **First actual 4D pilot:** quantify `V_r` and `V_{r+1}` for an original SU(2) periodic Gibbs measure at explicitly stated finite `beta,L,r`. A sample covariance or a Monte Carlo estimate alone is evidence, not a rigorous lower bound on `kappa_r`.
3. **Mathematical certificate:** obtain a rigorous lower bound on shell loss, or a direct upper bound on the source Fisher length along the *physical* scaling path, with independent control of the probability of problematic exteriors. The native pushed-forward joint block law and all Gauss sectors need their own checks.
4. **Acceptance:** insert only a proved spatial-decay bound into the VOL07 transfer/reconstruction criterion, with the original eleven continuum construction requirements reviewed individually.

**Status:** (20.2)–(20.10) exact finite-volume analytic identities; (20.11)–(20.12) valid conditional sufficient implication; native SU(2) high-beta shell-loss lower bound OPEN; 4D all-sector physical mass gap and eleven continuum gates OPEN. The candidate note, exact rational fixture, expected-output HBP and workflow belong on draft PR #113 and in its staged source map. Production 3D atlas and `main` remain unchanged.