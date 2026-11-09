# Gaussian channel continuity and the exact small-program norm bound

2026-11-07. CLOSED independent mathematical review within the open
Gaussian-channel-mixture pass. Read STATE/TRAPS,
`GAUSSIAN_CHANNEL_MIXTURE_ADMISSION.md`, the Gaussian-channel source
1604.01954, and the actual FLO-learning source Proposition 2.6. No
network/API, Git, implementation or finite experiment was used.

**Verdict:** a gap-free polynomial diamond-continuity bound holds for
single STANDARD quasifree Gaussian CPTP maps. The exact reference-marginal
factorization and CP program norm lemma are also valid with the tensor
gauges below. These facts do not yet supply a deterministic efficient
low-rank channel implementation or a full mixture learner.

## 1. Precise full-channel convention

The channel is the ordinary-qubit map obtained from an even Gaussian
Stinespring unitary with a Gaussian environment, using system modes first
and environment last. Equivalently it is the standard quasifree map on
the FULL Majorana algebra, including odd operators. A and B specify this
map, with covariance action `Gamma -> A Gamma A^T+B` and
`I-AA^T+iB>=0` (complex conjugation gives the alternate sign convention).

Only specifying the action on even input covariances is insufficient.
Identity and parity dephasing `(rho+P rho P)/2` agree on every even state
but differ on arbitrary input coherences; on one qubit, |+> witnesses raw
trace-norm difference one. Nor can one discard the sign of A: A and -A
have identical covariance actions but generally different odd actions.

For Choi queries fix REFERENCE FIRST, then system, then the environment.
The known pure Gaussian state

    Omega_RS=2^(-n/2) product_j(1+a_Rj^dagger a_Sj^dagger)|vac>

equals `(V_R tensor I_S)|Phi_standard>`, where
`V_R=product_{i<j} CZ_(Ri,Rj)`. This follows from the fermionic sign
`(-1)^(w(w-1)/2)` when the selected pair creators are put into reference-
then-system order. Applying the ordinary query on S produces a Gaussian
J_G: the even SE dilation is also Gaussian on RSE, and the environment
is traced last. Ordinary Choi and J_G differ by the known reference V_R.
This is not an uncharged identification of ordinary and graded tensor
products. V_R has O(n^2) elementary gates.

## 2. A fixed pure-environment dilation with no inverse noise matrix

Put d=2n and, for a physical parameter pair, set

    M=I-AA^T+iB,  sqrt(M)=U+iV,
    R=[A,U,V],  J_E=[[0,-I_d],[I_d,0]].

Here U,V are real matrices. Multiplying sqrt(M) by its adjoint gives

    UU^T+VV^T=I-AA^T,
    VU^T-UV^T=B.

Thus RR^T=I, and the fixed pure Gaussian environment on 2n modes with
covariance J_E produces noise
`[U,V] J_E [U,V]^T=B`. Complete R to an element O of SO(6n), adjusting
one unused output row's sign if necessary. Its Gaussian unitary on 3n
modes, this fixed environment, and ordinary environment discard realize
the desired channel. All output-system Majorana monomials depend only on
R, so the completion's other rows are immaterial.

The claim is about the full channel, not just Gaussian inputs. Expanding
the transformed Majorana monomials and evaluating the even Gaussian
environment uses its Wick contractions; these are determined by A,B.
This gives the standard quasifree adjoint on every monomial, which is an
operator basis. In particular its degree-one action is exactly A.

For two physical pairs define
`alpha=||A-A'||op`, `beta=||B-B'||op`. Since A,A' are contractions,

    ||M-M'||op<=2 alpha+beta.

For positive matrices the operator square-root inequality is
`||sqrt(M)-sqrt(M')||op<=sqrt(||M-M'||op)`. It also follows directly
from operator monotonicity and `sqrt(X+tI)<=sqrt(X)+sqrt(t)I`, in both
directions. The real block `[U-U',V-V']` has operator norm at most the
complex norm of the square-root difference: test its transpose on a real
unit vector. Consequently

    eta:=||R-R'||op<=alpha+sqrt(2 alpha+beta).              (1)

Zero eigenvalues of M cause no singular inverse and require no noise gap.

## 3. Nearby completions and the diamond bound

Here is an explicit local completion argument. Let X=R^T and Y=R'^T have
orthonormal columns and assume eta<=1/4. Write P=XX^T, Q=YY^T, so
`||P-Q||<=2 eta`. The polar factor U0 of

    N=QP+(I-Q)(I-P)

maps ran(P) to ran(Q), belongs to SO(6n), and satisfies
`||U0-I||<=2||P-Q||<=4 eta`. Indeed
`N-I=(Q-P)(2P-I)` and `N^T N=I-(P-Q)^2`; the latter has smallest
eigenvalue at least 3/4, giving the stated bound on the polar factor.
Put C=Y^T U0 X. It is orthogonal and `||C-I||<=5 eta<2`, so det(C)=1.
Then

    U1=Y C^T Y^T+I-Q,  U=U1 U0

