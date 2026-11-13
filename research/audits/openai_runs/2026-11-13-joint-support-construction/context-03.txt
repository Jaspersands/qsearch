# Relative norm equations without a supplied normal closure

7 November 2026. Reviewed WRITTEN polynomial-BIT composition under explicit
GRH; core/source/endpoint review and exact classical control complete. The additional
Claude support attempt timed out without a report and is not evidence. No novelty, speedup, hardness,
integral solution, short solution or quantum execution claim.

## Selection and native contract

Start: STATE/TRAPS, corpus been-tried (one refresh; subsequent no-refresh),
primary literature, and corpus baselines. Compare three independent problems:

* General Galois-group computation: expanded polynomial input, permutation
  generators as output; coherent root-permutation tests might avoid closure
  construction, but no paid hiding function/receiver is supplied. Existing
  classical factoring/resolvent and permutation-group methods are the baseline.
  Polynomial quantum time is only a target; root alignment, coherent access,
  conditioning and total BIT cost are unpaid. A classical invariant matching
  the proposed test or exponential closure/precision would falsify admission.
* Arbitrary central-simple-algebra minimal modules: explicit structure
  constants, primitive idempotent as output; splitting A tensor A-op gives
  only the already available regular A-module. Classical maximal-order/local
  Schur-index methods remain relevant. No paid global minimal-module extraction
  mechanism is supplied. The known split-algebra quantum theorem does not
  establish this extension; local rank-one/global index mismatch is a falsifier.
* Relative norms: explicit arithmetic input and an exact verifiable compact
  output, with a specific support reduction and existing full relation routine.
  This removes a blocker to a complete native Diophantine solver, rather than
  adding a new arithmetic subsystem. Select this question for that reason.

Input: number fields K contained in L, degrees m=[K:Q], N=[L:Q], d=N/m,
explicit MAXIMAL-order integral bases and rational multiplication tables for
both fields, an explicit Q-linear embedding K->L, and an expanded a in K.
All data, degrees and coordinate bit lengths are charged. The embedding and
field/order promises are part of the input contract; no Galois closure,
units, class group, solution or factorization advice is supplied.

Optionally verify that the supplied embedding is unital and multiplicative
on basis pairs and that m divides N; these are polynomial exact checks.
The theorem is stated for the promised field/order input, not malformed data.

Output NO or x in L, represented as a polynomial-size signed power product
of polynomial-size expanded L-atoms with binary exponents, such that
N_(L/K)(x)=a. Correctness probability at least1-eta, time polynomial in the
explicit input and log(1/eta), assuming GRH for the fields specified below.
For a=0 return0; for d=1 apply the supplied embedding to a.

Intended advantage: a quantum polynomial-BIT upper bound using the known
complete S-unit primitive, avoiding a possibly factorial normal closure.
This is not a new quantum primitive or a proved classical separation. The
same support/coordinate reduction with classical S-units is the matched
baseline; retain index calculus and published relative norm solvers. Quadratic
relative norms also admit the stronger conic/quadratic-form comparison.

The actual Biasse--Song2510.02280v2 section8.6 directly states arbitrary
GALOIS L/K and identifies the normal-closure cost in the cited general method.
Simon2002 and Fieker--Jurk--Pohst1997 are prior relative norm algorithms.
Their full priority overlap is not settled by this statement or by abstracts.

## Relative support theorem

Reuse the exact rational support argument in TENSOR_SQUARE_RATIONAL_NORMS.md,
but use the etale K-algebra L tensor_K L = product_j E_j. Each factor carries
two embeddings iota_1,iota_2:L->E_j agreeing on K. For b in E_j*, put

    y_j(b)=iota_1^-1 N_(E_j/iota_1(L))(b)
            / iota_2^-1 N_(E_j/iota_2(L))(b).

Transitivity gives N_(L/K)(y_j(b))=1 IN K*, not merely after taking the
absolute norm. Keep both labelled embeddings, even for isomorphic factors.

Let S be rational primes containing all primes ramified in L, all primes
supporting a in K, and the rational primes below a class-generating set of
EVERY E_j. Then

    N_(L/K)(L*) intersect O_(K,S)^* = N_(L/K)(O_(L,S)^*).       (1)

