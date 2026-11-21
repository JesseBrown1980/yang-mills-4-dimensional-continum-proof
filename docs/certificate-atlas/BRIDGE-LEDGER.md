# Cross-repository Certificate Match & Open-Obligation Ledger

**Date:** 2026-11-21. **Project:** original four-dimensional continuous SU(2) Wilson lattice, positive OS transfer, physical gauge projection and physically normalized spectral quantities. The source files listed below are *pointers* to other authors' original work; no external result is rebranded as an internally proved continuum certificate.

## Matching standard: when an existing certificate can be reused

An external candidate becomes an accepted mathematical input only after recording and checking:

1. **Model identity:** continuous SU(2) (or explicitly proved compact-group extension), lattice dimension, periodic/open boundary, plaquette action, link and time conventions.
2. **Physical space and observables:** exact gauge projector/Gauss law, Wilson normalized trace, spatial-slice source, vacuum and time normalization.
3. **Proof form and assumptions:** unconditional finite lemma versus conditional implication, Lean kernel replay versus paper argument versus float experiment; exact rational/interval receipt where claimed.
4. **Scale of conclusion:** one link, one cube, finite lattice, infinite volume, physical spacing or continuum; theorems are carried only across *proved* maps.
5. **Provenance:** immutable source SHA, exact toolchain inputs, license and the verification result or explicit HOLD.

These checks implement the same independent provenance principle as the finite S₃ certificate atlas.

## Explicit OPEN certificate queue

