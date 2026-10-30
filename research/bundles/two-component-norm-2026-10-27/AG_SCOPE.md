# A Geometric Scope For The Two-Component Attack

27 October 2026. Scoped independent AI mathematical review completed. This is a
conditional-on-public-geometry CLASSICAL algorithm, not a new quantum
algorithm. Read RESULT.md first. The existing degree-eight control has a
handpicked divisor and does not test the distributional argument here.

## Retained Native Source

Use the existing tower contract over ODD q: a smooth geometrically connected
curve X/F_q of genus g=5e+1, e>=8; m=22e distinct rational evaluation points D;
an effective public divisor I of degree e disjoint from D; a uniformly
sampled closed prime G of degree d=10e+3; and the complete code
V=ev_D L(G), with k=5e+3. The prime degree exceeds one, so G cannot meet D
or the support of I when I is the pullback of the rational infinity point
in the existing unramified tower. Retain that tower-specific support fact;
do not infer it for an arbitrary effective I with high-degree support.

The input representation must expose X,D,I,G, effective Riemann-Roch
evaluation and, for a monomially transformed B, the corresponding public
coordinate multipliers. B alone does NOT supply these data by this note.
The existing geometry-recovery results are separate dependencies, not
silently imported. The syndrome s remains arbitrary; no planted answer.

## Public Auxiliary Construction

Set A=ev_D L(8I), with r>=3e. Its columns are nonzero because 1 is a
section, and evaluation on more than 8e points is injective. Compute

    Hspace = (ev_D L(G+16I))^perp.

It annihilates V*A^2. Via the usual residue/evaluation duality, its zero
patterns are those of L(J), J=D+K_X-G-16I, of degree 6e-3. This is an
effective code computation, not a supplied h oracle. Nonzero coordinate
scales in the duality do not change zeros. Also dim(Hspace)>=e-3>0.

Suppose Hspace has no coordinate which is identically zero. Then for
uniform h in Hspace the expected number z of zero coordinates is m/q.
Markov gives

    Pr[z >= 4e-3] <= 22e/[q(4e-3)].                         (A1)

The algorithm checks z<4e-3 and retries h if necessary. For a passing h,
every nonzero c in V has wt(h*c)>=12e-3-z>8e. Thus all restrictions
A_support(h*c) have rank r, exactly the sufficient promise of RESULT.md.
No exponential enumeration of c is required under the geometric promise.

The random-offset failure bound is therefore at most

    m q^(k+2-2r) <= 22e q^(5-e).                           (A2)

If q>=1019 and e>=8, (A1) and (A2) are each below 1/2. With the additional
condition q^2>=44e, the zero-pair union bound is at most 1/2 as well.
The nested h/offset/kernel retries have bounded expected constant counts;
linear algebra, field arithmetic and the PAID geometric preprocessing
dominate. Hard caps can be chosen for any requested error probability.

## Why The Generic Prime Source Has No Such Base Points

For any P in D, Riemann-Roch implies that P can be a base point of L(J)
only if L(K_X-J+P) is nonzero. Here

    K_X-J+P = G+16I-D+P,       degree t=4e+4.

As [G] varies, this is a translation between degree-d and degree-t Picard
torsors. At most A_t classes are bad for a fixed P, where A_t is the total
number of effective degree-t divisors. A union bound gives at most m A_t
bad classes for some P. No uniform-Picard assumption is being made.

Using the curve zeta function and Weil's |alpha_j|=sqrt(q),

    A_t <= q^t (1+q^(-1/2))^(2g)/(1-q^(-1)).              (A3)

Indeed the coefficient of 1/((1-T)(1-qT)) at degree u is at most
q^u/(1-q^(-1)); bounding the numerator coefficients by
binom(2g,j)q^(j/2) and summing proves (A3).

For d>2g-2, a fixed rational degree-d class contains at most
(q^(d-g+1)-1)/(q-1) effective divisors, hence at most that many prime
divisors. Use the existing source's prime-count lower bound

    number of closed degree-d primes >= q^d/(2d).         (A4)

This bound is an explicit imported prerequisite, not inferred merely
from existence of a tower. Combining (A3)-(A4), the UNIFORM-PRIME source
has base-point failure probability at most

    beta = min(1, 2 d m q^(-e+3)
                       (1+q^(-1/2))^(10e+2)/(1-q^(-1))^2). (A5)

If the source then rejects matrices whose Schur cube is not full, the
conditional bad probability is at most min(1,beta/(1-epsilon_cube)), where the
existing source proof supplies Pr[cube not full]<=epsilon_cube<1.
To assert a small conditional failure probability, the denominator needs
a quantitative lower bound, not merely positivity. This conditioning
factor must not be dropped. A directly observed
base-point-free Hspace is an unconditional certificate for THAT input;
it does not require the distributional argument.

## Consequence And Exact Boundary

For this geometric source, outside the explicitly bounded bad-divisor
event, the attack solves EVERY syndrome in expected polynomial time when
q>=1019 and q^2>=44e. It broadens the known easy parameter range from a
linear field-size cutoff to a square-root cutoff. The public geometry and
all preprocessing remain charged; this is not yet a B-only theorem.

At q=1019 the certified interval extends through e<=floor(1019^2/44)
=23599, hence through dyadic e=16384. This does NOT construct matrices at
those degrees, certify practical runtime, or resolve e->infinity at fixed
q. The earlier generic greedy cutoff was e<=202, hence dyadic e=128.
The sharper known fiber-repair theorem applies to its own special divisor
family, not automatically to this generic-prime distribution.

For growing fields q>=sqrt(44e), this is an asymptotic classical threat
that must be applied before promoting a quantum signal. At fixed q and
larger e, the present guarantee stops. A small success is not evidence
that the guarantee continues, and failure is not evidence of hardness.

The tools used are standard Riemann-Roch, AG duality, Weil bounds and the
prior quadratic-annihilator idea. No novelty claim is made for their
composition. These source deductions do not replace the already reviewed
native tower/Riemann-Roch backend or its remaining implementation work.
