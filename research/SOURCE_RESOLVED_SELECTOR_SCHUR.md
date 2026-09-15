# Source-Resolved Selector Spin Blocks and Their Cost

Status: standard representation-theoretic reduction specialized to this
channel; derived, review pending. No novelty, general efficient measurement,
classical dequantization, intermediate-band obstruction or speedup is claimed.

The question was whether the [radial-mask reduction](SELECTOR_MASK_SYMMETRY.md)
also makes the surviving occupation band's output matrices small. The answer
is conditional: yes at a fixed number of source categories, but not from
symmetry alone with the full growing-degree irrep record. This changes the
next experiment: do not invest in a large fixed-degree mask optimizer as a
surrogate for the hard growing-degree measurement problem.

## Scope and Exact Block Formula

Keep the fixed common group-algebra query, standard mixed coset inputs,
one shared uniform hidden involution, irrep-coarsened classical sources,
physical discard, and a fixed radial pure mask. This is the same architecture
as the [occupation-band note](OCCUPATION_BAND_LOCALIZATION.md). Let

    U = sum_g a_g R(g),
    p_eta,j(g) = Tr(P_j R(g) rho_eta),
    alpha(S) = sqrt(w_|S| / binomial(K,|S|)).

For a fixed source tuple J, the unmasked Schur coefficients are

    C_eta,J = sum_(g',g) conj(a_g') a_g tensor_i B_eta,ji(g',g),
    B_eta,j = [[p_eta,j(e),       p_eta,j(g'^-1)],
               [p_eta,j(g),       p_eta,j(g'^-1 g)]].                 (1)

Rows and columns of B are selector bits. The group-pair row is g' and
column g. These B matrices need not be positive, normal or invertible.
Positivity is required of the complete physical channel, not of its signed
coefficient terms. Average the SAME h only after constructing each product.

Sort the source tuple into categories with counts c_1,...,c_r. Its stabilizer
is the product S_(c_1) x ... x S_(c_r). The radial mask commutes with this
stabilizer, including its off-diagonal coherences between Hamming weights.
On c selector qubits, the standard tensor-power decomposition is

    B^tensor(c) ~= direct-sum_(ell=0)^floor(c/2)
        [det(B)^ell Sym^(c-2ell)(B)] tensor I_(f_c,ell),
    f_c,ell = binomial(c,ell)-binomial(c,ell-1).                      (2)

Use binomial(c,-1)=0. Polynomial continuation extends the identity from
invertible matrices to singular ones. In the normalized Dicke basis, a
one-sector weight index u=0,...,c-2ell corresponds to physical weight ell+u.
Explicitly, for B=[[a,b],[c,d]] and m=c_count-2ell,

    Sym^m(B)[u,v] = sqrt(binomial(m,v)/binomial(m,u))
        sum_z binomial(v,z) binomial(m-v,u-z)
            a^(m-u-v+z) b^(v-z) c^(u-z) d^z.                       (3)

The z range is max(0,u+v-m)..min(u,v). This formula uses a normalized basis;
a nonunitary monomial-basis similarity would not preserve the trace norm.

For each count vector c and defect vector ell, replace every factor in (1)
by (2). Multiply on both sides by the diagonal mask entries at total weight
sum_j(ell_j+u_j). The resulting matrices X_eta,c,ell retain all weight
coherence. Their dimensions and multiplicities are

    d_c,ell = product_j(c_j-2ell_j+1),
    f_c,ell = product_j f_(c_j,ell_j),
    o_c = K! / product_j c_j!.

The exact class-decision distance is therefore

    T = (1/2) sum_c o_c sum_ell f_c,ell
        || E_h X_h,c,ell - X_0,c,ell ||_1.                          (4)

No rare source has been normalized or discarded. Sorting sources is justified
by simultaneous source/selector covariance and radial amplitudes. It is not
justified for an arbitrary position-asymmetric mask. The spin multiplicity
and source-orbit multiplicity are distinct and BOTH must be included.

This application is to selector QUBITS. It does not assert that a qubit
Schur transform solves internal tensor products of S_n Specht carriers.

## Actual Cost

For a fixed histogram c, the number of spin matrix entries per hypothesis is

    sum_ell d_c,ell^2 = product_j binomial(c_j+3,3).                  (5)

The identity follows by summing (c-2ell+1)^2. Summing (5) over all count
vectors gives, by the generating function (1-z)^(-4r),

    total entries = binomial(K+4r-1,4r-1).                          (6)

Thus this is polynomial in K at FIXED r, not uniformly polynomial in both
K and r. Largest blocks have dimension product_j(c_j+1). Even (6) excludes
the group-pair contraction: this implementation sums |G|^2 coefficient terms
for every hidden member. For G=S_n that enumeration remains factorial, and
high-degree polynomial evaluation also needs a numerical precision analysis.
No end-to-end efficient evaluation or measurement compiler follows.

For K=64, one source category has largest block dimension 65. Sixty-four
distinct sources have trivial stabilizer and a single block of dimension
2^64. This is the dimension left by THIS symmetry reduction, not a lower
bound on general circuit complexity or proof of full rank for every query.

## Distinct Labels Are the Asymptotic Full-Source Case

Use the existing Plancherel and elementary-symmetric routines; do not create
a second source-distribution model. Under the null and alternative,

    p_lambda = d_lambda^2/n!,
    q_lambda = d_lambda(d_lambda+chi_lambda(h))/n!,
    0 <= q_lambda <= 2p_lambda.

The q law is independent of WHICH conjugate h is shared. Hence source labels
are iid under either hypothesis despite the shared hidden element. In this
architecture source projectors commute with the query, so selector-mask
choice does not alter these source probabilities.

For either law v, the exact all-distinct probability on K source draws is
K! e_K(v). Its complement is at most binomial(K,2) sum_lambda v_lambda^2.
In particular, the q collision sum is at most four times the p collision
sum, and also at most 2 max_lambda p_lambda. Existing maximal-dimension
bounds give max p_lambda=exp(-Theta(sqrt(n))). Thus, at any polynomial K,
both collision probabilities tend to zero faster than any inverse polynomial.

Consequently the full irrep source record has a trivial copy stabilizer with
asymptotically full natural probability. The source-resolved spin reduction
then leaves a 2^K block. Global permutation covariance still relates DIFFERENT
ordered source blocks; it does not create a nontrivial stabilizer inside one
all-distinct block. This parallels the already recorded source-block covariance
boundary, without reusing its different wreath-carrier input model.

This does NOT say the finite controls are already asymptotic. For example,
if K exceeds the number of partitions, all-distinct sampling is impossible.
No explicit large-degree crossover is obtained from unspecified asymptotic
constants. Do not extrapolate the small-degree rows into such a certificate.

Erasing source labels does increase symmetry, but it is a lossy channel.
The physical controls give strict losses of decision distance. Therefore a
small-r experiment must measure the retained information and charge the loss;
it cannot stand in for the full-source optimum without another argument.

## Verification and Falsifiers

`theorems/coset_selector_schur.py` implements (2)-(6), the independent physical
spectrum comparison and the exact rational source-law checks. Tests use
normalized Dicke/singlet embeddings to compare the full tensor action against
each spin block, including singular and nonnormal matrices. Multiplicities
must recover 2^c, not c+1, dimensions.

Regular-basis S3 K2,3 and S4 K2 controls compare EVERY source histogram and
hidden member's full spectrum after restoring multiplicities. These are
floating-point checks of an exact identity, not interval-certified spectra.
They also retain counterexamples to top-spin-only projection, unit
multiplicities, weight pinching, source erasure and averaging individual
distances instead of states. S3 K4,6 controls exercise the representation
without constructing D^K physical matrices. Their signals are finite
calibrations, not algorithm candidates or growing-degree speedup evidence.

The primary falsifiers for a proposed use of this subsystem are: a missing
source or spin multiplicity; a mask-dependent change to the source law;
an uncharged source erasure; a group-pair enumeration described as polynomial
in n; or a claim that the lack of symmetry proves a circuit lower bound.

## Literature and Next Action

The underlying spin decomposition and multiplicities are standard; see
[Moroder et al., section 5.1](https://arxiv.org/html/1205.4941#S5.SS1).
[Bacon, Chuang and Harrow](https://arxiv.org/abs/quant-ph/0407082) provide
efficient Schur transforms within their specified tensor-power setting, not
the state-dependent final measurement needed here. The existing maximal-source
atom bound is supported by the classical Vershik-Kerov result, recorded in
[Moore, Russell and Schulman, Theorem 5](https://arxiv.org/html/quant-ph/0501056),
and refined by [Aggarwal and Elboim, Theorem 1](https://arxiv.org/html/2605.25995).
The refinement is not needed for the collision conclusion.

The symmetry-only polynomial-readout hypothesis fails its cost audit.
The intermediate band itself remains OPEN. Continue only with extra structure
in the large surviving blocks, or a quantitatively justified small-category
measurement. Compare that with a concrete retained-physical primitive; do
not spend the next pass optimizing more fixed-S3 masks.
