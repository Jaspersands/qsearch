# Native Descent: Adaptive Error And Exact Phase-Contrast Loss

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. This composes the new source-driven
reference receiver with actual original-source promises and exhibits an exact
noise failure mechanism for its common-index compression. It is neither a
Gaussian noise identification nor a universal lower bound on quantum recovery.

## Adaptive Error Budget

Let C=K*sum_(j=0)^(L-1) W^j be the receiver's ORIGINAL copy upper bound,
W=(n+1)^2, K=n+8. Suppose the paid source consists of independent labelled
registers whose joint preparation can be compared to the ideal IID source.
Per-original trace-distance promises delta give a joint error <=min(1,C*delta)
by the tensor-product telescoping inequality. Marginal closeness alone does
not establish this for correlated inputs. Public label laws and preparation
correlations must be included in the promise, not silently discarded.

The complete adaptive receiver, including measurements, learned-prefix gates,
classical feedback and failure outcomes, is a CPTP instrument. Trace distance
contracts through it. There is no division by a rare measured branch and no
postselection amplification of the guarantee. The fixed cap is necessary for
an a priori statement; substituting an attractive ideal-run copy count is not
automatically valid for a different noisy adaptive execution.

Each original lineage traverses at most L-1 merges. Thus conservative known
SUM gates and complement measurements are bounded by (L-1)*C. Final digit
gates number <=(2L-1)*K (Fourier gates at all levels, phase corrections above
level1); final digit measurements number L*K. With a per-known-unitary operator
error eps_U and per-measurement half-diamond error eps_M, hybrid replacement
gives implementation loss <=

    min(1,C*delta + ((L-1)*C+(2L-1)*K)*eps_U
                  + ((L-1)*C+L*K)*eps_M).

The conditional ideal correct-recovery lower bound becomes

    max(0,1-L*(3^n-1)/(2*3^K)-implementation_loss).

These are promised error bounds, not implemented hardware synthesis or tests
that a supplied source is really IID. A zero lower bound means that this
generic guarantee is insufficient. It does NOT predict actual failure or
exclude a sharper distribution-specific analysis.

## Composing The Existing Noisy Classical-Pair Preparation

`native_noisy_phase_input.py` provides the averaged-density bound
delta <=20*V/q^2 plus paid preparation error, for independent symmetric errors
with a true integer second-moment promise V. This is not a bound on every
individual pure realization. It supplies even level L=2r at q=3^r, uniform
native labels, and an unknown integer-embedded secret; the new full-ring
receiver includes that special secret family.

The composition charges 2C independent ORIGINAL classical records and the
existing preparation gate precision at C qutrits. Native receiver gate and
measurement error are separate, set to zero only in the ideal reference
compositions. Source rounding is still owed and explicitly excluded here.
When q=3^n and V/q^2=n^-6, the growing-depth generic composition is vacuous.
This does not refute the original capacity/Gaussian refinements, which concern
different indexed-bank access and weighted exposure. It shows that the
measured recursive receiver does not inherit their favorable budget for free.

Access distinction: a classical-pair preparation begins with classical noisy
records; classical attacks may keep them. Copy-only native data cannot be
called a separation for that original classical problem without comparing
against those attacks and proving the reduction's distributions and hardness.

## Exact Independent Dephasing Family

For ideal uniform-modulus native phase vector psi, consider the actual density

    rho_v=v*|psi><psi|+(1-v)*I_3/3, 0<=v<=1.

This is a phase-dephasing channel: random ternary Z phases with probabilities
(1+2v)/3,(1-v)/3,(1-v)/3. Its trace distance from the ideal pure input is exactly
2*(1-v)/3. This explicit legal noise family is NOT claimed to be the Gaussian
classical-pair source above.

For supplied independent densities rho_i and measured offsets v_i, the
unnormalized retained density in the literal common-index instrument is

    rho_out[t,u]=product_i rho_i[(t+v_i) mod3,(u+v_i) mod3].

Every diagonal equals3^-B, so every complement outcome still has probability
3^(1-B). Off-diagonals multiply the input contrasts. After normalization,
the output is exactly the ideal native CHILD density with visibility

    visibility_child=product_i visibility_i.

This identity works for full ring secrets and keeps the same public child
labels. No selected branch is more favorable. Repeated disjoint merges give
visibility=(1-eta)^B for a packet with B ORIGINAL ancestors, where each original
has contrast1-eta. B is actual lineage size, not the pessimistic recursion
upper bound promoted to a typical or necessary exposure.

