# Independent Adversarial Review: Orthogonal Exterior Receiver

27 October 2026.

## Verdict And Scope

**The core receiver argument is valid under the stated ordinary coherent
full-stabilizer oracle promise.** I found no counterexample to its kernel,
support, extension-count, escape, unknown-rank stopping, or sampler claims.
Its proved range is odd prime powers q, n >= 3, and 1 <= k <= n-2.
In particular, n=3/k=1 works. The d=1 boundary really is blind; the method
does not solve n=3/k=2. Composition with the supplied higher-rank theorem
covers all nonzero singular ranks for n >= 4.

**The companion classical lower-bound argument is also valid in its
stated opaque, randomly relabeled oracle model.** It proves an
Omega(sqrt(q)) classical query lower bound for hidden singular LINES,
against the polynomial-log(q) quantum receiver at fixed n >= 3.
It does not prove a natural-input speedup, a lower bound for every rank,
or literature novelty.

Important qualifications:

1. Exact kernels are essential to the receiver's deterministic soundness
   argument. Insufficient Fourier rank can create an accepted but polluted
   support. The parent now explicitly charges this event; that repair is
   adequate. A concrete counterexample appears below.
2. The sampler analysis must couple capped sampling to uncapped sampling.
   Exactly uniform sampling conditional on all caps succeeding is not
   needed and should not be claimed. The parent correctly avoids it.
3. Approximation error must mean an additive statistical/instrument bound,
   not a per-amplitude or per-matrix-entry error. Section 9 supplies a
   precise sufficient interpretation.
4. The lower bound is a worst-case opaque-oracle conclusion obtained from
   a distribution of labelings. It is not a lower bound for every allowed
   labeling separately, nor for access to a hiding function's source code.
5. The reviewed RESULT.md, Section 7, still says no low-rank classical lower
   bound is proved. If the companion comparator is adopted, update that
   sentence to distinguish the proved line case from unproved other ranks.
   This is a document-consistency issue, not a defect in either proof.

Reviewed sources, read-only:

- `/Users/jaspersands/Developer/qsearch-research-work/orthogonal-exterior-2026-10-27/RESULT.md`
- `/Users/jaspersands/Developer/qsearch-research-work/orthogonal-exterior-2026-10-27/CLASSICAL_COMPARATOR.md`
- `/Users/jaspersands/Developer/qsearch-research-work/orthogonal-general-rank-2026-10-27/RESULT.md`
  as context for composition, not a fresh audit of that entire theorem.

This review supplies mathematical proofs, not code validation. No code
audit, test execution, literature search, repository/Git/UI modification,
or external contact was performed. The only created artifact is this review
in the requested new directory.

## 1. Contract And Legal Oracle Restriction

Let F=F_q with odd q, and let

    V = E + F0,                 Q(x,y) = x.y,
    B((x,y),(x',y')) = x.y' + x'.y.

Here F0 denotes the second coordinate space, not the coefficient field.
The hidden U is a nonzero TOTALLY singular F-linear subspace. Thus B
vanishes on U x U. Merely assuming that the restricted form is degenerate
would not suffice.

Assume a supplied effective field presentation and public matrix encoding
of G=O^+(2n,q) or SO^+(2n,q). The oracle is the ordinary fixed-width
coherent evaluation oracle for f, with

    f(g)=f(h) iff g^-1 h is in P_U=Stab_G(U).

Opaque labels are permitted. No coordinates or dimension of U are inputs.
The full stabilizer promise cannot be replaced by an unspecified subgroup
of that stabilizer.

For a public maximal singular R and singular Witt complement R*, write

    T_A(x,y)=(x+A y,y),         A^T=-A.

Since q is odd, y^T A y=0. Thus T_A preserves Q, is unipotent of determinant
one, and satisfies T_A T_C=T_(A+C). Its parameterization is injective.
With a public Witt frame S, the submitted matrix is g_A=S T_A S^-1.
It is in SO even when det(S)=-1. Neither S nor an illegal intermediate
matrix is queried; computing such matrices publicly is not an oracle call.

Moreover g_A^-1 g_C=g_(C-A), so the restricted oracle has exactly the
ordinary additive HSP promise on F^a, a=n(n-1)/2. No ambient orthogonal
Fourier transform, extended GL oracle, or hidden-dependent preparation
has been introduced.

## 2. Exact Kernel And Image Support

Identify R* with the dual of R under B, and put

    X=U intersect R,            Y=projection_(R*) U.

