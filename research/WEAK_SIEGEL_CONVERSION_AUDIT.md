# Weak Siegel Source: Conversion And Stabilization Audit

**Later constructive refinement (same date):**
[SIEGEL_CAYLEY_REPOLARIZATION.md](SIEGEL_CAYLEY_REPOLARIZATION.md) gives a
genus-two plus-quotient construction and weak-mask-independent kernel and
mark transport. It avoids the failed complement below. Affordable
multiplier selection, actual torsion/model costs and coherent joint
canonicalization remain unresolved. The original weak-input problem is
not solved. [SIEGEL_REVERSE_TRANSPORT_ATTACK.md](SIEGEL_REVERSE_TRANSPORT_ATTACK.md)
adds an original-input classical attack when the target model exposes
informative computable polarized automorphisms; no full target order is
needed for that scoped attack.

2026-10-30. Four focused automated agents checked literature applicability,
stabilization, classical interpolation, and elliptic-factor reduction.
These are mathematical deductions and exact arithmetic controls, not an
implemented geometric source, a cryptanalytic break, or a speedup claim.

## Decision And Input

Keep the original problem open, but do not implement a purported oracle
by substituting interpolation for repolarization. The checked statements
do not justify that substitution. A constructive stabilization attempt
below gets a smooth quotient but the wrong pulled-back polarization.

Use exactly the input in [the elementary-lift note](SIEGEL_ELEMENTARY_REPOLARIZATION.md):
fixed g>=2, A=E^g with known evaluable End(E), an original polarized model
(B,lambda_B), and a weak ell-polarized isogeny phi:A->B. At an accessible
auxiliary order r the evaluator returns a_r*phi on a full ordered basis,
with ONE unknown unit a_r for the whole basis. Charge point fields,
pairings, small discrete logarithms and model conversions. No geometric
ell-torsion, full End(B) basis, or Hom(A,B) module is provided.

For an actual degree-one lift sigma of a queried symplectic matrix, put

    S = sigma^dagger sigma,
    psi = phi sigma^-1,
    H = (1/ell) phi S phi^dagger = phi S phi^-1.

Adjoints here use the ORIGINAL polarizations. The prior deduction gives
an integral positive principal polarization lambda_B H, and

    psi^dagger H psi = [ell],
    F := psi^dagger psi = ell sigma^-dagger sigma^-1,
    psi psi^dagger = ell H^-1.

The still-missing operation constructs the new geometric polarized model
with point transport and ONE jointly marked canonicalization. The target
is not merely an abstract torsion module or an evaluator string.

## 1. Verified Literature Boundary

