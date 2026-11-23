# YM4 VOL27 — strict original SU(2) centered-source exterior predictability at every positive finite coupling

**23 November 2026 · finite-cutoff analytic research candidate · periodic original 4D continuous SU(2) Wilson measure.** This note accepts the nonzero centered-plaquette *exterior-predictor* target left open in VOL26, including the actual production coupling \(\beta=9^{12}\). The mathematical input is the **classical strictly positive Wilson transfer matrix**, not a claim to have proved a new transfer theorem. The conclusion is strict positivity, with an exact positive spectral representation. A quantitative continuum-uniform rate remains OPEN.

## 1. The exact physical source and one original exterior witness

Use the full original Wilson Gibbs measure on an untwisted even periodic four-torus \((\mathbb Z/L\mathbb Z)^4\), with normalized continuous SU(2) Haar links and action
\[
  \mu_{\beta,L}(dU)\ \propto\
  \exp\left\{\beta\sum_{p}\operatorname{Re}U_p\right\}\,dH(U),
  \qquad \beta>0.
\]
Take the centered cube \(Q_r=[-r,r]^4\), \(r\ge1\), \(b=2r+1\), and even \(L\ge2(b+2)\); let \(T_r\) be its positive internal links and \(\mathcal E_r\) its entire outside-link sigma-field. Freeze exactly the VOL26 physical source
\[
  F_0=\frac{1+\operatorname{Re}U_{p_0}}2,\qquad
  p_0=((0,0,0,0);0,1).
\]
Use coordinate direction **2 as Euclidean time**, so the source plaquette spans the spatial 0–1 directions. Translate the *same* spatial plaquette by
\[
 d=r+1,\quad p_d=((0,0,d,0);0,1),\qquad
 F_d=\frac{1+\operatorname{Re}U_{p_d}}2. \tag{27.1}
\]
Every one of the four positive links of \(p_d\) has coordinate \(x_2=d>r\), hence \(F_d\) is an actual bounded, gauge-invariant **exterior observable** in \(L^2(\mathcal E_r)\). The checker reconstructs all original 4D links for radii 1–4 and checks periodic injectivity. We have \(1\le d<L\) and the two supports are distinct.

As in VOL15–VOL21, the genuine original-Wilson interior conditional law factorizes through its quaternion resultants \(B_r\), so the same source predictor can be written in either form
\[
 M_r=\mathbb E[F_0\mid\mathcal E_r]
    =\mathbb E[F_0\mid B_r]=\phi_r(B_r),
 \qquad V_r=\operatorname{Var}(M_r). \tag{27.2}
\]

## 2. Exact strictly positive SU(2) Wilson transfer operator

Work on one original three-dimensional spatial \(x_2=\mathrm{constant}\) periodic slice. The unconstrained Hilbert space is \(L^2(SU(2)^{3L^3},dH)\), and its physical subspace \(\mathcal H_{\rm phys}\) is invariant under the site-wise SU(2) gauge group; denote the orthogonal gauge projector by \(P\).

The standard original Wilson transfer operator in direction 2 has, up to a harmless positive normalization,
\[
  T=V^{1/2}P K_\beta P V^{1/2},\qquad
  (K_\beta f)(U)=\int
    \prod_{e\in E_{\rm spatial}}
       e^{\beta\operatorname{Re}(U_e V_e^{-1})}
       f(V)\,dH(V), \tag{27.3}
\]
where \(V(U)=\exp\{\beta\sum_{p\subset\mathrm{slice}}\operatorname{Re}U_p\}\) is strictly positive and gauge invariant. The gauge integration of the original temporal links produces \(P\); the factors \(V^{1/2}\) distribute the genuine spatial plaquette action across adjacent time steps.