For u=(x,y) in U,

    T_A u-u=(A y,0).

Consequently T_A U=U if and only if A Y is contained in X: necessity is
immediate, and sufficiency gives T_A U contained in U, hence equality by
invertibility and dimension. Therefore

    K={A alternating : A Y subset X}

is exactly the hidden subgroup, and is F-linear. This does not assume
that U is a graph or that the learner knows X or Y.

For a subspace K of alternating maps, its support

    supp(K)=sum_(A in K) image(A)

equals the sum over any F-basis of K: the image of any linear combination
is contained in the sum of its constituent images.

### Nonzero intersection

Isotropy gives X subset Y^ann. For x in X and r in R, the alternating map

    (x wedge r)(y)=y(r)x-y(x)r

sends Y into X, hence belongs to K. Fix x != 0. Whenever r is independent
of x, this map has image span(x,r), since the two evaluation functionals
are independent on R*. These images span R for n >= 2. Thus

    X != 0  ==>  supp(K)=R.

This rules out a bad intersecting probe passing the proper-support screen
when K is exact.

### Zero intersection

If X=0, projection U -> Y is injective and dim(Y)=k. Choose dual bases
in which Y occupies the first k dual coordinates. A Y=0 makes the first
k columns of A zero; skew symmetry also makes those rows zero. The
remaining unrestricted alternating block is precisely

    K=exterior_square(Y^ann).

Writing d=n-k, its support is all of Y^ann when d >= 2: each coordinate
appears in a rank-two alternating map with another coordinate. For d=0
or d=1 the entire block is zero. Also, directly from the pairing,

    Y^ann=R intersect U^perp.

Therefore, for 1 <= k <= n-2,

    0 < dim(supp(K)) < n  iff  R intersect U=0,
    dim(supp(K))=n-k on every accepted probe.

Both identities are basis-independent and remain valid over extension
fields. Exterior-square notation describes alternating maps R* -> R;
it is not an assertion that R has an intrinsic nondegenerate dot product.

## 3. The Parent's Schubert-Cell Sampler

The explicit sampler in the parent proof is sufficient; a singular-flag
sampler is not required.

Fix the public maximal E. For a particular j-space X in E, consider all
maximal R with R intersect E=X. Necessarily R lies in X^perp. The quotient
X^perp/X is split of dimension 2(n-j), with maximal E/X. In a public
hyperbolic decomposition of that quotient, every maximal transverse to
E/X is the graph of a unique alternating (n-j)-square matrix. Conversely
every such graph is transverse and lifts uniquely to an R containing X.
There are exactly q^((n-j)(n-j-1)/2) choices.

It follows that the number in the cell j is exactly

    w_j = [n choose j]_q q^((n-j)(n-j-1)/2).

Choosing j with weights w_j, then a uniform X, then a uniform alternating
matrix gives every maximal R the same probability. The q-binomial identity
gives

    sum_j w_j = product_(i=0..n-1)(1+q^i)
              = 2 product_(i=1..n-1)(1+q^i).

This is the union of BOTH maximal families. No restriction to one
determinant class of frames may be silently inserted into this sampler.

For uniform X, sequentially accept independent uniform rows of F^n.
At row r+1, with r<j, every vector outside the previous r-space has the
same conditional probability. All ordered independent j-tuples therefore
have the same probability, and every j-space has the same number of
ordered bases. This proves uniformity of X, not just full row rank.

The rejection probability per row attempt is q^(r-n) <= 1/q, including
j=n. At most n rows are needed per probe. A cap b gives a union bound
T n q^(-b) on row-cap failures. Each attempt uses n field-element tickets,
so the bound

    C=T[1+n^2 b+a]

on integer requests is adequate: one cell ticket, at most n^2 b row-entry
tickets, and at most a alternating-entry tickets per probe.

Uniform integers in [0,D) are generated from ceil(log2 D) random bits,
rejecting values at least D. For D>1 rejection probability is less than
1/2; D=1 is deterministic. A cap h therefore adds at most C 2^(-h)
failure probability. Coupling with uncapped draws proves the parent's
epsilon/8 + epsilon/8 bound. No claim about the conditional distribution
given all caps succeeding is used.

Gaussian coefficients and tickets have O(n^2 log q) bits and can be
computed by integer recurrences and exact arithmetic. There is no search
with success probability 1/q. An explicit field presentation is needed;
the theorem does not supply one from an unstructured black-box field.

### Public Witt complements

