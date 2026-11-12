# Two branching circuits: proposed clean Jack transform

2026-11-13, REVIEWED WRITTEN full circuit construction. Independent300line
proof fully parent-read and checked: audits/reviews/2026-11-13-jack-branching-
independent.md. Admitted cost is polynomial(D,1/epsilon), not polylog precision.
This is a constructive replacement for the coupon-collector label decoder,
not a consequence inferred from fixed-label state preparation. Same native
alpha3 degree-D Hall coefficient-state model as JACK_LAX_PREPARATION_CANDIDATE.

## Algebra and overlaps already independently derived

Write j_mu for normalized Jack and v_(lambda,s) for normalized Lax vector.
The all-degree identity A psi=J, positive normalizations and AA†=3nI imply

 V_(n-1) j_mu = sum_(r removable mu) sqrt(q_mu,r) v_(mu-r,r),
 q_mu,r = tau_(mu-r,r) ||J_mu||²/[3n ||J_(mu-r)||²].

All coefficients are POSITIVE. Up-corner tau>=3/[16(n-1)] for n>1;
q>=1/n. Norms are actual integral-Jack hook products. All q and tau are
computable rational numbers with polynomial bits from the explicit shapes.
General alpha>0 algebra does NOT imply these integer-gap bounds for all
binary-real alpha; alpha=3 remains fixed.

## Quantum Fock branching B_n

1. Apply the native isometry V=A†/sqrt(3n), implemented by removing mode k
   with amplitude sqrt(k*m_k/n) and storing marker k-1.
2. Coherently extract integer content c with phase estimation of L_(n-1).
   Use modulus a power of2 exceeding the full spectral width, retain signed
   c, and erase phase-estimation workspace. Charge sparse simulation error.
3. Controlled on c, apply the positive polar map of P0 P_c, where P0 is
   marker-zero projection and P_c is the content projector. Globally its
   nonzero singular pairs are (v_(lambda,s),j_lambda), c(s)=c, and singular
   values sqrt(tau_(lambda,s)). Different lambda are orthogonal; no supplied
   Jack projector or recursively prepared inverse is present.

The ACTUAL Gilyen--Su--Low--Wiebe1806.01838v1 Theorem26, read locally, supplies
positive singular-vector transformation with uniform error above a threshold,
O(delta^-1 log(1/error)) projector calls and one ancilla. Need convert its
projected operator error to clean isometry error (square-root loss harmless
if internal tolerance squared). Phase compilation and native simulation must
be polynomial BIT, not only query complexity.

The intended clean isometry is

 B_n: j_mu |0> -> sum_r sqrt(q_mu,r) j_(mu-r) |c(r)>.

Compose n=D down to1, retaining each content record. This yields vacuum
times a coherent distribution over removal paths. Each path's amplitude is
the positive square root of its product of q weights. Different terminal
shapes have disjoint valid content paths: reverse the path from the empty
partition; at each step a content identifies a UNIQUE addable corner.

## Classical-label branching C_n, implemented reversibly

On a shape register mu, enumerate its removable corners and calculate q.
Prepare sum_r sqrt(q_mu,r)|c(r)> coherently, then update the shape to mu-r.
The update is reversible on valid pairs: from (mu-r,c(r)), the unique
addable corner with content c(r) reconstructs mu. No extra copy of mu or
oracle for Jack coefficients is retained. All corner/weight arithmetic and
state preparation involve polynomially many polynomial-bit quantities.

Thus the intended clean isometry on LABELS is

 C_n: |mu>|0> -> sum_r sqrt(q_mu,r)|mu-r>|c(r)>.

Compose C_D,...,C_1 to map |mu> to the SAME positive removal-path state,
with empty shape register. Recode empty shape as Fock vacuum by a fixed
known unitary, then apply B_1†,...,B_D†. This should produce j_mu and erase
ALL paths, uniformly on arbitrary superpositions of mu. There is no
postselection, coupon collector, recursively prepared state inverse or
unstated label-erasure operation. The inverses are of explicit native
branching circuits with polynomial total descriptions.

## Decisive obligations

Verify global singular pairs despite content degeneracy; exact relative
phase agreement between B and C; clean native isometry extensions; coherent
shape update injectivity; uniform operator-norm error without a p(D) factor;
and full finite gate/bit precision including source phase compilation.
An invalid pair or input outside the valid subspace needs a unitary extension,
not a claimed inverse of a rectangular matrix. No circuit implementation is
requested until this complete argument survives review and classical checks.

If sound this is a polynomial change of basis at fixed alpha3, not a proof
of classical hardness, novelty, useful computational separation or a physical
finite-variable Calogero--Sutherland position transform. The strongest current
classical sampler costs poly(D)*#{nu subset mu}^O(1), polynomial for bounded
Durfee size; general sampling remains unmatched, not hard.