Proof. For a prime q of K outside S, L at q is a product of unramified
extensions of K_q of relative residue degrees f_i. Tensoring any pair
gives gcd(f_i,f_j) copies of the unramified degree lcm(f_i,f_j) extension.
The difference of the two norm pushforwards of a prime in that factor is

    (f_j/gcd(f_i,f_j))e_i-(f_i/gcd(f_i,f_j))e_j.

ALL such pairs generate the full integer kernel of (f_1,...,f_r). For
g=gcd_i f_i, h_i=f_i/g and sum b_i h_i=1, any kernel vector z satisfies
z=sum_(i,j) b_i z_j(h_i e_j-h_j e_i); each term is an integer multiple
of the displayed primitive pair vector. No fixed-star or saturation shortcut.

If N(x)=a, its outside-S divisor belongs to that kernel at EVERY q.
Lift its finitely supported divisor to fractional divisors D_j of E_j by
these pair relations. Class generation gives S-supported A_j with
D_j+A_j=(b_j). Divide x by product_j y_j(b_j). This removes every outside-S
valuation and preserves its exact relative norm. Ordinary class groups
suffice: signs/archimedean phases cancel by norm transitivity itself.
Unknown x, its valuations, E_j and b_j are proof objects, never read by an
algorithm. Equation(1) does not substitute local solvability for global norms.

## Polynomial support, including nonrational targets

Every factor of L tensor_K L is a factor of L tensor_Q L. Indeed the former
is the quotient by all k tensor1-1 tensor k; the latter is finite etale, so
the quotient selects whole field factors. Thus the EXISTING absolute tensor
order discriminant bound applies without constructing a relative free order:

    log |D_Ej| <= 2N log |D_L|.

Take B0=48*max(1,2N*bit_length(|D_L|))^2, using the actual GRH class-generator
constant from Biasse--Song section8.2. Include every rational prime <=B0,
every divisor of D_L, and every divisor of c and |N_(K/Q)(c*a)|, where a's
denominator c is chosen so c*a lies in the supplied maximal order of K.
Using ONLY N_(K/Q)(a) is invalid: valuations can cancel over a rational prime.
All listed integers have polynomial bit length; Shor factoring is charged.
B0 is polynomial numerically, so its enumeration is a polynomial loop.
GRH is used for the auxiliary factor fields' class-generation bound even
though the algorithm never constructs those fields.

Decompose the rational S primes in the supplied maximal order of L using
finite-algebra factoring/radicals, not a bad-prime power-basis shortcut.
There are at most N primes over each rational prime, of polynomial norm bits.
Run the actual complete compact S-unit algorithm on this L and this list.
A finite-index independent list is insufficient. Its adjustable completeness
and compact-output bounds are inherited from the source, with finite clocks.

Adjoin the FULL roots of unity of L; using only -1 is insufficient for
relative norms. Reuse CYCLIC_SUPPORT_MONOMIAL_DESCENT.md's explicit classical
bounded cyclotomic-algebra procedure: order w<=2N^2, decompose L[T]/Phi_t
for t<=2N^2 using actual Lenstra--Silverberg Theorem1.10, retain linear-over-L
factors and choose a primitive root of maximum successful order. Degrees,
table sizes, exponent sizes and the enumeration are polynomial. This is an
existing classical interface, not a new number-field or root-search oracle.

For clarity, t succeeds iff L contains a primitive t-th root, equivalently
t divides w. Such a root is exactly a linear factor of Phi_t over L. The
factor's composite map from L is injective and has equal Q-dimension, so
rational linear inversion recovers that root in L. Restricting the loop to
phi(t) dividing N is safe and bounds each algebra dimension by N^2; the
unrestricted loop is also polynomial. Check Phi_t(root)=0 exactly.

## Exact relative norm coordinates and compact endpoint

Build an L/K vector-space basis by rational Gaussian elimination: greedily
add supplied L basis vectors until their products with a K-basis span L.
There are at most d chosen vectors. The resulting N-by-N rational matrix
and inverse have polynomial coordinate bit length by determinant bounds.
It converts each L multiplication operator to a d-by-d K matrix. Its
determinant computes N_(L/K)(beta) for an expanded atom beta in polynomial
BIT time, yielding an expanded K element of polynomial size.

