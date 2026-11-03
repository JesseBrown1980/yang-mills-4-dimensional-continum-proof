# Lemma YM4-01 — SU(2) plaquette gauge covariance in four dimensions

**Claim:** PROVED (elementary algebra); independent review OPEN. **Executable:** EXACT-TEST on a small periodic four-dimensional lattice. **This is not a continuum existence or mass-gap theorem.**

Let Λ be a finite periodic four-dimensional hypercubic lattice, with positively oriented SU(2) link variables U_μ(x), and an arbitrary local SU(2) gauge transformation g(x). Under

```text
U_μ(x) -> U'_μ(x) = g(x) U_μ(x) g(x+μ)^(-1)
```

and for μ < ν, with the positively oriented plaquette matrix

```text
U_{μν}(x) = U_μ(x) U_ν(x+μ) U_μ(x+ν)^(-1) U_ν(x)^(-1),
```

the exact transformation law is

```text
U'_{μν}(x) = g(x) U_{μν}(x) g(x)^(-1).
```

**Proof:** Substitute the four transformed links. Gauge factors at each intermediate vertex cancel with the inverse factor from the next incident link. The two remaining factors at the base vertex x conjugate the plaquette. Therefore Tr(U'_{μν}) = Tr(U_{μν}), and the Wilson action S_W is gauge invariant. SU(2) matrices have unitary eigenvalues, so -2 ≤ Re Tr U_{μν} ≤ 2 and S_W ≥ 0 for β ≥ 0. QED.

## Finite executable test

`tests/test_exact_su2_4d.py` uses exact Python rational quaternions, the standard-library `fractions.Fraction`, and *genuinely noncommuting* SU(2) elements—not a fixed finite subgroup model. It chooses independent link values and independent gauge transformations at all 16 sites of (ℤ/2ℤ)^4; 64 positive links and all 96 μ<ν plaquettes are checked.

The nontrivial rational SU(2) generators include (3/5,4/5,0,0), (5/13,0,12/13,0) and (8/17,0,0,15/17); every value has unit quaternion norm in exact fractions.

The executable checks plaquette matrix covariance under conjugation, invariant plaquette traces and invariant Wilson action, for four reproducible pseudorandom seeds. It requires two intentional errors to fail: shifting one trace by 10^-6 and dropping an endpoint inverse in the gauge law. The test fails closed if either deliberate error passes.

```bash
python3 -I tests/test_exact_su2_4d.py
```

Expected:

```text
EXACT_SU2_4D|sites=16|links=64|plaquettes=96|seeds=4|gauge_covariance=PASS|wilson_action=PASS|fault_controls=2/2|failures=0|json=0
SCOPE|finite_periodic_lattice_only=1|continuum_existence=OPEN|physical_mass_gap=OPEN|json=0
```

**What remains OPEN:** finite-volume reflection positivity matched to the chosen precise setting, a rigorous RG transformation with uniform scale bounds, the nonperturbative continuum limit, OS/Wightman reconstruction, and an actual positive physical mass gap. These are separate claims in the proof-obligation ledger.
