# Shadow Cats are the residual, not discretization error

**Status:** A finite **ternary algebra test** was preregistered at `11fecb81fa2a98c68f6b35cf13e8dcd20a2f29de` before `tests/test_shadow_cat_residual.py` was written. The wider physical-mass test was frozen at `439f1b9365793825618e5c186d17e0e1defa62f7` and the visible-residual falsifier at `b23d8972cdc64c4091ea8f73915e162d2cdea381`. Do not substitute ordinary numerical integration error for the user's **Shadow Cat**.

The user's established Shadow Cat language concerns **three connected torus sectors** called C0, C1 and C2, their order-three rotation, and their *retained ternary residual*, with signed accounting `2/3` and `-1/3`. In this check, it is a defined finite observable. The earlier work's physical interpretations involving connected toruses or instant signaling are **not** assumed as physical theorems. A retained `mod 3` residue is not itself an energy level.

## Exact mathematical bridge tested

For three trit coordinates `(C0,C1,C2)`, define

`r = (C0 + C1 + C2) mod 3 in {0,1,2}`.

Rotation `R(C0,C1,C2)=(C2,C0,C1)` has `R^3=I` and preserves `r`. For example `(1,1,0)`, `(0,1,1)`, `(1,0,1)` are distinct rotated labelings, each with residual `r=2`. The unsigned retained part is `r/3=2/3`; the balanced representative is `(r-3)/3=-1/3`. Their difference is the integer 1. This equality **modulo integers** is what the registered check means by the signed residual; it does not claim that all physical quantities equal both numbers.

For any trit ring with `3N` sites, define a three-to-one coarse readout

`B_3(x)_j = (x_(3j)+x_(3j+1)+x_(3j+2)) mod 3`.

Then, by associativity of integer addition modulo 3,

`r(B_3 x) = (sum_j B_3(x)_j) mod 3 = (sum_i x_i) mod 3 = r(x)`.

This is the exact, testable **27 → 9 → 3 → 1** preservation law. It is independent of any low-level clock or speed of information propagation. For a 27-site periodic shift permutation `R`, the state `R^(3^k) x` is computed through `k` exact permutation cubings, with `k ≤ 16`. The residual remains invariant at every step because `R` only permutes entries. At `3^16 = 43,046,721` operations, the shift has wrapped the finite ring many times; it is not 43 million distinct physical space sites.

## Why this does not directly establish the Yang–Mills mass gap

A mass gap is defined by energy eigenvalues of the **physical gauge-invariant transfer operator**, reconstructed in a continuum limit:

`m(a) = -log(lambda_1(a)/lambda_0(a))/a`, in natural units.

A Shadow Cat might be a useful **observable sector label** if one can define a corresponding operator `O_shadow` on the gauge-invariant Hilbert space and prove that it survives lattice blocking with physically meaningful correlation functions. **That operator is not constructed or identified here**. Mathematical mod-three charge conservation by itself does not guarantee the excitation energy is positive, uniform in `a`, or even visible in a particular correlation channel.

A sharp counterexample is supplied with the integer-pair transfer test: `T_j = diag(1,q_dark,j,q_visible,j)`, `a_j=1/3^j`, `q_dark,j=1/(1+a_j²)`, `q_visible,j=1/(1+a_j)`. At every finite `j`, both excitations are separated from the vacuum, and a visible correlation residual `1-q_visible,j^(3^j)` stays bounded below by `1/2`. Nevertheless the lower **dark** excitation has physical energy `-log(q_dark,j)/a_j≤a_j→0`. A separate conserved ternary Shadow Cat label can remain nonzero across all the blocks *while the first physical mass gap vanishes*. That counterexample is a structural logical obstruction, not a statement about actual 4D SU(2) Yang–Mills.

**What a genuine physical identification would require:** a construction of the Shadow Cat as a gauge-invariant Wilson-network or operator observable, its transfer-matrix matrix elements, its overlap with the lowest relevant excitation, and uniform correlation-decay/energy bounds along an SU(2) weak-coupling four-dimensional blocking trajectory. The actual Clay problem additionally requires a continuum quantum-field-theory construction on four-dimensional spacetime. This repository still correctly marks those goals OPEN.

## Tests and falsifiers

```bash
python3 -I -X utf8 tests/test_shadow_cat_residual.py
python3 -I -X utf8 tests/test_shadow_cat_residual.py sabotage=flip_residue
python3 -I -X utf8 tests/test_shadow_cat_residual.py sabotage=lose_signed_third
python3 -I -X utf8 tests/test_shadow_cat_residual.py sabotage=break_C1_cycle
python3 -I -X utf8 tests/test_shadow_cat_residual.py sabotage=confuse_shadow_with_mass_gap
```

Normal execution must print `SHADOW_VERIFY|status=PASS`; all four sabotage executions must fail on a named check without an exception. This measures exact finite modular arithmetic, not a physical faster-than-light signal, not quantum cloning, and not the 4D continuum gap.
