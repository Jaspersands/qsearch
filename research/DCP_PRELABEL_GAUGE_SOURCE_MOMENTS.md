# Prelabel Gauge And Correlated Native Source Moments

LOCAL DERIVATION / REVIEW PENDING. No new noise-reduction theorem verified
against a complete lattice construction, independent theorem review, novelty,
unknown-residue decoder or speedup. This extends the EXISTING source gauge in
`core/dcp_pairing_programs.py` and `research/DCP_PAIRING_PROGRAMS.md`, not a new
gate-injection discovery. It refines the preceding physical-noise audit.

## Correction To An Overly Pessimistic Interpretation

Arbitrary basis contamination is not itself IID phase noise, and X measurement
is not generally lossless. But a legal preprocessing can balance PRELABEL
basis faults. Do not conclude that the reduction's arbitrary bad basis bit
necessarily prevents a phase-channel interface. The existing X/sign gauge
already supplies a conditional transfer; its actual lineage must be checked.

Assume a classical mixture of product good phase states or bad basis states.
The fault mask and bad bits precede independent uniform Fourier labels A_i.
Choose independent uniform coins c_i, apply X^(c_i), and replace A_i by
(-1)^(c_i) A_i. Discard OLD labels and coins before selection and inference.
Good phase states become the right phase states for their new labels, up to
global phase. Conditional on updated labels, each failed qubit is I/2.
Keeping old labels or coins invalidates that conditional averaging; postlabel
bad bits can also break it. The retained counterexample is b(A)=1[A>=4]
at q=8: conditional updated label 1, the bad output is always |0>, not I/2.

For a prelabel joint classical fault mask F, the resulting source is a mixture
of physical Z errors: each failed coordinate gets an independent fair Z flip,
and good coordinates get none. Hence for any support S,

    phi(S)=Pr[F avoids S].

If fault statuses are independent with probability gamma_i, this is the
physical phase-error model with epsilon_i=gamma_i/2. Fault independence is
NOT inferred from marginal bounds. Correlated classical faults remain a
correlated phase channel, not an arbitrary entangled-noise model. The gauge
is a legal degradation of the ORIGINAL biased quantum experiment, not a
lossless equivalence. The known-residue phase experiment after degradation
has the classical sample reverse channel from the preceding note.

## A Nonenumerative Native Source Formula

Let the supplied pair have native n-by-3n public labels. Condition each first
n-column low block invertible; charge its squared product probability. The
charts each have n random uniform pivot rows and k=2n fixed free unit rows.
Assume the prelabel law is independent of these new labels. For an explicit
joint fault law mu(F_L,F_R), the full Bell source moment is

    Cbar_mu = E_(F,F' independent draws from mu) C(F_L union F'_L,F_R union F'_R).

These independent draws are a mathematical expansion of phi(h)^2; they do
NOT duplicate physical states or assume independence between the ACTUAL left
and right packet faults. Each draw is their entire joint fault law.

For the union masks, let b be the number of faulted pivot rows across BOTH
packets. Let d be the number of logical free coordinates faulted in NEITHER
packet. Set N=2^k. Then

    C = [N + (2^d-1)2^-b
           + (2^(k-d)3^d-N-2^d+1)2^-b(3/4)^(2n-b)]/N.       (1)

Derivation: the fourth-moment source sum counts pairs of logical directions
h,j disjoint in each physical chart. Surviving h must avoid the union fault
masks. Each of the d unfaulted free coordinates permits (h,j)=(0,0),(0,1),
(1,0); each other free coordinate forces h=0 and leaves two choices for j.
h=0 contributes N, and j=0,h!=0 contributes 2^d-1 possible directions with
pivot survival 2^-b. After subtracting these cases, nonzero disjoint h,j are
linearly independent. A faulted random pivot requires h_i=0, probability1/2;
an unfaulted pivot requires disjointness, probability3/4. Multiply their
independent row expectations to obtain (1).

This is polynomial in n and the SQUARED explicit law support, with no 2^k
logical mask or random-chart enumeration. For IID faults an explicit support
is exponentially large; use the closed IID physical-phase formula instead.
Fully faulted inputs give C=1; no faults recover the clean source formula.
Effective secret character order >=4 is still required. The formula is a
joint public-source/output moment, not an efficient inference algorithm.

## Proving The IID Extrapolation Wrong

Let ALL supplied registers fail together with probability gamma, and none
fail otherwise. Each register marginal is gamma. After the gauge, every
nonempty physical support has Fourier contrast1-gamma, regardless of width:

    Cbar_correlated = 1+(1-gamma)^2(Cbar_clean-1).

At gamma=1/8, the same marginals under IID faults give physical epsilon1/16
and the previous fixed-Bell uniformization regime. The correlated law instead
retains the exponentially growing clean excess moment up to factor49/64.
At n=256 the reports certify both behaviors with the same fault marginals.
This falsifies a marginal-only no-go transfer, not a claim that the actual
reduction supplies that shared-fault law or that collision proves decoding.

## Two-Point Promise: Completion Is Not Constant-Rate LPN

[Regev, Quantum Computation and Lattice Problems](https://cims.nyu.edu/~regev/papers/quantum_average.pdf),
Definition3.1, specifies two-point coordinates in [0,M) and failure bound
(n log2(2M))^-f. For power-of-two M and q=2M, pad each position coordinate
to q and apply the coordinate QFT. Every original good or bad register gives
a uniform label in (Z_q)^n, before label-dependent selection. The integer
difference has a unique signed lift from its residue modulo q.

Under the prelabel gauge assumptions, fault marginal gamma=(n log2 q)^-f
gives physical Z-flip marginal at most gamma/2. Once the CORRECT lower residue
is known, the classical clean-block union bound applies WITHOUT IID faults:

    P(correct high-bit completion) >= max(0,1-(n+lambda)gamma/2-f_rank).

For n=128,q=256,f=1,lambda=40 this exceeds .9. The report records the exact
rational budget. This removes a fabricated constant-rate LPN bottleneck for
that conditional two-point completion regime. It does not find the unknown
residue. The lattice construction's actual M, supply of fresh registers,
q=poly(n) versus larger q, QFT/correction precision and conditional-history
failure bounds for verification remain separate unverified obligations.

## Tests, Artifacts And Next Choice

`theorems/dcp_prelabel_fault_gauge.py --save` generates
`research/phase_workbench/dcp_prelabel_fault_gauge.json`. The transfer gate
rejects missing lineage/discard assumptions; passing declarations does not
prove a source. Tests cover every n=1 union fault mask against all systematic
charts/disjoint directions, all-source IID matching at half the rate, sparse
correlations, 64-bit logical transport and large-n nonenumerative controls.
The existing gauge tests independently enumerate actual density matrices.
The Node checker adds physical phase identities, union-source counts, exact
large-n law-pair moments, two-point ledgers and dependency hashes.

Next GPT effort should now go to a CONSTRUCTIVE unknown-residue mechanism at
growing q, not a larger inventory of noise certificates. A possible design
space is consumed program-state phase processing on public Boolean functions;
its random known byproducts, unavailable repeated/doubled labels and source
coverage must be proved before any oracle or alignment claim. This is not
implemented and is not an accepted candidate. Gemini handles production
integration of these scoped source interfaces and existing regression repairs.
