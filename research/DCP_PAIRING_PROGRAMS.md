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
their signal. The following explicit rule now reaches useful coverage in the
intervening range, but its runtime is exponential. Compare any improvement
with existing subset-sum/sieve methods before calling it new. These elementary
constructions may overlap known reductions; a novelty review and independent
mathematical audit remain required.

## An Actual Finder: Affine-Marked Isolated Edges

Implemented in `core/dcp_affine_marked_pairing.py`, and included in the SAME
CLI, experiment and report. This is a classical reversible-program baseline
for the quantum parity readout, not a new input oracle or an efficient decoder.

For fixed labels, form the IMPLICIT undirected graph on Boolean assignments:
b,c are neighbors when 1<=|b xor c|<=r and f(c)-f(b)=N/2. It is undirected
because N/2=-N/2 modulo N. Let D=sum_{w=1}^r C(m,w) and lambda=D/N.
Choose a uniform binary ell-by-m matrix H and uniform offset v, independently
of labels, and mark b when Hb+v=0. DO NOT condition on H having full rank or
the marked set being nonempty. The public seed has ell*(m+1) bits.

Define F(b) as its unique marked neighbor if b is marked and has exactly one
marked neighbor; otherwise return failure. The reciprocal compiler accepts
exactly endpoints of isolated edges in the marked induced graph. This is
input-dependent, not one canonical witness for each residue.

### Exact Natural-Source Coverage Bound

For fixed b, every nonempty support S gives a uniform signed sum modulo N.
Two distinct supports S,T have a 2-by-2 coefficient minor of determinant
+1 or -1: use a common coordinate and one in the symmetric difference for
nested supports, or one coordinate unique to each otherwise. Their sum
events are therefore pairwise independent over uniform labels, even for the
composite modulus 2^n. The degree d_b has EXACT moments

    E[d_b] = lambda,
    E[d_b^2] = lambda^2 + lambda*(1-1/N).

Uniform affine maps on F_2^m are three-wise independent on distinct inputs.
Indeed any three distinct augmented vectors (b,1) are linearly independent
over F_2; independent uniform rows then give independent output vectors.
They are NOT four-wise independent on affine parallelograms. Let theta=2^-ell.
For an edge (b,c), its endpoints are marked with probability theta^2. Given
both are marked, every other neighbor is marked with probability theta.
The union bound, requiring no higher independence, yields

    Pr[(b,c) is isolated] >= theta^2 - theta^3*(d_b+d_c-2).

Count ORIENTED edges and divide by M so each accepted endpoint counts once.
For every fixed graph, sum_b sum_{c~b}(d_b+d_c-2)=2 sum_b d_b^2-2 sum_b d_b.
Average over ALL natural labels, including graphs with no successful edges:

    E_{a,H,v}[accepted source mass]
      >= theta^2*lambda*(1-2*theta*(lambda-1/N)).

Choose ell=max(0,ceil(log2(4lambda))). The bracket is at least 1/2, so the
bound is positive. If r is the first radius with D>=N, then 1<=lambda<m+1:
the previous partial binomial sum is below N and C(m,r)<=m*C(m,r-1), with
r=1 handled directly. Hence theta>1/(8lambda) and the mass is at least
1/(128*(m+1)). This proves a polynomial natural-source lower bound for
polynomial m, not a success guarantee for each label tuple or each hash.

For m=n^2 and n>=2 this radius exists. For n>=4,
C(n^2,floor(n/2)) >= (n^2/floor(n/2))^floor(n/2) >= 2^n, so r<=n/2;
n=2,3 are direct. More sharply, r<=ceil(n/log2 n) follows from
C(n^2,k)>=(n^2/k)^k>=n^k, while D<=r*m^r gives an Omega(n/log n) lower
bound. Thus r=Theta(n/log n). At prelabel fault marginal <=1/n, even the
correlated-mask guarantee retains at least half the clean coverage, and
asymptotically a fraction tending to one. This does NOT make the finder fast.

