# Richardson-Gaudin preparation by joint-charge randomization

Pass 2026-11-07. CLOSED conditional derivation and independent reviews.
Full native algorithm remains UNADMITTED: polynomial SAME-SECTOR joint
separation is still OPEN. No full implementation or quantum execution.

Later same-day update: GAUDIN_TWO_CLUSTER_GAP.md now gives a CLOSED native
finite-distinct-site counterfamily to uniform Omega(1/N) SQUARED separation:
N=2n, M=n, two width-n^-7 clusters, spacingn^-8, g1/(2n), upper2312n^-5/3.
Its exact128-site certificate is <1/400<1/128. The accepted Lutzv3 source
still explicitly leaves the general gap open; no proved theorem or tested
equally-spaced/random family is refuted. The conditional construction here
is unchanged. A weaker inverse-polynomial all-path gap remains OPEN.

## Scientific question and native contract

Can a polynomial lower bound on the JOINT charge separation be proved for
real rational spin-1/2 Richardson-Gaudin models, thereby giving an actual
all-eigenstate preparation algorithm without a classical Bethe-root oracle?
This is externally motivated by highly excited interacting eigenstate
preparation. It is a different operation from the failed all-prefix
Gaudin-determinant deletion route in RATIONAL_GAUDIN_PREFIX_ADMISSION.md.

Native input is N, distinct binary rational sites eps_i, rational G>=0,
an N-bit product-state label b at g=0, target trace-distance error epsilon, where TD(rho,sigma)=||rho-sigma||_1/2. Set g=sG,
s in [0,1]. Charges on N physical qubits are explicitly

    Q_i(s)=n_i+(sG/2) sum_{j!=i}(P_ij-I)/(eps_i-eps_j),
    n_i=(I+Z_i)/2, P_ij=SWAP(i,j).

Output is a quantum state close to the unique continuously followed joint
branch starting at b. The branch label is part of the ordinary input;
no target roots, charge eigenvalues at s>0, prefixes, eigenvectors,
measurements, inverse maps or adiabatic schedule are supplied as advice.
The desired resource target is polynomial in input bits,N,1/epsilon for
polynomial-conditioned sites and coupling: G and inverse minimum spacing
must be polynomially bounded, or the explicit coefficient norms are charged.
Polynomial in log(1/epsilon), arbitrary binary G, or arbitrary near-coincident
sites is NOT claimed. A general quantum output state has no classical
explicit-output counterpart; compare specified samples/observables separately.

Mechanism: random evolution under the complete COMMUTING charges performs
approximate projection onto a joint branch. A sufficiently fine Zeno path
then prepares the branch. Unlike the source's target-dependent squared
parent Hamiltonian, the operation never evaluates the unknown q_i(s).
All input Hamiltonians and their Pauli coefficients are explicit.

Expected upside is a polynomial quantum preparation for all interacting
branches where general deterministic preparation has exponential resources.
No classical lower bound, novelty or separation is established. The SAME
source already proposes a conditional adiabatic route. The new task is
paying its missing operations and proving its unresolved quantitative gap.

## Prior work and source admission

Corpus been-tried queries: adiabatic Richardson Gaudin parent Hamiltonian
complete conserved charges; quantum Zeno eigenpath traversal joint commuting
charges unknown eigenvalues. Baselines query returned no catalog match,
which does NOT establish absence of classical competitors. Earlier prefix
source/control and its one-site marginal/classical sampling comparator reused.

Actual primary source: Lutz, Piroli, Styliaris, Cirac, arxiv2503.21741v2,
retained under audits/sources/gaudin_charge_tracking/lutz.pdf/.txt with
source.json hash. PDF equations10-12 (HTML11-13), text220-310, define these
charges and quadratic equations. It explicitly leaves polynomial classical
charge tracking and finite-g same-sector joint separation unproved. Its
weak-coupling and g->infinity results and finite numerics do not imply the
uniform finite-g theorem. AppendixH's small Smale lower bounds do NOT prove
small true gaps or hardness. Do not repeat those source assumptions as facts.

