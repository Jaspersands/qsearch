# Classical Recovery For Query-And-Discard Sources

2026-10-30. Constructive source filter, not a general dequantization of
quantum state learning. It tests a concrete route to the
[purity-gap Pauli learner](PAULI_CONJUGATION_SYMMETRY_LEARNING.md): build a
uniform coherent query to an efficiently classically evaluable function,
then discard its output. The function, including any chosen label hash,
is available to BOTH algorithms. No circuit inverse or hidden basis is
given to the classical algorithm. No novelty or hardness claim is made.

## Input And Claim

Let G=F_p^n, p odd, N=p^n. An exact deterministic evaluator f has arbitrary
equality-comparable labels and cost C_f per query. Its discarded-label
state is

    |Psi_f> = N^-1/2 sum_x |x>|f(x)>,
    rho_f[x,y] = K(x,y)/N, K(x,y)=1[f(x)=f(y)].

This is the ordinary query-and-discard construction; standard coset
states are a special case. See the source model in
[Childs-van Dam](https://harvest.aps.org/v2/journals/articles/10.1103/RevModPhys.82.1/fulltext).
The result here concerns this explicit kernel, not all states obtainable
from quantum queries or arbitrary succinct quantum circuits.

Suppose rho_f is exactly diagonal in a common eigenbasis of ONE unknown
maximal commuting Pauli subgroup (not merely any orthonormal list of
stabilizer states),
gamma=Tr(rho_f^2)>=1/R, and every positive Pauli conjugation loss is at
least a supplied delta>0. Then the FULL phase-free Pauli symmetry group
can be recovered CLASSICALLY in polynomial(n,R,delta^-1,log p,
log(1/epsilon),C_f) resources. All evaluator queries, field randomness,
elimination and quotient enumeration are charged. Numerical R and
inverse delta must be polynomial, exactly as for the quantum learner.

The promises are assumptions, not certified by the sampling algorithm.
Output is a probabilistic recovery under those promises, not a proof that
an arbitrary supplied evaluator satisfies them.
The gap is ABSOLUTE purity loss. If a promise is instead normalized by
gamma, its absolute lower bound is delta/R and must be charged accordingly.

## Exact Algebraic Structure

Define two public-but-unknown linear subspaces by the function itself:

    D = span{x-y : f(x)=f(y)},
    T = {t : K(x+t,y+t)=K(x,y) for all x,y}.

T preserves the equality RELATION; it may permute output labels. Requiring
f(x+t)=f(x) would give the wrong group. Both spaces are over F_p. For
Pauli coordinates (t,z), conjugation translates K and multiplies each
nonzero matrix entry by omega^(z.(x-y)). Since entries of K are exactly
0 or 1, phases cannot compensate for changed support. Therefore

    H(rho_f) = T x D^perp.

The symplectic orthogonal of H is D x T^perp. Thus H is coisotropic iff
D is contained in T. A state diagonal in a maximal stabilizer basis has
coisotropic Pauli symmetry. Conversely, if D is contained in T, the
n-dimensional commuting space X_D Z_(D^perp) lies in H and diagonalizes
rho_f. We obtain the exact characterization

    rho_f stabilizer-diagonal  <=>  D subset T.

This does NOT mean f is an ordinary coset oracle: different D-cosets can
be partitioned by different subgroups of D. The classical algorithm below
covers such nonuniform partitions too.
Every fiber is nevertheless affine. In each D-coset, translation by D
preserves equivalence, so its classes are cosets of a subspace K_c<=D.
Their Fourier-on-D/computational-on-G/D eigenvalues are
|K_c|/N on characters trivial on K_c, and zero otherwise. Affine fibers
alone do not imply the common-basis condition. For odd p, a nonconstant
one-bit function cannot meet it: affine fiber sizes are powers of p, so
the number of nonempty fibers is 1 modulo p-1, never 2.

Every fiber of f lies in an affine D-coset. Hence its size is at most |D|,
and

    gamma = N^-2 sum_fibers |fiber|^2 <= |D|/N.

In particular [G:D]<=R. The quantum learner's inverse-purity promise
forces a polynomial-size quotient that will be explicitly enumerated.

## Recovering D Without A Table

Repeatedly sample independent uniform x,y in G, evaluate both labels,
and, only when they agree, insert x-y into an incrementally maintained
row span V. Every inserted vector belongs to D; at most n basis rows
are stored. No density matrix or list of all N inputs is constructed.

For a proper V<D choose a proof-only z in V^perp outside D^perp. Its
phase Pauli is not a symmetry, so

    d(Z_z) = E_(x,y)[K(x,y)(1-cos(2 pi z.(x-y)/p))] >= delta.

The integrand is zero unless a collision difference lies outside V, and
is at most 2. Thus each fresh pair increases rank with probability at
least delta/2 until V=D. The algorithm never computes z or any complex
phase; the quantum gap promise only enters the proof of its classical
sampling success.

With beta=epsilon/3, use

    C = ceil(16 delta^-1 (n+ceil(log_2(1/beta))))

collision pairs. A binomial lower coupling and Chernoff bound give span
failure at most beta. If p^(n-dim V)>R afterward, ABORT before enumerating
anything. Under correct recovery the quotient cap is guaranteed. Passing
the cap alone does not certify V=D; the failure allowance is still needed.

## Recovering T With One-Sided Classical Tests

From an RREF basis of D, standard basis vectors at nonpivot columns give
an explicit complementary space. Enumerate its at most R vectors t. Since
D subset T, they represent every possible translation class modulo D.

For each t sample fresh uniform pairs and compare the two Boolean values
K(x,y) and K(x+t,y+t), using FOUR evaluator calls. The mismatch indicator
has exact mean

    E[1_(K(x,y)!=K(x+t,y+t))] = 2 d(X_t).

This follows from K^2=K and translation invariance of uniform sampling.
For a true symmetry mismatches never occur. For a nonsymmetry they occur
with probability at least 2 delta. Reject a representative at its first
mismatch; accept it only after

    V = ceil(ceil(log_2(R/beta))/(2 delta))

trials without a mismatch. A union bound over at most R representatives
gives false acceptance probability at most beta. Analyze on the ideal
correct-D branch, then add the earlier span failure; do not silently
condition the original sample law on all future tests passing.

Return the span of D and all accepted translation representatives,
together with the phase generators D^perp. This is exactly T x D^perp
on the successful event. Equality-label encodings may be arbitrary;
neither numeric label values nor a label-ordering oracle are used.

## Resource Accounting

There are at most 2C+4RV evaluator calls. Multiply by the actual C_f,
including original-input access and label comparisons. Field-vector
operations use n coordinates of log p bits; basis work is polynomial.
Only the quotient is enumerated, with its size checked BEFORE allocation.

At most M=2n(C+RV) uniform field coordinates are needed. Generate each
from k=ceil(log_2 p) random bits with rejection of integers >=p. Cap its
attempts at L=ceil(log_2(M/beta)); each attempt succeeds with probability
at least 1/2. A union bound charges at most beta for any randomness abort.
Thus random bits are capped by M L k and total failure by 3beta=epsilon.
Reproducible seeded test runs are finite controls, not evidence for the
probabilistic theorem. Exact evaluation of f and IID ideal randomness
are the algorithmic input model.

An additional user work cap may abort sooner and supplies NO recovery
guarantee. Neither a work cap nor an incorrect supplied promise justifies
claiming native infeasibility, hardness, or success.

## Source Consequences And Limits

- Ordinary additive HSP: if f separates cosets of K0, then D=K0,
  T=G, and gamma=1/[G:K0]. The polynomial-purity regime is already
  classically accessible by collisions. High-index abelian HSP remains
  quantumly easy by existing Fourier algorithms; this filter does NOT
  dequantize that regime or general nonabelian HSP.
  Stronger classical query bounds for this special case are already known;
  see [Ye-Li](https://arxiv.org/abs/2110.00827).
- Discarding a public hash h(f(x)) is covered by replacing f with h composed
  with f, IF the resulting state obeys the same exact promises. It can
  erase the original hidden subgroup. Recovering the hashed state's H
  must not be called recovery of the original hidden object.
  The original f register and work garbage must first be uncomputed. Merely
  appending a hash and then discarding every label leaves rho_f unchanged.
- A supplied efficient Clifford C after label discard does not evade this
  filter. Its public symplectic matrix S preserves purity and permutes
  Pauli losses. Recover H for rho_f classically and return S H for
  C rho_f C^dagger. Known affine relabeling is also covered. No unknown
  Clifford description is inferred or granted for free.
- A coherent phase mask, nonuniform amplitudes, retained oracle-register
  coherence, or an unknown quantum channel is outside this kernel model.
  None is an automatic escape: a proposed bridge must supply its actual
  state, complexity, gap and original-solution decoding.
- Postselecting a fixed output or hash bin produces a different pure
  fiber state. Its preparation probability must be charged. A nonnegative
  uniform pure state is a stabilizer state only when its support is an
  affine subspace. Common bins then also give classical rejection samples;
  rare bins do not provide polynomial state preparation merely by being
  rank one. This is not a universal lower bound against other preparations.
  If the original label is NOT erased, an HSP bin containing k cosets out
  of m has acceptance alpha=k/m and conditional purity 1/k, so their
  product is 1/m. Retaining a full flat graph purification instead requires
  an affine encoded function to yield a pure stabilizer state; that function
  is classically learned with n+1 evaluations. The affine support fact is
  standard [stabilizer structure](https://arxiv.org/html/quant-ph/0408190v2#S5.SS2).

## Why This Is Not A Source-Simulation Theorem

Fresh random hashes do not define one deterministic equality kernel.
If each independently chosen hash has EXACT pairwise collision probability
a=1/B for distinct labels, clean evaluation and discarding its seed/output
gives

    rho_bar = (1-a) rho_S + a |+><+|.

For an HSP source of index m>1, it is Fourier-diagonal with purity
a^2+(1-a^2)/m and minimum positive loss a^2. Its unique heaviest Fourier
eigenlabel is zero, so its FULL conjugation group is G x {0}, independent
of the original subgroup S. Yet Fourier measurements still give useful
S^perp samples with constant probability for fixed a<1. This is consistent
with [May-Schlieper's compression-robust period finding](https://arxiv.org/html/1905.10074v3),
not a dequantization of it. A universal-hash upper bound alone, without
the exact collision probability, does not imply the displayed mixture.

Even a deterministic source satisfying ALL our promises can retain
information not contained in H. On F_3 x V, choose disjoint output tags

    f(0,x)=A, f(2,x)=C, f(1,x)=(1,f_S(x)).

For S<V of index m>=3, purity=(2+1/m)/9, gap>=(1-1/m)/9>=2/27,
and H=X_V Z_flag, independent of S. Constant R=5 suffices. Nevertheless
measuring flag1 (probability1/3) recovers the ordinary rho_S source. The
classical attack recovers H, not an arbitrary quantum measurement of rho
and not the original S. This flagged construction is a scope counterexample,
not a new native problem or explicit-input hardness claim.

The lesson is stronger than a source-access warning: **the full symmetry
group can be the wrong observable for the desired hidden object**, even
when purity and gap are excellent. Every proposed reduction must prove
solution decoding from that particular group.

A paid nonlinear/interference bridge does survive: the existing
[discrete-log phase construction](audits/reviews/2026-10-30-noisy-phase-native-scope.md)
uses group exponentiation, Fourier measurement and known rescaling to
prepare identical quadratic phase states at constant acceptance. It is
outside the nonnegative kernel model and recovers a known Shor/HPGP task,
not a new application of mixed-state learning.

## Finite Controls And Execution

The general proof is independent of these cases. Exact ternary references
use at most 27 inputs and enumerate all Pauli losses, including mixed XZ.
They are never called by `recover_partition_symmetry`, which receives
only the evaluator and public promise parameters.

- f(a,b)=(b,0 if b=0 else a): fiber sizes 3,1,1,1,1,1,1;
  purity5/27, gap2/27, D=T=<e1>, H=<X1,Z2>.
- f(a,b,c)=(c,b,0 if b=0 else a): purity5/81, gap2/81,
  D=<e1>, T=<e1,e3>, H=<X1,X3,Z2,Z3>. This full group is noncommuting.
- Different layers can contribute different collision directions: use
  labels (0,b) at c=0, (1,a) at c=1, (2,a,b) at c=2. Purity7/81,
  gap1/27, D=T=<e1,e2>, and no single fiber spans D.
- The singleton indicator on F_3^2 has purity65/81 and gap14/81, but
  D=G and T=0. It violates exact stabilizer diagonality despite high
  purity. It is a scope countercontrol, not a refutation of the theorem.

The CLI runs seeded classical recovery on the first two controls, checks
the generated groups against exact enumeration, and records actual oracle
queries/random bits and their caps. Run
`python qsearch.py phase-copy-baseline --partition-source --write`.
The output is `research/classical_baselines/partition_source_filter.json`.
It neither promotes a candidate nor marks arbitrary source promises verified.
Seeded successes validate implementation, not the asymptotic probability bound.

## Decision

The simple discarded-label bridge cannot turn the new purity-gap learner
into a superpolynomial classical-input speedup under its own promises.
This is a constructive matched-access filter, stronger than merely noting
low purity for one HSP example. It does not settle arbitrary source models,
the native Mersenne completion problem, or the general quantum-input
learning theorem. Future work must specify a different paid mechanism
and its classical competitor, not just attach a hard problem's name.
