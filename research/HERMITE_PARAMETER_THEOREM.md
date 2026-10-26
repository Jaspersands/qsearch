# Uniform Parameters For Pinned Hermite Streaming

2026-10-21. Written theorem proposal, with exact finite-parameter checks.
General correctness, implementation uniformity and novelty require independent
review. No native quantum execution, central claim admission or speedup claim.

## Result And Scope

The preceding notes establish a proposed fixed-accuracy construction. This
note supplies explicit sufficient conditions, and audits the dependence on
accuracy instead of hiding it in a constant.

**Proposed uniform upper bound.** Let m >= 2 be an integer. Let q be an odd
prime, n=q-1, and ell an integer satisfying

    ell >= 256*m^2,
    n >= 256*m^3*(ell+1).

For the explicit half-set Hermite-OPI stream, the proposed algorithm outputs
a polynomial with score at least `(1-1/m^2)*n`, with failure probability at
most `22*m^4/n < 0.01`. It uses one pass, absolute-constant workspace

    O(m^2*q*ell*log(q)*log(q*ell)),

and preprocessing, each update, and postprocessing time bounded by a fixed
polynomial in q, ell and m. This is a logical-circuit existence proposal,
not a compiled circuit or measured qubit count. Total time still includes
all `N=(q-1)*q^ell` input entries.

Since OPT <= n, the absolute score guarantee implies the stated
approximation ratio. This does not find the exact optimum. The domain does
not include ordinary OPI (`ell=1`) or every fixed multiplicity.

Dependencies are the local pinned-decoder, compact-decoder, independent
module-certificate and streaming-composition notes. They are not silently
upgraded from review-pending derivations to externally certified theorems.

## Input And Access

Use the half-rate code of length-ell Hasse jets over F_q at all nonzero
points, with degree bound `K=ell*n/2`. Each input row is a membership table
over F_q^ell with `(q^ell-1)/2` good addresses. All entries arrive once,
in arbitrary order. The algorithm has no table oracle, QRAM or second pass.
Random pins are input-independent. The decoder sees only the retained
augmented syndrome, not the true error or support.

