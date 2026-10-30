# Adversarial Review: Norm Completion And Its AG Scope

2026-10-27. Read the complete RESULT.md, norm_completion.py, AG_SCOPE.md,
and subsequently MATRIX_ONLY_BRIDGE.md and ALL_INPUT_SCOPE.md in the
two-component-norm-2026-10-27 bundle, plus LIFT.md and COMPRESSED_REVIEW.md.
This is a mathematical audit,
not an independent execution of the parent's exhaustive controls or native
replay. No source, Git, or UI edits. No novelty claim.

**Verdict:** no fatal error found in the intended odd-characteristic
linearization, exact marginal certificate, bound (3), or AG counting
argument. The subsequently supplied **all-input rank-loss strengthening
also checks out**, together with the matrix-only bridge and the
column-scaling correction below. The final conclusion is an
expected-polynomial classical algorithm for EVERY complete-AG matrix in
the stated parameter class and every syndrome, for odd q>=1019,
e>=8, q^2>=44e. The naive bounded-degree ring construction pays for the
native access in theory. No random-prime exception or cube-conditioning
factor is needed for this final conclusion. It is not an implemented
native backend, an inference from the handpicked e=8 example, or a
fixed-prime all-e dequantization. The older generic-prime proof is retained
below as a separately checked, now unnecessary sufficient argument.

## Fixes And Qualifications

1. State **q odd** explicitly in both mathematical theorems. Merely
   q>=1019 includes characteristic two: there are no nonsquares there,
   and the displayed M is zero. The implementation already enforces odd
   primes. This makes an implicit premise explicit, not a defect over F_1019.
2. In RESULT.md's proof of (3), distinguish a coefficient vector
   lambda in F_q^k from the row word c=B^t lambda in F_q^m. The expression
   M^t c is dimensionally wrong as written; it must be M^t lambda.
   The corrected argument below proves the unchanged numerical bound.
3. Make the field-size headline explicit: q^2>=2|T| controls kernel
   rejection AFTER a good offset is available. It alone does not certify
   good offsets. A convenient sufficient corollary is 2r>=k+4 together
   with q^2>=2|T| and the structural promises. More generally retain (3).
4. State the ordinary AG evaluation hypotheses, the residue-duality
   identification, and coordinate-scaling rule below. End-to-end polynomial
   time requires polynomial-cost geometric/Riemann--Roch preprocessing,
   not just its computability. Without that guarantee the runtime is
   T_geometry plus expected polynomial matrix/arithmetic work. The new
   matrix-only bridge below supplies a polynomial, albeit very large,
   construction for the specific section spaces actually needed here.
5. In MATRIX_ONLY_BRIDGE.md, the computed annihilator contains the
   INVERSELY COLUMN-SCALED complete comparison annihilator, not necessarily
   the unscaled one. This is a statement correction only: zero patterns
   are unchanged, and computing the actual product-code nullspace already
   handles these unknown scales without recovering them.

The parent's fixes to items 1-3 and 5 and the quantitative cube-conditioning
denominator were rechecked during this review. These entries record
the audit corrections, not a demand to change the norm formulas. The final
all-input theorem below does not use cube conditioning at all.

These are precision/dependency fixes. They do not overturn the conditional
parameter extension. The corrected upper endpoint is **e=23599**, not 23598.

## Norm And Kernel Certificate

Put C_j=A_T diag(B[j,T]*h_T) A_T^t. Identity (1) is exactly C_j=0 for
every j. Expanding the norm gives the stated constant and linear terms;
the remaining quadratic terms are z^t C_j z - nu*w^t C_j w=0. There is
no z*w cross term in this diagonal norm. Fixing y=1 off T and subtracting
those columns handles zero entries of h correctly.

Over an odd-order field, u^2-nu*v^2=0 with nu nonsquare implies u=v=0:
if v!=0 it makes nu a square; if v=0 then u=0. Thus the simultaneous-zero
test is exactly the original nonvanishing condition, not a relaxation.

For a full-column-rank kernel basis N, t=t0+N*xi is uniform on the affine
fiber when xi is uniform. The image E_i N*xi is uniform on a subspace of
size q^rho_i. Consequently p_i is precisely q^(-rho_i) when the required
target is in that image, and zero otherwise. This remains valid for
rho_i=0 and a zero-dimensional kernel. Different coordinates need NOT be
independent: the union bound alone proves success >=1-sum_i p_i.

