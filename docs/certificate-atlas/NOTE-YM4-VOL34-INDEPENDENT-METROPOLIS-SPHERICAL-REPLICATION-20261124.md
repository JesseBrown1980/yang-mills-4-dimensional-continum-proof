# YM4 VOL34 — independent SU(2) Metropolis replication and spherical off-diagonal Wilson validation

**24 November 2026 · original four-dimensional continuous-SU(2) Wilson model · finite-volume numerical research checkpoint.** The requested next test is a **second update algorithm** for the connected Wilson plaquette two-point function at nonzero separations, independently of the VOL32–33 single-link heat bath, plus a second direct-versus-pair-histogram reconstruction of **spherical connected residuals after subtracting common-plaquette covariance**.

**Verdict:** two independently implemented samplers agree on the nearest-time-slice \(6^4\), \(\beta=2\) Wilson correlation within estimated chain uncertainty. Independent sphere-direct and integer-displacement reconstruction agree on every retained configuration to floating precision. The **nonoverlapping** radius-1/d=3 and radius-2/d=3 spherical residuals have positive exploratory beta-two-minus-Haar contrasts after a four-case Holm adjustment. These are finite-lattice numerical observations, **not** production \(\beta=9^{12}\) results, upper exponential mass decay, or an \(a\to0\) continuum certificate.

## 1. Independent physical Monte Carlo update, acceptance and controls

Use the exact original untwisted periodic lattice Wilson Gibbs density
\[
 \mu_{\beta,L}(dU)\propto\exp\{\beta\sum_{p}\operatorname{Re}U_p\}
          \prod_{\text{original positive links }e}dH_{SU(2)}(U_e)
\]
with **continuous** SU(2) unit-quaternion links. The new implementation was written independently in **C++17**, without importing or reusing VOL33's Python original-link staple/heat-bath code.

Instead of heat-bath sampling, propose replacing a link \(U_e\) by \(Q\,U_e\), where \(Q\) is a symmetric mixture of (a) fresh SU(2) Haar quaternions and (b) local SU(2) rotations with an angle uniform on a symmetric interval and uniformly distributed transverse direction. The proposal density is invariant under \(Q\mapsto Q^{-1}\); its Haar component makes the link-update proposal irreducible on the compact group. Recompute **directly all six affected original elementary Wilson plaquettes before and after** the proposal and accept with the exact Metropolis rule
\[
 \alpha(U_e,U'_e)=\min\bigl(1,\exp\{\beta[S_e(U'_e)-S_e(U_e)]\}\bigr).
\]
Proposal symmetry and this ratio establish the *standard finite-dimensional detailed-balance equation*. At \(\beta=0\), use complete fresh independent Haar-link refreshes as the exact red. On randomized noncommuting SU(2) configurations, the local six-plaquette action difference was independently compared with the **entire** Wilson action change, and independently generated local gauge transformations preserved original plaquette traces, both within the indicated numerical tolerances \(2\cdot10^{-10}\) and \(2\cdot10^{-11}\). At beta two, the observed link proposal acceptance fraction was approximately **0.486**.

This is a floating numerical experiment outside the project's original strict integer-only mathematical kernel. All source files, full raw configuration-level outputs, seed tables, numerical statistic scripts, and their SHA-256 evidence hashes are supplied as conversation attachments; only fixed-point chain summaries, aggregate estimates, native geometric algebra witnesses and the explicit numerical scope are staged in the research branch.

## 2. Second implementation reproduces genuine \(6^4\) Wilson two-point signals

The original source is \(P_x=\operatorname{Re}U_{p_x}\) on the spatial 0–1 plaquette at site x, with the transfer time direction x2. A translationally averaged connected two-point function is
\[
 K_\beta(h)=E[\operatorname{avg}_x P_xP_{x+h}]-E[P_x]^2.
\]
The physical centered \(F_x=(1+P_x)/2\) has connected covariance exactly \(K_\beta(h)/4\), leaving the normalized \(K_\beta(h)/K_\beta(0)\) unchanged.

Completed independent Metropolis sampling:
- \(\beta=2\), \(L=6\): **8 independent seeds**, 1,300 warmup sweeps, 650 saved configurations per seed separated by four complete sweeps: **5,200** total.
- \(\beta=0\), \(L=6\): **6 independent seeds**, 20 warmup refreshes, 550 independent-Haar configurations per seed: **3,300** total.
- \(\beta=2\), \(L=4\): **6 independent seeds**, 900 warmup sweeps, 650 configurations per seed separated by four sweeps: **3,900** total.
- An exploratory beta-one extension was stopped after only part of the intended seeds and is **excluded** from reported comparisons.

