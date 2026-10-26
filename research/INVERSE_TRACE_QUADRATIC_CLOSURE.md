# Inverse Trace: Coupled Degree-Two Linearization Still Admits False Answers

2026-10-22. Local theorem and exact countercertificates, REVIEW PENDING.
No general classical lower bound, solving-degree theorem, novelty claim,
quantum execution, or demonstrated speedup.

## Decision

INVERSE_TRACE_ALGEBRAIC_AUDIT.md ruled out a particularly weak procedure:
independent-monomial local equations plus UNMULTIPLIED global constraints.
Its explicit limitation was important. Multiplying global parity checks
by variables introduces genuine cross-block constraints. This note tests
that stronger next proposal instead of treating the earlier observation
as evidence against all algebraic attacks.

Result: for n>=5 and N>=2K+1, even the complete degree-two binary linear
relaxation described below has every linearly legal first-variable
assignment in its projection. In particular, for every nonzero target b,
it admits x=0 together with a suitable false inverse witness y. The
construction works after eliminating the original linear equations too.

Do not implement another degree-two equation-count/rank campaign hoping
that it alone will recover the native variables. Degree-three and higher
closure, product/rank consistency, nonlinear factoring, branching, and
adaptive native-witness constructions are NOT excluded.

## Exact Scope

The original task is unchanged: over F_q, q=2^n, distinct public alpha_i,

    H[j,i]=alpha_i^j, 0<=j<K;  Hx=0;
    y_i=inv0(x_i);  Tr(y_i)=b_i.

Inversion includes inv0(0)=0. Let C=ker(H), a high-rate dual-RS code.
The binary quadratic description x_i^2*y_i=x_i, x_i*y_i^2=y_i is exact.

The relaxation replaces each binary product z_r*z_s by an independent
coordinate M[r,s], where z consists of all x bits then all y bits. It
retains M symmetric, M[r,r]=z_r, and ALL of the following equations:

1. Every local Boolean polynomial identity of degree at most two that is
   valid on G_b={(x,inv0(x)):Tr(inv0(x))=b}, with the ACTUAL target b_i.
   This includes more than the five identities compiled in the first audit.
2. Every original global binary linear constraint L*z=c.
3. Every such linear constraint multiplied by EVERY original variable:
   L*M=c*z^T. Linear combinations and affine multipliers are thus included.

All arithmetic here is over F_2. M is a formal product table, NOT a real
positive-semidefinite matrix or the moments of a probability distribution.
No claim about sum-of-squares/convex relaxations over the reals follows.

## Lemma 1: The Target-Conditioned Inverse Graph Has Full Allowed Affine Hull

For n>=5 and b in F_2,

    aff_F2(G_b) = {(x,y):Tr(y)=b}.

Proof: parameterize G_b by y with Tr(y)=b. An affine relation has the form

    Tr(a*inv0(y)+c*y)=d  for every y with Tr(y)=b.

If a=0, the trace pairing is nondegenerate, so the only such relations
are the given hyperplane equation and tautologies. Suppose a!=0. Define

    T(a,c)=sum_y (-1)^Tr(a*inv0(y)+c*y).

If c=0, inversion is a permutation and T(a,0)=0. Otherwise the known
Kloosterman/Weil estimate, conservatively including the zero term, gives
|T(a,c)|<=1+2*sqrt(q). The character sum restricted to Tr(y)=b is

    [T(a,c)+(-1)^b*T(a,c+1)]/2.

Its absolute value is at most 1+2*sqrt(q)<q/2 for q>=32. A constant sign
on the whole hyperplane would instead have absolute sum q/2, a contradiction.
There are therefore no additional affine relations.

