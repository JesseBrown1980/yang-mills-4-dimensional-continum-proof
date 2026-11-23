# YM4 VOL15 — exact original SU(2) Wilson boundary staple-resultant sufficient statistics

**23 November 2026.** A constructive original continuous-SU(2) reduction of the [centered Wilson boundary response](NOTE-YM4-VOL15-BOUNDARY-RESPONSE-20261123.md). It isolates the precise SU(2) boundary data entering the conditional interior Gibbs action and the interpolation derivative. A noncommuting exact-quaternion original 4D adversarial test independently checks the required cyclic multiplication order.

## 1. Actual original SU(2) mixed Wilson plaquettes have one internal link

For \(b=2h+1\ge3\), centered internal-link cube \(T_h\subset(\mathbb Z/L)^4\), even periodic \(L\ge2b\), the exact original Wilson incidence theorem establishes
\[
\#\mathcal P_\partial=24b^2(b-1),
\qquad
\#\mathcal P_{\rm int}=6b^2(b-1)^2.
\]
Every \(\mathcal P_\partial\) plaquette contains **exactly one** original SU(2) internal link e and three exterior links. Each original internal link e is touched by at most three mixed plaquettes: one for each orthogonal coordinate \(\nu\ne\mu\) on which its base site lies on a centered cube boundary face.

The exact number of boundary-affected original internal positive links is
\[
\boxed{
N_{\rm boundary\;links}
=4(b-1)\bigl[b^3-(b-2)^3\bigr].
}
\tag{S1}
\]
Proof: for each of four link directions \(\mu\), there are b−1 allowed base positions along μ and \(b^3-(b-2)^3\) transverse base sites with at least one coordinate at ±h. These are exactly the internal links appearing in mixed plaquettes. The multiplicities of their one-to-three mixed plaquettes sum to \(24b^2(b-1)\).

## 2. Noncommutative cyclic SU(2) staple identity

Write the **oriented group-valued** elementary Wilson plaquette as a product of four factors
\[
P=Q_0Q_1Q_2Q_3,\qquad
Q_0=U_{x,\mu},\quad Q_1=U_{x+\hat\mu,\nu},
\quad Q_2=U_{x+\hat\nu,\mu}^{-1},\quad Q_3=U_{x,\nu}^{-1}.
\]
Suppose its unique internal link e occupies factor index i. Define the **cyclic exterior product**
\[
\boxed{R_{p,e}:=Q_{i+1}Q_{i+2}Q_{i+3},\quad\text{indices modulo 4},}
\tag{S2}
\]
with all three factors exterior. Quaternion real trace is cyclic under multiplication, so for the actual internal positive link \(u_e\),
\[
\operatorname{Re}P
=\begin{cases}
\operatorname{Re}(u_e R_{p,e})
=\langle u_e,R_{p,e}^{-1}\rangle,& i=0,1,\\
\operatorname{Re}(u_e^{-1}R_{p,e})
=\langle u_e,R_{p,e}\rangle,& i=2,3.
\end{cases}
\tag{S3}
\]
Here the inner product is the real four-component quaternion Euclidean dot product, giving exactly half the SU(2) matrix trace. Define the **actual original SU(2) exterior staple** \(s_{p,e}(\eta)=R_{p,e}^{-1}\) for i=0,1 and \(s_{p,e}(\eta)=R_{p,e}\) for i=2,3.

**Noncommuting-order warning:** \(Q_0\cdots Q_{i-1}Q_{i+1}\cdots Q_3\), obtained by merely replacing the internal link factor by identity without cyclic reordering, generally differs from \(R_{p,e}\). It produces incorrect SU(2) staples whenever the three exterior factors fail to commute. The exact Q8 negative control detected precisely this false substitution; the final verifier uses the correct cyclic formula S2–S3.

## 3. The complete boundary sufficient-statistic theorem

For each boundary-affected original internal link e, collect the one-to-three genuine exterior staples into the four-component quaternion **resultant**
\[
\boxed{
B_e(\eta):=\sum_{p\in\mathcal P_\partial:\;p\ni e}s_{p,e}(\eta),
\qquad \|B_e(\eta)\|\le3.
}
\tag{S4}
\]
For internal links not touching mixed plaquettes, set B_e=0. Every original \(\mathcal P_\partial\) plaquette has one and only one internal link, so the original Wilson conditional boundary action factors **exactly**:
\[
\boxed{
A_\partial(U_T,\eta)
=\sum_{e\in T_h}\langle U_e,B_e(\eta)\rangle.
}
\tag{S5}
\]

