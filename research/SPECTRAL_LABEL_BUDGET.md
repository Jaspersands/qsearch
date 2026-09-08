# Spectral Label Budget

## Decision

Stop seeking an inverse-polynomial **minimum adjacent eigenvalue gap** in a
single bounded-norm separator that labels every direction in a typical
hidden-involution branching multiplicity. This target is incompatible with
the source law already used by the project. Finite scalar-commutant evidence
remains useful for algebra generation, but does not evade this obstruction.

This is an elementary derivation, not a new quantum lower-bound result or a
machine-checked formal proof. Independent mathematical review remains open.

## Derivation

Let G=S_(2m), K=C2 wr S_m and h be the fixed-point-free involution centralized
by K. On an h-even branch (lambda,mu), write b for the branching multiplicity.
The one-coordinate source law is q=2 d_lambda d_mu b / |G|. The conditional
source is the identity on this multiplicity factor. Set

    I_(2m) = sum_lambda d_lambda
    J_m^+ = sum_(h-even mu) d_mu
    C_m = 2 I_(2m) J_m^+ / (2m)!.

For every nonnegative integer L, dropping the branching compatibility
restriction only increases a sum of nonnegative terms, so

    q{b <= L} <= min(1, L C_m).

An operator with norm at most one has spectrum in [-1,1]. If all b
eigenvalues are distinct and their minimum separation is delta, then

    (b-1) delta <= 2.

For r commuting Hermitian contractions, encode a joint eigenvalue vector
x by the r integers floor((x_j+1)/delta). Two vectors in the same cell differ
by less than delta in every coordinate. Thus pairwise delta-separated joint
labels require

    b <= (floor(2/delta)+1)^r = L,
    source mass with such a complete label system <= min(1, L C_m).

Endpoint cells are included. Commutativity is essential to the joint-eigenbasis
interpretation. A numerical scalar common commutant does not supply it.

For an elementary asymptotic estimate, use Cauchy-Schwarz and the regular
representation dimension identities:

    C_m <= 2 sqrt(p(2m) p_2(m) / M),  M=|G|/|K|=(2m-1)!!.

Here p_2 counts all bipartitions; including odd parity makes this conservative.
The crude bounds p(n)<=2^n and p_2(m)<=(m+1)2^m already suffice. Since
log(M)=m log(m)+O(m),

    log(C_m) <= -0.5 m log(m) + O(m).

For fixed r,c and delta=m^-c, L is polynomial. Hence L C_m vanishes faster
than every inverse polynomial. The report evaluates the stronger exact I,J
bound with integer arithmetic, not this loose partition-count estimate.

## Average Decoding Variant

Small minimum gaps alone do not imply poor average performance. A separate
counting argument applies when a task asks to recover a uniformly selected
copy eigenlabel j in a known branch, and the decoder receives **only** a
classical transcript y taking at most L values. Its best success probability
is at most (1/b) sum_y max_j P(y|j) <= L/b. Averaging gives

    E_q[min(1,L/b)] <= min(1,L C_m).

This also bounds a depth-t adaptive transcript tree with at most B outcomes
per step by setting L=B^t. The report computes a necessary depth for half of
the source mass. This is a capacity requirement, not a construction.
The transcript alphabet must be specified explicitly: noisy real-valued
estimates are not automatically a bounded alphabet.

## Attempts to Refute the Recommendation

### Separate Tensor-Multiplicity Source Law

The older TT1+TC1 separator scans use Kronecker multiplicities, not K-branching
multiplicities. Their source law must be derived separately. For k independent
Plancherel registers in S_n fused to nu, let g be the tensor multiplicity.
The joint law is

    q_0(lambda_1,...,lambda_k,nu) = (prod_i d_lambda_i) d_nu g / (n!)^k.

It normalizes because sum_nu d_nu g = prod_i d_lambda_i. Consequently

    q_0{g <= L} <= min(1, L I_n^(k+1) / (n!)^k).

An order-two coset density matrix satisfies rho_h <= 2 I/|G|. Conditional on
one fixed h, k independently prepared coset registers therefore satisfy
rho_h^tensor(k) <= 2^k I/|G|^k. This positive-operator inequality is preserved
by a common unitary, a measurement, and averaging over h. Thus for the
unpostselected physical coset input,

    q_h{g <= L} <= min(1, 2^k L I_n^(k+1) / (n!)^k).

For fixed k>=2 and polynomial L, I_n<=sqrt(p(n)n!) shows that this bound
vanishes superpolynomially. The same spectral packing argument now applies
to complete tensor-multiplicity spectra. This excludes a typical complete
fixed-count gapped-label claim, not the finite simple spectra already found.

Crucial limits: do not condition on a handpicked lambda tuple and keep the
same bound; postselection changes probabilities. Do not claim that the
conditional physical multiplicity state is maximally mixed. The uniform
copy-label average-decoding argument above is NOT transferred to this model.
For growing k, use the explicit bound instead of a fixed-k asymptotic statement.

There is also a separate argument for the exact maximum-dimension pair used
in the old finite scans. For lambda maximizing d_lambda, the *dimension*
target law is q_dim(nu)=d_nu g(lambda,lambda,nu)/d_lambda^2. It obeys

    q_dim{g<=L} <= L I_n/d_lambda^2 <= L I_n p(n)/n!.

The last inequality follows from sum_lambda d_lambda^2=n! and the p(n)
possible source partitions. For polynomial L the bound vanishes. In
particular, at least one occupied target has superpolynomial multiplicity,
so a single normalized complete separator cannot retain inverse-polynomial
minimum gaps on *every* target of these maximum-dimension sources. This
argument does not pretend q_dim is the conditional physical coset law.

### Escape Audit

- **Use multiple observables.** A fixed number does not fix the capacity
  problem; a growing hierarchy can. Polynomially many label bits are sufficient
  in principle, so the result supplies no superpolynomial circuit lower bound.
- **Use a noncommuting generator algebra.** Scalar commutant proves generation
  in exact arithmetic, not efficient joint diagonalization. Noncommuting
  procedures are outside the simultaneous spectral-label assumption.
- **Resolve only the relevant information.** This is a genuine escape. An HSP
  decoder need not recover all multiplicity basis labels. Neither bound above
  measures information about the unknown involution itself.
- **Choose separators per branch.** Packing holds separately on every branch;
  choosing coefficients adaptively from the branch does not change it.
- **Fast-forward a Hamiltonian or keep quantum memory.** This may bypass the
  proposed inverse-gap-cost argument. No time/query lower bound is asserted.
- **Most mass avoids the closest eigenpair.** This defeats an inference from
  minimum gap alone. Use the separate finite-transcript bound only when its
  uniform-label and no-side-information assumptions actually hold.
- **Change the source distribution.** Re-derive the bound. It is not licensed
  for arbitrary correlated multi-copy sources or postselected ensembles.

## Next Research Contract

Develop a polynomial-depth, source-aware hierarchy of coarse projectors, or
a direct subduction transform. Each proposal must specify reversible access,
normalization, conditional mass, accumulated error, and what information
about the hidden involution survives. Arbitrary dense eigendecomposition
followed by binary encoding of its eigenvectors is not an implementation.

The surrounding literature already distinguishes an efficient symmetric-group
QFT from an HSP decoder: [Beals, STOC 1997](https://doi.org/10.1145/258533.258548)
provides the former; [Moore, Russell and Schulman](https://arxiv.org/abs/quant-ph/0501056)
give a strong single-register Fourier-sampling obstruction. Neither source
is claimed to prove the project's specific packing calculation.
