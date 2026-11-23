# YM4-VOL12 pilot — unconditional finite-volume two- and four-star Wilson bounds

**23 November 2026 · original continuous SU(2) Wilson measure · finite-volume analytic derivation and integer replay; independent external mathematical review OPEN.**

This note provides a rigorous **unconditional**, gauge-invariant finite-volume joint bound for bad stars whose incident original plaquette sets are disjoint. It addresses a limited part of [issue #112](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/112), while deliberately retaining **VOL10-JOINT**, physical-size cube, and all eleven continuum obligations as **OPEN**.

## Original model and condition

On the periodic four-dimensional lattice \(\Lambda_L=(\mathbb Z/L\mathbb Z)^4\), \(L\ge3\), let \(V=L^4\), \(N_E=4V\) positive links and \(N_P=6V\) plaquettes. The original continuous-SU(2) Wilson measure is
\[
d\mu_{\beta,L}(U)=Z_{\beta,L}^{-1}\exp\left(\beta\sum_p W_p(U)\right)\prod_e dU_e^{\rm Haar},
\qquad W_p=\tfrac12\operatorname{Tr}U_p,\quad\beta\ge1.
\]
For each original positive link \(e\), the fifteen gauge-invariant double-staple loops define \(B_e=1\) iff some pair of its six preferred staples has \(s_i\cdot s_j<1-\epsilon\). Fix \(0<\epsilon<1\). Choose \(S\) of size \(r\) with **no original plaquette shared by any two selected links**.

## Exact finite-volume joint theorem

VOL09 and VOL11 prove the configuration-wise implication
\[
B_e=1\quad\Rightarrow\quad
\exists p\ni e:\;1-W_p>\epsilon/4.
\]
For \(r\) plaquette-separated links, these forced plaquettes are distinct. Thus every configuration in \(E_S=\bigcap_{e\in S}\{B_e=1\}\) satisfies
\[
\sum_p W_p\le N_P-r\epsilon/4.
\]
Because product Haar has total mass one, the **unnormalized** Wilson weight on \(E_S\) is at most \(\exp[\beta(N_P-r\epsilon/4)]\).

The original continuous-Haar all-link cap lower bound from [VOL09](NOTE-YM4-VOL09-PERIODIC-GOOD-STAR-FREQUENCY-20261122.md) is
\[
Z_{\beta,L}\ge e^{\beta N_P-N_P/2}
(1536\beta^{3/2})^{-N_E}.
\]
Division gives, for every finite \(L\ge3\), every \(\beta\ge1\), and every such \(S\),
\[
\boxed{\mu_{\beta,L}(E_S)\le
\min\{1,(1536\beta^{3/2})^{4L^4}
\exp(3L^4-r\beta\epsilon/4)\}.}\tag{VOL12.1}
\]
This is a **joint original Gibbs estimate without good-exterior conditioning**, not an assumed product of single-star probabilities. Its cost grows exponentially in \(L^4\).

## Fully integer rational upper envelope and independent finite examples

Fix \(\epsilon=1/16\), \(\beta=9^k\), and write
\[
A_k=27(1536\cdot27^k)^4,\qquad
n_{k,r}=\lfloor r9^k/128\rfloor.
\]
Using elementary \(e^3<27\) and \(e^2>2\) produces the **integer-only envelope**
\[
\boxed{\mu_{9^k,L}(E_S)\le
\min\{1,A_k^{L^4}/2^{n_{k,r}}\}.}\tag{VOL12.2}
\]
Indeed \(\exp(-x)<2^{-\lfloor x/2\rfloor}\) for \(x>0\). A conservative simpler test avoids enormous power expansions:
\[
m_{k,L,r}=n_{k,r}-L^4\operatorname{bitlength}(A_k)>0
\Rightarrow\quad \mu(E_S)<2^{-m_{k,L,r}}.
\]
At \(k=7\), \(\beta=4{,}782{,}969\), the exact margins are:

| Torus | Two-star independent set | Four-star independent set |
|---|---|---|
| \(L=3\) | \(P<2^{-60072}\) | \(P<2^{-134806}\) |
| \(L=4\) | \(P<2^{-28397}\) | \(P<2^{-103131}\) |

The [source incidence checker](../../tests/ym4_su2_vol12_finite_packet.py) reconstructs all original links and plaquettes for \(L=3,4\), checks six plaquettes and eighteen neighbors per link, constructs separated packets of sizes two and four, checks these integer margins, and rejects the adjacent-star additivity error. It also uses \(L=8\) at the **same** \(\beta\) as a negative control: the conservative bound is vacuous there, so a volume-uniform conclusion would be unjustified. The source-linked [HBP receipt](YM4-VOL12-FINITE-PACKET-PILOT-20261123.hbp) is replayable.

## Mathematical status and next acceptance

- **Established analytically, pending external referee:** unconditional finite-volume \(r\)-star inequality (VOL12.1) in the *original continuous SU(2) Wilson model*, for plaquette-separated stars, using VOL09's partition cap and the deterministic VOL10/VOL11 defect implication.
- **Exact finite-check acceptance:** integer arithmetic and original \(3^4/4^4\) graph reconstruction; no floating-point approximation and no finite-subgroup substitution for Haar integration.
- **OPEN:** a nontrivial **volume-uniform** joint two-/four-star inequality; uniform \(\rho_\beta^{|S|}\) activity for all separated sets; correlated bad-exterior suppression; physical-size averaged cube; eleven original continuum gates; external mathematical signoff.

The decisive next calculation should replace the all-\(4L^4\)-link partition normalization by a **localized comparison of conditional partition functions**, with boundary frustration treated explicitly. Compare the stronger multiscale and chessboard approaches in [Bhattacharjee et al., *One Cube Estimate Implies the Yang–Mills Mass Gap*, v7](https://hexagonmath.org/2610.00341v7) before making any originality claim.

**No continuum mass-gap inference follows from this finite-volume pilot.**
