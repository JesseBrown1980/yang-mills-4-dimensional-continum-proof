# YM4-WG09 research pilot — six-mode symmetry algebra

**21 November 2026. Status: exact structural calculation PASS; second-order coefficients, finite-beta spectral ordering, and continuum mass gap OPEN.**

This stage builds on WG06's continuous-SU(2) 42-state magnetic matrix, WG07's interacting physical six-state spectral cluster, and WG08's individual spatially symmetric Wilson-coupled eigenvector. It independently reconstructs the original L=2 24-link supports, 24 plaquette networks, 18 double-winding networks, 48 affine spatial actions, and first magnetic support adjacency.

## Three orbitals and three spectral characters

The induced 48-element action on the six first-order positive magnetic components is faithful. Its orbits on ordered pairs have sizes **6** (same component), **6** (opposite components), and **24** (different-axis components). Therefore every real symmetric six-by-six operator commuting with the group is uniquely of the form

    H = a I + b O + c X,

where O is the opposite-pair involution and X=J-I-O connects different-axis components. Its three invariant eigenvalues are exactly:

| Spatial symmetry class | Dimension | Eigenvalue |
|---|---:|---|
| Fully invariant | 1 | a+b+4c |
| Opposite-even, total-zero | 2 | a+b-2c |
| Opposite-odd | 3 | a-b |

The fully invariant mode is **strictly highest for this effective matrix exactly when c>0 and b+2c>0**. The result is a structural criterion, not a claim that the actual unknown second-order coefficients have those signs. The exact projectors are J/6, (I+O)/2-J/6, and (I-O)/2.

## Second-order candidate support count

For the two-magnetic-insertion term <phi_i, W_p W_q phi_j>, per-link fundamental SU(2) center parity requires

    mask(i) XOR mask(j) = mask(p) XOR mask(q).

The standalone integer routine counts ordered quadruples (i,j,p,q) between magnetic components. It finds **200 necessary-parity candidates** for each diagonal component pair and **32** for every off-diagonal component pair. These are **combinatorial candidates only**, not continuous-SU(2) Haar values or matrix-element signs. They show that the second-order candidate-support filter alone leaves both opposite and different-axis mixing available.

## Reproduction and acceptance boundary

Run:

    python3 -B tests/ym4_su2_six_symmetry_orbitals.py

It reconstructs the support graph from geometry instead of importing the preceding producers. Assertions check 48 first-magnetic edges, six K4,2 components, six isolates, 48 symmetry actions, group equivariance, three orbitals, opposite-pair involution, rank-1/2/3 eigenspace identities, and the exact parity counts. The deterministic result records **effective_b_c=OPEN**, **full_beta3_remainder=OPEN**, and **first_neutral_energy_order=OPEN**.

## Next mathematical calculation

Evaluate the genuine second-order SU(2) transfer/Feshbach coefficient within the six positive-slope modes, using the WG07 exact fourth-order Haar tensor and the **complete** electric-36, vacuum, and all-spin tail resolvents. Extract the two off-diagonal coefficients b and c with independent exact-integer/rational checking. Then obtain a certified order-three error small enough that both strict symmetry inequalities persist throughout a stated beta interval. Only then can the energy ordering of the WG08 Wilson-coupled individual eigenvector be promoted to the first neutral spectral level.

This draft is a verified **reduction of the next calculation**, not a WG09 final spectral-order certificate. Larger-volume weak-coupling and continuum Yang-Mills obligations remain open.
