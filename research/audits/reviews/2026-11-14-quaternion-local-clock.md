# Compact quaternion words do not bound Page's residual local walk

2026-11-14. Algebraic check only; no CAS run or parameter scan.
Source: `audits/sources/integral_quaternion_selection/page.txt`, physical LF.

Let A=(2,3)_Q, i^2=2, and let O be ANY maximal order containing i.
Such orders exist, since the standard integral order embeds in a maximal
order. At p=7 the algebra is split and Q_7(i)=Q_7 x Q_7. The two roots of
X^2-2 in Z_7 reduce to +3 and -3. Their difference is a unit, so the
spectral idempotents of i belong to O_7. They split its rank-two matrix
lattice into rank-one direct summands: i is integrally diagonalizable.

Set xi=(3+i)^2=11+6i. Since N(3+i)=7, its two local eigenvalues have
valuations 0 and 1: at i=+3 the residue of 3+i is 6, while at i=-3 it
vanishes. Their product is exactly 7. Hence xi has eigenvalue valuations
0,2, and nrd(xi)=49.

For n>=0 let M=2^n and I_M=xi^M O. This is an integral principal right
ideal, with a compact power description of O(n+1) bits over fixed O and xi.
Its local matrix elementary divisors at 7 are (0,2M), and

    nrd(I_M)=(7^(2M)),   d(P_0,xi^M P_0)=2M.

(As a rank-four Z_7 lattice its Smith exponents are 0,0,2M,2M.)
Because one matrix elementary divisor is a unit, I_M is not contained in
7O. Thus Page PReduce Step 1 extracts r=0; it does not remove this distance
as a two-sided central factor. The initial Step 2 value is k=2M.

Source Subalgorithm 3.9, LF403–417, initializes b=0, changes k to k-2
only on b=1 iterations, toggles b, and stops at k<2. Therefore this input
requires EXACTLY M pairs of iterations, or 2M edge steps. Proposition
3.10, LF430–433, independently identifies one edge of progress per iteration.
This is exponential in the binary exponent length, without any cancellation
or eigenvalue approximation assumption.

This does NOT contradict Page's stated bound: LF922–928 bounds the walk by
log N(I) and charges an expanded ideal input, whose size here is already
Theta(M). It refutes using compact word length ALONE as a bound on this
unchanged residual walk. It does not show that a new HNF-based compiler must
produce this family, or rule out batching, a different representation, or
a different algorithm. The principal generator is itself already compact.

There is also an exact norm-only support warning. Put

    u=(3+i)/(3-i)=(11+6i)/7,                 nrd(u)=1.

In Q(sqrt(2)), write P_+=(7,i-3), P_-=(7,i+3). Then
v_(P_+)(u)=-1 and v_(P_-)(u)=+1. Away from 7, both 3+i and 3-i are
units. The rational norm cancels the two nonzero valuations, but u is not
an O_7-unit (indeed it is not integral there). Thus, if 7 is outside the
allowed support, nrd(u)=1 does NOT certify quaternion S-unit membership.
An implementation must retain field-prime valuations, or an equivalent
local integral-membership certificate, rather than only rational norm data.
This example does not obstruct norm-one lifting with those data retained.
