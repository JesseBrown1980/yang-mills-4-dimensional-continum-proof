# YM4 VOL32 — independent-method audit of exact original SU(2) Haar shell covariance

**24 November 2026 · internal analytic proof review, not an external signed referee report.**

## A. Confirm the physical model: PASS

At beta=0, the **actual original periodic Wilson Gibbs measure** on L=128 is normalized product Haar on all independent original SU(2) positive links. The gauge-field configuration is not a finite subgroup, a 24-point quadrature approximation, or a geometric point cloud. Each original 0–1 spatial elementary plaquette \(U_{p_x}\) is a product of four distinct Haar SU(2) links/inverses, thus itself Haar-distributed. Its quaternion scalar is real trace/2. Its continuous SU(2) Haar first moment is zero and its second moment is \(1/4\), giving centered \(F_x=(1+\operatorname{Re}U_{p_x})/2\) mean \(1/2\) and variance \(1/16\).

## B. Distinct same-orientation plaquette orthogonality: PASS

For any two original positive 0–1 plaquettes at distinct starting sites x,y on L=128, their oriented four-link edge sets differ. At least one positive link occurs in the first plaquette but not the second. The product of the two traces is linear in the fundamental matrix representation of this link (or its inverse), while the second plaquette trace is independent of it. Normalized SU(2) Haar integration of a single fundamental representation coefficient equals zero. Therefore
\(E_H[\operatorname{Re}U_{p_x}\operatorname{Re}U_{p_y}]=0\) for x≠y, even if the plaquettes share one or more other links. At x=y, the Haar second moment is \(1/4\). Pairwise uncorrelated is sufficient; full probabilistic independence of different plaquette traces is neither needed nor claimed.

This argument is specific to the original Wilson elementary 0–1 plaquettes and L>=4, and is exact for the observed L128 geometry; it is not a claim about general intersecting loops.

## C. Exact two-ended shell-average covariance: PASS

Both 4D integer shell sets have N_R different original plaquette starting addresses (periodically injective since L=128, r<=21 and outer offset24). Exactly J_R addresses coincide. The covariance matrix of the individual bounded Wilson fields is diagonal \(1/16\), hence
\(\operatorname{Var}(M_R^c)=1/(16N_R)\),
\(\operatorname{Cov}(M_R^c,M_R^z)=J_R/(16N_R^2)\),
and the Pearson correlation \(J_R/N_R\).
At R12 the first nonzero correlation is 1/312; at R16 it vanishes, since the shells have no shared integer site; at R21 it equals 8/247. The exact 24-cell radius sequence R=2,4,8,16 has N=24 and fixed shell-average variance 1/384. All 20 N and J counts are independently recomputed by the strict integer verifier; rational covariance arithmetic is exact, with no floating division or sampling errors.

**Crucial physical distinction:** This exact nonzero correlation arises from shared *identical Wilson plaquettes*. At beta=0, nonoverlapping distinct plaquettes are uncorrelated and there is no interacting gauge-field propagation. These new shell-average covariances are **different observables** from VOL30's predictor variances \(W_R=\operatorname{Var}(E[G\mid I_R(c)])\). At beta=0 and radius R<=21<d=24, the distant individual source G uses links outside the center ball, so its conditional predictor is constant and \(W_R=0\). The overlapping shell-averages may still have \(J_R/N_R>0\). Their distinct behavior is mathematically consistent.

## D. All-beta translation control: PASS

For any finite beta, the original periodic Wilson measure and the same orientation 0–1 plaquette definition are translation invariant. Thus the one-point expectation \(E_\beta[F_x]\) is independent of x, and every finite shell average has the same expected value. This holds at beta=9^12 but does **not** calculate the unknown production-coupling mean. Any apparent ensemble one-point radial banding would require a broken symmetry, systematic numerical error, selection bias or a different observable.

Connected shell correlation at beta>0 is the exact double sum of true two-point \(K_\beta(y-x)\) over both sets, with the common-site overlap only the diagonal contribution. Physical dynamical information lies in the off-diagonal terms. The exact Haar formula describes the beta=0 limit and cannot be extrapolated numerically to production coupling without new proof or measurement.

## E. Numerical pilot boundary — separate provisional observation

The exploratory L4/L6 finite-beta single-link heatbath experiment is documented in [VOL32 pilot note](../docs/certificate-atlas/NOTE-YM4-VOL32-EXPLORATORY-SU2-HEATBATH-PILOT-20261124.md). The staple-action and local gauge tests passed, and beta2 showed a positive nearest-time-slice connected Wilson correlation on both small lattices. These decimal estimates use floating arithmetic and three finite chains; they have not been certified by the integer-only mathematical verifier, represent no L128 radial shell measurement and cannot establish continuum mass decay. They are not entered into VOL32 HBP.

## F. Review conclusion

**Analytic PASS:** exact original continuous-SU2 beta-zero Wilson shell means/variances/correlations on all 20 two-ended 4D spherical frames, exact 24-cell sampling variance fingerprint, and all-beta translation symmetry of one-point means. The result is not equivalent to an interacting mass-gap phenomenon.

**HOLD:** original beta9^12 two-point \(K_\beta\) measurements at 4D radial displacements, the conditional spherical predictor \(W_R\) at positive coupling, nonzero beta(a) continuum scaling, the upper physical mass rate, the eleven continuum construction obligations and independent externally signed proof acceptance.

Keep the beta-zero Haar theorem, the finite-beta numerical pilot and the 24-cell geometry under separate atlas labels and proof dependencies.
