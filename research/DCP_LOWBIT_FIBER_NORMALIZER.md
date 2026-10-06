# Reversible First-Layer Fiber Normalization

LOCAL DERIVATION / REVIEW PENDING. A constructive subroutine, not an accepted
candidate or full decoder. The common-isotropic construction is reused from
`dcp_carry_packets.py`; no novelty or quantum-speedup claim is made.

This follows `DCP_DENSE_PHASE_TRANSPORT.md`. The goal is to replace exponential
residue matching with a polynomial operation. This pass supplies the FIRST
residue bit plane and explicitly tests why its quadratic proof cannot simply
be repeated. It does not restore circuit search or propose a toy oracle.

## Construction Without A Fiber Table

For the native zero-origin packet F_A(z)=A x(z)/2 mod(q/2), its residue modulo2
has the form

    f(z) = L_H z + q_B(z),

where q_B is a vector of quadratic Boolean forms determined only by the binary
labels B. Middle label bits supply the uniformly random linear part. Higher
unused bits do not enter this first-layer construction.

Choose a common totally isotropic subspace U of dimension d using the existing
polynomial greedy constructor, which guarantees d>=ceil(k/(n+1)). Extend U to a
full binary basis [U,V]. For coordinates z=Uu+Vy, total isotropy implies

    f(Uu+Vy) = L_y u + c_y.

L_y and c_y require only public residue evaluations at the background and its
d direction neighbors; no ANF expansion or fiber enumeration is needed.
If L_y has rank n, append standard rows to make an invertible d by d matrix
T_y whose first n rows are L_y. Normalize

    w = (T_y u + (c_y,0), y).

The first n output bits equal the n actual residue bits. If rank is deficient,
use the identity on u instead. The complete operation remains a permutation
on ALL k-bit assignments, including failures. Its inverse recomputes y,T_y
and uses binary Gaussian elimination. No successful-background postselection
is built into the permutation.

The compiler, evaluation, and inverse are uniformly polynomial classical
algorithms. They can in principle be made reversible with charged workspace
and uncomputation. A physical backend/export is NOT implemented or validated.
Large-dimension matrices have not been executed. All bounded enumeration is
in calibration controls, never in the normalizer's compiler or evaluators.

## Exact Native Source Law

For EVERY fixed low B and fixed complementary background y, the random middle
labels restrict to an IID uniform n by d binary matrix on U. Indeed, physical
kernel images of independent U directions are independent; each native middle
row maps surjectively to d independent coefficients. The deterministic quadratic
background term merely translates this matrix distribution. Thus

    E_middle fraction_good_backgrounds
      = product_(i=0)^(n-1) (1-2^(i-d)),
    E_middle fraction_bad_backgrounds
      <= (2^n-1)/2^d < 2^(n-d).

These background events are NOT independent. The proof uses linearity of the
source expectation, not a product of event probabilities. The certificate
substitutes the guaranteed minimum d for a conservative lower success bound.

In the natural lattice-coordinate regime, k=4n^2+16 gives d>=4n-3 for large n.
The source-mean bad fraction is consequently exponentially small. This is a
bit-plane normalization bound, NOT secret-recovery probability. Prefix source
acceptance and original-state consumption still belong to the dense contract.

Unused higher labels remain independent before good-background conditioning.
Conditioning or measuring the good-background flag reweights the joint source.
It does NOT create a new native parity chart for the next layer. The underlying
packet magnitudes are uniform, so the flag probability does not depend on the
unknown secret; its rejection still costs original states and source mass.

## What This Does Not Accomplish

For a successful background, write the complete higher residue as

    F_A(P(t,r)) = t + 2 R_t(r),

where t is the vector of first residue bits. The phase is still

    exp(2 pi i s.(t+2R_t(r))/(q/2)).

Its dependence on t is generally entangled with r. Normalizing a bit plane
does NOT extract independent secret equations, justify a partial QFT, remove
the higher phase, or grant clean copies. Measuring t retains a phased fiber
but loses information and changes the source; it is not a free recursion.
Keeping t coherent and recursively normalizing R_t is the actual unfinished
transport task. Coordinate-bit ordering can be handled by a known permutation
once ALL layers are constructed.

The full classical two-call witness baseline remains applicable IF this
classically evaluated permutation is extended to a complete transport.
The first layer alone is neither an arithmetic witness finder for the full
modulus nor a DCP decoder.

## A Concrete Recursion Falsifier

The bounded native label row

    A=(9,13,11,9,9,11), q=16

has k=5. The low-selected isotropic directions are (1,6,24), extended by
(2,8). EVERY complementary background has full first-layer rank. Fix the first
residue bit to0. The low bit of the higher quotient R_0, in its four remaining
canonical coordinates, has ANF masks

    1,2,4,8,12,13,14,15.

Its degree is FOUR, not at most two. This is a direct counterexample to blindly
applying the native quadratic-model theorem after this reparameterization.
The example is not selected as an algorithmic success; it falsifies a closure
assumption. Other parameterizations might have lower degree. Higher-degree
circuit representations may remain efficient. Neither every recursion nor
every higher-bit algorithm is excluded.

Potential failure modes for the positive direction:

- The next family requires solving a growing-degree polynomial system.
- Selecting directions that linearize it already solves the target arithmetic.
- Rank normalization survives but conditional source independence does not.
- Success losses multiply through Theta(n) layers in the lattice regime.
- Reversible rank/unrank or inverse costs become exponential.
- A purely classical completed transport provides the same arithmetic witness
  success as the exact two-call baseline; reassess its role instead of falsely
  claiming that the DCP source itself was classically simulated.

## Next Theory Task

Find a structure-preserving recursion on the compact PHYSICAL Boolean evaluator,
not an exponentially expanded ANF. State the invariant, construct each inverse,
and derive the native conditional source law at every stage. Test it first on
the quartic countercontrol. Alternatively find a quantum branch-mixing operation
that does not require coherent fiber ranking. Existing Gram/thermal/walk audits
already reject generic normalization and local-walk shortcuts; do not repeat
those audits without an actual new arithmetic operation.

Stop immediately if the proposal assumes the next quotient is another native
quadratic chart merely because unused higher label bits are still random.
That implication is false: their Boolean coefficient functions have changed.
No independent theorem review or novel full-modulus algorithm has emerged.

## Verification

`python theorems/dcp_lowbit_fiber_normalizer.py --save` generates the report.
Eight focused tests cover inverse arithmetic, whole-space reversibility,
source-lineage geometry, complete middle-label matrix laws, and the quartic
countercontrol. Two complete ensembles contain64 and4,096 middle-label tables
and67,584 full-permutation inverse/residue checks. The independent Node checker
recomputes these bounded properties and the scaling formulas. Full production
registry/CLI validation and reversible backend construction remain Gemini work.