### Charged Implementation And Its Failure As A Speedup

The actual program enumerates radius-r supports, computes their signed sum
and affine marking, and reversibly accumulates the FULL hit count plus the
XOR of hit neighbors. The count uses ceil(log2(D+1)) bits. If the count is
one, copy the encoded neighbor/valid flag to the caller's XOR output. A
second pass subtracts hit counts and cancels the image XOR, cleaning all work.
These updates commute, so no exponential history list is needed. No saturated
counter, irreversible early-exit flag, precomputed fiber table or free neighbor
list is hidden in the primitive.

One XOR-F call costs exactly 2D support-predicate evaluations; six cost 12D.
Each predicate and support-generation step also has charged polynomial bit
arithmetic. This gives polynomial workspace and uniform exponential-time
computation. The code replays this procedure on basis wires, including dirty
workspace permutations, and composes actual finite proposal outputs with the
previous six-call physical compiler. Gate export is still not implemented.

Since D>=2^n, this finder remains exponential. A generic square-root-search
domain estimate is also exponential; it is recorded only as a reference, not
an implemented coherent minimum/counting routine or a lower bound against
algorithms exploiting arithmetic structure. No improvement over known DCP
time/query tradeoffs is claimed. Recent worst-case subset-sum improvements
are also already audited in `dcp_four_block_ksum_noncollapse.py`; they cannot
be called polynomial by renaming the variables or omitting coherent memory.

### What Must Replace Enumeration

For a marked b, put z_i=(1-2b_i)a_i mod N. A neighbor corresponds to a support
vector s satisfying

    1<=|s|<=r,     sum_i z_i s_i = N/2 (mod N),     Hs=0 (over F_2).

This is an explicit short signed modular subset-sum search with a binary
syndrome, not arbitrary oracle access. An efficient clean valid-or-error
proposal that returns the neighbor on these isolated-edge instances would
inherit their coverage. It need NOT certify uniqueness on every input: a
deterministic valid output on multiple-neighbor inputs may produce additional
reciprocal edges, and the compiler checks those. The present counter-based
implementation chooses to reject them. Do not accidentally impose global
canonical ranking or a stronger uniqueness-decision oracle on every future
solver. A quantum relation routine would need its own coherent composition
argument; a measured witness finder is not automatically a clean XOR oracle.

### Attempted Refutations

- Full-rank conditioning destroys the exact hash premise: on two input bits,
  a nonzero one-row hash cannot mark all of 0,1,2, whereas unrestricted affine
  hashing gives probability theta^3. Dropping the offset also fixes h(0)=0.
- Pairwise-independent marks alone are insufficient. On the four-cycle from
  N=4, labels=(2,2), radius 1, mark all vertices with probability 1/16, each
  singleton with probability 3/16, and none with probability 3/16. Marginals
  are 1/4 and pair probabilities 1/16, but there is never an isolated edge.
  Substituting three-wise independence would incorrectly predict mass>=1/16.
- Small graph success cannot stand in for the average theorem. Controls exhaust
  every label tuple, hash seed and source assignment in their declared small
  domains, and check BOTH degree moments and the rational mass lower bound.
- Marking only one endpoint or omitting reciprocal filtering does not produce
  the clean pair asserted by the proof. The existing compiler is retained.
- Selected demonstration labels are used only for full-workspace circuit tests,
  and explicitly not as coverage estimates. No favorable seeds are discarded
  from the source-average controls.
- Polynomial seed size and workspace do not imply polynomial time. Exact
  scaling rows expose the exponential predicate count instead of fitting a
  runtime exponent from small examples.
- Correlated prelabel faults use support survival, not independent eta^r.
  This construction does not inherit the constant-independent-noise no-go as
  a general noise theorem, nor does it solve arbitrary quantum corruption.

The graph-thinning argument is elementary and may be known in another form;
no novelty or independent-review claim is made. The research gain is the
explicit separation between achievable short-move source coverage and the
unresolved computational cost of finding the partner.

