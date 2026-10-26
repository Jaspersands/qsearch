# A Single-Polynomial Collaborative Decoder

2026-10-20. Constructive application and proof REVIEW PENDING. Known DQI and
collaborative Reed-Solomon decoding ingredients, not a claimed new quantum
paradigm, novelty result, or classical separation.

Producer: `theorems/paired_residual_decoder.py`.
Artifact: `research/phase_workbench/paired_residual_decoder.json`.

## Decision And Input Contract

Generic adjacent-pair errors do not automatically admit a fast structured
locator: the relation between two shifted locator factors is nonlinear.
Instead of granting that missing algorithm, choose evaluation pairs with
an exact algebraic decomposition: a,-a for a=1,...,M, M<=(p-1)/2.

This CHANGES the explicit optimization task. For public nonzero b_i and
explicit scalar halfsets F_i of size(p-1)/2, return ONE polynomial deg(P)<n
maximizing

    C_i(P) = 1[P(-a_i) + b_i P(a_i)^2 in F_i].

Take even n=2K<=2M. These are disjoint pair tests, not the old natural-order
chain with2051 constraints. The frozen author chain's0.60666 classical score
does NOT apply. Explicit tables cost O(Mp) bits before arithmetic/lookup costs;
they are not free random membership oracles over an exponential alphabet.

Proposed mechanism: prepare the usual score-polynomial source on independent
pairs, Fourier transform, split ONE polynomial syndrome into its even and
odd coordinates, collaboratively decode, herald a certified safe sector,
erase the original label reversibly, and apply ONE inverse QFT over F_p^n.
Unlike `PRIME_CHARACTER_INTERLEAVED_PROBE.md`, there are no extra output
polynomials or discarded which-support packets.

Expected upside: a concrete fixed-input high-score algorithm with a modest
known algebraic decoder, replacing a missing capacity decoder. A substantial
classical advantage is entirely OPEN. This is a research candidate formulation,
not admission of a speedup. It is relevant only if its explicit optimization
task survives stronger classical attacks or acquires a meaningful reduction.

## Prior Art And Novelty Boundary

