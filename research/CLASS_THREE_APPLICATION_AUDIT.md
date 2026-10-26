# Fixed-Class HSP: External Application Audit

2026-10-21. Status: classical filters, the large-prime abelian fallback,
and transporter-reduction costs audited for the fixed-class proposals. No useful external
application established. The proposals in CLASS_THREE_HSP_THEOREM_DRAFT.md
and BOUNDED_CLASS_METABELIAN_HSP.md are NOT refuted. This is a mathematical
scope audit, not a new candidate campaign; the historical filename remains.

## The Required Reduction

Given an explicit object X and a supplied group Gamma acting on it, set
`H = Stab_Gamma(X)` and `f(g) = g.X`, with a canonical object encoding.
Then `f(g) = f(g')` iff `g'^{-1}g in H`, so f separates left cosets gH.
This is a legitimate HSP reduction only when the action, encoding,
group presentation, and coherent evaluator are efficient in the
ORIGINAL input length. A fast algorithm must also beat algorithms
that inspect X directly, not merely algorithms querying opaque f labels.

For a linear code, reduced row echelon form removes generator-basis
gauge without enumerating codewords. This makes a valid hiding function;
it does not make the resulting computational problem classically hard.

## Classical Baselines

### Graphs And Explicit Colorings

For a supplied solvable permutation group Gamma, color/set stabilizers
are polynomial-time classical problems. Graph stabilizers follow by
the induced action on vertex pairs, whose domain has size at most N^2.
See [Schweitzer, Theorem 10 and its graph application, Section 6](https://drops.dagstuhl.de/storage/00lipics/lipics-vol080-icalp2017/LIPIcs.ICALP.2017.66/LIPIcs.ICALP.2017.66.pdf),
which states the relevant Luks result explicitly.

Every nilpotent group is solvable. Thus a supplied class-three
permutation ambient group does not create a superpolynomial graph or
explicit-string stabilizer advantage. This is NOT a solution of
unrestricted graph isomorphism, nor of finding an unknown ambient group.

### Codes, Including Large Hulls

[Luks, Computing in Solvable Matrix Groups, Theorem 3.2(5),(7), Section 6.3](https://ix.cs.uoregon.edu/~luks/solmatgrp.pdf)
gives vector/subspace stabilizers and subspace transporters in time
polynomial in `D + log(q) + mu` and generator input size. Here
`Gamma <= GL(D,q)` is supplied and solvable; mu is its largest prime
divisor other than the field characteristic (take mu=1 if absent).
The finite-field encoding must support efficient arithmetic.

Our application: embed `Gamma <= S_N` by permutation matrices.
Since `|Gamma|` divides `N!`, mu <= N. For a generator matrix M,
`Gamma intersect Aut(rowspace(M))` is exactly this subspace stabilizer.
The bound is polynomial in the explicit code input; no codeword list,
hull assumption, or hull-shortening step is needed. Equivalence within
the supplied Gamma is likewise a subspace transporter.

Defining-characteristic p-group matrix actions have mu=1. Explicit
fixed-arity tensor actions also linearize into polynomial dimension;
the same baseline applies when mu is polynomially bounded.

These are deductions using a published theorem, not a local
implementation or independent proof of Luks's algorithm. Its conference
version omits some structural proofs.

### Large Cross-Characteristic Primes Do Not Require A New Nonabelian Solver

For the EXPLICIT nilpotent matrix stabilizers above, the previous
large-prime gap closes using existing abelian quantum algorithms. This
is not full classical dequantization, a new algorithm claim, or a result
about arbitrary succinct actions. The actual representation dimension D
and object encoding are charged. Nilpotence of the supplied ambient group
is essential; solvability alone is insufficient for the following split.

**Dimension lemma.** If p is prime, p>D and p does not divide q, every
p-subgroup of GL(D,q) is abelian. Luks already uses this observation and
the small/large-prime split in Section 5; it is not new here. The following
elementary order argument also covers extension fields directly.

Let e be the multiplicative order of q modulo p, k=floor(D/e), and
a=v_p(q^e-1). For odd p the valuation identity gives

```
|GL(D,q)| = q^(D(D-1)/2) product_(i=1)^D (q^i-1),
v_p(|GL(D,q)|) = sum_(j=1)^k (a+v_p(j)) = k*a,
```

since k<p. Embed k independent copies of the multiplicative group of
F_(q^e), acting on k disjoint e-dimensional blocks, and identity on the
remainder. Their p-parts form an abelian subgroup of the entire Sylow
order p^(ka). Sylow conjugacy gives the claim. If k=0, the p-part is
trivial. The only omitted even case has p=2>D, hence D=1 and is already
abelian. No diagonalizing basis needs to be computed by the reduction.

**Constructive split without large integer factorization.** Set

```
ell = characteristic(F_q),     Delta = {ell} union {primes <= D},
M = |GL(D,q)| = M_small * M_large,
```

where M_small contains exactly the Delta-primary factors. M has
O(D^2 log q) bits. Enumerating primes up to D and repeatedly dividing
by them and ell constructs both coprime factors in polynomial time;
factoring M_large is unnecessary. Compute CRT exponents

```
e_small = 1 (mod M_small),  0 (mod M_large),
e_large = 0 (mod M_small),  1 (mod M_large).
```

A trivial factor uses projector exponent zero. For each input generator
g, compute g^e_small and g^e_large by repeated squaring. A finite nilpotent
Gamma is the direct product of its Sylow subgroups, so these power maps
are its Hall projections and their images generate B and A respectively:

```
Gamma = B x A,    gcd(|B|,|A|)=1,    mu(B)<=D.
```

Each Sylow factor of A is abelian by the dimension lemma. Distinct Sylow
factors commute, so A is abelian and central in Gamma. B is still
nilpotent. For ANY subgroup H<=Gamma, powers of h stay in H and therefore

```
H = (H intersect B) x (H intersect A).
```

This last step prevents a hidden coupling between the two components;
it would be false for arbitrary direct products of noncoprime order.

**Costed baseline for H=Stab_Gamma(X).** Compute Stab_B(X) using the
published classical bounded-mu algorithm. To recover Stab_A(X), let
a_1,...,a_s be the projected input generators, and use the ordinary
abelian HSP with domain C_(M_large)^s and evaluator

```
x |-> (product_i a_i^x_i).X.
```

All a_i orders divide the KNOWN M_large, so this map is well-defined.
Its fibres are exactly cosets of the preimage of Stab_A(X). Redundant
generators and an oversized common exponent add kernel elements, not
ambiguity. Map the returned subgroup generators back to matrices and
join them with Stab_B(X). There is no assumption that the a_i orders,
a diagonalization, or a decomposition of A are supplied. This uses the
standard [abelian stabilizer/HSP algorithm](https://arxiv.org/abs/quant-ph/9511026)
over a known product of cyclic groups, with approximate Fourier operations
and total error charged, not a new fixed-class HSP subroutine.

Matrix exponentiation and the object evaluator have polynomial cost in
s, D, log q and the explicit object size. Canonical output encodings
are required: use the vector itself, reduced row echelon form for a
subspace, or a sorted explicit finite set, for example. A fixed-arity
tensor is covered only after its polynomial-dimensional linearization.
Reversibly computing these encodings supplies the ordinary oracle.
The abelian domain has s*log(M_large) bits, not M_large elements loaded
as input. The B algorithm and the abelian quantum primitive are cited
dependencies, NOT implementations in this repository.

**Conclusion and exceptions.** These explicit nilpotent vector/subspace/
finite-set stabilizers, including large-prime monomial cases, cannot
motivate the proposed NONABELIAN HSP improvement: classical methods plus
already-known abelian quantum primitives suffice. This does not establish
classical polynomial time for their large-prime component. Nor does it
cover arbitrary solvable ambients, unknown ambients, opaque labels,
succinct nonlinear actions or the problem of finding a transporter.
The characteristic ell may exceed D and support nonabelian unipotent
groups; ell was deliberately assigned to B and is excluded from mu.
For a nonfaithful abstract representation, computing the kernel and
lifting answers require a separate costed interface.

### Sparse Pauli Objects Under Nilpotent Clifford Actions

2026-10-21: the preceding finite-set baseline applies to a concrete
quantum-symmetry application, PROVIDED phases and input access are kept.
Learning arbitrary unknown quantum states is not covered by this filter.

Let p be an ODD prime, v=(x,z) in F_p^(2n), and use symmetric Weyl
operators D(v), with the convention in PRIME_CLIFFORD_REALIZATION.md.
Supply a group Gamma of Clifford conjugation actions by faithful public
tableaux, and a sparse operator

```
O = sum_(v in S) a_(j(v)) omega^(t_v) D(v),   omega=exp(2*pi*i/p).
```

Here S has polynomial size, each label v occurs ONCE after exact
coefficient coalescing, and all coefficients are nonzero. The a_j are
canonical amplitude classes modulo multiplication by p-th roots of
unity: a_j/a_k is not such a root for j!=k. The phases t_v are supplied
as integers modulo p. Distinct nonzero real rational coefficients give
valid separate classes at odd p, for example. General algebraic or
approximate coefficients need their own costed normalization/equality
procedure; do not assume an arbitrary complex number comes with a free
exact phase-class label.

For any Clifford U, symmetric Weyl multiplication implies

```
U D(v) U^dagger = omega^(ell_U(v)) D(M_U v),
M_U is symplectic,       ell_U:F_p^(2n)->F_p is LINEAR.
```

Linearity follows because conjugation preserves the Weyl product and
M_U preserves its alternating form. In particular the full tableau is
not just M_U. Composition obeys

```
M_(UV) = M_U M_V,
ell_(UV) = ell_V + ell_U M_V.
```

Encode each nonzero coefficient as the field vector
(v,t_v,e_(j(v))), where e_j is a one-hot color in F_p^s and s is the
number of amplitude classes. The conjugation action is the LINEAR map

```
          [ M_U   0   0 ]
L_U   =   [ ell_U 1   0 ],       dimension 2n+1+s,
          [  0    0  I_s]

A_O = {(v,t_v,e_(j(v))) : v in S}.
```

The composition identity makes U -> L_U a homomorphism. Distinct Pauli
labels are linearly independent over C, so, with the canonical classes,

```
U O U^dagger = O     iff     L_U(A_O)=A_O.
```

This is a finite SET stabilizer, not the stabilizer of the span, an
unweighted Pauli support, or a vector containing p^(2n) coefficients.
Both the dimension and explicit set size are polynomial in the sparse
input. All physical global phases of U disappear because the task is
conjugation symmetry; if an abstract input group has an additional
kernel, computing/lifting that kernel remains a separate obligation.

For a supplied defining-characteristic p-group Gamma, its image is a
solvable matrix p-group over F_p and mu=1. Consequently
[Luks, Theorem 3.2(6), with the set algorithm discussed in Section 6.4](https://ix.cs.uoregon.edu/~luks/solmatgrp.pdf)
gives a classical polynomial-time stabilizer algorithm in n, |S|,
generator size and log p. This applies even when p is exponentially
large in its bit length and Gamma has nonabelian derived group. For an
arbitrary supplied NILPOTENT tableau group, the earlier Hall split gives
the classical bounded-mu component plus an EXISTING abelian quantum
component. Neither needs the proposed class-four HSP receiver.

This filters an apparently natural route via sparse Hamiltonians or
explicit sparse density operators. It is consistent with current
[Clifford-symmetry work on qudit Hamiltonians](https://arxiv.org/abs/2605.30428),
which reduces the unrestricted symmetry search to graph automorphisms
with phase checks. The deduction here concerns a SUPPLIED nilpotent
ambient; it does not solve unrestricted graph automorphism or the full
Clifford-symmetry problem in classical polynomial time.

**Limits that prevent an overbroad rejection.**

- Unknown copies of rho do not supply its Pauli coefficients or a sparse
  description. Exponentially many nonzero coefficients cannot be expanded
  for free. Nor does a Hamiltonian oracle automatically supply its sparse
  list or normalized vectorized state at polynomial cost.
- Clifford actions on arbitrary nonstabilizer states are not a blanket
  Gottesman--Knill instance. Even the coherent control needed by StateHSP
  can be non-Clifford: sum_a |a><a| tensor P^a has phase a*t^2/2. Its
  conjugation of target X contains phase a*t+a/2, which is not linear in
  the joint Pauli coordinates. Thus efficient tableau descriptions of
  each R(g) do not simulate the controlled quantum algorithm.
- Conjugation symmetry of rho is not Bose symmetry of its vector or
  support. Z fixes |1><1| but does not fix |1> as a vector. The strict-gap
  transfer note distinguishes these tasks and its pure projective route.
- Large magic and entanglement alone do not establish a hard alternative.
  [Arunachalam--Bravyi--Dutt--Yoder](https://arxiv.org/abs/2208.07851)
  already learn fixed-degree BINARY qubit phase states efficiently; their
  generalized Boolean-domain phase learner is not stated to run in
  polynomial time. For growing-prime full-domain phase copies, see the
  separate known-technique adaptation in
  POLYNOMIAL_PHASE_COPY_LEARNING_BASELINE.md. Recent
  [Haug](https://arxiv.org/abs/2609.27128) and
  [Aguilar--Jerbi--Eisert--Bittel](https://arxiv.org/abs/2609.27565)
  give learners for specified Clifford-scrambled product structure.
  Their promises/access must be checked, not generalized to every mixed
  state or arbitrary growing-prime qudit input. Hard sampling does not
  by itself imply hard structural learning.

Seven controls in tests/test_clifford_sparse_object_baseline.py compare
the phase-colored embedding with dense Clifford conjugation over p=3,5,7,
check the semidirect phase law, reject discarded phases/colors, and test
a faithful nonmetabelian UT5 tableau family at a 127-bit prime without
Hilbert-space expansion. Separate controls reject the two overbroad
quantum-input claims above. These tests validate the reduction identities,
not Luks's asymptotic algorithm; no production stabilizer backend or new
candidate was implemented. The genuine remaining application task is a
motivated succinct/quantum input outside these explicit-description
filters, with paid access and a proved gap, not another planted symmetry.

### Low-Degree Algebraic Labels Beyond Class Three

The derivative attack in NIL3_POLYNOMIAL_HIDING_ATTACK.md now covers
any supplied nilpotency bound c<p, not just class three or metabelian
groups. If the ORIGINAL hiding function exposes degree-e field values
in public Lie coordinates, set D=max(1,2*floor((c-1)/2)) and, for e>0,
require p>max(c,e*D,2*(e-1+D)). The stabilizer is recovered classically
by a polynomial number of chosen queries and linear algebra. Constant
evaluators are handled separately. Higher nilpotency class alone does
not escape this baseline. A class-five correction is needed in the
right-action field; ignoring it would make the attack unsound.

This filter is separate from Luks's explicit matrix algorithms.
It does not cover every succinct nonlinear action, exponential-degree
arithmetic circuit, or opaque-label oracle. It does not solve a general
transporter problem merely by computing a stabilizer. Those exclusions
are missing coverage, NOT evidence of hardness or quantum advantage.

### Succinct Circuits Need A White-Box Attack

NEW [SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT.md](SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT.md)
costs an ordinary hiding oracle for FORMAL polynomial stabilizers under
supplied matrix p-groups: one fixed random extension-field evaluation
separates the complete polynomial orbit with bounded failure, without
coefficient expansion. This is a conditional input-problem reduction,
not a useful hard instance or an admitted quantum algorithm.

The same audit derives a stronger classical filter when
`p>max(D,(D-1)*Delta)`, with matrix dimension D and formal degree Delta.
Public circuit gradients and extension-field sampling recover the Lie
stabilizer in time polynomial in circuit size, log Delta and log p;
the degree bound proves equality with the FINITE stabilizer. Thus even
exponentially high degree does not rescue the sufficiently large-
characteristic regime. This is a written argument with exact controls,
not a production solver or a novelty claim.

Below that characteristic bound, derivatives can err in either direction.
Nevertheless, exposed coordinatewise Frobenius or Artin--Schreier lifts
have exactly the same linear stabilizer as their base polynomial and
must be deflated. Surviving uncovered circuit models are not hardness
evidence. Do not launch a synthetic high-degree campaign on that premise.

The same note now handles MIXED exposed Frobenius levels: a polynomial-size
lift to independent variable blocks preserves finite stabilizers when its
degree delta<p. For p>max(D,(D-1)*delta), the lifted white-box derivative
attack applies even when the original degree is enormous. Its implementation
transforms public circuit DAGs and differentiates the lift; it is not a
general semantic root extractor or a complete stabilizer backend. Degree-p
carries and non-base-field matrices are explicit scope counterexamples.

## Scope That Must Not Be Lost

- Large hull or self-duality does NOT rescue code equivalence restricted
  to a known solvable permutation ambient group. Do not launch a
  high-hull campaign on that premise.
- A promise that the UNKNOWN stabilizer is nilpotent does not supply a
  nilpotent AMBIENT group. The HSP algorithm needs the latter. General
  code equivalence still ranges over S_N, not over its unknown answer.
- The prime bound above is for permutation representations. General
  monomial actions can introduce prime divisors of q-1 much larger
  than N; do not silently reuse mu <= N.
- An implicit tensor with exponentially many coordinates is not an
  explicit polynomial-dimensional linear representation. Charge any
  expansion before using either a classical or quantum algorithm.
- Large cross-characteristic primes in an explicit nilpotent matrix
  stabilizer split into an abelian factor as proved above. They do not
  rescue a NEW nonabelian quantum contribution. This fallback is quantum,
  not an assertion of classical polynomial time or a transporter solver.
- The degree promise in NIL3_POLYNOMIAL_HIDING_ATTACK.md concerns the
  original evaluator. The new matrix-action baseline does not require
  that promise. Neither baseline applies to every opaque HSP oracle.

## The Equivalence Wreath Product Does Not Preserve The Promise

For a single object, stabilizer H is a subgroup. For two objects, the
set of equivalences, if nonempty, is generally a coset, not a subgroup.
The usual two-object hidden-shift reduction uses
`W = (G x G) semidirect C_2`, where the involution swaps the factors.
One cannot assume W remains class three merely because G is class three.

Here is a direct obstruction, independent of the code encoding.
If G contains an element a of odd prime order p, put

```
r = (a, a^-1, 0),       t = (1, 1, 1).
t r t = r^-1,           [r,t] = r^-2,
[...[r,t],...,t] = r^((-2)^j)       (j commutations).
```

The commutator convention is `[x,y] = x^-1 y^-1 x y`.
No displayed iterated commutator is identity for odd p. Thus W is
not nilpotent at all, and the proposed class-three solver cannot be
applied to this reduction unchanged. In particular this affects the
growing odd-prime regime motivating the theorem draft.

The odd-prime condition matters. `C_2 wr C_2` has order eight and
nilpotency class two. It is a counterexample to the overbroad assertion
that every such wreath product is nonnilpotent. This calculation rejects
one reduction, not all possible equivalence algorithms or reductions.

## A Characteristic-p Wreath Repair Also Loses The Promise

Replacing the swap C_2 by a regular C_p action does not provide a
fixed-class reduction in the large-p regime. Already the smallest
example is

```
C_p wr C_p = V semidirect C_p,     V=Fp^p.
P = cyclic coordinate shift,      J=P-I.
```

V is abelian, so this group is metabelian. Its lower central subgroups
from gamma_2 onward are J*V, J^2*V, ..., with harmless inverse-shift
convention changes. In characteristic p,

```
J^p=P^p-I=0,
J^(p-1)=I+P+...+P^(p-1) != 0.
```

The second identity follows by expanding (x-1)^(p-1) modulo p; applying
it to a coordinate vector gives the nonzero all-ones vector. Thus the
nilpotency class is exactly p. Moreover, if a=(e_0,P), then a^p is the
all-ones base element, of order p. Every p-th power is in V, hence the
group has exponent p^2, not p. These are direct group identities, not
complexity conclusions inferred from small examples.

Whenever G has a subgroup C_p, its regular wreath G wr C_p contains
this example, so its class is at least p. Growing p therefore breaks
both the fixed-class bound and the large-characteristic c<p core. The
explicit regular-wreath input also has p base components, potentially
exponential in log p. Holding p fixed changes the regime and may invoke
existing bounded-prime results; it does not supply the claimed new
large-prime application. Nor have we established a valid two-object
transporter reduction to this alternative wreath in the first place.
This rejects the obvious repair, not every possible reduction.

## Stabilizer Recovery Does Not Give A Target Transporter State

Let x,y be explicit objects under an efficiently evaluable action of G.
Knowing H=Stab_G(x) does not itself find t with t.x=y. If such t exists,
the solution set is the coset tH. In the direct proposed preparation,
start uniformly over G, evaluate g.x, and postselect the output y.
Writing M=|G.x|=|G|/|H|, its exact success probability is

```
Pr[g.x=y] = |H|/|G| = 1/M.
```

Conditioned on success, measuring g already gives a transporter. No HSP
solver is needed then; the missing resource is efficient preparation.

Repeating this preparation costs M trials in expectation. Applying
standard [amplitude amplification](https://arxiv.org/abs/quant-ph/0005055)
to this sampler uses order sqrt(M) calls to preparation and inverse,
assuming their coherent implementations and reflections are paid for.
For this fixed initial sampler, its two-dimensional rotation angle
is arcsin(1/sqrt(M)), so a constant-success Grover schedule needs
order sqrt(M) rotations. This is NOT a lower bound for all algorithms
that might exploit the objects' structure.

If M is polynomial in the original input length, ordinary breadth-first
orbit traversal under the supplied generators finds a transporter in
polynomial time, storing a witness word per distinct encoded object.
If M is superpolynomial, this specific target-postselection/amplification
route does not yield polynomial time. On a negative instance there is
no accepted outcome at all; unbounded postselection is not a decision
algorithm. Measuring an arbitrary orbit label produces a RANDOM coset,
not the desired tH. Mapping that random label to y is another transporter
problem, not a free classical correction.

Also, a single target coset state is not an ordinary hiding-function
oracle for a subgroup. The present checked HSP composition uses fresh
cosets, original-oracle membership checks and restricted/quotient
evaluators. A reduction must supply the actual required interface;
postselecting tH neither supplies it nor identifies a subgroup whose
generators automatically yield t. Assuming an efficient whole-orbit
canonicalization can itself hide the original equivalence problem.

## Reproducible Controls

`tests/test_nil3_application_reductions.py` checks:

1. A supplied dihedral permutation group of order 16 has lower-central
   orders 16,4,2,1, hence genuinely has class three.
2. The binary length-eight code generated by
   `e_i + e_(i+4)` for i=0,1,2 has dimension-three hull. Its canonical
   rowspace orbit labels separate precisely the stabilizer cosets.
   Direct permutation-matrix subspace stabilization gives the same H.
   Inverse conventions and a nontrivial generator-basis change are tested.
3. Exact wreath-product arithmetic verifies the iterated-commutator
   formula for p=3,5,7,11, plus the p=2 exception.
4. For p=2,3,5,7,11, the regular characteristic-p wreath has successive
   commutator-image ranks p-1,...,0 and an explicit element of order p^2.
5. The same code-action fixture supplies a target coset distinct from
   its stabilizer. Its preparation probability is exactly 1/4, and a
   generator-only orbit traversal recovers a transporter in exactly
   |orbit| times |generators| action calls.

The independent higher-class derivative and recovery controls are in
tests/test_nil3_polynomial_hiding_attack.py; their guarantees and input
limits are derived in the companion note, not from these finite counts.

`tests/test_nilpotent_linear_action_baseline.py` adds separate controls:

- Sylow-order/torus counts over prime and extension fields; CRT projectors
  including trivial factors. These arithmetic helpers are test-only.
- Actual mixed generators for UT_3(F_11) x C_5 x C_5 in GL(4,11), with
  nonabelian small-prime factor, central large-prime factor and a vector
  stabilizer splitting into factors of orders 11 and 5.
- Cross-characteristic Weyl groups at the sharp D=p boundary; the
  defining-characteristic nonabelian exception when p>D.
- A nonnilpotent dihedral matrix group whose projected generator powers
  do not define a Hall homomorphism, a noncoprime diagonal subgroup, and
  a transporter coset that is not power-closed.
- Exact coset fibres with a redundant abelian domain, without known
  minimal generator orders. This checks the reduction, not a quantum QFT.

Finite enumeration here checks the reductions, NOT Luks's complexity
theorem and NOT a quantum speedup. These are regression controls for
universal arguments, not new toy-oracle hypotheses.

Replay:

```
python -m pytest -q tests/test_nil3_application_reductions.py tests/test_nilpotent_linear_action_baseline.py
```

## Decision And Next Scientific Work

Do not market the proposed theorem as a code-equivalence, graph-
isomorphism or lattice algorithm. No such consequence has been derived.
Do not abandon the oracle theorem solely because these applications fail:
a correct, new uniform fixed-class metabelian HSP result could be a meaningful
algorithmic contribution without yet supplying a Shor-level application.

Before another application campaign, require all of the following:

1. A pre-existing computational problem with explicit input/output
   encodings, not an opaque oracle invented to fit the solver.
2. A constructible fixed-class metabelian AMBIENT presentation, with no unknown
   stabilizer generators, hidden advice, or uncharged basis acquisition.
3. A costed quantum evaluator and a reduction preserving the full input
   promise. State copies are not interchangeable with oracle access.
4. A classical-baseline comparison using the original input, including
   solvable permutation/matrix methods and low-degree reconstruction.
5. For equivalence, a transporter reduction, not just a stabilizer
   algorithm. Charge target preparation and check the new ambient group.
6. A reason the residual problem is not already solved by Shor or by a
   known HPGP algorithm.

The scope extension has not created an external application by itself.
Do not initiate more polynomial-output, regular-wreath or explicit
nilpotent linear-stabilizer campaigns merely by increasing the prime.
The remaining priorities are independent full-proof/prior-art review
of the oracle theorem and a concrete pre-existing problem that survives
these filters. A compact high-degree input or an uncovered classical
regime is only a reason to investigate, not a positive result. No central
claim or registry status is promoted by this audit.
