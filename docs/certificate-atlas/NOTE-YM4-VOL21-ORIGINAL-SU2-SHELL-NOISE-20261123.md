# YM4 VOL21 — original SU(2) Wilson shell-noise floor and explicit boundary statistic census

**23 November 2026 · candidate research theorem.** Mathematical continuation of VOL15–VOL20 on the **actual original continuous-SU(2) Wilson Gibbs measure** on an untwisted even four-dimensional periodic lattice. This proves a strictly positive one-shell conditional-variance loss for every finite Wilson coupling, with an explicit lattice-size-independent constant. The bound is exponentially small in the shell surface area and bare coupling, so it does **not** meet the physical-distance, continuum-uniform mass-rate criterion of VOL20.

## 1. Centered original link sets and the precise shell carrying the resultant

For integer `r>=1`, set `Q_r=[-r,r]^4`, `b=2r+1>=3`, and let `T_r` be all original positively directed SU(2) links whose two endpoints belong to `Q_r`. Embed `Q_(r+1)` without wrapping collisions in an even periodic torus of side `L>=2(b+2)`. The exact number of internal links is `|T_r|=4(b-1)b^3`.

VOL15 proves the conditional interior Wilson law depends on its entire exterior solely through the cyclically ordered quaternion boundary resultants `B_r`, one per boundary-affected internal link. Each mixed original elementary plaquette contains **exactly one** link of `T_r`; its other three links are outside `T_r` but **all inside** `T_(r+1)`. Define `R_r` as the union of these exterior three-link supports over all mixed plaquettes. Therefore

`R_r subset T_(r+1) \ T_r` and `B_r` is measurable with respect to `sigma(U_e: e in R_r)`.

This is a concrete one-lattice-step **boundary-statistic factorization**, not an artificially chosen spatial weight. As in VOL20, for any bounded gauge-invariant original Wilson source `F` supported in `T_r`, the original Gibbs conditional expectation is

`M_r := E_mu[F | E_r] = Phi_F(B_r) = f_r(U_Rr)`, where `E_r=sigma(U_e: e outside T_r)`.

Since `R_r subset T_(r+1)`, the random vector `U_Rr` is disjoint from `E_(r+1)`.

## 2. Exact census of the original 4D boundary support and its touching plaquettes

Every positive link of `R_r` belongs to **exactly one of two geometric classes**:

* **Radial crossing link:** its base coordinate in its positive direction `mu` is either `-r-1` or `r`, and each of its other three coordinates is in `[-r,r]`. There are `8b^3` such links (four directions, two sides, `b^3` transverse choices).
* **Parallel outer-face link:** its positive base coordinate along `mu` is in `[-r,r-1]`, exactly one of the other three coordinates is `+(r+1)` or `-(r+1)`, and the remaining two are in `[-r,r]`. There are `24(b-1)b^2` such links.

Consequently the exact resultant support cardinality is

`|R_r| = 8b^3 + 24(b-1)b^2 = 8b^2(4b-3)`. **(21.1)**

Let `P(R_r)` be the set of original unoriented elementary Wilson plaquettes containing at least one link of `R_r`. Its number is **exactly**

`N_r := |P(R_r)| = 24b(3b^2+b-3)`. **(21.2)**

Here is an explicit counting derivation. Fix one of the six coordinate-plane orientations `(mu,nu)` and classify the remaining two transverse coordinates. If both lie in `[-r,r]`, there are `b^2` choices; the plane's original plaquette bases touching `R_r` form two four-sided boundary strips containing `8b-4` sites. If exactly one transverse coordinate equals `+(r+1)` or `-(r+1)` and the other lies in `[-r,r]`, there are `4b` choices, each with `(b-1)(b+3)` admissible bases in the `(mu,nu)` plane. If both transverse coordinates are outside `[-r,r]`, no original plaquette of that orientation contains `R_r`. The count for one orientation is therefore `b^2(8b-4)+4b(b-1)(b+3)=4b(3b^2+b-3)`. Multiply by six orientations to obtain (21.2). The enumeration verifier checks all four links on every original face, not an abstract adjacency approximation.

## 3. A continuous-SU(2) Gibbs conditional density minorization, for *all finite beta*

Let `mu_(beta,L)` be the full original SU(2) Wilson Gibbs measure with normalized Haar product reference and action `beta * sum_p Re U_p`; allow any finite `beta>=0`. Condition on every link **outside** `R_r`. Only the `N_r` original plaquettes in `P(R_r)` depend on the links `U_Rr`, and each has `Re U_p` in `[-1,1]`. Writing `H_R` for independent normalized continuous SU(2) Haar measure over `R_r`, the exact original conditional density obeys, for every fixed complement configuration,

