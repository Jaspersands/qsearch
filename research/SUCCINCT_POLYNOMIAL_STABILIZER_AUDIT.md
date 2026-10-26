# Succinct Polynomial Symmetry: Reduction And Classical Filter

2026-10-21. Written reduction/attack under review, with exact finite
controls. NOT an admitted quantum result, novelty claim, useful hard
instance, general polynomial-equivalence algorithm or executed HSP solver.
This probes an exclusion in CLASS_THREE_APPLICATION_AUDIT.md instead of
repeating the already-covered explicit graph/code/tensor cases.

2026-10-23 parameter extension: BOUNDED_CODIMENSION_HSP_REDUCTION.md
replaces the fixed-class assumption by [Gamma:H]<=p^k for supplied matrix
p-groups with p>max(D,4). Public logarithm/commutator closure supplies the
growing-class Lie input; the SAME fixed fingerprint and all classical
filters remain mandatory. The conditional terminal Rees bound is
2^O(k^3 log(k+2))*poly(s,D,log p). No independently motivated hard family,
novelty certification or quantum execution follows. The k=1 case already
reduces to ordinary abelian HSP. Existing fingerprint/orbit-module tests
were rerun in the 125-test selected suite; all PASS.

2026-10-22 additional filter: MOORE_GRADIENT_CLASSICAL_FILTER.md recognizes
scalar Moore forms from their arbitrary public arithmetic DAG, without an
exposed row basis, via ordinary gradients and an independently tested full
polynomial identity. This reduces their p-group symmetry to a known
subspace-stabilizer problem even when the orbit rank is exponential. The
UT10(F_p)^m construction has exact orbit rank10^m and still collapses.
Failure of the old degree guards AND orbit-rank cap is not hardness evidence.

2026-10-22 update: POLYNOMIAL_ORBIT_MODULE_CLASSICAL_FILTER.md adds a
different classical route: learn a small cyclic orbit module by adaptive
extension-field PIT, retain a faithful original-matrix block, and reduce
to a known matrix vector-stabilizer algorithm. It needs neither derivative
guard. Exact controls include the actual class-nine ambient group and a
degree-11,966,490,760,401 polynomial with orbit rank 10. No quantum
advantage or general classical stabilizer implementation is claimed.

## 1. Actual Computational Problem

Input: a division-free arithmetic circuit C over F_p, of binary gate size
s, computing a FORMAL polynomial F in D variables; a known prime p>4;
and matrix generators of a PROMISED p-subgroup Gamma<=GL(D,p) of class
at most four and exponent p. Output generators of

```
H = {g in Gamma : F(g^-1 x) = F(x) as formal polynomials}.
```

Matrix entries and circuit constants are public input. No hidden subgroup
or circuit generating its invariants is supplied. A syntactic upper bound
Delta on total degree can be computed gate by gate (max at addition, sum
at multiplication); Delta<=2^s is sufficient. Its binary description is
polynomial even when the polynomial has exponentially many coefficients
or exponentially large degree. Constant/zero circuits are allowed.

This is a stabilizer problem, NOT the transporter F(g^-1 x)=G(x).
The old wreath-product and postselection obstructions are unchanged.
An arbitrary Boolean oracle relabeled as a circuit is not an application.

## 2. A Costed Ordinary Hiding Oracle Without Monomial Expansion

Let delta be a fingerprint error budget and choose q=p^k with

```
q >= Delta * p^(2D^2) / delta,        k >= 1.
```

For Delta=0 use k=1. Construct an explicit extension field E=F_q and
choose ONE uniform point z in E^D, fixed for the complete algorithm.
Set `f_z(g)=C(g^-1 z)`, represented canonically as k base-field entries.
Polynomial orbits that are equal always have equal labels. For unequal
orbit polynomials, their difference is nonzero of degree at most Delta.
The Schwartz--Zippel bound and a union bound over fewer than
`|Gamma|^2 <= p^(2D^2)` pairs give

```
Pr_z[any false orbit collision] <= Delta*p^(2D^2)/q <= delta.
```

On the complementary event f_z hides EXACTLY H: with the action
`g.F(x)=F(g^-1 x)`, equality holds iff `g'^{-1}g in H`, equivalently
`gH=g'H`. This is a single global good event, not a per-query guarantee.
It remains valid for adaptive quantum queries because the same fixed z
separates the WHOLE orbit before those queries begin. Fresh z on each
query would not define this oracle. No efficient certificate that a
particular z is good is assumed.

Here k=O(D^2+(log(max(1,Delta))+log(1/delta))/log p+1).
A field element uses O(k log p) bits. Inverting a matrix, applying it to z
and evaluating C costs polynomial time in D,s,k,log p. Reversible
simulation retains g and uncomputes its workspace, leaving the canonical
field label. There is no coefficient table, orbit list, or inverse circuit
problem hidden in this evaluation cost.

