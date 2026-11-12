# External four-dimensional Yang–Mills existence assessment — November 12, 2026

**Research classification:** external reviewed claim, not a result independently verified by this repository. **Our project’s Clay mass-gap status remains OPEN.** No changes to frozen finite certificates or to the protected coupling-`r=9` floor launch.

## Primary evidence and scope

- [OpenAI, *Working with academic communities to build scientific understanding*, October 26, 2026](https://openai.com/index/building-scientific-understanding-with-academic-communities/): an internal system produced an existence construction for 4D pure Yang–Mills and QCD, building on Balaban’s renormalization-group program.
- [Yang–Mills working group, public evidence repository](https://github.com/yang-mills-group/YM), [assessment PDF](https://github.com/yang-mills-group/YM/blob/main/docs/assessment-1.pdf): the group’s assessment dated November 10, 2026 judges OpenAI’s **October 28** Lean submission to construct a relativistic Wightman QFT as a scaling limit of four-dimensional Wilson lattice gauge theory for simple compact gauge groups. The group **does not** claim a positive mass gap or uniqueness of the infinite-volume limit.
- [The working group’s precise check scope](https://github.com/yang-mills-group/YM/blob/main/submissions/openai-20261028/docs/checks.md): formal acceptance relates the finite Wilson law, selected UV/IR limits, phase averaging/reconstruction, selected scalar OS stress-trace hierarchy, operator labels, normalization and leading short-distance behavior. A **positive lattice probe is not an intrinsic positive continuum mass**. The combined statement does not assert uniqueness, confinement, a mass gap or all-orders perturbative matching. The separate OPE check is **not** automatically the same existential witness as the combined existence theorem.
- [Reproduction instructions](https://github.com/yang-mills-group/YM/blob/main/submissions/openai-20261028/docs/rerun.md): pinned submission uses **Lean 4.32.0**, pinned Comparator and Mathlib, a source-hash/axiom audit, negative controls and kernel rechecks. The initial build is resource-intensive; check source interfaces and provenance before launching full compilation.
- The same group records an **OpenAI November 4 submission as work in progress**. Its claims are not accepted in the first assessment.

**External-review caveat:** the group’s statement is an expert judgment plus formal evidence, not a mathematical proof of every possible physical interpretation. The checker explicitly separates Lean derivations from human evaluation that its definitions match the intended quantum field theory. We have **not** rerun its Lean package or audited each of its declarations.

## Immediate effect on the three scopes of this repository

1. **Primary finite continuous-SU(2) Wilson lattice:** unchanged. Our fixed-spacing transfer/cluster proofs and exact arithmetic remain independently meaningful. They do not inherit the external continuum result as their own theorem.
2. **Fixed physical finite volume with a→0:** the external Wilson scaling-limit framework offers a possible reference construction for the corresponding observables, normalization and limit ordering. To invoke it, we must prove **an explicit model/observable correspondence**, not merely cite its existence theorem.
3. **Clay R⁴ continuum theory with a positive mass gap:** the construction portion now has a public external candidate judged successful for its scoped criteria, but the **positive physical gap is still OPEN**. Our target must not be relabeled “proved” until a rigorously compatible gap theorem for that *same* continuum Hilbert space is available.

Our finite gauge-group `S3` Hamiltonian is **not** the simple compact Lie-group Wilson `SU(2)` lattice measure covered by the external construction. The `r=12` finite magnetic-cutoff spectrum and the protected `r=9` finite run cannot be promoted to a continuum `SU(N)` gap by group- or cutoff-identification. No finite-`S3` mass estimate alone supplies a renormalized weak-coupling trajectory.

## The concrete continuum-gap bridge to pursue (YM4-06 / YM4-07)

For the physical transfer matrix at lattice spacing `a`, volume `L` and actual Wilson inverse coupling `β(a)`, define (where the transfer is positive and the vacuum is isolated)

```
γ(a,L) = - log(λ_first_excited(a,L)/λ_vacuum(a,L))
m(a,L) = γ(a,L)/a.
```

The required nonperturbative certificate is **not** merely `γ(a,L)>0` for each lattice, but a strictly positive fixed physical lower bound `m(a,L)>=m_*>0` along the actual asymptotically free `β(a)→∞` and suitable volume limits, with the complete relevant physical spectrum represented. The bound must survive infinite volume, continuum reconstruction and every symmetry sector, including states invisible to a selected Wilson loop.

An alternative suitable target, subject to OS positivity and a dense physical observable algebra, is a **scale- and volume-uniform positive-time connected correlation bound** in physical units:

```
0 <= <(O-<O>)Ω, exp(-tH)(O-<O>)Ω> <= C_O exp(-m_* t)
```

for every `O` in an appropriate dense set of local gauge-invariant reconstructed operators (with normalizations and constants controlled through the continuum limit), not just one Wilson loop. Spectral positivity then excludes spectral support in `(0,m_*)` in the selected phase. **Neither the external existence submission nor our current YM4-04 strong-coupling bounds establishes this uniform statement.**

Before treating an existing block estimate as proof of continuum mass:

- Match the **same** 4D Wilson measures, field/operator dictionary, selected pure phase, physical-time semigroup, normalization and order of limits to the external construction’s checked `LatticeAndScale` / OS interface.
- Show actual renormalized `β(a)→∞` and uniformly control nonlocal Wilson networks/induced effective actions and discarded spectral weight. Our `β=1/1000` Dobrushin regime is not the UV regime.
- Obtain a first full-spectrum lower gap or a correlation bound on a dense observable family. Single-operator decay and `S3` finite magnetic first-gap numerics cannot exclude spectrally dark or nontrivial symmetry states.
- Audit hypotheses and check counterexamples before claiming the continuum gap; preserve exactly which independent Lean checks have *actually* been rerun.

The external formal existence result should be used as **a candidate target theorem and shared language**, not as a magic lift of our finite calculations.

## Immediate priorities

1. Map the review’s `CombinedAcceptance`/`LatticeAndScale`/OS construction to YM4-05 and YM4-07. Pin exact definitions, coupling scheme and the physical transfer/observable interfaces. Cite the same witness instead of combining incompatible existential choices.
2. Keep YM4-06 as the full physical-gap objective. Focus on uniform weak-coupling, complete-spectrum control in physical time, not more fixed-`β` proof-of-existence.
3. Track the separate **November 4** external submission, but assign it *no mathematical conclusions* until assessed.
4. Retain the independent finite `S3` spectral research and `r=9` gate. No dependency or authorization has changed for the protected floor freeze.

**Verdict as of November 12, 2026:** significant external progress on continuum Yang–Mills **existence**, no proof of the Millennium **mass gap**, and no automatic bridge from our finite group to the reviewed continuous gauge-group theory.
