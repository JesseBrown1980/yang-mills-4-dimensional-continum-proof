# YM4-WG07 — original continuous-SU(2) full physical six-eigenstate Feshbach cluster and true Wilson weight

**21 November 2026.** This certificate starts with the merged original 3+1D, spatial-L=2 Wilson positive physical transfer and the source-authenticated exact WG04–WG06 construction. The proof concerns *the entire original infinite-dimensional continuous-SU(2) physical Gauss-invariant Hilbert space*, all 24 magnetic spatial Wilson plaquettes, all 24 temporal Wilson Haar-convolution links, and every higher-spin Peter–Weyl sector.

**New fixed-spatial-lattice acceptance targets.**

- For **every \(0<\beta\leq1/10000\)**, the complete interacting center-neutral physical transfer has an actual **spectrally isolated rank-six eigenspace**, consisting of precisely the neutral eigenvalue indices **2–7**, after its simple neutral vacuum.
- For **every \(0<\beta\leq1/1000000\)**, the **true interacting-vacuum centered original local Wilson plaquette** has squared physical spectral weight **strictly greater than \(9/400\)** in that actual rank-six eigenspace. At least one of its six genuine transfer eigenvectors therefore carries squared weight **greater than \(3/800\)**.
- This theorem identifies a genuine first-six neutral spectral cluster. The **first individual center-neutral eigenvalue's Wilson weight remains OPEN**, as does the weak-coupling, volume-uniform 4D continuum mass gap.

The source predicts these inequalities before implementation in [YM4-WG07 prediction freeze](certificate-atlas/PREDICT-YM4-WG07-FESHBACH-SIX-20261121.hbp). Exact independent tests and hosted SHA-based acceptance are required.

## 1. Original full physical transfer and its isospectral form

Let \(K\) be the original normalized positive 24-link SU(2) Wilson Haar convolution restricted to the complete SU(2) Gauss-invariant physical Hilbert space. Let \(W_p=(1/2)\operatorname{Tr}U_p\) be the original real SU(2) fundamental spatial plaquette halftrace, and set

\[
V=\sum_{p=1}^{24}W_p,\qquad \|V\|\leq24.
\]

The complete magnetic multiplier of the original Wilson action is

\[
B=e^{-24\beta}e^{\beta V}.
\]

Its positive physical transfer is

\[
T_{\rm phys}=B^{1/2}KB^{1/2}.
\]

The common scalar \(e^{-24\beta}\) does not change eigenvectors or spectral projectors. Define

\[
T'=e^{\beta V/2}Ke^{\beta V/2},\qquad
J=K^{1/2}e^{\beta V}K^{1/2}.
\]