Field construction is charged too. Sample monic degree-k polynomials,
test irreducibility by Frobenius powers and polynomial gcds, and retain
one that passes. For p>4 the success probability per trial is at least
1/(2k); O(k log(1/delta_field)) capped trials suffice. Factoring the
integer k by trial division costs polynomial time in k, not in p.
All accepted fields are verified; exhausting the cap is explicit failure.
This is standard finite-field construction, not new quantum machinery.

The proposed black-box input reduction in CLASS_FOUR_BLACK_BOX_INPUT.md
can then supply the receiver's coordinates from the matrix generators.
Its group-operation costs and error remain charged. CONDITIONAL on the
entire proposed receiver being correct, this gives quantum polynomial
time in the ORIGINAL circuit/matrix input and log(1/epsilon), with total
failure bounded by delta_field+delta+epsilon_receiver. It is a candidate
application corollary, not independent evidence that the receiver works.

The exact budget helper uses integer arithmetic and no group enumeration.
The finite tests use FLINT extension fields, including a 127-bit prime;
they do not execute the quantum reduction or construct a hard instance.

## 3. Stronger White-Box Classical Attack

High degree alone does NOT escape classical algorithms. The black-box
interpolation cost in NIL3_POLYNOMIAL_HIDING_ATTACK.md is not appropriate
when the complete circuit is public: the chain rule supplies a gradient
circuit with polynomial overhead, independent of the numeric degree.

**Sufficient regime.** For a supplied matrix p-group Gamma<=GL(D,p),
suppose `p>max(D,(D-1)*Delta)`. There is a randomized classical
polynomial-time stabilizer procedure in D,s,log p,log(1/epsilon).
The following is a local written derivation, not a claim of novelty or
an imported general-purpose polynomial-equivalence theorem. Class four
is unnecessary for this classical sufficient condition.

1. A matrix p-group in defining characteristic preserves a full flag,
   hence is simultaneously conjugate into UT_D(F_p). With p>D its
   nilpotency class is <p. Matrix log/exp truncate before degree D;
   denominators are invertible. Compute log of each supplied generator,
   close their F_p-span under matrix commutators, and obtain a basis
   A_1,...,A_d of log(Gamma), d<=D^2. Lazard subgroup correspondence
   proves that this is the whole log(Gamma). Only explicit matrix
   arithmetic is used; finding the triangularizing flag is unnecessary.
2. Define `R_j(x)=gradient(F)(x)^T A_j x`, each of degree <=Delta.
   A linear combination A belongs to the infinitesimal stabilizer iff
   its same combination of the R_j is the zero formal polynomial.
3. Learn those F_p-linear dependencies by evaluating all R_j at d fresh
   uniform points over an extension E with `|E|>=d*Delta/epsilon`.
   Expand E-valued equations into base-field coordinates. If the current
   kernel contains any false dependence, fix one for the proof. Its
   nonzero polynomial vanishes at a fresh point with probability at most
   Delta/|E|. Unless the kernel is already correct, each successful point
   increases rank. A union bound over d steps proves total error <=epsilon.
   Use D^2 instead of d in the field bound if desired. No coefficients
   are expanded, and log |E|, not |E|, is the field arithmetic parameter.
4. The remaining issue is FINITE versus infinitesimal symmetry. For
   A in log(Gamma), put `P_A(t,x)=F(exp(tA)x)`. Its t-degree is at most
   `(D-1)*Delta<p`. If exp(A) preserves F, all its p powers do; thus
   P_A(t,x)-F(x) has p roots and is identically zero. In particular
   `R_A=0`. Conversely, R_A=0 implies
   `d P_A/dt=R_A(exp(tA)x)=0`. Degree <p makes P_A constant, so exp(A)
   preserves F. Both directions use the strict degree bound.
5. Exponentiate a basis of the learned kernel to generate H. Closure
   follows either from the derivation commutator identity or from the
   equality with log(H) just proved. No quantum primitive is required.

Constants are immediate: H=Gamma. The bound is sufficient, not necessary.
The implementation currently checks its parameter guard; the proof and
symbolic controls do NOT constitute a production gradient/stabilizer
backend. A guard failure is missing baseline coverage, not hardness.

This attack also covers EXPONENTIALLY high degree when p is still larger
than (D-1)*Delta. Merely replacing a polynomial degree input by log degree
would therefore overstate the prospective quantum advantage.

## 4. Why Small Characteristic Does Not Automatically Rescue The Idea

For the linear shear `(x,y)->(x+t*y,y)` over F_p, take

```
F_plus  = x^p,
F_minus = x^p - x*y^(p-1).
```

