# Native Ternary Kernel Packets: A Correlated Receiver Target

LOCAL DERIVATION / REVIEW PENDING. No candidate or breakthrough claim. This
continues `CYCLOTOMIC_RESCALING_GATE.md`: retaining many registers is not the
same as producing many useful independent samples.

See `TERNARY_PHASE_DEPTH.md` for the growing-depth successor: an exact local
derivative engine, weighted higher-Schur admission constraints, and a
conditional degree-versus-secret-visibility gate. Formal lifted quadratic
degree must not be substituted for additive phase degree.

## Native Compiler And Exact Source

For odd L>=3, take m existing IID cyclotomic phase samples with integer secret
s and public labels y_i in R_L^n. Let A have columns y_i modpi. Public GF3 RREF
gives pivot/free columns. A known SUM shear writes each independent syndrome
into a pivot register; measure these r=rank(A) registers, keeping every outcome.
Retain h=m-r registers, with physical indices j=x+Vz over F3.

The original ternary CCP starts at even level2t. Acquiring these intermediate
odd-level samples requires earlier native transformations and their sample
costs; this packet module does NOT charge or solve that acquisition stage.
Treat its results as conditional receiver building blocks, not a new free
source oracle or a complete CCP algorithm.

For each secret component l, define the known native frequency

```text
q = 3^((L+1)/2)
C_l(j) = q*sum_i B_L(lambda_(j_i), y_(i,l)) modq
Q_l(z) = (C_l(x+Vz)-C_l(x))/3 mod(q/3)
```

The numerator is ACTUALLY divisible by3. For odd L, the normalized trace row
has equal nonzero residues mod3, so C_l(j) mod3 is a fixed unit times the
low-label linear form. That form is constant on the public kernel fiber.

Every syndrome has probability3^-r, independent of secret and full labels.
The surviving normalized state, up to the retained branch's global phase, is

```text
3^(-h/2) sum_z exp(2*pi*i*sum_l s_l*Q_l(z)/(q/3)) |z>
```

The public compiler does not know s. Secret-dependent amplitudes are bounded
calibration, not an available preparation/inverse or a classical phase oracle.
Its compact evaluator is scalable; dense tables/interpolation are explicitly
capped. Independent JS checks the native formulas, GF3 elimination, every
branch amplitude, source norm and reduced-register purity.

The measured output sees only s mod(q/3). Its top secret digit is lost in
branch global phases, which cannot be coherently recombined after measurement.
Full recovery needs a proved, charged digit-recursion/source transformation.
A different coherent instrument retaining syndrome registers is not excluded.

## Level3 Is Cubic, Not A Product Or Stabilizer Shortcut

At L3, q9 and for a label y=(a,b), the scalar native frequency values are

```text
C_y(0)=0, C_y(1)=a-2b, C_y(2)=-a-b mod9.
C_y(2)-2*C_y(1) = 3*(b-a) mod9.
```

Each frequency is a linear lifted digit plus3 times a quadratic digit function.
Its fourth additive differences vanish mod9. Substitution by an affine GF3
chart preserves that additive degree. Divisibility by3 therefore makes Q_l
a classical F3 polynomial of total degree<=3. Tensor interpolation confirms
the exact reduced polynomial, not a numerical fit.

The leading cubic terms depend only on A and its kernel chart. A higher-label
perturbation by pi*z contributes a quadratic digit phase after division, and
an affine syndrome shift cannot change the leading cubic terms. Tests vary
both higher digits and all syndromes while preserving the cubic signature.

Three unfiltered L3 controls have degree3 component functions and entangled
survivors. First-register purities include5/9 and11/27, unlike1 or1/3 for a
pure ternary stabilizer's one-register reduction. This verifies non-stabilizer
examples, not that every secret/source instance is non-stabilizer. Zero secret
or cancellations between components can remove a cubic phase.

The output is a FAMILY of known random functions Q_l weighted by the SAME n
unknown secret coordinates. It is not IID PSP samples and not identical copies
of one unknown polynomial state. Learning the entire arbitrary polynomial
would ignore this potentially valuable low-dimensional parameter structure.
The higher-impact target is a receiver recovering s from different public
native packets with known Q_l, without assuming phase-evaluation access.

## Conditional Three-Packet Degree Reduction

Suppose three independently supplied packets have the same leading cubic
polynomial for EACH secret component, in aligned coordinates. Public SUM
differences and measurement would retain the pointwise phase sum

```text
sum_(i=1)^3 Q_(i,l)(z+x_i).
```

Translation leaves its leading degree unchanged;3 times the common cubic
part is zero in F3. The sum is quadratic. The packets need not have identical
lower-degree terms or identical states. Tests check every shift pair in a
bounded calibration and reject mismatched leading tensors. The live artifact
uses fresh independent high labels CONDITIONED on a common low matrix.

This pass verifies the conditional algebra, NOT a full three-packet instrument
or native matcher. It records required independent input count rather than
pretending three repeated descriptors certify physical copies.

Literal low-matrix matching of second/third batches to the first costs
3^(-2*n*m). For the calibration n2,m4 this is3^-16; conditioning all three
initial syndromes to zero costs another3^-6. These are exact costs for that
literal strategy, NOT lower bounds for all tensor alignment or packet matching.
All native instrument controls retain every syndrome; zero-syndrome selection
belongs only to the separately costed conditional algebra experiment.

