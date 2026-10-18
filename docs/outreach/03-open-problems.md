# Draft: open problems post

Status: DRAFT, not posted. Venue: [forum, blog or mailing list]. Repository: [link].

---

## Four small open problems from a quantum-vs-classical audit

Our project proposes quantum mechanisms and attacks each one classically. Most attacks
close the case. The four below did not. Each is finite and concrete, comes with code
that regenerates its numbers, and might be settled by someone who knows the right tool.
Scores in problems 1 and 2 are total-variation distances between outcome laws. Success
probability is (1 + TV)/2.

### 1. Does LOCC reach the separable optimum for a sign-ambiguous two-packet test?

A dihedral-coset phase qubit is ρ(θ, γ) = (I + γ cos θ X + γ sin θ Y)/2, with θ = 2πhs/q
for header h, secret s and modulus q. Take two pure packets (γ = 1) with q = 64 and
headers 16 and 17. The test is secret 0, where both angles are 0, against secret ±1. The
sign is unknown, so the alternative hypothesis is the equal mixture of the angle pairs
(π/2, 17π/32) and (−π/2, −17π/32).

- Our product and one-way adaptive local searches find nothing above the X-basis score
  of 0.7745.
- The collective Helstrom score is 0.8305207. The PPT program's primal solution is, up
  to solver tolerance, a PPT and so (on two qubits) separable measurement, and it comes
  within 1e-7 of that score. This rests on solver precision, not on a certificate.

**Question:** what is the best LOCC score in [0.774504, 0.830521]? A two-way protocol,
or a proof that LOCC stays at the X-basis score, would settle it.

### 2. Close the local window on a three-packet mixed instance

Take three mixed packets ρ(θ_k, γ_k) with purities γ = 0.85, 0.8 and 0.75. The test is
all angles 0 against the known angles π/4, π/3 and 2π/3. The PPT bound certifies that no
local protocol exceeds 0.6895. The collective optimum is 0.6993, a
certified gap of 0.0098. The best one-way adaptive circuit we found reaches 0.68676.

**Question:** does some local protocol reach 0.6895, or is the true LOCC optimum below
the PPT bound? The window is 0.00271.

### 3. Low-rate explicit quadratic-character OPI

Take p = 2^61 − 1, N = 127 and K = 39, with mixed quadratic-character constraints and
public seeded shifts and orientations. The best classical witness we have is 109/127,
from local repair. Among the radii evaluated, a finite DQI certificate beats 109 only
at decoding radius 32, and only given an exact source and an exact unique decoder beyond
half the minimum distance. The norm-form
attack that solves the K = 77 instances needs dimension 70 or 65, depending on the seed.

**Question:** is there a classical algorithm that reaches 110 or more on these inputs, or
an argument that it cannot?

### 4. Adversarial signs for the polar Gibbs source

For polar codes at N = 32768 and rate 1/2, classical successive-cancellation shaping has
average error E_J TV ≤ 0.010221 over uniformly random clause signs. For one sign pattern
the error can be much worse. On a length-2 calibration the average is 2/5 and the worst
case is 18/25.

**Question:** is there an efficient classical sampler with a worst-case-sign guarantee
for this polar family? Or is there a sign pattern where a quantum receiver provably helps?

### Scope

All four problems are finite instances. None is a claim of quantum advantage or of
classical hardness. Most derivations are marked review pending in our notes. To
regenerate every number:

```bash
pip install -e packages/qsearch_classical
docs/papers/classical-competitors/reproduce.sh OUT
```

The circuit search behind problems 1 and 2 is `tools/circuit_search/dcp_readout.py`.
