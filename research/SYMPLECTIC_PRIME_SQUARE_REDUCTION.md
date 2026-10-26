# A Lawful Socle-To-Polynomial Reduction For Siegel HSP

2026-10-23. Proposed algorithmic deduction, REVIEW PENDING. Exact finite
matrix controls pass; no quantum HSP or hidden-polynomial solver was run.
This is not a novelty certification, a classical lower bound, a natural
cryptographic application, or a Shor-level result.

2026-10-23 extension: SYMPLECTIC_CHAIN_RING_DIGIT_REDUCTION.md supplies
full-precision scalar-unit probes for all intermediate digits and the
same elementary-Levi final digit over odd-residue chain rings. The written
scope includes growing chain length; the new arithmetic backend implements
Z/p^e. This does not extend a field oracle to a ring. It also shows why
field-only unipotent certificates and transvection membership tests fail
on lifted submodules. No natural source or independent review follows.

Later same-day update: SYMPLECTIC_FIELD_CHART_REDUCTION.md proposes a
separate FIELD-ONLY route using constant-density Lagrangian graph charts
and HPGP, plus a scoped opaque-label classical query lower bound. It does
not revive the invalid additive whole-Lie oracle. The ring proof below
retains its own input contract; no field/ring oracle extension is implied.

## Decision And Input

An older branch was closed too broadly. Its O(n q^k) transvection attack
is not polynomial in the encoded field size log(q) for arbitrary growing q.
Its missing multiplicative-to-additive oracle was a genuine gap over a
FIELD, but a square-zero congruence layer supplies such an oracle over a
different, explicitly stated ring input. This is not permission to extend
a finite-field hiding function to that ring for free.

