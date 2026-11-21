# YM4-07C — finite-Wilson spectral-source bridge and genuine 4D SU(2) acceptance gates

**November 20, 2026. Result: exact transfer lemma and numerical certificate budget. Actual 4D SU(2) continuum construction and full physical mass-gap proof: OPEN.**

This note uses the independently accepted 3×4 finite S₃ Wilson source as an authenticated **calibration anchor**, then formulates the exact additional operator inequalities needed before any of its spectral information can inform a continuous SU(2) theory in four Euclidean dimensions. The calculation does not posit an SU(2)/S₃ equivalence.

## 1. The finite source input and its exact tolerance

The original finite Wilson proof chain ([finite #349](https://github.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C/pull/349), [independent source #350](https://github.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C/pull/350)) establishes for the **original finite S₃ model only**, with normalized first and second physical eigenstates \(u_F,v_F\) and original seven-loop Wilson \(O_F\):
\[
w_F=|\langle v_F,O_Fu_F\rangle|^2>
\frac{17\,074\,763}{10^{12}}.
\]
The original shifted Wilson signed margin is \(9\,285\,530\,088/10^{12}>0\). Its full-state normalization is already in this finite bound.

Set \(A_F=\sqrt{17\,074\,763/10^{12}}\). Using integer square roots without numerical floating-point assumptions,
\[
\boxed{\quad
\frac{4\,132\,162\,024}{10^{12}}<A_F<
\frac{4\,132\,162\,025}{10^{12}}.\quad}
\]
These are independently verified *strict* inequalities, not source claims about 4D SU(2).

## 2. Exact source/projection-transfer lemma

Let \(P_F=|v_F\rangle\langle v_F|\), \(x_F=O_Fu_F\) in the W-normalized finite physical Hilbert space \(\mathcal H_F\). On a genuine continuous SU(2) 4D lattice with physical time spacing \(a_k\), renormalized bare coupling \(\beta_k\), spatial physical volume \(R\), let \(H_{k,R}\) be a gauge-invariant physical Hamiltonian, and let
\[
 Q_{k,R}=1_I(H_{k,R})
\]
be its orthogonal spectral projector onto a fixed bounded interval \(I\subset(0,\infty)\) **in physical energy units**. Let \(x_{k,R}\) be an explicitly defined and correctly renormalized gauge-invariant source vector, appropriate to the SU(2) vacuum.

Assume an **explicit isometry** \(J_{k,R}:\mathcal H_F\to\mathcal H_{k,R}\) is supplied, and the *two distinct source estimates*
\[
 \|x_{k,R}-J_{k,R}x_F\|\le\delta_{k,R},\quad
 \|Q_{k,R}J_{k,R}x_F-J_{k,R}P_Fx_F\|\le\epsilon_{k,R}
\]
have independently validated original-source proofs. The first estimate includes the critical finite-eigenstate-to-continuum-vacuum comparison and actual Wilson-source/operator normalization. The second independently controls the spectral projector, not just two approximate eigenvalues.

Since \(Q\) is contractive and \(J\) is isometric,
\[
\begin{aligned}
 \|Q_{k,R}x_{k,R}\|
 &\ge \|J_{k,R}P_Fx_F\|
       -\|Q_{k,R}J_{k,R}x_F-J_{k,R}P_Fx_F\|
       -\|Q_{k,R}(x_{k,R}-J_{k,R}x_F)\|\\
 &> A_F-\epsilon_{k,R}-\delta_{k,R}.
\end{aligned}
\]
Therefore, if \(\delta+\epsilon<A_F\),
\[
\boxed{\qquad
\langle x_{k,R},Q_{k,R}x_{k,R}\rangle
 >(A_F-\delta-\epsilon)^2>0.\qquad}
\]

A sufficient exact-integer gate, for outward-rounded total error \(B=\lceil10^{12}(\delta+\epsilon)\rceil\), is \(0\le B<4\,132\,162\,024\). Then the SU(2) spectral weight in the selected physical window would be strictly greater than
\[
 \frac{(4\,132\,162\,024-B)^2}{10^{24}}.
\]
For the **hypothetical, unmeasured** budget \(B=4\,000\,000\,000\), this lower numerator equals \(17\,466\,800\,587\,776\,576\). It is a benchmark for future source transports, **not** a current SU(2) measurement.

There is no proved cross-group isometry, source comparison or SU(2) spectral-projector comparison in the current research. The exact integer threshold makes the missing mathematical work specific and falsifiable. A low Wilson spectral weight at an isolated finite source does not imply any spatial or temporal continuum gap.

## 3. Matrix-law factor-three error accounting

Within continuous SU(2), suppose **genuine** consecutive-cutoff source and spectral comparisons are constructed at \(a_k=a_0/3^k\). If the total error over step \(j\) is at most \(c_j\), triangle inequalities give an accumulated amplitude loss at most \(\sum_jc_j\), after compatible source Hilbert-space embeddings are supplied.

An illustrative exact summable family
\[
 c_j\le\frac{1}{2000\,4^j},\qquad
 \sum_{j=0}^{\infty}c_j\le\frac1{1500},\qquad
 \sum_{j=k}^{\infty}c_j\le\frac{1}{1500\,4^k}
\]
is verified by the checker via integer geometric-series algebra. The factor-three jump reduces the number of scale indices to reason about, while the factor-four geometric sum gives a closed tail bound. It says nothing about the unconstructed physical SU(2) weak-coupling RG at \(\beta(a)\to\infty\). An **SU(2) first-scale spectral source** must be established independently, even if the finite S₃ example serves as a source-controller test.

## 4. Two exact counterexamples: source visibility and full gap are different

For \(a_k=3^{-k}\), consider the positive transfer matrices
\[
 T_k=\operatorname{diag}\left(1,\frac{1}{1+a_k^2},\frac{1}{1+2a_k}\right).
\]
The first entry is the vacuum. The dark energy satisfies
\[
0<\Delta_{k,\mathrm{dark}}=
\frac{\log(1+a_k^2)}{a_k}\le a_k\to0.
\]
A Wilson test source selecting the third eigenvector sees
\[
\Delta_{k,\mathrm{visible}}=
\frac{\log(1+2a_k)}{a_k}\ge\frac{2}{1+2a_k}\to2,
\]
although the full physical gap vanishes. Alternatively, a source selecting the **first excited dark state** has normalized first-excitation weight one at every finite \(k\), still with vanishing physical gap. These are exact rational matrices, and the logarithmic inequalities follow from \(x/(1+x)\le\log(1+x)\le x\); the executable uses no floating-point logs.

Consequently a single nonzero Wilson overlap establishes **spectral visibility**, while a positive **full** continuum mass gap requires control of all physical gauge-invariant excitations.

## 5. Full physical-spectrum and continuum gates

In the genuine continuous SU(2) theory, a sufficient full-spectrum physical gap target (at all sufficiently fine cutoff spacings and arbitrarily large physical spatial volume) is
\[
\|e^{-tH_{k,R}}(I-P_{0,k,R})\|
\le e^{-\Delta_*t},\quad
\Delta_*>0,\quad t>0.
\]
[YM4-07B](NOTE-YM4-07B-QUANTIFIED-CONTINUUM-BRIDGE-20261116.md) already provides the conditional strong-semigroup/vacuum-projection limit argument. The missing inputs are a **volume-uniform weak-coupling nonperturbative bound**, a nontrivial reflection-positive Osterwalder–Schrader continuum measure, control of the order of cutoff and thermodynamic limits, and ultimately the physical Wightman field theory. The [Clay/Jaffe–Witten problem](https://www.claymath.org/millennium/yang-mills-the-maths-gap/) sets this scope.

The next physical experiment should therefore specify a *genuine continuous-SU(2)* gauge-invariant Wilson source, common physical-energy interval and weak-coupling source/projection map. It must retain the six-staple mixed-plane chair/network couplings documented in [YM4-05A](NOTE-YM4-05A-CHARACTER-WEAK-COUPLING-20261107.md), then estimate its actual source/projector defect. Predict and pin a quantitative error budget before measuring it. If a bound can be extended to a summable all-scale tail, the source-visibility lemma supplies the positive-weight part; YM4-04/05/06 still supply the hard **full-spectrum** and **continuum** proof obligations.

## 6. Executable acceptance

[The independent exact-integer verifier](../tests/test_ym4_07c_wilson_projection_bridge.py) checks the square-root interval, strict conditional weight bounds, factor-three/four scale-tail algebra and both physical-gap falsifiers. It requires nine deliberately corrupted continuum claims to fail closed: missing SU(2) source, wrong gauge group, unproved spectral projector, fixed strong coupling labeled UV, finite-only gap, missing OS construction, missing infinite-volume control exhausted amplitude tolerance, and a forged record whose seven status fields all say PASS.

Scientific status emitted on success:

- Finite S₃ source: externally pinned prior finite-model acceptance.
- Source/projection lemma: **MATHEMATICAL PASS**, quantitative budget available.
- Cross-group or UV SU(2) map: **OPEN**.
- Weak-coupling all-scale RG: **OPEN**.
- Nontrivial continuum OS construction: **OPEN**.
- Physical full-spectrum continuum mass gap: **OPEN**.

This is an actionable next theorem interface, not a claim that the continuum problem has been solved.


## 7. A genuine continuous-SU(2) four-dimensional finite-scale source theorem

We can also establish an **actual continuous-SU(2) result**, independent of the finite S₃ numerical input. Let \(\Lambda\) be a four-dimensional periodic hypercubic Wilson lattice with each side at least two, \(\beta\ge0\) finite, normalized Haar links, and normalized Wilson plaquette \(W_p(U)=\frac12\operatorname{Re}\operatorname{Tr}U_p\in[-1,1]\). Let \(\mu_{\Lambda,\beta}\) be its actual Wilson Gibbs probability measure.

**Theorem (local Wilson Gibbs variance).** For every such lattice and every plaquette,
\[
\boxed{\quad\operatorname{Var}_{\mu_{\Lambda,\beta}}(W_p)
\ge\frac14 e^{-12\beta}>0,\quad}
\]
**independent of the number of lattice sites and plaquettes**.

**Proof.** Choose one of the four links in \(p\), and condition on all other link variables. In four dimensions that link participates in exactly **six** distinct plaquettes. Their part of the Wilson Boltzmann weight is a continuous positive function \(f(U)\) with \(e^{-12\beta}\le f(U)\le1\) after removing fixed factors, since each of the six terms has action between \(0\) and \(2\beta\). Its normalized conditional density relative to Haar is \(f(U)/\int f\,dU\ge e^{-12\beta}\).

For the selected plaquette, fixing the other three links turns its normalized trace into \(\frac12\operatorname{Re}\operatorname{Tr}(UA)\) or an equivalent inverse/orientation, with \(A\in\mathrm{SU}(2)\) fixed. By Haar invariance and character orthogonality,
\[
\int W_p(U)\,dU=0,\qquad
\int W_p(U)^2\,dU=\frac14.
\]
Therefore for every real conditional center \(c\),
\[
\int(W_p(U)-c)^2\,d\mu(U\mid\mathrm{other\ links})
\ge e^{-12\beta}\int(W_p(U)-c)^2\,dU
=e^{-12\beta}\left(\frac14+c^2\right).
\]
Minimizing over \(c\) shows that the conditional variance is at least \(e^{-12\beta}/4\); the law of total variance proves the theorem. The bound is independent of volume because it conditions only on the six incident plaquettes. For a fixed \(\beta\), the same local variance inequality persists under any weak infinite-volume Gibbs limit with that fixed coupling, since \(W_p\) and \(W_p^2\) are bounded local continuous functions.

**Machine-checkable exact controls.** [The new integer checker](../tests/test_ym4_07c_su2_local_wilson_variance.py) enumerates all 24 binary-tetrahedral quaternion points \(Q_8\cup\{(\pm1\pm i\pm j\pm k)/2\}\), proves their coordinate covariance exactly \(\delta_{ij}/4\), and checks the normalized character second moment \(1/4\). The finite 24-point second-moment design is an independent **control for the degree-two continuous Haar identity**, not a replacement for the continuous measure in the theorem. To avoid floating-point exponentials, for rational \(x=12\beta\) and integer \(n>x\) it proves
\[
 \frac14e^{-x}\ge\frac14\left(1-\frac{x}{n}\right)^n.
\]
Examples:
- \(\beta=0\): variance \(\ge1/4\), in fact equality;
- \(\beta=1/1000,\ n=1\): variance \(\ge247/1000\);
- \(\beta=1/8,\ n=3\): variance \(\ge1/32\);
- \(\beta=1,\ n=24\): variance \(\ge1/67\,108\,864\);
- \(\beta=16,\ n=384\): variance \(\ge2^{-386}\).

Nine altered-claim controls reject wrong link incidence, negative coupling, invalid exponential enclosure, finite-group substitution, missing plaquette dependence, mistaking nonzero variance for a full gap, asserting weak-coupling uniformity, assuming an OS source identification, and changing the Haar second moment.

**Interpretation.** This establishes a **nonconstant genuine SU(2) local Wilson observable at every fixed lattice and finite coupling**, with a volume-independent quantitative variance floor. The floor decays as \(\beta\to\infty\); a renormalized ultraviolet source norm therefore still needs a separate scale-uniform estimate. Moreover, equal-time Euclidean Gibbs variance must be connected to the gauge-invariant Osterwalder–Schrader transfer Hilbert space by a genuine source identification before being called a spectral weight. The operator/projection transport theorem in section 2 and full-gap requirements in section 5 remain distinct.

**Next physical gate sharpened:** construct the genuine SU(2) time-zero Wilson source in the positive transfer representation, prove an appropriate cutoff-uniform *renormalized* source norm and projector comparison that accounts for mixed-plane network terms, then combine it with a physical full-spectrum gap estimate along the actual \(\beta(a)\) flow.
