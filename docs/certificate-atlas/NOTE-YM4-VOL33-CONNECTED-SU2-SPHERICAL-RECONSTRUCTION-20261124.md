# YM4 VOL33 — measured connected Wilson two-point function and spherical diagonal-subtracted reconstruction

**24 November 2026 · original continuous-SU(2) Wilson gauge model · research candidate.** This stage implements the request to measure a *connected (contracted)* original Wilson two-point function at nonzero separations and then reconstruct spherical correlations by separately subtracting their **same-plaquette contribution**. It provides a mathematically exact integer contraction/geometry certificate and a separately marked **exploratory floating numerical** interacting SU(2) measurement on an accessible finite torus. The production L=128 original spherical atlas geometry and beta=9^12 physical shell values remain OPEN.

## 1. New exact decomposition, valid at any coupling

Let \(P_x=\operatorname{Re}U_{p_x}\) be the original genuine gauge-invariant continuous-SU(2) **spatial 0–1** Wilson plaquette trace at 4D lattice site x. For any original even periodic L, beta and time-translation-invariant Wilson Gibbs measure, let
\[
 \mu_\beta=E_{\beta,L}P_x,\quad
 K_\beta(h)=E_{\beta,L}[P_xP_{x+h}]-\mu_\beta^2,\quad
 K_\beta(0)=\operatorname{Var}_{\beta,L}P_x.
\]
For two translated original integer site shells \(A,B\subset(\mathbb Z/L\mathbb Z)^4\), both of size N, define their original plaquette averages \(M_A=N^{-1}\sum_{x\in A}P_x\) and \(M_B=N^{-1}\sum_{y\in B}P_y\). Define the **exact integer pair-displacement histogram**
\[
 H_{A,B}(h)=|\{(x,y)\in A\times B:y-x=h\bmod L\}|,\quad
 \sum_hH(h)=N^2,\quad J=H(0)=|A\cap B|.
\]
Translation invariance yields the **two independently computable, exactly equal** representations
\[
 \boxed{\operatorname{Cov}(M_A,M_B)
   =\frac1{N^2}\sum_hH(h)K_\beta(h)
   =\frac{J}{N^2}K_\beta(0)
    +\frac1{N^2}\sum_{h\ne0}H(h)K_\beta(h).}\tag{33.1}
\]
The last term is the **off-diagonal connected Wilson contribution** after subtracting same-plaquette overlap. The diagonal term at beta>0 must use the **actual interacting** \(K_\beta(0)\): substituting the beta-zero value 1/4 into a beta-two numerical reconstruction would be wrong. For the centered physical source \(F_x=(1+P_x)/2\), all covariance terms on the right are divided by exactly four; correlation ratios remain unchanged.

At beta=0, original continuous Haar gauge links give \(K_0(h)=\delta_{h,0}/4\), recovering VOL32's exact spherical covariance \(J/(4N^2)\) for P and \(J/(16N^2)\) for F. This is the exact red control.

## 2. Independently verified finite-torus spherical geometry

For new interacting measurements, use **L=6** (1,296 original 4D sites, 5,184 original positive SU(2) links) and the genuine original full Wilson action. The two endpoints are separated by d=2 or d=3 along original transfer coordinate 2. Radius 1 and 2 shells are actual integer four-sphere site sets mapped injectively into the periodic L=6 torus; all pair histograms preserve their original modular displacements. The geometry of each measured shell pair is:

| Radius R | Endpoint separation d | Points per shell N | Exact common plaquettes J | Exact ordered pair count N² | Distinct displacement bins |
|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 8 | 1 | 64 | 33 |
| 1 | 3 | 8 | 0 | 64 | 33 |
| 2 | 2 | 24 | 9 | 576 | 129 |
| 2 | 3 | 24 | 0 | 576 | 129 |

