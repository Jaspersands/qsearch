# A constructive restriction to a small affine search problem

**Status: proved probabilistic reduction, not a complete classical solver.**
The original input remains arbitrary distinct supplied points, arbitrary
target bits, q=2^n, N=n² and K=floor(N/8). No witness is supplied. This
reduction uses ordinary accepted-root sampling and polynomial arithmetic.

## Second moment over public syndromes

For any m>=K supplied columns, write H_U for their K-by-m Vandermonde
matrix. Let Z_U(s) count the accepted vectors with H_U x=s and put

    mu_U=(q/2)^m/q^K,       lambda_U(s)=Z_U(s)/mu_U.

The mean of lambda_U over uniform s in F_q^K is exactly one. For the
normalized Fourier coefficient of a local accepted set, r_i(0)=1 and,
for u!=0, r_i(u)=(-1)^b_i W(u)/q. Thus |r_i(u)|<=beta, where
beta=(1+2*sqrt(q))/q. Orthogonality gives the exact identity

    E_s |lambda_U(s)-1|²
      = sum_(v!=0) product_i |r_i((H_U^T v)_i)|².          (1)

This is an average over syndromes, not an assumed fixed-syndrome bound.
The evaluation code H_U^T F_q^K is MDS. For 0<=z<=1 its nonzero weight
enumerator obeys

    sum_(d!=0) z^wt(d)
      = sum_(t=0)^(K-1) binom(m,t)(1-z)^t z^(m-t)(q^(K-t)-1)
      <= q^K [z+(1-z)/q]^m.

To verify the equality, expand each factor as
z+(1-z)*1_(d_i=0), and count polynomials vanishing at a specified set
of t distinct points. No randomness of the evaluation points is used.
Taking z=beta² in (1), and using beta²<=8/q, gives the convenient bound

    V_m := 9^m q^(K-m) >= E_s |lambda_U(s)-1|².          (2)

Consequently the fraction of syndromes with no accepted preimage is at
most V_m. More generally, the fraction with |lambda_U(s)-1|>epsilon
is at most V_m/epsilon². These are Markov bounds on the nonnegative
square in (1), not independence assumptions about the trace bits.

## The actual randomized restriction

Choose any fixed residual set U of size

    m=K+s,       s=ceil(4K/n).

On its complement T, of size ell=N-m, independently sample each x_i
uniformly from its given accepted root set. Compute the residual syndrome

    h = -H_T x_T.

The remaining task is exactly H_U x_U=h with the original predicates
on U. It is an affine system with s free field variables after Gaussian
elimination. All sampled prefix coordinates already satisfy their own
target bits.

The syndrome distribution induced by x_T is within

    (1/2)*sqrt(V_ell)

in total variation of uniform: its density relative to uniform is the
same lambda_T, so Cauchy--Schwarz applies to (1). It follows that

    Pr[the sampled prefix has no full native extension]
       <= V_m + (1/2)*sqrt(V_ell).                       (3)

At N=n², K=floor(N/8), the first term is 2^-Omega(n²) and the second
is 2^-Omega(n³). Indeed s=4K/n+O(1), so
log2(V_m)<=(log2(9)-4)K+O(n), with log2(9)<4.
The procedure has polynomial running time and uses no extension oracle.

Finite evaluations of the conservative bounds (not search experiments):

| n | residual m | free field variables s | log2(V_m) upper bound | log2(prefix TV) upper bound | log2(mean extensions) |
|---|---:|---:|---:|---:|---:|
| 17 | 45 | 9 | -10.35 | -1382.27 | 108 |
| 31 | 136 | 16 | -64.89 | -9620.91 | 360 |
| 61 | 496 | 31 | -318.72 | -79069.50 | 1395 |

The bounds are uniform in the given points and target bits. The displayed
mean is q^s/2^m, averaged over syndromes; it is not an unconditional lower
bound for every residual syndrome.

## Self-attack and the remaining algorithmic obligation

The reduction does NOT output a witness and does not certify an individual
sampled prefix as extendable. Gaussian elimination leaves s=Theta(n)
field variables, hence Theta(n²) Boolean unknowns, subject to m=Theta(n²)
inverse-trace constraints. Enumerating q^s choices remains exponential.
The affine residual problem has a high check rate K/m and is not the
original fixed-rate native family; no quantum or classical theorem for
the original rate may silently be applied to it.

Its use as an attack is precise: an algorithm that solves these residual
instances for all but a negligible fraction of uniform syndromes, with
the same arbitrary public columns and target bits, would compose with
the restriction to solve the original native problem in polynomial time.
The public syndrome is computed, not supplied as a witness. A solver
that only succeeds on a specially chosen or planted syndrome would not
suffice. Any returned extension is verified against the original input.

There is a concrete reason not to turn the average statement into a
worst-syndrome statement: with K=1, two residual coordinates, target bits
(0,1), and syndrome zero, the check x_1+x_2=0 forces equal coordinates
and hence equal inverse-trace bits. That residual fiber is empty. This
does not contradict (1)--(3), which allow exceptional syndromes, and is
not a counterexample to the full native fixed-rate theorem.

The strongest falsifier of (3) would be a missing Fourier normalization
in (1) or a non-MDS column set. Both are explicit: the source probability
of s is lambda_U(s)/q^K, and arbitrary distinct evaluation points preserve
rank K for every set of at least K columns. The next decisive question
is a polynomial algorithm for this small-dimensional, high-check-rate
affine inverse-trace system, rather than more counting estimates for the
already abundant full-size fibers.