are special orthogonal, UX=Y, and `||U-I||<=9 eta`. For any completion
O of R, take O'=O U^T. It completes R' and differs from O by at most
9 eta. This is an existence/comparison gauge, not advice required by a
learner; any completion of the same rows implements the same channel.

Actual `gaussian_channel_selection/flo_learning.txt`, Proposition 2.6,
bounds half diamond norm of m-mode FLO unitary channels by
`m ||O-O'||op`. Here m=3n. Fixed environment preparation and discard
contract diamond norm, hence the RAW diamond norm is at most
`54 n eta`. Combining (1), for alpha+beta<=1/144 this is bounded by
`200 n sqrt(alpha+beta)`. For larger error the trivial raw bound two
already suffices. Thus uniformly,

    ||G_(A,B)-G_(A',B')||diamond
       <=min{2, 200 n sqrt(||A-A'||op+||B-B'||op)}.         (2)

This includes arbitrary ancillas and odd input coherences. The proof
neither converts normalized Choi trace distance by a dimension factor
nor assumes a spectral gap. Matrix square roots and orthogonal
completions have polynomial finite-precision cost; choosing output
accuracy inverse-polynomial in n and the target channel error pays the
Holder loss. A learned parameter pair still must be made physical.

## 4. Exact constant-mode marginal for all core operators

Let Psi be the standard Gaussian state channel from an m<=2 mode core
to the reference-first RS system. Its reference marginal has parameters
L_R,Z_R. If the target core mixture sigma has zero reference covariance,

    Z_R=-L_R Gamma_sigma L_R^T.

Thus both im(L_R) and the support of Z_R lie in a real space of dimension
at most 2m<=4. A reference-only Gaussian rotation aligns this space with
the first at most two reference modes, padding its dimension to an even
one if necessary. The parameters then have the form
`L_R=[L_H;0]`, `Z_R=Z_H direct_sum 0`.

This proves the FULL operator identity

    Psi_R(tau)=T(tau) tensor I_rest/D0                    (3)

for every core operator tau, not just Gaussian or even states. To see
this, apply the quasifree adjoint to a distinct-index Majorana monomial.
Any monomial containing a rest-mode index vanishes: that row of L_R
is zero and every noise contraction involving it is zero. On monomials
in the first reference modes the action is exactly T^dagger. This is a
complete operator basis; in ordinary tensor coordinates the Jordan-Wigner
parity factors do not change the vanishing of every nonidentity rest
coefficient. Equation (3) follows. T is CP/TP by marginalization.

## 5. Normalization, transpose and gauge in the CP norm lemma

First work with ORDINARY normalized Choi matrices in reference-first
order. Suppose Psi:M_r -> M_D tensor M_D is CP/TP and its reference
marginal is (3), with D=h D0. Reorder the program reference P and the
channel reference R as the joint input. The positive matrix

    C_Lambda=r D J_standard(Psi)

is the UNNORMALIZED Choi matrix of a CP map Lambda. Linking program tau
and channel input rho gives Phi_tau(rho), where
`J_standard(Phi_tau)=Psi(tau)`. There is no unintended program transpose:
`Tr(tau^T |i><j|)=tau_ij`. The effect operator is

    Lambda^dagger(I)
      =(Tr_output C_Lambda)^T
      =(r h J_standard(T) tensor I_D0)^T.                (4)

The transpose is on the FULL joint input, not a partial transpose.
It preserves positivity and operator norm. As J(T) is positive of trace
one, `||Lambda||diamond=||Lambda^dagger(I)||op<=r h`. Therefore

    ||Phi_tau-Phi_sigma||diamond<=r h ||tau-sigma||1.      (5)

The target Phi_tau is TP exactly when `T(tau)=I_h/h`; its CP property
follows for every positive tau. These are ordinary full-channel statements.

For the actual Gaussian gauges, do not apply the above reshuffling to
the raw Gaussian matrix without correction. With Gaussian J_G(Psi) in
the order P,R,O, the desired ordinary C_Lambda is

    r D Ad(V_P tensor V_R)[J_G(Psi)].

The Gaussian CP map Lambda_G whose combined-reference Gaussian Choi
matrix is the raw J_G(Psi) instead has ordinary Choi correction
`V_(P,R)=V_P V_R W_PR`, where
`W_PR=product_{i in P,j in R} CZ_ij`. Since these real diagonal gates
commute and square to identity, the desired map is

    Lambda=Lambda_G composed_with Ad(W_PR).

This explicit program/input cross gate is essential. It costs O(m n)
gates, and the reference-only V_R costs O(n^2); neither changes the norm
bound. A separate reference rotation likewise only conjugates the
input effect and does not change its norm. In particular the raw
Gaussian matrix is not automatically the ordinary Choi of the desired
processor.

Equations (3)--(5) settle the exact norm/marginal issue, not compilation.
Reshuffling a large Choi matrix does not supply an efficient circuit.
A CP implementation with constant heralded success cannot be retried
after consuming the unknown channel input. A deterministic CPTP endpoint,
the stable noisy core constraint, and the full mixture error ledger remain
separate open obligations. No complete channel learner or quantum
execution is established by this review.
