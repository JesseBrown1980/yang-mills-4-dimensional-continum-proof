# YM4 VOL28 — explicit original-SU(2) nearest-slice Wilson correlation lower margin at production beta

**23 November 2026 · original four-dimensional continuous-SU(2) Wilson Gibbs model · analytic finite-volume theorem with exact integer controls.** Advances the strictly positive centered-source predictor of VOL27 to an **explicit nonzero nearest-slice numerical lower bound at the actual production \(\beta=9^{12}\)**. This is a true native-SU(2) finite-volume lower certificate, using the original positive transfer operator and the first nontrivial SU(2) Peter–Weyl mode of a plaquette. It depends on the *spatial volume* \(L^3\), is extraordinarily conservative, and does **not** prove a continuum-uniform Wilson mass rate.

## 1. Precise native problem and finite-volume result

Let \(\mu_{\beta,L}\) be the original normalized-Haar SU(2) Wilson law on an even, untwisted periodic \(L^4\) four-torus. Time is the 2-coordinate; the spatial slices have exactly
\[
 E=3L^3\quad\text{positively oriented spatial links},\qquad
 Q=3L^3\quad\text{spatial elementary plaquettes}.
\]
The centered source is precisely VOL26–27's original spatial 0–1 plaquette
\[
 F(U)=\frac{1+\operatorname{Re}U_{p_0}}2\in[0,1].
\]
Write \(C_0=\operatorname{Var}_{\mu_{\beta,L}}F>0\) and
\(C_1=\operatorname{Cov}_{\mu_{\beta,L}}(F_0,F_1)\).
For **every finite \(\beta\ge4\)** and every such even L,
\[
 \boxed{C_1>
 \frac{e^{-30\beta L^3}}{1280(9\beta^2)^{3L^3}},
 \qquad
 \frac{C_1}{C_0}>
 \frac{e^{-30\beta L^3}}{320(9\beta^2)^{3L^3}}.} \tag{28.1}
\]
At the original production coupling
\[
 \beta=9^{12}=3^{24}=282429536481,
\]
both are certified using **integer exponents only**:
\[
 \boxed{
 C_1>\frac1{1280\cdot3^{N_L}},\qquad
 \frac{C_1}{C_0}>\frac1{320\cdot3^{N_L}},
 \quad N_L=(30\beta+150)L^3
       =8472886094580\,L^3.} \tag{28.2}
\]
For the smallest original even torus used in the centered-cube packet, L=10, this becomes the strictly positive rational
\[
 \boxed{\frac{C_1}{C_0}>
   \frac1{320\cdot3^{8472886094580000}}.} \tag{28.3}
\]
Writing the bound in exponent notation is an exact certificate; expanding the enormous integer denominator is unnecessary. This theorem covers all original periodic even L, so in particular the r>=1 centered cubes of VOL27 with \(L\ge2(2r+3)\). Its lower bound decays rapidly with L and beta.

## 2. Complete Wilson transfer and exact one-plaquette Fourier test

Use the **original** physical one-step transfer from VOL27, with the normalized product Haar measure on all E spatial SU(2) links:
\[
 T=M_{V^{1/2}}P K_\beta P M_{V^{1/2}},\quad
 V(U)=\exp\{\beta\sum_{\mathrm{spatial}\ p}\operatorname{Re}U_p\},
\]
\[
 (K_\beta f)(U)=\int
       \prod_{e=1}^{E}e^{\beta\operatorname{Re}(U_eW_e^{-1})}
       f(W)\,dH(W).
\]
Here P projects onto the complete gauge-invariant spatial Hilbert space, retaining winding holonomies. Define two *positive* true SU(2) Haar integrals
\[
 a_0(\beta)=\int_{SU(2)}e^{\beta\operatorname{Re}g}\,dH(g),\quad
 A_\beta=\frac{\int e^{\beta\operatorname{Re}g}
                   \operatorname{Re}g\,dH(g)}{a_0(\beta)}
          =\frac{I_2(\beta)}{I_1(\beta)}. \tag{28.4}
\]
The one-link convolution eigenvalue on the trivial representation is \(a_0\); on each matrix coefficient of the fundamental SU(2) representation it is \(a_0A_\beta\), by centrality and Schur orthogonality. Put \(p(U)=\operatorname{Re}U_{p_0}\) on a spatial slice. Since this native Wilson plaquette uses **exactly four distinct spatial links**, each in the fundamental representation,
\[
 K_\beta 1=a_0^E1,\qquad
 K_\beta p=a_0^E A_\beta^4 p,\quad
 \int p\,dH=0,\quad \int p^2\,dH=\frac14. \tag{28.5}
\]
This is an exact *four-link Fourier diagonalization inside the original SU(2) theory*. It requires no evaluation of any large transfer-matrix eigenvector.

