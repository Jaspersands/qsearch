# Class-Four HSP: End-To-End Claim Under Review

2026-10-21. PROPOSED THEOREM AND PROOF DRAFT, not an admitted result,
independently reviewed proof, novelty certificate or executed algorithm.

SOURCE ALTERNATIVE (2026-10-21): CENTRAL_REGULAR_JET_SOURCE.md is now the
preferred source for the generic nonlinear receiver. It uses central-only
Fourier with a retained regular carrier, removing variable-radical and
equivariance dependencies. This draft's irrep route and sharper class-four
phase/cost formulas remain separate; do not silently mix their budgets.
This consolidates the existing source construction and narrows the final
reduction dependencies. Passing local Lean/Python checks is not a proof
of this complete statement. No application comparable to factoring is known.

## 1. Exact Claim And Input Model

Candidate claim: the ordinary HSP in a supplied d-dimensional nilpotent
Lie algebra L over F_p, of class at most four with p>4, is solvable by a
uniform bounded-error quantum algorithm in polynomial time in d, log p
and the requested amplification parameter log(1/epsilon). The associated
group is G=exp(L), with multiplication given by truncated BCH. The output
is generators for an ARBITRARY hidden subgroup H, with failure <=epsilon.

Inputs are a valid public bracket table, prime p, and a coherent reversible
hiding oracle f with f(g)=f(g') iff gH=g'H. Addresses are unique vectors
in F_p^d. Oracle output length and its gate cost are charged separately;
the oracle may return arbitrary labels, not polynomial coordinates.
The table is promised to describe the group; finite controls are not a
validity test for an adversarial purported presentation.

Uniform sampling, subgroup bases, centers, normalizers and quotient sections
are built from public field arithmetic. No hidden projection, subgroup
generator, polynomial coefficient, coset origin, irrep matrix table or
conditional state source is supplied as advice. Fresh ordinary oracle
queries prepare the mixed coset states; their output registers are traced.

This statement deliberately STARTS WITH Lie coordinates. Extending it to
arbitrary black-box nilpotent groups requires effective presentation and
inverse-BCH conversion. The existing class-three converter is not itself
a class-four implementation. Small primes, growing class and unknown
group operations are outside this input contract.

There is now a separate proposed input reduction in
[CLASS_FOUR_BLACK_BOX_INPUT.md](CLASS_FOUR_BLACK_BOX_INPUT.md): for a
unique-encoding black-box exponent-p/class<=4 group with known p>4 and
coherent multiplication, corrected public inverse-BCH words and KNOWN
abelian-HSP kernel learning acquire an additive basis and bracket table.
Only forward encoding into the original hiding oracle is required; there
is no assumed coherent logarithm or normal-word decoder. This setup uses
no hiding-function queries but does use charged quantum group operations.
The public word evaluators are implemented; quantum setup and the whole
receiver are not. This conditional corollary does not extend to nonunique
encodings, state-only access, general exponents or unknown operations.

A subsequent conditional scope reduction is now written in
[CLASS_FOUR_PRIME_POWER_INPUT.md](CLASS_FOUR_PRIME_POWER_INPUT.md).
It acquires a mixed-order additive Lie ring for a p>4 Sylow group, extracts
local order-p subgroups by integer normal forms, and supplies public
normalizers/quotients in one chart. Known Sylow splitting and the existing
small-prime algorithm would then cover general class-four nilpotent inputs.
Quantum setup, general recursion and the complete receiver remain
unimplemented/unreviewed. This is known-method input transport conditional
on the proposed core, not an unconditional extension or novelty claim.

A separate access reduction is now written in
[STATE_SYMMETRY_COSET_TRANSFER.md](STATE_SYMMETRY_COSET_TRANSFER.md).
IID mixed-state copies, a paid controlled linear action and a GLOBAL
absolute-overlap gap supply approximate reduced coset states on every
public restriction/quotient address map. The source overhead is
O((log|G|+log B+log(1/delta))/gamma) copies per original source call,
where B caps the WHOLE workflow. This gives a conditional explicit-chart
Bose-symmetry application without preparation-inverse access. It neither
proves this receiver nor grants arbitrary quantum-oracle or DCP access.

## 2. Transverse Core: A Single Common Potential

First assume H intersect N=1 for N=G'. Write V=L/L', with a fixed public
linear section s:V->L. Then H is abelian and log(H) maps injectively to
a subspace U of V. In the proof only, choose one projection pi:V->U and
write the inverse lift as h(u)=exp(s(u)+a(u)), with a linear a:U->L'.
Fix this choice throughout all batches, irrespective of observed labels.

The group-word potential is

```
F(q)=exp(s(q-pi(q))) h(pi(q)) exp(-s(q)) in N.
```

The section-word identity in CosetMatrixSource gives the right action
`(n,q) h(u) = (n F(q)^-1 F(q+u), q+u)` in normal-first coordinates.
This is a proof identity, not an instruction to evaluate F.

Put Q=log F. Truncated BCH gives degree at most four in q. More explicitly,
modulo gamma_3(L), BCH reduces to its quadratic terms, so

```
Q(q) = a(pi(q)) + [s(q),s(pi(q))]/2   (mod gamma_3(L)).
```

To check the half coefficient, apply the class-two three-factor formula
to X=s(q-pi(q)), Y=s(pi(q))+a(pi(q)), Z=-s(q). The linear sum is a(pi(q));
the sum of pairwise brackets is [s(q),s(pi(q))] modulo gamma_3.
Every remaining term has bracket weight at least three. Since
[gamma_3(L),L'] subset gamma_5(L)=0, gamma_3(L) is central inside L'.
Consequently Q_W, in W=L'/Z(L'), is quadratic, and its central complement
Q_Z is quartic. This is the precise class-four structural fact, not a
degree observed by interpolation on one group.

### Explicit Universal Potential Certificate

Set X=s(q), Y=s(pi(q)), A=a(pi(q)), C=[X,Y]. With filtration weights
wt(X)=wt(Y)=1, wt(A)=2, the full class-four identity is

```
Q = A + C/2
    + [X,A] - [Y,A]/2 + [X,C]/3 - [Y,C]/6
    + [X,[X,A]]/2 - [Y,[X,A]]/2 + [Y,[Y,A]]/6 + [A,C]/4
    + [X,[X,C]]/8 - [Y,[X,C]]/8 + [Y,[Y,C]]/24.
```

This is obtained by expanding log(exp(X-Y) exp(Y+A) exp(-X)) through
weighted degree four. The rational coefficient identity is checked in
the faithful left regular representation of the weighted truncated free
associative algebra: ALL 49 words of weight <=4 are present. It is not
interpolation on sample inputs. The exponential/logarithm calculation is
independent of the displayed bracket expression. All denominators have
prime factors only 2 and 3, so it transports to every p>4. Interpreting
the expression as a Lie polynomial uses BCH; terms of weight >4 vanish
because A lies in gamma_2 and the Lie algebra has class <=4. No associative
matrix embedding of the actual input is required.

Every term after A+C/2 has filtration weight >=3, and therefore commutes
with all of L'. This proves the claimed noncentral quadratic projection.
Although A has filtration weight two, it is LINEAR in q; filtration weight
and polynomial degree must not be conflated. The maximum polynomial degree
in q is four, reached by the last three terms. This coefficient certificate
and the written transport argument are not a new Lean theorem.

The class boundary is genuine for this route. In the free class-five Lie
algebra on x,y, take H=exp(span(y)), s(q1,q2)=q1*x+q2*y and pi(q)=(0,q2).
This is a valid transverse cyclic H. Along q=(t,t), the degree-three
coefficient of Q is

```
C3 = [x,[x,y]]/3 + [y,[x,y]]/6.
```

Its bracket with [x,y] is nonzero in the free weight-five component
(including after reduction to any p>5). Hence this cubic coefficient
survives modulo Z(L'), so the single quadratic-jet premise fails already
on a legitimate ordinary-HSP input. This only falsifies the unchanged
class-four receiver at class five, not all possible class-five algorithms.

Exact controls: `tests/test_class_four_transport.py`. The potential and
projection remain proof witnesses, never additional algorithm inputs.

A subsequent proposal in NONLINEAR_JET_HSP_RECEIVER.md retains the cubic
jet instead of declaring it linear, uses weighted phase cancellation, then
Fourier readout and a second erasure. That would broaden the scope to
class-two derived algebra, including class five. It is under review and
does not change this counterexample or the present resource estimates.

## 3. Quotient-Image Receiver

The detailed arguments and conventions are in
[CLASS_FOUR_VARIABLE_RADICAL_SOURCE.md](CLASS_FOUR_VARIABLE_RADICAL_SOURCE.md).
The logical composition is as follows.

1. Compute Z=Z(N), W=N/Z, public bracket forms, and adapted coordinates.
   If W=0 use the scalar-source construction directly. Otherwise let
   m=dim V, w=dim W, z=dim Z; the bracket has zero common radical.
2. Apply the complete class-two normal QFT, measure (lambda,alpha), trace
   only the representation row. With H transverse to N, lambda is uniform,
   alpha is uniform conditional on lambda, and the normalized matrix kernel
   is `[q-q' in U] W(q)^dagger W(q')/(p^m*dim carrier)`. Keep varying ranks
   and radical characters. Reject only lambda=0 with a finite draw cap.
3. On canonical row-space inputs, find quartic label relations in independent
   blocks. Ignore ranks/alpha in witness selection. Multiply blocks by fresh
   uniform nonzero scalars. Prepare fresh coherent uniform q, shear and
   measure every old quotient. Full outcomes Y are conditionally independent
   uniform for product inputs, not because their marginals look uniform.
4. Form K/J and reject deficient rank. The equivariance/rank argument bounds
   failure by 1/p using B=2w(m+2)+2 blocks. Add genuine maximally mixed padding,
   extend the explicit target isometry deterministically, and implement the public
   S using the correctly phased arithmetic-qudit Clifford plan.
5. The common-jet theorem derives X displacement `(a_Y+Tq,b_Y)` for one T.
   Measure ONLY spectator carrier coordinates. All outcomes yield scalar
   kernels on U_jet=graph(-T on U), with a cubic phase linear in a fixed
   lift of the unknown polynomial coefficients. The radical character and
   Weyl half-phase are included. The retained coordinates are not measured.
6. Erase cubic, quadratic and linear phases with verified PUBLIC diagonal
   relations. Use disjoint source trees and one complete transcript. The
   lifted parameter vector and U_jet stay fixed under every shear. Erasing
   to a constant gives the ordinary mixed subgroup state for U_jet.
7. Fourier sample enough independent roots to span U_jet's annihilator;
   compute its orthogonal complement and PROJECT to V. This recovers U
   without learning T, the projection pi, a or any phase coefficient.

The physical channels are coherent field arithmetic, Fourier/phase gates,
Clifford primitives, mixed-state padding, measurements and discards. No
amplitude table from the tests is part of the algorithm. The remaining
full-composition review must verify that every use meets its cited premise.

The existing fixed-input/full-controller-transcript induction in
BOUNDED_CLASS_METABELIAN_HSP.md, together with the matrix batch and common-
jet identities, supplies the required product-source invariant. An erased
root is the SAME rho(U_jet,0) for every successful controller transcript,
so it decouples from that classical record. This is not decoupling from
an arbitrary inaccessible quantum purification. Do not condition the
source proof on discarded hiding-output labels or silently average away
a shared record BEFORE invoking a product-input identity.

## 4. Arbitrary H And A Shorter Finish

Use the known nil-2 algorithm on the original oracle restricted to N=G'
to learn K=H intersect N, with its own failure budget. N has class at most
two. On the correct-K event, compute M=N_G(K); H<=M. In Lie coordinates,
the normalizer is the solution of [x,log K] subset log K. It agrees with
the group normalizer in the present Lazard range. Work in M/K through a
public reversible representative map. One quotient-oracle call costs one
original f call plus encoding/uncomputation. Since K<=H, the lifted oracle
has exactly the required fibers. The quotient hidden subgroup is transverse
to its derived group, since M'<=G'. This restores the core promise.

After the class-four core recovers the image, let T1=HN inside this quotient
(bars suppressed). T1 is public because it is the preimage of the learned U.
Since H is abelian, T1' is generated by [H,N] and N', hence is contained in
gamma_3(G). Thus gamma_3(T1)<=gamma_4(G) and gamma_4(T1)=1: T1 has class <=3.

Now put A=T1'. It is abelian and H intersect A=1. Run the existing
class-three scalar quotient-image receiver ONCE to learn HA/A. Its
public preimage T2=HA has commutator contained in [H,A]<=gamma_4(G),
which is central in G. Therefore T2 has class <=2. Apply the known nil-2
HSP solver to the original lifted oracle restricted to T2, and lift the
answer back through M/K together with K.

This finish needs TWO quotient-image calls (class four, then class three)
and TWO known nil-2 HSP calls (initial intersection, final recovery), with
trivial/abelian cases allowed to terminate earlier. It does not depend on
the broader metabelian class-descent controller, optional HPGP learning,
or ideal Fourier samples supplied by the diagnostic report.

Allocate, for example, epsilon/4 to each of those four randomized calls.
Public restrictions and representative lifts are exact arithmetic in the
ideal analysis. A missed part of K or a lost hidden direction is a genuine
failure; generator membership checks alone do not certify completeness.

The algorithm must remain total on bad earlier histories. Put explicit
input-size polynomial clocks on every external subroutine, reject malformed
outputs, verify proposed K generators lie in the public original N, and
form their Lie closure. Check quotient/subgroup charts and each required
class drop before the next call. Membership checks cannot prove K=H
intersect N, so later HSP promises may still fail on the initial solver's
error event. All loops, random draws and gate schedules must nevertheless
have the same fixed caps on that event. Correctness is proved conditioned
on preceding successful calls and the error probabilities are then union-
bounded; off-promise execution is not allowed to run indefinitely. No
accepted-output certificate or zero-error result follows from these guards.

### Why The Public Normalizer And Quotient Are Legitimate

Let k=log K and D=ad(x). In class <=4, D^4=0, and conjugation by exp(x)
on Lie coordinates is E=exp(D)=I+D+D^2/2+D^3/6. If D preserves k,
so does E. Conversely E(k)=k implies (E-I)(k) subset k, whence

```
D = (E-I) - (E-I)^2/2 + (E-I)^3/3
```

preserves k. Thus the normalizer equation is exactly linear in x, not a
first-order approximation to group conjugation. Gaussian elimination
computes its solution space m, which is a Lie subalgebra, and k is an
ideal in m. This equivalence uses the nilpotence/characteristic promise;
it is not valid as a blanket statement for unrelated matrix groups.

Choose a public linear section r:m/k->m. For quotient addresses b,c,
equality of quotient left cosets b(H/K)=c(H/K) means
exp(r(c))^-1 exp(r(b)) is in H, because K<=H and both representatives
are in M. This is exactly f(exp(r(b)))=f(exp(r(c))). The section need
NOT be a homomorphism. Evaluate it reversibly and uncompute its coordinate
workspace; do not replace f by a freely supplied quotient state source.

K is normal in H because K=H intersect G' and G' is normal in G.
Consequently H<=M. Finally (H/K) intersect (M/K)'=1: an element of
H intersect M'K lies in H intersect G'=K. Both normalizer transport and
transversality therefore survive the quotient without a split-extension
assumption. The class-drop proof above only uses these established facts.

### Canonical-Output Amplification

For the claimed logarithmic amplification overhead it suffices instead
to run this entire procedure with constant failure <=1/3. Canonicalize
each output as the reduced row basis of its generated Lie subalgebra in
the ORIGINAL input coordinates; invalid encodings count as ABORT. Repeat
independently O(log(1/epsilon)) times and take a strict majority of these
canonical outputs, or ABORT if none exists. The correct subgroup has a
unique canonical output. A majority of correct runs suffices, so the
usual Bernoulli tail bound applies without an oracle for verifying H.
This avoids claiming that the cited QFT's inverse-polynomial-error size
bound already covers every exponentially small requested epsilon.

## 5. Explicit Resource Envelope

[Ivanyos--Santha](https://arxiv.org/pdf/1503.09016), Propositions 9/10,
Theorem 11 and Section 3.3, supply the needed diagonal solvers. For e
equations, usable arities are (e+1)^2 for squares and
(9e+1)(3e+1)(e+1) for cubes; when p=2 mod3, cubes need only e+1.
For fourth powers use the unrounded constructive recurrence
`G(4,e)^3=4^18*(e+1)^12`; when p=3 mod4, the square reduction needs
only (e+1)^2. These are known dependencies, not locally invented solvers.
The compact printed logarithmic comparison should not be used literally
as a sharper cap: with log interpreted as log2, G(4,e)^3 exceeds
4^32*(e+1)^8 for e>=128. This arithmetic observation does NOT refute
the fixed-degree polynomial-time conclusion. Our bound uses the explicit
collision construction, whose ceiling is unambiguous.

The exact schedule is implemented in
`theorems/class_four_complete_budget.py`, using integer/rational arithmetic.
It assumes valid source and capped solver contracts; it does not execute
them. With D=w(m+1), v=m+D, define

```
hW=w*binom(m+2,2), hZ=z*binom(m+4,4),
P=1+hW+hZ+hW*(hW+1)/2,
E_j=P*binom(v+j-1,j),
t=v+ceil(log_p(4/eta)), M=t*a1*a2*a3,
T=(2w(m+2)+2)*a4(z),
r_label=ceil(log_(p^z)(100T)), r_mat=ceil(log_4(4M/eta)),
Q_image <= M*r_mat*T*r_label.
```

This includes consumed zero-scale leaves and failed full attempts. Fourier
rank failure, exhausted matrix attempts, scalar solver failures and complete
instrument error each receive eta/4. The attempt bound is
3/100+1/p<1/4 after the deterministic alignment replacement in
DETERMINISTIC_JET_ALIGNMENT.md. The remaining field-sampling allocation
covers nonzero block multipliers, not a Lagrangian sampler. The error
comparison includes ABORT; never
divide by a rare branch probability. The source note gives the derivation.

For fixed eta and d=m+w+z, hW=O(d^3), hZ=O(d^5), P=O(d^6), v=O(d^2).
Hence E1,E2,E3 have bounds O(d^8), O(d^10), O(d^12). Ignoring only
logarithmic retry factors and fixed constants gives the following
CONSERVATIVE QUERY upper bounds for this quotient-image construction:

| Prime residue mod 12 | Quartic arity growth | Cubic arity growth | Q_image |
|---|---|---|---|
| 11 | O(d^2) | O(d^12) | soft-O(d^46) |
| 7 | O(d^2) | O(d^36) | soft-O(d^70) |
| 5 | O(d^12) | O(d^12) | soft-O(d^56) |
| 1 | O(d^12) | O(d^36) | soft-O(d^80) |

These are not lower bounds, observed scaling, native gate counts, or the
total HSP cost. Add the other three calls, public arithmetic, state widths,
symbolic compilation and coherent gate synthesis. All are polynomial under
their stated fixed-degree/input contracts. The current envelopes can be
astronomical even for small dimensions; no practical advantage is inferred.
Approximate cyclic transforms are standard machinery, e.g.
[Hales's QFT construction](https://arxiv.org/abs/quant-ph/0212002), Chapter
5. For a constant-error whole run, inverse-polynomial primitive accuracy
in the TOTAL input length is enough, with workspace and gate costs charged
accordingly. The required guarantee is uniform on superpositions, including
entangled inputs, not only closeness of measured Fourier distributions.
Compose the complete channels including ABORT before applying the outer
canonical-output repetition above. This draft supplies no exact native
gate exponent.

## 6. Prior Art, Impact And Kill Criteria

[ISS](https://www.irif.fr/~santha/Papers/iss12.pdf) supplies nil-2 HSP and
the subgroup/quotient-closed fixed-class reduction, not this proposed
variable-radical alignment. Its reduction is not permission to omit the
presentation/conversion costs of a larger black-box claim.
[Imran--Ivanyos](https://arxiv.org/abs/2304.08376) establishes a fixed-class,
bounded-prime result; it also already uses quotient-image descent.
The [Morales 2026 preprint](https://arxiv.org/abs/2608.05321) does not
automatically cover this exponent-p nonabelian core: its scalar p-power
action on an elementary abelian p-group is trivial; an exponent-p
quasi-Hamiltonian group is abelian because every pair of cyclic subgroups
permutes and generates a group of order at most p^2. This is a scope
comparison, not an independent review of that preprint.

A search false positive also needs care: the phrase "class 4" in
[Inui--Le Gall, Theorem 1 and Section 4](https://www.rintonpress.com/xqic7/qic-7-56/559-570.pdf)
is the fourth entry in their classification of cyclic semidirect products,
not a claim about all groups of nilpotency class four. That wording alone
does not subsume this proposal. Nor does excluding that hit certify novelty.

The possible contribution is the whole growing-prime class-four ordinary-
oracle composition, not new QFTs, Clifford synthesis, diagonal solving,
Fourier sampling or subgroup restriction. No literature search proves
novelty. Inherited abelian-oracle query separations would not establish
new nonabelian impact. Explicit linear-action applications remain subject
to CLASS_THREE_APPLICATION_AUDIT.md's classical/known-abelian filters.

SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT.md now supplies a costed conditional
reduction for formal polynomial circuit stabilizers, but no independently
motivated hard family. It also removes the large-characteristic regime
using a white-box derivative attack that does not expand polynomial
degree. This is an input-domain corollary under review, not evidence of
the receiver's correctness or a useful external speedup.
The mixed-Frobenius circuit lift further removes exposed low-lifted-degree
families even when the ordinary-degree guard fails. Missing coverage of
arbitrary succinct circuits still does not supply a natural hard problem.

High-priority falsifiers and review questions:

- A valid transverse class-four input with no SINGLE quadratic Q_W and
  quartic Q_Z in the stated chart kills the source premise.
- A defect in the row-space-invariant selection or independent-block rank
  law can make matrix success vanish with input size. Witness verification
  alone does not prove its distribution or expected success.
  EquivariantLabelSelection now checks invariant-event/record balance and
  separate-postselection factorization. It does NOT justify conditioning
  uniformity on the full new physical transcript or certify the entire
  rank probability theorem; use the ex-ante fresh-block law.
- Missing radical phases, wrong Weyl conventions, pure rather than mixed
  padding, or branch-dependent hidden jets can break composition despite
  correct matrix ranks and normalized traces.
- Efficient preparation of isolated sectors is insufficient; the entire
  instrument, full transcript and disjoint consumption must match.
- A required field/group/gate subroutine with exponential dependence on
  log p invalidates the algorithmic claim even if every finite test passes.
- A known reduction already solving this input class removes novelty.
  A classical algorithm for a proposed concrete application removes that
  impact claim without necessarily refuting the opaque-oracle construction.

The unrestricted claim stops at class four for a structural reason: in
class five, gamma_3(G) need not be central inside G', so Q_W can be cubic.
Its quadratic translated coefficients depend on Y; a quartic label relation
alone no longer certifies their joint isotropy. Do not extend by analogy.

A separate conditional derivation in
[QUADRATIC_NONCENTRAL_HSP_SCOPE.md](QUADRATIC_NONCENTRAL_HSP_SCOPE.md)
retains the explicit identity [gamma_3(L),L']=0 at any FIXED class c<p.
It derives the quadratic noncentral potential universally, but requires
degree-c central scalar erasure and up to c-2 image calls, not the cubic
backend/two-image finish here. A coupled nonmetabelian family verifies that
the scope is nonempty beyond class four; a UT6 counterexample rejects the
weaker premise that L' merely has class two. The extension is under review
and adds no implemented higher-class receiver or external speedup.

## 7. Evidence Boundary And Next Action

The existing guarded Lean modules check source-word/kernel, batch shear,
conditional scalarization and common-jet identities. The Clifford plan has
a written universal synthesis proof and independent controls. The rank and
complete adaptive resource arguments are written, not one composed Lean
theorem. There is no complete oracle-driven quantum receiver, independent
proof review, novelty certification or useful external reduction.

Next scientific action: attack this exact statement and proof chain,
starting with the distributional rank and complete adaptive composition
arguments. The explicit universal potential/normalizer transport above
removes reliance on finite-group interpolation, but has not undergone
independent review. A counterexample is more valuable than
another nearby passing fixture. Missing general-prime backend integration
belongs to mechanical follow-up, not a reason to count tests as a theorem.
