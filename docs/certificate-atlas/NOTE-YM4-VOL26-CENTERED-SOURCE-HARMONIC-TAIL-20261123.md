# YM4 VOL26 — centered Wilson plaquette, exact one-face conditional response, and harmonic completeness certificate

**23 November 2026 · original four-dimensional continuous SU(2) Wilson theory · analytical candidate.** Continues VOL20–VOL25 and fixes one concrete **centered physical source** for the requested high-coupling source-predictor acceptance. The new results are an original-Wilson one-face derivative identity, a radius- and volume-independent Lipschitz bound, an exact positive continuous-SU(2) Haar approximation kernel, and a certified variance *tail* for every finite harmonic truncation. A genuine center-even spin-two Wilson-loop red control independently demonstrates the limitation of degree-two/13-coordinate truncation. The high-beta positive centered-source covariance lower bound remains an explicit OPEN obligation.

## 1. Freeze an actual original centered source

Use the original untwisted even periodic 4D SU(2) Wilson model with action
\[
 \mu_{\beta,L}(dU)=Z_{\beta,L}^{-1}
 \exp\{\beta\sum_{p}\operatorname{Re}U_p\}\,dH(U),\quad
 \beta\ge0,\quad L\ge2(b+2),\quad b=2r+1,\ r\ge1.
\]
The centered physical source is the elementary 0–1 plaquette at the lattice origin,
\[
 p_*=(0,0,0,0;0,1),\qquad
 F_*(U)=\frac{1+\operatorname{Re}U_{p_*}}2\in[0,1]. \tag{26.1}
\]
Every original link of this plaquette lies in the internal-link set \(T_r\). Its source-normalized exterior predictor is the genuine conditional Gibbs observable
\[
 f_r(B_r)=\phi_r(B_r)=\mathbb E_{\mu_{\beta,L}}[F_*\mid B_r].
\]
For the VOL15 exact original boundary-resultant action, define the finite-dimensional, strictly positive **actual continuous-Haar** interior partition integral
\[
 Z_r(B;t)=\int_{SU(2)^{T_r}}
 \exp\{\beta A_{\mathrm{int}}(U)+\beta\langle X(U),B\rangle+
             t\,\operatorname{Re}U_{p_*}\}\,dH_{T_r}(U).
\]
Then the selected physical predictor is explicitly
\[
 \boxed{\phi_r(B)=\frac12+\frac12\partial_t\log Z_r(B;t)\big|_{t=0}.} \tag{26.2}
\]
The formula is gauge-invariant and holds at every finite beta. At beta=0 the source predictor equals 1/2 identically, so the normalized variance \(V_r=\operatorname{Var}(\phi_r)\) is zero. To obtain a nonzero physical mass-rate certificate at beta>0 requires independently establishing \(V_r>0\) and a quantitative positive Dirichlet witness.

## 2. Original 4D geometry: four witness links each enter exactly one mixed plaquette

For each \(s,t\in\{\pm1\}\), use the VOL23–24 original outer-face parallel 0-link
\[
 q_{s,t}=((0,s(r+1),tr,0),0).
\]
The independent original-face enumeration proves **for every \(r\ge1\)** each of these four links belongs to exactly **one** original plaquette with precisely one internal link of \(T_r\). They are all contained in \(R_r\subset T_{r+1}\setminus T_r\). The all-r coordinate argument is simple: a mixed plaquette containing this 0-link needs a second 0-link with both endpoints in \(Q_r\), hence its other direction is the normal direction 1, and the inward face in that plane is unique. The four selected links have distinct original Wilson face supports; the rest of the source/collar remains the full original noncommuting lattice.

