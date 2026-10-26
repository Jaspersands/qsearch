# Low-degree inverse-trace multiples: explicit reconstruction and scope

**Proved deduction.** The published low-algebraic-immunity observation
does produce explicit equations for the native task. It does not by itself
produce a polynomial algorithm for their coupled solution. Here is a direct
construction, including its exceptional point and actual degree growth.

Let f(x)=Tr(inv0(x)) on F_(2^n). Take n>=5, an integer s>=2, and
a=ceil(n/s)>=2. Let d have binary ones at positions
0,s,2s,...,(a-1)s. Its cyclic gaps are at most s. For j=0,...,n-1 let
r_j be the representative of d-2^j modulo 2^n-1 in {1,...,2^n-2}.
None is zero because d has at least two ones. Define the field-valued
polynomial function

    h_b(x)=sum_j x^(r_j) + b*x^d.

For nonzero x this is exactly x^d*(f(x)+b). It is also zero at x=0.
Consequently

    h_0(x)=0 iff f(x)=0,
    h_1(x)=0 iff [f(x)=1 or x=0].

Subtracting 2^j from d removes a one if that bit was set. Otherwise a
cyclic borrow removes the next one and fills at most s-1 zero positions.
Thus wt_2(r_j)<=a+s-2, and every binary coordinate of h_b has algebraic
degree at most D=a+s-2. Choosing s close to sqrt(n) gives D=O(sqrt(n)).
The identity is valid in any supplied field basis; Frobenius powers are
binary linear maps, and field multiplication is bilinear.

This is a spaced-bit realization of the low-degree-multiple idea in the
[Nawaz--Gong--Gupta upper-bound construction](https://cacr.uwaterloo.ca/techreports/2006/cacr2006-09.pdf).
The full primary PDF became accessible later in this review. Section 4,
Lemma 3 and Theorem 2 use spaced exponent bits and bound the inverse-trace
multiple degree by s+ceil(n/s)-2. The field-valued algebra above was
independently derived and preserves an exact predicate equation away from
zero. The exact immunity value
ceil(2*sqrt(n))-2 is stated in the
[Feng--Gong published abstract](https://link.springer.com/article/10.1007/s11424-016-5208-z);
no unaccessed proof is being represented as read.

## Composition with the native code

Substitute a systematic linear parametrization x=Gz of C, with
n*(N-K) binary message variables. This gives nN explicit polynomial
coordinate equations h_(b_i)(x_i)=0 of degree at most D. On the stratum
where every target-one coordinate is nonzero, these equations are exactly
the original trace conditions, together with the already imposed Hx=0.
Legal zero coordinates at target-zero positions are retained.

The sparse field formulas have polynomial evaluation circuits. Expanding
them as generic Boolean equations and linearizing through degree D,
however, exposes a monomial basis of size

    sum_(j=0)^D binom(n*(N-K),j)=2^Theta(sqrt(n)*log(n))

for the native scaling and s~sqrt(n). This describes that generic basis,
not a lower bound on all sparse or structured algorithms, and not an upper
bound on the degree a complete solver would need. No polynomial-size
elimination closure or recovery procedure follows from the degree bound.
The many scalar coordinate equations have algebraic dependencies: they
encode one predicate multiplied by the unknown field value x^d.

## Self-attack and the exact unresolved step

Dropping the nonzero conditions gives an immediate false solver: the
all-zero word satisfies every h_(b_i) equation and Hx=0 for every target,
including the all-one target. An independent native verifier rejects it.
This defect is in the relaxed classical formulation, not in the quantum
argument. Adding an inverse variable with x_i*y_i=1 at target-one
positions removes it, but returns a coupled polynomial system rather than
a linear solve.

The strongest falsifier of the remaining assessment would be a constructive
algorithm exploiting these particular sparse multiples and the Vandermonde
geometry with polynomial bit cost, including the nonzero conditions. A
low-degree multiplier, a large solution count, or a generic Boolean solver
call without a complexity argument does not supply that missing step.
This investigation gives an exact attack interface and a false-solution
counterexample, not classical hardness.
