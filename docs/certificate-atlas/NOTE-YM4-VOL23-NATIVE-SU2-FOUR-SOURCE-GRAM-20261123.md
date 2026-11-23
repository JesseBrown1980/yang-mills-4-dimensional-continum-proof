# YM4 VOL23 — genuine high-beta continuous-SU(2) four-source boundary-resultant Dirichlet Gram

**23 November 2026 · analytic original Wilson theorem, exact integer/noncommuting geometric falsifier.** Continues VOL19–VOL22. This certificate constructs **four explicit gauge-invariant original SU(2) Wilson loops that are measurable functions of the VOL15 boundary resultants** and proves a positive, volume-independent, source-restricted \(4\times4\) shell Dirichlet inequality at the production bare coupling \(\beta=9^{12}\). The functions are boundary-shell observables; the centered-interior-source predictor subspace and the 11 continuum obligations remain OPEN.

## 1. Four native boundary-resultant Wilson loops in the original 4D cube

Fix an integer \(r\ge1\), original centered cube \(Q_r=[-r,r]^4\), \(b=2r+1\), and an untwisted even periodic original Wilson torus with \(L\ge2(b+2)\). As in VOL21, \(T_r\) is the set of all positive links with both endpoints in \(Q_r\), \(R_r\subset T_{r+1}\setminus T_r\) is the original six-staple boundary support, and \(B_r\) is the exact noncommutative boundary-resultant field.

For each \((s,t)\in\{-1,+1\}^2\), take the **original internal positive 0-link**
\[
 e_{s,t}=(x_{s,t},0),\qquad x_{s,t}=(0,sr,tr,0).
\]
This edge touches exactly two original mixed plaquettes, one normal to direction 1 and one normal to direction 2. Their cyclically ordered three-link exterior staples are unit quaternions \(S_1,S_2\), supported on **six distinct original links of \(R_r\)**. With the VOL15 inner-product convention,
\[
 B_{e_{s,t}}=\overline S_1+\overline S_2,\quad
 f_{s,t}(B_r):=\frac{\|B_{e_{s,t}}\|^2-2}{2}
     =\operatorname{Re}(S_1S_2^{-1})\in[-1,1]. \tag{23.1}
\]
Thus \(f_{s,t}\) is an **actual contractible length-six Wilson-loop trace**, a measurable gauge-invariant function of the boundary sufficient statistic. There is no independent boundary action, finite-group replacement, or source-selected spatial weight.

The original 4D link enumeration proves that all four six-link supports are mutually disjoint. Select from each first staple the **parallel 0-link on the exterior direction-1 face**, \(q_{s,t}=(x_{s,t}+s\hat1,0)\). Each \(f_{s,t}\) depends linearly on the selected unit-quaternion link \(U_{q_{s,t}}\), with a unit-quaternion coefficient when the other links are fixed. The four selected links are distinct, and **no original elementary plaquette contains two selected links**. Consequently, conditional on *all other original links*, their true full-Wilson Gibbs law factorizes into four original single-link SU(2) Haar heat baths, each with at most six original plaquette staples. This is a finite original-4D geometric statement, checked at \(r=1,2,3,4\), with an all-\(r\) coordinate proof given by the links above: any two selected bases differ by at least 2 in direction 2 or by \(2r+2\) in direction 1, while one original plaquette spans at most one step of either transverse coordinate.

## 2. Nonexponential all-beta lower covariance of an original SU(2) Wilson heat bath

For an arbitrary original positive link, condition on all other original Wilson links. The six plaquette staples give the genuine continuous SU(2) law
\[
 \nu_{\beta,H}(du)\ \propto\ \exp\{\beta\langle u,H\rangle\}\,dH_{SU(2)}(u),
 \qquad \|H\|\le6,\quad\kappa=\beta\|H\|\le6\beta. \tag{23.2}
\]
Identify SU(2) with the Haar-uniform unit three-sphere \(S^3\subset\mathbb R^4\). For **every** unit direction \(c\in\mathbb R^4\), the following elementary, valid-at-high-beta estimate holds:
\[
 \boxed{\operatorname{Var}_{\nu_{\beta,H}}\langle u,c\rangle
       \ \ge\ {1\over 36864(1+\kappa)^2}
       \ \ge\ {1\over36864(1+6\beta)^2}.} \tag{23.3}
\]

