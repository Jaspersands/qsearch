# Normal-Character Measurement Is Not Free Central Descent

LOCAL DERIVATION / REVIEW PENDING. Exact channel scope, no general quantum
lower bound, novelty claim or native receiver. This cuts a tempting shortcut
after `NATIVE_STATE_HSP_BRIDGE.md`, not the coherent alternative.

## The Concrete Shortcut

Take M actual native phase qutrits at level r with known labels a_i in
(O/(pi^r))^n and one shared secret s. Write

    F(x)=sum_i lambda_(x_i)*a_i,
    psi_s(x)=3^(-M/2)*chi_s(F(x)).

The known translation action is diagonal with frequency

    E(x)=sum_i zeta^(x_i)*a_i = sum_i a_i + pi*F(x).

Measure the normal subgroup K=pi^c A, hoping to skip r-c central levels in
one step. Its character is E(x) modulo pi^(r-c). This observable is computable
by public ring arithmetic: no secret oracle is needed. But when c<r-1 this
is generally NONCENTRAL, so it is not the benign last-centre measurement.

Let C_eta be the words with the same observed character. The COMPLETE
channel, including the recorded outcome, is

    sum_eta |eta><eta| tensor P_eta |psi_s><psi_s| P_eta.

Every outcome has raw probability |C_eta|/3^M, independent of s. Conditional
states retain coherence only within C_eta. A dense class or a large original
batch does not restore coherence between different eta outcomes.

## Exact Precision Loss, For Every Label Cohort And Batch Size

Within one C_eta, E(x)-E(y) is divisible by pi^(r-c). The displayed identity
implies F(x)-F(y) is divisible by pi^(r-c-1). Therefore for EVERY
delta in pi^(c+1) A,

    chi_delta(F(x)-F(y))=1.

The phase difference between s and s+delta is constant inside each class.
Their complete measured output density operators are IDENTICAL, even with
the character outcomes retained. Any further secret-independent processing
of those outputs cannot distinguish these secrets. The result holds for
every fixed public label cohort, not only in expectation over random labels.

For the actual integer-embedded secret at modulus3^ceil(r/2), the remaining
precision is at most ceil((c+1)/2) trits per coordinate. Under a uniform full
secret prior, any decoder using ONLY these measured outputs succeeds with
probability at most

    3^(-n*(ceil(r/2)-min(ceil(r/2),ceil((c+1)/2)))).

Unlimited disjoint batches measured in this same way do not break the alias.
Extra untouched original states are NOT covered. A preceding arbitrary
noncommuting operation can change the character/phase relation and is also
outside the scope. This is not a lower bound on all sample-only algorithms.

At c=r-1 the subgroup really is central and the alias ideal is pi^r A=0:
there is NO nontrivial loss from this theorem. At c=2, measuring gamma_3
retains at most TWO integer trits per coordinate, not just the one trit
retained by a homomorphic class2 group projection. The two interfaces are
different and must not share an incorrect bound.

## Coherent Retention Is A Genuine Escape, Not Yet A Decoder

Compute the character into a clean register WITHOUT measuring it:

    |x>|0> -> |x>|E(x) mod pi^(r-c)>.

This public isometry preserves all original inner products and all secret
information. The r6 integer secrets0 and9 can have distinct original states
and distinct coherent outputs while their measured normal-character outputs
are exactly identical. Cross-character phases are the lost resource.

This operation leaves the original word register and all its correlations.
It does NOT cleanly erase a fiber, prepare normalized conditional states,
rank/unrank words or implement a class2 quantum source. Tracing out that
word register destroys the off-character coherence in this simple encoding.
A useful compiler must explicitly mix characters, transform the word
workspace or otherwise read the cross-character phases. A known hash
computation followed by a frequency QFT is not such a compiler by itself.

This points back to the source-weighted erasure and coherent-multiplicity
targets, while ruling out a new route that merely measures the deep normal
characters and advertises a reduced nilpotency class.

There is a POSITIVE public eraser for the COMPUTED character pointer: measure
it in its conjugate Fourier basis. Outcome b has probability1/|K| even for
reference-entangled inputs. The word state acquires the known diagonal
byproduct chi_(E(x))(b)^*. Apply its PUBLIC inverse, which is a known normal
translation action, to restore the entire original joint input. No unknown
state-preparation inverse is used. This is ordinary measurement/feedforward
algebra, not a new algorithmic discovery. It cannot undo an already recorded
computational-basis normal-character measurement, and it does not erase the
original word register or reveal the secret.
The byproduct has a precise native meaning: since E=A0+pi*F, a normal
translation b in pi^c A shifts the phase secret by -pi*b, up to a common
phase. These shifts lie in the SAME pi^(c+1) alias ideal erased by the
computational normal-character measurement. Known feedforward reverses
them. This identity concerns public normal actions, not a reusable oracle
for arbitrary unknown secret phases.

In fact the reduced computed-pointer density operator is diagonal, with
weights |C_eta|/3^M, independent of s. ANY measurement confined to that pointer
alone therefore has a secret-independent outcome law. Joint operations on
the word and pointer are outside this statement. The required positive
advance is such a costed cross-character/inter-word operation, not choosing
a different pointer readout basis and calling its outcomes a decoder.

## Verification And Falsifiers

The producer replays ALL words, character classes and raw outcomes for six
actual native source channels, including two secret dimensions, central and
noncentral cases. Rational phase differences certify exact aliases; complete
complex density matrices independently replay the trace distance. Explicit
non-alias controls retain visible information, so the result is not a code
path that always reports erasure. Large precision ledgers are symbolic,
not extrapolated numerical fits or group enumeration.
Three full conjugate-basis controls retain arbitrary reference entanglement,
replay all81 outcomes each, and apply known feedforward. The independent
exact checker verifies the operator identity, not just a density-table fit.

Reject wrong normal-dual quotient dimensions, dropped outcomes, unknown
state inverses, phase differences computed at the wrong root, claims that
the full word workspace disappeared, and promotion of the measured-channel
bound to a coherent or arbitrary-receiver lower bound. Physical IID and
input errors are inherited from the actual source, not certified by indices.

The native group/phase source is the one in
[Boucher--Fouque--Shen, Sections2.3/3](https://arxiv.org/html/2609.34996v1).
The exact pinching-alias and coherence comparison here are LOCAL channel
calculations, not asserted source-paper theorems. External review remains.
