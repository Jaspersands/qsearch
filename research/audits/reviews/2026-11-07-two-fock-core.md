# Independent actual-text core review: two Fock branches

7 November 2026. Read current STATE/TRAPS, the complete
`TWO_FOCK_GAUSSIAN_LEARNING.md`, and the exact-source fallback scope in
`2026-11-07-two-fock-sources.md`. **ACCEPT the written uniform learner under
those sourced primitive contracts.** No quantum execution, optimality,
novelty, or classical-input separation is established by this review.

The statement is for a shared EVEN Gaussian G applied to two equal-parity
Fock strings, with known physical Majoranas and exact IID copies. Arbitrary
Gaussian branches need not have commuting covariances and are not covered.
Read n as a positive integer and epsilon,eta in (0,1). Coincident strings,
when present in a normalized description, are simply one Fock branch.

## Moment algebra and eigenvalue

For k>=6 the two/four-Majorana cross matrix elements vanish in the Fock
frame, and Gaussian conjugation preserves these degree bounds. With the
main note's signs C_ab=i<gamma_a gamma_b> and
T_abcd=-<gamma_a gamma_b gamma_c gamma_d>, Wick's formula gives T=W(C)
for one Gaussian branch. The mixture calculation therefore yields exactly
K=a W(J), a=4p(1-p), with the stated commuting B,J decomposition.

Flattening in the coordinates X_ab, a<b, gives

    (W(J) X)_ab = <J,X> J_ab + (J X J)_ab,
    <J,X>=Tr(J^T X)/2.

On active skew matrices, X -> JXJ is an involution. It is -1 on matrices
commuting with J and +1 on anticommuting matrices. Separating J itself
gives precisely the listed multiplicities and top eigenvalue a(k-1).
Outside active pairs the map is zero. The top gap is a(k-2), not a
dimension-independent gap assumed as advice. The note correctly avoids
the mixture formula at k=2 and invokes the small-core fallback there.

## Rounding constants

Clipping measured moments preserves their error bounds and bounds each
factor by one. Each product in W(Chat) consequently has error at most
2delta, so K entry error is at most 7delta. A matrix on at most 2n^2
pair coordinates has operator error at most 14n^2 delta. The covariance
Frobenius bound c<=2n delta is also correct.

In the true-k, non-small-weight case, a>=2tau. The stated Davis--Kahan
bound d=4sqrt(n)e/tau is conservative even after the sqrt(2) conversion
from pair-vector Euclidean norm to skew-matrix Frobenius norm. The given
delta ensures e<gap/4 with a very large margin. J is feasible for nearest
rank-2k partial-complex-structure rounding, so

    ||Jhat-J||F<=2d,       ||Phat-P||F<=4d.

Equal-rank projectors at distance below one admit the usual direct
principal-plane rotation R, with ||R-I||F<=2||Phat-P||F. This is an
existence comparison only. Transporting B by R gives a feasible Btilde
on the learned complement with error at most 16d.

Let Ehat=(I-Phat)Chat(I-Phat). Since ||C||op<=1 and its true compression
is B, ||Ehat-B||F<=c+8d. Hence ||Ehat-Btilde||F<=c+24d. Nearest polar
rounding on that complement gives

    ||Bhat-B||F <= 2(c+24d)+16d = 2c+64d.

Adding the J error proves the displayed 2c+66d branch bound. In the true
trial the compressed matrix is nonsingular and well conditioned because
it is close to Btilde, whose nonempty singular values are all one. An empty
complement at k=n is harmless. Wrong trials may use the specified fallback.

## State reconstruction, parity, and uniformity

In a pure Gaussian reference's particle-hole vacuum frame, expected total
excitation number is ||Gamma-Gamma'||F^2/8. The probability of any excitation
bounds infidelity, proving the note's covariance-to-state estimate with
the stated normalization. Aligning the two branch ray phases, their vector
errors also bound the distance of alpha|branch0>+beta|branch1> to the learned
two-dimensional span. There is no hidden relative-phase assumption here.
The displayed delta is far smaller than required to make these errors
less than epsilon/1000.

The candidates cover all cases: constant-dimensional tomography handles
n<6; the exact fixed-4 pure learner handles k<=4; for k>=6 a branch of
weight at most tau can be discarded at distance at most sqrt(tau), and
polar(Chat) approximates the dominant branch; otherwise the true-k trial
has the proved inverse-polynomial gap. No algorithm must identify which
case is true before constructing its candidate list.

Because Bhat and Jhat have orthogonal supports, simultaneous Gaussian
normal form gives two exactly orthogonal known Fock strings differing
on k modes. An occupation-sign adjustment permits an SO rotation while
retaining odd branch parity. Equivalently the note's known X1 conjugation
flips the entire input parity sector and can be restored. Neither approach
supplies the unknown G or identifies O(2n) with SO(2n).

The affine-bit-map measurement of the unnormalized 2x2 block is legal:
failed spectator checks contribute zero. For the true candidate its weight
is close to one and the block is rank one before sampling error; PSD
projection and a top eigenvector therefore recover the coherent phase
with a constant spectral separation. The block protocol is not exponential
in k and does not postselect without paying failures. Its output and the
Gaussian frame yield an explicit pure preparation circuit.

Fresh-copy validation with additive epsilon^2/100 error selects a candidate
with infidelity at most epsilon^2/100+2epsilon^2/100<epsilon^2 whenever the
promised good candidate and all validation estimates succeed. A union
bound over the polynomial list and all stated source events suffices;
independence between those success events is not assumed.

## Resource and source boundary

The moment cost is O(n^4 delta^-2 log(n/eta)), hence the displayed
O(n^24 epsilon^-20 log(n/eta)) bound. Pair-matrix diagonalization, skew
rounding, and simultaneous normal form involve polynomial-dimensional
matrices. Additive numerical errors smaller than delta leave all correct-
trial gaps intact; arbitrary degenerate wrong trials are capped and can
return a fixed valid circuit. Gaussian compilation uses O(n^2) rotations,
each implementable with polynomially many ordinary gates and polynomial
precision. This charges time/BIT cost as well as measurement count.

The exact fixed-4 PURE fallback is the imported Mele--Herasymenko contract
identified in the source review; the approximate mixed-output theorem is
not used. The remaining argument above is the local mathematical deduction.
The supplied-description Gaussian/Pfaffian classical baseline remains, and
all reconstruction processing is classical. This review does not audit
other literature beyond the cited source contracts or infer priority.
