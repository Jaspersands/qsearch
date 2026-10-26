# Independent Hermite Module Certificate

2026-10-21. Exact finite certificates and a written general completeness
argument. This is not an external peer review, formal proof-assistant
verification, or a new quantum algorithm claim.

## Scientific Question

The compact decoder finds a short row in a polynomial interpolation module.
Checking that its output satisfies the interpolation equations is necessary
but does not prove that its maintained basis spans the full module.
Completeness is needed for the all-input guarantee that a sufficiently
short row exists in the computed basis.

For a particular received word, any already-verified short interpolant
still gives its own root guarantee even if a larger proposed basis is
incomplete. The issue is the uniform existence/computation theorem, not
automatic invalidation of every decoder output.

This pass constructs the same module by a different route, certifies its
codimension, compares bounded solution spaces against independent dense
equations, and checks the differential solver via direct polynomial
columns. The original producers and reports are unchanged.

## 1. Canonical Quotient Description

Let `F=F_q`, `h=ell-s`, `r=s+2`, and `M=(q-1)h`.
At each nonzero field point `a`, define local polynomials modulo `Z^h`:

    Y_(a,0)(Z)=1,
    Y_(a,j+1)(Z)=sum_(u<h) binom(j+u,j)*y_(a,j+u)*Z^u.

Let `P=product_(a!=0)(X-a)^h`, a monic degree-M polynomial.
By the Chinese remainder theorem, there is a unique polynomial `R_j`
of degree less than M whose local expansions match `Y_(a,j+1)`.
Then the interpolation module is exactly

    L = {Q in F[X]^r : Q0 + sum_(j=0)^s Q_(j+1)*R_j == 0 mod P}.

This is the kernel of a SURJECTIVE F[X]-linear map to `F[X]/(P)`:
the Q0 component alone reaches every residue. Therefore

    dim_F(F[X]^r/L) = M.

There is also an explicit triangular basis:

    ( P,     0, 0, ..., 0 )
    (-R_0,   1, 0, ..., 0 )
    (-R_1,   0, 1, ..., 0 )
     ...
    (-R_s,   0, 0, ..., 1 ).

Its determinant is P. To see spanning directly, subtract the rows
`(-R_j,e_j)` with polynomial coefficients Q_(j+1). The remaining first
component is divisible by P precisely when Q belongs to L.

The implementation constructs R_j by incremental CRT. If the current
modulus is P_old and the next point is a, calculate

    W_j(Z) = (Y_(a,j+1)(Z)-R_j(a+Z))/P_old(a+Z) mod Z^h,
    R_j <- R_j + P_old(X)*W_j(X-a).

The denominator has nonzero constant coefficient because previously
processed points differ from a. This is NOT the original producer's
discrepancy-update algorithm.

## 2. Checkable Completeness Criterion

Use the same shifts

    w0=-(K-1), w_(j+1)=-j.

Suppose a square polynomial matrix B passes three checks:

1. EVERY row satisfies EVERY local interpolation constraint.
2. The rows have distinct shifted leading positions, with largest column
   index breaking ties.
3. If delta_i are their shifted row degrees, then

       sum_i delta_i - sum_j w_j = M.

These checks certify that the row module of B is exactly L.

**Proof.** Distinct leading positions imply polynomial row independence.
In the determinant expansion the product of the leading entries has
degree `sum delta_i-sum w_j`. No other permutation can achieve that
degree: to use an equally weighted term to the right of any row's leading
position is impossible, while a nontrivial permutation cannot move every
selected position weakly left. Thus the leading determinant term cannot
cancel.

For a nonsingular polynomial matrix over F[X], the F-dimension of its
quotient module is its determinant degree. This follows, for example,
by diagonal reduction over the PID F[X]: multiplication by each nonzero
diagonal polynomial leaves a quotient with dimension its degree.

Let L_B denote B's row module. Check 1 gives `L_B subset L`. The exact
quotient sequence gives

    dim_F(L/L_B)
       = dim_F(F[X]^r/L_B) - dim_F(F[X]^r/L)
       = deg(det B) - M = 0.

Consequently `L_B=L`. No assumption about the algorithm that produced B
is used in this certificate.