- [Shang and Stilck Franca](https://arxiv.org/abs/2609.35101), Section5, supplies
  the nonlinear pair source, relative-decoding framework and exact
  4D+2<=n score-transfer guarantee. Its published chain is not our paired
  benchmark. We reuse the source/filter construction, not claim it as new.
- [Schmidt, Sidorenko and Bossert](https://arxiv.org/abs/cs/0610074) and
  [Yu and Loeliger](https://arxiv.org/abs/1612.07854) develop collaborative
  multi-sequence RS reconstruction. We reuse the repository's already tested
  whole-cap Prony implementation; no new classical decoder is asserted.
- [Chailloux and Tillich](https://arxiv.org/abs/2411.12553) already use soft
  decoding in quantum sampling/optimization. Our small fixed-input source
  calculation is not a claim to originate that broad idea.
- [Kramer et al.](https://arxiv.org/abs/2610.02145) covers folded DQI and
  stronger coherent-fiber constructions on random oracle instances. Its
  oracle lower bounds do NOT transfer to these scalar explicit tables.

The specific fixed-predicate rank law and guarded-observable application
below still need independent mathematical and novelty review.

## The Exact Source Law

For one pair, put r=y+b x^2, rho=(p-1)/(2p), and
h(r)=(1[r in F]-rho)/sqrt(rho(1-rho)). With normalized character coefficients,

    fhat(u,v) = hhat(v) / p * sum_x exp(2 pi i (v b x^2-u x)/p).

The coefficient vanishes for v=0. For v!=0 the quadratic Gauss sum has
magnitude sqrt(p), so

    |fhat(u,v)|^2 = |hhat(v)|^2 / p.

Thus v has the ACTUAL fixed table's Fourier distribution and u is uniform
and independent of v. This needs neither random tables nor uniform v.
Because a selected pair's Fourier label is never the zero vector, different
edge subsets have disjoint Fourier supports. For the radial source

    g = sum_(k<=D) c_k / sqrt(binom(M,k)) * sum_(|S|=k) product_(i in S) f_i,

normalized by sum|c_k|^2, the exact basis law is: choose k with its radial
weight, S uniformly, and the independent local laws above. Phases are retained.
This is not a mixture approximation to an overlapping chain pilot.

The known residual-coordinate/Dicke preparation applies to these disjoint
pairs. Classical preprocessing, uniform halfset/complement preparation,
prime-field QFT precision and all lookups must be paid.

## One Syndrome, Two Rows

For physical Fourier values u_i at+a_i and v_i at-a_i, let z_i=a_i^2 and

    A_i=u_i+v_i, B_i=a_i(u_i-v_i).
    s_(2j)   = sum_i A_i z_i^j,
    s_(2j+1) = sum_i B_i z_i^j,  0<=j<K.

The two length-K rows are just a permutation of the n public syndrome
coordinates already computed from the original label. There is no second
input state, copied support, additional quantum evidence or extra output row.
Both rows have the same pair support, though one row's value may be zero.
Recover u=(A+B/a)/2 and v=(A-B/a)/2 afterwards.

The implementation pads these rows with zeros at nonsquare nodes and reuses
`prime_character_interleaved_probe.decode_burst`, which scans all nonzero
field nodes. On a verified answer, it checks that recovered nodes belong to
the public pair set, unfolds the label and replays the original syndrome.
It certifies against ALL two-row errors on at most C blocks, including
neighbors with v=0; restricting uniqueness to the pilot's v!=0 law would
not suffice for score transfer.

That verifier computes the rank d of the CAP-C recurrence matrix, solves a
degree-d locator, finds all its roots and replays every syndrome. Its
whole-cap uniqueness proof is already in `PRIME_CHARACTER_INTERLEAVED_PROBE.md`.
Rank-good labels are decoded uniquely even against a rank-bad competing
representation. A syndrome-only decoder success, followed by an equality
check with the input label, gives an implementable herald, not a hidden
unique-decoding oracle.

## Fixed-Input Rank-Failure Bound

Let the actual support have size j<=D, choose C>=D, and put
m=2(K-C)=n-2C. Assume m>=D. After a public row permutation, the cap matrix
has the same rank as the m-by-j matrix with columns

    u_i V_m(a_i) + v_i V_m(-a_i),
    V_m(a)=(1,a,...,a^(m-1))^T.

Fix support and ANY nonzero v_i. The remaining u_i are independent uniform.
If a nonzero nullvector w has support T of size t, then

    sum_(i in T) w_i u_i V_m(a_i)
       = -sum_(i in T) w_i v_i V_m(-a_i).

The positive-node matrix has rank t since t<=m. All2t positive/negative
nodes are distinct. Therefore the space of negative coefficients compatible
with the positive span has dimension max(0,2t-m). Multiplication by fixed
nonzero v_i is invertible. Up to scalar, there are at most
(p^(2t-m)-1)/(p-1) compatible nonzero w; none if2t<=m.
For a fixed full-support w, the u_T solution is unique, so its probability
is p^-t. Union-bound over support and projective nullvectors:

    Pr[rank failure] <=
       sum_(t=floor(m/2)+1)^j binom(j,t)
           (p^(2t-m)-1)/((p-1) p^t)
       <= epsilon_D,

where epsilon_D replaces j by D. This covers every source shell, every
support and every fixed right-frequency vector, hence the actual coherent
pilot probability. It does NOT invoke independent uniform A/B row values.

A coarser bound is

    epsilon_D <= p^(D-m)/(p-1) * (1+1/p)^D.

The nonzero-v condition is essential. The exact p11 two-pair control has
10/121 failures for both tested nonzero-v vectors, below the12/121 bound.
Setting both v=0 violates the premise and exceeds that bound. Such outcomes
are impossible in the centered nonlinear source, not silently discarded
possible source outcomes.

## Guard The Observable, Not An Unproved Target State

Use C=D+1, not just D. Let G consist of accepted source labels of pair
weight<=D. Every e in G is unique against the ENTIRE pair ball of radius C.
The map U:|e> -> |V^T e> is then an isometry on G.

Multiplication by one score term has Fourier shifts z supported on one
pair. If e,e' in G and V^T(e+z)=V^T e', then e+z has pair weight<=D+1=C.
Uniqueness of e' forces e+z=e'. Consequently, for the normalized total score
T/M,

    U^* (T_target/M) U = Pi_G (T_source/M) Pi_G

on this accepted subspace. This is an exact compressed-observable identity,
not a claim that the entire unheralded target polynomial filter has source
normalization or the full binomial score law.

If b is the rejected source probability, the normalized accepted source
has pure-state trace distance sqrt(b) from the original normalized guide.
Since0<=T/M<=1 and b<=epsilon_D,

    E[score fraction | herald] >= mu_source-sqrt(epsilon_D),
    E[score fraction, ABSTAIN scored0] >=
        (1-epsilon_D)*max(0,mu_source-sqrt(epsilon_D)).

The decoder/flag/work registers can be reversibly computed and uncomputed
on the accepted branch. Failed branches ABSTAIN and keep their cost; there
is no uncharged repeat-until-success. Any separately established compilation
TV error eta subtracts at most eta from the one-attempt mean.

This resolves the readout issue without bounding the norm of a coherently
summed bad fiber. Full unheralded target-filter preparation remains unclaimed.
To transfer higher score moments this way, enlarge C to D+r and recompute
the rank budget; the first-moment certificate does not license r=2.

## Executed Evidence

At p2053,M1026,n204,D67,C68, exact rational arithmetic gives:

- Rank-failure upper bound2.452468945789447e-7.
- Source mean lower bound0.7327220055090983.
- One-attempt mean lower bound0.7322266018475371, including ABSTAIN.
- Probability of at least719/1026 passing tests greater than0.10800, using
  only the bounded score and the mean, not a guessed target binomial tail.
- Ordinary arbitrary-pair exact-transfer degree50 gives source mean about
  0.700204 on THIS same paired problem, not the published chain.

Numerical eigensolving only proposes rational radial weights. Existing
integer square-root enclosures certify their Rayleigh quotient and the
rejection penalty; eigenvector optimality is not assumed.

At fixed R=n/(2M) with0<R<3/4, choose D approximately n/3 but leave
n-3D>=3. The failure bound is O(p^-2), and the usual source-shell limit gives
the attainable envelope1/2+sqrt((2R/3)(1-2R/3)). The old arbitrary-pair
guarantee uses D approximately n/4 and envelope1/2+sqrt((R/2)(1-R/2)).
These are quantum score envelopes on the new paired problem, not a time
separation or claim about the full overlapping chain.

One fixed-seed basis control uses67 pairs and Fourier values from the
derived fixed tables. The two-row decoder recovers the complete original
label from syndromes only; the ordinary scalar decoder does not. The
u=v control deliberately removes one row and remains ABSTAIN. This is not
a coherent execution or empirical estimate of the tiny failure bound.

The independent bounded sparse pure-state control uses p11,M5,n8,D2 and a
nonradial two-term source. Unguarded target normalization is exactly1 within
roundoff, but its mean differs from the source by1.101928e-5. With C3 guarding,
the compressed source/target means agree within1.67e-16. All rejected mass
10/121 is retained. Numerical controls test formulas; they are not a proof
by finite enumeration or target advantage evidence.

## Classical Challenge And Why This Might Not Matter

The large control derives a NEW instance from Zhong-Xia Shang and Daniel
Stilck Franca's [frozen RDQINumerics data](https://github.com/dsfranca/RDQINumerics/tree/v1.0.0):
take the first1026 saved halfsets/multipliers but test them on the pairs
P(i+1),P(-(i+1)), with n204. Parent hashes and CC-BY-4.0 attribution remain.
Original chain witness scores must never be reused for this changed task.

An ACTUAL feasible information-set comparator forces102 pairs, interpolates
204 values, verifies the polynomial on all1026 predicates, and scores536.
This is one weak baseline, not evidence of advantage. The known ensemble
mean of such information-set sampling is rho+(1-rho)*102/1026; it is not a
bound on a fixed input or on stronger search.

The strongest immediate competitors are code-aware search on

    P(X)=E(X^2)+X O(X^2), deg E,deg O<K,
    r_i=E(z_i)-a_i O(z_i)+b_i(E(z_i)+a_i O(z_i))^2,

including information-coordinate/block search, annealing, soft reconstruction,
algebraic list recovery and structure-preserving reductions. This two-polynomial
form may make the task easier than the overlapping chain. No strong matched
portfolio has been run, no hardness reduction is known, and there is no
fault-tolerant gate budget. A decoder improvement is not a Shor-level result.

Falsifiers and revisions:

- A classical polynomial method reaching the same feasible-score envelope
  defeats the advantage motivation, even if our quantum bound is correct.
- Failure of the actual fixed-predicate Fourier law or full-cap uniqueness
  would invalidate the rank/readout proof. Both have explicit counterchecks.
- Importing scalar-uniform error laws, copying extra source rows or scoring
  only one marginal reintroduces the old objective-changing mistake.
- Dropping the observable margin preserves norm but can change mean; the
  unguarded sparse control demonstrates that failure rather than hiding it.
- Membership-oracle lower bounds do not become public-table hardness.
- Prior folded/soft-decoding work may subsume this application; publication
  or novelty claims require a more thorough comparison and external review.

## Next High-Reasoning Work

First independently review the guarded-observable and projective-rank proofs.
Then challenge the two-polynomial classical formulation above. Gemini can
adapt existing feasible classical kernels to this new explicit task with
full budget/witness accounting; do not call the536 control a strong baseline.

A more ambitious possible extension is m-th-root orbits instead of pairs.
Group a,zeta*a,...,zeta^(m-1)*a and test a nondegenerate quadratic sum in the
first m-1 values plus the last value against a scalar halfset. Conditional
on its nonzero last Fourier frequency, the first m-1 frequencies are uniform.
The one original syndrome decomposes into m collaborative rows. This suggests
D approximately n/(m+1), versus n/(2m) for generic Hamming decoding, with
an observable margin. It is a PROPOSAL, not implemented or proved here.
Its fixed-frequency rank law, source preparation, one-polynomial readout and
classical norm/algebraic attacks all need checking. Do not merely generate
an m-sweep and label it a stronger algorithm.

## Reproduction

```sh
python theorems/paired_residual_decoder.py --reference /path/to/RDQINumerics/data/reference --write
python -m pytest -q tests/test_paired_residual_decoder.py -W error::RuntimeWarning
```

The existing Prony reference is limited to word primes and at most4096 public
nodes. This is an implementation bound, not a theorem on admissible field
sizes. No central candidate admission, CLI/UI expansion or GPT commit is
part of this pass.

Verification:22 new/226 connected tests PASS6.59s with RuntimeWarning fatal;
Python compilation, registry validation valid:true/issues[], check_site and
dependency hashes PASS. This was not the full repository test suite.
