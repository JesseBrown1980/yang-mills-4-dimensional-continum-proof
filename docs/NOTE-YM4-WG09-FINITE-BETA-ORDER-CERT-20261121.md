# YM4-WG09 — independent audits and explicit finite-beta first-neutral spectral-order certificate

**21 November 2026. Status:** submitted for independent hosted source/replay verification. The mathematical statement below is restricted to the original spatial \(L=2\), continuous-SU(2), fully Gauss-projected Wilson transfer at \(0<\beta\le10^{-12}\). It combines the independently recomputed WG09 exact second/third Haar coefficients with a new conservative *full infinite-dimensional* Schur–Feshbach fourth-order estimate. Continuum, variable-volume, and weak-coupling scaling obligations remain OPEN.

## 1. Statement and normalization

Let \(K\) be the full 24-link physical electric SU(2) Wilson convolution; let \(V=\sum_{p=1}^{24}W_p\), \(W_p=\tfrac12\operatorname{Tr}(U_p)\), so \(\|V\|\le24\). Up to the positive common scalar \(e^{-24\beta}\), the physical transfer is unitarily isospectral to \(J=K^{1/2}e^{\beta V}K^{1/2}\).

Write \(t=\kappa_1(\beta)^4\), where \(\kappa_r=I_{r+1}(\beta)/I_1(\beta)\). The neutral electric subspace decomposes as

\[
\mathcal H_{\rm neutral} = \mathbb C1 \oplus E_{42}\oplus R_1\oplus R_{\ge6},
\]

where \(E_{42}\) is the 42-dimensional four-fundamental WG06 space, \(R_1\) comprises the 12 two-link spin-one winding states of electric representation-index sum four, and \(R_{\ge6}\) is the entire remaining neutral all-spin Hilbert space.

**Finite-beta ordering theorem (exact scope):** for every \(0<\beta\le10^{-12}\), the fully spatial-symmetric rank-one genuine physical neutral eigenmode of WG08 is the first neutral nonvacuum transfer level (the highest transfer eigenvalue below the neutral vacuum), separated from the remaining five leading neutral modes by

\[
\lambda_{\rm sym}-\lambda_{\rm next,neutral}
>e^{-24\beta}\,t\,\frac{21}{320}\beta^3.
\]

The true interacting-vacuum centered local contractible Wilson source carries squared spectral overlap \(>1/289\) with that individual first-neutral eigenmode by WG08. The full first physical excitation is still center-charged and local-Wilson-decoupled by WG03 at these parameters. This is a finite spatial-\(L=2\), strong-coupling/small-\(\beta\) certificate.

## 2. Independent audit A: SU(2) Haar coefficients

A separate pure-Python exact rational tensor integrator (different contraction code from the WG09 producer) rebuilt the 24-link geometry, 42 normalized spin networks, six magnetic \(K_{4,2}\) blocks, and true SU(2) quadratic/fourth Haar coordinate contractions. It obtained:

\[
P_+V^2P_+=\frac{381}{64}I_6+J_6,\qquad
P_+VP_0VP_+=\tfrac12 J_6.
\]

It verified every entry of the \(42\times42\) \(V^2\) matrix and all 48 first-magnetic edges. Direct \(V^3\) trace enumeration across the five off-diagonal orbit representatives returned 6 for each ordered pair of distinct blocks; the diagonal is 40. An independently written complementary 36-dimensional Schur calculation recovered the entire matrix of third-order terms, with

\[
H_2=\tfrac12 E_{42}V^2E_{42}-vv^*,\quad
H_3=\tfrac16 E_{42}V^3E_{42}-\tfrac12(vw^*+wv^*),
\quad v=E_{42}V1,\ w=E_{42}V^21,
\]

and \(m=\sqrt2/4\), \(Q=E_{42}-P_+\):

\[
P_+H_2P_+=\frac{381}{128}I_6,\qquad
P_+\bigl(H_3+H_2Q(m-QMQ)^{-1}QH_2\bigr)P_+
=\sqrt2\left(\frac{36499}{49152}I+\frac1{32}O+\frac1{64}X\right).
\]

Here \(O\) exchanges the three pairs of opposite magnetic blocks, and \(X=J_6-I_6-O\) joins different-axis blocks. The three symmetry classes have dimensions \(1,2,3\), with the fully invariant eigenvalue exceeding the two other classes by \(3\sqrt2/32\) and \(\sqrt2/8\) in third-order units.

The clean-room local audit scripts are preserved separately with SHA-256 source digests:

