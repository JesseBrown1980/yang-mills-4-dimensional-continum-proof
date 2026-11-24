# YM4 VOL33 — independent-method audit of Wilson two-point contraction and shell overlap subtraction

**24 November 2026 · internally separate exact-mathematics / statistical review.** Scope: verify the new exact decomposition of original SU(2) Wilson spherical correlation into same-plaquette and off-diagonal connected contributions, scrutinize numerical independence and source-state acceptance, and assess evidence for a radial dynamical effect. Not an external signed referee review.

## A. Original gauge-invariant observables and normalizations — PASS

Fix the true four-dimensional periodic SU(2) Wilson Gibbs measure \(\mu_{\beta,L}\), and let \(P_x=\operatorname{Re}U_{p_x}\) be an elementary *spatial 0–1* plaquette trace with site x. Its centered physical source in VOL26 is \(F_x=(1+P_x)/2\). Hence for every displacement \(h\), \(\operatorname{Cov}(F_0,F_h)=\operatorname{Cov}(P_0,P_h)/4\), including h=0. All normalized correlation ratios are unchanged. The pilot reports P covariance, not F covariance, and labels it.

Translation invariance implies \(K_\beta(h)=E[P_xP_{x+h}]-(E P)^2\) independent of x. The two-shell connected covariance equals a positive-**multiplicity** contraction over *all* original pair displacements \(h=y-x\bmod L\), including displacements whose individual K_beta(h) may have either sign. The exactly shared-site diagonal is \(J K_\beta(0)/N^2\). For **nonzero beta**, K_beta(0) is not fixed to its Haar value of 1/4; the pilot correctly measured beta=2 K0≈0.135766. Subtraction uses the same beta-specific sample K0.

At beta=0, the exact original continuous-Haar result is \(K_0(h)=\delta_{h,0}/4\). Thus exact distinct-plaquette residual zero is a rigorous red control, and no positive radial dynamics is inferred from common plaquettes.

## B. Two independent computational routes and exact algebraic falsifier — PASS

For each saved continuous-SU(2) gauge configuration, the pilot computes (i) direct spatial-translation averaged products of both shell mean fields, and independently (ii) the full real lattice autocorrelation of the original plaquette field using an FFT, contracted with a separately enumerated pair-histogram H(h). In **unsubtracted** form these match to absolute <4×10⁻¹² in completed runs. The same common ensemble centering by the squared mean then produces identical connected answers. They share the *same gauge configurations* and are **algorithmically independent calculations, not independent statistical samples**.

More strongly, the strict integer-only mathematical checker [VOL33 geometry test](../tests/ym4_vol33_shell_pair_histogram.py) reconstructs all four L6 pair histograms and proves the direct/sum identity numerically with *exact integer equality* for two independent synthetic integer 4D fields. It also tests the exact connected subtraction and diagonal/off-diagonal split using common integer denominators. Such synthetic fields are algebraic falsifiers; the actual SU2 interacting data are independently obtained by the floating Monte Carlo simulation and not certified by this integer checker.

## C. Independent experimental controls and precision — PROVISIONAL

The experimental source is stored as a separate reproducible conversation artifact with SHA-256 **c18fb1871f8a46c875fe12de68ff3e7c018afcdd0e4dd7455c53ab1a5c750a5c**. It imports the earlier SU2 heatbath's exact continuous-group conditional distribution, and independently computes the plaquette field, full displacement-space FFT correlation and direct shell-averaged products. The L6 beta2 completed measurement includes eight separate pseudorandom seeds ×105 configurations, with 95 warm-up sweeps and two thinning sweeps. The beta0 red includes six seeds ×110 configurations, 15 Haar-link warmups and one independent Haar refresh between samples. All original six-link-staple finite-difference and site-gauge invariance numeric checks passed at <1e-11 on tested data.

The reported "seed_SE" treats the independent chain as a statistical cluster, rather than pretending 840 individual configurations are independent. This is a reasonable descriptive uncertainty statistic. **Potential unbounded errors**: finite warmup, within-chain autocorrelation not independently assessed for beta2, only eight chains, stochastic precision, and finite-volume systematic bias. Standard errors do not constitute rigorous confidence intervals or a mathematical acceptance of a mass gap.

The nearest time-like beta2 correlation C1(P)≈0.004234±0.000161 and nearest spatial C_(e0)(P)≈0.000815±0.000111 are positive and agree qualitatively with a local interacting gauge measure. The beta0 nonzero-displacement control is consistent with exactly zero. Larger temporal separation estimates at d2/d3 remain comparable to statistical noise.

## D. Spherical residual and inference — CONDITIONAL / OPEN

At L6, four exact shell pairs (R1/R2, endpoint d2/d3) have J=(1,0,9,0) and N=(8,8,24,24). The beta2 full connected spherical cross-correlations are approximately (0.00220791,0.00012474,0.00213868,0.00014960). Subtracting the actual measured J/N²×K_beta(0) leaves residuals approximately (0.00008657,0.00012474,0.00001734,0.00014960), each with seed-SE (0.00003624,0.00004293,0.00002831,0.00003198). The radius-two/d2 residual is smaller than one seed-SE. The beta0 control residuals are compatible with zero. The beta2-minus-beta0 contrasts of those four residuals are not all statistically decisive.

**Interpretation:** the pilot **demonstrates how to isolate the off-diagonal connected Wilson information from common-plaquette geometry**. It does not yet establish a reproducible shell-radius law, original L128 field measurements, production beta9^12 behavior or continuum Yang–Mills mass decay. One cannot transfer the L6 d2/d3 overlap/fingerprint to the L128 d24 visualization because periodic geometry, weights, and physical separations differ.

## E. Acceptance verdict

- **Analytic / strict integer candidate PASS:** all-coupling exact displacement-histogram contraction formula, its beta-specific diagonal J K_beta(0)/N² subtraction, and exact L6 geometry and integer synthetic-field checks, with a dedicated hosted HBP.
- **Numerical provisional:** real continuous-SU2 interacting finite-volume K_beta(h) and spherical off-diagonal residual measurements, independently seeded but collected via one shared heatbath implementation; duplicate FFT/direct reconstructions validate arithmetic consistency, not independent physics calibration.
- **Open:** separate numerical codebase validation, larger sizes and effective sample sizes, production beta9^12/L128 shell data, source-shell conditional variance, a physical exponential *upper* mass decay estimate and all eleven original continuum construction obligations.

The research atlas must label the math/geometry verification independently from the exploratory numerical field measurements. The original accepted 115-node production certificate atlas and main branch should remain unchanged.
