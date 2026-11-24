# YM4 VOL34 — independent-method audit: SU(2) Metropolis replica, autocorrelation and radial contrast

**24 November 2026 · internal reviewer checklist and cross-method acceptance boundary.** The original model is the genuine finite-lattice continuous SU(2) Wilson Gibbs measure. The published independent algorithms are **floating numerical estimates**, while the separately hosted script checks only exact arithmetic on rounded reported chain means. This audit is distinct from external signed mathematical referee acceptance.

## 1. Does the second chain sample the same physical law? Conditional PASS

The original VOL33 sampler used direct conditional **heat bath**. The new program independently implements a symmetric random SU(2) left-multiplication **Metropolis proposal**, recomputes the **six original Wilson plaquettes** sharing each updated link, and accepts by \(1\wedge \exp(\beta\Delta S)\). Its Haar proposal component makes the per-link proposal support full SU(2), while the local rotational component is symmetric under group inverse. Proposal symmetry gives detailed balance with respect to the link's exact Wilson conditional law; sequential coordinate Gibbs/Metropolis compositions preserve the target original Wilson measure. One-link action differences were tested against a full-lattice Wilson action recomputation; site-wise independent SU(2) gauge changes preserved sampled plaquette traces. **Finite burn-in has no proof of stationarity**, so these checks justify the algorithm rather than certify perfect equilibrium.

Both simulations use the same lattice \(L=6\), pure Wilson plaquette sign convention, spatial 0–1 orientation, and temporal transfer direction x2. For the shifted bounded observable \(F=(1+\operatorname{Re}U_p)/2\), the connected covariance is one quarter the unshifted trace covariance, while normalized \(C_d/C_0\) is unchanged.

## 2. Is the independent C1 signal reproducible? FINITE-VOLUME NUMERICAL PASS

The heat bath's eight \(\beta=2\) chain means yield \(C_1=0.004233811\pm0.000161085\). The independent Metropolis's eight chain means (5,200 configurations) yield \(C_1=0.004031749\pm0.000051370\). Their difference is \(-0.000202062\) with combined standard error \(0.000169076\): **1.195 standard errors**. The nominal Welch 95% difference interval is \([-0.000589,0.000185]\). The independent \(L=4\) beta-two Metropolis gives \(C_1=0.003784461\pm0.000197943\), compatible at pilot resolution. No finite-volume extrapolation is fitted.

Six independent \(L=6\), beta-zero Metropolis Haar chains (3,300 configurations) give \(C_1=-0.000002292\pm0.000065039\), matching the exact continuous-SU2 Haar zero red. Heat bath's Haar control gives \(-0.000138017\pm0.000232216\), also compatible with exact zero. At beta two the Metropolis spatial \(K(e_0)\) is \(0.000674388\pm0.000096332\), compatible with heat bath's \(0.000814911\pm0.000110715\). The two-time-step correlator has substantial relative error and remains unresolved.

The integrated autocorrelation time estimated on the **linearized** per-config C1 contribution by a Geyer positive-sequence method has median about 0.66 saved configurations and the minimum estimated per-chain effective count is about 350. The early-minus-late chain comparison does not resolve a significant drift. However, autocorrelation truncation estimates and a finite split test are not **rigorous mixing bounds**. The Metropolis beta-two link acceptance fraction is about 0.486; this is a diagnostic, not a convergence proof.

## 3. Is the spherical correlation independently reconstructed? NUMERICAL CONSISTENCY PASS

The new C++ spherical implementation constructs direct original L6 four-integer-square shell sums, **without using the original Python FFT route**, and separately constructs the ordered pair-displacement histogram. For each of the **4,000** interacting and **2,700** Haar retained configurations, both give the same uncentered shell-pair product to worst-case absolute discrepancy less than \(1.5\cdot10^{-15}\). The **exact** equality is independently proved by the integer algebra in VOL33, and the empirical check guards implementation errors.

The reported connected residual subtracts \(JK_\beta(0)/N^2\) with the **measured coupling-dependent** self variance. At beta zero, the analytic Haar residual is zero for all four cases. The finite beta-two sample's raw residuals are positive for the three listed cases R1d2, R1d3 and R2d3; the R2d2 value is below estimated uncertainty. To test true beyond-overlap effects, the report compares each beta-two value with an **independent beta-zero control** of the same geometry and numerical procedure.

## 4. Multiplicity, independent chains and important finite-size safeguard

Across exactly four specified shell contrasts, Welch tests on independent chain means and Holm correction give approximate adjusted p values **0.241, 0.00157, 0.241, 0.0000172** for R1d2, R1d3, R2d2, R2d3. The **two geometrically nonoverlapping J=0** pairs (R1d3, R2d3) have replicated beta-two-minus-Haar residuals; the overlapping J>0 pairs remain inconclusive. The strict integer machine checker independently proves that **rounded reported chain means** meet the stated 2/4/6-combined-SE comparisons. It does not prove the validity of Welch sampling assumptions or generate authentic SU(2) samples.

**Critical finite-volume caveat:** On L6 with d=3, the two endpoint centers are separated by **half the periodic extent**. Wilson correlation can propagate around both time directions of the torus, and the radial shell neighborhoods are strongly affected by periodic geometry. A nonoverlap J=0 excludes the trivial **same-plaquette** covariance, but it does not remove all periodic and finite-volume effects. Before assigning physical radial decay, the next experiment should use increasing even L while holding the relevant radial/source distances away from L/2, check a truly connected dynamical term with confidence bounds and independently calibrate mixing.

The beta-zero R2d3 control happened to be \(-0.00003985\pm0.00001563\) in six chains; this supports **reporting all four comparisons** and a multiplicity adjustment instead of selecting favorable cases post hoc. The Gaussian/t approximation and estimated chain-to-chain variation remain exploratory; finite thermalization, serial dependence, unknown numerical roundoff accumulation and sample-mean centering bias have not been rigorously bounded.

## 5. Exact proof boundary and next independent acceptance

The original continuous SU2 beta-zero Haar mathematical theorem (VOL32), exact four-dimensional spherical pair geometry and offdiagonal split (VOL33), and previous analytic transfer bounds are unaffected. The VOL34 machine verifier accepts **only integer data-integrity and statistical arithmetic** of the six-source-group, 42 independent chain summaries, rounded to a declared factor of \(10^{12}\). The numerical C++ engine and individual floating Monte Carlo samples are provided as conversation downloads, not imported into the project's integer-only mathematical verifier.

**Stage achieved:** second independent continuous-SU2 numerical algorithm; successful gauge/action checks; fixed L6 beta-two nearest-slice replication; successful four-case direct-vs-pair histogram reconstruction; two provisional nonoverlap shell residual contrasts surviving the stated chain-based Holm correction.

**Open:** externally audited stationarity and autocorrelation error, larger even L radial finite-size study, original full L128 spherical field measurements at \(\beta=9^{12}\), proof of a **uniform upper Wilson correlation-decay rate**, beta(a), infinite-volume continuum construction, Gauss/winding sectors and all **eleven** remaining gates. A finite-volume positive connected correlation is separate from a physical continuum mass gap.

Internal verdict: **PASS as independently replicated exploratory finite-volume SU(2) data and fixed-point arithmetic checks; HOLD as continuum/mass-decay evidence.**