For \(m=\langle F\rangle_{\mu_{\beta,L}}\in[0,1]\), define the genuine centered spatial observable \(S=F-m=(1/2-m)+(1/2)p\). It lies in the two exact eigenmodes of (28.5), so
\[
 \begin{aligned}
 \langle S,K_\beta^{-1}S\rangle_{H}
 &=a_0^{-E}
   \left[(1/2-m)^2+\frac{1}{16A_\beta^4}\right]\\
 &\le\frac5{16}\,a_0^{-E}A_\beta^{-4},
 \qquad 0<A_\beta<1. \tag{28.6}
 \end{aligned}
\]
The inverse is used **only on this two-mode finite Fourier subspace**; no bounded inverse of the compact full transfer operator is postulated.

## 3. Two elementary, uniform SU(2) one-link inequalities

**Riccati lower comparison.** The exact S³ integration-by-parts recurrence from VOL25 gives
\[
 A_\beta'=1-A_\beta^2-\frac{3A_\beta}{\beta},\qquad
 A_\beta=\frac\beta4+O(\beta^3)\ \text{as }\beta\downarrow0.
\]
For \(B_\beta=\beta/(\beta+4)\), at a contact \(A_\beta=B_\beta\) the slope difference is
\[
 1-B_\beta^2-\frac{3B_\beta}{\beta}-B_\beta'
      =\frac{5\beta}{(\beta+4)^2}>0.
\]
Since \(B_\beta=\beta/4-\beta^2/16+O(\beta^3)\), the one-dimensional comparison theorem proves
\[
 \boxed{A_\beta\ge\frac{\beta}{\beta+4}\ge\frac12
        \quad\text{for }\beta\ge4.} \tag{28.7}
\]

**Explicit trivial-character lower bound.** For \(u\in SU(2)=S^3\), put \(w=1-\operatorname{Re}u\). Its exact Haar density is
\((2/\pi)\sqrt{w(2-w)}\), \(0\le w\le2\). For \(\beta\ge1\),
\[
 \begin{aligned}
 a_0&=e^\beta E_H e^{-\beta w}
   \ge e^{\beta-1}\Pr_H(w\le1/\beta),\\
 \Pr_H(w\le1/\beta)&\ge\frac4{3\pi\beta^{3/2}}
   >\frac1{3\beta^2}.
 \end{aligned}
\]
Using \(e<3,\ \pi<4\), obtain the all-integer-friendly strict bound
\[
 \boxed{a_0(\beta)>\frac{e^\beta}{9\beta^2}
        \quad(\beta\ge1).} \tag{28.8}
\]
Both inequalities concern the **actual continuous SU(2) Haar integrals**, with no finite-group physical substitution.

## 4. Positive transfer Perron lower control — entire physical Hilbert space

