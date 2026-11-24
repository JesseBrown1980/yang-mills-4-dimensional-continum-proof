# YM4 VOL32 — exact original continuous-SU(2) Wilson spherical correlations at beta zero

**24 November 2026 · rigorous original SU(2) Haar benchmark on all 20 VOL30/31 spherical frames.** This is the first exact, numerical-valued *gauge-invariant field-observable* correlation table at the same two-ended 4D lattice shell addresses, rather than only a point-cloud geometric count. The result is for the genuine original SU(2) Wilson model at **\(\beta=0\)**. The production-coupling \(\beta=9^{12}\) correlation values and any continuum mass rate are separate OPEN targets.

## 1. Genuine original four-dimensional Wilson observables

Fix exactly the VOL30 even periodic original lattice \((\mathbb Z/128\mathbb Z)^4\), normalized independent continuous-SU(2) Haar links at \(\beta=0\), and shell centers
\(c=(0,0,0,0)\), \(z=(0,0,24,0)\).
For any integer starting site \(x\), let \(p_x\) be the *positively oriented original spatial 0–1 plaquette* with origin x, and define its true gauge-invariant fundamental Wilson observable
\[
 F_x(U)=\frac{1+\operatorname{Re}(U_{x,0}U_{x+e_0,1}U^{-1}_{x+e_1,0}U^{-1}_{x,1})}{2}.
\]
For each \(R=2,\dots,21\), let \(S_R(c), S_R(z)\) be the exact **site** spheres from VOL30, with
\(N_R=|S_R(c)|=|S_R(z)|\) and \(J_R=|S_R(c)\cap S_R(z)|\).
Define the *actual SU(2) Wilson field observables* averaged over **all sites** of the two shells:
\[
 M_R^c=\frac1{N_R}\sum_{x\in S_R(c)}F_x,\qquad
 M_R^z=\frac1{N_R}\sum_{x\in S_R(z)}F_x.
\]
Every \(x\) is an original 4D integer lattice position; every \(F_x\) is a continuous-Haar SU(2) Wilson trace. Since R<=21 and the centers differ by 24 on an L=128 torus, all starting plaquette addresses are distinct modulo L unless x=y in the **actual shell overlap**. The two shells have the same cardinality by exact coordinate reflection.

## 2. Exact Haar one-point and two-point law, without sampled gauges

At \(\beta=0\) the physical original Wilson law **is precisely product normalized continuous SU(2) Haar**. Each original elementary plaquette holonomy is Haar-distributed because it is a product of independent Haar SU(2) links and inverses. Thus
\[
 E_H[\operatorname{Re}U_{p_x}]=0,\qquad
 E_H[(\operatorname{Re}U_{p_x})^2]=\frac14,\qquad
 E_H[F_x]=\frac12,\quad \mathrm{Var}_H(F_x)=\frac1{16}.
\]
For two *distinct* original plaquettes \(p_x\ne p_y\) of the **same spatial 0–1 orientation**, at least one original positive link occurs only in one plaquette. Haar integration over this unique link kills the product of two fundamental traces exactly. Therefore
\[
 \boxed{\mathrm{Cov}_H(F_x,F_y)=\frac1{16}\mathbf1_{\{x=y\}},}
 \qquad (\beta=0,\ L=128,\ \text{same 0--1 orientation}). \tag{32.1}
\]
This **pairwise orthogonality** does not assert statistical independence of every distinct Wilson plaquette; only the covariance calculation is needed.

Summing (32.1) over the two exact integer sets gives the complete original continuous-SU(2) benchmark:
\[
 \boxed{
 E_H[M_R^c]=E_H[M_R^z]=\frac12,\quad
 \mathrm{Var}_H(M_R^c)=\mathrm{Var}_H(M_R^z)=\frac{1}{16N_R},\quad
 \mathrm{Cov}_H(M_R^c,M_R^z)=\frac{J_R}{16N_R^2},\quad
 \rho_R:=\mathrm{Corr}_H(M_R^c,M_R^z)=\frac{J_R}{N_R}.
 } \tag{32.2}
\]
The constant 1/2 means the **ensemble mean of the Wilson plaquette has no radial band structure at \(\beta=0\)**. The two-ended shell-average **connected covariance** nevertheless follows the exact 4D overlap geometry. This is an original Wilson observable result, but at \(\beta=0\) it measures common plaquette identity, not propagation from a nonzero Yang–Mills coupling.

## 3. A rigorous all-beta control separating geometry from dynamics

For **every** finite \(\beta\ge0\), even L and fixed plaquette orientation, the original periodic Wilson measure is invariant under lattice translations, so
\[
 \boxed{E_{\beta,L}[M_R^c]=E_{\beta,L}[M_R^z]
        =\mu_{01}(\beta,L)\quad\text{for every }R.} \tag{32.3}
\]
This remains true at the production \(\beta=9^{12}\) even though \(\mu_{01}(\beta,L)\) has not been numerically evaluated. A nonflat **ensemble one-point radial mean** in a purported translation-invariant production simulation would therefore signal a sampling, boundary, orientation or implementation problem.

Let \(K_\beta(h)=\operatorname{Cov}_{\beta,L}(F_0,F_h)\) be the genuine connected two-point Wilson plaquette function for original spatial 0–1 plaquettes (h is a four-dimensional lattice displacement). Then, identically for every beta,
\[
 \boxed{
 \mathrm{Cov}_{\beta,L}(M_R^c,M_R^z)
   = \frac1{N_R^2}
      \sum_{x\in S_R(c)}\sum_{y\in S_R(z)}K_\beta(y-x).
 } \tag{32.4}
\]
At beta=0, \(K_0(h)=\delta_{h,0}/16\) and the double sum reduces exactly to \(J_R/(16N_R^2)\). At beta>0 the **off-diagonal displacements \(h\ne0\)** contribute genuine gauge-field dynamical correlations. These are the physical quantities to measure. The fact that a 24-cell appears at R=2/4/8/16 does not by itself establish a dynamical field pattern.

