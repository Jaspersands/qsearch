# CSA minimal module: independent integrated review

2026-11-07. CLOSED. Reviewed the updated complete
`research/CSA_MINIMAL_MODULE.md`, including the relative discriminant,
maximal-order certificate, transcript-relative canonicity and adaptive-pivot
repairs. No implementation or controls were run for this review.

**Disposition:** the written composition establishes the stated conditional
quantum polynomial BIT construction under its field/CSA input promises and
the explicit GRH/source assumptions imported for the known complete S-unit
and KM split-algebra algorithms. I found no remaining mathematical or compact
resource blocker. The deterministic positive certificate is sound independently
of GRH under those input promises. This does not establish priority, a classical
lower bound, an expanded-output bound, practical complexity or quantum execution.

## 1. The index is paid and separately certified

Actual Voight Theorem7.2 covers a general semisimple algebra with integer and
finite-field polynomial factoring oracles. Apply it over Q to the restriction
of scalars of A, of dimension m*n^2. This removes a possible fixed-number-field
reading and never assumes a free O_K-basis of the maximal order. A maximal
Z-order contains central O_K: adjoining central integral elements produces an
overorder. The initial trace-dual bound gives polynomial bit height for HNF
representatives of every intervening overorder. Finite-field factoring remains
a randomized polynomial operation with checked outputs and finite clocks.

Nebe--Steel §§3.1--3.2 use the RELATIVE REDUCED-trace discriminant. Its local
exponent is e_q=n*(n-n/d_q). The ordinary rational regular-trace discriminant
is suitable for support but cannot replace this ideal in that formula.
The note's implementation without a relative free basis is valid: construct
Lambda* by rational lattice preimages enforcing that every relative reduced
trace has integral O_K coordinates. For M0=Lambda*/Lambda and q above p,
E=v_p(|M0|) bounds the q-primary module's nilpotence length. Hence

    Lambda*/(Lambda+q^E Lambda*) = M0/q^E M0

is exactly the q-primary part. Its size is Norm(q)^e_q. At any different prime
q' above p, q acts invertibly, so that component is killed in this quotient.
E is at most the bit length of |M0|; the powers and HNF computations are
polynomial-size. This handles split rational primes without confusing their
different local indices. Real trace signatures and the lcm of all local
indices then determine the global index exactly.

The added deterministic maximal-order certificate is sufficient. At each q
above the completely factored initial absolute trace discriminant, a nilpotent
two-sided ideal Jbar with semisimple quotient is the exact radical. The displayed
separability-element equations certify semisimplicity: averaging a vector-space
projection P by sum x_i*P(y_i v) makes it a module projection. Finite-field
semisimple algebras are separable, so this linear certificate exists. A field
center, checked by a full-degree irreducible generating polynomial, makes that
semisimple quotient simple. For the preimage J, the exact lattice calculation
O_r(J)=Lambda invokes Nebe--Steel Theorem3.7 to give hereditaryness; its local
block description and Lemma3.10 then give maximality because the radical
quotient has one simple block. Outside the initial discriminant, trace duality
already precludes an overorder. All these are expanded lattice/finite-algebra
computations of polynomial dimension; they do not compute a minimal left ideal.

This certificate is ESSENTIAL, not decorative. A degree-a splitting field with
a a larger multiple of the true index also passes the later Hom and affine-rank
arguments, yielding an idempotent with left ideal dimension n*a. It need not be
primitive. Therefore the later modular ranks cannot certify d by themselves.
The updated note no longer makes that inference.

## 2. The prescribed splitting field has polynomial expanded size

For d>1, the finite places include those above 2 and hence form a nonempty set.
Uniform monic irreducible degree-d sampling has probability at least 1/(2d):
the union of proper subfields has at most sum_(j<=d/2) Q^j <= Q^d/2 elements.
Verified capped trials pay this uniformly, including Q=2 and d=2,3.

The CRT coefficients N_i have polynomial bit height. With M=Norm(I),
T=1+M*2^s is 1 modulo every selected prime and can be chosen >=4dU using
polynomially many bits. Thus the polynomial P has its prescribed irreducible
reductions. At each real nonsplit place d is even, and the total perturbation
of X^d+1 is bounded by (1/4)*max(1,|x|^d), proving that P has no real roots.
At every finite ramified place the extension has local degree d, divisible by
the local index. These conditions imply splitting by the stated local criterion.
No local invariant numerator, normal closure, cyclicity or computed embedding
of F in A is supplied for free.

The absolute degree is m*d <= m*n. Primitive-element conversion, residue maps,
and maximal orders of the NEW fields are charged expanded computations with
factoring. The construction of a splitting field does not itself construct the
split map A tensor F -> M_n(F); the latter is precisely the remaining published
KM quantum arithmetic task.

## 3. Compact KM access and the exact extraction ranks

The known compact interface is used in its audited form: an expanded Amitsur
presentation and cocycle; complete compact S-unit generators retaining torsion;
expanded small mapped atoms; LS's full integral relation lattice; and an integer
HNF preimage for the cochain. This invokes neither LS on compact sums nor a
generic additive circuit identity oracle. The largest etale tensor dimension
is m*d*n^3 <= m*n^4. The canonical representation is reconstructed from the
checked transcript, rather than accepted as an arbitrary circuit assertion.

