# Lemma YM4-01 — SU(2) plaquette gauge covariance in four dimensions

**Claim:** PROVED (elementary algebra); independent review OPEN. **Executable:** EXACT-TEST on a small periodic four-dimensional lattice. **Scope:** each finite periodic lattice. The executable runs the 2⁴ torus.

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

`tests/test_exact_su2_4d.py` uses exact rational quaternions held as integer tuples, and noncommuting generators A, B, C of infinite order. The palette also holds the identity. It chooses independent link values and independent gauge transformations at all 16 sites of (ℤ/2ℤ)^4; 64 positive links and all 96 μ<ν plaquettes are checked.

The nontrivial rational SU(2) generators include (3/5,4/5,0,0), (5/13,0,12/13,0) and (8/17,0,0,15/17); the link and gauge values have unit quaternion norm, checked in exact integers.

The executable checks plaquette matrix covariance under conjugation, invariant plaquette traces and invariant Wilson action, for four reproducible pseudorandom seeds. It requires two intentional errors to fail: corrupting one link of the transformed field and dropping an endpoint inverse in the gauge law. The test fails closed if either deliberate error passes. It also pins the four values of the Wilson action, a one-link fixture with S_W = 18/5, and the product A·B, and it replaces each of the 96 plaquettes on each seed by a wrong matrix, which the covariance check must detect. At 372 of the 384 positions the wrong matrix keeps the trace. At the other 12 the plaquette is the identity, the only SU(2) element with half trace 1, so the wrong matrix moves the trace as well. **Correction, November 3:** before this date the first control compared a value with itself plus 10⁻⁶, which passes on any arithmetic, and the receipt read `fault_controls=2/2` then as well. It now corrupts one link of the transformed field.

```bash
python3 -I tests/test_exact_su2_4d.py
```

Expected:

```text
EXACT_SU2_4D|sites=16|links=64|plaquettes=96|seeds=4|gauge_covariance=PASS|wilson_action=PASS|fault_controls=2/2|failures=0|json=0
EXACT_SU2_4D_VALUE|seed=20261103|S_W=449929987986/3508004825|json=0
EXACT_SU2_4D_VALUE|seed=1729|S_W=193195378719/1349232625|json=0
EXACT_SU2_4D_VALUE|seed=314159|S_W=185342826929127/1490902050625|json=0
EXACT_SU2_4D_VALUE|seed=271828|S_W=2969866827969/22936954625|json=0
EXACT_SU2_4D_CHECKER|one_link_fixture_S_W=18/5|wrong_plaquettes_detected=384/384|kept_the_trace=372|json=0
SCOPE|finite_periodic_lattice_only=1|continuum_existence=OPEN|physical_mass_gap=OPEN|json=0
```

**What remains OPEN:** finite-volume reflection positivity matched to the chosen precise setting, a rigorous RG transformation with uniform scale bounds, the nonperturbative continuum limit, OS/Wightman reconstruction, and an actual positive physical mass gap. These are separate claims in the proof-obligation ledger.
