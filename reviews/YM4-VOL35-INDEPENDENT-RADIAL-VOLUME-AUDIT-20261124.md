# YM4 VOL35 — independent mathematical/statistical acceptance review of L8 vs L10 radial Wilson measurements

**24 November 2026 · internal independent-method review, not signed external human signoff.** Separate the exact original discrete geometry and source algebra from empirical Metropolis sampling, dependence estimates and continuum upper-mass claims.

## A. Exact two-ended geometry and diagonal subtraction — PASS

For every original torus L=8 and L=10, the original Euclidean integer radius-one and radius-two shell starting sites are injective modulo the torus. Endpoints at d=2 and d=3 along transfer axis x2 have, respectively, four \((N,J,\text{distinct ordered pair bins})\) patterns:
\((8,1,33),(8,0,33),(24,8,165\ \text{L8 or}\ 169\ \text{L10}),(24,0,165\ \text{L8 or}\ 169\ \text{L10})\).
The strict integer program independently enumerates all original sites and all N² ordered source pairs; it also confirms the crucial L6-to-L8 correction from the previous stage: the spurious shared L6 radius-two/d-two site is removed. At R2,d3, J=0 at both L8 and L10, but the *entire* periodic displacement histograms differ. Thus matching J alone does not establish volume independence.

At any beta the original Wilson covariance contraction
\(\operatorname{Cov}(M_A,M_B)=N^{-2}\sum_hH(h)K_\beta(h)\)
is algebraically exact. The shared-site contribution is \(J K_\beta(0)/N^2\); using the beta-zero Haar K(0)=1/4 at beta=2 would bias the subtraction. The numerical implementation uses the actual measured beta-two K(0). Raw direct-versus-histogram contractions match to around \(10^{-15}\) at each field. Such machine equality validates the reconstruction arithmetic, not the Monte Carlo probability distribution.

## B. Independent original continuous-SU2 algorithm — qualified PASS

VOL34's C++17 link-proposal Metropolis samples the genuine SU2 Haar reference group, computes all six original plaquettes adjacent to each proposed link and uses the exact Wilson action ratio. Random SU2 site-gauge transforms left the plaquette traces invariant and the six-plaquette local energy matched a full action recomputation. The proposal includes fresh Haar group moves and symmetric left-multiplication rotations, so formal finite-dimensional target stationarity is supported by detailed balance. However, this **does not imply that 900/1000 sweeps suffice for equilibrium** at beta=2 on all chains. The original heat-bath implementation is a separate cross-algorithm check of the nearest-time signal, not an independent large-volume L8/L10 algorithm replicate.

The new **26 complete chains** were fixed by independent seeds. L8 beta-two has 8×350 configurations after 1000 sweeps; L10 beta-two 6×220 after 900 sweeps; L8/L10 beta-zero each 6×500 independent Haar refreshes, 10,120 configurations in total. One post-run exported L10 file was truncated; regeneration from the same fixed seed produced the original logged SHA-256, and the truncated copy was excluded. Per-chain fixed-point evidence has an explicit \(\times10^{12}\) rounding scale.

## C. Is C1 volume-compatible? FINITE-VOLUME NUMERICAL PASS

\(K_{\beta=2}^{L8}(e_2)=0.0039919168\pm0.0000468205\) and
\(K_{\beta=2}^{L10}(e_2)=0.0040149104\pm0.0000129282\)
in the *unshifted* plaquette trace P. Difference \(-0.00002299\) is smaller than the combined estimated seed-SE \(\approx0.00004857\); this is numerical consistency, not an infinite-volume theorem. Beta-zero controls give \(+0.00000281\pm0.00007463\) and \(+0.00005915\pm0.00002633\), both compatible with exact Haar zero at their finite chain precision.

The beta-two nearest single spatial shift \(K(e_0)=0.0007166\pm0.0000348\) at L8 and \(0.0006696\pm0.0000359\) at L10, also positive in both volumes. Time-two and time-three correlations are substantially smaller, with uncertainty comparable to some estimates; do not infer a spectral mass from their ratios without full transfer overlap and controlled bias.

## D. Which spherical signals persist? EXPLORATORY with visible volume effect

After the exact common-plaquette subtraction, the two zero-overlap cases have:
- R1,d3: L8 beta-two \(0.00007517\pm0.00000939\); L10 beta-two \(0.00006127\pm0.00000598\).
- R2,d3: L8 beta-two \(0.00008242\pm0.00000394\); L10 beta-two \(0.00006383\pm0.00000380\).
The corresponding beta-zero control means are close to zero, with explicit seed SE in the mathematical note. Four-comparison Welch/Holm beta-two−Haar contrasts yield corrected p≈0.0137/0.00000354 at L8, p≈0.00179/0.00000375 at L10, respectively. These are **not** exact p-value certificates; their validity presupposes appropriate equilibrium, effective sample sizes and chain-mean assumptions.

A second prespecified four-case Welch/Holm volume comparison gives R1d3 p≈0.572 and **R2d3 p≈0.0217**. The R2d3 L8−L10 residual difference \(0.00001859\pm0.00000547\) is a genuine **finite-volume warning** under the numerical assumptions. There is no acceptable extrapolation to L=∞ or a claim that radial interaction strength is volume-independent.

Approximate integrated autocorrelation times on linearized C1 contributions have median 0.64 saved samples at L8 beta-two and 0.63 at L10 beta-two; minimum estimated effective per-chain counts are ~177 and ~115. Split-chain early/late differences are not conclusively different from zero. These tests cannot rule out slow modes or validate all source-specific radial observables, especially on weakly coupled scaling trajectories.

## E. Exact-integer checker / hosted acceptance boundary

The new strict verifier independently reconstructs L8/L10 pair histograms, reads 26 **integer-scaled reported chain records**, confirms unique seeds/counts and positive reported self variances, and uses *only integer polynomial comparisons* to test the Haar-red, nearest-slice and spherical contrast thresholds (2,3,5 standard errors). The tests are **checks on rounded reported chain means**, not a mathematical statement about the Wilson Gibbs expectation or valid inferential p-values. Its frozen HBP, input and expected SHA-256 are pinned in the dedicated hosted VOL35 workflow. IEEE floating statistics are performed outside the no-float proof gate and remain in the separately downloadable full raw research bundle.

**Mathematical PASS:** exact periodic geometry and spherical contraction identity, as in VOL33–34. **Finite numerical confirmation:** stronger original SU2 beta-two nearest-time C1 and both nonoverlap J0 signals on L8 and L10. **Scientific HOLD:** residual finite-volume effect (R2,d3), unproved equilibrium, original L128 production beta9^12 Wilson shell measurements, uniform-in-volume upper exponential distance decay, physical beta(a), nonzero continuum renormalized source, all Gauss/winding limits and eleven original continuum-construction obligations.

**Next theorem acceptance:** derive a genuinely source-local **upper** connected two-point correlation decay with constants valid uniformly in L on the necessary beta(a) interval; distinguish weak-beta proven cluster domains from the physically unproved production high-beta coupling. More simulation alone does not settle this proof gate.