- independent_haar_audit.py: 59f9278e3dca60e1be2d4e75be32b65780d55b96218b68cd0d7619c8362fedcb
- independent_schur_audit.py: 6003dd083999aa285699cbd20ac07d61d43040c799298d9de288f1f58e45e04b

These independent audits did not import the WG09 producer. The repository's earlier independently hosted WG09 producer passed at run 44947346077.

## 3. Independent audit B: complete low-order physical electric spectrum

A separate spin-assignment enumerator runs through every labeling of the 24 spatial links with total representation index \(S=\sum_er_e\le5\), \(r_e=2j_e\). For each vertex, an SU(2) invariant intertwiner exists exactly when the incident spin indices sum to an even integer and the largest does not exceed the sum of the others. The three spatial center charges are evaluated on the original torus cuts.

The complete neutral enumeration finds no nonvacuum state at \(S=2,3,5\), and at \(S=4\) precisely **42 four-fundamental loops plus 12 spin-one two-link loops**, all with unique allowed neutral intertwiners. On the bipartite cubic graph, each vertex's center parity implies that every gauge-invariant configuration has even total \(S\), so all remaining neutral states have \(S\ge6\).

For any positive \(\beta\le10^{-6}\), put \(y=\beta^2/4\). The positive Bessel series for the exact original one-link Wilson convolution gives

\[
\kappa_r=\left(\frac\beta2\right)^r
\frac{\sum_{k\ge0} y^k/[k!(k+r+1)!]}{\sum_{k\ge0}y^k/[k!(k+1)!]}
\le \frac{2}{(r+1)!}\left(\frac\beta2\right)^r
\le 2(\beta/4)^r\quad(r\ge1).
\]

The last step follows from \((r+1)!\ge2^r\), and the first from \(e^y<2\), positive denominator \(\ge1\). Moreover \(\kappa_1\ge\beta(1-y)/4\ge\beta/5\); thus \(t\ge\beta^4/625\). Therefore the full all-spin \(S\ge6\) complement satisfies the **operator inequality**

\[
0<K_{R_{\ge6}}/t\le(625/64)\beta^2 I<10\beta^2 I.
\]

For the 12 \(S=4\) spin-one states, \(\kappa_2^2/t\le \rho:=\frac4{9(1-y)^6}<9/20\). Crucially, \(E_{42}V R_1=0\) **exactly**. Link-center parity forces the inserted plaquette and input four-fundamental support to coincide; for that case \(\chi_1(U_p)^2=\chi_0(U_p)+\chi_2(U_p)\), whose spin-one term occupies all four plaquette links, orthogonal to the two-link spin-one states. The other 18 \(E_{42}\) states have distinct double-winding supports. No higher-spin truncation is used.

## 4. Full infinite-dimensional vacuum/tail Schur error

For \(\beta\le10^{-6}\), \(\|V\|\le24\) and positive exponential series imply, in operator norm,

\[
\|e^{\beta V}-I\|\le25\beta,\quad
\|e^{\beta V}-I-\beta V\|\le289\beta^2,
\]
\[
\left\|e^{\beta V}-I-\beta V-\frac{\beta^2V^2}{2}\right\|\le2400\beta^3,
\quad
\left\|e^{\beta V}-\sum_{k=0}^{3}\frac{\beta^kV^k}{k!}\right\|\le14000\beta^4.
\]

Let \(\lambda\) lie in the six-eigenvalue window of WG07, write \(\nu=\lambda/t\), and define \(a=\langle1,e^{\beta V}1\rangle\), \(f=E_{42}e^{\beta V}1\). For these spectral parameters \(a-\lambda\ge99/100\), \(\lambda\le2\beta^4\), and \(|(a-\lambda)^{-1}-1|\le300\beta^2\). Thus

\[
\left\|\frac{ff^*}{a-\lambda}
-\beta^2vv^*-\frac{\beta^3}{2}(vw^*+wv^*)\right\|
\le(50\cdot2400+576^2/4+300\cdot625)\beta^4
=390444\beta^4.
\]

For \(R=R_1\oplus R_{\ge6}\), let \(D=K_R/t\). Eliminating the vacuum modifies the \(E_{42}\)-to-\(R\) coupling by \(E e^{\beta V}R-f(a-\lambda)^{-1}P_0e^{\beta V}R\). By the **exact vanishing** \(EVR_1=0\), its \(R_1\) block has norm \(\le(289+632)\beta^2=921\beta^2\); the \(R_{\ge6}\) block is \(\le26\beta\). Multiplying by \(\sqrt D\), using \(\sqrt{\rho}<7/10\) and \(\sqrt{10}\beta<4\beta\), gives an aggregate weighted coupling \(<750\beta^2\).

