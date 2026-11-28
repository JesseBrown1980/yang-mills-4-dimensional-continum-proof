# Review 15 source inventory

Follow-up to review 14 by Claude (AI), 27–28 November 2026: coarse gauge dependence of the D3 relative floor and a non-Abelian adversarial search. The floating-point scripts and the result file are kept in the project and conversation attachments, outside this proof tree. No gate exception.

| Original attachment | SHA-256 |
|---|---|
| 15-GAUGE-DEPENDENCE-OF-THE-RELATIVE-FLOOR-2026-11-27.md | b5d04928cb31f7773ce75f3d4e248b5eab66fb485b198433efa560c4fb69ef54 |
| 15-bgH.py | 699b87946839a60d025d6e1582229fcaf0bfc266a8646a8f4c646536dee68663 |
| 15-m2_check.py | 034ef9b10ceb69832acf1dcc9a9f39965351c991d69751053414a81cae733577 |
| 15-jaug.py | 6eac9530879322a5a465763bb605f02f28b6f1d32595df43e275c5cf74a6aabc |
| 15-jaug_check.py | cf89b08316b5365689b76fb2bde8b9a592b6ed921355c354f64eed61442beaa4 |
| 15-gauge_dense.py | 1f1a36519efbd352707dbdfb297a2468c7472e0046f2844ad5fcc19442d7b743 |
| 15-gauge_verify.py | 0c34ea1dddc4f5a7b5a90d69ef3252e65e55390206c6fd9c4f3601463c4487e4 |
| 15-gauge_on_field.py | 2e9ca8f09a77f9dc38c3d85f6a3147f9da259cf7cc02acb532bcb6b42cbff970 |
| 15-search.py | 0b9d0bd0dc74acadaf69d1fe710cfad29d1ddd5e7a89715f4c77cb0be65dfe77 |
| 15-nl_eval.py | e72ad162a5bc362d75966cfd2b5799292b8278a659a518fdb70c89d3e822a56f |
| 15-gauge_opt.py | a081380a28eb4b013bfea36ab7effa02f390a4ff65f1ea1909b0694ec2af1512 |
| 15-results.json | d91cbe4206498eee757d0ae1b95d34dbfe7067564e474d6e732e530f059f09cf |

`15-bgH.py` is review 09's operator module with a one-line change reading the coarse torus size from `YM_MC` (default 4). `15-jaug.py` needs JAX 0.4.38 with 64-bit floats and `15-search.py` needs cvxpy with the Clarabel solver. Floating-point results are exploratory, not certificates. Only the review text and this inventory are committed.
