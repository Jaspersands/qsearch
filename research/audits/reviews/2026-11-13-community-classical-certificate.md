# Community certificate: primary-source audit and repaired interface

2026-11-13. Source: Schmidhuber--Zlokapa, arXiv:2510.08494v1, retained as
`audits/sources/2026-11-13-community-selection/schmidhuber_zlokapa.{txt,pdf}`.
Definitions 24--29, Lemmas 30/32/33/34, Corollary 35, Theorem 11, Lemma 52
and Theorem 56 were read in their actual text. PDF pages 18,20,36 were also
rendered and inspected, confirming the problematic formulas below. No API,
network, Git, new experiment, cloning audit or C.3 covariance claim is used.
After the source proof was written, ONLY section 4 of the completed native
compiler report was read as an independent certificate alternative. Section 8
below verifies that stronger, all-label argument directly.

**Strongest source flaw:** Lemma 30's null bound is false at its printed
scope. Bernstein's summand bound omits the amplitude of the normalized
Bernoulli observation. This does NOT invalidate the desired above-threshold
certificate interface: correcting that bound and the block multiplicities
gives the same SNR/ell scaling with new constants depending only on p,k.

## 1. Native model and repaired conclusion

Fix an EVEN p>=4 and k>=3. Write d=p/2, ell=p*lambda, with integer lambda>=1
and ell=o(sqrt(n)). Labels x_i are independent uniform elements
of [k]. Conditional on x, the p-subset observations are independent with
  Y_E~Bern(theta+epsilon*f(x_E)),
  f(a_1,...,a_p)=sum_(c=1)^k product_j (1_(a_j=c)-1/k),
  0<epsilon<theta<1/2,
  A_E=(Y_E-theta)/sqrt(theta*(1-theta)),
  beta=epsilon/sqrt(theta*(1-theta)).
The tensor is extended by ZERO on tuples with repeated VERTICES. This is
the native hyperedge interpretation explicitly used in source equation 38.
The certificate is an analysis witness depending on unknown labels; no
algorithm is granted access to those labels.

There are constants c=c_(p,k)>0 and B=B_(p,k)<infinity such that, if
  beta >= B*n^(-p/4)*ell^((2-p)/4)*sqrt(log n),               (1)
the actual ordered-vertex Kikuchi matrix K satisfies the following. Let
  D=n^d*ell^d,  tau=c*beta*D/2,
and P be its spectral projector for eigenvalues >=tau. With probability
1-o(1) under the planted model,
  ||P J V||^2 >= (c/8)||V||^2,                              (2)
  (1-ell^2/(mu*n))||f||^(2lambda) <= ||V||^2
                                      <= ||f||^(2lambda),  (3)
where V, J and the p-subset vector f are defined precisely below, and
  mu=E f(x_E)^2=k^(1-2p)*((k-1)^p+(k-1))>0.
Under the null model, ||K||<=tau/2 with probability 1-o(1).
All constants are independent of n,ell,theta,epsilon within this scope.
Sections 5--6 first treat growing lambda; section 8 also pays bounded lambda.

This theorem concerns the ACTUAL matrix SNR beta. If another construction
attenuates it, (1) must be imposed on that attenuated SNR. No optimized
runtime, quartic advantage, or comparison at unchanged ell follows from
calling the attenuation a constant: costs n^Theta(ell) retain that penalty.

## 2. Exact p-subset to ordered-vertex normalization

Let H_p have orthonormal basis e_E for p-subsets E. Set
  f=sum_E f(x_E)e_E,  F=||f||^2=sum_E f(x_E)^2,
  V=Pi_lambda f^tensor(lambda),
where Pi_lambda removes tuples of blocks with intersecting vertex sets.
This is exactly Definition 29 in the normalized p-set basis.

For E={i_1,...,i_p}, define the isometry
  J_1 e_E=(1/sqrt(p!))*sum_(pi in Sym(p)) |i_pi(1),...,i_pi(p)>.
Restrict J=J_1^tensor(lambda) to the collision-free block space. Its image
lies in the ordered-vertex space T_n(ell); J*J=I and ||JV||=||V||.
For an ordered injective ell-tuple, JV has coefficient
  (p!)^(-lambda/2)*product_(blocks E_i) f(x_E_i).             (4)
Using the RAW ordered tensor with coefficient f(x_E), instead, multiplies
the vector by (p!)^(lambda/2), and its squared norm by (p!)^lambda. These
are exponentially many block-normalization factors and cannot be dropped.

