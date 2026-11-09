# Sparse Fock torus: moment-source and quantitative audit

7 November2026. Read STATE/TRAPS, the Paley counterexample review, and
the actual retained Sugita/Paley/CIT texts under
`audits/sources/sparse_fock_torus/` (matching PDFs/source.json). No network,
Git/API, implementation, or full learner audit. **ACCEPT the quantitative
extension with the scope and epsilon qualifications below.**

## Sugita normalization and representation dimension

`sugita.txt`: Eq3 at47--52 defines M^(q)=c integral |overlap|^(2q).
The resolution of unity Eq7 and Eq8 at93--101 explicitly give c=dimD_lambda.
Taking traces of Eq7 shows the coherent-state measure has total mass1.
Thus Eq14--16 at140--155 gives the UNNORMALIZED probability twirl

    integral (|zeta><zeta|)^tensor2 dmu = Pi_(2lambda)/dimD_(2lambda),

not an extra factor of dimD_lambda. The coherent tensor square lies in
the single highest-weight/Cartan-product irrep, Eq11--13 at130--141.
Its multiplicity is one: the tensor product's extremal2lambda weight
space is one-dimensional. The projection formula holds against ANY unit
vector psi in the representation, not only coherent psi; its projector
expectation is at most1. No state ensemble for psi is assumed.

SectionIV(ii), Eq31 at251--255, applies to the antisymmetric w-particle
representation of SU(n). At q=2 its product simplifies to

    D2 = product_(j=0)^(w-1) (n+1-j)(n-j)/[(j+2)(j+1)]
       = binom(n,w)^2*(n+1)/[(w+1)(n-w+1)].

Footnote12 at341--343 permits using U(n): its central action is a global
phase on a fixed-particle sector, irrelevant to these absolute overlaps.
No assumption of Haar randomness on the full U(D) is being made. The
trivial w=0,n endpoint formulas give D=D2=1 directly.

For fixed occupation S, Haar invariance turns U^dagger|S> into that
coherent-state orbit. With D=binom(n,w), therefore

    E_U sum_S |<S|Lambda^w(U)|psi>|^4
      = (D/D2) ||Pi_(2lambda)(psi tensor psi)||^2 <= D/D2.

Each basis vector S has the same Haar integral; this is where the factor
D enters. The stated normalizations and dimension are correct.

## Approximate support and independent lists

Let theta=1-epsilon^2>0, i.e.0<=epsilon<1, and p_S be these probabilities.
If ANY subset A of size at most R has mass at least theta, then

    theta^2 <= R sum_S p_S^2.

Markov's inequality gives probability at most R*D/(D2*theta^2), capped
at1 if needed. The support subset A may depend arbitrarily on U: the
maximum is INSIDE the event, and no union bound over subsets is needed.
For pure states this is exactly the threshold for the best normalized
R-support projection to have trace distance at most epsilon.

For ANY random list of at most L passive frames jointly INDEPENDENT of U,
condition on the entire list. Each relative rotation is Haar, so the union
bound multiplies the result by L. Frames need not be mutually independent
or Haar. They may depend on the fixed psi or on U-independent transcripts.
They may not depend on additional U-informative data without a new proof.

## Paley application and measurement boundary

`paley.txt`: Theorem32 at464--473 gives the nonzero quadratic-residue
difference set for q=3 modulo4 with parameters(q,(q-1)/2,(q-3)/4).
Definition33 at474--477 identifies the symmetric2-design. The design
incidence identity at64--79, applied to this symmetric case, supports the
counts used in the existing counterexample review. Its source is ordinary
design theory; the fermionic moment/stabilizer deductions are separate.

For the reviewed p=n family, w=(n-1)/2 and r=n, so D/D2=(n+3)/(4D).
The list-success probability is at most

    L*R*(n+3)/[4*binom(n,(n-1)/2)*(1-epsilon^2)^2].

For polynomial L,R and fixed epsilon<1 (or inverse-polynomial theta),
this is exponentially small along the prime3-mod4 family. It quantifies
APPROXIMATE support failure, strengthening mere generic exact nonvanishing.

Identical second/fourth Majorana moments imply identical full outcome laws
for INDIVIDUAL binary Pauli/Majorana monomials of degree at most4 on fresh
copies: each Bernoulli law is fixed by its mean. Conditioning inductively
shows that adaptive choices of such observables and all resulting moment-
based frame lists are U-independent too. This does NOT apply to arbitrary
qubit-Pauli weight2/4, a general multi-outcome spectral measurement of a
quadratic sum, several joint occupation outcomes on the SAME copy,
higher-degree data, or coherent joint-copy protocols. It also concerns
the stated torus-compatible PASSIVE completions, not all Gaussian frames.
Thus it is not a full sparse-Fock learner lower bound or hardness theorem.

## CIT scope

`cit.txt`: definitions68--73 specify input circuit C AND order n, and ask
whether f(zeta_n)=0; the syntactic-degree bound is unary. Leaf monomial
exponents are binary, and ordinary polynomial degree may be much larger
(55--66). Theorem2 at114--121/574 places this SPECIFIED-root zero test in
randomized NC, with two-sided error; lines563--572 explain random Galois
conjugate evaluation. It does not promise existence or construction of a
small-order/small-degree root at which an arbitrary target is NONZERO.
The powerful-skew PIT application at586--591 instead chooses root order
greater than the polynomial's ordinary degree, which may be exponentially
large numerically. Do not turn either result into an unpaid small good
specialization theorem or a small-number-field constant-map interface.
