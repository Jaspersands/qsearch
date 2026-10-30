# Classical Filter For Finite-Field Tensor-Train Stabilizers

2026-10-29. Independently automated-reviewed mathematical reduction and
guarded executable specialization. No novelty, human peer review, quantum
advantage, or general tensor-network simulation claim.

## Research Decision

An exponentially large orbit span does NOT make the following stabilizer
problem a credible quantum-advantage application. Given an explicit
polynomial-size tensor train over F_p and an explicit sitewise p-group,
its exact stabilizer has a polynomial-time classical reduction to published
matrix-group algorithms. Stop promoting these instances on orbit dimension
alone. This does not invalidate a general Rees HSP theorem; it excludes a
proposed application class with additional public structure.

The implementation is narrower than the mathematical reduction. It implements
the common-nilpotent-algebra regime below, not Luks's general algorithm.
Failure of that guard is UNSUPPORTED, not a hardness certificate.

## Input And Output

An order-N tensor A belongs to the tensor product of V_i=F_p^(d_i), supplied
as exact cores with bond dimensions b_i and boundary bonds one. A group
Gamma is supplied by tuples of invertible local matrices acting on columns.
For the general theorem, Gamma is promised to be a p-group. Matrix entries,
cores, sites, and generators are explicit and charged in the input length.
The output is generators of H={g in Gamma : g A=A}.

No site permutations, semilinear actions, complex MPS amplitudes, numerical
rank thresholds, succinctly encoded exponentially many sites, or arbitrary
tensor networks are covered. A transporter between two tensors is also a
different problem. Individual generators of order p do not by themselves
certify that their generated group is a p-group.

## Prefix-Support Reduction

Let P_i be the tensor product of the first i sites and Q_i the remaining
sites. Define U_i as the image of the flattening A:Q_i^* -> P_i. These are
actual algebraic contraction spaces, not images of Gram matrices. We have

    U_i <= U_(i-1) tensor V_i, dim U_i <= b_i.

Every stabilizer of A preserves U_i because its suffix action is invertible.
Two finite-field rank-factorization sweeps construct full-column-rank
embeddings E_i:U_i -> U_(i-1) tensor V_i without expanding the tensor.
The right-to-left sweep removes dead suffix directions; the left-to-right
sweep removes dependent prefix directions. Invertible changes of TT gauge
do not affect the resulting contraction spaces.

Starting with K_0=Gamma, suppose K_(i-1) already preserves U_(i-1). Let
R_(i-1)(g) be its induced prefix action and retain the original faithful
representation F(g)=diag(g_1,...,g_N). Use the augmented representation

    rho_i(g)=diag(F(g), R_(i-1)(g) tensor g_i).

Compute the setwise stabilizer of 0 direct-sum im E_i. This gives exactly
K_i, the subgroup of K_(i-1) preserving U_i. The faithful block prevents
loss of elements in the kernel of the compressed action. A left inverse
L_i E_i=I gives the next induced representation

    R_i(g)=L_i (R_(i-1)(g) tensor g_i) E_i.

For nonzero A, U_N is the line F_p A. A p-group's scalar image in F_p^*
is trivial since p and p-1 are coprime. Hence K_N=H, not merely a projective
stabilizer. For zero A, H=Gamma. This mathematical argument includes p=2;
the present Lie-based implementation deliberately accepts only odd primes.

## Imported Classical Algorithm And Cost

