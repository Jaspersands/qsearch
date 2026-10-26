# A Complete Written Composition For The Induced HSP Receiver

2026-10-22. PROVISIONAL THEOREM, UNDER REVIEW. This joins the ordinary
hiding oracle, public induced-phase compiler, two erasure stages and
arbitrary-subgroup recursion into one procedure. It does not report an
executed quantum algorithm, independent verification, novelty or a useful
external speedup. The intended advance is a precise theorem that can be
refuted, rather than another collection of compatible-looking interfaces.

The audit found an omitted formal interface: diagonal solvers guarantee
a nonzero vector, while the existing weighted channel theorem assumed
every scale nonzero. The new active-support theorem and partial-trace
lemma close that interface. A separate exact counterexample shows that
correct marginal sources and correct branch probabilities do NOT suffice
without conditional tensor independence. No new obstruction to the
written composition was found; the implementation remains incomplete.

## 1. Provisional Statement

Fix c and k with 2<=k<=floor(c/2). Given an n-dimensional Lie algebra
L/F_p in public structure constants, with class(L)<=c, N=L' metabelian,
class(N)<=k and prime p>kc, let G=exp(L) with its explicit BCH encoding.
An ordinary coherent oracle computes an opaque label f(g), with

```
f(g)=f(g')  iff  g^-1 g' belongs to H,
```

for an arbitrary subgroup H<=G. These are LEFT cosets gH. Assume fixed
length output labels of length ell_f and reversible oracle access.

The candidate theorem is a bounded-error quantum algorithm returning
generators of H in time polynomial in n, log(p), ell_f and log(1/epsilon),
apart from the charged oracle cost. Polynomial exponents depend on c,k.
It uses the published uniform fixed-degree diagonal solver, ordinary
abelian HSP/QFT algorithms and explicit reversible finite-field algebra.
It does not assume a hidden-potential evaluator or an image oracle.

The assertion concerns fixed-class, prime-exponent, explicitly encoded
groups. It says nothing about growing class, arbitrary black-box input,
prime-power exponent, DCP, lattice problems or general graph isomorphism.
Polynomial query separation for opaque labels is not itself a new
application. The existing sufficient bounds are impractical.

## 2. Public Data Versus Proof Witnesses

The controller knows the Lie brackets, public bases, field, chosen
sections, measurement records, coefficient tables and error budget.
Within one transverse image call it creates formal variables for ALL
coefficients of a degree-D polynomial Q:V->N, with D=c. The same formal
basis is used at every leaf and every merge of that call. Tables describe
polynomials in these variables; they are not estimates of their values.

The witnesses U, Q, a retraction onto U and a hidden-subgroup lift below
are used only to prove the distribution of the controller's outputs.
They are never supplied to a gate, solver, rank test or stopping rule.
Separate recursive calls have separate formal bases. Matching dimensions
alone never authorizes merging states from distinct calls or instances.

The algebraic identities used here are proved in the companion source,
universal-cocycle, full-Taylor and resource notes. Their Lean coverage is
local, not a single verified implementation of this procedure.

## 3. One Transverse Image Call

First suppose H intersects exp(N) trivially. Write V=L/N and m=dim(V).
H is abelian because its commutators lie in H intersect exp(N). Under
the prime-field Lazard correspondence, log(H) is an abelian subalgebra,
and its projection U<=V is injective. Let s:V->L be any public linear
section. For the proof only, write the inverse lift as s(u)+a(u), with
a:U->N linear, and choose a linear retraction pi:V->U.

Put h(u)=exp(s(u)+a(u)) and

```
g(q) = exp(s(q-pi(q))) h(pi(q)) exp(-s(q)) in exp(N),
Q(q) = log(g(q)).
```

The three exponents are linear in q. Truncated BCH therefore gives
degree(Q)<=c, even though its coefficients are unknown. Since H is
abelian, h is additive. For q'-q=u in U,

```
g(q') exp(s(q')) = g(q) exp(s(q)) h(u).
```

