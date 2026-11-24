# YM4-VOL12 independent arithmetic and scope review

23 November 2026. Separate arithmetic reconstruction by the assistant; external mathematician signoff remains OPEN.

## Proof reconstruction

For E_S, the event that every link in a plaquette-separated packet S has a bad exterior, each bad star forces an incident plaquette deficit greater than epsilon/4. Because no two selected links share a plaquette, these are r distinct defective plaquettes. The Wilson action on E_S is at most 6V-r*epsilon/4. Product Haar probability is normalized to one, so the constrained numerator is at most exp(beta*(6V-r*epsilon/4)). The VOL09 continuous-SU2 all-link cap lower bound for the partition function is exp(6*beta*V-3V)*(1536*beta^(3/2))^(-4V). Dividing yields VOL12.1 exactly. No conditional independence is assumed.

## Independent BigInt reconstruction

A separate JavaScript BigInt calculation used direct integer multiplication and binary-string bit length. At beta=9^7=4782969, A=27*(1536*27^7)^4 has exactly 181 bits. The conservative margins floor(r*beta/128)-L^4*181 are:

| L | r=2 | r=4 |
|---|---:|---:|
| 3 | 60072 | 134806 |
| 4 | 28397 | 103131 |
| 8 | -666643 | -591909 |

These reproduce the local Python checker independently. Negative margins at L=8 ensure no inference of uniform finite-volume suppression at fixed beta.

## Review status

- Original continuous SU2 finite-volume analytical bound: DERIVED, pending outside mathematical review.
- Local Python normal and optimized byte replay: PASS. SHA-256 receipt: 3a253d1e7b9e20b05e12d8784688d9f89622ba25fb61a18770abc732ad6bb238.
- Independent BigInt arithmetic: PASS.
- Hosted CI, 3D atlas promotion, external signoff: PENDING.
- Volume-uniform joint bad-star activity, correlated exterior control, physical-size cube, all eleven continuum obligations: OPEN.

The next mathematical task is to localize the global partition-function prefactor. This is an elementary finite-volume pilot, with no first-in-literature claim. Related prior work: https://hexagonmath.org/2610.00341v7 .
