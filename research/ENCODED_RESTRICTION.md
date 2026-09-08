# Encoded Subgroup Restriction

## What This Changes

Explicit multiplicity labels are stronger than carrier extraction. For a
**known** subgroup K_m=C2 wr S_m of G=S_(2m), there is a normalized two-QFT
reduction which extracts the K-type and carrier while retaining multiplicity
as an encoded subspace. It does not require a globally gapped separator,
a signed-tensor embedding, or postselection.

This is a standard representation-theoretic construction evaluated here as
a research access primitive, not a claim of a new quantum algorithm. The
module implements permutation factorization and finite matrix verification;
it does not implement scalable gate-level QFT circuits.

## Construction

Fix a G irrep lambda and a computable column j0 in its standard basis. Use
the Fourier convention

    F_G |g> = sum_(lambda,i,j) sqrt(d_lambda/|G|) rho_lambda(g)_(i,j)
                                       |lambda,i,j>.

Appending j0 and applying F_G^dagger is an isometry J_lambda from V_lambda
to C[G]. Its amplitudes are

    <g|J_lambda|i> = sqrt(d_lambda/|G|) conjugate(rho_lambda(g)_(i,j0)).

Schur orthogonality gives J_lambda^dagger J_lambda=I. It intertwines the
chosen representation with left multiplication on C[G]. Preparing these
small individual amplitudes is not an amplitude-amplification task: the
inverse QFT is a unitary applied to one normalized Fourier basis state.

Let P0 be the standard matching. The left K-coset Kg is determined by
Q=g^-1(P0). Order Q's pairs lexicographically and map the ordered endpoints
of pair i to (2i,2i+1), obtaining t(Q). Then

    g = k t(Q),  k = g t(Q)^-1 in K.

This is a bijection g <-> (k,Q). Both directions use polynomial-time
permutation arithmetic and sorting, with no enumeration of the matching
space. They can be implemented reversibly by compute/copy/uncompute.

Finally apply F_K to the k register. The resulting isometry is

    E_lambda = (F_K tensor I_Q) FACTOR J_lambda.

Its output has labels (mu,a,b,Q), where a is the K carrier row. By
intertwining and Schur's lemma,

    E_lambda restricted to mu = I_(V_mu) tensor W_(lambda,mu),

after any abstract restriction decomposition. Here W embeds the actual
copy space C^b(lambda,mu) into the registers (K-column b, matching Q).
Equivalently the image projector on that sector factors as

    E_mu E_mu^dagger = I_(V_mu) tensor P_code.

The finite controls verify this factorization, the rank of P_code, and all
K-generator intertwining identities, including a repeated S_8 copy block.
The S_8 check uses factored representation matrices and thin verification
bases, not a dense |G|-by-|G| image projector.

## Resources and Error

The reduction uses one inverse G-QFT, one K-QFT, register preparation and
reversible coset arithmetic. It has no postselection step and no source-mass
normalization loss. Registers use O(m log m) qubits, excluding additional
workspaces of the chosen QFT implementations. This is a statement about
register encodings, not an assertion that the classical verification scales.

For QFT approximations with operator errors epsilon_G and epsilon_K, the
isometry error is at most epsilon_G+epsilon_K by the triangle inequality.
There is no inverse rare-branch probability in this coherent, unconditioned
bound. Selecting or discarding particular mu outcomes would require a new
success and information analysis.