Complements require no hidden information or root extraction. Given a
basis r_i of R, solve B(r_i,v_j)=delta_ij and let C_ij=B(v_i,v_j). Then

    f_i = v_i - (1/2) sum_j C_ij r_j

satisfies B(r_i,f_j)=delta_ij and B(f_i,f_j)=0. Thus span(f_i) is a
singular Witt complement. Gaussian elimination and inversion of 2 are
enough over any odd extension field.

## 4. Good-Probe Probability

In a split 2m-space, the number of nonzero singular vectors is

    D_m=(q^m-1)(q^(m-1)+1).

Indeed, y=0 contributes q^m-1 vectors; each of the q^m-1 nonzero y has
q^(m-1) choices of x in y^ann. A fixed singular line belongs to

    2 product_(i=1..m-2)(q^i+1)

maximal spaces, by passage to its split polar quotient; all maximal
spaces number 2 product_(i=1..m-1)(q^i+1). Equivalently one can double
count point-generator incidences. The containment probability is
1/(q^(m-1)+1).

A nonzero intersection with U contains a line of U. Hence

    Pr[R intersect U != 0]
      <= (q^k-1)/[(q-1)(q^(n-1)+1)]
      < 1/[q(q-1)] <= 1/6

for k <= n-2. Independence of the line-containment events is neither
asserted nor required. Thus a fresh probe is good with probability at
least 5/6, uniformly in the unknown U.

## 5. Equal Extension Counts And Uniform Lifts

Put D=U^perp and d=n-k. The quotient D/U is a nondegenerate split
2d-space. Define C to be the d-dimensional singular W contained in D
with W intersect U=0. Their images M in D/U are maximal singular spaces.

Every good R gives W=R intersect D in C. Conversely, fix W in C. The
quotient W^perp/W is split of dimension 2k, and the image Ubar of U is
a maximal singular k-space there. Maximal R containing W correspond
bijectively to maximal spaces Rbar of this quotient. Moreover

    R intersect U=0 iff Rbar intersect Ubar=0.

For the nontrivial direction, if u+w represents an element of R/W, with
u in U and w in W subset R, then u is already in R. There are exactly
q^(k(k-1)/2) maximal complements to Ubar, parameterized by alternating
k-square matrices in any fixed Witt decomposition. For each of these
extensions, R intersect D has dimension d and contains W, so equals W.

Thus EVERY W in C has exactly the claimed number of good maximal
extensions. Uniform good R induces uniform W, not merely an invariant
distribution with unexamined orbit weights.

For each maximal M in D/U, choose a linear splitting of its preimage.
Its d-dimensional complements to U are precisely graphs of maps M -> U.
There are q^(kd) of them. Since U is the radical of D, adding U-components
does not change Q; all these graphs are singular. Hence M is uniform
over both quotient families, and conditional on M the graph map is
uniform in Hom_F(M,U).

As a cross-check, these counts give the exact probability

    Pr[good] = product_(i=d..n-1) q^i/(q^i+1).

This agrees with the point-incidence calculation at k=1 and the lower
bound above. In particular the k=1 extension multiplicity is exactly one,
not an omitted extra factor of two.

## 6. Hyperplane Escape

Let H be a proper hyperplane of D, defined by a nonzero functional ell.

If ell restricted to U is nonzero, then for each fixed M the map

    Hom_F(M,U) -> M*,          phi -> ell|U composed with phi

is surjective and all its fibers have size q^((k-1)d). The fixed section
of M merely translates this uniform functional. Therefore

    Pr[W subset H | good]=q^(-d) <= 1/9.

If ell vanishes on U, it descends to a nonzero functional on D/U. By
nondegeneracy it is B(v,.) for a unique nonzero quotient vector v.
For maximal singular M in this quotient, M^perp=M. Thus

    W subset H iff M subset v^perp iff v in M.

The probability is zero if v is nonsingular. If v is singular, it equals
1/(q^(d-1)+1) by the same point-generator count, and is at most 1/4
when d >= 2. These statements hold equally over prime and extension fields.

For any current proper span S subset D, choose a hyperplane H of D
containing S. A good W outside H necessarily grows S. Consequently

    Pr[an accepted probe grows S] >= (5/6)(3/4)=5/8.

The hyperplane need not be computable by the learner: it is a device in
the proof. Fresh probes are independent of the previous ideal transcript,
so the bound applies at every adaptive stage. There is no claim that
the dimension increments themselves are independent.

