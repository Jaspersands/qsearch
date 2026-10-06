# Dimension-Free Codomain Channel Simulation

LOCAL DERIVATION / REVIEW PENDING. No independent mathematical review, novelty
claim, accepted candidate, general DHSP lower bound or algorithmic speedup.
This is a theoretical source screen with bounded physical regressions, not a
new toy oracle problem. Production integration belongs to Gemini.

## What Changed

The [earlier instrument audit](DHSP_CODOMAIN_INSTRUMENT.md) left full-dimensional
codomain encoders open because its trace-norm bound grew with sqrt(dimension).
This follow-up removes that dimension dependence for the SAME binary
uniform-domain-erasure architecture, and allows codomain-controlled operations
on incoming quantum memory rather than only fresh output vectors.

It does NOT replace quantum computation by classical computation. It replaces
coherent function evaluations in a declared source channel with CLASSICAL
function samples and KNOWN quantum processing. The subsequent computation can
still be quantum, and its time/gate cost is not claimed small unless the
original public circuits and the explicit sample-table loader are small.

## Exact Declared Physical Channel

Every call begins with a NEW domain register uniformly superposed on
K_epsilon, independent of the current memory. Compute f into a fresh value
register, apply a KNOWN unitary/isometry W_y to memory controlled ONLY by the
codomain y=f(a), then uncompute f. Project the domain onto its starting uniform
state with a binary H/F flag. Discard the domain in BOTH branches; retain all
other outputs, including encoder ancillas, memory, reference and flags.

For the conditional label distribution p, define

    M = sum_y p_y W_y,
    E(rho) = sum_y p_y W_y rho W_y^dagger,
    V(rho) = E(rho)-M rho M^dagger
           = sum_y p_y (W_y-M)rho(W_y-M)^dagger.

The complete channel has H block M rho M^dagger and F block V(rho).
V is COMPLETELY positive, not merely positive on a tested state, and

    tr V(rho) = tr[(I-M^dagger M)rho] <= tr rho.

The same statement holds with an arbitrary entangled reference. This variance
identity, not the dimension of the memory, controls the simulation error.
W_y may act on quantum program/control registers and earlier coherent memory;
it need not create a fresh codomain state or commute with other W_y.
Its CONTROLLED implementation and relative phase convention must be known.
Equal standalone quantum channels can have different controlled unitary phases:
I/-I is a saved cancellation control. A bare black-box CPTP-channel interface
does not supply those phases. W_y cannot hide extra calls to the unknown oracle.

## An Actual Classical-Query / Quantum-Processing Simulator

Draw m independent classical uniform-domain samples and evaluate f on each.
Store ONLY the output list (y_1,...,y_m) for this simulation. Values can repeat.
Keep each SAMPLE POSITION j; deduplicating values changes the source channel.

Use a known uniform-index preparation and a reversible classical-table loader:

    (1/sqrt(m)) sum_j |j> W_{y_j}|memory>.

The classical data lookup is uncomputed using j. Binary uniform-index projection
and index discard implement the empirical H/F channel. This requires no
unknown M circuit, inverse-function oracle, image-membership advice, quantum
RAM assumption or coherent evaluation of f. A sequential multiplexed loader
costs O(m*(label_bits+log m)) elementary-controlled-gate work, plus the original
known controlled-W evaluator and uniform-index preparation/precision costs.
Power-of-two m allows exact Hadamard index preparation in the ideal gate model.
Other m requires a costed preparation, not an automatic free state.

AVERAGE over the fresh sample list CONDITIONAL on the fixed underlying oracle:

    E_sample M_hat rho M_hat^dagger
      = (1-1/m) M rho M^dagger + E(rho)/m,
    E_sample F_hat(rho) = (1-1/m) V(rho).

