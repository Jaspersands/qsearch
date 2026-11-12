# Book Theorem 9.2.5: model-minimality guard

2026-11-12. Focused source check for the parent support-height work.
Source: `../sources/surface_module_2026/couveignes_edixhoven_book.pdf`,
printed pages 195-200, PDF pages 207-212. The relevant text is Section
9.2, beginning at physical newline-based line 9347 in the retained text.
No Git, network, API, paid-context edit, or full height-chain inference.
Commands used `/opt/anaconda3/bin/python` and newline-based line counting.

## Finding

Relative minimality is NOT stated explicitly in the local opening
hypotheses of Section 9.2. They say that `X -> Spec O_K` is a
"regular, split semistable curve", with positive-genus geometrically
irreducible generic fibre. However, the written proof of Theorem 9.2.5
uses properties of the relatively minimal semistable regular model.
A regular model which is merely reduced and nodal, in Javanpeykar's
broader semistability convention, cannot be substituted without a
separate repair or contraction argument.

Two places make this necessary:

1. Theorem 9.2.5, printed pages 199-200 / PDF pages 211-212, is deduced
   from the identity in Theorem 9.2.1 by discarding a term using
   `(omega_X/B,omega_X/B)>=0` (physical lines 9561-9563).
2. The proof of Lemma 9.2.6, printed page 200 / PDF page 212, says that
   `omega_X/B`, `D`, and `D_x` intersect EVERY fibre component
   nonnegatively (physical lines 9586-9587). Relative nefness of the
   dualizing sheaf excludes rational exceptional tails.

The PDF's Theorem 9.2.5 contains the term

```
-(1/2)*(D,D-omega_X/B),
```

with the MINUS sign. The text extraction loses that sign; this review
does not use the positive-sign transcription.

The book's global convention also points toward an implicit minimal
model: Chapter 4, printed page 92 / PDF page 104, says that after finite
base extension a positive-genus curve has a UNIQUE semistable arithmetic
surface (physical lines 4490-4498). Such uniqueness is false if arbitrary
smooth-point blowups of a nodal model are admitted. Either the book's
word "semistable" includes exclusion of rational tails, or minimality is
implicit in this discussion. The source does not justify interpreting
Section 9.2 as allowing arbitrary nonminimal nodal models.

## Decisive check on a nonminimal model

Let `X_min/O_K` be a split semistable minimal regular genus-one model,
and blow up a smooth rational point of one special fibre over `s`:

```
f:X' -> X_min,       exceptional curve E.
```

The resulting surface is still regular; its fibre is reduced with an
ordinary node between `E` and the strict transform. Thus it is
semistable in Javanpeykar Definition 2.2.1's nodal sense. Javanpeykar
Remark 2.2.2 explicitly recognizes this nonminimal example.
The standard blowup and adjunction formulas give

```
omega_X'/B = f^*omega_X_min/B + E,
(E,E) = -log #k(s),
(f^*omega_X_min/B,E)=0,
(omega_X'/B,E) = -log #k(s) < 0,
(omega_X'/B,omega_X'/B)
  = (omega_X_min/B,omega_X_min/B)-log #k(s)
  = -log #k(s) < 0.
```

The last equality uses the minimal semistable genus-one canonical
self-intersection, which is zero. This refutes both properties used
by the written proof when applied to arbitrary nonminimal nodal models.
It is NOT a counterexample to the final numerical inequality of
Theorem 9.2.5: the other terms also change under blowup, and a separate
extension of that inequality could still hold.

## Consequence for the parent construction

Javanpeykar Theorem 4.3.2 supplies the MINIMAL RESOLUTION OF THE
NORMALIZATION of the finite cover. This is minimal among resolutions
of that normal surface; it need not be the RELATIVELY MINIMAL regular
model of its generic curve. Nonexceptional rational tails may remain.
The two different minimality statements must not be conflated.

Before invoking the book's written proof, either:

* pass to the relatively minimal semistable regular model and account
  explicitly for the change in the closures/intersections of `D`,
  `D_x`, and `P` under the contractions; or
* prove a nonminimal version, retaining and controlling the relevant
  canonical/exceptional contributions rather than assuming them
  nonnegative.

The exact identity in Theorem 9.2.1 may be useful for such a repair.
For instance, a smooth-point blowup decreases `omega^2` and increases
the weighted node count by the same `log #k(s)`, so their sum is
unchanged. That observation alone does not repair Lemma 9.2.6's
componentwise-nefness step. No nonminimal extension or full support-
height bound is established in this note.
