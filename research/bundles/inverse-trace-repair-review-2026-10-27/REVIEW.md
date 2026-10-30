# A Scoped Obstruction To Monotone Block Repair

2026-10-27. Independent mathematical review. No source, Git, or UI changes.

**Result:** a rigorous counterexample to a plausible worst-state repair
theorem, including the previously proposed residual block size. Fresh
accepted-root proposals, parity completion, and nonincreasing-defect
acceptance do not give polynomial repair from every one-defect codeword.
This is a first-move obstruction from a NONSOLUTION, not the earlier
solution-conditioned mixing argument. It is not a general hardness result
or a claim of literature novelty. No asymptotic solver was obtained.

## Native Input And The Repair Rule

Keep exactly the supplied field F_q, q=2^n, public irreducible basis,
growing prime n, N=n^2 distinct arbitrary alpha_i, K=floor(N/8), and
H_{j,i}=alpha_i^j for 0<=j<K. Write C=ker(H), f(z)=Tr(inv0(z)), and
D_b(x)=|{i:f(x_i)!=b_i}|. Zero remains legal exactly when its bit permits.

Fix a catalogue of L blocks B of size m=K+r<=N-K, before the starting
codeword and targets are generated. The catalogue may depend on the public
points. Consider this natural repair algorithm:

1. Given current x in C, select any catalogue block B and any r-subset F
   of B, adaptively using x, b, and the entire previous transcript.
2. Independently sample fresh uniform accepted values on F. Freeze x
   outside B, then solve the K parity equations for B\F.
3. Accept only if the total number of defects does not increase.

Every K-column submatrix is invertible, so this proposal is constructive.
The theorem permits arbitrary adaptive information sets, not just one
fixed pivot set. It does NOT permit arbitrary biased choices of the free
accepted values or blocks outside the predeclared catalogue.

## Counterexample Distribution And Bound

Fix any coordinate j. Sample X uniformly from C by ordinary systematic
linear completion, and set

    b_i = f(X_i) XOR 1_{i=j}.

Thus X is a known, invalid starting codeword with exactly one defect; no
solution is supplied or planted. This construction works for EVERY set of
distinct public points. Define

    rho = (2*sqrt(q)+3)/q,       p = (1+rho)/2,
    A = L * binom(m,r) * 2^r * (m+1) * p^(K+1).

For n>=5, rho<1. For the rule above, after at most T proposals,

    Pr[any nonzero accepted move, or a witness] <= min(1, T*A).       (1)

Probability is over X and the algorithm's coins. In particular, for

    r = ceil(4K/n),       L,T = poly(n),

the right side is 2^(-K+O(n log n)) = 2^(-Omega(n^2)). This is the EXACT
residual block size from the previous reduction, not a small-bit-block
substitute. It refutes a polynomial guarantee for every one-defect start.
It does not describe initialization from a uniform codeword independent
of a fixed, externally given b.

These are feasible native inputs, not empty-fiber counterexamples. The
previous uniform fiber estimate gives, for every b at sufficiently large n,

    |{x in C:f(x)=b}| = q^(N-K)*2^(-N)*(1+e_b),
    |e_b| <= q^K * [beta+(1-beta)/q]^N = o(1),
    beta = (1+2*sqrt(q))/q.

At K/N asymptotic to 1/8, the displayed error is
2^(-3*n^3/8+O(n^2)). The generated b is therefore covered too.

## Proof

**Exact independence, with its scope.** Any at most N-K coordinates of a
uniform X in C are independent uniform field elements: the remaining at
least K columns have full row rank and every prescribed projection has
the same number of completions. Separately, the shortened code

    C_B = {delta in C:supp(delta) subset B}

has dimension r and minimum nonzero weight at least K+1. On any r
coordinates of B its projection is bijective. Consequently, for fixed x,
a uniform proposal Y in x+C_B satisfies the prescribed bits on F with
probability EXACTLY 2^(-r). Step 2 is exactly this uniform proposal
conditioned on those r predicates. No independence after further
conditioning is assumed.

**Scalar translation bound, including zero.** Put psi(u)=(-1)^Tr(u).
For d!=0 and a=d^(-1), direct substitution x=d*t gives

    q*c(d) := sum_x (-1)^[f(x)+f(x+d)]
            = Kl(a)-1+2*psi(a),
    Kl(a)  := sum_{u!=0} psi(u+a/u).

