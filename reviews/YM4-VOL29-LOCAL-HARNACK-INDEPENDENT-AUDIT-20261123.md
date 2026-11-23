# YM4 VOL29 — independent-method audit of original SU(2) source-local volume-free lower bound

**23 November 2026; separate internal mathematical derivation; no signed human referee or Lean signoff.** Reviews [the VOL29 candidate theorem](../docs/certificate-atlas/NOTE-YM4-VOL29-LOCAL-HARNACK-VOLUME-FREE-20261123.md) against the original continuous-SU(2) Wilson transfer, paying special attention to its physical gauge projector, local Harnack constants, tensor Fourier inverse and finite periodic trace. The aim is a positive finite-cutoff *lower* correlation bound independent of spatial-volume size; upper continuum mass decay is a distinct open problem.

## A. Native model and gauge projector — analytic PASS

Use even periodic \(L^4\), transfer time coordinate 2, and a full original three-dimensional spatial positive-link Hilbert space \(\mathcal X=SU(2)^{3L^3}\). The transfer is the **original pure Wilson** \(T=b P K_\beta P b\) with \(b=e^{\beta A_{\rm spatial}/2}\), and \(K_\beta(U,W)=\prod_e e^{\beta\operatorname{Re}(U_eW_e^{-1})}\). This convolution commutes with simultaneous site gauge transformations of U,W, because each trace changes by conjugation at the link's starting vertex. Therefore K maps physical gauge-invariant vectors into themselves; **for every physical f**, \(T f=b K(bf)\) and \(\|Tf\|_2^2=\int V(K(bf))^2\,dH\), \(V=b^2\). This dropping of P in the physical quadratic form is justified, while the transfer's positive integral kernel is represented by integrating the same strictly positive K under endpoint site gauge transformations. Full spatial winding holonomies are retained.

The normalized-Haar positive transfer is selfadjoint trace class and has positive eigenvalues at every finite \(\beta>0\). Its pointwise transfer kernel is strictly positive. It follows that every integer \(n\ge1\) has a strictly positive kernel \(T^n(U,Z)\), which is gauge invariant in U.

## B. Four-link local geometry and Harnack exponent — exact PASS

The central spatial plaquette in directions 0,1 contains four original positive links A. On a 3D periodic spatial slice L>=4, each link touches four spatial faces. The central face occurs four times in the incidence sum; all 12 others are distinct: precisely **13** original spatial faces touch A. The strict checker independently enumerates this for L=4/6/10/14/18/22.

