# Constructive native-input selection: no new survivor

13 November 2026. STATE/TRAPS read first. Two externally motivated domains
were screened with corpus been-tried and baselines before proposal. No
network, API, Git, tests, infrastructure, or shared-status edits were used.
**Recommendation: zero paid operations.** I did not find an explicit new
operation that closes either native algorithm. The boundaries below are
selection decisions, not general impossibility or hardness statements.

## A. Bayesian syndrome decoding from an explicit parity-check matrix

**Native problem.** Input a full-row-rank binary LDPC matrix H, a syndrome
s, and rational crossover p in (0,1/2). Return a sample within TV epsilon
of

    P_s(e) = 1[He=s] p^|e| (1-p)^(n-|e|) / Z_s.

All arithmetic, matrix access, and random bits are charged. There is no
supplied quantum channel output, hidden codeword, posterior state, or
decoder oracle. This posterior is directly relevant to soft decoding and
uncertainty quantification. Producing a maximum-likelihood error or proving
reliable communication beyond a specified threshold would be separate
claims; posterior sampling alone does not assert either.

**Concrete operation considered.** Prepare the public product state with
amplitudes sqrt(p^|e|(1-p)^(n-|e|)), coherently compute H e, and measure its
actual syndrome y. Gaussian elimination supplies a right inverse R of H.
The reversible shift v=R(s-y) moves every basis vector to the requested
syndrome. The missing operation is an amplitude-consistent transport from
the resulting state to the posterior for s, implemented from H,s,p alone.
Unlike a supplied optimal decoder, the shift itself is a real native circuit.

The exact post-shift amplitude at e in the requested coset is proportional
to sqrt(P(e+v)), not sqrt(P(e)). Thus the required correction is

    sqrt(P(e)/P(e+v))
      = (p/(1-p))^((|e|-|e+v|)/2).

A controlled rotation implements a scaled version of this ratio, but
does not give its acceptance probability for free. Its ratio can span
((1-p)/p)^|v| over legal errors. No uniform polynomial acceptance or
alternative deterministic transport was obtained. Direct projection of the
original product state simply pays Z_s. On the legal easy input H=I,
s=1^n,p=1/4 this is 4^-n, although the posterior is a known point mass.
This rejects that preparation argument, not the transport architecture
on every instance and certainly not a general classical algorithm.

**Why existing receivers do not supply the operation.** The retained
COHERENT_BPQM_TREE.md LF20–60 gives actual parity/equality operations on
binary channel states and explicitly refuses reuse of one physical input
when a tree is unrolled around a cycle. LF64–74 requires exact full-code
root optimality for the commuting-on-code-span conclusion. Neither fact
gives the required fixed-syndrome amplitude transport on a general LDPC
graph. The native product preparation above does not create unknown-bit
channel states as extra advice. Replacing this step by a PGM or a conditional
partition-function oracle would only rename the unresolved computation.

**Target and strongest classical attack.** A useful target would be
poly(n,inputbits,1/epsilon) full-TV sampling on a stated growing-treewidth
family, with no rare-syndrome assumption. Classical sum-product/dynamic
programming handles trees and bounded treewidth; information-set decoding,
Stern/Dumer-style improvements, and Gibbs/importance methods must be matched
to any genuinely proposed noise and code promise. The corpus names these
baselines and the prior USD--Prange matching route. No new such promise or
constructive transport has survived here, so no gap/normalization prompt
is justified. A constant-expansion statement alone would not supply it.

**Cheapest falsifier for a future explicit proposal.** Compute its complete
conditional amplitude law after the syndrome shift, including the real
normalization and every retained record. If it samples P(e+v) instead of
P(e), or assumes that each check may receive a fresh copy, reject it before
any decoder benchmark. This is already a precise algebraic interface test.
Actual source priority, if a new circuit appears, should start with the
Mandal et al. BPQM source cited by the retained note and the exact
USD--Prange comparison. Their full theorems were not newly imported here.

## B. Planar statistical-mechanical partition functions via unitary circuits

**Native problem.** Input an explicit planar graph, a fixed spin count q,
and rational edge interactions. A physically useful output is a relative
approximation to the positive-temperature Potts partition function, or a
full-TV spin sample. Knot-theoretic complex evaluations are a related but
different endpoint. Graph and coefficient input lengths, output accuracy,
and any precision needed for analytic continuation are charged.

**Concrete operation considered.** Compile a unitary transfer/braid circuit
at a quantum-evaluable complex point, estimate its normalized partition
amplitude, and use analytic continuation or coefficient reconstruction to
obtain the real-temperature conditional partition functions needed for
sequential sampling. This is an attempted change of operation, rather than
assuming a Gibbs state or a partition-function oracle.

The first operation is a known Tutte/Jones quantum-estimation direction,
not a new algorithm. Its native guarantee must retain its circuit-dependent
normalization and additive error. The proposed second operation has no
uniform precision/normalization proof here. A bound of the form

    |Z_hat-Z| <= epsilon * A_graph

only gives relative error delta when epsilon <= delta*|Z|/A_graph.
Neither that ratio nor the conditioning of continuation/prefix extraction
is supplied by the unitary circuit. No new contour, scaling, or adaptive
procedure was derived that pays all of these quantities. Consequently the
known complex additive endpoint cannot be promoted to the physical sampler.
This also does not refute a different constructive partition algorithm.

**Baselines and source boundary.** Exact transfer-matrix/tensor contraction
at small width, planar zero-field Ising methods, and the established
positive-weight approximate-counting regimes are the first comparators.
Their parameter scopes must be matched to q, signs, field terms and error;
no blanket classical matcher for every Potts regime is asserted. The
relevant primary requests would be the Aharonov--Jones--Landau estimator
and Aharonov--Arad--Eban--Landau Tutte algorithm, with their EXACT additive
normalizations, followed by the matched real-temperature classical source.
Without a new continuation operation, fetching them is only priority
confirmation and does not justify paid mathematical work.

The corpus hit ANYONIC_BRAID_GROUP_HSP_COMMUTANT_BARRIER.md is not an
authority for the above scopes. Its LF201–210 mixes normalized Jones
estimation, knot classification, and sweeping HSP conclusions; none is
imported. I did not turn a word-problem algorithm or a weak-Fourier
limitation into a theorem about the partition endpoint.

## Disposition

The exact corpus queries were "quantum low density parity check decoding
Tanner expander coherent alternating syndrome projectors soft decoding"
and "native graph chromatic polynomial Tutte Jones anyonic quantum additive
approximation planar graph complex temperature". Their relevant topic
hits were read. Both proposed completions need an operation I have not
constructed; asking agents to supply an unspecified missing theorem would
repeat the old pattern. No new survivor, speedup, hardness result, or
implementation is claimed. The completed LC, matroid and Slater results
remain untouched; this selection does not reopen their adjacent variants.
