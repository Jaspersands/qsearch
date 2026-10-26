# UT5 Matrix-Phase Alignment

2026-10-21. Status: proposed reduction with an implemented exact public
linear-algebra controller, symbolic phase compiler and finite source controls. NOT an
admitted algorithm, novelty certificate, general nilpotent HSP solver, or
external application. No hidden advice is supplied to the controller.

Subsequent boundary work: `CLASS_FOUR_VARIABLE_RADICAL_SOURCE.md` proposes
a general replacement for the invertible-Weyl-map assumption, including
label-dependent radicals and a conditional arbitrary-H completion. It is
not an independently certified theorem and does not broaden this specific
UT5 compiler's input schema.

## 1. Question And Scope

Can the common-potential approach cross its abelian-derived-subgroup boundary?
Consider the standard matrix group

    G = UT_5(F_p)^r, p>4, m=4r, N=G', H intersect N=1.

Both r and log p may grow. The input is an ordinary deterministic hiding
oracle separating the left cosets gH, with coherent access charged, and
explicit matrix coordinates. It is NOT a supplied table, state-preparation
oracle, known hidden direction, or classically evaluable potential. Restrict
the present proposed large-characteristic route to p>=2r. This restriction
is essential to the label-acceptance bound below. No claim for the excluded
regime or nontransverse H is made.