For any two U,U' differing only on A and every fixed W, the source-local transfer kernel ratio is
\[
 e^{-\beta(13+2\cdot4)}
 \le T(U,W)/T(U',W)
 \le e^{\beta(13+2\cdot4)}=e^{21\beta}.
\]
The spatial half-weight b has ratio <=e^(13β), and the full spatial weight V has ratio <=e^(26β). Every \(h_Z(U)=T^n(U,Z)>0\) inherits the first bound because T^n integrates a **positive** kernel against T^(n−1). Thus \(a_Z=b h_Z\) has source-local ratio at most \(R=e^{34\beta}\), for every fixed complementary link configuration, every Z,n and every total spatial L. There is no Perron global-infimum or full spatial volume in these constants.

## C. Alternative direct local Cauchy check — analytic PASS

Split the original Fourier convolution into the exactly four central plaquette links and all other spatial links, \(K=K_A\otimes K_R\). Keep the actual SU(2) central character coefficient \(A_\beta=I_2(\beta)/I_1(\beta)>0\). For the true physical source \(S=F-m=(1/2-m)+p/2\), \(m=\mu F\in[0,1]\), Haar and the fundamental representation give:
\[
 K_A S=a_0^4[(1/2-m)+(A_\beta^4/2)p],\quad
 \int S^2dH_A\ge1/16,\quad
 \|K_A^{-1}S\|^2\le5/(16a_0^8 A_\beta^8).
\]
Only a **two-mode finite Fourier inverse** is applied, so there is no unbounded inverse on the full compact transfer Hilbert space.

For a strictly positive source-local Harnack vector a(u,x), fix the *output* complementary configuration y. The convolution \(K_R\), with pointwise positive kernel, turns it into a positive function \(\widetilde a_y(u)\) that inherits the same local sup/inf ratio R. With \(b_y=\int \widetilde a_y dH_A\), \(b_y/R\le\widetilde a_y\le R b_y\). The identity
\[
 \langle K_A(S\widetilde a_y),K_A^{-1}S\rangle
   =\int S^2\widetilde a_y\,dH_A
   \ge b_y/(16R)
\]
and exact Cauchy imply
\(\|K_A(S\widetilde a_y)\|^2\ge a_0^8 A_\beta^8 b_y^2/(80R^2)\).
The normalized-Haar Schur bound gives
\(\|K_A\widetilde a_y\|^2\le a_0^8R^2b_y^2\).
Multiplying both squared outputs by the genuine original positive V(U) can lower their ratio by at most \(e^{-26\beta}\) at fixed y. Thus for every positive \(h_Z\),
\[
 \frac{\|T(S h_Z)\|^2}{\|T h_Z\|^2}
 \ge \frac{A_\beta^8}{80e^{(4\cdot34+26)\beta}}
 =\frac{A_\beta^8}{80e^{162\beta}}.
\]
The ratio lower is **independent of the complementary link count** because both numerator and denominator contain the same positive complementary convolution and V integrates out with uniform local ratios.

## D. Even periodic thermal trace factorization and C1>=C2 — analytic PASS

For even L>=10 put n=(L−2)/2>=1. By selfadjoint positivity and the strictly pointwise-positive integer kernels,
\[
 T^{L-2}(V,U)=\int T^n(V,Z)T^n(U,Z)\,dH(Z).
\]
Thus the **actual periodic** connected two-time-slice plaquette covariance is
\[
 C_2=\frac{\int\|T(S h_Z)\|^2\,dH(Z)}
           {\int\|T h_Z\|^2\,dH(Z)}
 \ge A_\beta^8/(80e^{162\beta}).
\]
No ground-state weight or \(\lambda_0^L/\operatorname{Tr}T^L\) appears; a two-state *thermal* example checks the trace orientation at even L=4,6,10.

In the genuine physical transfer eigenbasis, each offdiagonal i,j pair contributes a nonnegative multiple of \(\cosh((L/2-d)\log(\lambda_i/\lambda_j))\) to C_d. On 0<=d<=L/2 this is nonincreasing, so \(C_1\ge C_2\). The source is the same real spatial plaquette translated in time, ensuring the Hermitian matrix-element pairing. Since \(C_0=\mathrm{Var}F_0\le1/4\), the normalized bound is
\[
 C_1/C_0\ge A_\beta^8/(20e^{162\beta}).
\]

## E. Exact production arithmetic and remaining bounds — PASS/OPEN

At \(\beta=9^{12}=282429536481\), the already audited native SU(2) Riccati comparison gives \(A_\beta\ge1/2\). With \(e<3\), the complete strict integer result is
\[
 C_1>1/[20480\cdot3^{45753584909922}],\quad
 C_1/C_0>1/[5120\cdot3^{45753584909922}].
\]
The source-local exponent is exactly **162β**, independent of L. VOL28's smallest even L=10 global exponent **8472886094580000** was volume-dependent; the new one improves the exponent for every L and is *uniform in spatial volume*. The log-convex source lower propagation to C_(r+1) and V_r is valid for fixed r and all even L>=2(2r+3).

**Accepted analytic scope:** a strictly positive explicit **lower** normalized nearest-slice correlation bound for the original continuous SU(2) pure-Wilson model on all indicated even periodic finite lattices, with integer geometry/arithmetic checks. **Still OPEN:** a quantitative *upper* connected-correlation decay or VOL20 shell-loss criterion \(\kappa_r\ge1-e^{-2ma}\), a physically justified beta(a) scaling path, renormalized nonzero continuum source, complete Gauss/winding continuum reconstruction and the eleven original continuum obligations. A signed external mathematician and formal proof checker are not supplied by this internal audit.

References: Lüscher, Commun. Math. Phys. 54 (1977), 283–292, DOI 10.1007/BF01614090; Osterwalder–Seiler, Ann. Phys. 110 (1978), 440–471, DOI 10.1016/0003-4916(78)90039-8.
