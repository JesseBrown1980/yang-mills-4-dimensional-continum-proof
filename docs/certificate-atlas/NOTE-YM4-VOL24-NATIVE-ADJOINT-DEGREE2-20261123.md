# YM4 VOL24 — native adjoint Wilson boundary Gram and complete degree-two SU(2) source witness

**23 November 2026 · research candidate; original four-dimensional continuous-SU(2) Wilson Gibbs measure.** Independent mathematical continuation of VOL23's four fundamental boundary-loop certificate. This note addresses a necessary center-neutrality safeguard: a genuine SU(2) Wilson observable may have positive shell information loss while every *first*-harmonic single-link witness from VOL23 §5 vanishes. We establish an explicit original-model adjoint four-loop Gram inequality with **polynomial** bare-beta dependence, and a complete thirteen-coordinate (four linear plus nine quadratic) SU(2) conditional-Haar projection for the true centered Wilson-source predictor.

## 1. Exact original Wilson center-even red control

Retain VOL23's four original internal boundary-affected 0-links based at x_(s,t)=(0,sr,tr,0), for (s,t) in {+1,-1}² and r>=1. Each carries two cyclic three-link exterior SU(2) staples S1,S2 with
\[
 f_{s,t}(B_r)={\|B_{e_{s,t}}\|^2-2\over2}
             =\operatorname{Re}(S_1S_2^{-1})\in[-1,1].
\]
The four original six-link contours are disjoint; their four distinguished exterior 0-links q_(s,t) have no common original plaquette. Define the **native center-even adjoint Wilson character**:
\[
 h_{s,t}(B_r):=f_{s,t}(B_r)^2-\tfrac14
      ={1\over4}\,\chi_{\mathrm{spin}\,1}(S_1S_2^{-1})
      \in[-\tfrac14,\tfrac34]. \tag{24.1}
\]
The SU(2) spin-one character identity is \(\chi_1(W)=(2\operatorname{Re}W)^2-1\); hence (24.1) uses a genuine continuous nonabelian Wilson loop, with zero extra approximation or chosen gauge frame. It is invariant when any one link in its contour is flipped by the nontrivial SU(2) center element -I.

At bare beta=0, the original links are independent normalized continuous Haar. Conditional on every link except one of the six q links in the contour, write f=\(\langle U_q,c\rangle\) with \(\|c\|=1\); then
\[
 \operatorname{Var}_H(h)=E_H(f^4)-E_H(f^2)^2
      ={1\over8}-{1\over16}={1\over16}>0,\qquad
 \operatorname{Cov}_H(h,U_q)=0. \tag{24.2}
\]
The last equality is **exact center parity**: h is even and U_q is odd under U_q -> -U_q. For an original shell link outside this contour the function h is independent of the link. Thus **every first-harmonic single-link witness can vanish while the original Wilson shell loss is strictly positive**. For the four disjoint h_i, beta=0 gives the actual native matrix values \(G^h=D^h=I_4/16\). This is a direct original-continuous-Haar counterexample to treating the single-link four-coordinate witness alone as complete for center-neutral physical source families.

## 2. Polynomial all-beta heat-bath variance for the adjoint character

For the genuine original continuous SU(2) Wilson one-link conditional heat bath
\[
 \nu_{\beta,H}(du)\propto\exp\{\kappa\,u\cdot n\}\,dH_{SU(2)}(u),
 \quad \kappa=\beta\|H\|\le6\beta,
\]
take any unit real quaternion direction c. Put \(T=u\cdot n\), \(R^2=1-T^2\), and \(\alpha=c\cdot n\), \(z=\alpha^2\in[0,1]\). For a uniformly distributed V on \(S^2\), the exact Haar latitude decomposition gives \(u=Tn+RV\) and \(u\cdot c=\alpha T+\sqrt{1-z}\,R V_1\). Using \(E[V_1^2]=1/3\), \(E[V_1^4]=1/5\) and parity, total variance yields
\[
\begin{aligned}
 \operatorname{Var}_\nu\big((u\cdot c)^2\big)
 &\ge { (4z-1)^2\over9}\operatorname{Var}_\nu(T^2)
       +{4(1-z)^2\over45}\,E_\nu[R^4]. \tag{24.3}
\end{aligned}
\]

