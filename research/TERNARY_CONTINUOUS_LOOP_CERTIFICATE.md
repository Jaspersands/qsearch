# Exact Continuous-Angle Self-Loop Certificates

IMPLEMENTED / LOCAL DERIVATION REVIEW PENDING / NO ALGORITHM OR SPEEDUP.
This pass closes a specific remaining escape route in the two-layer
population bound: the coarse
continuous self-loop ceiling43/27 can grow with the number of native inputs.
The earlier quarter-turn and near-entropy bounds remain valid independently.

The circuit starts from KNOWN uniform native words and attempts public
target-fiber preparation. It is not an arbitrary measurement lower bound
on the unknown-secret native phase states, nor their preparation inverse.

Each actual self loop is P(z,w)/81 for |z|=|w|=1, where P has integer
Laurent coefficients and degree<=1 in each variable. Sampling angles near
modulus1 does not prove a global bound. Instead search for the identity

    81^2-|P(z,w)|^2 = sum_j c_j |Q_j(z,w)|^2,

with POSITIVE RATIONAL c_j and INTEGER Q_j supported on the nine monomials
z^i*w^j, i,j in{0,1,2}. Every Q_j has coefficient sum zero, since the
left side vanishes at z=w=1. Multiplying P by z*w does not change its torus
modulus. The finite search pool uses zero-sum two-positive/two-negative
integer vectors, including repeated monomials and common-factor reduction.
A three-positive/three-negative fallback supplies certificates for the five
states not covered by the smaller pool. All137 states are now certified.

Linear programming proposes a support. An exact rational linear solve must
then give nonnegative weights, and EVERY Laurent coefficient in the complete
identity must agree. Numerical feasibility, sampled maxima, rounded weights
and unknown status cannot certify anything. Failure to find a certificate
in this restricted cone is NOT a counterexample to modulus<=1.

## Sharpened Population Bound

Every self loop has modulus<=1 at ALL continuous mixer angles. Along any
complete transfer path there are at most5 strict lattice increases, each
with total absolute outgoing weight<=18. Phase moments have modulus<=1.
Consequently, with G=q^n and D=3^M,

    s=min(1,G^-1*sum_(j=0..min(5,M)) binomial(M,j)*18^j)
    P_uniform <= s
    P_Born <= min(1,s+sqrt((G-1)*s/D)).

The fixed-angle bound has no exponentially growing factor in M. It is
exponentially weak when G grows exponentially in the input parameter and M
is polynomial in that parameter. For finite inputs it may still be vacuous;
Born decay also requires a growing ORIGINAL copy count. No near-entropy-only
premise or all-input-count Born-hardness claim is needed or justified.

For the original mismatch-cost circuit, the same implicit four-angle net
permits public label/target-adaptive GLOBAL angles:

    E[best_angle_success] <= min(1,m^4*s+88*(n+M)/(7*m)),
    m=ceil(ceil(1/s)^(1/5)).

Apply the original source-variance correction to this adaptive uniform bound.
The mathematical net is not an implemented optimizer or a free training
algorithm. Increasing the batch from M648 to M12800 at n128/q243 does not
restore this template's population success, whereas the former43/27 bound
becomes vacuous there.

## A Broader Fixed-Program Consequence

The same fixed-program bound covers two additional variations without
repeating numerical circuit menus:

- Each native word coordinate can have its own two product-mixer angles,
  chosen BEFORE the IID frequency rows and target. The transfer matrices may
  vary by coordinate, but share the same graph, loop bound1 and jump bound18.
- Each cost phase can be an arbitrary fixed function f_l:G->unit circle
  applied to F(x)-y. It need not split over frequency coordinates. For any
  path tuple, the joint full-root residual distribution is determined by
  its complete integer column lattice. Its phase product therefore has a
  lattice-dependent average of modulus<=1. The population path grouping
  remains valid even without the special factor m_L^n.

These extensions may be combined. They do NOT cover residual functions
trained on the actual labels, phases depending on absolute F(x)/y rather
than their difference, or target-specific coordinate angles. Such choices
can depend on the chart and break this grouping argument. A constant-size
family selected after labels admits a union bound; an unrestricted learned
function family or a2M-angle policy does not inherit the four-angle net.
New label-sensitive mixer SHAPES and genuinely different collective
operations remain open. This is a fixed shallow-family obstruction, not
general quantum hardness or a receiver construction.

Here is the exact source-law step behind the arbitrary-function extension.
For a pointed four-path coefficient matrix C with2M columns, the source
map C:(Z_q)^(2M)->(Z_q)^4 is a group homomorphism. Its independent uniform
input produces the uniform distribution on its image: every image point
has the same kernel-sized preimage. Two matrices generating the SAME integer
column lattice L have the same image modulo q, since each set of columns is
an integer combination of the other. Integer HNF reduction therefore
preserves the whole joint distribution, not just the annihilator size.
The n independent frequency coordinates produce the product image law.
For fixed f1,f2, average the unit-modulus function
f1(d1)*f2(d2)*conj(f1(d3))*conj(f2(d4)) under that law. This gives one
complex number m_L of modulus<=1 for every complete lattice. Neither a
factorization across frequency coordinates nor evaluation of the full image
is needed for the envelope. Public label-trained functions would enter this
average themselves and destroy the stated fixed-function step.

## Independent Verification

The independent Node checker reconstructs self-loop gate monomials from
the parent graph, verifies ALL Laurent defect coefficients with BigInt
rationals, requires positive weights and zero-sum integer square factors,
and recomputes all sharpened envelopes. The parent integer-lattice/Smith
checker is a separate prerequisite; both reports pin their upstream files.
Tests must reject coefficient, sign, missing-state and scope tampering.
Numerical support selection never establishes the result by itself.

Falsifiers: an exact identity fails; a square weight is negative; one state
is absent; the actual gate polynomial differs; source/chart invariance
fails; or an adaptive function policy is misclassified as a fixed program.
No accepted algorithm, quantum speedup or novelty claim is supplied.