The channel difference is the pair of blocks (+V(rho)/m,-V(rho)/m).
For any input/reference state its trace distance is tr V(rho)/m <=1/m.
For unitary controls the maximum equals ||I-M^dagger M||_operator/m. The
maximally entangled Choi test can be STRICTLY weaker: equal I/Z controls give
Choi distance1/(2m), but input|1> gives1/m. Both tests are saved.

For T calls with arbitrary quantum memory and classical adaptive subgroup
choices, an input/reference-uniform channel hybrid gives TOTAL simulation
error at most T/m for EACH fixed oracle and hidden hypothesis. Fresh sample
lists are independent conditional on that oracle; the oracle itself is NEVER
resampled. This remains true when earlier probes correlated memory with it.

For accuracy epsilon, m>=T/epsilon and total classical evaluations T*m are
polynomial in T and1/epsilon. These extra evaluations, table storage and lookup
are PAID; the simulator is not asserted to be a practical decoder. This only
removes an EXPONENTIAL coherent-query advantage attributable to this channel,
not every polynomial query improvement or a downstream computational speedup.

## Shared-Oracle Label Information: A Separate Gate

For f_s(b,x)=pi(x-b*s), index-two K_epsilon and uniform unknown fixed pi, correct
parity samples are uniform on ONE fixed unknown half subset S=pi(even). Wrong
parity samples are uniform on the whole N-label range and independent of S.
This is a LABEL-ONLY sampler: domain indices are discarded and there are no
other oracle calls or secret-correlated initial states in this information gate.

Condition on the COMPLETE classical label history and the hidden parity. Let
C contain the c DISTINCT outputs of previous correct-parity samples. Its
posterior S is uniform among N/2-subsets containing C. Wrong samples add no
constraint. The next correct-sampler response has probabilities

    2/N                         on C,
    (N-2c)/(N*(N-c))             outside C.

Its total variation from a fresh whole-range response is EXACTLY c/N.
Whenever a coupled history agrees, classical adaptive selection of epsilon
uses the same quantum memory/control operations. One hypothesis requests a
correct sample and the other a whole-range sample; the response distance is
at most t/N after t samples. Conditional quantum states are identical when
the classical histories agree because all their operations are known functions
of those histories. Thus even unlimited known quantum postprocessing cannot
increase the source-history coupling bound:

    label-only final distance <= min(1,Q*(Q-1)/(2N)).

This is a full JOINT adaptive law, not a tensor product of averaged one-copy
states. Tests compare the recursive posterior to direct uniform-subset
marginalization, with label-parity and collision-feedback selectors.

## Dimension-Free Parity Screen

The simulator uses Q=T*m labels. Apply the simulation hybrid to BOTH hidden
parities, then the label-information gate:

    D(original_0,original_1)
      <= min(1, 2*T/m + min(1,(T*m)*(T*m-1)/(2N))).

Equal-prior parity success is at most (1+D)/2. Any separately certified total
comparison error epsilon_0+epsilon_1 adds to D. The gate needs secret-independent
initial memory and no additional source/oracle access. The dimension of memory,
full label register or known W_y circuits does NOT appear.

For T=n^2, power-of-two m near (2N/T)^(1/3), the report saves exact rational
distance bounds; displayed decimal values below are only approximations:

| n | Samples Per Call m | Ideal Distance Upper |
|---|---|---|
| 32 | 256 | 1 (vacuous) |
| 64 | 262144 | 0.062499999971 |
| 128 | 274877906944 | 1.49011612e-7 |
| 256 | 1208925819614629174706176 | 1.35525272e-19 |

These large lists are ANALYTIC COUNTERFACTUAL SIMULATION costs used for a
bound, not resources supplied for free to the actual 2T-query probe algorithm.
Alternatively take m=T*n^2: for polynomial T the distance is bounded by
2/n^2 plus an exponentially small sample-collision term with polynomial
simulation overhead. Optimizing the analytic tradeoff gives order
T^(4/3)/N^(1/3), hence a LOCAL, architecture-scoped N^(1/4) call requirement
for constant bias. This is not a tight bound or a lower bound for general DHSP.

