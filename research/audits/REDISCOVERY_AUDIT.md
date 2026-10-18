# Rediscovery Audit

Generated 2026-10-19 by `tools/audit/rediscovery.py`; do not edit by hand.
Scope: the 976 records in `research/registry/negative_results.json`, grouped into
60 clusters by shared reasoning. A judge searched arXiv for each cluster's barrier
and labelled it; labels propagate from the members it read to the rest of the cluster.
"Published" requires a citation whose abstract contains the judge's quote verbatim.

## Headline

| Label | Records | Share of judged | Meaning |
|---|---|---|---|
| published | 309 | 32% | A retrieved abstract states the same barrier for the same problem setting; the records add at most instances. |
| adjacent | 452 | 46% | The technique or barrier is known, but in a different setting, or the literature only implies it. |
| not-found | 2 | 0% | No retrieved abstract states the barrier after a reasonable search. |
| unclear | 213 | 22% | The cluster is too heterogeneous or its records too terse to judge. |

Basis: 366 records were read by a judge; 610 inherited their cluster's label.

## By track

| Track | Records | Published | Adjacent | Not found | Unclear |
|---|---|---|---|---|---|
| Code equivalence | 457 | 37% | 31% | 0% | 32% |
| Coset observables / nonabelian HSP | 254 | 48% | 45% | 0% | 7% |
| Dihedral coset / hidden shift | 154 | 7% | 72% | 1% | 20% |
| Legacy toy oracles | 53 | 0% | 100% | 0% | 0% |
| Query lower bounds | 22 | 5% | 86% | 0% | 9% |
| Other | 17 | 12% | 53% | 0% | 35% |
| Applied-QC barriers from the literature | 11 | 45% | 0% | 0% | 55% |
| Lattices | 7 | 14% | 57% | 0% | 29% |
| DQI / OPI / prime characters | 1 | 0% | 0% | 0% | 100% |

## Ground truth

10 records restate textbook barriers and were chosen before judging. 7 of them came back published.

| Record | Known reference | Label | Verified citation |
|---|---|---|---|
| `NEG-BARREN-PLATEAUS-VARIATIONAL-QUANTUM-HORIZON` | Barren plateaus in parameterized circuits (McClean et al. 2018) and the Lie-algebraic variance theory. | published | 2312.09121 Does provable absence of barren plateaus imply classical simulability? |
| `NEG-BOSON-SAMPLING-PHOTONIC-LOSS-DEQUANTIZATION-BARRIER` | Classical simulation of lossy boson sampling (Oszmaniec and Brod 2018; Garcia-Patron, Renema, Shchesnovich 2019). | unclear |  |
| `NEG-CONTINUOUS-VARIABLE-GKP-NON-GAUSSIAN-BARRIER` | Efficient classical simulation of Gaussian and positive-Wigner circuits (Bartlett et al. 2002; Mari and Eisert 2012). | unclear |  |
| `NEG-LINEAR-CODE-EQUIVALENCE-WREATH-BARRIER` | Quantum Fourier sampling resists the code-equivalence HSP behind McEliece (Dinh, Moore, Russell 2011). | published | quant-ph/0501056 The Symmetric Group Defies Strong Fourier Sampling: Part I |
| `NEG-QAOA-BOUNDED-DEPTH-OPTIMIZATION-BARRIER` | Locality limits of bounded-depth QAOA (Farhi, Gamarnik, Gutmann 2020; Bravyi, Kliesch, Koenig, Tang 2019). | unclear |  |
| `NEG-QUANTUM-ERROR-MITIGATION-EXPONENTIAL-SAMPLING-BARRIER` | Universal sampling-cost bounds for error mitigation (Takagi, Endo, Minagawa, Gu 2022; Quek et al. 2022). | published | 2208.09178 Universal Sampling Lower Bounds for Quantum Error Mitigation |
| `NEG-QUANTUM-MACHINE-LEARNING-KERNEL-CONCENTRATION-BARRIER` | Exponential concentration in quantum kernel methods (Thanasilp, Wang, Cerezo, Holmes 2022). | published | 2208.11060 Exponential concentration in quantum kernel methods |
| `NEG-QUANTUM-SUPREMACY-RCS-ANTICONCENTRATION-BARRIER` | Polynomial-time classical simulation of noisy random circuit sampling (Aharonov, Gao, Landau, Liu, Vazirani 2022). | published | 2211.03999 A polynomial-time classical algorithm for noisy random circuit samplin |
| `NEG-STRONGLY-COSPECTRAL-QUANTUM-WALK-BLINDNESS` | Quantum walks fail to distinguish strongly regular graphs (Smith 2010; Gamble et al. 2010). | published | quant-ph/0501056 The Symmetric Group Defies Strong Fourier Sampling: Part I |
| `NEG-SYMMETRIC-GROUP-KRONECKER-RACAH-BARRIER` | Limits of Fourier sampling over S_n for graph isomorphism (Moore, Russell, Schulman 2005; Hallgren et al. 2006). | published | quant-ph/0501056 The Symmetric Group Defies Strong Fourier Sampling: Part I |

