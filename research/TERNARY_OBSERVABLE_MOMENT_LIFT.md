# Full Native Moment Consistency Still Needs Observable Circuits

LOCAL DERIVATION / REVIEW PENDING. Exact higher-rank counterexamples and a
costed all-rank repair for a specific diagnostic. No noisy decoder, native
likelihood tightness, random-source hardness or quantum speedup is claimed.

## An Actual Full-Translation Counterexample

The previous character synchronization circuit correctly constrains rank-one
solutions and excludes impossible perfect observed phase fits at every rank.
That does NOT establish that its higher-rank matrices represent mixtures of
secrets. Adding ALL actual equal-frequency-difference constraints is still
insufficient on the retained original native inputs.

Use the existing roots9/27 original sources, not invented oracle access.
Let native nodes have frequencies a_i,c_i. Impose g_(a_i)=g_(c_i) for every
record. Saturate equivalence classes under every selected circuit stencil AND
every full translation equality: if one entry joins the same class, the other
entry must also join the same class. At the fixed point define

    M_uv=1[class(u)=class(v)].

This is exactly the Gram matrix of orthogonal class unit vectors, so it is
PSD with diagonal1, of rank equal to the class count. Each stencil compares
two zeros or two ones. Audit ALL N^2 differences; a cap stops the experiment
rather than granting a partial certificate. No eigenvalue tolerance, numerical
solver or unknown secret enters this construction.

In all three preregistered native controls, the differences d_i=a_i-c_i
contain a unit basis of Z_(3^r)^n, all native pair moments equal1, and every
native anchor M_(a_i,0),M_(c_i,0) equals0. If a positive distribution over
true characters represented M, expectation chi_q(d_i.s)=1 would force each
of its support secrets to satisfy d_i.s=0. The unit basis forces s=0.
That distribution would give every native anchor1, contradicting0. Thus
the matrix has NO such representing distribution despite complete sparse
Bochner consistency. A basis inverse is retained as an exact certificate;
rank-deficient differences remain UNKNOWN.

The original source rows are random native ring labels already retained in
the existing synchronization report. Outcomes and planted calibration secrets
do not choose the equivalence classes or the new circuit. Source-independent
falsification of this representation is not proof of native average-case
inference failure. External physical IID supply is not certified here.

## Rational Separating Score Without Secret Enumeration

For m original records define the weighted native-harmonic diagnostic

    F(M)=sum_i Re M_(a_i,c_i)
         -w*sum_j Re M_(native_j,0),
    0<w<=1/(m*q^2).

The partition PSD point gives F=m. Secret0 gives m-2m*w. Any nonzero secret
has a nonzero basis difference; |1-chi_q(t)|>=4/q implies that one pair loses
at least8/q^2. Even giving all2m anchor penalties their maximal favorable
value, F<=m-8/q^2+2m*w<=m-6/q^2. Therefore the true character maximum is
EXACTLY m-2m*w, also the maximum over mixtures, with integrality gap2m*w.
The certificate uses polynomial modular algebra, not q^n secret enumeration.

This objective deliberately separates two feasible sets. It is NOT the
native noisy likelihood, whose three observed phase features have different
weights and centers. Do not report this gap as a planted-likelihood optimizer
failure, a general lower bound or a candidate algorithm. It nevertheless
falsifies the missing assertion that any higher-rank optimum can be rounded
merely because it satisfies all sparse native moment equalities.

## Repair In The Measured Observable Basis

Add explicit d_i=a_i-c_i nodes and anchor them by

    M_(d_i,0)=M_(a_i,c_i).

Choose n independent differences modulo3 and invert their basis D over the
FULL root q via prime-field inversion and Newton lifting. Compile q-multiple
loops on these basis nodes. For every original native row f_j, write

    f_j=sum_k lambda_jk*d_basis_k modq.

Use balanced integer coefficients |lambda|<q/2 and repeated doubling/adding,
including conjugation for negative coefficients. As before, addition z=u+v
imposes M_(z,0)=M_(u,-v). Identify each computed target anchor with its
original native anchor. Also keep all full translation constraints. This
adds O(m*n*log q) nodes/stencils plus the polynomial dense matrix and N^2
equality audit. No full q^n group or dense monomial enumeration is used.

