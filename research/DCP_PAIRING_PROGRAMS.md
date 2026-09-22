# DCP Pairing Programs: A Constructive Interface, Not A Solver

Status: DERIVED / REVIEW PENDING. No novelty, independent review, formal proof,
polynomial decoder or speedup is claimed. Run `python qsearch.py dcp-coherent-matching`
or `python qsearch.py run EXP-DHS-DCP-COHERENT-MATCHING-INTERFACE`.

## The Remaining Algorithmic Problem

Let N=2^n, m supplied phase qubits, M=2^m, and independent uniform public
labels a_i in Z_N. Write f_a(b)=sum_i a_i b_i mod N. The clean input is

    psi_d = M^(-1/2) sum_b exp(2 pi i d f_a(b)/N) |b>.

We need a uniform efficient operation pairing enough assignments whose sums
differ by N/2. Such assignments have relative phase (-1)^d. Merely finding
some valid witnesses, computing ideal measurement matrices, or inspecting
full fiber tables does not implement this operation. Per-label preprocessing,
inverse access, source probability and workspace cleanup are charged.

This is one sufficient architecture, not a necessary form of every DCP
algorithm. The repaired arbitrary-measurement reduction requires only valid
fiber-supported witnesses, not uniform fiber states. The separate symmetric
double-evaluation lift permits more general quantum relation solvers than
the older single-call overlap audit. Neither is excluded here.

## Six-Call Reciprocal Compiler

Supply a deterministic public proposal F_a(b) in {0,1}^m union {failure},
with an efficient reversible XOR evaluator including its valid-output flag.
An efficient uniform classical evaluator can be reversibly compiled with
charged time/space overhead. A truth table is not such an implementation.

Accept b precisely when c=F(b) exists, F(c)=b, and f(c)-f(b)=N/2. The accepted
set D consists of disjoint two-cycles. Computing both evaluations, toggling
the acceptance flag and uncomputing both costs four XOR-F calls. Measure the
flag; p=|D|/M, independently of d. Every failure is charged.

On success, compute F(b) into a clean register, compute e=[b>F(b)], and swap
the endpoints if e=1. The first register now holds r=min(b,F(b)); the second
holds s=max(b,F(b)). XOR F(r)=s clears the entire second register, including
its valid flag. This costs two further calls, for six on accepted attempts
(four on failures). Both orientations leave exactly the same r and clean
temporary workspace. A Hadamard on e returns d mod 2 without error for a
clean accepted input. No reflection about the unknown input, amplification,
success estimation, fiber counts or free erasure was used.

The implementation checks complete computational-basis permutations, not just
an ideal map on the desired subspace. All 625 partial functions on four
inputs are tested for clean workspace and the accepted projector identity.
The remaining reversible arithmetic uses polynomial resources in m,n plus
the charged F implementation. A gate-export backend is NOT implemented.

## Clean Permutations Need Not Be Reciprocal

Supply an efficiently implementable clean permutation P, with its inverse
or circuit, not merely a forward function. Define q(b)=[f(Pb)-f(b)=N/2].
Use a branch qubit to prepare

    ( |0>|1> psi_d + |1> sum_b psi_d(b)|q(b)>|P(b)> ) / sqrt(2).

The public q computation is cleaned before applying P. Two XOR-P evaluations
compute/uncompute q, followed by one clean controlled P; modular arithmetic
and inverse construction are not free. Measuring X on the branch qubit gives

    E[X] = (-1)^d |{b:q(b)=1}|/M.

There is no conditioning on flag 1. Valid edges in cycles longer than two
contribute correctly. A four-cycle with N=4, a=(2,0) has signal one but zero
reciprocal mass, explicitly falsifying the claim that mutuality is necessary.
This finite example is a circuit calibration, not a candidate input family.

## Pre-Fourier Basis Faults And A Random Gauge

Regev's [primary source](https://arxiv.org/abs/cs/0304005), locally cached as
`research/literature_cache/cs_0304005_source/quantum_average.tex` around lines
850-876, gives uniform measured Fourier labels for both good registers and
bad pre-Fourier basis states |b,x>. The latter become |b> with an irrelevant
global phase. This motivates, but does not itself prove, the following gauge.

Independently choose r_i uniformly, apply X^r_i, and replace a_i by
a_i'=(-1)^r_i a_i mod N. Discard original labels and gauge coins BEFORE
selecting F/P, which may use only updated labels and fresh randomness.
For a good qubit this produces the correct phase state for a_i', up to a
global phase. For a prelabel bad bit, r_i remains uniform conditional on
a_i', so b_i xor r_i is uniformly mixed. With independent fault probability
epsilon the resulting state is exactly

    rho_bc = exp(2 pi i d(f(b)-f(c))/N) eta^Hamming(b,c) / M,
    eta = 1-epsilon.

Thus the unconditional signed parity signal of either construction is

    G(a) = (1/M) sum_valid eta^Hamming(b,Pb).

For reciprocal proposals, accepted mass is still p and conditional bias is
G/p. Noise depends on changed coordinates, not the entire m-qubit batch.
Measuring the low n-1 sum bits first preserves these particular off-diagonal
terms, because valid endpoints have the same low sum. All Born weights stay.

Scope is essential: fault status/bad bits precede uniform Fourier labels;
product attenuation requires independent faults. Correlated faults need
their joint law. Program selection must not retain the original labels or
coins. A postlabel bad-bit choice b(a)=[a>=N/2] supplies an explicit
counterexample to the mixed-state conclusion (entrywise discrepancy 1/2).
Independent tests enumerate fault masks, coins, arbitrary prelabel bad bits
and complex amplitudes, rather than just re-evaluating the formula above.