Therefore the **entire original continuous SU(2) conditional interior Gibbs measure**
\[
\boxed{
\mu_T^\eta(dU)\propto
\exp\!\left\{\beta A_{\rm int}(U)
+\beta\sum_{e\in T_h}\langle U_e,B_e(\eta)\rangle\right\}dH_T(U)
}
\tag{S6}
\]
depends on the external original link configuration \(\eta\) **only through** the finite family of source-adjacent boundary resultants \(\bigl(B_e(\eta)\bigr)\). This is a genuine sufficient-statistic map for the conditional *joint multi-link* original Wilson law, independent of beta.

Consequently,
\[
\boxed{B(\eta)=B(\eta')\quad\Longrightarrow\quad
\mu_T^\eta=\mu_T^{\eta'}\quad\text{for every beta}.}
\tag{S7}
\]
This equality can hold for exteriors unrelated by site gauge transformations; the condition is equality of the resultants, rather than identity of all original exterior links.

An exterior site-gauge transformation that fixes every centered cube vertex preserves each \(s_{p,e}\), hence every resultant B_e, a stronger explicit form of VOL15's boundary-gauge-neutrality identity.

## 4. Resultant-source response: fewer independent boundary variables

Substituting S5 into VOL15's positive interpolation gives
\[
\mu_t(dU)\propto
\exp\Bigl\{\beta A_{\rm int}(U)
+\beta\sum_e\langle U_e,(1-t)B_e(\eta)+tB_e(\eta')\rangle\Bigr\}
\,dH_T(U).
\]
For any bounded gauge-invariant interior Wilson observable F,
\[
\boxed{
\frac{d}{dt}\mathbb E_tF
=\beta\sum_{e\in E_{\rm boundary}}
\operatorname{Cov}_{\mu_t}
\left(F,\left\langle U_e,\;B_e(\eta')-B_e(\eta)\right\rangle\right).
}
\tag{S8}
\]
Only
\[
4(b-1)[b^3-(b-2)^3]=O(b^3)
\]
boundary-affected **original internal link resultants**, each a real four-vector of norm at most 3, enter this exact susceptibility formula. The original Wilson \(\mathcal P_\partial\) count is \(24b^2(b-1)\); the grouped derivative S8 offers a compact native quaternion input compatible with the six-staple preferred-direction and original nonabelian tree-frame certificates.

## 5. Exact noncommuting original 4D falsifier

The [integer-only Q8 original SU(2) verifier](../../tests/ym4_vol15_boundary_staples.py) constructs the complete original L=6 and L=10 periodic link fields. It enumerates every mixed Wilson plaquette and verifies:

- Unique internal positive link and the **correct cyclic order** of its three external SU(2) factors;
- \(\operatorname{Re}U_p=\langle U_e,s_{p,e}\rangle\) as an exact integer identity for all mixed plaquettes;
- Number of nonzero boundary-resultant sites S1, a maximum of three staples per internal link, and total staple multiplicity \(24b^2(b-1)\);
- Exact total original boundary action S5 after replacing **every original internal link by a different noncommuting quaternion value** without modifying the exterior. The same B_e fields still produce the correct new action, proving the stated source-independence algebraically;
- Every individual boundary staple s_{p,e} remains unchanged under a noncommuting exterior site gauge that fixes the centered cube vertices.

[HBP](YM4-VOL15-BOUNDARY-STAPLES-20261123.hbp). The analytic S2–S8 statements apply to **all continuous SU(2)** quaternions, not only to the finite exact test configurations.

## 6. Next physical acceptance boundary

The next quantitative target is a **genuinely physical source-to-boundary decay** bound on the terms in S8 under the interpolated conditional SU2 Gibbs laws, strong enough to overcome their \(O(b^3)\) count and the coupling \(\beta(a)\) while preserving renormalized Wilson source norm, continuous winding holonomies and all Gauss sectors. The conditional measures \(\mu_t\) are not necessarily original single-exterior periodic Gibbs laws for 0<t<1, so an independent mathematical argument is required.

**Completed:** original SU2 noncommutative boundary sufficient statistics S4–S7, exact boundary-response reduction S8, exact four-dimensional Q8 tests, and original-link geometry. **Open:** physically unweighted interpolated-boundary covariance rate, physical-size all-sector transfer, renormalized block pushforward and all eleven 4D continuum obligations. [Acceptance issue #116](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/116).