The [integer-only checker](../../tests/ym4_vol33_shell_pair_histogram.py) derives all four integer histograms from scratch. It computes an arbitrary **integer synthetic local field** by two independent formulas and compares (A) direct spatially translated shell product contractions with (B) the histogram-weighted 4D two-point convolution. The raw and fully connected equations match exactly, including the common-versus-distinct split. This is an algebraic/geometry verification, **not** an SU(2) field sample. The host [HBP receipt](YM4-VOL33-SHELL-CONTRACTION-20261124.hbp) separately pins the exact checksum.

## 3. Genuinely interacting continuous SU(2) simulation, independently seeded

An exploratory experiment outside the no-float mathematical proof kernel generates the original Wilson Gibbs action using exact conditional single-link heat-bath sampling. Each original link has six Wilson staples. At beta>0 the proposed SU(2) unit quaternion is distributed according to the exact conditional density \(\exp(\beta u\cdot H_e)dH_{S^3}(u)\), using an exponential scalar proposal with acceptance probability \(\sqrt{1-t^2}\) and uniformly random S² transverse direction. At beta=0, the chain refreshes each link from true Haar SU(2).

**Numerical source checks:** local six-staple action identity and independent site-wise SU(2) gauge-invariance of Wilson traces passed on randomized test configurations to floating precision <1e-11. Four-dimensional site indexing, shell pair displacement histograms, Fourier convolution and direct shell averages use independently written code routes. For each individual field configuration, the FFT two-point contraction and direct shell-product average agree to absolute <4e-12, **before any ensemble mean subtraction**.

Two completed groups, all on the genuine **L=6** original periodic gauge model:
- beta=2, eight independent seeds 4117, 5147, 6211, 7321, 8431, 9511, 10627, 11743, each with 95 warmup sweeps, 105 retained configurations and two Gibbs sweeps between measurements: **840** configuration samples total.
- beta=0, six independent seeds 1201, 2203, 3209, 4211, 5231, 6257, each with 15 warmup sweeps, 110 retained configurations and one independent-Haar refresh between measurements: **660** controls.

The pilot uses double-precision numerical SU(2) quaternions/FFTs. The reported "±" is the standard error across complete **independent seed-specific** connected-correlator estimates, with each chain as the statistical unit. These are *descriptive*, not rigorous confidence intervals; chain autocorrelations, thermalization bias, estimator centering bias and finite-volume effects have not been bounded rigorously. No data for production beta=9^12 or L=128 spherical shell fields were sampled.

## 4. Independently sampled two-point function at nonzero separations

The following refer to the **unshifted plaquette trace P=Re U_p**; the centered F=(1+P)/2 covariance is one-quarter of each entry.

| Original displacement h | beta=0, mean ± seed-SE | beta=2, mean ± seed-SE |
|---|---:|---:|
| h=0 (self covariance) | 0.249700 ± 0.000348 | 0.135766 ± 0.000230 |
| 1 in original time x2 | -0.000138 ± 0.000233 | **0.004234 ± 0.000161** |
| 2 in original time x2 | 0.000083 ± 0.000186 | 0.000180 ± 0.000144 |
| 3 in original time x2 | 0.000122 ± 0.000330 | -0.000196 ± 0.000207 |
| 1 in spatial x0 | -0.000300 ± 0.000273 | **0.000815 ± 0.000111** |

The nearest temporal and one-spatial-step beta-two signals are positive at this small finite lattice and this pilot precision. Two- and three-step estimates remain close to sampling noise. At beta zero the observed nonzero displacements are compatible with the **exact** continuous-Haar value zero.

## 5. Subtract the genuine common-plaquette term; test radial interaction

The beta-two interacting self variance is **K_beta(0)=0.135766 ± 0.000230**, not the beta-zero 1/4. The exact overlap fraction in the raw shell covariance is \(J/N^2=1/64\) for both R1,d2 and R2,d2. This yields the actual measured shared-plaquette contribution 0.00212134. The independent FFT reconstruction and direct shell averaging agree to less than 1e-12 for all aggregate rows.

