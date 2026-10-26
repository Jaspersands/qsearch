# Accepted Flats In Random Cubic / Dual-RS Systems

Status: finite classical countercheck; mathematical derivation review pending.
No new quantum algorithm, asymptotic dequantization, or novelty claim.

## Question And Source

Can inexpensive local affine restrictions solve substantial finite instances
of a published succinct-input quantum search proposal?

The input distribution follows Section 3 of Briaud, Dinur, Ghosal, Jain, Lou,
and Sahai, [Quantum Advantage via Solving Multivariate Polynomials,
arXiv:2509.07276v1](https://arxiv.org/html/2509.07276v1).
There are m=n^2 independent uniform degree-at-most-three Boolean polynomials
f_i, each on n separate bits. Identify each block with F_(2^n). For distinct
public points gamma_i, set H[j,i]=gamma_i^j for 0<=j<r. Find x satisfying
every f_i(x_i)=0 and Hx=0.

The paper establishes an expected polynomial-time quantum algorithm in its
asymptotic parameter regime; classical hardness for cubics is conjectural.
Its Section 5.1 analyzes quadratic specialization and an asymptotic obstruction
to large cubic affine restrictions. Appendix A benchmarks a different,
specialized Groebner approach. We do not reproduce those timings or compare
them as matched benchmarks. The present finite test does not contradict the
paper's asymptotic statement.

## Concrete Classical Algorithm

For each block, build a zero flat

    A_i = a_i + span(v_i1,...,v_ik).

Start with a random accepted point. At each stage, draw a random direction
outside the current direction span, and evaluate every new point in the
candidate extension. Keep the direction only if every evaluation is zero.
Cap each stage at 4096 draws. Record every failure; never change the input
polynomial or condition the reported instance set on success.

Substitute x_i=a_i+sum_j t_ij v_ij into Hx=0. This is an EXACT binary
linear system in mk variables and rn equations, not a polynomial relaxation.
An arbitrary solution yields a native witness. All original ANF equations
and all extension-field syndromes are independently re-evaluated.

The generator stores the full packed ANF, not a truth table or hidden oracle.
Every squarefree monomial of degree zero through three has an independent
unbiased coefficient under ideal randomness. Reducing uniformly sampled
formal bounded-degree polynomials in the Boolean quotient gives this same
law. The recorded runs use reproducible pseudorandom seeds, not certified IID
trials. The field modulus and bit basis are saved.

## Conditional Rank Guarantee

This is our derivation, pending independent review. It is not a theorem
about how often local flat search succeeds.

Assume the m local direction spaces are independent uniform k-dimensional
subspaces of F_2^n. They need not be independent of their offsets. Put q=2^n
and

    p0 = (2^(n-k)-1)/(2^n-1).

A nonzero binary left-nullvector of the composed system is uniquely
represented, using the nondegenerate field trace pairing, by a nonzero
lambda in F_q^r. Its value at position i is the linear character with field
coefficient z_i=sum_j lambda_j gamma_i^j. A uniform local direction space
is annihilated by a nonzero character with probability p0; the zero
character always annihilates it.

For a subset S of s distinct positions, the number of nonzero lambda
vanishing there is q^(r-s)-1 if s<r, and zero otherwise. This follows from
the Vandermonde/MDS rank, not an assumption that the binary rows are IID.
Expanding the product of the local annihilation probabilities gives the
EXACT expected number of nonzero binary left-nullvectors:

    E = sum_(s=0)^(r-1) binom(m,s) p0^(m-s) (1-p0)^s (q^(r-s)-1).

Dropping the negative terms and extending the sum,

    Pr[rank deficient] <= E
        <= q^r (p0+(1-p0)/q)^m
         = 2^(rn-km).

Clip this upper bound at one. Full row rank implies consistency for EVERY
offset, so no independent-offset assumption is necessary.

Why does this apply conditionally to the proposed random local search?
Uniform cubic ANF is invariant under invertible affine changes of variables.
The capped extension algorithm is equivariant: such a change carries every
point, direction, acceptance decision, and failure event to its counterpart.
Conditional on success, the output flat is therefore uniform, by transitivity
of the affine group. Different blocks remain independent conditional on all
local searches succeeding, under ideal independent input/search randomness.
Early termination of individual rejected tests changes work, not decisions.

Do NOT apply this probability guarantee directly to a fixed seed, a
non-equivariant implementation, adversarial fixed polynomials, or a search
whose failures were removed. The seeded runs verify witnesses; they do not
measure a 2^-256 event.

## Native Results

Both cases were fixed before execution, at dual-code rate alpha=113/128.
This is strictly above 7/8. No quantum execution or finite quantum success
bound was evaluated.

| n | m | r | flat k | binary rows | flat variables | rank | result |
|---|---|---|---|---|---|---|---|
| 16 | 256 | 30 | 3 | 480 | 768 | 480 | all constraints satisfied |
| 32 | 1024 | 120 | 4 | 3840 | 4096 | 3840 | all constraints satisfied |

The initial n=32 run used 157211 random words and 304774 search evaluations,
with no failed local flat searches. The complete run, including input
construction, both linear systems, and independent native witness replay,
took about 22 seconds on this machine. Timing is diagnostic, not a
cross-implementation performance claim. The artifact retains full witnesses,
flat bases, work counts, the field modulus, and source/dependency hashes.

The conditional rank-failure bounds are 2^-288 and 2^-256 respectively.
Deleting the last direction of every n=32 flat leaves only 3072 parameters:
that exact restricted system has rank 3072 and is inconsistent. This is NOT
an unsatisfiability certificate for the original problem. At n=16 the
one-dimension-smaller control is still consistent, with 32 free parameters.

## Why This Is Not An Asymptotic Break

For a fixed affine k-flat, restriction of a uniform cubic is uniform among
degree-at-most-three ANFs on k variables. Thus its probability of being
identically zero is

    2^(-S(k)), S(k)=sum_(j=0)^min(3,k) binom(k,j).

There are exactly 2^(n-k) GaussianBinomial(n,k;2) affine k-flats. A first
moment bound therefore gives

    Pr[any zero k-flat]
       <= min(1, 2^(n-k) GaussianBinomial(n,k;2) / 2^S(k))
        < min(1, 2^(2+(k+1)(n-k)-S(k))).

The final inequality uses the elementary bound
GaussianBinomial(n,k;2)<4*2^(k(n-k)). Large positive exponents are VACUOUS,
not evidence of existence. The n=32,k=4 bound is vacuous. At fixed alpha,
surplus flat variables require k>=(1-alpha)n. That is linear in n, whereas
the negative cubic term eventually dominates the quadratic flat count.
For this run's rate, n=400,k=47 already gives a per-block existence upper
bound below 2^-300. Larger accepted flats would contain such a flat.

This obstructs a dimension-surplus strategy based on one local flat per
block at large n. It does NOT exclude lucky consistent restrictions,
adaptive searches over many flats, non-flat parameterizations, or another
classical solver. It is not a general computational lower bound.

## Research Decision

Do not use n<=32 instances of this distribution as classical-hardness
evidence without this attack. Do not count the previously known quantum
algorithm as a project discovery. The scientifically useful result is a
concrete native classical witness plus an explicit boundary on extrapolation.

Next mathematical test: cubic polarization. When a zero k-flat is extended
by v, its new two-direction derivative constraints are LINEAR in v. Solve
those first, then test the remaining quadratic/cubic constraints. This may
move the finite classical boundary substantially without altering the input
distribution. It still faces the zero-flat existence obstruction.

Run:

    python theorems/cubic_rs_affine_flats.py
    python -m pytest -q tests/test_cubic_rs_affine_flats.py

Files: `theorems/cubic_rs_affine_flats.py`,
`tests/test_cubic_rs_affine_flats.py`,
`research/classical_baselines/cubic_rs_affine_flats.json`.
No central candidate admission, qsearch/UI wiring, or legacy pipeline change.
