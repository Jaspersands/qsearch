# Full Pilot Sampling Through A Supplied Free-Fermion Root

Date: 2026-10-24. LOCAL, UNREVIEWED derivation and executable reference.
This is a classical baseline and a conditional coherent-preparation reduction,
NOT a new quantum advantage, independently reviewed theorem, or novelty claim.

## 1. Why This Pass

The degree-scale HDQI preparation gap is still unresolved. Mixed-spin
hypercontractivity does apply to the unweighted word-number semigroup:
[Junge et al., Section 2.1](https://arxiv.org/abs/1211.4759) records Biane's
estimate. It does not by itself give a thermal Poincare inequality or a
degree-dependent perturbation bound. No such upgrade was established here.

Instead this pass supplies a FULL-output classical sampler for a structured
input family, not another additive observable estimator. Forest roots have
polynomial cost at ALL finite temperatures. General roots have cost
exp(O(r))*poly(input size, precision), where r is their cycle rank. Thus
logarithmic-cycle-rank examples cannot support a full-pilot sampling advantage.
This includes arbitrary efficient classical postprocessing of the sampled
word, including nonlinear functions. It does not simulate an arbitrary
coherent decoder or noncomputational-basis measurement.

Free-fermion line-graph recognition and the need to retain cycle symmetries
are prior art: [Chapman--Flammia](https://arxiv.org/html/2003.05465v2).
The sequential nonsymmetric DPP sampler is also prior art:
[Poulson](https://arxiv.org/html/1905.00165v2). The contribution to this
project is their explicit composition for the INDEPENDENT canonical HDQI
word distribution, including the cycle-sector interference and its costs.

## 2. Native Input, Not An Oracle

Supply a simple undirected root graph R=(V,E), an ordering of its m edges,
real rational couplings |J_e|<=1, and finite rational beta>=0. Let v=|V|,
c be the number of connected components, and r=m-v+c. Isolated root
vertices are allowed. The actual HDQI anticommutation graph is G=L(R):
two generators anticommute exactly when their root edges share a vertex.

The native generators and task are UNCHANGED:

    O_e = X_e product_{f<e, f~e in G} Z_f,
    H = sum_e J_e O_e, S=exp(-beta H/2),
    |pi> = S|0>/sqrt(tau(S^2)), mu(y)=|<y|pi>|^2.

Their ordered words P(y) are trace-orthonormal and P(y)|0>=|y>.
The m independent X labels must not be quotient-identified with cycles.
No thermal state, amplitude table, fermionic sector, or eigenbasis is supplied.

For an already supplied G, an adapter must verify a root certificate and
the generator ordering; merely finding a similar graph is insufficient.
Root recognition is polynomial by the cited prior art but is NOT implemented
here. The triangle/star root ambiguity can change r: prefer a forest root
when one exists. The executable constructs G from its explicit root.

## 3. Faithful Trace Requires All Flux Sectors

Fix a spanning forest T; its r complementary edges are ordered chords.
Write B for the F_2 incidence map and a(y) for the chord bits of an edge
word. The map

    y -> (x=By, a=a(y))

is a bijection from F_2^m to pairs consisting of a vertex subset x with
EVEN parity in EACH root component and an arbitrary a in F_2^r. Given a,
subtract chord boundaries, then eliminate tree leaves. This costs O(v+m).

Take anticommuting Hermitian Majoranas gamma_i with gamma_i^2=1. Use an
extra unused Majorana if necessary, and the FULL normalized trace, not a
fixed-parity-sector trace. For z in F_2^r define a *-representation

    phi_z(O_e) = i gamma_u gamma_v                 (tree edge),
    phi_z(O_e) = (-1)^z_j i gamma_u gamma_v        (chord j),

with u<v. These have the correct squares and pairwise commutation signs.
Literal Clifford multiplication computes a known phase kappa(y) in
{1,-1,i,-i} such that

    phi_z(P(y)) = (-1)^(z.a(y)) kappa(y) gamma_(By).       (1)

If By is nonempty its Majorana trace vanishes. If By=0 and y!=0 then
a(y)!=0, so averaging the character over z vanishes. Consequently

    tau(T) = 2^-r sum_z tau_M(phi_z(T)),
    ||T||_2^2 = 2^-r sum_z ||phi_z(T)||_2^2.              (2)

This is a faithful Hilbert-space isometry of the whole abstract word
algebra. A single sector is not. For a four-cycle, the nonempty full-cycle
word maps to -I in the zero-flux sector although its native trace is zero.
The source must not silently become a symmetry-projected problem.

## 4. Explicit Gaussian Coefficients

Let A_z be real skew-symmetric, with upper edge entries J_e times the
chord sign. Then H_z=(i/2) gamma^T A_z gamma. Set

    K_z = -i tanh(beta i A_z/2) = tan(beta A_z/2),
    C_z = product_j cosh(beta epsilon_(z,j)/2),
    Z_z = product_j cosh(beta epsilon_(z,j)),

where +/-epsilon_(z,j) are the nonzero paired eigenvalues of iA_z;
zero modes contribute one. K_z is real skew with operator norm <=1.
An orthogonal two-by-two block diagonalization, followed by the exterior
power transformation rule, gives the coefficient of gamma_x in S_z:

    g_z(x) = C_z (-i)^(|x|/2) Pf((K_z)_x),                (3)
    sum_x |g_z(x)|^2 = C_z^2 det(I+K_z) = Z_z.            (4)

Odd component subsets have zero Pfaffian because K_z is component-block
diagonal. Empty Pfaffians/determinants are one. This is a coefficient
identity for S_z, not a claim that its eigenvectors are native word labels.

Writing S=sum_y c_y P(y), Fourier inversion of (1) gives

    c_y kappa(y) = 2^-r sum_z (-1)^(z.a(y)) g_z(By),
    Z_native = 2^-r sum_z Z_z.                           (5)

The common phase (-i)^(|By|/2) cancels from probabilities. It DOES matter
for coherent reconstruction. The tests retain it and kappa(y), rather
than testing only absolute values.

## 5. An Actual Full-Output Classical Sampler

Put L=2^r, W=sum_z Z_z. A proposal is:

1. Draw z with probability Z_z/W.
2. Draw x from det((K_z)_x)/det(I+K_z).
3. Draw a uniformly from F_2^r and decode y from (x,a).

Step 2 is a valid nonsymmetric L-ensemble: every principal minor of a
real skew matrix is either zero or a squared real Pfaffian. Its marginal
kernel is M=I-(I+K_z)^-1, generally NOT symmetric. At a sequential step
include i with probability p=M_ii. The remaining kernel is

    M_rest - M_rest,i M_i,rest / p             if included,
    M_rest + M_rest,i M_i,rest / (1-p)         if excluded. (6)

Never condition on a zero-probability branch or symmetrize M. Equation
(6) follows by a Schur complement of the DPP generating determinant.
It samples without enumerating vertex subsets, using O(v^3) arithmetic.

Let b_z=C_z Pf((K_z)_x); a common positive scale may be removed. Then

    q(y) = sum_z b_z^2 / (L W),
    mu(y) = |sum_z (-1)^(z.a) b_z|^2 / (L W).

Cauchy--Schwarz proves mu(y)<=L q(y). Accept the proposal with probability

    |sum_z (-1)^(z.a) b_z|^2 / [L sum_z b_z^2].            (7)

Its unconditional acceptance probability is EXACTLY 1/L. The accepted
word has law mu. Expected work is O(L^2 poly(v,m,precision)); this is
exponential in r, not a polynomial general-line-graph claim. A cap T
has failure probability (1-1/L)^T<=exp(-T/L); a failed cap returns no
sample. For r=0 every proposal is accepted and the algorithm is polynomial.

Replacing (7) by automatic acceptance is WRONG. The two-cycle finite
control at beta=1.2 has total-variation distance >0.7 between q and mu.
Drawing a flux sector classically loses precisely the interference needed
for the canonical independent-word problem.

## 6. Finite Precision Is A Separate Obligation

The executable obtains K_z and log C_z using floating-point Hermitian
diagonalization, then rationalizes K_z while preserving exact skew symmetry
and component blocks. It rationalizes alpha_z=C_z/max_w C_w in [0,1].
The DPP matrices, determinants, Pfaffians, sector weights, Bernoulli coins
and rejection ratios are then EXACT RATIONAL arithmetic for this surrogate.
It never clips an invalid probability to hide an error.

THIS DOES NOT CERTIFY THE FLOAT FRONT END. `native_error_certified` is
always false. Tiny dense discrepancies are finite controls, not an interval
certificate or a global rigorous bound on those computed matrix functions.

A precision route exists without rare-event conditioning assumptions.
Let B(K) be the unnormalized fermionic pairing vector with coefficients
(-i)^(|x|/2) Pf(K_x). For certified entry errors delta_K, scale errors
delta_alpha, and v delta_K<=1, interpolate between exact and approximate
skew matrices that retain the SAME component blocks. Their norms are <=2,
so ||B(K_t)||<=5^(v/4)<=2^v. Since

    dB(K_t)/dt = -i sum_(i<j) (Delta K)_ij c_i^dagger c_j^dagger B(K_t),

the difference of the direct-sum sector vectors is at most
sqrt(L) 2^v [delta_alpha + v(v-1)delta_K/2]. The exact direct-sum norm
is >=1 because one alpha_z is one and every sector has vacuum coefficient
one. Normalization multiplies the vector-error bound by at most two.
Walsh and coordinate/phase transformations are unitary, and measurement
cannot increase trace distance. A conservative bound implemented here is

    TV <= min(1, 2^(v+r+1)
                   [delta_alpha + v(v-1)delta_K/2]).       (8)

Thus O(v+r+log(v/epsilon)) certified precision bits suffice. The required
matrix-function/eigenvalue precision also charges log(1+beta), input bit
size and arithmetic costs. Standard certified matrix-function arithmetic
could supply these bounds; it is NOT part of the present float front end.
For rational surrogates all determinant ratios have polynomial bit length
by minor bounds, even when some conditional probabilities are tiny.
Expected exact random-bit sampling cost is polynomial; there is no free
real-valued probability oracle.

## 7. Constructive Coherent Reduction And Its Exact Blocker

There is also a useful coherent mechanism, not implemented as a circuit.
Suppose a clean preparation of the POSITIVE-amplitude flux state is paid:

    |flux> = sum_z sqrt(Z_z/W) |z>.

Conditioned on z, prepare the normalized Gaussian pairing state g_z/sqrt(Z_z).
It has v fermion modes and bounded pairing matrix -iK_z. Standard Gaussian
state compilation is polynomial; fermionic Gaussian operations and their
classical simulation are prior art, for example
[Bravyi](https://arxiv.org/abs/quant-ph/0404180). The matrix functions and controlled
arithmetic must be charged. Degenerate single-particle eigenspaces are not
an oracle promise; a covariance/QR compiler can avoid choosing a discontinuous
eigenbasis. Apply Hadamards to the r flux bits, convert (x,a) reversibly to y
plus the fixed component-parity ancillas, and multiply by kappa(y)^-1.
Equations (3)-(5) give EXACTLY the canonical pilot. Work registers must
be uncomputed; random phases in the flux source would invalidate the result.

For forests no flux source is needed. For r=O(log m), enumeration compiles
it but the classical algorithm already samples the complete output. For
large r, evaluating every individual Z_z in polynomial time DOES NOT imply
efficient coherent amplitude loading. A classical flux sampler is likewise
not a coherent source. The remaining constructive question for this family
is therefore a specific positive-weight flux-amplitude problem, not a free
Gibbs-oracle assumption. No polynomial solution for extensive r is claimed.

## 8. Adversarial Checks And Research Decision

- Native-input check: use explicit graph/couplings, no unknown phase states.
- Trace check: average all fluxes and retain each component's parity.
- Coherence check: signed full amplitudes match the native dense control;
  the incoherent shortcut fails by a large, recorded TV distance.
- Access check: determinants/eigensystems are computed on v by v matrices,
  not supplied; both 2^r sector enumeration and 2^r rejection are charged.
- Precision check: exact surrogate is not relabeled exact native sampling.
- Novelty check: free fermions, flux sectors and DPP sampling are existing
  techniques. This composition has no independent review or novelty claim.
- Reach check: arbitrary non-line graphs, extensive-cycle-rank sampling,
  arbitrary coherent decoders and the degree-scale parent gap remain open.

This removes full-output sampling as an advantage target on forest and
logarithmic-cycle-rank roots, at every finite beta. These are scalable,
connected nonproduct families. For example take a chain of h hubs with b
private leaves per hub. Its root has v=h(b+1), m=hb+h-1, r=0; the line graph
has d<=2b+2. At beta^2=1/[64(d+1)], beta^2 m grows as h/128, so it can be
superlogarithmic. The result is not merely the old total-mass certificate.

Next decisive task: find a structured extensive-cycle-rank root for which
clean flux-amplitude preparation is provably polynomial, then attack its
full word output with stronger classical algorithms. Alternatively prove
efficient classical sampling for more roots. Do not promote another forest
or low-cycle-rank numerical example, and do not assume a uniform flux source
approximates the weighted one without a norm/error bound.