In the original spatial-link Haar representation, \(P K_\beta P\) is a normalized average of the pointwise-positive K kernel over local site gauge transformations. Every kernel factor lies in \([e^{-\beta},e^\beta]\), and \(\|V^{1/2}\|\) lies pointwise in \([e^{-\beta Q/2},e^{\beta Q/2}]\). Thus the full physical transfer has a continuous *strictly positive integral kernel* obeying
\[
 \boxed{e^{-\beta(E+Q)}\le T(U,W)
                  \le e^{\beta(E+Q)}.} \tag{28.9}
\]
By positive-kernel Perron–Frobenius/Krein–Rutman, its maximal eigenvalue \(\lambda_0>0\) has a strictly positive gauge-invariant eigenfunction \(\Omega\), normalized by \(\|\Omega\|_{L^2(H)}=1\). The eigenvalue equation and the pointwise ratio in (28.9) give
\[
 \frac{\inf_U\Omega(U)}{\sup_U\Omega(U)}
       \ge e^{-2\beta(E+Q)}.
\]
Because Haar is normalized, \(\sup\Omega\ge\|\Omega\|_2=1\). Hence
\[
 \boxed{\inf\Omega\ge e^{-2\beta(E+Q)},\quad
 \inf_U V^{1/2}(U)\Omega(U)
       \ge e^{-\beta(2E+5Q/2)}.} \tag{28.10}
\]
This estimate deliberately pays a *full spatial-volume penalty*: it is a rigorous finite-volume bound, not a local or continuum Harnack inequality.

The positive trace-class transfer satisfies
\[
 \boxed{\operatorname{Tr}T\le\|V\|_\infty
   \operatorname{Tr}(P K_\beta P)
   \le e^{\beta Q}\operatorname{Tr}K_\beta
   =e^{\beta(E+Q)}.} \tag{28.11}
\]
Here \(\operatorname{Tr}K_\beta=e^{\beta E}\) follows from its exact positive continuous kernel on the diagonal and normalized Haar. The trace inequality uses the orthogonal gauge projector \(P\) and the positivity of K; no truncation of the physical Hilbert space is inserted.

## 5. One positive Fourier matrix element gives a *numerical* correlation margin

The genuine centered transfer multiplication observable is \(S=F-m\). Define the physical vector \(g=V^{1/2}S\Omega\). By (28.10), nonnegativity of \(S^2\), and the exact original Haar variance,
\[
 \begin{aligned}
 \langle g,S\rangle_H
 &=\int V^{1/2}\Omega S^2\,dH
 \ge e^{-\beta(2E+5Q/2)}
     \int S^2\,dH\\
 &\ge \frac1{16}e^{-\beta(2E+5Q/2)}. \tag{28.12}
 \end{aligned}
\]
The last step uses \(\int_H S^2=(1/2-m)^2+1/16\ge1/16\), valid for **the unknown actual high-beta thermal mean m**.

On the physical gauge-invariant subspace, \(P g=g\); the positive convolution's Cauchy–Schwarz inequality on the two Fourier modes of S yields
\[
 \begin{aligned}
 \langle\Omega,S T S\Omega\rangle
  &=\langle g,K_\beta g\rangle\\
  &\ge\frac{|\langle g,S\rangle|^2}
              {\langle S,K_\beta^{-1}S\rangle}\\
  &\ge\frac{a_0^E A_\beta^4}{80}
       e^{-\beta(4E+5Q)}. \tag{28.13}
 \end{aligned}
\]
Now use the **exact positive thermal spectral sum** of VOL27 at one time step. Retaining the terms with the maximal-eigenvalue state \(\Omega\) gives
\[
 \operatorname{Tr}(S T S T^{L-1})
 \ge\lambda_0^{L-1}\langle\Omega,S T S\Omega\rangle.
\]
Since all \(0<\lambda_j\le\lambda_0\),
\[
 Z_L=\operatorname{Tr}(T^L)
   \le\lambda_0^{L-1}\operatorname{Tr}T.
\]
Thus the actual original periodic Wilson covariance satisfies
\[
 C_1=\frac{\operatorname{Tr}(S T S T^{L-1})}{Z_L}
 \ge\frac{\langle\Omega,S T S\Omega\rangle}{\operatorname{Tr}T}
 \ge\frac{a_0^E A_\beta^4}{80}
        e^{-\beta(5E+6Q)}. \tag{28.14}
\]
Apply (28.7), (28.8), and \(E=Q=3L^3\) to obtain (28.1):
\[
 C_1>
  \frac{e^{\beta E}(1/2)^4}
       {80(9\beta^2)^E e^{\beta(5E+6Q)}}
 =\frac{e^{-30\beta L^3}}
       {1280(9\beta^2)^{3L^3}}.
\]
Because \(F\in[0,1]\), \(0<C_0\le1/4\) and \(C_1/C_0\ge4C_1\). For production \(\beta=3^{24}\), \(9\beta^2=3^{50}\), and \(e<3\) gives the exact integer-power certificates (28.2)–(28.3).

