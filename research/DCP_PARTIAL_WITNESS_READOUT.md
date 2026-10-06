# Native DCP Readout From One Partial Witness

LOCAL DERIVATION / REVIEW PENDING. Conditional reduction, not an implemented
polynomial solver, independently reviewed theorem, novelty claim or speedup.
No accepted candidate. Bounded enumeration below is calibration only.

FOLLOWUP: `DCP_DIRECT_WITNESS_FILTER.md` removes even this parity-chart step.
The preferred general arithmetic interface acts on the raw phase source, allows
a known purified quantum finder and recovers the full secret directly. This note
remains the deterministic/parity/source-covariance control.

## Research Decision

The previous dense phase-transport interface was sufficient but unnecessarily
strong as a universal research target. This alternative does NOT require a
complete fiber permutation, its inverse, rank/unrank, uniform fiber sampling,
two witnesses for one target, or a clean fixed junk state. It requires ONE
reproducible verified witness on an inverse-polynomial fraction of independent
uniform targets, and reversible uncomputation of the finder transcript.

This is a better next construction target, not evidence that it is easy.
The arithmetic finder may be classical: a classical arithmetic algorithm used
inside a quantum reduction does not classically simulate its unknown DCP input.

Prior art must not be erased. [Regev, Quantum Computation and Lattice
Problems](https://arxiv.org/pdf/cs/0304005), Section4, already reduces a
nonnegligible legal-input subset-sum solver to DCP using deterministic verified
preimages and coherent matching. Definition3.1 specifies the vector two-point
source and its failure parameter. The local direct vector-QFT calculation and
source/noise ledger here are NOT claims that the partial-witness connection is
new. Keep the existing matching route; this is another sufficient interface.

Authoritative implementation: `theorems/dcp_partial_witness_readout.py`.
Live artifact: `research/reductions/dcp_partial_witness_readout.json`.
Independent arithmetic implementation:
`research/certificates/dcp_partial_witness_crosscheck.js`.

## Exact Ideal Readout

Let q=2^L, Q=q/2, A an n-by-m IID uniform label matrix modulo q, and
m=nL+Delta with Delta>=0. Abort and charge only failure of FULL binary row rank,
not failure of a selected prefix. Let C=ker(A mod2), k=m-n, N=2^k and G=Q^n.
Then N/G=2^Delta. A zero-origin public parity chart gives

    |psi_s> = N^(-1/2) sum_(x in C) chi_s(F_A(x)) |logical(x)>,
    F_A(x) = A*x/2 mod Q.

At fixed public A and seed, a verified deterministic finder supplies w(t) for
t in a subset T of the effective group, with F_A(w(t))=t, or failure.
Coverage rho=|T|/G need not be uniform across matrices, and good matrices need
not be efficiently identifiable.

The complete computational-basis permutation is implemented conceptually as:

1. XOR F_A(x) into target workspace initially zero.
2. Run the fixed seeded finder, preserving its reversible computation history.
3. Verify its output and XOR a flag if valid AND x=w(t).
4. XOR the computed witness into the logical word register.
5. Uncompute witness, validity and ALL finder history using the unchanged t.

The module implements forward and inverse maps on EVERY basis value, including
nonzero target workspace and flag. Reversal uses the computation transcript,
not an inverse of the many-to-one witness function. Invalid finder outputs fail
closed and do not destroy the permutation. A bounded classical algorithm can
store and reverse its computation with polynomial overhead; a polynomial
expected-time or measured quantum routine does not automatically meet this
bounded coherent interface.

On flag1 the word register is zero and the target state is proportional to
sum_(t in T) chi_s(t)|t>. Inverse coordinate QFT yields, for EVERY fixed s,

    P(herald) = |T|/N = 2^(-Delta)*rho,
    P(correct residue AND herald) = |T|^2/(N*G) = 2^(-Delta)*rho^2,
    P(correct residue | herald) = rho.

These are not uniform-secret averages. Target-dependent garbage retained in
orthogonal states instead gives only |T|/(N*G) correct probability. Shared
randomness must be explicit, fixed across the superposed targets, independent
of the target and fault data, and every target-specific random transcript must
be uncomputed. Merely resetting or measuring such history is not equivalent.

## Source Conversion: Full Targets, Not Only Even Targets

Coverage for S(A,q,r,seed) on independent uniform r mod q does not directly
give coverage for r=2t. Use this exact parity-alignment wrapper instead.

Choose a fresh raw ORIGINAL-row syndrome sigma uniformly in F2^n. Solve B*u=sigma
on the public pivot columns, B=A mod2. For a logical target t mod Q define

    A' = D_u*A mod q, where column i is negated when u_i=1,
    r = 2t - A*u mod q.

If S(A',q,r,seed) returns a verified physical Boolean word x, set y=x XOR u.
The integer identity A*y=A*u+A'*x gives A*y=2t mod q and B*y=0. Extract its
logical word through the public free coordinates; independently verify it.

For full-rank IID A and independent uniform sigma,t, the pair (A',r) has EXACT
IID native-label and independent uniform FULL-target law conditioned on binary
full rank. Column signs depend only on B and sigma, preserve B, and permute
independent fresh higher entries. Target parity is sigma and its upper bits
are a uniform translation. Recovering sigma from r mod2 recovers u and A, so
this is a joint bijection, not only a marginal label assertion.

IMPORTANT: `compile_packet.syndrome` uses RREF row bits. They are generally NOT
the raw original-row sigma in this wrapper. `_origin` solves the original rows;
the n2 nonidentity-prefix test would detect confusing the two conventions.

This finder wrapper never requests a new unknown phase packet at labels A'.
Those labels are public classical solver input. The verified output is decoded
back into the EXISTING original-A packet.

Physical parity measurement also does not require zero-syndrome postselection.
For measured RREF syndrome with chart origin u0, its residual on logical z is
F_(D_u0 A)(Kz). `orient_measured_packet` keeps that syndrome and changes only the
public label description. Every outcome is retained. Conditional on each low
chart and syndrome, signs preserve the native IID higher-label law. Under the
fair-Z source below, parity outcomes remain uniform independent of fault masks.

Let beta be verified finder coverage averaged over UNCONDITIONED IID A,
independent uniform full target and independent seed. Binary rank failure obeys

    p_bad < 2^(n-m) = 2^(-k).

Conditioning the wrapper and then Jensen give original-attempt ideal success
at least 2^(-Delta)*(beta-p_bad)_+^2. The implementation conservatively rounds
retained coverage to beta/2 whenever p_bad<=beta/2, otherwise to
(beta-2^(-k))_+. Every failed rank attempt consumes all its original states.

For a finder promised only on GLOBALLY CONDITIONED legal (A,r) pairs, the
full Boolean preimage count D has E D=2^Delta and
E D^2=2^Delta+2^(2Delta)-2^Delta/q^n. Distinct words differ at a coefficient
of +1 or -1, giving uniform differences in every row. The second-moment bound
implies P(D>0)>=2^Delta/(1+2^Delta). Thus beta_legal times this mass is a valid
unconditional coverage lower bound. A mean of per-matrix legal ratios is a
different law. Planted or solvable-target benchmarks do NOT transfer for free.

## Noise And Completion Without IID Fault Statuses

Required source: a classical mixture of product good equatorial states and bad
computational-basis states. The status and basis-bit data precede ALL fresh
Fourier labels, solver seeds and latent gauge coins. Apply the existing prelabel
X/sign gauge and discard old labels and gauge data. Conditional on the status
data, each bad state becomes the independent fair physical Z mixture of the
ideal state. Statuses may be correlated, including across blocks, and may depend
on the fixed secret. Arbitrary entangled faults, raw unbalanced basis failures,
label-dependent fault laws and shared correlated Z coins are not covered.

For b bad states the block density contains the ideal block with weight2^-b.
Positivity of a correct-output POVM gives success>=2^-b times ideal success.
If E b<=mu, the sharp integer convex envelope is

    E[2^-b] >= 2^(-floor(mu))*(1-(mu-floor(mu))/2).

This does not require an all-good packet: exactly one bad state per packet has
all-good probability0 but ideal-component weight1/2. Independence from fresh
labels/seed is essential. The tests include an anticorrelation countermodel
where multiplying marginal ideal success and marginal survival overestimates
success.

Correct residue s mod Q leaves n final binary secret bits. Correct n+c fresh
original phase states by that residue, measure X, and solve their IID binary
linear equations. In the ideal block, rank failure is at most2^-c. Commit the
resulting full candidate BEFORE v fresh verification labels. An incorrect
candidate has average all-X-plus probability2^-v by character orthogonality;
fair balanced basis failures also give plus with probability1/2. The true
candidate is perfectly complete on the ideal component, NOT on raw noisy data.

Fault statuses can correlate every attempt, so a marginal per-attempt success
bound cannot be amplified as IID trials. Preallocate R disjoint COMPLETE blocks,
including selection, top-bit completion and verification, and promise marginal
bad-state probability gamma for each fixed secret. If a block has M original
states, set mu=M*gamma. With factor C>=2, Markov bounds aggregate fault count
above C*R*mu with probability<=1/C. On the complementary event at least
floor(R/2) blocks have at most ceil(2*C*mu) faults. Conditional on the statuses,
their fresh labels, seeds and latent gauge coins are independent, so with
p_ideal including ideal completion,

    q_good = p_ideal * 2^(-ceil(2*C*mu)),
    P(no correct verified candidate on budget event)
      <= (1-q_good)^floor(R/2)
      <= 1/(1+floor(R/2)*q_good).

Add R*2^-v for any wrong candidate passing fresh tests and 1/C for the budget
event. This analyzes every preallocated block even if operational execution
would stop early. It does NOT infer independent success from fault marginals.

Saved conditional controls use L=4n+1, gamma=1/(nL), assumed beta=1/n^2,
c=16, C=4, Delta0 or16, R=2^(40+Delta)*n^4, and v=ceil(log2 R)+32. n8/16/32
ledgers charge every original state and bound failure below1/3. The large
constant allocation is a CONDITIONAL ledger, not a practical executed solver.
Definition3.1's f1 promise matches gamma when q=2M, but finite state preparation,
discarded-data lineage, coordinate Fourier transforms, error budgets and actual
lattice reduction composition still require an independent proof. No natural
lattice algorithm is certified here. Do not extrapolate these finite ledgers
to all small n,L noise regimes without rechecking the budget.

## Attempts To Falsify This Direction

- **Rediscovery:** single verified preimages and coherent canonical filtering
  already occur in Regev. The useful change is the narrower research contract,
  not a novelty claim. An independent review may find the direct interface is
  merely a standard consequence; retain it only as a precise construction target.
- **Hardness moved, not solved:** native vector subset sum may be the entire
  hard problem. No finder with polynomial runtime and inverse-polynomial beta
  is supplied. Exhaustive tables, LLL quality plots, favorable kernels and
  fixed small moduli cannot satisfy that requirement.
- **Density:** one selected word per target pays2^-Delta. Increasing packet
  density far beyond logarithmic overhead can kill polynomial throughput even
  when target coverage is perfect. This is this filter's ceiling, not a generic
  DCP lower bound; a polynomial-list or genuinely quantum interface is separate.
- **Wrong distribution:** even-only, planted, per-label legal or favorable-prefix
  coverage can be large while native independent-target coverage is negligible.
  Require the exact wrapper law and an unconditional coverage theorem.
- **Hidden coherence cost:** measured randomized solvers, retained history,
  exponentially large advice, unknown-state reflections and target-dependent
  seeds do not pass. Supply a uniform bounded implementation and reversible
  transcript, not only a successful classical callback on one target.
- **Noise/composition:** correlated statuses are allowed only with the stated
  product-state, prelabel and independent-coin lineage. If the native source
  does not realize it, the noise result cannot be used. Polynomial preparation
  and accumulated finite-precision error must fit the actual failure margin.

## Next High-Thinking Work

Work on an ACTUAL partial arithmetic finder at m=nL+O(log(nL)), native IID
columns, independent uniform targets, L growing with n. Use the existing
conditional carry and terminal subset-sum audits to choose a new invariant;
do not repeat clean-tail obstruction refinements. Investigate compact nonlinear
carry correction, probabilistic arithmetic reconstruction with explicit shared
seed, and mathematically justified bounded preprocessing. Record verified
coverage and runtime in this source law, including failures and preprocessing.
If a proposed trick only solves planted or low-modulus instances, falsify it.
Keep quantum-only finders separate until their coherent interface is proved.

Gemini integration: expose this report and the new contract obligation in
existing proof/experiment/CLI registries; retain all claim gates and the explicit
missing-finder assumption. Run production regressions separately. No legacy
pipeline or cosmetic UI work is needed.

## Verification

Focused tests cover32 cases: whole basis maps, every small secret, invalid
outputs, original-versus-RREF syndromes, complete native source bijections,
all-syndrome retention, physical solver covariance, transcript destruction,
fair-Z survival, correlated status envelopes and anticorrelation, target legal
conditioning, completion, verification and full resource accounting.

The independent Node implementation checks160 basis states,12 fixed secrets,
48 physical fault masks,43,232 source image pairs,5 selector ledgers,5 complete
block ledgers,22 nonzero verification differences and8 dependency hashes.
These are independent code controls, NOT independent mathematical review.

    PYTHONPATH=theorems python -m pytest -q tests/test_dcp_partial_witness_readout.py
    python theorems/dcp_partial_witness_readout.py --save
    node research/certificates/dcp_partial_witness_crosscheck.js

Full production/qsearch validation is Gemini work and is not claimed here.
The combined focused regression with the direct-filter and earlier source/noise/
matching modules passes137 tests in30.22s;5 writer integration tests are deselected.
An earlier broader run exposed one existing subset-sum bridge registry-writer
failure, documented in `AGENT_HANDOFF.md`. Both reports, checkers, syntax and JSON
checks pass; the production suite is not being declared green.