Polynomial row reduction and predictable-degree arguments are established
tools; see [Mulders--Storjohann](https://cs.uwaterloo.ca/~astorjoh/jscpopov.pdf).
This is a problem-specific verification criterion, not a claim to have
invented a new normal form.

## 3. A Stronger Finite Cross-Check

For a certified weak-Popov basis, every vector has a unique representation
`Q=sum_i c_i B_i`. Its shifted degree is

    max_i (deg c_i + delta_i).

Indeed the largest shifted leading pair cannot cancel. Hence the exact
dimension of the module truncated at shifted degree b is

    H(b)=sum_i max(0, b-delta_i+1).

Independently construct a dense coefficient matrix for the original local
constraints, allowing component degrees at most
`b+K-1,b,b+1,...,b+s`. Its nullity must be H(b).

This checks the entire bounded interpolation space, not only the selected
short row. The diagnostic builds polynomial monomials, translates them,
multiplies by the local received polynomials, and extracts coefficients.
It does not call the original interpolation matrix or row-reduction code.

## 4. Deliberately Incomplete Basis

Multiply one row of a certified basis by `(X-a)`.
Every local equation remains valid, and the leading positions stay
distinct. But determinant degree increases from M to M+1.
The row module now omits one F-dimension of the true solution module.

The verifier rejects this basis with `DETERMINANT_CODIMENSION_MISMATCH`
even though `invalid_row_point_pairs` is empty.
Additional controls reject duplicate leading rows and corrupted local
equations. Recomputing the certificate from polynomial coefficients,
instead of accepting stored rank/degree flags, is essential.

## 5. Differential Solver Review

The production solver parametrizes a superset of solutions using its
nonzero descending pivots, and then imposes the residual equations and
pins. The independent checker instead forms the full polynomial columns

    L(X^t) = sum_(j<=t) A_j(X)*binom(t,j)*X^(t-j),

using FLINT polynomial operations. It extracts all coefficient rows,
appends independently expanded pin jets, and computes exact augmented
row reduction. It never calls `DescendingSystem.coefficient`,
`operator_matrix`, or the existing affine-system helper.

This detects disagreement in dimension, inconsistency, or a unique
solution. It retains the small-characteristic example `f'=0`, where
the degree-<K kernel has dimension `ceil(K/q)`, not one.
It also retains inconsistent high-degree equations and wrong pins that
would be missed by stopping immediately after nonzero pivots determine f.

The general correctness argument remains:

- Every genuine solution obeys the chosen nonzero-pivot equations.
- Descending triangular substitution includes every such solution.
- The remaining equations restrict, rather than expand, this parameter
  space.
- If reduced rank remains deficient, abstain.
- If it becomes full, reconstruct and recheck ALL original coefficient
  equations and pins, including unprocessed batches.

Thus early full rank does not authorize skipping consistency, and zero
pivots are not assumed to be genuine free solutions.

## Native Results

Same native input as the previous passes:
`q=31, ell=24, K=360, s=4`, source cap 8, guarded radius 10.
The CRT construction uses only the public syndrome-derived received word,
not the true errors, their supports, or the pin values.

- Six independent shifted leading pairs:
  `(11,5), (12,4), (13,3), (14,2), (81,1), (100,0)`.
- Sum of shifted degrees 231; sum of shifts -369.
  Certified determinant degree and required codimension both 600.
- The original incremental producer has the SAME leading-degree profile.
- At shifted bounds 37, 38 and 39, module dimensions and independent dense
  nullities are respectively 102, 106 and 110.
- Direct polynomial-column solving gives unpinned affine dimension one.
  The original eight pin positions give dimension zero for each of the
  two original errors sharing the syndrome.
- Both unique polynomials agree with the compact solver and its saved
  outputs. True errors are used only to construct and check diagnostic
  pin instances, not as arguments to either interpolation routine.
- Multiplying a row by `(X-1)` leaves all constraints valid but changes
  determinant degree to 601. The completeness certificate rejects it.

The dense matrices are independent diagnostics. Their storage does NOT
replace or strengthen the compact algorithm's workspace bound.
No quantum circuit was executed and no advantage follows from these
finite checks.

## Prior-Art Boundary

[Guruswami--Wang](https://arxiv.org/abs/1106.3951) already develops
linear-algebraic derivative-code decoding and noiseless side information
under a large-characteristic assumption. Do not claim either ingredient
as new.

[Fast multiplicity decoding, 2311.17841v4](https://arxiv.org/html/2311.17841v4)
also states the large-characteristic assumption for its near-capacity
guarantee. Its arbitrary-characteristic Johnson-radius result is a
different guarantee; it does not justify importing the small affine
dimension from the large-characteristic theorem.

Our proposal retains the larger `s*ceil(K/q)` solution-space bound and
uses true retained coordinate pins. Therefore it is NOT a solution to
ordinary small-characteristic list decoding without side information.
In particular it neither enumerates a small list nor proves one exists.

[Wu--Yang](https://arxiv.org/html/2610.01902v1) is the streaming problem
and quantum-composition source. The precise possible addition is
polynomial postprocessing at every fixed target below one for sufficiently
large fixed or growing multiplicity, paying logarithmic reversible
workspace overhead. All-multiplicity, ordinary OPI, exact-optimum, and
unrestricted runtime claims remain excluded.

No exact earlier match was identified in the targeted searches performed
for these passes. This is not an exhaustive novelty determination.

One tempting change was also checked: simply substituting folded
Reed--Solomon codes is not an unexplored general advantage mechanism.
Table 1 of the streaming paper already lists time and space advantages
for folded-RS codeword search, citing Yamakawa--Zhandry and
Goos--Gur--Jain--Li. That does not resolve this Hermite theorem, but a
plain code-family substitution is insufficient grounds for novelty.

## Decision And Remaining Risk

The central module-completeness concern now has a construction-independent
algebraic criterion and a native exact certificate. The compact solver's
coefficient equations also survive a separate implementation.

Remaining review must still connect the statements for ALL inputs:
small-characteristic pivot bound, independent-pin rejection probability,
guarded Fourier moments, and uniform reversible resource accounting.
The prior notes give written proofs; these checks are not a replacement
for outside review or machine-checked general theorems.

Do not add another generic audit subsystem or a larger native run.
The next substantive task is to state and verify explicit fixed-target
parameter ranges, then review the complete theorem as one argument,
including its classical comparison. Any attempted extension to ordinary
OPI needs a new mechanism, not a claim that extra multiplicity is free.

## Reproduce

    python -m theorems.hermite_module_certificate
    python -m pytest -q tests/test_hermite_module_certificate.py \
      tests/test_hermite_streaming_composition.py \
      tests/test_hermite_compact_decoder.py tests/test_hermite_pinned_decoder.py \
      tests/test_folded_rs_decoder.py -W error::RuntimeWarning

The artifact stores the full independent polynomial basis, not just a
boolean verdict, so its local and codimension checks can be replayed.
It also stores the received word and hashes its source fixture.

Verification: 9 new tests; 79 connected tests passed in 40.80 seconds
with runtime warnings fatal. Python and site JavaScript syntax, site
checks, registry validation, and whitespace checks passed. Full repository
tests were not run. Prior Hermite producers/reports are unchanged.
No central admission, qsearch/UI wiring, agents, commit or push.