For \(A=e^{\beta V/2}K^{1/2}\), we have \(T'=AA^*\) and \(J=A^*A\). The original Wilson \(K\) is positive and injective with dense range, and the magnetic exponential is strictly positive and boundedly invertible. Hence the polar isometry of \(A\) is unitary and carries the *complete nonzero spectral projectors*, including multiplicities, between \(J\) and \(T'\). The full interacting source weight must ultimately be evaluated in the \(T'\) representation.

## 2. Original electric decomposition and sixfold first magnetic slopes

By WG04, the center-neutral electric Hilbert space has orthogonal decomposition

\[
\mathcal H_{\rm neutral}=\mathbb C\,1\ \oplus\
E_{42}\mathcal H\ \oplus\ R\mathcal H.
\]

On the vacuum constant state \(K=1\); on the electric 42-dimensional spin-network subspace \(E_{42}\), \(K=tI\), with

\[
t=\kappa_1(\beta)^4.
\]

The **entire remaining neutral physical higher-spin tail** has \(0<K_R\leq\tau I\), where, putting \(y=\beta^2/4\),

\[
\tau\leq\frac{\beta^4}{576(1-y)^2},
\quad
t\geq\frac{\beta^4(1-y)^4}{256},
\quad
\rho:=\frac{\tau}{t}\leq\frac4{9(1-y)^6}<\frac9{20}
\]

for the stated small-coupling interval.

WG06 computes the exact first magnetic derivative \(M=E_{42}VE_{42}=A_{42}/8\). Its source-verified integer adjacency \(A_{42}\) consists of six \(K_{4,2}\) components plus six isolates, satisfies \(A_{42}^3=8A_{42}\), and has relative slope spectrum

\[
\operatorname{spec}(M)=
\left\{\begin{array}{ll}
+\sqrt8/8 &: 6,\\
0 &: 30,\\
-\sqrt8/8 &: 6.
\end{array}\right.
\]

In particular, its positive slope is strictly **greater than \(1/3\)** and is separated from the next slope (zero). Let \(P_+\) denote this exact *electric six-dimensional positive-slope spectral projector*. For the original local Wilson halftrace \(W=\phi_0/2\), WG06 proves

\[
\|P_+W\|^2=1/32,\qquad \|W\|^2=1/4.
\]

This last projection refers to the **electric first magnetic derivative**, not yet the full interacting transfer.

## 3. Complete vacuum–tail Schur complement at a fixed spectral threshold

Work with \(J=K^{1/2}e^{\beta V}K^{1/2}\). Write \(E=E_{42}\), \(P_0=|1\rangle\langle1|\), and \(R\) for the entire remaining neutral electric subspace. Define the exact threshold

\[
\theta=t\left(1+\frac{\beta}{6}\right).
\]

All inequalities in this section hold uniformly for \(0<\beta\leq1/10000\).

Let \(q=1/(1-24\beta)\). The full magnetic exponential satisfies the operator inequalities

\[
e^{-24\beta} I\leq e^{\beta V}\leq qI.
\]

Set \(\varepsilon=\|e^{\beta V}-I\|\). Elementary positive exponential-series bounds, checked exactly in the producer, give

\[
\varepsilon\leq25\beta,\qquad
\|e^{\beta V}-I-\beta V\|\leq289\beta^2.
\]

The \(E\) diagonal block consequently has the exact form

\[
J_{EE}=t(I+\beta M)+\mathcal R,\quad
\|\mathcal R\|\leq289t\beta^2.
\]

The vacuum block is the positive scalar \(a=\langle1,e^{\beta V}1\rangle\geq1-24\beta\); the remaining electric-tail diagonal block satisfies \(J_{RR}\leq q\tau I\). The off-diagonal blocks satisfy

\[
\|J_{E0}\|\leq\sqrt t\,\varepsilon,\quad
\|J_{0R}\|\leq\sqrt\tau\,\varepsilon,\quad
\|J_{ER}\|\leq\sqrt{t\tau}\,\varepsilon.
\]

For every spectral parameter \(\lambda\in[\theta,qt]\), the source-authenticated all-spin estimates give

\[
a-\lambda\geq99/100,\qquad
\lambda-q\tau\geq t/2.
\]

First eliminate the vacuum block, whose inverse is bounded by \(100/99\). The resulting tail block is the original \(J_{RR}\) minus a positive semidefinite vacuum-coupling correction, hence is still at most \(q\tau I\). Eliminate that **complete infinite-dimensional tail** next. The resulting self-adjoint 42×42 Schur complement \(\mathcal S_E(\lambda)\) satisfies

\[
\|\mathcal S_E(\lambda)-[t(I+\beta M)-\lambda I]\|
\leq t\Delta(\beta),
\]

where the following independently testable *rational* majorant retains **both** vacuum and tail effects:

\[
\Delta(\beta)\leq
289\beta^2
+\frac{100}{99}\varepsilon^2
+\frac9{10}\varepsilon^2
\left(1+\frac{100}{99}\varepsilon\right)^2.
\]

Since \(\varepsilon\leq25\beta\), exact integer-rational endpoint evaluation proves

\[
\boxed{\Delta(\beta)<1500\beta^2<\beta/6}
\]

for **every \(0<\beta\leq1/10000\)**. The scalar majorant divided by \(\beta^2\) increases monotonically with \(\beta\), so its endpoint check controls the entire interval.

At \(\lambda=\theta\), the reference \(42\times42\) matrix has **six strictly positive directions**, because \(\sqrt8/8>1/3\), and **36 strictly negative directions**, because the other slopes are zero or negative. Its minimum absolute spectral value is at least \(t\beta/6\). The Schur perturbation is strictly smaller, so Sylvester inertia is unchanged: the actual Schur complement has precisely **six positive, 36 negative directions**.

The scalar vacuum block contributes one positive direction and the complete tail block only negative directions at \(\theta\). Thus the original **full interacting center-neutral physical operator** has **exactly seven eigenvalues above the threshold**: its simple neutral vacuum plus exactly six additional eigenvalues. All remaining neutral eigenvalues lie strictly below \(\theta\). By compact positive min–max and the isospectral polar map, this proves an **actual isolated rank-six interacting physical neutral spectral projector**,

\[
\Pi_6
=\mathbf1_{(e^{-24\beta}\theta,\ \lambda_0)}(T_{\rm phys}|_{\rm neutral}),
\qquad
\operatorname{rank}\Pi_6=6.
\]

Here \(\lambda_0\) is the true physical vacuum eigenvalue. The six modes are precisely neutral transfer eigenvalue indices 2–7. The strict threshold gap proves that the cluster is separated from all 36 other WG04 neutral-band levels and the full higher-spin neutral complement. The charged sectors remain invariant and are handled separately by WG02–WG03.

## 4. Positive true physical Wilson source weight in the actual six-state cluster

To transfer the *electric slope* overlap of WG06 into an actual **interacting** spectral weight, we bound the distance between the exact rank-six physical projector \(\Pi_6\) and the electric \(P_+\).

Fix \(0<\beta\leq1/1000000\). For any normalized \(J\)-eigenvector \(\psi\) in the six-state cluster, the same vacuum/tail Schur elimination and its \(\Delta\) bound give:

\[
\|P_{E\ominus P_+}\psi\|\leq9000\beta,\qquad
\|P_R\psi\|\leq36\beta,\qquad
\|P_0\psi\|\leq26\sqrt t\,\beta.
\]

All three arise from the original block equations above. For the first, the complementary magnetic-slope eigenvalues are at most zero, while the true cluster eigenvalues exceed \(\theta=t(1+\beta/6)\), so the exact denominator is at least \(t\beta/6\). For the second, the full tail resolvent is bounded by \(2/t\), and \(\sqrt{\tau/t}<7/10\). For the third, the vacuum inverse is bounded by \(100/99\).

Consequently \(\|(I-P_+)\psi\|\leq9100\beta\). Six orthogonal cluster eigenvectors, the rational inequality \(\sqrt6<5/2\), and equality of the ranks show

\[
\|\Pi_6^{J}-P_+\|\leq22750\beta.
\]

The unitary polar map \(U\) from \(J\) to the actual interacting transfer acts on any six-cluster eigenvector as

\[
U\psi=e^{\beta V/2}K^{1/2}\psi/\sqrt{\lambda}.
\]

The original explicit vacuum/band/tail bounds, together with
\(e^{12\beta}-1\leq12\beta/(1-12\beta)\),
give \(\|U\psi-\psi\|\leq100\beta\): at most \(13\beta\) from the magnetic half-exponential, \(24\beta\) from the band normalization, \(26\beta\) from vacuum mixing, and \(36\beta\) from the full electric tail. Comparing the two rank-six orthogonal projectors by their orthonormal bases gives

\[
\|\Pi_6-\Pi_6^{J}\|\leq500\beta,
\quad\text{hence}\quad
\boxed{\|\Pi_6-P_+\|\leq23250\beta}.
\]

Let \(\Omega\) be the **true interacting positive physical vacuum**, \(m=\langle\Omega,W\Omega\rangle\), and \(u=(W-m)\Omega\) the **correctly centered original physical Wilson source**. WG05's full-original-vacuum perturbation controls it by

\[
\|u-W\|\leq6e+3d\leq148\beta,\quad
e=\frac{\kappa_{1,\mathrm{up}}^2}{1-48\beta},\quad
d=\frac{48\beta}{1-48\beta}.
\]

No Haar vacuum substitution is made in the physical source.

The triangle inequality combined with \(\|P_+W\|=\sqrt{1/32}>1/6\) and \(\|W\|=1/2\) gives

\[
\begin{aligned}
\|\Pi_6u\|
&\geq\|P_+W\|
-\|\Pi_6-P_+\|\,\|W\|
-\|u-W\|\\
&>\frac16-11773\beta
>\frac3{20}
\qquad(0<\beta\leq1/1000000).
\end{aligned}
\]

Therefore the **actual original interacting physical transfer** satisfies the exact rational squared source-weight theorem

\[
\boxed{\|\Pi_6(W-\langle W\rangle)\Omega\|^2>\frac9{400}}.
\]

By nonnegativity and rank six, **at least one true SU(2) physical eigenvector among neutral indices 2–7** has squared Wilson overlap \(> (9/400)/6=3/800\).

This is a **physical finite-\(\beta\), full-Gauss, full-magnetic, true-vacuum projector certificate**, extending the rank-42 weight of WG05. It does not yet determine *which of the six* modes carries that overlap or whether the leading neutral eigenvalue itself has positive weight.

## 5. Exact fourth-order SU(2) Haar quadrature and its role

The prior WG06 exact first-order triple traces had degree at most two per SU(2) link. Their eight-point quaternion Q8 quadrature was valid for that degree; it is not a fourth-order rule, since its fourth coordinate moment is \(1/4\), whereas normalized SU(2) Haar has \(E[q_0^4]=1/8\).

For a genuine fourth-order Haar source, construct the **24 uniform Hurwitz quaternion units**:
the eight signed coordinate axes \(\pm1,\pm i,\pm j,\pm k\) and the 16 quaternions \((\pm1\pm i\pm j\pm k)/2\) with all independent choices of signs. Their coordinate means vanish, and their exact tensor moments are

\[
E[q_aq_b]=\frac{\delta_{ab}}4,\qquad
E[q_aq_bq_cq_d]
=\frac{\delta_{ab}\delta_{cd}+\delta_{ac}\delta_{bd}+\delta_{ad}\delta_{bc}}{24}.
\]

These are exactly the continuous-SU2 Haar moments on \(S^3\) for every monomial of degree \(\leq4\). The producer and independent verifier check all 256 ordered fourth-index combinations using **integers only**. The directly relevant original plaquette example, with \(\phi=\chi_1(U_p)=2W_p\), is

\[
\langle\phi,W_p^2\phi\rangle_{\mathrm{Haar}}
=4E[q_0^4]=\frac12.
\]

Thus WG07 implements **an exact SU(2) fourth-Haar integration rule and one explicit second-order magnetic source fixture**. The complete 42×42 second-derivative coefficient matrix remains an optional next refinement. The full operator-norm Taylor remainder above already bounds every one of those terms for the six-mode rank and source-weight theorem, so their explicit enumeration is unnecessary for this acceptance.

## 6. Falsifiers, reproduction and continuation

The frozen [WG07 predictions](certificate-atlas/PREDICT-YM4-WG07-FESHBACH-SIX-20261121.hbp) precede both the producer and independent tests. The acceptance workflow independently rebuilds the Hurwitz 24-point set, verifies its full fourth-order tensor and Q8 negative control, computes the endpoint Schur margin with a separately written integer-pair rational kernel, checks vacuum/tail contributions, exact WG06 multiplicities, all six projector-angle constants, WG05's true interacting-vacuum source and independent beta rejection. It writes two byte-identical deterministic HBP transcripts and a SHA-256 digest.

    python3 -B tests/test_ym4_su2_wilson_six_feshbach.py -v
    python3 -B tests/ym4_su2_wilson_six_feshbach.py

**Next source-sensitive target:** exploit the six-block finite-\(\beta\) projector, lattice translation and cubic rotational symmetries, and a controlled next-order operator matrix to isolate the **leading individual neutral eigenspace** and measure its Wilson weight. An independent full transfer spectral comparison is still required for that individual-level acceptance. The physical charged-first zero local Wilson weight of WG03, the full original SU2 42-band WG04–WG05, and all eleven continuum mass-gap obligations retain their established scopes.