**Strict positive definiteness at every \(\beta>0\).** The one-link central kernel
\[
 k_\beta(g)=e^{\beta\operatorname{Re}g}
      =\sum_{n\ge0}\frac{(\beta/2)^n}{n!}\,
               \chi_{1/2}(g)^n
\]
has **strictly positive character coefficient in every SU(2) spin \(j\)**. Tensor-product multiplicities in \(\chi_{1/2}^n\) are nonnegative integers, and at \(n=2j\) the highest spin \(j\) occurs exactly once. Thus every coefficient is strictly positive for all \(\beta>0\), so convolution by \(k_\beta\) is strictly positive (injective) on \(L^2(SU(2))\) by Peter–Weyl; the product link operator \(K_\beta\) is strictly positive on the complete spatial link Hilbert space. For every nonzero physical \(f\), \(V^{1/2}f\ne0\) stays gauge invariant and
\[
  \langle f,Tf\rangle
    =\langle V^{1/2}f,K_\beta V^{1/2}f\rangle>0. \tag{27.4}
\]
The continuous positive-definite kernel on the compact finite link space is trace class; the bounded positive multipliers and gauge projection retain a positive trace-class operator \(T\) on \(\mathcal H_{\rm phys}\). Consequently there is a complete eigenbasis \(T|i\rangle=\lambda_i|i\rangle\) with **every \(\lambda_i>0\)** (possibly accumulating at zero). This is strict operator positivity, **not** a uniform positive lower bound on the spectrum.