Actual Boixo-Knill-Somma0903.1652 retained as boixo.pdf/.txt with hash in
boixo_source.json. Definition1,Lemma1,Theorem1 (text130-235) supply known
random-dephasing eigenpath machinery; they explicitly need no intermediate
measurement outcomes. The extension below uses the joint spectrum instead
of a single scalar Hamiltonian gap. Novelty NOT asserted.

## Conditional constructive theorem: no classical eigenvalue oracle

Let m commuting Hermitian Q_i(s), s in[0,1], be continuously differentiable,
with explicitly computable finite Pauli descriptions and efficient charged
simulation. Suppose a rank-one joint branch P(s)=|v(s)><v(s)| is continuous,
starts in an efficiently preparable state, and for every s and every
orthogonal joint eigenstate w,

    ||q_w(s)-q_v(s)||_2 >= kappa >0.

It suffices to impose this within an exactly preserved known symmetry sector.
Set L²=sum_i sup_s ||Q_i'(s)||², and A=sum_i sup_s ||Q_i(s)||_{Pauli,1}.
Use computable rational upper bounds on L,A and a positive rational lower bound kappa.
All bounds and inverse kappa must be paid/explicit. They are promises, not
computed from a finite scan. Target q(s) is NOT an input.

1. Differentiate each eigenvalue equation in parallel-transport gauge. For
   every w!=v, (q_wi-q_vi)<w|v'>=-<w|Q_i'|v>. Sum its squared modulus over
   i,w to obtain kappa²||v'||² <=sum_i ||Q_i'v||²<=L². Thus a uniform mesh of
   R steps has neighboring infidelity <=(L/kappa)²/R² (the projective-angle
   length bound). Ideal projective-measurement operations that preserve P
   and arbitrarily evolve its complement succeed with fidelity at least
   1-L²/(kappa² R), by retaining the always-target history. They need not
   report or recognize that history. Take R>=16L²/(kappa² epsilon²), at
   least1. Then fidelity-to-trace conversion gives trace distance<=epsilon/4.

2. At each mesh point independently sample m times t_i uniformly on[0,T],
   T=4ceil(sqrt(m))/kappa, and apply product_i exp(-it_i Q_i).
   This rational T lies between4sqrt(m)/kappa and8sqrt(m)/kappa. Repeat this round
   k times. For a target-other crossblock, the multiplier is

       phi_w=product_i exp(-iT d_i/2) sinc(T d_i/2), d_i=q_vi-q_wi.

   At least one |d_i|>=kappa/sqrt(m), so |phi_w|<=1/2. After k rounds it is
   <=2^-k. No scalar random combination is assumed to separate exponentially
   many eigenvalues, and there is no union bound over those eigenvalues.

3. Let D be this actual averaged random-unitary channel at one mesh point,
   and define M(rho)=P rho P + D((I-P)rho(I-P)). This is CPTP, and is an
   ideal target-projective-measurement operation. D-M consists ONLY of the
   two crossblocks. The target-to-complement block is multiplied on its
   complement side by a diagonal contraction of norm<=2^-k. For a density
   matrix its crossblock trace norm<=1/2; hence ||(D-M)(rho)||_1<=2^-k.
   This dimension-free estimate also holds with an untouched reference
   because the contraction acts only on the complement. Choose
   k=ceil(log2(8R/epsilon)); telescoping channel errors sum to<=epsilon/8
   in trace norm. The polynomial circuit generates randomness explicitly;
   tracing its classical random bits is a stated legitimate mixing step,
   not hidden postselection or discarded coherent source advice.