The full infinite-dimensional \(R\)-resolvent after vacuum elimination is bounded by \(2\), because the modified magnetic \(R\)-block is at most \(qD\), \(q=(1-24\beta)^{-1}\), and \(q\rho<1/2\). Thus the whole tail Schur contribution has norm \(<2\cdot750^2\beta^4=1125000\beta^4\), including the 12 spin-one modes and every higher representation. The complete 42-dimensional reduced operator satisfies

\[
\left\|F_E(\beta,\nu)-
 \left[I+\beta M+\beta^2 H_2+\beta^3 H_3\right]\right\|
\le(14000+390444+1125000)\beta^4
=1529444\beta^4<\boxed{2000000\beta^4}.
\]

All estimates are uniform over the required true six-eigenvalue spectral interval; no finite-spin cutoff or floating-point extrapolation is used.

## 5. Eliminate the remaining 36 electric modes

Let \(m=\sqrt2/4>1/3\), \(P=P_+\), \(Q=E_{42}-P\). The exact matrix bounds give \(\|H_2\|\le864\), \(\|H_3\|<17000\), hence

\[
\|F_E-(I+\beta M)\|
 \le(864+17000\beta+2000000\beta^2)\beta^2<865\beta^2.
\]

The six eigenvalues above WG07's threshold \(1+\beta/6\) must therefore satisfy \(|\nu-(1+m\beta)|<865\beta^2\), because all other magnetic slopes are nonpositive. The complementary \(Q\) block obeys

\[
\nu I_Q-QF_EQ\ge\beta I_Q/4.
\]

Set \(G=(mI_Q-QMQ)^{-1}\), so \(\|G\|<3\). The exact resolvent identity gives

\[
\|(\nu I_Q-QF_EQ)^{-1}-\beta^{-1}G\|\le21600.
\]

Also \(PF_EQ=\beta^2 PH_2Q+R_{PQ}\), \(\|R_{PQ}\|<17003\beta^3\) and \(\|PF_EQ\|<865\beta^2\). Therefore the *full six-mode* energy-dependent Feshbach matrix

\[
F_6(\beta,\nu)=PF_EP+PF_EQ(\nu I_Q-QF_EQ)^{-1}QF_EP
\]

satisfies

\[
\left\|F_6-
\left[(1+m\beta+\tfrac{381}{128}\beta^2)I_6+
\beta^3\sqrt2\left(\tfrac{36499}{49152}I_6+\tfrac1{32}O+\tfrac1{64}X\right)\right]\right\|
< C_6\beta^4
\]

with the explicit rational-integer budget

\[
C_6\le 2000000
 +(865+864)\cdot17003\cdot4
 +864^2\cdot21600
 =16243906348
 <\boxed{20000000000}.
\]

The 48 genuine spatial SU(2) lattice symmetries commute with every block and Feshbach operation above. Their six-mode permutation representation has exactly three invariant irreducible sectors of ranks \(1,2,3\). Thus the actual six-mode nonlinear spectral equation has one eigenvalue in the fully invariant class, a rank-two class, and a rank-three class, each within \(C_6\beta^4\) of its corresponding third-order polynomial eigenvalue.

## 6. Finite-beta acceptance

The verified exact third-order differences are \(3\sqrt2/32\) (symmetric versus even two-dimensional sector) and \(\sqrt2/8\) (symmetric versus odd three-dimensional sector). Since \(\sqrt2>7/5\), the smaller difference exceeds \(21/160\).

For every \(0<\beta\le10^{-12}\),

\[
2C_6\beta\le2(2\times10^{10})10^{-12}
=1/25<21/320,
\]
hence

\[
\nu_{\rm sym}-\nu_{\rm next}
>\beta^3(21/160-2C_6\beta)
>\boxed{(21/320)\beta^3}.
\]

Reinserting \(e^{-24\beta}t\) gives the physical-eigenvalue inequality in section 1. WG08's true interacting normalized physical vacuum Wilson source couples to the unique fully symmetric individual eigenvector with squared weight \(>1/289\); the cutoff here is inside WG08's accepted \(\beta\le10^{-6}\) interval.

**Acceptance boundaries:** spatial L=2 and \(\beta\le10^{-12}\), original continuous SU(2) and original 24-spatial-plaquette/24-temporal-link transfer. Large-volume uniformity, \(\beta\to\infty\) weak-coupling behavior, physical lattice-spacing scaling, Osterwalder–Schrader reconstruction, and 4D continuum Yang–Mills mass gap remain OPEN. Independent external mathematical peer review is additional to the deterministic hosted checks.
