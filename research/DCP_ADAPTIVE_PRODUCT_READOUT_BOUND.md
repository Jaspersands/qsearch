# Fixed-Order Adaptive Native Readout: A Narrow Collective Gap

LOCAL DERIVATION / REVIEW PENDING. No novelty, independent theorem review,
accepted candidate, efficient PGM circuit, decoder or speedup is claimed.

## Research Decision

Feedback cannot be screened using the earlier independent-product bound.
The new bound covers a strictly larger measurement class, but is much weaker.
At exactly the secret entropy width it certifies a source-mean collective
measurement gap. With two surplus qubits it becomes vacuous. In particular,
it does NOT close the repository's native m=n*log2(q)+16 decoding target.

This is a measurement-resource diagnostic, not another promising algorithm.
It prioritizes constructing a costed collective primitive, or a genuinely
source-valid feedback decoder beyond the gate, over repeating fixed-axis tests.

## Native Source And Measurement Class

Let q=2^L, G=q^n, A have IID uniform entries in Z_q, and let the unknown s
be uniform in Z_q^n independently of A. Receive exactly m qubits

    tensor_i (|0>+exp(2*pi*i*<a_i,s>/q)|1>)/sqrt2.

Each qubit is measured once to completion in a fixed physical order chosen
independently of A and outcomes. The current qubit's arbitrary POVM can depend
on ALL A and all earlier classical outcomes. Local private ancillas are allowed;
no quantum information may survive to couple different input qubits. Unlimited
computation on the resulting classical record is allowed. Abstention fails.

Shared randomness, including a prelabel random order, is covered by conditioning.
Label/outcome-adaptive ordering, interleaved weak measurements with revisits,
retained quantum memory, entangled preprocessing, additional supplied samples,
or selecting a favorable input batch are NOT covered. Do not relabel sorted
columns as IID and silently apply the fixed-order source theorem.

## Refinement And Weighted Collision

Write an effect as w*(I+r*sigma), w>0, |r|<=1, with sum w=1 and sum w*r=0.
Only r_x,r_y affect these equatorial inputs. Set R=|(r_x,r_y)| and split the
projected effect into two equatorial rank-one effects with weights
w*(1+R)/2 and w*(1-R)/2 and opposite unit xy directions. At R=0 choose any
direction. The sum has exactly the original probabilities on every phase state.
This projection/refinement is valid on this ensemble, not an equality of the
original out-of-plane operators. Future POVMs use the COARSE prior outcomes,
so the refined tree actually simulates the old controller without changing it.

For a leaf y let Q_y be the product of its conditional effect weights. This is
a normalized reference tree distribution, NOT uniform over leaves. The refined
likelihood is ell_s(y)=product_i(1+r_ix*cos(theta_i)+r_iy*sin(theta_i)).
Success and weighted collision cannot decrease when revealing refinement labels:
maxima are subadditive, and coarse collision obeys weighted Cauchy. For the
optimal arbitrary classifier on the refined record,

    P_A(correct)^2 <= C_A/G,
    C_A = E_s sum_y Q_y*ell_s(y)^2.

Proof: partition leaves into decision regions D_s. Cauchy bounds the squared
sum of Q_y*ell_s(y) over those regions by the product of sum_(s,y in D_s)Q_y
(at most 1) and sum_(s,y in D_s)Q_y*ell_s(y)^2 (at most G*C_A), divided
by G^2. This includes arbitrary classical/quantum computation on the record.

## What Feedback Does To The Fourier Expansion

For each refined equatorial direction put a=r_x-i*r_y, |a|=1. The squared
local likelihood has coefficients

    c_0=3/2, c_1=a, c_-1=conjugate(a),
    c_2=a^2/4, c_-2=conjugate(a)^2/4.

Expand the tree average in delta in {-2,-1,0,1,2}^m. If the LATEST nonzero
delta_i is linear (+1 or -1), its coefficient is zero. Collapse all later
zero-frequency tree levels: each contributes 3/2 regardless of the axis and
its branch weights sum to 1. At that latest level, sum w*a=0 by completeness.
Earlier odd frequencies need NOT cancel, because future axes can depend on
the corresponding outcomes. The saved q4 parity controller retains (1,2)
and achieves success 1 on A=(2,1). Dropping all odd terms is false.

Otherwise the absolute coefficient is at most product_i b_(delta_i), where
b_0=3/2, b_(+/-1)=1, b_(+/-2)=1/4. Call this weight W(delta); set it to
zero when the latest nonzero frequency is linear. Secret averaging gives the
simultaneous, controller-independent fixed-A envelope

    C_A <= E_A_fixed = sum_delta W(delta)*1[A*delta=0 mod q].

This remains valid when the WHOLE A chooses every adaptive POVM. It avoids
assuming that the controller's Fourier coefficients are independent of A.

Let H=(q/2)^n and C=(3/2)^m. Even nonzero delta have kernel probability 1/H;
any delta with an odd coordinate has probability 1/G, since an odd coefficient
is a unit modulo q. Total even weight is 2^m. Total allowed weight is

    C + (1/2)*sum_(j=1..m) 4^(j-1)*(3/2)^(m-j) = (4^m+4*C)/5.

