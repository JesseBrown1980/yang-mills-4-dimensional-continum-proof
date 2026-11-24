# YM4-VOL13 — geometric bad-path crossings and reflection-compatible ternary blocking

**Status:** AI-written mathematical derivation, pending independent and external human review and hosted checker replay. Prediction frozen first at e20318f995bb4818ce8c6c343a1a8a947d68f3bd. Source: [VOL12](NOTE-YM4-VOL12-CHESSBOARD-BAD-STAR-CLUSTERS-20261124.md). All eleven continuum obligations remain OPEN.

## A. Fine paths

Let the fine torus have even side L >= 4 and use VOL12's original continuous SU(2) Wilson periodic equilibrium measure with beta >= 1 and 0 < epsilon < 1. Write rho for its rho_star. Vertices of the link graph are positively oriented fine links, and adjacency means sharing an original plaquette. Its degree is 18. The anchor is the initial site of a positive link. In each coordinate a graph step changes anchors by at most one in periodic distance, since anchors lie on the four corners of a common plaquette.

For a prescribed starting vertex, the number of self-avoiding paths of b steps (b+1 vertices) is at most 18*17^(b-1) for integer b >= 1: the first step has at most 18 choices and each subsequent step excludes at least the preceding vertex. Each path consists of distinct links, so VOL12-C bounds the probability that it is entirely bad by rho^(b+1). The path count and union bound need no independence.

## B. Block event and annulus

Let b divide L, M=L/b >= 6, and let coarse sites t have coordinates in (Z/M)^4. Define the core Q_t to contain fine anchors bt+[0,b-1]^4 and the halo H_t to contain anchors bt+[-b,2b-1]^4, with periodic coordinates. Define E_t as the existence of a self-avoiding all-bad fine path of b steps starting with anchor in Q_t. Its witness anchors stay in H_t by the step bound. The event uses bad labels of links with anchors in H_t; the underlying gauge variables determining these labels may extend beyond H_t. Disjointness below concerns witness links, not the gauge-variable sigma-algebras.

There are 4b^4 starting links. Thus

$$\mu(E_t)\le q_b=\min\{1,4b^4\,18\,17^{b-1}\rho^{b+1}\}.$$

A bad connected path from Q_t to outside H_t contains a self-avoiding path (erase loops) of at least b steps; its first b steps witness E_t. This bounds annulus crossings, including periodic wraparound, by q_b. The event E_t is deliberately stronger than crossing: a long path inside the core also qualifies.

## C. Joint coarse events

Assume additionally M is divisible by 3, and color coarse sites by their four residues modulo 3 (81 colors). Distinct sites of one color have disjoint halos: in at least one coordinate their coarse cyclic displacement is a nonzero multiple of three, and the length-3b intervals on that coordinate are disjoint. Periodicity preserves this argument because M is divisible by three.

For a set T of sites of one color, choose one b-step witness for each E_t. Their fine link sets are disjoint even when their underlying gauge variables are correlated. VOL12-C bounds the probability of every witness being bad by rho^((b+1)|T|). Taking the union over all witness tuples proves mu(all E_t, t in T) <= q_b^|T| (using the trivial bound 1 when the unclipped activity exceeds one).

For arbitrary finite coarse set S, choose a largest color class T in S. Its size is at least ceil(|S|/81). Thus

$$\mu(\bigcap_{t\in S} E_t)\le q_b^{\lceil |S|/81\rceil}.$$

This is an unconditional periodic equilibrium joint bound, valid even for neighboring or overlapping halos. It does not assert conditional mixing.

## D. Coarse islands and exact fixtures

Use the coarse adjacency graph connecting sites of cyclic coordinate distance at most one in all four coordinates, excluding the site itself. The maximum degree is 3^4-1=80. The rooted depth-first tour argument from VOL12 bounds connected m-sets by (4*80)^(m-1)=320^(m-1). With C_b(o) the connected component of sites satisfying E_t, empty when E_o fails,

$$\mu(|C_b(o)|\ge m)\le\min\{1,320^{m-1}q_b^{\lceil m/81\rceil}\}.$$

At beta=9^5, epsilon=1/16, VOL12 certifies rho<2^-18. With N_b=4b^4*18*17^(b-1), the integer bit length of N_b yields strict upper bounds q_b<2^-k_b, where k_b is 18(b+1)-bit_length(N_b).

| b | k_b |
|---:|---:|
| 3 | 51 |
| 9 | 128 |
| 27 | 372 |
| 81 | 1117 |
| 243 | 3364 |

At b=81, 1117 >= 81*13, hence the joint activity is at most 2^(-13m); 320<2^9 gives the uniform coarse island tail at most 2^(-4m-9). The graph and coarse labels are geometric and derived from the original fine measure at a single fixed coupling. No iteration of a transformed measure is needed for this estimate.

## E. Reflection-compatible straight-link map

For a coarse positive link (t,mu), define B(U)_{t,mu} to be the ordered product of b fine links along the coordinate segment from bt to bt+b e_mu. This map is gauge equivariant: the interior gauge matrices cancel, leaving only the endpoint action. For a coarse site reflection t_nu -> 2k-t_nu, use the fine site reflection x_nu -> 2bk-x_nu. Straight segments map to straight segments with orientation reversal and inverse product when mu=nu. Thus B intertwines the two reflections. Since M is even, closed coarse half-lattices have their boundary planes at fine site-reflection planes; a coarse link lying in a closed half has its whole fine path in that half. For any bounded real coarse half-observable F, its pullback F o B belongs to the fine closed-half algebra. Fine reflection positivity (Lemma 0004, Theorem 2, as used in VOL12-A) gives

$$\mathbb E_{B_*\mu}[F\vartheta F]=\mathbb E_\mu[(F\circ B)\theta(F\circ B)]\ge0.$$

Hence this particular pushforward inherits site reflection positivity at the aligned coarse planes. This argument composes for nested straight-link maps. It establishes neither a Wilson form for the induced action nor bounds on its couplings or on blocked bad-star probabilities. The checker verifies the underlying path identities and gauge-word cancellation symbolically, without sampling a continuous gauge field.

## Acceptance and remaining target

[Prediction](PREDICT-YM4-VOL13-GEOMETRIC-CROSSINGS-20261124.hbp) · [integer checker](../../tests/ym4_su2_vol13_geometric_crossings.py) · [expected replay output](YM4-VOL13-GEOMETRIC-CROSSINGS-20261124.hbp). The latter is an expected output, not an independently measured receipt until hosted replay passes.

VOL13-A–D are original-measure geometric statements; E is a pushforward positivity theorem. Odd sides, arbitrary-boundary conditioned estimates, renormalized action and small-field control, physical-scale clustering and continuum mass gap remain OPEN. VOL14 should study the actual induced action and its local small-field/correlation bounds, retaining the scope of the original-scale estimates.
