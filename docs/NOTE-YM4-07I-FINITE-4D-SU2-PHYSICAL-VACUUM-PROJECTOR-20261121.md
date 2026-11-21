# YM4-07I — explicit physical vacuum-projector transport at \(\beta=64\) for original 4D SU(2)

**November 21, 2026.** [Frozen prediction-first HBP](PREDICT-YM4-07I-FINITE-4D-SU2-VACUUM-PROJECTOR-20261121.hbp) at commit \`cd50c0c592e9ae3d7ee1756adb0df79f1a3bd7ca\` precedes the checker. This work is stacked on [YM4-07H](NOTE-YM4-07H-ALLBETA-SU2-PETER-WEYL-CAP-20261121.md). It turns an **absolute** Peter–Weyl transfer truncation into a **physical relative vacuum spectral-projector comparison** at a fixed, genuine 4D continuous-SU(2) Wilson coupling \(\beta=64\), by selecting a sufficiently large exact power-of-three representation cutoff. The size is mathematically explicit but far beyond practical dense-matrix evaluation.

## 1. Original four-dimensional physical Hilbert space and uniform eigenvalue inequalities

Use the actual 4D Wilson transfer \(T=A^{1/2}BA^{1/2}\) and gauge projection \(P\) of [YM4-02c](LEMMA-0004-REFLECTION-TRANSFER.md) at spatial periodic side \(L=6\):
\[
V=216,\quad N_\ell=N_s=648,\quad\beta=64,\quad
\beta N_\ell=41472.
\]
The physical Hilbert space is \(PH\); the true \(T|_{PH}\) is positive, self-adjoint, compact, trace class, with simple Perron eigenvalue \(\lambda_0>0\), normalized physical vacuum \(\Omega\), and positive spectral separation \(\gamma=\lambda_0-\lambda_1\).

The [YM4-02d positive-kernel theorem](NOTE-YM4-02d-QUANTITATIVE-GAP.md), applied to the **full original SU(2) transfer**, proves
\[
\frac{\lambda_1}{\lambda_0}\le\tau,\qquad
\tau=\tanh(\beta N_\ell)=\tanh41472.
\]
Because \(1-\tanh x=2/(e^{2x}+1)\) and \(e<3\),
\[
1-\tau=\frac2{e^{82944}+1}>\frac1{3^{82944}}.
\]

Meanwhile the **true continuous-SU(2) Haar-cap Rayleigh floor** of YM4-07H, with \(k=8\) and \(r=1/64\), reads
\[
\lambda_0>\frac1D,\qquad
D:=3^{405}\bigl(3072\cdot8^3\bigr)^{648}
=3^{405}\,1572864^{648}.
\]
Combining these *independent accepted finite-lattice inequalities* gives an explicit **physical vacuum isolation floor**:
\[
\boxed{\quad
\gamma=\lambda_0-\lambda_1>
\underbrace{\frac1{D\,3^{82944}}}_{\displaystyle \gamma_{\rm floor}}>0.
\quad}
\]
The absolute value of this rational floor is extraordinarily small. Its importance here is that it is **strict and explicit** even at \(\beta=64\).

## 2. Genuine SU(2) Fourier cutoff and the ternary relative-error jump

As in YM4-07H, retain every Peter–Weyl matrix coefficient for each spatial link of dimension \(d\le N\), preserving the full spatial Wilson action and gauge invariance. Denote by
\[
T_N=A^{1/2}B_NA^{1/2},\quad
T_N^{\rm phys}:=T_N|_{PH}
\]
the resulting **finite-rank, positive physical transfer**, and use the universal rational operator approximation
\[
\boxed{\quad
\delta_N:=\|T|_{PH}-T_N^{\rm phys}\|_{\rm op}
\le\|T-T_N\|_1
<\widehat\delta_N
:=2N_\ell(N+1)(3/8)^N,\quad N\ge4\beta.
\quad}
\]
At \(\beta=64\), the condition is \(N\ge256\), so any of \(N=729,2187,6561,19683,\ldots\) is legitimate.

The **exact integer acceptance gate** is
\[
\widehat\delta_N<\frac{\gamma_{\rm floor}}{10^6}
\quad\Longleftrightarrow\quad
\boxed{\quad
10^6\cdot2\cdot648\cdot(N+1)\cdot3^{N+82944}
\cdot3^{405}\cdot1572864^{648}<8^N.\quad}
\]
This involves **integers only**, with no evaluated exponentials, logarithms, Bessel functions, rounded matrix spectra, or surrogate gauge group.

It gives the important **ternary cutoff jump**:

| SU(2) representation cutoff | Rational relative physical-gap gate |
|---:|---|
| \(N=3^{10}=59049\) | **HOLD** — the present upper bound does not meet the target |
| \(N=3^{11}=177147\) | **PASS** — \(\delta_N<\gamma_{\rm floor}/10^6\) |

There are \(N(N+1)(2N+1)/6\) retained matrix coefficients **per spatial link** and \(648\) links. Therefore this certificate shows **mathematical existence** of an explicit physical-sector finite-rank approximant; it does **not** claim a practical assembled transfer matrix or its calculated first excitation.

## 3. True gauge-invariant vacuum projector and first-level spectral enclosure

Write \(A_{\rm phys}=T|_{PH}\) and \(S=T_N^{\rm phys}\). Both are positive self-adjoint compact operators, and
\(\|A_{\rm phys}-S\|_{\rm op}\le\delta_N<\gamma/10^6\).
Let \(\lambda_0(S)\), \(\lambda_1(S)\) be the ordered eigenvalues of the **physical truncated operator**. The min–max principle gives
\[
|\lambda_j(A_{\rm phys})-\lambda_j(S)|\le\delta_N
\qquad(j=0,1,\ldots).
\]
Thus \(S\) has an **isolated simple** leading physical eigenvalue:
\[
\lambda_0(S)-\lambda_1(S)
\ge\gamma-2\delta_N>0.
\]
Write \(\Omega_N\) for its normalized physical Perron eigenvector (not assumed pointwise positive) and
\(\Pi=|\Omega\rangle\langle\Omega|\),
\(\Pi_N=|\Omega_N\rangle\langle\Omega_N|\) for the genuine physical vacuum spectral projectors.

Here is an **elementary independent projector proof**, avoiding a named perturbation theorem. Let \(Q=I-\Pi\), which reduces \(A_{\rm phys}\). The eigenvector equation
\(S\Omega_N=\lambda_0(S)\Omega_N\) gives
\[
(\lambda_0(A_{\rm phys})-A_{\rm phys})Q\Omega_N
=Q\Bigl[(\lambda_0(A_{\rm phys})-\lambda_0(S))\Omega_N
+(S-A_{\rm phys})\Omega_N\Bigr].
\]
On \(QPH\), the left operator is invertible with inverse norm at most \(1/\gamma\). Since \(|\lambda_0(A_{\rm phys})-\lambda_0(S)|\le\delta_N\), it follows that
\[
\|Q\Omega_N\|\le\frac{2\delta_N}{\gamma}.
\]
For two normalized rank-one projectors, \(\|\Pi-\Pi_N\|_{\rm op}=\|Q\Omega_N\|\) and \(\|\Pi-\Pi_N\|_1=2\|\Pi-\Pi_N\|_{\rm op}\). Hence the **true original SU(2) gauge-invariant vacuum-projector transport** satisfies
\[
\boxed{\quad
\|\Pi-\Pi_N\|_{\rm op}<\frac{2}{10^6}
=\frac1{500000}.\quad}
\]
This is an explicit **relative spectral-projector norm certificate** in the **actual finite-volume physical** SU(2) Hilbert space at \(\beta=64\). It uses the original kernel's accepted gap floor rather than a hypothetical truncation-specific gap.

The first excited eigenvalue obeys the *absolute* interval
\(|\lambda_1(T|_{PH})-\lambda_1(T_N|_{PH})|<\gamma_{\rm floor}/10^6\). The values of these eigenvalues have **not** been numerically computed; the theorem certifies how a future finite-rank calculation would transfer.

## 4. Matched Wilson-source vacuum amplitude and four-step correlator

Let \(F\) be multiplication by the normalized real fundamental Wilson trace of the genuine **fine 2×2 spatial rectangle**, the ordered pullback of a coarse plaquette. It is gauge invariant and \(\|F\|_{\rm op}\le1\). In the true and truncated **physical** vacuum states,
\[
m=\langle\Omega,F\Omega\rangle=\operatorname{Tr}(\Pi F),\quad
m_N=\langle\Omega_N,F\Omega_N\rangle=\operatorname{Tr}(\Pi_N F).
\]
The projector trace-norm inequality proves **without approximating either vacuum vector explicitly**
\[
\boxed{\quad |m-m_N|
\le\|\Pi-\Pi_N\|_1<\frac1{250000}.\quad}
\]

For the four-step **unnormalized transfer moment** of the matched Wilson source,
\[
c_4^{\mathrm{raw}}=\langle\Omega,F T^4F\Omega\rangle,\quad
c_{4,N}^{\mathrm{raw}}=\langle\Omega_N,F T_N^4F\Omega_N\rangle,
\]
the transfers use the same original Wilson normalization, with \(\|T\|,\|T_N\|\le1\). **This raw moment is not yet the physical time-separated vacuum correlator:** physical propagation requires dividing each transfer by its own leading physical eigenvalue. Telescoping and the trace-class ideal bound give
\[
\begin{aligned}
|c_4^{\mathrm{raw}}-c_{4,N}^{\mathrm{raw}}|
&\le\|\Pi-\Pi_N\|_1
+\|T^4-T_N^4\|_{\rm op}\\
&\le2\|\Pi-\Pi_N\|_{\rm op}+4\delta_N\\
&<\frac4{10^6}+\frac4{10^6}
=\boxed{\frac1{125000}}.
\end{aligned}
\]
This is an **explicit source-specific, true-vacuum, original four-dimensional continuous-SU(2) *unnormalized transfer-moment* error** at \(\beta=64\) for an exact Peter–Weyl cutoff. The full physical-time normalization and connected source are audited separately below. The numerical moment **value** is still OPEN: the finite-rank matrix and its vacuum were not built.


### 4.1. Post-freeze physical-time and vacuum-connected Wilson comparison — YM4-07I2

The original YM4-07I prediction and raw fourth-moment checker are retained unchanged. Before creating the new test, we froze the independent [YM4-07I2 normalized predictions](PREDICT-YM4-07I2-NORMALIZED-WILSON-CORRELATOR-20261121.hbp) at commit \`17e7a33346a201afefb61bd253803752adaec6a3\`. This extension addresses the indispensable **physical-time normalization**.

Let \(\alpha=\lambda_0(T|_{PH})\) and \(\alpha_N=\lambda_0(T_N|_{PH})>0\), and define
\[
\widetilde T=T|_{PH}/\alpha,\qquad
\widetilde T_N=T_N|_{PH}/\alpha_N.
\]
Both are positive contractions and correspond to the **same physical fine time step \(a\)**. The physical vacuum gap and Fourier cutoff from sections 1–3 yield
\[
\delta_N<\gamma_{\rm floor}/10^6,\quad
\alpha>1/D,\quad
\gamma_{\rm floor}=(1/D)3^{-82944},
\]
hence \(\delta_N/\alpha<3^{-82944}/10^6<10^{-6}\).

The **normalization error** is controlled by an exact two-term decomposition:
\[
\begin{aligned}
\|\widetilde T-\widetilde T_N\|
&\le \frac{\|T-T_N\|}{\alpha}
+\|T_N\|\,\biggl|\frac1\alpha-\frac1{\alpha_N}\biggr|\\
&\le\frac{\delta_N}{\alpha}
+\alpha_N\frac{|\alpha-\alpha_N|}{\alpha\alpha_N}
\le\frac{2\delta_N}{\alpha}
<\boxed{\frac1{500000}}.
\end{aligned}
\]
All operators in this display are restricted to \(PH\), and \(\|T_N|_{PH}\|=\alpha_N\). This shows that the large-\(\beta\) **physical normalized transfer semigroups** are close in operator norm for the selected exact representation cutoff, without asserting an actual finite-rank diagonalization.

For any bounded real gauge-invariant normalized Wilson loop \(F\) with \(\|F\|\le1\), define the **actual physical four-step vacuum correlators** and their vacuum-connected counterparts:
\[
\begin{aligned}
C_4&=\langle\Omega,F\widetilde T^4 F\Omega\rangle,
& C_{4,N}&=\langle\Omega_N,F\widetilde T_N^4F\Omega_N\rangle,\\
C_4^{\rm conn}&=C_4-\langle\Omega,F\Omega\rangle^2,
& C_{4,N}^{\rm conn}&=C_{4,N}-\langle\Omega_N,F\Omega_N\rangle^2.
\end{aligned}
\]
At the **same physical time separation \(4a\)**, telescoping normalized transfers and the rank-one vacuum projector bound give
\[
\begin{aligned}
|C_4-C_{4,N}|
&\le 4\|\widetilde T-\widetilde T_N\|
+\|\Pi-\Pi_N\|_1\\
&<4/500000+1/250000
=\boxed{\frac3{250000}}.
\end{aligned}
\]
Since the true and truncated Wilson means both lie in \([-1,1]\), their squared means differ by at most twice their absolute difference, i.e. \(<1/125000\). Therefore the **connected Wilson physical-time correlator error** satisfies
\[
\boxed{\quad
|C_4^{\rm conn}-C_{4,N}^{\rm conn}|
<\frac3{250000}+\frac1{125000}
=\frac1{50000}.
\quad}
\]

These are **rigorous approximation-error upper bounds for actual connected, physical-time Wilson correlation functions** at the stated finite lattice and \(\beta=64\), based on genuine continuous SU(2), gauge-invariant physical transfer, the original full spatial Wilson action and a large exact Fourier cutoff. We have **not** computed either connected correlator value, produced an original first-excited Wilson spectral weight, established an infinite-volume/UV limit, or inferred the continuum physical mass gap.

## 5. Independent limitations and next mathematical producer

The new certification closes a very specific finite-lattice gate: **relative top physical vacuum projector and Wilson correlator continuity under the exact high-β temporal Peter–Weyl cutoff**. Its efficiency is extremely poor: the necessary retained representation dimension is \(177{,}147\) *per spatial link*, and there are 648 links. The certificate relies on an exceptionally small known fixed-volume gap lower bound.

At the fixed coupling/volume here, the theorem does **not** compute the finite-rank spectrum, prove Wilson overlap with the **lowest excited eigenstate**, reconstruct the full time-dependent source spectrum, or establish uniformity when \(L\to\infty\) and \(\beta(a)\to\infty\). It does **not** certify the true 4D continuum mass gap. The unresolved nonperturbative RG induction and nontrivial OS continuum reconstruction are unchanged.

The next efficient producer needs a **character-sparse / gauge-invariant representation-network evaluator**, a substantially sharper physical vacuum and excited-sector estimate, and a **cutoff-and-volume-uniform** proof that its relative errors remain controlled. The exact rational upper-envelope method here establishes that such a finite-rank target can in principle approximate a fixed physical transfer to an explicitly certified norm.

**Acceptance ledger:** original 4D SU(2) physical vacuum projector **ANALYTIC FINITE-VOLUME**, exact rational cutoff predictions **FROZEN**, integer checker and hosted CI **TO VERIFY**, independent proof review **TO VERIFY**; finite-rank eigenvalue computation, running-coupling continuum OS construction and full gap **OPEN**.
