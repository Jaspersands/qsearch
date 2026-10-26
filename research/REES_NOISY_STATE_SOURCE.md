# Noisy Copies: Principal-Eigenstate Symmetry With Paid Purification

2026-10-22. A costed composition of KNOWN streaming purification with the
proposed Rees receiver. Not a new purification algorithm, fault-tolerance
theorem, independently verified HSP algorithm, or demonstrated speedup.

COPY-ONLY COSET BOUNDARY: NOISY_COSET_LPN_BOUNDARY.md gives an exact
sample-to-state reduction for globally depolarized mixed abelian cosets.
Its binary case is known LPN; odd primes have an explicitly different
q-ary noise law. Balanced symmetric purification of a flat rank-r coset
projector needs Omega(r) levels for constant improvement, unlike this
nondegenerate principal-state contract. This does not refute clean Rees
recovery or rule out other noisy decoders.

## 1. The Blocker And The Revised Task

The exact mixed scalar-support task in REES_PROJECTIVE_STATE_SOURCE.md is
not a noise-robust version of pure-state symmetry. If rho has full rank,

    |Tr(rho R(g))|=1  iff  R(g) is scalar on the ENTIRE Hilbert space.

Consequently, any nonzero global depolarizing admixture erases all state-
dependent exact ray stabilizers in that contract. This is not cured by
sampling more overlaps. Nor does a finite purification round restore the
exact stabilizer: full-rank input remains full rank after every round.

Instead, supply fresh IID copies of rho whose principal eigenvector psi
is nondegenerate, with a supplied spectral gap lower bound

    lambda_1(rho)-lambda_2(rho) >= Delta > 0.

Learn the RAY STABILIZER OF psi, not the scalar-support stabilizer of rho
or its conjugation symmetries. The existing explicit exponent-p Lazard
group, fixed class c<p and controlled LINEAR R contract is unchanged.
The principal state must have the separate GLOBAL orbit-gap promise

    |<psi|R(g)|psi>| <= 1-gamma for every g outside H_psi.

Delta and gamma are distinct resources. Neither is certified by the
planner or finite tests. For rho=(1-eta)|psi><psi|+eta I/d with known
eta<=eta_max<1, Delta>=1-eta_max. Arbitrary noise does NOT identify the
original pre-noise state with the principal eigenvector. Fixed constant
Delta gives the polynomial-time consequence below; shrinking Delta is
charged and is not automatically efficient.

## 2. Known Physical Protocol, Not Virtual Distillation

