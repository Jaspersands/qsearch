# Auxiliary Phase Feedback: Physical Rescue, Exponential Construction

2026-10-18. LOCAL PROOF APPLICATION REVIEW PENDING. No new algorithm,
classical hardness, independently accepted proof or matched runtime advantage.

Run `python theorems/prime_character_phase_feedback.py --write`. The producer
writes `classical_baselines/prime_character_phase_feedback.json`. Dense quantum
controls are deliberately bounded; the large records are analytic certificates.

FOLLOW-UP: the same producer now executes the two-way SOURCE-SPECIFIC
phase/erasure reduction below. This supersedes treating phase compilation as
an independently justified decoder bypass. It does NOT prove a general
syndrome-decoding equivalence or a new complexity lower bound.

## Question And Contract

Can the actual collaborative decoder from PRIME_CHARACTER_INTERLEAVED_PROBE.md
replace the expensive single-copy capacity decoder while preserving the
ORIGINAL single-polynomial OPI objective? The plain separate-readout replacement
failed. This pass tests its explicit auxiliary-measurement/support-phase repair,
not another parameter mesh or a differently named product-correlation task.

Input: prime p=3 mod4, N distinct public evaluation points, degree<K polynomial,
fixed public shifts and quadratic-residue/nonresidue predicates, either zero
convention. No membership oracle, random input shifts or advice is supplied.
Desired output is an explicit polynomial with many accepted positions.

Source: a normalized support vector b, |S|<=ell<K, with c independent nonzero
Fourier-value rows CONDITIONAL on S. The collaborative equation budget is
c(K-ell)>=ell. The syndrome-only classical primitive already runs at
N127,K39,ell32,p=2^61-1 with five/eight rows. Its coherent compiler is still
missing. This pass additionally assumes exact native-state reflections when
deriving large distances; it does not set synthesis costs or errors to zero
for an implementation.

Intended upside: retain the known DQI output with polynomial field-linear
decoding in place of a severe capacity decoder. Actual finding: state fidelity
can be rescued, but the supplied phase implementation is exponential. There is
NO established asymptotic advantage over classical algorithms.

## Why Feedback Can Restore The State

Let D=p^K, g_i=(accepted_i-rho)/sqrt(rho*(1-rho)),
V_S(Q)=D^(-1/2)*product_(i in S) g_i(Q(i+1)). Each column has norm1 for
|S|<=ell<K, by K-wise independence of uniform polynomial evaluations.
The ideal shared-support source is the normalized version of

    sum_S b_S V_S(Q_1) ... V_S(Q_c).

Measuring Q_2,...,Q_c leaves main support multiplier
product_(a>1,i in S) g_i(Q_a(i+1)). Define the PUBLIC mask

    z_i = parity_(a>1) [g_i(Q_a(i+1)) < 0].

Computing this mask uses (c-1)*N predicate evaluations. It is NOT the same
operation as applying the encoded phase (-1)^(z dot 1_S) after S has been
erased. Multiplying the physical Q register by the public predicate sign
does not implement that support phase. An independent vacuum-state test
retains this distinction.

The earlier whole-support frame bound gives ||V^dagger V-I||<=delta,
delta=max(1,M-1)*epsilon, M=sum_(j<=ell) C(N,j), with epsilon the uniform
whole-ball sparse-error ambiguity bound. For delta<1/2, polar V=J*sqrt(G)
has J an isometry, and ||V-J||<=gamma=delta/(1-delta). The implementation
rounds gamma UP to a256-bit dyadic. Zero delta stays zero.

Use the normalized hybrid

    H = (J tensor V tensor ... tensor V) sum_S b_S |S>^tensor c.

Its norm is EXACTLY1 because the first columns are orthonormal and every
other V_S has norm1. The unnormalized native source differs by at most
eta=gamma*(1+gamma)^(c-1). Normalizing costs at most2eta/(1-eta).
Measurement/feedforward/discard are a CPTP channel, so this trace-distance
error does not grow. On H the encoded phase on J cancels every branch sign.

Put R=(p+1)/(p-1), B=R^((c-1)*ell). The remaining POSITIVE amplitude
multipliers lie in [1/sqrt(B),sqrt(B)], ignoring a common D factor. For any
complex b, the normalized corrected branch has trace distance at most

    (B-1)/(B+1)

from J*b. Proof: for r in [a,b], (r-a)(r-b)<=0 implies
E[r^2]<=(a+b)E[r]-ab. Minimizing (E[r])^2/((a+b)E[r]-ab) gives fidelity
squared >=4ab/(a+b)^2. Here ab=1. A two-value complex-coefficient test
saturates the bound. Convexity extends it to the outcome mixture. Finally,
the normalized native target V*b/||V*b|| differs from J*b by at most
2gamma/(1-gamma). NO rare auxiliary outcome is selected or rerolled.

