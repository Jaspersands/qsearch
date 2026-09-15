# An All-Mask Bound for Low Coefficient-Mass Queries

Status: derived, review pending. No independent proof, formal certificate,
established novelty, classical sampler or quantum speedup is supplied.

This bounds ALL fixed selector states, including the unresolved intermediate
occupation band, but restricts the common query's group-algebra coefficient
mass. It complements rather than replaces the arbitrary-query occupation
bounds. The [source-stabilizer audit](SOURCE_RESOLVED_SELECTOR_SCHUR.md) did
not yield small matrices in general; this argument instead controls the
entire channel before optimizing the selector or its final measurement.

## Claim and Architecture

Let G=S_n, with even n>=8, D=n!, C the fixed-point-free involution class,
M=|C|=(n-1)!!, and r_G=p(n) the number of conjugacy classes of G. Keep
standard coset inputs rho_0=I/D and rho_h=(I+R(h))/D with ONE uniform h in
C shared across K copies. Use one fixed common group-algebra unitary

    U = sum_g a_g R(g),     A = sum_g |a_g|.

Retain the classical record of a fixed irrep-coarsening partition and the
selector, and discard the physical group registers. The selector state is
fixed before inputs and source records; it may be arbitrary, mixed, and
entangled with an independent reference. No hidden-correlated preprocessing
is available. The final joint measurement is unrestricted.

For these channels Phi_eta, the derived norm bound is

    E_h ||Phi_h-Phi_0||_diamond <= 4 K A^2 sqrt(r_G/M).               (1)

Consequently, for every allowed input selector/reference state,

    E_h T(Omega_h,Omega_0) <= min(1, 2 K A^2 sqrt(r_G/M)),
    T(E_h Omega_h,Omega_0) <= E_h T(Omega_h,Omega_0).                 (2)

The class-decision distance and average individual distance are different
quantities. Equation (2) bounds BOTH, in that order of implication. The
existing raw-copy cap must NOT be applied to the average individual distance.
r_G is the number of group conjugacy classes, not the retained source count.

## Cross Channels Have Completely Bounded Trace Norm at Most One