| ID | Needed certificate | Existing source investigated | Match verdict / acceptance gate |
|---|---|---|---|
| YM4-Q01 | Practical **gauge-invariant character/spin-network sparse evaluator** with exact algebra and Gauss-law basis | Anaxia's [character-basis exploratory calculation](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/scripts/check_isotropic_plaquette.py) | **PARTIAL / LEAD**: numerical one-plaquette class model; original interacting 4D physical tensor basis and exact source operator remain OPEN |
| YM4-Q02 | **Exact SU(2) Haar/recoupling coefficients** (integer/rational or certified algebraic), source moments and tail | 4D [existing Haar lemma](../LEMMA-0002-HAAR-MOMENTS.md), [Peter–Weyl bounds](../NOTE-YM4-07H-ALLBETA-SU2-PETER-WEYL-CAP-20261121.md) (draft), Anaxia [Lean one-cube](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/YangMills/OneCube/LemmaW.lean) | **PARTIAL**: low-degree Haar / conditional representation identities available; general physical Wilson-network sparse production OPEN |
| YM4-Q03 | Exact **Gauss-law projection / forest-gauge comparison** between source basis and original physical Wilson transfer | Anaxia [GaugeFix Lean](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/YangMills/StrongCoupling/GaugeFix.lean) and [independent verification](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/VERIFICATION.md) | **FOUND finite/conditional**; requires map from forest-gauge/single cube to periodic 4D spatial-slice physical Hilbert space |
| YM4-Q04 | Certified **original 4D Wilson Gram and normalized transfer moments** at usable beta and volumes | Internal PR #78–#80, original [transfer theorem](../LEMMA-0004-REFLECTION-TRANSFER.md) | **PARTIAL**: norm/error enclosures exist; actual physical Wilson moment *values* and residual traces OPEN |
| YM4-Q05 | Actual **first excited physical Wilson spectral weight**, isolated and certified | [Finite original S₃ first-weight certificate](https://github.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C/blob/main/docs/certificate-atlas/WILSON-FORMAL-ACCEPTANCE-20261120.md), continuous-SU(2) [projector approximation draft](../NOTE-YM4-07I-FINITE-4D-SU2-PHYSICAL-VACUUM-PROJECTOR-20261121.md) | **OPEN for SU(2)**: finite S₃ is a separate gauge model; vacuum-projector accuracy does not compute first excitation weight |
| YM4-Q06 | **Relative**, usable beta/volume character truncation and sparse physically normalized projector error | Internal PR #79–#80 and external [one-cube character inputs](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/YangMills/OneCube/Constants.lean) | **PARTIAL**: exact existence/error cutoff at fixed finite beta, but rank enormous; efficient relative certificate OPEN |
| YM4-Q07 | **Volume-uniform** mixing/physical energy gap along beta(a), large volumes | Anaxia [forest-gauge / Dobrushin finite strong-coupling certificates](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/YangMills/StrongCoupling/GaugeFix.lean); [published 2026 lattice theorem](https://hexagonmath.org/2610.00341v4) | **FOUND strong-coupling scope**; finite bare-beta ceiling does not establish weak-coupling continuum trajectory |
| YM4-Q08 | A **one physical-size cube** or multiscale RG contraction held *uniformly along tuning* | [Anaxia one-cube conditional theorem](https://hexagonmath.org/2610.00341v4) and [first scale certificates](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/YangMills/StrongCoupling/CubeOpen.lean) | **CONDITIONAL/OPEN**: paper explicitly says one-cube estimate along the whole continuum tuning remains OPEN |
| YM4-Q09 | Verified **UV continuum, nontriviality and OS/Wightman reconstruction** without assuming desired gap | [Formalized construction from certified assumptions](https://hexagonmath.org/2611.00492v1), [source repository](https://github.com/yang-mills-group/YM), and Balaban RG literature | **CONDITIONAL**: Lean verified construction from 16 external assumptions; unproved input package and nontriviality must be checked |
| YM4-Q10 | **Uniform physical exponential clustering** / positive continuum **full-spectrum mass gap** | [Conditional MG uniform-rate theorem](https://hexagonmath.org/2611.00492v1), [Clay problem status](https://www.claymath.org/millennium-problems/) | **OPEN**: source itself states its axioms do not imply mass gap; no source-verified accepted full result found |
| YM4-Q11 | **Source-to-source certificate transport** between finite S₃, original continuous SU(2), and external forest gauge | [finite atlas](https://raw.githack.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C/main/docs/certificate-atlas/atlas-current-20261120.html), original [4D conditional bridge](../NOTE-YM4-07C-WILSON-SOURCE-PROJECTION-BRIDGE-20261120.md) | **OPEN**: requires a proved intertwiner, action normalization, physical projector and error budget; matching vocabulary alone is insufficient |

## Existing certificates that we can use now

### 1. Anaxia 4Y-M: exact finite-gauge and one-cube verification references

- **Verified as a public source:** [Lean gauge fixing](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/YangMills/StrongCoupling/GaugeFix.lean), [Lemma W](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/YangMills/OneCube/LemmaW.lean), [exact rational line-field certificate producer](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/julia/onecube/be_certificates.jl), [independent verification report](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/VERIFICATION.md). The linked repository is MIT-licensed; preserve its attribution and theorem scope.
- **Reuse:** explicit lattice incidence/four-dimensional graph topology controls; exact rational constants, coefficient normalization, and independent gauge-fixing checks. A small exact rational source-envelope from their [single-cube certificate script](https://github.com/anaxia-research/4Y-M/blob/df315270aafd456068783359cf0d07e6f3d76de8/scripts/single_cube_constants.py) is suitable for a checker-to-checker replay, *with the finite-constants-only scope*.
- **Not automatically promoted:** floating-point character plots and sample eigenvalues, finite-strong-coupling bulk gap as continuum proof, one-cube conditional hypothesis without verification along the entire weak-coupling tuning.

### 2. Independent Lean construction with certified assumptions

- [November 2026 formal construction and validation report](https://hexagonmath.org/2611.00492v1) and [source repository](https://github.com/yang-mills-group/YM).
- **Reusable now:** theorem statement and proof *conditional on its sixteen registered analytic inputs*, checker/toolchain provenance, and the crucial **countermodel** showing the inputs allow an OS theory with no mass gap.
- **Required before importing into an SU(2) proof:** match all RG/UV/PH/AN/Y/B/C assumptions to our original Wilson action and actual verified inputs. The paper says the complete mass gap is equivalent to an additional uniform exponential rate (MG), still OPEN.

### 3. Finite S₃ companion Atlas

- [Original finite first-Wilson certificate](https://github.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C/blob/main/docs/certificate-atlas/WILSON-FORMAL-ACCEPTANCE-20261120.md) and [live 3D graph](https://raw.githack.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C/main/docs/certificate-atlas/atlas-current-20261120.html).
- **Reusable now:** SHA/HBP freeze, independent Feshbach Schur–Gram certificate architecture, original-source raw dual verifier methods, and fail-closed proof-object schema.
- The finite `3×4 S₃,r=9` physical Wilson first-weight theorem is **about finite S₃**, and the atlas correctly keeps it separate from the continuous SU(2) physical mass-gap requirement.

### 4. Other public proof candidates

A search located several 2026 works claiming stronger continuum results (published papers, Zenodo and preprints). These are **research leads**, not accepted imports. To upgrade any to a proof input, require an openly inspectable certificate or complete original derivation, verify all renormalization hypotheses and observables, and obtain independent reproduction. The Clay Mathematics Institute continues to list the full continuum Yang–Mills mass gap as unsolved.

## Prioritized producer order

**First:** use Anaxia finite exact lattice incidence and SU(2) one-cube identities as independent unit tests for our sparse transfer code; preserve the original continuous SU(2) Wilson transfer and our integer-only proof receipt. **Second:** compute a real normalized Wilson Gram and two-step/four-step transfer moment at a tractable spatial size with certified representation tails. **Third:** isolate the actual first Wilson-excited state and source spectral weight in that same physical sector. **Fourth:** tackle cross-volume weak-coupling and physical-size cube RG estimates, connecting to the externally formalized conditional OS construction.

Each subgate on the 3D graph points here, to its parent obligation and to candidate outside sources. **Import status at this checkpoint: mathematical references and exact finite constants available; the continuum mass-gap certificate remains OPEN.**