The original VOL33 heat bath completed eight \(\beta=2\), L6 chains with 840 configurations and six zero-beta control chains with 660 configurations. The independently recomputed per-chain connected estimates are:

| Measurement, unshifted trace \(P\) | Original heat bath L6 | Independent Metropolis L6 |
|---|---:|---:|
| \(\beta=2,\ K(0)\) | \(0.135766\pm0.000230\) | \(0.135838\pm0.000165\) |
| \(\beta=2,\ K(e_2)\) | **\(0.004234\pm0.000161\)** | **\(0.004032\pm0.000051\)** |
| \(\beta=2,\ K(2e_2)\) | \(0.000180\pm0.000144\) | \(0.000116\pm0.000057\) |
| \(\beta=2,\ K(e_0)\) | \(0.000815\pm0.000111\) | \(0.000674\pm0.000096\) |
| \(\beta=0,\ K(e_2)\) | \(-0.000138\pm0.000232\) | \(-0.0000023\pm0.0000650\) |

Errors are standard errors across complete independent chain estimates. The \(\beta=2\) C1 difference (Metropolis minus heat bath) is \(-0.0002021\), with combined seed standard error \(0.0001691\): **1.20 standard errors**, and a nominal Welch 95% difference interval approximately **[-0.000589, 0.000185]**. Therefore the two independently implemented algorithms are **consistent** at this resolution. The independent L4 beta-two C1 is \(0.003784\pm0.000198\), also consistent at its current finite-volume precision; systematic L dependence is not yet resolved.

The Metropolis L6 beta-two midpoint \(K(e_2)\) has chain-based nominal t95 interval **[0.0039103, 0.0041532]**, and its zero-beta control is consistent with the exact original Haar value zero. For each Metropolis L6 beta-two chain, the autocorrelation of the per-configuration **linearized covariance contribution** \(Z=\overline{P_xP_{x+e_2}}-2\widehat\mu\,\overline{P_x}+\widehat\mu^2\) was assessed with an initial-positive-sequence estimate. The **median integrated \(\tau_{\rm int}\) is 0.66 saved configurations**, and the minimum estimated within-chain effective sample count is roughly 350. These are descriptive autocorrelation estimates, not a proof of equilibrium or rigorous sample independence. Comparing the chain's late and early halves gives \(K(e_2)_{\rm late}-K(e_2)_{\rm early}=0.000155\pm0.000149\), with no resolved drift at current precision.

## 3. Independent two-ended spherical contraction and overlap subtraction

On the original periodic L6 torus, use exactly the VOL33 radius-1 and radius-2 four-integer-square shells, with endpoints separated in original direction 2 by d=2 or d=3. There are four shell-pair cases \((R,d;N,J)=(1,2;8,1),(1,3;8,0),(2,2;24,9),(2,3;24,0)\).

A **separate, from-scratch C++ spherical sampler** independently measures on each saved configuration:
1. The **direct translational shell-mean product** \(\frac1V\sum_tM_A(t)M_B(t)\), averaging the true spatial 0–1 SU(2) Wilson plaquette traces over both spherical sets.
2. The **integer pair-displacement histogram contraction** \(\sum_h H(h)\,V^{-1}\sum_t P_tP_{t+h}/N^2\).

These routes agree on *each configuration* to maximum absolute discrepancy **\(1.5\times10^{-15}\)** in the beta-two sample. The exact mathematical identity underpinning the comparison is independently hosted in VOL33's strictly integer arithmetic test. The centerings and shared-plaquette subtraction are computed **after ensemble averaging**, using the actual interacting \(K_\beta(0)\) rather than substituting its beta-zero value.

The spherical cross-check generated:
- beta two, L6, **8 independent seeds**, 1,000 warmup sweeps, 500 saved configurations separated by three sweeps: **4,000** total.
- beta zero, L6, **6 independent seeds**, 25 warmup refreshes, 450 independent-Haar configurations per seed: **2,700** total.
- A one-seed code smoke check is excluded from the reported evidence.

Independent-chain estimates of the genuine **distinct-plaquette connected term**, in the unshifted P normalization:

