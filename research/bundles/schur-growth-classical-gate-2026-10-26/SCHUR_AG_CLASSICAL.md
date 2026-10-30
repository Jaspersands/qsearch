# Full-Support Code Intersection: Classical Gate For The AG Extension

## Decision And Status

Do not promote standard high-degree algebraic-geometry (AG) evaluation codes
as a new quantum-advantage family merely because their Schur square is small.
For the full-support problem below, the existing classical quadratic ansatz
solves every syndrome throughout the nonvacuous regime of the specific
quantum guarantee being considered. This includes growing genus, arbitrary
odd finite fields, and monomially equivalent public matrices.

This is a written project deduction from known tools, with exact finite
controls, NOT an independently reviewed theorem or a novelty claim. The
classical algorithm is prior art. No quantum algorithm was run. No general
quantum lower bound, cryptographic break, or classical-hardness result follows.
In particular, the native inverse-trace, halfset and cubic-orbit problems are
NOT changed or dequantized by this result.

## Native Input And Primary Ingredients

The explicit input is a full-row-rank matrix B over F_q, of size k by m, and
a syndrome s. Output y satisfying B y=s and y_i != 0 at EVERY coordinate.
There is no hidden evaluation oracle or supplied solution. The implementation
uses verified odd primes below 2^63; the mathematical statement allows odd
prime powers with ordinary explicit field arithmetic.

Let V=rowspan(B), W=span(V*V), U=span(V*V*V), where * is coordinate product.
For a coordinate set Z, T[Z] means vectors of T that VANISH on Z, not vectors
supported on Z. Write Z(c) for the zero positions of c.

