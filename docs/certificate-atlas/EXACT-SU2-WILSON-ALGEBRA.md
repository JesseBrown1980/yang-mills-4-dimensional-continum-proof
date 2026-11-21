# Cross-repository exact SU(2) Wilson trace and gauge-holonomy certificate

**Pinned source provenance (2026-11-21).** [Jacobian exact rational quaternion fixture](https://github.com/morluto/jacobian/blob/f693b76a600f8ee0d95a4e429a53bb576e9aeac1/benchmarks/datasets/conjecture-probes-v1/yang-mills-gauge-invariance-certificate/solution/solve.py) and [finite-`N` SU(2) loop equations, Kazakov–Zheng](https://arxiv.org/abs/2404.16925). This note **derives the elementary algebra independently** and ties it to the 4D original Wilson-loop coefficient convention.

## Exact unit-quaternion carrier

Let (U=(a,\mathbf u)\), (V=(b,\mathbf v)) be **unit quaternions**, all four coordinates represented by exact rationals or certified algebraic numbers. The SU(2) defining trace is

\[
  \operatorname{Tr}U=2a,\quad
  \operatorname{scalar}(UV)=ab-\mathbf u\cdot\mathbf v,\quad
  \operatorname{scalar}(UV^{-1})=ab+\mathbf u\cdot\mathbf v.
\]

Consequently the **exact SU(2) trace closure identity**, for all SU(2) links (U,V), is

\[
\boxed{\operatorname{Tr}(U)\operatorname{Tr}(V)
      =\operatorname{Tr}(UV)+\operatorname{Tr}(UV^{-1}).}
\]

With the **normalized** Wilson observable (a(U)=\tfrac12\operatorname{Tr}(U)), this becomes

\[
\boxed{a(U)a(V)=\tfrac12\bigl(a(UV)+a(UV^{-1})\bigr).}
\]

This factor of (1/2) is essential for any sparse transfer evaluator that multiplies **normalized Wilson characters**. The identity closes products of fundamental loop traces algebraically and can be used as a deterministic finite-lattice linear relation. It does not calculate Haar/Gibbs expectations or identify physical excited states.

## Exact gauge-transport and orientation

For an oriented four-link plaquette (P=U_{01}U_{12}U_{23}U_{30}), the local gauge transformation (U'_{ij}=g_i U_{ij}g_j^{-1}) cancels every internal endpoint:

\[
P'=g_0Pg_0^{-1},\qquad \operatorname{Tr}(P')=\operatorname{Tr}(P).
\]

Reversing an oriented edge replaces (U_e) by (U_e^{-1}). The exact rational checker tests **four noncommuting unit-quaternion link values** and **four independent vertex gauge values** from the pinned Jacobian fixture. It independently recomputes plaquette holonomy, local conjugacy, scalar part invariance, and the trace-closure relation, and rejects an incorrectly oriented loop.

## Verification and precise boundary

The executable part is in [`tests/test_ym4_certificate_atlas.py`](../../tests/test_ym4_certificate_atlas.py), within the hosted certificate atlas workflow. It uses integer numerator/denominator pairs and exact operations; no floating point, imported Jacobian runtime, or numerical SU(2) quadrature is required.

- **DERIVED:** exact SU(2) algebraic gauge-transport and normalized first-character trace-closure identities.
- **INTEGRATED:** clean-room integer quaternion fixture, four-edge plaquette gauge-invariance, orientation negative control, single-trace identity.
- **OPEN:** original 4D Wilson Gibbs expectation, certified sparse *entire spatial-link* gauge-projector basis, physical connected moments and lowest excited Wilson spectral weight.
- **SEPARATE:** Kazakov–Zheng SDP numerical lattice-bootstrap bounds. Their exact loop identities are algebraic sources; any numerical SDP bound requires its own rigorous dual feasibility and error certificate before promotion.

This file is a finite exact algebraic input for atlas nodes **EXT-JACOBIAN**, **EXT-LOOP** and **YM4-Q02**. It is not a complete 4D Yang–Mills spectral certificate.