Given a correct learned prefix, the final Fourier character readout is right
with probability(1+2*visibility)/3 and wrong with probability(1-visibility)/3
for EACH other character. Its advantage above chance is2*visibility/3.
The exact compact power obeys

    max(0,1-B*eta) <= (1-eta)^B <= 1/(1+B*eta).

At eta=1 the visibility is zero. At large ancestry, even polynomially small
per-original dephasing may destroy this receiver's contrast. This is an exact
failure mode of this compression channel, NOT a no-go for error correction,
different collective receivers, different source access or quantum LWE.

## Transcript-Specific Error, Not A Simulated Robust Decoder

The report imports the complete, independently replayed ideal source traces.
For a FIXED full-rank public selector/offset transcript, disjoint final packets
have independent dephasing errors. The probability that EVERY digit readout
matches its ideal value is exactly

    product_packets (1+2*(1-eta)^(original_ancestry))/3.

On that event each prefix is correctly learned. The current noiseless solver
demands consistent full-rank equations; it has no error-correcting decoder.
Noisy contradictory equations can fail explicitly instead of returning a
secret. This calculation is a sufficient correct-recovery event and a
conditional instrument analysis, NOT a claim that a noisy receiver was run
or that a finite transcript characterizes the source population.

## Actual Symmetric-Error Kernel Transport

The existing even-native preparation uses two independent symmetric errors
per qutrit. Let gamma=E[exp(2*pi*i*e/q)] be their REAL characteristic value.
For the nonnegative-gamma regime considered here, its averaged native density
has the exact Schur coherence kernel

    K=[[1,gamma,gamma],[gamma,1,gamma^2],[gamma,gamma^2,1]].

The kernel is not isotropic dephasing. Source symmetry, independence and this
characteristic value remain promises; a second moment does not determine a
Gaussian density or an exact characteristic. An intermediate odd-level sample
is a descended native density, not newly prepared from imaginary fresh errors.

Every original computational index has the form t+tau_i mod3 in a retained
packet. A merge's measured offset is ADDED to each parent's accumulated tau_i.
The complete public trace determines the three original-offset counts c0,c1,c2,
with c0+c1+c2=B. For an off-diagonal pair(t,u), let m be the omitted ternary
index. Its exact contrast is gamma^(B+c_(-m)). Thus the correct Fourier-character
readout, GIVEN a correct measured prefix, has probability

    1/3 + 2/9 * (gamma^(B+c0)+gamma^(B+c1)+gamma^(B+c2)).

The report propagates actual ORIGINAL offsets through every recorded merge
and multiplies these probabilities on disjoint final packets. It does not
restart the same kernel at every level or replace it by a guessed Gaussian.
This transports the algebraic noise law of the existing preparation, without
yet proving its physical source promises or implementing a robust decoder.

For a FIXED, unfiltered disjoint tree with B original leaves, all B-1 relative
offsets are uniform: the complete SUM basis change is a permutation. One pivot
leaf has tau=0; the rest have independent uniform offsets. A multinomial sum
then gives mean retained visibility

    [gamma*(2+gamma)/3]^B.

This is only a fixed-tree average. Do not use it for arbitrary trees selected
after conditioning on full labels or outputs. The transcript-specific formula
above needs no such average-tree assumption. A parameter gamma near1 does not
automatically survive large ORIGINAL ancestry.

## Falsifiers And Next Decision

- Dense SUM-gate/complement projection differs from the product-entry density.
- Branch probabilities or contrasts depend on a preferred secret-dependent
  outcome, or a general error budget is divided by branch probability.
- Correlated source marginals are treated as independent joint preparation.
- This explicit dephasing channel is relabelled as Gaussian noise without proof.
- An upper-copy ledger or a vacuous error bound becomes universal impossibility.
- The noiseless equation solver is promoted to a robust noisy decoder.

NEXT: certify the original error characteristic/preparation promises,
estimate ancestry distributions without favorably filtering labels,
and design a robust decoding/noise-management mechanism. A polynomial-size
ideal receiver still needs a meaningful distribution-specific noise budget.

```
python theorems/native_descent_noise_composition.py --write
node research/certificates/native_descent_noise_crosscheck.js
python -m pytest -q tests/test_native_descent_noise_composition.py
```