The transfer construction and its gauge-sector positivity are classical: M. Lüscher, *Construction of a selfadjoint, strictly positive transfer matrix for Euclidean lattice gauge theories*, Commun. Math. Phys. 54 (1977), 283–292, DOI [10.1007/BF01614090](https://doi.org/10.1007/BF01614090); Osterwalder–Seiler, *Gauge field theories on a lattice*, Ann. Phys. 110 (1978), 440–471, DOI [10.1016/0003-4916(78)90039-8](https://doi.org/10.1016/0003-4916(78)90039-8). Equations (27.3)–(27.4) give a self-contained SU(2) character-positivity reduction for the particular pure-gauge Wilson model.

## 3. A strict positive connected physical Wilson-plaquette correlator

Let \(\mathcal F\) denote multiplication by the **genuine spatial** observable \(F_0(U)\in[0,1]\) on \(\mathcal H_{\rm phys}\). The original periodic Wilson measure is represented by the *physical trace* \(Z_L=\operatorname{Tr}(T^L)>0\). Translation invariance and the transfer construction give for \(1\le d<L\)
\[
 \langle F_0F_d\rangle_\mu
  =\frac{\operatorname{Tr}(\mathcal F T^d \mathcal F T^{L-d})}{Z_L},
 \quad
 \langle F_0\rangle_\mu=\frac{\operatorname{Tr}(\mathcal F T^L)}{Z_L}. \tag{27.5}
\]
Put \(\mathcal A=\mathcal F-\langle F_0\rangle_\mu I\). Then
\[
 \boxed{
 C_{\beta,L}(d):=\operatorname{Cov}_\mu(F_0,F_d)
 =\frac{\operatorname{Tr}(\mathcal A T^d\mathcal A T^{L-d})}{Z_L}
 =\frac{\sum_{i,j}
  \lambda_i^{L-d}\lambda_j^d
     |\langle i|\mathcal A|j\rangle|^2}
  {\sum_i\lambda_i^L}>0.} \tag{27.6}
\]
The strict sign follows because (a) all transfer eigenvalues are strictly positive, (b) the multiplication operator \(\mathcal F\) is not constant on the physical spatial configuration space: a gauge-invariant elementary plaquette has a nonconstant trace on open sets of positive Haar measure, and (c) a nonzero bounded selfadjoint \(\mathcal A\) has a nonzero matrix entry in a complete eigenbasis. The trace expressions are finite since \(T\) is positive trace-class and \(1\le d<L\). The full original spatial gauge-invariant space, including spatial winding holonomies, is retained; no flat-sector or finite-group projection is applied.

This is a finite-volume **strict signal** statement for a translated identical plaquette, not a decay-rate estimate. At \(\beta=0\), the link convolution collapses to a rank-one projector; distinct slices are independent and \(C_{0,L}(d)=0\). The strict \(\beta>0\) conclusion is consistent with that red control.

## 4. Accepted nonzero *exterior predictor* at production beta

Because \(F_d\) belongs to \(\mathcal E_r\), conditional expectation and Cauchy–Schwarz yield
\[
 \begin{aligned}
 0&< C_{\beta,L}(r+1)^2
      =\operatorname{Cov}(M_r,F_d)^2\\
  &\le V_r\,\operatorname{Var}(F_d)
   \le \tfrac14 V_r.
 \end{aligned}
\]
Hence the new, unconditionally rigorous **true original-SU(2) high-beta exterior-predictor positivity theorem** is
\[
 \boxed{
 V_r=\operatorname{Var}_{\mu}(\phi_r(B_r))
     \ge4\,C_{\beta,L}(r+1)^2>0
 \quad\text{for every }\beta>0,\ r\ge1,\ \text{even }L\ge2(b+2).
 } \tag{27.7}
\]
Since VOL26 also establishes \(0<\operatorname{Var}(F_0)\le1/4\), the normalized source predictability obeys \(\Gamma_r(F_0)=V_r/\operatorname{Var}(F_0)\ge16C_{\beta,L}(r+1)^2>0\).

At the **actual production \(\beta=9^{12}=282429536481\)**, (27.7) is valid, without a special high-coupling perturbation expansion. This accepts the strict positive-\(V_r\) part of VOL26's unfinished research criterion. It does **not** calculate the magnitude of \(C_{\beta,L}(r+1)\).

Combining with VOL22's original finite-beta shell-noise certificate (write \(s_r=\min\{24b(3b^2+b-3),24(b+2)^2(b+1)\}\)) also yields
\[
 \boxed{
 D_r(\phi_r)=V_r-V_{r+1}
 \ge e^{-4\beta s_r}V_r
 \ge4e^{-4\beta s_r}C_{\beta,L}(r+1)^2>0.
 } \tag{27.8}
\]
This proves **strictly positive genuine centered-source shell loss** at all finite \(\beta>0\), including the production coupling, with an explicit *conditional expression* for its lower bound. The multiplier \(e^{-4\beta s_r}\) remains far below the physical-rate requirement at high beta. No numerical lower enclosure for \(C_{\beta,L}\) or \(\kappa_r\) is supplied here.

## 4A. Exact log-convex transfer reduction: exterior signal from one time step

The strict positive spectral formula (27.6) also gives a useful **genuine original-Wilson correlation inequality**, rather than only an existential sign. For the translated **same** spatial plaquette source, write \(C_j=\operatorname{Cov}(F_0,F_j)\) for \(j=0,\ldots,L-1\), so \(C_0=\operatorname{Var}(F_0)>0\). With the same transfer eigenbasis,
\[
 C_j=\sum_{i,k}w_{ik}\rho_{ik}^{\,j},\quad
 w_{ik}={\lambda_i^L|\mathcal A_{ik}|^2\over Z_L}\ge0,\quad
 \rho_{ik}={\lambda_k\over\lambda_i}>0,\quad
 \sum_{i,k}w_{ik}=C_0. \tag{27.9}
\]
This is an **exact positive moment representation** of the original finite-periodic Wilson plaquette covariance sequence. Hölder/Cauchy–Schwarz on these nonnegative weights proves
\[
 \boxed{C_j^2\le C_{j-1}C_{j+1}\quad(1\le j<L-1),\qquad
 C_j\ge C_0\left({C_1\over C_0}\right)^j>0
 \quad(1\le j<L).} \tag{27.10}
\]
The latter is Jensen's inequality for \(x\mapsto x^j\), \(j\ge1\), under the probability weights \(w_{ik}/C_0\). The periodic source covariance is symmetric under \(j\leftrightarrow L-j\), fully consistent with the log-convex sequence.

For the **actual original centered source** and its first exterior translated plaquette at \(d=r+1\), this yields a more local version of (27.7):
\[
 \boxed{
 V_r\ge4C_d^2\ge4 C_0^2
       \left({C_1\over C_0}\right)^{2(r+1)}>0.} \tag{27.11}
\]
At every finite \(\beta>0\), VOL26 supplies a rigorous positive floor
\(C_0\ge[147456(1+6\beta)^2]^{-1}\). Consequently, **a rigorous lower bound for the single-step ratio \(C_1/C_0\)** would immediately give an explicit finite-volume physical centered-source exterior-predictor lower bound for *every* radius. This is an exact **lower** propagation inequality; the upper spatial-decay rate and continuum uniformity demanded by VOL20 remain independent, open research obligations.

The exact rational two-state transfer fixture independently checks \(C_0=1/4,\ C_1=123/1460,\ C_2=9/292\), and the strict log-convex determinant \(C_0C_2-C_1^2=81/133225>0\). The production coupling \(\beta=9^{12}\) enters the analytic SU(2) transfer theorem unchanged. No measured or rigorously enclosed value of its genuine original 4D \(C_1/C_0\) is asserted.

## 5. Independent strict integer checks and next physical acceptance

The [checker](../../tests/ym4_vol27_transfer_strict_predictor.py) reconstructs the two original 4D plaquettes, proves their relative internal/exterior support and no-wrap embedding for radii 1–4, and independently verifies the SU(2) tensor-power **strict coefficient witness** \(m_{n,n}=1\) in \(\chi_{1/2}^{n}\) and the nonnegative character fusion recursion through \(n=16\). A separate **abstract rational two-state** selfadjoint positive transfer matrix tests the spectral connected-covariance trace formula and its rank-one \(\beta=0\) red. These arithmetic examples are formal controls of the transfer and Peter–Weyl argument, **not** a native continuous-SU(2) numerical transfer diagonalization. The original SU(2) strict positivity comes from the analytic Wilson/Peter–Weyl proof in sections 2–3.

**Next main mathematical acceptance:** produce an explicit, independently certified lower bound on \(C_{\beta,L}(r+1)\) or the source-specific thirteen/higher-harmonic conditional covariance in VOL25–VOL26 at \(\beta=9^{12}\); then establish the rate uniformly under a physically proved \(\beta(a)\) trajectory, the renormalized nonzero source and all Gauss/winding-sector continuum obligations. The **sign** is accepted for every positive finite coupling; the **magnitude and scaling rate** remain OPEN. The eleven continuum-construction gates remain OPEN. Stage this as a review candidate on draft PR #113, leaving \`main\` and the production 3D atlas unchanged.


## 6. Audit and hosted verification checkpoint

The [independent-method mathematical review](../../reviews/YM4-VOL27-TRANSFER-STRICT-PREDICTOR-AUDIT-20261123.md) checks the original 4D source/exterior placement, each strictly positive SU(2) character coefficient, preservation of the physical gauge-invariant Hilbert space under the transfer, the finite-periodic spectral trace and log-convexity, and the beta-zero red. The classical transfer input is identified to Lüscher 1977 (DOI 10.1007/BF01614090); this internal review is distinct from a signed independent human or formal Lean referee.

[Dedicated hosted run #45253764999](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45253764999) **PASS** for strict repository no-float, original 4D exterior geometry, SU(2) fusion controls, rational spectral trace and pinned initial HBP. The supplemental one-step/log-convex HBP has SHA-256 **d8de14ddde99b18cfbe9a1d12d470724b931331c425b10b940f511a5b4aadc76**; its updated hosted [workflow #45254447911](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45254447911) was queued at the latest inspection and must be evaluated separately. Analytic continuous-SU(2) transfer positivity is a theorem statement, while the hosted checker validates finite original geometry, group representation arithmetic and rational spectral controls. Production numeric margin, upper mass rate and continuum construction remain OPEN.
