# Dense Native Phase Transport And Its Arithmetic Baseline

LOCAL DERIVATION / REVIEW PENDING. This is a conditional decoder target and a
falsification interface, not an accepted candidate, efficient algorithm,
independently reviewed theorem, novelty claim, or quantum speedup.

## The Actual Missing Operation

Let q>=8 be a power of two, Q=q/2, and let A=B+2H be native independent uniform
n by (n+k) labels, conditioned on the FIRST n binary columns being invertible.
The low-label kernel C has dimension k. A zero-origin parity chart identifies
z in F_2^k with a Boolean physical assignment x(z) in C. Define

    F_A(z) = A x(z)/2 mod Q.

All components of A x(z) are even; the division is integer division before
reduction. The supplied packet is

    2^(-k/2) sum_z exp(2 pi i s.F_A(z)/Q) |z>.

The phase depends on s mod Q, not the full original s mod q. Packet compilation
is public and efficient; preparing a second packet with the same labels is NOT
granted. Neither is an unknown preparation inverse, chosen hidden-phase oracle,
target-dependent advice, or an exponentially large lookup table.

The proposed missing operation is a known public permutation P_A from canonical
coordinates (t,j) to packet assignments. Applying P_A^{-1} should transport the
unknown packet to a Fourier reference. Both directions, classical preprocessing,
clean workspace, quantum gates, and precision must be polynomial in n and log q.
Enumeration currently implements a reference only. No efficient P_A is supplied.

## Sparse Sign Correction: A Restricted Obstruction

Consumed phase programming produces independent uniform signs b and updated
labels D_b A. Suppose an EXACT public monomial correction returns the unsigned
reference for EVERY secret. Both parameterizations must cover the full code C;
they and the correction may depend on every higher label. At s=0 both states
are flat, so the public diagonal correction is constant. The correction is
therefore a permutation, up to a global phase. Because the reference contains
the zero word, its possible secret-dependent global phase is a translation by
the signed phase of some w in C.

If b agrees with some codeword on all active coordinates, coordinate complement
is a direct correction. Its conditional sign probability is 2^(k-m_active).
The n systematic pivot rows are independently uniform k-bit vectors. Averaging
their zero-row indicators gives the exact direct-correction mean

    p_direct = 2^(-n) (1+2^(-k))^n.

Otherwise, for EACH possible w, choose an active coordinate i with w_i != b_i,
and a low-defined kernel basis word x with x_i=1. Any possible source preimage
y would require A v=0 mod q for v=D_b(y-w)-x. At i, v_i is -1 or -2; v is
nonzero. Conditioning on B, one independent higher coefficient therefore bounds
each row's probability by 2/Q=4/q. Union over w,y in C gives

    p_extra <= min(1, 2^(2k) (4/q)^n).
    E_source p_exact <= min(1, p_direct+p_extra).

Charge every supplied attempt and prefix failure. At k=2n,q=n=256, even n^2
attempts have upper success below 10^-50. This bound becomes vacuous in dense
packets or at small q. It does NOT prohibit keeping signed labels, approximate
transport, partial images, secret-specific correction, branch-mixing quantum
operations, or a general decoder. Source-dependent correction is already
allowed; source-dependent favorable-sign postselection is not free.

## Dense Approximate Transport: Existence, Not Construction

Set g=n log2 Q, G=Q^n, k=g+Delta, N=2^k, with even Delta>=0. For every fixed
full-rank low chart, different Boolean codewords have a difference containing
a coefficient +/-1. Native H makes their phase-residue difference uniform.
The exact histogram second moment is consequently

    E_H chi_squared(p_F,uniform_G) = (G-1)/N.
    E_H TV(p_F,uniform_G) <= sqrt((G-1)/N)/2.

Each canonical residue t has N/G desired slots (t,j). Match these slots to
assignments with residue t, then biject the unmatched slots arbitrarily. This
matches a fraction alpha=1-TV of the full basis. For EVERY secret, the transported
packet's overlap with the ideal reference is at least max(0,2alpha-1). The ideal
reference is a product of Q-ary phase states and uniform junk; its QFT returns
the residue. Jensen and the second moment give source-mean success at least

    max(0,1-sqrt((G-1)/N))^2 >= (1-2^(-Delta/2))^2.

Delta=16 gives (255/256)^2. At n=q=256, one packet uses 2,064 original phase
states. The existence proof enumerates 2^k assignments. Dense occupancy is NOT
a matching, ranking, fiber sampler, reversible implementation, or mixing-time
certificate. The likely failure is that constructing the matching is itself
a random subset-sum/fiber-uniformization problem.

## An Exact Two-Call Arithmetic Baseline

For ANY public permutation P(t,j), define

    d_j(t)=F_A(P(t,j))-t,
    L_j,c = number of t for which d_j(t)=c.

Character orthogonality gives its uniform-secret mean correct-QFT probability

    p_Q = sum_(j,c) L_j,c^2 / (N G).

On an independently sampled uniform residue challenge u, a classical routine
with charged chosen-input access to P can do the following:

1. Sample uniform j,t0; compute c=F_A(P(t0,j))-t0.
2. Evaluate x=P(u-c,j); return the physical assignment only if F_A(x)=u.

Its independent-challenge mean success is EXACTLY p_Q. There are two forward
P calls, two public F evaluations, and polynomial modular arithmetic. The
challenge is NOT planted from a witness. Additional public monomial phases
replace bucket counts by phase sums and can only decrease p_Q relative to this
arithmetic baseline. The earlier `DCP_WALSH_FEEDFORWARD.md` has a related linear
two-call mechanism; do not present this generalization as established novelty.