Explicit BIT check: clear the polynomially many coordinate denominators of
the d-by-d K matrix. A minor is a sum of at most d! products of at most d
entries. If coordinate numerators and structure constants have at most B
bits, the integer numerator coordinates have O(d*(B+log m+log d)) bits
after including the common denominator's polynomial bit length in B.
Fraction-free elimination, or elimination with entries as ratios of minors,
therefore has polynomial intermediate sizes; exact K-division is an m-by-m
rational linear solve. No large compact norm is expanded.

For every compact S-unit generator u_j, retain its small atoms beta_l and
binary exponent column p_j. Include the torsion generator's atom. Compute
gamma_l=N_(L/K)(beta_l), keeping all atoms and their signs/phases; do not
drop factors outside S that later cancel. Adjoin a to the labelled tuple.

Actual LS1509.08843 Theorem1.11(i), field Proposition8.2, computes the FULL
integral relation lattice Lambda of (gamma_1,...,gamma_J,a) in K* in
deterministic polynomial BIT time. It takes expanded SMALL atoms, never the
large compact norms. Repeated labels are allowed. It retains torsion, so do
not replace Lambda by its saturation or by real logarithmic dependencies.

An explicit implementation can deduplicate equal atoms by exact coordinates,
compute the kernel for distinct elements and restore the labelled kernel
with equality relations e_i-e_j. Thus no convention about the word "system"
in LS is needed. Reject zero/malformed source atoms before any negative power.

For a basis matrix R of Lambda and unknown integer z,h solve

    sum_j z_j (p_j,0) - e_(J+1) = R h

by polynomial-bit HNF/SNF. If infeasible return NO; on the complete source
event (1) makes that a correct nonsolvability decision. If feasible return
x=product_j u_j^z_j, flattened to its original atoms and polynomial-bit
exponents. Exact lattice membership of its norm residual gives a classical
positive certificate, independently of GRH or S-unit completeness. The
verifier can recompute the atom norms and full relation lattice itself.

The polynomial size of a feasible integer solution is substantive. For an
integer matrix A of rank r, select r independent columns and r pivot rows;
their determinant Delta is nonzero. Multiplying any other column by Delta
puts it in the pivot-column integer lattice. Starting from any solution,
reduce its nonpivot coefficients modulo |Delta| and compensate in pivot
coordinates. Cramer's rule then bounds all remaining coordinates by minors
and the target. Hadamard bounds give polynomial BIT size. HNF/SNF finds a
solution in polynomial time; the proof does not enumerate these residues.

Allocate eta/2 to complete compact S-units, and eta/2 across initial factoring
and finite-field randomized subroutines. Cap all sizes/clocks; detected
failure is allowed within this error probability, never an unbounded retry.
Integer/rational algebra, torsion enumeration, LS and verification are
classical deterministic polynomial-time operations under their stated inputs.

Every reported YES has its deterministic exact certificate under the input
promises. All possible errors are false NO answers, including capped source
failure; no test of a returned finite-index unit list can certify completeness.

## Decisive falsifiers and open review items

A factor's two embeddings failing to agree on K; wrong relative residue
weights; lost integral saturation; target support inferred from absolute
norm alone; missing relative torsion; an implicit normal closure; large
expanded source units; or source completeness/bit precision not actually
provided would block the composition. First run PARI's existing rnfisnorm
on an exact nonrational-target example and verify relative determinants and
torsion. One finite control is a falsifier only, not evidence for all fields.

Primary-source scope, independent review, Claude dispositions and the exact
control will be recorded here before any result is accepted. No norm-solver
backend, registry promotion, broad suite or benchmark campaign is admitted.

## Classical control and source audit

`audits/controls/relative_norms/control.py/.json` runs the existing PARI
rnfisnorm baseline on K=Q(sqrt5), L=K(cuberoot2), and

    a=(40+17sqrt5)/(40-17sqrt5)=(609+272sqrt5)/31.

