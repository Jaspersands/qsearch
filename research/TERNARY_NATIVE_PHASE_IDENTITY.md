# Compact Native Phase Merges And Soundness-Accounted Identity Testing

LOCAL DERIVATION / REVIEW PENDING. This supplies a growing-depth public phase
representation and a randomized verifier, NOT a useful merge-rule finder,
exact proof by testing, full-depth decoder or quantum speedup.

## The Representation Is Nonclassical

An acquired odd-level2r+1 native packet retains root3^r. Standardize d free
coordinates with real complement measurements, accepting every outcome.
Each physical input evaluates a three-entry frequency table at
b_i+D_i*z over F3. Its original modulus is N=3^(r+1). Group the nonzero D_i
by their canonical projective direction L (first nonzero entry1), absorbing
its sign and b_i into the table. The exact phase component functions are

    Q_l(z) = (sum_L T_(L,l)(L*z) mod N)/3.

Tables are normalized T(0)=0, T(2)=2T(1) mod3, and
sum_L T_(L,l)(1)*L=0 over F3. These ensure GLOBAL divisibility by3 for every z.
Individual tables need NOT be divisible by3. Dividing them separately or
treating the result as an ordinary low-degree F3 polynomial discards carries.
The test suite includes lift(x)+lift(y)-lift(x+y) as an explicit carry trap.

This uses3*n entries per occupied projective form, not all symmetric tensors
of growing order. Evaluations are exact modular integer arithmetic. Public
functions and derivatives are NOT an unknown secret-weighted phase oracle.
The existing native additive-degree bound D=2r+1 remains valid:

* For a local native table, Delta^2 T is divisible by3.
* Delta^3=-3*S*Delta with S^3=I; hence Delta^(2r+2) T=0 mod N.
* A nonzero ternary increment2 gives Delta_2=-S^2*Delta_1, so mixed local
  increments obey the same bound.
* Affine pullback and sums preserve additive degree; global exact division3
  maps the numerator's zero derivatives to zeros at retained root3^r.

The schema verifies low linearity, global kernel, canonical tables/directions
and the native bound; it does not accept an arbitrary caller-supplied degree.

An additional exact certificate uses each group's local valuations. Put
R=r+1, u=min valuation3(Delta T), v=min valuation3(Delta^2 T), assigning
valuation R to zero modulo3^R. The exact LOCAL additive degree is

    max(0,2*(R-u)-1,2*(R-v)).

This follows by locating the last nonzero odd/even difference in the same
operator identities. The maximum over groups/components is a valid GLOBAL
upper bound, not necessarily an equality: groups can cancel further. A
requested derivative order above this bound is algebraically certified
zero without random testing. No growing tensor is expanded. In particular,
if every merged table is divisible by3, the upper bound drops from2r+1 to
2r. That does not mean the phase is an ordinary quadratic over F3.

## One-Use Growing-Depth Merge

Keep all acquired program costs/IDs. For each selected supplied program,
SUM-c_j into its wires from known data and measure m_j, c_j in{1,2}.
The resulting diagonal data phase is Q_j(m_j+c_j*z), with EVERY outcome
probability3^-d even on reference-entangled data. Unselected programs remain
live but are not counted as fresh unconditioned samples. No clones,
conjugate states, unknown inverse or label-matching factory is provided.

Every group table shifts to T(L*m_j+c_j*t)-T(L*m_j). Merge coincident keys
by modular addition. The output remains in the same compact native-degree
class, at the SAME retained root. Unlike the preceding cubic factory, this
operation does not truncate to field3 or claim its higher top terms cancel.
All original-source branches and conditional injection masses are charged.
No full-depth IID output-label theorem is supplied here.

## A Dimension-Independent Identity Test

