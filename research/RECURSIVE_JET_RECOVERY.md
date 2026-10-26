# Arbitrary-Subgroup Recovery From The Jet Image Procedure

2026-10-22. **Provisional whole-algorithm composition in a precise input
model. Not an independently reviewed theorem, a synthesized receiver,
an application-level speedup, or a candidate admission.**

## 1. The Actual Claim Under Review

Fix a constant c. Input: a genuine n-dimensional Lie algebra L over a
known prime field F_p, p>c, with public structure constants and nilpotency
class at most c; and coherent ordinary function access to f on exp(L),
in the supplied logarithmic coordinates. Its b-bit labels obey
f(x)=f(y) iff x^-1*y is in an arbitrary unknown subgroup H. Output a basis
of log(H), equivalently at most n group generators, with error at most
epsilon. The zero-dimensional case returns the trivial subgroup directly.

**Provisional theorem claim:** the nonabelian jet homogenization and mixed
descent lemmas, composed as below with the published fixed-degree SDE
algorithm, give time polynomial in n, log(p), b and log(1/epsilon), for
each fixed c. No assumption N''=0 is needed. The polynomial degree depends
very badly on c. This is exponent-p explicit Lazard input, NOT arbitrary
nilpotent black-box groups, prime-power exponent, growing class, or state-
only input. The case c=1 is ordinary abelian HSP, including p=2.

The proof is provisional because its new nonabelian polynomial lift and
whole physical refinement have not received independent review. Passing
the tests below does not prove this theorem. This note makes the entire
claim and its remaining failure points inspectable instead of leaving an
undefined image oracle in an alleged algorithm.

## 2. The Image Procedure Is Constructive, Not Hidden Advice

For a public ambient S with h=log(H) transverse to S', construct its
ACTUAL lower-central adapted normal basis. Write m=dim(S/S') and w_i for
the normal coordinate weights. The following dependencies have written
proofs and separate exact controls in this repository:

1. AMBIENT_SECTION_POTENTIAL.md bounds the unknown section potential's
   coordinate degrees by w_i. It is a proof witness, never evaluated.
2. NONABELIAN_JET_HOMOGENIZATION.md constructs the public polynomial-map
   group J and K=J semidirect F_p^m. The graph subgroup H_F is transverse
   to J and preserved by all public nonzero dilations.
3. JET_ORACLE_HOMOGENIZATION.md constructs an ordered tuple of original
   hiding-function queries on a deterministic simplex. Injective
   evaluation makes this an ordinary hiding oracle for H_F. Its cost is
   ell=binom(m+k,m+1) original current-ambient queries for class k.
4. CENTRAL_CHARACTER_DESCENT.md removes each top grade using full central
   Fourier instruments, public label SDE cancellation, controlled right
   multiplication and fresh copies. Every ideal label tuple has the same
   correct quotient output. At grade one, abelian Fourier recovery gives
   the subgroup image; its projection to the ORIGINAL V is U=pi(h).

There is no metabelian restriction on J or S'. No polynomial potential,
hidden basis, chosen coset, or correct image U is supplied operationally.
The general SDE algorithm is a published computational dependency. The
current executable callbacks and capped exhaustive tests do not implement it.

## 3. Arbitrary H: Correctness And Strict Termination

Use the Lazard subgroup/subalgebra correspondence for class below p.
The following algorithm operates on a public Lie algebra S and an
inherited ordinary hiding oracle. All returned generators are Lie-closed.

```
Solve(S, inherited_f):
    if S=0: return empty basis
    if S is abelian: return AbelianHSP(S, inherited_f)
    N = [S,S]
    K0 = Solve(N, inherited_f restricted to N)
    M = {x in S : [x,K0] subset K0}
    Q = M/K0
    f_Q = inherited_f composed with a public section Q -> M
    while Q is nonabelian:
        U = the image procedure of Section 2 on (Q,f_Q)
        Q = the inverse image of U in Q/Q'
        restrict f_Q to this Q and rebuild its actual filtration
    B = AbelianHSP(Q,f_Q)
    return LieClosure(K0, public lifts of B)
```

On a correct history K0=h intersect S'. Since S' is an ideal, K0 is an
ideal of h, so h is contained in its public Lie normalizer M. K0 is an
ideal of M by construction. The hidden quotient algebra h/K0 is transverse
to Q'=(M'+K0)/K0: a hidden representative in M'+K0 lies in h intersect S',
and therefore in K0. DO NOT assume S' is contained in M. Computing M is
linear algebra in the public bracket tensor, with a basis of learned K0.