Records that cite an arXiv id themselves (ids were hidden from the judge):

- `NEG-COSET-TYPICAL-FIXED-SOURCE-CATALOG-COVERAGE` cites 2605.25995: retrieved by search yes, cited by the judge yes, label adjacent.
- `NEG-DCP-QUERY-SFT-ACCESS-TRANSFER` cites 1607.01842: retrieved by search yes, cited by the judge yes, label adjacent.

## Spot check

A fresh reviewer re-read 30 randomly chosen judged records with their label and citations and agreed with 27 (90%). By basis: propagated 16 of 18; shown 11 of 12.

| Record | Basis | Cluster | Assigned | Reviewer |
|---|---|---|---|---|
| `HS-DEQUANTIZED-QUADRATIC_CHIRP` | shown | C14 | unclear | label=adjacent; The record is clear: a quadratic-chirp hidden shift is recovered classically from an explicit evaluator, because the shift difference is a linear phase. This is known for Boolean quadratic/bent hidden shifts (2408.02778, folklore O(n)-query attack); a chirp is a neighbouring setting. |
| `NEG-COSET-STABLE-LEAKAGE-AS-SINGLE-COMPLEMENT-REPAIR` | propagated | C06 | adjacent | label=not-found; The record's barrier (leakage spreads over every character-allowed complementary sector, so one extra intermediate partition cannot close the associator) differs from the cluster's spectral-gap/circuit barrier. No cited abstract states it or clearly implies it. |
| `NEG-DCP-QW-HISTORY-INDEPENDENCE-AS-REGEV-COMPOSITION` | propagated | C08 | published | label=not-found; Mis-clustered. The record is a DCP/quantum-walk interface gap (walk-internal history independence does not certify the outputs Regev's reduction needs), not symmetric-group Fourier sampling. The cited S_n abstracts do not address it. |

## Review queue

Clusters a human should check first: published, adjacent or unclear labels, lowest judge confidence first.

| Cluster | Records | Label | Confidence | Barrier | Citation |
|---|---|---|---|---|---|
| C07 | 26 | adjacent | 0.45 | In multiregister coset-state measurements for the symmetric-group/wreath-product hidden subgroup problem (graph-isomorphism or code-equivalence type), trivial and sign representation components give common subspaces shar | quant-ph/0612089 |
| C05 | 29 | adjacent | 0.50 | The dihedral coset problem supplies only i.i.d. uniformly random Fourier labels on possibly faulty coset states, so shortcuts needing chosen or correlated queries (sparse/significant Fourier transforms, chosen-multiplier | quant-ph/0302112 |
| C15 | 22 | adjacent | 0.50 | A fixed finite span of low-support conjugacy-class (orbit-average) operators has degenerate spectrum on some Kronecker multiplicity spaces, so it cannot uniformly resolve those spaces as n grows; resolving them needs gen | 1911.11649 |
| C38 | 13 | adjacent | 0.50 | In Regev's subset-sum-measurement template for the dihedral coset problem, fixed- or sub-logarithmic-order moment and correlation statistics of low-bit-conditioned density-one modular subset-sum fibers retain no persiste | 2609.40062 |
| C47 | 8 | published | 0.50 | Code pairs claimed to be hard non-equivalent instances are actually equivalent, as an exact classical canonical-form check (matching basis-normalized column multisets) shows. Classical code-equivalence algorithms decide  | 1111.4382 |
| C58 | 6 | adjacent | 0.50 | Classical post-processing of independent single-register dihedral coset (DCP) samples with linear, fixed-degree product or U-statistic estimators of coarse Fourier buckets runs into a Parseval/variance bound that forces  | 2206.14408 |
| C01 | 53 | adjacent | 0.55 | Speedup claims for ad hoc oracle secret-finding problems backed only by tiny (N=3) custom-oracle simulations, with no successful runs and no natural scalable family, give no evidence of an asymptotic quantum speedup; gen | 1401.2910 |
| C09 | 26 | adjacent | 0.55 | Splitting the optimal joint measurement on several symmetric-group coset states into local pairwise (pair-carrier) measurements fails because the shared hidden label correlates the registers and overlapping isotypic proj | quant-ph/0501066 |
| C21 | 19 | published | 0.55 | Graph-isomorphism instances built from Cai-Furer-Immerman (CFI) constructions over small base graphs are not evidence for quantum coset-state advantage, because they are solved classically by Weisfeiler-Leman with indivi | 2107.03778 |
| C23 | 19 | adjacent | 0.55 | Dihedral-coset relation finding needs coherent preparation or transport of subset-sum solution superpositions (fiber states), which is as hard as average-case subset sum and state generation of the index-erasure type. Fi | 1608.02003 |
| C28 | 16 | adjacent | 0.55 | Collisions of coordinate or tuple weight-profile invariants between small random codes turn out to be genuinely equivalent codes that classical canonicalization or support-splitting-style invariants resolve, so they are  | 1111.4382 |
| C33 | 15 | adjacent | 0.55 | Partial structure for density-one modular subset sum (polynomial-size representations of the low-order bits, finite-size algebraic fits of carry or 2-adic lifting predicates, or reduction to a relation-solving interface) | 2002.05276 |
| C39 | 12 | adjacent | 0.55 | Building the pretty good measurement (inverse square root of the frame operator) for multi-copy wreath-product/symmetric-group coset states requires controlling every irrep-tuple sector, including correlated multi-copy b | quant-ph/0501066 |
| C46 | 8 | published | 0.55 | In the code-equivalence hidden subgroup problem the hidden subgroup is determined by the code's permutation automorphism group, so instances cannot be assumed rigid (order-two hidden subgroup); coset-state no-go results  | 1008.2390 |
| C51 | 7 | adjacent | 0.55 | In the code-equivalence hidden subgroup formulation over GL_k x S_n, the GL_k row-scrambler factor is removed classically by putting generator matrices in canonical (reduced row echelon) form, so a high-rate gap in scram | 1008.2390 |
| C53 | 7 | adjacent | 0.55 | Self-dual codes have hull equal to the whole code, so hull-based local signatures from puncturing and shortening (the invariants behind support splitting and trivial-hull reductions to graph isomorphism) are forced and u | 1905.00073 |
| C60 | 5 | adjacent | 0.55 | Hidden-shift problems for explicitly described low-degree algebraic functions over finite fields (traces of low-degree rational functions, Kloosterman-type families) are classically solvable, because a few evaluations yi | 1502.06631 |
| C06 | 27 | adjacent | 0.60 | Exact spectral data (characteristic polynomials of a Racah/recoupling operator) on symmetric-group coset states does not by itself give an efficient collective measurement; a spectral gap, an efficient coherent circuit f | quant-ph/0609138 |
| C12 | 23 | published | 0.60 | Structured code families (cyclic, Goppa/alternant, Tanner) proposed as hard code-equivalence instances are resolved or reduced by classical structural invariants (low-weight codeword/matroid structure, closures, support  | 1111.4382 |
| C14 | 22 | unclear | 0.60 | Heterogeneous grab-bag of claimed quantum advantages that vanish under classical baselines: hidden shifts of explicitly given bent or quadratic functions are recoverable classically, and NISQ proposals (noisy random circ | 2408.02778 |

## Clusters

| Cluster | Records | Main tracks | Label | Top terms |
|---|---|---|---|---|
| C01 | 53 | Legacy toy oracles | adjacent | speedup, simulation, evidence algorithmic, simulation cap, tiny, tiny custom |
| C02 | 34 | Code equivalence, Coset observables / nonabelian HSP, Dihedral coset / hidden shift | unclear | count, finite control, count finite, control, theorem count, control count |
| C03 | 30 | Code equivalence | unclear | count, tail, theorem count, theorem, count tail, log2 |
| C04 | 29 | Coset observables / nonabelian HSP, Code equivalence, Other | published | involution, hidden involution, hidden, decoder, outcome, involution decoder |
| C05 | 29 | Dihedral coset / hidden shift, Lattices | adjacent | dcp, label, reflection, bad, log, labels |
| C06 | 27 | Coset observables / nonabelian HSP | adjacent | stable, separation, root separation, normalized, gap, racah |
| C07 | 26 | Code equivalence, Dihedral coset / hidden shift, Other | adjacent | common, norm, frame, orientation, block, exact |
| C08 | 26 | Coset observables / nonabelian HSP, Dihedral coset / hidden shift, Code equivalence | published | different, independent, justified routes, reject specified, architecture different, specified architecture |
| C09 | 26 | Coset observables / nonabelian HSP, Code equivalence, Other | adjacent | carrier, pair, label, multiplicity, source, local |
| C10 | 24 | Dihedral coset / hidden shift, Lattices, Coset observables / nonabelian HSP | unclear | polynomial, legal, coverage, inverse, inverse polynomial, solver |
| C11 | 24 | Code equivalence | unclear | count, theorem count, control count, validation failure, validation, theorem |
| C12 | 23 | Code equivalence | published | code_low_weight_structure low, matroid equivalent, equivalent control, weight matroid, code_low_weight_structure, matroid |
| C13 | 23 | Coset observables / nonabelian HSP, Dihedral coset / hidden shift, Code equivalence | published | omega, log, mutual information, mutual, omega log, bits |
| C14 | 22 | Applied-QC barriers from the literature, Dihedral coset / hidden shift, Code equivalence | unclear | quantum, classical, advantage, quantum advantage, time, attacks |
| C15 | 22 | Coset observables / nonabelian HSP, Code equivalence | adjacent | multiplicity, targets, blocks, exact, multiplicity blocks, transposition |
| C16 | 21 | Code equivalence | published | canonicalization, code, code equivalence, equivalence, row, set canonicalization |
| C17 | 21 | Code equivalence, Coset observables / nonabelian HSP, Other | adjacent | endpoint, polar, normalization, metric, addressed, sqrt |
| C18 | 20 | Query lower bounds, Coset observables / nonabelian HSP, Other | adjacent | source, mask, review, review pending, pending, physical |
| C19 | 19 | Coset observables / nonabelian HSP | published | cfi, gadget, cfi gadget, gadget promise, promise, parity |
| C20 | 19 | Coset observables / nonabelian HSP, Other, Query lower bounds | unclear | fixed, character, centralizer, weighted, negative character, fixed point |
| C21 | 19 | Coset observables / nonabelian HSP | published | cfi, structural cfi, tensor, dequantized, row, wl |
| C22 | 19 | Coset observables / nonabelian HSP, Code equivalence | adjacent | source, typical, mass, partitions, support, coefficient |
| C23 | 19 | Dihedral coset / hidden shift | adjacent | source, coverage, relation, fiber, source coverage, verified |
| C24 | 18 | Code equivalence | unclear | count, component, theorem count, count natural, theorem, control |
| C25 | 18 | Code equivalence, DQI / OPI / prime characters | unclear | count, theorem count, theorem, edge theorem, edge, control |
| C26 | 17 | Coset observables / nonabelian HSP | adjacent | observable, tensor, cycle, nonclassical, vs, wl |
| C27 | 17 | Code equivalence | unclear | count, theorem count, theorem, control, control count, failure count |
| C28 | 16 | Code equivalence | adjacent | profile, profile collisions, collisions, tuple profile, collisions far, far |
| C29 | 16 | Code equivalence, Dihedral coset / hidden shift, Coset observables / nonabelian HSP | adjacent | polynomial, normalization, spectral, generic, pgm, encoding |
| C30 | 15 | Code equivalence | published | code, information set, set, supplies hard, collision supplies, profiles |
| C31 | 15 | Code equivalence | published | code, support splitting, splitting, weak, code equivalence, equivalence |
| C32 | 15 | Code equivalence | published | exact dual, weight incidence, dual weight, schur hull, goppa, incidence |
| C33 | 15 | Dihedral coset / hidden shift | adjacent | solver, carry, high, witness, quotient, geometry |
| C34 | 15 | Code equivalence | unclear | count, pressure, margin, stored, failure count, failure |
| C35 | 15 | Code equivalence | adjacent | cyclic, quasi cyclic, quasi, cyclic tuple, tuple profile, profile collision |
| C36 | 14 | Dihedral coset / hidden shift, Lattices, Code equivalence | adjacent | marker, coverage, affine, source, marker aware, plane |
| C37 | 13 | Code equivalence | published | controls, rows, code baselines, collapse standard, rows provide, standard code |
| C38 | 13 | Dihedral coset / hidden shift, Code equivalence | adjacent | moment, order, subset, bad, fixed, signal |
| C39 | 12 | Code equivalence | adjacent | equal, unequal, moment, equal pair, sectors, commutator |
| C40 | 10 | Coset observables / nonabelian HSP | published | involution ensemble, ensemble, route, involution, copy, explicit collective |
| C41 | 10 | Coset observables / nonabelian HSP | published | distinguishability, pgm, pgm capacity, level coset, representation decoder, size measurement |
| C42 | 10 | Query lower bounds | adjacent | query, sample, lower, decoding, shift, lower bound |
| C43 | 10 | Coset observables / nonabelian HSP | published | row column, weak fourier, irrep, bias, fourier irrep, irrep labels |
| C44 | 9 | Dihedral coset / hidden shift | adjacent | low degree, audit record, use family, shift evidence, record identify, hidden shift |
| C45 | 8 | Code equivalence | published | closure, polynomial time, time, powers algebraic, minor invariant, separates code |
| C46 | 8 | Code equivalence | published | rigid order, hsp, rigid, rowspace, instance, order |
| C47 | 8 | Code equivalence | published | column multiset, normalized column, multiset, multiset exact, equivalence witness, column |
| C48 | 8 | Code equivalence | adjacent | hull, self dual, self, define coordinate, hard self, codes collision |
| C49 | 8 | Code equivalence | published | schur, filtrations, shortening filtrations, puncture shortening, powers local, apply primal |
| C50 | 7 | Dihedral coset / hidden shift | adjacent | recoveries, recoveries random, tested, random sample, access, complexity evaluator |
| C51 | 7 | Code equivalence | adjacent | row scrambler, scrambler, high rate, opening, gl_k, rate |
| C52 | 7 | Code equivalence | adjacent | sufficient, apply, dimension, closes self, hypotheses failed, theorems checking |
| C53 | 7 | Code equivalence | adjacent | rank hull, puncture shorten, shorten, shorten rank, forced, hull profiles |
| C54 | 6 | Coset observables / nonabelian HSP | published | recovers, graph, cfi, legal, legal graph, legal regular |
| C55 | 6 | Code equivalence | published | cfi, cfi_code_reduction faithful, reduction cfi, cfi_code_reduction, promise dequantized, dequantized code |
| C56 | 6 | Code equivalence | published | isomorphism style, rigid, graph isomorphism, isomorphism, style, hsp |
| C57 | 6 | Code equivalence | published | stratum, rigid, hsp, instance, structure hsp, obstruction stratum |
| C58 | 6 | Dihedral coset / hidden shift | adjacent | margin, retry, bucket, dcp, buckets, kernels |
| C59 | 5 | Code equivalence | published | incidence isomorphism, proof debt, debt, isomorphism, incidence, proof |
| C60 | 5 | Code equivalence | adjacent | natural trace, trace family, trace, hidden shift, shift, trace function |