For \(\kappa\ge1\), put \(X=\kappa(1-T)\in[0,2\kappa]\). As in VOL23's original S³ proof, its true continuous density is proportional to \(\sqrt{X(2-X/\kappa)}e^{-X}\). Its normalizer is strictly less than 2, while each interval \(A=[1/4,1/2]\) and \(B=[3/4,1]\) has probability greater than \(1/48\). On these intervals \(T\ge0\), and the squared latitudes are separated by at least \(1/(8\kappa)\). The exact two-replica variance identity therefore yields
\[
 \operatorname{Var}_\nu(T^2)>
 {1\over147456\,\kappa^2}. \tag{24.4}
\]
On B, \(R^2=(1-T)(1+T)\ge3/(4\kappa)\), so
\[
 E_\nu[R^4]>{3\over256\,\kappa^2}. \tag{24.5}
\]
If \(z\ge1/2\), the first term in (24.3) gives \(>1/(1327104\kappa^2)\). If \(z<1/2\), its second term gives \(>1/(3840\kappa^2)\), which is stronger. For \(0\le\kappa<1\), the heat-bath density relative to Haar is pointwise greater than \(1/9\), while \(\operatorname{Var}_H((u\cdot c)^2)=1/16\). Combining both regimes proves **for every direction and every finite beta**:
\[
 \boxed{\operatorname{Var}_{\nu_{\beta,H}}\big((u\cdot c)^2\big)
 \ge {1\over1327104(1+\kappa)^2}
 \ge {1\over1327104(1+6\beta)^2}.} \tag{24.6}
\]
This bound concerns the **original SU(2) Haar measure**, not an abstract probability fixture or a finite group. It has polynomial \(1/\beta^2\) behavior even for the worst possible six-staple environment.

## 3. Genuine original high-beta center-even 4x4 Gram certificate

Let \(h=(h_{s,t})\) be the four original boundary-resultant functions (24.1), with \(\lambda_r,K_r\) the true periodic-Wilson boundary-resultant laws of VOL21. Define
\[
 G^h_{ij}=\operatorname{Cov}_{\lambda_r}(h_i,h_j),\qquad
 D^h_{ij}=E_{\lambda_{r+1}}\operatorname{Cov}_{K_r}(h_i,h_j).
\]
Condition on **all original links except the four selected q_(s,t)**. The four original heat baths factorize exactly, because their supports share no original plaquette. For each i the corresponding \(h_i=(u_{q_i}\cdot c_i)^2-1/4\), with \(\|c_i\|=1\). Conditional covariance and (24.6) imply for every \(a\in\mathbb R^4\)
\[
 a^\top D^h a
 \ge {1\over1327104(1+6\beta)^2}\sum_i a_i^2. \tag{24.7}
\]
Each \(h_i\in[-1/4,3/4]\) has range width exactly 1. The bounded-variance inequality and Cauchy–Schwarz give \(a^\top G^h a\le(\sum|a_i|)^2/4\le\sum a_i^2\). Therefore the actual continuous-SU(2) matrices satisfy
\[
 \boxed{D^h-k_\beta^{\mathrm{adj}}G^h\succeq0,\qquad
 k_\beta^{\mathrm{adj}}={1\over1327104(1+6\beta)^2}.} \tag{24.8}
\]
For the original production beta \(9^{12}=282429536481\),
\[
 \boxed{k_{9^{12}}^{\mathrm{adj}}=
 {1\over3810901164235731112280396414976}.} \tag{24.9}
\]
This is a native, radius-independent, **center-even/adjoint four-source** high-beta Dirichlet certificate. Every quantity \(G^h,D^h\) belongs to the original 4D Wilson Gibbs theory. The matrix entries at positive beta are bounded by the analytic argument, rather than numerically evaluated; the integer checker verifies its group-geometric and rational inputs.

## 4. The complete degree-two, thirteen-coordinate native SU(2) link witness

