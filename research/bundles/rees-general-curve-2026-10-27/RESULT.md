# A Fixed-Class Polynomial-Curve Gap For The Rees State Source

2026-10-27. Constructive mathematical deduction with one completed independent
AI adversarial review; no fatal flaw found within the stated scope. Exact
algebra diagnostics are separate from the proof. Not a novelty certificate,
a native quantum implementation, human peer review, or a speedup.

## Scientific Question And Answer

Can the existing class-at-most-three random-dilation source conversion be
extended to every FIXED nilpotence class without assuming a pointwise state
displacement gap that can shrink with p?

The argument below gives such an extension for sufficiently large primes
depending only on the fixed class. It replaces that microscopic promise by
the same subgroup-twirl robustness promise used in the existing class-three
result. The receiver, zero-moment design and ray-character cancellation are
imported from existing repository work, not newly claimed here.

This does not address the growing-class source-tree obstruction, prove a
hard application, or settle novelty of the underlying HSP theorem. In
particular, a source conversion is not an end-to-end useful algorithm.

## 1. Precise Curve Theorem

Let c>=1 be fixed, p>c prime, and F_c the free Lie algebra on generators
X_1,...,X_c with weights 1,...,c, modulo all words of total weight greater
than c. Write D=dim(F_c) and G_c=exp(F_c), with Lazard/BCH multiplication.
The elementary tensor embedding gives D<=D_*=2^c-1: there are 2^(w-1)
nonempty associative words of weight w. No ambient input dimension occurs
in D. For example, D at c=1,...,6 is 1,2,4,7,13,22.

Define

    A(t)=sum_(j=1..c) t^j X_j,    g(t)=exp A(t),
    T_pi=(1/p) sum_(t in F_p) pi(g(t)),
    m=2D^2+1,
    P_c=max(16*c^D, 4D(c-1), 4(c-1)^2, c+1).

For every nontrivial irreducible COMPLEX unitary representation pi and
every prime p>=P_c,

    ||T_pi|| <= theta_c=2^(-1/(2m)) <= 1-1/(4m).              (1)

All bounds remain valid, more conservatively, with D_* substituted for D
in m, P_c and the gap. There is no claim that these constants are sharp.
No small-prime extension is made. At c<=3 the existing specialized result
has substantially better constants and should remain the preferred bound.

For any class-at-most-c Lie algebra L over F_p and coefficients
A_j in gamma_j(L), the assignment X_j -> A_j defines a quotient onto
K=exp Lie<A_1,...,A_c>. Thus (1) applies to the non-K-invariant part of
any unitary representation of K for the curve exp(sum t^j A_j). Extra
relations, zero coefficients and lower actual class do not invalidate it.

## 2. A Bounded Full-Rank Word

The right logarithmic tangent is

    W(t)=g'(t)g(t)^(-1)
        =sum_(k=0..c-1) ad(A(t))^k A'(t)/(k+1)!.

This formula is formal differentiation over F_p, not a real derivative.
All factorials are units since p>c. Its weight-j component is t^(j-1)Y_j,
where

    Y_j=jX_j + a Lie polynomial in X_1,...,X_(j-1).

Consequently W has degree <=c-1, its values at t=0,...,c-1 span all Y_j,
and the Y_j generate F_c by induction on weight. The tangents themselves
span only c dimensions; conjugation is essential when D>c.

Start V_0=span{W(0),...,W(c-1)}, and define

    V_(r+1)=V_r + sum_(s=1..c) Ad(g(s)) V_r.

If this chain stabilizes, its limit V is invariant under all Ad(g(s)).
It is therefore invariant under log Ad(g(s))=ad(A(s)), since the truncated
logarithm is a polynomial in Ad(g(s))-I. The nonzero-point Vandermonde
matrix (s^j), 1<=s,j<=c, is invertible, so V is invariant under every
ad(X_j). It is a Lie ideal containing all Y_j; hence V=F_c. This proof
does not require enumeration of G_c or a mixing assumption.

Every strict step raises dimension. Thus choose a basis

    Ad(x_i) W(t_i), i=1,...,D,

where x_i is a word of length <=D-1 in g(1),...,g(c). Form the word

    F(h)=product_(i=1..D)
           x_i g(t_i+h_i) g(t_i)^(-1) x_i^(-1).

At h=0 every block is identity. Its D derivative columns in log coordinates
are precisely the chosen basis, so its Jacobian has full rank. Each block
uses <=2D signed curve factors, for <=2D^2 in total. Insert g(0)=1 factors
to embed these signed factors in the alternating word

    Psi(u)=g(u_1)^(-1) g(u_2) ... g(u_(2m-1))^(-1) g(u_(2m)).  (2)