The proof matches `prepare`'s augmented-rank membership test and `sample`'s
kernel parametrization. No mathematical change to those formulas is
needed. Independence/uniformity claims refer to ideal random field draws,
not a theorem about an individual deterministic PRNG seed.

## Offset Bound And A Countercontrol

Fix lambda!=0 and c=B^t lambda. Full row rank of B makes c nonzero.
The blocks of M^t lambda are

    2 A_T diag(h_T*c_T) a,
    -2 nu A_T diag(h_T*c_T) b.

The support-spanning promise makes each map surjective onto F_q^r.
Independent uniform a,b therefore give a uniform vector in F_q^(2r).
Since A_i!=0, the subspace

    L_i = span((A_i,0),(0,A_i))

has dimension two. Its probability is q^(2-2r). Rank deficiency gives
a nonzero lambda with M^t lambda=0, which belongs to every L_i. Otherwise,

    rho_i = 2 - dim(rowspace(E_i) intersect rowspace(M)).

Thus rho_i<2 supplies a nonzero vector M^t lambda in L_i. Union over i and
the q^k-1 nonzero lambda proves (3), without any independence across those
events. Optionally divide its untruncated bound by q-1 by unioning over
projective coefficient classes; this improvement is not needed here.

All rho_i=2 requires 2r-k>=2. The simpler sufficient condition
2r>=k+4 makes the original (3) at most |T|/q^2. Hence q^2>=2|T| then
makes BOTH rejection stages constant-cost. This explains exactly where
the square-root field scale is conditional.

**Concrete countercontrol to omitting the kernel test:** over F_5 take

    B = [[1,-1,0],[0,1,-1]],  A = [[1,1,1]],  h=(1,1,1),
    nu=2,  a=(0,1,0),  b=(0,0,1),  s=(4,3).

Identity (1) and the support-spanning promise hold. Here
M=[[3,0],[2,4]] is invertible, q^2>=2m, and the unique coefficient pair
is zero. Its norm output is (0,1,3), which is invalid. Yet the original
syndrome has the full-support witness (1,2,4). The exact certificate gives
eta=1 and correctly rejects this offset. This is NOT a counterexample to
the actual algorithm; it shows why syndrome rank and field size alone
cannot replace the marginal certificate.

If the offset failure bound is delta<=1/2, using a offset trials and b
kernel trials per admitted offset gives failure at most
[delta+(1-delta)*2^(-b)]^a under fresh independent randomness. Uniformity
of the resulting native witness is not implied.

## AG Distance And Concrete Dimensions

For ordinary evaluation, take distinct rational evaluation points away
from the divisor support. A nonzero section of L(D_A) cannot vanish on a
set S with |S|>deg(D_A): otherwise div(f)+D_A-S would be effective of
negative degree. Thus evaluation on S is injective. With V=rowspan(B),

    |support(h*c)| >= d_V-z > deg(D_A)

proves rank(A_support(h*c))=r for every c!=0. This proves RESULT.md's AG
implication. Base-point freeness of A is a separate requirement, supplied
by the constant section when D_A is effective and disjoint from evaluation.

For AG_SCOPE.md's actual parameters, Riemann--Roch gives

    l(G)=5e+3=k,    l(8I)>=3e,
    l(G+16I)=21e+3,    dim(Hspace)>=22e-(21e+3)=e-3.

Evaluation of L(G) and L(8I) is injective. The designed distance is
d_V>=22e-(10e+3)=12e-3. Products L(G)*L(8I)*L(8I) lie in L(G+16I),
so the proposed Hspace supplies the exact annihilator. If desired,
Clifford's inequality (or nonspecial Riemann--Roch) also gives r<=4e+1<k:
the smaller-than-k auxiliary dimension is genuine here.

For the zero-pattern claim, choose a differential eta with a simple pole
and nonzero residue at every evaluation point, and use K_X=div(eta).
Then J=D+K_X-G-16I is disjoint from D, and the dual consists of
(res_P(eta)*f(P))_P for f in L(J). Such residues can be chosen with sum
zero; m=22e is even, so pairs 1,-1 suffice. The residue theorem and
Riemann--Roch provide the differential. This justifies the claimed zero
patterns; an arbitrary unqualified canonical representative need not be
disjoint from D. Also deg(J)=6e-3<m, so this evaluation is injective.

When Hspace has no zero coordinate functional, uniform h, INCLUDING h=0,
has E[z]=m/q. Markov yields (A1). For z<4e-3, the distance inequality
above gives support size >8e, as required. Finally

    k+2-2r <= 5-e,