For an arbitrary square-integrable centered interior Wilson-source predictor \(f(B_r)=\phi_r(B_r)\), choose one genuine original link \(q\in R_r\) and condition on all original links except \(U_q\). Define the 13 real features
\[
 \Psi(u)=(u_0,u_1,u_2,u_3,\;u_0u_1,u_0u_2,u_0u_3,u_1u_2,u_1u_3,u_2u_3,\;
 u_0^2-u_3^2,u_1^2-u_3^2,u_2^2-u_3^2). \tag{24.10}
\]
These are **all** degree-one quaternion coordinates (dimension 4) and the traceless degree-two spherical harmonics (dimension 9) on SU(2)=S³. Put \(v_q=\operatorname{Cov}_{\nu_q}(f,\Psi)\) and \(C_q=\operatorname{Cov}_{\nu_q}(\Psi,\Psi)\). At every finite beta, \(C_q\succ0\): a nonzero linear plus traceless quadratic polynomial cannot be constant on S³, and the original heat-bath density is strictly positive everywhere. Orthogonal projection and the original Wilson tower give the **exact 13x13 source-specific witness**
\[
 \boxed{D_r(f)\ge E_\mu[v_q^\top C_q^{-1}v_q].} \tag{24.11}
\]
This extends VOL23's incomplete four-coordinate first-harmonic witness. It is gauge-covariant under the induced quaternion rotation; the Rayleigh quotient is basis-independent.

At beta=0, Haar orthogonality makes the covariance block diagonal. The four linear coordinates have covariance \(I_4/4\); the six off-diagonal quadratics have covariance \(I_6/24\); and the three diagonal differences have covariance \((I_3+\mathbf1\mathbf1^\top)/12\), with all cross-block covariances zero. Thus the complete inverse is **explicit and rational**:
\[
 C_H^{-1}=\mathrm{diag}\big(4I_4,\ 24I_6,\ 12(I_3-\tfrac14\mathbf1\mathbf1^\top)\big). \tag{24.12}
\]
For the genuine original beta-zero center-even Wilson loop \(h(u)=u_0^2-1/4=(3d_0-d_1-d_2)/4\), the first four covariances vanish identically, whereas the degree-two covariance has \(v_{d}=(1/12,0,0)\). Equation (24.12) gives exactly \(v^\top C_H^{-1}v=1/16=\operatorname{Var}_H(h)\). Thus **the added quadratic harmonics recover 100% of the shell-loss variance in the explicit adjoint red control**, where the prior four-coordinate witness gives zero.

The genuine physical acceptance objective is now precise: rigorously certify the expectation on the right of (24.11), with any required higher-harmonic remainder, for **actual centered interior Wilson-source predictors** over physical shells along beta(a). VOL24 supplies a positive high-beta boundary adjoint calibration and a sufficient source-specific projection interface; it has not evaluated those centered-source covariances or proved a continuum mass gap.

## 5. Exact arithmetic scaling test and scope

The polynomial bound in (24.8) has an important *conditional* scaling property. If a physically established Wilson trajectory has \(a_n=3^{-n}\), \(\beta(a_n)\le n\) and desired rate parameter \(m=1\), then for all integers \(n\ge23\), the strict integer inequality
\[
 3^n\ge 2\cdot1327104(1+6n)^2 \tag{24.13}
\]
implies \(k_{\beta(a_n)}^{adj}\ge2a_n\ge1-e^{-2a_n}\). The checker proves the base \(n=23\) and the factor-three induction for \(n\ge23\). Such a beta(a) trajectory is an **illustrative hypothesis**, not a scale-setting theorem for this project. At the fixed production beta \(9^{12}\), the analogous inequality first holds in powers of three at \(n=65\), again only as an arithmetic comparison. These comparisons show why a **polynomial** Wilson shell bound can in principle be scale-compatible, provided the bound holds on the true centered source family and its actual physical beta(a) trajectory is separately certified.

**Verifier and receipt:** [tests/ym4_vol24_native_su2_adjoint_degree2.py](../../tests/ym4_vol24_native_su2_adjoint_degree2.py) uses exact integer numerator/denominator arithmetic, independently checks the center-even low-beta red control on the original SU(2) Haar 24-unit-quaternion degree-four cubature, the complete 13x13 Haar covariance/inverse, original VOL23 noncommuting four-loop support assumptions, cap constants, production-beta denominator, and conditional scaling inequalities. The cubature tests fixed Haar moments only; no claim of finite-group equivalence at beta>0. The continuous-Haar conditional variance proofs are analytic and retain separate mathematical-review status.

**Acceptance:** Native continuous-SU(2) center-even 4x4 boundary-source Gram **ANALYTIC** with exact geometry and arithmetic falsifiers; native 13-feature predictor inequality **ANALYTIC**; production-beta centered interior-source witness and physical continuum scaling **OPEN**; all Gauss/winding-sector transfer and eleven original continuum-construction obligations **OPEN**. Preserve as draft PR #113 candidate evidence, with \`main\` and the production 3D atlas unchanged.