For completeness, here is an explicit proof with integer-controlled constants. At \(\kappa<1\), the normalized density relative to Haar is pointwise at least \(e^{-2\kappa}>1/9\); Haar has \(\operatorname{Var}\langle u,c\rangle=1/4\). The bound is then greater than \(1/36\).

For \(\kappa\ge1\), choose the axis \(n=H/\|H\|\), write \(t=u\cdot n\), \(w=1-t\), and \(z=\kappa w\). The exact continuous Haar latitude law on \(S^3\) gives \(z\)-density proportional to
\[
 \sqrt{z(2-z/\kappa)}\,e^{-z},\quad 0\le z\le2\kappa.
\]
Its normalizer is less than 2: \(\sqrt{2-z/\kappa}\le\sqrt2<2\) and \(\int_0^\infty\sqrt z\,e^{-z}dz\le\int_0^\infty(z+1)e^{-z}/2\,dz=1\). On each interval \(A=[1/4,1/2]\), \(B=[3/4,1]\), the integrand exceeds \(1/6\) because \(\sqrt z\ge1/2\), \(\sqrt{2-z/\kappa}\ge1\), and \(e^{-z}\ge e^{-1}>1/3\). Thus \(\Pr(A),\Pr(B)>1/48\). Their \(w\)-values differ by at least \(1/(4\kappa)\), so the independent-replica variance identity yields
\[
 \operatorname{Var}(t)>1/(36864\kappa^2).
\]
For each transverse unit direction \(v\perp n\), the conditional angular variance is \(\mathbb E[(1-t^2)/3]\). On \(B\), \(w\le1\) and \(1-t^2=w(2-w)\ge w\ge3/(4\kappa)\), giving transverse variance \(>1/(192\kappa)\), at least \(1/(36864\kappa^2)\). Rotational symmetry about \(n\) eliminates mixed covariance. This proves (23.3) in every direction, including the worst longitudinal one. Every input inequality is elementary and uniform in the staple directions. In particular, the **genuine original Wilson one-link covariance has a polynomial-in-beta spectral floor**, unlike the conservative full-shell density minorization of VOL21–22.

## 3. A rigorous original SU(2) \(4\times4\) Dirichlet/Gram certificate at \(\beta=9^{12}\)

Let \(\lambda_r\) be the actual periodic Wilson Gibbs law of \(B_r\), \(K_r(b',db)=\operatorname{law}(B_r\mid B_{r+1}=b')\) the exact original-shell transfer kernel of VOL21, and enumerate the four \(f_i=f_{s,t}\) of (23.1). Define the **actual original continuous-SU(2) matrices**
\[
 G_{ij}:=\operatorname{Cov}_{\lambda_r}(f_i,f_j),\qquad
 D_{ij}:=\mathbb E_{b'\sim\lambda_{r+1}}\operatorname{Cov}_{K_r(b',\cdot)}(f_i,f_j). \tag{23.4}
\]
For any \(a\in\mathbb R^4\), put \(F_a=\sum_i a_i f_i(B_r)\). Let \(\mathcal C\) be the sigma-algebra of **all original links except the four selected links \(q_i\)**. Since \(B_{r+1}\) is determined by links outside \(T_{r+1}\), \(\sigma(B_{r+1})\subset\mathcal C\). By original-plaquette nonoverlap, the four conditional heat baths factorize, and each \(f_i\) is a unit-direction quaternion-linear observable in its selected link. The conditional variance and tower laws therefore give
\[
 a^\top D a=\mathbb E\operatorname{Var}(F_a\mid B_{r+1})
 \ge\mathbb E\operatorname{Var}(F_a\mid\mathcal C)
 \ge {1\over36864(1+6\beta)^2}\sum_i a_i^2. \tag{23.5}
\]
Since each \(f_i\in[-1,1]\),
\[
 a^\top G a=\operatorname{Var}(F_a)
 \le(\sum_i|a_i|)^2\le4\sum_i a_i^2. \tag{23.6}
\]
Combining (23.5)–(23.6) proves the **native four-source matrix inequality**
\[
 \boxed{D-k_\beta G\succeq0,\qquad
 k_\beta={1\over147456(1+6\beta)^2}>0.} \tag{23.7}
\]
This holds **without estimating or replacing any** of the original SU(2) Gibbs mixed moments, for every \(r\ge1\), every finite \(\beta\ge0\), every untwisted even torus \(L\ge2(b+2)\), and the four exact noncommutative boundary-loop functions above.

