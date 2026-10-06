# Full Bell Source Moments: Correlation Is Not A Decoder

Status: **LOCAL DERIVATION / REVIEW PENDING**. No independent review, novelty,
efficient inference, sample-complexity, typical-source, or speedup claim.
Read `research/DCP_CORRELATED_BELL_READOUT.md` for the physical circuit and
the distinction between joint output and a selected parity.

The new result challenges our own narrow negative direction. Exponentially
weak individual parities do NOT establish weak full-output structure. The
whole Fourier spectrum can retain substantial correlations, including at
growing modulus. The unresolved problem is computationally extracting the
shared secret from varying native examples, not plotting a promising moment.

## Fixed-Low Source Identity

Let q=2^t>=8, Q=q/2, and condition on the public low labels B, initial syndrome
charts and a Bell XOR outcome u. The left and right packets have common logical
width k and N=2^k. Their remaining label entries Z=(A-B)/2 are IID uniform in
Z_Q, in both packets. Take a fixed secret s with at least one odd component.
No identical-state copies, chosen labels or oracle are used.

Write p_s(v|u,A) for the FULL conditional Bell distribution. For h in F2^k,
stack all physical rows K_i of both charts for which K_i.h=1, and let R(h) be
their binary rank. Define

```text
D = #{(h,j): (K_1 h) AND (K_1 j)=0,
              (K_2 h) AND (K_2 j)=0},
C = E_Z [N sum_v p_s(v|u,A)^2].
```

Then the exact source identity is

```text
D = sum_h 2^(k-R(h)),
C = D/N = sum_h 2^-R(h) >= 2-1/N.
```

It is independent of u, the syndrome origins, the fixed odd secret and the
modulus within q>=8. It is a HIGH-LABEL SOURCE AVERAGE, not a property of every
fixed public label matrix or a bound on secret mutual information.

### Fourth-Moment Derivation

Expand the fourth power of the Bell amplitude. Averaging a higher-label entry
gives a cyclic character sum. Because s has an odd component, a quartet
(z1,z2,z3,z4) survives iff, in EACH physical coordinate of EACH packet,

```text
x(z1)+x(z3)-x(z2)-x(z4) = 0 mod Q.
```

The integer difference is in {-2,-1,0,1,2}. Since Q>=4, this means integer
zero. Injectivity of the chart implies z1+z2+z3+z4=0 over F2: equality of
physical XORs is equality of logical XORs. Put z1=z, z2=z+h, z4=z+j,
z3=z+h+j. Integer equality in a coordinate holds exactly when its h and j
flip masks do not overlap. Origins and the right XOR offset can change only
the sign of a nonzero difference, not whether it vanishes.

Every surviving quartet also has ZERO fixed-low phase difference: the phase
is linear in the physical bits before restriction, even though it becomes
a high-degree logical carry polynomial. Hence every surviving term equals
one, with no unproved cancellation assumption. There are N D quartets.
Normalization gives E|amplitude|^4=D/N^3. Every v has the same averaged
fourth moment, yielding the stated C.

For fixed h, allowed j form the common kernel of the selected physical rows,
of size 2^(k-R(h)). The 2N-1 pairs with h=0 or j=0 give the universal lower
bound. The same calculation gives E_Z tau_s(u,h)^2=2^-R(h) for a single
parity, even at q>8 where its exact per-label derivative is not quadratic.
This strengthens the earlier Parseval inequality to equality.

The modulus and secret conditions matter. At q=4, differences of +/-2 vanish
modulo Q=2, producing additional terms. An all-even secret may similarly see
a smaller effective modulus; the zero secret produces a deterministic v.
The implemented certificate explicitly refuses q=4 and flags the odd-secret
precondition. Extending to other secret valuations requires using their
effective character modulus, not silently reusing this theorem.

## Exact Native Systematic-Source Mean

For independent native low-label matrices of size n by 3n, retain the public
event that EACH first n-column block is invertible. Its exact probability is

```text
P_prefix = [product_(j=1..n) (1-2^-j)]^2.
```

This is a constant-probability source filter, NOT free conditioning. Charge
both rejected quantum batches and their public labels. On this event the
canonical kernel chart has k=2n free coordinates and n IID uniform pivot rows,
independently in each packet. The event is secret-independent. Syndrome choices
do not change these kernel rows.