For ANY feasible PSD matrix, Gram-vector errors relative to any fixed true
character obey epsilon_(u+v)<=epsilon_u+epsilon_v and conjugation preserves
the error. Set, at secret0,

    A=sum_basis_k [1-Re M_(d_k,0)],
    B=sum_native_j [1-Re M_(f_j,0)],
    C=sum_j sum_k lambda_jk^2.

Cauchy--Schwarz on each reconstructed row gives B<=C*A. At exact pair
saturation A=0, every native anchor is1 AT EVERY RANK. More generally, all
native moments are close to those of the shared character whenever C*A is
small. The same derivation holds after twisting by any fixed true character;
it does not require knowing a planted secret, but finding the right phase
center under noise remains a separate inference problem.

Choose

    w=min(1/(m*q^2),1/(1+C)).

The total all-pair deficit A_all dominates the chosen-basis deficit A.
Hence in the REPAIRED relaxation

    F=m-2m*w-A_all+w*B
      <=m-2m*w-(1-w*C)*A_all
      <=m-2m*w.

Secret0 attains equality: the previous diagnostic now has an exact all-rank
optimum equal to the true character optimum. This is a constructive repair,
not just another rejection. Re-running orthogonal-class saturation collapses
all native nodes to the anchor, independently checking its exact limit.
The rational certificate requires exact PSD and exact equality feasibility.

## Conditional Numerical Residual Budget

Keep PSD and diagonal1 EXACT but allow every selected complex moment equality
residual to have absolute value at most tau. Each affected anchored squared
error changes by at most2*tau. Triangle inequality gives an additional
sqrt(2*tau) per conjugation, addition or target step. A pair anchor contributes
one such term. Repeated doubling/accumulation for a positive coefficient c has
error coefficient3c, a negative coefficient at most4|c|; outer row additions
add at most2 per nonzero coefficient, and target equality adds1. Consequently

    epsilon_native_j <= sum_k |lambda_jk|*sqrt(2*a_basis_k)
                        +beta_j*sqrt(2*tau),
    beta_j=6*sum_k |lambda_jk|+1.

This upper bound deliberately does not use a rank-one approximation. Let
E=sum_j beta_j^2. Minkowski/Cauchy--Schwarz imply

    sqrt(B)<=sqrt(C*A)+sqrt(E*tau).

Substitute into the weighted objective and maximize the resulting quadratic
over sqrt(A_all)>=0. Because w*C<1, this proves

    F <= (m-2m*w) + [w*E/(1-w*C)]*tau.

The module retains every beta, the exact rational amplification, and the
maximum tau giving at most half of the old diagnostic gap as excess. This
gives a concrete precision falsifier rather than accepting an optimizer's
status. However, floating solver eigenvalues and approximate diagonals do NOT
certify the required exact PSD/unit-diagonal premises; their repair/error
budget is still separate. Nor does this certify native noisy recovery.

## Why This Is Still Not A Decoder

Native paired noise is not small angular noise. Its first harmonics are1/3,
so a real planted noisy fit generally has substantial basis-pair deficit.
The bound B<=C*A can then be vacuous; C grows with dimension and root size.
The proof repairs this separating objective, not the observed likelihood.
Large PSD rank still does not establish a representing distribution, and
the repaired matrix is not proved tight for every objective.

No sample advantage or new quantum operation is established. This remains
a classical representation audit of actual measured native states. Coherent
LWE examples, chosen-frequency queries, free postselection and clean unknown
state inverses remain ungranted.

The broader distinction between positive truncated moments and a representing
measure is established research. See the primary
[Laurent--Mourrain flat-extension paper](https://arxiv.org/abs/0812.2563).
Its extension conditions motivate future certification; we have not verified
that those conditions apply to this finite-group circuit. No novelty claim.

## Revised Next Experiment

Any numerical experiment must include both original-row and observable-basis
circuits, exact full translation accounting, numerical constraint-error
budgets, and the retained separating-score positive/negative controls.
Do NOT rerun only the old selected circuit and call an optimizer rank a
character distribution. Next research targets are native-source likelihood
tightness or an exact/approximate flat-extension certificate with polynomial
resource bounds. A further chart repair is only valuable if it improves that
native noisy inference question rather than fixing a convenient diagnostic.

Gemini owns optional CLI/registry integration and production validation. Run:

```sh
python theorems/ternary_observable_moment_lift.py --write
node research/certificates/ternary_observable_moment_lift_crosscheck.js
python -m pytest -q tests/test_ternary_observable_moment_lift.py
```