## 4. Exact all-20-frame measurements and reversible geometry controls

The [strict integer verifier](../../tests/ym4_vol32_exact_haar_shell_correlations.py) reconstructs *all* exact original four-dimensional integer shell sites from independent two-square decompositions and checks both two-ended source addresses, all counts from VOL30, and every J_R by a separate three-square enumeration. It then computes the **exact rational** \(1/(16N_R)\), \(J_R/(16N_R^2)\) and \(J_R/N_R\), with no floating-point approximation, and pins the output in [VOL32 HBP](YM4-VOL32-EXACT-HAAR-SPHERICAL-CORRELATIONS-20261124.hbp).

Particularly informative original finite SU(2) results:
- R=12: N=312, J=1, \(\rho_{12}=1/312\); the first exact shared integer site is (0,0,12,0).
- R=13: N=1464, J=30, \(\rho_{13}=5/244\).
- R=16: N=24, J=0, \(\rho_{16}=0\); continuous geometric spheres can overlap while exact-radius integer-shell Wilson averages share no plaquette.
- R=17: N=2456, J=96, \(\rho_{17}=12/307\).
- R=21: N=5928, J=192, \(\rho_{21}=8/247\).

At R=2/4/8/16, the exact 24-cell shell count N=24 yields \(\mathrm{Var}(M_R)=1/384\) even though the Wilson one-point ensemble mean remains 1/2. These recur because of the **sampling count**, a different phenomenon from a nonzero-coupling physical field correlation. The Haar standard deviation is \(1/(4\sqrt{N_R})\), so 24-cell frames have larger typical shell-mean fluctuations than high-count frames.

## 5. Interpretation and next measurement acceptance

**CONFIRMED at the exact continuous-SU(2) Haar reference:** the visual 4D spherical overlap leaves a precise fingerprint in *gauge-invariant Wilson shell-average correlations* \(\rho_R=J_R/N_R\). This is not merely a diagrammatic resemblance. The pattern is an overlap covariance of common physical plaquettes and exists even when the bare coupling is zero.

**UNMEASURED at physical production coupling \(\beta=9^{12}\):** the connected \(K_\beta(h)\) at nonzero separation and hence the actual dynamical shell-average profile. The classical exact translation identity fixes the one-point means only, and VOL29–30 supply rigorous **bounds** on selected time-slice correlations, not actual all-displacement field values. The all-beta connected radial estimator must report and subtract the known diagonal common-site covariance and quantify the off-diagonal connected contribution before attributing any residual to dynamics.

**Next experimental protocol:** independently sample the true original continuous SU(2) Wilson action using detailed-balance single-link updates on accessible small 4D periodic lattices, report thermalization, chain autocorrelation, multiple independent seeds, controls at beta=0, and genuine connected correlator uncertainties. A production L=128, beta=9^12, a→0 continuum numerical study cannot be inferred from those smaller finite-volume samples. The user's strict integer-only mathematical kernel and signed SHA/HBP proof statuses remain separate from any exploratory floating numerical simulation.

The visible 24-cell pattern and five-band signature of VOL31 are classical geometric facts. The new result is their exact placement inside a true original continuous-SU(2) Wilson *two-shell observable* benchmark for all twenty original atlas radii. The eleven continuum construction gates, mass-rate upper decay, beta(a) and nonzero continuum renormalized source remain OPEN.

**Status:** exact beta-zero continuous-SU(2) Haar Wilson shell-covariance mathematical theorem + independent integer enumerator and HBP; actual nonzero-beta Monte Carlo shell measurements **OPEN**; production continuum acceptance **OPEN**. Research candidate on draft PR #113; main and accepted 115-node atlas remain unchanged.


## 6. Hosted exact verifier and independent review

[Dedicated GitHub Actions #45391920783](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45391920783) **PASS**: repository-wide integer-only source gate; independent original 4D shell/three-square geometry enumeration for all 20 radii; exact native-Haar quadratic moment controls; normal and optimized byte-identical frozen HBP; SHA-256 **d421c07b9b509d942a3e20229ea4dd464493ca4e486dd9d6da26f8255fb93397**; and artifact upload. The later [standalone exact Wilson correlation plot](vol32-exact-haar-correlations.html) and the clickable candidate atlas card have a separate hosted link-integrity check in the refreshed workflow.

The [independent-method mathematical audit](../../reviews/YM4-VOL32-EXACT-HAAR-SPHERICAL-CORRELATIONS-AUDIT-20261124.md) checks Haar fundamental orthogonality for **distinct** original spatial plaquettes, all original torus injectivity requirements, exact shared-site covariance, and the separation from VOL30's true conditional source predictor. The [exploratory interacting numerical pilot](NOTE-YM4-VOL32-EXPLORATORY-SU2-HEATBATH-PILOT-20261124.md) reports beta=2 small-volume nearest-slice correlations with limited empirical uncertainty; its floating Monte Carlo is explicitly outside this integer-only mathematical acceptance.

**Review boundary:** The analytic beta-zero Haar group measure is the original full continuous SU(2) theory at that coupling. It is not a nonzero beta=9^12 physical shell measurement, and neither the exact geometry nor the tiny interacting finite-L Monte Carlo pilot proves a continuum mass gap.
