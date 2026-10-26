# Hybrid Reversible Workspace For The Hermite Decoder

2026-10-21. Constructive resource proposal with classical field-operation
reversal controls. Not a compiled quantum circuit, independently reviewed
theorem, novelty certification or admitted algorithmic advantage.

## Decision From The Proof Audit

The starting question was whether a conservative decoder's acceptance set
breaks moment transfer. The source's
[Claim 5.4, equation (5.8)](https://arxiv.org/html/2610.01902v1) already states
the identity for every vector supported on isolated labels. Our accepted
set is a subset of those labels: uniqueness in the affine superspace
certifies uniqueness in the entire guarded ball. Restriction to that subset
therefore preserves the identity. Its additional rejected mass must still
be bounded, as in HERMITE_PINNED_DECODER.md.

This does not require inventing a new moment theorem. The remaining
resource question is more substantive: the previous proof applied a
logarithmic reversible-simulation overhead to every large work array.
Most of those arrays need not be copied into checkpoints.

## Proposed Bound

Retain the decoder's parameters, strict guarded interpolation condition,
and independently chosen random pins. Let q be prime, ell<q, differential
order s<ell, K=ell*(q-1)/2, M=(q-1)*(ell-s), and u=s+2.

The proposed input-preserving decoder uses polynomial(q,ell,s) time with
an absolute polynomial degree and reversible workspace

    O(((s+2)^2*q*ell + s^2*ell^2*log(q*ell))*log q).

The first term pays persistent arrays AND their explicit row-operation
history. The second pays recursive checkpoints of the small streamed
echelon state. No checkpoint contains a full regenerated coefficient vector.

Under the additional sufficient condition

    ell*ceil(log2(q*ell)) <= q,

the total becomes `O((s+2)^2*q*ell*log q)`. For fixed s this is
`O_s(q*ell*log q)`, the same asymptotic space scale as the original
streaming construction, with target-dependent constants.

Combine this with the parameter theorem only in the intersection of their
domains. In particular it includes sufficiently large fixed ell above
the accuracy-dependent threshold, and ell=floor(q^a) for every fixed
0<a<1 eventually. It does NOT include ell=1 via this decoder, arbitrary
multiplicity, or an unconditional removal of every logarithmic overhead.

## 1. Explicit Interpolation History

The compact decoder maintains a u-by-u polynomial basis. Each polynomial
has degree at most M+K-1. Allocate fixed coefficient width

    L = M+K+1.

For each scalar interpolation constraint, record the chosen pivot row
and the u elimination factors. The pivot factor is zero by convention.
If using the incremental local jet cache, also record the u coefficients
discarded by shifting its pivot row. There are exactly M public
constraint slots, including no-ops. Thus this history costs
`O(u*M)` field elements and `O(M log u)` index bits.

Forward operations are:

    B_i <- B_i - factor_i*B_p,  i != p;
    B_p <- (X-a)*B_p.

To reverse, first undo the pivot multiplication, then add the recorded
multiple of the restored pivot to each nonpivot row. Restore shifted-away
cache entries from the recorded tails. The old basis/cache then determines
the pivot, factors and tails again; XOR their computed encodings out of
the record. This clears history coherently, rather than deleting it.

At each point boundary the jet cache equals the jets of the CURRENT
basis. It can be uncomputed from that basis and rebuilt when reversing.
The implementation verifies these boundary identities in both directions.
Alternatively, one may recompute every discrepancy from the basis and
avoid this cache history, at a larger polynomial time cost.

### Multiplication Must Have A Reversible Extension

Ordinary polynomial multiplication by X-a increases degree, so writing
"multiply then discard overflow" would not justify a unitary.
Here a is a nonzero field point. Multiplication by X-a modulo X^L is a
bijection on the FULL fixed-width register: its matrix is lower triangular
with nonzero diagonal -a.

For coefficients x_0,...,x_(L-1), execute

    for j=L-1,...,1: x_j <- -a*x_j + x_(j-1);
    x_0 <- -a*x_0.

The inverse first rescales x_0, then solves upward. Each assignment is an
invertible modular multiply-add. On every valid intermediate polynomial,
the public degree bound ensures no overflow, so the modular operation
equals ordinary multiplication. On other encodings it remains a bijection.
The case a=0 is excluded and tested.

The Python trace uses trimmed polynomials as a diagnostic representation;
its fixed-width primitive is tested separately on every vector in F_3^3.
It is not a physical register allocator or gate compiler.

## 2. Row Reduction Also Has Bounded History

For shifted weak-Popov reduction, record receiver, donor, monomial shift
and field factor for each cancellation. The inverse adds the monomial
multiple back. On the restored old basis, the deterministic collision
choice reproduces that record, allowing it to be cleared.

Let w be the existing shift vector. Each cancellation strictly reduces

    u*shifted_degree + leading_position

for one row. Every shifted degree is between -(K-1) and M, so at most
`u^2*(M+K)` cancellations occur. Each record has O(log(q*ell)) bits:
one field factor and a constant number of indices. Since ell<q, this
logarithm is O(log q). Publicly pad to the bound, using no-op records
after termination. This is polynomial time and `O(u^2*q*ell*log q)`
history space, already within the basis scale.

Row/degree selection is computed coherently from the retained basis, not
measured. A scan can retain its prefix indices for at most u^2*L
coefficients, copy the selected record, then reverse the scan before
changing the basis. This temporary O(u^2*L*log L) workspace is reused
at each step and fits the same bound because log L=O(log q). It is not
a separate full-basis snapshot for every cancellation.

Monomial row additions are reversible with the donor and factor retained,
even on fixed-width coefficient arrays. Valid executions do not overflow.
Polynomial row reduction itself is established work; see
[Mulders--Storjohann](https://cs.uwaterloo.ca/~astorjoh/jscpopov.pdf).
This note only accounts for its use in the proposed coherent decoder.

Copy the selected interpolant into its output register while the basis is
available. Uncompute the selection scan, then reverse all row operations
when that interpolant is no longer needed. Do not erase the selected
polynomial prematurely.

## 3. Which Large Computations Need No Checkpoints?

### Public Right Inverse And Dual Map

The cardinal polynomials and local dual matrices depend only on public
q,ell and the fixed information set. They can be generated classically,
one at a time, in O(q*ell) field storage with polynomial time. The
classical controller applies their coefficients as modular multiply-adds
to the retained syndrome and blank output registers.

This is not input-dependent advice: the coefficients have explicit
generation algorithms from earlier notes. Their classical storage counts
toward the space bound. They are independent of the quantum input, so
discarding public generation scratch does not decohere the syndrome.
The syndrome-dependent output remains and is uncomputed by reversing the
same linear transformation. No dense global right inverse is stored.

Local matrix inversion is likewise a public computation. An ell-by-ell
local matrix fits O(q*ell) field elements because ell<q.

### Triangular Coefficient Vectors

Keep the selected differential operator as an immutable quantum input.
For each degree t descending, the coefficient f_t is either a specified
free coordinate or a function of the operator and higher coefficients.
Compute that function and add it to the initially zero f_t register.

To clean the vector, visit t in ASCENDING order and subtract that same
function. Higher coefficients are still present when needed. Division
occurs only on the nonzero-pivot branch; free positions use their
specified values. The earlier Frobenius directions remain free.

For a row oracle, compute one vector, accumulate the requested residual
or pin evaluation into the scalar output, then reverse the vector sweep.
Repeat for the offset and each direction. At most O(K) coefficient
scratch is present; no K-by-z direction matrix is stored.

The control copies full vectors only to compare their values with the
reference solver. That diagnostic copy is not what the proposed row
oracle retains: it keeps only its scalar evaluation.

## 4. Checkpoint Only The Small Echelon State

There are at most `z=s*ceil(K/q)` provisional free coefficients.
Process all residual identities and all pin equations in a public order.
Do not stop early without checking the remaining equations.

The mutable state consists of an echelon system with at most z rows and
z+1 columns, pivot indices, rank and an inconsistency flag. It has
`O(z^2 log q)` bits. The selected operator, offset polynomial, syndrome,
pins and public parameters remain read-only inputs to this stage.

Allocate for the PUBLIC upper bound z, not a measured input-dependent
dimension. The actual number of free coordinates is a coherent field in
the state, with unused slots masked. Likewise process a public upper
bound on identity degrees, including trailing zero equations. No array
allocation, loop termination or classical branch may reveal the syndrome.

For one transition:

1. Generate its equation row with the clean row oracle above.
2. Reduce it against the OLD echelon rows. Keep the intermediate reduced
   row after each elimination; there are at most z such rows, costing
   O(z^2) field scratch.
3. Compute a copy of the next echelon state, including a normalized new
   row or an inconsistency flag.
4. Reverse the reduction and row generation, leaving only the old state
   and the new state.

This supplies a clean evaluation of one deterministic transition with
`O(K+z^2)` field scratch. The large row-oracle scratch is zero on return.
No ordinary irreversible row drop is treated as a free quantum operation.

Now use binary reversible checkpointing on E such transitions, padding E
to a power of two. To compute a segment of length 2h:

    compute its midpoint state in a blank checkpoint;
    compute the final state from that midpoint;
    reverse the first computation to clear the midpoint.

There are O(log E) simultaneously live checkpoints and `3^ceil(log2 E)`
leaf-transition evaluations, which is polynomial in E. A single clean
transition workspace is reused at the leaves; it is NOT replicated at
every recursive level. Read-only inputs are not checkpointed either.
This is a direct form of
[Bennett's reversible simulation](https://doi.org/10.1137/0218053).

Here E=poly(q,ell,s), with fixed polynomial degree. Since s<ell<q,
`log E=O(log(q*ell))`. The stage therefore uses

    O(K + z^2*log(q*ell)) field-equivalent storage.

The final coordinates and error are computed and copied to the decoder's
output, and the whole stage is reversed. Finally reverse interpolation
and the syndrome conversion. The result is input-preserving and clean
on all valid encodings. Invalid encodings must have totalized branches;
all schedules are padded to their public bounds.

This is a constructive scheduling proof, not an executed full gate-level
checkpoint network. That distinction remains a review obligation.

## 5. Combined Space And Consequences

Combining the explicit interpolation trace, public arithmetic, clean
coefficient generation and small checkpoints gives

    S = O((u^2*q*ell + s^2*ell^2*log(q*ell))*log q).

The term O(K) and all classical controls are included in the first term.
Both the q*ell-scale basis and the z^2-scale checkpoints can coexist
within this sum. The blanket extra log factor is not charged to the
large basis a second time.

For the uniform schedule s=8m-2 and
ell*ceil(log2(q*ell))<=q, this becomes

    S = O(m^2*q*ell*log q).

Thus the earlier growing family ell=floor(q^a),
m=floor(q^(a/4)), 0<a<4/7, has the proposed bound

    O(q^(1+3a/2)*log q)

instead of the preceding log-squared bound. More importantly, for every
fixed approximation target and sufficiently large fixed multiplicity,
the proposed construction is polynomial-time with O_alpha(q*ell*log q)
space, not merely polynomially enlarged workspace.

This is a restricted response to the similar-space decoding question.
It does not resolve ordinary OPI or all fixed multiplicities. All failure,
pin loss, precision and classical-comparison conditions from the previous
notes remain. Reading N entries still takes time proportional to N.

## Falsifiers And Executed Controls

- A degree overflow in a valid interpolation path invalidates the use of
  the fixed-width polynomial multiplication as ordinary multiplication.
- Removing a cached tail can prevent exact uncomputation. The negative
  test changes a tail and the reverse audit rejects the execution.
- A history record is reversible data, NOT an authentication certificate.
  Changing a nonzero cancellation factor can reconstruct a different valid
  original basis. A zero factor inconsistent with an actual cancellation
  is rejected. Both cases are tested.
- Copying the clean row-oracle scratch into every checkpoint restores the
  old overhead and invalidates the tighter bound.
- A retained batch of K-by-z directions or an uncharged public inverse
  matrix invalidates the storage accounting.
- The q31/ell24 native control does NOT satisfy the sufficient logarithm-
  absorption inequality. It validates reversal, not the asymptotic region.
- No physical fault tolerance, quantum gate counts or independent proof
  review are supplied by the classical trace.

Native input: the SAME received word as the independent module certificate,
q31, ell24, K360, s4, guard10. All 600 interpolation records reverse,
the basis returns to identity, and every local cache boundary checks.
The leading profile matches the independent CRT basis after ignoring row
order. The offset and all 12 provisional direction vectors match the
reference and clean their scratch. Standalone controls exercise row
cancellation even though this native interpolation needs no final
cancellations.

Producer: `theorems/hermite_reversible_workspace.py`.
Artifact: `research/reductions/hermite_reversible_workspace.json`.
Earlier producers and reports are preserved.

12 new / 104 connected tests pass in 42.52 seconds, with RuntimeWarning
fatal. Python and site JavaScript syntax, site checks and registry
validation pass. The full repository suite was not run. SHA256 checks
confirm all five preceding Hermite producers and reports are unchanged.

## Next Research Decision

The coherent-moment restriction is a direct use of existing prior art.
The present resource improvement is also assembled from established
reversible techniques. Its end-to-end correctness and novelty still need
adversarial review, particularly the clean transition interface and
quantifier scope of the same-space comparison. Do not label this as a
Shor-level or practical result.

Avoid an unconditional quantum promotion or a native-size campaign.
The useful next question is whether the exact polynomial-time,
same-space Hermite statement is already an immediate corollary of known
decoding results, and whether any missing control invalidates the
proposed coherent schedule.