The source and streaming model are inherited from
[Wu--Yang, Sections 4--5](https://arxiv.org/html/2610.01902v1).
The proposed improvement is the compact, small-characteristic decoder
substitution with its explicitly charged accuracy dependence, not the
existence of a streaming separation itself.

## 1. Explicit Schedule

Set

    alpha_m = 1 - 1/m^2,
    lambda = 1/2 - 1/(4m),
    tau = 1/2 - 1/(8m),
    s = 8m-2,
    d = floor(tau*n),
    h = ell-s.

The parameter conditions imply `0 <= s < ell < q`. Define

    M = n*h,
    c = (s+1)*(s+2)/2,
    A = max(0, floor((M-K-c)/(s+2)) + 1),
    D = A+K-1.

This is the same minimal interpolation budget used by the decoder.
Its number of unknown scalar coefficients is `(s+2)*A+K+c > M`.
The decoder must certify isolation throughout radius `d+2`, not merely d.

Let

    b = ceil(log2 n),
    t = s*ceil(K/q),
    r = 8*(t+b),
    L = b + ceil(log2 r),
    epsilon0 = 2^(-b).

Here r is the number of distinct random pin positions, L caps rejection
sampling attempts per position, and epsilon0 budgets each small failure.
The schedule is conservative, not optimized for constants.

## 2. Strict Guarded Root Inequality

First, the max in A is inactive. Indeed,

    M-K-c = n*(ell/2-s)-c,
    ell/2-s >= 128*m^2-8m+2 >= m^2,
    c = (8m-1)*8m/2 <= 32*m^2,
    n > 32.

From the definition of A,

    D <= (M-K-c)/(s+2)+K.

Dividing by n*h and using K=ell*n/2 gives

    D/(n*h)
      <= (s+3)/(2*(s+2))
         + s*(s+1)/(2*(s+2)*h) - c/((s+2)*n*h).

The gap between `1-tau` and the first term is

    gamma = (1/2-tau) - 1/(2*(s+2)) = 1/(16m).

The finite-multiplicity term is at most gamma/4. This is equivalent to

    h >= 4*(8m-2)*(8m-1),

which follows from

    h >= 256*m^2-8m+2
       > 256*m^2-96m+8.

Also `2/n <= gamma/4`, since n >= 128m. Consequently

    (1-tau-2/n) - D/(n*h) >= gamma/2 > 0,
    (n-d-2)*h > D.

This is the required strict root inequality including the two-block guard.
It also implies `D<M`, excluding a nonzero Q0-only interpolant. No finite
examples are used in this general argument.

## 3. Pin Budget And Failure

The small-characteristic differential-kernel bound is

    dim W <= t = s*ceil(K/q) <= 4m*(ell+1).

It is not the invalid large-characteristic bound `dim W <= s`.
The latter is already falsified by Frobenius directions in the earlier tests.

We need to pay the score loss r/n. For n >= 16,

    ceil(log2 n) <= 2*sqrt(n).

One proof uses `log2 n <= sqrt(n)` for n >= 16 and adds at most one.
Our conditions give `n >= 65536*m^5 >= 16384*m^4`, hence

    b <= n/(64*m^2),
    32*m^2*t <= 128*m^3*(ell+1) <= n/2,
    32*m^2*b <= n/2.

Therefore

    4*m^2*r = 32*m^2*(t+b) <= n,
    r/n <= 1/(4*m^2).

In particular r<n, so sampling distinct positions is legal.

For each fixed error, the affine solution space is chosen independently
of the pins. While its remaining dimension is nonzero, a newly exposed
pin reduces it with probability at least one half. The rank-exposure
argument in HERMITE_PINNED_DECODER.md gives

    eta <= Pr[Bin(r,1/2)<t].

Since t <= r/8, Hoeffding gives

    eta <= exp(-9r/32) <= exp(-r/8)
         <= exp(-b) <= 2^(-b).

This is a dimension-exposure argument, not enumeration over q^t messages.

For the product source, theta <= lambda and rejection above d satisfies

    Pr[weight>d] <= exp(-2*(tau-lambda)^2*n)
                 = exp(-n/(32*m^2))
                 <= exp(-b) <= epsilon0.

Thus rejected mass, averaged over public pins, is at most

    delta <= 2*epsilon0 <= 2/n.

The capped partial Fisher--Yates sampler from the composition note aborts
with probability at most `r*2^(-L) <= epsilon0`. Conditional on no abort,
the subset is exactly uniform. Abort is charged as failure; the stream is
not retried. Allocate at most epsilon0 additional total output-TV error
for all nonexact gates.

## 4. Uniform Mean And Unconditional Success

The ideal mean fraction before the finite-alphabet correction is

    beta = 1/2 + sqrt(lambda*(1-lambda))
         = 1/2 + (1/2)*sqrt(1-1/(4*m^2))
         >= 1 - 1/(8*m^2).

The inequality uses `sqrt(1-x) >= 1-x` for 0 <= x <= 1.
The finite-alphabet estimate must also be uniform in m. Write a=q^(-ell).
The exact source mean from the composition note is

    p_good = 1/2 - a*(1/2-lambda) - lambda*a^3
             + (1-a^2)*sqrt(lambda*(1-lambda+lambda*a^2)).

Its deficit from beta is at most

    a*(1/2-lambda) + lambda*a^3 + a^2*sqrt(lambda*(1-lambda))
      <= a/2 + a^2/2 <= a <= 1/q.

Here `0<=lambda<=1/2` and `0<=a<=1`; no constant deteriorates as m grows.
Combining this with `1/q <= 1/(8*m^2)` and the pin bound gives

    g = mu/n-alpha_m-r/n
      >= 7/(8*m^2)-1/q-r/n
      >= 1/(2*m^2).

The guarded-neighbor moment transfer is the critical quantum-composition
dependency. Using it on unnormalized accepted states gives the joint
accepted-bad probability

    (1/(2n)+2*delta)/g^2 <= 18*m^4/n.

Adding sampler abort, herald rejection and total synthesis-TV gives

    failure <= (4+18*m^4)/n <= 22*m^4/n
            <= 22/(65536*m) < 0.01.

There is no division by acceptance probability for any individual pin set.
This is an unconditional guarantee, including an abort fallback answer.

## 5. Uniform Resource Proof

The previous `O_s` and `poly_s` notation alone does NOT justify growing m.
The following audit removes that hidden dependency from the proposed
algorithm, using the actual loops in `hermite_compact_decoder.py`.

Let u=s+2=8m and D0=M+K=O(q*ell).

1. The polynomial-module basis contains at most `u^2*(D0+1)` field entries.
   Its local jet cache contains at most `u^2*ell`. There are at most M
   constraint updates, each consisting of bounded polynomial loops over
   those arrays. Rows are not enumerated as field assignments.
2. Weak-Popov cancellation decreases the integer potential
   `u*shifted_degree+leading_position` of one row. Shifted degrees stay
   between `-(K-1)` and M. Across u rows there are at most
   `O(u^2*(M+K))` cancellations. Each is a monomial row update with
   polynomial work, so the polynomial degree does not depend on u.
3. The fixed right inverse generates K cardinal polynomials one at a time.
   Their degrees are O(K), and all divisions, local series inversions and
   translations have polynomial loops. No K-by-K inverse is stored.
4. The descending solver has at most `z<=s*ceil(K/q)=O(m*ell)` provisional
   free coordinates. It recomputes coefficient vectors instead of retaining
   K-by-z directions. The batch is at most 2K field entries; its echelon
   system has `z*(z+1)=O(m^2*ell^2)` entries. All residual and pin constraints
   are imposed or rechecked; no early-rank assumption discards equations.
5. Since ell<q, all these arrays fit in `O(m^2*q*ell)` field entries.
   Integer loop indices need O(log(q*ell)) bits. Exact integer binomial
   intermediates have O(q*ell) bits and are transient, not retained as a
   dense coefficient table. Modular binomial generation is also possible.

Thus the deterministic decoder has absolute-constant bit workspace
`O(m^2*q*ell*log q)` and time bounded by a fixed polynomial in q,ell,m.
This is an algorithmic storage proof, not a claim about Python object
overheads or FLINT's peak process memory.

Given its retained input, use input-preserving
[Bennett reversible simulation](https://doi.org/10.1137/0218053) only on
postprocessing, not on the input-reading history. Because m<ell<q and
classical T is a fixed polynomial, `log T=O(log(q*ell))` with an absolute
constant. This gives the workspace stated above. The logarithmic overhead
is retained.

The stream updates are exact logical Boolean-controlled phase gates.
Uniform Fourier circuits and public rotations occur only polynomially
many times outside those updates; synthesize each to its share of the
total epsilon0 budget. Generate the gate description incrementally.
Neither a dense field-Fourier matrix nor the whole circuit description is
stored. The source, pin sampler, output and retained registers fit within
the same space bound. The computation on malformed encodings must be
totalized and padded to its public polynomial bound.

This does not include physical fault tolerance. Logical exactness does
not prevent hardware errors over a stream of length N.

## 6. Growing-Accuracy Corollary

Choose any fixed rational `0<a<4/7` and take, along primes q,

    ell = floor(q^a),
    m = floor(q^(a/4)).

Eventually both sufficient conditions hold: the ratio ell/m^2 grows as
q^(a/2), and q/(m^3*ell) grows as q^(1-7a/4). Integer floors do not alter
these positive powers. The proposed bounds become

    target = 1 - Theta(q^(-a/2)),
    failure = O(q^(a-1)),
    workspace = O(q^(1+3a/2)*log(q)^2),
    preprocessing / each update / postprocessing = poly(q).

Since log N=Theta(q^a*log q), these workspace and component-time bounds are
polylogarithmic in N. TOTAL time is not: every input entry is read.
The allowance of unsatisfied rows grows as Theta(q^(1-a/2)); approaching
one in relative score is not exact optimization.

For a fixed rational alpha<1 instead, choose
`m=max(2,ceil(sqrt(1/(1-alpha))))`. This recovers the fixed-target result
with explicit sufficiently large multiplicity. It still excludes ell=1.

## 7. Matched Classical Comparison

Use a FIXED classical target `alpha_c in (3/4,1)`. The external
[Wu--Yang Theorem 1.7](https://arxiv.org/html/2610.01902v1) gives

    p*S_classical >= q^(1+ell*kappa)/(ell*log2(q))^(C*ell),
    kappa = (4*alpha_c-3)/(4*alpha_c-2),

where C=C_alpha_c>0 is unknown. Do not substitute the growing alpha_m
and assume its C is uniform.

Instead fix

    0<a<=min(1/2, kappa/(4*C)).

This is within the upper bound's a<4/7 regime. For sufficiently large q,
`log_q(log2 q)<=a` and ell<=q^a, so

    log_q(ell*log2 q) <= 2a,
    p*S_classical >= q^(1+ell*kappa/2) >= N^(kappa/2).

The quantum target alpha_m eventually exceeds alpha_c. The external lower
bound uses random tables in a grouped stream order; the proposed quantum
algorithm handles all promised tables and orders, including that subset.
There is no mismatch from using a stronger quantum output guarantee.

The bound is external and not independently reproved here. The unknown C
prevents certifying a numerical separation at a selected a such as 1/4 or
1/2. The artifact's examples of those exponents are UPPER-BOUND examples
only. This is a streaming space/pass comparison, not unrestricted classical
time hardness, a practical speedup, or a Shor-level result.

## 8. Attempts To Break The Argument

- **Hidden growing-order cost:** leaving the old O_s notation unchanged
  would invalidate the corollary. Section 5 pays m^2 and a fixed-degree
  time polynomial. A loop exponential in s or a retained K-by-z direction
  table would require revising that section.
- **Nonuniform classical constants:** C may depend badly on approximation.
  A fixed alpha_c avoids this; no chosen finite example claims a separation.
- **Loss of guard or clean uncomputation:** either breaks the moment
  transfer, independently of the scalar inequalities. The native missing-
  guard second-moment and retained-garbage controls remain mandatory.
- **Wrong characteristic:** the free space can have dimension proportional
  to ell even at constant s. The actual small-characteristic bound is paid.
- **Source mean near one half:** its finite-alphabet correction is proved
  uniformly above; it is not imported with an unspecified m-dependent
  constant.
- **Finite success mistaken for proof:** the new executable allocates no
  code matrices, stream tables or quantum states. Passing its checks only
  verifies the arithmetic for those inputs, not the general proof.
- **Novelty collapse:** linear differential interpolation, noisy-word
  side-information pruning, polynomial-module reduction and reversible
  simulation are established methods. The combined upper bound may already
  follow from prior work. No exhaustive novelty claim is made.
- **Wrong research significance:** even a valid new improvement here is
  an explicit-table streaming result. It does not furnish a succinct
  evaluator, solve ordinary OPI, or imply unrestricted cryptanalytic
  advantage. Those are separate reduction problems.

## Executable Evidence And Next Decision

Run `python -m theorems.hermite_parameter_theorem`. The exact-rational
artifact is `research/reductions/hermite_parameter_theorem.json`.
Its large-prime examples are parameter certificates only. Out-of-region
controls are labeled insufficient conditions, not no-go results.

### Targeted Prior-Art Check

[Guruswami--Wang, Section 4.2](https://arxiv.org/pdf/1106.3951) already avoids
list enumeration using noiseless derivative side information under its
characteristic hypotheses.
[Kopparty--Ron-Zewi--Saraf--Wootters, Sections 4.2--4.6](https://arxiv.org/pdf/1805.01498)
goes further: differential solution spaces of degree greater than q are
closed under degree-bounded multiplication by X^q; their q-dimension is
bounded by the operator order. Theorem 4.8 and Claim 4.15 give random-jet
dimension contraction and pruning. Thus neither the existence of the
small-characteristic affine space nor pruning it is new here.

That theorem averages over ALL F_q, whereas our pins use F_q^* without
replacement. A future use must rederive the restricted-domain exposure
bound, check `K-1 <= (ell-s)*q`, and charge the changed pin budget. Do not
substitute a whole-field bound without those checks. The current arithmetic
certificate retains its elementary rank-exposure bound and does not depend
on this stronger result.

[Venkitesh, Section 1.2](https://arxiv.org/html/2412.01755v1) supplies
characteristic-insensitive divided-difference codes, but changes the
encoding. Replacing Hasse jets by that code is not automatically a
score-preserving reduction of the same streaming problem. No such reduction
has been supplied here.

These checks increase the risk that the remaining upper bound is a direct
application of established ideas. They do not certify either novelty or
redundancy of the complete compact quantum-streaming statement.

### Verification

13 new / 92 connected tests pass in 40.25 seconds with RuntimeWarning fatal.
Python syntax, site JavaScript syntax, site checks and registry validation
pass. The full repository suite was not run. The four previous Hermite
producers and their reports are unchanged, checked by SHA256.

The next high-value work is adversarial proof and prior-art review of the
complete statement, especially the guarded moment-transfer substitution
and the uniform computational model. More large-number parameter examples
would not address those questions. Keep every algorithm-claim gate false
until that review is resolved.
