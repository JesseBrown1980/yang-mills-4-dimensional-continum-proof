# YM4 VOL29 — source-local Wilson transfer coercivity removes the spatial-volume penalty

**23 November 2026 · research candidate · original 4D continuous SU(2) Wilson Gibbs measure.** This theorem follows the VOL28 Fourier–Perron finite-volume lower certificate. It replaces the global Perron infimum and global trace ratio by a **local transfer-kernel Harnack estimate on only the four genuine spatial links of the central plaquette**. For every even periodic original SU(2) Wilson lattice side \(L\ge10\), the nearest-slice normalized Wilson plaquette connected correlation has an explicit **positive lower bound independent of \(L^3\)**. The theorem works for all \(\beta>0\); production integer bounds are given for \(\beta=9^{12}\). It remains a **lower** source-signal certificate; a continuum-uniform **upper** correlation-decay/mass-rate certificate remains OPEN.

## 1. Original Wilson transfer and physical centered source

Time is coordinate 2; on an \(L^4\) even untwisted periodic lattice, let \(\mathcal X=SU(2)^{3L^3}\) be the original spatial positive-link configuration space with normalized product Haar. Its full physical gauge-invariant subspace is \(\mathcal H_{\rm phys}\), with orthogonal site-gauge projector \(P\). The exact classical pure-Wilson transfer (Lüscher 1977; Osterwalder–Seiler 1978) is
\[
 T=M_b P K_\beta P M_b,\quad
 b(U)=\exp\{\tfrac\beta2\sum_{p\subset\text{spatial slice}}\operatorname{Re}U_p\},
 \quad V(U)=b(U)^2,
\]
\[
 K_\beta(U,W)=\prod_{\text{spatial links }e}
    \exp\{\beta\operatorname{Re}(U_eW_e^{-1})\},\qquad \beta>0. \tag{29.1}
\]
The gauge averaging implicit in \(PK_\beta P\) preserves a strictly positive **pointwise** integral kernel for \(T\). The unprojected \(K_\beta\) commutes with the simultaneous local gauge action and therefore maps physical gauge-invariant functions into themselves; in quadratic forms of physical vectors the P factors drop exactly.

Fix the actual central original spatial 0–1 plaquette \(p_0\) and the same centered source as VOL26–28,
\[
 F(U)=\frac{1+\operatorname{Re}U_{p_0}}2,\quad
 m=\mathbb E_{\mu_{\beta,L}}F\in[0,1],\quad
 S(U)=F(U)-m.
\]
Let \(F_j\) be its translation by \(j\) units in original time direction 2 and \(C_j=\operatorname{Cov}(F_0,F_j)\), \(C_0>0\). Then the true original periodic Gibbs trace on the full physical space gives
\[
 C_j=\frac{\operatorname{Tr}(S T^j S T^{L-j})}{\operatorname{Tr}T^L}. \tag{29.2}
\]
Here S denotes the gauge-invariant multiplication operator.

## 2. An exact 4-link/13-plaquette local geometry count

