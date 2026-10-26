# Class-Three Normal Source And Full-Jet Receiver

2026-10-21. CONSTRUCTIVE PROPOSAL, UNDER REVIEW. The public algebra and
adversarial tests are implemented, not a quantum receiver. No independently
validated new algorithm, novelty certificate, useful external speedup or
central-registry admission is claimed. Read this before extending the old
Weyl compiler beyond its class-two-normal premise.

## 1. The Change That Matters

The previous source retains N/Z(N) and has a Weyl gauge when N is class
two. UT7 has a genuinely class-three derived subgroup: with Eij denoting
matrix units, [[E13,E35],E57]=E17. Its regular gauge has nonscalar
commutators, so unchanged Weyl alignment is invalid.

There is a more constructive alternative than merely calling this gauge
Clifford-valued:

1. Fourier-transform a further abelian carrier coordinate B, but KEEP its
   frequency mu coherent. The remaining action is translation plus a
   quadratic carrier phase, not an arbitrary affine permutation.
2. Retain the FULL Taylor jet of the translated coordinates, including the
   highest-degree part. Align translations with a public GL permutation.
   There is no top-displacement cancellation or isotropy requirement.
3. Erase the resulting weighted polynomial phase, Fourier-read every jet
   character, and erase the ordinary degree-D residual. The second erasure
   is now D through 1, NOT D-1 through 1.

This removes the matrix-leaf label SDE and general symplectic alignment at
the price of a larger jet and higher phase-erasure degree. It does not
remove the phase-erasure SDEs, coherent oracle access or source consumption.
It is not a universal resource improvement over the class-two variant.

## 2. Input Model And Proposed Scope

2026-10-22 scope investigation: METABELIAN_DERIVED_HSP.md derives a
different right-fiber induced source for metabelian N of larger class.
It includes an actual ambient class-nine/derived-class-four witness and
noncentral Fourier-side falsifiers. This is an UNDER-REVIEW extension,
not implemented by the class-three compiler below. It requires higher
hidden-parameter lifts, different degree/resource bounds and a larger
recursion cap. Do not relax this module's guards based on that note.

Public finite-dimensional Lie algebra L over F_p, fixed nilpotency class
c>=4, ordinary coherent hiding-function access on exp(L), unique Lie
coordinates, and derived algebra N=L' of class at most THREE. Let
D=c-2 and conservatively require p>max(c,3D). All arithmetic, Fourier
precision, fresh queries, rejected batches and control workspace are paid.