## A Real Phase Action, Not A Free Oracle

On the polar frame the desired unitary is the product, over z dot S odd, of

    I - 2 |J_S><J_S|.

The explicit native implementation instead multiplies the genuine unitaries
I-2|V_S><V_S| in a fixed support order. Each differs from its polar factor
by at most2gamma. Telescoping bounds the entire operator error by2q_z*gamma.
Using I-2*V*P_odd*V^dagger as if it were unitary is INVALID when columns are
nonorthogonal. A one-dimensional-dual native Gram at p10007,N5,K4,ell3
detects that shortcut; the actual reflection product remains unitary.

Individual state preparation is not the main counted obstruction: predicate
evaluation and bounded amplitude rejection can propose a V_S preparation with
success R^(-|S|), since E|product g_i|^2=1. Reflection needs a UNITARY
preparation and its inverse, including coherent amplification/rotation
precision, not a postselected vector returned by a simulator. No such gate
compiler is supplied here. EVEN GRANTING one cheap exact state preparation,
the number of sequential reflection calls is exponential:

    q_z = sum_(j<=ell) sum_(k odd) C(|z|,k) C(N-|z|,j-k).

Every nonzero mask has

    q_z >= sum_(j<ell) C(N-1,j).

To see this, choose an active coordinate i. Each pair T,T union {i},
T contained in the other N-1 coordinates, |T|<ell, lies inside the ball and
has opposite mask parity. These pairs are disjoint; each contributes one
reflection. This is a count of THIS factorization, not a query/gate lower
bound against all structured phase compilers. Each reflection costs two
state-preparation calls plus a vacuum reflection. Total synthesis error e
requires individual operator errors O(e/q_z); those errors have not been
compiled or charged as an actual gate count.

The zero mask does not make this construction cheap on average. Under uniform
independent auxiliary polynomial words, mask indicators are pairwise
independent Bernoulli(nu), where nu=(1-(2rho-1)^(c-1))/2. Chebyshev gives
Pr[z=0]<=(1-nu)/(N*nu), WITHOUT a full-binomial assumption. Hybrid auxiliary
density is at most B times uniform. Add source/hybrid and rank-herald trace
errors to transfer this event bound to the actual heralded source. Therefore
the expected correction-call count is at least
(1-Pr[z=0])*sum_(j<ell)C(N-1,j). No output-row independence is assumed.

The prior rank-herald error is separately paid: zeta=ell/(p-1),
C=(M-1)*epsilon, squared trace distance <=(zeta+C)/(1+C). This is NOT
M*zeta and is NOT equal to failed source mass. Source rank-herald success
is at least1-zeta under the stated conditional independent-value source.

## Executed Results

Four COMPLETE two-row controls use p7/11,N4,K2,ell1. Independent physical
error/syndrome/QFT amplitudes agree with the native product expansion. Every
auxiliary measurement outcome is retained and its actual reflection product
is applied. All145/401 error vectors,2401/14641 joint output words, and dense
49/121-dimensional operators are charged. This is NOT a scalable gate test.

| Field / Zero Convention | Raw Mean | Corrected Mean | Desired Mean |
| --- | ---: | ---: | ---: |
| 7 / Including | .553571 | .759111 | .760829 |
| 7 / Strict | .446429 | .730685 | .734043 |
| 11 / Including | .534091 | .784842 | .785897 |
| 11 / Strict | .465909 | .711026 | .712033 |

Corrected purity is .982221/.992781, NOT1: finite-field amplitude distortion
remains. Trace distances to the target are .0102251/.00413566. A separate
three-row native test with COMPLEX support coefficients requires XOR of both
auxiliary sign masks; correcting just one mask fails.

At p=2^61-1,N127,K39,ell32, c5/8, local exact-rational certificates give:

- Distance to the original native single-copy state <=3.726e-9, including
  rank herald, frame, magnitude and ordered native reflection errors.
- Magnitude distortion <=5.552e-17 /9.715e-17, respectively. Ordered reflection
  approximation <=1.735e-38. Rank-herald error dominates.
- Original chosen radial weights are saved explicitly, with their norm and
  support convention. Transferring the PREVIOUS finite mean proof gives mean
  >.90285 and one-attempt110/127 tail >.31458, CONDITIONAL on those exact
  mathematical operations. This is not a new large quantum execution.
- Every nonzero mask needs at least408774727362072591332623950512 reflections
  in this construction. The nonzero-mask probability is >.99212598, giving
  expected calls >4.0555e29. There is no efficient decoder bypass here.

## Adversarial Decision And Next Experiment

What survived: auxiliary measurement need NOT irreversibly lose the score.
There is a concrete interference-restoring action, verified on full native
states and locally bounded without selecting fortunate outcomes.

