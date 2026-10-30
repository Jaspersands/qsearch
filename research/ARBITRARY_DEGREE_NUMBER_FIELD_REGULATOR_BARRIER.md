# Number-Field Quantum Algorithms: False Barrier Retracted

Status: RETRACTED UNIVERSAL NO-GO; published constructive algorithms restored
to the usable research toolkit. Reviewed 2026-10-30. No new quantum algorithm
or implementation is claimed. `speedup_claim_allowed = False` and
`accepted_speedup_candidate = False` describe this repository contribution,
not a denial of the published quantum algorithms.

## What Was Wrong

The previous document claimed that growing field degree forces
`2^{Omega(n log n)}` quantum runtime for unit groups and principal ideals.
It called this formally proved without a formal proof and cited a paper
establishing the opposite result. The complete original registry record is
preserved, not rewritten, in `registry/quarantined_campaign_negatives.json`:

- ID: `NEG-ARBITRARY-DEGREE-REGULATOR-EXPONENTIAL-BARRIER`.
- Canonical SHA-256:
  `cd1ae36604d9f68eda100d19d07fc765df7cba283b3799b2cc651c4f221768f9`.
- Canonicalization: ASCII-default `json.dumps(record, sort_keys=True,
  separators=(",", ":"))`, UTF-8 encoded.

Only this individually reviewed arithmetic record is retracted here. Other
number-field and lattice records have not been certified or blanket-retracted.

## Published Constructive Baselines

