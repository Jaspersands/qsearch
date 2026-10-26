# Signed Trine BPQM: A Certified Constructive Entry Point

2026-10-20. Exact arithmetic with a local physical-degradation derivation,
INDEPENDENT REVIEW PENDING. Known BPQM mechanism, not a novelty claim or a
new quantum algorithm. No finite-block receiver or sampler is executed here.

## Question And Change Of Direction

The previous graph-coloring pass had variable degree TWO. Its all-depth rank
calculation was not a decoding-error guarantee, and its binary root-gap
transplant failed. Do not try to rescue it by making larger density tables.

Instead test the native signed trine channel on random-coefficient regular
LDPC codes with variable degree THREE and check degree SIX. Genuine branching
at variable nodes permits a doubly exponential fidelity tail. The channel is
still mu=(0,1/2,1/2), overlap -1/2; no positive-overlap replacement or copies.

An exploratory population calculation suggested convergence. It is NOT the
certificate: finite-pool dependencies, rare branches and floating rounding
make such a simulation insufficient. The saved result is deterministic,
integer-accounted, one-sided channel degradation plus an analytic tail bound.

The q-ary local operations and density framework are prior art in
[Mandal--Pfister](https://arxiv.org/abs/2601.21330). The
[q-ary LDPC block theorem](https://arxiv.org/html/2609.05857v1#S6), Theorem30,
already gives asymptotically vanishing ensemble-average block error inside its
BPQM success region at dv>=3. This pass certifies a concrete channel's tree
entry condition; it does not invent that theorem or independently verify its
proof. The ensemble must include its independent uniform nonzero socket
coefficients, parallel sockets and possible matrix dependencies.

## Physical Simplex Degradation

For any normalized nonnegative spectrum mu, the source is

    psi_(mu,x) = sum_j sqrt(mu_j)*omega^(xj)|j>.

Suppose mu=sum_h p_h*nu_h EXACTLY, with p_h a probability law. Define a
frequency-controlled isometry by

    V|j> = sum_h sqrt(p_h*nu_(h,j)/mu_j) |h>|j>.

For mu_j=0 all numerators are zero; complete that unused column arbitrarily
and orthogonally. Normalization gives V-dagger V=I. Consequently

    V psi_(mu,x) = sum_h sqrt(p_h)|h> psi_(nu_h,x).

Dephase the flag h, keeping every block. This is an explicit channel from the
original source to the heralded mixture of grid channels, so it can only
WORSEN discrimination. It is not nearest-grid rounding and has no statistical
confidence parameter. Four actual complex-amplitude isometries and dephased
block controls include an off-grid singular channel and unequal full-rank
spectra. This establishes the comparison's direction independently of the
density calculation.

Triangulate the probability simplex on denominator G. Every spectrum is a
convex combination of at most three neighboring grid vertices, found by
integer division in two coordinates. The weighted spectra match EXACTLY,
including zero coordinates. G divisible by six contains both the physical
trine and the perfect channel exactly. Do not average states or overlaps and
assume that the result is physically ordered.

This is a CQ PERFORMANCE comparison. Dephasing these flags inside a future
coherent decoding/uncompute algorithm would generally be WRONG. The comparison
certifies the original ideal BPQM recursion, not a compiler made from rounded
channels or discarded environments. Cyclic spectral gauges are likewise used
only for CQ density statistics, not to clear branch-dependent phases for free.

## Integer Node And Probability Accounting

For input grid numerators a,b with sum G, bit-node weights are their cyclic
convolution with total G^2. A check branch h has weights a_(j+h)*b_j and total
d_h. When its normalized spectrum is simplex-split, the d_h denominator
cancels the branch's probability d_h/G^2. Every transition therefore has a
COMMON denominator G^2 and integer numerator weights. Zero branches remain
exactly zero; nonzero small branches are never silently truncated.

Message probabilities are integer weights summing to 2^80. After every
transition, round weights DOWN and send all leftover probability to the
completely uninformative point-spectrum channel. That is another physical
degradation, not renormalization of retained favorable mass. Coefficient
averaging implements the real uniform F_3^* factors and accounts for its own
dyadic loss. No chosen signs or coefficient-blind theorem substitution.

Positive binary Gram/affine-erasure no-gos are not verdicts here: a flagged
grid channel is generally still a nonorthogonal qutrit channel, not a positive
uniform-affine-subspace instrument with a matched classical sampler.

Mean fidelity is a weighted square root of the exact Eisenstein norm
(a^2-ab+b^2)/G^2 of the off-diagonal Gram entry. Integer square roots supply
OUTWARD rational bounds. Symbol-error bounds are outward as well. No floating
eigenvalue, population estimate or fitted exponent enters the certificate.

## Executed Certificate

Settings: dv3,dc6,G24, probability precision80 bits, fidelity precision80 bits.

- First level is independently exactly F_1=961/2048. Each five-input check
  remains a trine with probability1/16, otherwise a point spectrum.
- At level13 the degraded channel has mean fidelity <=0.006332239.
- Let r=dc-1, p=dv-1, f be this rational upper bound and
  A=(1/2)*(((1+2f)^r-1)/f)^p. The published q-ary bound implies
  lambda=A*f^(p-1)<0.333064<1. All inequalities are evaluated rationally.
- Since the polynomial quotient is increasing, induction on the ORIGINAL
  unrounded recursion gives F_(13+t)<=f*lambda^((p^t-1)/(p-1)). Thus fidelity
  and symbol error tend to zero; this is not support-rank decay alone.
- The exact comparison performs169750 message-pair visits. Its largest saved
  density law has32 states. This compact calculation does NOT execute the
  11,111,111,111,111 distinct original outputs of that extrinsic tree.

The same nominal rate at dv4,dc8 does not automatically certify: the bounded
control remains UNKNOWN. A small iteration budget also reports UNKNOWN.
Neither outcome proves failure or impossibility. No parameter/seed hunt is
used to manufacture the dv3,dc6 certificate.

Under the cited theorem's assumptions and this LOCAL comparison derivation,
the result supplies the missing SUCCESS-REGION premise for the known
asymptotic decoder. It does not provide numerical finite-N block error,
a physically compiled reliability register, a gate budget or a sampling
reduction. Those obligations remain separate and unpromoted.

## Natural Computational Target And Classical Tests

Let H be the code's sparse parity-check matrix, with M code coordinates and
V=M/2 check rows. Given public independent offsets J in F_3^M, seek or sample
x in F_3^V such that every entry of J+H-transpose*x is NONZERO. Sockets in a
column have degree three, so this is a natural sparse linear-constraint CSP,
not an oracle puzzle. Parallel sockets are summed modulo three, not removed.

For C=ker H and a basis matrix G of C, the target is equivalently
y in{1,2}^M with Gy=GJ, followed by an ordinary uniform affine lift to x.
Empty inputs and gauge multiplicity must be retained. For uniform J the
expected number of x solutions is 3^V*(2/3)^M, not a SAT promise. The bounded
live producer saves original sockets, aggregated H-transpose and all offsets.

Z3 on the SAME public inputs finds a verified witness at V16/M32, seed711;
V32/M64, seed712 reaches its one-second limit and is UNKNOWN. No filtering,
changing offsets or timeout-as-hardness inference. SAT is a SEARCH baseline,
not a uniform sampler or evidence that sampling is hard. No quantum sampler
was run on either input.

A separate actual anti-trine POVM yields the classical exclusion record
channel P(z|u)=0 for z=u and1/2 otherwise. Its Shannon capacity is exactly
log2(3)-1 bits/use. The dv3,dc6 code has rate at least log2(3)/2 bits/use;
Fano therefore prevents reliable word recovery from THIS fixed product
readout even with unlimited classical postprocessing. This comparison
motivates collective decoding, but does NOT exclude other measurements or
classical CSP/search/sampling algorithms. It is not a classical lower bound
for the natural computational problem.

## Try To Kill The Direction

1. **Wrong information order.** Exact Gram identities, actual isometries,
   independently recomputed node laws, directed roots and lost-mass checks
   must all agree. Tests include singular boundaries and opposite coefficient
   orientations. Reversing a comparison invalidates the entire certificate.
2. **Wrong ensemble.** The degree-three random-coefficient socket model is not
   the preceding graph cycle code, a simple-hypergraph-conditioned source,
   dense IID matrices, or a designed polar code. Do not import those results.
3. **Coherence or source costs.** A performance certificate does not implement
   phase-correct reliability arithmetic, a coherent whole-block receiver or
   its adjoint. No decoder success postselection, cloned leaves or free source
   inverses are allowed.
4. **No natural reduction.** A binary positive-temperature DQI sampling theorem
   cannot simply be asserted for this signed, singular q-ary source. Derive
   the actual unconditional q-ary decoder-to-target map, including empty
   sectors, normalized versus unnormalized comparison states and average-J
   error, before claiming even a conditional sampler.
5. **Classical algorithm wins.** SAT witnesses, local heat bath, algebraic
   constraint solvers, tensor contraction and uniform/approximate CSP samplers
   must be compared on the SAME ensemble and target distribution. A single
   product-measurement capacity obstruction is nowhere near sufficient.
6. **Known result.** BPQM decoding is published work. Any useful consequence
   may already be known, or may have easy classical sampling in this density
   regime. No novelty, numerical breakthrough probability or speedup claim.

## Next Scientific Task

Second follow-up: TERNARY_CLASSICAL_SAMPLING.md now finds exact complete-pool
classical uniform samplers on BOTH saved16/32-spin inputs. The old Z3 timeout
is not evidence of hardness. Its count/planting analysis also removes global
count estimation as the advantage metric under this same decoding premise.
Only uniform CONDITIONAL sampling and the growing coherent receiver remain
meaningful targets; no asymptotic classical sampling theorem is inferred.

Follow-up,2026-10-20: TERNARY_DECODED_SAMPLER.md now supplies the unconditional
q-ary reduction argument, actual bounded coherent BPQM gates, public source
preparation and polynomial affine lift. It preserves empty inputs and all
work registers. That removes the first task below at the LOCAL REVIEW-PENDING
level; it does not supply the growing, precision-paid receiver or a speedup.
The remaining priority is that receiver and stronger matched classical samplers.

First derive and test a full UNCONDITIONAL q-ary decoder-to-constrained-product
sampling reduction for this ensemble, keeping empty targets and every work
register. Then either construct the actual phase-correct receiver with paid
precision, or kill the target with a stronger classical sampler. Do not spend
another pass on finer threshold plots now that a sufficient premise exists.
Routine CLI/registry exposure stays in the mechanical handoff; no accepted
candidate, central proof or negative record is automatically admitted.

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python theorems/ternary_bpqm_certificate.py --write
    python -m pytest -q tests/test_ternary_bpqm_certificate.py

Artifact: research/phase_workbench/ternary_bpqm_certificate.json. Its hashes
bind the producer and the two imported local theorem modules.