## 7. Unknown Rank, Clock, And High-Rank Composition

With exact kernels the first nonzero proper W reveals d=dim(W), hence
k=n-d. Before that event, use S=0. Thereafter all accepted W have this
same dimension and lie in D. The target dimension

    dim(D)=2n-k

is therefore known from public output, not supplied as rank advice.
Once the accumulated span has that dimension, it equals D; nondegeneracy
of B gives D^perp=U exactly. An implementation may abort on inconsistent
support dimensions or overshooting the target; neither happens in an
exact successful run. These guards do not replace the error budget.

Use 2n blocks of L fresh probes, with

    2n (3/8)^L <= epsilon/4,    T=2n L.

While incomplete, any block has probability at most (3/8)^L of producing
no dimension increase. At most 2n-k <= 2n-1 increases suffice. A union
bound proves the stated geometric failure budget. The block clock and
failure outcome do not require k. Stage caps with the same parameters
give the same conclusion.

For k=n-1 or n, every exact support is either zero (disjoint R) or R
(intersecting R). No support is accepted, so this bounded routine returns
failure. It cannot infer a high rank merely from absence of acceptance.

For n >= 4, run this routine first and run the supplied k>=3 receiver only
if it returns no candidate. Allocate errors between the two. On low ranks
the first routine succeeds with its promised probability. On the two high
ranks its exact screen rejects everything and the second theorem applies.
An erroneous first output due to Fourier/circuit error is already charged.
This sequential argument does not need to assume that a second routine is
sound outside its promise: on low ranks reaching it already lies inside
the first routine's failure event. The parent's stronger observation about
the old dimension gates on k=1,2 is consistent with the supplied kernel
classification for n >= 4, but is unnecessary to this composition proof.

This conclusion uses the prior higher-rank theorem as supplied context;
it is not a new verification of its implementation or every prior lemma.

## 8. Boundary Cases And A Real Undersampling Counterexample

### n=3, k=1

Here d=2, K on a good probe has dimension one, and its nonzero alternating
map has rank two. Its image is the required W. Good probability is
q^2/(q^2+1); the worst conditional hyperplane containment is 1/(q+1).
Thus growth probability is at least

    q^3/[(q^2+1)(q+1)] >= 27/40 > 5/8.

No low-dimensional exception spoils this case. However the combination
of ranges {1} and {3} still leaves k=2 uncovered when n=3.

### d=1 or d=0

For example take R=E and U=span(f_1,...,f_(n-1)). Then R intersect U=0,
but Y^ann=span(e_n), whose exterior square is zero. The support is zero,
NOT Y^ann. With U=span(f_1,...,f_n) the same blindness holds at d=0.
For other R the earlier classification gives only zero or full support.

The hypothetical quotient hyperplane estimate at d=1 would also be
1/(q^0+1)=1/2, not 1/4, but the receiver fails already at support recovery.
Increasing the sample count does not repair a zero exact kernel.

### Incomplete Fourier rank

Take n=4, R=E, U=span(f_1,f_2), and write A_ij=E_ij-E_ji. Then

    K=span(A_34),
    Khat=span(A_34,A_13) strictly contains K,
    supp(Khat)=span(e_1,e_3,e_4).

The estimated support is nonzero and proper, but e_1 is not in U^perp.
It would falsely infer k=1. This Khat is a possible exact-sample rank
failure: Khat^ann is a subspace of K^ann, and a finite collection of
uniform samples from K^ann can span precisely Khat^ann with positive
probability.

Even checking Khat=exterior_square(supp(Khat)) is not a general fix:
adding A_14 gives exactly the exterior square of span(e_1,e_3,e_4), still
containing K and still polluted. Thus the failure is not merely a missing
easy consistency check. The parent's decision to charge ALL Fourier-rank
failures is necessary and sufficient for its bounded-error theorem.

## 9. Extension Fields, Query Counts, And Precision

Let q=p^r. Use a public F_p-basis of F_q and its trace-dual basis. With
upper-triangular alternating coordinates, characters are

    chi_z(A)=exp(2 pi i Tr_(F_q/F_p)(z.A)/p).

The trace annihilator of an F_q-linear K is its F_q dot-product
annihilator. Indeed if Tr(z.A)=0 for every A in K, closure under cA for
all c in F_q and nondegeneracy of the trace pairing force z.A=0 in F_q.
This is why Fourier outcomes may be decoded as F_q vectors and spanned
over F_q. Blindly reinterpreting prime-field output coordinates without
the dual-basis conversion is not justified.

