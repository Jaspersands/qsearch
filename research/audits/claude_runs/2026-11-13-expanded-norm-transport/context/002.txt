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

