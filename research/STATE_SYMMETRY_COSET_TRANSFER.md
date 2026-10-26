# State Symmetry To Restricted Coset Sources

2026-10-22: REES_PROJECTIVE_STATE_SOURCE.md proposes a simpler copy-only
route for explicit exponent-p groups of ANY FIXED class c<p and LINEAR
action. Public zero-moment Rees evaluations cancel unknown scalar-support
characters with at most (c+1)! copies per block, independent of p. It
requires neither conjugate copies nor state-preparation inverse. This
extends the written interface, NOT independent receiver correctness,
general projective representations, or mixed-state conjugation symmetry.
The existing source-distance planner is reused after the new phase-erasure
lemma; projective_pair=False alone still does not erase arbitrary phases.

2026-10-21. LOCAL REDUCTION / REVIEW PENDING. The reduction below supplies
an access interface; it does not prove the proposed higher-class HSP
receiver, establish novelty, or give a classical-hard application. Tensor
amplification and polar orthogonalization are standard tools, not the
prospective contribution.

## 1. The Question And The Input

Can the proposed arbitrary-subgroup receiver learn NONNORMAL symmetries
of supplied quantum states without assuming a classical hiding oracle?
For the strict Bose overlap promise, the written answer is yes, provided
the receiver consumes only fresh reduced coset sources on public address
maps. This includes learned restrictions and legitimate quotients, not
just samples from the original ambient group.

Input: a finite group G with public efficient coordinates/arithmetic,
|G|<=N, IID copies of one density operator rho on q qubits, and an
efficiently controlled LINEAR representation R of G. Promise:

```
H = {g : R(g) rho = rho},
Tr(rho R(h)) = 1                 for h in H,
|Tr(rho R(g))| <= 1-gamma         for g outside H,  0<gamma<=1.
```

The two descriptions on H agree: expectation one of a unitary forces it
to fix the support of rho pointwise. This is left-action (Bose) symmetry,
NOT the condition R(g)rho R(g)^dagger=rho. The gap is a GLOBAL supplied
promise, not certified by a few sampled overlaps. Its inverse is charged.
The controlled action must work on coherent addresses; classical access
to g -> R(g), copies alone, or varying labeled DCP packets do not suffice.

