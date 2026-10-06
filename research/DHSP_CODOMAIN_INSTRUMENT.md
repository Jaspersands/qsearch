# Full-Oracle Codomain Instrument Audit

LOCAL DERIVATION / REVIEW PENDING. No independent mathematical review, novelty
claim, accepted candidate, efficient DHSP algorithm or general oracle lower
bound. The literal tables below are regression controls, not oracle candidates.

## Why This Input Model

Previous collective-decoding audits mainly start with supplied coset/phase
states. A full function oracle is a different resource. This pass audits a
codomain-only use of that resource rather than assuming every oracle algorithm
reduces to the already-screened projector processors.

[Moore-Young v1](https://arxiv.org/pdf/2202.09697v1), Definition4.2 and
Lemma4.3, constructs a domain/function/hash superposition and asserts a pure
hash state after discarding two registers. The
[withdrawal notice](https://arxiv.org/abs/2202.09697) identifies that lemma as
incorrect and essential to the algorithm. We test the actual channel and a
different, legitimate heralded repair; we do not rehabilitate that algorithm.

## Physical Repair And Complete Outputs

Let A have D elements and p_w=|{a:z(f(a))=w}|/D. Evaluation produces

    D^(-1/2) sum_a |a,f(a),z(f(a))>.

Tracing out domain and function gives diag(p), NOT |sqrt(p)><sqrt(p)|.
For uniform K-bin p, the distance from that claimed pure state is 1-1/K.
In particular the uniform-hash projection on the discarded state has probability
1/K independently of the image size. The claimed constant first-step separation
does not survive physical partial trace.

A legal repair computes f and z, applies the evaluation oracle's inverse to
erase f, then makes a BINARY projection of the domain onto its initial uniform
state. This costs TWO evaluations; U_f inverse is not an inverse-function
oracle. Discard the domain in both branches, but retain the tag and entire
quantum hash output. The normalized, trace-one instrument is

    sigma(p) = |H><H| tensor pp^T
             + |F><F| tensor (diag(p)-pp^T).

The accepted vector is p, not sqrt(p). Its probability h=sum p_w^2 can be
inverse polynomial for a compressed hash. This alone is not an algorithm:
unconditional H-and-uniform-hash probability is STILL exactly 1/K. The three
outcomes (failure, H-flat, H-perpendicular) have probabilities
(1-h,1/K,h-1/K). No conditional success is substituted for total success.

Two independent CLASSICAL uniform-domain samples reproduce the ENTIRE
computational tag/hash output: query f,z on both, mark equal hashes as H,
and return the FIRST hash. The probabilities are p_w^2 and p_w(1-p_w).
This is an exact two-query baseline, not a simulator for off-diagonal hash
coherence or arbitrary subsequent quantum computation.

All preparation/hash/uniform-domain circuit costs remain payable. Bounded table
construction is exponential calibration, not efficient oracle synthesis.

## Actual Dihedral Source

Use D_N with N=2^n and multiplication
(b,x)(c,y)=(b xor c,x+(-1)^b y). Hide the reflection (1,s) using

    f_s(b,x)=pi(x-b*s mod N),
    K_epsilon={(b,x):x mod2=epsilon*b}.

Pi is a FIXED unknown output permutation shared by every probe. Uniform
preparation on K_epsilon is easy. If epsilon=s mod2, its image is pi(even),
each label twice; otherwise it is the whole range, each label once. We charge
no chosen-label, inverse-permutation or image-membership oracle.

For a public balanced hash into K bins, fixed independently of pi, the wrong
subgroup gives u=(1/K,...,1/K); the correct subgroup gives the histogram p of
a uniformly random N/2-subset. Exact hypergeometric moments are

    E p = u,
    Cov(p) = (I-J/K)/(K*(N-1)),
    delta = E ||p-u||^2 = (K-1)/(K*(N-1)).

For ONE averaged complete instrument, the state difference has blocks
(Cov(p),-Cov(p)) and trace distance delta. H-perpendicular attains that distance.
This is a source mean, not a bound for every output permutation. The affine
permutation control has a large parity-hash signal; the bit-reversal control
has none. Both remain visible. Natural codomain structure may invalidate the
uniform-permutation assumption and must be independently modeled.

## Shared Nuisance: A Required Counterexample

Do NOT tensor independently averaged one-copy states: pi is not resampled.
For K=2 write p=(1/2+d,1/2-d), and rotate hashes to U=(0+1)/sqrt2,
V=(0-1)/sqrt2. The H block is [[1/2,d],[d,2d^2]], and the F block has
only its V entry, 1/2-2d^2. Exactly

    E d^2 = 1/(4*(N-1)),
    E d^4 = (3*N-8)/(16*N*(N-1)*(N-3)).

Take two probes of the same subgroup. A known projector onto the following
four orthogonal vectors requires no hidden-permutation advice:

    HH: (UU-VV)/sqrt2; HF: U,V; FH: V,U; FF: V,V.

Its probability difference from two wrong-subgroup probes has magnitude
5 E d^2 - 6 E d^4. At N=8 it is **11/70**, exceeding twice the averaged
one-copy distance, **1/7=10/70**. This EXACT rational witness falsifies the
tempting averaged-state hybrid, not the legitimate pointwise hybrid below.
It is not scalable algorithm evidence. Fresh-resampled pi is a separate
countercontrol, never silently substituted for the real source.

## A Correlation-Safe Scaling Screen

For each fixed pi and hash, rank-one trace-norm inequalities give

    D(sigma(p),sigma(u))
      <= (||p||+||u||+sqrt(K)/2)||p-u||
      <= (2+sqrt(K)/2)||p-u||.

For T fresh preparations, classically adaptive selection from a PREDECLARED
R-hash menu, and arbitrary quantum memory/postprocessing of retained tag/hash
systems, a channel hybrid is applied CONDITIONAL on pi. Only afterwards do
we average: E max_r ||p_r-u|| <= sqrt(R*delta). Hence

    final binary parity success <= 1/2
      + (1/2) min(1,T*(2+sqrt(K)/2)*sqrt(R*delta)).

Hash choices need not be independent of earlier records. The menu itself is
independent of pi. No posterior resampling argument is used. The thinner
three-outcome CLASSICAL transcript has the stronger bound T*R*delta on its
total variation, by conditional coupling and E max<=sum E.

For K near n, R=n and T=n^2, saved ideal quantum-distance dyadic bounds are:

| n | Distance Upper |
|---|---|
| 16 | 1 (vacuous) |
| 32 | 1/2 |
| 64 | 1/16384 |
| 128 | 1/8796093022208 |
| 256 | 1/20282409603651670423947251286016 |

The report saves exact squared bounds and conservative dyadic rounding, not
floating underflow. A separately CERTIFIED total composed trace-error budget
adds to the ideal distance; epsilon=1e-6 leaves that physical error floor.
We have no circuit-precision proof for these asymptotic ledgers.

## Coherent Hash Selection Is Not An Automatic Escape

Allow a known codomain-only unit vector v_y in a d-dimensional retained output,
including a freshly prepared coherent superposition of hashes. After erasing f,
the same binary domain projection gives

    sigma_S = H tensor mu_S mu_S^dagger
            + F tensor (rho_S-mu_S mu_S^dagger),
    mu_S=mean_{y in S} v_y, rho_S=mean_{y in S} v_y v_y^dagger.

For a random half subset and all-range reference (mu,rho), exact sampling
identities give

    E ||mu_S-mu||^2 = (1-||mu||^2)/(N-1),
    E ||rho_S-rho||_F^2 = (1-tr(rho^2))/(N-1).

Use D<=2||mu_S-mu||+sqrt(d)||rho_S-rho||_F/2, and the same conditional hybrid.
For R predeclared encoders of output dimension at most d, its ideal distance
is at most T*(2+sqrt(d)/2)*sqrt(R/(N-1)). Thus fresh coherent hash control
does not rescue POLYNOMIAL HILBERT-DIMENSION compression in this instrument.
All encoder ancillas must be counted in d; an ignored label register invalidates
the premise. Complex, nonorthogonal and coherent two-hash controls are retained.

Polynomial QUBITS do NOT imply polynomial DIMENSION. A full n-qubit label
register has dimension N and this bound can be vacuous. This distinction is
essential: THIS dimension-dependent argument does not screen every encoder.
The subsequent [sample-channel simulation](DHSP_CODOMAIN_SAMPLE_SIMULATION.md)
removes the dimension restriction for the same binary domain-erasure template,
including known codomain controls on incoming quantum memory. It is a
classical-query / quantum-processing simulation, NOT classical computation.

## Literature Gate: Do Not Overtransfer Index Erasure

[Lindzey-Rosmanis 2022, Theorem1](https://www.rintonpress.com/xxqic22/qic-22-78/0594-0626.pdf)
gives bounded-error noncoherent index-erasure query complexity Theta(sqrt(L))
for injective functions [L]->[M], provided M>=L^(3+epsilon) for fixed epsilon>0.

Embedding an arbitrary injection g as f(b,x)=g(x) hides the KNOWN reflection
H_0 and simulates each f evaluation with one g query. Generic pure-image
preparation from this full oracle would solve index erasure. This obstructs
that generic preparation primitive with the stated large-range promise. It
does NOT prove DHSP hard: this instance's subgroup is already known.

It also does NOT automatically transfer to surjective/permutation-only
codomains M=L, nor to structured natural evaluations, approximate compressed
histograms or arbitrary HSP algorithms. The report explicitly rejects using
the theorem's large-range premise at M=L. Unknown efficient recoding of the
codomain cannot be granted as a notational convenience.

The [2023 KU defense abstract](https://i2s-research.ku.edu/quantum-polynomial-time-reduction-dihedral-hidden-subgroup-problem)
describes a reduction to a Codomain Fiber Intersection Problem. We have only
read that abstract, NOT the dissertation or a complete CFIP definition/proof.
This pass neither validates nor refutes that conditional reduction.

## What Remains Open, And Next Falsifiers

- Retained domain registers, detailed failed-domain measurements, coherent
  subgroup choices, domain-dependent controls and other full-oracle algorithms
  remain outside. Full-dimensional codomain-only outputs in this same template
  are now covered by the linked follow-up, not by the earlier dimension bound.
  Natural structured codomain promises still require their own information gate.
- Specify CFIP's actual access/interface and extract a costed primitive, rather
  than treating its name or the withdrawal's state conclusion as a solver.
- For any new source, demonstrate its full joint distribution and retention
  policy. A changed promise can be legitimate, but requires a reduction from
  a consequential problem and a matched classical baseline.
- Kill an alleged compressed advantage first with collisions, chosen-query
  attacks, conditional source simulation and shared-nuisance collective tests.
- Independently review the pointwise channel norm, adaptive classical selector
  assumption, mean/max step and general encoder dimension accounting. A single
  permitted violation is a falsifier. These are local analytic derivations,
  not formally machine-proved theorems.

## Artifacts And Verification

`theorems/dhsp_codomain_instrument.py` produces
`research/classical_baselines/dhsp_codomain_instrument.json`. It checks 108
literal query/hash/query-inverse circuits, exact subset moments, four shared
two-copy laws, complex encoder covariance and native scaling/precision ledgers.

```
python -m pytest -q tests/test_dhsp_codomain_instrument.py
python theorems/dhsp_codomain_instrument.py
node research/certificates/dhsp_codomain_instrument_crosscheck.js
```

The independent Node checker verifies 3780 physical matrix entries, 3072 exact
two-copy entries, 168 complex encoder entries, exact covariance and ten scaling
ledgers. These are proof-supporting regression checks, not mathematical review.
Production CLI/registry/literature wiring and full-suite runs remain Gemini's
work; this pass performs no candidate acceptance, commit, push or UI change.
New tests:40 passed. Related focused regression:111 passed,3 writer/runner tests
deselected (production integration not performed). Python/JS syntax and strict
JSON checks pass. The pre-existing writer omissions have not been repaired here.