At the production \(\beta=9^{12}=282429536481\), the strict integer rational acceptance is
\[
 \boxed{D-\frac1{423433462692859012475599601664}\,G\succeq0.} \tag{23.8}
\]
The matrix inequality is a **proved enclosure for the actual continuous-SU(2) \(D,G\)**; it is not an exact numerical evaluation of their individual entries. The bound is tiny but, unlike VOL22's whole-shell floor, decreases only polynomially in bare beta and is **independent of shell radius and total torus volume** for this four-loop subspace.

At \(\beta=0\), independent continuous Haar links yield four independent Haar-distributed loop holonomies. Thus the full native matrices can be evaluated exactly: \(G=D=\tfrac14I_4\), and the exact shell loss on this subspace is \(k=1\). The 24 Hurwitz unit quaternions are used by the verifier **only as an exact low-order cubature falsifier** for Haar second/fourth moments, not as a substitute Gibbs measure at positive beta.

## 4. Exact independent checks, provenance, and the next source-predictor bridge

The strict integer checker [tests/ym4_vol23_native_su2_boundary_gram.py](../../tests/ym4_vol23_native_su2_boundary_gram.py) enumerates the four six-link original Wilson loops for r=1..4; matches each to exactly two mixed original plaquettes and the VOL15 resultant norm; tests path-order correctness under a noncommuting Q8-valued field and local site gauges; verifies pairwise disjoint supports and **absence of shared original plaquettes among the four selected links**; and independently reconstructs the exact Haar \(S^3\) quadratic/fourth moments using a 24-point unit-quaternion cubature. The checker calculates the exact production-beta denominator in (23.8) without floating point.

The mathematical SU(2) proof is analytic, relying on continuous Haar integrals and the *original full 4D Wilson conditional heat baths*. The Q8 configuration tests are algebraic falsifiers, and the Haar cubature verifies fixed-degree identities only. The numerical 4×4 matrix entries at positive beta have not been evaluated. **Dedicated hosted checker PASS:** [GitHub Actions #45241628900](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45241628900) independently passed the repository-wide strict integer-only gate, noncommuting original 4D loop and Q8 gauge control, exact low-order Haar cubature moment checks, normal and optimized byte-identical replay, pinned HBP SHA-256 `fa5b0898227f3ff90e174c2d4017185b002094393961d1e1aacfb8e87b87d16b`, and artifact upload. This hosted result accepts the exact geometry and arithmetic checks; the continuous-SU(2) conditional heat-bath inequality is analytic and still requires independent mathematical referee/formal verification.

**Exact next obligation:** establish overlap or an explicit source-generated transfer bound for the **centered interior-source predictors** \(\phi_r(B_r)=\mathbb E_\mu[F_{\mathrm{interior}}\mid B_r]\) in the VOL20 criterion. The four boundary-shell Wilson functions \(f_i(B_r)\) furnish a real positive channel certificate, but the current theorem does **not** establish that arbitrary centered interior Wilson-source predictors belong to their span, nor the required uniform mass-rate in all Gauss and winding sectors. If a projection/approximation scheme is used, its \(G\)- and \(D\)-norm residuals and cross terms must be bounded before transferring (23.7). The original eleven continuum construction obligations remain OPEN. Keep VOL23 in draft PR #113's candidate certificate map; the production 3D atlas and \`main\` remain unchanged.
