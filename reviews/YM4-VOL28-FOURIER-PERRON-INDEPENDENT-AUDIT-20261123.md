# YM4 VOL28 — independent-method review of explicit nearest-slice SU(2) lower margin

**23 November 2026 · internal mathematical audit, separate from the implementation checker.** Reviews [VOL28's finite-volume original continuous-SU(2) Fourier–Perron proof](../docs/certificate-atlas/NOTE-YM4-VOL28-NEAREST-SLICE-MARGIN-20261123.md) against VOL27's classical positive transfer theorem. This is a mathematical cross-check and acceptance-boundary inventory, **not** independent signed human referee approval or Lean formal verification.

## Original model and full physical transfer — PASS subject to the classical construction

- The time direction is coordinate 2. An L³ spatial slice has exactly E=3L³ positive links and Q=3L³ plaquettes; original centered 0–1 plaquette uses four distinct spatial links when L>=10.
- SU(2)'s Wilson one-step transfer \(T=V^{1/2}PK_\beta PV^{1/2}\) acts on the **complete physical gauge-invariant link Hilbert space**, with site-gauge projector P, positive convolution kernel \(K_\beta\), and true spatial Wilson action V. This is the classical Lüscher 1977 input also used in VOL27. Winding holonomies remain present; the continuum all-Gauss-sector question remains separate.
- The double gauge average \(PK_\beta P\) has a continuous **pointwise positive** kernel between \(e^{-\beta E}\) and \(e^{\beta E}\). Multiplication by \(V^{1/2}\in[e^{-\beta Q/2},e^{\beta Q/2}]\) yields the global transfer-kernel bounds in VOL28 (28.9). The spatial-link normalized Haar reference is crucial: \(\sup\Omega\ge1\) for an L²-normalized positive Perron vector.

## Independent control of Perron and trace inequalities — PASS

- The positive compact integral operator T admits a normalized strictly positive maximal eigenvector \(\Omega\). From the positive kernel's ratio bound,
  \(\inf\Omega\ge e^{-2\beta(E+Q)}\), and
  \(\inf V^{1/2}\Omega\ge e^{-\beta(2E+5Q/2)}\).
  This is an all-link, **volume-dependent** Harnack bound; its large exponent is explicit rather than silently omitted.
- \(\operatorname{Tr}T\le e^{\beta Q}\operatorname{Tr}PKP
  \le e^{\beta(E+Q)}\).
  The first step uses the positive trace-class P K P and \(V\le e^{\beta Q}I\); the second uses the orthogonal projector and \(K\ge0\), \(\operatorname{Tr}K=e^{\beta E}\). The inverse transfer operator is never used.
- In the periodic spectral sum, choose all terms whose left eigenindex is the top eigenvector. Then
  \(\operatorname{Tr}(S T S T^{L-1})\ge
   \lambda_0^{L-1}\langle\Omega,S T S\Omega\rangle\).
  Since \(\operatorname{Tr}T^L\le\lambda_0^{L-1}\operatorname{Tr}T\),
  the lower bound \(C_1\ge\langle\Omega,S T S\Omega\rangle/\operatorname{Tr}T\) is rigorous. No term-by-term sign cancellation can occur because the transfer eigenvalues are strictly positive.

## Independent SU(2) Fourier/Haar check — PASS

- For a single central plaquette, its group product is Haar-uniform in the original product-link reference, giving \(\int p\,dH=0,\ \|p\|_2^2=1/4\).
- The one-link SU(2) *central* convolution eigenvalue for a fundamental matrix coefficient is \(\int e^{\beta\operatorname{Re}u}\operatorname{Re}u\,dH=a_0A_\beta\). Four different original spatial links yield \(Kp=a_0^E A_\beta^4 p\). The constant eigenvalue is \(a_0^E\). The unknown thermal mean \(m\in[0,1]\) changes only the constant-mode amplitude of \(S=F-m\); the Fourier inverse on the **two-dimensional test subspace** costs at most \(5/(16a_0^EA_\beta^4)\). This finite-subspace inverse has no compact-spectrum domain ambiguity.
- With \(g=V^{1/2}S\Omega\), the test overlap is \(\langle g,S\rangle=\int V^{1/2}\Omega S^2\,dH\ge
e^{-\beta(2E+5Q/2)}/16\). Positive Fourier Cauchy–Schwarz gives \(\langle g,Kg\rangle\ge a_0^E A_\beta^4 e^{-\beta(4E+5Q)}/80\). The factor **80** was independently obtained as \(256\times5/16\).
- The exact one-dimensional SU(2) Riccati equation for \(A_\beta=I_2/I_1\) has strict lower barrier \(B_\beta=\beta/(\beta+4)\), because at a crossing the vector-field derivative excess is \(5\beta/(\beta+4)^2>0\); \(A_\beta=\beta/4+O(\beta^3)\) near the origin. Therefore \(A_\beta\ge1/2\) at beta>=4.
- The exact S³ Haar latitude density gives \(\Pr(1-\operatorname{Re}U\le1/\beta)>1/(3\beta^2)\) at beta>=1. Multiplication by the minimum Boltzmann factor on that cap gives \(a_0>e^\beta/(9\beta^2)\). This is an all-beta **continuous-group** inequality rather than a sampled bound.

## Production exponent and total volume dependence — PASS, with explicit limitation

Collecting the preceding terms gives
\[
 C_1>\frac{a_0^EA_\beta^4}{80 e^{\beta(5E+6Q)}}
   >\frac{e^{-\beta(4E+6Q)}}{1280(9\beta^2)^E}.
\]
For E=Q=3L³, the exponential factor is exactly \(e^{-30\beta L^3}\). At beta=9¹²=3²⁴, \(9\beta^2=3^{50}\), and \(e<3\). Thus
\[
 C_1/C_0>1/(320\cdot3^{(30\beta+150)L^3}),\qquad
 (30\beta+150)=8472886094580.
\]
For L=10, exponent=8472886094580000; the integer verifier also checks the minimal even lattices L=14/18/22 of centered r=2/3/4. This is an *extremely small* but completely explicit actual-original-SU(2) numerical lower enclosure. It deteriorates with spatial volume, so no infinite-volume source lower margin follows.

The checker also supplies an **independent rational 2x2 spectral analog**, not a native SU(2) simulation: positive kernel \(T=\begin{pmatrix}3&1\\1&3\end{pmatrix}\), eigenvalues (4,2), even trace length 6, and centered bounded insertion \(S=\operatorname{diag}(1,-1)/2\). It has exact \(C_1=17/130>1/12=\langle\Omega,S T S\Omega\rangle/\operatorname{Tr}T\). This falsifies the key spectral/trace orientation if reversed.

## Next mathematical acceptance boundary

- **PASS analytic finite-volume theorem:** explicit \(C_1/C_0\) lower bound for every original even periodic L>=10 at production beta=9¹². The result is fully native continuous SU(2); only its integer inputs and a rational spectral analog are machine-checked.
- **OPEN:** spatial-volume-independent lower bound on the nearest-slice correlation and physically meaningful lower margin as L grows. The global Perron infimum in (28.10) and the global trace upper bound are the precise bottlenecks.
- **OPEN (independent objective):** uniform **upper** source-to-exterior correlation decay / VOL20 \(\kappa_r\ge1-e^{-2ma}\) along a correctly established beta(a), nontrivial renormalized continuum source, full winding/Gauss transfer, and all eleven continuum-construction gates.

Keep as research-candidate evidence on draft PR #113. Do not change production 3D atlas or main without the independent human mathematical review and accepted proof-dependency gates.