Relevant primitive sources are [Beals](https://doi.org/10.1145/258533.258548)
and [Generic Quantum Fourier Transforms](https://arxiv.org/abs/quant-ph/0304064).
The recent [Quantum Fourier Transform Toolbox](https://arxiv.org/abs/2608.28573)
provides wreath-product circuit constructions. Their existence does not
certify that the repository's finite matrix routines are efficient circuits.

## Logical Operations Without Copy Decoding

For a computable permutation x define the Hermitian orbit average

    A_x = (1/(2|K|)) sum_k rho(k) [rho(x)+rho(x)^dagger] rho(k)^dagger.

It has norm at most one and commutes with K. Uniform preparation of k and
one inverse-choice bit, controlled representation action, and unpreparation
give a normalization-one block encoding. Uniform K preparation can use
inverse K-QFT on its trivial Fourier label. Representation action can use
inverse G-QFT, reversible left multiplication, and G-QFT. These are conditional
circuit reductions, not gates compiled by this module.

Conjugation by the encoded restriction implements I_carrier tensor C_x on
the copy code without decoding W. The finite checks cover every
support-at-most-four Hermitian orbit representative. The repeated S8 block
has noncommuting C_x. All norms retain inherited normalization one, even
when C_x is small. No useful spectral gap, fast-forwarding, or efficient
polynomial approximating the desired measurement follows.

## Physical Convention and Reference Alignment

For real orthogonal Young representations and rho_h=(I+R_h)/|G|, the physical
group QFT has block

    (I_row tensor [I_column+rho_lambda(h)]) / |G|.

Thus the construction applies to the physical column; the row is maximally
mixed. An independent full S4 QFT check covers all three hidden matchings.
This resolves the convention in the stated basis, not hidden alignment.
Testing reference-odd parity (I-rho_lambda(h0))/2 and summing natural lambda
weights gives

    Pr[reference-odd | h] = (1-delta_(h,h0))/2.

Use the regular-character identity sum_lambda d_lambda chi_lambda(g)=
|G| delta_(g,e). The physical check finds zero odd mass only when aligned,
and one half otherwise. Never silently apply the aligned h-even source law
to an arbitrary fixed reference.

## Identification Bound and Escape Routes

Suppose the entire final POVM commutes with diagonal K conjugation on all
input copies. Covariance makes outcome likelihoods constant on K-orbits of
hidden matchings. These are classified by the half-lengths of alternating
components in their union with the reference matching, a partition of m.
See the standard double-coset classification in
[Diaconis and Simper](https://arxiv.org/abs/2102.04576).

An orbit of type nu has size 2^(m-length(nu))*m!/z_nu. Exhaustive controls
at m=2,3,4 check this formula and the actual subgroup orbits. There are p(m)
orbits and M=(2m-1)!! hypotheses. For the uniform prior, identical likelihoods
within each orbit permit at most 1/M average correct-identification
contribution per orbit, hence

    Pr[identify h] <= p(m)/M.

This is independent of jointly measured copy count. It does NOT rule out
binary class detection, whose hypotheses are already conjugacy invariant,
carrier-sensitive effects, different reference frames, or priors supplying
orientation information. Carrier extraction does not force the final POVM
to be invariant. The optional r-round bound p(m)^r/M is only for a classical
adaptive oracle returning one partition-valued orbit label per query, not
a quantum multi-reference protocol with retained memory.

## What Is Still Missing

- **Unknown subgroup alignment.** The algorithm knows the reference K used
  by FACTOR. It does not know the centralizer of an unknown hidden involution.
  The earlier h-even source law is stated in an aligned analysis frame;
  that frame is not free algorithmic access. A covariant or candidate-controlled
  use must charge alignment and aggregation separately.
- **Explicit copy index.** (b,Q) is an encoded subspace, not a compact
  canonical label j in [branching multiplicity]. The map W is not given as
  a decoded table of basis vectors at growing rank.
- **Target effect.** Carrier extraction does not implement the multi-copy
  hidden-involution support measurement or PGM. It supplies no decoder.
- **Logical normalization.** Known K-invariant orbit averages act on the
  implicit copy code, but the actual target effect must still be synthesized
  with a controlled normalization and approximation cost.
- **Circuit realization.** The physical column convention and reduction are
  specified, but scalable QFT gate implementations are external primitives.

## Next Experiment

Logical orbit-average action and the physical column convention now pass
finite checks. Formulate a binary effect or symmetry-breaking identification
protocol with charged normalization and information. Do not use the
dimension of the implicit code as an automatic circuit lower bound, and do
not promote efficient carrier access to a solution of the remaining measurement.

## Attempted Refutations

- Tiny inverse-QFT amplitudes do not imply postselection: check the full norm.
- Multiplicity-free examples could conceal failure: S8 has a repeated copy
  code with noncommuting logical actions.
- A column convention could be unphysical: independently transform complete
  coset density matrices.
- An identification obstruction could falsely kill decision: the proof
  needs separate hidden labels and does not cover the binary mixture.
- Orbit averages could look useful after rescaling: keep normalization one.
- Numerical tests are not proofs: general derivations remain review-pending,
  and decoder/speedup gates remain false.