## Capped Balanced Lists: An Actual Meet-In-The-Middle Baseline

Implemented in `core/dcp_balanced_pairing.py`, in the SAME CLI, experiment,
and artifact under `pairing_programs.balanced_mitm_program`. Status remains
DERIVED / REVIEW PENDING. This is an explicit computational baseline, not a
new speedup or a classical solution of DCP. A Python basis-wire replay and
a reversible construction are supplied; a gate exporter is not.

### Coverage Does Not Require A Full Hamming Ball

The preceding moment proof needs only a fixed family of DISTINCT nonempty
supports, independent of labels, assignments and hash seed. Any two distinct
supports still have a unit signed-sum minor. Thus the same first/second
moments and thinning bound hold with D equal to the exact family size.
The support family can be structured to make the computation less expensive.

Partition m=2t coordinates into equal blocks. Let k be the first integer
with C(t,k)^2>=N. In each block retain only the first L=ceil(sqrt(N))
weight-k supports in lexicographic order of their index tuples. A full flip
chooses one retained support in EACH block. This gives D=L^2 distinct
supports, all of width 2k. It is NOT the whole radius-2k ball, nor usually
the full Cartesian product of all weight-k supports. The truncated family
is fixed publicly; no favorable label, assignment or seed is selected.

For n>=2, 1<=lambda=L^2/N<2. The prescribed hash has ell=2 or 3, so
theta>=1/8 and the general lower bound gives

    E accepted source mass >= theta^2*lambda/2 >= 1/128.

For even n, lambda=1 and the stronger exact bound is (1+1/N)/32.
This removes the artificial inverse-polynomial loss from overshooting the
desired degree with a full binomial shell. The full-shell option remains an
explicit comparison; it is not silently substituted for the capped family.

Linear phase samples already suffice for a constant SCOPED noise signal.
Take m=2n, n>=6. Set k0=ceil(n/4). Then k0<=n/3<n/e, and x log(n/x) is
increasing up to n/e. Consequently

    C(n,k0) >= (n/k0)^k0 >= 4^(n/4) = 2^(n/2).

The minimal k is <=k0, so 2k<=2n/3. Under the stated classical PRELABEL
fault-mask model, each fault marginal <=1/n therefore preserves >=1/3 of
every accepted edge's signal, giving source-averaged signed signal >=1/384.
This includes within-batch correlations, NOT arbitrary quantum corruption.
With m about n^2 the earlier k=O(n/log n) argument gives survival tending
to one. The artifact compares both sample regimes. Independence or a suitable
conditional guarantee across fresh batches is still needed for concentration.
No full-secret decoder is implemented by this parity calculation.

### Join In The Correct Product Group

For source assignment b, write z_i=(1-2b_i)a_i mod N. For each retained left
support u generate key (sum z_i u_i mod N, H u). For each right support v
generate key (N/2-sum z_i v_i mod N, H v). Equal keys are precisely the
modular-sum AND binary-syndrome constraints. Syndrome components combine
by XOR, not integer addition. The affine offset cancels on a difference,
but the separate test Hb+offset=0 must still be applied to the source.

