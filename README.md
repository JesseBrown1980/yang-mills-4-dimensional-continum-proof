# Yang's Mills Four-Dimensional Continuum Proof

**Status: ACTIVE RESEARCH — NOT A SOLUTION TO THE FOUR-DIMENSIONAL YANG–MILLS EXISTENCE AND MASS-GAP PROBLEM.**

This is a separate, auditable research program toward rigorous four-dimensional pure Yang–Mills quantum field theory and a strictly positive *physical* mass gap. The initial concrete gauge group is **continuous SU(2)**, represented in small exact tests by rational unit quaternions. The official Clay problem concerns every compact simple gauge group and requires **both** a nontrivial quantum theory on four-dimensional spacetime **and** a mass gap.

**Official target:** [Clay Mathematics Institute — Yang–Mills and the Mass Gap](https://www.claymath.org/millennium/yang-mills-the-maths-gap/) and [Jaffe–Witten's formal problem description](https://www.claymath.org/wp-content/uploads/2022/02/MPPc.pdf).

## Separate from the finite-lattice programs

The existing [Yang–Mills / HEB-C repository](https://github.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C) develops finite S₃ lattice spectra, exact checks, 3×4 store-based certificates, and a two-dimensional quantum-double stability track. The companion [SU(N) repository](https://github.com/JesseBrown1980/Finite-Universe-SU-N-solved) investigates Q8, 2T, 2O, 2I and other finite models. These are valuable tests but **do not imply a four-dimensional continuum SU(2) theorem**: finite-group results cannot simply be promoted to continuous SU(2), and two spatial dimensions are not four spacetime dimensions.

This new repository starts with a **four-dimensional Euclidean SU(2) Wilson lattice construction** and a ledger of all remaining mathematical steps.

## First executable lemma

The initial reproducible control uses the periodic lattice `(Z/2Z)^4`, with 16 sites, 64 positively directed links and 96 oriented plaquettes. It represents SU(2) matrices by exact rational unit quaternions, including noncommuting elements. It checks gauge covariance and invariance of all Wilson plaquette traces and the Wilson action, and includes two deliberately failing controls.

Run:

```bash
python3 -I tests/test_exact_su2_4d.py
```

Expected receipt:

```text
EXACT_SU2_4D|sites=16|links=64|plaquettes=96|seeds=4|gauge_covariance=PASS|wilson_action=PASS|fault_controls=2/2|failures=0|json=0
SCOPE|finite_periodic_lattice_only=1|continuum_existence=OPEN|physical_mass_gap=OPEN|json=0
```

The exact check is a **standard finite-lattice algebraic fact**, not a novel continuum existence or mass-gap proof. Read [PROBLEM.md](PROBLEM.md), [docs/PROOF_OBLIGATIONS.md](docs/PROOF_OBLIGATIONS.md) and [Lemma 0001](docs/LEMMA-0001-GAUGE-INVARIANCE.md) for the proof and its scope.

## Research program

The required chain is **Euclidean Wilson lattice SU(2) → gauge-covariant multiscale renormalization → uniform nonperturbative scale estimates → infinite-volume and zero-spacing limits → nontrivial Schwinger functions with OS axioms → Hilbert-space reconstruction → strictly positive physical spectral gap**.

Each arrow requires its own proof and independently reproducible evidence. A positive gap in lattice units or at finite volume does not establish a continuum physical mass gap. The ledger explicitly marks PROVED, EXACT-TEST, DERIVED-CONDITIONAL, CONJECTURE, OPEN, FAILED and RETRACTED claims. No failed test is silently reclassified as a success.

Reference: Osterwalder and Seiler, *Gauge field theories on a lattice*, Annals of Physics 110 (1978), 440–471, [DOI:10.1016/0003-4916(78)90039-8](https://doi.org/10.1016/0003-4916(78)90039-8).