| L6 shell case | Shared plaquettes J | \(\beta=0\) residual ± seed-SE | \(\beta=2\) residual ± seed-SE | \(\beta=2-\beta=0\) residual contrast |
|---|---:|---:|---:|---:|
| R1, d2 | 1 | \(+0.00002976\pm0.00002793\) | \(+0.00007547\pm0.00001493\) | \(+0.00004572\pm0.00003168\) |
| R1, d3 | 0 | \(-0.00002522\pm0.00002708\) | \(+0.00014877\pm0.00002366\) | \(+0.00017399\pm0.00003597\) |
| R2, d2 | 9 | \(-0.00001317\pm0.00001045\) | \(+0.00000789\pm0.00000629\) | \(+0.00002106\pm0.00001220\) |
| R2, d3 | 0 | \(-0.00003985\pm0.00001563\) | \(+0.00013400\pm0.00001268\) | \(+0.00017384\pm0.00002012\) |

Under a **Welch comparison of independent chain means**, with a Holm adjustment across these four planned contrasts, the adjusted two-sided p-values are approximately \(0.241,0.00157,0.241,0.0000172\), respectively. The two cases **with zero shared plaquettes** show beta-two-minus-Haar differences even after this multiplicity adjustment. The two overlapping-shell contrasts are currently inconclusive. This is exploratory evidence for finite-volume **distinct-plaquette dynamical connected correlations**, not a demonstrated four-dimensional continuum radial law.

**Important beta-zero safeguard:** one Haar radial residual in a completed six-chain control is \(-0.00003985\pm0.00001563\), a chance excursion under multiple testing (and possible estimator/systematic uncertainty). Reporting beta-two residuals relative to an independently sampled beta-zero reference, with the full four-comparison adjustment, is more conservative than inspecting their sign alone. A variance check of the individual source and independent chain drift/mixing remains necessary for future production measurements.

## 4. Exact integer witness and evidence provenance

The [VOL34 fixed-point 42-chain inventory](YM4-VOL34-FIXED-POINT-CHAINS-20261124.csv) rounds the numeric **per-chain** estimates to a declared factor \(10^{12}\). The separate [strict integer verifier](../../tests/ym4_vol34_fixed_point_replica_verifier.py) *only* tests the arithmetic of those reported chain means: unique seeds, group counts, exact integer self-variance signs, two-method beta-two nearest-slice agreement within twice the combined seed-SE, both beta-zero Haar red controls, and which spherical beta-two-minus-Haar contrasts exceed two/four/six combined seed-SE. Its [frozen HBP](YM4-VOL34-INDEPENDENT-REPLICA-20261124.hbp) and dedicated workflow do **not** turn empirical seed standard errors into a mathematical proof of the SU(2) Gibbs expectation.