There is another, bounded, multiplicity in the compressed matrix J*KJ.
For a nonzero transition between block tuples (A_i) and (B_i), put
  t_i=|A_i minus B_i|=|B_i minus A_i|.
Unchanged blocks have t_i=0; changed blocks have t_i>=1 and sum_i t_i=d.
There are no cross-block vertex overlaps except the same-block common
vertices: any such overlap would repeat a vertex in the tensor argument
and give zero. Let E be the union of all removed and added vertices. Then
  <A|J*KJ|B>=(product_(changed i) t_i!)*A_E.                (5)
For each ordering of A, common vertices must stay in their positions; the
new vertices have t_i! permitted orderings in block i. Dividing the total
number of pairs of orderings by (p!)^lambda proves (5).

Source equation 54 has the correct normalizing factors, but equation 56
drops the product t_i!. The missing factor lies between 1 and d!, so it
does not grow with lambda. It equals 1 in the leading configuration of d
blocks with one changed vertex each. The exact equalities require repair;
the asymptotic leading signal and its positive lower bound survive.

For downstream directional estimates, no assertion that J*PJ is itself a
projector is needed. It is a positive contraction. If a=||PJV||>0, take
  s=J*PJV/a.
Then ||s||<=1 and <s,V>=a. This is the exact normalization needed to pass
the ordered-vertex certificate to an estimate in p-subset block coordinates.

## 3. The printed null bound fails; corrected Bernstein works in (1)

Lemma 30 writes K=sum_E A_E K_E, but uses R<=d! for the random summands.
The correct bound is
  ||A_E K_E||<=d!/sqrt(theta*(1-theta)).                     (6)
The omitted amplitude is visible in PDF page 18, equation 39's preceding
paragraph, and is not an extraction/OCR artifact.

For a concrete all-n counterfamily to its printed equation 37, choose
  theta=n^(1-p), epsilon=theta/2,
  ell=p*ceil(log(n)/p).
These are valid native probabilities and obey the asymptotic parameter
regime (14). Under the null, the expected number of edges is Theta(n), so
an edge exists with probability 1-exp(-Theta(n)). Its coefficient has size
Theta(n^((p-1)/2)). For every such edge there is a legal ordered transition
(choose d of its vertices in the tuple and d outside); hence
  ||K||>=max_entry |K_entry|>=Theta(n^((p-1)/2)).
This exceeds the printed bound
  sqrt(6*n^(p/2)*ell^(1+p/2)*log n)
by a power of n for every fixed p>=4. This family is BELOW the detection
threshold (1), so it does not refute that repaired detection regime.

For that regime use epsilon<theta, which implies
  1/sqrt(theta*(1-theta)) <= 2/beta.                       (7)
The deterministic hyperedge matrices satisfy
  ||K_E||<=d!,
  ||sum_E K_E^2||
    <=(d!)^2*binom(ell,d)*binom(n-ell,d) <= D.              (8)
The second bound follows by row sums: a tuple is active for exactly
binom(ell,d)*binom(n-ell,d) edges, and a squared active matrix has row sum
(d!)^2. Also the number of neighbors of a tuple is
d!*binom(ell,d)*binom(n-ell,d)<=D, so
  ||E[K|x]||<=beta*D.                                     (9)
Here |f|<=1 follows, for example, by Holder over the community index.

For the planted centered summands, conditional edge independence holds,
their variance is <=4, and their magnitude is bounded as in (7):
theta+epsilon*f <=2theta and 1-theta>1/2. The null variance is 1. Thus both
cases have matrix variance <=4D and summand norm <=2d!/beta. With dimension
at most n^ell, two-sided matrix Bernstein gives, for any fixed gamma>0,
  Pr(||K-E[K|x]||>=gamma*beta*D | x)
    <=2*n^ell*exp[-gamma^2*beta^2*D/
                          (2*(4+2d!*gamma/3))].            (10)
For the null, replace the mean by zero. The bound is UNIFORM in the labels.
Taking gamma=c/4 and B^2>=4*2*(4+2d!*gamma/3)/gamma^2 makes (10) at most
2*n^(-3ell) under (1). This pays the full Bernoulli amplitude even when
theta tends to zero. No unjustified Gaussian/subgaussian replacement is used.

## 4. The certificate norm, with no overlapping-set independence claim

Changing one label changes F in at most binom(n-1,p-1) terms, each by at
most 1. Since E F=mu*binom(n,p), bounded differences gives
  Pr(|F/(mu*binom(n,p))-1|>=a)
     <=2*exp[-2*a^2*mu^2*n/p^2].                           (11)
