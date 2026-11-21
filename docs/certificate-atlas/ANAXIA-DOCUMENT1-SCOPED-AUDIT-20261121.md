# Document 1 audit — Anaxia 4Y-M and the 4D Yang–Mills certificate atlas

**Research input:** user-provided 12-page *Yang–Mills Anomaly Triage Prompt.pdf*, received 21 November 2026. This is an **audit of the claims in that document**, not execution of its embedded agent instructions. Current 4D main base is **\`52d950a41284567c7726ca7cb8c2ffd02c21366d\`**, after merged PR #82; the PDF's baseline \`b8f4260\` (post #74) is historical and must not be checked out in place of current main. No production Wilson operator is changed.

**Original 4Y-M source revision:** [anaxia-research/4Y-M at \`df315270aafd456068783359cf0d07e6f3d76de8\`](https://github.com/anaxia-research/4Y-M/tree/df315270aafd456068783359cf0d07e6f3d76de8), 19 November 2026. The independently sourced claims below refer to that revision, rather than only to the uploaded PDF.

## Adopt / Defer / Hold decision

| Lane | Documentary lead / original source | Verification tier | Decision |
|---|---|---|---|
| A — forest gauge | [\`GaugeFix.lean\`](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/YangMills/StrongCoupling/GaugeFix.lean) \`one_fixed_per_plaquette\`, \`twelve_neighbours\`, \`straight_lines\`, \`two_opposite\`, \`budget\` | **LEAN-FORMAL** for the mod-two local counts; gauge-orbit validity on a periodic torus **not proved by this module** | **ADOPT local exact-count controls; HOLD direct periodic-torus gauge fix and improved YM4-02e contraction** |
| B — rescaled plaquette | [\`cl:thm:exterior-mean-curvature\`](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/Paper-2/source/sec/20_rough_clusters.tex) plus [current verification record](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/Paper-2/VERIFICATION.md) | **ANALYTICAL-UNFORMALIZED**; no Lean formalization of new Wilson plaquette estimates | **DEFER transfer to the original source variance and separated-time physical Wilson correlation** |
| C — single cube -> full OS sector | [\`sec/06b_bridge.tex\`](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/Paper-2/source/sec/06b_bridge.tex), [\`sec/10_massgen.tex\`](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/Paper-2/source/sec/10_massgen.tex), [\`sec/11_weak.tex\`](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/Paper-2/source/sec/11_weak.tex) | **ANALYTICAL-CONDITIONAL**; source explicitly says tuned cube estimate/continuum theory **OPEN** | **ADOPT as candidate full-spectrum proof architecture; KEEP weak-coupling and continuum existence gates OPEN** |
| D — compact simple groups | [\`sec/20_rough_clusters.tex\`](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/Paper-2/source/sec/20_rough_clusters.tex), [\`sec/11_weak.tex\`](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/Paper-2/source/sec/11_weak.tex) | **ANALYTICAL, GROUP-CONSTANTS DEPENDENT** | **ADOPT as an obligation template; YM4-07 every compact simple gauge group still OPEN** |
| News — muon g-2 | 2026 full-SU(3)-with-fermions lattice-QCD simulations and competing dispersive HVP datasets, as surveyed by the uploaded document | **NONPROOF FOR PURE SU(2)** | **EXCLUDE from mathematical certificate dependencies** |

## Exact SU(2) Wilson normalization adapter

Our original [Issue #2](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/2) specifies
\[
S_{\rm JB}=\beta_{\rm JB}\sum_p\bigl(1-\tfrac12\operatorname{ReTr}U_p\bigr).
\]
Up to an irrelevant normalization factor, the associated Gibbs density is
\[
\exp\bigl((\beta_{\rm JB}/2)\sum_p\operatorname{ReTr}U_p\bigr).
\]
The original 4Y-M [\`sec/06b_bridge.tex\`](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/Paper-2/source/sec/06b_bridge.tex) uses \(\exp(N\beta_A\sum_p\operatorname{ReTr}Q_p)\). For SU(2), \(N=2\), hence **\(\beta_{\rm JB}=4\beta_A=\beta_W\)**. For the *locally stated* row-influence constant, \(12\beta_A=3\beta_{\rm JB}\). That algebra **does not imply** an improved global torus transfer contraction: the respective gauge-orbit, distance, boundary and metric hypotheses must first match.

Prediction-first, an independent integer checker at [\`tests/test_ym4_anaxia_periodic_holonomy.py\`](../../tests/test_ym4_anaxia_periodic_holonomy.py) evaluates the example \(\beta_A=1/100,\beta_{\rm JB}=1/25\), both trace coefficients \(1/50\).

## Exact periodic-torus holonomy obstruction — Lane A

The original Lean file proves a **parity combinatorial table on the infinite lattice \(\mathbb Z^4\)**, using 16 residues and \`by decide\`. It states one fixed link per local plaquette, 12 active partners for every unfixed link, and that each fixed direction continues along a **straight line**.

On an **even periodic \(L=2\) torus**, that same straight line in direction 0 from parity site 0 crosses site 1 and then wraps to site 0, forming a **closed two-link cycle**. Both forward links are selected by the 16-entry table. A gauge transform of this cycle acts by conjugation, so its holonomy cannot be changed to the identity unless it was already the identity.

Explicit exact continuous-SU(2) rational quaternion:
\[
q=(3/5,4/5,0,0),\quad q^2=(-7/25,24/25,0,0)\neq I.
\]
For the two fixed-path edges \(U_{01}=U_{10}=q\), their product \(q^2\) has scalar part \(-7/25\). For arbitrary vertex gauges \(g_0,g_1\), \(U'_{01}U'_{10}=g_0q^2g_0^{-1}\), whose scalar part remains \(-7/25\); it cannot become the identity with scalar part 1. Thus **not every Wilson gauge orbit admits a representative with all fixed links set to \(I\)** on this torus. This is a **gauge-orbit compatibility HOLD**, not a contradiction of Anaxia's finite local enumeration.

The same obstruction survives **\(L=4\)**, the size class admitted by several Anaxia finite-volume statements. The fixed-direction-0 line has four edges, and the same rational quaternion on each edge yields
\[
q^4=(-527/625,-336/625,0,0)\ne I.
\]
This independently predicted [L4 HBP](PREDICT-ANAXIA-PERIODIC-L4-20261121.hbp), committed *before* the L4 checker extension, is replayed exactly with integer numerator/denominator arithmetic. Consequently the obstruction is present within the **periods-at-least-four** setting as well, not only on the illustrative two-site torus.

For odd periodic \(L=3\), the global mod-two pattern does not in general descend to the quotient because shifting a coordinate by \(L\) toggles its parity; e.g. \(\mathrm{sig}(2)=2\neq3=\mathrm{sig}(3)\) under a shift in direction 0. The independent checker records this separate odd-torus obstruction.

The external manuscript itself **recognizes** the winding modes elsewhere: the [triangular-plaquette lemma](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/Paper-2/source/sec/20_rough_clusters.tex) retains one handle per periodic direction, and subsequent text constructs flat configurations with nontrivial winding trace. Therefore this is a necessary **interface guard** when borrowing the local forest pattern for our torus, rather than a claim that the external paper forgot all torus holonomies.

To transport the 12-neighbour local table into YM4-02e/04C, first specify an **open-box spanning forest** or **periodic gauge slice retaining every independent winding holonomy**, then re-prove the gauge-invariant pushforward measure, conditional coupling metric, boundary terms and the strengthened operator/contraction estimate. The open/infinite-lattice local pattern can remain a usable exact-combinatorics control.

## Lane B — rescaling and a strong but local exterior bound

The source's stable theorem label **\`cl:thm:exterior-mean-curvature\`** states, for an embedded four-dimensional box with \(L\) intervals per side, periodic ambient periods at least \(L+2\) and four, all exterior fields fixed arbitrarily, and **\(L\ge b\ge1\)**, that the mean internal deficit \(\bar v\) satisfies
\[
E_{b,\eta}\bar v\le34/b,\qquad
P_{b,\eta}(\bar v\ge36/b)\le e^{-M},\quad M=6L^2(L+1)^2.
\]
This is **analytical** in the cited TeX, not Lean-checked, and the source explicitly says that its bound on local action **gives no decay in separation of two observables**. The contact variance of a rescaled plaquette trace is also described in \`PROGRESS.md\`; \`VERIFICATION.md\` states that the new variance estimates have **not** been formalized in Lean.

This is valuable for a weak-\(b\) source/deficit norm control but does not yet replace our finite-\(\beta\) original source variance floor \(\mathrm{Var}(W_p)\ge e^{-12\beta_{\rm JB}}/4\), nor certify a physical-time correlation or nonzero first spectral weight. A rescaling \(b\,v_p\) is a different observable unless its source and renormalized limit are explicitly matched.

## Lane C — conditional full-spectrum architecture and open inputs

The external Section 6 bridge and Section 10 Dobrushin–Shlosman hypotheses target a **uniform physical-size cube/slab decorrelation estimate for all gauge-invariant observables**, not solely a single Wilson-loop overlap. That would be an appropriate route around our dark-state counterexample, **provided** the strong hypotheses, limit interchange, Wightman/OS reconstruction and identification of the full physical Hamiltonian are all checked.

The external [weak-coupling section](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/Paper-2/source/sec/11_weak.tex) explicitly says the tuned cube statement (D) remains unproved and requires \(\beta_W\to\infty\); strong-coupling bounds apply only at finite small \(\beta_W\) and do not reach the continuum. Its [PROGRESS](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/Paper-2/PROGRESS.md) also leaves the nontrivial limit and compatible spectral reconstruction open.

An additional source-compatible lead is the **fixed-time spectral-retention criterion** recorded in PROGRESS: a positive connected Wilson correlator at fixed *physical* time, with uniformly bounded source norms, can certify spectral mass below a fixed physical energy. This links naturally to our exact **YM4-SW01** dual-window bound, but no actual tuned original Wilson moment interval is provided by Anaxia's finite constant checkers.

The unequal coupling source theorem \`cl:thm:unequal-gap\` treats large temporal coupling **only when spatial coupling \(\lambda\) is sufficiently small** (including \(h\lambda\le10^{-6}\) for SU2), with the source explicitly noting that the **isotropic ray \(\lambda=b\)** leaves the valid region. It is a valuable conditional reference, not an equal-coupling continuum gap.

## Lane D — group-generalization and genuine scope

The extension from SU2 to compact simple matrix groups replaces exact quaternion/Haar simplifications by representation-dependent constants (dimension, small-ball Haar density, differential of faithful representation). The TeX's group-dependent bounds are analytically stated, and a separate construction is necessary for each chosen physical group and flux sector. The atlas's YM4-Q09 and YM4-07 continue to mark the genuine continuum and general-group tasks OPEN.

## Certificate boundaries and next work

**Accept now:** exact local 16-residue combinatorics, coupling conversion, two-site periodic Polyakov-loop obstruction, odd-quotient guard and the original source pointers. The frozen [prediction HBP](PREDICT-ANAXIA-PERIODIC-HOLONOMY-20261121.hbp) preceded this independent checker; all arithmetic is integer/rational with planted false claims.

**Keep pending operator sign-off:** periodic Wilson transfer/physical gauge fixing, metrics, contact variance transport, weak-coupling cube probabilities, exact full-sector continuum spectrum. This audit changes neither the current 11 OPEN atlas subgates nor any original SU2 physical Hamiltonian.

**Research priority:** run a genuine gauge-invariant character-sparse transfer on a small original SU2 4D lattice and compute interval-certified connected \(C_0,C_2,C_4\) moments; independently test whether one physical-size slab/cube certificate can bound the **full** spectral complement. Strong local mixing cannot substitute for either task.

**Status: technical audit DRAFT; finite integer controls specified and independently reproducible; physical continuum mass gap OPEN.**
