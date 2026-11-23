# YM4 VOL25 — exact block diagonalization of the native SU(2) 13-harmonic Wilson heat bath

**23 November 2026 · analytic continuous-SU(2) original-Wilson one-link theorem; strict integer tests.** Builds on [VOL24's genuine adjoint four-source polynomial Dirichlet Gram and 13-feature centered-source witness](NOTE-YM4-VOL24-NATIVE-ADJOINT-DEGREE2-20261123.md). The next arithmetic step is to make the 13-coordinate conditional covariance **explicit** and reduce its inversion to 2x2 problems. This is an exact local Wilson heat-bath reduction at every finite bare beta, not a numerical calculation of the centered interior-source predictor.

## 1. Original Wilson conditional law and exact scalar moment recurrence

For any original SU(2) link, condition on all remaining original four-dimensional Wilson links. Its six cyclic plaquette staples sum to a real unit-quaternion resultant H with norm at most 6. The **exact continuous-Haar** conditional link law is
\[
 \nu_{\kappa,n}(du)=Z(\kappa)^{-1}e^{\kappa(u\cdot n)}\,dH_{SU(2)}(u),
 \quad \kappa=\beta\|H\|\in[0,6\beta],\quad \|n\|=1.
\]
Set \(t=u\cdot n\). The original normalized S³ Haar marginal of t has density \((2/\pi)\sqrt{1-t^2}\) on [-1,1]. Let \(m_j=E_{\nu}(t^j)\), \(m_0=1\). Integrating the exact derivative of
\(t^j(1-t^2)^{3/2}e^{\kappa t}\), with the vanishing endpoint factors, yields for all nonnegative integers j:
\[
 \boxed{\kappa(m_j-m_{j+2})+j m_{j-1}-(j+3)m_{j+1}=0,} \tag{25.1}
\]
with the j=0 term \(j m_{j-1}\) interpreted as zero. Hence for \(\kappa>0\), **all moments through degree 4 follow from a single scalar** \(A=m_1\):
\[
 \begin{split}
 m_2 &= 1-3A/\kappa,\\
 m_3 &= A-3/\kappa+12A/\kappa^2,\\
 m_4 &= 1-6A/\kappa+15/\kappa^2-60A/\kappa^3.
 \end{split} \tag{25.2}
\]
Equivalently \(A=\partial_\kappa\log Z(\kappa)=I_2(\kappa)/I_1(\kappa)\) for the positive modified Bessel functions, or directly the ratio of two one-dimensional S³ Haar integrals. At κ=0 use the regular Haar limits \(m_1=m_3=0,m_2=1/4,m_4=1/8\). Formulas (25.2) can have substantial cancellation for large κ: any rigorously enclosed calculation must propagate correlated high-precision bounds for A rather than subtracting unrelated rounded quantities.

## 2. Exact 2+6+5 block structure of the source feature covariance

Choose any orthonormal real quaternion frame taking n to the first basis axis. Then
\(u=(t,Rv)\), where \(R=\sqrt{1-t^2}\), \(v\) is uniform on the transverse sphere S² and independent of t. The degree-one and degree-two harmonic span of VOL24 has 13 real coordinates; use this equivalent adapted basis:

- **Scalar pair (2):** \(t,\ q_0=t^2-\frac14\).
- **Three vector pairs (6):** \((u_i,\ t u_i)\) for i=1,2,3.
- **Five transverse tensors (5):** \(u_1u_2,u_1u_3,u_2u_3,u_1^2-u_3^2,u_2^2-u_3^2\).

Put \(R_4=E_\nu[(1-t^2)^2]=1-2m_2+m_4>0\). Haar angular moments on S² are \(E(v_i^2)=1/3\), \(E(v_i^4)=1/5\), \(E(v_i^2v_j^2)=1/15\) for i≠j. Conditioning on t gives the **complete conditional covariance of these genuine SU(2) features**, with no off-block entries:

\[
 \boxed{
 C_{\nu}=
  C_{\rm scal}\oplus
  (C_{\rm vec}\oplus C_{\rm vec}\oplus C_{\rm vec})\oplus
  {R_4\over15}I_3\oplus
  {2R_4\over15}(I_2+\mathbf1_2\mathbf1_2^\top), } \tag{25.3}
\]
where
\[
 C_{\rm scal}=
 \begin{pmatrix}
 m_2-m_1^2 & m_3-m_1m_2\\
 m_3-m_1m_2 & m_4-m_2^2
 \end{pmatrix},
 \qquad
 C_{\rm vec}={1\over3}
 \begin{pmatrix}
 1-m_2 & m_1-m_3\\
 m_1-m_3 & m_2-m_4
 \end{pmatrix}. \tag{25.4}
\]

All blocks are positive definite for each finite κ. The original SU(2) density is strictly positive on S³, and these 13 functions together with constants are linearly independent as spherical harmonics. At κ=0, the formula reproduces the *exact* original continuous Haar covariance: scalar diag(1/4,1/16); each vector pair diag(1/4,1/24); three transverse scalars 1/24; and transverse diagonal block \((I_2+\mathbf1\mathbf1^\top)/12\).

The inverse requires **only two 2x2 inversions**, shared across the three vector blocks, plus scalar reciprocals and the fixed two-dimensional inverse:
\[
 C_{\rm tens,diag}^{-1}
   ={15\over2R_4}\left(I_2-\tfrac13\mathbf1_2\mathbf1_2^\top\right),\quad
 C_{\rm tens,off}^{-1}={15\over R_4}I_3. \tag{25.5}
\]
This is an exact reduction of VOL24's conditional 13x13 covariance inversion from a general matrix problem to native one-link Wilson scalar moments. The frame rotation is a standard real quaternion/SO(4) basis change; the scalar Rayleigh quotient is unchanged by that choice.

## 3. The actual centered physical-source witness in block coordinates

Let \(F_{\rm ctr}\) be any centered, square-integrable, gauge-invariant original Wilson source supported inside \(T_r\), and let \(f(B_r)=\phi_r(B_r)=E_\mu[F_{\rm ctr}\mid B_r]\) be its genuine original exterior predictor. Fix a shell link q in \(R_r\) and the complement of all other links. Define conditional, **centered** covariance vectors of f with the adapted harmonic blocks:
\[
 v_{\rm scal}\in\mathbb R^2,\quad
 v_{{\rm vec},i}\in\mathbb R^2,\quad
 v_{\rm off}\in\mathbb R^3,\quad
 v_{\rm diag}\in\mathbb R^2.
\]
The VOL24 analytic orthogonal projection and (25.3) yield the exact *positive-square* certificate interface
\[
\boxed{\begin{aligned}
 D_r(\phi_r)\ge E_\mu\bigg[
  &v_{\rm scal}^\top C_{\rm scal}^{-1}v_{\rm scal}
  +\sum_{i=1}^3v_{{\rm vec},i}^\top C_{\rm vec}^{-1}v_{{\rm vec},i}\\
  &+{15\over R_4}\|v_{\rm off}\|^2
  +{15\over2R_4}\left(\|v_{\rm diag}\|^2
                    -\tfrac13(\sum_j v_{{\rm diag},j})^2\right)
  \bigg]. \tag{25.6}
\end{aligned}}
\]
Every piece is a conditional covariance under the **real original continuous-SU(2) Wilson one-link heat bath**. It is gauge invariant after the frame change and has no artificial full-shell distance weight or exponential-in-surface minorization. For a center-even source, its tensor components can detect information that the four first-harmonic coordinates miss, as the exact VOL24 adjoint red control proves.

To meet the VOL20 physical criterion, the missing **quantitative** acceptance is an independent, scale-uniform lower bound on the physical expectation in (25.6), relative to \(V_r=\operatorname{Var}(\phi_r)>0\), of at least \(1-e^{-2ma}\) along a *proved* bare-coupling/spacing trajectory. The existence of the positive-square representation alone implies no such lower bound. One must also control higher harmonics if (25.6) does not capture a sufficient fraction of the true centered source's shell loss. The original continuous winding and Gauss sectors and all eleven 4D continuum obligations remain OPEN.

## 4. Independent exact-integer checks and limitations

The [integer verifier](../../tests/ym4_vol25_su2_heatbath_13blocks.py) checks the native SU(2) Haar m_0..m_4 moments with the exact 24-quaternion degree-four cubature and independently reconstructs all 13x13 entries in the adapted basis. It verifies every zero cross-block, the two 2x2 blocks, three identical transverse vector blocks and the full five-dimensional tensor block with integer cross-products. It also verifies the integration-by-parts moment recursion at κ=0 and on a clearly **synthetic rational algebraic recurrence fixture** at κ=1, A=6/25 (not the actual Bessel ratio), including positivity and exact block inverses. This synthetic fixture checks the formulas only; the analytic theorem is about the true continuous SU(2) heat bath.

The original Wilson geometry and the polynomial high-beta adjoint four-loop Gram remain source-pinned in VOL23/VOL24. There is no numerical assertion that the centered physical SU(2) source expectation in (25.6) has already been computed. Hosted normal/optimized strict-integer acceptance is reported separately.

**Status:** native continuous-SU(2) conditional 13-feature block formula and 2x2 inversion **ANALYTIC**; exact Haar/recurrence control **INTEGER TEST**; centered-source quantitative bound at production β and continuum scaling **OPEN**; all-sector transfer and 11 continuum construction gates **OPEN**. Stage in draft PR #113 and its candidate atlas; \`main\` and production 3D viewer unchanged.
