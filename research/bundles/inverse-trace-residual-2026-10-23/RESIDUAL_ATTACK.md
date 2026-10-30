# Exact Residual SAT Attack: An Implemented Attempt, Not A Dequantization

2026-10-23. Standalone while the source repository is migrating.
No source/staging edits, central candidate admission, or quantum execution.

## Scientific Question

Can an access-matched classical solver find witnesses for the prime-degree
affine inverse-trace residual left by the completed independent review?
This is a concrete missing algorithm, not another counting or mixing bound.

The input is F_(2^n) in a verified polynomial basis, distinct supplied
points alpha_i, K Vandermonde checks, target bits b_i, and syndrome h.
Find x with

    sum_i alpha_i^j*x_i = h_j,    j=0,...,K-1,
    Tr(inv0(x_i)) = b_i,          inv0(0)=0.

At native N=n^2, K=floor(N/8), the residual has m=K+ceil(4K/n) positions.
The prior review proves that a sampler/solver succeeding for almost all
uniform syndromes would be useful on the full native task. It does NOT
provide that solver, a hardness result, or a guarantee for one seeded input.

## Implemented Mechanism

The first K public columns form an invertible Vandermonde matrix. For the
Lagrange basis polynomials L_i at those pivot points, solve exactly

    x_i = sum_j coeff_j(L_i)*h_j + sum_(t>=K) L_i(alpha_t)*x_t.

This leaves s=m-K field variables, or n*s Boolean coordinates, before the
nonlinear predicates. No hidden witness enters this elimination. All
points remain the original supplied points, including zero when present.

Two COMPLETE encodings of each local predicate are tested:

1. Inverse graph: introduce y_i and impose
   ((x_i=0 and y_i=0) or x_i*y_i=1), together with Tr(y_i)=b_i.
   This retains every legal zero and rejects zero at target-one positions.
2. Conic: fix a public c with Tr(c)=1 and introduce u_i with
   u_i^2+x_i*u_i+c*b_i*x_i^2=1. ALSO impose x_i!=0 whenever b_i=1.
   For nonzero x, the Artin--Schreier criterion proves equivalence. For
   x=0 the unique auxiliary value is u=1 and is legal only if b_i=0.

The second formulation is from the repository's independent conic audit;
it is not a new theorem. Omitting its nonzero guards would accept x=0 for
every target, including all ones. Exact exhaustive controls retain that
falsifier. Auxiliary conic multiplicities also mean that random SAT models
would NOT automatically give uniform x samples.

