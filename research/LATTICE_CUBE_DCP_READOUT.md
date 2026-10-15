# Actual Lattice Parent To Opaque Noisy DCP Registers

The clean public cube evaluator now has in-place position embedding, positive
position QFT, signed cell measurement, and Fourier-label measurement while
retaining the colour qubit. Compilation and numerical sampling use ONLY the
public basis, prime/residue/coordinate guess, width/box, and offsets. They
never look up a short vector, hidden shift, clean flag or cell preimages.
This implements a known source reduction mechanism, not a new algorithm.

The known FULL phase-parent inverse is available, but applying it to a
normalized specified cell/label branch returns all-zero with that branch's
joint Born probability, not1. A dense gate-level inverse test verifies this.
It does not price sampling ANY good cell or rule out other coherent algorithms
that use public geometry and the unmeasured full parent.

## In-Place Embedding And Exact Instrument

For b=log2M, reinterpret each coordinate's ORIGINAL b wires followed by one
zero padding wire as a base-2M digit. The QFT's ordered wire list therefore
represents x(a)=sum_i a_i*(2M)^i. No second copy of a is made, so no copied
position register remains to destroy coherence. Noncontiguous logical
wire ordering is intentional; physical routing costs are not certified.

Measure the signed cell outputs F(t,a), apply QFT_N to the position wires,
then measure label k. These act on disjoint cell/position registers, so the
same conditioned instrument follows from a coherent parent with QFT and
joint final cell/label projection. The retained colour state has unnormalized
density entries

    rho_(r,k)[t,u] = 1/(D*N) sum_(a in C_r,t) sum_(a' in C_r,u)
                          exp(2*pi*i*k*(x(a)-x(a'))/N), D=2M^n.

The trace is the joint Born probability, not uniform over cells. For valid
two-point fibres, labels are uniform, good cells yield the phase qubit with
common shift x(a1)-x(a0), and singleton cells yield bad basis states. All
cells, labels and zero-probability branches remain in the exact reference.
Invalid same-colour/multipoint fibres may bias the label distribution and
are refused by the DCP operation backend, NOT reclassified as ordinary bad
registers. Under this source geometry, discarding public cell information
gives the balanced-bad marginal already established in the source audit.

Exact reference arithmetic uses Phi_N(X)=X^(N/2)+1 for dyadic N. It is
bounded and PRIVATE calibration machinery, not an efficient preimage oracle.
The compiler and emitter do not call it. A separate JS checker reconstructs
all public lattice inputs and the full exact instrument independently.

## Numerical Snapshot Trap Found And Guarded

With installed Aer0.17.2, a naive conditional qubit snapshot after cell/label
measurements can still return an averaged premeasurement density while
measurement memory lists different labels. Conditional snapshots also key
on internal classical-register bits; using only one feed-forward bit can
coarsen the keys even after forcing shot execution. Such data are invalid
as individual DCP registers and are explicitly rejected.

The diagnostic circuit uses a WHOLE-register zero condition for a public Z
frame, saves the qubit snapshot, then undoes that frame. This forces actual
shot-conditioned simulation and stores all measured bits in the snapshot
keys. Undo the recorded frame when reconstructing the final private density.
Both frame gates are included in the diagnostic circuit; the physical final
qubit is unchanged. The ordinary source readout circuit needs no snapshots
or simulator workaround. A mandatory guard rejects deferred sampling,
missing/coarsened keys, or snapshot multiplicities differing from the actual
shot transcript. It must remain in place across simulator upgrades.

Every shot is charged as a fresh source preparation and function evaluation.
The MPS simulator uses zero configured truncation threshold and no imposed
bond cap, but floating-point evolution/SVD is NOT a certified channel error
bound. Every emitted calibration qubit is compared to its exact conditioned
instrument with tolerance1e-7; disagreement yields UNKNOWN, never a speedup.
The127-qubit source is compiled only, not numerically simulated. Simulator
size caps do not prove classical hardness or quantum advantage.

## Opaque Operations And Honest Scope

Public receipts contain IDs, modulus, measured label, public cells and source
ancestry, not density matrices, phases, shortest vectors or good/bad flags.
The diagnostic backend supports destructive X/Y/Z measurement and a genuine
two-register CNOT/target measurement. Both parents are consumed; a single
actual branch is sampled with its density-derived probability. No cloning,
same-register pairing, overlapping ancestry, or free postselection is allowed.
An emitted batch can be claimed only once; copying a batch or live backend
and reopening a claimed batch are rejected. Diagnostic RNG seeds are trusted
experiment settings, NOT receiver-selected physical randomness or chosen-label
access. Receivers get the already-created operation interface and may not
construct new backend worlds, reset RNGs or inspect private simulator state.
Unresolved numerically rare branches consume inputs and yield UNKNOWN rather
than an invented normalized state. Python privacy is an access-model contract,
not a security sandbox; private matrices in artifacts are marked audit-only.

Source shots are independent CONDITIONAL on the declared fixed public source
parameters. This does not prove independence for every reduction, unknown
shared offset, extra noise channel, or reused physical register. Public basis,
offset and cell access are retained: these are stronger resources than opaque
copy-only DCP. A uniform hidden-shift prior is NOT inferred from the source.

Finite shape validity, numerical f1 bad-rate budget, and full growing-family
Regev promise are separate fields. A nontrivial-shift small control violates
the f1 budget and stays a high-noise DIAGNOSTIC. Other controls have shift0
and no hidden-shift information even when their noise budget passes. Public
LLL solves these integer lattice calibrations. None is an algorithm candidate.

The next scientific task is a robust receiver operating on these actual
registers under their real access/noise contract, with serious classical
baselines. The source alone supplies no receiver, speedup, novelty or no-go.
