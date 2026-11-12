# Jack Lax preparation: candidate, not an algorithm claim

Selected 2026-11-13 after corpus been-tried/baselines lookups and actual
Mickler--Moll, Lapointe--Vinet and Stanley primary-source retrieval. The
preceding sparse-torus support mechanisms have no general completion bound.
An independent Anderson-impurity alternative was screened out by the actual
October 2026 classical polynomial ground-energy/compact-state papers.

## Native problem and potential value

Input is an explicit partition lambda of numerical size D, fixed alpha=3,
and accuracy epsilon. In the stable symmetric-function Hall space,
<p_mu,p_nu>=delta(mu,nu) z_mu 3^length(mu), prepare the normalized coefficient
state of the integral Jack J_lambda in the orthonormal power-sum basis.
Output is a quantum state; the corresponding classical competitor is sampling
its Born distribution (and any claimed application needs a matched output).
D is charged numerically. This is NOT a physical Calogero--Sutherland position
state. There is no supplied eigenvector, Jack oracle, reflection, postselection
or constant-field advice. Explicit partition-space diagonalization costs
exp(Theta(sqrt(D))); that is only a baseline, not a lower bound. Efficient
classical sampling, other transforms and useful readout remain to be checked.
Expected target is polynomial(D, log(1/epsilon)) or an explicitly weaker
polynomial precision dependence, NOT a claimed advantage or novelty.

## Proposed mechanism

Let F=C[V1,V2,...], deg Vk=k, and augment by w of degree1. Orthogonal
V_mu w^l have squared norm z_mu 3^length(mu); w has norm1. On degree d,

    L_d = 2 w d/dw + sum_k 3k (d/dVk) w^k + sum_k Vk pi w^(-k).

In normalized occupation basis, edges have weights sqrt(3 k m_k) or
sqrt(3 k(m_k+1)), at most O(d) neighbors and polynomial norm. Spectrum is
integer corner contents c(s)=3x-y, within [-d,3d]; distinct values have gap1.
Global degeneracy is allowed. Mickler--Moll Thm1.4 and Lemmas3.3--3.5 give
orthogonal cyclic spaces Z_lambda, simple corner spectrum in each, and
unique psi_(lambda,s) with pi0 psi=J_lambda. The overlap with normalized
J_lambda is tau_(lambda,s), the explicit interlacing residue (1.18).

Define A_d(V_mu w^l)=V_mu V_(l+1). Its weighted adjoint is
sum_(l>=0) 3(l+1) partial_(V_(l+1)) g w^l, so Euler's identity gives

    A_d A_d^dagger = 3(d+1) I.

Thus V_d=A_d^dagger/sqrt(3(d+1)) is an isometry, implementable by selecting
an occupied mode k with probability k m_k/(d+1), removing it and setting
l=k-1. Its images have disjoint basis supports because adding mode l+1
reconstructs the input. This is a proposed reversible circuit interface,
not an implemented circuit. Range projector P_A=V_d V_d^dagger is native.

NOW PROVED ALGEBRAIC IDENTITY (independent211line proof parent-read):

    A_d psi_(lambda,s) = J_(lambda+s).

Exact Sage control d=3, lambda=(2,1), alpha3 verifies all three contents
6,2,-2 and AA^dagger=12I. This cannot prove the identity at all degrees.
The block identity L_(d+1)=[[0,A_d],[A_d^dagger,L_d+2I]] and compressed
spectral interlacing suggest the formula but do not by themselves identify
partition labels inside degenerate global content eigenspaces.

If the identity and inverse-polynomial overlap bounds hold, use a fixed
classical one-box growth path to lambda. Stage1 alternates measurements
of pi0 and the desired content projector of L_d, inside invariant Z_lambda,
to reach psi_(lambda,s). Stage2 alternates P_A and the same content projector
to reach V_d J_(lambda+s), then applies V_d^dagger. The desired invariant
space is spanned by psi_(mu-r,r), r removable in mu=lambda+s; contents there
are distinct. Every failed measurement and resetting step must be proved.
No recursively prepared state inverse may be used: that would reintroduce
an exponential product cost. All measurements need finite precision and a
finite runtime clock with bounded final trace error/failure.

## Proof obligations and immediate falsifiers

1. CLOSED algebraic identity for every real alpha>0, including all global
   degeneracies; native circuit and full-transform consequences are separate.
2. Bound both stage success overlaps uniformly over ALL partitions/corners
   by inverse polynomial d at fixed alpha3, with explicit constants.
3. Prove invariant subspaces and alternating-measurement runtime under
   approximation, native sparse simulation, workspace accounting and
   failure branches; pay all normalization and state preparation.
4. Try exact classical coefficient recurrences, representation-theoretic
   sampling, Jack growth chains and tensor constructions on the SAME Born
   distribution. A classical polynomial sampler removes sampling advantage.