In particular F>=mu*binom(n,p)/2 with probability 1-exp(-Omega_(p,k)(n)).

For any label vector satisfying this lower bound, sample a p-subset with
probability f(x_E)^2/F. The probability it contains a specified vertex is
at most 2p/(mu*n). Consequently two independent such subsets intersect
with probability at most 2p^2/(mu*n). A union bound over lambda draws gives
  Pr(all draws disjoint)>=1-ell^2/(mu*n).
Multiplying by F^lambda proves the DETERMINISTIC bounds (3) for these labels.
The sampling argument only counts the norm; it does not expose labels to
the actual detection algorithm.

This also repairs the norm interface used in source Lemma 52. Equation (11)
and lambda=o(sqrt(n)) imply
  F^lambda=(mu*binom(n,p))^lambda*(1+o_P(1)),
and (3) implies the same for ||V||^2. Distinct p-sets need not give
independent f-values. Source equation 152 should be an upper bound, not its
printed equality; the desired concentration follows without that equality.

## 5. Positive label motifs and the actual conditional signal

Let Z_c(a)=1_(a=c)-1/k and
  C_ij=E[Z_i(x)Z_j(x)],
so C has diagonal a=(k-1)/k^2 and off-diagonal b=-1/k^2. In a changed-block
type t_1,...,t_r>=1, sum t_i=d, put s_i=p-t_i. All involved vertex sets
(shared, removed, added, for each block) are disjoint. Expanding each f and
averaging over the independent VERTEX labels gives exactly
  psi_t=E[ product_i f(A_i)f(B_i) * f(E) ]
       =k*product_i g(s_i),
  g(s)=sum_(u,v) C_uv^s C_uc^(p-s) C_vc^(p-s),               (12)
independently of the fixed c. This is source Lemma 32 in the actual disjoint
motif scope. It does not factor averages across merely distinct p-sets.

Its positivity is elementary and useful. Let z_u=C_uc^(p-s). Then
  g(s)=z^T C^(Hadamard s) z.
Here d<=s<=p-1, so s>=2. For k>=3 the matrix with diagonal a^s and
off-diagonal b^s is POSITIVE DEFINITE: its eigenvalues are a^s-b^s and
a^s+(k-1)b^s, both positive. Thus every psi_t is positive. There are only
finitely many such types for fixed p,k, and their minimum is positive.

This gives a conditional proof, avoiding any questionable long moment
factorization. With probability 1-exp(-Omega_(p,k)(n)), every community
frequency is within a sufficiently small fixed delta of 1/k. Deleting at
most ell vertices preserves that condition with a slightly larger delta.
For each type the average of its bounded kernel over DISTINCT vertices
in any remaining set differs from the iid empirical-label average by
O_p(1/n). The latter is continuous in the k label frequencies. Hence,
uniformly over ALL such deletions, the motif average is at least psi_t/2
for large n. This uses only finite-order kernels, not concentration of an
exponentially long product or independence of overlapping hyperedges.

All modified-block contributions to the CONDITIONAL mean are therefore
nonnegative. Retain only r=d, t_1=...=t_d=1. Write
  m_*=d*(p+1), psi_0=k*g(p-1)^d.
For each ordered tuple of lambda-d unchanged blocks, its weight is the
nonnegative product of their f^2. The motif on the remaining vertices has
at least
  (psi_0/2)*(n/4)^m_*/((p-1)!)^d
weighted embeddings for sufficiently large n. There are binom(lambda,d)
choices of the modified positions. The norm argument of section 4 gives
the total unchanged weight at least F^(lambda-d)/2. Finally F<=n^p and,
eventually, binom(lambda,d)>=lambda^d/(2^d*d!). It follows that
  <JV,E[K|x]JV>/||V||^2 >= c*beta*n^d*ell^d,                (13)
where a permissible fixed positive constant is
  c=min(1/4, psi_0 /
       [2^(2*m_*+d+2)*d!*((p-1)!)^d*p^d]).                (14)
The required balancing tolerance can be chosen from the finite positive
minimum of (12), so (13) holds on one label event of probability 1-o(1).
No matrix or certificate label oracle is part of this proof.

## 6. Source expectation and variance statements: precise disposition

The normalization repair allows an exact check of Lemma 33. With t ranging
over positive compositions of d into r parts, direct counting gives
  E <JV,KJV>/beta
   =(n)_(ell+d) * sum_(r=1)^min(lambda,d) binom(lambda,r)
       *mu^(lambda-r)/(p!)^(lambda-r)
       *sum_t psi_t / product_i[(p-t_i)!*t_i!].             (15)