4. All sampled times are bounded. For each elementary evolution, round time
   to a dyadic grid of width <=epsilon/(C R k m (1+B)), where B bounds
   every ||Q_i||, and approximate the resulting unitary to operator error
   epsilon/(C R k m). Uniform continuous times are analyzed by coupling to
   uniform grid sampling; ||exp(-itQ)-exp(-it'Q)||<=B|t-t'|. Round Pauli
   coefficients to operator precision epsilon/(C R k m (1+T)); known
   polynomial-length Pauli lists pay this with polynomial bits. Hybrid
   channel error is O(epsilon) for a fixed sufficiently large constant C.
   One explicit allocation is C=192 in all three bounds; each unitary
   differs by at most epsilon/(64Rkm), and all channel implementation
   errors sum to at most epsilon/32 in trace norm. Thus total standard
   trace distance is below epsilon. No unbounded random evolution clock
   or unspecified real-number oracle.

Total charged evolution/Pauli norm cost <=R k T A, with polynomial
simulation overhead in m,N and log(Rkm/epsilon). R has inverse-epsilon²
cost. A loose ordinary product-formula simulation also suffices for this
polynomial contract. No quantum execution or full implementation is done.
The final averaged state is close to the desired pure branch; this is NOT
an arbitrary-input coherent transform of branch labels and provides no
fast-forwarding claim.

For rational Gaudin, let S_i=sum_{j!=i}1/|eps_i-eps_j|. Then
L<=G sqrt(sum_i S_i²), B_i<=1+G S_i, and explicit Pauli lists have O(N)
terms per charge. These bounds are computable directly from native input.
The only unresolved spectral premise is a suitable kappa along the path.

## Gap obligation and cheapest falsifiers

All charges preserve M=sum n_i and sum_i Q_i=M. Different-M pairs satisfy
||q(v)-q(w)||² >=(M_v-M_w)²/N. This elementary bound does not address the
relevant same-M competitors; the random evolutions preserve M exactly.
The source's proposed global squared gap1/N remains a conjecture here.
The stronger tempting same-M floor2 is REFUTED exactly: N=3, eps=(0,1,2),
g=1/10, M=1 has squared joint gap1.879457164624401... . Its minimal
polynomial is 32000000x^3-194880000x^2+394881000x-266221129, and its exact
root lies in(1879/1000,47/25). The frozen control certifies all8 joint
eigenvectors algebraically, charge identities/commutators, and rounded
256-bit residual<1.73e-77. This is NOT a counterexample to1/N or a
vanishing-gap family. See audits/controls/gaudin_charge_tracking/control.py
and result.json. No old controls were rerun.
Finite success can only fail to falsify, never prove a uniform gap.

Classical attacks required: exact diagonalization within fixed M, actual
quadratic Bethe equations and their known homotopy/Newton continuation;
MPS/tensor approximations only with paid bond/entanglement guarantees;
known one-site/determinant correlators and CT sparse-observable estimators
under their actual inputs. If an efficient ALL-prefix amplitude-norm
routine exists, classical sampling/sparse readouts remain matched by the
prior note. Easy M=0,1,N-1,N sectors do not support an advantage. In fact M=1 admits
an exact analytic comparator. For g>0, its N secular roots satisfy
sum_i 1/(v-eps_i)=2/g, and q_i(v)=g/[2(v-eps_i)]. Distinct rootsv,w
give sum_i1/[(v-eps_i)(w-eps_i)]=0 by subtracting the two secular
equations. Thus their charge vectors are orthogonal and each sums to1;
squared pair distance=||q(v)||²+||q(w)||²>=2/N. Atg0 the bitstring basis
pays the sector directly. The rational rank-one one-particle Hamiltonian
and secular root isolation classically pay this sector; this is not the
growing-filling algorithm. It explains why the M=1 floor2 counterexample
cannot invalidate the weaker same-sector gap. Bulk M=Theta(N) is decisive.
Do not infer hardness from absent prefix or failed continuation bounds.

False claim gates: unconditional native efficient preparation, universal
joint gap, generic Bethe solver, strong same-sector floor2, classical
separation, novelty, coherent arbitrary-input transform, quantum execution.

## Next decisive question

Prove or falsify polynomial SAME-SECTOR joint separation for an explicit
natural growing-N family (e.g. eps_i=i, g in[0,1]). Further work must address
that actual operation, not another mesh/filter/label wrapper. A failure of
a stronger constant lower bound is not a failure of inverse-polynomial gap.

## Paid independent obligations and dispositions

Two distinct requests were made with explicit source packets and high effort,
24576 output-token cap each. Initial local validations rejected PDF form-feed
characters before any API call; the plain-text packet was repaired, with no
paid retry. Both actual API runs are now terminal and reaped.

- audits/claude_runs/2026-11-07-gaudin-tracking-proof, Opus5-5,
  statusTRUNCATED/max_tokens,8056bytes of partial response,
  input5565/output24576, usage estimateUSD0.513780. This is NOT a completed
  review. Parent read the full available response. Its QPE alternative
  correctly requires uniform tail amplification and amplitude-level leakage
  accounting; those cautions are accepted. Its L5 displayed norm identity
  omits the target tail outside its good-outcome set; adding that term still
  yields the claimed m*eta bound. Initial rank and known label cannot supply
  an endpoint-to-start branch map. The partial QPE construction is not used
  to establish the simpler randomized-dephasing theorem, which has separate
  complete source/core review. No blanket approval or new gap result accepted.
- audits/claude_runs/2026-11-07-gaudin-gap, Fable5-1,
  statusTRUNCATED/max_tokens,EMPTY response, input5343/output24576,
  usage estimateUSD1.282230. No findings; no retry or inference from it.

Combined estimateUSD1.796010, not an invoice or account balance. The owner
continues to authorize useful spending of the dedicated expiring allocation;
no additional call is justified solely to repeat these unfinished questions.

## Completed classical attacks and review boundary

The exact N3 floor2 counterexample above is frozen separately from the
bounded bulk-sector test. bulk_control.py/bulk_result.json checks exactly
12 native rational cases: N4,M2 and N6,M3, sitesi and one stated clustered
irregular pattern each, g=1/10,1,10. Exact commutator/quadratic/sum identities
pass; numerical simultaneous-eigenvector residuals are below2.03e-12.
No numerical candidate violating1/N occurred. The smallest observed squared
gap is1.0750245619 atN6,M3,eps=(0,1,2,3,4,5),g1, above1/6. This is
FINITE NONFALSIFICATION ONLY, not a lower bound, scaling evidence or proof.
One residual failure was repaired by using alternative fixed rational
linear combinations for diagonalization, without changing physical cases.
The old M1 fixture and previous-pass controls were not rerun.

Parent read both complete CLOSED reviews:
- audits/reviews/2026-11-07-gaudin-tracking-core.md;
- audits/reviews/2026-11-07-gaudin-tracking-source.md.
Their rational-clock and trace-distance-convention repairs are incorporated.
Parent independently checked the norm/channel/derivative arguments and actual
primary source scope. Source use is conditional composition, not evidence
that a universal gap has been proved. Both finite scripts were fully read.

Independent selection compared this operation with native growing-degree
Legendre reconstruction (copy input, coefficient output, known exponential
mask resource and classically matched chosen SQ features) and scalar OPI
(expanded halfset tables, verified high-score polynomial, published adaptive
basis-pivot comparator). Their existing contracts and falsifiers remain in
LEGENDRE_HANKEL_RESULTANT_READOUT.md and SCALAR_OPI_NATIVE_PRIORITY.md.
Neither comparison identified a new operation removing its main blocker.
Gaudin ranks first here because the explicit charge channel removes one
actual source assumption; no commitment to keep extending it by inertia.

The scoped milestone is audits/controls/gaudin_charge_tracking/checkpoint.json.
Do not add a new filter, QPE implementation, broad scan or agreement review.
Next hard work must derive an actual bulk-sector polynomial-gap inequality
or a counterexample family; independently compare external value first.