`exp(-2*beta*N_r) <= d mu(U_Rr | U_(Rr)^c) / dH_R <= exp(2*beta*N_r)`. **(21.3)**

This uses the complete noncommutative original Wilson action; no independent-plaquette approximation, good-star assumption, chessboard estimate, gauge choice, or finite Q8 counting model appears in the analytic bound. By conditional expectation, the same density envelopes hold for `mu(U_Rr | E_(r+1))` and for the unconditional `mu(U_Rr)`, because `E_(r+1)` is a sub-sigma-field of the complement of `R_r`.

Taking the quotient of these two positive densities gives the pointwise measure domination

`mu(dU_Rr | E_(r+1)) >= exp(-4*beta*N_r) * mu(dU_Rr)` **(21.4)**

for almost every exterior, as measures on the complete original continuous-SU(2) shell-support configuration space. The factor is **independent of the overall periodic torus size L**.

## 4. Rigorous positive source information loss per shell

For any square-integrable `f(U_Rr)` the variational formula for variance, `Var_P(f)=inf_c E_P[(f-c)^2]`, and (21.4) imply

`Var_mu(f(U_Rr) | E_(r+1)) >= exp(-4*beta*N_r) Var_mu(f(U_Rr))` **(21.5)**

for almost every exterior. Apply this with the **actual** Gibbs-conditioned Wilson-source predictor `f=M_r=Phi_F(B_r)`. From VOL20's tower identity,

`V_r - V_(r+1) = E_mu[ Var_mu(M_r | E_(r+1)) ]`, where `V_r=Var_mu(M_r)`.

Hence for **every** gauge-invariant Wilson source `F in L^2(sigma(T_r))` with `V_r>0`, the actual original periodic continuous-SU(2) Wilson Gibbs law satisfies the strict finite-coupling theorem

`boxed: kappa_r(F) := (V_r-V_(r+1))/V_r >= exp(-4*beta*N_r) > 0`, **(21.6)**

uniformly over even `L>=2(b+2)`. Equivalently the source-to-exterior conditional-expectation operator, restricted to the source-generated range and normalized in variance, has per-shell squared contraction norm at most `1-exp(-4*beta*N_r)`.

At the production integer `beta=9^12=282429536481`, the elementary analytic inequality `e<3` supplies an integer-only, conservative strict certificate:

`kappa_r(F) > 3^(-4*beta*N_r)` **(21.7)**.

The estimate also holds for any centered source supported in an earlier inner cube, because that source remains measurable in `T_r`. For zero `V_r`, all later `V` also vanish and no division is needed.

### Quantitative original-geometry checks

| radius r | side b | boundary-support links `|R_r|` | touching plaquettes `N_r` | exact exponent `4*(9^12)*N_r` |
|---:|---:|---:|---:|---:|
| 1 | 3 | 648 | 1,944 | 2,196,172,075,676,256 |
| 2 | 5 | 3,400 | 9,240 | 10,438,595,668,337,760 |
| 3 | 7 | 9,800 | 25,368 | 28,658,689,925,800,032 |
| 4 | 9 | 21,384 | 53,784 | 60,760,760,760,376,416 |

These are **exponents in a proven lower bound**, not observed mixing rates. They quantify the present estimate's enormous loss of strength at high beta.

## 4A. Exact consecutive-boundary Markov transfer on original Gibbs resultants