Fix any such \(q\), all other exterior links, and treat the value \(u=U_q\in SU(2)=S^3\) as a variable. Exactly **one** mixed Wilson plaquette contains \(q\), so the original interior Gibbs action can be rewritten
\[
 A_{\rm int}(U)+A_{\rm mixed}(U,\eta_{\widehat q},u)
       =A_0(U,\eta_{\widehat q})+\langle u,C(U,\eta_{\widehat q})\rangle,
 \qquad \|C(U,\eta_{\widehat q})\|=1. \tag{26.3}
\]
The quaternion coefficient is a genuinely original product of one internal and two other exterior SU(2) links, with correct cyclic orientation. For \(u,v\in S^3\), interpolate the **positive conditional interior density** with \(u_\tau=(1-\tau)u+\tau v\in\mathbb R^4\) in the *linear boundary source term*, keeping all original internal Wilson plaquettes unchanged. Covariance differentiation yields
\[
 \frac{d}{d\tau}\phi_r(u_\tau)
 =\beta\,\operatorname{Cov}_{\mu^{u_\tau}_{T_r}}
 \left(F_*,\langle v-u,C(U)\rangle\right).
\]
Since the two variables have ranges 1 and at most \(2\|v-u\|\), the elementary variance/Cauchy bound \(|\operatorname{Cov}(A,B)|\le\mathrm{range}(A)\mathrm{range}(B)/4\) proves the **sharp geometric one-face response envelope**
\[
 \boxed{|\phi_r(u)-\phi_r(v)|
               \le \frac{\beta}{2}\,\|u-v\|.} \tag{26.4}
\]
This bound is **independent of cube radius, total 4D torus size, and the values of every other exterior link**. It uses the real physical centered plaquette \(F_*\), not a boundary-loop substitute. The recentered source \(\phi_r-\mu(F_*)\) has the identical Lipschitz constant.

## 3. An explicit positive original SU(2) polynomial kernel with exact Haar moments

For any integer \(m\ge0\), define the normalized zonal kernel and polynomial operator
\[
 k_m(u,v)=\frac{((1+u\cdot v)/2)^m}
      {\int_{S^3}((1+u\cdot w)/2)^m\,dH(w)},\qquad
 (\mathcal B_m f)(u)=\int_{S^3}k_m(u,v)f(v)\,dH(v). \tag{26.5}
\]
Rotational Haar invariance makes the denominator independent of \(u\). Hence \(\mathcal B_m f\) is a **real polynomial in the four quaternion coordinates of total degree at most \(m\)**, restricted to \(S^3\); it is also a positive weighted mean of the true bounded function \(f\).

Let \(z=(1+u\cdot v)/2\in[0,1]\). Under the original continuous SU(2) Haar measure, \(z\) has the **exact** Beta(3/2,3/2) latitude law. Reweighting by \(z^m\) gives Beta(m+3/2,3/2), so
\[
 \int k_m(u,v)\,\|u-v\|^2\,dH(v)
       =\frac6{m+3}. \tag{26.6}
\]
This can also be proved without special-function tables from the exact Haar polynomial moment recurrence
\[
 \frac{\mathbb E_H z^{m+1}}{\mathbb E_H z^m}
       =\frac{2m+3}{2m+6}.
\]
Applying (26.4), Jensen and (26.6) gives a **uniform original-Wilson predictor approximation** for each fixed complementary exterior:
\[
 \boxed{\|\phi_r-\mathcal B_m\phi_r\|_{L^\infty(S^3)}
             \le \frac{\beta}{2}\sqrt{\frac6{m+3}}.} \tag{26.7}
\]
This is a mathematically explicit and unweighted source-specific harmonic completeness statement. The polynomial is constructed from continuous Haar integration; no finite-group physical approximation is substituted.

## 4. Exact local information-loss bracket, including VOL25's 13-harmonic witness

Condition on **all original links except \(q\)**. The true one-link Wilson conditional law is the continuous six-staple heat bath \(\nu_q\) of VOL25. With \(f(u)=\phi_r(B_r(\widehat U_q,u))\), set
\[
 \delta_q:=\mathbb E_\mu\operatorname{Var}_{\nu_q}(f),\qquad
 W_{q,m}:=\mathbb E_\mu\operatorname{Var}_{\nu_q}(P_{\le m}^{\nu_q}f), \tag{26.8}
\]
where \(P_{\le m}^{\nu_q}\) is the **true conditional \(L^2(\nu_q)\) orthogonal projection** onto all degree-\(\le m\) real spherical harmonics (including the constant). The polynomial \(\mathcal B_m f\) is an admissible competitor for this least-squares projection. Orthogonality and (26.7) therefore establish
\[
 \boxed{0\le\delta_q-W_{q,m}
 \le\min\left\{\frac14,\frac{3\beta^2}{2(m+3)}\right\},\qquad
 D_r(\phi_r)\ge\delta_q\ge W_{q,m}.} \tag{26.9}
\]
The term \(1/4\) follows from \(0\le f\le1\). The **first inequality brackets the local one-link loss \(\delta_q\)**; the full shell variance \(D_r\) can also contain information lost through the other shell links. Thus (26.9) is a valid local-source bracket, not an upper bound on the complete shell loss.

