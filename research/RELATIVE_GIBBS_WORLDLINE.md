# Relative Decoding Meets Correlated Classical Pinning

2026-10-20. LOCAL DERIVATION REVIEW PENDING. No novelty, quantum advantage,
universal no-go, or central registry promotion is claimed.

Producer: `python theorems/relative_gibbs_worldline.py --write`.
Artifact: `research/classical_baselines/relative_gibbs_worldline.json`.
Tests: `tests/test_relative_gibbs_worldline.py`.

Scoped follow-up: `COHERENT_GIBBS_READOUT.md` now supplies a bounded
classical estimator for canonical-TFD two-sided Pauli expectations in
the conditional-product subfamily with no quantum-block interactions.
It includes an explicit pin sampler and arithmetic/statistical error
ledger. This does NOT extend the present interacting-chain sampler to
general coherent readout; the new tests exhibit an interaction that
invalidates the product contraction.

## Question And Literature Decision

Can a constructively decoded source-to-target Hamiltonian route escape the
current sparse-CSP receiver bottleneck?
[Shang, Wang and Stilck Franca](https://arxiv.org/abs/2610.06667), Theorem 8.1,
already give such a chain construction. Their Appendix B.3 already proves
that the Pauli quotient removes central directions. Neither is our discovery.
The [companion framework](https://arxiv.org/abs/2609.35101) supplies relative
polynomial transduction. Reimplementing these as new mechanisms would be
misleading. Their coherent-state output is stronger than a classical sample.

The useful new repository question is a matched classical output-law analysis.
[Crosson and Slezak](https://arxiv.org/abs/2002.02232) establish worldline heat-bath
methods for high-temperature Ising simulation. Our existing
`PARITY_BLOCK_USD_PRANGE.md` supplies the classical pin-and-solve precedent.
Below is a local extension to a CORRELATED source, with an explicit error
ledger. It needs independent mathematical and literature review.

## Exact Input And Output

The public input is a binary r-by-N matrix F and real coefficients of
magnitude at most J0. Write c_i(R)=product_a R_a**F[a,i], with R_a in {+1,-1}.

    H_B = sum_i [a_i X_i + b_i Z_i + e_i c_i(R)
                         + h_i c_i(R) Z_i] + sum_i j_i Z_i Z_(i+1).

All coefficients, F and beta are available classically. There are no hidden
fields, samples from the answer, partition-function oracles or quantum inputs.
The task audited here is sampling a computational-basis measurement of
exp(-beta H_B)/Z_B, including a charged ABSTAIN outcome. It is NOT preparing
that density operator, the canonical TFD, or arbitrary measurements of a TFD.
Conjugating by single-qubit Z operators makes every transverse coefficient
negative without changing this output distribution.

The source H_A replaces F by the N-by-N identity: its central signs c_i are
independent variables, but their Gibbs distribution is NOT independent of
the quantum chain. The parity code is ker F. Its minimum distance d is a
proof premise, not inferred from successful samples or a failed attack.

## Correlated Source Pinning

Use M symmetric Trotter slices. A chain worldline q_i has M signs and periodic
boundary conditions. Its transverse weight is

    phi_i(q_i) = tanh(beta*abs(a_i)/M)**number_of_flips(q_i).

Let W(q) contain these weights and the b,j interactions. Define

    g_i(q) = e_i + h_i * mean_t q_i(t),
    p_i(q) = tanh(beta*abs(g_i(q))),
    s_i(q) = -sign(g_i(q)).

The choice of s when g=0 is immaterial because p=0. After integrating the
source central signs, the exact source path marginal is

    Q(q) proportional to W(q) * product_i 2*cosh(beta*g_i(q)).

Algorithm:

1. Classically sample the FULL source path system by whole-worldline heat
   baths, then discard its central signs. Retain q, not merely one time slice.
2. Independently include i in T with probability p_i(q).
3. If columns F_T are dependent, output ABSTAIN. Even a consistent dependent
   system is rejected; accepting it uniformly would change the mixture law.
4. Otherwise solve c_i(R)=s_i(q), i in T, and choose ALL free R bits uniformly
   using exact GF2 elimination. Return (q(0),R).

No decoder, enumeration, rare source conditioning or retry is used. Source
correlations are retained in both Q(q) and the path-dependent pin probabilities.

### Output-Law Proof

The local identity is

    exp(-beta*g_i*c_i) / cosh(beta*g_i)
      = (1-p_i) + 2*p_i * 1[c_i=s_i].

Expand the product into pin sets. Conditional on q, let v_q(T) be their
independent Bernoulli probability. The UNNORMALIZED target joint extension
on (q,T,R), normalized relative to the source, has weight

    Q(q) v_q(T) 2**(|T|-r) 1[F_T^T R_bits = preferred_bits].

For full-column-rank T, summing over R gives exactly Q(q)v_q(T). This is
precisely the algorithm's accepted subdistribution G. For dependent T the
factor is 2**nullity(F_T), or zero if inconsistent. These are not uniform
mixture weights and cannot be silently dropped.

Set A(q)=sum_(0!=z in ker F) product_(i:z_i=1) p_i(q). Counting kernel vectors
supported on T proves the identity

    E_T [2**nullity(F_T)-1] = A(q).

Thus the probability u of ABSTAIN is at most A=sup_q A(q). The target's bad
extension mass b is at most A+u, hence at most 2A. Its total relative mass is
Z=1-u+b >= 1-A. Compare both laws with G/(1-u). Including ABSTAIN gives

    TV(algorithm, target_Trotter) <= A + 2A/(1-A),  provided A<1.

Clamp the bound to one when it is uninformative. Marginalizing T and all but
the first time slice cannot increase TV. This proof does not assert that
discarding ABSTAIN produces an exact target sampler: the finite controls
explicitly exhibit residual bias after that uncharged postselection.

### Distance-Only Bound And The Published Window

Since abs(g_i)<=2J0, set p=tanh(2 beta J0). Then

    A <= sum_(w=d)^N binomial(N,w) p**w
      <= binomial(N,d) p**d / [1-(N-d)*p/(d+1)]

when the denominator is positive. If Np/d<1/5 this is at most
(5/4)*(e/5)**d. The producer retains a logarithmic bound to avoid interpreting
floating underflow as exact zero.

In the published chain certificate, d>2*tau*N and beta<tau/(5J0), with
tau a fixed positive unique-decoding radius fraction. Hence Np/d<1/5.
The pinning error is exponentially small when d is linear. A nontrivial code
has tau<1/2, so beta J0<1/10. The easy SOURCE has block influence at most
3*tanh(beta J0)<0.3, regardless of the target matrix's row/column weights.

**Local conclusion:** throughout that stated norm/Taylor temperature window,
this chain family's computational-basis samples have a polynomial classical
algorithm to inverse-polynomial TV accuracy, for sufficiently large N. This
uses the SAME distance premise as the quantum construction, but no decoder.
The finite implementation reports its explicit pinning error, not an
arbitrarily small requested error that ignores the exponential residual.

This does not refute efficient TFD preparation. It does not cover all source
Hamiltonians, lower-temperature refinements, nonstoquastic sources, or a task
requiring coherent access to the purification. It is not a lower bound on
every quantum algorithm. The code family is not being declared easy for
decoding, minimum-distance computation, or unrelated cryptographic tasks.

## Implementable Source, Outward Interval Lowering, And Error Ledger

For a worldline i, changing its neighbor's entire path changes the conditional
log density by an oscillation at most 4 beta abs(j_i). The likelihood-ratio
TV inequality gives influence tanh(beta abs(j_i)); the same argument gives
tanh(beta abs(h_i)) for a central/quantum pair. On the identity-parity source
there are no central-central edges. For B=2N blocks and alpha<1, random-scan
maximal coupling gives

    worst_start_TV(t) <= B exp(-(1-alpha)*t/B).

Each periodic worldline conditional is sampled by O(M) two-state backward
messages, conditioning first on its initial spin. A central conditional is
a single logistic coin. Neither procedure enumerates 2**M paths. Zero
transverse fields and beta=0 keep only constant paths and remain supported.

To discharge the conditional-update numerical allowance reserved by
`sampling_budget`, `exp_interval`, `tanh_interval`, `logistic_interval`,
`interval_ring_path`, `interval_central_update`, and `interval_pin_given_paths`
evaluate the multiplicative periodic-path backward messages, central logistic
probabilities, and source-pin probabilities using outward dyadic rational
intervals $[p_-, p_+]$. `draw_interval_bernoulli` refines dyadic coin prefixes
against $[p_-, p_+]$ up to `max_coin_bits`, guaranteeing single-step conditional
TV perturbation at most $(p_+ - p_-) + 2^{-\text{max\_coin\_bits}}$ under fair
coins. `certified_interval_update_audit` verifies that every periodic-path and
central update has total conditional TV strictly within
`conditional_TV_tolerance_per_update = epsilon / (3 * updates)`. Software PRNGs
remain explicitly flagged as uncertified coin sources (`prng_is_not_a_certified_fair_coin_source = True`).

For completeness, the implementation also samples the TARGET directly.
Its majorant includes central-central entry
tanh(beta*sum_shared_i(abs(e_i)+abs(h_i))). This bound can fail badly while
the source-pinning algorithm still works. It is not used to reject that route.

Trotter control is independent of geometry. Let H=V-G, K>=norm(V)+norm(G),
a=beta K and S=exp(-beta V/(2M)) exp(beta G/M) exp(-beta V/(2M)). Matching
Taylor coefficients through degree two bounds

    norm(S-exp(-beta H/M)) <= (a/M)**3 exp(a/M)/3.

Both positive matrices have minimum eigenvalue at least exp(-a/M). The
integral formula for the operator logarithm is Lipschitz with constant
exp(a/M), so norm(M log S + beta H)<=a**3 exp(2a/M)/(3M**2).
The Gibbs variational identity bounds relative entropy by twice this value;
Pinsker gives trace distance, and hence diagonal TV, at most its square root.
Choosing M=O((beta K)**(3/2)/epsilon) is polynomial. No exponential
exp(beta K) prefactor is hidden in this argument.

## Falsifiers And Decision

- Exhaust every path, pin set and affine solution on a bounded noncommuting
  input. Check the full law and ABSTAIN, not only energy or acceptance.
- Remove source correlations as a deliberate wrong-source control; the
  claimed small-error bound must fail. Preserve all free affine coordinates.
- Check the periodic conditional against its entire direct probability law,
  both in floating point and inside certified outward rational intervals,
  and target Trotter diagonals against independent matrix exponentiation.
- Exhaust boundary pairs and all starting states for the finite heat-bath
  chain. Treat a failed influence certificate as UNKNOWN, not hardness.
- Check a high-incidence repetition-code calibration where target mixing
  fails but source pinning succeeds. This known easy code is NOT an algorithm
  discovery candidate. Its distance is witnessed by a one-dimensional kernel.
- A new source with signed worldline weights does not satisfy this proof.
  A better quantum temperature window must be rechecked quantitatively.
- A TFD task must specify a coherent observable/output that these diagonal
  samples cannot reproduce, plus its strongest classical estimator.

Do not fund another large receiver or benchmark campaign for a diagonal
sampling advantage in this specific certified window. Next theory work must
identify a concrete coherent-output task or change the source in a way that
actually breaks the positive sparse-pinning argument.
