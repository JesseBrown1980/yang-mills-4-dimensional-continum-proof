# YM4-07F — dark-sector spectral trace budget, small-Gram witness jumps, and continuous SU(2) calibration

**November 21, 2026.** This is the next exact, matrix-free candidate after [YM4-07E](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/76). Predictions were frozen **before** the new checker in [TRACE HBP](PREDICT-YM4-07F-TRACE-BUDGET-20261121.hbp), commit \`a0a4dd7fa06e20c93ab2fc15ed0978aba02d83fb\`, and [SU(2) HBP](PREDICT-YM4-07F-SU2-CLASS-CONTROL-20261121.hbp), commit \`5171b5c0864d1d99c87edaaf1a227f7b1b7f03f3\`.

The result turns the *unseen physical-energy spectrum* into a **positive transfer-trace residual** from a few coarse Wilson-network witnesses. Its first completely computed genuine continuous-SU(2) instance is a **one-link central convolution on class functions at \(\beta=1\)**. The actual four-dimensional weak-coupling trace and Wilson Gram inputs remain future production obligations.

## 1. Exact theorem — the dark spectrum from a finite Gram pencil

Let \(\mathcal H\) be the gauge-invariant physical OS Hilbert space at fixed finite spatial volume, and let \(T\) be a positive, self-adjoint, trace-class transfer operator with simple maximal eigenvalue \(\lambda_0>0\) and normalized vacuum \(\Omega\). These are the finite Wilson transfer hypotheses recorded in YM4-02/03. Write \(A=T/\lambda_0\), a positive contraction, and let \(\mathcal K\subseteq\mathcal H\) be any closed **reducing subspace for \(T\)** containing \(\Omega\). YM4-07E supplies such a \(\mathcal K\) from the chosen coarse spatial-slice Wilson-network algebra in its specified infinite-time vacuum representation.

Choose linearly independent witness vectors \(v_1,\ldots,v_d\in\mathcal K\), including \(\Omega\), and set \(E=\operatorname{span}\{v_i\}\). For any integer \(m\ge1\), form the **small positive Gram and moment matrices**
\[
G_{ij}=\langle v_i,v_j\rangle,\qquad
M_{ij}^{(2m)}=\langle v_i,A^{2m}v_j\rangle,\qquad
G>0.
\]
Define the exact trace residual
\[
\boxed{\mathcal R_{2m}(E)
=\operatorname{Tr}(A^{2m})-\operatorname{tr}(G^{-1}M^{(2m)}).}
\]
Let \(V:\mathbb C^d\to\mathcal H\) send the standard basis to the \(v_i\). The orthogonal projector onto \(E\) is \(P_E=VG^{-1}V^*\). Cyclicity of the trace gives
\[
\operatorname{tr}(G^{-1}M^{(2m)})
=\operatorname{Tr}(P_E A^{2m}),\qquad
\mathcal R_{2m}(E)=\operatorname{Tr}((I-P_E)A^{2m})\ge0.
\]
Since \(E\subseteq\mathcal K\), \(0\le P_{\mathcal K^\perp}\le I-P_E\). Since \(\mathcal K\) reduces \(A\), positivity and trace monotonicity yield
\[
0\le\operatorname{Tr}((A|_{\mathcal K^\perp})^{2m})
\le\mathcal R_{2m}(E).
\]
The largest singular value of a positive trace-class operator cannot exceed the positive \((2m)\)-Schatten norm. Hence
\[
\boxed{\quad
\|A|_{\mathcal K^\perp}\|^{2m}\le\mathcal R_{2m}(E).
\quad}
\]

**Binary acceptance gate:** for any rational \(q\in(0,1)\),
\[
\boxed{\quad\mathcal R_{2m}(E)<q^{2m}
\quad\Longrightarrow\quad
\operatorname{spec}(A|_{\mathcal K^\perp})\subset[0,q).\quad}
\]
Thus the dark sector has no physical-energy support in \((0,-a^{-1}\log q]\) after the vacuum is removed. This statement includes the endpoint since the spectral radius is **strictly** below \(q\); it does **not** infer any bound on \(\mathcal K\cap\Omega^\perp\). Combining this dark-sector certificate with an independent cyclic-sector bound \(\|A|_{\mathcal K\cap\Omega^\perp}\|\le q\) proves the *whole finite-volume* gap \(\Delta\ge -a^{-1}\log q\).

**Vacuum handling:** if \(\Omega\notin E\), then \(\mathcal R_{2m}(E)\ge1-\|P_E\Omega\|^2\). For reliable large-\(m\) certificates, \(\Omega\) must be included or its missing contribution rigorously bounded. A passing finite-moment experiment with unknown vacuum normalization cannot silently omit this term.

## 2. Unnormalized transfer and exact Wilson witness increments

The criterion does not require first dividing by an unknown \(\lambda_0\). For the unnormalized transfer, define
\[
R_{2m}^T(E)=\operatorname{Tr}(T^{2m})
-\operatorname{tr}\big(G^{-1}M_T^{(2m)}\big),\qquad
(M_T^{(2m)})_{ij}=\langle v_i,T^{2m}v_j\rangle.
\]
If \(L>0\) is a **certified lower bound** on \(\lambda_0\), then
\[
\boxed{\ R^T_{2m}(E)<(qL)^{2m}\quad\Longrightarrow\quad
\|T|_{\mathcal K^\perp}\|<q\lambda_0.\ }
\]
This avoids subtracting two differently rescaled estimates of the normalized transfer trace. It is particularly appropriate for independently enclosed Perron eigenvalues.

An added independent witness \(w\in\mathcal K\) has Schur residual \(u=(I-P_E)w\). When \(u\ne0\), orthogonal projection gives the exact **witness jump law**
\[
\boxed{\quad
\mathcal R_{2m}(E+\mathbb Cw)
=\mathcal R_{2m}(E)
-\frac{\langle u,A^{2m}u\rangle}{\langle u,u\rangle}.
\quad}
\]
The decrease is nonnegative; the small Gram matrix records it exactly even when \(w\) is strongly correlated with existing witnesses. **Never** subtract individual normalized moment quotients of nonorthogonal witnesses without the Gram inverse.

### Transfer-moment provenance in genuine four dimensions

For the original continuous-SU(2) four-dimensional Wilson lattice at fixed spatial volume, \(\operatorname{Tr}(T^{2m})\) is represented by the appropriately normalized *periodic Euclidean-time* partition function with \(2m\) slices and the correct gauge projection, as recorded in YM4-03. The witness entries \(\langle F_i(Q)\Omega,T^{2m}F_j(Q)\Omega\rangle\) are **vacuum-limit** Wilson-network correlators of the exact SU(2) measure, not finite-temperature correlators at one fixed temporal extent. The required normalization, continuum Haar integrations, Perron lower bounds and certified truncation tails must be included in the production receipts; the current PR supplies their exact acceptance inequality, not numerical four-dimensional values. Physical time step \(a\) must remain explicit. Temporal extents \(2m\ge4\) are preferred for production to avoid short-period plaquette coincidences.

## 3. Exact rational dark-state falsifier and a one-witness jump

Take the positive rational transfer model
\[
A=\operatorname{diag}(1,3/4,1/2,1/4),\quad
\mathcal K=\operatorname{span}(e_0,e_2),\quad
E=\operatorname{span}(e_0,e_0+e_2).
\]
The **nonorthogonal** Gram matrix is
\[
G=\begin{pmatrix}1&1\\1&2\end{pmatrix},\qquad
G^{-1}=\begin{pmatrix}2&-1\\-1&1\end{pmatrix}.
\]
The exact trace subtraction equals \(1+(1/2)^{2m}\), leaving
\[
\mathcal R_{2m}(E)=(3/4)^{2m}+(1/4)^{2m}.
\]
The frozen exact results are:

| Moment power | Witnesses | Residual | Threshold \(q\) | Verdict |
|:---:|---|---:|:---:|---|
| 2 | vacuum only | \(7/8\) | \(4/5\) | HOLD |
| 2 | vacuum + blocked witness | \(5/8\) | \(4/5\) | PASS |
| 4 | vacuum + blocked witness | \(41/128\) | \(4/5\) | PASS |
| 8 | vacuum + blocked witness | \(3281/32768\) | \(4/5\) | PASS |
| 2 | vacuum + blocked witness | \(5/8\) | \(3/4\) | HOLD |

The Schur witness increment at power 2 is exactly \(1/4\), moving a HOLD to PASS without constructing a larger operator. The true dark radius is \(3/4\), so the strict \(q=3/4\) gate must fail.

For an unnormalized \(T=4A\), \(\lambda_0=4\) and \(R_2^T=10\): a certified \(L=4\) passes \(q=4/5\), while a weaker \(L=3\) leaves the same gate on HOLD. These exact controls expose insufficient Perron floors rather than silently improving them.

## 4. Genuine continuous-SU(2) group calibration at \(\beta=1\)

To check the transfer-trace method on a **continuous group**, take the central convolution operator
\[
(Cf)(g)=\int_{\mathrm{SU}(2)}
e^{\operatorname{ReTr}(gh^{-1})/2}f(h)\,dh
\]
on the Haar **class-function** Hilbert space. It is a positive, self-adjoint, trace-class operator. Its orthonormal character eigenvectors \(\chi_n\) correspond to irreducible representation dimensions \(n=1,2,\ldots\). Character orthogonality and the Wilson character expansion give
\[
C\chi_n=2I_n(1)\chi_n,\qquad
A:=C/(2I_1(1)),\qquad
t_n:=I_n(1)/I_1(1).
\]
The vacuum is \(\chi_1=1\); the first Wilson-trace mode is \(\chi_2\). Define \(E=\mathcal K=\operatorname{span}(\chi_1,\chi_2)\). This two-channel reducing space is a **calibration**, not a claim that it is the entire Wilson-network cyclic algebra in four dimensions.

The exact modified-Bessel positive series is
\[
I_n(1)=\sum_{k\ge0}\frac{1}{2^{n+2k}k!(n+k)!}.
\]
The elementary strict inequality \(e^{1/4}<4/3\), together with
\(I_1(1)\ge1/2\), gives
\[
0<t_n<\frac{4}{3}\frac{2^{1-n}}{n!}.
\]
Hence for the **actual infinite-dimensional, continuous-SU(2) class-function operator**, the full dark trace at power two satisfies
\[
\begin{aligned}
R_2&=\sum_{n=3}^\infty t_n^2
<\sum_{n=3}^\infty\frac{16}{9}\frac{4^{1-n}}{(n!)^2}\\
&\le \frac1{324}\sum_{k=0}^\infty(1/64)^k
=\boxed{\frac{16}{5103}}<\frac1{100}.
\end{aligned}
\]
The ratio inequality uses the exact successive ratio \(1/[4(n+1)^2]\le1/64\) for \(n\ge3\). Consequently
\[
\boxed{\ \|A|_{\mathcal K^\perp}\|<1/10.\ }
\]
This is a certified spectral tail bound for a **genuine continuous-SU(2) transfer operator**, using only integer and rational inequalities plus the analytic character-series identity.

The **visible** first Wilson-trace eigenvalue satisfies
\[
\frac{3}{16}<t_2<\frac13,
\]
by \(I_2(1)\ge1/8\), \(I_2(1)<1/6\), \(1/2\le I_1(1)<2/3\). Thus \(q=1/10\) passes for the **dark** modes but fails for the full class spectrum. Combining the actual visible bound \(t_2<1/3\) with the certified dark bound \(<1/10\) proves a **strict class-function convolution spectral gap**
\[
\boxed{\quad\Delta_{\mathrm{class}}>\log(3)/a_{\mathrm{step}}\quad}
\]
at \(\beta=1\) for this one-link model. This is a one-link calibration of the certificate machinery; the four-dimensional physical Yang–Mills Hamiltonian, weak-coupling continuum limit and volume-uniform full-spectrum bound remain separate.

## 5. Four-dimensional production target and stop rules

To apply the theorem to the real four-dimensional Wilson transfer in YM4-04/06, the producer must:

1. Freeze the genuine continuous-SU(2) original Wilson transfer normalization, spatial volume, temporal extent, \(\lambda_0\) enclosure and gauge projector.
2. Obtain **rigorous upper** bounds for \(\operatorname{Tr}T^{2m}\) from the periodic-time Wilson integral, **rigorous exact/enclosed** \(d\times d\) Gram/moment inputs from the matched blocked Wilson-network time-slice sources, and a certified \(L\le\lambda_0\).
3. Prove the residual upper envelope \(R^T_{2m}(E)<(q(a)L)^{2m}\), including all rational/analytic tail allowances. Add a Schur-residual witness if the inequality is on HOLD; never silently drop the unobserved trace.
4. Separately prove the cyclic excited-spectrum bound \(\|A|_{\mathcal K\cap\Omega^\perp}\|\le q(a)\), and choose \(q(a)\le e^{-a\Delta_*}\) in physical units.
5. Establish that the bounds persist as spacing \(a\to0\) **and** spatial volume increases, with the nontrivial OS continuum reconstruction obligations independently discharged.

This route avoids constructing an explicit basis for the entire dark Hilbert space. Its cost is a **full transfer-trace upper bound** and reliable subtraction; when the trace budget is too large, the result is a certified **HOLD**, not a full-gap claim. No four-dimensional numerical trace receipt is claimed in this PR.

**Acceptance status:** abstract positive-transfer dark-trace theorem **DERIVED**; finite rational matrix controls **EXACT**; continuous-SU(2) one-link class-convolution calibration **ANALYTIC + RATIONAL**; full four-dimensional weak-coupling transfer input **OPEN**; nontrivial continuum and full physical mass gap **OPEN**.
