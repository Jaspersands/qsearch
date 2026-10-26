# A Structural Extension Of The Class-Four HSP Proposal

2026-10-21. CONDITIONAL SCOPE DERIVATION, UNDER REVIEW. This extends the
written receiver argument; it is not an independently verified theorem,
executed higher-class algorithm, novelty claim or useful external speedup.
The class-four source/composition dependencies remain under review.

Subsequent proposed extension: NONLINEAR_JET_HSP_RECEIVER.md replaces the
quadratic jet by a translation-closed nonlinear jet, weighted cancellation
and a second scalar erasure. It targets class-two L' without condition (A),
including class five, with different field/resource bounds. It remains
under review; the present scope and its counterexamples are unchanged.

## 1. Question And Exact Scope

The relevant boundary is not just nilpotency class. Fix c>=4 and assume a
public finite-dimensional Lie algebra L over F_p with p>c, class <=c, and

```
[gamma_3(L), L'] = 0.                                      (A)
```

Here gamma_1=L and gamma_(j+1)=[L,gamma_j]. Use the ordinary coherent
left-coset hiding oracle on exp(L), unique Lie coordinates, and arbitrary
hidden subgroup H, with all bracket arithmetic and oracle costs charged.
No hidden projection, polynomial potential or representation label is an
input. The proposed conclusion is bounded-error quantum polynomial time
in dim L, log p and the ordinary input/oracle cost, FOR EACH FIXED c.
No uniform polynomial bound for growing c is asserted.

Every class-four algebra satisfies (A); so does every metabelian algebra.
The condition also admits nonmetabelian algebras of arbitrarily high fixed
class, as the coupled family below demonstrates. It is stronger than
merely requiring L' to have class two, and should NOT be renamed as the
entire centre-by-metabelian class.
Condition (A) is publicly checkable: compute bases of L' and gamma_3(L)
from the bracket table and test all brackets of their basis pairs. This
costs polynomial field arithmetic and requires no information about H.

The new scientific claim is a structural reduction of the existing proof,
not new Fourier transforms, diagonal solving or classical group operations.
Its asymptotic comparison is with opaque-oracle HSP algorithms. It gives
no new classical hardness argument for a concrete encoded application.

[STATE_SYMMETRY_COSET_TRANSFER.md](STATE_SYMMETRY_COSET_TRANSFER.md) now
gives a conditional mixed-copy Bose-symmetry application for this SAME
explicit-coordinate scope. Its global overlap gap, IID source, controlled
action and complete-call budget are additional premises. It does not turn
the present structural proposal into an established algorithm or allow
arbitrary state-only inputs with no representation access.

## 2. Why The Matrix Part Still Has A Quadratic Jet

Put N=exp(L'). Since [L',L'] is contained in gamma_4(L), hence gamma_3(L),
(A) implies that L' has class at most two. Also gamma_3(L) is contained
in Z(L'). Jacobi shows that Z(L') is an ideal in L, so the relevant
quotient and the normal class-two Fourier transform remain legitimate.

After enforcing H intersect N=1, fix the same proof-only section s,
projection pi onto U=HN/N, and linear lift a used in the class-four draft.
The section-word potential is still

```
F(q)=exp(s(q-pi(q))) exp(s(pi(q))+a(pi(q))) exp(-s(q)).
```

Truncated BCH has degree at most c in q. Reduction modulo gamma_3 gives

```
log F(q) = a(pi(q)) + [s(q),s(pi(q))]/2  (mod gamma_3(L)).
```

Thus Q_W in W=L'/Z(L') has degree at most TWO, while the central
complement Q_Z has degree at most c. This argument is universal: it uses
the filtration and (A), not interpolation in a selected matrix group.
The common potential is fixed before any label or measurement is drawn.

The normal QFT, radical characters, selected-label equivariance and
independent-block rank proof use only the class-two N and quadratic Q_W.
Consequently their K/J maps, quartic label relation, rank bound, genuine
mixed padding and deterministic symplectic alignment are unchanged.
The same unknown linear T occurs in every scalarized packet, so support
is the common U_jet=graph(-T on U), not a higher-degree hidden graph.

## 3. What MUST Change In Scalar Erasure