Supply an odd prime p, n>=2, R=Z/p^2Z with ordinary integer arithmetic,
and the standard symplectic form J on R^(2n). The ordinary coherent oracle
f on Sp_(2n)(R) hides exactly P_W, the stabilizer of an unknown FREE
LAGRANGIAN DIRECT SUMMAND W of rank n. Thus f(g)=f(g') iff gW=g'W; this
does NOT say that the oracle reveals a matrix representation of gW.
Oracle labels have fixed polynomial width and all calls are charged.

**Proposed conclusion:** recover W, and hence generators of P_W, in
bounded-error quantum time polynomial in n, log(p), log(1/epsilon).
The reduction uses one abelian HSP and n degree-two hidden polynomial
graph problems with output dimension m=n(n+1)/2. The quantum subroutines
are published algorithms, not the repository's unreviewed general Rees
receiver. This is an input-preserving reduction inside a structured matrix
HSP, not a tiny circuit or a planted performance benchmark.

## Published Dependencies And Search Scope

- [Imran, 20 October 2026](https://arxiv.org/html/2610.28368v1), Section 3,
  uses socle probes for GL over chain rings. That paper motivates revisiting
  legal congruence probes; its theorem is not a theorem about Sp. Its
  final-layer shift construction is not silently imported here.
- [Ivanyos--Santha](https://arxiv.org/html/1503.09016), Theorem 5 and
  Corollary 6, supply a quantum polynomial-time solver for univariate
  constant-degree HPGP' over prime fields, with GROWING output dimension.
  Our reduced degree is two. Their Sections 4--5 are the dependency,
  not an exponential classical interpolation over p inputs.
- Abelian HSP, finite-field symplectic linear algebra, and unit-group
  computations are standard paid components. No new primitive is claimed.

Targeted searches did not locate this precise Sp prime-square composition.
That is not evidence that it is new. Independent proof and literature
review must precede any novelty or discovery admission.

## 1. Recover The Reduction Of W By A Real Abelian Oracle

Let sp be the Lie algebra over F_p, represented by matrices satisfying
X^T J+JX=0. The map

    X -> I+pX  (mod p^2)

is an injective homomorphism from (sp,+) to Sp_(2n)(R): the quadratic
product term vanishes modulo p^2. It is invertible with inverse I-pX.
This is precisely why the old invalid field-level map I+X is NOT used.

For a direct summand W, pXW is contained in W iff X preserves Wbar.
Indeed W intersect pR^(2n)=pW, and multiplication by p identifies the
residue space with the socle. Consequently f(I+pX) hides the ADDITIVE
linear space p_Wbar={X in sp: X Wbar subset Wbar}. One ordinary f query
implements a query to this derived oracle, with public reversible arithmetic.

In a symplectic basis with Wbar the first n coordinates,

    X in sp: X=[ A B ; C -A^T ],  B=B^T, C=C^T;
    X in p_Wbar: C=0.

For odd p the pairing Tr(XY) on sp is nondegenerate. Its restriction in
these blocks is 2Tr(AA')+Tr(BC')+Tr(CB'). Orthogonality to p_Wbar therefore
gives u_Wbar={ [0 B;0 0] : B symmetric }. The span of the images of ALL
matrices in u_Wbar is Wbar. Compute the annihilator from a learned basis
of p_Wbar by linear algebra, then concatenate its image columns. No
nonabelian Fourier transform or unknown unipotent-radical oracle is used.

There is an exact verification step. Require the candidate Wbar to be
Lagrangian of dimension n. Compute a basis of its stabilizer algebra and
test f(I+pX)=f(I) on that basis. Containment in the true stabilizer algebra
then implies equality: both have dimension n^2+m. Taking annihilators and
image spans proves the candidate Wbar correct. This is stronger than merely
checking that the abelian learner returned linearly independent vectors.

## 2. Standardize Without Assuming A Field Embedding In The Ring

Extend a basis of Wbar to a symplectic basis over F_p. Lift its entries
to a matrix B0 over R. An arbitrary entrywise lift is not necessarily
symplectic, so compute

    B0^T J B0 = J+pD mod p^2,
    C = (1/2) J D mod p,
    B = B0(I+pC) mod p^2.

D is skew-symmetric and C^T J+JC=-D, so B^T J B=J modulo p^2. All divisions
by p above are ordinary divisions of known divisible integer residues;
division by two is in F_p. No hidden coordinate is used.

Conjugate the oracle by this known B. Its hidden subspace now has the
unique graph form

    W_S = columns [ I ; pS ],  S symmetric over F_p.

The graph form follows from the invertible top projection; Lagrangian
isotropy says p(S-S^T)=0 modulo p^2. Learning S completes the answer.

## 3. Legal Queries Give A Degree-Two Hidden Polynomial Graph

Fix i!=j and E=E_ij. For t in F_p take its canonical integer representative
and put A_t=I+tE over R. Since E^2=0, its inverse is I-tE. For symmetric X
over F_p define the ACTUAL symplectic matrix

    g_ij(X,t) = [ I 0 ; pX I ] diag(A_t,A_t^(-T)).

These queries do not depend on S. Acting on W_S and normalizing the top
basis gives the graph of p(X+A_t^(-T) S A_t^(-1)), where the expression
in parentheses is computed modulo p. Therefore, setting

    B_ij = -(E^T S+S E),
    C_ij = E^T S E,
    P_ij(t)=t B_ij+t^2 C_ij,
    F0(X)=f([I 0;pX I]),

we have the exact common-label identity

    f(g_ij(X,t)) = F0(X+P_ij(t)).

F0 is injective: distinct lower socle shifts give distinct graph submodules.
With symmetric matrices encoded by their m upper-triangular entries,
uniform (X,t), one oracle query and measurement of its value produce

    p^(-1/2) sum_t |t>|z-P_ij(t)>,

with z uniform in F_p^m. These are precisely HPGP' states for Q=-P, with
zero constant term and degree at most two. Negate the learned coefficients
before using B_ij,C_ij below. All p values of t, INCLUDING ZERO, are legal;
there is no missing-parameter postselection or rank-one scalar-unit trick.
Corollary 6 of the cited paper applies uniformly in m and log(p).

**Important carry check:** t -> A_t using representatives of F_p in Z/p^2
is NOT a group homomorphism. For example A_4 A_4 != A_3 modulo25. We did
not assert one: the actual oracle fibers, established above by their
subspace action, are the HPGP promise. Extra pE carries do not change that
action on graph lifts. Treating the chosen representatives as an embedded
field would be an incorrect proof, even though the final fiber identity holds.

## 4. Recover Every Entry And Verify The Learned Polynomials

For i=0,...,n-1 choose j=(i+1) mod n and solve that HPGP. The linear
coefficient alone determines column i of S:

    S_(k,i) = -B_ij[k,j]       if k!=j,
    S_(j,i) = -B_ij[j,j]/2.

n queries to the HPGP SUBROUTINE, not n original oracle queries, therefore
give all of S. Check its symmetry and coefficient consistency. Those checks
alone would not certify a different but internally consistent wrong S.

Fortunately each returned polynomial has an EXACT four-query verifier:
for t=1 and t=-1 compare

    f(g_ij(0,t)) == f([I 0;p P_candidate(t) I]).

Injectivity of F0 makes these equality tests exact polynomial-value tests.
Both polynomials have zero constant term. Agreement at 0,1,-1 implies
agreement of both coefficients over every odd F_p. This works also at p=3.
A test only at 1 misses B->B+D, C->C-D; a control below exhibits that fault.
No hidden S is passed to the real verifier.

Return B times the columns [I;pS]. To output subgroup generators, conjugate
the standard Siegel generators by B[I 0;pS I]. Standard generators consist
of the symmetric upper unipotents and diag(A,A^(-T)) for generators A of
GL_n(R). Elementary matrices and diagonal unit generators suffice over
this local ring. If unit generators are not supplied, charge standard
quantum factoring of p-1 and primitive-unit construction/verification; that
known arithmetic speedup is not part of a new contribution.

## 5. Clocks, Error, And Classical Baselines

The public abelian dimension is n(2n+1), HPGP output dimension is m, and
there are n HPGP calls of fixed degree two. Matrix arithmetic, interpolation
checks, basis changes, and reversible query preparation are polynomial in
n and log(p). Every HPGP source query is one original f call. Use the
published bounded-error solvers with their precision costs; none of them
is implemented by the present arithmetic module.

Each subroutine has a deterministic oracle verifier as described above.
Repeat an independent constant-success subroutine a fixed
O(log((n+1)/epsilon)) number of times, retaining ABORT on exhaustion.
Union-bound failed stages; do not postselect away them or assert an exact
quantum receiver. Approximate gates have a separate complete-circuit error
budget. With the exact promised oracle, the verifiers cannot admit a wrong
Wbar or a wrong degree-two P. Prime validation and unit-group output costs
are explicit public preprocessing, not discovery claims.

The older field transvection attack costs O(n q^k) queries. It is polynomial
only when q^k is polynomial in the stated input size; k=1 does not suffice
when log(q) grows. That attack is neither a lower bound nor automatically
an algorithm for every lifted-ring problem. A direct classical reconstruction
using the FULL original Sp oracle would be the strongest dequantization test.
Restriction to our probes cannot establish a lower bound against other
queries. An explicit application whose oracle already exposes W is trivial.
The finite tests use canonical image labels only to check fibers, not as a
hardness model or a claimed quantum-versus-classical runtime comparison.

## 6. Try To Break The Claim

- **Input mismatch:** a hiding oracle only on Sp(F_p) cannot evaluate our
  matrices over Z/p^2. This does not solve the old finite-field problem.
- **Not a direct summand:** the socle criterion and graph normal form use
  freeness and purity. Arbitrary torsion submodules are outside the claim.
- **Characteristic two:** the trace pairing and division by two fail. No
  binary extension is asserted.
- **Rank one:** n>=2 is essential to this construction. Indeed over Z/9,
  distinct lines <(1,0)> and <(1,3)> have IDENTICAL stabilizers in SL_2.
  Recovering a unique W in that case is impossible from the HSP oracle.
  This does not rule out recovery of the common subgroup.
- **Only socle samples:** they determine Wbar, not S. Every graph lift
  with the same Wbar has the same stabilizer intersection with the socle.
- **Wrong labels/sign:** use one common F0; negate HPGP's Q=-P, retain
  full fibers, and validate both t=1,-1. A membership-only test is not a
  replacement for the supplied coset-label oracle.
- **Dependency failure:** the growing-output-dimension HPGP theorem, not
  a constant-m algorithm or an unproved Rees claim, must be applicable.
- **No significance shortcut:** correctness would establish this structured
  oracle reduction, not classical hardness or a useful cryptographic attack.

## Controls And Next Work

`theorems/symplectic_socle_probes.py` constructs legal public queries,
the symplectic lift correction, verification query pairs, and postprocesses
SUPPLIED correct polynomial coefficients. `graph_polynomial(S,...)` is a
ground-truth proof helper, not a learner. No SDE/HPGP/HSP solver is present.

The standalone tests check actual matrix images and whole small oracle
fibers, odd-characteristic trace duality in nonstandard coordinates,
large-prime exact arithmetic, all-column reconstruction, the representative
carry fault, the rank-one ambiguity, and the insufficient one-point verifier.
They do not simulate the published quantum algorithm or prove novelty.

Validation checkpoint:23 new matrix/fiber checks plus7 cut-list counterchecks
pass. Together with the prior75 Rees/source checks,105 tests pass. Python
syntax checks pass. No full repository suite, qsearch validation, central
registry refresh or quantum execution is claimed.

NEXT: independent proof review of the two oracle interfaces and exact
verifiers; a genuinely stronger classical attack using the full ring-group
oracle; and a costed application that supplies this parabolic hiding promise.
Do not start a sweep of nearby ring sizes or claim Sp(F_p) is solved.
