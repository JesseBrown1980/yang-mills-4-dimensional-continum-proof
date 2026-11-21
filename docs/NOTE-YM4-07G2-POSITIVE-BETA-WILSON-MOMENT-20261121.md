# YM4-07G2 — explicit positive-coupling fourth transfer moment for a genuine 4D SU(2) blocked Wilson loop

**November 21, 2026.** This **post-original-freeze** improvement was predicted in [YM4-07G2 HBP](PREDICT-YM4-07G2-POSITIVE-BETA-WILSON-MOMENT-20261121.hbp) at commit \`b3dd81419e554412f5e0ec268bf559f7d03fc070\`, **before** the dedicated added moment test. The initial [YM4-07G frozen prediction](PREDICT-YM4-07G-ORIGINAL-4D-TRANSFER-20261121.hbp) remains untouched and continues to describe the positive-\(\beta\) Wilson moment as uncomputed there. This note supplies a subsequent **analytic lower enclosure** at one rigorously fixed coupling for the original four-dimensional Wilson transfer.

## 1. Genuine physical SU(2) source and transfer setting

Use the exact 4D continuous SU(2) finite Wilson transfer of [YM4-02c](LEMMA-0004-REFLECTION-TRANSFER.md) and the four-dimensional lattice geometry of [YM4-07G](NOTE-YM4-07G-ORIGINAL-4D-TRANSFER-TRACE-20261121.md): spatial 6³, \(V=216\), \(N_\ell=N_s=648\), normalized product Haar, \(\beta=1/(2000V)=1/432000\), positive injective self-adjoint
\[
T=A^{1/2}BA^{1/2},\quad
A(U)=\prod_{p\,{\rm spatial}}e^{-\beta(1-a(U_p))},\quad
B(U,U')=\prod_{\ell\,{\rm spatial}}e^{-\beta(1-a(U_\ell U_\ell'^{-1}))},
\]
with \(a(g)=\frac12\operatorname{ReTr}g\). Let \(\Omega>0\) be the **true normalized Perron vacuum** \(\|\Omega\|_{L^2({\rm Haar})}=1\) of \(T\); its gauge invariance is established in YM4-02c.

Let \(F\) be the normalized fundamental character of the **eight-edge fine 2×2 spatial Wilson rectangle**, the pullback of the coarse spatial plaquette under the original ordered factor-two line map. All eight fine edges are distinct, so under free product Haar \(F\) has mean zero, second moment \(1/4\), and \(|F|\le1\). Set
\[
m=\langle\Omega,F\Omega\rangle,\qquad
u=(F-m)\Omega,\qquad
0<\|u\|^2=\operatorname{Var}_{\Omega^2\,d{\rm Haar}}(F)\le1.
\]
Both \(\Omega\) and \(F\Omega\) are in the chosen **blocked spatial-slice cyclic subspace** \(\mathcal K\) of YM4-07E. In the YM4-07F witness jump, the exact positive-\(\beta\) subtraction is
\[
d_4=\frac{\langle u,T^4u\rangle}{\langle u,u\rangle}.
\]
The goal is an explicit strictly positive **rational** lower bound for this physical transfer fourth-moment quotient.

## 2. Exact SU(2) Peter–Weyl one-link eigenvalue

For a single spatial link, the central Wilson-convolution kernel \(w_\beta(UV^{-1})\) acts on irreducible SU(2) matrix coefficients of representation dimension \(d\) by the scalar \(b_d=\int w_\beta(g)\chi_d(g)/d\,dg\). The constant channel has
\[
b_0=\int e^{-\beta}e^{\beta a(g)}\,dg
\ \ge e^{-\beta},
\]
by Jensen and \(\mathbb E_{\rm Haar}a(g)=0\). The spin-\(\frac12\) fundamental channel has \(\chi_{\rm fund}=2a\), so
\[
b_{\rm fund}
=e^{-\beta}\int a(g)e^{\beta a(g)}dg
=e^{-\beta}\sum_{k=0}^\infty
\frac{\beta^{2k+1}}{(2k+1)!}\mathbb E[a^{2k+2}]
\ \ge e^{-\beta}\frac{\beta}{4}>0.
\]
All odd Haar moments vanish under \(g\mapsto-g\), and all even terms are nonnegative. The exact Haar second moment \(\mathbb E[a^2]=1/4\) is independent of any finite quaternion design.

The Wilson rectangle \(F\) contains exactly eight distinct fundamental (or dual fundamental) matrix coefficients and is constant on the remaining \(N_\ell-8\) links. Hence it is an **exact eigenfunction of the linkwise convolution \(B\)**:
\[
BF=b_{\rm fund}^{8} b_0^{N_\ell-8}F,\qquad
b_{\rm fund}^{8} b_0^{N_\ell-8}
\ \ge\ e^{-\beta N_\ell}(\beta/4)^8.
\]
This is a genuine SU(2) character decomposition, with the original unmodified Wilson kernel.

## 3. Lower bound on overlap with the physical vacuum

From the positive original transfer kernel range \(e^{-12\beta V}\le T(U,U')\le1\), the Perron equation and normalized Haar imply
\[
e^{-12\beta V}\le\Omega(U)\le e^{12\beta V}.
\]
The spatial half-action obeys \(e^{-3\beta V}\le A^{1/2}(U)\le1\). Put \(h=A^{1/2}\Omega\). At \(\beta V=1/2000\),
\[
h(U)\ge e^{-15\beta V}>1-\frac{15}{2000}=\frac{397}{400},
\quad
h(U)\le e^{12\beta V}<\frac{1}{1-12/2000}=\frac{500}{497}.
\]
The true vacuum Wilson mean differs from the Haar-zero mean by
\[
|m|=\left|\int F(\Omega^2-1)d{\rm Haar}\right|
\le e^{24\beta V}-1
<\frac{24/2000}{1-24/2000}=\frac3{247}.
\]
Define the **actual Haar Fourier overlap of the physical Schur witness**
\[
C=\langle F,A^{1/2}u\rangle
=\int F(F-m)h\,d{\rm Haar}.
\]
Using \(\int F^2d{\rm Haar}=1/4\) and \(|F|\le1\),
\[
\begin{aligned}
C&\ge \frac14 \min h-|m|\max h\\
&>\frac{397}{1600}-\frac{1500}{247\cdot497}
=\boxed{\frac{46335323}{196414400}}>\frac15.
\end{aligned}
\]
This is a **positive quantitative overlap with the genuine four-dimensional physical-vacuum-centered Wilson source**, derived without computing \(\Omega\) numerically.

## 4. Positive fourth transfer-moment and Schur-decrement certificate

Set \(g=A^{1/2}u\). Because the true \(B\) is positive and its Wilson rectangle \(F\) is an eigenvector,
\[
\begin{aligned}
\langle u,Tu\rangle
&=\langle g,Bg\rangle\\
&\ge b_{\rm fund}^8b_0^{N_\ell-8}
\frac{|\langle F,g\rangle|^2}{\|F\|^2}\\
&>4\,e^{-\beta N_\ell}(\beta/4)^8\left(\frac15\right)^2
=\frac4{25}e^{-\beta N_\ell}(\beta/4)^8.
\end{aligned}
\]
Here \(\beta N_\ell=3\beta V=3/2000\), so \(e^{-\beta N_\ell}>1-3/2000=1997/2000\), and \(\beta/4=1/1728000\). Therefore
\[
\boxed{\quad
\langle u,Tu\rangle>
\frac{1997}{12500\,(1728000)^8}.
\quad}
\]
For the positive operator \(T\), the spectral probability measure of the normalized \(u/\|u\|\) and Jensen's \(x\mapsto x^4\) inequality yield
\[
d_4=\frac{\langle u,T^4u\rangle}{\|u\|^2}
\ge\left(\frac{\langle u,Tu\rangle}{\|u\|^2}\right)^4.
\]
As \(\|u\|^2\le1\), we conclude the **strict fully rational physical Wilson-source fourth-moment bound**
\[
\boxed{\quad
d_4>
\left[\frac{1997}{12500\,(1728000)^8}\right]^4
=\frac{1997^4}{12500^4\,1728000^{32}}>0.
\quad}
\]
Thus adding the actual blocked Wilson source to the vacuum witness strictly lowers the full four-dimensional YM4-07F fourth-trace residual by at least this explicit rational amount, at **positive** \(\beta=1/432000\). It is extremely small and does not independently advance the accepted whole-spectrum gap threshold from YM4-07G. Its significance is a source-authenticated nonzero positive-\(\beta\) moment calculation for the original genuine-SU(2) Wilson transfer.

## 5. Calibration and next gates

The exact integer checker in [the YM4-07G2 test](../tests/test_ym4_07g2_positive_beta_wilson_moment.py) verifies the SU(2) character normalization, eight distinct link supports, the strict rational \(C>1/5\) inequality, the one-link and fourth-moment rational lower bounds, and adversarial controls that reject replacing the true Perron vacuum by the constant vector at positive coupling. The analytic proof above supplies the group integration and spectral arguments; integer checks validate exact constants rather than substituting finite sampling for Haar.

**Status:** first fully explicit **positive-\(\beta\) fourth transfer-moment lower bound on a matched Wilson source of the original 4D SU(2) lattice**, analytically DERIVED; amount is conservative and finite-volume; external independent proof review and hosted verification pending. **Open:** actual 4D transfer-moment value and upper enclosure tight enough for large \(\beta\), effective weak-coupling action and all-scale RG, ultraviolet/infinite-volume uniformity, nontrivial OS continuum and full physical mass gap.