The additive group is (F_p)^(ra). Standard approximate finite-abelian
Fourier/state-preparation primitives therefore have polynomial cost in
a, log q, and log(1/delta); the theorem is conditional on their usual
fault-free circuit model, not on a supplied quantum hardware realization.

If the true annihilator has F_q-dimension h <= a, m=a+s independent
uniform samples fail to span it with probability at most

    [(q^h-1)/(q-1)] q^(-m) <= 1/[(q-1)q^s].

This follows by union over its hyperplanes and includes unknown h. For
h=0 there is no rank failure. The parent's condition

    T/[(q-1)q^s] <= epsilon/4

therefore bounds all rank failures, including probes chosen adaptively.
No field-size factor is lost through the extension degree.

One sample requires one call to the SAME f oracle: prepare A uniformly,
compute g_A reversibly, query f(g_A), uncompute the g_A/work registers
using A, discard or measure the label, Fourier transform A, and measure.
Leaving an injective g_A register entangled with A would destroy the
required interference; deterministic public computation must be cleaned
up. Cleaning it up does not require a second f call. The label is retained
or traced out, not coherently erased for free.

Thus at most

    T(a+s)

original oracle calls suffice. Reversible field and matrix arithmetic,
linear-algebra postprocessing, public sampling, and fixed-width label
handling are polynomial in n, log q, label width, and log(1/epsilon).
Dense classical enumeration of q^a probe elements is not part of this
quantum resource bound.

A precise sufficient interpretation of the parent's approximation budget
is: each complete sampling instrument differs from its ideal instrument
by at most epsilon/[4T(a+s)] in operational total variation, uniformly
over its allowed inputs; a corresponding half-diamond-distance bound is
stronger and also suffices. Allocate and compile elementary gates to meet
that whole-instrument target. The ordinary oracle itself is exact under
the problem promise; any noisy-oracle variant would need an extra budget.

Hybrid/telescoping bounds then give epsilon/4 total instrument error.
Together with epsilon/4 each for geometric failure, Fourier-rank failure,
and capped classical sampling, total failure is at most epsilon.
Analyze these by coupling to the ideal process, not by assuming that
conditioning on all learners being correct preserves the probe law.

## 10. Companion Classical Lower Bound: Fixed Points

The comparator's proof works. It is slightly cleaner to say g not in
Z={I,-I} throughout than to rely on an unproved classification of the
group center. The argument below applies to EVERY nonscalar orthogonal
matrix, including any hypothetical non-scalar central matrix.

There are

    N=D_n/(q-1)

possible hidden singular lines. A fixed F_q-line of g lies in an
F_q-eigenspace of g with a nonzero F_q eigenvalue. Distinct eigenspaces
form a direct sum, so their dimensions d_i sum to at most 2n. No
diagonalizability over F_q or over its algebraic closure is required.
A 2n-dimensional eigenspace would make g scalar; orthogonality would
then force its scalar to be +1 or -1.

If every d_i <= 2n-2, relax to partitions with total dimension 2n and
part-size cap 2n-2. The function q^d-1 is increasing and discretely
convex, so transferring dimensions toward a largest part increases the
sum until the maximal partition (2n-2,2) is reached. For n >= 3 this yields

    sum_i(q^d_i-1) <= q^(2n-2)+q^2-2 <= 2q^(2n-2).

Ignoring the singular condition only enlarges the numerator, so this
bounds nonzero vectors on fixed singular lines. Missing eigenspace
dimensions cause no problem in this relaxed upper bound.

If an eigenspace E has dimension 2n-1, Q restricted to E is a nonzero
quadratic polynomial. Otherwise E would be totally singular, impossible
since a totally singular subspace of a nondegenerate 2n-space has dimension
at most n. The degree-two polynomial zero bound gives at most
2q^(2n-2) zeros on E, including zero. All other eigenspaces have total
dimension at most one and contribute at most q-1 nonzero vectors. Counting
zero in the first bound only makes this upper bound more conservative.

Finally

    D_n=q^(2n-1)+(q-1)q^(n-1)-1 > q^(2n-1).

Dividing the two numerator bounds by D_n gives, respectively, 2/q and
3/q as valid upper bounds. The same factor q-1 occurs for nonzero vectors
per line in both numerator and denominator. Therefore for every g not in Z,

    Pr_U[g U=U] <= mu=min(1,3/q).