What failed as an efficient algorithm: replacing that action by a cheap public
sign calculation, a nonunitary simultaneous projector sum, or the explicit
exponential reflection product. Keeping the support register makes its phase
cheap but leaves the original erasure/decoder task unsolved; copying a syndrome
before Fourier measurement retains which-support information, not a free fix.

Still assumed: scalable coherent collaborative decoder, gate-level source and
reflection synthesis, independent review of the frame/rank/feedback proof,
and a competitive classical-runtime comparison. Earlier classical norm/Morse
attacks defeat high-rate regimes; the saved SAME-input K39 classical word
scores109/127. Neither its best-known status nor this conditional tail proves
classical hardness. Direct score amplification/rejection is another classical
or quantum comparator that must be paid, not assumed absent.

Next work must supply a SPECIFIC polynomial structured support-phase compiler,
or compare a genuinely independent constructive route. Do not add mask/seed/
radius meshes, generic oracle labels, or a new rejection registry around this
same exponential construction. This pass does not justify more DCP bridges.

## Is The Encoded Phase Really An Easier Task?

Let D_i act on the ORTHONORMAL polar frame by
D_i J_S=(-1)^[i in S] J_S. Suppose KNOWN controlled implementations are
available, uniformly on the whole frame. Introduce an N-bit label register
and execute

    E = H^N * product_i controlled_(label_i)(D_i) * H^N.

On |a> J_S, the phases are the Fourier character(-1)^(z dot S), so E gives
|a XOR S> J_S. This is the elementary Hadamard/phase extraction mechanism,
not a novel algorithm. Consequently E extracts S from a native packet with
a zero label, and its adjoint erases a supplied S. It needs N controlled
singleton phase calls,2N Hadamards and N label qubits. No additional
interleaved polynomial or rank herald is needed by this ABSTRACT circuit.

Conversely, let W be any uniform CLEAN eraser satisfying
W(|S> J_S)=|0> J_S. Then W^dagger followed by label Z_i followed by W gives
the encoded D_i with clean workspace. This costs two eraser/adjoint calls
and one Pauli gate. The relation holds only on the stated source frame.
It is not implied by a procedure converting ONE predeclared state, or an
uncontrolled black-box unitary ALONE: its global phase is invisible
uncontrolled but changes a naively chosen controlled matrix. HOWEVER, that
is NOT an additional impossibility here: the native family has a known
eigenstate, giving the constructive reference circuit below. For approximate
factors use the ACTUAL inverse order/adjoints; native reflection products
need not commute or be Hermitian.

### A Native Reference Removes The Extra Control Assumption

Self-critique removed an unnecessarily strong premise in the first derivation.
V_empty is the known uniform polynomial state. Centering and ell<K imply
<V_empty,V_S>=0 for every nonempty S. Thus J_empty=V_empty, and every genuine
native reflection, singleton phase and its polar counterpart fixes this vacuum.

Prepare a reference in that vacuum. Controlled-swap the main and reference
registers, apply UNCONTROLLED U to the reference, and controlled-swap back.
For U*v=lambda*v, this gives

    |0> psi v -> lambda |0> psi v,
    |1> psi v -> |1> U*psi v.