Let \(A\) be the four distinct original spatial positive links of \(p_0\), and \(R\) all other spatial links. On an \(L\ge4\) original three-dimensional spatial torus, **exactly 13 distinct spatial plaquettes touch A**: the central plaquette plus three other spatial plaquettes at each of its four links. All independent incidences are enumerated in the strict original geometry checker at \(L=4,6,10,14,18,22\). Denote
\[
 |A|=k=4,\qquad
 N_A=|\{p_{\mathrm{spatial}}:p\cap A\ne\emptyset\}|=13. \tag{29.3}
\]
The count is independent of L. When only these four links of U are changed, every affected spatial plaquette trace changes by at most 2, while each temporal Wilson kernel term changes by at most 2. Consequently:
\[
 \frac{b(U)}{b(U')}\in[e^{-\beta N_A},e^{\beta N_A}],
 \quad
 \frac{V(U)}{V(U')}\in[e^{-2\beta N_A},e^{2\beta N_A}],
\]
\[
 \frac{T(U,W)}{T(U',W)}
 \in[e^{-\beta(N_A+2k)},e^{\beta(N_A+2k)}]
 \quad\text{for every W}. \tag{29.4}
\]
The transfer bound is preserved by positive gauge integration. For every integer \(n\ge1\) and every fixed Z, the **pointwise-positive kernel section**
\(h_Z(U)=T^n(U,Z)>0\) inherits the same U-local ratio bound, uniformly over Z, n, total spatial volume and all other spatial link values. Therefore \(a_Z=b\,h_Z\) has the *local* positive Harnack bound
\[
 \boxed{
 \sup_{u\in SU(2)^A}a_Z(u,x)
 \le R_A\,\inf_{u\in SU(2)^A}a_Z(u,x),\quad
 R_A=e^{\beta(2N_A+2k)}=e^{34\beta},
 } \tag{29.5}
\]
for every fixed complementary spatial configuration \(x\in SU(2)^R\). This is a **local bound on a transfer kernel section**, not a global infimum over \(\mathcal X\).

## 3. The four-link SU(2) Fourier coercivity lemma

Write the unprojected convolution exactly as \(K_\beta=K_A\otimes K_R\), where each factor is the true continuous-SU(2) Wilson one-link convolution. Let
\[
 a_0(\beta)=\int_{SU(2)}e^{\beta\operatorname{Re}g}\,dH(g)>0,\quad
 A_\beta=\frac{\int \operatorname{Re}(g)e^{\beta\operatorname{Re}g}\,dH(g)}{a_0(\beta)}
        =\frac{I_2(\beta)}{I_1(\beta)}\in(0,1). \tag{29.6}
\]
On the four genuine plaquette links A, let \(p=\operatorname{Re}U_{p_0}\). By SU(2) Peter–Weyl and Haar invariance,
\[
 K_A1=a_0^4 1,\quad
 K_Ap=a_0^4 A_\beta^4p,\quad
 E_{H_A}p=0,\quad E_{H_A}p^2=1/4.
\]
Thus for \(S=(1/2-m)+p/2\) with \(0\le m\le1\), its **finite two-mode** inverse under \(K_A\) has the exact native continuous-SU(2) norm
\[
 \|K_A^{-1}S\|_{H_A}^2
 =a_0^{-8}\left[(1/2-m)^2+\frac{1}{16A_\beta^8}\right]
 \le\frac5{16a_0^8 A_\beta^8}. \tag{29.7}
\]
No inverse of the compact full Wilson transfer or \(K_R\) is required.

**Source-local weighted coercivity lemma.** Suppose a strictly positive function \(a(u,x)\) on \(SU(2)^A\times SU(2)^R\) obeys \(\sup_u a(u,x)\le R_A\inf_u a(u,x)\) at each fixed x. Then, for any strictly positive spatial Wilson weight V with local ratio \(\sup_u V(u,x)/\inf_u V(u,x)\le R_V\),
\[
 \boxed{
 \frac{\int V(M)[K_\beta(Sa)(M)]^2\,dH(M)}
      {\int V(M)[K_\beta a(M)]^2\,dH(M)}
 \ge\frac{A_\beta^8}{80\,R_A^4R_V}.} \tag{29.8}
\]

*Proof with all constants.* Fix the output complement \(y=M_R\). Because \(K_R(x,y)>0\) pointwise,
\(\widetilde a_y(u)=\int K_R(x,y)a(u,x)\,dH_R(x)>0\)
inherits the same \(R_A\)-ratio in u. Put \(b_y=\int\widetilde a_y\,dH_A>0\). Then for all u,
\(b_y/R_A\le\widetilde a_y(u)\le R_A b_y\).
The exact source Haar variance gives
\[
 \int S(u)^2\widetilde a_y(u)dH_A(u)
 \ge\frac{b_y}{R_A}\left[(1/2-m)^2+\frac1{16}\right]
 \ge\frac{b_y}{16R_A}.
\]
Apply Cauchy to \(K_A(S\widetilde a_y)\) against the **explicit finite Fourier test** \(K_A^{-1}S\); (29.7) implies
\[
 \|K_A(S\widetilde a_y)\|_2^2
 \ge a_0^8A_\beta^8\,b_y^2/(80R_A^2).
\]
On the other hand, normalized-Haar Schur's bound \(\|K_A\|_{2\to2}=a_0^4\) and \(\widetilde a_y\le R_A b_y\) give
\(\|K_A\widetilde a_y\|_2^2\le a_0^8R_A^2 b_y^2\).
After multiplying by V, the ratio of the local V infimum to supremum is at least \(1/R_V\), so the output-slice ratio is at least \(A_\beta^8/(80 R_A^4R_V)\). Integrate over the remaining output links y with their **positive** original Haar measure. This proves (29.8) without counting any links outside A.

For the genuine original spatial Wilson \(V=b^2\), (29.4) gives
\[
 R_V=e^{2\beta N_A}=e^{26\beta}.
\]
For the positive h_Z from (29.5),
\[
 \boxed{
 \frac{\|T(S h_Z)\|_2^2}{\|T h_Z\|_2^2}
 \ge\frac{A_\beta^8}{80e^{(4(2N_A+2k)+2N_A)\beta}}
 =\frac{A_\beta^8}{80e^{162\beta}}.} \tag{29.9}
\]
This equality uses the physical-gauge invariance of h_Z and S, so the P factors in T drop when applying K. The norm here is on the original physical spatial SU(2) Hilbert space.

## 4. Even periodic time: a positive two-step square and exact one-step monotonicity

The original periodic extent L is **even**, \(L\ge10\). Put \(n=(L-2)/2\ge1\). Because T has a strictly positive pointwise kernel and is self-adjoint, the kernel of \(T^{L-2}=T^nT^n\) factorizes:
\[
 T^{L-2}(V,U)=\int h_Z(V)h_Z(U)\,dH(Z),\quad
 h_Z(U)=T^n(U,Z)>0.
\]
The exact periodic Wilson trace therefore becomes a **positive average of the local quadratic ratios**:
\[
 C_2=\frac{\int dH(Z)\,\langle Sh_Z,T^2 Sh_Z\rangle}
           {\int dH(Z)\,\langle h_Z,T^2 h_Z\rangle}
     =\frac{\int\|T(S h_Z)\|_2^2\,dH(Z)}
            {\int\|T h_Z\|_2^2\,dH(Z)}
     \ge\frac{A_\beta^8}{80e^{162\beta}}. \tag{29.10}
\]
Every h_Z is nonnegative and inherits the *source-local* Harnack estimate (29.5). The denominator is strictly positive. Neither the Perron eigenfunction nor \(\operatorname{Tr}T\) appears in this proof.

Finally, the native physical strictly positive Wilson transfer has eigenvalues \(\lambda_i>0\). Pairing (i,j) and (j,i) in the exact periodic spectral representation for **the same real plaquette source** gives terms proportional to
\[
 2(\lambda_i\lambda_j)^{L/2}
    \cosh\!\left[(L/2-d)\log(\lambda_i/\lambda_j)\right].
\]
For \(0\le d\le L/2\), these are nonincreasing in d. Therefore \(C_1\ge C_2\) for every even \(L\ge4\). Combining with (29.10) proves:
\[
 \boxed{
 C_1\ge C_2\ge\frac{A_\beta^8}{80e^{162\beta}}>0,
 \qquad
 \frac{C_1}{C_0}\ge4C_1
       \ge\frac{A_\beta^8}{20e^{162\beta}}.} \tag{29.11}
\]
This is a **spatial-volume-independent** quantitative original continuous-SU(2) Wilson nearest-slice lower bound. The ratio is normalized by the true \(C_0=\operatorname{Var}_\mu F_0\le1/4\), and all original spatial winding/gauge states are retained in the physical transfer.

## 5. Production exact integer certificate and exterior-signal propagation

The native SU(2) Riccati barrier proved independently in VOL28 gives
\(A_\beta\ge\beta/(\beta+4)\ge1/2\) for \(\beta\ge4\). Therefore
\[
 C_1\ge\frac{e^{-162\beta}}{20480},
 \qquad
 \frac{C_1}{C_0}\ge\frac{e^{-162\beta}}{5120}.
\]
For the **actual** production coupling \(\beta=9^{12}=282429536481\) and \(e<3\), these imply the **strict exact rational certificates**
\[
 \boxed{C_1>\frac1{20480\cdot3^{45753584909922}},
 \qquad
 \frac{C_1}{C_0}>
 \frac1{5120\cdot3^{45753584909922}},} \tag{29.12}
\]
for **every** even \(L\ge10\), with **no spatial-volume exponent**.

The original VOL27 spectral log-convexity then gives, with \(d=r+1<L/2\),
\[
 C_d\ge C_0(C_1/C_0)^d.
\]
VOL26's independent true original centered-source variance bound supplies
\(C_0\ge B_\beta^{-1}\) where \(B_\beta=147456(1+6\beta)^2\). Therefore put
\(H_\beta=5120\cdot3^{162\beta}\). For every centered r>=1 and even original L>=2(2r+3),
\[
 \boxed{C_{r+1}>\frac1{B_\beta H_\beta^{r+1}},\qquad
 V_r=\operatorname{Var}(E[F_0\mid B_r])
    >\frac4{B_\beta^2H_\beta^{2(r+1)}}.} \tag{29.13}
\]
This *lower* exterior-signal bound is now **independent of the total spatial volume** for each fixed radius r, unlike VOL28. VOL22 independently gives \(D_r\ge e^{-4\beta s_r}V_r>0\) with an explicit finite-beta shell loss; this remains far too weak for the physical **upper** correlation-decay rate \(\kappa_r\ge1-e^{-2ma}\) and does not settle continuum existence, renormalization or Gauss/winding limits.

## 6. Independent checks, safety conditions and acceptance boundary

The [integer verifier](../../tests/ym4_vol29_local_harnack_volume_free.py) independently enumerates the exact original 3D spatial link/plaquette incidence \(k=4,N_A=13\) at L=4/6/10/14/18/22; checks the *local* output transfer Harnack exponent \(N_A+2k=21\), the positive h_Z and b product ratio exponent \(2N_A+2k=34\), the V ratio exponent \(2N_A=26\), and the final \(4(2N_A+2k)+2N_A=162\). The checker confirms the Haar four-link plaquette moments and exact SU(2) source Fourier eigenmode multiplier \(A_\beta^4\) as algebraic identities. It also performs an **independently specified finite rational two-state positive-transfer control** for L=4,6,10, using the exact thermal trace and pairwise spectral monotonicity; this is a spectral falsifier, not a finite-group substitute for the SU(2) Gibbs measure. The integer production exponent \(162\beta=45753584909922\) and fully explicit volume-uniform lower ratios are frozen in HBP.

**Analytic acceptance:** the original continuous-SU(2) lower source signal (29.11)–(29.13) is proved under the standard strictly positive pure-Wilson transfer construction and source geometry; the independent strict integer checker audits its geometry, constants and spectral controls. A *signed external referee* or native Lean verification is a separate obligation.

**Physical HOLD:** a scale-uniform **upper** mass-decay or normalized shell contraction estimate \(\kappa_r\ge1-e^{-2ma}\) along proved \(\beta(a)\), continuum Yang–Mills construction, nonzero renormalized limiting source, Gauss/winding-sector transfer and the eleven original continuum obligations remain OPEN. The new uniform **lower** margin does not imply any upper decay theorem. Stage in draft PR #113 and candidate atlas; main and production 3D viewer unchanged.

**Classical Wilson transfer provenance:** M. Lüscher, *Construction of a selfadjoint, strictly positive transfer matrix for Euclidean lattice gauge theories*, Commun. Math. Phys. 54 (1977), 283–292, DOI 10.1007/BF01614090; Osterwalder–Seiler, *Gauge field theories on a lattice*, Ann. Phys. 110 (1978), 440–471, DOI 10.1016/0003-4916(78)90039-8.