- **Corte-Real Santos--Piasecki--Wesolowski, ePrint 2026/1142:** the
  [abstract](https://eprint.iacr.org/2026/1142) was accessible on this date;
  ordinary requests for the full PDF returned HTTP403. Author publication
  pages linked back there; no independent full text was located. Its
  full theorem hypotheses remain UNVERIFIED, not disproved.
- Their [April presentation, slides 10--16](https://jc2-2026.sciencesconf.org/file/1366992)
  states interpolation for two already encoded PPAVs and exact torsion
  assignments. Its dimension dependence is L^poly(g). Those slides do not
  establish our weak-input change-of-polarization operation.
- [Page--Robert--Soumier, Theorem6.9](https://www.math.u-bordeaux.fr/~damienrobert/pro/publications/articles/ClapotisHD.pdf)
  constructs polarized varieties from supplied Hermitian modules.
  Definition5.2/Theorem5.8 require generators of the WHOLE Hom group;
  Remark5.1's small-prime evaluation interface does not remove that
  requirement. Fixed dimension and its other setup assumptions matter.
- [Robert, Theorem5.19 and Corollary5.22](https://www.math.u-bordeaux.fr/~damienrobert/pro/publications/articles/isogeny_survey.pdf)
  give elliptic HD interpolation from exact CRT torsion images at N>deg(phi),
  coprime to that degree. Separate CRT fields are allowed; the explicit
  cost charges their degrees. This is not reconstruction from independently
  projective tuples, nor a new higher-dimensional target polarization.
- [Montessinos, Definitions2.14/2.18 and Theorem3.5](https://arxiv.org/html/2601.18050#S3)
  uses good full-ring representations, including evaluators and additional
  data, with stated GRH/KLPT assumptions. One torsion-only endomorphism is
  not that input.

Applying polarized interpolation directly to psi requires its target
(B,lambda_B H) already encoded. Applying it to H on the OLD polarized B
also fails generically: H^dagger H=H^2 need not be a scalar. Supplied target
End/Hom lattices enable the separate classical attacks already documented;
they cannot be added without changing the comparison problem.

## 2. A Constructive Source-Side Completion

This removes one plausible obstacle without pretending it solves conversion.
For any nonzero integer k, replace F by k^2 F. It is an explicitly known
positive Hermitian matrix over the source quaternion order O.

Start a rectangular matrix U with I_g. For each i<j append the row with
conjugate(F_ij) in column i, -1 in column j, and zero elsewhere. Its
off-diagonal Gram entries are -F_ij. Let c_i=(U^dagger U)_ii. Choose a
squarefree product N of accessible small odd primes, avoiding p*ell, with

    N > max_i(F_ii+c_i).

Each diagonal deficit N-F_ii-c_i is a positive integer. Express it as four
integer squares and append the four corresponding single-coordinate rows.
The resulting known, evaluable C:A->E^m has

    C^dagger C = N I-F,        m=5g+g(g-1)/2.

No matrix square root or hard quaternion norm solution is hidden here.
Unconditional expected polynomial-time four-square decomposition is supplied
by [Pollack--Trevino, Section4](https://math.colgate.edu/~integers/sjs15/sjs15.pdf),
not their ERH-conditional Section3 algorithm. Bit lengths of N and C remain
polynomial in the known source data. Fixed g keeps the stabilized dimension
fixed; it does not make point-field and model-conversion costs disappear.

Temporarily GRANT exact, globally consistent auxiliary images of psi. Set

    X=(B,lambda_B) x E^m,
    j=(k psi,C):A->X.

The identity rows make j an embedding; j^dagger j=[N]. Hence j(A[N]) is
isotropic in X[N]. With the required encoded models and kernel coordinates,
extend it to a maximal isotropic L prime by prime and compute q:X->Y=X/L
with q^dagger q=[N]. This uses the usual polarized quotient operation;
neither its geometric implementation nor the exact-image grant is supplied
by our finite controls.

Since qj kills A[N], it factors as qj=h[N]. The identity

    [N]^2 h^dagger h = j^dagger q^dagger qj = [N]^2

gives h^dagger h=I. Thus Y has A as a principally polarized factor.
Grant explicit splitting Y=A x D as well, to isolate the next failure.

## 3. The Complement Has The Wrong Polarization

Let i_B:B->X be the original factor inclusion. The natural complementary
map is delta=(I-hh^dagger)q i_B. From h^dagger q=j^dagger,

    delta^dagger delta
      = i_B^dagger (q^dagger q-jj^dagger) i_B
      = N I-k^2 psi psi^dagger
      = N I-k^2 ell H^-1.

It therefore pulls lambda_D back to lambda_B(NI-k^2 ell H^-1), NOT to
lambda_B H. This identity is independent of the isotropic completion L.
The factor D has dimension m, not g; neither the identity nor abstract
splitting supplies a desired B-factor inside it.

There is a sharper obstruction in dimension TWO. Write the known
S=sigma^dagger sigma as a 2x2 Hermitian quaternion matrix. Its positive
Moore determinant is one. With t the sum of its two integral diagonal
entries,

    S^2-tS+I=0,     H^2-tH+I=0,     H^-1=tI-H.

The second equation follows by rational conjugacy, not by assuming a known
standard Rosati presentation for End(B). In the prior reduced-trace
convention t=Tr(H)/2. If H is nonscalar, I and H are rationally independent
and t is an integer >=3. For any rational c,

    NI-k^2 ell H^-1 = cH
      implies c=k^2 ell and N=k^2 ell t.

Thus ell divides N, contrary to the chosen coprime smooth quotient budget.
No integer rescaling k of THIS map repairs it. When H=I this obstruction
does not apply; that is the case with no new polarization needed.

This excludes the direct complementary-map criterion only. Different maps,
additional isogenies, or a genuinely new factor-identification construction
are not excluded. A useful continuation must specify such a construction
and its costs, not just assert that an appropriate factor exists.

## 4. Weak Signs Are A Separate Obstacle

For an odd auxiliary prime r and a primitive source pairing zeta,

    e_B(a_r phi(P),a_r phi(Q)) = zeta^(ell a_r^2).

Small-order discrete logarithms recover a_r^2. Dividing the whole image
tuple by either square root gives epsilon_r phi(P_j), epsilon_r=+1 or -1.
These are exact Kummer images at that order, but signs at distinct primes
are independent. For squarefree M with s odd prime factors there are 2^s
square roots of a unit square, or 2^(s-1) choices modulo global sign.

For example let alpha^dagger alpha=[M-ell] on A^u, using an integer
four-square matrix with u<=4. At r|M the graph

    {(alpha P, epsilon_r phi^(x u)(P)): P in A^u[r]}

is maximal isotropic for EQUAL-DIMENSION polarized source/target factors:
its pairing multiplier is (M-ell)+epsilon_r^2 ell=0 mod r. Every sign
assignment passes this test. It need not yield the quotient splitting
required to interpolate the true phi. The Kummer quotient of a PRODUCT
identifies simultaneous negation, not changing only the second component.
Separate Kummer coordinates do not determine this graph.

Queries at composite orders do not remove the ambiguity by pairing/group
arithmetic alone. Extend any choices epsilon_r by CRT, consistently along
prime powers, to epsilon_m with epsilon_m^2=1. Replacing the hypothetical
unmasked torsion action by epsilon_m phi_m and the mask by a_m epsilon_m
preserves every weak answer and pairing. This is a statement about torsion
data, NOT about a second global geometric morphism: the existing rigidity
bound can force geometric uniqueness up to global sign. Finding that
geometrically compatible choice is still an algorithmic task.

### A Conditional Escape, With Its Cost

At an odd prime power R=r^a a unit square has only two roots. If the full
R-torsion basis and common-mask queries are affordable, normalization gives
exact assignments up to one harmless global sign. The pairing logarithm
can use Pohlig--Hellman, charging r, a and the point-field representation.
This really removes the relative-sign obstacle, not repolarization or
abstract-kernel extraction.

For scalar Frobenius [lambda] over the base field, the extension degree
needed for full R-torsion is its multiplicative order modulo R. If

    d=ord_r(lambda),    c=v_r(lambda^d-1),

then for odd r the degree is d*r^max(0,a-c). This follows directly by
lifting valuations of lambda^d-1. For E:y^2=x^3-x with p=11 mod36,
Frobenius over F_(p^2) is [-p]; at r=3, d=c=1. Taking R=3^a>ell for the
standard graph interpolation needs extension degree 3^(a-1)>ell/3.
That is exponential in log(ell), not cheap because 3 is small.

Large c can instead give accessible torsion and an easier input regime.
Neither case alone recovers the abstract ell-kernel: compact interpolation
and kernel-coordinate recovery are distinct computational tasks.

## 5. Elliptic Factors Leave The Gluing Problem

Write V_i=E_i[ell], d_i=dim(K intersect V_i), and factor the restriction
geometrically as phi|E_i=j_i f_i through the elliptic image C_i. Isotropy
gives d_i in {0,1}. Degree and polarization pullback give

    deg(f_i)=ell^d_i,
    j_i^*lambda_B = ell^(1-d_i) lambda_C_i.

For d_i=1 this is a degree-ell elliptic isogeny onto a principally polarized
factor. For d_i=0 it is an isomorphism onto an embedded curve whose induced
polarization has multiplier ell. With s=sum_i d_i, the addition map
product(C_i)->B has geometric degree ell^(g-s), from factoring phi through
the product of the f_i. Recovering each intrinsic elliptic isogeny need
not recover this remaining gluing.

The proposed coordinate projectors expose the exact obstruction. If e_i
is the coordinate idempotent on A, then

    q_i = (1/ell) phi e_i phi^dagger = phi e_i phi^-1,
    q_i in End(B) iff e_i K is contained in K iff d_i=1.

The first equivalence is descent through A/K. For the second,
(projection_i K)^perp=K intersect V_i by K=K^perp. Thus projection_i K
has dimension 2-d_i; its containment in K intersect V_i holds exactly
when d_i=1. When d_i=0, the denominator ell is genuine. Defining q_i(P)
by an arbitrary ell-division point followed by ell*q_i is not even
well-defined. Nevertheless its torsion matrices away from ell are
W_r e_i W_r^-1, with W_r=a_r phi_r; scalar cancellation does not make
this rational projector an integral geometric morphism.

An actual easy fixture is A=B=E^2, ell=5,

    phi = [[1,2],[-2,1]],       phi^dagger phi=5I,
    K = {(P,2P): P in E[5]},
    q_1 = (1/5)[[1,-2],[-2,4]],
    q_2 = (1/5)[[4,2],[2,1]].

Both restrictions are embeddings and both projectors are nonintegral.
Reversing off-diagonal signs gives a different kernel with the same
intrinsic degree-one elliptic instances. There are 120 nonsplit graph
Lagrangians and 36 split ones among all 156 Lagrangians in F_5^4.
This demonstrates missing gluing information in the PROPOSED reduction,
not hardness or absence of information in the original input.

If K splits across all coordinate factors, a direct factorwise reduction
is plausible, but still needs explicit elliptic models, point transport,
and the weak evaluation access required by the genus-one algorithm.
[Chen et al., Definition2 and Section4.2](https://arxiv.org/html/2305.19897#S4.SS2)
cannot be invoked on an unspecified embedded image. An algorithm recovering
the full embedded gluing outside the split case would be a new step.

## 6. Scope And Next Decisive Work

The public source matrix completion is constructive. The source as a whole
is still CONDITIONAL on geometric conversion and joint labeling. No new
classical solution to its original input has been established here.

Reopen the conversion claim only with one of:

1. The full2026/1142 theorem and proof, checked against the actual weak
   input and changed polarization, not the abstract or old slides.
2. A new geometric repolarization construction with point transport that
   avoids both full target lattice inputs and the complementary-map
   mismatch above.
3. A genuine classical attack on the same weak input, with its field,
   normalization, and abstract-kernel conversion costs paid.

Do not spend another pass adding generic quotient wrappers, more small
Gram examples, or candidate records for this unfinished source. The tests
are falsification controls, not an experiment claiming quantum advantage.

## Verification

Downloaded-source SHA-256 receipts, checked2026-10-30:

| Primary document | SHA-256 |
| --- | --- |
| April PPAV slides | `19e42963355051027e1d67d69edb14d3192d9377f00d24dd4d1191fe213f0bdd` |
| Page--Robert--Soumier full paper | `c4b1fad2d64d9a9c8527f3c93f972dd62de8545683cf364fa20b69608b1eec47` |
| Robert isogeny survey | `b46bc67d5db739d3137d7539d2b0f2ccada45a7b2060c8a6befe7995a80c9121` |

`tests/test_siegel_stabilization.py` checks rectangular completion, the
complementary pullback, the forced ell factor, the scalar exception, and
actual quaternion lift identities, plus the factor/projector controls.
No geometric quotient is executed.
`tests/test_weak_isogeny_signs.py` checks the independent CRT signs,
isotropic graph ambiguity, and prime-power field-degree accounting.
There are82 new controls in these two files. Parent verification with
`/opt/anaconda3/bin/python` passed221 focused tests across seven files,
including the prior geometric-source and supplied-lattice controls and CLI
parser tests. Both new files compile; twelve site JavaScript files pass
`node --check`; `python qsearch.py validate` returns valid=true, issues=[].
This is not the full repository suite, a Lean proof, or geometric/quantum
execution. An independent final automated mathematical read found no fatal
or scope error; that reviewer's default Python lacked flint, so its test
collection did not run. The reported221 executions are the parent's.
