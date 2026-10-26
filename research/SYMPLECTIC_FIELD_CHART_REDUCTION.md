# A Field-Only Graph-Chart Reduction For Siegel HSP

2026-10-23. PROPOSED THEOREM AND PROOF, independent review pending.
The exact controls exercise matrix identities, oracle fibers and rejection
certificates. They do not execute a quantum HPGP solver. No novelty,
cryptanalytic application, or Shor-level discovery is claimed.

Ring-scope warning (2026-10-23): the new
SYMPLECTIC_CHAIN_RING_DIGIT_REDUCTION.md gives a separate odd-residue
ring algorithm. The final unipotent-only certificate and transvection
membership equivalence in THIS FIELD note are false for lifted ring
submodules. The ring lower-bound coupling must also quotient by its larger
common stabilizer, not just the center. None of those ring counterexamples
retracts the field statements under their original input contract.

## Decision

The prime-square route is not necessary for the finite-field Siegel case.
A random symplectic change of coordinates puts the hidden Lagrangian into
a graph chart with probability greater than one half. Actual unipotent and
elementary Levi queries then produce a degree-two hidden polynomial graph.
A final certificate remains sound even when the chart promise fails.

This is NOT the old invalid additive oracle on the whole symplectic Lie
algebra. No oracle is extended from a field to a ring, and no hidden matrix
is supplied as advice. The older ring result remains a different input
problem; neither construction automatically solves the other's inputs.

There is also a proposed FULL-ORACLE classical query lower bound below.
It is distributional over opaque labels, not a restriction to one probe
family. Its force is growing q, not growing rank at fixed q. This is still
a structured oracle result, not an application to an explicit hard problem.

## Input, Output And Dependencies

Supply an effective finite field F_q, q=p^a, with odd prime p, an F_p basis,
field arithmetic, n>=2, and G=Sp_(2n)(F_q) for J=[[0,I],[-I,0]]. A coherent
oracle of fixed polynomial output width satisfies

    f(g)=f(h) iff g P_W = h P_W iff gW=hW,

where W is an unknown n-dimensional Lagrangian and P_W is its full
stabilizer. We use LEFT cosets g P_W. An oracle supplied with the opposite
convention can be inverted on input, at the cost of public matrix inversion.
The output is a basis of W, hence an explicit description of P_W. This is
not an oracle hiding an arbitrary subgroup contained in that stabilizer.

Proposed conclusion: recover W with bounded error in time polynomial in
n, log(q), log(1/epsilon), charging all original oracle calls and arithmetic.
Rank one is excluded because the row-recovery construction needs i!=j;
the separate rank-one RING counterexample is not a field obstruction.