These Lie normalizers also agree with group normalizers. Conjugation by
exp(x) acts as exp(ad x). Stability under ad x implies stability under
its exponential; conversely stability under exp(ad x) and its inverse
implies stability under its finite logarithm ad x. All denominators are
invertible because p>c. No unknown normalizer is an extra oracle.

After an exact image call, the next ambient is T=h+Q'. Transversality
makes h abelian, since [h,h] lies in h intersect Q'. Thus
[T,T] is contained in gamma_3(Q), and by induction
gamma_j(T) is contained in gamma_(j+1)(Q) for j>=2. Every nonabelian image
step strictly drops class. Also T' is contained in Q', so h stays
transverse. At the final abelian ambient, ordinary abelian HSP recovers
all of the remaining h, not only its earlier quotient image. Lifting it
and adjoining K0 recovers the original hidden algebra.

The only recursive Solve call is on S', whose class is at most floor(k/2)
when S has class k: gamma_j(S') is contained in gamma_(2j)(S). Let I(c)
and A(c) bound image and abelian-base calls. Then

```
I(0)=A(0)=0, I(1)=0, A(1)=1,
I(c) <= I(floor(c/2)) + c-1,
A(c) <= A(floor(c/2)) + 1,
I(c)+A(c) <= 2*c - popcount(c) < 2*c.
```

These are upper bounds, not exact call counts for each subgroup. Empty
quotients and faster class drops only reduce them. Explicit class-drop,
ambient-membership and Lie-closure guards enforce finite control flow
also on wrong histories. They do NOT certify that an image answer is right.

## 4. Ordinary Oracle Access Survives Quotients

Let pi:M->Q be the quotient homomorphism with kernel K0 contained in H.
For ANY public right inverse sigma, even when it is not a homomorphism,

```
f(sigma(q)) = f(sigma(r)) iff q^-1*r in pi(H).
```

Indeed pi(x) in pi(H) iff x in H whenever ker(pi) is contained in H.
Changing sigma changes a representative by a hidden-kernel element and
does not change its label. A public linear section of the quotient Lie
space supplies sigma in logarithmic coordinates. Restrictions are just
inclusions. Nested sections compose; their linear matrices can be
flattened, without querying any oracle or preserving a hidden potential.

For a coherent call, compute sigma(q) in a zeroed workspace, query the
ORIGINAL f into the label register, and uncompute sigma(q). This uses
one original f call, not its inverse. The labels remain. All nested
sections are public arithmetic around that same query. Hence query costs
ADD across Solve calls, rather than recursively multiplying by old budgets.

Cleanup is necessary. If the injective representative workspace is traced
out instead, the label-source kernel is additionally multiplied by
[sigma(q)=sigma(r)]=[q=r]. The state becomes I/|Q| for EVERY H; all subgroup
coherence is lost. If K0 is not contained in H, even the quotient labels
can depend on the chosen representative. Both failures have explicit tests.

Formal/RecursiveOracleReduction.lean proves quotient hiding, section-label
independence, composition and kernel containment, an actual reversible
compute/query/uncompute basis identity, and the workspace-leak identity.
It does not formalize the entire Lie recursion or synthesize gates.

## 5. Whole-Algorithm Resources, Including Failure Histories

Every ORIGINAL recursion ambient has dimension at most n. Jet groups are
internal image workspaces and are never passed recursively to Solve.
Use these deliberately loose public envelopes for all correct histories:

```
ell <= binom(n+c,c-1),
r_d <= n*binom(n+c-d,c-d),
D_final <= n+r_1,
B_d = (d^(d(d-1)/2) * (r_d+1)^d)^ceil(log2(d+1)),
P = product_(d=2..c) B_d.
```

The B_d bound comes from the fixed-degree diagonal-equation construction
of [Ivanyos and Santha, Theorem 11 and Section 3.3](https://arxiv.org/pdf/1503.09016).
Section 3 reduces degrees not dividing p-1 to gcd(d,p-1). The original
larger degree's arity is a conservative bound. This does not assert a
polynomial algorithm when c grows with the input.

Let R=2c-popcount(c), t=ceil(log_p(3R/epsilon)), S=D_final+t and S0=n+t.
Taking S samples covers every image Fourier reconstruction, and S0 every
abelian base. A hyperplane union bound gives total rank failure at most
R/((p-1)*p^t) <= epsilon/3. A sufficient original query bound is

```
Q_original <= I(c) * S * P * ell + A(c) * S0.
```

The standalone certificate counts every SDE node and source preparation
in all these trees. Allocate solver abort probability epsilon/(3*N_SDE)
per node, and half-diamond error epsilon/(3*N_instruments) per COMPLETE
instrument, including records and abort flags. The resulting global error
bound is at most epsilon. On the first erroneous image/base answer, its
correct-history promise still holds; union-bound those first errors. No
correctness guarantee is asserted for later calls on an incorrect history.
Cap all solver/controller runtimes and verify every SDE witness.

At fixed c, multiplication, BCH precomputation, public charts, polynomial
evaluation, linear algebra, published SDE and approximate prime Fourier
transforms have polynomial bit/gate cost at the required global precision.
This is an asymptotic argument, not an elementary-gate count. Oracle label
width b and all temporary registers must be charged. Even storing the
whole polynomial-sized tree gives a polynomial space bound at fixed c;
this does not make the bound practical.

For constant target error the conservative query dimension exponent is
E_c+2c-1, E_c=sum_(d=2..c) d*ceil(log2(d+1))*(c-d+1).
At c9 this is 473. The n19 whole-recovery envelope has query ceil-log2
2922 at both example primes, versus the earlier SINGLE-IMAGE 1763 bound.
These are different upper bounds, not a regression, speedup measurement,
or evidence of feasibility. The astronomical bound remains a limitation.

## 6. Falsifiers, Baselines And Remaining Review

The new tests cover actual proper NONABELIAN hidden subgroups in UT5 at
p7 and a127-bit prime, and a full-hidden-subgroup case in UT9 where the
derived algebra is not metabelian. These use explicitly KNOWN-H reference
callbacks to check recursion only. Another test deliberately supplies the
wrong zero image: all public guards pass and the old controller returns
SUCCESS with the wrong subgroup. Its status is not a correctness proof.

No quantum advantage is inferred from the dense controls. Full-table
classical simulation costs exponentially many group entries. For actual
applications, low-degree reconstruction, public action stabilizers, and
the small-orbit-module classical reduction remain mandatory filters;
see POLYNOMIAL_ORBIT_MODULE_CLASSICAL_FILTER.md. A public function circuit
can be classically easy even if its abstract hiding-oracle problem has
a useful quantum algorithm. No surviving hard application is supplied here.

Central descent and normalizer recovery are prior art; see
[Imran--Ivanyos](https://arxiv.org/pdf/2304.08376). A fresh check of
[Morales v2, introduction and Appendix A.3](https://arxiv.org/pdf/2608.05321)
still distinguishes unrestricted-prime class-two results from the
bounded-prime constant-class result, and treats quasi-Hamiltonian and
restricted scalar-action families. This is evidence about stated scopes,
NOT a comprehensive novelty certificate. The possible new contribution
is the nonabelian homogenization plus its uniform-large-prime composition
in the explicit input model, if correct and not already known.

Most likely ways to falsify the full claim: a counterexample to the
universal ambient degree/tuple-hiding lemma; incorrect preservation under
a quotient; a nonpolynomial public control hidden in the fixed-class
accounting; or prior work already giving this composition. The current
controls address local instances, not universal completeness. Independent
whole-proof review and a meaningful application take priority over more
small verifier modules or a physical receiver demonstration.

## Verification

159 connected Python tests pass in56.72s, including13 new tests and the
reused Milestone23 controls; RuntimeWarning was fatal. Full cached
`lake build --wfail` passes3472 jobs and all three new axiom guards.
Python syntax, generated formal crosscheck, `qsearch.py validate`, site
JavaScript/site checks, whitespace and the live artifact workflow pass.
The full Python suite was not run. No CLI/UI/admission or Git actions.