The class-four shortcut to a cubic scalar phase does not extend unchanged.
The central contribution is sum_i lambda_i Q_Z(Y_i+s_i q). For c>4,
its terms of degree c need not cancel under sum_i s_i^4 lambda_i=0.
Even its degree-four coefficient can depend on the observed Y_i through
higher-degree terms. Keep ALL of these coefficients.

The Weyl/Clifford scalar terms still have degree at most three after the
same alignment. The radical-character part is quadratic. Therefore a
safe total scalar degree is c for c>=5; for c=4 the existing cubic bound
continues to apply. The scalar variables are (q,retained carrier position).

Let m=dim(L/L'), w=dim W, z=dim Z(L'), D=w(m+1), v=m+D. A sufficient
fixed unknown-parameter lift uses

```
hW = w*binom(m+2,2), hZ = z*binom(m+c,c),
P  = 1+hW+hZ+hW*(hW+1)/2.
```

Central coefficients enter linearly; only the quadratic noncentral
coefficients require pair products for the Weyl phase. Substitution and
addition do not multiply unknown coefficients during later scalar erasure.
At degree j, E_j=P*binom(v+j-1,j) public homogeneous equations suffice.
Run the existing symbolic degree-reduction argument from degree c down
to one on disjoint source trees, keeping the full controller transcript.
All packets retain the SAME unknown parameter lift and support.

This is not an assertion that the current cubic-only Python compiler
accepts higher-degree input. It does not. A future implementation needs
a degree-c central symbolic table and the corresponding erasure schedule.

## 4. Resource And Published-Dependency Audit