For fixed g,g', define the single-selector-bit cross channel Psi_eta^(g,g')
by using controlled R(g) on its ket side and controlled R(g') on its bra
side, recording source j and tracing the physical register. Its Schur kernel is

    B_eta,j(g',g) = [[p_eta,j(e),   p_eta,j(g'^-1)],
                     [p_eta,j(g),   p_eta,j(g'^-1 g)]],
    p_eta,j(x) = Tr(P_j R(x) rho_eta).

The cross channel need not be positive when g!=g'. Nevertheless it has
the factorization Tr_E[V_eta,g X V_eta,g'^dagger] through two isometries.
To see this, purify rho_eta, copy the source label into both its output and
an environment register, and apply controlled R(g). The source projectors
are complete and the state has trace one, so V_eta,g^dagger V_eta,g=I.
The environment copy makes the retained source record classical.

For every reference extension and every operator X, left/right multiplication
by isometries and the completely bounded trace norm of partial trace give

    ||Psi_eta^(g,g')||_diamond <=1.                                 (3)

Equivalently the adjoint has the form V_eta,g'^dagger(Y tensor I)V_eta,g,
which has completely bounded operator norm at most one. This is a norm bound
on a cross map, not a claim that each signed coefficient term is a channel.
No source block is individually renormalized or postselected.

## Average the Shifted Character Squares

The difference of local coefficients is p_j(hx), where
p_j(x)=Tr(P_j R(x))/D and x is one of e,g,g'^-1,g'^-1 g. Source-weighted
character orthogonality, already used in the vacuum note, gives

    sum_j |p_j(x)|^2/q0_j <=1/|class(x)|,   q0_j=p_j(e),
    sum_j |p_j(x)| <=1/sqrt(|class(x)|).                            (4)

This includes x=e. For any FIXED x, h->hx is injective and hence

    E_(h in C) 1/|class(hx)|
       <= (1/M) sum_(y in G) 1/|class(y)| = r_G/M.                  (5)

Each conjugacy class contributes one to the full group sum. Jensen and (4)
give E_h sum_j |p_j(hx)| <=sqrt(r_G/M), uniformly in fixed x.

The difference cross map is a sum of four selector matrix-entry maps with
these coefficients. Each matrix-entry map X->|s><s|X|t><t| has completely
bounded trace norm <=1; a direct sum over classical j sums trace norms.
Therefore

    E_h ||Psi_h^(g,g')-Psi_0^(g,g')||_diamond
       <=4 sqrt(r_G/M).                                          (6)

This does not replace the shared h by independent hidden elements. It only
bounds a single local difference averaged over the same prior.

## Tensor Hybrid and Coefficient Charge

For one fixed h and one fixed pair (g,g'), tensor telescoping and (3) yield

    ||(Psi_h)^tensor(K)-(Psi_0)^tensor(K)||_diamond
       <=K ||Psi_h-Psi_0||_diamond.                               (7)

The other factors in each hybrid term have norm at most one, even though
they are cross maps. Now the complete fixed-common-query channel is

    Phi_eta = sum_(g,g') a_g conj(a_g') (Psi_eta^(g,g'))^tensor(K).

Take the coefficient triangle bound, THEN average h and apply (6)-(7).
The coefficient sum is A^2, proving (1). Every reference and selector input
is covered by the norm argument; no Hamming-weight truncation, radialization,
selector-rank charge or final-POVM restriction was used.

Both uses of fixedness matter: the coefficients cannot depend on h or source
records, and the input selector cannot have been prepared conditionally on
source records. Such adaptations do not inherit this tensor cross-map proof.

## Which Queries Are Excluded?

Unitarity in the regular group algebra gives sum_g |a_g|^2=1. Thus a query
with at most S nonzero canonical coefficients has A^2<=S. At polynomial K
and polynomial S, (2) is superpolynomially small, independently of the mask.

The coefficient l1 norm is submultiplicative under group-algebra products.
For a nonidentity involution v,

    exp(i theta R(v)) = cos(theta) I + i sin(theta) R(v),
    coefficient l1 norm <=sqrt(2).

A product of q such factors therefore has A^2<=2^q. Since
log2 M=(n/2)log2 n-O(n), and log2 p(n)=O(sqrt(n)), polynomial K and
q<=(1/4-epsilon)n log2 n for any fixed epsilon>0 imply negligible distance.
This is a restriction on this TYPED query word, not on an arbitrary circuit
with q gates. Duplicate group words can reduce the actual coefficient mass.

Large coefficient mass does not imply difficult implementation. Dense
spectral queries or longer typed words might be efficiently compiled and
remain outside a useful version of this bound. Nontrivial information
requires enough coefficient mass to evade (2), but that is not sufficient.

### Dense Low-Dimensional Irrep Reflections Also Fail

For a fixed target irrep lambda, U=I-2P_lambda has canonical coefficients
a_g=delta_(g,e)-2 d_lambda chi_lambda(g)^*/D. Row orthogonality and Cauchy
give sum_g |chi_lambda(g)|<=D, so A<=1+2d_lambda. Consequently every single
polynomial-dimensional target reflection is also obstructed for all masks.
More generally, a central phase change on a target list has
A<=1+sum_lambda |exp(i theta_lambda)-1|d_lambda; a polynomial total target
dimension is insufficient to evade (2).

For the sign irrep, the EXACT mass is A=3-4/D<3, even though all canonical
coefficients are nonzero for D>2. Thus sparsity alone would miss this
obstruction. In the fixed-point-free S_n case the sign is a missing harmonic
only when n/2 is odd; no missing-harmonic claim is made when n is divisible
by four. Coefficient bounds still apply independently of that distinction.

At n1024 and K=n^2, A^2<=9 gives E_h T<=2^-2113. This rules out discarding
the physical registers after this fixed common query, not the retained-data
span measurement. The latter is the separate construction described by
[Moore and Russell](https://arxiv.org/html/quant-ph/0504067): efficient access
to individual subset projectors does not supply their collective span
measurement. Finding such a compiler remains unresolved.

## Integer Envelopes and Falsification

`source_selector_coefficient_mass_contract` takes an explicit exact-rational
upper bound on A^2. It uses SymPy's partition count and outward integer
rounding of 4 K^2 A^4 p(n)/M. The supplied coefficient certificate is an
assumption, not independently inferred from an arbitrary program.

At K=n^2, the rounded upper bounds on E_h T are:

| n | support <=n^2 | n involutory rotations | (n log2 n)/8 rotations | generic A^2<=n! |
|---|---|---|---|---|
| 128 | 2^-133 | 2^-19 | 2^-35 | 1 |
| 512 | 2^-894 | 2^-400 | 2^-336 | 1 |
| 1024 | 2^-2097 | 2^-1093 | 2^-837 | 1 |

These are conditional bound evaluations, not large-degree quantum simulations.
The finite controls reconstruct all S3/S4 single-bit cross maps from actual
purifications and projectors, test reference-ancilla contractions on arbitrary
complex operators, and check K2/K3 products against the full physical channel.
Exact S3/S4/S6 character sums verify (5) for every group shift. Gaussian-integer
word coefficients verify normalization and support accounting independently of
the physical products. Nineteen exact S3/S4/S6 target-irrep controls verify
every central Fourier eigenvalue, Parseval normalization and the reflection
mass bound, including a sign target that is NOT a missing harmonic for S4.
Numerical probes corroborate identities; they do not
replace the completely bounded norm proof or independent review.

Falsify any proposed extension that drops A^2, renormalizes rare sources,
averages h before tensoring, gives the selector hidden-correlated information,
calls a cross map positive, or translates coefficient mass into a generic
gate lower bound. Dense-query vacuity must remain visible. This is NOT a
classical sampling algorithm and does not obstruct retained physical data.

The norm tools are standard; see [Watrous, chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf).
Character orthogonality and group-class counting are also standard. Novelty
of their specialization to this architecture has not been established.
The next constructive target must evade this coefficient charge as well as
the earlier mask bounds, or change physical access in a fully specified way.
