# YM4-04C E1 / C03 — exact closed-polymers through 12 plaquettes

**2026-11-11. Scope:** complete finite C03 class-root enumeration through n=12 on periodic 4D fine tori N=8 and N=12. Two separately written implementations, full closed-set SHA-256 membership cross-check, all six hosted jobs, exact counting-gap tests and three seeded faults. This is a **reproduction** of the existing prediction row C03 tagged `prefreeze=CROSS_READ`, not a new blind prediction. It is **not** a weak-coupling or continuum Yang–Mills theorem.

## Definition, geometry and completeness

Take the fine lattice `(Z/NZ)^4` with positive oriented link `(x,mu)`. An off link has nonzero number `c(x,mu)` of odd transverse coordinates. The off support of each positively oriented plaquette consists of its 2 or 4 non-line links. Two plaquettes are adjacent exactly when they share an off link. A polymer is a **connected** subset of plaquettes in which *every off link that occurs is incident to at least two plaquettes of the subset*. C03 counts distinct subsets holding a fixed off link w, without dividing by a symmetry factor. One representative per class c=1,2,3 is used; the class-representative reduction rests on Lemma 3.14 from the unchanged frozen note, separately checked in earlier E0/G-attack material.

The Python and Rust programs independently rebuild **all** positive plaquettes on each lattice, each link's face incidences and each off-neighbourhood. Every original positive link touches six faces and every plaquette has exactly four distinct links. The off-face adjacency degree is 10 or 20, matching `5 * |off(p)|` throughout the full lattice.

**Exhaustiveness argument for the closure-guided recursion:** Begin with each of the six faces containing the fixed seed off link w. For any partially grown connected P contained in a target closed connected S, if P contains an off link with multiplicity one, closure of S guarantees a further face of S through **the lowest such link**, and this face is adjacent to P. If P already has no singly occurring off link but is a proper subset of S, connectedness guarantees a face of S outside P sharing an off link with P; the implementation explores **all** those faces. Therefore every target S has at least one complete search path. The only feasibility pruning is `number_of_singletons > 4*(12-|P|)`: every remaining face can cover at most four previously single off links, so no target of size ≤12 could have been lost. Canonical sorted face-ID tuples deduplicate exact partial states; all closed states are saved and sorted for a deterministic SHA-256 of the entire closed-set membership collection. The Rust implementation uses its own incidence construction and a full-equality hash set (hash collisions cannot silently merge unequal subsets).

## Computed refined coefficients — identical at N=8 and N=12

| Number of plaquettes n | Class 1 | Class 2 | Class 3 | Valid head N(n)=max |
|---:|---:|---:|---:|---:|
| 4 | 1 | 0 | 0 | 1 |
| 5 | 0 | 0 | 0 | 0 |
| 6 | 12 | 12 | 12 | 12 |
| 7 | 0 | 0 | 0 | 0 |
| 8 | 32 | 12 | 0 | 32 |
| 9 | 32 | 12 | 0 | 32 |
| 10 | 304 | 240 | 216 | 304 |
| 11 | 284 | 244 | 228 | 284 |
| 12 | 2326 | 1640 | 1242 | 2326 |

For each N and class, the two routes agree on the complete count vector, exact number of visited subsets at every size, and the **SHA-256 of every closed sorted face set**. The totals of visited exact partial sets per class are respectively 4,598,910; 4,343,327; and 4,615,510. The six separate source-pair receipts and manifests are stored in `evidence/`. The source SHA freeze `c74e6388295a6309674268dd18deba3728a4eb627a1530c42054182b2fadc404` from original commit `6ebf63272ae230bfb08ef48b3156cb4202c24627` is reproduced byte-for-byte as the first 42 frozen prediction rows.

The growth control uses exact `F_20(n)=binom(20n,n)/(19n+1)` and checks `6 F_20(n)/N(n)` lies in the frozen strict brackets: for n=8, between 1.09×10¹⁰ and 1.10×10¹⁰; n=10, between 2.31×10¹² and 2.33×10¹²; n=12, between 6.49×10¹⁴ and 6.50×10¹⁴. It also checks `N(10)/N(8)=19/2`, `N(12)/N(10)=1163/152`, with the frozen F20 ratio intervals.

## Evidence and mandatory release gates

All six hosted shards run the Python enumeration AND native Rust 1.81 strict Clippy for the same lattice and root class. They compare counts, per-order state totals and exact closed-state membership SHA-256. The workflow also runs the whole-repository strict no-float source gate, three fail-closed planted errors (missing a root face, skipping connected extensions of already closed sets, and a forged n12 count), and the post-six-shard Fuss–Catalan fan-in. It now **requires** every committed evidence file to regenerate byte-for-byte, with no optional missing-receipt route.

**Unresolved:** The row C03 and the valid head N(4..10) are now reproduced as finite data. The G0/G1 induction gate, the KP search from these precise heads (C05/C06/C14), the original separate evidence-list review PR #45 and its inherited `no-float-list-unchanged` hold, the complete E0–E9/W workflow and weak-coupling continuum construction remain OPEN. No r=9 blind run was launched. Leave this PR as DRAFT until independent proof/code review and evidence-list approval; do not merge from CI alone.