At most twice as many positions plus parity padding suffice. The selected
positive-factor parameters are t_i+h_i; all other positions are fixed to
the constants just constructed, or zero. With m=2D^2+1 there is ample
padding. Hence one specified D-column Jacobian minor J of log Psi is
nonzero at a point over F_p, for EVERY prime p>c.

The witness may depend on p, which causes no issue: the uniform degree and
word-length bounds do not. This is stronger than assuming a rational
determinant happens to stay nonzero modulo all sufficiently large primes.

## 3. Good Fibers And The Spectral Bound

Weighted BCH shows that every coordinate of log Psi is a polynomial of
total degree <=c in the 2m scalar inputs. In fact a weight-w coordinate
is homogeneous of degree w. Thus deg J<=D(c-1), and the elementary
finite-field polynomial zero bound gives

    beta=Pr[J(u)=0] <= D(c-1)/p.                              (3)

Keep only inputs with J(u)!=0 and let nu_good be their pushforward as an
UNNORMALIZED subprobability distribution on G_c. Fix an output and the
2m-D unselected variables. The remaining D equations have degree <=c;
every retained root has nonsingular Jacobian. There are at most c^D such
roots, even if the same fiber also has positive-dimensional singular
components. This precise nonsingular-root form is Corollary 1.3 of
[Bafna, Sudan, Velusamy and Xiang](https://arxiv.org/html/2102.00602v1).
It follows that

    max_g nu_good(g) <= c^D/p^D,
    |G_c| sum_g nu_good(g)^2 <= c^D.                          (4)

Do not assert that all fibers are finite, bounded, or equidistributed.
No Lang-Weil estimate is needed. Only the fixed nonzero-minor part is used.

Use Fourier convention hat(nu)(pi)=sum_g nu(g)pi(g). Finite-group
Plancherel, with ordinary Hilbert-Schmidt norm, says

    sum_pi dim(pi) ||hat(nu_good)(pi)||_HS^2
       = |G_c| sum_g |nu_good(g)|^2 <= c^D.

For a nonlinear irreducible pi, dim(pi)>=p: complex irreducible degrees
of a finite p-group are powers of p. For example this follows from the
induction theorem for nilpotent groups in
[Teleman's representation-theory notes, Theorem 17.5](https://www.math.uchicago.edu/~margalit/repthy/RepThry.pdf).
Therefore the good part has operator norm at most sqrt(c^D/p), while the
discarded bad part has operator norm at most beta. For the distribution
nu of (2), independence and the chosen signs give EXACTLY

    hat(nu)(pi)=(T_pi^* T_pi)^m,
    ||T_pi||^(2m) <= sqrt(c^D/p)+D(c-1)/p <= 1/2.             (5)

This is a singular-value argument. The false substitution T_pi^(2m)
would fail for nonnormal matrices. Inverses occur only in this mathematical
proof, not as unknown-state inversion resources in the source.

Linear nontrivial characters must be handled separately; G_c is NOT a
quasirandom group in the all-nontrivial-representations sense. Such a
character on g(t) is an additive character of a nonconstant polynomial
sum alpha_j t^j of degree <=c<p. The usual polynomial exponential-sum
bound gives ||T_pi||<=(c-1)/sqrt(p); degree one gives zero exactly.
At P_c this is <=1/2, which is stronger than (1). Finally Bernoulli's
inequality gives (1-1/(4m))^(2m)>=1/2, proving the rational gap in (1).

This uses the standard representation-dimension/flattening mechanism,
not a newly invented Fourier principle; compare
[Tao's discussion of quasirandomness and flattening](https://terrytao.wordpress.com/2011/12/16/254b-notes-3-quasirandom-groups-expansion-and-selbergs-316-theorem/).
The concrete work here is the weighted-curve word and source composition.

## 4. Native Source Contract And Conversion

Retain the existing source contract: explicit prime-field Lie algebra L;
fresh IID copies of a fixed PURE state rho=|psi><psi| on q qubits; and a
uniform coherent linear representation action SELECT(U). Let H be the
ray stabilizer of psi. For every subgroup K not contained in H assume

    TD(rho, T_K(rho)) >= delta,
    T_K(rho)=|K|^(-1) sum_(g in K) U(g) rho U(g)^*.

The twirl is an analytic quantity, not an oracle supplied to the algorithm.
No state-preparation inverse, conjugate copies, hidden H, or prime-sized
state bank is supplied. A black-box unit-cost SELECT permits only a QUERY
complexity claim; a gate theorem must charge its uniform implementation.

Apply (1) in the conjugation representation on Hilbert-Schmidt space,
where rho has squared norm one and the invariant projector is T_K. Then

    E_t |<psi|U(exp(sum t^j A_j))|psi>|^2
       <= 1-g_c*(1-Tr(rho T_K(rho)))
       <= 1-g_c*delta^2,       g_c=1/(4m),                   (6)

when K is not contained in H. The last implication uses purity and
TD(rho,sigma)<=sqrt(1-Tr(rho sigma)). Vectorization/conjugation occurs
only in the proof; it does not authorize preparing conjugate inputs.

Reuse the existing nonzero multiset S with moments sum_s s^j=0 for
j=1,...,c and enough distinct evaluations. Its existing bound is
M=|S|<=(c+1)!, with construction costs still paid. For an address a in
the lower-central Rees group, one packet consists of M fresh native copies
and independent u uniform in ALL of F_p, controlled by

    tensor_(s in S) U(exp(E_(su)(log a))).

Discard both scale record and targets. Each evaluation, including u=0,
is a homomorphism. On the lifted H the existing moment identity cancels
the ray character EXACTLY, so averaged overlap is one. Off the lifted H,
some coefficient A_j is outside log H and the generated K is not in H.
Keep any one factor s_0!=0 in the squared-modulus upper bound; s_0*u is
uniform. Cauchy-Schwarz and (6) give

    |Fbar(a)| <= sqrt(1-g_c*delta^2) <= 1-g_c*delta^2/2.      (7)

Independent packets use fresh states and independent discarded scales.
The address kernel is Fbar(b^(-1)a)/|A| with the existing convention.
Keeping or reusing scale records is a different source contract.

For a validated receiver cap B, ell>=log2|A| and total error epsilon,
the old amplification proof accepts

    gamma=g_c*delta^2/2,
    k=ceil((ell+ceil(log2(4B/epsilon)))/gamma),
    Q=B*k*M,
    per-SELECT half-diamond error eta=epsilon/(8Q).

This allocates at most epsilon/4 to source amplification and epsilon/8
to the complete adaptive-channel SELECT hybrid. It does not certify the
remaining receiver/arithmetic/sampling errors. Q counts both native copies
and coherent action calls; gate cost includes Q*C_U(eta), q, public Rees
arithmetic, moment design, address preparation, native acquisition, uniform
scalar sampling, and the existing receiver. For FIXED c all new constants
are independent of n and log p. The new source does not repair a
superpolynomial receiver or unpaid native access.

## 5. Attempts To Refute The Claim

1. Nonnormality would destroy a naive walk-power proof. Equation (5) uses
   alternating inverse/positive factors, and a nilpotent-matrix regression
   demonstrates why replacing it by T^(2m) is wrong.
2. Singular fibers may be huge. Only a nonzero fixed Jacobian-minor subset
   is bounded, without renormalizing the good mass. The nonsingular-root
   theorem applies after fixing the other coordinates.
3. Small characteristic destroys interpolation and factorials. We require
   p>c even for algebra diagnostics and p>=P_c for the stated gap.
4. Unconjugated tangents cannot span the nonabelian algebra. The exact
   controls deliberately show rank c<D and require the adjoint closure.
5. Almost invariant pure inputs make delta small. The cost scales as
   delta^(-2); the theorem does not extract tiny asymmetries for free.
6. Mixed inputs break the pure-overlap implication. No mixed-state source
   extension is asserted. A classical convex mixture is not substituted
   for the pure native state.
7. Constant-class gaps do not imply growing-class efficiency: D may be
   exponential in c, P_c very large, and moment packets factorial in c.
   The previously reviewed destructive-source obstruction still applies.
8. No hard application has been supplied. Easy abelian states already
   separate pointwise and twirl robustness; that demonstrates the changed
   promise, not algorithmic novelty or quantum/classical separation.

## 6. Implementation And Next Decision

`curve_certificate.py` constructs the weighted free Lie algebra inside the
truncated associative tensor algebra, closes tangents under conjugation,
and writes an explicit alternating word and nonzero Jacobian minor.
An independent product-rule derivative checks each witness; tests use
FLINT for an additional determinant/rank check. These bounded computations
do not prove the arbitrary-c theorem. The proof above does not rely on
them. No Hilbert-space, group, or hiding-function enumeration is performed.

`source_plan` conservatively requires D_* or a larger upper bound, not an
unchecked smaller dimension. It reports conditional copy/query costs and
explicitly declines to certify a total elementary-gate cost or the supplied
moment-design/receiver assumptions. `replay.py` emits deterministic live
algebra artifacts only. No main CLI, candidate admission or UI is changed.

Next high-value work is a concrete natural state/action task whose input
really supplies this access and inverse-polynomial twirl robustness, then
a comparison with existing stabilizer-learning and classical algorithms.
Do not spend another pass merely improving these very loose constants.

The parent read all of `../rees-general-curve-review-2026-10-27/REVIEW.md`.
That review independently reconstructed the proof, accepted the conditional
source and direct-HS application corollary, and emphasized the imported
design/receiver boundaries. It did not audit the code, certify novelty, or
establish an application. See REVIEW_RESPONSE.md for retained qualifications.