The executable certificate uses the weaker integer bound
1+2*ceil(sqrt(q))<q/2. The imported ingredient is classical character-sum
theory, not a new bound. See the definition and introductory estimates in
[Gologlu, McGuire and Moloney](https://www.impan.pl/shop/publication/transaction/download/product/82372).
We retain the conservative extra1 instead of transferring conventions.

Consequently, ANY desired pair (x_bar,y_bar) with Tr(y_bar)=b is an odd
binary sum of genuine points in G_b. Apply that same odd sum to their
quadratic product tables. It produces local first moments x_bar,y_bar and
local second moments satisfying EVERY target-conditioned local quadratic
identity. This is stronger than combining points with different targets.

## Lemma 2: Codewords With Separated Supports

For each coordinate i, choose disjoint sets A_i,B_i of K other coordinates.
This is possible exactly under the sufficient hypothesis N>=2K+1. There
are codewords u_i,v_i in C with respective supports {i}+A_i, {i}+B_i and
with u_i[i]=v_i[i]=1. Thus their supports intersect ONLY at i.

Explicitly, on any set S of K+1 distinct points, use coefficients

    w_r = 1 / product_(s in S, s!=r) (alpha_r-alpha_s).

For 0<=j<K, sum_r alpha_r^j*w_r=0 by comparing the coefficient of X^K
in the Lagrange interpolation formula for X^j. Normalize by w_i. This
derivation pays only public finite-field arithmetic; no hidden decoder,
codeword table, or exponential support enumeration is needed.

These are standard MDS support facts, not newly discovered coding theory.
For context see [MIT coding notes, Theorem8.4](https://ocw.mit.edu/courses/6-451-principles-of-digital-communication-ii-spring-2005/bb895c1dee9ce0b39d6846e0aa984981_MIT6_451S05_FullLecNotes.pdf).

## Theorem: Every Linearly Legal Projection Extends

Choose ANY x_bar in C and ANY y_bar with Tr(y_bar_i)=b_i. Lemma1 supplies
local quadratic product tables with those means. Subtract each local
rank-one table (x_bar_i,y_bar_i)*(x_bar_i,y_bar_i)^T to obtain local
covariances. A binary symmetric covariance has zero diagonal: its diagonal
is z_r+z_r^2=0. Denote the xx,xy,yy blocks by X_i,B_i,Y_i.
Here the matrix B_i is unrelated to the support set in Lemma2.

Let t be the binary vector representing absolute trace. Because the local
points all have the same target, the trace equation and all its variable
multiples give

    B_i*t=0,  Y_i*t=0.

We now construct a GLOBAL symmetric covariance Q with the prescribed
local blocks and with L*Q=0 for every homogeneous part of the global
linear equations.

### XX Blocks

An alternating binary n-by-n matrix is a sum of elementary matrices
e_r*e_s^T+e_s*e_r^T, r<s. For each term of X_i, take the binary encodings
p of the field codeword (basis_r)*u_i and q of (basis_s)*v_i. Add

    p*q^T + q*p^T

to the global xx covariance. Both p and q are native codewords, so both
sides obey every parity check. At coordinate i the diagonal block is the
required elementary alternating matrix. At any other coordinate one of
the two codewords vanishes, so that entire local diagonal block is zero.
The corrections at different i therefore do not interfere.

### XY Blocks

For each row r of B_i, let w be that binary y-row, placed ONLY in block i.
Add the outer product of the codeword (basis_r)*u_i and w to the global xy
covariance, and its transpose to yx. Its x columns obey H; its y rows
obey trace because w*t=0. It changes only the desired diagonal xy block.
Off-diagonal xy blocks are allowed and are what the uncoupled relaxation
was missing.

### YY Blocks And Assembly

Place Y_i on the local yy diagonal blocks and zero elsewhere. Their trace
constraints follow from Y_i*t=0. Combining all three constructions gives
L*Q=0. Set

    M = z_bar*z_bar^T + Q.

Then M is symmetric with Boolean diagonal z_bar. Since L*z_bar=c,
L*M=c*z_bar^T, as required. Every local block equals the odd sum of genuine
target-conditioned local tables, so all local quadratic identities hold.
This proves the theorem without assuming independence of any equation.

It also survives prior linear elimination. Write the affine solution space
as z=z_0+J*t with J injective, and take a left inverse R. The covariance
Q has image in ker(L)=im(J), so Q=J*(R*Q*R^T)*J^T. The middle matrix is
again alternating. This supplies a valid product table for the free binary
variables. Merely substituting the linear equations first does not repair
the degree-two relaxation.

For any nonzero target choose x_bar=0. Some b_i=1, so this is not a native
answer. The theorem supplies a relaxed product table anyway. In fact the
projection onto x is all of C, not just this one false point.

## Executable Countercontrols

`theorems/inverse_trace_quadratic_closure.py` implements the construction
with a separate verifier that recomputes every parity/trace equation and
its product with every variable. It also verifies symmetry, Boolean
diagonals, direct local inverse identities, and the stored odd sums of
genuine target-conditioned graph points. It does not trust reported ranks
or residuals as certificates of a native answer.

Local large-field controls use n17/31/61 with fixed capped sampling and
explicit field moduli. These do NOT enumerate the fields or construct the
large native global matrices. Failed local span acquisition is UNKNOWN.
The dense global controls use (n,N,K)=(5,3,1),(5,5,2),(7,7,3) and retain
the actual product tables. They are exact theorem countercontrols, not
quantum experiments or scalable solving benchmarks. Dense width is capped
at256 variables. Arbitrary nonzero projections and tampered tables are
tested separately.

## What This Does NOT Establish

- No native solution is obtained by the countercertificate. Its products
  deliberately do not equal the products of its projected variables.
- No lower bound on general solving degree, Groebner runtime, SAT, or a
  nonlinear degree-two solver follows. Factoring/rank enforcement and
  branching need not coincide with this linear relaxation.
- Degree-three and higher global/local products are not covered. Local
  identities of arbitrary degree alone were handled by the earlier note;
  global coupled higher-degree closure is a different question.
- N<2K+1 and n<5 are outside this proof, not claimed hard or easy.
- The previous n17/n31 native CLASSICAL witnesses remain valid. A weak
  algebraic relaxation failing to recover them does not erase that evidence.
- The quantum balanced-codeword proposal remains review-pending, with no
  established classical hardness or natural cryptanalytic application.

## Next Decision

Stop local-annihilator and plain quadratic-linearization campaigns. The
next classical attack must identify a concrete mechanism for enforcing
products or exploiting higher-degree cross-block structure, with native
output checks. More equations without that mechanism are not progress.
The alternate high-value task is independent review of the FULL quantum
construction, not implementation of a generic decoder before the input
family has survived serious classical scrutiny.

Replay: `python -m theorems.inverse_trace_quadratic_closure --write`.
Standalone report: `research/classical_baselines/inverse_trace_quadratic_closure.json`.
No central registry, qsearch, UI, Git, or automation changes.
