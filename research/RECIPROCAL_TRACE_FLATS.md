# Reciprocal Trace: Constructive Classical Accepted Flats

2026-10-22. Local derivation, REVIEW PENDING. This adapts the repository's
accepted-flat baseline to the actual inverse-trace predicate. No claimed
asymptotic dequantization, hardness, novelty, or quantum advantage.

## Constructive Local Lemma

Let q=2^n. Fix any d-dimensional binary subspace V of F_q, of size
M=2^d<n. Choose a uniform translation a. If a belongs to V, reject this
trial; otherwise all z in A=a+V are nonzero. Solve, for lambda in F_q,

    Tr(lambda/z)=b  for every z in A.

These are M binary LINEAR equations in n bits. For b=0 a nonzero solution
always exists, since M<n. For b=1 full row rank suffices; consistency is
checked exactly, not assumed. A solution for b=1 is automatically nonzero.
Given a nonzero solution, A/lambda is an accepted affine flat:

    Tr(inv(z/lambda))=Tr(lambda/z)=b.

Multiplication by lambda^-1 preserves binary affine dimension. Enumerate
the M points and verify the ORIGINAL predicate at each. This is polynomial
in n because M<n; no field table or generic truth-table sampler is used.
The implementation uses the first d public basis elements for V, resamples
only its translation and the linear-solution choice, and caps attempts.
This does not change the given target or RS code.

## Why Local Construction Has A Guarantee

The M inverse points are binary independent unless some nonempty S subset V
has sum_(v in S) 1/(a+v)=0. Let P_S(T)=product_(v in S)(T+v). Then

    sum_(v in S) 1/(a+v) = P_S'(a)/P_S(a).

P_S is square-free, so its derivative is NOT the zero polynomial, also in
characteristic two. Its degree is at most |S|-1. On translations outside
V the denominator is nonzero. A union bound over all nonempty subsets
therefore bounds bad outside translations by

    sum_(empty != S subset V) (|S|-1)
      = (M-2)*2^(M-1)+1.

Including the M translations in V, one uniform trial fails the sufficient
independence test with probability at most

    min(1, [M+(M-2)*2^(M-1)+1]/q).

This is an analysis of the union, NOT an instruction to enumerate 2^M
subsets. The implementation checks rank with binary elimination. It can
also accept a consistent rank-deficient system, so the same failure bound
remains conservative. For M<=n/2 the bound is exponentially small in n;
d=floor(log2(n/2)) yields efficiently constructed logarithmic-dimensional
flats. At n17,d3 the exact bound is 777/131072.

Every b=0 system has a nonzero null vector. If the sampled linear solution
is zero, the code constructs one from a free column without uncharged
rejection sampling. A failed translation cap returns UNKNOWN, not evidence
that the original codeword problem is unsatisfiable.

## Compose With The Native Code

For each coordinate i independently construct a flat

    x_i=o_i+sum_(j=1)^d z_ij*v_ij,  z_ij in F_2,

inside the set Tr(inv0(x_i))=b_i. Substitute these expressions into the
ORIGINAL Hx=0 for the K-row Vandermonde matrix. This leaves nK binary
linear equations in Nd binary variables. Reuse restricted_system and
solve_binary from cubic_rs_affine_flats.py, then verify every native
field syndrome and every inverse-trace bit of the resulting witness.

Nd>=nK is necessary for FULL ROW RANK, not sufficient for it. Even full
row rank at some tested inputs is not a distributional or asymptotic
theorem. If the restriction is inconsistent, report failure only for
this product flat. The full native problem may still have many answers.
Do not import the earlier random-cubic flat-orientation theorem: the
inverse-trace predicate and scalar-normalized flat distribution differ.

## Fixed Counterchecks And Scope

Before execution, the two live cases were fixed at n17,d3 and n31,d4,
N=n^2,K=floor(N/8). Targets are b_i=popcount(i) mod2 and evaluation points
are the first N polynomial-basis labels. Attack seeds are 1000*n+22.
Inputs are not constructed from an output witness, retried on success,
or replaced when the attack fails. The report retains all local flats,
native witnesses or scoped failures, actual linear rank and source hashes.

Both fixed runs returned verified native classical witnesses. Observed ranks:
612/612 at n17 and 3720/3720 at n31. Every output is replayed a second time
using polynomial-basis binary multiplication, exponentiation and trace,
independent of FLINT's field operations and the original predicate helper.
The exact field modulus and the complete witnesses are retained. These
are two explicit inputs, not a claim about every target at these sizes.

At n17 there are 867 variables and 612 binary equations. At n31 there
are 3844 variables and 3720 equations. These are the same parameter
sizes as two earlier quantum failure certificates, although those
certificates apply to every target and do not specify this test input.
Classical witness construction here refutes using these finite sizes
alone as evidence of advantage; it does not refute the quantum theorem.

At n61,d5 the counts are 18605 variables and 28365 equations. Only this
count is recorded, not a global attack execution or a hardness result.
For fixed positive K/N, the guaranteed d=Theta(log n) eventually supplies
too few variables for full row rank. This does NOT exclude larger flats,
lucky consistent restrictions, target-adaptive choices, algebraic attacks,
or a different classical solver. It also does not establish inverse-trace
flat absence, which would require a separate theorem.

NEXT: evaluate target-adaptive constructions or a proven distributional
rank bound for this specific flat sampler, and investigate the known
low-degree inverse-trace annihilators noted in RECIPROCAL_AFFINE_PENCIL.md.
Do not run a broad seed campaign or build a decoder based only on failure
of these restricted classical attacks.

## Replay

`python -m theorems.reciprocal_trace_flats --write` writes
`research/classical_baselines/reciprocal_trace_flats.json`.
Tests: `tests/test_reciprocal_trace_flats.py`, alongside the existing
balanced-codeword, reciprocal-pencil and cubic-flat tests. No qsearch,
UI, central registry, Git, or background execution changes.