Carryless multiplication and reduction are explicit bit-vector circuits;
squaring, constant multiplication and trace are binary linear maps. Z3 is
the existing solver, not a newly invented domain engine. Its optional ANF
and extended linear simplification modes are separately recorded.
[Official parameter reference](https://microsoft.github.io/z3guide/programming/Parameters/).

No field-size table is materialized. The encoding has polynomial size in
m,K,n, but solving it has NO proved polynomial runtime. The free-variable
surplus and abundance of witnesses are not a complexity argument.

## Clock, Provenance And Verification

The standalone runner distinguishes two input protocols:

- Uniform: h is drawn directly from the whole syndrome space; no accepted
  full vector or planted residual solution is used to generate h.
- Induced: fix U first, sample accepted coordinates on its complement,
  and compute h from that prefix. Sampling y from the prescribed trace
  hyperplane and applying inv0 is exact in the ideal-randomness model.
  The prefix is not a supplied full witness. A successful residual answer
  is joined to it and checked against the ORIGINAL N-coordinate relation.

The finite trials use Python's seeded PRNG, not a claim that experiments
certify ideal uniformity. Configuration, public points, targets, syndrome,
prefix, solver version, statistics, resource caps and source hashes are
recorded when the worker returns. A whole-worker timeout instead retains
the deterministic input-reconstruction configuration and explicit UNKNOWN.

The external subprocess wall cap covers startup, input construction,
encoding, SAT, and verification. Timed-out workers are terminated and reaped.
The separate Z3 resource limit can end a run earlier. Resource counts are
implementation-specific, not bit-operation complexity bounds.

SAT models are verified by extended-Euclidean inversion and ordinary
polynomial-basis arithmetic, independently of the symbolic formula.
UNSAT is labeled as reported by Z3; no independently checked proof
certificate is emitted. Exhaustive bounded fibers cross-check its meaning.
UNKNOWN is neither UNSAT nor evidence for classical hardness.

## Verified Outcomes

All five final receipts use seed2301, the same stated random-point protocol,
and record their own configuration and exact code hashes. Timings are single
local runs, not scaling estimates or an encoding-performance ranking.

| n | Syndrome | Encoding | Resource cap | Outcome | Wall seconds |
|---|---|---|---:|---|---:|
|7|Induced|Inverse graph|1,000,000|Verified full native witness|0.121|
|7|Induced|Conic with ANF|1,000,000|UNKNOWN, resource cap|0.193|
|17|Uniform|Inverse graph|5,000,000|UNKNOWN, resource cap|4.631|
|17|Uniform|Conic|5,000,000|UNKNOWN, resource cap|4.599|
|17|Induced|Conic with ANF|50,000,000|UNKNOWN, resource cap|8.860|

The degree17 instance has N289, K36, m45 and9 free field variables
(153 Boolean coordinates). No instance was resampled after failure. The
degree7 conic calibration does succeed in the unit test's larger cap;
that does not retroactively change the failed one-million-resource receipt.

30 local tests PASS in0.58s. Together with the previous normalizer/quotient
bundle,98 tests PASS in14.42s. Python syntax checks pass for all three new
Python files. Receipt input hashes, all source hashes, prime-degree field
presentations, native sizes, and exact exhaustion counters were checked.

The saved full witness was also verified using the earlier independent
review's polynomial arithmetic, without importing this attack's field or
verifier code. That resident checker was read-only, with SHA256
dc39bad41c682adaec8d03ab3dbb3aa09bb9f7b2bc132f1853f2eaa3767e5bc4.
This certifies one witness, NOT solver scaling or any claimed quantum result.
No full-repository tests or qsearch.py validation ran during migration.

## Decision And Handoff

The checked solver is now an actual attack interface. The degree-17
attempts to date have not produced a residual witness; do not promote
these limited failures into a surviving speedup claim. Degree-7 success
is only calibration, not a new asymptotic search result. Previous accepted-
flat controls already found FULL native witnesses at larger finite degrees;
those do not solve this high-check-rate residual interface or uniform sampling.

Do not spend main-model effort on an open-ended SAT budget campaign. The
next conceptual improvement would have to exploit coupled conic/Vandermonde
structure, give a constructive prime-degree accepted-family algorithm, or
identify a useful different native source. The unrelated PPAV conversion
paper 2026/1142 still returned403 for its full PDF; its unavailable theorem
was not imported. No new inverse-trace normality theorem was found or assumed.

Gemini may perform mechanical follow-up only after the authoritative
repository migration is verified: integrate the solver as an explicitly
experimental CLASSICAL baseline; preserve exact-zero and conic guards;
use fixed, recorded original points and both syndrome protocols; compare
an XOR-aware SAT backend without changing the relation. Keep search and
sampling statuses separate. Do not modify the closed independent review,
admit candidates, create synthetic oracle benchmarks, or infer a lower bound.

This bundle deliberately does not wire qsearch.py or the UI while copying
is in progress. Its three Python files are the attack, bounded runner and
tests. Receipts are local JSON outputs, not central registry records.

## Reproduction

From this directory, with /opt/anaconda3/bin/python and external cache:

    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q
    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python run_attack.py --bits 7 --mode induced --encoding inverse --seconds 10 --resource-limit 1000000
    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python run_attack.py --bits 7 --mode induced --encoding conic --algebraic --seconds 10 --resource-limit 1000000
    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python run_attack.py --bits 17 --mode uniform --encoding inverse --seconds 30 --resource-limit 5000000
    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python run_attack.py --bits 17 --mode uniform --encoding conic --seconds 30 --resource-limit 5000000
    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python run_attack.py --bits 17 --mode induced --encoding conic --algebraic --seconds 60 --resource-limit 50000000

No command is a quantum execution or an asymptotic performance certificate.