Up to one common global lambda this is controlled-(U/lambda), with CLEAN
reference. No eigenphase estimation or correction gate is applied. Changing
U to exp(i*theta)U changes only the common global phase. This exactly supplies
the native encoded action anchored on V_empty. The generic uncontrolled-U
no-go must not be used as an obstacle once this additional information exists.
This is a known eigenstate-assisted control construction, not a novel claim;
see [Navas-Merlo--Garcia-Escartin](https://arxiv.org/abs/2602.19250) and the
scope of [Araujo et al.](https://arxiv.org/abs/1309.7976).

The SAME reference can be reused for all exact native phase calls. Charge
K*ceil(log2 p) extra qubits and2N*K*ceil(log2 p) controlled BIT swaps, plus
one reference preparation and N uncontrolled phase calls. The saved large
input uses2379 extra qubits and604266 controlled bit swaps. Its uniform-range
gate compiler, synthesis costs and errors are still NOT supplied. Full native
two-register tests retain the reference and complex control/main amplitudes;
U,-U and exp(.37i)U all give the same controlled native action up to global
phase. A non-eigenstate reference is rejected. Dense2D^2 amplitudes are charged
for these small calibrations. This removes an unnecessary access blocker,
NOT the exponential cost of U itself.

For our existing native reflection construction, singleton i needs exactly
L=sum_(j<ell)C(N-1,j) reflections. The full extraction unitary differs from
its polar counterpart by at most2NL*gamma. A labeled native source
sum_S b_S |S> V_S has unit norm and differs from its J source by at most
gamma; labels make all cross terms vanish. Thus erasure distance to the
normalized native one-copy target is at most

    gamma + 2NL*gamma + 2gamma/(1-gamma).

The new large exact-rational record gives distance<=5.468e-37, but costs
51914390374983219099243241715024 reflections (twice as many native-state
preparations/inverses). The127 controlled calls are NOT127 cheap gates.
No scalable compiler or new speedup is supplied. This construction removes
the auxiliary rows by assuming precisely the uniform source-specific erasure
ability needed for the original interference; it is not independent evidence
that the missing primitive is easy.

### Native Execution And A Critical Counterexample

All four p7/11 controls use complex support coefficients, genuine native
reflection factors and the complete label register. Extraction, inverse
erasure, forward replay and converse clean phases agree in COMPLEX amplitudes
to<1.2e-15. A separate randomly rotated orthonormal frame checks every label
and every support in a radius2 ball. A nonorthogonal control preserves the
actual leakage and rejects using forward E as its own inverse.

Do NOT conclude that the source-specific extractor solves arbitrary classical
syndrome decoding. The Fourier image of one classical syndrome is not a V_S
packet. At N4,K2,ell1, syndrome(1,1) has unique support{0}, confirmed by the
actual syndrome-only decoder. Its projection onto V_{0} has probability
1/(p-1), and its remaining component is outside the source frame. The
explicit phase circuit labels that remainder0, so it recovers the true support
with probability1/6 at7 or1/10 at11, not1. This single counterexample invalidates
the stronger logical implication, NOT every possible decoder or phase extension
outside the frame. No classical hardness inference follows.

### Independent Route Comparison And Stop Rule

The primary-literature check changes the novelty boundary:

- [Sun--Wootters,8 Oct2026](https://arxiv.org/abs/2610.12357), Theorem1.8
  and Section6, give worst-case prime-field OPI quantum guarantees using
  capacity list decoding. This is existing work, not a discovery here. Its
  asymptotic guarantee is not a finite N127 gate budget, and its oracle
  hardness does not transfer to public character descriptions.
- [Jo](https://arxiv.org/abs/2607.16541) gives a complete-list coherent-sum
  sampler. This is an independent known receiver construction, not a new
  source eraser supplied by this project. It still requires the actual decoder.
- [Rank-metric DQI](https://arxiv.org/abs/2606.04843) explicitly identifies a
  Gabidulin covering-radius obstruction to its proposed advantage. Merely
  changing distance geometry is not a constructive speedup candidate.
- [Chailloux--Tillich](https://arxiv.org/abs/2411.12553) uses soft decoding for
  non-flat Fourier profiles and RS-ISIS-infinity. This is a DIFFERENT native
  problem/source mechanism worth a matched classical attack, not a reason to
  claim our flat source is new.

Decision: retain this exact reduction and its counterexample; stop extending
the phase-oracle proposal without an actual new gate mechanism. Generic
worst-case OPI is an existing-algorithm benchmark, not a novelty claim. The
next independent concrete question is whether a compact non-flat interval
source plus soft RS decoding retains any regime after charged interpolation,
lattice and sampling baselines. Define that SAME-input problem and test the
published reduction before inventing a new algorithm or expanding a registry.
The current degree39 compact-character runtime/hardness gap remains open.

Primary phase-extraction context: [Bernstein--Vazirani](https://doi.org/10.1137/S0097539796300921).
The frame-restricted equivalence and finite error accounting above are local
applications, review pending, not a new theorem attributed to that source.

Relevant primary literature: [collaborative RS decoding](https://arxiv.org/abs/cs/0610074)
provides the coding context; [quantum rejection sampling](https://arxiv.org/abs/1103.2774)
treats amplitude conversion under explicit oracle access; and
[symmetry-assisted state-generation adversaries](https://arxiv.org/abs/1012.2112)
prove a GENERIC coherent index-erasure bound. Their abstracts/scope were
checked this pass; no full-paper proof review or reduction of this structured
family to that lower bound is claimed. Our numerical/analytic local results
are not presented as theorems from those papers.

Original feedback milestone:13 focused checks and113 selected connected regressions pass
in9.19s with RuntimeWarning as error. The standalone producer, source/dependency
hash replay, strict finite JSON/evidence paths, Python compilation, site JS
syntax, plain registry validation and diff whitespace checks pass. This is
NOT a full-repository test run. No central registry entries were promoted.

Current erasure/reference follow-up:12 new focused checks,25 combined phase/
erasure checks and125 selected connected regressions pass in9.31s. Live report
regeneration, source/dependency SHA replay, strict finite JSON/five evidence
paths, Python compile, site JS syntax, plain validation and diff checks pass.
All owned sessions are terminal; this still is NOT the full repository suite.