`y*dF_plus/dx=0`, but no nonzero t preserves F_plus. Conversely,
`y*dF_minus/dx=-y^p !=0`, but EVERY t in F_p preserves F_minus.
Thus first derivatives can both overestimate and underestimate the finite
stabilizer when the degree guard is dropped. These are easy two-monomial,
abelian controls, not novel algorithms or hard benchmark families.

There is a further explicit dequantization filter. For r>=1, each of
`Phi(x)=(x_i^(p^r))_i` and `Phi(x)=(x_i^(p^r)-x_i)_i` commutes with
every matrix over F_p. The substitution map Q->Q(Phi(x)) is injective:
its leading monomials have distinct exponent vectors multiplied by p^r.
Consequently, for every supplied linear group Gamma,

```
Stab_Gamma(Q(Phi(x))) = Stab_Gamma(Q(x)).
```

If a compact Q and this factorization are exposed by the input construction,
remove the lift before any hardness claim. Low-degree Q may already fall
to the classical derivative attack or explicit representation algorithms.
This is not an efficient factorization theorem for arbitrary circuits.
It rejects the proposed way of MANUFACTURING difficult-looking families.

Also, x^p-x is zero on every base-field point without being the zero formal
polynomial. Testing only F_p inputs silently changes the problem to a
polynomial-FUNCTION stabilizer. The UT3 control shows that doing so merges
distinct formal orbit cosets; extension-field evaluation repairs this.

### Mixed Frobenius Levels Also Admit A Classical Filter

The single-map deflation above is not the only easy case. Suppose the
PUBLIC division-free circuit exposes gates meaning p-th power, with all
constants and ambient matrices over F_p. Count a Frobenius gate as
O(log p) ordinary multiplication gates, not a free operation. Let s be
the number of these exposed nodes, E the longest Frobenius depth, and
delta the syntactic degree obtained by assigning degree one to variables,
zero to constants, max at addition, sum at multiplication, and UNCHANGED
degree across a Frobenius gate. This is a computable bound, not a promise
that a mysterious high-degree polynomial has an accessible p-th root.

Introduce independent variables Y_(i,e), 1<=i<=D, 0<=e<=E. Push Frobenius
gates to the variables using addition/multiplication compatibility and
the fact that constants are in F_p. Memoize each (original node, level)
pair. This constructs an ordinary circuit Q with at most s(E+1) nodes,
total degree <=delta and

```
F(x) = Q((x_i^(p^e))_(i,e)).
```

The circuit is not expanded into monomials. Its ordinary degree may be
as large as delta*p^E, but its lifted circuit size remains polynomial.
Include a COMPLETE D-variable block at every level, even if Q mentions
only some of its variables: the matrix action can mix in the others.

**No-carry lemma.** If delta<p, specialization is injective on the space
of lifted polynomials of degree <=delta. A monomial has each exponent
alpha_(i,e)<p; its specialized exponent of x_i is sum_e alpha_(i,e)*p^e.
Uniqueness of base-p digits makes distinct monomials remain distinct.
This statement concerns formal polynomials, not their functions on F_p.

For g over F_p, Frobenius commutes with its linear action, and Q(gY)
still has degree <=delta. Consequently

```
Stab_Gamma(F) = Stab_diag(Gamma,...,Gamma)(Q),  if delta<p.
```

This covers genuinely mixed levels, not just F=Q(Phi(x)) for one common
Phi. It is a local elementary derivation using known Frobenius algebra;
no novelty claim or general circuit-factorization theorem is made.

**Classical stabilizer procedure.** Assume additionally
`p>max(D,(D-1)*delta)`. Compute a Lie basis A_j of the supplied matrix
p-group as in Section 3. The lifted infinitesimal equations are

```
R_j(Y) = sum_(e=0..E) gradient_(Y_e) Q(Y)^T * A_j * Y_e.
```

Use reverse differentiation of the public lifted circuit and independent
extension-field Y values to learn their F_p-linear kernel. There are
d<=D^2 unknown coefficients, not D^2*(E+1)^2: the SAME A acts in every
block. The d-step rank/PIT argument from Section 3 applies with degree
delta, and field size at least d*delta/epsilon. Field construction and
all D(E+1) input values remain charged. Constant Q needs no samples.

For A in that Lie algebra, Q((exp(tA)Y_e)_e) has t-degree at most
(D-1)*delta<p. The nilpotency index remains the ORIGINAL matrix dimension
D, not the number of lifted variables. Finite invariance and vanishing
lifted derivative are equivalent by the same p-root/degree argument.
Exponentiating the learned kernel recovers the finite H. The cost is
polynomial in the circuit/generator input, D, log p and log(1/epsilon),
even when delta itself and the original degree are exponentially large.
There is no dense tensor-representation or monomial expansion.

Do NOT differentiate through the Frobenius specialization to justify this
step. Its equivariance uses matrices over F_p; it does not commute with
the same matrix action at an indeterminate or extension-field parameter.
Apply the derivative argument to Q only AFTER proving the finite-group
stabilizer equality. This is precisely why the lift can recover finite
symmetries that the ordinary derivative of F misses.