A single exact wrong coefficient, an exponentially small required overlap,
leakage requiring an unavailable Jack projector, or a matched polynomial
classical sampler changes the next scientific action. Passing finite tests
does not establish an algorithm, complexity separation or useful application.

Sources: https://arxiv.org/pdf/2211.01586v2 (actual main theorem and inner
product proof read); https://arxiv.org/pdf/q-alg/9509003 (formal creation,
not automatically a unitary); Stanley primary PDF at
https://math.mit.edu/~rstan/pubs/pubfiles/73.pdf (norm/Pieri scope still to
check, poor OCR). Local source files are audits/sources/jack_transform/.

## All-degree algebraic gate closed, 2026-11-13

Full independent proof audits/reviews/2026-11-13-jack-lax-intertwiner-
independent.md (211lines) was parent-read and checked. A†J_mu is spectrally
supported only on removable contents. For lambda=mu-r, the addable contents
of lambda intersect removable contents of mu only at c(r). Up-Pieri gives
its projection along tau psi_(lambda,r). The sum of those projection norms
is EXACTLY ||A†J_mu||² by the adjoint-Pieri V1^d coefficient identity. There
is therefore no residual component in any degenerate global eigenspace.
Taking adjoints proves A psi=J with scalar1 for ALL alpha>0 and all sizes.

This identity is related to Mickler2306.11115v2 Shift Thm3.4, but that
paper's printed down-residue/eigenvector signs conflict with its positive
shift normalization. Correct positive choices are -Res(1/m_mu) and
(L|Z_mu-theta)^(-1)J_mu; an inverse on the WHOLE space may not exist.
The norm-saturation proof uses neither flawed sign nor generic continuation.
No novel algebraic identity is claimed. Source and exact countercheck are
recorded in the independent proof.

Parent proposed inverse-polynomial overlaps and a clean nondemolition label
decoder from both corner sets; these resource claims remain under review.
The fifth DISTINCT paid job handles clean coherent decoding/full-transform
consequences, which do not follow just from fixed-label state preparation.
Five jobs have combined local ceilings31USD, NOTcharges, in the jack-lax
manifest. Strongest classical sampler and complete circuit gates stay OPEN.

## Overlaps and matched classical sampling checked

Independent209line overlap proof and195line classical sampler proof fully
parent-read. At fixed alpha3, tau>=3/(16d) for d>=1, q>=1/(d+1); zero degree
is deterministic. Exact two-projector failure is
(1-p)[p^2+(1-p)^2]^M. Other positive corner masses also bound1-p away from
zero, except deterministic single-corner cases, giving O(D^2 log(D/eta))
ideal measurement cost on a full path. Universal joint-projector ancilla
dilution is an alternative; it must not reveal refined failure outcomes.
Finite-precision/coherent circuit gates remain separate.

The unconditional classical Born sampler computes all derivative norms in
the partition down-set, using raising commutators and actual hook norms.
Its exact expected BIT cost is poly(D)*M^2, M=#{nu subset lambda}; bounded-
time TV-epsilon costs poly(D,log1/epsilon)*M^2. A universal denominator
lcm(1..4D)^(D^2+4D) proves O(D^3 log(D+1)) bit lengths. Thus bounded-Durfee
families are classically polynomial. Quasipolynomial upper bounds for other
families do NOT exclude a possible polynomial-versus-quasipolynomial gap.
The report's stronger restriction and unnecessary finite sweeps are rejected.
No general classical polynomial sampler or hardness result was established.

The paid all-degree OpenAI report also completed and was fully checked:
a commuting content-Hamiltonian lift plus full transfer resolvent proves
Apsi=J without importing Pieri. Its transfer function identifies partitions
from interlacing pole/zero differences. It confirms algebra already proved
independently, with a useful exact content-only degeneracy counterexample;
no extra quantum resource claim. Saved under openai_runs/2026-11-13-jack-
intertwiner. Six distinct jobs now have33USD combined ceilings, not charges.

## Full transform resource gate now closed

JACK_COHERENT_BRANCHING_TRANSFORM.md and the independently checked300line
proof give the FULL clean alpha3 basis change with polynomial(D,1/epsilon)
gates/BIT work, uniformly on superpositions. This supersedes earlier open
resource statements above; it uses no measured history or postselection.
All six paid reports are terminal and fully parent-read. General classical
sampling, novelty, useful computational advantage, and physical-position
applications remain unestablished. Next decisive classical attack is against
actual positive map/creation formulas, not another finite quantum control.


Resource upgrade (Nov13): JACK_LOG_PRECISION_COMPILER.md and the fully
parent-checked300line independent composition proof replace half-phase QPE
and first-order simulation. The SAME full clean alpha3 transform now has
WRITTEN poly(D,log1/epsilon) BIT/gate cost, including all workspace and
reference. Earlier inverse-accuracy estimates remain valid historical
constructions. No implementation, novelty or classical separation follows.
