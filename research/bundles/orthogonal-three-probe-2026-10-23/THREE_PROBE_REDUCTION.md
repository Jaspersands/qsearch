# A Three-Probe Reduction For Split Orthogonal Parabolic HSP

2026-10-23. **Proposed theorem and local proof; independent review and novelty
determination pending.** This uses standard abelian HSP, not the unreviewed
Rees theorem. The accompanying program is an exact public controller plus
an explicitly exponential dense reference simulator. No natural hard
application, cryptanalytic consequence or Shor-level result is established.

## 1. Problem And Proposed Result

Let F_q be an effectively presented odd-characteristic finite field. Supply
its prime-field basis, arithmetic and q, and let n>=3. Set

    V = F_q^n + F_q^n,   Q(x,y)=x.y,
    B(v,w)=Q(v+w)-Q(v)-Q(w).

An unknown maximal totally singular L has dimension n and L-perp=L. The
ordinary coherent fixed-width oracle f on O+(2n,q), or on SO+(2n,q), satisfies

    f(g)=f(h) iff gL=hL iff g^-1 h belongs to P_L=Stab(L).

The hidden group must be the FULL stabilizer, not an arbitrary subgroup
contained in it. Labels are opaque. Their width and all original oracle
calls are charged. Opposite coset conventions require input inversion.

**Proposed conclusion:** recover a basis of L, hence an explicit description
of P_L, in bounded-error time poly(n,log q,log(1/epsilon),label width). This
includes both components of the maximal-singular Grassmannian. The proof
does not extend by substitution to chain rings, nonsplit spaces, nonmaximal
subspaces, arbitrary flags, or characteristic two.

This is a standard structural HSP family, not a manufactured small oracle
benchmark. Nevertheless it is still an ORACLE result, not a solution to an
explicit lattice, isogeny, code-equivalence or graph problem.

## 2. An Abelian Probe Whose Kernel Has Geometric Meaning

Choose a public nonzero singular e. Find a public singular f0 with
B(e,f0)=1, and let W=<e,f0>-perp. This needs only linear algebra: choose v
with B(e,v)=1 and set f0=v-Q(v)e. For w in W define the linear transformation

    E_e(w) z = z + B(z,e)w - B(z,w)e - Q(w)B(z,e)e.

Direct substitution gives preservation of Q and

    E_e(w) E_e(w') = E_e(w+w').

The map is injective, since E_e(w)f0=f0+w-Q(w)e determines w. In a basis
ordered as e,W,f0 it is unitriangular, so det E_e(w)=1. Consequently every
query is legal even if the supplied oracle is only on SO. The restriction
`w -> f(E_e(w))` is a genuine abelian HSP on the additive group of W.

**Kernel lemma.** If e is in L, the entire probe fixes L. Otherwise, put

    H0=L intersect e-perp,
    T_e=projection_W(H0) along <e>.

Then the hidden additive kernel is exactly T_e, of dimension n-1.

Proof: H0 has dimension n-1 and does not contain e. Projection is injective
and preserves its zero quadratic form. Choose l0 in L with B(e,l0)=1.
If E_e(w) stabilizes L, then

    E_e(w)l0-l0 = w-[B(l0,w)+Q(w)]e