Sort the 2L records using a fixed bitonic comparator network, padding with
sentinels to P=2^ceil(log2(2L)) records. A record contains its product-group
key, side flag and support mask. Wire addresses never depend on b or keys.
Every comparison retains a swap bit; the final computation reverses swaps
and recomputes the original comparisons to erase those bits. Reversible
sorting is prior technique, not a new quantum primitive; see
[Beals et al., pp. 4 and 6-8](https://arxiv.org/pdf/1207.2307).

Scan equal-key runs while retaining a fresh register for each prefix state:
left/right counts and XOR masks, current key, total pair count, and total
XOR of pair masks. A new right record v adds c_left to the count and
X_left XOR (v if c_left is odd else 0) to the pair-mask XOR. The left-side
formula is symmetric. Every pair is counted once; disjoint blocks ensure
each pair is a distinct support. Colliding keys MUST retain multiplicity.
No dictionary deduplication or explicit enumeration of all matching pairs
is needed. Full counters avoid irreversible saturated uniqueness flags.

When the source is marked and the count is exactly one, XOR its encoded
neighbor/valid flag into the requested output register. Reverse every prefix
calculation, reverse sorting, and uncompute the original records. This
restores all scratch registers. Prefix updates are functions XORed into
fresh registers, not irreversible resets on the quantum data. The diagnostic
Python return fields are NOT retained quantum outputs or measurements.

The retained records depend on b. When b is in superposition, they are
COHERENT storage, even though the underlying partner-search algorithm is
classical. No constant-time coherent RAM access is assumed. Fixed-address
operations can be composed as reversible word circuits, with polynomial
arithmetic scratch and cost; the current tests do not export such gates.

### Exact Resource Accounting

Let q=log2(P). One forward sort uses C=P*q*(q+1)/4 comparators. One XOR-F
evaluation charges 2C comparators, 4L generated/uncomputed records and 2P
scan steps. An accepted six-call pairing charges 12C comparators, plus all
other work. Failures, source preparation and repetition remain charged.
The artifact counts stored record bits, comparator flags and prefix states;
the stated bit count excludes reusable polynomial arithmetic scratch,
caller-owned input/output registers and fault-tolerance overhead.

Thus time is O(L*log(L)^2*poly(n,m)) and coherent storage is O(L*poly(n,m)).
L=ceil(2^(n/2)) remains exponential. This improves on the original exhaustive
support scan at the cost of exponential storage; it is not a polynomial
decoder or an established improvement on known DCP tradeoffs. In particular,
[linear-query exponential-time DCP algorithms already exist](https://arxiv.org/abs/2206.14408).
Compare matched sample, time and memory models before drawing any advantage
claim. Do not confuse the modulus bit length n with the Boolean variable
count m in published subset-sum running-time exponents.

### Isolation Does Not Leave A Free Dense Instance

For a fixed b, conditioning on its affine mark leaves H uniform: for each H
there is exactly one offset that marks b. Each nonempty support s then has
uniform Hs independently of its uniform signed modular sum. Therefore

    E[number of marked neighbors | b marked] = D/(N*2^ell) = lambda*theta.

For lambda>=1 our hash choice gives 1/8<lambda*theta<=1/4. Equivalently the
product-group target domain has between 4D and 8D elements. Enlarging the raw
support catalogue and then re-isolating increases the syndrome constraints
as well; it does not automatically supply the dense-instance regime that a
generalized-birthday argument may require. This is an expectation and a
resource check, NOT an independence theorem for entire lists, a hardness
proof, or an exclusion of list-free arithmetic algorithms. Different proposal
rules and the separate clean-permutation readout remain open.

### Counterchecks And Remaining Research Target

- Two unsorted inputs can produce one sorted output; saved swap history is
  essential for reversibility. Boolean network controls and duplicate-key
  controls independently check sorting and inverse histories.
- Labels (1,1,1,1) at N=4 have four balanced witnesses at b=0, not one.
  A one-entry-per-key dictionary would falsely accept uniqueness.
- A valid move contained wholly in one block is absent from this graph.
  Neither full-radius nor full-shell coverage can be used for capped lists.
- Hs=0 alone does not imply that either endpoint is marked. An impossible
  constant affine offset is an explicit zero-acceptance countercontrol.
- Finite source controls exhaust their full label, seed and assignment laws,
  checking both degree moments, coverage and post-mark conditional degree.
  Selected program controls separately compare an independently enumerated
  graph, workspace cleanup, arbitrary XOR outputs and the physical readout.
  Large scaling rows are exact analytic counts, not executed large circuits.

The next substantive target is a LIST-FREE or otherwise competitive structured
partner solver, or a different readout that evades this architecture's costs.
Do not spend another pass improving the coverage bound alone: constant source
coverage with linear samples is now supplied under the stated model. The
exponential coherent computation is the unresolved problem. None of these
elementary constructions has received independent or novelty review.