Disjointness of physical free coordinates requires h AND j=0. Among the
3^k such ordered logical pairs, 2N-1 have a zero member. Every other pair has
two linearly independent directions. A uniform pivot row has their two inner
products jointly uniform; it avoids (1,1) with probability 3/4. There are 2n
independent pivot rows across the two packets. Therefore

```text
E_(B | prefix) C = 2-1/N
                    + [(3^k-2N+1)/N] (3/4)^(2n), k=2n.
```

The leading contribution grows as (9/8)^(2n), unlike the one-bit dictionary
information upper bound. At n=1 the COMPLETE 16-systematic-pair control gives
65/32. This expression remains valid at q=poly(n); no growing-degree likelihood
algorithm is inferred from the expression.

## Attempt To Kill The Interpretation

**Mean versus typical source.** A large average may come from rare bad public
matrices or rare output spikes. No variance, tail concentration, bounded
likelihood-ratio or typical-instance result is supplied. It could be useless
for every efficient protocol on most native sources.

**Output structure versus unknown parameter information.** Collision measures
nonuniformity over v for fixed s. It does not compare different secrets. A
distribution could have the same spikes for all secrets; its collision would
be high while its secret information was zero. Do not log C as recovered bits,
query advantage, Bayes success or a speedup metric.

**Computational inference versus statistics.** Even identifiable distributions
can require exponential secret search, phase evaluation, rank optimization,
or fiber inversion. The mask-sum certificate enumerates 2^k possibilities and
has a hard default cap. The analytic native mean is polynomial arithmetic,
but not an algorithm for finding an informative mask or decoding a transcript.

**Negation ambiguity.** The uncorrected packet state for -s is the complex
conjugate of that for s. CNOT, Hadamard and computational measurement are real.
Consequently p_s(u,v|A)=p_-s(u,v|A) EXACTLY for all labels and moduli. The same
holds for classical-history adaptive protocols composed only of real quantum
operations. For a uniform Z_Q^n prior, maximum full-identification success
from such transcripts alone is at most

```text
(1 + (2/Q)^n)/2,
```

because there are (Q^n+2^n)/2 negation orbits. This is an identifiability gate,
not a hardness theorem. Public complex phase correction, Y-sensitive readout
or legally costed verification of a decoded +/- candidate can break the
symmetry. Those capabilities are permitted research targets, not implemented
decoders here. Do not extend the gate to arbitrary measurements.

### Legal Known-Candidate Verification Repair

If the reduction supplies FRESH ORIGINAL phase states
(|0>+exp(2 pi i A.s/q)|1>)/sqrt(2) with IID native public A, commit to a known
candidate c BEFORE seeing their labels. Apply the public diagonal rotation
exp(-2 pi i A.c/q) on |1>, then H and computational measurement. It returns
zero with probability [1+cos(2 pi A.(s-c)/q)]/2. Correct candidates pass with
certainty in the ideal model. For ANY fixed nonzero difference, cyclic
character orthogonality over the native labels gives mean acceptance 1/2.
Thus M fresh tests accept an incorrect committed FULL original-secret candidate
with probability exactly 2^-M. If a decoder already returns a FULL original
secret orbit {c,-c}, this resolves the sign with error at most 2^-M unless the
two candidates are identical modulo q. A packet residue is NOT such a full
candidate: the first parity chart has lost the highest original bit in each
coordinate. The interfaces below handle that distinction.

This uses a known public phase rotation, NOT an unknown preparation inverse
or secret oracle. The symbolic certificate computes the character image order
q/gcd(q,s-c) without exponential enumeration. It does not reveal s-c to an
actual verifier; that difference is only a proof/calibration parameter. Test
probabilities do not require it at execution time.

Candidates selected after inspecting verification labels, chosen favorable
labels, or reusing training registers do not get this soundness theorem. A
committed list of L candidates costs L*M fresh registers with union bound
L*2^-M. This interface is unavailable if only carry packets, not original
phase states, are supplied. Noise and finite rotation precision require a
separate completeness/soundness budget; an aggregate measurement variation
bound eta changes the transcript error bound by at most eta. The implemented
certificate claims only ideal noiseless exact measurement, not that missing
noise guarantee. Candidate verification does not construct candidates.

### Packet-Residue Verification And Lost-Bit Completion