A quadratic output is still NOT a secret decoder. The quadratic tensors and
linear terms vary across packets. No identical-state learner, unknown inverse,
complex conjugation, cloning or free matched-source promise is granted.

## Growing-Level Falsifier

At L5, q27 and frequencies are C1=-a-b, C2=-2a+b. After the same kernel step,
the phase modulus is9 rather than3. A native source control's fourth mixed
additive derivative, directions(e1,e1,e2,e3), equals(3,6) mod9 across its two
secret components. The classical cubic model therefore does NOT transfer.
No universal higher-level receiver impossibility is asserted.

Constant-fraction REGISTER retention can coexist with difficult correlated
phase decoding, lost secret digits, and increasing phase depth. Solving just
the fixed L3 case would not establish polynomial complexity for growing q.

## Literature Transfer Checks

[Arunachalam, Bravyi, Dutt and Yoder](https://arxiv.org/html/2208.07851) study
copies of one unknown phase function on a Boolean domain; their Section5.1
generalized separable theorem additionally assumes even q. It is not a theorem
for our varying ternary packets. An adaptation remains a research possibility.

[Allcock, Doriguello, Ivanyos and Santha](https://arxiv.org/html/2405.06357)
give qudit stabilizer-learning methods and demonstrate limits of ordinary Bell
sampling. Their stated stabilizer learner uses copies of an unknown stabilizer
state. Our native cubic packets, and unaligned quadratic outputs, do not
automatically meet that input promise. Neither paper is being refuted.

## Sharper Receiver Target: Public Polynomial Fibers

For L3, let Q(z)=(Q_1(z),...,Q_n(z)), N=3^n and
P(v)=|Q^-1(v)|/3^h. Uniform secret prior is an explicit assumption here.
Let |nu_v> be the normalized uniform state on each nonempty public fiber.
The actual packet is sum_v sqrt(P(v))*omega^(s.v)*|nu_v>.

The standard covariant square-root measurement, adapted to this ensemble, has

```text
mu_s = N^(-1/2)*sum_(v:P(v)>0) omega^(s.v)*|nu_v>
optimal average success = (sum_v sqrt(P(v)))^2/N
                       <= number_of_nonempty_fibers/N.
```

Character orthogonality makes sum_s |mu_s><mu_s| the projector on the fiber
span; complete the measurement arbitrarily off that span. For optimality,
the dual operator Y=(sum sqrt(P)/N)*sum_v sqrt(P(v))*|nu_v><nu_v| dominates
|psi_s><psi_s|/N for every s by weighted Cauchy-Schwarz. Its trace equals the
displayed achievable success. This is an information benchmark, not a new
measurement algorithm or novel PGM theorem.

Zero-syndrome calibrations for seeds46011/12/13 have9/9/6 nonempty fibers and
ideal successes about.923/.940/.635. These small conditional values say nothing
about scaling advantage or source acquisition. They were independently
recomputed from the public residual tables, not promoted to live speedups.

The computational obligation is an efficient COHERENT fiber-basis transform
or another receiver with comparable recovery, without constructing a3^h
table. Computing Q coherently and then measuring its value destroys the
unknown secret phase as a fiber-global phase; it is NOT this measurement.
A classical preimage sampler alone also does not supply the required coherent
uncomputation. The structured native cubic map is the target, rather than
generic phase-state tomography or another primitive-only benchmark.

## Evidence And Next Obligations

`TERNARY_SCHUR_TENSOR.md` replaces the dense cubic signature with the exact
factored native formula T_l=-sum_i A_li*(Vu)_i*(Vv)_i*(Vw)_i. All diagonal
polarizations vanish automatically in characteristic3; mixed-term tests are
mandatory. It also adds stronger2012/2016 polynomial-graph baselines: known
univariate methods can handle DIFFERENT public coefficient matrices sharing
unknown parameters, so identical copies are not a universal requirement.
Fixed-level source variation alone must not be claimed as a general barrier.

`CYCLOTOMIC_FIBER_RECEIVER.md` now checks this measurement target on the
ORIGINAL even-level source with the FULL secret, avoiding this conditional
odd-source acquisition and lost-digit issues. Exact coordinates expose IID
three-choice modular subset sums, not a new source correlation. The charged
binary/cyclotomic conversion is already known. An actual bounded public-DP
receiver works, but its count table is exponential ON AVERAGE at informative
sample density. That reference does not rule out implicit or non-PGM decoders.
Read its contract before proposing a new packet-based algorithm.

- Six unfiltered L3/L5 controls;54 native syndrome branches;1,458 complete
 complex amplitudes independently replayed. JS checks729 cubic function values
 and81 conditional quadratic-sum values, plus the higher-level countercontrol.
- 19 focused tests, including all small one-row low sources, exact interpolation,
 invertible basis compilation, fourth differences, cubic-signature invariance,
 every matching shift, mismatch rejection, secret loss and source costs.
- No full production/CLI green claim. Source records and routine integration
 remain Gemini's task. No commit or push.

Next: exploit the native public tensor structure to align source packets at
polynomial cost, or devise a receiver for varying correlated phase functions
without matching. Keep classical inference and strongest known quantum
baselines in the SAME access model. Reject any route whose growing-depth
complexity, rare filtering or secret-digit recursion recreates quasi-polynomial
cost. Public polynomial rank alone is not a decoder: its coefficients do not
contain the unknown secret.

```sh
python theorems/ternary_carry_packets.py
python -m pytest -q tests/test_ternary_carry_packets.py
node research/certificates/ternary_carry_crosscheck.js
```