For ANY additive polynomial P:H->G of degree<=D on a finite abelian group,
with P not identically0, its relative support is at least2^-D. Proof:
degree0 nonzero functions are constant and have support1. Otherwise choose
h with Delta_h P nonzero. Its degree is at most D-1, and its support lies in
supp(P) union(supp(P)-h). Induction gives2*wt(P)>=2^(-(D-1)). If P is already
nonzero constant the stronger bound1 applies. The proof works for vector
codomains, with support meaning at least one component is nonzero.

To test degree<=t, sample the identity

    H(x,v_1,...,v_(t+1))=Delta_(v_1)...Delta_(v_(t+1)) Q(x).

As a function of ALL its variables, H still has degree<=D: it is a signed
sum of affine pullbacks of Q. Its degree is NOT automatically D-(t+1) when
the directions also vary. If this identity is false, uniform independent
samples detect a counterexample with probability at least2^-D each.

T=kappa*2^D tests therefore give false acceptance at most
(1-2^-D)^T<=exp(-kappa)<=2^-kappa. For native D=2r+1 this is

    T=2*kappa*4^r=2*kappa*q^(log_3(4)), q=3^r,

polynomial in q and INDEPENDENT of d and tensor-entry counts. It is not
polynomial in log q, and can still be expensive at cryptographic moduli.
Evaluate derivatives by repeatedly differencing each three-entry ridge table:
O(n*groups*(t+1)) modular work per test, no2^(t+1) cube and no3^d table.

Commit the candidate representation and order BEFORE drawing fresh points.
Adaptive candidate search must use fresh independent tests for each proposal
and a union/error budget across proposals. Default tests use SystemRandom;
fixed seeds are reproducible CALIBRATIONS, not a mathematical randomness
certificate. If the requested sample budget is not met, return uncertified
no-witness status, never a claimed identity. Any observed nonzero derivative
is an exact counterexample regardless of randomness or budget. Passing a
finite test remains probabilistic evidence, not an accepted proof obligation.

## Live Growing-Depth Falsification

The producer starts with the real n2/d3 source cohort used by the cubic
factory. It lifts each original pair from modulus9 to27/81, preserving its
low chart, with prespecified additional high digits. The same cubic relation
and signed injections are then evaluated at retained roots3/9/27. This
tests a CONCRETE naive extension rather than an unrelated artificial oracle.
Check the quadratic identity and the proposed top-degree cancellation at
each depth; retain exact counterexamples. The pinned controls actually have
an exact ridge upper bound2r: the highest odd native degree cancels, but
the degree-two identity FAILS at retained roots9 and27. Their recorded
nonzero third derivatives are exact falsifiers of naive quadratic transfer.
Preserved low charts/calibration
seeds are not an IID population acceptance estimate. The three complete
small word tables independently verify the compact evaluator against actual
original frequencies. Physical SUM replays consume each program once and
test all outcomes on maximally reference-entangled data.

The independent JS checker reconstructs native frequency charts, whole small
tables, merged phases, exact derivative witnesses from finite differences,
resource counts, degree-class membership and identity budgets. It does not
claim to certify pseudorandom test soundness or an external quantum source.

## Why This Matters, And What It Does Not Solve

This removes high-degree tensor expansion from evaluating explicit native
merge proposals. It enables high-variance search over compact factored
programs with soundness accounting and definitive counterexample records.
It does NOT find useful relations, guarantee adequate source throughput,
retain a useful output label law, eliminate upstream errors or decode a
large-root secret. A compact representation is not a compact solver.

Known cyclotomic sieves already have quasipolynomial time/sample bounds when
q=poly(n), and limited approximate inputs remain a separate obstacle:
[Boucher, Fouque and Shen](https://arxiv.org/html/2609.34996v1).
Any claimed advance must improve the complete algorithm against those costs,
not merely accelerate the public verifier. Next research: propose a compact
merge policy that cancels a useful native layer WITHOUT multiplying fresh
cohort costs, and attack it with this verifier before expanding tensors.

```
python theorems/ternary_native_phase_identity.py --write
node research/certificates/ternary_native_phase_identity_crosscheck.js
python -m pytest -q tests/test_ternary_native_phase_identity.py
```
