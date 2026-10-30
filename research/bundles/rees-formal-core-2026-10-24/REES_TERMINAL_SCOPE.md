# Native Rees Terminal Measurement And Recovery

2026-10-25. This pass extends the existing conditional proof, not the
claimed algorithmic scope. It establishes no novelty, classical hardness,
practical implementation or Shor-level result. No additional independent
review was commissioned.

## Research Decision

The preceding decoder-margin pass weakened the case for useful HDQI
readout advantage. This pass reconsidered the unchanged inverse-trace
residual, modular norm equation, native noisy-source access, and Rees
frontiers before selecting more work. No constructive inverse-trace solver
or new natural Rees application emerged. Failed proposals are not results.

A targeted primary-literature check retained the Rees theorem as a
substantive proposal, not an established discovery:

- [Imran--Ivanyos](https://arxiv.org/pdf/2304.08376), especially the
  concluding questions, restrict their unconditional fixed-class result
  to bounded primes. Their general central-erasure reduction alone is
  not a growing-prime solver.
- [Ivanyos--Santha](https://arxiv.org/html/1503.09016v2), Theorem 5 and
  Proposition 7, give the polynomial-graph learner and the special
  abelian-by-cyclic reduction. A general BCH coset parametrization has
  basepoint-dependent coefficients; merely observing bounded degree does
  not construct the required translated-graph input. No complete reduction
  of the Rees problem to that learner was found or ruled out here.
- [Luks--Miyazaki](https://dmtcs.episciences.org/531/pdf) explicitly place
  set stabilizers for solvable permutation groups in classical polynomial
  time. Supplying an explicit string and a nilpotent permutation action
  is therefore not by itself a new hard application. Replacing that string
  by a succinct or quantum source changes the input contract and needs
  a separate charged construction.
- [Morales](https://arxiv.org/abs/2608.05321) remains relevant structured
  semidirect/quasi-Hamiltonian prior art. Earlier local scope comparisons
  are not repeated as a new result. This search was not exhaustive.

The selected unresolved obligation is the actual terminal receiver. The
previous checked native-copy acquisition and recursive channel stopped at
a mixed source on the grade-one quotient. A source identity is not yet an
output recovery theorem.

## What Lean Now Checks

`ReesTerminalRecovery.lean` defines the terminal measurement on an arbitrary
matrix rho, without a hidden subgroup argument:

    Readout(rho,l) = (1/|V|) sum_(x,y) psi(l(x)) rho[x,y] conjugate(psi(l(y))).

This is the diagonal of U rho U*, where U[l,x]=psi(l(x))/sqrt(|V|).
For a supplied faithful unitary additive character and the complete dual
space, the module proves the character sum, equal cardinalities of V and
its dual, column orthogonality, and preservation of total measurement mass.
It proves faithfulness and unitarity of the actual standard character of
Z/p. The intended field application takes p prime; the standard-character
lemmas themselves also hold for nonzero cyclic moduli. They do not make
Z/composite a field or extend the Lazard theorem to small characteristic.

For the additive mixed-coset source of a linear space H, the actual
measurement law is

    Pr[l] = |H|/|V| if l vanishes on H, and zero otherwise.

The proof derives this from the double sum, using a translation of the
address and character orthogonality on H. It does not assume the desired
Fourier distribution. Measurement completeness proves normalization. Thus
the supported outcomes are uniform on the annihilator.

The module then proves that the ACTUAL first Rees quotient has this
additive source. Its group operation becomes addition by the previously
checked quotient centrality and the supplied base polynomial group law.
Substituting the native acquisition and complete source tree gives the
native-to-terminal law. A separate theorem preserves every complete
unnormalized transcript weight. There is no conditioning on favorable
records or division by rare outcome probabilities.

Given sampled linear forms, define the returned space to be their common
kernel. The checked conclusions are:

1. Legal annihilator samples make this kernel contain H, not necessarily
   equal H.
2. The returned space equals H if and only if those samples span H's full
   annihilator, in finite dimension.
3. Through the actual grade-one map, membership in this recovered space is
   membership in ALL of the original hidden Lie subspace, including its
   derived directions. It is not just an abelianization.

The proof uses the public linear forms, not a supplied hidden basis. The
definition is a mathematical common kernel; a verified executable Gaussian
elimination algorithm is not extracted from Lean in this pass.

## Sampling Bound: Written Proof, Not A Lean Probability Theorem

Let q be the field order, r the annihilator dimension, and k the number of
fresh independent uniform terminal outcomes. For k>=r, the probability of
spanning is

    product_(j=0..r-1) (1 - q^(j-k)).

For k<r it is zero; for r=0 the empty product is one, even with no samples.
To prove the formula, place the samples in an r-by-k matrix. All q^(rk)
matrices are equally likely. Its rows are independent in the coordinate
space F_q^k in (q^k-1)(q^k-q)...(q^k-q^(r-1)) ways. Row rank equals
column rank. Division gives the formula.

A proper span is contained in a hyperplane. There are (q^r-1)/(q-1)
hyperplanes, and each contains all k independent samples with probability
q^(-k). Hence failure is at most

    min(1, ((q^r-1)/(q-1))*q^(-k)).

If n is a known ambient dimension, k=n+t suffices without knowing H or r.
Choose t so 1/((q-1)q^t)<=epsilon/3. The sampling schedule in
`terminal_controls.py` uses this conservative bound. The formulas are
proved here and independently counted on bounded finite domains; the
probability/counting argument itself is NOT Lean-formalized.

For ascending grade packet arities M_2,...,M_c, put P=product M_d. The
budget charges kP lifted leaves, ckP native copies, k*sum_(d=2..c)
product_(j=2..d-1) M_j conversions, and k final readouts. Identical subtrees
still consume distinct sources. All lifted preparations, conversions and
readouts receive full-channel error allowances epsilon/(3*N_instruments).
The classical SDE abort allowance is a separate epsilon/3. The usual
full-channel hybrid and first-failure union bound are written deductions,
not new Lean theorems. Raw source error must be included in the preparation
allowance or separately charged per original copy; it is never free.

Arity sufficiency remains a separate SDE obligation. The live class-three
budget uses the conservative published-theorem envelope already written
in REES_RESOURCE_AND_PRIOR_ART.md, with ranks 3 and 2. The larger example
uses q=65537, quadratic arity 1001^2 and cubic arity 1001: cubing is a
bijection because gcd(3,65536)=1. These are symbolic plans, not executions.
The latter still charges 3,012,018,012,003 native copies. Polynomial is not
synonymous with practical.

## Decisive Controls

All six subspaces of F_3^2 are tested against literal rational-cyclotomic
U rho U* calculations. The readout routine receives only density entries,
the field and coordinate size; H is confined to fixtures and comparisons.
These are channel/proof controls, not generated oracle-search candidates.

- Repeated legal samples can return a strictly larger common kernel.
- Four IID uniform samples from F_3^2 span with probability 2080/2187.
  Four identical copies of one uniform sample have the same marginals
  but spanning probability zero. This does not refute the fresh-tree
  construction; it refutes replacing its joint promise with marginals.
- Using the trivial character in place of a Fourier basis gives total
  outcome mass nine on the full-subspace fixture. Character completeness
  and unitarity cannot be silently dropped.
- Dephasing the full-subspace source before readout changes the distribution
  by total variation 8/9.
- Exact rank censuses include zero-dimensional, insufficient-sample and
  adequate-sample cases. Large enumerations are rejected, not run open-ended.

## Remaining Boundary And Stop Rule

The new proof has 20 theorems and three operational definitions. Its axiom
audit includes all 23 declarations, recompiles the preceding chain, and
requires the frozen native receipt to match exactly. No prior proof or
receipt is rewritten. Only standard foundational axioms are allowed.

Still unresolved here: the base BCH/Lazard theorem and subgroup
correspondence; constructing the full public cancellation plans from the
published SDE procedure; verified polynomial-time arithmetic, gate/QFT
compilation and approximation; outer black-box reductions; novelty and a
consequential natural application surviving classical comparison. The
group/source law is a real explicit premise, not an imported opaque axiom.

This closes the exact terminal-distribution and span-to-answer obligation.
It does not make the entire algorithm formally verified. The immediate
research priority is no longer another Fourier identity or a larger finite
HSP example. A specialist reduction/novelty audit, genuinely useful native
source, or substantive algorithmic improvement is more valuable than
further standard terminal formalization. Gemini may integrate this finished
certificate after checkout migration is verified.
