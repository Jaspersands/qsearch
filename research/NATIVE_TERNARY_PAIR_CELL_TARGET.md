# Exact Native Babai Coverage Target

LOCAL DERIVATION REVIEW PENDING. NOW IMPLEMENTED in
`theorems/ternary_pair_cell_coverage.py`; see `TERNARY_PAIR_CELL_COVERAGE.md`.
This targets the demonstrated missing two-witness coverage of
`TERNARY_PAIR_LATTICE.md`, not more blind restarts or bigger demo instances.

## Exact Recovery Predicate

For a FIXED public reduced row basis R with exact Gram-Schmidt rows R_i*, let
the integer lattice point of a valid word z be P=3E(z-z0). For its actual target
T=E(ones)-3E(z0), the residual is

```text
e=T-P=E(ones)-3E(z).
```

The particular coset solution z0 CANCELS. Thus the residual of a native word,
and its rounding-error predicate, do not depend on its target. Public fixed
center perturbations add the same known vector to e. The public basis may
depend on stripped labels and randomness, but not a hidden word or phase.

Define rho_i=<e,R_i*>/||R_i*||^2, with EXACT rational half-up rounding
round(x)=floor(x+1/2). Integer-translation invariance means that, conditional
on all higher rounding decisions equalling this word's true basis coefficients,
the required forced deviation at row i is -round(rho_i).

Therefore this word occurs in the COMPLETE current nearest-plane list iff:

- every round(rho_i)=0 (ordinary Babai); or
- exactly one is nonzero and it is+1 or-1 (one forced rounding deviation).

This is an IFF, not a sufficient heuristic margin. With two wrong rows, the
single-deviation list cannot return this word. A forced deviation at the one
wrong row restores the true higher-prefix condition, so recomputed lower
roundings all agree. Unique coefficients in the full-row-rank basis preclude
other paths returning the same point. At ties, -1/2 is inside the zero cell;
+1/2 is outside. Never replace this with symmetric floating tolerances.

## Coverage Without Enumerating All Targets

For each public basis/center, classify the original3^M words with this exact
predicate. Take the union across the FIXED full scheduled lists, then bucket
recoverable words by their original frequency. A target has pair coverage iff
its bucket has at least TWO DISTINCT recoverable words. Early exit on finding
two words does not change this event. This gives exact conditional uniform-
target coverage without running Q independent target decoders; it still costs
exponential3^M words and is an analysis tool, not a polynomial solver.

For a fixed label array let gamma be the recovered fraction of all original
words. Counting at least two words per pair-covered target gives

```text
beta_label <= (3^M/(2Q))*gamma = gamma/6 at the underfull scalar source scale.
```

This is a deterministic counting bound. Average over actual label arrays to
get a population bound only when gamma's population behavior is proved.
Uniform WORD samples measure word recovery, not uniform TARGET pair coverage.
Their targets are planted/size-biased. Keep them in a separate geometry probe,
never in the main uniform-target success denominator.

## Implementation And Falsification

1. Derive primitive INTEGER scaled GS directions from the exact Bareiss
   profile. Project native word errors using integer dot products and exact
   rational thresholds; no repeated huge Fraction arithmetic per word needed.
2. Prove predicate equivalence by full bounded word/list/coset tests including
   both half-cell endpoints, perturbations, multiple bases and duplicate paths.
3. Compute full-target coverage by this word predicate on affordable widths.
   Cross-check every target against the actual decoder, not only successes.
4. On larger widths, independently sample original WORDS for rounding-error
   count/magnitude diagnostics. Mark the diagnostic as a planted-word probe.
5. Analyze the source law of error projections and dependence across GS rows.
   Do not assume independent rounding errors, continuous-uniform cells, or
   independent coordinates after reduction. Constant covolume per dimension
   is not a coverage proof.
6. Test whether a bounded-error list width can stay polynomial while recovering
   two words on inverse-polynomial uniform targets. Prove useful bounds or
   register a narrowly scoped obstruction to this particular decoder family.

Likely failure: random one-hot cosets require many correlated rounding repairs;
enumerating all repairs becomes exponential. Counter-evidence would be an
actual source-law theorem concentrating errors into a constant number of
computable coordinates, with pair coverage and all work charged. The theorem
must survive fresh labels, uniform targets and adaptive-slice distribution
checks. Merely finding isolated low-error words is not enough.

No obstruction here would rule out arbitrary CVP algorithms, nonlinear native
processing, general joint POVMs, or the underlying quantum source family.