## Elementary precision fallback proposed by parent

Do NOT use known-angle Hoyer rotations inside B_n: its input Jack label is
unknown, so computing its tau from that label would be circular. Instead
let W=(2P0-I)(2P_c-I). In each desired real Jordan plane, source psi and
positive-overlap target J have angle theta=arccos(sqrt(tau)) in[0,pi/2).
W rotates by2theta. Its PRINCIPAL square root rotates bytheta and hence
maps psi to J with the desired positive phase. The eigenphases stay at
least Omega(sqrt(tau_min)) away from the cut at -1. A coherent ordinary
phase estimate, application of exp(i*estimated_phase/2), and inverse phase
estimation therefore implement the required rotation uniformly with
polynomial(D,1/epsilon) calls: use a good phase error h=O(epsilon), bad
probability O(epsilon^2), and keep the cut guard explicit. Uncomputing phase
workspace gives vector error O(h+sqrt(bad_probability)). The actual finite
clock and errors of W's native reflection calls still need independent
checking. This weaker polynomial-precision route avoids any unverified
polylog-precision phase-synthesis theorem. Null singular blocks may be
extended arbitrarily; the promised inputs have the positive uniform gap.

## Admitted theorem and report dispositions

For every numerical D>=0 and 0<epsilon<1, a uniform finite-gate circuit maps
an arbitrary superposition sum_mu a_mu |mu>|0> to
sum_mu a_mu |Jhat_mu>|0> within epsilon in restricted isometry/operator norm.
The output is the normalized integral-Jack alpha3 power-sum coefficient
state, in the explicit occupation encoding. The full BIT/circuit cost is
polynomial(D,1/epsilon), with a fixed exponent independent of p(D). Loading
an arbitrary input superposition is not supplied free. All ancillas have
error bounded jointly with the output; no measurement or postselection is
used. This is a written algorithm, not a circuit implementation.

The independent proof pays the elementary principal-square-root compiler:
g0=1/[2(D+1)], h=min(g0/4,zeta/4), xi=zeta²/64, M the least power2 at least
16/(xi h²). QPE circular-error tail <=pi²/(M h²), clean uncompute error
<=h/2+2sqrt(xi), and <2M native walk calls with per-call error zeta/(32M).
Canonical matching metadata survives each two-level rotation unchanged, so
compute/rotate/uncompute really is clean. Source sparse simulation and a
direct first-order product formula pay the whole native gate clock.
C and B share the identical positive path states. The inverse-on-range
bound pays actual approximate B inverse circuits, with no p(D) loss.

All SIX paid reports completed/nonempty and were fully parent-read:
- Intertwiner: independent Hamiltonian-lift/resolvent proof accepted; global
  content-only label shortcut falsified exactly. No additional quantum claim.
- Overlap: stronger1/d bounds accepted. Its generic near-one warning is
  repaired by the OTHER corner masses; new scans are unnecessary.
- Classical sampler: derivative identity/down-set construction accepted;
  bit clock repaired by common LCM denominators and hook norms. Its stronger
  Durfee restriction for any advantage is rejected.
- Native measured preparation: invariant spaces, binary-Lueders requirement,
  isometry, finite clock and global error accepted. Exact exponent and claimed
  polylog precision are not imported into the full-transform theorem. Optional
  dirty-signal measurements must not be inserted inside coherent inverses.
- Coupon decoder: two-corner reconstruction, history-by-history orthogonality,
  clean XOR decoder and known-LABEL controlled rotations checked. Both shape
  sets must be regenerated for validation. This is a separate longer route;
  the admitted transform uses the simpler C/B composition. Measured histories
  still cannot be discarded. Its explicit numerical counterexamples were
  checked by direct corner arithmetic, not a parameter sweep.
- Branching transform: all remaining stated assumptions are paid by the
  verified positive identity, overlap proof and specified Hall encoding.
  The report independently derived the same principal-square-root fallback.
  Its phase tail must use CIRCULAR distance; the independent proof does so.
  Its exact cost exponent and QSVT-phase compilation are not adopted.

All general-classical-hardness, novelty, Shor-level speedup, practical gate
count, physical-position/FQH-state and polylog-precision gates remain FALSE.
The strongest checked classical sampler is poly(D)*M(lambda)^2, polynomial
for bounded Durfee; unrestricted polynomial sampling remains OPEN.


Resource upgrade (Nov13): JACK_LOG_PRECISION_COMPILER.md and the fully
parent-checked300line independent composition proof replace half-phase QPE
and first-order simulation. The SAME full clean alpha3 transform now has
WRITTEN poly(D,log1/epsilon) BIT/gate cost, including all workspace and
reference. Earlier inverse-accuracy estimates remain valid historical
constructions. No implementation, novelty or classical separation follows.