[Ragavan-Shutty, 2610.00502v1](https://arxiv.org/html/2610.00502v1),
Theorem 5.4 and Lemma 6.4, give the expressions

    Q = 2 q^k sum_{c in V, c != 0} q^dim(W[Z(c)]) / (q-1)^wt(c),
    C = 1/(q-1) sum_{c in V, c != 0} q^(dim(U[Z(c)])-wt(c)).

The quantum failure guarantee is Q+epsilon with runtime polynomial in m,q
and log(1/epsilon). The classical expression C is a union bound for the
rank test of their annihilator algorithm. These are NOT actual failure
probabilities. A value above one is vacuous. Fixed-q complexity must not be
silently reinterpreted as polynomial in log(q).

The AG multiplication input is standard:
[Couvreur, Marquez-Corbella, Pellikaan, Theorem 5 and Corollary 6](https://arxiv.org/html/1401.6025v3),
also [IEEE TIT 2017](https://doi.org/10.1109/TIT.2017.2712636).
If deg(G)>=2g+1, products of t sections of L(G) span L(tG).
Riemann-Roch and evaluation then determine the relevant code spaces. These
facts, not recovery of secret curve equations, are what the proof uses.

## 1. General Comparison Gate

Suppose a known v in V is verified to have no zero coordinate. Multiplication
by v maps W injectively into U and preserves every coordinate zero set. Put
Delta=dim(U)-dim(W). The map

    U[Z] / (vW)[Z] -> U/(vW)

is injective. Consequently dim(U[Z])-dim(W[Z]) <= Delta for every Z. Comparing
the individual nonzero-codeword summands gives

    C <= q^(Delta-k)/(2(q-1)) * Q.

The omitted factor ((q-1)/q)^wt(c) is at most one. Thus when the displayed
factor is at most one, a nonvacuous quantum guarantee also implies a
nonvacuous classical guarantee. For odd q this includes Delta<=k+1, not
only Delta<=k. This is a sufficient-comparison gate, not a necessity result.
Failure to verify v or the inequality yields NO CERTIFICATE, not advantage.

There is also a useful universal floor on Q. Since dim(W[Z]) >= dim(W)-|Z|,

    Q >= 2(1-q^(-k)) q^(2k+dim(W)-m).                 (1)

This bounds the expression Q from below, NOT the quantum failure probability.
In particular, 2k+dim(W)>=m makes this published guarantee vacuous for q odd.
Both checks use only matrix operations and integer arithmetic.

## 2. Checked Constructive Classical Completion

Take h in U^perp, T=support(h). If rank(B_T)=k, choose a k-column information
set I in T and let w be its indicator on T. Given a nonsquare nu, put

    y0_i = (w_i^2/h_i - nu*h_i)/4,       i in T,
    s'   = s - B_outside * 1,
    (B_T diag(w) B_T^t) z = 2(s' - B_T y0),
    u    = B_T^t z,
    y_i  = h_i*((u_i+w_i/h_i)^2-nu)/4,  i in T,
    y_i  = 1,                          i outside T.

The square matrix on the left is B_I B_I^t. It is invertible because B_I
is square and invertible; no positive-definiteness assertion over F_q is
being made. The quadratic term in B y vanishes by h perpendicular to V^3,
and the linear term is exactly the solved equation. A nonsquare makes all
entries nonzero. Every output is independently checked against the ORIGINAL
B,s. A failed rank test is UNKNOWN/RETRY, never UNSAT or evidence of hardness.

This is the published quadratic ansatz, with an explicit choice of pivot
columns and a deterministic first-annihilator option. It is not our new
quantum mechanism and does not produce uniformly distributed witnesses.

## 3. Every Nonzero AG Annihilator Passes

Let X be a smooth projective geometrically connected curve of genus g over
F_q. Let D be m distinct rational points, G a divisor disjoint from them,
and d=deg(G). Initially suppose d>=g, V=ev_D L(G), and the input rows are
independent. Put A3=ev_D L(3G). If

    m > ell(3G) = 3d-g+1,                            (2)

then A3^perp contains a nonzero h. EVERY such nonzero h has rank(B_support(h))=k.

Proof. If not, some nonzero row combination c=ev_D(f) vanishes on support(h).
Its zero set Z has size z<=d, since (f)+G is effective of degree d and G
does not meet D. Hence h is supported on Z. But

    deg(3G-Z) = 3d-z >= 2d > 2g-2,
    ell(3G)-ell(3G-Z) = z.

The evaluation L(3G) -> F_q^Z is surjective, by Riemann-Roch. No nonzero
vector supported on Z can annihilate all these evaluations, a contradiction.
Equivalently, this is the familiar designed dual-distance argument. Also
V^3 is contained in A3, so h is legal for the constructive completion. QED.

For d>=2g+1 the multiplication theorem gives U=A3. Therefore the solver
computes everything directly from B: form the Schur cube, take any nonzero
kernel basis vector, pass the rank check, and complete the witness. No curve
reconstruction, random h retries, or hidden AG representation is necessary.

Under this promise the EXACT failure probability of uniform h in U^perp
is q^(-dim(U^perp)): only h=0 fails. The union bound C counts this same bad
event once per projective codeword and can be greater than one. The
deterministic nonzero basis-vector choice removes that failure entirely.

Monomial equivalence does not defeat the construction. With coordinate
multiplier v, the cube is v^3*A3. If h annihilates that cube then v^3*h
annihilates A3 with the same support. Row-basis changes and coordinate
permutations preserve the argument. The implementation does not infer the
AG promise from dimensions; its individual output remains directly checked.

## 4. Covers The Nonvacuous Published Quantum Regime

Now assume 2g+1<=d<m and V=ev_D L(G), including its monomial equivalents.
Set

    k = d-g+1,
    a = ell(2G-D),
    dim(W) = 2d-g+1-a.

We must allow 2d>=m; ignoring the evaluation kernel a would be a gap.
Suppose m<=3d-g+1. If m>2d then a=0 and

    2k+dim(W)-m >= d-2g+2 >= 3.

If m<=2d, the elementary bound a<=2d-m+1 instead gives

    2k+dim(W)-m >= 2d-3g+2 >= g+4.

In either case (1) forces Q>1. Contrapositively,

    Q<1  ==>  m>3d-g+1  ==>  the deterministic classical completion applies.

Thus any positive-success certificate from this particular quantum theorem
on standard high-degree AG codes already lies inside a deterministic
classical regime (once a nonsquare is supplied or sampled). This comparison
does not require computing the exponential sum Q. It does not assert that
the quantum algorithm fails outside its sufficient guarantee.

## 5. Adversarial Checks And Scope Limits

- High genus looked like an escape from the dimension gate. It is not an
  escape from the stronger rank argument. The genus-three control has
  Delta=k+2, so the first gate is inconclusive, but every nonzero h works.
- The shortening notation is easy to reverse. Tests check zero restrictions
  directly, including every nonzero elliptic codeword.
- Cubes need not equal ev L(3G) below d=2g+1. The general d>=g lemma requires
  actual access to A3; no secret Riemann-Roch basis is given for free.
- Special-divisor codes, arbitrary subcodes, multivariate codes and restricted
  alphabets are not covered by the matrix-only AG theorem. They remain
  unassessed here, not certified advantage candidates. A supplied AG parent
  does give the first lemma for its subcodes under (2), but may be additional
  advice; a weaker length bound or hidden parent requires separate work.
- The input is full support, not Tr(inv0(y_i))=b_i. The latter is in
  characteristic two, where both the predicate and the nonsquare ansatz
  differ. Translating this result into native inverse-trace hardness or
  dequantization would be invalid.
- Exact finite controls test implementation and fragile identities, not the
  asymptotic theorem. No independent reviewer or proof assistant checked it.
- The proof is a specialization of known multiplication, dual-distance and
  quadratic-ansatz tools. Do not label it a literature-first discovery.

## 6. Resources, Controls And Next Decision

From explicit B, RREF, pair/triple products, nullspace and completion require
polynomially many field operations in k,m. A conservative dense bound is
O(k*m^4) field operations and O(k*m^2) field elements of temporary storage;
the backend is not optimized. A public nonsquare can be found by uniform
nonzero sampling with Euler testing, expected two trials, polynomial in
log(q) for prime fields. Given it, the AG branch needs no randomness. A hard
trial cap must return UNKNOWN rather than pretend to have a nonsquare.

The Python backend validates a supplied nonsquare and restricts p<2^63.
It is not an arbitrary-size field implementation. Exact Q,C enumeration is
refused beyond 4096 codewords; exhaustive annihilator controls beyond 10000.
Neither enumeration is part of the scalable classical solver or proof.

Controls use smooth curves y^2=x^(2g+1)+x+c with G=(2g+1)*infinity:

| g | p | c | m | k | dim W | dim U | nonzero h checked |
|---|---|---|---|---|-------|-------|-------------------|
| 1 | 11 | 6 | 12 | 3 | 6 | 9 | 1330 |
| 2 | 19 | 1 | 15 | 4 | 9 | 14 | 18 |
| 3 | 19 | 1 | 22 | 5 | 12 | 19 | 6858 |

All return original-relation witnesses. The third is deliberately beyond
the growth gate. Its C is vacuous even though the actual random-h failure
is 1/6859. These small examples are arithmetic controls, not hard benchmarks.

Research decision: reject the naive high-degree AG extension and stop genus
parameter sweeps. Before spending on a new coding candidate, specify an
actual route around the cubic annihilator completion, not just a small square
or a vacuous classical bound. For subcodes, test auxiliary-code and Schur-
closure attacks first. For the native inverse-trace problem, keep the
existing global-decoder assumptions and public-carry gap separate.