1. **Unit groups, arbitrary degree.** Eisentrager, Hallgren, Kitaev and Song,
   STOC 2014, Theorem 1.2 (PDF page 3), give quantum time polynomial in degree
   and log discriminant. Their construction uses efficiently computed ideal
   bases and smoothed Gaussian lattice states, with a continuous-HSP oracle
   satisfying specified periodicity, Lipschitz and separation conditions.
   It does not merely enumerate a high-dimensional grid. Their input model
   includes an explicit integral basis/multiplication representation and
   controlled embedding precision. The output is approximate; it must not be
   silently equated with a list of fully expanded, potentially enormous units.
   [Primary paper](https://www.cse.psu.edu/~sjh26/units-stoc.pdf).

2. **S-units, principal ideals, class groups.** Biasse and Song, SODA 2016,
   Theorems 1.1--1.3 (PDF page 2), give polynomial-time quantum S-unit and
   principal-ideal algorithms with exact compact output. The PIP theorem
   includes degree, log discriminant and log ideal norm in the runtime.
   Theorem 1.2 for class-group computation explicitly assumes GRH; Theorem
   1.3 for PIP does not state that assumption. Their introductory prose is
   less precise, so use the individual theorem statements. Do not turn a
   compact arbitrary generator into a short generator without another
   theorem and its field/distribution promises. For a new reduction, prefer
   explicit maximal-order inputs; nonmaximal orders require their own
   representation and conductor analysis, not an automatic transfer.
   [Primary paper](https://fangsong.info/files/pubs/BS_SODA16.pdf).

3. **Detailed S-unit analysis.** Biasse and Song's 2025 manuscript supplies
   the oracle and precision analysis, compact recovery in Section 8.1,
   GRH-dependent class groups in Proposition 8, and PIP in Section 8.3,
   Algorithm 6 of v2 (Algorithm 4 is compact recovery). For PIP, factor the
   input ideal, compute units supported on its prime divisors, solve the
   integer valuation system, then assemble
   a compact generator. This does not require a factor base generating the
   entire class group. The class-group application does require its stated
   generation guarantee. The manuscript contains unresolved cross-reference
   and notation defects; this audit checks the scoped claims, not every
   displayed formula in that paper.
   Use **v2, 24 November 2025**, not the initially inspected v1 for cost
   formulas. V2 acknowledges that 2016 Theorem 5.1 and v1 Theorem 2
   displayed coefficient magnitudes instead of bit-size dependencies, which
   the authors describe as a typo. It corrects the formula and adds
   precision analysis in response to de
   Boer--Felderhoff. This audit records that correction, not a line-by-line
   independent certification of the revised proof or its concrete exponent.
   [Primary manuscript, corrected version](https://arxiv.org/abs/2510.02280v2).

The 2016 PIP theorem literally states orders, but its prime-factorization
reduction needs care for nonmaximal/noninvertible cases. The clean reusable
scope here is an explicit ring of integers and nonzero ideal with an
integral-basis representation; do not identify Z[theta] with that ring.

Classical **index calculus** remains a matched baseline for number-field
arithmetic. This note's link from the baseline catalog records the quantum
scope correction, not a proof that index calculus defeats these published
algorithms. Charge the particular classical algorithm's field-degree,
discriminant, smoothness and proof/heuristic assumptions separately. Neither
a classical upper bound nor a failed reconstruction is a quantum lower
bound. Do not reuse the old title as evidence for the retracted claim.

A subsequent exact example in INTEGRAL_SIMILARITY_OUTPUT_SIZE.md shows why
compact output is essential to downstream reductions: O(m)-bit 2x2 input
matrices can require Theta(2^m) bits for EVERY expanded integral conjugator.
This does not restore the retracted barrier or refute the decision primitive.
AMITSUR_ARITHMETIC_REUSE_AUDIT.md separately records a compact splitting
map and the distinction between a bad chosen output and a minimum-output
lower bound.

COMPACT_RESIDUE_CONDUCTOR_DECISION.md now proves a valuation-normalized
finite-residue interface for compact power products and applies the known
coprime-conductor principality criterion. It handles denominator factors
and ramification without expanding huge units. This supports a scoped
decision composition, not arbitrary compact circuits or expanded witnesses.

## Direct Errors In The Old Argument

These are independent mathematical checks, not benchmark-based conclusions.

- **Independent samples are not a lattice basis.** In `Z^2`, `(2,0)` and
  `(0,1)` are linearly independent but generate an index-two sublattice.
  Inverting their column matrix produces `(1/2)Z x Z`, not the dual of
  `Z^2`. Lattice generation, saturation and precision analysis cannot be
  replaced by the assertion that enough independent samples were collected.
- **Cardinality is not circuit cost.** An `r`-coordinate grid with `b` bits
  per coordinate has `2^(rb)` points, but its uniform superposition requires
  `rb` qubits and Hadamard gates. A tensor product of standard QFT circuits
  uses `r*b*(b-1)/2` controlled-phase gates, plus Hadamards and swaps, in an
  ideal rotation model. Fault-tolerant approximation adds precision cost.
  This disproves the cardinality-to-runtime inference; it does not establish
  any particular hiding function's efficient implementation or sampling law.
- **No hardness reduction was given.** Generic SIVP/CVP difficulty is not a
  lower bound for this structured reconstruction task. Even a valid
  NP-hardness statement would not unconditionally imply an exponential
  quantum runtime. An `n^{O(n)}` upper bound for one implementation cannot
  be promoted to a `2^{Omega(n log n)}` lower bound for every algorithm.
- **Precision must be proved, not guessed.** Large expanded unit coefficients
  explain compact representations, not an inevitable exponential overhead
  for manipulating compact representations.

The useful elementary structure survives: the logarithmic units form a
lattice, and its reciprocal characters matter. A regulator also depends on
the chosen embedding/measure convention; no conflicting determinant and
Euclidean-covolume normalizations from the old note are retained.

## Research Consequence

These are existing primitives. A valuable next contribution must construct
a new, efficiently represented native problem reduction to them, or a new
continuous quantum hiding map with proved access and separation bounds.
Reimplementing an already known unit-group algorithm is not a breakthrough.
Known polynomial quantum algorithms do not prove classical hardness or an
unconditional quantum/classical separation; no such classical lower bound
is established by this audit.

Before admission, a proposed reduction must specify field/order construction,
degree and coefficient growth, integral-basis access, ideal norm, precision,
compact-output consumption, and its strongest classical competitor. It must
not assume a hidden ideal, secret transporter, or a basis that solves the
original problem. These results do not automatically solve generic lattice
problems, arbitrary short-generator recovery, elliptic-curve torsors,
arbitrary tensor isomorphism, or arbitrary continuous HSP instances.

## Reproducible Scope

The existing hash-bound audit command performs the narrow quarantine:

```sh
python -m theorems.nonabelian_barrier_scope_audit --quarantine --write
python -m pytest tests/test_number_field_barrier_scope.py tests/test_nonabelian_barrier_scope_audit.py
```

The command name is historical; the sixth record has its own review path.
No quantum number-field solver is implemented by this correction. Retrieval
fixtures containing the old ID are historical retrieval checks, not valid
negative evidence; their queries should retrieve the quarantined record.

Primary PDF snapshots in `research/literature_cache/`, downloaded 2026-10-30:

| File | SHA-256 |
| --- | --- |
| `ehks_2014_units_stoc.pdf` | `c7667a168f429b1fba679ba8afaa12582cfda408298c6c23e7688b85bd178671` |
| `biasse_song_2016_sunits.pdf` | `4660348ea86809387b5d9047f782d928d0cc146a79181d07e926bc9a7fae7a15` |
| `arxiv_2510_02280v1.pdf` | `b10beca1c6b20b13a6f5df8be26fde1b67e41d77631fcfb9a1c2569e727bc2a0` |
| `arxiv_2510_02280v2.pdf` | `037f365f75cd9c8d00870fe20ca3d04a78c2b23831cf91e5b53d7d6c31d58a4a` |

The v1 snapshot is retained solely to make the audited version difference
checkable; v2 supersedes its cost formula.
