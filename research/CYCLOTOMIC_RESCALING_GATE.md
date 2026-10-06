# Cyclotomic Rescaling: Legal Gaussian Levels, Not A Polynomial Sieve

LOCAL DERIVATION / REVIEW PENDING. No novelty, full decoder, candidate admission,
Shor-level speedup, generic no-go or standard LWE attack is claimed.

## Source And Target

Primary source: [Boucher, Fouque and Shen, arXiv2609.34996v1](https://arxiv.org/html/2609.34996v1).
Sections3.1-3.3 specify the ramified trace pairing and IID phase samples;
Section4.2 gives difference-register combining and conditional output uniformity.
CCP uses integer-embedded secrets, while Definition9 also defines general ring
secrets. The paper's sample budget does not directly yield a standard LWE attack.

We audit the existing CCP/PSP sample model, not a new oracle promise. Write
R_L=Z[zeta_p]/(pi^L), pi=zeta_p-1, and

```text
B_L(x,y) = Tr(x*y/(p*pi^(L-1))) mod1
lambda_j = (zeta_p^j-1)/pi
psi_y(s) = p^(-1/2) sum_j exp(2*pi*i*B_L(lambda_j*s,y)) |j>
```

The following is our local deduction from this model. It is not attributed as
a new theorem of the source paper or established as unpublished research.

## Exact Public Rescaling

Let a be nonzero modp, b=a^-1, and sigma_b(zeta_p)=zeta_p^b.
For INTEGER-EMBEDDED s, physically permute old j to a^-1*j. Then

```text
lambda_(a*j) = lambda_a * sigma_a(lambda_j)
sigma_b(lambda_a) = pi/sigma_b(pi)
T_(a,L)(y) = (pi/sigma_b(pi))^L * sigma_b(y)
B_L(lambda_(a*j)*s,y) = B_L(lambda_j*s,T_(a,L)(y))
```

Proof: apply sigma_b to the field-trace argument; it fixes s. Moving its
denominator back to pi^(L-1) contributes L-1 unit factors, and transformed
lambda_a contributes one more. Therefore

```text
T_(a,L)(y) modpi = a^L * (y modpi), NOT a*(y modpi).
T_(a,L)(pi*z) = pi*T_(a,L-1)(z).
```

This is a known, secret-independent label operation plus a public basis
permutation. No unknown phase-state preparation, inverse, cloning or phase
oracle is invoked. General ring secrets are not fixed by sigma_b: a concrete
countercontrol fails the same-secret identity there.

The available low-label coefficients form the L-th-power subgroup of F_p*;
its size is (p-1)/gcd(L,p-1). All nonzero Gaussian coefficients are available
exactly when gcd(L,p-1)=1. At L divisible by p-1, all are one. This classifies
this operation, not every possible quantum encoding or joint instrument.

## Ternary Physical Compiler

For p3, T_(2,L)(y)=(-zeta_3)^L*bar(y). Odd L admits both weights1/2; even L
does not. On n+1 labels, find a nonzero dependence of their low residues by
FLINT RREF. Select its support, solve a_i^L=c_i, apply the index permutations,
then apply known SUM gates and measure all difference registers.

For x_1=0 and every measured difference tuple, the surviving qudit has

```text
Y = sum_i zeta_3^x_i * T_(a_i,L)(y_i)
child_label = Y/pi
global_phase = chi_s(sum_i lambda_x_i*T_(a_i,L)(y_i))
outcome_probability = 3^(1-r), r=selected inputs
```

All branches are retained and the global phase is checked, not silently
removed before comparison. One output consumes r<=n+1 selected qudits. Unused
inputs are reported. The arithmetic uses the actual ramified ideal quotient:
R_3 has characteristic9, not characteristic3 like a field with27 elements.

Output uniformity: condition on all low residues. The RREF choice and a_i are
now fixed; each label is a fixed lift plus pi times independent uniform z_i.
After division, each selected high part undergoes the invertible map
zeta_3^x_i*T_(a_i,L-1). Conditioning on differences and all but one selected
high vector leaves the output uniform. Disjoint input batches therefore give
IID children. Reading higher digits to select merges is OUTSIDE this proof.

Even-level falsifier: y1=y2=1 at L2 has formal weights(2,1), but T_(2,2)(1)
plus1 has residue2, not0. Thus these operations cannot implement that weighted
level drop. All SIX qutrit basis permutations are affine j->a*j+b; their
transport T_(a,L)(zeta^b*y) has the same a^L residue. None bypasses the gate at
even levels. This does not rule out arbitrary single-qudit unitaries, special
label subsets, non-native outputs, multiple copies or collective instruments.

RREF chooses the first free column. Failure of that particular kernel choice
at an even level is NOT a proof that no admissible dependence exists there.
An all-ones dependence is correctly accepted by the same physical compiler.

## Throughput Critique

Starting at L2t and stopping at L1, there are t even stages and t-1 odd stages.
A conservative one-output-per-batch consumption ledger is

```text
(n+1)^(t-1) * S(n,3)^t
```

Final decoding, confidence amplification and secret-digit recursion are extra.
This is not an optimal sample lower bound. For q=3^t=poly(n) with growing
t=Theta(log n), the Gaussian stages ALONE retain exp(Theta(log^2 n)) batch
consumption. Even a constant-cost even-stage primitive would not make THIS
construction polynomial. Fixed t is a different asymptotic regime.

Research priority must therefore be **many useful outputs per batch or a
non-sieve receiver**, not further one-output Gaussian benchmarking. A primitive
yielding a constant fraction of useful outputs per level could change the
sample ledger to polynomial when the number of levels is logarithmic. This
is a conditional research target, not an implemented method.

## Verification And Falsifiers

- 35 focused tests;86 related tests across carry packets, source law,
 throughput and state-isomorphism transfer pass. No full production green claim.
- Exact rational identities for all bounded ternary labels/integer secrets;
 independent field matrices check p3/5/7 through L6. These finite checks support
 the algebraic derivation, not its asymptotic complexity or a theorem review.
- Eight unfiltered native controls at L3/L5; independent JS replays96 complex
 amplitudes and32 complete quantum branches,243 conditioned source pairs,
 six ideal/trace charts,48 power-subgroup classifications and six permutations.
- Perfect-pairing Fourier unitarity, nilpotent arithmetic, quotient compatibility,
 noninteger-secret failure, every outcome's uniform source posterior, and
 first-kernel-selection limits are explicitly tested.

Falsifiers: any exact integer-secret phase mismatch, nonuniform child after
conditioning a fixed difference outcome, accidental higher-digit selection,
unaccounted inverse access, or a residue outside the asserted power subgroup
invalidates the stated primitive/proof. A better collective receiver would
invalidate any attempted universal interpretation, which we do not claim.

## Next Deep Task

Analyze a source-legal multi-output compiler or direct receiver. It must retain
the entire secret, keep correlations between surviving registers, prove the
source law and count total consumed samples. Do not call retained qudits IID
PSP outputs merely because their number is large. Prove throughput adequate
across a growing number of levels, or falsify that architecture and move on.

Gemini handles routine CLI/registry wiring and full production workflows.
Preserve the positive odd-level result AND both throughput blockers. No
candidate may be promoted from this local primitive alone.

```sh
python theorems/cyclotomic_rescaling_gate.py
python -m pytest -q tests/test_cyclotomic_rescaling_gate.py
node research/certificates/cyclotomic_rescaling_crosscheck.js
```