The one-shell support observation also removes the arbitrary-exterior interpolation from the **actual transfer operator**. Let `lambda_r=(B_r)_#mu` be the genuine original Gibbs marginal of the finite-dimensional boundary-resultant field. For each outer resultant `b'=B_(r+1)`, define a transition kernel `K_r(b',db)` as follows: sample all original internal links `U_(T_(r+1))` from the true conditional Wilson Haar law `mu_(T_(r+1))^(b')`, then calculate the inner boundary-resultant `B_r` from its genuine three-link exterior staples on `R_r subset T_(r+1)`. VOL15's sufficient-statistic factorization ensures this conditional pushforward depends only on `b'`, not on any further exterior details. Thus

`lambda_r(db) = integral K_r(b',db) lambda_(r+1)(db')` **(21.9)**.

For every inner Wilson source `F`, set `phi_r(b)=E[F|B_r=b]`. The tower property gives the exact, original-periodic-Gibbs transfer

`phi_(r+1)(b') = integral phi_r(b) K_r(b',db)` **(21.10)**.

Consequently the shell variance loss can be evaluated **entirely on consecutive boundary-resultant distributions**:

`V_r-V_(r+1) = integral Var_(K_r(b',.))(phi_r) lambda_(r+1)(db')`. **(21.11)**

The operator `(T_r f)(b')=integral f(b)K_r(b',db)` maps `L^2_0(lambda_r)` to `L^2_0(lambda_(r+1))`. By the same continuous-Haar minorization (21.4), for **every** centered square-integrable `f` on the actual boundary-resultant space,

`||T_r f||²_(lambda_(r+1)) <= [1-exp(-4*beta*N_r)] ||f||²_(lambda_r)`. **(21.12)**

This is a strict finite-beta strong-data-processing (maximal-correlation) inequality for the **original Wilson boundary-statistic transfer**, not a raw single-link total-variation Dobrushin assertion. It retains all simultaneous noncommutative cycle information of VOL19, and gauge-invariant source functions descend to the appropriate orbit quotient. The numerical bound on the full operator norm remains weak at high beta. The next task is to certify a substantially sharper norm on the **source-generated invariant subspace** along the physical scaling path, without bounding unrelated high-frequency boundary functions.

## 5. What the bound establishes and the genuinely next physical target

Combining (21.6) with VOL20 yields the actual original-SU(2) finite-collar inequality

`V_h <= V_(r0) * product_(r=r0)^(h-1) [1-exp(-4*beta*N_r)]` **(21.8)**

whenever all cubes through `h` fit inside the periodic lattice. This is an unconditional finite-volume inequality for the **original** Wilson Gibbs law and all interior source functions, rather than a toy probability space or hypothetical coupling.

The bound's weakness is precise: `N_r=O(r^3)` and the bare coupling is large. The conservative shell-loss lower bound decays like `exp(-constant*beta*r^3)` as the buffer radius grows, whereas the physical criterion (VOL20 20.11) asks for loss of order `1-exp(-2ma)` in shells spanning a fixed physical distance. Equation (21.6) therefore certifies strict finite-beta shell information loss but cannot yield a positive physical mass rate, continuum uniformity, or infinite-volume clustering from this envelope alone. For fixed beta, the sum of these lower-bound rates over unbounded r is finite; the corresponding infinite product need not tend to zero.

**Next acceptance:** replace the worst-action Haar density ratio across all `N_r` touching plaquettes by a **source-restricted, gauge-covariant local shell transfer inequality**: certify a lower bound on the Dirichlet/variance loss for `M_r=Phi_F(B_r)` that is uniform in boundary surface area and scales at least as `1-exp(-2ma)` along `beta(a)`. Good-star activity, center/winding holonomy, and interfacial frustration must be controlled under the actual conditional shell laws, rather than silently imported from periodic equilibrium or the VOL15 linear interpolation. All eleven 4D continuum construction gates, all-Gauss-sector transfer, and nonzero continuum source construction remain OPEN.

## 6. Verifier and acceptance boundary

The strict integer-only verifier `tests/ym4_vol21_original_su2_shell_noise.py` independently reconstructs original 4D positive links, all mixed Wilson plaquettes, the three exterior staples of each mixed face, the exact `R_r` classification, the touching-plaquette set, six orientation counts, and a no-wrap embedding in an even periodic torus for `r=1,2,3,4`. It checks (21.1)–(21.2) and exact integer production exponents in (21.7), with normal/optimized byte-identical expected receipt `YM4-VOL21-ORIGINAL-SHELL-NOISE-20261123.hbp`.

The continuous-SU(2) Haar Gibbs density/conditional variance steps (21.3)–(21.6) are analytic and apply at every finite beta. The integer geometry and exponent checker is an independent falsifier of their original-lattice inputs, not a formal Lean kernel proof or numerical high-beta mixing measurement. **Dedicated hosted acceptance PASS:** [original SU2 shell-noise workflow #45234976698](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45234976698) completed successfully, including the repository-wide no-float audit, original 4D geometry census at radii 1–4, normal/optimized byte-identical replay, frozen HBP SHA-256 `5c69d67fe8ff22f8f3509c3177c52c2579c7bd6b66d9214afa8939b6d7b435be`, and artifact upload. The continuous-SU(2) density and conditional-variance theorem is analytic and remains separate from this exact-integer hosted falsifier. This certificate is staged on draft PR #113 and the research candidate map; production 3D atlas and `main` are unchanged.
