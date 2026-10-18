# Explicit Prime-Field Character OPI

2026-10-17. Local derivations REVIEW PENDING. No novelty, hardness or speedup
claim. Producer: `python theorems/prime_character_opi.py --write`.
Output: `classical_baselines/prime_character_opi.json`.

SUPERSEDING high-rate competitor: [quadratic-extension norm search](PRIME_CHARACTER_NORM_ATTACK.md)
now reaches perfect127/127 on BOTH saved N127,K77 mixed inputs, including
strict siblings, with unchanged shifts/orientations. It proves a local
inverse-polynomial first-trial population bound under IID shifts, NOT a
fixed-instance success theorem. An explicit strict input solved by Q13
falsifies uniform success of the first monic pencil; varying the square
leading coefficient repairs that instance. Existing scores/proposals below
remain the original producer's historical results, not the strongest current
high-rate baseline. K39 and general fixed-input/asymptotic solvability remain open.

## Scientific Question And Portfolio Choice

Can compact prime-field power-character predicates support a code-intersection
advantage after algebraic attacks, without hiding a random membership oracle?
This replaces more DCP barriers or polar mesh scans as the next constructive
test. The binary-extension accepted-flat attack does not automatically apply
to prime fields. That observation is NOT evidence of classical hardness.

The known quantum mechanism is dual-code list decoding plus Fourier readout.
[Sun-Wootters Theorem1.8](https://arxiv.org/html/2610.12357#S1.SS2) states
prime-field OPI guarantees approaching SCL_rho(R), with perfect search for
fixed R+rho>1. Below R=1-rho, SCL is
`(sqrt(rho*(1-R))+sqrt((1-rho)*R))^2`; above it SCL=1, not the declining branch
of that expression. These are asymptotic guarantees with fixed positive
margins, NOT finite scores for our24 instances. Their random-oracle separation
does not transfer to our explicit predicates. No compiled coherent decoder
or finite success/gate certificate is supplied here.

The large-field decoder dependency matters: the
[Dao-Kominers-Thaler abstract](https://eprint.iacr.org/2026/2056) states
poly(n,log p) decoding at fixed capacity gap in sufficiently large characteristic.
Only its abstract was audited here, not its full proof or Lean development.
The [Jeronimo algorithm](https://arxiv.org/html/2609.05870) has polynomial
dependence on the field size in its stated decoder; that alone is insufficient
when log p, rather than p, is charged. A constant-gap finite implementation
must include uniform decoder synthesis and index-erasure/list-padding costs.

## Explicit Input Model

Prime p, N<p distinct points a_i=i+1, RS dimension K, fixed r dividing p-1.
Public input: shifts t_i, orientations sigma_i, and a verified generator of
the r power cosets. Put beta_i=g^sigma_i. The problem is to maximize

    #{i : Q(a_i)-t_i belongs to beta_i*(Fp)^r}, deg(Q)<K.

The original mode INCLUDES ZERO; density is exactly `(1+(p-1)/r)/p`.
The new strict mode EXCLUDES ZERO; its exact density is `(p-1)/(r*p)`.
The specification records an explicit Boolean convention and checks it on
round-trip. Strict lists lose zero-residual witnesses, but the constructive
extension below handles common cosets with just one degree of slack.
The shifts are public, not a secret hidden shift. The usual Legendre hidden-
shift algorithm is therefore not itself a solution to this intersection task.
Membership uses modular exponentiation, polynomial in log p; no full list,
acceptance table, hidden advice or oracle is supplied. Reversible arithmetic
could implement this public predicate, but is not already compiled here.

`global` inputs have one common coset; `mixed` inputs have independent seeded
orientations. Paired runs keep identical shifts/generator. No source is
discarded for a poor score. Seeded replay is not an IID confidence theorem.
The reference caps r<=8 and N<=4096 remain, not hardness boundaries. The
arbitrary127-bit prime cap was removed for the explicit Morse field regime;
public primes are still checked by FLINT. No field-sized list is introduced.

## Constructive Classical Power Completion

For M selected common-coset positions, let T interpolate their shifts and
V=product(X-a_i). Set D=ceil(M/r), choose nonzero lambda and define

    W=lambda^r * X^(rD-M)*V,
    F=W-T/beta.

F has degree rD and leading coefficient lambda^r. In the formal series at
infinity, compute the polynomial part R of F^(1/r), of degree D. Then
`deg(R^r-F)<(r-1)D`. The code uses normalized reversed series, doubling Newton
precision and exact FLINT congruence/degree checks, not numerical roots.

    Q=T+beta*(R^r-W)=beta*(R^r-F)

has degree<(r-1)D and, at every selected point,
`Q(a_i)-t_i=beta*R(a_i)^r`. Thus ALL common-coset inputs are solved perfectly
whenever `K >= (r-1)*ceil(N/r)`. This is a uniform constructive classical
explanation, not an inference from successful finite examples. At M<=K,
ordinary interpolation also works for arbitrary orientations because zero
residual is accepted. All final witnesses use independent Python modular
Horner evaluation, not just the formal-root implementation.

For lower rates one can force roughly rK/(r-1) common-coset constraints.
Under independent shifts at unseen coordinates the one-trial expected score
fraction approaches rho+R below the perfect threshold, with rho=1/r. It does
NOT match the published double-semicircle target throughout that region.
This expectation is neither worst-case, adaptive-attack nor best-of-restarts.
Do not call this an all-rate OPI dequantization.

## Strict Nonzero Powers: Constructive Zero Avoidance

New2026-10-17. Excluding zero is NOT an asymptotic rescue for the common-coset
perfect-search window. Reuse the formal root R and let
`b=(r-1)*ceil(M/r)`. The original Q has degree<b. Choose a PUBLIC constant c
outside `{-R(a_i) : i selected}`. There are at most M forbidden values, so
one of0,...,M works because M<p. This needs M root evaluations, an O(M)-size
forbidden set and at most M+1 membership probes, not a field-size search
when p is much larger than M. Reconstruct

    Q_new=T+beta*((R+c)^r-W).

At each selected coordinate the residual is `beta*(R(a_i)+c)^r`, nonzero and
in the desired power coset. Meanwhile

    Q_new-Q=beta*sum_{j=1}^r binom(r,j)*R^(r-j)*c^j

has degree<=b. Hence K>=b+1 is a uniform sufficient condition for perfect
STRICT common-coset completion. For every fixed rate R>1-1/r this additive
one-coefficient cost eventually vanishes as a rate penalty. This closes a
specific attempted escape, NOT all-rate or mixed-coset hardness. The local
derivation remains review pending and no novelty is claimed.

The formal Newton congruence applies to the BASE root, not R+c. Both roots,
the shift and every avoidance cost are stored separately; the final native
polynomial uses independent Horner checks. For M<=K, direct interpolation
uses `Q(a_i)=t_i+beta_i`, not the invalid strict zero-residual shortcut.
The general jet/conic attack is explicitly disabled on strict inputs: at
zero offset and an opposite coset there may be NO valid nonzero local root.

Tight degree deserves a separate statement. At p5,N4,K2,r2, shifts(0,0,0,1),
all25 native polynomials fail perfect strict satisfaction. At K3 the new
construction succeeds. This finite exhaustive counterexample prevents
silently dropping the extra degree or calling an algorithmic non-applicability
result an unsatisfiability proof on other instances.

Live artifact retains TEN additional strict controls: six seeded large-field
siblings, all perfect, and four exact-power root-zero traps at r2/3/4/8.
The traps deliberately make the BASE root vanish and require nonzero shifts
2,1,2,3, respectively. They are adversarial proof calibrations, not putative
hard benchmarks. Six hundred twenty-five complete small shift vectors also
check the strict guarantee. No source is rerolled for a favorable root.

## Mixed-Coset Quadratic Jet Attack

Varying cosets prevents the one-common-lift identity, but that is not hardness.
For r=2 choose M<=2K positions from the largest coset, degree
`D=max(ceil(M/2),floor(K/2))`, and construct R0 as above. Protect
`h=max(0,2D-K+1)` high coefficients. The remaining
`f=D-h+1` coefficients may vary through a polynomial L of degree<f:

    R=R0+L,
    Q=T+beta*(R^2-W).

When h>0, `deg(2R0*L+L^2)<K`; when h=0, `2D<K` directly. All original M
acceptance constraints survive. At up to f outside points choose root values
z, then interpolate L to those values minus R0. Their local predicate is
`a+beta*z^2 in beta_i*(Fp)^2`, where a is explicitly known.

For a=0 take z=0. For a!=0, the elementary quadratic character sum is
`sum_z chi((a+beta*z^2)/beta_i)=-chi(beta/beta_i)`. Including Z zeros, the
accepted count is `(p-chi(beta/beta_i)+Z)/2 >= (p-1)/2`. Uniform proposals
therefore succeed with probability>=1/3; no field scan or discrete log is
required. A cap failure is UNKNOWN, never source rejection or unsatisfiability.
The conservative union bound `min(1,f*(2/3)^budget)` refers to truly uniform
independent proposals, not the seeded PRNG's statistical confidence.

The artifact retains every paid trial, root coefficients, perturbation,
forced coordinates, proposals, caps and final polynomial. It charges native
Horner/membership evaluations and interpolation divisions. These counters
are not a complete bit-operation budget and cannot be compared with an
unimplemented quantum circuit's nominal size.

## Live Controls And What They Do Not Show

Twenty-four sources: six (p,N,K,r) configurations, seeds29/71, both modes.
Each r=2 source pays eight completion and eight jet trials plus one linear
baseline; higher r sources pay eight completion trials plus the baseline.
All344 native trial/baseline witnesses are retained, not just best successes.

At p=2^61-1, N127,K39, current global scores are108/110 and initial mixed
scores102/102. At N127,K77, global inputs are perfect and initial mixed
scores are118/118. The adaptive pass below improves the mixed witnesses.
Earlier fixed-leading jet trials scored120/118; releasing an extra leading
coefficient changes the seeded proposals and need not monotonically improve
best-of-eight. This is not an optimized benchmark or hardness indication.
At N31,K16 mixed scores improve31/29 to31/30; global inputs are perfect. Common-coset
r=3,N63,K46 and r=4,N32,K24 controls are also perfect.

Missing a perfect mixed witness on one finite input does not imply classical
hardness. Finding a perfect one does not dequantize an asymptotic family.
Neither best classical score nor a theoretical quantum mean is a matched
runtime/tail comparison. No positive candidate or active negative is admitted.

## Adaptive Root-Value Exchange Is Now Executed

The next falsifier proposed below is IMPLEMENTED, not a future wiring task.
For extra forced coordinates E, let b_e be their Lagrange basis, equal1 at e
and0 at the other coordinates. Changing R to R+delta*b_e preserves all other
root values, all common-coset constraints, and the degree budget because
`deg(b_e)=|E|-1<f`. Test the released predicate, score the WHOLE native word,
and retain only strict improvements. This is a constructive code-aware attack,
not independently rerolling candidate polynomials or source instances.

The default run repairs the best of the already-paid eight jet trials, with
eight paid proposals per coordinate. It stops at perfection, one full pass
without a sampled improvement, or a declared pass cap. Strict improvements
bound the default number of passes by N-initial_score+1. An incomplete random
pool never proves a coordinate-wise or global optimum; cap termination is
UNKNOWN. Degenerate a=0 opposite-coset coordinates can accept only the zero
root, so no uniform1/3 proposal guarantee is claimed for adaptive exchanges.

Live24-source artifact:16 repair stages,1934 retained proposals,11 accepted
moves and116319 charged native Horner point evaluations during repair.
For N127,K39 mixed inputs,102/102 improves to109/109. For N127,K77,118/118
improves to124/122. All four stop with NO_SAMPLED_IMPROVEMENT, not certified
local optima. Every rejected proposal, released-predicate outcome, feasible
score, accepted polynomial and final witness is saved. Independent tests
replay each proposal through interpolation and native integer Horner.

This weakens the proposed mixed-coset escape, not the published quantum
algorithm: a finite near-perfect classical word does not disprove asymptotic
perfect quantum search. More proposal counts or seed scans are not the next
scientific question. A structural classical bound/solver or an actual quantum
decoder with finite resources would change the comparison.

## Diagonal Reduction And Affine-Point Guard

Dual GRS weights v_i=1/V'(a_i) give parity checks H[j,i]=v_i*a_i^j for
j=0,...,N-K-1. Perfect OPI is equivalent to the INHOMOGENEOUS system

    sum_i H[j,i]*beta_i*z_i^r = -sum_i H[j,i]*t_i.

For strict lists the equations additionally require EVERY z_i nonzero; zero
affine roots are explicitly rejected, not converted into false native witnesses.
The exporter is not a solver. Homogenizing the right side with w^r and invoking
existence of a nonzero homogeneous solution does not ensure w!=0. The verifier
rejects the zero vector and nonzero points at infinity before normalizing a
true affine witness. [Ivanyos-Santha](https://arxiv.org/abs/1503.09016) provides
algorithms in a larger polynomial-variable regime; its existence/algorithm
conditions are not automatically met by this linear-ratio inhomogeneous task.

## Failure Audit And Next Decisive Work

- Common-coset high-rate perfect search is constructively classical both with
  zero included and, at one extra degree, with zero excluded. Do not keep
  varying seed, field size, power index or this zero convention as an escape.
- Mixed cosets may also be classically easy. The jet attack already exploits
  free coefficients overlooked by a straight formal-root test.
- Low-rate common-coset and mixed targets still lack matched quantum tails
  and stronger adaptive classical bounds. Failure of the current attack is
  only missing evidence, not a promising signal.
- The adaptive root-value falsifier is now implemented above. Its success
  does not prove a polynomial-time perfect mixed solver; its sampled stopping
  rule proves no lower bound against other attacks.
- A solver using simultaneous diagonal forms, algebraic elimination or
  rational approximants must return native affine witnesses and charge all
  setup/search. A homogeneous infinity point does not remove this blocker.
- A quantum proposal must provide the actual coherent capacity decoder and
  readout/resource analysis, or a different mechanism bypassing that dependency.

Tests exhaust1593 zero-including common-coset shift vectors at three small
thresholds,625 strict common vectors,625 mixed vectors for the free-jet degree
argument, all small diagonal roots including strict nonzero side conditions,
projective countercontrols, nontrivial cosets, Newton-vs-independent-square-root
series, search caps, adaptive monotonicity/full proposal replay, every saved
witness and deterministic artifact replay.
Passing these checks does not certify novelty or the asymptotic paper proof.