The group here is not automatically one covered by our HSP proposal. The
conditional application uses the precise explicit-coordinate class-four
contract, or FIXED c<p with [gamma_3(L),L']=0 in
QUADRATIC_NONCENTRAL_HSP_SCOPE.md. Neither arbitrary groups nor growing
nilpotency class inherit an efficient solver from this transfer.

## 2. An Actual Source, Not An Overlap Table

Let D be a public address set of size d<=N with reversible representative
map r:D->G. Prepare |D>, take k FRESH IID copies of rho, apply R(r(a)) to
each copy controlled by address a, uncompute representative workspace and
discard the state copies. The address density matrix is exactly

```
sigma_k[a,b] = Tr(rho R(r(b))^dagger R(r(a)))^k / d.
```

Compare with tau[a,b]=1/d if r(b)^(-1)r(a) is in H, and zero otherwise.
Tau is the output of an ideal ordinary hiding-function query with its
output discarded. Its existence does not reveal H or construct labels.
On equal fibers the coefficient is exactly one; on different fibers its
modulus is at most eta=(1-gamma)^k. Therefore

```
||sigma_k-tau||_F <= eta,
TD(sigma_k,tau) <= sqrt(d)*eta/2 <= sqrt(N)*eta/2.
```

The inequality is a proof bound; the implementation never constructs the
exponentially large density matrix or Gram matrix. At gamma=1 the source
is exact using a single copy. For nontrivial N the looser bound
(N-1)*eta also suffices, and is shared by the unitary comparison below.
For N=1 the source is exact.

If D is a subgroup S, this is the usual coset state for H intersect S.
If K is a KNOWN normal subgroup of S with K<=H, D can encode S/K and r
can be any fixed public section. The fibers are those of (H intersect S)/K.
The section need not be a homomorphism, and R(r(a)) need not form a
representation on the entire workspace: equality on the occupied support
is enough. This does NOT learn K for free or allow quotienting by an
unknown subgroup.

The comparison with an ideal ordinary hiding source also holds for any
other public map r into G, even on a bad adaptive history; it simply may
not describe a valid quotient HSP there. Public size/circuit clocks and
malformed-chart rejection remain mandatory. This permits an ordinary
hybrid argument without assuming every earlier inference was correct.

## 3. Which Receiver Operations Are Covered?

The matrix and scalar image receivers in this repository use the original
hiding oracle to prepare reduced uniform coset states, then act only on
those registers. Their later coherent shears, QFTs and joint measurements
are channels on the prepared packets. Source trace distance is contractive
under the WHOLE channel, including rejection and classical records.

The known nil-2 dependency also fits this source interface in the
explicit exponent-p setting: [Ivanyos--Sanselme--Santha, Section 4,
Lemma 4](https://arxiv.org/pdf/0707.1260) uses the original hiding output
only to prepare a random coset, then uses public group operations. The
latent coset representative need not be read. Section 3 restrictions and
normalizer quotients need fresh sources on their representative maps;
those are exactly what Section 2 provides. Their abelian finishes likewise
discard labels. This is an interface audit, not a new nil-2 algorithm.

Thus, CONDITIONED ON correctness of the proposed ordinary receiver and
its written caps, its explicit-coordinate class-four and structural
higher-class versions transfer to mixed-copy Bose symmetry learning.
There is no need for A^dagger, purification, conjugate preparation, a
chosen Fourier label, or p identical central sectors for this route.
It supersedes the polynomial-in-p same-sector bottleneck of the older
cyclic/vector-centre construction AS AN ASYMPTOTIC INTERFACE argument;
it does not retroactively validate its native implementations.

For class two this uses an EXISTING solver, so a growing-prime StateHSP
corollary is not evidence for novelty of our higher-class proposal.
Do not transfer this paragraph to a black-box setup algorithm that needs
different access, or to any solver that reads hiding-label bits, reuses a
consumed source, or invokes a source-preparation inverse.

## 4. Full Error And Resource Ledger

Let B be a deterministic cap on ALL original source calls in the complete
amplified workflow, including failed trials, both nil-2 calls, every
restriction/quotient and all image calls. A budget for just the first
matrix image is not B. Choose exact rational error allocation delta and

```
ell = N.bit_length(),
b = ceil(log2(4*B/delta)),
k = ceil((ell+b)/gamma),        or k=1 if gamma=1.
```

Then eta<=exp(-gamma*k)<=2^(-ell-b), and
B*(N-1)*eta<=delta/4. Sequential replacement of fresh packets bounds the
total output-distribution error by this quantity, INCLUDING classical
adaptive histories and ABORT. This does not bound error after arbitrarily
rare postselection and renormalization; retries must be within B.

Cost: B*k original state copies and B*k controlled representation calls,
plus public encoders and uniform-address preparations. The copies for one
discarded-label packet can be processed sequentially with the SAME address
register, so they need not all be stored at once. Subsequent receiver
packet storage is unchanged and is still charged. In particular,

```
k = O((log N + log B + log(1/delta))/gamma).
```

The overlap gap can destroy efficiency if it is exponentially small.
Known polynomial state dimension is not assumed, but efficient preparation
or physical acquisition of the q-qubit input IS charged. Approximation of
the source, action, coordinates and all receiver gates is additional:
if each fresh-copy/controlled-action channel pair has uniform trace/diamond
error at most e, a conservative addition is B*k*e, plus address/receiver
errors. Marginally correct but correlated copies do NOT meet that premise.

theorems/state_symmetry_coset_transfer.py implements this exact parameter
ledger only. It does not certify the promise, construct sources, execute
the HSP receiver, or establish the cap B for a caller.

## 5. A Separate Pure-State Unitary Interface

If psi=A|0> has actual unitary preparation AND inverse access, the
controlled tensor-label preparation U can be compared to a genuine
quantum hiding procedure in operator norm, not just on uniform addresses.
This stronger lemma is optional; Section 3 does not require it.

Take one actual vector v_C=(R(g)psi)^tensor(k) for each left coset C.
Let X have these M<=N columns and K=X^dagger X. With t=(M-1)*eta<1,
Gershgorin bounds ||K-I||<=t. The POLAR comparison Y=X K^(-1/2) has
orthonormal columns and

```
||X-Y|| = ||K^(1/2)-I|| <= t/(1+sqrt(1-t)) <= t.
```

Each <v_C,y_C>=(K^(1/2))[C,C] is positive real. A two-plane unitary V_C
maps v_C to y_C with ||V_C-I||=||v_C-y_C||<=t. Consequently

```
U_ideal = (sum_g |g><g| tensor V_(gH)) U,
||U_ideal-U|| <= t,    ||U_ideal^dagger-U^dagger|| <= t.
```

The ideal zero-target labels form a quantum hiding set. The comparison
unitary is a PROOF WITNESS ONLY: no coset enumeration, Gram inversion or
unknown label decoder is implemented. A B-call forward/inverse hybrid
costs at most B*t in output trace distance, including entangled inputs.
This is NOT a compiler for a classical XOR oracle. A caller must be valid
for quantum hiding procedures with arbitrary orthonormal labels and
arbitrary unitary completion away from the designated zero target.
Mixed copies alone do not supply U or U^dagger. Inverse uses, if present,
must count in B and in the charged preparation/action calls.

## 6. Projective Pure-State Symmetries Need Different Access

This section describes the conjugate-copy route, not an impossibility
theorem for copies alone. TWISTED_STATE_SYMMETRY_RECEIVER.md now proposes
a separate route for the explicit fixed-class, class(L')<=3 LINEAR-action
setting: keep character-twisted sources, learn known-subgroup characters,
and recurse through character-preserving normalizers. Its full receiver
is under review and unimplemented. It does not authorize ignoring phases
in this note's ordinary-coset transfer or extending to arbitrary groups.

For H_proj={g:R(g)psi=e^(i theta_g)psi}, phases inside H_proj break the
strict Bose promise. If ACTUAL copies/preparations of psi* and controlled
R(g)* are available, use

```
chi = psi tensor psi*,       T(g)=R(g) tensor R(g)*.
<chi|T(g)|chi> = |<psi|R(g)|psi>|^2.
```

T is a representation even when R has a scalar projective cocycle: the
cocycles cancel. Its Bose stabilizer is exactly H_proj. An outside
absolute-overlap gap gamma becomes 1-(1-gamma)^2, at least gamma. One
paired copy costs TWO source preparations and TWO controlled actions.
The planner requires an explicit conjugate-access declaration but cannot
verify that a caller really has it. A public classical gate description
may permit conjugate compilation; unknown copies and A^dagger ALONE do
not grant complex conjugation.

For a LINEAR R, after H_proj is genuinely learned, its phases form a
one-dimensional character. Its Bose kernel can be recovered using ordinary
abelian Fourier sampling on H_proj/[H_proj,H_proj] with original copies
and public representatives. On each address the state acquires precisely
that character, so no small real-part gap from nearby roots of unity is
needed. This uses a supplied efficient abelian chart and the correctly
learned H_proj, not filtering a list of generators by their individual
phases. For projective R that character argument needs a separate lift;
do not assume it automatically.

For mixed rho, rho tensor rho* with T has overlap |Tr(rho R(g))|^2.
It concerns scalar left-action on the support, NOT general conjugation
symmetry. Example: rho=I/2 commutes with Z but Tr(rho Z)=0.

## 7. Literature Dependency Traps And Negative Controls

[Holt--Subramanian v2, Section 8.2](https://arxiv.org/html/2609.38085v2#S8.SS2)
uses R'(g,j)=omega^(-j)R(g) on G x Z_E and asserts an outside absolute
gap for its phase graph. That assertion cannot be imported here: for
R(e)=I, (e,1) is outside the exact graph but has overlap modulus ONE.
Tensor powers do not reduce it. Their abelian phase-exception result in
Section 8.1 is a different promise; it is not this strict-gap source lemma.
This is a local premise mismatch, not a claim that all their results fail.

The following generator-filtering instruction in that section is also
insufficient in general. In additive F_5^2, generators (1,1),(2,1) have
nonzero second coordinates, but their difference (4,0) is a nontrivial
element of the phase kernel. One must compute the kernel/intersection.
No external correspondence or correction submission was made.

Replacing conjugation by inverse action is another rejected shortcut.
On S3 with psi=e_1, choose g=(12), h=(23). Then gh psi=g psi, whereas
the inverse-paired vectors for g and gh are orthogonal. R tensor R^-1
does not generally respect group multiplication. Conjugate pairing does.

Tests also show that two copies with the correct I/2 marginals can be
classically correlated so Tr(rho_pair (Z tensor Z))=1, rather than the
IID value zero. This would invent a symmetry. The small permutation-group
tests, partial traces, quotient sections, polar rotations and phase
counterexamples are falsifiers of the access lemma, not proposed hard
oracle families or empirical speedup benchmarks.

## 8. Attempt To Reject The Application

- [Bouland--Giurgica-Tiron--Wright, Fact 3.3](https://people.eecs.berkeley.edu/~jswright/papers/hidden-cut.pdf)
  already amplify orbit-state orthogonality with tensor copies and compare
  Fourier statistics with ordinary HSP. Our trace-distance/restriction
  bookkeeping applies that established mechanism to this receiver; it is
  not an independent quantum-algorithm discovery. Novelty would have to
  lie in a VALID higher-class receiver and a useful scope consequence.
- [Liu--Carrasco--Eisert--Bellante](https://arxiv.org/abs/2609.35656) already
  distinguish copy and unitary access and give optimal abelian sample/query
  bounds. Our conservative transfer is not an abelian improvement and
  does not achieve their square-root-in-gap query dependence.
- Efficiently simulable preparations/actions, explicit small state spaces,
  stabilizer states and low-width tensor networks need their direct
  classical or established quantum learners checked first. Failure of one
  baseline does not establish a separation. A classical comparison must
  specify equivalent input access, not give one side an exponential table.
- The sparse-Pauli subsection of CLASS_THREE_APPLICATION_AUDIT.md now
  explicitly reduces supplied nilpotent Clifford conjugation symmetries
  to phase-colored finite-field set stabilizers. Defining-characteristic
  p-group instances are classically polynomial-time, even for large p.
  This does NOT expose unknown copies' coefficients or simulate arbitrary
  controlled Clifford actions on nonstabilizer inputs.
- Planting a known coset state or a known symmetry into a preparer gives
  a control, not a hard natural input. An unknown laboratory state supplies
  a learning problem but is not a classical-input factoring-style result.
- Exponential gap loss, source acquisition cost or receiver resources can
  make a mathematically polynomial reduction useless. Existing image-query
  exponents are already very large; this note does not improve them.
- A receiver step that inspects hiding labels, needs an unavailable inverse,
  or conditions on a rare event outside the fixed cap falsifies the claimed
  copy-only composition. A failure of the higher-class receiver also kills
  its corollary, even though the standalone source bound remains correct.

NEXT: independently challenge the full receiver and seek a genuinely
motivated state family with paid controlled action, inverse-polynomial gap,
nonnormal higher-class symmetries and a serious access-matched baseline.
Do not add more small symmetry fixtures or call a gap assertion a candidate.
No central admission, production receiver, CLI/UI work or Git action is
authorized by this note. Routine integration belongs to Gemini/Antigravity.