Indeed, away from t=0,1, the inverse sum is a/(t^2+t). The map
t -> t^2+t is two-to-one onto the trace-zero subspace. The nonzero image
contributes Kl(a)-1; the two totalized endpoints contribute 2*psi(a).
The classical bound |Kl(a)|<=2*sqrt(q) therefore gives |c(d)|<=rho.
Thus either value of f(U+d) XOR f(U), for uniform U, has probability at
most p. The Kloosterman normalization and elliptic-curve relation are
checked against [Ahmadi--Granger, Section 1 and Lemma 2.1](https://arxiv.org/pdf/1104.3882).

**A fixed nonzero displacement.** Fix delta in C_B, with weight w.
Since w<=m<=N-K, the bits

    f(X_i+delta_i) XOR f(X_i),     i in supp(delta),

are independent, each with either probability at most p. If j belongs to
the support, D_b(X+delta)<=1 allows only w+1 bit patterns: no change,
flip j, or flip j and one other position. If j is outside, only no change
is allowed. Hence

    Pr_X[D_b(X+delta)<=1] <= (w+1)*p^w
                              <= (m+1)*p^(K+1).                  (2)

**Pay for the actual proposal.** For each fixed B,F,x, conditioning the
uniform displacement on the r free-coordinate predicates increases the
probability of any event by at most 2^r. Averaging over X and uniform
delta in C_B, excluding delta=0, equation (2) gives

    E_X Pr[nonzero nonworsening proposal | X,B,F]
        <= 2^r*(1-q^(-r))*(m+1)*p^(K+1)
        <= 2^r*(m+1)*p^(K+1).                                   (3)

Let a(X) be the maximum such transition probability over all L*binom(m,r)
choices. Maximum is at most sum, so E[a(X)]<=A. Before the first nonzero
accepted move the state remains X, even with neutral moves permitted.
Conditional on X and any rejection transcript, the next proposal uses a
fresh draw from one of these kernels. Its chance of moving is at most
a(X). A union bound over T attempts proves (1). This explicitly handles
adaptive block/information-set selection WITHIN the catalogue; it does not
assume that failed attempts preserve the initial distribution of X.

## Stronger Existence Failure For Smaller Blocks

There is also a counterexample independent of the proposal distribution.
Union (2) over all q^r-1 nonzero displacements in each fixed block:

    Pr_X[any nonzero nonworsening move in the catalogue]
        <= L*(q^r-1)*(m+1)*p^(K+1).                              (4)

For r=floor(K/(2n)) and polynomial L, this is at most
2^(-K/2+O(log n)). With the complementary probability, X is a strict
one-defect local minimum: even exhaustive search of every field assignment
in every catalogue block finds no nontrivial nonworsening move. This is a
probabilistically specified native counterexample family, not a claim that
an individually sampled example has been exhaustively certified.

## Costs, Checks, And Limits

Generating X,b costs polynomial time: O(K^3+KN) field operations for
systematic completion, then N inverse/trace evaluations. A proposal costs
O(K^3+Kr) field operations with naive elimination, r accepted-root samples,
and verification. Uniform accepted roots are obtained by sampling the
appropriate trace hyperplane and applying inv0. A full native verifier
uses O(NK) field operations plus N inversions/traces. All field operations
are polynomial in n; no field-size lookup table is assumed. Enumeration
of q^r candidates is used only in the proof of (4), not as a cheap routine.

Bounded arithmetic controls run during this review:

- Exhaustively verified the scalar identity for all nonzero d in F_8,
  F_32, F_128 with moduli X^3+X+1, X^5+X^2+1, X^7+X+1. All 165 checks
  passed, including endpoint values; these are identity controls only.
- Replacing sqrt(q) by ceil(sqrt(q)) and using integer comparisons gives
  the following certified upper bounds for L=N. Multiply the A column
  by T in (1); the n=17 residual-size bound is vacuous.

| n | Residual m,r | Upper bound on A | Smaller m,r | Bound in (4) |
|---|---|---|---|---|
| 17 | 45,9 | 2^16 | 37,1 | 2^-6 |
| 31 | 136,16 | 2^-20 | 121,1 | 2^-73 |
| 61 | 496,31 | 2^-250 | 468,3 | 2^-262 |
| 127 | 2080,64 | 2^-1519 | 2023,7 | 2^-1103 |

These are theorem-bound evaluations, not solver benchmarks. No SAT,
large-flat, norm-carry, or native witness campaign was run.

**What remains open:** state-dependent construction of new supports from
the full exponential set of blocks; biased/adaptive free-value proposals;
uphill steps, annealing, restarts, or a special distribution of near-solutions
that avoids these inputs. In particular, replacing L by all binom(N,m)
blocks destroys the useful bound. The existence of many global witnesses
or almost-all-syndrome residual extensions does not furnish these missing
algorithms, but neither does this obstruction rule them out. The parent's
fixed-prime full-support-code approach is outside this result.

**Prior-work boundary:** read the requested
[classical algebra audit](</Users/jaspersands/Desktop/quantum algorithm search/research/independent_review_2026_10_22/CLASSICAL_ALGEBRA.md>),
[residual attack](/Users/jaspersands/Developer/qsearch-research-work/inverse-trace-residual-2026-10-23/RESIDUAL_ATTACK.md), and
[accepted-flat note](</Users/jaspersands/Desktop/quantum algorithm search/research/RECIPROCAL_TRACE_FLATS.md>),
plus their classical restriction, sampling, and Gibbs audits. Their
accepted-flat and residual existence statements are retained, not promoted
to algorithms. The new deduction here is the scoped nonsolution-start
repair bound (1), with the stronger small-block counterexample (4).