Here N is a product of r Heisenberg groups and a 3r-dimensional central
vector group. In one factor its coordinates are

    a=n13, b=n35, z=n15; d=(n14,n24,n25),
    (a,b,z,d)(a',b',z',d')=(a+a',b+b',z+z'+ab',d+d').

Thus N is nonabelian. Its center has dimension 4r and W=N/Z(N) has
dimension 2r. The earlier scalar-normal-register proof does not apply.
The implemented controller tests a replacement, not a relabeling of that proof.

## 2. Actual Matrix-Valued Source

H is abelian: its commutators lie in both H and G'. Let U be its image in
V=G/G'=F_p^m. For the proof ONLY choose a projection pi:V->U and the unique
hidden lift h(u)=exp(u+a(u)), with a linear. For q, put u=pi(q), r0=q-u and

    F(q)=exp(r0) h(u) exp(-q) in N.

Then, for v in U, a group-word identity gives

    exp(q) h(v) = F(q)^(-1) F(q+v) exp(q+v).                 (1)

Neither pi, a nor F is evaluated by the public controller. In class four,
Q(q)=log F(q) has total degree at most four. More importantly, its projection
Q_W to W has degree at most TWO: every Lie word of length at least three
lies in gamma_3(G), and [gamma_3(G),gamma_2(G)]=1. Linear contributions from
the hidden normal lift are retained, not assumed zero.

The finer matrix-weight bound matters: an entry (i,j) has degree at most
j-i in these exp/log words, since every strictly upper-triangular factor
advances the column index. Consequently the log-center coordinates
(c15,d14,d24,d25) have bounds (4,3,2,3). Only c15 can be quartic. Treating
all four central coordinates as arbitrary quartics is an unnecessary
relaxation and would hide the cancellation used below.

Use X|s>=|s+1>, Z|s>=omega^s and

    D(x,zeta)=omega^(x.zeta/2) X^x Z^zeta,
    [v,w]=zeta.x' - x.zeta'.

Then D(v)D(w)=omega^([v,w]/2)D(v+w). For nonzero central label lambda,

    rho_lambda(a,b,z)=omega^(lambda z) X^b Z^(lambda a),
    rho_lambda(exp(a,b,c))=omega^(lambda c) D(b,lambda a).

The three other central coordinates carry an arbitrary character mu. No
postselection on mu=0 is allowed or needed. For r factors condition on all
lambda_j nonzero; the carrier is r qudits, not an enumerated p^r table.

An explicit normal QFT uses negative F_p transforms on z and a. Their
outputs are lambda and eta. For lambda!=0 relabel j=eta/lambda, i=j+b.
For lambda=0, Fourier transform b as well to obtain the one-dimensional
characters. Tensor these circuits and the transforms on d. This realizes
the convention with matrix entries conjugate(rho(n)_ij), using only a
constant number of field operations/transforms per factor. It does not
require a Fourier transform on all of G. Approximate F_p transforms must
be charged to the global channel-error budget; this note does not assert
exact finite-gate implementations.

Starting with the ordinary mixed H-coset state, (1) and Schur orthogonality
give, after measuring the irrep label and discarding the independent row
multiplicity register, the normalized active block

    sigma(q,q') = 1/(p^m d) 1[q'-q in U] W(q)^dagger W(q'),  (2)
    W(q)=rho(F(q)), d=p^r.

The conjugated-QFT convention is important: the active kernel is not
silently replaced by its transpose. Labels obey Plancherel because
H intersect N=1. Each lambda coordinate is uniform on F_p, including the
aggregate one-dimensional sector lambda=0. Hence acceptance probability
is (1-1/p)^r >= 1-r/p >= 1/2. A finite counterexample H=Z(N) destroys this
law and makes the desired nonzero labels impossible. Quotienting by a
nontrivial intersection need not preserve the present representation family.

## 3. Why Measuring All Carriers Fails

For a genuine one-factor example H=<exp(E12+E23+E34+E45)>, pi(q)=q1*(1,1,1,1),
the noncentral log coordinates are

    a(q)=q1(q1-q2)/2, b(q)=q1(q3-q4)/2.

After q_i=Y_i+s_i q, quartic cancellation can make the quadratic
displacement coefficients commute. Their pairing with LINEAR displacement
coefficients still contains a nonzero multiple of sum_i lambda_i s_i^3 Y_i1.
For fixed active scales and labels this is uniform on F_p. Requiring the
whole coefficient space to be isotropic succeeds only 1/p in this example.
A Clifford cannot erase a nonzero symplectic pairing.

This falsifies that particular all-carrier measurement shortcut, NOT the
whole matrix-valued route. Instead retain a canonical graph of the linear
displacements as part of the unknown support.

## 4. Public Jet Alignment

Take fresh accepted source packets with public labels lambda_i. Choose
nonzero active scales, allowing consumed zero-scale inputs, such that

    sum_i s_i^4 lambda_i=0 in F_p^r.                        (3)

For p=3 mod4 the existing square construction gives beta_i with
sum lambda_i beta_i^2=0 from (r+1)^2 inputs. Set
s_i=beta_i^((p+1)/4), so s_i^4=beta_i^2. Take m+3 independent disjoint
relations, concatenate them and multiply each relation by an independent
nonzero scale. Each relation has at least two active inputs, since every
lambda_i is componentwise nonzero. Thus a>=2(m+3) active inputs. Rescale
relations until the active vector s is not constant; a fresh rescaling
fails with probability at most 1/(p-1). All checks precede the shear.
The existing square backend uses machine-word linear algebra and an
uncapped conic loop; it is a reference primitive, not a complete bounded
large-prime implementation. General primes require the published fixed-degree
diagonal-equation solver with its own bounded-retry accounting.

Introduce a fresh uniform q register, shear q_i to Y_i=q_i-s_i q and
measure every Y_i. Equation (2) has uniform diagonal q blocks, so the
Y_i are independent uniform vectors. Every outcome is accepted before
the public rank check. A branch has probability p^(-mk), not a preferred
rare value. Active nonzero scales leave the support difference q'-q in
the SAME U; zero-scale carriers contribute independent maximally mixed
factors and can be discarded. Never recycle their consumed input packets.

Write the common, unknown polynomial as

    Q_W(q)=c+Lq+(1/2) sum_jk B_jk q_j q_k,
    T=stack(L,B_1,...,B_m), D=2r(m+1),

where B_j is the 2r by m matrix of Hessian entries with first input index j.
Let D_i(b,a)=(b,lambda_i*a). For R=ar carrier qudits the stacked
displacement is

    v(q)=v0 + J T q + K Q_2(q),
    K_i=s_i^2 D_i,
    J_i=[s_i D_i, s_i Y_i1 D_i,...,s_i Y_im D_i].           (4)

All of K and J are PUBLIC. T is never supplied. Equation (3) makes im K
isotropic; K has rank 2r. After invertible block row operations, [K|J]
is the scalar design with rows (s_i,1,Y_i1,...,Y_im), tensored with I_(2r).
Nonconstant s makes its first two columns independent. The probability
that the remaining uniform columns fail full rank is at most

    sum_(j=0)^(m-1) p^(2+j-a) < p^(m+2-a)/(p-1).           (5)

Check this rank publicly. In particular im K intersect im J=0 and J is
injective. Constant s is a real failure, not a degenerate case to ignore.

The former random transverse-Lagrangian construction has been replaced by
the explicit isometry extension in
[DETERMINISTIC_JET_ALIGNMENT.md](DETERMINISTIC_JET_ALIGNMENT.md).
For R>=D+2r, prescribe the K columns in Z with separate extra coordinates
and the J columns with first-D X image equal to the identity; their Z
coordinates reproduce all original pairings. Deterministic transvections
extend this equal-Gram map to the ambient symplectic space. No randomness,
Lagrangian success estimate or retry cap is needed. The resulting S has

    (S K)_X=0, (S J)_X=(I_D,0)^T.                         (7)

This is stronger than simply making the quadratic terms diagonal:
the unknown linear part is IDENTICALLY Tq in every independently
generated batch, not a packet-dependent M Tq. The implementation verifies
both identities and S^T Omega S=Omega with arbitrary-precision field
arithmetic. Its input signature contains only p, labels, scales and outcomes.

## 5. Scalar Source With Fixed Support

Odd-prime Clifford synthesis can implement S, with a public phase convention
chosen so D(v) maps exactly to D(Sv). This is an established symplectic
Clifford primitive, not a newly assumed arbitrary unitary. No coherent
gate compiler is implemented in this pass.

Write the transformed gauge as

    W(q)=omega^psi(q) D(A(q),B(q)),
    A(q)=constant+(Tq,0), deg B<=2,
    phi(q)=psi(q)+A(q).B(q)/2.

The scalar psi is the sum of lambda_i*c15(Y_i+s_i q) and the three
mu-weighted other log-center coordinates. Its degree-four coefficient
is sum_i s_i^4 lambda_i times the SAME unknown corner coefficient, hence
vanishes by (3). Therefore deg psi<=3 and deg phi<=3. The quartic
isotropization step ALSO removes the leading scalar phase; no additional
degree-four scalar-erasure stage is required for the actual UT5 family.

Its exact matrix kernel in carrier coordinates t,t' is nonzero when

    q'-q=u in U, t'-t=-(Tu,0),

and its exponent is phi(q')-phi(q)-B(q).t+B(q').t'. Consequently it is
a scalar coset-state mixture with potential

    P(q,t)=-phi(q)-B(q).t, deg P<=3.

Measure only the last R-D carrier coordinates. Their differences are
zero; every outcome is uniform and accepted. The normalized remaining
state is the scalar phase source on a FIXED unknown subspace

    U_jet={(u,-Tu):u in U} <= F_p^(m+D).                    (8)

Constant displacements affect phases/coset origins, not (8). No unknown
unitary removing them is physically applied. The tests keep nonzero
constant displacements and explicitly verify spectator probabilities,
normalization, positivity and the sign in (8).

The scalar parameter interface is also polynomial-size, not an arbitrary
function table: take theta to contain all coefficients of Q in its six-r
Lie coordinates with their matrix-weight bounds. psi is public-linear in theta;
A and B are public-linear in theta. P is therefore public-linear in

    Theta=(1, theta_alpha, theta_alpha*theta_beta).

Use the SAME ordered symbolic Theta in every batch. The compiler uses
h=3r*binom(m+2,2)+2r*binom(m+3,3)+r*binom(m+4,4) base coefficients, and
1+h+h(h+1)/2 lifted parameters
suffice. Relations among these unknown parameters cause no problem:
coefficient-map cancellation is valid for all parameter values. Compiler
logic must never learn theta, expand a p^(m+D) table, or use truth-based
interpolation. `ut5_scalar_phase_compiler.py` now constructs this sparse
map directly from public affine substitutions and S. Tests compare it
with independent unknown coefficient assignments and actual matrix-word
UT5 potentials, including the distinction between log c and raw n15.
A nonzero mixed finite difference falsifies a linear-only base-parameter
compiler. A separate coefficient-level test keeps a nonzero unknown
corner quartic, verifies cancellation of its degree-four contribution
and retains its translated cubic terms. The sparse output is NOT yet an input to the production erasure
dispatcher. Keeping a common descriptor ordering is necessary but not
sufficient: the protocol must also pin the same hidden instance/chart.

The existing proposed CUBIC scalar unknown-support erasure argument would
then produce ordinary Fourier samples for U_jet. Projection to the original
q coordinates recovers U. For primes p=11 mod12 the initial quartic witness
uses the square-root construction and the later cubic/square/linear
controllers have the existing arithmetic interfaces. General primes still
require the appropriate published SDE solvers. Neither the sparse packet
adapter, a complete bounded large-prime tree nor the coherent matrix-source
instrument is implemented. Passing the tests does not close those gaps.

## 6. Cost, Completion And Limits

One alignment block uses k=(m+3)(r+1)^2 accepted source packets for the
p=3 mod4 construction. Per-packet label rejection costs at most two source
queries in expectation in the stated regime. Per-packet caps of
ceil(log2(k/delta)) make the chance of any missing accepted packet at most
delta. Equation solving, nonconstant rescaling, rank rejection, Clifford
sampling, transform approximation and scalar-erasure retries all need
separate budgets. Rejected quantum blocks are consumed. Unlimited retries
or free purification are not part of the proposed interface.

R<=rk=O(r^4), D=O(r^2), and all stored public matrices have polynomial
size in r and log p. Repeated exact row reduction in the reference
controller is polynomial, not an optimized implementation. Scalar
erasure at each of degrees 3,2,1 has a polynomial number of public
coefficient equations and a fixed-degree polynomial input arity. Its
total leaf count is the PRODUCT of these three arities times k, not their
sum. These polynomials can have enormous exponents. No useful runtime
estimate or numerical advantage has been established.

If exact U (or a certified class-dropping overestimate) is recovered,
restrict the ORIGINAL hiding oracle to its public preimage. For the exact
preimage HN, H is abelian and

    (HN)'=[H,N] N' <= gamma_3(G).

Thus HN has class at most three. This group-theoretic step does not need
N abelian. It connects to the previous proposed class-three completion,
not to a claimed new class-four scalar source for arbitrary subgroups.
Fresh subgroup cosets, proper coordinate compilation and the joint
approximation budget remain necessary. An arbitrary quotient after
learning H intersect N is not proved to fit this UT5 controller.

Strong classical filter: if the ORIGINAL hiding labels are bounded-degree
field polynomials in the group coordinates and the characteristic bound
holds, the existing value-query derivative/stabilizer attack applies,
including to nonmetabelian groups. The quantum intermediate's polynomial
potential does not imply such classical access to the original labels.
Opaque-label HSP is a standard research interface, not a demonstrated
external application. No factoring, discrete-log, graph-isomorphism,
code-equivalence or lattice consequence is asserted here.

## 7. What Would Kill Or Downgrade This Route

- A wrong orientation or missing multiplicity factor in (2): independently
  checked against the finite Heisenberg QFT and Schur sum, but still needs
  full symbolic source review for the complete proposed composition.
- Nontransverse H, or exponentially rare all-nonzero labels: explicit
  restrictions, not hidden promises to remove by assertion. H=Z(N) is a
  concrete failing control for the first shortcut.
- Cubic noncentral displacement terms: the present quadratic-jet argument
  no longer applies. A test injects such a term and detects residual X
  displacement. No extension to growing nilpotency class is claimed.
- Demanding all displacements commute or measuring all carriers: concrete
  controls destroy the intended support. Retaining (8) is essential.
- Packet-dependent hidden slopes: (7), not merely isotropy, is required.
  Two independently generated public batches are tested against the same
  unknown quadratic polynomial, including its constants and linear terms.
- Nonuniform shears, biased conditional label states, hidden symbolic
  coefficients, or discarded transcript correlations: any one invalidates
  reuse of the scalar erasure theorem. The formal source/composition proof
  has not been extended to this matrix-source route.
- Existing literature already supplies the same reduction: this remains
  possible. Targeted searches are not a novelty certificate.
- No important non-oracle input survives the classical filter: still the
  main impact limitation even if the whole proposed reduction is correct.

## 8. Evidence And Next Decisive Work

Code: `theorems/ut5_matrix_phase_alignment.py` is the public exact controller;
`theorems/ut5_scalar_phase_compiler.py` constructs the sparse symbolic map.
Tests: `tests/test_ut5_matrix_phase_alignment.py` checks actual UT5 matrix
exp/log structure, nonabelian increments, all central characters, the
normal QFT, the active block convention, the matrix-source shear including
zero-scale consumption, public canonical alignment for
one and two factors, a 127-bit prime, constants, stable hidden jets,
scalar branch kernels, the lifted-parameter compiler, exact scalar quartic
cancellation using matrix weights, and rejected/aborted
cases. Dense state matrices
are finite diagnostics only. No central claim/registry admission follows.

Verification at this pass: all 29 new controls and 553 connected Python
tests pass, with RuntimeWarning fatal. Touched Python syntax, the existing
formal crosscheck, site syntax/site checks and `qsearch.py validate` pass.
The full repository Python suite was not run; no new Lean proof or build
certifies this derivation.

Next: independent full-proof review of this source-to-scalar composition,
followed by a costed bounded controller only if the restricted theorem
survives. The public sparse compiler now exists; a complete erasure tree,
coherent Clifford compiler and matrix-source formal proof still do not.
Do not spend another pass
merely sampling more seeds, changing UI, or broadening the claim label.
Full nontransverse-H closure and a useful external reduction remain
separate harder questions.

Primary prior art checked, with deliberately limited attribution:

- [Bacon, Clebsch-Gordan transforms for Heisenberg HSP](https://arxiv.org/abs/quant-ph/0612107):
  efficient Heisenberg representation combination is established, not
  itself a new algorithmic primitive here.
- [Hostens, Dehaene and De Moor](https://arxiv.org/abs/quant-ph/0408190):
  modular symplectic descriptions and efficient elementary Clifford
  decomposition. This supports the Clifford primitive, not (4)-(8).
- [Ivanyos and Santha](https://arxiv.org/abs/1503.09016): fixed-degree
  diagonal equations and polynomial-phase methods. Their specified
  semidirect-product interface must not be silently equated with this one.
- [Imran and Ivanyos](https://arxiv.org/abs/2304.08376): quotient-image
  recovery followed by subgroup restriction is prior art. Their bounded
  prime-factor result does not certify this growing-prime source mechanism.

The derivation (1)-(8) is local proposed work, not a statement attributed
to those papers or an independently verified new theorem.
