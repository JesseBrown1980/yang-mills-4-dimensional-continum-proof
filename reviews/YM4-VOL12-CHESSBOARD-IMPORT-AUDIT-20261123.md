# YM4-VOL12 independent chessboard-import audit and acceptance boundaries

**23 November 2026. AI assistant independent arithmetic/geometric reconstruction; external human referee and independent Lean kernel rebuild OPEN.**

## External theorem consulted

- [*Rarity of large plaquettes — the chessboard estimate*, Part 22](https://computoergosum.com/en/principia/yang-mills/22-01-rarity-by-chessboard.html), current public HTML chapter: stated original Wilson continuous-SU2 even-torus chessboard estimate, \`FoldMix.rarity_orient\` single-orientation extension, \`FoldMix.rarity_uniform_all_mix\` arbitrary-threshold six-orientation extension, and \`FoldCap.rarity_explicit\` numerical large-plaquette result.
- [Bhattacharjee et al., *One Cube Estimate Implies the Yang–Mills Mass Gap*, v7](https://hexagonmath.org/2610.00341v7), independent block-level context.

The source specifies the Wilson weight \`exp(beta sum_p Re U_p)\`, \`Re U_p=halftrace U_p\`, normalized Haar, **untwisted periodic even side L>=4** for the same-orientation mixed-site/midpoint reflections, gauge-invariant plaquette indicators, and
\[
Q=\exp[\beta(48a^2-y)]/h(a)^4
\]
as a one-orientation defect rate. It also notes that the broader chessboard strategy is classical reflection positivity / Peierls.

**Update — source successfully attested:** The published upstream archive (SHA-256 f8a444517b2f013a287ec20075977cb0afa71c019de2d3c3da577118c05aea62) was downloaded on hosted Actions; actual FoldChess/MixAllV1.lean:66–71 contains the complete FoldMix.rarity_orient proof statement with N=2m, m≥2, beta≥0, any y, radius r>0, one orientation and every Finset of sites. The archive's axioms.txt prints [propext, Classical.choice, Quot.sound], and its toolchain is Lean 4.33.1. See [new independent source attestation](YM4-VOL12-UPSTREAM-FOLDMIX-SOURCE-ATTESTATION-20261123.md) and [hosted SHA verification](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45173527653). The separate kernel rebuild and outside referee review remain OPEN.

## Independent implication proof audit

1. VOL09's quaternion inequality and VOL10 geometry imply each original 15-loop bad-star event contains at least one of six original plaquette-defect events \`1-W_p>epsilon/4\`. This is a deterministic statement under the *unmodified* Wilson measure.
2. If selected stars are independent in the original link graph, their selected incident plaquettes are distinct for **every** choice of one plaquette per star. There are at most \`6^r\` assignments.
3. All original plaquettes are partitioned into the six \`(mu,nu)\` orientations; every chosen \`r\`-tuple has at least \`ceil(r/6)\` in one orientation. Restricting the event to that one orientation and invoking external same-orientation activity gives \`P<=Q^ceil(r/6)\` for \`Q<1\`.
4. The union bound yields \`P(all r bad stars) <=6^r Q^(r/6)\` for all independent \`S\`. No Gibbs product independence, gauge fixing, or volume-dependent partition factor is assumed.
5. This fits the full quantifier order of the VOL10 joint hypothesis **on the restricted even L>=4 source family**, allowing its 18-degree independent-set combinatorics to produce the rooted island probability.

The improvement is a **new source-linked bridge for this project**; the reflection-positivity theorem itself is prior research and has published stronger plaquette-rarity statements.

## Second integer-only constant reconstruction

With \`epsilon=1/16\`, \`y=1/64\`, \`a=y/20=1/1280\`, Haar geodesic cap lower bound \`h(a)>=a^3/24\` and the exact exponent
\[
y-48a^2=1597/102400
\]
give \`A=(24*1280^3)^4\`, \`Q<A*2^(-N)\`, \`N=floor(beta*1597/204800)\`. At \`beta=531441\`, \`N=4144\` and \`A.bit_length=143\`. Therefore \`Q<2^-4001\`; \`6 Q^(1/6)<2^-663<18^-57\`. Direct BigInt exponent comparison also passes: \`6^6*A*18^342<2^4144\`; the left side has 1584 bits, leaving a 2560-bit conservative margin.

At \`beta=9^5=59049\`, \`Q<1\` but the conservative \`rho<=18^-57\` comparison **fails**. These assertions guard against conflating a one-defect tail with the much stronger cluster activity threshold.

## Acceptance and scope

- **CONDITIONAL MATHEMATICAL BRIDGE PASS:** from CB-ORIENT to joint bad-star activity and VOL10 root-island tail for even L>=4, beta=531441, epsilon=1/16.
- **INTEGER / ORIGINAL-LATTICE REPLAY:** L=3 negative scope; L=4,L=6 positive geometry; r=2,4,20 packet orientations; 143-bit cap constant, N=4144, 1584-bit threshold comparison.
- **EXTERNAL FORMAL SOURCE ATTESTATION:** source archive SHA, exact declaration, and published axiom record PASS; independent Lean kernel rebuild and human mathematical review OPEN.
- **ODD periodic volumes:** OPEN. **Fixed arbitrary boundary, twisted bundle, coarse-scale pushforward:** OPEN. **Physical-size cube and all eleven continuum obligations:** OPEN.
- **Continuum mass gap:** OPEN. No first-in-community novelty claim.

The correct next stage is to **audit the chessboard input independently**, then investigate whether its uniform one-scale island activity can be propagated through the explicit, boundary-aware multi-scale block conditions, rather than treating the finite-lattice result as a physical-scale Yang–Mills mass gap.