lies in H0, forcing w in T_e. Conversely, for w in T_e its unique lift
`h=w+a e` belongs to H0. Orthogonality to l0 gives a=-B(l0,w), and Q(w)=0.
Thus E_e(w)l0-l0=h. For any h' in H0, B(h',w)=B(h',h)=0, so E_e(w) fixes
h'. It therefore stabilizes L. If e lies in L instead, B(e,L)=0 and all
differences are multiples of e, proving the exceptional whole-kernel case.

An abelian HSP learner returns T_e in the public W coordinates. It therefore
constructs the known maximal singular neighbor

    S_e = <e> + T_e = <e> + (L intersect e-perp).

This does NOT return L after one probe. Assuming that it does is a falsifier.
No hidden coordinate or character is supplied to the learner.

## 3. Three Neighbors Recover The Original Subspace

Take three independent public singular probes e1,e2,e3. Suppose their images
in V/L are linearly independent. Equivalently, the functionals
`lambda_i=B(e_i,.)|_L` are independent, since L-perp=L. Then

    S_i intersect S_j = L intersect ker(lambda_i) intersect ker(lambda_j).

Indeed, writing a vector as l_i+a_i e_i=l_j+a_j e_j, independence modulo L
forces both a_i and a_j to vanish. The converse follows from the definition
of S_i. Three independent functionals can be completed to a dual basis of L.
The three pairwise kernels together span every corresponding basis vector,
including their common kernel. Hence

    L = (S1 intersect S2) + (S1 intersect S3) + (S2 intersect S3).

The controller does NOT test independence using the unknown L. It forms
the right-hand side, rejects unless it is maximal singular of dimension n,
and applies the independent exact certificate below. Degenerate probes can
cause rejection; they cannot justify accepting a wrong answer.

## 4. Uniform Probes And Constant Success Probability

There are `(q^n-1)(q^(n-1)+1)` nonzero singular vectors. A uniform sampler
does not reject random ambient vectors with probability 1-1/q. Instead:

- With probability `1/(q^(n-1)+1)`, choose x uniformly nonzero and set y=0.
- Otherwise choose y uniformly nonzero and x uniformly in y-perp.

Both branches use polynomial-bit uniform integers and linear equations.
Nonzero vectors can be indexed by integers 1,...,q^n-1 without enumerating
them. Bit-level rejection for uniform integers has acceptance at least 1/2;
cap those draws globally and charge their abort probability.

For any fixed L, a probe is outside L with probability
`a=q^(n-1)/(q^(n-1)+1)`. Conditioned on this, its nonzero class in V/L is
uniform: in coordinates adapted to L each nonzero y has q^(n-1) singular
lifts. Thus the exact probability of three independent classes is

    a^3 * (q^n-q)(q^n-q^2)/(q^n-1)^2.

For q>=3,n>=3 this is at least
`(9/10)^3 * (8/9) * (2/3) > 1/3`. Fresh trials succeed with constant
probability, independently of numeric q. The argument is not based on an
unanalysed random walk or a favorable finite seed.

## 5. A Sound Output Certificate

Given a candidate maximal singular R, complete it to a known hyperbolic
basis. In these coordinates test the following `n(n-1)+1` matrices against
f(I):

    diag(I+E_ij, I-E_ji),   for all i!=j;
    [[I,D],[0,I]],          D=E_12-E_21.

Conjugate them back by the known frame. Each is in SO and stabilizes R.
The frame itself need not lie in SO; its determinant cancels in conjugation.

If all tests also stabilize the actual L, its projection Y onto the bottom
coordinates is invariant under every I-E_ji. Any nonzero F_q-subspace with
this property is all F_q^n: subtract an elementary transform of a vector
with a nonzero coordinate to get coordinate vectors, then span them. Hence
Y is zero or full. In the first case L=R. In the second L is the graph of
a linear map C. The last upper unipotent sends `(Cy,y)` to `(Cy+Dy,y)`;
graph invariance forces D=0, a contradiction. Thus all tests pass IFF L=R.

This certificate does not require a primitive field element, factorization
of q-1, or a full generating set of GL_n(F_q). The elementary tests alone
are NOT sufficient: they also stabilize the opposite maximal subspace.

## 6. Complete Query And Error Schedule

Take B trials with `(2/3)^B <= epsilon/4`. There are at most 3B abelian HSP
calls on F_q^(2n-2). For each, take m=2n-2+s Fourier samples, where

    3B / [(q-1)q^s] <= epsilon/4.

Uniform samples of an annihilator of dimension k<=2n-2 fail to span it with
probability at most `(q^k-1)q^-m/(q-1)`, so the displayed bound covers every
call and every prior history. Fourier sampling over an extension field uses
the supplied prime-field basis and trace-dual characters; the annihilator
is F_q-linear and rank reconstruction is over F_q.

Each sample prepares uniform w, computes E_e(w) reversibly, makes ONE f
query, uncomputes the query matrix/workspaces, discards or measures the label,
and applies the additive Fourier transform. The total original query cap is

    3B*m + B*[n(n-1)+1] + 1.

Allocate complete-instrument trace/diamond error epsilon/(12Bm) to each
Fourier source/readout, and epsilon/4 to capped classical uniform sampling.
Geometry, rank, channel and sampler errors sum to at most epsilon. Source
arithmetic and field QFTs have polynomial gate cost at this precision. No
error bound is conditioned on a rare normalized outcome. This is a written
algorithmic bound, not a compiled gate estimate or the cost of the simulator.

## 7. Full-Oracle Classical Comparison

The lower-bound argument is for opaque randomly relabeled cosets, NOT an
efficient natural source and NOT a restriction to the selected probes.
Choose L uniformly from the KNOWN alternating graph chart
`L_T=image[I;T]`, T=-T^T. Its size is `N=q^(n(n-1)/2)`.
The classical algorithm may even be told this chart promise. A lower bound
on this subfamily also bounds an algorithm required to solve the full family.
Using this prior avoids any assumption about component sizes or chart mass.

Write a fixed group matrix as [[A,B0],[C,D0]]. It fixes L_T exactly when

    C + D0*T - T*A - T*B0*T = 0.

If this polynomial identity holds identically on alternating T, its constant,
linear and quadratic parts vanish. Thus C=0, D0*T=T*A, and T*B0*T=0.
Using T=E_ij-E_ji in the quadratic identity kills every 2-by-2 principal
submatrix of B0, so B0=0. In the linear identity a third index kills all
off-diagonal entries of A,D0 and equates their diagonal entries. For n>=3
this forces A=D0=aI; orthogonality forces a=+1 or -1. Consequently any
noncentral g has at least one nonzero degree-at-most-two graph polynomial.
Schwartz--Zippel gives

    Pr_L[gL=L] <= beta = 2/q.

In particular the common stabilizer on this chart is exactly {+I,-I}. Universal
central collisions must be recognized rather than counted as information.
Couple any adaptive Q-query classical algorithm to a dummy transcript that
returns fresh random labels except for those known universal collisions.
Before the first other collision this transcript is independent of L. A
union bound on its fixed noncentral query differences gives

    Pr[correct output] <= 1/N + binomial(Q,2)*beta.

This yields a proposed Omega(sqrt(q)) classical query lower bound for
constant success, compared with polynomial quantum time in n and log q.
It says nothing exponential in n at fixed q. It does not transfer to labels
containing gL, to supplied coordinates, or to a succinct evaluator whose
implementation may leak additional structure. The simulator uses arbitrary
integer labels, but it does not itself establish this asymptotic bound.

A straightforward matched classical upper bound is substantially better than
the dense reference table: birthday collisions in each additive probe produce
uniform kernel differences. Repeating until their span is complete costs
O(poly(n,log(1/epsilon))*q^((n-1)/2)) expected queries, since the quotient
has at most q^(n-1) labels. Fresh collision batches avoid dependence issues;
the same final certificate checks the recovered L. This is a derived generic
baseline, not an implemented attack or a claim of optimality. The simulator's
q^(2n-2) table is deliberately NOT advertised as the best classical method.

The n=2 exception is substantive: a noncentral elementary SL2 Levi fixes
EVERY alternating graph. The polynomial argument and three-independent-probe
reconstruction both fail there. Do not remove the rank guard.

## 8. Second Route And Prior-Art Risk

An independent check uses a good alternating graph chart `L_S=image[S;I]`.
For E=E_ij, i!=j, let A_t=I+tE, U_X=[[I,X],[0,I]] for alternating X, and
D_t=diag(A_t,A_t^-T). Then

    f(U_X D_t)=F0(X+t*(E*S+S*E^T)),

with injective unknown F0, because `E*S*E^T=S[j,j]*E_ii=0`. Unlike the
symplectic symmetric-matrix case, this is LINEAR, not quadratic HPGP.
Each restriction is an abelian hidden-subspace problem. For each entry
S[j,k], choose i distinct from j,k; the coefficient at (i,k) is S[j,k].
At n>=3 these recover every entry. Bad charts require an independently
sound final certificate and paid random positioning. This second route is
an algebraic cross-check, not an implemented second receiver here.

This simplicity is a reason to be cautious about novelty. Abelian probes,
classical certification and query-collision bounds are established tools:
[Decker et al.](https://arxiv.org/html/1406.6511) give them for GL parabolics;
[Imran](https://arxiv.org/html/2610.28368v1) extends GL to chain rings.
Neither checked text states an orthogonal theorem. The rank-one related
groups are treated by [Denney--Moore--Russell](https://www.rintonpress.com/xxqic10/qic-10-34/0282-0291.pdf).
Search results and absent terminology do NOT certify this composition is new.
Rank three also has the accidental D3=A3 relationship, so finite rank-three
success is especially inadequate evidence of a new scope.

## 9. What Would Falsify Or Deprioritize This

- A legal radical element preserving L outside the claimed kernel falsifies
  the reduction. Exact controls exhaust all 260 probes in one F3 ambient.
- A wrong maximal singular R passing the certificate falsifies soundness.
  All 6,400 candidate/hidden pairs in the 80-space F3 geometry are checked.
- If hidden information enters through labels or the learner, the execution
  does not establish access legality. The reference controller receives only
  opaque labels; large-prime supplied-kernel checks are separately labeled.
- A polynomial classical algorithm using the SAME opaque full oracle would
  contradict the proposed lower bound, requiring its proof to be revisited.
- Existing equivalent algorithms would remove novelty, not correctness.
- Failure to find a useful non-oracle source sharply limits research impact.
  Do not build a new benchmark campaign around this result or claim that the
  oracle separation itself supplies a Shor-level application.

The worthwhile next step is independent scrutiny of this short reduction and
its full-oracle bound, plus a source search that retains the exact classical
access model. Routine controller integration is deferred during migration.
