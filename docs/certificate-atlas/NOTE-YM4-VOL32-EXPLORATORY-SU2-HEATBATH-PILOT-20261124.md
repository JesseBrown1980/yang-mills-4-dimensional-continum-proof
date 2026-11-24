# YM4 VOL32 pilot — actual interacting continuous-SU(2) Wilson heat bath on small 4D tori

**24 November 2026 · exploratory numerical evidence, separate from exact integer certificates.**

## Model and exact local heat bath

The pilot samples the actual original untwisted periodic 4D SU(2) Wilson Gibbs action \(e^{\beta\sum_p \operatorname{Re}U_p} dH_{SU(2)}(U)\) on L=4 and L=6 lattices. Each original link enters six Wilson plaquettes. The one-link heat bath is drawn from its exact continuous-Haar conditional density \(\exp(\beta\, u\cdot H_e)dH_{S^3}(u)\). The scalar \(t=u\cdot H_e/\|H_e\|\) is sampled from the truncated exponential proposal and accepted with probability \(\sqrt{1-t^2}\); the remaining direction is uniform on a transverse S². At beta zero, links are sampled independently from normalized SU(2) Haar.

The implementation independently verified: (a) its six-staple quaternion vector reconstructs the full exact original local plaquette action difference to absolute error less than \(10^{-11}\) on tested random noncommuting configurations; (b) local site-gauge transformations leave every tested Wilson plaquette trace invariant to less than \(10^{-11}\); (c) the zero-beta numerical means, variances and disjoint-plaquette correlations agree with the exact original Haar benchmark within pilot fluctuations.

Measurements are averaged over **all spatial 0–1 plaquettes** and their translations in original time direction 2. Let \(p_x=\operatorname{Re}U_{p_x}\) and \(C_d=E[\operatorname{avg}_x(p_xp_{x+de_2})]-(E p)^2\). For the centered physical \(F=(1+p)/2\), \(C_d(F)=C_d(p)/4\), and the **normalized \(C_d/C_0\) is unchanged**.

## Finished pilot samples

| L | β | 3 independent seeds | configs per seed | warmup sweeps | thinning | mean Re(plaquette), all orientations | C₀(Re 01) | C₁(Re 01) | C₁/C₀ | tentative 95% t halfwidth on C₁ |
|---:|---:|:---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0 | 1081,2017,3041 | 85 | 60 | 2 | -0.000635529 | 0.249794997 | -0.000370178 | -0.001481928 | 0.000757662 |
| 4 | 1 | 1081,2017,3041 | 85 | 60 | 2 | 0.241798011 | 0.222160152 | 0.000715274 | 0.003219633 | 0.003871994 |
| 4 | 2 | 1081,2017,3041 | 85 | 60 | 2 | 0.503462283 | 0.135278576 | 0.004093780 | 0.030261849 | 0.001130385 |
| 6 | 2 | 1091,2027,3067 | 100 | 100 | 3 | 0.500940294 | 0.135426851 | 0.003743612 | 0.027643053 | 0.001000793 |

The reported halfwidth uses only **three** independent seed-specific connected-correlation means and a Student-t multiplier with two degrees of freedom. This is a descriptive approximation, not a rigorous statistical confidence certificate. The underlying chains have within-chain serial dependence. Thermalization, autocorrelation, finite-volume bias, and double-precision numerical errors require further review. The beta=1 L4 C₁ is inconclusive against its pilot uncertainty; the beta=2 values on L4 and L6 are positive exploratory measurements.

## Exact provenance of completed artifacts

- Experimental local source file ym4_vol32_su2_monte_carlo_pilot.py SHA-256: 90bd3278d2d790fd7394577b9b830f6292f985b713c3fbda318bf856f8524180.
- Completed raw L4 CSV, 765 configurations, SHA-256: f87a6546d457c5aa75c60670be0e2e32d4e96c65b7ba235ddd2ba936c8766869.
- Completed raw L6 beta2 CSV, 300 configurations, SHA-256: fef4ed7ce34c5b8983a4382b224d55e1b18ec74933cdea18c11991e752c0950c.
- A later larger L6 run exceeded execution limits while processing beta2. The incomplete extension is **excluded** from all acceptance evidence.

The float-based experimental source and complete raw samples are supplied as downloadable conversation artifacts rather than tracked Python inside this repository, preserving the project's **integer-only exact mathematical verification gate**. Their reproducibility is described here, and their SHA values prevent confusion with a later run.

## Scope and next step

The [VOL32 mathematical certificate](NOTE-YM4-VOL32-EXACT-HAAR-SHELL-CORRELATIONS-20261124.md) proves exact continuous-SU2 beta-zero correlations on the **same full original L128 spherical frames**. This numerical pilot instead measures nonzero-coupling connected Wilson plaquette correlations on smaller L4/L6 tori; it does **not** populate nonzero-beta L128 spherical field values. No beta=9^12 field covariance or physical continuum mass-rate data are asserted.

A future true production spherical simulation must sample all relevant original periodic Wilson links at nonzero coupling, establish equilibrium and mixing, measure connected radial covariances and uncertainties, subtract the common-site overlap baseline, and obtain independent physical validation. Eleven continuum construction obligations remain OPEN.

**Verdict:** informative but provisional interacting small-volume numerical evidence. Not a mathematical proof, physical production certificate, or continuum limit.