The recursive SWAP-test protocol is due to
[Childs et al.](https://arxiv.org/abs/2309.16387), with general-spectrum
analysis by [Grier et al.](https://arxiv.org/abs/2503.22644). We reuse it;
the conservative elementary bounds below are for our explicit cap/error
contract, not an improvement over their sharper bounds.

On TWO INDEPENDENT copies, project onto the symmetric subspace, discard
one target and keep the other only on the symmetric outcome. Then

    p_success = (1+Tr(rho^2))/2 >= 1/2,
    rho_next = (rho+rho^2)/(1+Tr(rho^2)).

Rejecting consumes both inputs. Ignoring the herald gives rho again, not
the purified state. The normalized operator rho^2/Tr(rho^2) is NOT this
physical output. The two retained targets after symmetric projection
are generally correlated, so returning both as independent copies is
also invalid. There is no conjugate copy, inverse preparation, unknown
eigenvector projector, or unknown-state reflection in this protocol.

At level j, acquire two independent successful level-(j-1) outputs; retry
that merge after failure. Fixed level and IID inputs make the accepted
output independent of the number of earlier failed attempts. An iterative
stack implements the same recursion, with at most K+1 input registers and
one SWAP-test ancilla at depth K. The standard controlled-SWAP gate acts
on the whole encoded register and costs O(log d) elementary Fredkin gates.

## 3. Explicit Dimension-Independent Envelope

Write a=lambda_1, b=lambda_2, e=1-a, P=sum_j lambda_j^2. The update gives

    (a-b)_next = (a-b)(1+a+b)/(1+P) >= a-b,
    (lambda_j/a)_next = (lambda_j/a)(1+lambda_j)/(1+a).

The first inequality uses P<=a. Thus every nonprincipal-to-principal
ratio contracts by at most q=1-Delta/2, throughout the recursion. Initially
e/a<=(1-Delta)/Delta. Put

    b_bits = ceil(log_2(max(1, 7*(1-Delta)/Delta))),
    K0 = ceil(2*b_bits/Delta).

Because q^K0<=exp(-b_bits)<=2^-b_bits, after K0 burn-in levels e/a<=1/7,
hence e<=1/8. Each level has expected cost factor 2/p_success<=4; the
burn-in costs at most 4^K0 raw copies per intermediate output. This bound
is loose and becomes enormous as Delta shrinks. It is NOT a lower bound
or a claim that sharper published algorithms cannot do better.

For the low-error tail let S=sum_(j>1) lambda_j^2<=e^2. Then

    e_next = (e+S)/(1+(1-e)^2+S)
           <= e*(1+e)/(2-2e+2e^2)
           <= (2/3)*e,                         e<=1/8,
    e_next <= e/(2*(1-2e)).

The first ratio is increasing in S. The last two bounds follow by
cross-multiplication of positive denominators. Consequently sum_j e_j
over the tail is <=3e_0<=3/8. Using product(1-u_j)>=1-sum u_j,

    e_L <= e_0*2^-L / product_(j<L)(1-2e_j) <= 2^(-L-1),
    product_(j<L) p_success,j >= product_(j<L)(1-e_j) >= 5/8.

Here p_success>=a=1-e. Choose L=ceil(log_2(1/delta)) for desired
single-output trace distance delta<=1/8. Since the eigenbasis is unchanged,
TD(rho_(K0+L), |psi><psi|)=e_(K0+L). Expected raw cost per output is at most

    C <= 4^K0 * 2^(L+1) < 4*4^K0/delta.

This is uniform in Hilbert-space dimension. Delta fixed makes C=O(1/delta),
with a Delta-dependent constant. Our displayed burn-in is not polynomial
uniformly in 1/Delta. Dimension-independent sample complexity still costs
log d gates per SWAP and (K0+L+1)*log d memory bits/qubits for purification,
in addition to the downstream receiver's registers and computation.

## 4. A Hard Clock Without Hidden Postselection

Let T bound EVERY ideal pure copy requested by the complete Rees run.
The uncapped process to supply T outputs has expected raw cost <=T*C.
Given whole-stream abort allowance beta, impose ONE global raw-copy cap

    N_cap = ceil(T*C/beta).

Abort the whole algorithm if another acquisition would exceed the cap.
Markov's inequality bounds this event by T*C/N_cap<=beta. Do not restart
the global cap for each leaf or accept a partial receiver answer after an
abort. There are at most N_cap SWAP tests, since each merge decreases the
number of live registers by at least one. All rejected raw inputs count.

Couple this process to the uncapped fresh-IID recursion: until the cap is
hit they agree; thereafter the capped one emits ABORT. This bounds the
complete output difference, including herald records. It does not divide
by a rare branch's probability or infer independence from marginals. A
variable runtime is not a new state-preparation inverse.

The opaque-token controller capped_purification_stream implements this
stack, hard clock, rejection consumption, streaming delivery and cleanup.
It never sees amplitudes, eigenvectors or H. Its backend must implement
the stated physical symmetric instrument and fresh-copy acquisition.
The tested controller is not itself a quantum gate backend.

## 5. Composition With The Full Rees Tree

For total error epsilon, call projective_source_budget with epsilon/2.
Its T includes all M copies per moment-design block, all amplification
blocks, and every discarded leaf in the receiver source tree. Set

    delta = epsilon/(8T),   beta = epsilon/8.

Replace its ideal pure copies by independently purified outputs. A hybrid
over the COMPLETE receiver circuit adds at most T*delta<=epsilon/8,
even with adaptive measurements. Add beta for the global clock and reserve
epsilon/8 for all purification implementation errors. The inherited ideal
budget is <=epsilon/2, so total error is <=7epsilon/8, leaving slack.

There are at most N_cap acquisition operations and N_cap SWAP instruments.
The implemented budget allocates epsilon/(16*N_cap) complete-channel error
to each. Divide further among primitive gates in an actual backend. This
comparison includes all branches and ABORT; there is no normalized-branch
precision amplification. Controlled group-action errors were already
reserved in the inherited ideal budget. The raw IID noise model is a
source promise, not something instrument precision can manufacture.

For fixed Delta this gives expected O_Delta(T^2/epsilon) raw copies and
a hard O_Delta(T^2/epsilon^2) cap. At constant total error it preserves
polynomial time IF the entire proposed Rees receiver is correct. These
are upper bounds, not optimized exponents. The explicit schedule has
polynomial rather than logarithmic dependence on 1/epsilon; a separately
costed whole-algorithm confidence amplification can be used when appropriate.

No approximation is declared to satisfy exact scalar symmetry. The target
is psi throughout. Finite purified copies still have scalar-support kernel
only; the hybrid to the ideal psi circuit is the reason recovery can work.
No noisy mixed coset state is purified instead: its top eigenspace may
be highly degenerate, and purifying before tracing the original targets
is a different access model from receiving only those coset states.

## 6. Attempt To Disprove The Repair

- CORRELATED SOURCE: sum_i lambda_i |ii><ii| has the correct single-copy
  marginals. Its symmetric test succeeds with probability one but leaves
  rho unchanged. Success rate and correct marginals do not prove IID.
- COHERENT ROTATION: if the actual principal vector is phi!=psi, the
  protocol converges to phi. Even a small coherent rotation can remove
  an exact symmetry. General original-state recovery is not implied.
- DEGENERATE TOP: equal leading eigenvalues remain equal. A mixed code
  projector does not become its unknown pure component under this method.
- LOCAL NOISE: tensor-product local depolarization on growing registers
  need not retain a constant principal weight/gap or the same principal
  vector. It is not the global depolarizing model. No hardware threshold.
- VANISHING GAP: the cost can be superpolynomial despite a well-defined
  principal state. Preserve the spectral parameter; it is not gamma.
- UNHERALDED/REUSED OUTPUTS: forgetting outcomes gives no purification;
  returning both correlated targets breaks subsequent tensor contraction.
- CLASSICAL COMPARISON: if the input supplies a sparse/tableau/low-width
  description, its existing learner can remain superior. A quantum-input
  noise repair does not create a classical-input speedup.

The finite controls check the actual two-copy projector and partial trace,
not just the eigenvalue formula; exact rational tail bounds; runtime caps
and disjoint lineages; and a noisy nonnormal UT3 orbit source. None of the
planted controls is admitted as a research candidate.

## 7. Decision And Next Scientific Question

Keep this known purification dependency as a viable route for CONSTANT-
GAP principal-eigenstate symmetry, especially known global depolarization.
Do not reject the copy-only route merely because its raw source has full
rank. Equally, do not describe it as generic noise correction or promote
the unreviewed Rees theorem. The costs remain impractical on the class-nine
profile, and a natural hard application has not been established.

The initial polynomial-phase application screen did not justify a new
candidate. Translation-plus-polynomial-phase groups have abelian derived
subgroup, so do not specifically require the newly broader Rees scope.
[Arunachalam et al.](https://arxiv.org/abs/2208.07851) give an efficient
fixed-degree BINARY separable learner. Their generalized Boolean-domain
phase learner has polynomial sample complexity but not a stated polynomial
runtime (Table 1 and Section 5); the earlier blanket efficiency claim was
too broad. Neither promise is automatically the growing-prime qudit task.
POLYNOMIAL_PHASE_COPY_LEARNING_BASELINE.md now gives an access-matched
direct route for full-domain fixed-degree F_p phase copies by adapting the
known Ivanyos--Santha elimination, without requiring the Rees receiver.
This is a quantum baseline under review, NOT classical dequantization.

Next: independent whole-receiver scrutiny or a motivated nonabelian
principal-state problem with PROVED spectral and orbit gaps. A local-noise
threshold, arbitrary noisy-coset purification, full Clifford symmetry
learning and a Shor-level application are all still unsupported. Mechanical
backend work should not be mistaken for resolving those scientific questions.

Standalone replay: `python -m theorems.rees_noisy_state_source --write`.