The only nontrivial quantum learning dependency is
[Ivanyos--Santha, Theorem 5 and Corollary 6](https://arxiv.org/html/1503.09016):
univariate constant-degree HPGP' over a prime field has a polynomial-time
quantum solution with growing output dimension. Here the degree is two,
the scalar field is F_p and the output dimension is a*n*(n+1)/2. The
state-source convention in their Definition 4 and equation (5) fixes the
minus sign below. This dependency is published; the unreviewed general
Rees algorithm is not used.

[Decker et al.](https://arxiv.org/abs/1406.6511) solve parabolic HSP in GL
over fields. [Imran](https://arxiv.org/html/2610.28368v1) treats GL over chain
rings. Neither is silently taken as an Sp theorem or a permission to query
outside Sp. Targeted searches for symplectic/Siegel/parabolic hidden-subgroup
algorithms did not identify this exact composition. That is not a novelty
check sufficient for publication. The primitives and several ingredients
are known; this may be a straightforward or already known application.

## 1. A Constant-Probability Chart, With An Actual Sampler

Let L0 be the top coordinate subspace. Draw a known uniform C in G and
define f_C(g)=f(C g C^(-1)); its hidden subspace is W'=C^(-1)W. If W' is
transverse to L0, it has a unique column basis

    W_S = image [S; I],       S=S^T in Sym_n(F_q).

The symmetry condition follows directly by evaluating the form J on the
columns. Write m=n(n+1)/2. There are q^m graph Lagrangians. The total number
Lambda_n of Lagrangians is product_(r=1)^n (q^r+1): count pairs (L,v!=0 in L)
and quotient by <v> inside v-perp to get

    (q^n-1) Lambda_n = (q^(2n)-1) Lambda_(n-1).

The group is transitive, so

    Pr[good chart] = q^m/Lambda_n
                   = product_(r=1)^n (1+q^(-r))^(-1) > 1/2.

For the last inequality, use product(1-u_r)>=1-sum(u_r) with
u_r=1/(q^r+1), and sum(u_r)<1/(q-1)<=1/2. This does not assume n is fixed.

Uniform C is available by symplectic basis sampling: in the remaining
nondegenerate 2r-space choose uniform nonzero v, then uniform w in the
affine hyperplane <v,w>=1, and recurse on their symplectic orthogonal
complement. Choose a deterministic coordinate basis for each complement.
Every symplectic basis has the same probability by induction. Linear
systems and uniform field elements cost polynomial time; nonzero-vector
rejection has constant expected cost. Cap rejection globally and charge
its failure. An unanalysed short random walk is NOT an adequate substitute.

## 2. Legal Queries And Exact Hidden-Polynomial Fibers

Fix i!=j, E=E_ij, and t in the PRIME SUBFIELD F_p. Put

    U_X = [[I,X],[0,I]],               X=X^T,
    A_t = I+tE,                       A_t^(-1)=I-tE,
    D_t = diag(A_t,A_t^(-T)),
    g(X,t) = U_X D_t.

These are actual matrices in G for all X,t, including t=0. They depend on
no secret. On a good chart their action is

    g(X,t) W_S = W_(X + A_t S A_t^T),
    A_t S A_t^T = S + P(t),
    P(t) = t B + t^2 C2,
    B = E S + S E^T,       C2 = E S E^T.

Define F0(X)=f_C(U_X). Since X->W_(S+X) is injective, so is F0, despite its
unknown labels. Consequently the derived oracle is exactly

    f_C(g(X,t)) = F0(X+P(t)).

Prepare uniform X in Sym_n(F_q) and t in F_p, compute the actual query,
call f, uncompute the query matrix/work registers, and measure the label.
Every fiber has p elements, giving a fresh normalized state

    (1/sqrt(p)) sum_(t in F_p) |t>|z-P(t)>,

with uniform z in Sym_n(F_q). The unknown constant S is absorbed into F0;
we never read an image-subspace matrix out of an oracle label. Only ONE
original f query is used per source state, with charged reversible matrix
arithmetic. Do not call this one query for an entire HPGP solution.

Expand the m symmetric entries in the supplied F_p basis of F_q. Because
t belongs to F_p, this is HPGP'(F_p,1,a*m,2) with Q=-P. After learning Q,
NEGATE its coefficients before reconstruction. Degree two is below p.
Using t in all of F_q and citing a prime-field theorem would leave a gap;
restriction of scalars here avoids that gap without treating Z/p^a as F_q.

## 3. Learn Every Row

For each j choose i=(j+1) mod n and learn the corresponding B,C2. Then

    B[i,k] = S[j,k]    if k!=i,
    B[i,i] = 2 S[j,i].

Thus n HPGP calls determine S, using the inverse of 2. Recompute expected
B,C2 from the answer and reject malformed or inconsistent data. Each call
has its FULL polynomial source budget. Supplying B from the known test
secret is a proof control, not an implementation of the learner.

Under a known good chart, four queries also certify a proposed B,C2:
compare f_C(g(0,t)) with f_C(U_(tB+t^2 C2)) for t=1,-1. Injectivity of F0
and invertibility of 2 determine both coefficients. Testing only t=1 misses
the substitution (B,C2)->(B+D,C2-D).

IMPORTANT: these local checks are NOT sound without the chart promise.
For W'=L0 all U_X and D_t stabilize W'. Every derived label is constant;
B=C2=0 passes every local check but gives the wrong subspace [0;I]. The
next section supplies the missing global rejection certificate.

## 4. A Sound Final Certificate Even On A Bad Chart

For any proposed symmetric S_hat set

    T_hat = C [[S_hat,-I],[I,0]],
    W_hat = T_hat L0.

This T_hat is known and symplectic. Let B run over the m standard symmetric
matrix basis elements over F_q. Check, using the ORIGINAL oracle,

    f(T_hat U_B T_hat^(-1)) = f(I).

This uses m+1 calls with f(I) shared, not a search over all q^m matrices.
All tests pass for the true W. Conversely conjugate everything by T_hat.
The hidden n-space V must be invariant under each U_B, hence under N_B=U_B-I.
Since V is F_q-linear, it is invariant under every F_q-linear combination
N_X. Therefore it is invariant under ALL U_X for X symmetric.

The only n-dimensional subspace with this property is L0. If (x,y) lies in
V with y!=0, then (Xy,0) lies in V for every symmetric X. The map X->Xy is
surjective: choose j with y_j!=0, set X_kj=w_k/y_j for k!=j, impose symmetry,
and choose X_jj so the remaining coordinate is w_j. Thus V contains L0 as
well as a vector outside it, contradicting dim(V)=n. Otherwise V is L0.
This proves W_hat=W whenever the certificate passes, even after completely
arbitrary HPGP outputs on a bad chart.

Subtle extension-field point: these m basis elements do NOT generate the
whole additive unipotent group over F_p when a>1. The proof uses F_q-LINEAR
INVARIANCE of the promised subspace, not that false group-generation claim.
Using all a*m F_p-basis elements would also be sound, but is unnecessary.

This also proves faithfulness: distinct Lagrangians have distinct full
stabilizers. An oracle hiding a proper subgroup, approximate label
collisions, or a non-F_q-linear object would not satisfy this verifier proof.

## 5. Complete Bounded-Error Procedure And Costs

Each independent attempt does the following:

1. Sample C with a charged bounded clock.
2. Run the n degree-two HPGP instances, with per-call error at most 1/(4n).
   Include amplification and runtime-cutoff failure in that allowance.
   Enforce polynomial clocks on ALL histories, including bad-chart inputs
   that violate the HPGP promise. Malformed/capped outputs abort the attempt.
3. Reconstruct S_hat, check its symmetry and coefficients, and optionally
   perform the local checks. Apply the mandatory final certificate.
4. Return W_hat on success; otherwise start a fresh independently chosen C.

Conditioned on a good chart all calls succeed with probability >=3/4, so
each ideal attempt succeeds with probability >=3/8. R attempts fail with
probability at most (5/8)^R. Take R=ceil(log(2/epsilon)/log(8/5)) and spend
the remaining epsilon/2 on field sampling and whole-circuit approximation.
Return ABORT after R failures, not a fabricated subgroup or a no-go result.
The exact final verifier gives no false positive under the oracle promise.

Let Q2(a*m,log(p),eta) be the FULL source-copy bound of the published
degree-two algorithm including amplification/caps. Original-oracle calls
are bounded by

    R * [n*Q2(a*m,log(p),1/(4n)) + 4*n + m + 1],

where 4*n is optional local certification. Public field/matrix arithmetic,
state preparation, all stored copies and error precision are also paid;
the resulting bound is polynomial, not a practical resource estimate.
No exponential enumeration from the exact tests is part of this algorithm.

If subgroup generators are required, symplectically complete the recovered
basis and conjugate generators of the standard Siegel parabolic: upper
symmetric unipotents and diag(A,A^(-T)) for GL_n generators. Field-basis
elementary generators and unit-group generators must be constructed and
charged. Unlike the verifier, GROUP generation of all unipotents needs the
F_p coefficient basis. A basis of W already specifies the output without
assuming unit generators are supplied for free.

## 6. An Unrestricted Classical Query Lower Bound

This is an adversarially checked proof proposal, not a simulated baseline.
Let S be uniform in Sym_n(F_q), and independently label the left cosets of
P_(W_S) by a random injection into a known sufficiently large finite set.
Its labels have polynomial bit width, for example O(log|G|). The classical
algorithm may be randomized, adaptive, computationally unbounded, and query
ANY g in G. It is not confined to upper unipotents or elementary probes.

### Fixed-point bound

For g=[[A,B],[C2,D]], invariance of graph W_S is equivalent to

    A S+B - S C2 S - S D = 0.

Each entry is a degree-at-most-two polynomial in the m independent entries
of S. If every entry is the ZERO FORMAL POLYNOMIAL, the constant part gives
B=0. The quadratic part gives S C2 S=0 identically; evaluate at S=I to get
C2=0. The linear part gives AS=SD for every symmetric S. Taking S=I gives
A=D. Commutation with all diagonal units and symmetric off-diagonal units
then gives A=lambda I. Symplecticity gives lambda^2=1. Thus only the known
center Z={I,-I} can make all these polynomials identically zero.

For each noncentral g, at least one nonzero polynomial has total degree at
most two, hence has at most a 2/q fraction of zeros on uniform S by the
elementary polynomial zero-counting bound. The standard induction conditions
on all but one variable, separates vanishing leading coefficients, and
uses that a nonzero univariate degree-d polynomial has at most d roots.
Therefore Pr_S[g in P_(W_S)] <= 2/q. This applies to every matrix in G,
not just to the generators checked by the test suite. Odd q>=3 suffices.

### Adaptive transcript coupling

Simulate the algorithm using fresh random distinct labels for each queried
center coset gZ, reusing labels only for already queried center cosets.
This entire simulated query sequence and its output are independent of S.
Couple its labels to the real random coset-label oracle until the first
collision between two distinct center cosets that are equal modulo P_W.

For each pair of distinct center cosets, the relative matrix is noncentral.
Conditioned on the simulated path, its collision probability over S is at
most 2/q. The union bound over at most Q*(Q-1)/2 pairs gives divergence
probability at most Q*(Q-1)/q. Adaptivity is allowed because the SIMULATED
path, unlike a collision-conditioned real path, is independent of S.

The simulator's output matches the random hidden S with probability at
most q^(-m); stabilizer faithfulness makes this also true for subgroup
output. Coupling therefore gives

    Pr[success after Q classical queries]
        <= min(1, q^(-m) + Q*(Q-1)/q).

In particular bounded-error worst-case classical query complexity is
Omega(sqrt(q)). This is exponential in log(q), including at fixed n=2.
Do NOT argue simply that 'no collision means no information': conditioning
on noncollisions excludes possible secrets. The coupling is what pays for
that effect. Known center collisions are deliberately excluded; including
them would invalidate the fixed-point estimate.

### What this bound does not establish

- It is weak at fixed q and large n; it proves no exponential-in-rank bound.
- It is a worst-case random-label oracle separation, NOT a claim that every
  hiding-label encoding is hard. Labels exposing gW reveal W in one query.
- A random lookup oracle need not have a short natural reversible circuit.
  No explicit computational problem inherits this bound without a separate
  efficient source/reduction argument. That is the central impact blocker.
- It does not establish a practical quantum advantage or a cryptographic
  attack. The published HPGP polynomial may have large constants/exponents.
- It gives a lower bound, not a matching classical upper bound. A valid
  transvection baseline samples v and tests membership using f(I) and f(T_v).
  For a Lagrangian W, T_v preserves W iff v lies in W; accepted uniform
  vectors arrive with probability q^(-n). Spanning recovery costs expected
  O(q^n*(n+log(1/delta))) queries. Do not call that polynomial in log(q).

## 7. Attempts To Break The Claim

| Attack or suspected gap | Resolution or surviving limitation |
| --- | --- |
| Field oracle was extended to a ring | No: every query is in the original Sp(F_q). |
| Hidden S was used to build queries | No: only reference controls receive S; the learner must obtain coefficients through HPGP. |
| Graph chart occurs exponentially rarely | Count gives probability >1/2 uniformly in n for odd q. |
| A small random walk supplies a uniform chart | Not assumed; a symplectic-basis sampler is specified. |
| Bad-chart HPGP outputs pass local tests | They can; the L0 counterexample is explicit. The final certificate is necessary. |
| Extension-field theorem was imported without justification | Scalar t is F_p and outputs use a supplied F_p basis; degree remains two. |
| Small verification basis fails to generate all field elements | Generation is not needed for verification; F_q-linearity supplies invariant operator combinations. |
| Coefficients have the wrong sign or orientation | Graph is [S;I], Q=-P, and row formula uses E_ij S+S E_ji. Ring formulas differ. |
| Classical lower bound counts only a weak attack family | It considers every Sp matrix via its block graph-invariance polynomial. |
| Adaptive noncollision information defeats the bound | Independent simulated paths and a divergence coupling account for it. |
| Labels give extra algebraic information | They may; the classical lower bound explicitly uses independent opaque labels. |
| This is automatically new or useful | Unresolved. Known-primitive composition and missing natural input are major limitations. |

Further decisive falsifiers are a counterexample to the exact fiber identity,
a wrong n-space passing all final certificate queries, a noncentral matrix
fixing more than 2/q of graph subspaces, or a mismatch in the published
growing-dimension HPGP source contract. Any such finding invalidates the
corresponding claim, irrespective of the finite tests that passed.

## 8. Artifacts And Next Decision

`theorems/symplectic_field_chart.py` constructs prime-field public queries,
reference coefficients, postprocessing and final certificates; it also
evaluates the exact chart density and the proposed classical-bound formula.
It does not implement random chart sampling or a quantum HPGP learner.
`tests/test_symplectic_field_chart.py` includes complete rank-two small
fibers, all 40 Lagrangians over F3, large-prime arithmetic, extension-field
F9 fibers via FLINT, bad-chart rejection and center-aware controls. These
are algebraic proof falsifiers, not empirical quantum/classical timings.

The next HIGH-VALUE work is independent whole-proof/prior-art review and an
explicit useful input source for this stabilizer promise. In particular,
identify the accessible data, prove equality of labels is exactly equality
of parabolic cosets, and cost a coherent evaluator. Do not build a synthetic
random-label search campaign or infer such a source from the word
'symplectic'. Do not spend the next pass only extending nearby fields or
adding more successful finite fixtures. Without a meaningful application
or a new broadly useful mechanism, this remains a scoped structural result.

Follow-on source audit: SIEGEL_NATURAL_SOURCE_AUDIT.md rules out two tempting
shortcuts. An accessible torsion basis plus coherent isogeny evaluation
already permits abelian kernel recovery. Unmarked isogeny codomains can
identify distinct kernels, as an explicit polarized product counterexample
shows. A concrete weak-representation/marked-label source lemma is still
needed; neither issue is repaired by a synthetic oracle benchmark.