In public coordinates n exp(s(q)), coset membership is consequently
q'-q in U and n'=n g(q)^-1 g(q'). This derives the common potential
from the ORIGINAL oracle relation, not from a desired state ansatz.

### 3.1 Obtain The Matrix Source

If N is abelian, use the scalar branch in Section 4. Otherwise choose
I=N', an abelian ideal, and a public linear section s_A of A=N/I.
Write n=r(x)exp(i), where r(x)=exp(s_A(x)). This is the right-fiber
coordinate order, not exp(i)r(x), and the section need not be a homomorphism.

Prepare uniform G, call f, and trace its label register. Invert the normal
coordinate, compute the right-fiber chart, Fourier transform I with the
positive sign, and measure lambda in I*. Retain EVERY lambda including 0.
The source proofs give its probability 1/|I| and normalized kernel

```
rho_lambda[(q,x),(q',x')] =
  (|V||A|)^-1 [q'-q in U]
  (W_lambda(g(q))^dagger W_lambda(g(q')))[x,x'],

W_lambda(g)|x> = omega^(lambda.kappa(g,x)) |x+pr_A(log(g))>,
kappa(g,x) = log(r(pr_A(log(g))+x)^-1 g r(x)).
```

This kernel is derived by contracting the actual oracle's two normal
indices. It does not grant coherent access to g. Every lambda block is
normalized, including blocks that carry little or no phase information.

### 3.2 Align The Full Taylor Jet

Use B fresh matrix sources, fresh nonzero public scales s_i and a fresh
uniform q register. Subtract s_i*q from each old quotient register and
measure its value Y_i. At fixed past record, labels and scales, the
complete Y tuple has probability |V|^-B. No outcome is selected for
containing a favorable hidden value.

The public scalar feature rows are the coefficients of the nonconstant
Taylor expansion at Y_i+s_i*q. After dividing by s_i they are the distinct
monomials in (s_i,Y_i) through degree D-1. There are
ell=binom(m+D,m+1) features. Full row span permits a public GL transform
on the B copies of A that converts their displacement to

```
constant offset + (F(q), 0),
```

where F is the complete Taylor coefficient jet of the A part of Q and
has width J=dim(A)*ell. This equality holds coefficientwise for every Q;
the GL computation uses feature rows, not coefficients of Q.

Measure the complementary coordinates zeta in the computational basis
and retain every outcome. Their probability is 1/|spectator space|.
The retained normalized kernel is

```
sigma_P[(q,t),(q',t')] = (|V| p^J)^-1
  [q'-q in U] [t+F(q)=t'+F(q')]
  omega^(P(q,t)-P(q',t')).
```

The public symbolic compiler obtains

```
P(q,t) = -sum_i lambda_i.kappa(Q(Y_i+s_i*q), L^-1(t,zeta)_i).
```

Only the expression is computed. Unknown Q is substituted FORMALLY.
The universal cocycle has degree <=k in its Q and carrier arguments.
The closed commuting-adjoint formula and its specialization proof justify
the compiler for arbitrary admissible N, not just the tested filiform N.
Assign q weight 1 and each Taylor coordinate its scale weight. Then
weight(P)<=kD. Parameter monomials are shared across the entire call.
The sharper support envelope in INDUCED_END_TO_END_RESOURCE_AUDIT.md is
preserved by this construction and all subsequent pullbacks.

If feature rank fails, discard the whole batch and retry using fresh
queries. Use bounded retries and report ABORT on exhaustion. The capped
schedule and p>kD>=2D give the existing conditional rank bound; never
replace it by empirical rank frequency.

The later AMBIENT_FILTERED_INDUCED_RECEIVER.md gives a guarded refinement
of Sections3.2--3.4: actual ambient adapted coordinates yield individual
degree bounds w_i; heterogeneous full jets preserve component filtration;
the weighted phase bound becomes c rather than kD. It keeps the same
source and complete-instrument normalization. The uniform-degree path
below remains a valid conservative formulation; its integer parameters
must not be reduced without that new coordinate/transport proof.

### 3.3 Erase The Weighted Phase

For d=kD,...,1, obtain the scheduled number of disjoint children whose
phases have weight <=d. Expand every weight-d coefficient over the SAME
formal parameter-monomial basis. Apply the fixed-degree diagonal solver
to the PUBLIC coefficient columns to obtain t_i, not all zero, with

```
sum_i t_i^d c_(i,alpha,nu) = 0    for every leading alpha and nu.
```

Choose this witness BEFORE the new measurements. The leading Taylor
action is t_i^d, independent of those new outcomes. A solver that guesses
hidden parameter values or uses not-yet-obtained outcomes is not this
algorithm. Verify the returned public relation; verification does not
replace the solver's all-input termination guarantee.

Let S={i:t_i!=0}. Trace out all other inputs; their freshly prepared
states are consumed, not recycled. S is nonempty. The diagonal relation
restricts to S because d>0. On the retained tensor prepare fresh uniform
(q,t), subtract t_i*q from the old quotient registers and measure Y_i;
then subtract A(Y_i,t_i)*t from the old jet registers and measure Z_i.
Here A is the PUBLIC full-Taylor transport. These are reversible shears;
no operation evaluates F or Q. Invertibility of A for t_i!=0 supplies
the support implication in the proof.

For every outcome o, the unnormalized branch equals

```
(|V| p^J)^(-|S|) sigma_R,
R(q,t) = sum_(i in S) P_i(Y_i+t_i*q, Z_i+A(Y_i,t_i)*t).
```

The exact Taylor coefficient matrix is weight triangular with diagonal
t_i^weight, so the public relations imply weight(R)<d. The branch has
the stated mass, independent of the hidden coefficients. In particular,
the exponent is |S|, not the allocated solver arity. The new Lean
active_degree_reduced_branch covers arbitrary nonzero vectors by using
the active subtype. The accompanying trace lemma justifies its input
after discarding normalized independent factors.

After d=1, R is constant and its phase cancels in the density matrix.
This is removal of the scalar phase, NOT removal of the nonlinear curve.

### 3.4 Read And Erase The Remaining Curve Phase

Fourier transform the ENTIRE retained jet with the negative sign and
measure eta. Every eta is kept and has probability p^-J. The quotient
state has kernel

```
rho_(U,P_eta)[q,q'] = |V|^-1 [q'-q in U]
  omega^(P_eta(q)-P_eta(q')),
P_eta(q) = eta.F(q).
```

This phase has ordinary degree <=D and is linear in the original
A-potential coefficients. Run ordinary affine erasure at degrees D,...,1
using fresh disjoint children and public diagonal relations exactly as
above. Scalar affine erasure preserves U without knowing it. Its terminal
kernel is |V|^-1 [q'-q in U]. An ordinary Fourier measurement is therefore
uniform on U-perp.

Take the prescribed number of roots, span their Fourier outcomes and
return the annihilator of that span. For a fixed input the terminal state
does not depend on the prior successful record. A spanning error bound
can therefore be applied to the ideal completed roots. Bounded retries
are dealt with by first-failure probabilities, NOT by asserting that
conditioning the entire run on future success preserves IID records.

## 4. Degenerate Branches

If the whole ambient algebra is abelian, use ordinary abelian HSP.
If N is nonzero abelian, take I=N and A=0, Fourier measure N, and obtain
the scalar degree-<=c phase directly from Q. Apply ordinary erasure only;
there is no GL alignment or nonzero-dimensional jet. The newer Python
MetabelianLieChart deliberately requires positive carrier width and does
NOT implement this scalar dispatch. The older scalar theory supplies it.

If a phase's current leading coefficient list is empty, any singleton
active witness is valid for that stage. If U=0 the source may be maximally
mixed and hide Q entirely; the output must be U=0, not coefficients of Q.
If U=V the terminal Fourier output is always zero. No step assumes the
dimension of U, a nontrivial character or a nonzero phase polynomial.

## 5. Arbitrary Hidden Subgroups Without Hidden Advice

Use this recursion on public ambient S and its inherited hiding oracle:
internally its answer is a full F_p basis of the hidden Lie subalgebra,
not just an arbitrary group-generating list. Exponentiating that basis
gives the generators required by the external statement. If a subroutine
returns only group generators, first take the Lie closure of their logs
by adjoining brackets until the span stabilizes. At most dim(S) strict
dimension increases occur. Taking their linear span alone would be wrong
for a nonabelian subgroup.

```
Solve(S):
    if S abelian: return AbelianHSP(S)
    N = [S,S]
    K = Solve(N)                         # basis of log(H intersect exp(N))
    M = normalizer_S(K)
    T = M / K
    while T nonabelian:
        U = TransverseImage(T)           # Section 3, not a supplied oracle
        T = preimage_T(U in T/[T,T])
    R = AbelianHSP(T)
    return a basis of span(K, public lifts of R)
```

On correct histories exp(K) is normal in H, hence H<=exp(M). K is an ideal
of M. The hidden subgroup of M/K is transverse to its derived group:
its derived algebra is contained in (N intersect M)/K, and
H intersect exp(N)=exp(K). Recompute the derived algebra of the quotient;
the previous N need not be contained in M. Lie and group normalizers
agree here: conjugation is exp(ad x), and the finite logarithm recovers
ad x from exp(ad x) on an invariant subspace because p>c.

The transverse hidden algebra h is abelian. The preimage of its exact
image is T=h+S'. Thus [T,T] is contained in gamma_3(S). Inductively,
gamma_j(T) is contained in gamma_(j+1)(S) for j>=2. Each nonabelian image
step strictly reduces ambient nilpotency class while preserving H and
transversality. Subalgebras and quotients preserve metabelianness of the
derived algebra.

Because N is metabelian, its own intersection recursion reaches the
abelian ideal N'. Its image path has at most k-1 steps; the outer image
path has at most c-1. Total: at most c+k-2 image calls and three abelian
calls. This is not a dimension-decreasing heuristic or a recursion that
quietly assumes the first intersection already known.

A public linear section of M/K need not be a homomorphism. Different
representatives differ by exp(K), so composing f with ANY such section gives
the same quotient labels on correct histories. Coherently compute the
representative, call the original oracle once, and UNCOMPUTE the
representative workspace. Discarding that workspace would leak which
representative was queried and destroy the required coherence. Nested
sections compose as public reversible computations; each final query
uses one original f call, not a product of recursive query budgets.

## 6. Adaptive Correctness And Complexity

Fix H and all its proof witnesses. Conditional on the complete classical
record, live registers are a tensor of independently produced kernels.
This is an induction on operations on disjoint register sets: a new raw
oracle source is fresh, local instruments have the derived conditional
outputs, discarded factors have trace one, and classical adaptation
chooses only public operations. Nodes may depend on all previous public
records. This does not let them share unrecorded random seeds, quantum
registers or a consumed child.

The distinction is necessary, not bookkeeping. For odd p define
|+_l>=p^-1/2 sum_x omega^(lx)|x> and

```
Gamma = p^-1 sum_l (|+_l><+_l|) tensor (|+_l><+_l|).
Gamma[(a,b),(a',b')] = p^-2 [a+b=a'+b'].
```

Both marginals are I/p, valid U=0 sources. Merge with scales (1,-1).
Every outcome has the SAME probability p^-2 as for independent inputs,
but its normalized output is |+_0><+_0| rather than I/p. Fourier sampling
would incorrectly suggest full support. The new test checks this exactly
over three fields. Even separable shared randomness can invalidate a
proof based only on marginal identities and branch normalization.

Use the per-call finite caps in INDUCED_END_TO_END_RESOURCE_AUDIT.md.
The fixed number kc+c of erasure levels, polynomial-size formal tables,
published fixed-degree SDE arities and their product are polynomial in
n and log(p) at fixed c,k. The standard solver is a constructive
dependency, not an additional black-box oracle. Its local implementation
is still missing beyond the restricted backend. The reference is
[Ivanyos--Santha, Theorem 11 and Section 3](https://arxiv.org/pdf/1503.09016).

BCH, polynomial arithmetic, field linear algebra, public coordinate
changes and reversible cleanup have polynomial bit complexity. Quantum
Fourier transforms and uniform preparation require precision polynomial
in the logarithm of the complete operation count. Count all oracle,
arithmetic, solver and output workspace; the existing data-register
certificate alone is not a total space bound.

For the whole recursion allocate delta=epsilon/(c+k+1) per call. Use
uniform global dimension/class envelopes and enforce finite caps on ALL
histories, including malformed output and wrong-subgroup histories.
On the first erroneous call the exact-history guarantee applies; a union
bound controls total failure. No correctness of later calls on that
wrong history is asserted. Abort on violations of public input, class
or loop guards. Add query costs across calls.

Approximation must be bounded on COMPLETE instruments including ABORT,
uniformly over their classical controls. A CPTP hybrid bounds the total
variation of the complete run by the sum of half-diamond errors. Do not
normalize individual rare branches and amplify the bound by their inverse
probability. The ideal product-state induction is not claimed verbatim
for an approximate device conditioned on unlikely records.

## 7. What This Audit Did And Did Not Establish

The written argument now gives one public procedure from f to H, with
the specific active-support omission repaired. Known algorithmic
dependencies have been separated from missing local software. Calling
the published SDE theorem is legitimate in a complexity proof; calling
an undefined TransverseImage oracle would not be.

Existing Python recursion still accepts an ideal quotient-image callback
and rejects class(N)>3. Its known-H diagnostic callbacks are not an
implementation of Section 3. The compiler does not consume quantum
states, enforce provenance, synthesize gates, or run the general SDE.
No end-to-end execution or speedup claim follows from its tests.

| Obligation | Current evidence | Residual obligation |
| --- | --- | --- |
| Ordinary f to induced source | Written Lie argument; abstract Lean source identities | Single Lazard-to-instrument formal refinement |
| Cocycle to public polynomial | Universal written proof; exact coefficient certificates; operator Lean lemmas | Extracted compiler correctness |
| Active weighted merge | New active-subtype and tensor-discard Lean theorems | Controller provenance and measurement implementation |
| Two erasures and final U | Local channel identities plus the induction above | One adaptive end-to-end formal theorem |
| Arbitrary H and resources | Normalizer/class-drop proof and capped schedule | General controller, SDE and synthesis implementation |
| Novelty and significance | Strict-scope witness; targeted comparisons | Independent review and a useful hard application |

### Fresh Prior-Art Check

[Morales, August 2026](https://arxiv.org/html/2608.05321v1) treats scalar
semidirect products with bounded abelian generator rank and an exponent
restriction, and quasi-Hamiltonian groups with structured input. This is
not an exhaustive novelty review. Two elementary scope checks are useful:

1. A scalar p-power-order automorphism of an elementary abelian p-group
   is trivial, since its scalar order divides p-1. Thus the corresponding
   prime-exponent scalar semidirect product is abelian.
2. A quasi-Hamiltonian group of exponent p is abelian: any two order-p
   cyclic subgroups permute, their product has order at most p^2 and is
   abelian, so their generators commute.

These are our group-theoretic comparisons, not conclusions supplied by
that paper. Neither stated family subsumes the nonabelian prime-exponent
scope witness. This does not exclude other prior algorithms or reductions.

## 8. Decisive Remaining Falsifiers

- Find a source/cocycle/Taylor sign or support mismatch in the UNIVERSAL
  identities, not merely an unimplemented interface. It would invalidate
  the provisional theorem even if every finite diagnostic passes.
- Exhibit a legal adaptive schedule that violates the conditional tensor
  invariant despite keeping the full record and consuming disjoint
  sources. The shared-randomness counterexample does not meet those rules.
- Find a hidden-coefficient dependency in the published solver inputs,
  alignment, quotient oracle, or loop termination. The construction above
  is intended to exclude it explicitly.
- Show a claimed polynomial operation actually enumerates F_p or that
  fixed-class constants secretly depend on n. No full-table simulator
  or finite exhaustive test can resolve this uniformity question.
- Locate a prior uniform-large-prime arbitrary-H theorem that subsumes
  this exact input class. The receiver could then be a reformulation,
  not a new algorithm, even if the mathematics is correct.
- Show all natural efficient label or state sources in the class admit
  access-matched classical algorithms. Existing application audits are
  already negative for several tempting graph/code/matrix actions.

Next theory work should target independent novelty/application review or
a mechanism that materially reduces the huge erasure tree. More local
filiform examples, status wrappers or interface-only modules have low
research value. Mechanical work has a concrete specification above but
must not relabel ideal callbacks as an implemented quantum receiver.

## Verification

549 connected Python tests pass in 155.91 seconds with RuntimeWarning
fatal, including the ten new composition controls. Full cached
`lake build --wfail` passes (3467 jobs); the four new guards permit only
propext, Classical.choice and Quot.sound. Python syntax, formal crosscheck,
site JavaScript/site checks, `python qsearch.py validate` and whitespace
checks pass. All owned processes are terminal. The full repository Python
suite was not run. No CLI/UI change, central admission, commit or push.