| Original L=6 shells | beta=2 full connected covariance | Exact common-plaquette term | Residual off-diagonal contribution | Across-seed SE of residual |
|---|---:|---:|---:|---:|
| R1, d2 (J=1) | 0.00220791 | 0.00212134 | +0.00008657 | 0.00003624 |
| R1, d3 (J=0) | 0.00012474 | 0 | +0.00012474 | 0.00004293 |
| R2, d2 (J=9) | 0.00213868 | 0.00212134 | +0.00001734 | 0.00002831 |
| R2, d3 (J=0) | 0.00014960 | 0 | +0.00014960 | 0.00003198 |

At beta=0 the corresponding residuals are -0.00000138±0.00002627, +0.00010628±0.00006218, +0.00000241±0.00003862 and +0.00002142±0.00004895. All beta-zero red residuals are statistically compatible with zero in this preliminary experiment.

The contrast in R1/d2 and R2/d2 is useful: they have the **same diagonal overlap fraction** yet very different estimated distinct-plaquette contributions. The residual depends on the full shell displacement histogram and genuine K_beta(h), beyond the 24-cell shared-site count. However, the radius-two/d2 residual is smaller than its seed-SE, and differences between interacting residuals and zero-beta controls are not consistently resolved across all four cases. Therefore this pilot does **not** certify a reproducible radial dynamical pattern or a mass gap.

Machine-readable **provisional** GitHub measurement summaries: [nonzero-separation Wilson two-point function with chain errors](YM4-VOL33-EXPLORATORY-L6-TWO-POINT-20261124.csv) and [eight two-ended shell residual/control rows](YM4-VOL33-EXPLORATORY-L6-SHELL-RESIDUALS-20261124.csv). These are rounded summaries, distinct from the raw conversation-hosted numerical samples and the strictly integer HBP.

## 6. Provenance and signoff boundary

The experimental source, raw row-level outputs and complete seed-level summaries are provided as downloadable conversation artifacts, outside the strict integer-only mathematical repo. Their exact SHA-256:
- experimental code: **c18fb1871f8a46c875fe12de68ff3e7c018afcdd0e4dd7455c53ab1a5c750a5c**;
- beta-two 840-row CSV: **b95e71aacc52f703054a86185b3b45e0954d07d316dad39b8c816deaadcaf22e**;
- beta-zero 660-row CSV: **8a4905a9b5e3a4dce8efe15969663ebc41c4d5111ed2f82ce2bebbf1dda5160a**;
- beta-two summary JSON: **7145eefca8b93a72059bb0653dae486161f3c33bffcba112997773966143cb3f**;
- beta-zero summary JSON: **ffeda213898cea823e5df6e26b6cc205a5f5ffca3b01096cd8bad582e2f072f4**.

The strictly integer-only geometry/convolution verifier and its HBP are **separate** from these finite-precision numerical observations and subject to dedicated hosted CI. The [interactive research comparison plot](vol33-connected-shell-residual.html) displays the preliminary measurements and clear scope labels. The existing [VOL30 L128 3D 20-frame player](vol30-spherical-fischer.html) remains an exact 4D geometric viewer; no invented L128 beta-two or beta-production field values are overlaid.

**Conformity verdict:** Exact 4D spherical pair-contraction and same-plaquette subtraction **mathematically PASS**. Exact continuous-SU2 beta-zero Haar limit PASS through VOL32. Independently seeded nonzero-coupling finite SU2 Wilson measurements **numerically consistent but provisional**. Physical continuum exponential upper decay, beta(a), renormalized nonzero source, Gauss/winding limit and eleven original construction obligations **OPEN**.

**Next research target:** a second *independent* simulation implementation or mathematically rigorous interval estimator, more finite lattice sizes and truly variance-controlled *longitudinal/time and radial* K_beta(h) profiles; only then test radial dynamical shape against Wilson/transfer certificates and a physical beta(a) scaling trajectory.