## Required Falsifiers And Countercontrols

1. **Not a general oracle theorem.** For the two promise shifts s=0 or1, chosen
   classical domain queries (0,0),(1,0) distinguish perfectly by equality.
   They are NOT the random label-only sampler. Domain-retaining operations,
   domain-dependent W_{a,y}, coherent subgroup choices, nonuniform/chosen domain
   preparations, interleaved oracle algorithms and other side states remain open.
2. **Not independent nuisance.** A two-call tag-adaptive, entangled-reference
   control has a shared-versus-resampled state difference greater than0.1 in
   Frobenius norm. Both matrices are retained, with every flag and failure.
3. **Not a heralded pure-image shortcut.** For a full orthogonal label encoder
   over an M-element image, true herald is1/M. Empirical averaged herald is
   1/M+(1-1/M)/m, and its normalized accepted pure-target overlap is
   m/(m+M-1). At M=2^127,m=2^34, full-output error is below1e-9 while conditional
   overlap is below2^-90. Small unconditional error does NOT license rare-branch
   postselection or contradict the range-qualified index-erasure barrier.
   That large-range theorem is NOT applied to this half-of-N-label example.
4. **Not a natural-source converse.** Structured pi, useful label semantics,
   correlated side information or different subgroup images invalidate the
   uniform-half-subset information gate. The channel simulation still holds
   pointwise for any p, but quantum processing of CLASSICAL natural data may
   still be algorithmically useful. Specify a reduction and matched classical
   computation rather than calling classical-query access classical computation.
5. **Not a mathematical review.** Independent-language arithmetic and bounded
   physics regression support the algebra, not novel-theorem or peer-review
   status. Review CP variance, reference-assisted norm, adaptive conditioning,
   loader implementation and source-interface premises independently.

## Research Consequence

Do not spend another candidate generation pass on arbitrary codomain encoders
inside this same binary domain-erasure template merely because the output has
many qubits or memory persists across calls. Those formerly open loopholes are
now screened under explicit source assumptions. Pursue a genuinely different
domain/codomain interference primitive, or a natural structured source whose
label semantics survive a consequential reduction and stronger classical attacks.

The [domain-retaining collision walk](DHSP_DOMAIN_COLLISION_WALK.md) now tests
one actual outside-template primitive with reversible preparation and oracle-only
verification. Its current pilots fail matched baselines; separate local-driver
and oracle-independent-marker bounds do not extend this channel simulation to
arbitrary retained-domain algorithms.

The 2023 CFIP definition and reduction remain UNOBTAINED/UNVERIFIED, as documented
in `research/literature_audits/dhsp_codomain_instrument_sources.json`. This
channel audit does not refute a conditional CFIP theorem whose interface has
not been read. Obtain its full text before treating it as a research primitive.

## Reproduction And Integration

```
python -m pytest -q tests/test_dhsp_codomain_sample_simulation.py
python theorems/dhsp_codomain_sample_simulation.py
node research/certificates/dhsp_codomain_sample_simulation_crosscheck.js
```

Report: `research/classical_baselines/dhsp_codomain_sample_simulation.json`.
New focused tests:33 passed. The independent Node checker verifies159 empirical
sample tuples,1152 exact channel entries,6656 adaptive label probabilities,
768 complex physical entries,6144 exact adaptive-memory entries and6 scaling
ledgers, plus the rare-herald counterledger.

Gemini: expose the report next to the earlier codomain audit; register only
scoped negative results and proof-review debt. Preserve the access distinctions,
all failures, chosen-query countercontrol and nonclassical downstream disclaimer.
No candidate acceptance, theorem certification, generic dequantization, UI
cosmetic work or full production validation is performed by this theory pass.
Related focused regression:144 passed,3 production writer/runner tests deselected
in6.22s. Python/JS syntax and3 strict JSON records pass. The known production
writer omissions are not fixed, and no full-suite or qsearch validation is claimed.
