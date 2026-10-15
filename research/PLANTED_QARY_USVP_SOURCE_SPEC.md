# Next Source Family: Planted Q-Ary Unique-SVP

The generator, public kernel basis, exact prime certificates, classical
attacks, tests and independent replay now live in PLANTED_QARY_USVP_SOURCE.md
and its producer. This specification is retained as derivation history, NOT
a novel reduction, hardness theorem or admitted quantum algorithm. It targets
the actual source gap: all current small cube-source calibrations are solved
by public LLL. Harder-looking unimodular disguises of diagonal lattices would
not fix this: HNF, modular rank-one recovery and elementary geometry can expose
the planted direction. Do not confuse random-looking bases with hard lattices.

## Public Problem And Private Calibration

Choose an odd prime q, dimension n, row count m<n-1, and a PRIVATE dense
primitive planted vector u in{-1,0,1}^n with a unit coordinate. Require support
at least n/3; sparse two-column relations are a low-ceiling calibration.
Sample each row of H in F_q^n independently and uniformly from u^perp by
choosing all but a unit coordinate and solving the remaining coordinate.
Accept only full row rank m, recording every attempted matrix and charging
the rejection process in generator metadata. The public lattice is

    Lambda={v in Z^n: H*v=0 modq}.

The solver receives H,q and an exact public integer basis only. The plant,
its PRNG seed, basis coefficients, and uniqueness calibration data are private
audit information. Reproducibility is not permission to hand a solver the
seed that regenerates its answer. No plant, seed or short-vector advice may
enter lattice source compilation, state sampling or classical attacks.

## Public Basis Without Short-Vector Advice

Find pivot columns P with invertible H_P and remaining columns F. Compute
C=H_P^(-1)*H_F modq. In original ambient column ordering take basis rows:

    q*e_(P_i), i=1..m;
    e_(F_j)-sum_i C_ij*e_(P_i), j=1..n-m.

Every row lies in the public modular kernel; absolute determinant is q^m.
Full rank H makes the kernel index q^m, so these n independent rows span
the FULL lattice, not merely a sublattice. Verify both membership and the
determinant/index identity. Then use public LLL/BKZ/basis attacks with their
costs and transformation certificates retained. Computing a basis uses no u.

## A Conditional Uniqueness Certificate, Not Assumed Hardness

Let R be an exact integer and require R<q/2. For any nonparallel integer v
with ||v||2<=R, its residue is NOT in span_Fq(u). Indeed, u's coordinates
are0 or+/-1. If v modq=alpha*u, centred lifting under |v_i|<q/2 gives
v_i=alpha_centered*u_i at every coordinate; hence v is an integer multiple
of u, contradicting nonparallelity. Odd q avoids midpoint ambiguity.

For a fixed such v, each original independently sampled row of u^perp has
H_row*v uniform in F_q. Thus Pr[H*v=0]=q^-m. There are at most
(2R+1)^n integer points in the containing coordinate box, so BEFORE rank
conditioning:

    Pr[exists nonparallel v with ||v||2<=R] <= (2R+1)^n/q^m.

The probability of full row rank in the (n-1)-dimensional orthogonal space is

    P_rank=product_(i=0..m-1) (1-q^(i-(n-1))).

The accepted full-rank distribution is not IID unconditioned rows. A valid
conditional failure upper bound is

    min(1, (2R+1)^n / (q^m * P_rank)).

If no nonparallel vector has norm<=R and R>=G*||u||2 with G>1, the lattice
is G-unique, u is shortest up to sign, and the statistical certificate's
failure event is explicit. Since u is primitive, there is no shorter
parallel lattice vector. Choose R=ceil(G*sqrt(support(u))) using exact
integer square comparisons, not floating-point exponent heuristics.

The bound is a distributional source guarantee. It does NOT certify a
specific large matrix as unique, prove average-case computational hardness,
or prove that a growing quantum receiver is efficient. Enumerate all vectors
only in bounded finite validation controls, including ALL nonparallel ones;
do not infer absence from a truncated heuristic search.

## First Parameter Sweep And Serious Attacks

For fixed f1 cube-source research, a polynomial unique gap of order n^3 is
relevant. A deliberately conservative initial family may take G=n^3,
m near n/2, and prime q at least n^12, additionally verifying q>2R.
This can make the uniqueness union bound small, but often makes small
instances VERY easy for LLL/BKZ. That is expected and must be recorded.
The promised gap must also meet the actual dyadic cube-width guard and
prime/residue guessing costs; do not transplant the improved BALL gap.

Classical attacks to implement before claiming any quantum signal:

- Public LLL/BKZ with exact output membership/norm and measured work.
- Modular nullspace low-alphabet search, meet-in-the-middle and bounded SIS.
- Public HNF/SNF and centred-lift reconstruction, including rank-one controls.
- Column-pair/small-support relations; these should kill sparse planted families.
- MILP/bounded integer lifting where feasible, with timeout reported UNKNOWN.
- Basis/coordinate leakage from generator construction and shared PRNG seeds.
- Polynomial-gap versus achieved root-Hermite-quality accounting, without
  turning heuristic quality into a theorem about all classical algorithms.

For n32..128, polynomial gaps can exceed practical LLL quality by orders
of magnitude. Repeated classical recovery is a negative for THAT generated
regime, not for unique-SVP or the full reduction. Larger dimensions may
survive implemented attacks but that is not a hardness certificate. Never
choose dimensions only to exceed a classical timeout and call it advantage.

## Proposed Implementation Boundaries

Check for concurrent files before adding unique namespaces:

    theorems/planted_qary_usvp_source.py
    research/PLANTED_QARY_USVP_SOURCE.md
    research/reductions/planted_qary_usvp_source.json
    research/hypotheses/planted_qary_usvp_source_contract.json
    research/certificates/planted_qary_usvp_source_crosscheck.js
    tests/test_planted_qary_usvp_source.py

Use exact finite-field APIs supporting primes beyond a machine word, exact
determinants, rank-conditioned probability ledgers and structured source
records. Large probability bounds should have replayable factored integers,
not underflow-to-zero floats or unbounded decimal JSON. The independent
checker must derive the kernel/index, full-rank probability and union bound,
not replay the producer's labels as assertions.

Keep generator/private audit, public problem, classical attacks, cube-source
outer guesses and actual quantum receiver as separate interfaces. Supply
correct residue/coordinate guesses only to marked calibration sweeps; a
real receiver pays the outer search. Returning a planted phase expression
is NOT lattice-to-DCP preparation. Reuse the compiled public source instead.

## How This Can Fail

The low-alphabet plant, large gap, large q, conditioning distribution or basis
construction may enable fast classical reconstruction. The uniqueness bound
may be vacuous at useful parameters; widening cubes may demand gaps that
make classical attacks even easier. Large n can exceed both classical and
quantum practical resources, leaving only an asymptotic question. Source
noise and receiver costs may still overwhelm any proposed quantum gain.

Falsify these possibilities first. This family is a better-controlled test
bed than disguised diagonal lattices, not evidence of a breakthrough.