which proves (A2). Both rejection estimates are <1/2 for q>=1019,e>=8;
q^2>=44e supplies the remaining kernel estimate. No additional random-rank
heuristic is hidden in this step.

## All-Input Strengthening: Final Audit

**Accept ALL_INPUT_SCOPE.md's substantive deduction under the complete-AG
promise and the matrix-only construction audited below.** None of the
following steps requires a random G, a base-point-free complete
annihilator, or a full Schur cube.

### Rank Loss In The Offset Lemma

For lambda!=0, put c=B^t lambda and
W_c=span{A_i : h_i*c_i!=0}. If dim(W_c)=d_c>=R, each block of
M^t lambda is uniform in W_c. Its intersection with span(A_i) has
dimension at most one, so its probability is at most q^(1-d_c), hence
at most q^(1-R). The two blocks remain independent. The same rowspace
argument as before proves

    Pr[rank(M)<k or some rho_i<2]
        <= min(1, |T|*(q^k-1)*q^(2-2R)).

Thus S1 is correct; replacing r by the uniform restriction-rank lower
bound R does not assume uniformity on all of F_q^r. The coefficient/row
word distinction lambda versus c must also be retained in this lemma.

### Fixed Divisor And Random Zeros

For the punctured complete comparison annihilator, deg(J)=6e-4 and
h^0(J)>=deg(J)+1-g=e-4. Let F be its full geometric fixed divisor and
M=J-F. Base change of complete section spaces identifies these with the
geometric linear series, so Clifford applies even over the finite field.
We have h^0(M)=h^0(J)>1 and F effective.

If M is nonspecial, Riemann--Roch gives
h^0(M)=e-4-deg(F), forcing deg(F)=0. If M is special, Clifford gives
deg(M)>=2h^0(M)-2>=2e-10. Consequently

    deg(F)<=4e+6.

This remains valid if the displayed divisor J is not effective: its
nonzero complete linear series is what supplies effective representatives.
Every identically zero rational evaluation coordinate contributes at
least one to deg(F). The actual mixed-annihilator contains the inversely
scaled complete annihilator, so its number b of fixed zero coordinates
also satisfies b<=4e+6. Computing b is just a scan of a nullspace basis;
the algorithm does NOT have to compute F.