For \(m=2\), the conditional harmonic space has dimension \(1+4+9=14\), including the constant. The variance-projection term \(W_{q,2}\) is **exactly** VOL25's original-Wilson 13-feature covariance witness:
\[
 W_{q,2}=\mathbb E_\mu[v_{13}^\top C_{13}^{-1}v_{13}]. \tag{26.10}
\]
For every \(m>2\), (26.9) provides a rigorous **source-tail** specification for an expanded, original SU(2) harmonic verifier. Its constants are deterministic, all-beta and independent of the full 4D volume.

## 5. Native spin-two red: degree-two features can miss an entire original Wilson shell signal

Use one of VOL23's *genuine original six-link contractible Wilson holonomies* \(W=S_1S_2^{-1}\) and let \(x=\operatorname{Re}W=f_{s,t}(B_r)\). The normalized SU(2) **spin-two** character is the center-even genuine boundary Wilson observable
\[
 g(B_r)=\frac{\chi_2(W)}5
       =\frac{16x^4-12x^2+1}{5}. \tag{26.11}
\]
At beta=0 and conditional on all original links other than its selected outer-face link \(q\), \(x=u_q\cdot c\) for a fixed unit quaternion \(c\), and \(u_q\) is exactly Haar-uniform. The exact continuous \(S^3\) even moments are
\[
 E_H(x^2,x^4,x^6,x^8)=
  \left(\frac14,\frac18,\frac5{64},\frac7{128}\right).
\]
They prove
\[
 \boxed{E_H g=0,\quad\operatorname{Var}_H(g)=\frac1{25}>0,\quad
    \operatorname{Cov}_H(g,\psi)=0
 \ \text{for every spherical harmonic }\psi\text{ of degree }\le2.} \tag{26.12}
\]
Thus the **genuine original SU(2) Wilson** 13-coordinate witness equals zero for this center-even spin-two boundary function at beta=0, despite strictly positive one-link and shell variance. This extends VOL24's first-harmonic adjoint red to the **entire degree-two witness**. It gives a precise reason to require a higher-harmonic tail budget before declaring physical completeness.

The red control is a **boundary Wilson loop** designed to challenge the truncation. The centered interior physical source under certification remains the fixed plaquette (26.1).

## 6. Quantitative production coupling arithmetic and next acceptance

At the exact production integer \(\beta=9^{12}=282429536481\), requiring the rigorous local variance-tail allowance \(\delta_q-W_{q,m}\le1/256\) via (26.9) yields the sufficient exact harmonic degree
\[
 \boxed{m\ge 30630314141519043787530621.} \tag{26.13}
\]
The integer verifier checks this minimal degree for the stated **generic Lipschitz envelope** using only cross-multiplication. It is an intentionally conservative, computationally impractical uniform bound at such large bare beta: the full degree-\(\le m\) S³ polynomial space has dimension \((m+1)(m+2)(2m+3)/6\). Therefore the efficient next route is to obtain **source-specific** bounds on the actual first 13 (or a small adaptive set of higher) conditional harmonic covariances, rather than enumerate this conservative all-directions truncation.

**Independent exact checker:** [tests/ym4_vol26_centered_source_harmonic_tail.py](../../tests/ym4_vol26_centered_source_harmonic_tail.py) checks the original four-dimensional centered-plaquette link support, the exact single-mixed-face incidence for each of the four q links at radii 1–4, native Haar even moments through degree eight, the genuine spin-two red orthogonality, positive zonal kernel moments, the \(m=2\) 13-feature identification, and the production-beta integer tail threshold. Normal/optimized and strict no-float checks are frozen in the attached HBP/workflow.

**Acceptance scope:** physical centered Wilson source **SPECIFIED**; exact true-original-model one-face response, positive continuous-Haar polynomial kernel and local Dirichlet-tail inequality **ANALYTIC**; geometry/Haar/spin-two red/integer degree checks **REPRODUCIBLE**; strictly positive centered-source \(\delta_q\), \(V_r\), and source-normalized physical \(D_r/V_r\) at beta=9^12 **OPEN**; beta(a), all Gauss/winding-sector transfer, and the eleven original continuum construction requirements **OPEN**. Stage as a research candidate in draft PR #113; published 3D atlas and main remain unchanged.
