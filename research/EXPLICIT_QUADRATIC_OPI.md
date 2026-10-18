# Explicit Quadratic-Target OPI Versus Structural Classical Attacks

2026-10-16. Explicit inputs, known DQI filter score, classical attacks and a
local rank-probability derivation REVIEW PENDING. No new quantum algorithm,
accepted candidate, oracle separation or general classical-hardness claim.

## Portfolio Decision And Question

The preceding cyclic BPQM construction failed a monotone-unrolling test, and
even ideal spectral sharpening did not fix its native subspaces. Rather than
keep refining it, this pass compared independent constructive mechanisms.

- The rank-metric DQI paper [2606.04843](https://arxiv.org/html/2606.04843v1)
  already disclaims an advantage and explains its covering-radius/proxy gap.
  Repeating its nearest-codeword setup is not a new candidate mechanism.
- [2609.40321](https://arxiv.org/html/2609.40321v1) already gives polynomial
  quantum F3 subset sum at each fixed positive quadratic density. A projection
  shortcut still needs enough independent Boolean-liftable output vectors;
  overlapping subsets or a hidden decoder do not supply that step.
- HHL on algebraic/Macaulay systems is not automatically exponentially faster:
  [2111.00405](https://arxiv.org/abs/2111.00405) gives conditioning limitations
  for the specified Boolean approach. Finite-field elimination cannot simply
  be reinterpreted as a complex linear system.
- Folded/list-decoded OPI is also prior art, including the recent oracle result
  [2610.02145](https://arxiv.org/html/2610.02145v2). Its random membership
  oracles and classical query lower bound must not be silently instantiated
  by compact public circuits.

Chosen question: can a compact, genuinely explicit balanced OPI target family
retain a useful quantum-quality gap after structure-aware classical attacks?
This tests a specific family, not more oracle demonstrations or decoder APIs.

## Actual Input And Known Quantum Mechanism

Let t>=3 be odd, q=2^t, N=q-1, and C the scalar Reed-Solomon code evaluating
degree<K polynomials at all nonzero field points. The input at each position
i is a public invertible binary matrix T_i and offset b_i. In binary
polynomial-basis coordinates z=T_i y, accept y exactly when

    h_i(y)=z_0+sum_(j=1)^((t-1)/2) z_(2j-1) z_(2j)+b_i=0.

The target is EXACTLY balanced: for each assignment to z_1,...,z_(t-1) there
is one acceptable z_0. Its quadratic polar rank is t-1. This excludes weak
constant-rank examples while giving O(t^2) public description bits and an
efficient reversible membership circuit. No random-membership oracle or
exponential target table is supplied. Finite-field arithmetic uses FLINT,
with its actual irreducible polynomial recorded for replay.

The proposed quantum route is the KNOWN conventional balanced-DQI algorithm:
prepare the error-weight layers, coherently decode the generalized-RS dual,
erase the error label, and Fourier-read the polynomial. The dual distance is
K+1. For the exact EXPECTED score law, impose the strict condition

    2 ell+1 < K+1,

not merely a unique-decoding inequality with an off-by-one. Choose ell at
most floor((K-1)/2). The known score matrix has off-diagonal entries
sqrt((j+1)(N-j)). A rational filter w has expected score

    1/2 + sum_j w_j w_(j+1) sqrt((j+1)(N-j)) / (N sum_j w_j^2).

The implementation encloses that Rayleigh quotient using integer square-root
bounds. Numerical eigenvectors only SELECT rational coefficients; they do not
certify optimality. A complete small-message enumeration independently checks
normalization and the mean using the ideal Krawtchouk filter law.

This is a theorem-based reference, NOT an executed coherent decoder or quantum
circuit, and not a discovery of DQI. A polynomial reversible membership circuit
can compute T_i y, apply the hyperbolic-pair predicate and reverse its scratch;
all code/field/filter/decoder costs still need a real implementation ledger.
The known quantum target is a quality gap at polynomial cost, not an asserted
runtime separation or numerical breakthrough probability for this family.

This is ordinary OPI with structured target predicates. It does NOT rely on
the invalidated state-preparation step in the separate max-QUADSAT proposal
[2510.08061v2](https://arxiv.org/html/2510.08061v2), whose author explicitly
reports the error. No theorem or novelty claim is inherited from that work.

## Classical Attack: Interpolate Accepted Affine Flats

Fix the r=(t-1)/2 odd hyperbolic coordinates to arbitrary bits a_j. The
remaining acceptance equation becomes linear:

    z_(2j-1)=a_j,
    z_0+sum_(j:a_j=1) z_(2j)=b_i.

Thus each predicate contains affine accepted flats of codimension c=r+1,
and their union over a covers its entire accepted set. Composing these
constraints with RS evaluation gives binary LINEAR equations on Kt message
bits. This uses partial accepted values, not ordinary interpolation of K
complete field symbols. It can force about Kt/c, nearly2K, positions.

The implemented attack considers a fixed public prefix, tries its local flats
with every linear solve charged, retains inconsistent/bad-rank instances, and
samples a solution to the accumulated consistent system. Independent FLINT
Horner evaluation verifies its polynomial and all forced positions. The
unqueried suffix still has independent random offsets in the mathematical
source model, yielding an expected baseline near1/2+R*t/(t+1), R=K/N.
That is NOT a fixed-instance guarantee or an oracle lower bound.

Sixteen paid restarts retain ALL attempts and choose by full-instance score.
This selection reads the explicit input and charges every solve and scoring
operation; it is not free postselection. A separate direct quadratic Z3-SAT
baseline tries to satisfy every target, with resource/time caps. Every SAT
After those restarts a structural repair attack releases one selected flat,
keeps the other flats through an exact RREF solve, and enumerates the small
remaining affine neighborhood. It retains the released predicate's NONLINEAR
acceptance, not its old flat, and chooses a strict full-score improvement.
The algorithm rebuilds the flats from the new word after each move. A full
pass with no improvement certifies only this local neighborhood fixed point.
Dimension caps are UNKNOWN; they do not certify local or global optimality.
Default pass budget is N-initial_score+1, enough for a no-improvement pass or
a perfect witness because each improving pass raises an integer score. Every
solve, enumerated word and predicate evaluation is charged. Final witnesses
are checked by independent native-field evaluation. This is not a convergence
or global polynomial-success theorem.

The direct Z3 baseline is separate. Every SAT witness is checked against native
field arithmetic. UNKNOWN does not imply
hardness; an UNSAT claim contradicting a verified perfect witness is an error.

## A Scoped High-Rate Perfect-Solution Bound

For independent uniform T_i in GL(t,2), the c-dimensional rowspace specifying
one fixed local flat is a uniform c-dimensional subspace. A fixed nonzero
binary linear functional lies in it with probability

    p=(2^c-1)/(2^t-1).

A dependence among the binary flat equations corresponds, through the
nondegenerate field trace pairing, to a nonzero word of the generalized-RS
dual supported on the constrained positions. For w>K fixed positions, the
shortened dual has dimension w-K over F_q. Hence it has at most q^(w-K)-1
nonzero words with exactly that support; for w<=K it has none. Union bound:

    Pr(flat rows fail full row rank)
      <= sum_(w=K+1)^m binom(m,w) (q^(w-K)-1) p^w
      <= q^(-K) (1+q p)^m.

Full row rank solves EVERY right-hand side, not only random offsets. For all
m=N positions and fixed rate R>1/2, t->infinity through odd values gives
c/t->1/2, so this upper bound tends to zero exponentially in Nt. Gaussian
elimination then finds PERFECT solutions to this specific quadratic family
in polynomial time with high probability under the stated IID GL source.
It is not a theorem about arbitrary OPI predicates or lower rates.

`fixed_flat_attack` executes the exact all-zero-flat linear system used in this
argument. Inconsistent flat systems are NOT declared unsatisfiable OPI inputs.
The predeclared N127,K90,seed29 control has508 independent rows in630 message
bits and a verified perfect native solution from ONE Gaussian elimination.
The seed is retained, not selected after a successful solve.

`flat_rank_failure_bound` evaluates the finite union bound as an exact rational,
with no floating underflow. Example t=7,K=90 gives an upper bound below2^-100.
An independent complete small check enumerates all7^3 choices of 2D subspaces
at three F8 RS positions: true rank-failure probability175/343, bounded by
27/49. This calibrates the implementation, not the entire asymptotic proof.
Seeded generator replays are explicitly NOT IID probability certificates.
The derivation is local/review pending and its novelty has not been verified.

## Live Controls And Their Limits

Run `python theorems/explicit_quadratic_opi.py --write`.
Artifact: `classical_baselines/explicit_quadratic_opi.json`.
All eight original inputs plus the predeclared high-rate control are retained,
with explicit predicate descriptions, every restart, solver outcomes and
independently checked witnesses.

| N,K | Seed | One flat | Best of16 | After repair | Known filter mean |
| --- | --- | --- | --- | --- | --- |
| 7,3 | 29 | 5/7 | 7/7 | 7/7 | 0.688982 |
| 7,3 | 71 | 6/7 | 7/7 | 7/7 | 0.688982 |
| 31,9 | 29 | 25/31 | 28/31 | 28/31 | 0.747358 |
| 31,9 | 71 | 23/31 | 26/31 | 28/31 | 0.747358 |
| 31,19 | 29 | 31/31 | 31/31 | 31/31 | 0.889110 |
| 31,19 | 71 | 31/31 | 31/31 | 31/31 | 0.889110 |
| 127,39 | 29 | 91/127 | 104/127 | 109/127 | 0.816830 |
| 127,39 | 71 | 95/127 | 102/127 | 109/127 | 0.816830 |

The initially mixed127-position comparison disappears after repair: both
controls reach109/127=0.858268, above the chosen quantum expected reference.
Repair adds136 linear neighborhood solves and4608/4384 enumerated candidates
AFTER the16 restart attacks. Maximum free dimension is6, no cap was hit, and
both end at a checked uncapped local fixed point. This is still NOT an
asymptotic dequantization or a fair full runtime/tail comparison: a quantum
sampler could also repeat. A stronger claim requires matched tail probabilities,
repetitions, costs and more than finite inputs. No real quantum run occurred.

Z3 found perfect7-position witnesses but hit its configured resource limits
on the larger inputs, INCLUDING31-position cases already solved perfectly by
linear algebra. This is a direct control against converting solver timeouts
into evidence of quantum advantage or generic classical difficulty.

## Revised Research Direction

The high-rate quadratic family has a constructive classical explanation, not
a remaining quantum-advantage candidate. The proposed lower-rate repair is now
implemented and removes the finite mean-score signal in both127-position
controls. Do not repeat the repair as a missing task, or extend blind size,
seed or restart scans on the strength of the earlier weaker baseline.

A later compact target family without large accepted affine flats may have
higher upside, but higher algebraic degree alone is no hardness argument.
For example the dense symmetric Boolean cubic e3 satisfies e3=e1*e2 in the
Boolean quotient, so fixing parity e1=0 annihilates it. A predicate z0+e3+b
therefore has an accepted codimension2 flat, WORSE than this quadratic family.
The identity is checked independently over all small inputs. Do not propose
that naive cubic mutation as a way around the demonstrated classical attack.
Keep conventional RS decoding, strict distance conditions and compact circuit
access explicit. Do not transfer any random-oracle classical bound: here even
all Nq membership values can be read in polynomially many queries. The open
question is computational complexity of these EXPLICIT inputs.

Gemini may wire this standalone producer into CLI/EXP and replay witnesses.
SMT statuses/timeouts need not be reproducible across versions/machines;
exact field basis, generator, deterministic attack, filter and stored native
witness checks are the reproducible parts. No commit/push or central candidate/
negative admission is made by this main-model research pass.
