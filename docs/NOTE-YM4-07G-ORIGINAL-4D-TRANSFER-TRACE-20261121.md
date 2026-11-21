# YM4-07G — first original four-dimensional continuous-SU(2) transfer-trace certificate and Wilson-source Gram floor

**November 21, 2026.** [Prediction HBP frozen before the new checker](PREDICT-YM4-07G-ORIGINAL-4D-TRANSFER-20261121.hbp), commit \`50aa5c56f39e4b965f71c85d268d2cd16b449b40\`. This is the first direct **four-dimensional original Wilson transfer** test of the small-trace spectral budget in [YM4-07F](NOTE-YM4-07F-DARK-TRACE-GRAM-CERTIFICATE-20261121.md). The calculations below use genuine normalized Haar SU(2), full gauge projection, the positive Wilson transfer, and a genuine spatial 2×2 rectangular Wilson loop on a 6³ lattice. All constants are analytic with exact rational checking; no discretization of SU(2) is substituted.

**Scope:** a finite spatial volume and an extremely small bare coupling \(\beta=1/(2000V)\), \(V=L^3\). This is a **very-strong-coupling proof-of-method**. Its finite-volume gap is already covered more strongly by the positive-kernel contraction theorem in [YM4-02d](NOTE-YM4-02d-QUANTITATIVE-GAP.md). The new deliverables are a direct four-dimensional **trace-budget** calculation in the genuine transfer normalization and a positive-beta Wilson-source **cyclic Gram determinant floor**. A weak-coupling renormalized trajectory and the volume-uniform continuum gap remain separate objectives.

## 1. The genuine four-dimensional transfer and its four-slice trace

Let the spatial lattice be \((\mathbb Z/L\mathbb Z)^3\) with \(L\ge6\) even, and write \(V=L^3\). There are
\[
N_\ell=3V\quad\text{spatial links},\qquad N_s=3V\quad\text{spatial plaquettes}.
\]
Take normalized Haar SU(2) fields on those links. Let \(w_\beta(g)=\exp[-\beta(1-\operatorname{ReTr}g/2)]\) with \(\beta\ge0\); \(e^{-2\beta}\le w_\beta\le1\). On \(\mathcal H=L^2(\mathrm{SU}(2)^{N_\ell})\), put
\[
A(U)=\prod_{p\ \mathrm{spatial}}w_\beta(U_p),\qquad
B(U,U')=\prod_{\ell\ \mathrm{spatial}}w_\beta(U_\ell U_\ell'^{-1}),\qquad
T=A^{1/2}BA^{1/2}.
\]
Use the exact gauge projector \(P\) and its invariant Hilbert space \(P\mathcal H\). [Lemma YM4-02c, Theorem 5](LEMMA-0004-REFLECTION-TRANSFER.md) establishes that for \(\beta>0\), \(T\) is self-adjoint, positive, injective and trace class with a simple, positive **gauge-invariant** Perron eigenfunction \(\Omega\), and
\[
Z_{\Lambda,L_t}=\operatorname{Tr}(T^{L_t}P)
\]
is the full periodic Wilson partition function with all temporal gauge-link integrals retained.

For \(L_t=4\), the actual four-dimensional periodic lattice has \(4V\) sites and \(6(4V)=24V\) plaquettes: \(12V\) spatial and \(12V\) timelike. At \(L=6\), these are 864 sites and 5,184 plaquettes; \(N_\ell=N_s=648\), and 648 timelike plaquettes per step.

**First rigorous four-dimensional trace upper bound.** \(B\) is positive trace class with \(\operatorname{Tr}B=1\), because its diagonal equals \(1\) for all SU(2) link fields; by cyclicity and positivity
\[
0<T\le_{\rm norm}1,\quad \operatorname{Tr}T=\int A(U)\,dU\le1.
\]
The expression \(T\le_{\rm norm}1\) means \(\|T\|\le1\), not a pointwise inequality. Since \(0\le P\le I\) commutes with \(T\),
\[
\boxed{\quad
0<\operatorname{Tr}(T^4P)\le\operatorname{Tr}T^4
\le\operatorname{Tr}T\le1.\quad}
\]
Equivalently, the **genuine** four-dimensional SU(2) four-slice Wilson partition function obeys \(0<Z_{\Lambda,4}\le1\) in the repository's normalized Wilson convention. This is a rigorous **enclosure**, not a claim of numerical evaluation of the Haar integral.

## 2. Independent Perron lower bound by the actual SU(2) kernel

The constant trial vector \(1\in P\mathcal H\) has norm one, so \(\lambda_0\ge\langle1,T1\rangle\). This Rayleigh quotient is the normalized double-Haar integral of
\[
\exp\Big[-\beta\Big(\tfrac12\sum_{p\ {\rm spatial}}\!(1-a_p(U))
+\tfrac12\sum_{p\ {\rm spatial}}\!(1-a_p(U'))
+\sum_{\ell\ {\rm spatial}}\!(1-a(U_\ell U_\ell'^{-1}))\Big)\Big],
\]
where \(a(g)=\operatorname{ReTr}g/2\).

On spatial sides at least two, every spatial plaquette has four distinct links and its holonomy is Haar after integrating one exclusive link. Under the normalized independent product-Haar measure for \(U,U'\),
\[
\mathbb E[a_p(U)]=\mathbb E[a_p(U')]=0,\qquad
\mathbb E[a(U_\ell U_\ell'^{-1})]=0.
\]
Jensen applied to the **genuine continuous-SU(2)** kernel therefore yields
\[
\boxed{\quad
\lambda_0\ge\langle1,T1\rangle
\ge\exp[-\beta(N_s+N_\ell)]
=e^{-6\beta V}.\quad}
\]
This uses the actual transfer kernel rather than a separate finite model or a guessed Perron root. The weaker pointwise lower bound \(e^{-12\beta V}\) is also valid; the factor-two Jensen improvement is critical to the first certificate's pass.

## 3. Exact four-dimensional four-moment gap certificate

For the explicit 6×6×6 spatial lattice and four temporal slices choose
\[
V=216,\qquad \beta=\frac1{2000V}=\frac1{432000},\qquad
q=\frac13,\qquad L_0=\frac{997}{1000}.
\]
Since \(e^{-x}>1-x\) for \(x>0\), the Perron bound gives
\[
\lambda_0\ge e^{-3/1000}>L_0.
\]
Let \(\lambda_1\) denote the largest nonvacuum eigenvalue of \(T\) on the **full gauge-invariant** Hilbert space. Its fourth power obeys
\[
\lambda_1^4
\le\operatorname{Tr}(T^4P)-\lambda_0^4
<1-L_0^4=\frac{11946107919}{10^{12}}.
\]
The **integer-only strict margin** is
\[
\boxed{\quad
\left(\frac{L_0}{3}\right)^4-(1-L_0^4)
=\frac{10209575321}{40500000000000}>0.\quad}
\]
Hence \(\lambda_1<L_0/3<\lambda_0/3\), yielding the genuine finite-volume **whole gauge-invariant transfer** result
\[
\boxed{\quad \frac{\lambda_1}{\lambda_0}<\frac13,\qquad
\Delta_{\rm physical}:=\frac1a\log\frac{\lambda_0}{\lambda_1}
>\frac{\log3}{a}.\quad}
\]
At positive \(\beta\), the transfer is injective, so the positive second eigenvalue exists on this nontrivial SU(2) Hilbert space. The zero-coupling endpoint has rank-one transfer and an infinite gap.

**Adversarial controls:** using only this trace/Perron envelope, \(q=1/4\) at \(\beta V=1/2000\) is HOLD; \(q=1/3\) at \(\beta V=1/1000\) is HOLD; changing Jensen's coefficient from \(6\) to \(12\) at \(\beta V=1/2000\) is HOLD. The acceptance gate must reject all three instead of treating an arithmetic inequality as a full-space theorem.

## 4. Genuine blocked-Wilson source: exact Haar Gram at \(\beta=0\) and positive-beta Gram floor

Take an ordinary **spatial 2×2 rectangle** \(C\) anchored at an even fine site in two spatial directions. Its ordered boundary has eight distinct fine links on \(L\ge6\) and equals the pullback of the coarse plaquette via the factor-two blocking map of YM4-07E. Let
\[
F(U)=\frac12\operatorname{ReTr}\operatorname{Hol}_{C}(U).
\]
Integrating any one of its eight independent fine links makes its SU(2) holonomy exactly Haar. Thus
\[
\boxed{\quad \mathbb E_{\rm Haar}F=0,\qquad
\mathbb E_{\rm Haar}F^2=\frac14.\quad}
\]

At \(\beta=0\), \(A=B=1\), and \(T_0\) is the **rank-one** constant projector on the full (and physical gauge-invariant) Hilbert space. Hence \(\Omega_0=1\), and for the two independent matched-source witnesses \(v_0=\Omega_0=1\), \(v_1=F\Omega_0=F\),
\[
G_0=\begin{pmatrix}1&0\\0&1/4\end{pmatrix},\qquad
M_0^{(4)}=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad
\operatorname{Tr}(T_0^4P)=1.
\]
The exact small-Gram transfer residual is therefore **zero**. This is an exact original-four-dimensional **SU(2) source-and-moment** calibration at \(\beta=0\).

For every finite \(\beta>0\), use the true positive normalized Perron eigenfunction \(\Omega_\beta\), not the constant Haar vector. The two actual Wilson-source witnesses
\[
v_0=\Omega_\beta,\qquad v_1=F\Omega_\beta
\]
belong to the **blocked spatial-slice cyclic sector** \(\mathcal K\) of YM4-07E. Their \(2\times2\) Gram determinant is the Wilson-source variance in the true vacuum density:
\[
\det G_\beta
=\langle\Omega_\beta,F^2\Omega_\beta\rangle
-\langle\Omega_\beta,F\Omega_\beta\rangle^2
=\operatorname{Var}_{\Omega_\beta^2\,d{\rm Haar}}(F).
\]

The original transfer kernel satisfies, for all \(U,U'\),
\[
e^{-2\beta(N_s+N_\ell)}\le T(U,U')\le1.
\]
Writing \(\lambda_0\Omega_\beta(U)=\int T(U,U')\Omega_\beta(U')\,dU'\) and using \(\Omega_\beta>0\) gives
\[
\frac{\max_U\Omega_\beta(U)}{\min_U\Omega_\beta(U)}
\le e^{2\beta(N_s+N_\ell)}=e^{12\beta V}.
\]
Since \(\|\Omega_\beta\|_{L^2(d{\rm Haar})}=1\), \(\min\Omega_\beta\ge e^{-12\beta V}\). The \(L^2\) source variance therefore satisfies
\[
\begin{aligned}
\det G_\beta
&=\min_{c\in\mathbb R}\int(F-c)^2\Omega_\beta^2\,d{\rm Haar}\\
&\ge e^{-24\beta V}\min_c\int(F-c)^2\,d{\rm Haar}
=\frac14e^{-24\beta V}.
\end{aligned}
\]
At \(\beta V=1/2000\), the elementary bound \(e^{-x}>1-x\) gives
\[
\boxed{\quad \det G_\beta>\frac14\left(1-\frac3{250}\right)
=\frac{247}{1000}.\quad}
\]
This proves the **actual positive-beta blocked-Wilson witness remains independent and quantitatively conditioned**, with no SU(2) integration approximation.

Because \(T_\beta\) is injective and positive, the nonzero Schur residual \(u=(F-\langle\Omega_\beta,F\Omega_\beta\rangle)\Omega_\beta\) satisfies \(\langle u,T_\beta^4u\rangle>0\); hence a second Wilson witness **strictly decreases** the trace residual of YM4-07F. Its numerical decrement and the exact \(\beta>0\) moment matrix remain **OPEN**; this note does not substitute the \(\beta=0\) moments for positive coupling.

## 5. Research implications and next production gates

The two pieces together demonstrate that the YM4-07F **same-group transfer trace + Wilson Gram methodology works in genuine four-dimensional continuous SU(2)**: the positive-coupling full-spectrum trace certificate passes at very small volume-dependent \(\beta\), and the matched blocked-Wilson vacuum-source Gram determinant has a strict positive-coupling rational floor. The earlier YM4-02d contraction theorem provides a stronger fixed-volume gap here; the new result is an independently testable bridge between trace moments and Wilson-network witnesses.

The all-scale weak-coupling challenge requires more:

- Evaluate or rigorously enclose \(\operatorname{Tr}(T_\beta^{2m}P)\) with a **much sharper volume-uniform envelope** along \(\beta(a)\to\infty\).
- Enclose the Perron vacuum and the true matched Wilson-network \(M_\beta^{(2m)}\) beyond the \(\beta=0\) endpoint; use a certified Schur witness decrement.
- Establish a physical source space with sufficient spectral visibility and a cyclic-excitation bound, and prove ultraviolet and infinite-spatial-volume stability.
- Construct a nontrivial continuum OS theory with a full strictly positive physical mass gap.

**Classification:** genuine 4D SU(2) finite-volume **very-strong-coupling** trace/gap and Wilson-Gram **DERIVED**; rational geometrical certificate **predicted before checker**; actual positive-\(\beta\) transfer moment matrix **OPEN**; running-coupling all-scale 4D mass gap and nontrivial continuum **OPEN**.