This result is a **constructive native-SU(2) quantitative bound**, unlike VOL27's strict sign alone. It sacrifices enormous strength through the global Perron-Harnack and trace upper envelopes, so its magnitude is far below a physical mass-rate threshold.

## 6. Propagate the finite-volume lower signal, with the remaining scale boundary explicit

VOL27's genuine transfer log-convexity gives
\[
 C_d\ge C_0(C_1/C_0)^d,\quad d=r+1.
\]
VOL26's independent centered-source variance floor gives \(C_0\ge B_\beta^{-1}\) for
\(B_\beta=147456(1+6\beta)^2\). At production, put
\(H_L=320\cdot3^{N_L}\). Equations (28.2) and VOL27 then certify the exact finite-volume lower margins
\[
 \boxed{C_{r+1}>\frac1{B_\beta H_L^{r+1}},
 \qquad V_r> \frac4{B_\beta^2 H_L^{2(r+1)}}.} \tag{28.15}
\]
The centered-source shell loss also satisfies VOL22's *independent* all-beta floor
\[
 D_r=V_r-V_{r+1}\ge e^{-4\beta s_r}V_r
 >\frac4{3^{4\beta s_r}B_\beta^2H_L^{2(r+1)}}. \tag{28.16}
\]
Every exponent is explicit integer arithmetic at production beta; no unknown original Gibbs correlator remains on the right. These are **lower information-signal bounds** that deteriorate rapidly with L and r. They do not give an *upper* correlation-decay estimate or the desired \(\kappa_r\ge1-e^{-2ma}\) uniformly along a physically accepted trajectory \(\beta(a)\).

## 7. Independent exact verifier and staged acceptance

The [strict integer checker](../../tests/ym4_vol28_nearest_slice_margin.py) independently verifies: the original 3D spatial link and plaquette counts \(E=Q=3L^3\), exact centered and translated original 4D 0–1 plaquette placement, SU(2) Haar plaquette mean/variance moments, the Riccati rational barrier algebra \(5\beta/(\beta+4)^2\), the Perron/trace/Fourier factor accounting \(4E+6Q=30L^3\), the factor \(9\beta^2=3^{50}\) at production, the exact exponents for L=10/14/18/22, and a **separately labeled rational 2x2 positive transfer control** demonstrating the principal-eigenstate spectral lower projection. The 2x2 fixture is an algebraic falsifier of the trace reasoning, not a replacement for continuous SU(2) Wilson integration. The actual SU(2) inequalities (28.4)–(28.14) are analytic.

**Status:** explicit lower \(C_1/C_0\) at \(\beta=9^{12}\) on each original finite even periodic lattice **ANALYTIC, EXACT INTEGER EXPONENT**; native full 4D finite-volume transfer/source geometry **CERTIFIED VIA INTEGER FALSIFIER**; rigorous volume-uniform/lattice-spacing-uniform spectral lower margin **OPEN**; the physical **upper** normalized covariance/mass-rate criterion, all-sector continuum reconstruction, and the eleven continuum obligations **OPEN**. Preserve as draft PR #113 research candidate. Leave \`main\` and the accepted live 3D certificate atlas unchanged.