This is valid over all odd extension fields. At q=3 the estimate mu=1 is
uninformative, which is harmless for the q -> infinity separation.

### Common action kernel

If g fixes every singular line, it fixes each coordinate line e_i and f_i.
Write the corresponding eigenvalues a_i,b_i. Fixing the singular lines
e_i+e_j and f_i+f_j makes all a_i equal and all b_i equal. Fixing
e_i+f_j for i != j equates these two values. Thus g is scalar, and
orthogonality forces g=+I or -I. Conversely these scalars fix every line
and have determinant one in dimension 2n. The common kernel is exactly
Z in BOTH O and SO. The proof uses only public coordinate lines and
n >= 2, so there is no exceptional n=3 issue.

## 11. Companion Classical Lower Bound: Adaptive Labels

Take U uniform among the N singular lines. Given U, label the cosets of
P_U by an independent uniform injection into a fixed alphabet with at
least |G| elements. This is an allowed ordinary hiding oracle; the large
alphabet does not reveal the coset or U. Its width is O(log |G|), hence
polynomial in n and log q. Arbitrary opaque oracle evaluation is charged
equally on both the quantum and classical sides; no efficient explicit
construction of a random hiding-function table is asserted.

Run the classical learner, with its random coins, against a fake oracle
that assigns distinct uniformly random labels to new classes gZ and
repeats the label for an already queried class. Take the entire fake
experiment independent of U. Its query sequence and its output are
therefore independent of U, despite adaptivity.

Condition on this fake experiment. For each pair of queried distinct
central classes, g_i^-1 g_j is outside Z. The fixed-point bound gives

    Pr_U[g_i^-1 g_j in P_U] <= mu.

A union bound over at most binomial(t,2) pairs bounds the event B that
any such pair is equal under the true coset oracle. Repeated central
classes are excluded from B: their collisions are known in advance and
contain no information about U.

The lazy-injection coupling is valid. Before the first event of this type,
each new fake central class also represents a new true coset, so both
oracles can use the same uniformly unused label. At the first true coset
collision between distinct central classes, the real oracle repeats an
old label and the fake oracle uses a new one. After divergence one can
continue the real oracle with its own lazy uniform injection, preserving
the correct real marginal distribution. Thus transcript divergence has
probability at most Pr(B).

The fake output has success probability at most 1/N, because U is
uniform and independent of that output. This is an UNCONDITIONAL statement:
conditional on no true collisions, the hidden-line posterior may indeed
change. The coupling inequality avoids needing any false conditional
independence claim. It follows that

    Pr[real output is U] <= 1/N + binomial(t,2) mu.

This allows arbitrary classical computation, adaptivity, and randomness.
It does not assume labels can only be compared for equality: all bits of
the random opaque labels are available to the learner in both experiments.

For example, success at least 2/3 with a worst-case query cap t, at q>3,
requires

    t(t-1) >= (2q/3)(2/3-1/N),

and hence t=Omega(sqrt(q)). A learner that succeeds for every promised
hidden line and every allowed labeling must also succeed on this input
distribution. This proves the asserted worst-case-oracle lower bound.

The quantum receiver is label-invariant and uses precisely the same
coherent evaluation oracle, so at fixed n >= 3 and fixed target error
its poly(log q) time/query bound gives the claimed same-oracle separation.
There is no transfer to algebraic labels that encode the hidden subspace,
access to the oracle's implementation, every other hidden rank, or natural
explicit problems. The lower bound does not close the gap to the supplied
O(nq) O-oracle reflection upper bound for lines, and does not need to.

## 12. Final Assessment

The proposed receiver survives this adversarial mathematical review, as
does the newly supplied line-only opaque-oracle lower bound. The parent's
current undersampling and bounded-sampler guards address the substantive
pitfalls rather than assuming them away. The remaining recommendations
are precise instrument-error terminology and synchronization of the
comparator statement in RESULT.md with its companion lower-bound draft.

This verdict is a proof-level assessment of the specified oracle problem.
It is not an implementation certificate, a human review, a claim of
novelty, or evidence that a natural hard task supplies this oracle.

The user subsequently reported 103 selected passing tests and the stated
finite geometry/oracle controls. I did not execute or audit them, and none
is a premise of the proofs above. The user also reports that the comparator
now credits Decker et al. (2014), Section 7.2, for the lower-bound method.
That attribution is consistent with treating the collision argument as an
established method; its bibliographic details were not independently
checked here. No further experiments or literature search were undertaken.