PARI returns an expanded witness in this small instance, whose exact
relative norm is checked. Independently, (2+sqrt5+cuberoot2)/(2-sqrt5+cuberoot2)
has norm a, as a three-dimensional multiplication determinant and after a
K-basis change. Norm_K/Q(a)=1, but valuations at the two primes above31
are -1,+1 and31 does not divide D_L=1458000. This is a decisive finite
counterexample to the absolute-norm-only support shortcut, which the theorem
already excludes. Clearing the coordinate denominator recovers31. In degree
2 over Q(zeta3), the relative norm of zeta3 is zeta3^2, not a rational sign.
This checks the need to retain full torsion without claiming to test all fields.
The first harness attempt used PARI's default shallow denominator operation;
its exact coefficient readback showed denominator31, and flag1 fixes the API
use. Final control PASS; no mathematical claim changed to obtain that result.

Actual BS source Theorem1, complete-generation Theorem5/Proposition2,
compact-output Proposition7 and sections8.2/8.6 were reused and independently
checked. Actual LS Theorems1.10/1.11 and field Proposition8.2 were read.
Their PDF hashes and the installed PARI help are recorded in
`audits/sources/relative_norms/source.json`. PARI's actual help retains its
normal-closure sufficient-support guarantee; this finite positive witness
needs no claim that its negative answer is complete at flag50.

Simon2002 full PDF fetch was denied at AMS and unavailable at the returned
mirror. Its abstract is not a substitute for its full theorems; priority/overlap
remain UNKNOWN. Parent rendered and read ORIGINAL thesis PDF pages67 and74
(the OCR is not symbol authority): CorollaryIII.2.7 uses relative class
conditions in the normal closure and its cyclic fixed fields; AlgorithmIII.3.1
and sectionIII.3.1 already reduce relative norms to S-units and integer
linear algebra. This is substantial classical prior overlap. The proposed
quantitative support reduction is the point requiring review, not that
established endpoint. These two pages are not an audit of the later paper
or a priority certificate. Fieker--Jurk--Pohst1997 is
retained as a prior-art lead, not an audited uniform polynomial competitor.
No missing source is used as a premise of the written support proof.

A further actual-source baseline is Kliuchnikov--Lauter--Minko--Paetznick--Petit,
[arXiv2203.10064v2](https://arxiv.org/abs/2203.10064), section6:
Problem6.1 is an INTEGRAL norm over K(i)/K; Definition6.2 requires cyclicity,
principal/norm-Euclidean orders, known unit generators and a unit-norm
surjectivity condition. Algorithm2/Proposition6.4 applies in that setting.
The earlier prose charges a factoring oracle; its Step2's practical candidate
rejection is not a worst-case factoring proof. This is a stronger classical
baseline on its promised special inputs, not a checked arbitrary-growing-field
solver and not a source of those promises for our native input.

## Independent review and Claude dispositions

The independent review `audits/reviews/2026-11-07-relative-norm-composition.md`
checks the full support, discriminant, source, coordinate and finite-clock
composition, including growing degrees and positive-verifier/NO asymmetry.
Parent checked its mathematical arguments rather than adopting its verdict.
Its zero-atom guard is integrated. Primitive pair vectors, full torsion and
nonsaturated relations remain essential; no new source promise was added.

Opus's completed compact-coordinate audit is saved in
`audits/claude_runs/2026-11-07-relative-norm-coordinates`, estimate USD0.312188.
Its substantive suggestions were checked: the relative K-basis uses rational
linear algebra; determinants require a minors BIT bound; cyclotomic factors
pay full torsion; duplicated atoms can be deduplicated with equality relations;
HNF witnesses have polynomial bits; all L-primes above S and full source
completeness are required. Explicit clarifications are integrated above.
The packet did not include field Proposition8.2, so Claude correctly declined
to audit that citation; parent and independent reviewer read the actual source.
Theorem1.11 itself suffices. Checking an already-promised embedding is optional,
not an extra mathematical input. The entire endpoint is classical; only
initial factoring and complete S-units supply the quantum dependencies.
The distinct Fable support attempt is terminal ReadTimeout with no report,
usage_is_partial=true and billing_status=unknown. Its USD0.006250 partial
counter is NOT its final charge; no retry or scientific finding is accepted.
No final claim is inferred from any agent label or control.

## Scoped milestone

2026-11-07: full dated review read; five source records (four PDFs and installed
PARI help) match their SHA256 values. Saved control PASS and false execution/
speedup gates checked. STATE full title/Now/table, handoff and mechanical entry
match. Two Claude calls terminal: one completed useful report, one ReadTimeout
with unknown billing and partial usage. No retry, live call or broad suite.