The fixed-degree SDE dependency is supported by
[Ivanyos--Santha, Theorem 11 and Section 3.3](https://arxiv.org/pdf/1503.09016).
For degree j use the safe unrounded arity

```
a_j(E) = (j^(j*(j-1)/2)*(E+1)^j)^ceil(log2(j+1)),  j>=2,
a_1(E) = E+1.
```

Reducing j to gcd(j,p-1) only decreases this conservative bound; degree
one uses linear dependence and an invertible power map. The cited general
construction is deterministic, unlike the smaller randomized warm-up
arities. It needs no unproved ERH or factoring of p-1. Use a proven fixed
polynomial clock, not an arbitrary timeout interpreted as a success bound.
This audit found no obstruction in that mathematical dependency. It does
not validate the repository's uncapped reference solver as production code.

For r=c (c>=5), let t=v+ceil(log_p(4/eta)) and
M=t*product_(j=1..r) a_j(E_j). Reuse B=2w(m+2)+2, T=B*a_4(z),
r_label=ceil(log_(p^z)(100T)), and r_mat=ceil(log_4(4M/eta)) when w>0.
Then M*r_mat*T*r_label is still a conservative matrix-source query cap.
Use the direct scalar branch when w=0. The existing failure allocations
remain conservative; deterministic SDE leaves its allocated failure unused.
Charge each degree-j solve, symbolic coefficient table, gate precision,
source width and complete adaptive schedule. For fixed c all factors are
polynomial; their product can be enormously larger than the class-four
bound. The degree-46/70/56/80 figures in the old artifact DO NOT apply.

The [Imran--Ivanyos dependency](https://arxiv.org/pdf/2304.08376), Theorem 2,
has zero-sum input length p^O(p log^2 p)*n^O(p log p), not poly(n,p).
Consequently its bounded-prime theorem cannot simply be promoted to a
polynomially growing-prime baseline. This corrects a tempting comparison,
not a claim that this proposal is novel or avoids all other algorithms.

## 5. Arbitrary Hidden Subgroups And Closure

Property (A) is inherited by subalgebras and quotients: their third and
second lower-central terms are contained in, or images of, those of L.
It is therefore preserved by the initial normalizer/quotient reduction.

First learn K=H intersect N with the known nil-2 HSP solver. Compute
M=N_G(K) and pass to M/K. In Lazard coordinates, the normalizer equation
[x,log K] subset log K is exact: exp(ad x) and its truncated logarithm
preserve the same subspace since (ad x)^c=0 and p>c. All arithmetic is
public. The quotient oracle uses a reversible representative section and
one original oracle call. As before, H/K is transverse to (M/K)'.

Suppress bars and set T_0=G. The first matrix quotient-image call gives
the public subgroup T_1=HG'. Because H is abelian,

```
T_1' subset gamma_3(G),  and therefore T_1' is abelian by (A).
```

For j>=1, run a scalar quotient-image call on T_j to construct
T_(j+1)=H*T_j'. Inductively T_j' is contained in gamma_(j+2)(G),
T_j has class at most c-j, and H intersect T_j'=1. Indeed the next
commutator is [H,T_j'] since T_j' is abelian, which advances the original
lower-central index by one. This is a known PUBLIC preimage once its
quotient image is learned; it does not require generators of H in advance.

Stop as soon as the ambient group has class at most two and use the known
nil-2 solver. In the worst case there are ONE matrix call, at most c-3
scalar image calls, and TWO nil-2 calls including the initial intersection.
The old two-image finish is special to c=4, not valid unchanged here.
These successive calls add costs; source-tree arities within each call
multiply. Apply the existing fixed clocks on bad earlier histories and
canonical-original-coordinate output amplification. This pass makes no
new black-box presentation, prime-power or small-prime input claim.

## 6. Nonvacuous Family And Sharp Falsifiers

Let U=ut_5(F_p), let V have basis v_0,...,v_(c-1), and let U act on V
through the coefficient of E12: [E12,v_j]=v_(j+1), ending at zero.
All other U basis elements act trivially, and V is abelian. This is a
valid semidirect Lie algebra because the E12 coefficient annihilates U'.
It has dimension 10+c and class c. Its derived subgroup is nonabelian,
with [E13,E35]=E15; nevertheless [gamma_3,L']=0. The same E12 generator
acts in both parts, so this is not merely an independent direct-product
example. No hardness claim is made for this explicit family.

For x=E12 and h=E23+v_0, consider the legitimate transverse cyclic H
generated by exp(h). Along q=t(x+h), with pi(q)=t*h, the actual potential is

```
log(exp(t*x) exp(t*h) exp(-t*(x+h)))
  = t^2*E13/2 + sum_(j=1..c-1) j*t^(j+1)*v_j/(j+1)!.
```

Its noncentral part is quadratic. Its central degree-c coefficient is
(c-1)*v_(c-1)/c!, nonzero for every p>c. Thus simply reusing the cubic
scalar stage would be wrong. Exact rational matrix checks cover c=5,6,8;
the family and formula above are defined for every c>=5.

The witness contract itself does not remove these terms. At p=257, take
scales (1,2) and central labels (-16*lambda,lambda), with lambda nonzero
on both E15 and v_(c-1). The quartic relation holds, and both Weyl sectors
have nonzero rank. The degree-c central coefficient is proportional to
2^c-16, nonzero for c=5,6,8. Shear offsets (1,0) also leave a nonzero
quartic coefficient from this term. This is a counterexample to using
the quartic equation alone as a certificate of cubic scalar degree, not
a simulation of an entire accepted multi-block packet.

The weaker condition "L' has class two" fails already for ut_6. Take
x=E12+E34+E56 and y=E23+E45. The same potential along t(x+y), pi=t*y,
has cubic coefficient C3 with [C3,[x,y]]=4*E16/3 !=0. Its cubic term
therefore survives modulo Z(L'), even though L' has class two. This is
an explicit obstruction to dropping (A), not a general HSP lower bound.

Additional kill criteria: a branch-dependent T or unknown-parameter lift;
an omitted degree-c central term; loss of product inputs/full transcripts;
input-dependent solver acceptance violating selected-label symmetry; or
superpolynomial dependence on log p hidden inside a primitive. Existing
class-four checks are necessary dependencies, not independent evidence
that this larger composition is correct. The exact tests here neither
execute the quantum receiver nor verify its full distributional proof.

## 7. Decision

The proposal can be stated structurally beyond class four, but only under
(A), with genuinely higher-degree scalar erasure and a longer finish.
This is constructive theoretical scope progress, not a breakthrough claim.
Do not create another synthetic-oracle campaign or promote a registry
candidate from these controls. The external-application classical filters
remain in force, and no independently motivated hard instance is supplied.
Next: challenge the complete structural theorem and its novelty/impact;
do not relax (A) or claim growing-class efficiency from this derivation.

Validation: 12 new exact controls and 162 connected Python tests pass,
including source, shear, common-jet, Clifford, scalar-erasure, class-four
budget and metabelian-interface tests. Syntax, generated formal crosscheck,
site JS/site checks, registry validation and whitespace pass. No new Lean
proof/build or full-repository test run; no higher-class source execution.