[Luks, Computing in Solvable Matrix Groups](https://ix.cs.uoregon.edu/~luks/solmatgrp.pdf),
Theorem 3.2(7), gives subspace stabilizers for generator-described solvable
matrix groups in time polynomial in dimension, log field size, and the
largest non-characteristic prime dividing group order. For a p-group over
F_p the last parameter imposes no growing-prime cost. This is reliance on
the published theorem, not a new implementation or reconstruction of its
omitted subroutines. Membership testing from the same theorem permits
pruning generator lists to O(D_0^2 log p), D_0=sum_i d_i, between stages.

There are N calls, each on dimension D_0+(dim U_(i-1))*d_i. No call uses
the full dimension product_i d_i. Exact rank computations and induced
actions are polynomial in the explicit core sizes. The current rank-sweep
code repeats RREF solves: a conservative uniform-bond schoolbook bound is
O(sum_i d_i chi^4) field operations, not the cubic bound obtainable by
batching those solves. Field arithmetic is charged in log p.

## Executable Guarded Specialization

`theorems/tensor_train_pgroup_stabilizer.py` uses existing exact matrix
logarithm, Lie closure, and exponential helpers. At EVERY actual augmented
stage, it computes the common associative algebra

    J_i=Alg_Fp(rho_i(g)-I : current generators g)

and requires J_i^nu=0 for nu<=p. This certifies the required unipotent
common-algebra regime. Checking only original site matrices, abstract group
class, or individual generator orders is insufficient after tensoring.

Under the guard, log/exp identifies the generated group with its Lie
algebra. If B embeds the prefix support and N spans its full left
annihilator, subspace preservation is exactly the linear condition

    N X_active B=0.

The kernel is a Lie subalgebra. Exponentiating a vector-space basis
generates its entire corresponding subgroup. The original faithful blocks
recover correlated sitewise generators. Every output is checked against
the augmented action and terminal scalar-one condition.

Unsupported stages return `generators=None` and `exact_subgroup_claim=False`.
An empty tuple of generators means a VERIFIED trivial subgroup; it is not
used for unsupported cases. No full tensor, ambient group, or orbit span
is materialized by the solver. Tiny test references may enumerate them.

The shared common-algebra backend previously evaluated g**p through a
machine-sized exponent interface. A 127-bit prime reproduced OverflowError.
It now uses the existing binary-power helper with O(log p) multiplications;
the regression exercises exact stabilizer recovery at p=2^127-1.

## Decisive Controls And Falsifiers

- For A=e_4 tensor ... tensor e_4 and independent UT4(F_p) factors,
  p>=5, the TT bond dimension is one, the orbit span is 4^N, and the
  exact stabilizer is UT3(F_p)^N in the upper-left blocks. This generally
  nonnormal subgroup is recovered without orbit enumeration. The live
  control uses p=5,N=3, even though the augmented dimension exceeds p;
  its common-algebra index is only four.
- Redundant bonds cannot be used as prefix supports: a dead suffix can
  introduce a spurious direction moved by a genuine tensor stabilizer.
  Tests include redundant, cancelling, and gauge-modified cores.
- Over F_5 the nonzero vector (1,2) has zero self-pairing. Gram-based
  support recovery is invalid; exact flattening ranks survive this control.
- Correlated site actions, noncommuting groups, compressed-action kernels,
  and nonnormal stabilizers are tested against complete tiny references.
- A p=3 common-index failure is retained as unsupported, never as a solved
  trivial subgroup. Corrupted output exponentials are detected.

## Review And Replay

Lorentz independently reviewed the general reduction and Luks scope.
McClintock independently reviewed the guarded proof and implementation,
tested additional tiny random cases, and caught the report's stale source
count. That test now asserts the complete source filename set. These are
automated adversarial reviews, not human peer review or formal verification.
Their distinction between the general theorem and narrower implementation
is essential. No concrete new classically hard Rees application survived
this pass.

    python -m theorems.tensor_train_pgroup_stabilizer --output research/classical_baselines/tensor_train_pgroup_stabilizer.json
    python -m pytest tests/test_tensor_train_pgroup_stabilizer.py tests/test_moore_common_algebra_stabilizer_backend.py tests/test_hpgp_coset_interface.py -q -W error

The JSON records live controls and hashes the solver, tests, and direct
helper dependencies. Next application proposals must evade the stated
sitewise/polynomial-bond assumptions for a concrete reason, or confront this
classical solver. Guard failure alone is not such a reason.
