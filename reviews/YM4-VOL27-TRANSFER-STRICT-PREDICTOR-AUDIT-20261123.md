# YM4 VOL27 — independent-method mathematical audit of strict Wilson exterior prediction

**23 November 2026 · internal mathematical audit on research draft PR #113.** The scope is the original pure SU(2) continuous-Haar Wilson model and the centered source of VOL26. This check derives VOL27's key sign claim through a **separate transfer/eigenvalue route**, away from VOL21's single-shell density minorization. It is an internal audit, not a signed external referee report or a computer-formal proof.

## 1. Hypotheses and original geometric placement — PASS

- Original even periodic four-dimensional SU(2) Wilson action \(\beta\sum_p\operatorname{Re}U_p\), normalized product Haar, and finite \(\beta>0\).
- The centered spatial 0–1 plaquette sits on slice \(x_2=0\); choose \(d=r+1\) and the translated 0–1 plaquette on \(x_2=d\). All four translated links have \(x_2>r\), hence lie in the true exterior sigma-field of \(T_r\). For even \(L\ge2(2r+3)\), neither support wraps into the other. The exact checker enumerates r=1–4; the coordinate inequalities prove all r.
- \(F=(1+\operatorname{Re}U_p)/2\) is real, bounded [0,1], gauge invariant, and nonconstant on every spatial-link Hilbert configuration space (continuous plaquette holonomy can vary freely).

## 2. Kernel positivity and Gauss projection — PASS (classical proof input identified)

Set \(k_\beta(g)=\exp[(\beta/2)\chi_{1/2}(g)]\). The SU(2) representation ring gives
\[
 \chi_{1/2}^{n}=\sum_j m_{n,j}\chi_j,\quad
 m_{n,j}\in\mathbb N_0,\quad m_{2j,j}=1.
\]
Every character coefficient of \(k_\beta\) is therefore **strictly positive** at finite \(\beta>0\), and its Peter–Weyl convolution eigenvalue is the coefficient divided by \(2j+1\). This is strict \(L^2\) positivity because Peter–Weyl matrix coefficients form a complete orthonormal basis, not because the kernel is pointwise positive.

In the original temporal direction 2, the transfer factors as \(T=M_{V^{1/2}}\,P K_\beta P\,M_{V^{1/2}}\). The scalar spatial multiplier and its inverse are bounded and positive on the finite compact configuration space, and preserve gauge invariance. Therefore for every nonzero **physical gauge-invariant** vector f, \(\langle f,Tf\rangle>0\); the temporal gauge averaging P does not introduce a physical null vector. Positive character coefficients are summable in dimension-weighted trace, so the finite-spatial-volume convolution and T are positive trace-class. This agrees with M. Lüscher's classical strictly positive Wilson transfer construction (Commun. Math. Phys. 54 (1977), 283–292, DOI 10.1007/BF01614090); the connected pure-gauge finite periodic temporal-trace law includes P and the Wilson spatial half-weights.

**Safeguard:** a strictly positive compact operator can have eigenvalues approaching zero. No bounded inverse, no spectral gap and no quantitative beta(a) mass rate follows from strict positivity alone.

## 3. Nonzero centered-source exterior predictor — PASS

With \(A=M_F-\mu(F)I\) and \(Z_L=\operatorname{Tr}(T^L)>0\), the true periodic thermal trace obeys
\[
 C_d=\operatorname{Cov}(F_0,F_d)
 =Z_L^{-1}\operatorname{Tr}(A T^d A T^{L-d})
 =Z_L^{-1}\sum_{i,j}\lambda_i^{L-d}\lambda_j^d|A_{ij}|^2.
\]
Every term is nonnegative; all \(\lambda_i>0\) and \(A\ne0\), so **the sum is strictly positive** for \(0<d<L\). The conclusion applies at \(\beta=9^{12}\) with no extrapolation and no numerical integration.

Since \(F_d\) is exterior-measurable, \(\operatorname{Cov}(F_0,F_d)=\operatorname{Cov}(E[F_0\mid\mathcal E_r],F_d)\). With \(\operatorname{Var}(F_d)\le1/4\) and finite \(\operatorname{Var}(F_0)>0\),
\[
 V_r\ge4 C_{r+1}^2>0.
\]
The exact VOL15 conditional law implies \(E[F_0\mid\mathcal E_r]=\phi_r(B_r)\). VOL22's independent finite-beta strict shell minorization then establishes \(D_r\ge e^{-4\beta s_r}V_r>0\).

## 4. Log-convex signal propagation — PASS

Spectral factors give a positive discrete measure \(\sum w_{ij}\delta_{\lambda_j/\lambda_i}\) with total mass \(C_0=\operatorname{Var}(F_0)>0\) and moments \(C_d\). Cauchy–Schwarz proves \(C_d^2\le C_{d-1}C_{d+1}\). Jensen gives
\(C_d\ge C_0(C_1/C_0)^d\).
All quantities are true original-periodic connected Wilson correlations; no assumption about high-beta exponential *upper* decay has been inserted.

The attached exact-rational two-state transfer fixture verifies the independent spectral-trace and log-convex identities: eigenvalues (3,1), L=6,d=2, \(C_0=1/4,\ C_1=123/1460,\ C_2=9/292\), \(C_0C_2-C_1^2=81/133225>0\). At rank-one beta-zero T, the distant covariance vanishes. This fixture is a test of **spectral algebra only**, not a numeric SU(2) transfer model.

## 5. Remaining acceptance and sign-off boundaries

**Accepted analytically in the original continuous SU(2) finite Wilson theory (subject to traditional transfer assumptions):** \(V_r>0\) and \(D_r>0\) for every beta>0 on the specified even periodic volumes, including production beta=9^12.

**Still OPEN:** any explicit production-coupling numerical lower enclosure for \(C_1/C_0\), the quantitative source-normalized *upper* decay/mass criterion \(\kappa_r\ge1-e^{-2ma}\), proved beta(a) scaling, renormalized nonzero continuum source, full continuum winding/Gauss-sector reconstruction, and all eleven continuum gates. The transfer proof supplies the sign and a local quantitative target. A different, independently signed mathematical referee review and native Lean formal acceptance remain separate obligations.

No modifications to main or the published 3D atlas are implied by this research-stage review.