Every counted vertex is distinct; (5) supplied one t_i! that cancels one
of the two factorials from choosing removed/added sets. For lambda->infinity
and ell=o(sqrt(n)), its leading term is
  (binom(n,p)*mu)^lambda * beta*n^d*lambda^d
       *[p^d*psi_0/(d!*mu^d)]*(1+O(1/lambda+ell^2/n)).      (16)
Thus the source's asymptotic leading scaling is correct under its GLOBAL
condition ell=omega(1), despite its intermediate missing multiplicities.
Its lemma statement alone should not be read as the same asymptotic constant
uniformly for every fixed lambda.

The variance claim can also be repaired without false independence. Let
Patt be the nonzero block-pair patterns; their count is
Theta_(p)(binom(n,p)^lambda*n^d*lambda^d). Each matrix multiplicity is <=d!.
Every pattern involves exactly m=ell+d vertices. If two such vertex unions
are disjoint, the terms are independent, so their covariance is zero.
If they overlap in r vertices, at most r unchanged blocks in either family
are affected. Cauchy--Schwarz, using independence WITHIN either disjoint
block family, bounds the relevant unchanged-label product by
  C_(p,k)*mu^(2lambda)*C_(p,k)^r.
For different edge variables, conditional edge independence supplies beta^2;
for a common edge, its conditional second moment is bounded by 3 because
epsilon<theta<1/2. Covariance subtraction changes only fixed constants.

For different edges, overlapping-union counts are bounded by
  |Patt|^2*binom(m,r)*(m/n)^r.
For equal edges, symmetry makes that p-set uniform. Conditional on it, the
remaining m-p vertices are uniform subsets of its complement. Summing the
overlap weights gives at most
  C_(p,k)*|Patt|^2/binom(n,p)*exp(C_(p,k)*m^2/n).
These two bounds yield
  Var(<JV,KJV>)/(E<JV,KJV>)^2
     <=C_(p,k)*(ell^2/n + 1/(beta^2*n^p))=o(1)             (17)
when ell=o(sqrt(n)) and beta>>n^(-p/2), as needed for the printed sufficient
condition in Lemma 34. Factors in some intermediate printed lines, such
as the binomial power in equation 85, cannot be taken literally; (17) is
the independent bound. This proof distinguishes disjoint VERTEX unions
from merely distinct, overlapping edge sets throughout.

Corollary 35's positive Rayleigh lower bound consequently survives with
repaired constants. For the downstream interface, the stronger conditional
argument (13) and the correct noise estimate (10) already suffice.

## 7. High-probability leading-subspace mass and scope

On the good label event, (13) gives certificate Rayleigh mean at least
c*beta*D. Equation (10) with gamma=c/4 gives, with probability 1-o(1),
  <JV,KJV>/||V||^2 >=3c*beta*D/4,
  ||K|| <=(1+c/4)*beta*D<=2*beta*D.
For tau=c*beta*D/2, put w=||PJV||^2/||V||^2. The spectral theorem gives
  <JV,KJV>/||V||^2 <= tau*(1-w)+||K||*w,
so w>=c/8. This proves (2); (3) holds on the same good label event. Under
the null (10) gives ||K||<=tau/2. In particular the desired strict positive
spectral gap and constant certificate mass do not require the literal
constant in source Theorem 56, or its sample-split independence claim.

Admitted classical certificate interface: fixed even p>=4,k>=3, actual
native probabilities epsilon<theta<1/2, ell=p*lambda with integer lambda>=1,
ell=o(sqrt(n)), and the repaired above-threshold condition (1). The norm is
the p-SUBSET norm; J pays its ordered-vertex interpretation exactly. The
constants may be very small/large functions of p,k. This is an asymptotic
probability theorem, not a finite gate compiler or a practical threshold.

Not imported: the false unconditional null Lemma 30; source C.3's sample-
splitting independence; directional covariance or higher-moment claims for
the guiding state; an optimized quantum/classical exponent comparison after
attenuation; community-label recovery, novelty or hardness. Those are
separate tasks. This audit writes only the present proof note.

## 8. Independent PSD repair: conditional signal for EVERY label vector

The completed report
`audits/openai_runs/2026-11-13-community-native-source-compiler/response.md`,
section 4, proposes a simpler alternate certificate proof. The following
checks establish its claims; other sections of that report are not imported.
This can replace the balanced-label argument of section 5.