For a known residue candidate r modulo Q=q/2, a fresh native packet can be
corrected by the KNOWN public diagonal exp(-2 pi i r.F(z)/Q), followed by H^k
and measurement of all logical qubits. Correct residues return all zero with
certainty in the ideal model. For every fixed nonzero residue difference,
averaging the fresh higher labels kills every off-diagonal overlap term:
injectivity gives a physical coordinate with difference +/-1, and a nonzero
secret-difference component supplies a nontrivial cyclic character. Mean
false acceptance is exactly 2^-k, conditional on ANY low chart and syndrome.
No odd-secret condition is needed. M fresh packets give 2^(-kM) when widths
are fixed; variable widths require their actual sum in the exponent.

The residue candidate must be committed before seeing fresh higher labels;
discarding unfavorable labels or recycling training packets is not covered.
Implement the known public phase using the carry evaluator with reversible
arithmetic; this is not an inverse for the unknown state. A q=8, three-input,
two-logical-qubit control exhausts all 64 higher-label tables for every
residue difference, including the even difference. This only VERIFYs a
candidate or distinguishes a proposed +/- residue orbit; it does not find one.

The module supplies a simpler explicit correction plan: for each physical
coordinate compute x_i=a_i XOR K_i.z into ONE reusable clean ancilla, apply
diag(1,exp(-2 pi i (sum_l r_l A_li)/q)), then uncompute it. Repeat across m
coordinates. This realizes exp(-2 pi i r.F(z)/Q) up to a known global phase.
It uses at most 2 sum_i wt(K_i) CNOTs, 2 wt(a) X gates and m known rotations,
not an exponential logical polynomial expansion or inverse fiber compiler.
Masks and modular angle numerators are serialized as hex integers. Algebraic
phase identities are tested, including a 64-logical-qubit plan; actual physical
backend execution and approximate rotation precision are not certified.

Once the CORRECT residue r=s mod(q/2) is known, fresh ORIGINAL phase states can
be corrected by exp(-2 pi i A.r/q). The remainder s-r=(q/2)b is binary, so
Hadamard measurement yields the exact equation (A mod2).b. With n+lambda fresh
states, classical GF(2) elimination recovers b except on a rank-deficiency
event bounded by (2^n-1)2^(-n-lambda)<2^-lambda. Charge these states separately
from residue discovery and verification. Incorrect residues, noisy samples or
imprecise correction do not satisfy this noiseless equation guarantee.

Thus a hypothetical efficient packet decoder up to negation can be completed
with independently costed residue verification and high-bit equations, IF the
reduction actually supplies the necessary fresh inputs. The difficult and
UNIMPLEMENTED component remains discovering the residue without enumeration.

**Fixed-modulus distraction.** q=4 and q=8 already have polynomial-resource
known methods. An improved constant-modulus estimator alone is not the goal.
Only source-preserving inference through growing modulus, including sample
consumption and natural-problem reductions, could justify further promotion.

## Revised Priority

The full-output path remains OPEN, but collision is only a representation
diagnostic. Next theory should compare candidate-secret laws, locate a
constructible sufficient statistic or alignment map, and test whether its
inference reduces to a known hard matrix-pencil/fiber problem. If the only
method is exhaustive secret scoring, record the obstruction and do not build
an attractive new benchmark around it. A complex-sensitive final verification
interface must be part of any eventual full decoder.

This note uses the correlated Bell primitive as an explicit mechanism, not as
a transfer of identical-state learning. The cited source-model barriers and
learning literature are in the companion note. All new equalities here need
independent mathematical review, regardless of the arithmetic controls.

## Artifacts And Checks

`theorems/dcp_full_bell_source_moments.py` supplies the capped rank-sum
certificate, exact systematic-source mean, full q=8 root-count controls and
growing-modulus quartet constraints. The live report is
`research/phase_workbench/dcp_full_bell_source_moments.json`.

```sh
python theorems/dcp_full_bell_source_moments.py --save
python -m pytest -q tests/test_dcp_full_bell_source_moments.py
node research/certificates/dcp_full_bell_source_crosscheck.js
```

Controls exhaust 4,096 higher-label tables at two XOR outcomes, checking exact
full probabilities and negation invariance; 1,024 quartets across q=8,16,32,128;
16 systematic low-label pairs; and eight exact scaling/source-probability rows.
These are bounded arithmetic certificates, not independent theorem review.
Production CLI/registry wiring and full regression remain Gemini work.