Numerical results and raw sources were generated in the local conversation runtime. Independent source and completed data SHA-256:
- First independent C++17 Metropolis implementation: \`ym4_vol34_independent_metropolis.cpp\`, **c18c4ff91811e1b7a2d8a573ac6695e2223718e695b8e40705f82f6104350e6b**.
- Independently constructed spherical Metropolis measurement version: \`ym4_vol34_independent_metropolis_spherical.cpp\`, **ea3976eaae4db72b2f80736a08b430266f5dfe3ebf3d40fb46a4c0abde350149**.
- Combined independent original-Metropolis two-point samples: \`ym4_vol34_metropolis_all_samples.csv\`, SHA **b6bb28dab84c0e57c33fca58c9286846e5aeeb603ac5e86a89d23161a3faa9bb**.
- Spherical beta-two 4,000-configuration raw dataset: \`ym4_vol34_spherical_Metropolis_L6_beta2_raw.csv\`, SHA **ff8853996fab061f62e7ddd521d2e6f2c87db2c6d71e0f3c740aa09df1be87b1**.
- Spherical beta-zero 2,700-configuration raw dataset: \`ym4_vol34_spherical_Metropolis_L6_beta0_raw.csv\`, SHA **379cc786287ae3c5e39d00355d9aa17fe7cbfc644ed713e0eedd71c8e9092b98**.
- Per-chain spherical statistics CSV: SHA **1a949c5c1441c712c296a4e887a74a752cc3eefb6c9f233cae7b70533e979128**.
- Per-chain spherical statistical analysis JSON: SHA **833598d3689ee24d3eeee16c5a07baa1a257122318952fa4f542659c076e8665**.
- GitHub fixed-point chain CSV (normalized LF line endings): expected SHA **616e59d84d82d259a9d9b9b91d23085f3133bd8efc7ce9b9bfd258b8dc0296d8**.
- [Concise GitHub exploratory results table](YM4-VOL34-INDEPENDENT-METROPOLIS-RESULTS-20261124.csv) tracks 20 predeclared observable/control rows.

Source and full raw CSV artifacts are available for download in the conversation, separated from the project's **no-floating-point mathematical proof kernel**. The GitHub branch includes the documented algorithms, fixed-point per-chain chain summaries and finite numerical summary, but does not contain the full multi-megabyte raw numerical runs or floating C++ source. That boundary is explicit.

## 5. Acceptance ledger and next targeted mathematical computation

**Exact mathematical acceptance:** the VOL33 original periodic four-dimensional pair-histogram identity and common-site/off-diagonal decomposition remain fully exact; VOL32's beta-zero Haar Wilson shell covariance is fully analytic. VOL34's strict verifier certifies **reported statistical arithmetic only**. The independent physical samplers agree numerically on the small-lattice beta-two two-point function, and two zero-overlap spherical cases replicate positive finite-beta residual contrasts.

**Open acceptance:** rigorous equilibrium/mixing and statistical error control, additional source lengths and independent L values for **radial** observables, nonzero-bare-coupling true original L128 20-shell Wilson samples, production beta \(9^{12}\), uniform-in-volume **upper exponential Wilson correlation decay** along a proved beta(a) continuum path, nonzero limiting renormalized source, physical Gauss/winding transfer, and all **eleven** continuum-construction gates. An observed finite-lattice positive correlation has a different role from a continuum mass-gap certificate.

**Next objective:** independently vary \(L=6,8,\dots\) and shell radii on controlled even tori with full longitudinal/radial \(K_\beta(h)\), apply blocking/variance reduction and independent mixing diagnostics, then compare those field-specific predictions against the original SU(2) analytic upper/lower interval. Prioritize a **uniform upper rate proof** rather than additional geometric displays. Research candidate in draft PR #113; production \`main\` and accepted 115-node atlas unchanged.


## 6. L8 finite-volume extension: exact periodic alias and preliminary long-loop screen

The [separate VOL34 L8 periodic alias and screening certificate](NOTE-YM4-VOL34-L8-PERIODIC-ALIAS-SCREENING-20261124.md) resolves a real original-lattice geometry issue: for (radius R=2, center separation d=2), the two exact sphere shells have **J=9** shared plaquettes on the periodic L6 torus, but only **J=8** on L8 and L10. The one extra L6 shared site is \((0,0,4,0)\), a periodic identification of the center's \((0,0,-2,0)\) and the outer shell's \((0,0,2+2,0)\). The full original periodic displacement histogram has 129 occupied bins at L6 and 165 at L8. The [exact integer verifier](../../tests/ym4_vol34_periodic_alias_verifier.py), [frozen HBP](YM4-VOL34-PERIODIC-ALIAS-20261124.hbp), and [new hosted geometry gate](../../.github/workflows/ym4-vol34-independent-replica.yml) explicitly enforce these counts.

A new **L8 beta-two screening run** completed **three independent chains, 280 configurations each**; three separate L8 beta-zero Haar chains each completed 280 configurations. A fourth beta-two chain stopped after 95/280 configurations and is **excluded**. With the corrected coupling-dependent J8 diagonal overlap, \(C_1^{L8}(\beta=2)=0.00393156\pm0.00010011\), compatible with both prior L6 methods. At L8,d3, the two nonoverlapping-shell residuals are R1,d3 \(+0.00008811\pm0.00002455\) and R2,d3 \(+0.00006561\pm0.00000444\), both smaller than their corresponding L6 exploratory means. However the beta-zero L8 three-chain controls have standard errors \(0.00002400\) and \(0.00003167\); **the differences are not resolved** at this very limited L8 sample size. This screening prevents a premature claim of continuum-radial invariance and makes the next fully powered larger-L experiment precise.

The [compact screening CSV](YM4-VOL34-L8-SCREENING-20261124.csv) contains ten explicit observable/control rows. Six complete L8 raw finite SU2 numerical chains (1,680 configurations) are in the conversation data bundle at SHA-256 **768c0dd4ca2169fedcee91179837b130e323d33e71c49c8c443a94e9d2da8000**. The exact integer geometry and pilot floating statistical evidence retain separate acceptance statuses.
