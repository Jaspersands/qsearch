# Change The Divisor Class, Not Just Its Convenient Representative

## Status

Application of existing Riemann-Roch-system results to the concrete tower
from the preceding pass. This is an existence/measure argument, NOT a
generated candidate, uniform class sampler, classical hardness theorem,
implemented quantum algorithm or novelty claim. It prevents overextending
the near-canonical classical negative result into a false universal claim.

The full-support native relation stays Bz=s with every coordinate nonzero.
The proposed escape only removes the SAME-code cubic-annihilator solver;
auxiliary-code methods and unrelated classical attacks remain live.

## A Precise Escape From The Particular Classical Obstruction

Fix one actual curve X/F_100003 in the certified S-split tower, degree e>=8,
with genus g=5e+1 and the22e distinct rational evaluation points D. Let G
range over ALL F_p-rational degree-d divisor classes, d=10e+3=2g+1, not
only canonical-plus-effective-small-divisor classes or one-point divisors.

The code V=ev_D L(G) has k=5e+3 and square dimension w=15e+6. This is
independent of the divisor class because d>=2g+1 and22e>2d. The previously
proposed quantum sufficient bound is therefore unchanged.

Normal generation and AG duality give the exact identity

    dim((V^3)^perp) = ell(K_X-3G+D).                 (1)

The right-hand divisor degree is a=2e-9, strictly between0 and g-1. Thus
avoiding the cubic attack means solving the Riemann-Roch equation
ell(-3G+(K_X+D))=0. This is a known type of problem, not a new mathematical
representation introduced here.

Let h=#J(F_p), let J[3] denote rational3-torsion, and let A_a be the number
of effective degree-a divisors. The map [G] -> [K_X+D-3G] has either zero
or #J[3] preimages for each class. At most A_a image classes are effective.
For UNIFORM [G] in Pic^d(F_p),

    Pr(ell(K_X-3G+D)>0) <= #J[3] A_a/h.             (2)

This does not assume multiplication by3 is onto. Omitting its torsion
factor is false: in J=(Z/3Z)^2 the image is a single class and a one-element
bad set can capture every input. The tests contain that countercontrol.

[Cascudo-Cramer-Xing, Theorem3.2 and Proposition3.4](https://arxiv.org/html/1207.2936)
give the RR-system counting criterion and the bound
A_a/h <= g/[p^(g-a-1)(sqrt(p)-1)^2]. Their discussion also distinguishes
existence from efficient sampling and code construction. Applying their
bound with the elementary #J[3]<=3^(2g), and sqrt(100003)>316, yields

    Pr(bad) <= 9^(5e+1)(5e+1) / (100003^(3e+9) * 315^2).       (3)

At e=8 this is41*9^41/(100003^33*315^2), below10^-128. It decreases
geometrically: increasing e by1 multiplies it by
9^5/100003^3 * (5e+6)/(5e+1), which is <2*9^5/100003^3<1 for e>=1.
The helper uses exact rational arithmetic. Its decimal display is not the
proof. No numerical parameter tuple is being asserted to generate a curve:
the source existence was established separately with a concrete seed.

Consequently suitable divisor classes EXIST on every such curve, and
overwhelmingly many classes kill the same-code cubic annihilator while
retaining the square-decoder sufficient bound. The earlier near-canonical
examples are highly nongeneric in this distribution; that is fully
consistent with their persistent93-section classical obstruction.

## Important Missing Steps

1. Actually generate an appropriate class. Sampling a random rational point,
   a short sum of such points, a one-point divisor, or K+three points is NOT
   uniform Pic^d sampling. No mixing or near-uniformity claim is supplied.
   A sampler at total-variation distance epsilon gives only the modified
   bad bound (3)+epsilon, not (3) itself.
2. Produce an explicit presentation of the higher prime-field tower level,
   then its divisor arithmetic, Riemann-Roch basis and parity matrix. The
   tower existence theorem alone supplies none of these complexity bounds.
3. Move the chosen divisor to a representative disjoint from D. Weak
   approximation permits this mathematically, but a charged implementation
   must be supplied. Moving within a class does not change the obstruction
   ell(K-3G+D); selecting a new class is the substantive step.
4. Run the actual matrix test U=V^3. It must have full rank m. An existence
   probability or random seed is not a substitute for that test.
5. Attack with AUXILIARY codes E. Removing (V^3)^perp does not remove
   annihilators of V*E^2, low-degree reconstruction, classical full-support
   search, or special covering-curve algorithms.
6. Supply a useful-problem reduction and novelty comparison. Neither the
   existence theorem nor failure of one classical method supplies them.

The existing
[COFI-DQI work of Matthews-Shapiro](https://arxiv.org/html/2609.31484v1)
already studies AG-code/DQI constructions. Its discussed objective and
families differ from this particular full-support/cubic-annihilator question,
but the broad idea of combining curves and decoded interference is prior
art. No first-in-literature claim is justified here.

## The Strongest Immediate Classical Counterproposal

The cubic method chooses E=V. On a curve, an alternative evaluation code
E=ev_D L(F) can use a differential in Omega(G+2F-D). Finding an effective
representative of K_X-G-2F+D could therefore restore the classical norm
attack even when (1) is zero. If deg F=d, the residual degree is again a.
The selection problem now involves multiplication by2 on the Jacobian,
not3. The theorem (3) says nothing about searching adaptively over F.

This auxiliary-code route is the next high-value falsifier. Before building
a generalized class-search system, determine whether choosing F can be done
constructively in polynomial time and whether the required product/rank
conditions follow. Do not confuse existence of some F with an algorithm
for finding it, or failure of a few choices with hardness.

## Handoff

The only implementation here is an exact arithmetic bound with mathematical
countercontrols. It deliberately does not populate a candidate registry.
Gemini may wire the existing RR/curve backend after a verified main checkout
and a precise source/sampler algorithm are available. Do not spend effort
on a new generic pipeline or large parameter sweeps before the auxiliary
classical attack question is answered.
