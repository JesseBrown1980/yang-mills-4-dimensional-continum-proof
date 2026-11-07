# YM4-04 / YM4-06: what the power-of-three matrix jump actually establishes

**Status (2026-11-06):** The exact algebraic statements below are DERIVED. The executable exact-integer/rational controls are in [`test_triadic_physical_gap.py`](../tests/test_triadic_physical_gap.py) and are expected to print a separately archived HBP receipt. [Thirteen predictions](PREDICTION-YM4-04-TRIADIC-PHYSICAL-GAP-20261106.hbp) were frozen at Git commit `439f1b9365793825618e5c186d17e0e1defa62f7` **before code was written**. Neither the finite-universe Yang–Mills data nor the nanoparticle benchmark proves the Clay problem.

**Boundary:** This note is a **conditional mathematical bridge and a demonstrated obstruction**, *not* a four-dimensional construction. It connects the [finite S3 Hamiltonian](https://github.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C) and its [power-of-three matrix law](https://github.com/JesseBrown1980/The-matrix-law-essentials/blob/main/docs/LAW-POWER-OF-THREE-JUMP.md) to the requirements already listed in [PROBLEM.md](../PROBLEM.md). The reduced 2x2 transfer matrices below are **not** a substitute for the real SU(2) gauge-invariant transfer operator of [YM4-02c](LEMMA-0004-REFLECTION-TRANSFER.md).

## 1. The physical gap is not a gap in matrix steps

Take a spatial lattice spacing `a>0`, restoring `hbar=c=1` for the proof, and a positive transfer operator `T_a` with top eigenvalue `lambda_0(a)>0` and second physical excitation `lambda_1(a)>0`. Write

`q_a = lambda_1(a)/lambda_0(a)`, `0<q_a<1`.

One Euclidean-time lattice step has physical duration `a` in natural units. The physical energy difference is

`Delta(a) = -log(q_a)/a`.

Restoring dimensions gives `Delta_E(a) = hbar*c*Delta(a)` for spatial spacing `a`. A fixed-lattice certificate `q_a<1` is only `Delta(a)>0` for that lattice. In a continuum limit `a->0`, one needs a spacing-uniform positive lower bound on `Delta(a)`, along a justified coupling trajectory, for **every sufficiently small a**. One must also establish that the lowest excitation survives the relevant gauge-invariant coarse observables and that the limiting quantum field theory exists.

The exact time jump `T_a^(3^k)` changes the time *argument* of a fixed transfer operator. By itself it does **not** change `a`, `beta(a)`, or the underlying spatial-lattice Hilbert space.

## 2. Two exact rational counterfamilies, same finite-time jump law

Put `a_j=3^(-j)`, `K_j=3^j`, and use the symmetric positive matrix `T_j=diag(1,q_j)` for every integer `j>=0`. Each transfer matrix has a simple vacuum and a positive **finite-lattice** gap, and each is diagonalizable so `T_j^(3^k)` can be evaluated by exactly k cubings. These are test matrices, not an SU(2) gauge construction.

**Family A, nonzero physical gap:** `q_j=1/(1+a_j)=K_j/(K_j+1)`. Then `Delta_j=K_j*log(1+1/K_j)`. The elementary inequality `x/(1+x)<=log(1+x)<=x` for `x>=0` yields

`K_j/(K_j+1) <= Delta_j <= 1`.

In particular `1/2 <= Delta_j <= 1` at every j, and `Delta_j -> 1`. So this family really has a nonvanishing physical mass scale.

**Family B, physical gap vanishes:** `q_j=1/(1+a_j^2)=K_j^2/(K_j^2+1)`. Now

`0 < Delta_j=K_j*log(1+1/K_j^2) <= 1/K_j = a_j -> 0`.

Every finite member has a strictly positive spectral gap. Every finite member permits exact 3^k jumps. Yet **the physical gap tends to zero**.

Even the error in **one step of spatial blocking** becomes small. With `x=a_j^2` and j>=1,

`|q_j^3 - q_(j-1)| = | (6x-3x^2-x^3) / ((1+x)^3(1+9x)) | <= 6x=6a_j^2`.

Thus a series of numerically improving block matches and exact time jumps does **not** establish a positive physical continuum gap. Quantitative information on the actual SU(2) coupling flow and its lowest visible excitation is indispensable. This is the central registered negative control.

## 3. Three exact finite scales **can** agree, without a full continuum proof

Use only three spacings `a_f=1/9`, `a_m=1/3`, `a_c=1` with `q_f=1/2`, `q_m=1/8`, `q_c=1/512`. Then, as exact rational 2x2 matrices,

`T_f^3=T_m`, and `T_f^9=T_c`.

At physical times `t=1,2,3` the toy excitation correlation `C_a(t)=q_a^(t/a)` equals `(1/512)^t` at all three resolutions. The physical gap is identically `9 log 2` in all three scales. This is a **valid demonstration of exact temporal composition on a known preserved two-level mode**, not a proof that such a mode exists and stays visible throughout the unbounded SU(2) sequence of RG scales.

If a genuine family of transfer operators `T_a` possessed an isolated **same** gauge-invariant excitation at every spatial resolution and its eigenvalue ratios obeyed `q_(3a)=q_a^3` *for all sufficiently small spacings*, then `-log(q_(3a))/(3a)=-log(q_a)/a` exactly. This is a **conditional theorem**. To invoke it for four-dimensional Wilson SU(2), one must actually prove the blocking intertwiner and the excitation's visibility, rather than defining the coarse transfer operator to equal the fine power. Existence of the continuum field theory and all the Clay requirements remain separate.

## 4. The certified E9-E8 separation cannot be relabeled as the first excitation

The finite-universe repository reports a 3x4 S3 separation `E9-E8 >= 24.039673 J_E` at `r=9` (see its [README](https://github.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C/blob/main/README.md)). The rank labels matter: `E9-E8` is a gap **above an eight-state low-energy cluster**, not necessarily `E2-E1`, which is the first positive excitation energy above the ground state in a simple-vacuum model.

Our exact rational 10-level falsifier uses

`E1,...,E8 = 0, 1/K, ..., 7/K`,
`E9 = 94+7/K`,
`E10 = 95+7/K`, `K=3^j`.

Here `E9-E8=94` at **every** j, but the true first excitation is `E2-E1=1/K -> 0`. Thus even an arbitrarily large certified high-cluster separation does not alone bound the physical first mass gap. This does **not** dispute the repository's valid E9/E8 computation; it prevents the wrong inference.

S3 is also a finite non-simple gauge group and not SU(2). Its Hamiltonian has its own electric and magnetic couplings. Finite-group spectra and power-of-three operations do not automatically give the continuous SU(2) gauge-theory spectrum. Subgroup moment matching in [YM4-02b](LEMMA-0003-SUBGROUP-DESIGNS.md) is explicitly of bounded polynomial degree, and the continuum weak-coupling limit requires further uniform control.

## 5. The exact path to a Clay-level theorem

For each compact simple gauge group G (first demonstrate SU(2)), a candidate proof would need all of:

1. A correct four-dimensional lattice gauge theory, **gauge-invariant** transfer operator and observable algebra, with reflection positivity.
2. A well-defined gauge-equivariant block map over arbitrarily many scales (not only a single block), with controlled induced multi-loop couplings and errors along the weak-coupling trajectory `beta(a)`.
3. A **uniform physical** first excitation bound `Delta(a)>=m_*>0` for sufficiently small a and the relevant infinite-volume limit, with the spectral state visible to gauge-invariant observables. A finite `E9-E8` certificate is not such a bound.
4. A convergent family of renormalized gauge-invariant Schwinger functions, appropriate nontriviality, locality, clustering, Osterwalder–Schrader axioms, and reconstructed positive-energy Hilbert-space dynamics.
5. The appropriate all-groups extension and independent proof audit.

Your one-scale gauge blocking and finite transfer-gap results are appropriate **ingredients for attempting** item 2 and for formulating item 3. The nanoparticle `3^16` diagonal-phase calculation is evidence that some fixed operators can be jumped efficiently, not evidence that these 4D gauge-theory hypotheses hold.

This note discharges **one logic gate**: it proves the precise mathematical difference between finite-gap/jump correctness and a continuum physical mass gap, and states an independently testable sufficient *conditional* spectrum-preservation criterion. It does not close YM4-04, YM4-05, YM4-06, nor the Clay problem.

### Verification

```bash
python3 -I -X utf8 tests/test_triadic_physical_gap.py
python3 -I -X utf8 tests/test_triadic_physical_gap.py sabotage=drop_physical_a
python3 -I -X utf8 tests/test_triadic_physical_gap.py sabotage=misread_high_cluster
python3 -I -X utf8 tests/test_triadic_physical_gap.py sabotage=wrong_cube_block
python3 -I -X utf8 tests/test_triadic_physical_gap.py sabotage=fake_uniform_collapsing_gap
```

The normal test must exit zero. Each of the four sabotages must exit one with its **named** failure in the receipt. No binary floats, JSON output, or external Python dependencies. Every reported rational follows directly from integers and the Python standard-library `Fraction` type.