Thus W_odd=(4^m+4*C)/5-2^m and

    E_A[P_A(correct)^2] <= B
      = C/G + (2^m-C)/(G*H) + W_odd/G^2,
    E_A[P_A(correct)] <= min(1,sqrt(B)).

This is uniform-secret/source-mean, NOT a pointwise secret or label claim.
The same common envelope yields a Markov typical-label bound B/delta^2,
capped at 1, simultaneously over controllers in this class.

## Collective Benchmark Without A Poisson Heuristic

For x in {0,1}^m let eta_t=|{x:A*x=t}|. Put N=2^m and mu=N/G.
Normalized nonempty fiber vectors |F_t> give the state decomposition
N^(-1/2)*sum_t sqrt(eta_t)*chi_s(t)*|F_t>. Character orthogonality makes
the ensemble average diagonal with eigenvalues eta_t/N. Applying the PGM
on its support therefore gives

    P_PGM(A) = (sum_t sqrt(eta_t))^2/(N*G).

The cyclic DHSP PGM/fiber connection is established in
[Bacon, Childs and van Dam](https://arxiv.org/html/quant-ph/0501044),
Sections 4, 5 and 8. The vector-group formula above follows from the displayed
character decomposition; it is not a claim that their paper states this exact
source bound. An exponential multiplicity table is NOT an efficient circuit.

Average over BOTH IID A and an independent uniform target t. Then

    E eta = mu,
    E eta^2 = mu^2+mu*(1-1/G).

For distinct nonzero Boolean x,y, their 2-column vectors have a 2-by-2 minor
with determinant +/-1, so (A*x,A*y) is uniform in (Z_q^n)^2. If one vector
is zero, random t and the nonzero vector still give joint hit probability 1/G^2.
This accounts for the zero witness rather than incorrectly claiming its fixed
target event is random. Each single hit has probability 1/G. No prime-field
assumption, Poisson limit or independence of all witnesses is used.

Holder, applied to Z=sqrt(eta), gives

    E eta <= (E sqrt(eta))^(2/3)*(E eta^2)^(1/3).

Jensen over A in the PGM formula then proves

    E_A P_PGM(A) >= (1/mu)*(E_(A,t) sqrt(eta))^2
                    >= mu/(1+mu-1/G).

This is a SOURCE-MEAN attainable collective success bound, not high probability,
efficient implementation, a fixed-secret statement, or a lower bound for each A.

## Actual Comparison And Attempt To Break It

At m=nL+Delta, with fixed Delta and G,H growing, B tends to 4^Delta/5.
At Delta=0 the adaptive mean upper tends to 1/sqrt(5), while the collective
mean lower tends to 1/2. Exact ledgers at n=8,16,32, L=4n+1 confirm the strict
gap. This compares source means in one quantum-state task, NOT quantum runtime
against classical computation. It supplies no implementation of either optimum.

At Delta=1 these bounds do not separate the classes. At Delta>=2 the adaptive
bound is vacuous. At L=1 the even-character alias makes it vacuous even at
entropy width; the ordinary binary easy regime is NOT excluded. The collective
lower bound at +16 is high, but the computational bottleneck was already known.

Potential failure checks: out-of-plane refinement is ensemble-specific; future
policy must retain coarse history; rank-one zero coefficients use fixed physical
order; native source probabilities require genuinely IID labels and a uniform
independent secret. Numerical agreement is calibration, not proof review.
Arbitrary POVM outcome spaces can be handled by integrals with the same bounded
coefficients; this compiler tests only finite trees.

The recent [adaptive stabilizer learner](https://arxiv.org/html/2610.02031)
uses repeated copies of one fixed state and changes its basis across copies.
It does not supply duplicate varying native packets. Nor does this single-qubit
fixed-order result exclude adaptive multi-qubit basis changes on native packets.

## Verification And Next Work

- Python module: `theorems/dcp_adaptive_product_readout_bound.py`.
- Tests: `tests/test_dcp_adaptive_product_readout_bound.py`.
- Artifact: `research/classical_baselines/dcp_adaptive_product_readout_bound.json`.
- Independent-language checker: `research/certificates/dcp_adaptive_product_readout_crosscheck.js`.

Complete native censuses cover 16, 512 and 256 matrices, not favorable samples.
They test exact collision envelopes and fiber moments; physical trees test
refinement, optimal record decisions, retained odd terms and Fourier aliasing.
Growing certificates use exact rationals without floating-point underflow.

Next high-value debts: a source-valid feedback/quantum-memory decoder with full
input accounting; a sharper feedback bound that remains useful with +16 samples;
or a costed collective fiber/readout mechanism. Before scaling a guessed local
controller, derive its actual source law and try to falsify its claimed advantage.
Production CLI, registry, full-suite integration and UI remain delegated to Gemini.

Follow-up: [projected PGM normalization audit](DCP_PGM_PROJECTED_ENCODING.md)
constructs an actual public comparison block and charges its herald, exposing
why generic bounded spectral filtering is not a cheap collective decoder.