Write A=M_r(D), deg(D)=d, n=r*d. A simple left module has K-dimension r*d^2=n*d.
Thus V=F^n, of exactly this dimension, is simple. With R=m*n^2 and N=m*n*d,
the equations L_b f=f R_b for a FULL Q-basis of A, including the center, have
kernel dimension N in R*N unknowns. More generally dim_Q Hom_A(W,A)=dim_Q W
for any finite A-module W, so the required upper rank R*N-N follows from the
certified representation without depending on a sampled rank or minimality.
A certified nonzero minor of that size therefore gives an exact Cramer kernel
basis satisfying every row of the system.

An injective V->A exists. On a grid of size 4N, a fixed nonzero N-minor of a
linear combination of kernel maps is a polynomial of degree at most N, giving
success probability at least 3/4. A fresh modular nonzero N-minor certifies
injectivity and the image left ideal L. This step could be simplified for a
simple V, but the written random method and its clock are valid.

The right-identity equations l_j e=l_j with e in L are consistent because every
left ideal of a semisimple algebra is generated by an idempotent. If
dim_K L=n*a, a conceptual conjugation to the first t-column ideal in M_r(D0),
where a=t*deg(D0), shows that right multiplication by an element of L depends
exactly on its t-by-t upper block. Its Q-rank is m*a^2. In the selected minimal
case this is m*d^2. That conjugation is a proof, not computed advice. A certified
minor of this rank, the proved upper bound and consistency justify a canonical
Cramer affine solution with the nonpivot unknowns zero. Consequently e^2=e,
Ae=L, and the independently certified d makes e primitive.

The N image columns form a Q-basis. Choosing a Q-basis (omega_a) of K with
omega_1=1 and using omega_a*theta^t*e_i as the Q-basis of V makes the n*d
columns indexed by a=1 a K-basis of L. The remaining columns are their known
K-multiples by A-linearity. The given action on V transfers to this K-basis.
The split, division and n=m=1 cases are covered; the rank-zero Hom system uses
the empty determinant 1 and its full coordinate kernel.

## 4. Self-contained compact stage and prime clock

Flatten every known field operation into rational scalar arithmetic. Use DAG
sharing, binary powering, and a division-free determinant construction. Pad a
polynomial node budget T to include ALL rational leaves, output slots, matrix
entries, and a determinant circuit for ANY candidate maximal minor of the
current dimensions. Let H bound the leaf bit lengths. Addition, subtraction,
multiplication and reciprocal gates give an unreduced numerator/denominator
bit bound

    B = 2^(T+2)*(H+1).

A reciprocal swaps the numerator and denominator, so introduces no larger
recurrence. It is only permitted where an upstream exact certificate/theorem
has proved its rational argument nonzero. All denominator failures, including
numerators of formerly inverted nodes, are rejected during modular evaluation.
The expanded value can be enormous; only log B is polynomial and only this is
used in the modular sampling analysis.

Fix the current matrix BEFORE its prime, and fix for analysis any one existing
nonzero maximal minor. At most (T+1)*B primes divide its numerator or any input
denominator. For a per-stage failure budget delta choose

    b = 2*(T + ceil(log2(H+1)) + ceil(log2(T+1))
           + ceil(log2(1/delta)) + 32).

The retained explicit dyadic prime bound, pi(2X)-pi(X) > 3X/(5 log X), applies
at X=2^(b-1). Substitution bounds the bad-prime fraction below delta. Sampling
uniform b-bit integers and testing primality deterministically gives a uniform
prime conditional on success; O(b*log(1/delta_gen)) capped trials suffice for
generation error delta_gen. Each modular operation has polynomial bit cost.

Gaussian elimination may choose the pivot minor AFTER seeing this prime.
This is sound: a modular nonzero determinant is an unconditional exact nonzero
certificate over Q. The probability proof uses the pre-existing analysis-fixed
minor, not independence of the adaptively selected one, and does not enumerate
all minors. If that fixed minor survives, the modular rank reaches the proved
target. A good prime cannot exceed the rational upper rank. At the next stage,
condition on all earlier choices, freeze its new matrix and select a FRESH prime.
The uniform circuit budget applies to every such transcript.

The compact affine stage needs no new equality-testing promise: the theorem
already proves its augmented rank equals its coefficient rank. Exact lower
minors plus that upper rank and consistency make the selected rows sufficient.
The verifier rebuilds the prescribed circuits from the transcript and checks
these minors; it does not accept arbitrary alleged equal circuits. This is
transcript-relative canonicity, not an input-canonical normal form or a
lexicographically first nonzero-minor algorithm.

There are polynomially many source calls, field factors, sampling attempts and
rank stages. The note's five error buckets can be subdivided among these calls.
Capped independent retries make exhaustion probability at most eta while
retaining polynomial dependence on log(1/eta). Invalid factorization, a zero
modular denominator, insufficient rank or a finite-clock failure causes ABORT.
No erroneous cochain passes the exact LS certificate merely because the source
failed to produce a complete generating set.

## 5. Scope and remaining nonclaims

The factoring-conditioned classical index algorithm is already published. The
quantum upper bound composes known arithmetic primitives with the explicit
splitting-field and compact module extraction arguments. A supplied split
representation, as used in a finite control, is not the native input. The
reported PARI general-table algindex UNSUPPORTED result is a backend receipt,
not a mathematical barrier. The verified control and Claude reports are not
inputs to this proof's validity.

No expanded-size primitive idempotent, integral element, division-algebra
normal form, generic compact equality algorithm, unique canonical output,
recognition of malformed field/CSA inputs, novelty, or unmatched classical
complexity is established. A complete classical prior-art comparison remains
open. No further proof repair is required for the exact conditional contract
reviewed here.