For fixed, arbitrary labels put w_c(i)=1_(x_i=c)-1/k and define the auxiliary
FULL ordered tensor T=sum_c w_c^tensor(p), allowing repeated vertices here.
Let G_ab=<w_a,w_b>. Since p is even,
  ||T||^2=sum_(a,b) G_ab^p
        >=sum_a ||w_a||^(2p)>=k*(n/k^2)^p.                 (18)
The last inequality uses ||w_a||^2=n/k^2+(1-2/k)*N_a>=n/k^2.
Every entry of T has absolute value at most 1, so ||T||^2<=n^p as well.

On all ell ordered registers set
  B_lift=sum_(J subset [ell], |J|=d) sum_c
          (tensor_(a in J) |w_c><w_c|) tensor I_(J^c).
It is positive semidefinite and ||B_lift||<=k*binom(ell,d)*n^d<=C_pk D.
If Pi_cf removes repeated vertices, the actual mean obeys
  E[K|x]/beta=Pi_cf B_lift Pi_cf-E_bad,
  ||E_bad||<=C_pk*ell^d*n^(d-1).                          (19)
Indeed, when exactly d positions change to fresh vertices there is exactly
one contributing J and its matrix entry is f of the 2d changed vertices.
For a fixed row/J, every extra assignment uses one of the old J vertices
among the new J vertices; there are at most d^2*n^(d-1) such assignments.
Assignments hitting unchanged coordinates are already killed by Pi_cf.
Sum over J and use symmetric absolute row sums. This includes diagonal
and fewer-than-d-change entries, rather than incorrectly identifying the
actual mean with a positive matrix without the error term.

Let phi=(T/||T||)^tensor(lambda). For one marked position in one block put
  H_c=||(<w_c| tensor I)T||^2/||T||^2.
Cauchy--Schwarz against w_c^tensor(p-1), and
  <w_c^tensor(p-1),(<w_c| tensor I)T>=sum_a G_ca^p>=G_cc^p,
give
  H_c>=G_cc^(p+1)/||T||^2>=n/k^(2p+2).                   (20)
Selecting just the positive summands of B_lift with one marked position
in each of d different blocks yields
  <phi,B_lift phi> >=binom(lambda,d)*p^d*sum_c H_c^d
                   >=c_full*D,
  c_full=k^(1-(2p+2)*d)/(2^d*d!),                          (21)
eventually when lambda>=2d. Dropping other summands is legitimate because
they are positive semidefinite. For balanced labels H_c=n/k^2 is also
correct, but the proof does not require balance.

Bounded lambda is also paid. For 1<=lambda<2d, select d positions in ONE
block. The same Cauchy--Schwarz argument for contracting those d positions
gives a contribution per community at least
  G_cc^(p+d)/||T||^2>=n^d/k^(2p+2d).
There are lambda*binom(p,d) such choices. Therefore the energy is at least
c_small*D, where one uniform positive choice is
  c_small=binom(p,d)*k^(1-2p-2d)/(p^d*(2d)^(d-1)).
Replace c_full by min(c_full,c_small) for an all-positive-lambda bound.

The squared block amplitudes have each coordinate marginal <=C_pk/n by
(18), and any within-block collision has probability <=C_pk/n by counting
at most n^(p-1) possible tuples. Different blocks are in product state.
A union bound over coordinate pairs therefore gives
  ||(I-Pi_cf)phi||^2<=C_pk*ell^2/n.
The normalized projected state differs from phi by O_pk(ell/sqrt(n)).
Its B_lift energy consequently changes by at most
O_pk(D*ell/sqrt(n)), and (19) costs another O_pk(D/n). Thus its actual
conditional-mean Rayleigh quotient is at least (c_full/4)*beta*D for all
large n, UNIFORMLY over every label vector.

Finally the exact identity is
  J V=(p!)^(-lambda/2)*Pi_cf T^tensor(lambda).               (22)
So the normalized projected state is precisely the source certificate in
the correct ordered encoding, not a different spectral witness. Applying
section 3's corrected noise bound and section 7's spectral argument proves
(2) with c replaced by min(1/4,c_full/4), conditional on ANY labels, using
the preceding minimum if bounded lambda is included.
The same all-label estimates give norm comparability to ||f||^(2lambda)
with an O_pk(ell^2/n) loss. The sharper displayed coefficient 1/mu in (3)
uses the high-probability label event from section 4 and remains valid.

This alternate strengthens and simplifies the certificate interface. It
does not validate the false null Lemma 30, source sample splitting, a guide
moment bound, a runtime comparison, or any other part of the new report.
