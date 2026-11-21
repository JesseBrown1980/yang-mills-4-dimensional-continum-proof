# YM4-07H — genuine four-dimensional continuous-SU(2) weak-coupling transfer by certified Peter–Weyl cutoffs

**November 21, 2026.** The [prediction-first HBP](PREDICT-YM4-07H-ALLBETA-SU2-PETER-WEYL-20261121.hbp) was committed at \`0fa5c2dcdecec61ae409333e8cdc25dbfbc6c9c8\` **before** the checker. This note advances the original 4D Wilson transfer work from [YM4-07G/G2](NOTE-YM4-07G-ORIGINAL-4D-TRANSFER-TRACE-20261121.md) to **arbitrarily large finite \(\beta\)**. Its essential improvement is a rigorous **absolute trace-norm truncation certificate** for the complete gauge-projected transfer, with a separate **polynomial-coupling Perron floor**. The remaining challenge is to make these bounds *relative* to the vacuum and uniform in spatial volume and physical cutoff.

## 1. Original four-dimensional SU(2) transfer, without changing the gauge group

Work with the genuine continuous group \(G=\mathrm{SU}(2)\), normalized Haar measure, the finite spatial periodic lattice \((\mathbb Z/L\mathbb Z)^3\), \(L\ge 6\), spatial volume \(V=L^3\), \(N_\ell=N_s=3V\). Use the **original** Wilson Boltzmann weight
\[
w_\beta(g)=\exp[-\beta(1-\tfrac12\operatorname{ReTr}g)],\quad \beta>0.
\]
On \(H=L^2(G^{N_\ell})\) define
\[
A(U)=\prod_{p\ {\rm spatial}}w_\beta(U_p),\quad
B(U,U')=\prod_{\ell\ {\rm spatial}}w_\beta(U_\ell U_\ell'^{-1}),\quad
T=A^{1/2}BA^{1/2}.
\]
Let \(P\) be the full gauge-invariant projector. By [YM4-02c](LEMMA-0004-REFLECTION-TRANSFER.md), \(P\) commutes with \(T\), \(T\) is positive trace class, \(0\le T\), \(\operatorname{Tr}T=\int A\le1\), and its simple maximal eigenvalue \(\lambda_0>0\) has a gauge-invariant positive eigenfunction. Also \(\operatorname{Tr}(T^nP)=Z_{\Lambda,n}\), the original periodic-time four-dimensional Wilson partition function with **all spatial and temporal interactions** for integer \(n\ge2\).

## 2. Exact Peter–Weyl temporal-link spectrum and power-of-three truncation

The normalized Wilson convolution on a **single continuous SU(2) link** is
\[
(B_1f)(u)=\int_Gw_\beta(uv^{-1})f(v)\,dv.
\]
For every irreducible representation of dimension \(d=1,2,\ldots\), character orthogonality gives the eigenvalue
\[
\boxed{\quad b_d(\beta)
=e^{-\beta}\frac{2}{\beta}I_d(\beta)>0,\quad
\text{multiplicity }d^2.\quad}
\]
Here \(I_d\) is the modified Bessel function. The identity is for the **continuous SU(2)** Wilson character expansion, not a discrete design. Since \(B_1(u,u)=w_\beta(1)=1\), Mercer/character completeness gives
\[
\sum_{d=1}^{\infty}d^2b_d(\beta)=\operatorname{Tr}B_1=1.
\]

Let \(\Pi_N\) retain **all matrix coefficients** of irreducible representations of dimensions \(1,\ldots,N\). This projector is invariant under independent left and right group translations; hence its tensor product over all spatial links commutes with every lattice gauge transformation. Define
\[
B_N=B_1^{\otimes N_\ell}\left(\Pi_N^{\otimes N_\ell}\right),\qquad
T_N=A^{1/2}B_NA^{1/2}.
\]
Then \(0\le B_N\le B\), \(0\le T_N\le T\) (operator order), and \(T_N\) is **finite rank**, self-adjoint, positive and gauge invariant; in particular \([T_N,P]=0\). The complete spatial Wilson action \(A\) remains **exact**. The only approximation is discarding high irreducible channels from each **temporal transfer convolution**.

The rank of \(B_N\) is
\[
\operatorname{rank}B_N=
\left(\sum_{d=1}^N d^2\right)^{N_\ell}
=\left(\frac{N(N+1)(2N+1)}6\right)^{N_\ell}.
\]
The gauge-invariant rank is no larger. This number is enormous for a large spatial volume: it is an exact mathematical truncation, **not** a claim that a dense matrix of that dimension has been constructed or diagonalized.

## 3. Nonperturbative high-representation tail bound for every \(\beta\ge1\)

The exact **positive** Bessel series is
\[
I_d(\beta)=\frac{(\beta/2)^d}{d!}
\sum_{j=0}^{\infty}\frac{(\beta^2/4)^j d!}{j!(d+j)!}.
\]
Since \((d+j)!\ge d!(d+1)^j\),
\[
I_d(\beta)\le\frac{(\beta/2)^d}{d!}
\exp\left(\frac{\beta^2}{4(d+1)}\right).
\]
If \(N\) is any integer satisfying \(N\ge4\beta\) and \(d>N\), then
\(\beta^2/[4(d+1)]\le\beta\), so \(e^{-\beta}\exp(\cdots)\le1\). Thus
\[
0<d^2b_d(\beta)\le
\frac{d^2(\beta/2)^{d-1}}{d!}=:a_d.
\]
For \(d\ge N+1\),
\[
\frac{a_{d+1}}{a_d}
=\frac{\beta(d+1)}{2d^2}<\frac14,
\]
because \(d\ge4\beta\ge4\). Therefore the omitted **one-link trace** is bounded by
\[
\begin{aligned}
\varepsilon_N(\beta)
&=\sum_{d>N}d^2b_d(\beta)
<2a_{N+1}\\
&=\frac{2(N+1)}{N!}\left(\frac{\beta}{2}\right)^N
\le2(N+1)\left(\frac{3\beta}{2N}\right)^N\\
&\le\boxed{\,2(N+1)(3/8)^N\,}.
\end{aligned}
\]
The last inequalities use the elementary factorial bound \(N!>(N/e)^N\) and \(e<3\), with **no decimal approximation**. The same proof extends to \(0<\beta<1\) when \(N\ge4\), but all new weak-coupling benchmarks use \(\beta\ge1\).

**Tensor and full-operator error.** Since \(B=B_1^{\otimes N_\ell}\) and \(\operatorname{Tr}B_1=1\),
\[
\begin{aligned}
\|B-B_N\|_1
&=\operatorname{Tr}(B-B_N)
=1-(1-\varepsilon_N)^{N_\ell}\\
&\le N_\ell\varepsilon_N.
\end{aligned}
\]
As \(0\le A\le1\), the trace-class ideal inequality yields
\[
\boxed{\quad
\|T-T_N\|_1\le N_\ell\varepsilon_N
<2N_\ell(N+1)(3/8)^N.\quad}
\]
Exactly the same upper bound holds after gauge projection \(P\), because compression by a norm-one orthogonal projection cannot increase trace norm. This is an **actual original-four-dimensional continuous-SU(2) transfer-operator approximation theorem for all finite \(\beta\ge1\)**. It includes the complete noncommutative spatial Wilson action and all gauge-invariant physical sectors.

Because \(\|T\|,\|T_N\|\le\operatorname{Tr}T\le1\), the noncommutative telescoping identity
\(T^n-T_N^n=\sum_{j=0}^{n-1}T^{n-1-j}(T-T_N)T_N^j\)
gives for every integer \(n\ge1\)
\[
\boxed{\quad
0\le \operatorname{Tr}(T^nP)-\operatorname{Tr}(T_N^nP)
<2nN_\ell(N+1)(3/8)^N.\quad}
\]
Trace positivity follows from min–max eigenvalue monotonicity on the invariant physical subspace, **not** from an unjustified claim that noncommuting \(T^n-T_N^n\) is operator-positive. For any finite source vector \(v\),
\[
|\langle v,(T^n-T_N^n)v\rangle|
\le2nN_\ell(N+1)(3/8)^N\,\|v\|^2.
\]
Also \(0\le\lambda_0(T)-\lambda_0(T_N)\le N_\ell\varepsilon_N\). Controlling the *physical spectral projector* or *relative* vacuum error requires an additional spectral-separation estimate; the absolute bound above is not silently promoted.

## 4. Exact ternary cutoff jumps at nontrivial \(\beta\)

Take the same original 4D spatial geometry as YM4-07G: \(L=6\), \(N_\ell=N_s=648\); use the genuine temporal period \(n=4\). The universal rigorous **absolute** moment error upper bound is
\[
E_{4,N}=2(4)(648)(N+1)(3/8)^N.
\]

| Bare coupling | Irrep cutoff \(N=3^k\) | Truncation gate | Rigorous four-step trace error |
|---|---:|---|---|
| \(\beta=4\) | \(N=27\) | PASS | \(E_{4,27}<10^{-6}\) |
| \(\beta=9\) | \(N=81\) | PASS | \(E_{4,81}<10^{-20}\) |
| \(\beta=64\) | \(N=243\) | HOLD (\(243<4\beta=256\)) | Not certified by this envelope |
| \(\beta=64\) | \(N=729\) | PASS | \(E_{4,729}<10^{-100}\) |

The cutoff jumps \(27\to81\to729\) are *representation-space jumps*, not power-of-three time evolution and not a claim of polynomial-time matrix multiplication. They avoid a continuum-group discretization: every retained Fourier matrix coefficient is an **exact SU(2) representation channel**. Errors are genuine trace bounds on \(T\), even though no gigantic finite matrix or its spectrum has been computed.

For an arbitrary finite sequence of couplings \(\beta_j\ge1\), spatial volumes \(N_{\ell,j}\), and integer moment powers \(n_j\), choose a power-of-three cutoff \(N_j=3^{k_j}\) so that
\[
N_j\ge4\beta_j,\qquad
2n_jN_{\ell,j}(N_j+1)(3/8)^{N_j}<3^{-j}.
\]
Such \(k_j\) **exists** because the exponential tail outruns any fixed polynomial. This is a concrete summable **per-scale Fourier approximation budget**, \(\sum_{j\ge1}3^{-j}=1/2\). It does not imply an RG comparison between different Hilbert spaces or any volume/cutoff-uniform mass gap: those need the corresponding renormalization maps and spectral estimates.

## 5. Genuine high-coupling Perron floor by an SU(2) Haar cap

The existing constant-trial Jensen bound \(\lambda_0\ge e^{-6\beta V}\) becomes exponentially weak in \(\beta\). Here is an independent **polynomial-coupling** alternative at fixed volume. Given any real \(\beta\ge1\), choose an integer \(k\ge1\) with \(\beta\le k^2\), and put \(r=1/(8k)\le1/8\). Regard SU(2) as the unit-quaternion 3-sphere. Define the northern Haar cap
\[
C_r=\{u=(\sqrt{1-|x|^2},x)\in S^3: x\in\mathbb R^3,\ |x|\le r\}.
\]
The normalized Haar density in this coordinate ball is
\((2\pi^2)^{-1}(1-|x|^2)^{-1/2}dx\), so
\[
\operatorname{Haar}(C_r)>
\frac{2r^3}{3\pi}>\frac{r^3}{6}.
\]
Every \(u\in C_r\) obeys \(|u-1|\le2r\). Consequently, for any four-link plaquette of fields in the cap, the quaternion product inequality gives \(|U_p-1|\le8r\), and for two same-link fields \(u,u'\in C_r\), \(|uu'^{-1}-1|\le4r\). Since \(1-\operatorname{ReTr}(g)/2=|g-1|^2/2\), the spatial and temporal Wilson exponents on the cap satisfy
\[
\frac{S_{\rm spatial}(U)+S_{\rm spatial}(U')}{2}
+S_{\rm temporal}(U,U')
\le\beta r^2(32N_s+8N_\ell).
\]

Let \(\phi\) be the normalized characteristic function of \(C_r^{N_\ell}\) in the **full** spatial Haar Hilbert space. Although this particular \(\phi\) is not gauge invariant, Rayleigh–Ritz is valid on the full \(H\), and the **simple top eigenfunction is gauge invariant**, so its top eigenvalue is exactly the physical \(\lambda_0\). Thus
\[
\lambda_0\ge\langle\phi,T\phi\rangle
>\left(\frac{r^3}{6}\right)^{N_\ell}
e^{-\beta r^2(32N_s+8N_\ell)}.
\]
Using \(\beta r^2\le1/64\), the **original finite-volume SU(2) Perron root** satisfies
\[
\boxed{\quad
\lambda_0>
(3072\,k^3)^{-N_\ell}
\exp[-N_s/2-N_\ell/8].\quad}
\]
At spatial \(L=6\), \(N_\ell=N_s=648\), and using \(e<3\), this becomes the **exact rational floor**
\[
\boxed{\quad
\lambda_0>
\frac{1}{3^{405}(3072\,k^3)^{648}}\,,\quad \beta\le k^2.\quad}
\]
For \(\beta=k^2\), this behaves **polynomially in \(\beta\)** at fixed volume, with a large volume-dependent exponent. It is an *analytic vacuum lower enclosure*, not a solved large-\(\beta\) eigenvalue.

**Concrete comparison at \(\beta=64\).** Choose \(k=8\). Since \(3072\cdot8^3=1{,}572{,}864<3^{14}\), the new floor is \(>3^{-9477}\). The old Jensen lower bound is \(e^{-6\beta V}=e^{-82944}\), which is **strictly smaller than** \(2^{-82944}<3^{-41472}\), by \(e>2\), \(2^2>3\). Thus the cap floor is provably far stronger at this coupling:
\[
\boxed{\quad \lambda_0>3^{-9477}>3^{-41472}>e^{-82944}.\quad}
\]
This is a real **large-\(\beta\)** improvement in the original Wilson transfer's certified vacuum floor.

## 6. The remaining spectral bottleneck is now measurable

The Fourier tail bounds in section 4 are **absolute**. A continuum physical gap requires comparing the actual excited spectrum to \(\lambda_0\), and transferring the resulting estimates uniformly as both spatial volume and bare coupling grow. The cap bound is much better than the earlier exponential Jensen floor at large \(\beta\), yet extremely conservative.

At \(\beta=64\) and \(N=729\), the currently certified upper bound \(2N_\ell(N+1)(3/8)^N\) on \(\|T-T_N\|_1\) remains **larger than** the cap lower bound on \(\lambda_0\). This means **the available pair of bounds does not certify a small relative vacuum error**, even though the absolute transfer trace error is below \(10^{-100}\) at four steps. This is a *certified HOLD for the present envelopes*, not a claim that the actual truncation error is that large.

The next producer should exploit (i) a stronger spatially localized/gauge-fixed vacuum Rayleigh trial; (ii) high-accuracy character-sparse evaluations of the **finite-rank** \(T_N\), retaining the full \(A\); (iii) rigorous **relative** eigenvalue/projector enclosures and Wilson-source Gram/moment entries; (iv) volume-uniform and summable across-cutoff RG control. In particular, a verified small **absolute** transfer error alone does not imply the complete continuum spectral gap.

## 7. Acceptance status and adversarial controls

- **DERIVED:** original 4D continuous-SU(2) Peter–Weyl temporal convolution, gauge-covariant finite-rank \(T_N\), explicit positive trace-norm bound, four-step partition/moment error, exact power-of-three cutoffs.
- **DERIVED:** Haar-cap variational lower bound on the **physical** Perron eigenvalue that is polynomial in \(\beta\) at fixed finite volume, with strict rational \(\beta=64\) improvement.
- **FROZEN FIRST:** prediction HBP committed before test source.
- **MEASUREMENT REQUIRED:** integer-only rational controls at \(\beta=4,9,64\), invalid \(N=243\) refusal, absolute-versus-relative HOLD, independent mathematical review, hosted execution.
- **OPEN:** practical finite-rank matrix evaluation, 4D positive-\(\beta\) vacuum and Wilson source moment enclosures at large \(\beta\), relative spectral projector control, volume- and cutoff-uniform all-scale renormalization, interacting OS continuum construction and physical mass gap.

In this theorem, \(\beta\ge1\) spans arbitrarily large finite weak bare couplings, but **no continuum cutoff limit or infinite-volume physical gap** follows from these finite-volume truncation bounds.
