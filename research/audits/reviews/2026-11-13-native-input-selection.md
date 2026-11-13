# Two native-input candidates: neither selected

13 November 2026. STATE/TRAPS read first; corpus been-tried and baselines
queried before proposal. No network, API, Git, tests, or shared-status edits.
**Recommendation: zero new operations for paid dispatch.** The two problems
below have external motivation and explicit classical input. The first
repeats an identified conditioning problem; the second has a complete
same-output classical sampler. Neither conclusion is a general quantum
lower bound or a claim that all useful endpoints in its domain are solved.

## 1. Boolean algebraic root recovery through an implicit Macaulay inverse

**Input/output.** Explicit sparse rational quadratic equations in n Boolean
variables, with polynomial-size coefficients and a promise of one Boolean
solution; return that solution and verify it exactly. This is a natural
algebraic cryptanalysis/constraint-solving endpoint. No solution state,
quotient basis, condition bound, or inverse oracle is supplied.

**Proposed operation and target.** In C[x]/(x_i^2-x_i), index squarefree
monomials by n-bit subsets. All monomial multiples of the equations form
an implicit sparse matrix; a quadratic term has only constantly many
preimages under squarefree multiplication, so both row and column access
are polynomial from the native input. Fix the constant monomial to 1,
solve the remaining linear system coherently, and extract the root from
its monomial moments. A polynomial(n,inputbits) clock would be substantial.
The exponential matrix dimension alone is not the obstruction.

**Cheapest exact falsifier of the bare inverse claim.** Take x_i-1=0,
i=1,...,n. Discard zero rows and retain each nonzero multiple once. The
homogeneous matrix is the oriented incidence matrix of the n-cube:
rows are e_(S union {i})-e_S, i not in S. Deleting the constant column
gives the grounded incidence matrix A. For y equal to 1 on every nonempty
subset,

    ||Ay||^2=n,   ||y||^2=2^n-1,
    sigma_min(A)<=sqrt(n/(2^n-1)),
    kappa(A)>=sqrt((2^n-1)/n).

A has full column rank, since a function constant on cube edges and zero
at the empty vertex is zero. Also sigma_max(A)>=1, which proves the stated
condition bound. Thus a uniformly polynomial inverse clock is already
false on an explicitly classically easy family. This is not a statement
about every preconditioner. Moving instead to assignment coordinates makes
the diagonal constraint Hamiltonian have gap 1, but projection of the
uniform assignment state onto its unique ground state succeeds with 2^-n.
That specific replacement transfers the cost to overlap.

**Baseline/disposition.** Gaussian elimination solves the displayed family.
F4/F5, XL, Boolean SAT, and specialized cryptanalytic methods are the real
comparators for the full input class. The corpus already points to
EXPLICIT_QUADRATIC_OPI.md LF20–23 and arXiv:2111.00405 for conditioning
limitations, and DCP_BINARY_ERROR_SOURCE_BRIDGE.md LF136–139 rejects rank
alone as a quotient solver. The primary 2111.00405 theorem was not imported
here: the cube calculation is independent. A source-priority check would
read it alongside Chen--Gao's Boolean-equation algorithm. No new source-
valid preconditioner AND root-readout operation survived this screen;
requesting another unspecified condition-number theorem is not a proposal.

## 2. Matroid topology through its sparse integral-spectrum Laplacian

**Input/output.** An explicit matrix over Q or an explicitly represented
finite field defines a rank-r matroid M on n columns. Return the normalized
top reduced Betti number beta_(r-1)(IN(M))/#bases to additive epsilon with
failure probability eta, or sample the normalized full top-Laplacian
spectral distribution to TV epsilon. Matrix entries and field arithmetic
are charged. Delete loops by rank tests and thereafter use n for the
remaining ground size; rank 0 is the trivial one-state case. No independence,
uniform-basis, or spectral oracle is an input.