The proposed conclusion, contingent on the whole reduction and composition
proof, is bounded-error quantum polynomial time in dim L and log p for
each fixed c. This includes every ambient class <=7 since
gamma_4(L') is contained in gamma_8(L). It is not a result for growing c,
arbitrary encodings, prime-power exponent or DCP. Class-two normal groups
are now supported by B=0 in the SAME full-jet compiler. An abelian normal
group uses the scalar phase-erasure branch; an abelian ambient group uses
ordinary abelian HSP. Section 7.1 makes that recursion explicit.

Initially assume H intersect exp(N)=1. Then H is abelian. The SAME
proof-only potential g(q) from NONLINEAR_JET_HSP_RECEIVER.md Section 2
exists without requiring N to be class two: it is a section-word identity.
The raw ordinary-coset block is the regular action of g(q)^-1 g(q'). No
coherent evaluator for g, projection onto U, or polynomial coefficients
is supplied to the receiver.

Put C=Z(N), B=(N'+C)/C, A=N/(N'+C), with public linear sections.
Dimensions are z,s,r respectively. Bracket arithmetic constructs these
spaces in polynomial time. Coordinates Q=log g=(a,b,c0) satisfy
deg(a),deg(b)<=D and deg(c0)<=c: homogeneous coefficients of degree >=c-1
lie in gamma_(c-1)(L), which commutes with N and thus lies in C.
Using an arbitrary smaller central subspace would NOT justify that bound.

INPUT-DEGREE UPDATE: AMBIENT_SECTION_POTENTIAL.md gives the full Lie-word
argument from log(exp(X) exp(Y+Z) exp(-X-Y)), with linear X,Y,Z and Z in N.
AmbientPotentialFiltration.lean checks long-word centrality and projected
polynomial degree. A separate exact free-associative coefficient verifier
checks the actual section word through class seven, independently of
input dimension and hidden values. A UT7 coefficient E16/30 shows why
using Z(L) instead of Z(N) fails. BCH/Lazard remains a published dependency;
the Python certificate and all quantum stages are not one Lean theorem.

## 3. Exact Regular Gauge

Write the public structure tensors as

```
[A,A]_B=beta, [A,A]_C=gamma, [A,B]_C=delta,
[B,B]=0, [C,N]=0.
```

Beta and gamma are alternating; Jacobi is
delta(a,beta(a',a''))+delta(a',beta(a'',a))+delta(a'',beta(a,a'))=0.
The BCH product for g=(a,b,c0), h=(x,y,z0) is

```
g*h = (a+x, b+y+beta(a,x)/2,
       c0+z0 + (gamma(a,x)+delta(a,y)-delta(x,b))/2
              + (delta(a,beta(a,x))-delta(x,beta(a,x)))/12).
```

Apply negative Fourier to C and negate the remaining log coordinates.
Equivalently invert the full group coordinate, then apply positive C
Fourier. Each measured lambda in C* has probability p^-z, including zero.
The retained carrier has p^(r+s) basis states, not an irreducible dimension.
The regular gauge is

```
W_lambda(g)|x,y> = omega^R(g;x,y) |x+a, y+b+beta(a,x)/2>,
R = lambda(c0)
  + lambda(gamma(a,x)+delta(a,y)-delta(x,b))/2
  + lambda(delta(a,beta(a,x))-delta(x,beta(a,x)))/12.
```

Therefore the conditional mixed source is

```
rho[(q,t),(q',t')] = p^-(m+r+s) [q'-q in U]
                     (W_lambda(g(q))^dag W_lambda(g(q')))[t,t'].
```

This is a reducible regular-sector source. d^2/|N| is the wrong label
probability. The construction measures no radical, row or B coordinate.

### Complete Oracle-To-Central Instrument

Formal/CentralRegularSource.lean now proves the central-source step from
verified public charts. It reuses CosetMatrixSource's already proved
ordinary hiding-output trace and common section-word identity rather than
assuming a polynomial oracle or repeating those arguments.

For a public central-fiber chart N=T x C, write
`chart^-1(x,z)=central(z)*section(x)`, with central(C) commuting with N.
The actual public Fourier amplitudes, INCLUDING normal inversion, are

```
K_chi[x,n] = |C|^(-1/2) [x=pr_T(n^-1)] chi(pr_C(n^-1)).
sum_chi K_chi^dag K_chi = I_N.
```

Here chi ranges over ALL additive characters of C. Completeness follows
from finite-abelian dual orthogonality, not from assuming irreducibility,
a full nonabelian QFT, or a claimed probability for one sector. The
normal-coordinate inversion changes the right-regular density relation
into the left-action monomial convention of Section 3.

Let `(a_h(x),c_h(x))=chart(h*section(x))`. The operator
`W_chi(h)|x>=chi(c_h(x)) |a_h(x)>` is derived to be a unitary representation.
The actual two-sum source contraction, after tracing the hiding output, is

```
B_chi[(q,x),(r,y)]
 = |G|^-1 [r-q in U] W_chi(g(q)^-1*g(r))[x,y]
 = |C|^-1 (|V| |T|)^-1 [r-q in U]
     (W_chi(g(q))^dag W_chi(g(r)))[x,y].
trace B_chi = |C|^-1.
```

Thus the central label really is uniform, including the trivial label.
The hidden retraction, parametrization of ALL H and potential appear only
in the correctness side; no potential query enters the instrument. The
class-three BCH central coordinate is the displayed phase R(g;x,y).
The universal chart theorem is not a separate kernel derivation of every
input Lie algebra's public chart or the scalarized extra-B-Fourier compiler.

Seven axiom guards permit only standard Lean axioms. Three new controls
start with actual gH labels (right H action), a nonlinear public normal-first
section and proper U. Class-three, vector-center and abelian instances
check all sectors, two hidden projection gauges and cross-sector zeros;
missing inversion and the wrong d^2/|N| mass are falsified. These are
mathematical fixtures, not new candidate oracle problems.
A fourth control has a nontrivial hidden central intersection: characters
nontrivial on that intersection have zero mass. Thus uniform labels cannot
be used before the transverse preprocessing has been justified.

RETAINED-FOURIER UPDATE: RETAINED_FOURIER_SOURCE.md and
Formal/RetainedFourier.lean identify linear frequencies mu:B->F with all
additive characters under a FIXED nontrivial base character. Both coherent
Fourier orthogonality laws and the actual BCH-source two-sum contraction
are checked, retaining the shifted frequency in the phase. The base
character is not lambda: zero measured central labels remain valid.
Actual class-three gH controls with scalar/vector centers agree through
the combined C/B transforms; measuring mu or using its old frequency fails.
These generic-normal-subgroup fixtures do not certify N=L' or the full
input model. The batch-shear/alignment and adaptive protocol composition
remain open. The corrected v2 central
audit explicitly separates genuine coset preparation from an assumed
potential kernel and nonlinear-chart controls from linear-section bounds.

VECTOR-SOURCE COMPOSITION UPDATE: VECTOR_CENTRAL_ORACLE_SOURCE.md and
Formal/VectorCentralSource.lean construct the actual vector-center BCH
group and public central chart. ALL linear projections prove the vector
group law; a single character is not assumed faithful. Complete central
indexing and the actual coherent B contraction yield a derived unitary
monomial representation. original_source composes the ORIGINAL hiding-
output trace and shared section-word identity into
`|C|^-1 [r-q in U] (|V||A||B|)^-1 W(g(q))^dag W(g(r))`, without a
potential evaluator in the operational definition. The physical |C|
survives even lambda=0. Ten guards cover this composed source result.
The ambient input-to-chart refinement and full batch/GL/erasure/adaptive
controller are not all one kernel-checked theorem, nor an executed solver.

This closes exact central-instrument completeness and its source formula,
not efficient gate extraction, input-to-chart/degree proofs, adaptive
freshness, rank probability or the complete algorithm. Ordinary Fourier
analysis of coset states is established prior art, for example
[Krovi and Roetteler](https://arxiv.org/abs/0810.3695). No new algorithm or
novelty claim follows from this verification.

## 4. The Extra Fourier Transform

Conjugate W by I_A tensor F_-^B, where
F_-|y>=p^(-s/2) sum_mu omega^(-mu.y)|mu>. Define

```
l_lambda(a)(y)=lambda(delta(a,y))/2,
d(a,b,x)=b+beta(a,x)/2,
R0(g;x)=R(g;x,0).
```

Summing over y forces mu'=mu+l_lambda(a). The exact action becomes

```
W'_lambda(g)|x,mu> = omega^Phi(g;x,mu)
                     |x+a, mu+l_lambda(a)>,
Phi=R0(g;x) - (mu+l_lambda(a)).d(a,b,x).
```

Thus its displacement is D_lambda*a with D_lambda=(I_A,l_lambda).
This is injective for EVERY lambda. Its scalar phase has carrier degree
at most two and group-parameter degree at most two. Products such as
delta(a,beta(a,x)) are quadratic, not cubic, in unknown coefficients.

Mu is a quantum coordinate, not a measured representation label. In the
filiform control, measuring it annihilates a nonzero hidden-support
off-diagonal block. B-elements act by nonconstant diagonal phases; this
does not contradict the prior nonscalar-commutator obstruction to Weyl.

## 5. Full Jet And Public GL Alignment

Retain all coordinates

```
F_(alpha,k,a)(q)=sum_|nu|=k binom(alpha+nu,nu) theta_(alpha+nu,a) q^nu,
1<=k<=D, |alpha|+k<=D, 1<=a<=r.
ell=binom(m+D,m+1), J=r*ell.
```

Now a(Y+s0*q)=a(Y)+sum_(alpha,k) s0^k Y^alpha F_(alpha,k)(q), with
NO discarded highest-degree term. The old public Taylor transport works
also for k=D: F(Y+s0*q)=F(Y)+A(Y,s0)F(q). A is triangular by weight k,
has diagonal s0^k, and is invertible when s0!=0.

Take b0 independent raw sources. Draw independent nonzero scales s_i,
then use a fresh uniform coherent q register and measure ALL old quotient
registers after q_i -> q_i-s_i*q. The matrix-shear identity gives
independent uniform Y_i conditional on prior labels and scales. Do not
replace this by a pivot shear with a fixed Y row.

The stacked displacement coefficient map is

```
Jmat_i[(alpha,k,a)] = s_i^k Y_i^alpha D_lambda_i[:,a].
Phi_i[(alpha,k)] = s_i^k Y_i^alpha.
```

Full scalar feature rank ell implies rank(Jmat)=J through its identity A
rows, irrespective of labels. It also implies R=b0*(r+s)>=J. Complete
the columns of Jmat to a public basis T of F_p^R and use L=T^-1:
L*Jmat=(I_J,0). The module uses a pivot-row minor and standard complement
columns. This is exact arbitrary-precision field arithmetic, not numerical
rank or hidden advice. Applying |t> -> |L*t> costs polynomially many
reversible field operations (e.g. Gaussian elementary gates).

The transformed displacement is an unknown constant plus (F(q),0).
No commutator relation, isotropic subspace, radical selection, artificial
mixed padding, or implementation of the unknown W(g(q)) is required.

Dividing each scalar feature row by s_i gives all monomials of degree
<=D-1 in (s_i,Y_i). For independent draws, a union bound gives

```
Pr[rank Phi<ell | arbitrary prior labels]
 <= (p^ell-1) ((D-1)/(p-1))^b0,
b0=(ell+1)*bit_length(p)+2  => bound <=1/(4p), when p>2D.
```

The bound is BEFORE rank acceptance, not conditional on an observed
accepted transcript. A failed batch is consumed and retried in full.

## 6. Scalarization And Both Erasures

Conjugating by the GL permutation preserves the monomial phase exactly:
Phi_i is evaluated at (L^-1 t)_i; no projective Clifford phase is dropped.
Measure the R-J spectators, retain every outcome zeta. Each is uniform.
Direct matrix contraction gives

```
rho[(q,t),(q',t')] = p^-(m+J) [q'-q in U]
                    [t+F(q)=t'+F(q')]
                    omega^(P(q,t)-P(q',t')),
P(q,t)=-sum_i Phi_lambda_i(g(Y_i+s_i*q); (L^-1(t,zeta))_i).
```

The compiler checks the COMPLETE symbolic translation identity, not just
its top coefficients. There is no extra symmetric-Weyl -X.Z/2 term: that
phase belongs to a different source convention.

Give q weight 1 and jet coordinate (alpha,k,a) weight k. Every old carrier
coordinate after L^-1 has weight <=D. The largest terms are a*a*x,
a*x*x, and mu*a*x, of weight <=3D. Hence e=max(c,3D) bounds P.
Its fixed parameter schema is coefficients of Q_A,Q_B,Q_C plus their
quadratic lift. Public affine pullbacks do not raise parameter degree.

UNIVERSAL COMPILER UPDATE: Formal/ClassThreePhaseBounds.lean lifts the
actual bundled beta/gamma/delta maps to polynomial coefficients and proves
evaluation equal to the exact source phase. It constructs every component
as a PUBLIC shifted monomial sum with formal, shared unknown coefficients,
and each carrier row as a PUBLIC affine form including spectator offsets.
The actual negative batch sum has operational weight <=max(c,3D) and
parameter degree <=2. Neither conclusion is assumed in the batch theorem.
Central labels are public coefficients, not fresh hidden parameters.

Independent SymPy expansion without the compiler's quadratic cutoff
matches the entire expression at small and 127-bit primes, with vector
centers, nonzero gamma, zero labels and spectator contributions. Both
the 3D bound and c>3D case are attained. In the filiform example,
a=(h*q^D,0), x=(0,t), b=c0=mu=0 gives Phi=-h^2*q^(2D)*t/6.
If a purported alignment substitutes t=h, the parameter degree becomes
three. Publicness is essential, not a software provenance convention.

This proves the SOURCE COMPILER estimate given degrees D,D,c of the
potential components. The separate ambient Lie-word argument above now
derives those degrees for a genuine class-c Lie input and full-center
chart. The compiler module itself does not identify that chart, implement
the SDE, or compose all physical stages.

Apply weighted erasure through e,...,1 with the same full-jet transport.
The arbitrary-monomial-gauge contraction and nonlinear support identity
in Formal/NonlinearJetChannel.lean are generic interfaces. Separate
ClassThreeMonomial, FullJetAlignment, ClassThreePhaseBounds and
FullJetWeightedErasure modules prove the indicated local algebra,
alignment, degree and erasure laws. Their existence is not yet one
composed original-input-to-output algorithm theorem.

After full weighted erasure, negative Fourier of t gives eta.F(q), for
every retained eta. This has ordinary degree <=D and can attain D.
Ordinary erasure must run D,...,1. Only then does quotient Fourier sample
U-perp without the unknown polynomial phase. Measuring mu early, reading
the jet early, or dropping that last ordinary stage invalidates the route.

## 7. Complete Resource Substitutions And Recursion

2026-10-22: FULL_JET_ADAPTIVE_RESOURCE_THEOREM.md supplies a single capped
schedule, the conditional-history freshness/rank argument and a joint
instrument error budget. It also derives smaller STAGE-SPECIFIC equation
counts from three invariant q/jet/hidden-parameter support blocks. The
new standalone certificate uses them by default. The formulas immediately
below remain valid GENERIC comparison bounds, not the preferred counts.
The refinement is a written proof plus exact symbolic controls, not a new
Lean theorem or an executed receiver. It does not remove either tree or
reduce the maximum erasure degree.

Use the bounded composition/error argument in NONLINEAR_JET_HSP_RECEIVER.md
Section 10, with the following changed quantities, not its old leaf costs:

```
h=(r+s)*binom(m+D,m)+z*binom(m+c,m), Hlift=1+h+h*(h+1)/2,
v=m+J, E_w <= Hlift*binom(v+e,e), E_o <= Hlift*binom(m+D,m),
a_1(E)=E+1,
a_j(E)=(j^(j*(j-1)/2)*(E+1)^j)^ceil(log2(j+1)), j>=2,
M=t * product_(j=1..D) a_j(E_o) * product_(j=1..e) a_j(E_w).
```

These intentionally overcount constraints; exact leading-column counts
may be lower. M is the number of matrix leaves for t final Fourier samples.
The SDE arity uses the explicit collision recurrence in
[Ivanyos--Santha, Theorem 11 and proof of Theorem 3](https://arxiv.org/html/1503.09016v2),
with the standard gcd(j,p-1) reduction when needed. It is a published
all-input fixed-degree algorithm, NOT a backend supplied by this module.

Each matrix attempt consumes b0 ordinary queries. There is no label
rejection and no degree-2D source-level SDE. Cap each nonzero scale draw
at ceil(log_p(8*b0)) uniform field draws. Scale exhaustion is <=1/8 and
rank failure <=1/(4p), so a trial succeeds with probability >1/2 under
the stated product-source premises. With

```
retries=ceil(log2(4*M/epsilon)),
raw queries <= M*retries*b0,
```

the leaf exhaustion union bound is <=epsilon/4. Choose enough final
annihilator samples and budget bounded binary field rejection and joint
instrument error as in Section 10; do not divide an unconditioned error
budget by an uncharged postselection probability. Depth-first live-source
storage is bounded by the sum of stage arities times register width, plus
the current matrix batch; gate/oracle ancillas are additional.

Every exponent above is constant only when c is fixed. These bounds can
be astronomically impractical. Removing the leaf SDE does not justify a
claim of lower total complexity: e and the second tree have increased.

### 7.1 One Well-Founded Arbitrary-H Algorithm

AUDIT UPDATE: a separate unexamined class-three HSP subroutine is not
needed as an AXIOM. Unroll it using the same scalar image primitive and
abelian base case. This removes an opaque dependency from the proposed
proof; it does not independently establish the resulting algorithm.

Use Lie notation for subgroups via Lazard correspondence. Input is
(L,f), class(L)<=c, class(L')<=3, in the explicit prime-field model.

```
Solve(L,f):
  if L is abelian: return AbelianHSP(L,f)
  N := L'
  K := Solve(N, f restricted to exp(N))
  M := {x in L : [x,K] is contained in K}
  S := M/K, with a public linear section and the induced hiding oracle
  while S is nonabelian:
    U := Image(S, induced f)  # image of the CURRENT hidden subgroup in S/S'
    T := inverse image of U in S
    require class(T) < class(S); otherwise ABORT
    restrict to T and recompute its Lie data
  R := AbelianHSP(S, induced f)
  lift R through the recorded public maps and include generators of K
```

Each loop uses a fixed image-recovery cap. Validated early class descent
from an overestimate is optional, not necessary for this proof. Every
algorithmic oracle below is a restriction/clean section of ORIGINAL f.
There is no state-creating oracle for the unknown subgroup or free
coherent evaluation of its potential.

**Well-founded call.** If L has actual class c0>=2, then
class(L')<=floor(c0/2), since gamma_j(L') is contained in gamma_(2j)(L).
Thus the single recursive intersection call strictly lowers class. Under
the standing promise, that callee has class at most THREE. Its own
derived algebra is abelian; its intersection call is ordinary abelian
HSP. No nil-2 or class-three HSP theorem is assumed as a black box.

**Three image branches, no missing degeneracy.**

- S' abelian: central Fourier measures all normal coordinates. The source
  is rho(U,lambda.Q), deg Q<=class(S). Ordinary scalar erasure through
  that degree gives U-perp samples. A common parameter basis of all
  normal-coordinate polynomial coefficients is sufficient; no jets or
  irreducible decomposition are needed. This is the full branch from
  BOUNDED_CLASS_METABELIAN_HSP.md, not its older line-only implementation.
- S' class two: C=Z(S'), B=0, A=S'/C. Set beta=(), delta=0 with empty
  B rows. The formulas above become translation by a and phase
  lambda(c0)+lambda(gamma(a,x))/2. The same full-jet GL alignment applies
  WITHOUT a label relation. The symbolic compiler now accepts precisely
  this zero-dimensional B case; no phantom Fourier register is added.
- S' class three: use the complete construction in Sections 2-6. Its
  phase erasure has degree e=max(c0,3(c0-2)).

For the second branch the sharper weight bound is max(c0,2(c0-2)); using
the conservative 3D bound remains correct but more expensive. A growing
prime satisfying the top-level bound also satisfies every smaller
branch's bound. If S' is zero, S was already an abelian base case.

### 7.2 Correct Quotient And Strict Descent

On the event that K is correct, K=H intersect N is normal in H. Hence
H<=M=N_L(K), and K is an ideal in M. The normalizer formula holds beyond
class three: ad(x) preserving K implies exp(ad x) preserves it;
conversely the finite logarithm of exp(ad x)-I recovers ad(x). The
nilpotence and p>c bounds justify these inverse polynomials.

IMPORTANT CORRECTION TO AN INHERITABLE ASSUMPTION: when N is nonabelian,
N need NOT be contained in M. Do not form N/K or assume the old normal
subgroup survives unchanged. What is actually defined is

```
S=M/K,
S'=(M'+K)/K contained in (N intersect M)/K,
(H/K) intersect ((N intersect M)/K) = 0.
```

Thus the hidden subgroup in S is transverse to its RECOMPUTED derived
ideal. The derived ideal remains class <=3 because it is a subquotient
of N. In UT7, take H=span(E12,E13), K=span(E13). E35 is in N but not M,
since [E35,E13]=-E15 is outside K. The new regression checks this exact
failure, the correct quotient containment, and subsequent class descent.

Now rename the current hidden Lie subalgebra h and the current algebra S.
Transversality implies h is abelian. The exact image preimage is T=h+S'.
Even when S' is NONABELIAN,

```
[T,T] = [h,S']+[S',h]+[S',S'] contained in gamma_3(S),
gamma_j(T) contained in gamma_(j+1)(S) for j>=2.
```

The term [S',S'] must not be omitted; it lies in gamma_4(S), which is
contained in gamma_3(S). The induction then uses T<=S. Consequently T
has class at most class(S)-1. Every later restriction still contains h,
and its derived ideal is contained in the first S', so transversality
persists. No new intersection/normalizer call is required inside the loop.

If an exact-source sample nullspace Uhat strictly contains U, its preimage
still contains h. It is safe to stop at a PUBLIC strict class drop without
knowing whether Uhat=U. A mere dimension decrease is not the stated class
certificate. The worst-case fixed cap is justified by exact image recovery.

At the abelian finish, lift the learned subgroup through each restriction
and section and adjoin K. Its image is H/K and its kernel contains K,
so it is H. Membership of a few generators alone never certifies this
completeness statement. An earlier incorrect K may break the oracle
promise; the global proof counts that as an earlier failure rather than
pretending subsequent membership checks necessarily detect it.

### 7.3 Whole-Algorithm Cost And Error

For top-level c>=4 there are at most c+1 image calls and THREE abelian
HSP calls. To see this, the top-level loop has at most c-1 image calls.
The intersection solver has ambient class <=3 and at most two image
calls; its own intersection is abelian. Its final solve and the main
final solve are also abelian. Lower-class cases only reduce these counts.

Let B_c(n,p,eta) dominate BOTH scalar and full-jet image query envelopes
over all public dimensions <=n and classes <=c. The scalar envelope is
t*product_(j=1..c0) a_j(E_j), with the same fixed-degree SDE and no
matrix-rank trials. For full jets use Section 7's M*retries*b0, including
both erasure trees. Then a conservative total query bound is

```
Q_total <= (c+1)*B_c(n,p,eta) + 3*Q_abelian(n,p,eta).
```

This is ADDITIVE across group reductions. It is not an excuse to omit
the real products INSIDE each erasure tree. Each restricted/quotient
query is ONE original f query with public reversible compute/uncompute
of its argument. In explicit Lie coordinates these lifts compose linear
sections and subspace inclusions; sections need not be homomorphisms.
K contained in the hidden subgroup is what makes the induced oracle
well-defined on a quotient. Group operations still use charged BCH.

For a target error epsilon, assign eta=epsilon/(2*(c+4)) to each
probabilistic primitive and reserve the rest for implementation error
not already inside that primitive's complete-instrument allowance.
Conditioning on no prior error, each call has the promised source and
uniform cap. A first-error union bound covers all adaptive calls. Do not
multiply branch-conditional error bounds or divide by rare outcomes.

Every branch is capped even on invalid earlier answers: validate supplied
Lie spans, normalizer ideals, field sizes and class bounds, and ABORT on
malformed public data. Such checks do not prove a hidden subgroup answer
complete. The complete CQ product induction, source ownership, binary
sampling and approximation analysis from the earlier controller remain
required. Keep parameter bases separate for different image calls.

For fixed c all table dimensions, arities, call counts and precision bit
lengths are polynomial in n and log p. The constants are enormous. This
is a complete WRITTEN reduction to abelian HSP, public group/linear algebra,
the SDE algorithm and the stated phase-channel identities. The new global
composition is not machine-checked or executed by this repository.

## 8. Attempts To Kill The Proposal

- WRONG SOURCE: actual ordinary regular kernels are transformed directly,
  not assumed to be polynomial-phase oracles. All center sectors, lambda=0
  and reducible normalization are checked. General section/source
  composition still needs independent review.
- WRONG REPRESENTATION: independent UT4 matrix exponentials check BCH,
  including a nonzero gamma; random action compositions check phases.
  The actual UT7 derived algebra has dimensions (r,s,z)=(9,2,4), exact
  center and a nonzero triple bracket. It passes the same identities.
- LOST COHERENCE: measuring the B frequency removes an off-diagonal
  source block in the control. The algorithm explicitly keeps it quantum.
- HIDDEN ADVICE: alignment receives only structure tensors, center labels,
  scales and measured outcomes. Hidden coefficients appear only as formal
  parameter indices. Truth-based fixture evaluators are not controller APIs.
- INCOMPLETE JET: exact coefficient tests include k=D and multivariate
  transport. Omitting the top term defeats the proposed translation
  identity. A retained top-character test has residual degree exactly D.
- BAD SAMPLE MODEL: fixed scales/outcomes can be rank deficient. Fresh,
  disjoint sources and pre-outcome scale choice remain essential. Python
  transcript validation cannot certify quantum independence.
- CHEAP PHASE CLAIM: symbolic compilation retains quadratic parameter
  products, spectator-dependent terms and weight 3D. It checks cancellation
  coefficientwise, not at sampled hidden coefficients.
- DEQUANTIZATION: a Clifford description of each KNOWN element does not
  supply g(q) or simulate the coherent opaque hiding oracle. Conversely,
  explicit sparse Pauli objects and polynomial stabilizer encodings remain
  subject to the classical filters in CLASS_THREE_APPLICATION_AUDIT.md.
  This pass creates no access-matched hard external problem.
- PRIOR ART: diagonal-equation phase cancellation and polynomial graph
  methods are established techniques, not claimed inventions. The
  [multivariate HPGP oracle result](https://arxiv.org/abs/1107.2189) and
  [constant-prime nilpotent HSP result](https://arxiv.org/abs/2304.08376)
  must remain in the comparison. The former does not immediately supply
  the unknown-proper-U mixed-state interface; the latter has a different
  prime regime. These distinctions do NOT prove novelty.

The route should be retracted or narrowed if a same-instance source
counterexample breaks the common potential, if alignment requires hidden
data, if a phase needs an unbounded parameter lift, if the complete
controller loses product-state provenance, or if access-matched prior art
already yields the claimed scope. It should be deprioritized for impact if
no useful problem survives the classical application filters.

### Current Prior-Art Collision Check

The September 2026 version of
[Morales, Theorems B and C](https://arxiv.org/html/2608.05321v2) gives
scalar-action abelian-by-cyclic and structured quasi-Hamiltonian cases.
These do not DIRECTLY contain the present UT7 growing-prime scope.
Our structural inference is that the former groups are metabelian,
whereas UT7 has nonabelian derived group. UT7 is not quasi-Hamiltonian:
its subgroups generated by I+E12 and I+E23 do not permute, since their
two ordered products differ in the E13 entry. The same obstructions
persist in UT7(F_p)^k with arbitrary hidden subgroups. This is a
scope distinction, NOT proof that no reduction to those algorithms exists
or that the proposal is novel. The literature search is not exhaustive.

## 9. Implementation And Next Scientific Question

NEW theorems/class_three_monomial_jet.py: validated structure tensors,
known-element BCH/Fourier fixtures, FullTaylorJetChart, exact public GL
alignment, conditional rank schedule, full symbolic phase compiler.
NEW tests/test_class_three_monomial_jet.py: 31 tests covering the controls
above, including degree-four full jets, arbitrary-precision prime data,
the class-two B=0 branch, the nonabelian normalizer counterexample, and
agreement with the checked linear-plus-bilinear parameter decomposition.
The existing weighted-erasure and character-residual APIs are reused.

This is stronger than a compact descriptor or a nearby no-go lemma: it
supplies a proposed public source-to-nonlinear-graph mechanism past the
previous class-two-normal obstruction. It is still not an executed HSP
solver. No generic SDE implementation or central claim has been added.

### Kernel-Checked Source Algebra

Formal/ClassThreeMonomial.lean now proves the coordinate product's
associativity, identity and inverse laws from the bilinear structure maps,
alternation and Jacobi. Its monomial phase satisfies

```
Phi(h,t)+Phi(g,T_h(t)) = Phi(g*h,t).
```

The difference before applying Jacobi is exactly one sixth of
delta(a,beta(b,x))+delta(b,beta(x,a))+delta(x,beta(a,b)). No action law or
vanishing commutator is assumed. Translation bijectivity and inverse-phase
cancellation are checked as well.

The SAME phase has a bundled, universal coefficient-degree certificate:

```
L_t(a,b,c0) = c0-mu(b)
  +(gamma(a,x)-delta(x,b)-mu(beta(a,x)))/2
  -delta(x,beta(a,x))/12,
Q_t((a,b,c0),(a',b',c0')) = -delta(a,b')/2-delta(a,beta(a',x))/6,
Phi(g,t)=L_t(g)+Q_t(g,g).
```

Here c0, gamma and delta are already evaluated by lambda. L_t is a Lean
linear map and Q_t a bundled bilinear map. This certifies the quadratic
lift in UNKNOWN group parameters, not merely behavior on a finite grid.
ClassThreePhaseBounds now separately certifies weighted degree after
public polynomial substitution and affine alignment as described above.

The separate partial-Fourier theorem starts from the actual two register
sums for a modulation ell and displacement d. It derives the output
character nu=mu+ell with phase alpha*conjugate(nu(d)), including the
normalization. This pins the shifted-frequency term and sign in Section 4.
It assumes no nonzero lambda or positive B dimension. By itself it does
not prove the central-source instrument or a compiled quantum Fourier
circuit. The separate CentralRegularSource theorem in Section 3 derives
the former from verified public charts; gate extraction remains outside it.

Seven headline axiom guards permit only standard Lean axioms; no `sorry`
or new logical axiom is used. The field identities need characteristic
different from two and three. All original stronger algorithmic field,
filtration, source-access and SDE conditions still apply. New Python
regressions connect the fixture formula to L_t+Q_t at small and 127-bit
primes, including gamma!=0, lambda=0 and B=0. They are NOT a formal
Python-to-Lean refinement or execution of the receiver.

### Kernel-Checked Full Taylor Transport

Formal/FullTaylorTransport.lean removes two assumptions from the nonlinear
measurement interface: the curve transport law and invertibility of its
public linear map. For one component, let Y be m formal variables and s
one additional formal variable. The coefficient polynomial

```
J_Q(q)(Y,s) = Q(Y+s*q)-Q(Y)
            = sum_(alpha,k>0) F_(alpha,k)(q) Y^alpha s^k
```

has exactly the full jet coordinates in Section 5. Expanding a monomial
theta_(alpha+nu) (Y+s*q)^(alpha+nu) gives
`F_(alpha,k)(q)=sum_|nu|=k binom(alpha+nu,nu) theta_(alpha+nu) q^nu`.
This is a coefficient identity, not interpolation of a finite-field
function; no hidden-coefficient evaluation is supplied to the controller.

Define the PUBLIC operator on coefficient polynomials by

```
(A(z,t)P)(Y,s) = P(Y+s*z,s*t).
A(z,t) A(w,u) = A(z+t*w,t*u).
A(z,t)^-1 = A(-z/t,1/t), t!=0.
J_Q(z+t*q) = J_Q(z)+A(z,t)J_Q(q).
```

Lean proves these identities, total-degree nonincrease under linear
substitution, and preservation of the zero-s kernel. It identifies the
kernel intersected with degree<=D EXACTLY with support
`{(alpha,k):k>0, |alpha|+k<=D}`. This is finite dimensional and has the
same coordinates as the Python full chart, not an uncharged infinite
polynomial register or a larger box of coordinatewise degrees. Counting
these monomials gives binom(m+D,m+1); r components give J as above.

The resulting public matrix has entries

```
(A(z,t)F)_(alpha,k,a)
 = sum_(j=1..k) sum_|beta|=k-j
     binom(alpha+beta,beta) z^beta t^j F_(alpha+beta,j,a).
```

This formula follows by expanding each input monomial Y^(alpha+beta)s^j.
Rows of weight k use only columns of weight j<=k and have diagonal t^k.
The transpose is NOT interchangeable. The formal space/support and
substitution proofs are universal; this expanded binomial entry formula,
the closed dimension count and Python refinement are not separately
kernel-checked. Independent coefficient expansion checks every implemented
basis column for D=2,3,4 at p=5,11 and a 127-bit prime. Additional controls
pin the unknown coefficient schema, composition, inverse and weight
triangularity; 22 new tests pass. No new candidate is created.

The scalar support theorem and vector-valued actual mixed-branch theorem
now instantiate NonlinearJetChannel without ASSUMING either Taylor
closure or injectivity. Six headline axiom guards allow only standard
Lean axioms. The source polynomial Q is still a proof witness. This does
not itself prove the GL alignment/rank result in Section 5, weighted erasure,
generic SDE execution, gate synthesis, or the complete recursive solver.
The characteristic-free transport proof does not relax p>3D elsewhere.

Attempts to invalidate this step: (1) an enlarged/infinite jet space is
excluded by the exact support theorem; (2) secret coefficients in the
inverse are excluded by its explicit (-z/t,1/t) construction; (3) reversed
matrix composition is caught by independent substitution and transpose
controls; (4) scalar-only closure is addressed by the vector-channel
corollary. Hidden source access, independence across leaves, rank and
erasure resources remain genuine obligations, not resolved by this result.

### Kernel-Checked Public Source Alignment

Formal/FullJetAlignment.lean now closes the deterministic alignment part
of Section 5 and its spectator-source conclusion. The probability of
getting feature rank remains a separate written argument.

For J_0 the scalar jet space, define the PUBLIC evaluation map
`E:J_0->F_p^b0` by `(E P)_i=P(Y_i,s_i)`. Formal polynomial evaluation
gives `E(J_Q(q))_i=Q(Y_i+s_i*q)-Q(Y_i)`. For r components define

```
(T j)_i = (v_i, ell_i(v_i)),  v_i=(E(j_a)_i)_a,
ell_i(a)=lambda_i(delta(a,-))/2.
```

If E is injective, equality of T's first coordinates implies equality
of E(j_a) for every a, hence T is injective. This proves the rank lift
for ARBITRARY ell_i, including zero, fixed and correlated labels. The
source displacement is derived as `a(q)=a(0)+T(F(q))` from the polynomial
evaluation identity, not assumed as a certificate involving hidden Q.

Given ANY public left inverse P with P*T=I, put S=ker(P). Then

```
L(x) = (P*x, x-T*P*x) in J x S,
L^-1(j,k) = T*j+k,
L(T*j)=(j,0),
L(a(q))=((L(a(0)))_J+F(q), (L(a(0)))_S).
```

These are kernel-checked linear equivalences and identities. A left
inverse exists from injectivity of T; that existence proof uses standard
classical linear algebra, not extracted polynomial-time elimination.
The Python pivot-minor construction is a concrete public certificate
implementation. Its spectator coordinates represent the same residual
`x-T*P*x` in a chosen basis of ker(P). No operation needs a(0), F, Q or
their coefficients; those occur only in the correctness statements.

The formal module also evaluates the actual TWO-SUM permutation
conjugation. For an arbitrary monomial phase gamma it gives

```
W_new(q)|t> = gamma(q,L^-1(t)) |L(a(q))+t>.
```

Density conjugation preserves normalization because L is bijective.
Combining with the actual spectator Kraus sums yields the nonlinear
common-jet density of Section 6 for every spectator outcome, with phase
`conjugate(gamma(q,L^-1(t,zeta)))`. In particular, matching translation
while retaining a phase from a different complement is WRONG.

Seven guards allow only standard Lean axioms. Six additional exact
Python controls test left inverses/kernel residuals under different
public complements, zero/fixed labels and the wrong-phase falsifier,
at small and 127-bit primes. They are not a formal refinement or an
execution of the quantum channel. Production compiler APIs are unchanged.

Attempts to falsify this step addressed by the proof: loss of rank at
lambda=0; dependence of the retained jet on the chosen public complement;
confusing a noninvertible projection with the full carrier permutation;
and a missing phase pullback. Still open: random feature-rank success,
the full hiding-oracle-to-source composition, weighted phase erasure,
SDE execution, complete recursion/error accounting and a useful hard
application. The local batch-shear and source-alignment theorems have not
yet been assembled into one theorem beginning at the original oracle.
The next subsection closes the universal algebraic cancellation step,
not that whole composition. The full algorithm remains UNDER REVIEW.

### Kernel-Checked Weighted Cancellation

Formal/WeightedPhaseErasure.lean now proves the algebraic erasure law for
arbitrary polynomial phases over any commutative coefficient ring R.
Take positive variable weights w_j and public affine maps

```
f_i(X)_j = b_ij + sum_k M_ijk X_k,
M_ijj = s_i^w_j,
M_ijk = 0 if j!=k and w_j<=w_k.
```

If P_i has weighted degree at most d, the coefficient at every monomial
of weight d in P_i(f_i(X)) is exactly s_i^d times its old coefficient.
Consequently, public coefficientwise relations
`sum_i s_i^d coeff_a(P_i)=0` imply `sum_i P_i(f_i(X))` has weight <d.
This holds for every offset and every permitted lower-weight matrix entry,
so the SDE may be solved before the outcomes fixing those entries arrive.
The theorem does not itself encode temporal order or source consumption.

The proof uses a multiplicative filtered-polynomial agreement relation,
not interpolation at finite points. R can be a polynomial ring in unknown
parameters. A separate lemma proves that cancelling every public lift
column cancels its combination for ALL parameter values, including
quadratic products and constants. No hidden evaluation is an operational
input. At the final stage d=1, positive weights imply a constant polynomial;
its global phase cancels in the density kernel. The actual phase-product
identity is also checked using additive characters and polynomial
evaluation: the merged phase is the SUM of pullbacks, not an average.

Nine headline guards allow only standard Lean axioms. Six new regression
cases at p=17/11 and 2^127-1 check the compiler against these conditions,
all parameter-lift types, mixed weighted monomials, arbitrary lower terms
and zero-scale discards. They explicitly prohibit hidden-parameter
evaluation. An outcome-dependent equal-weight off-diagonal perturbation
passes the old diagonal relation but fails actual degree descent. This
falsifies the weaker assumption that an arbitrary block-triangular map
with the correct diagonal entries suffices.

Boundary: FullTaylorTransport's auxiliary-polynomial substitution has the
needed matrix form by the displayed monomial expansion above, but that
coefficient-level bridge is supplied by the next subsection. The tests
are not a formal Python refinement. The algebra permits zero scales; the physical
channel requires them to be discarded, a nonempty active set and fresh
independent same-curve inputs. SDE existence/execution, source scheduling,
rank probability and whole-oracle composition are not supplied here.
No new candidate or speedup claim is admitted.

### Composed Full-Jet Erasure Branch

Formal/FullJetWeightedErasure.lean closes the actual coefficient bridge,
rather than assuming that some matrix satisfies the required conditions.
For an input auxiliary monomial b=Y^alpha s^k, factor out s^k. Public
transport sends that factor to t^k s^k. For the remaining Y polynomial,
the transported polynomial minus itself vanishes at s=0, so every
correction has positive s exponent. Therefore

```
A(z,t)(Y^alpha s^k) - t^k Y^alpha s^k
  has support only at scale powers STRICTLY greater than k.
```

The direction matters: larger auxiliary scale powers mean that output
coordinate weight j receives input coordinate weights k<=j. At equal
weight it receives only itself, scaled by t^j, with NO off-diagonal block.
This is proved directly from polynomial substitution. Neither a fitted
evaluation table nor the expanded binomial coefficient formula is assumed.

The finite coordinates have exactly k>0 and |alpha|+k<=D. Lean proves
that reconstruction and coefficient extraction recover the full jet-space
element and that the derived matrix agrees with finiteTransport on EVERY
register vector. With quotient coordinates and r components, evaluating
the polynomial affine images gives exactly
`(q,T)->(Y+s*q,Z+vectorTransport(Y,s)(T))` from the physical channel.
This excludes the weaker possibility of matching only on the unknown
curve while acting incorrectly on other computational-basis states.

The new degree_reduced_branch theorem composes that point identity,
coefficientwise cancellation and the actual tensor-input Kraus sums.
It returns an explicit summed-pullback polynomial of weight <d, the SAME
hidden curve, and the original branch normalization. Nonzero scales and
a nonempty active set are required. A public parameter-lift corollary
works for all theta assignments; products may remain separate lift
coordinates. At d=1, terminal_kernel proves that the constant residual
cancels from the density matrix for a unit additive character.

Eight axiom guards use only standard Lean axioms. Four new small/127-bit
tests independently substitute arbitrary reconstructed register vectors
and compare the entire symbolic phase, including lower terms, offsets
and quadratic parameter products. No hidden coefficient is evaluated.
Together with the 22 previous full-Taylor controls these give 26 cases;
they are not a formal refinement of the Python implementation.

Still not supplied: independent preparation of the input tensor factors,
adaptive source-consumption accounting, probabilistic rank, executable
SDE, complete normal-source/gate synthesis, and whole-oracle recursion.
The fixed-degree solver of [Ivanyos and Santha](https://arxiv.org/html/1503.09016v2)
is prior art and an external dependency, not a result of this module.
No new scope, novelty or speedup claim is admitted by this composition.

NEXT: the well-founded algorithm above removes the unexplained lower-class
subroutine, but independent validation, full formal composition, practical
SDE execution and an access-matched hard application remain open. Compare
this explicit scope to existing HSP reductions before adding another layer.
A generalization to class-four N is a separate question:
the same partial Fourier can leave carrier-dependent affine frequency
motion, and this module does not cover it. Do not extrapolate to arbitrary
constant-class HSP or to Shor-level significance from the present controls.