For uniform h in that actual space, each of the other m'-b coordinate
functionals vanishes with probability 1/q. No pairwise independence is
needed. With a=floor(e/4),

    Pr[w>a] <= (m'-b)/(q*(a+1)) <= (22e-1)/(q*(a+1)) <88/q.

This proves the proposed h-rejection bound. The zero vector has
w=m'-b>=18e-7>a and is indeed rejected.

### Restriction Rank And Numerical Gate

Every nonzero punctured row word has weight >=12e-4. For an admitted h,

    |S|=|support(h*c)| >= 8e-10-a.

The auxiliary is the COMPLETE L(8eP0), evaluated injectively away from P0.
Thus its restriction kernel is exactly H^0(8eP0-S), not an assumed generic
kernel. The degree is at most a+10, and h^0(D)<=max(0,deg(D)+1) gives
kernel dimension <=a+11. As r>=3e,

    rank(A_S)>=3e-a-11=R,
    k+2-2R=27-e+2a.

This proves S3 and S4 uniformly over all row words, including dependent
evaluation configurations. At e=64 the real envelope is
1407*q^(-5)<1/2. Its ratio from e to e+1 is

    [(22e+21)/(22e-1)]*q^(-1/2)<1

for e>=64,q>=1019. Hence it bounds the offset failure below 1/2 for
EVERY integer e>=64. The kernel union bound is still at most
m'/q^2<=1/2 under q^2>=44e.

**Minor text fix:** the stated two-step monotonicity is false. The integer
exponent is -8 at both e=67 and e=69, while 22e-1 increases. The integer
bound is therefore larger at 69 than at 67. Delete that two-step remark;
the decreasing REAL envelope above and the four-step comparison are valid
and already prove the required claim. No cutoff changes.

### Small Degrees And Final Scope

The small-e fallback can also be justified constructively. Since
d(V)>=12e-3>k, deleting ANY k coordinates leaves column rank k. Pick one
column basis I and then a disjoint basis J from its complement. Fix all
other outputs to 1. Invert B_J to write the J-values as k affine forms
of the k I-values; their coefficient matrix is invertible. Assign the
I-values sequentially, forbidding zero and the root of each affine form
whose last unassigned variable is being set. At most k+1 values are
forbidden per step. Choose among k+2 distinct field elements, so the
construction is polynomial in k,log(q), not a scan of all q values.
It succeeds when q>k+1, which holds for 8<=e<64 and q>=1019.

Together with the paid matrix-only adapter, this proves an all-input
expected-polynomial witness algorithm for the promised complete-AG family
at odd q>=1019, e>=8, q^2>=44e. For e>=64 the h, offset, and kernel
stages each have constant acceptance probability for EVERY promised B and
EVERY syndrome; the smaller cases use the two-basis construction. There
is no exceptional source distribution left to condition on. In particular
the conclusion survives restricting the input family to full-cube codes.

This strengthens the interpretation of the q=1019 cutoff to every promised
input through e=23599, hence dyadic e=16384, not merely most generic-prime
inputs. It still does not cover e->infinity at fixed q. The adapter remains
unimplemented on native instances, and exact uniform witness sampling is
not proved. No practical runtime or literature novelty is claimed.

## Optional Earlier Uniform-Prime Argument

The following independently checked argument is superseded for the final
all-input conclusion. Its distributional qualifications remain necessary
when citing this OLDER argument on its own.

The base-point implication is correct. Riemann--Roch gives

    l(J)-l(J-P) = 1+l(K_X-J)-l(K_X-J+P).

If the left side is zero, the last space has a nonzero section. Its
divisor class is [G+16I-D+P], of degree t=4e+4. Translation is a bijection
of the rational Picard torsors, so at most A_t source classes are bad for
that P. Unioning over m points costs exactly the advertised factor m.

The zeta coefficient estimate (A3) is valid: take absolute values of the
numerator coefficients, bound them by binom(2g,j)*q^(j/2), multiply by
q^(t-j)/(1-q^(-1)), and sum. No assertion of uniform Picard classes occurs.

For each degree-d rational divisor class, d>2g-2 gives exactly
(q^(d-g+1)-1)/(q-1) rational effective divisors, so this is a valid upper
bound on the number of degree-d primes in it. Using the explicitly
IMPORTED prime-count lower bound (A4), the bad-source probability is
bounded by

    m A_t * [(q^(d-g+1)-1)/(q-1)] / [q^d/(2d)]
    <= 2dm q^(t-g) (1+q^(-1/2))^(2g)/(1-q^(-1))^2.

Here t-g=-e+3 and 2g=10e+2, exactly (A5). The per-class multiplicity bound
is the necessary correction for sampling primes rather than Picard classes.
I found no missing factor q or d. A4 remains a source prerequisite in this
review, not something inferred from tower existence or a finite replay.

For full-cube conditioning, the correct statement is

    Pr[bad | cube full] <= min(1, beta/(1-epsilon_cube)).

No independence is required. To claim a high success fraction AFTER this
conditioning, retain a quantitative source bound on 1-epsilon_cube;
merely epsilon_cube<1 does not make the displayed ratio small. Checking
that a computed basis of Hspace has no all-zero column directly certifies
this geometric gate for an individual input, without source statistics.

One unnecessary restriction can be removed: since deg(G)=10e+3>e=deg(I),
an effective degree-e I cannot contain the closed point G at all. Their
disjointness here follows from degrees even without the tower-specific
infinity support fact. Disjointness from D follows from deg(G)>1.

## Scope And Input Accounting

Relative to the SUPPLIED earlier guarantee q>k+1=5e+4, the new geometric
theorem has a larger certified range. At q=1019 the old strict inequality
gives e<=202, hence dyadic 128. The new inequality gives

    1019^2 = 44*23599+5,

so e<=23599 and dyadic 16384. This is a theorem about the generic
uniform-prime source, outside its explicitly bounded exceptional event,
not an inference from the specially selected e=8 divisor. It is not a
claim that the corresponding large matrices were constructed or solved.
The old cutoff is a guarantee's limit, not a lower bound on other attacks.

Public geometry must include the coordinate correspondence. If
B=U B_geom diag(lambda) after matching the coordinate order, construct
h=h_geom/lambda (and order A correspondingly), or explicitly undo the
monomial map and transform the syndrome. Otherwise Hspace orthogonality
for the geometric code need not imply (1) for the supplied B. This rule
uses the public multipliers already required by the source note.

The original geometric version requires public X,D,I,G and polynomial-cost
Riemann--Roch/evaluation access; B is not automatically that interface.
The matrix-only bridge reviewed below constructs the needed replacement
spaces and avoids recovering I,G or their evaluation frames. Growing-field
q>=sqrt(44e) remains conditional on the stated complete-AG/source promises.
At fixed q the present guarantee stops at the finite cutoff. Neither a
vacuous union bound nor failure of a trial establishes hardness.

## Comparison With Ragavan--Shutty 6.1

[Section 6.1, Algorithm 6.1 and Theorem 6.2](https://arxiv.org/pdf/2610.00502v1#page=44)
use h/4*((A^t z+omega/h)^2-nu), product orthogonality, and a rank-k
syndrome map. They obtain automatic nonvanishing from the fixed nonzero
second component. Setting a=omega/(2h), b=1/2, freezing the new w=0,
and replacing the new z by the old z/2 recovers that formula exactly.

The reviewed variation frees both components, replacing the k-by-r map
by a k-by-2r map and paying for simultaneous zeros via the kernel
certificate. The rank obstruction r<k concerns only the one-component
map using this same A. It does not invalidate their theorem, exclude a
different auxiliary code, or establish novelty of the variation.

## Matrix-Only Bridge: Subsequent Audit

**Accept the theoretical construction under its promises, not an executed
matrix-only solver.** The following checks discharge the access issue for
this particular attack; they do not supply general Jacobian arithmetic or
recognize complete AG codes from arbitrary matrices.

### Lift And Bounded Ring

Here d=2g+1 and ell=d+1=2g+2. For e>=8,
m>=2d+4 and m-1>2ell both hold. The lift uses
E=2G,F=G-P0 in the Schur quotient identity: deg(F)=2g and
deg(E)<=m-4=(m-1)-3, including the required inclusive endpoints.
[Couvreur--Marquez-Corbella--Pellikaan, Theorem 5 and Proposition 7](https://arxiv.org/html/1401.6025v3#S2.SS2)
give the multiplication and quotient statements. Column weights transform
as lambda,lambda^2,lambda^(-1),lambda through the relevant operations,
so the lifted columns retain the correct projective points.

Keeping the original k rows and appending one lifted section identifies
P0=[0:...:0:1]. Every quadric vanishing on the other m-1>2ell points
vanishes on the curve. Thus the computed kernel is the TRUE I_2, not just
a collection of sample relations. Normal generation and ideal generation
by quadrics at degree ell>=2g+2 are the standard high-degree curve facts;
the finite-field reconstruction setting is also described in
[Marquez-Corbella et al., Computing Y](https://www.singacom.uva.es/~iremarquez/MMPR-2012.pdf).

Let S be the polynomial ring on the k+1 lifted coordinates. For each
t<=8, form I_t as the span of I_2 times ALL degree-(t-2) monomials, then
row-reduce S_t/I_t, retaining representatives and multiplication. There
are O((k+1)^8) monomials; even naive dense elimination has a polynomial
field-operation bound. There are only O(m*ell) subsequent filtration
steps. This is an explicit algorithm, not an unspecified general Groebner
routine or an appeal to effective geometry. Degree is fixed at eight,
even though the multiplicity cutoffs grow with e. Do NOT obtain higher
pieces from evaluation on the finite point set, which is no longer
injective. Compressed methods are optional for polynomiality and essential
only to plausible practicality; their full certificates must be retained.

### Product/Colon Spaces

For 1<=j<ell, multiplication W_j*W_1 is onto
H^0(4H-(j+1)P0). Its factor degrees are 2ell-j and 2ell-1, both >2g.
Dividing the vanishing condition by the globally generated R_2 gives
exactly W_(j+1). This proves the first recurrence inductively.

The residual bundle 2H-jP0 has degree >=ell=2g+2 for j<=ell, hence is
globally generated. Consequently the common zero divisor of W_j is
EXACTLY jP0. A nonzero sigma in W_ell exists by Riemann--Roch. Interpret
its divisor here as the effective zero divisor of a SECTION of 2H, not
the principal divisor of an unframed rational function. For z in R_2,

    z W_j subset sigma R_2
    iff (z/sigma) W_j subset R_2
    iff div(z/sigma)+jP0 >= 0.

Conversely, multiplying any f in L(jP0) by sigma remains in R_2 because
sigma vanishes at least ell>=j times at P0. Therefore Z_j=sigma L(jP0)
with no requirement to locate or remove sigma's other zeros. This covers
j=8e<ell and constructs the COMPLETE auxiliary space, not a subcode.

### Common-Zero Evaluation

For Q!=P0, write the analogous recurrence explicitly as

    U_(l+1) = {v in R_4 : v R_4 subset span(U_l U_1)}.

It uses only R_8. Through l+1=2ell+1 the residual degrees stay above 2g,
so product surjectivity and global generation prove its exactness.
Global generation of R_2 then proves
F_l={z:z R_2 subset U_l}=H^0(2H-lQ).

The zero order of sigma as a section is at most 2ell; F_(2ell+1)=0.
At its actual order l, the quotient F_l/F_(l+1) has dimension one because
Q is rational and sigma gives a nonzero class. A ratio z/sigma regular
at Q has z in F_l. Its unique c with z-c*sigma in F_(l+1) is its residue
value at Q: the leading coefficients in any local frame have ratio c.
Changing the frame multiplies both by the same nonzero factor. Thus this
procedure really evaluates all ratios, including common zeros, without
granting a uniformizer, jet oracle, or original column multiplier.

### Actual Matrix, Source Law, And Outcome

Let lambda denote the UNKNOWN coordinate multipliers, and let
C_F=ev_(D-P0)L(G+16eP0). The needed comparison is

    V0*A^2 subset diag(lambda) C_F,
    diag(lambda^(-1)) C_F^perp subset (V0*A^2)^perp.

This corrects the bridge's unscaled containment claim. The algorithm
computes the right-hand space directly from original B and reconstructed
A; lambda is only used in the proof. Inverse scaling preserves zero
patterns. A base-point-free comparison annihilator therefore implies the
ACTUAL computed space is base-point-free, and uniform sampling from the
larger space still gives E[z]=m'/q. It also enforces (1) for the original
punctured matrix without recovering G's frames.

The updated counts are correct:

    m'=22e-1,  dim(C_F^perp)>=e-4,  deg(J')=6e-4,
    t'=4e+5,  d_(V0)>=12e-4,  z<4e-4.

The prime-class proof consequently has exponent t'-g=4-e, giving exactly
the stated beta'. Keep the same imported prime-count prerequisite and
min(1,beta'/(1-epsilon_cube)) after cube conditioning. The first labelled
source coordinate is fixed independently of G. A G-dependent permutation
or choice of P0 would require controlling that selection, for example
an additional union over the m possible points. This warning concerns
only the superseded distributional proof: the all-input strengthening
works for every choice of the punctured coordinate.

Puncturing preserves row rank since the original minimum distance is >1.
A full-support solution of B' y'=s-B[:,0] extends by y_0=1 to the exact
original syndrome. The three numerical gates remain controlled by
q>=1019 (odd) and q^2>=44e, so the same e<=23599/dyadic-16384 extension
applies to this MATRIX-ONLY mathematical construction for the generic
source, with its explicit exceptional-source probability.

For the EARLIER generic-source version, one can check the actual
annihilator for zero columns before random retries and return UNKNOWN on
failure. On that certified branch the
distance promise and accepted h-zero threshold give the offset theorem,
then every syndrome is solved in expected polynomial time. This makes
the source-exception and runtime boundaries explicit. No field-size truth
table, geometry advice, infinity point, canonical divisor computation,
point-counting algorithm, or native section-ring implementation is being
silently assumed. The source's prime-count theorem remains a PROOF
prerequisite, not a computational subroutine. For the FINAL all-input
algorithm, do not abort merely because b>0: allow b<=4e+6 and enforce the
additional-zero threshold w<=floor(e/4). That version uses neither the
prime-count theorem nor any source-exception probability.

## Reviewed State

The implementation formulas were reread after the parent's update, and the
later statement corrections were checked. No independent exhaustive
arithmetic campaign or native replay was run. Reviewed source snapshots
(later parent edits can of course change these):

    RESULT.md          b5478ec16a831baad7c8bd867802ecc82ec3e08b2be2eaa464a3241e48a6e663
    norm_completion.py 23eab105b8e275c326630c50789cc1f4c0221b5bd1e6ff58e2ff39db2a4ade97
    AG_SCOPE.md        b7854eb2d80fa7d2899a636aaa31ad72644914395dcbfcfedcc8accfc406a85a
    MATRIX_ONLY_BRIDGE.md 168cc4120f04feedf2943300d7bae59bf92874a3f244f659f1bfe22b636f7d95
    ALL_INPUT_SCOPE.md d1df348dd933e451b61177bef4d86daf5dc01f504648ff5b28fa303e711b8fd4