This is not a classical simulation of the unknown DCP input. A polynomial
classical arithmetic witness routine could still improve a quantum reduction.
If P is only quantum-evaluable, the reduction gives a quantum arithmetic routine,
NOT a classical one. General branch-mixing quantum decoders are not covered.
Test a proposed classical P on identical native labels and independent targets
before crediting its Fourier success as uniquely quantum progress.

The established connection between optimal DCP measurements and subset-sum
computation is relevant prior art, not evidence that this missing permutation
is efficiently implementable. See [Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044).

## Conditional Robust Full-Secret Composition

This section assumes the specific prelabel CLASSICAL mixture of product good
coset states and failed basis states. All fault masks/bad bits precede fresh
uniform Fourier labels. Apply the existing X/sign gauge and DISCARD old labels
and gauge coins. Conditional on the complete prelabel classical data, each
failed site becomes I/2: it is equivalent to an independent fair Z coin at that
site. Fault STATUSes can remain arbitrarily classically correlated. Labels,
gauge-error coins, and independent per-attempt measurements must be independent
conditional on this data. Arbitrary joint Z-error laws, entangled corruption,
postlabel faults, adaptive batch reuse, and secret-averaged-only fault promises
do not inherit this argument.

Allocate R disjoint attempts before labels are selected. Each uses a training
packet with m=n+g+Delta states, L=n+lambda original states for lost-bit completion,
and M fresh verification states. A full candidate is committed before its
verification labels. For a completely error-free block, success is at least

    a=(9/32)(1-2^(-Delta/2))^2(1-2^(-lambda)).

The prefix probability is uniformly >=9/32: the first two factors are 3/8,
and the remaining product is >=1-sum_(j>=3)2^-j=3/4. Conditional on f_i failed
sites in attempt i, its clean component has weight 2^-f_i. With each register's
basis-fault marginal <=gamma=1/(n log2 q) for each FIXED secret, Markov gives
Pr(mean_i f_i > c*block*gamma)<=1/c. Jensen then gives average clean-attempt
rate >=a 2^-K, K=ceil(c*block*gamma). Conditional independence gives

    Pr(no correct accepted candidate) <= 1/c + 1/(1+R a 2^-K).

For a WRONG full candidate, every fresh-label verification vote is exactly
fair conditional on its prelabel data, whether its original site was good or
a gauged basis failure. Nontrivial character orthogonality handles good sites;
I/2 handles failed sites. Thus accepting at least ceil(3M/4) zero votes has
false-positive probability equal to the corresponding Bin(M,1/2) upper tail.
Union over R candidates adds R times this tail. No conditional gamma-budget
on the candidate history is needed IN THIS GAUGED MODEL. The more general
arbitrary-bad-state verifier still requires its stronger conditional promise.

With Delta16, lambda40, c6, R16,384, M256, the n=q=256 conditional upper failure
is about .21969. It charges 42,860,544 original states. At n=q=64 the same bound
is about .63921: it does NOT certify bounded error. These are formulas, not
large experimental runs or an implemented decoder. Gate/source perturbations
must fit the remaining margin below1/3. Efficient transport is still absent.

Falsifier: four independent fair single-site errors leave no clean attempt with
probability1/16. A single shared fair coin flipping the same site in all four
attempts has identical marginals but probability1/2. This invalidates extending
the clean-component amplification argument to arbitrary correlated Z laws;
it is not a lower bound on the full decoder's behavior under those laws.

## Natural Lattice Target And Next Research

[Regev's primary reduction](https://cims.nyu.edu/~regev/papers/quantum_average.pdf),
Definition3.1 and Lemma3.12, uses M=2^(4n). Coordinate Fourier processing therefore
has q=2M=2^(4n+1), g=4n^2, and dense m=4n^2+n+16. Runtime must be polynomial
in n AND log q; polynomial in q is exponential here. The paper also budgets
approximate product-state preparation. The supplied parameter ledger checks
the conditional register/failure arithmetic, NOT the full lattice composition,
the actual preparation trace-distance budget, or a cryptographic consequence.

Priorities, ranked:

1. Find a uniform quantum-only fiber operation or genuinely branch-mixing decoder
   with charged growing-q cost. Show actual residue inference, not occupancy.
2. If transport is classical, test the exact two-call independent-target baseline
   and identify what its arithmetic solver contributes to the quantum reduction.
3. Prove source-valid conditional low-bit/fiber recursion, including normalization
   and reversible rank/unrank cost. A fiber oracle is the missing operation, not
   an allowed input. Check existing thermal/walk audits before repeating them.
4. Compose a SUCCESSFUL decoder with lattice state preparation and total precision.
   Do not spend on production backend work before a polynomial mechanism exists.

The decisive falsifier is exponential matching/fiber cost or loss of native
source coverage. A prospective positive result must survive classical arithmetic
attacks, independent uniform targets, full-secret completion, and original-state
accounting. A quantum-only arithmetic routine would still need a genuine
improvement over known subset-sum methods and DCP sieves.

## Executable Checks

`python theorems/dcp_dense_phase_transport.py --save` writes the live report.
The focused test file has 11 tests. The independent Node checker recomputes
bounded native-source histograms, exact Gaussian-root QFT probabilities,
independent-target witnesses, monomial-phase controls, scaling/fault formulas,
and dependency hashes. These are implementation crosschecks, NOT independent
theorem review. No full production/qsearch validation is claimed in this pass.
