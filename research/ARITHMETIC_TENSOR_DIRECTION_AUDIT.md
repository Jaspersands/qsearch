# Arithmetic Tensor Isomorphism: Constructive Baselines First

Date: 2026-10-30. Status: two-agent mathematical review, parent source check;
no new quantum algorithm, implementation, candidate or general lower bound.
Ordered tensor factors and the stated coefficient ring matter throughout.

Follow-up: UNMARKED_INTEGRAL_PENCIL_REDUCTION.md proves that, for degree
n>=3 irreducible pencils with a supplied source unimodular slice, the
unmarked GL(2,Z) layer is polynomial classical preprocessing to at most n
integral-similarity decisions. INTEGRAL_SIMILARITY_OUTPUT_SIZE.md proves
a separate exponential minimum-output bound for expanded conjugators.
Neither observation establishes new quantum advantage.

## Existing Quantum Result

Grochow, Qiao, Stange and Sun, STOC 2025, Theorem 3.7 (printed p. 781),
already place integer 2x2x2 tensor isomorphism decision in BQP via
real-quadratic principality decision. Definition 3.3 uses independent GL
actions, not factor permutations. The theorem does not impose primitiveness
or nondegeneracy; the overview treats square discriminants separately and
uses balanced oriented ideal triples for nonsquare discriminants. It also
mentions nonmaximal quadratic orders. The eight-page paper does not supply
the full reduction proof, orientation bookkeeping, reverse reduction or
transporter-output bounds. No longer proof was located in the checked
author listings. This is a limitation of this audit, not a novelty claim.
[Published paper](https://opus.lib.uts.edu.au/bitstream/10453/189641/2/3717823.3718286.pdf).

Local snapshot: `literature_cache/gqss_2025_tensor_rings_stoc.pdf`, SHA-256
`e117a57afb93b9ac3857b3af110092b3f374608d02d5c8a9da388d8c191a7b50`.

Do not infer an efficient explicit integral transporter from a decision
theorem. A correct extension must also survive the classical comparison.

## A Classical Algorithm For The Smooth 3x3x3 Promise

**Scoped deduction.** Given two integer 3x3x3 tensors T,U whose determinantal
plane cubics are smooth over the algebraic closure of Q, equivalence under
GL(3,Z)^3 is decidable, with a witness when one exists, in deterministic
classical time polynomial in their coefficient bit length. The constants
can be enormous. This is not an implemented or practical algorithm.

Smoothness means that `det(T(x,-,-))=0` is a smooth projective plane cubic,
not merely that all tensor flattenings have full rank. It is an effectively
testable fixed-format promise. Inputs of different smoothness cannot be
equivalent; singular inputs are outside the argument.

Bhargava--Ho, Theorem 5.1 and its stabilizer discussion, pp. 48--49, identify
the stabilizer of a nondegenerate tensor as finite modulo the scalar kernel
`K={(aI,bI,cI):abc=1}`. The finite part comes from 3-torsion and elliptic
automorphisms; exceptional j-invariants enlarge that finite part, not its
dimension. Corollary 5.4, p. 54, gives a genus-one curve/line-bundle/marked-
Jacobian-point description over fields. It is not an integral orbit
classification or an ideal-principality reduction.
[Primary classification](https://archive.intlpress.com/site/pub/files/_fulltext/journals/cjm/2016/0004/0001/CJM-2016-0004-0001-a001.pdf).

Here is the direct algorithmic deduction, avoiding any torsor-trivialization
or rational-point oracle for a positive-dimensional curve:

1. For each of the eight triples `epsilon in {+1,-1}^3`, introduce three
   3x3 matrices A,B,C and impose `(A tensor B tensor C)T=U` and the three
   separate equations `det A=epsilon_1`, `det B=epsilon_2`,
   `det C=epsilon_3`. There are 30 equations, degree at most three, in
   27 variables. Coefficient bit lengths are bounded by the input size.
2. If a branch has a geometric solution g0, its geometric solution set is
   a translate of `Stab(T) intersect SL(3)^3`. Intersecting K with SL(3)^3
   leaves `mu_3^2`, a finite group. Hence every branch is empty or
   zero-dimensional. Crucially, a constraint on the PRODUCT of the three
   determinants alone would leave the scalar torus and would not suffice.
3. Compute a rational Groebner basis. The number of variables and input
   degrees are fixed absolute constants. A degree bound depending only
   on those constants gives constant-dimension Macaulay linear systems
   with polynomial-bit entries. Thus exact rational linear algebra has
   polynomial bit cost in the input coefficient size. An enormous constant
   bound is acceptable for this asymptotic statement, not for a benchmark.
4. In the nonempty case construct the finite-dimensional Q-algebra
   `E=Q[variables]/ideal`. Its dimension is bounded by an absolute constant
   and its multiplication table has polynomial bit length. Compute its
   maximal ideals and residue fields. Keep the residue fields of dimension
   one over Q; their quotient maps give every rational solution, including
   when the coordinate algebra was not presented as reduced.
5. Retain solutions whose 27 coordinates are integers. Verify the original
   tensor identity and all three determinants exactly. Every integral
   transporter occurs in one of these branches and is returned. No search
   up to a guessed coordinate-height bound is used.

For Step 3, Dube's Theorem 8.2 / Corollary 8.3 (p. 773) supply the
degree bounds; homogenization uses 28 variables and dehomogenization
returns to the affine problem.
[Primary degree bound](https://cs.uwaterloo.ca/~r5olivei/courses/2025-spring-cs860/D90.pdf).
For Step 4, Lenstra--Silverberg, Theorem 1.10, gives a deterministic
polynomial-time maximal-ideal/residue-field algorithm for explicitly
represented finite-dimensional commutative Q-algebras.
[Primary algebra algorithm](https://arxiv.org/abs/1509.08843).

This is a proof-based baseline, not an inference from small examples. Two
independent agent reviews found no fatal gap in the scoped argument. No
external peer review, formal proof or large constant-size elimination was
performed. The fixed format and finite determinant-normalized stabilizer
are essential; this does not give a uniform polynomial algorithm as tensor
dimensions grow, or an algorithm for singular positive-dimensional branches.

## Why The Tempting Quantum Extension Is Weak

- A rational transporter is not an integral unimodular transporter. For
  primitive nonzero T, T and 2T are rationally equivalent but have different
  coefficient content, which GL(Z)^3 preserves.
- A Jacobian and marked Jacobian point do not identify the genus-one torsor
  or supply a rational point on it. Shor discrete logarithms on supplied
  finite-group points do not solve this rational-point problem.
- Conversely, torsor difficulty does not establish isomorphism difficulty.
  The finite-transporter algorithm above compares smooth tensors without
  trivializing their curves. In particular, T is equivalent to itself
  regardless of whether its curve has a rational point.
- Known quantum principal-ideal algorithms remain useful at growing field
  degree. The old repository claim excluding them was false; see
  ARBITRARY_DEGREE_NUMBER_FIELD_REGULATOR_BARRIER.md. But this does not turn
  every arithmetic orbit problem into a principal-ideal problem.

## Priority Decision

Do not build a smooth 3x3x3 Hallgren wrapper or promote it as a major
quantum-separation candidate. First inspect singular/positive-dimensional
stabilizer strata or growing-format arithmetic actions. A plausible next
question is whether a specified native integral orbit problem reduces to
commutative ideal equivalence with polynomial degree, order construction,
input height and output cost, without already being covered by existing
integral-matrix-similarity algorithms. Search that prior art BEFORE coding.

For every proposed extension, falsify either half independently: the
classical orbit problem may already be polynomial, or the putative quantum
oracle may require the unknown transporter. No new accepted candidate is
justified by the current comparison.