### Correlations Need Not Destroy The Useful Guarantee

The primary DCP definition gives per-register failure probabilities; we must
not silently replace a marginal promise by an independent-fault assumption.
For a classical joint fault mask J fixed before the uniform Fourier labels,
the same gauge gives the more general attenuation

    rho_bc = exp(2 pi i d(f(b)-f(c))/N) Pr[J intersects (b xor c) trivially] / M.

This follows by conditioning on the complete mask: each faulty coordinate
is fully dephased, so a matrix element survives exactly when no changed
coordinate is faulty. Average over the mask law only after this step. It
applies to mixtures of the stated product inputs, not arbitrary entangled
corruption or an unknown quantum channel. Program selection cannot depend
on the hidden fault mask. Uniform measured labels make that mask independent
of the updated public labels in this model.

If each coordinate has fault marginal at most epsilon, the union bound gives
survival >=max(0,1-epsilon*w) at distance w. Consequently any width-r pairing
with source coverage p has G>=max(0,1-epsilon*r)*p even with arbitrary
within-batch classical correlations. At epsilon<=1/n, an r<=n/2 construction
would retain at least half its coverage as signal. This identifies a useful
conditional target between very short, low-coverage moves and generic
high-density, very long moves. It does NOT construct a matcher in that range.

Correlations can help OR hurt relative to eta^w: all-or-none faults with
probability epsilon give survival 1-epsilon at every nonzero width, while
exactly-one faults on two changed coordinates give survival zero. Both are
physical countercontrols. In particular, the constant-noise envelope below
cannot be extended to arbitrary correlated masks. Independent repetition
across batches also needs to be supplied or replaced by conditional success
guarantees; within-batch bounds alone do not give a concentration theorem.

## Coverage Versus Noise: An Exact Necessary Bound

Fix b and a nonempty flip support S. The sum difference after flipping S is
sum_{i in S}(1-2b_i)a_i. One coefficient is a unit modulo N, so this
difference is uniform over independent uniform labels. Therefore even an
unbounded label/input-adaptive selector obeys

    E_a p_w(a) <= C(m,w)/N,     sum_w E_a p_w(a) <= 1,
    E_a p_{<=r}(a) <= min(1, sum_{w=1}^r C(m,w)/N).

Here p_w is the uniform-diagonal mass of accepted endpoints at distance w.
No assumption of a fixed polynomial dictionary is used. Dropping all
consistency/matching constraints gives the exact relaxation

    E_a G(a) <= max sum_w eta^w x_w,
    subject to 0<=x_w<=C(m,w)/N and sum_w x_w<=1.

Fill shortest distances first to solve this relaxation with rational
arithmetic. It is an upper bound, not an achievable pairing. Tests compare
with a separate numerical LP and exhaustive best permutations on all small
label tuples. The artifact evaluates m=n^2 through n=4096 at eta=3/4 and
eta=1-1/n. Favorable-label selection must pay its probability.

For a transparent asymptotic consequence, take r=floor(n/(2 log2(2m))).
For sufficiently large n and polynomial m, the short-distance contribution
is at most r*m^r/2^n <= r*2^(-n/2); the tail is at most eta^(r+1).
If r>=m there is no tail and the same short-distance bound suffices. Thus
fixed eta<1 gives a superpolynomially small signal at every polynomial m.
At eta=1-1/n this reasoning does NOT rule out useful mass. This is a bound
on the declared readouts under the declared noise/source law, not on all
DCP measurements, error correction or coherently composed procedures.

## Two False Shortcuts And Their Counterchecks

1. **Canonical witness success is not reciprocal coverage.** If F returns
   one canonical witness for each target residue, at most N assignments can
   satisfy F(F(b))=b. Consequently p<=N/2^m, even if all proposals are valid.
   Input-dependent rank pairing can match all available endpoints and escapes
   this cap. Finite rank and maximum-noise-weight assignment references show
   the distinction. Their 2^m tables and assignment cost matrices are charged
   as exponential reference work, not candidate algorithms.
2. **More variables do not automatically make the classical search easy.**
   [Flaxman and Przydatek](https://crypto.ethz.ch/publications/FlaPrz05.html)
   prove expected polynomial time in the number of variables when log N is
   O((log m)^2). That stated regime does not establish polynomial time for
   m=poly(log N); it requires a much larger variable budget as N grows.
   [DCP time/query tradeoffs](https://arxiv.org/abs/2206.14408) also distinguish
   linear-query exponential-time methods from subexponential sieves. A small
   sample budget must not hide exponential classical or quantum work.

## What Would Count As Progress

Supply an explicit uniform family of efficient F or clean P/inverse circuits
on natural labels, with polynomial per-label preprocessing and sample count,
and prove E_a G(a)>=1/poly(n) in the required fault model. Fresh independent
batches yield a parity estimator in O(Gbar^-2 log(1/delta)) attempts, including
zero outputs for rejected reciprocal attempts. No favorable labels are free.
Better heralded variance bounds are possible but not needed for this
conditional polynomial implication. Repeat on fresh states with known-bit
phase corrections to recover successive secret bits, with a per-stage
guarantee and charged total error/resources. This full decoder is NOT coded
or proved for a concrete pairing family here.

The immediate search objective is natural-label-averaged noise-weighted mass
per charged computation, not one-witness success or a conditional visibility.
Very short moves have too little coverage; generic very long moves can lose
their signal. A uniform computable rule exploiting structure in the intervening
range is missing. Compare any proposal with existing subset-sum/sieve methods
before calling it new. These elementary conditional constructions may overlap
known reductions; a novelty review and independent mathematical audit remain
required. Repeatedly generating more interface records is not a substitute
for constructing or falsifying that rule.