**Sharp premise failures and scope.** At delta=p, the nonzero polynomial
`Y_(1,0)^p-Y_(1,1)` specializes to zero. A simultaneous shear in both
blocks does not preserve this lifted polynomial, while every shear
preserves its zero specialization. Thus lifting without the no-carry
guard can change the stabilizer. For matrices with coefficients outside
F_p, the level-e action instead uses Frobenius-twisted coefficients;
the identical-block algorithm here does NOT cover that input.

NEW `theorems/frobenius_circuit_lift.py` implements the topological DAG
transformation, degree bounds, reverse differentiation and attack guard.
It neither recognizes arbitrary semantic p-th powers in an unstructured
circuit nor implements the full matrix-group/PIT stabilizer backend.
Its guard explicitly leaves stabilizer_solver_executed false.

The exact nonabelian UT3 control uses
F=x^p*z+x*z^p-2*y*y^p. The lifted gradient recovers log symmetries
a=2b,c=0; the raw derivative misses the nontrivial symmetry
2E12+E23. Exhaustive finite group comparison checks the actual equality,
not only consistency of returned constraints. A shared-DAG control uses
a 127-bit prime, 40 Frobenius levels and lifted degree 2^50, without
coefficient expansion; a 1500-level chain checks iterative traversal.
These are baseline/counterexample controls, NOT proposed hard families.

This removes another way of manufacturing apparent hardness by mixing
large p-power exponents. Failing the guard, hiding the gate structure,
or lacking an implemented backend is not evidence of quantum advantage.

## 5. Literature Checks And Limits

[Dvir, Oliveira, Shpilka, Theorems 1.5--1.6](https://arxiv.org/pdf/1401.3714)
give shift-equivalence algorithms with polynomial dependence on degree
and characteristic zero or larger than degree. Their abstract's succinct
representation language must not be read as a general poly(log degree)
result. The current action is linear and nonabelian, so their theorem is
neither a direct solver nor a hardness statement here. Its PIT sampling
lemma also supplies the standard fingerprint bound above.

[Baraskar et al., TR24-104](https://eccc.weizmann.ac.il/report/2024/104/)
concerns finding a transformation to a sparse or constant-support
polynomial. That orbit-optimization hardness does not imply hardness
of a single polynomial's stabilizer inside a supplied p-group.

The explicit linear-action Luks filter in CLASS_THREE_APPLICATION_AUDIT.md
applies if the induced polynomial representation can actually be written
in polynomial dimension. Its dimension generally grows with degree and
the number of variables; a small arithmetic circuit does not provide that
representation for free. On the other hand, compact Frobenius deflation
or a polynomial-dimensional invariant representation may restore it.

The new orbit-module filter MAKES THE LATTER TEST CONSTRUCTIVE when a
public rank cap is supplied. It uses at most 1+rR candidate translates,
base-field coordinate solving and fresh identity tests. A small orbit
module is discovered without prior monomial or representation advice;
the faithful block prevents loss of the action kernel. Exceeding the cap
only certifies R+1 independent translates. The simple x0^(p-1) control
has large rank but an immediate factorization-based stabilizer, so this
failure must not be promoted to hardness. General closure is Monte Carlo;
the Moore controls also have an independent exact exterior-power check.

The targeted search did not establish a solver for ALL remaining succinct
circuits, nor a complexity lower bound. Unlocated prior work is still a
novelty risk. Known abelian HSP already handles abelian ambient groups;
known fixed-small-prime regimes also cannot justify a new growing-prime
nonabelian claim.

## 6. Decision And Falsifiers

The reduction is concrete and costed, but the impact case is NOT yet made.
A plausible surviving regime needs growing nonabelian groups, large p,
Delta comparable to p/(D-1) or larger, and a succinct circuit whose
stabilizer is not exposed by its construction. Mixed Frobenius levels
with low lifted degree now fall to the additional classical filter above,
even when the ordinary-degree guard fails. That describes missing
coverage, not a known natural hard problem or quantum advantage.
Low-rank orbit families now also fall to the new classical route even
when BOTH derivative guards fail. Neither high degree nor a failed
rank cap is sufficient evidence for an application.

Before any campaign or candidate promotion, require an independently
motivated family and attack it using the PUBLIC circuit. Kill it if a
compact equivariant deflation, invariant representation, coefficient
reconstruction or another classical symmetry algorithm recovers H in
polynomial time. Reject hidden-H-generated invariant circuits as hardness
evidence until their generation and white-box leakage are audited.

Next research decision: seek such a family or a stronger general classical
attack, while independently reviewing the complete HSP theorem. Do not
turn this open input regime into another synthetic oracle benchmark or
claim a solution of graph/code equivalence, lattice problems or factoring.