**Quantum mechanism considered.** The top Laplacian is boundary-adjoint
times boundary on the basis-indexed chain group. Its diagonal is r and
its off-diagonal entries are signs for single-element basis exchanges;
row sparsity and rank-test access are polynomial. Kook--Reiner--Stanton
(KRS), Corollary 17, actually proves integral spectra, so its positive gap
is at least 1 before polynomial normalization. Sampling a basis and then
spectrally filtering could estimate the normalized zero multiplicity.
The hoped-for gain is avoiding an exponentially large chain matrix, with
polynomial(n,inputbits,1/epsilon,log(1/eta)) resources. Exact Betti recovery
or relative error on arbitrarily tiny Betti density is a different target.

### Same-output classical algorithm, with a native finite-bit clock

Fix the natural column order. KRS LF117–123 and LF258–264 identify the
number of bases with internal activity zero with the absolute reduced
Euler characteristic and, by shellability, with beta_(r-1). Its Tutte
formula at LF181–186 therefore gives the exact identity

    beta_(r-1)/#bases = T_M(0,1)/T_M(1,1)
                     = Pr_uniform_basis[i(B)=0].

An element b in B is internally active exactly when no e<b outside B
makes B-b+e a basis. At most nr rank tests decide the indicator. The
definition agrees with the fundamental-bond definition in KRS LF69–74.

The actual Anari--Liu--Oveis Gharan--Vinzant source (ALOV) defines its chain
at LF68–71: remove a uniform element of B and uniformly choose a completing
element among those giving a basis. Corollary 1.3, LF120–139, applies to
EVERY matroid with an independence oracle and bounds mixing by
r log(n^r/delta)<=r^2 log(n/delta). Thus greedily find a starting basis,
enumerate at most n possible completions per step, and run this many
steps independently for each sample. Native matrix rank pays every oracle.
Use delta=epsilon/8, and O(epsilon^-2 log(1/eta)) independent samples of
the internal-activity indicator. The sampling bias is at most delta;
Hoeffding pays the remaining additive error and confidence.

All finite choices are uniform among at most n explicitly listed items.
Binary rejection has success at least 1/2 per trial; cap each draw at
ceil(log2(8H/eta)) trials, where H is the prescribed total number of draws.
Couple with uncapped exact coins; the trajectories agree unless a cap is
exhausted, whose total probability is at most eta/8. An arbitrary output
on failure is charged to eta. This gives a fixed polynomial BIT clock,
not an unbounded fair-coin
sampler. The spectral sampler below uses the same construction with
mixing and coin-failure budgets totaling epsilon.

### Immediate full top-spectrum match

KRS Theorem 1 (LF75–90) gives a polynomial greedy decomposition of a basis
B=B1 disjoint-union B2: repeatedly set V=cl(B1) and remove an internally
active element of B1 in M restricted to V, until none remains. There are
at most r removals; closure and activity use polynomially many rank tests.
The theorem bijects bases with triples (V,B1,B2), with B1 internally
inactive in V and B2 externally inactive in M/V. KRS Corollary 13 and
LF518–525, Theorems 14–15 (LF544–555,586–600), show that the corresponding
orthogonal summand E(V) has eigenvalue n-|V| and dimension

    beta_top(IN(V)) * |mu_(M/V)(0,1)|.

This equals the number of such triples for V, using KRS LF117–123.
Consequently a uniform basis followed by that greedy decomposition and
output n-|cl(B1)| samples each eigenvalue with probability equal to its
multiplicity divided by #bases. Approximate basis sampling contracts TV
under this deterministic map. This matches the maximally mixed TOP-chain
spectral law, not the spectral measure of an arbitrary specified state,
eigenvector preparation, or arbitrary coherent dynamics.

## Selection evidence and boundary

Both corpus queries used the exact mechanism names above; baseline lookup
named Groebner/XL for the first and had no direct matroid entry. The
targeted notes were read. Parent supplied the actual KRS and ALOV PDFs/text
under audits/sources/matroid_betti_screen/; the numbered theorem/definition
passages above, not their abstracts, were inspected. No additional source
or paid proof is needed to reject the specified matroid endpoint as a
superpolynomial-advantage candidate. No new operation is recommended.
