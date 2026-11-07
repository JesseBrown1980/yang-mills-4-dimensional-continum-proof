# YM4-05A — weak-coupling character control and the first genuine 4D Wilson-link interaction obstruction

**Date:** November 7, 2026. **Status:** EXACT **two-dimensional continuous-SU(2) heat-kernel** refinement control; EXACT **four-dimensional Wilson one-link Haar** mixed-interaction evidence. Eight intentionally false claims rejected on a hosted runner. **Not** a full four-dimensional RG transformation, induced-action estimate, first excitation or continuum Yang–Mills mass-gap proof.

This is [PR #38](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/38), based on the already merged #36/#37 results. The [16-row prediction](PREDICT-YM4-05A-CHARACTER-WEAK-COUPLING-20261107.hbp) was committed at **\`af616ac87525b5696a957df23824464ee1960900\` before any checker source**. The [source](../tests/test_ym4_05a_character_weak_coupling.py), [14-row hosted receipt](../tests/YM4_05A_CHARACTER_WEAK_RECEIPT.hbp), and [dedicated CI](../.github/workflows/ym4-05a-su2-character-weak.yml) are integer-only and reproduce all accepted claims. The first CI attempt failed for invalid Python keyword names; this was corrected without editing the prediction. The later hosted run passed; do not erase failed initial CI history.

## 1. A positive control: the *exact* 2D SU(2) heat-kernel semigroup

On the compact **continuous** group SU(2), label irreducible characters by their dimensions \(n=1,2,\ldots\), corresponding to spin \((n-1)/2\). The quadratic Casimir is \(c_n=(n^2-1)/4\). Define the normalized heat-kernel family on SU(2):

\[
K_q(g)=\sum_{n=1}^{\infty}n\,q^{n^2-1}\,\chi_n(g),
\qquad 0<q<1.
\]

It is a positive class-function probability density (by the classical compact-group heat-kernel theorem); the coefficient in the trivial representation is 1. The source group identities are
\[
\int_{\mathrm{SU(2)}}\chi_n(Au)\chi_m(u^{-1}B)\,du
=\frac{\delta_{nm}}{n}\chi_n(AB).
\]
Hence the **Haar convolution** of these positive densities satisfies exactly
\[
K_q*K_r=K_{qr}.
\]

On a **simply connected two-dimensional lattice region with boundary holonomy fixed**, integrating shared interior links by this formula multiplies normalized character coefficients. Thus a \(3\times3\) patch (9 plaquettes) has coarse density \(K_{q^9}\), and the next factor-three block (81 fine plaquettes total) gives \(K_{q^{81}}\):
\[
\boxed{B_3(B_3 K_q)=B_9 K_q=K_{q^{81}}.}
\]
This is an exact statement for the 2D heat-kernel model, not an assertion that the *four-dimensional Wilson* effective action closes under blocking. Global topological sectors on a torus require additional treatment, which is why this control is formulated for a disk.

**Independent integer algebra:** the checker uses SU(2) characters \(\chi_n(\cos\theta)=U_{n-1}(\cos\theta)\), where \(U\) is a Chebyshev polynomial of the second kind. SU(2) Haar on \(S^3\) has exact monomial moments
\[
\mathbb E_{\rm Haar}[(\cos\theta)^{2m}]
=\frac{1}{4^m}\frac{1}{m+1}\binom{2m}{m};
\quad \mathbb E[(\cos\theta)^{2m+1}]=0.
\]
It checks **144 orthogonality products** independently for \(n,m=1,\dots,12\) and validates the correct representation dimensions and \(1/n\) Schur convolution normalization. The infinite heat-kernel semigroup itself uses the classical representation-theoretic identity; the 144 tests are its finite algebraic corroboration, not an exhaustive infinite-series proof.

### A controlled sharpening sequence at increasing heat-kernel coupling

Take a sequence of finer 2D plaquettes of area \(a_k^2=9^{-k}\), and set
\[
q_k=1-\frac{1}{2\cdot9^k},\qquad m_k=9^k.
\]
As \(k\) increases, \(q_k\uparrow1\), the heat kernel on each fine plaquette becomes sharply localized around the identity, and the inverse diffusion parameter \(1/(1-q_k)=2\cdot9^k\) grows. This is a **heat-kernel coupling parameter**, not the identical bare Wilson coupling \(\beta\).

At fixed blocked physical area one, the exact coefficient for representation \(n\) is
\[
c_{n,k}=q_k^{m_k(n^2-1)}.
\]
For every integer \(m\ge1\), using \(-x-x^2/[2(1-x)]\le\log(1-x)\le-x\) at \(x=(2m)^{-1}\) gives
\[
-\frac12-\frac1{8m-4}
\le m\log\left(1-\frac1{2m}\right)
\le-\frac12.
\]
Therefore each fixed representation has the **exact** controlled limit
\[
\boxed{c_{n,k}\longrightarrow \exp\left(-\frac{n^2-1}{2}\right),}
\]
with log-coefficient error at most \((n^2-1)/(8m_k-4)\). The checker validates rational blocked coefficients for \(k=1,2,3,4\) (9, 81, 729 and 6,561 fine plaquettes), their strict monotonicity, and the explicit rational remainder denominators 68, 644, 5,828 and 52,484. The all-\(k\) statement comes from the preceding logarithm inequality, not extrapolating four values.

**Certified representation-tail control:** \(q_k^{m_k}\le2/3\). Since \(|\chi_n(g)|\le n\) and the successive tail terms \(n^2(2/3)^{n^2-1}\) decrease by a factor less than \(1/2\) for \(n\ge10\), truncating \(K_{q_k^{m_k}}\) after \(n=9\) has a uniform supremum-norm error bounded by
\[
\sum_{n=10}^{\infty} n^2(2/3)^{n^2-1}
\le 200(2/3)^{99}<10^{-12}.
\]
All inequalities are exact rational checks. The 2D heat kernel is a valuable mathematically exact **increasing-coupling benchmark**, not a solution of the interacting 4D problem.

**References:** the [2D heat-kernel formulation and subdivision property](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.104.065003) and the [exact 2D versus approximate higher-dimensional Migdal recursion distinction](https://citeseerx.ist.psu.edu/document?doi=e29aac1e79609368496d9c16927e4a13a331d620&repid=rep1&type=pdf) are established background. The project checker independently checks exact low-representation Haar identities and the supplied rational tail gates.

## 2. Four-dimensional Wilson action: the local obstruction is explicit

Now switch to **four-dimensional continuous-SU(2) Wilson theory**, with the actual plaquette Boltzmann factor \(e^{\beta a_p}\), \(a_p(U)=\tfrac12\operatorname{ReTr}(U_p)\). An oriented link \(U\) is incident to **six plaquettes**, two in each of the three transverse directions. Express each incident plaquette term as \(a_p=\tfrac12\mathrm{ReTr}(UA_i)\), with six **unit SU(2)** staple holonomies \(A_1,\dots,A_6\) depending on the other link variables (and orientations incorporated into \(A_i\)).

The exactly integrated one-link local weight is
\[
Z_\beta(A_1,\dots,A_6)
=\int_{\mathrm{SU(2)}}\exp\left(\beta\sum_{i=1}^{6}
  \frac{\mathrm{ReTr}(UA_i)}2\right)dU.
\]
Identify SU(2) with unit quaternions \(u\in S^3\), and associate to each staple its real four-vector \(v_i\) so that \(a_p=u\cdot v_i\). With \(Q=\left|\sum_i v_i\right|^2\), the **actual Haar integral reduces exactly** to
\[
\boxed{Z_\beta(Q)=
 \sum_{m=0}^{\infty}\frac{(\beta^2 Q)^m}
   {4^m\,m!(m+1)!}.}
\]
This equality is exact for any fixed \(\beta\ge0\) and any physically admissible staple six-tuple. Every term is a nonnegative rational number when \(\beta,Q\) are rational. It is **not** a numerical evaluation of all links in the full lattice.

The first interaction term is
\[
\log Z_\beta
=\frac{\beta^2 Q}{8}+O(\beta^4),
\qquad
Q=6+\sum_{i<j}\operatorname{Tr}(A_i^{-1}A_j).
\]
So at second order, one eliminated link introduces **15 pairwise staples** with coefficients \(\beta^2\operatorname{Tr}(A_i^{-1}A_j)/8\). Of these pairs, **12 connect plaquettes in different transverse planes**. Their combined oriented boundary includes **six edges, forming a nonplanar chair loop** rather than one elementary plaquette. Integer geometry explicitly verifies that two \((\mu,\nu)\) and \((\mu,\rho)\) plaquettes share precisely one link and have six remaining boundary edges.

A nontrivial mixed term can be certified **well beyond the infinitesimal-\(\beta\) series**. Fix four staple holonomies to \(+I\) and let the other two independently be \(+I\) or \(-I\). Their four exact quaternion-sum squared norms are
\[
Q_{++}=36,\quad Q_{+-}=Q_{-+}=16,\quad Q_{--}=4.
\]
The mixed second derivative (in the sign-variation sense) is
\[
Q_{++}-Q_{+-}-Q_{-+}+Q_{--}=8,
\]
so the mixed coefficient in \(\log Z_\beta\) at \(\beta^2\) is **exactly 1**. This rules out treating the one-link integrated weight as a product of functions independent in those two varying staples. It is a *local non-factorization control*, not a proof that every possible 4D coarse-link action must contain an independent chair coupling.

### Exact rational Haar-tail certificates at increasing Wilson \(\beta\)

For a partial sum through \(m=N\), write \(a_m=(\beta^2Q)^m/(4^m m!(m+1)!)\). The successive term ratio is
\[
\frac{a_{m+1}}{a_m}=\frac{\beta^2Q}{4(m+1)(m+2)}.
\]
Once the ratio falls below one, the omitted positive tail is bounded by its first omitted term divided by one minus the following maximal ratio. The checker uses this exact bound for \(Q\in\{0,4,16,36\}\), at the following genuine **Wilson** \(\beta\):

| Wilson \(\beta\) | Taylor terms through \(N\) | Certified interval for \(R=Z_\beta(36)Z_\beta(4)/Z_\beta(16)^2\) |
|---:|---:|---:|
| 1 | 40 | \([1.365888,1.365889]\) |
| 4 | 40 | \([1.512545,1.512546]\) |
| 16 | 96 | \([1.533420,1.533421]\) |
| 64 | 384 | \([1.538087,1.538088]\) |

All four strict interval bounds are certified with **exact integer comparisons**, relative Taylor tail below \(10^{-12}\), and \(R>6/5\). These values are bounds on a local gauge-link Haar integral at imposed staple values, not experimental masses or 4D bulk observables.

The takeaway is precise: the **two-dimensional heat-kernel semigroup works exactly**, including as its bare kernel becomes sharply concentrated. Meanwhile **four-dimensional Wilson link elimination necessarily involves mixed staple interactions in the local integrand**. A Wilson-only proxy or naïvely iterated character law omitting such networks cannot be promoted to a rigorous 4D weak-coupling renormalization map without bounding its error.

## 3. What remains to prove in the actual four-dimensional Yang–Mills program

Our next viable RG certificate must work with a **gauge-invariant Wilson-network basis**, not only plaquette couplings. It must quantify at least:

1. **Nonplanar chair and higher-character network coefficients** created by an exact decimation and their overlap/compatibility on adjacent eliminated links.
2. **Large-field tails and induced long-range interaction norms** along an actual four-dimensional running \(\beta(a)\to\infty\), rather than the finite-volume or strong-coupling-only norms of YM4-04A/B.
3. **Transfer operator positivity and full physical spectral control**, including either a uniform lower bound on the true first gap in physical units or an independently certified nonzero first-excitation overlap. A tiny upper bound on a chosen Wilson correlation alone is insufficient.
4. **Summable, volume-uniform scale errors** for arbitrarily many ternary refinements and an actual nontrivial 4D SU(2) continuum reconstruction.

The exact 2D model is a comparator for method and error discipline, **not evidence that the higher-dimensional induction is complete**. The new 4D local calculation identifies an explicit class of interactions that any serious weak-coupling block operator must retain or quantitatively control.

## Verification

The [predictions](PREDICT-YM4-05A-CHARACTER-WEAK-COUPLING-20261107.hbp), [integer-only verifier](../tests/test_ym4_05a_character_weak_coupling.py), [14-row hosted measurement](../tests/YM4_05A_CHARACTER_WEAK_RECEIPT.hbp), and [dedicated CI workflow](../.github/workflows/ym4-05a-su2-character-weak.yml) preserve evidence hashes and require **eight false mathematical statements** to exit with named RED receipts.

**Disposition:** exact two-dimensional increasing-coupling benchmark **PASS**, local four-dimensional Wilson-link mixed-network diagnostic **PASS**, true four-dimensional renormalized flow **OPEN**, physical mass gap **OPEN**, nontrivial continuum SU(2) Yang–Mills existence **OPEN**. No Clay Millennium proof is claimed.
