# A Uniform Bound For Every Surface-Source Query

2026-10-23. Explicit arithmetic construction and proof; geometric and
coherent-source implementations remain absent. This closes the public
trace-bound calculation, not the entire source-correctness obligation.

## 1. Bounded Elementary Compiler

Let d=2g and M in SL_d(F_ell), ell odd. Gauss--Jordan elimination without
normalizing pivots uses at most d(d-1) elimination transvections. A signed
row exchange costs three more. At most d-1 exchanges occur because the
last pivot cannot be zero in an invertible triangular remainder.

After elimination the diagonal D has determinant one. Express it using
d-1 two-coordinate diagonal corrections. Each correction is

    diag(a,a^-1)=w(a)w(-1),
    w(a)=e_ij(a)e_ji(-a^-1)e_ij(a),

and therefore costs six transvections. Inverting the elimination word
does not increase its length. A uniform physical-word bound is

    W=(d-1)(d+9).

For g=2, d=4, W=39. A physical elementary operation between different
elliptic factors lifts directly to a quaternionic elementary unit. An
operation within one factor is replaced by the four-factor commutator
through a physical coordinate in another factor. Therefore the number
of quaternionic factors is at most L=4W=156. These bounds hold for every
matrix, not merely sampled symplectic matrices.

`sl_word` implements this elimination, and `lift_symplectic` performs the
same-factor expansion and centered quaternion lifts. It records an exact
inverse word. Tests check matrix reduction, inverse products, polarization
congruence, and the quadratic identity on the resulting S=sigma^dagger sigma.

## 2. Public Trace Bound From The Actual Source Basis

Let b_1,...,b_4 be the supplied integral quaternion basis and put

    B=sum_i nrd(b_i).

Solve each required split-matrix lift modulo ell, choosing centered basis
coefficients z_i in [-(ell-1)/2,(ell-1)/2]. The definite quaternion norm is
Euclidean, so the triangle and Cauchy--Schwarz inequalities imply

    nrd(sum_i z_i b_i)
      <= (sum_i |z_i| sqrt(nrd(b_i)))^2
      <= (sum_i z_i^2) B
      <= (ell-1)^2 B.

A quaternionic elementary factor E=I_2+E_ab(q), a!=b, has squared
quaternion Frobenius norm 2+nrd(q). Define

    U=2+(ell-1)^2 B,       t_max=U^156.

Submultiplicativity gives ||sigma||_F^2 <= U^L <= t_max. The empty word
has squared norm 2, also below this bound. For the source's two-dimensional
matrix S, its trace parameter is exactly

    t=S_11+S_22=||sigma||_F^2.

Thus the smooth-repolarization identity may use this ONE t_max for every
query. The bound depends only on the public full order basis and ell,
not on the secret K, an observed t, or a sampled maximum. With t>=2 and
Moore determinant one, Tr(H^2)=2(t^2-2) supplies a uniform Rosati norm
bound as well. No generic g>2 quadratic identity is claimed.

The exponent 156 is deliberately conservative. It establishes a bit-length
bound, not a practical implementation. It must be updated if a different
compiler, coefficient lift, or basis representation is substituted.

## 3. One Smooth Denominator And Fixed Auxiliary Data

Multiply successive small primes, omitting p and ell, until

    D > t_max+2.

Because p and ell are odd, D is even. It is squarefree, supported away
from p*ell, and is the SAME integer for every query. Standard primorial
growth bounds make its largest prime and log D polynomial in the public
bit input. Omitting two primes changes only those polynomial bounds.
No factorization of t+2 or t-2 is required.

The earlier smooth-repolarization construction uses r^2-torsion for each
prime r dividing D. Obtain the common-unit weak phi images of full source
bases at these fixed levels once, along with the fixed marking levels.
Subsequent query-dependent sigma/H/C/F actions use the stored coordinates.
There is no need to ask the weak phi evaluator coherent queries. This
does NOT make the geometric quotient/canonicalization computations free.

The naive dimension-16 direct quotient lists can involve r^32 kernel
elements. They remain fixed-dimension polynomial in the bit input only
because r is polynomially bounded; the constants and exponents are severe.
The uniform bound is not a practical resource estimate.

## 4. Fixed Random Tapes: A Conditional Coherence Compilation

The group size is

    |Sp_4(F_ell)|=ell^4*(ell^2-1)*(ell^4-1) < ell^10.

Suppose a query has at most B_alg randomized subcalls, with a public
polynomial expected-time bound and recognizable successful output for
each Las Vegas subroutine. Cap each attempt at twice its uniform expected
bound; Markov gives success at least 1/2. After R independent attempts,
its failure probability is at most 2^-R. Choose

    R >= ceil(log2(|Sp_4|*B_alg/delta)).

Select random tapes once before the quantum computation. A union bound
then gives probability at least 1-delta that ALL capped subcalls succeed
on ALL group inputs. Correlations from tape reuse across inputs do not
invalidate that union bound. On this event the program is deterministic
and correct on the whole superposition domain and has a fixed polynomial
clock. Reversibly compute the canonical label, copy it, and uncompute
garbage. Pad labels and work registers to public length bounds.

This is a compilation lemma, not proof that every required geometric
routine has the assumed uniform bound, verification mechanism, field
control, or canonical output. Monte Carlo routines require their own
worst-case correctness analysis. Arbitrary raw quotient coordinates are
not canonical labels; randomized choice independence must be proved after
joint marked canonicalization. Failed histories cannot silently be
assigned plausible subgroup labels.

## 5. What Remains Open

The exact compiler and public denominator are now executable. The proposed
geometric source still needs independent review, honest theta/point
controls, a fully charged canonicalization implementation, and an attack
using the real classical data. The receiver still has no executed quantum
HPGP learner. No new hardness or speedup claim follows from this bound.
