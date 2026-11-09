# Physical constant-core Gaussian CP processor

2026-11-07. CLOSED for the exact interface and the near-TP/finite-precision
addendum below. Read STATE/TRAPS,
GAUSSIAN_CHANNEL_MIXTURE_ADMISSION.md, the source/convention review, and the
actual Gaussian Schmidt/purification passages in gaussian_channels.txt.
No network, API, implementation or finite control was used in this review.

**Disposition:** the proposed physical processor is valid with the explicit
ordering correction and coherent amplification given here. This closes the
constant-success-postselection endpoint for a KNOWN exact Gaussian state map
and a KNOWN exactly feasible constant-size program. It does not close the
mixture-channel learner or noisy rank selection. The later addendum separately
closes near-TP repair and finite-precision implementation under their stated
structural hypotheses; it does not supply generic Choi-to-diamond conversion.

## Exact interface and Choi convention

Let P have a modes and dimension r=2^a, R have n modes and dimension D=2^n,
and O be the output. Let Psi:P->R,O be a known ordinary-qubit Gaussian CPTP
state map, using the reference-first convention of the source review. After
a known reference Gaussian rotation, suppose on ALL program operators

    Psi_R(tau) = T(tau) tensor I_B/D0,
    R=A,B, dim A=h=2^b, D=h*D0,

where a,b are constants. The all-operator statement, rather than an equality
only on even Gaussian test inputs, is an assumption of this interface.
For a known density matrix tau on P satisfying T(tau)=I_A/h, define Phi_tau
by its corrected Choi state Psi(tau). Its ordinary normalized Choi state is
Ad_(V_R) Psi(tau), where

    V_X = product_(j<k in X) CZ_jk.

The native full-qubit input can be entangled with an arbitrary inaccessible
reference. The output construction uses only known gates and a known program;
it never accesses an inverse or controlled version of the unknown source channel.

Let G=J_G(Psi) be the normalized corrected Choi state in P,R,O order. Thus
G=Ad_(V_P) J_std(Psi). The desired ordinary CP processor Lambda:P,R->O has
UNNORMALIZED ordinary Choi matrix

    C(Lambda) = r*D * Ad_(V_P V_R) G.

The r*D factor is essential. Applying the ordinary link formula to a program
tau gives Lambda(tau tensor rho)=Phi_tau(rho), with tau itself, not tau^T.
The transpose appearing in the Choi contraction cancels the matrix-unit
transpose in the input reference; it is not a required physical transpose.

Define Lambda_G by taking G as its normalized corrected Choi operator for the
JOINT input I=P,R. Its ordinary Choi matrix is r*D*Ad_(V_I)G. Since

    V_I = V_P V_R W_PR,
    W_PR = (-1)^(N_P N_R) = product_(j in P,k in R) CZ_jk,

and W_PR is real, symmetric and self-inverse, ordinary Choi precomposition gives

    Lambda = Lambda_G composed with Ad_(W_PR).

The correction acts on the actual program and channel input BEFORE Lambda_G.
It is not an output correction. It costs a*n=O(n) CZ gates for fixed a.
The known reference rotation can likewise be transferred to a known physical
input rotation using the corrected-Choi transpose rule; it supplies no advice.

## Effect support and Gaussian compilation

The ordinary effect of Lambda_G is

    E_G = r*D * ( V_I (Tr_O G) V_I )^T.

The apparent non-Gaussian V_I is harmless for this EVEN operator, but this
needs a proof. For S=diag(1,i), V_M differs from S^tensor M by the scalar 1
on the even sector and -i on the odd sector. Therefore conjugation by V_M
on any parity-commuting operator equals conjugation by the Gaussian phase
S^tensor M. It also sends an even Gaussian unitary to a Gaussian unitary.
Full transposition preserves Gaussian operators: on a quadratic Majorana
expression it only changes the known signs and order of the Majoranas.
Consequently E_G is Gaussian. This argument would NOT justify replacing V
by S when acting on an arbitrary parity-coherent input vector; W_PR above
must still be physically implemented.

Before the V/transpose correction, Tr_O G is a Gaussian density matrix on
P,A tensor I_B/D0. Its covariance support has at most 2(a+b) dimensions.
The known corrections preserve this constant-mode structure up to a known
Gaussian input rotation. In particular, for c<=a+b, some known Gaussian
input unitary diagonalizes the effect as

    E_G = 2^c U_in^dagger (sigma_c tensor I_bulk) U_in,

with sigma_c a normalized c-mode Gaussian state. Thus

    0 <= E_G <= C*I,     C=r*h=2^(a+b).

Equivalently, Lambda_G/C is trace-nonincreasing, as is Lambda/C. This bound
also follows from the constant-size Choi matrix of T. No factor D survives.

Here is a physical compilation, not an appeal to efficient preparation of a
Choi state followed by exponentially unlikely Bell measurement. Purify the
known Gaussian G using O(n) Gaussian environment modes, putting input I first
and output plus environment last. Apply the Gaussian Schmidt decomposition
(the actual source Eq2). All bulk input one-mode marginals are I/2, hence
their Schmidt occupancies are exactly 1/2. The remaining c input modes have
occupancies mu_j in [0,1]. In Schmidt coordinates the scaled Stinespring
operator for Lambda_G/C is, up to known Gaussian input/output unitaries,

    sqrt(2^c/C) *
    [ tensor_(j=1)^c diag(sqrt(1-mu_j),sqrt(mu_j)) ]
    tensor I_bulk,

followed by a Gaussian isometry into output plus environment. This includes
occupancies 0 or 1 and requires no inverse of a filter eigenvalue. Additional
pure output modes and, if necessary, parity-balancing/padding modes are known
ancillas. The reference Schmidt unitary transfers to the physical input as
the transpose of its conjugate by V_I; the preceding even-unitary observation
proves that this is again Gaussian.

Compile the constant-size diagonal contraction by a constant-size unitary
dilation with a success flag; its complementary failure block is included.
Compile the Gaussian rotations/isometry with polynomially many ordinary qubit
gates. This gives a known UNITARY dilation U_G of the entire heralded processor,
including failure, rather than merely successful Kraus operators. U_G^dagger
is available by reversing this learned/known circuit. The environment is kept
coherent until the final output channel is formed.

The construction uses matrices of O(n) dimension and constant-size filters.
It does not form a 2^n-by-2^n Choi matrix. One may first diagonalize the CONSTANT
effect block. In a Gaussian purification the bulk cross-covariance columns are
orthonormal, so their output Schmidt partners require no division by small
bulk singular values. The final addendum below pays finite-precision compilation
by cutting off tiny core links, without exact-zero decisions or inverses of
arbitrarily small links. It does not identify this exact structural core from
noisy native data.

## Exact feasibility pays coherent, input-independent amplification

Prepare a purification of the known constant-size tau as part of the circuit,
apply W_PR, and run the preceding dilation for Lambda_G/C. Retain the program
purifier and all channel environment registers. Let K be the successful
Stinespring block from the actual unknown R input to O plus all retained work.
The exact feasibility equation T(tau)=I_A/h gives

    K^dagger K = I_R/C.

This operator equality, not an average success probability on a maximally
mixed input, is the necessary amplification hypothesis. It holds after
tensoring with every external reference. The preparation of tau is known
and reversible because tau is constant-dimensional classical output.

For completeness, exact ideal amplification needs no unproved generic channel
inverse. Put theta=arcsin(1/sqrt C) and

    j = ceil(pi/(4 theta)-1/2),
    theta' = pi/(4j+2) <= theta,
    beta = sin(theta')/sin(theta) <= 1.

Add an independent known coin of success amplitude beta, and define success
as the original filter success AND the coin success. The new successful block
has squared singular value sin(theta')^2 times I_R. With U the COMPLETE known
unitary including program and coin preparations, reflection about the initial
zero-work subspace and reflection about the success flags give the usual
two-dimensional Grover rotation for every input vector, with the SAME angle.
After j rotations the angle is (2j+1)*theta'=pi/2, so success is deterministic
and the successful Stinespring isometry is exactly sqrt(C)*K, up to one common
global phase. The complementary bad vectors are orthonormal across input
vectors because K^dagger K is scalar. Thus the rotation proof is linear and
holds for entangled inputs, rather than just basis states.

The circuit uses O(sqrt C) calls to U and U^dagger. Initial-zero reflections
include all program, purification, filter and environment work; they require
only O(n) ordinary reversible gates. The success reflection checks the flags,
not the unknown input or environment. No trial consumes an input and then
requests that input again. There are no calls to the inverse of the native
unknown channel. Gaussian-only or parity-superselected output gates are not
being promised: W, flag reflections and amplification are ordinary qubit gates.

Exactness here is in the ideal computable-gate model. Over a finite universal
gate set, approximate all known rotations to a chosen operator-norm budget.
Telescoping the polynomial circuit gives the requested Stinespring error and
hence diamond error, with polynomial synthesis cost. Discarding the final work
and flags ALWAYS gives a CPTP channel; one does not postselect the small residual
failure or claim exact finite-gate synthesis of arbitrary irrational angles.

## Scope of closure

The exact constant-core physical processor is a paid constructive operation.
The ordinary-qubit convention, r*D normalization, Gaussian bulk isometry,
constant-size filtering and input-independent amplification all have explicit
roles. Gaussianity alone without the constant effect support would not give
the same filter norm bound or constant amplification cost.

Remaining gates belong to the learner, not this exact processor: obtaining an
exactly CP/TP model and feasible program from noisy moments; a stable low-rank
reduction and all conditioning bounds; and a full diamond-error ledger linking
that model to the unknown channel. If feasibility is merely approximate then
K^dagger K need not be scalar, and the exact amplification argument above
cannot simply be reused. No end-to-end learner, novelty or separation follows
from this review alone.

## Final addendum: near-TP normalization and finite compilation

This addendum closes the proposed NEAR-TP physical repair. It supersedes the
need to solve T(tau)=I/h exactly for the learned program. The structural model
Psi itself is still an exact known Gaussian CPTP map with the displayed
constant-reference marginal form, obtained in the parent argument from its
projected RR-zero mean. This review does not infer that structural identity
from a merely small numerical residual.

Let sigma be an unknown feasible target program, let tau be a known even
positive density matrix, and suppose ||tau-sigma||_1<=delta. Put C=r*h<=64,
t=C*delta<=1/2, and F=Phi_tau^dagger(I). The earlier CP processor norm bound gives

    ||Phi_tau-Phi_sigma||_diamond <= t,
    ||F-I|| <= t,             (1/2)I <= F <= (3/2)I.

After the known corrected-reference rotation/transpose, F is the constant
h-dimensional matrix h*T(tau)^T tensor the bulk identity. Because tau and
T(tau) are even, the parity-sector observation above removes any apparent
bulk dependence of V_R in this EFFECT conjugation. All needed conjugating
gates are known and polynomial-size; no unknown channel input is measured.

Define B=F^(-1/2) and Q=Phi_tau composed with Ad_B. Then

    Q^dagger(I)=B F B=I.

Thus Q is exactly CPTP. Functional calculus on [1/2,3/2] gives ||B||<=sqrt2
and ||B-I||<=t, since

    |lambda^(-1/2)-1|/|lambda-1|
       =1/[sqrt(lambda)*(1+sqrt(lambda))] <= 1.

Consequently ||Ad_B-Id||_diamond<=(sqrt2+1)*t and

    ||Q-Phi_sigma||_diamond
       <= t+(1+t)*(sqrt2+1)*t < 5*t <= 10*C*delta.

This is a full-input diamond estimate. It does not multiply normalized Choi
trace distance by D. B is computed only on a CONSTANT block whose eigenvalues
are uniformly bounded away from zero. A matrix inverse square-root iteration
or polynomial approximation on that fixed interval needs no eigenvector gap.
The contraction B/sqrt2 has a constant-block unitary dilation, for example the
usual two-by-two block completion using sqrt(I-B^2/2). The latter square root
is continuous at zero; no inverse of that square root is required.

Coherently apply this filter FIRST to the actual unknown input, then prepare
the program and apply Lambda/C with its ordering correction. The combined
successful Stinespring block K now obeys

    K^dagger K = I/(2*C).

The exact amplification construction therefore applies with success probability
1/(2C), even though tau was not feasible before normalization. There is no
ill-conditioned feasibility SDP and no consumed-input retry. Actual finite-gate
implementation is an approximation to this ideal Q; unitary execution followed
by discarding work remains exactly CPTP.

### Tiny-link cutoff without a full-Choi error conversion

The remaining compilation issue is not solved by demanding exact tests on
arbitrary computable irrational parameters. The following direct Schmidt
cutoff supplies a quantitative alternative. Let c<=log2 C be the number of
possibly nonmaximally mixed INPUT modes of the Gaussian CP processor. In the
Gaussian purification's Schmidt form, write their occupancies as mu_j and
their cross-link sizes as s_j=2*sqrt(mu_j*(1-mu_j)). All bulk links equal 1.
Choose a tolerance zeta<1/4. Retain links above the tolerance and replace a
discarded occupancy by its nearer endpoint 0 or 1. With interval/approximate
thresholding, use an overlap band: every retained link is at least zeta/2
and every discarded link is at most 2*zeta. No equality-at-threshold or
exact-zero question must be decided.

This replacement has a DIRECT Stinespring operator bound. In the original
abstract Schmidt frame, a discarded diagonal factor
diag(sqrt(1-mu),sqrt(mu)) changes in operator norm by at most s<=2*zeta.
There are at most c such factors, all factors are contractions, and the
overall scalar sqrt(2^c/C) is at most 1. The scaled processor Stinespring
therefore changes by at most 2*c*zeta. This compares operators on arbitrary
inputs; it never derives channel error from normalized full-Choi trace error.

The truncated processor can be computed without finding the discarded Schmidt
directions. For a pure covariance with input block A and cross block X,
XX^T=I+A^2. Once the constant input block is diagonalized, bulk cross rows are
orthonormal and retained core rows can be normalized with inverse at most
2/zeta. They determine the retained output partners. On the orthogonal output
complement, the remaining covariance has singular values at least
sqrt(1-4*zeta^2): its only nonpure Schmidt modes correspond to discarded links.
Replace it by its polar complex structure, preparing the resulting pure
Gaussian state. That polar inverse is uniformly conditioned. In the original
Schmidt frame this performs exactly the endpoint replacement just bounded.
No normalization of a discarded link is needed.

All matrices have O(n) dimension. Orthonormal completion of the retained frame,
the uniformly conditioned residual polar operation, and Gaussian gate synthesis
are polynomial operations. Approximate constant-block diagonalization can be
done with its residual controlled directly, rather than requiring separated
eigenvectors. Retained-row normalization loses only polynomial factors in
1/zeta; residual polar normalization has a fixed lower spectral bound. Hence
the known matrices need only polynomially small absolute errors, computable
at polynomial bit precision in the learned finite-description model. This
assumes their numerical evaluation is paid; it is not a claim about arbitrary
unrestricted real-number oracles. Very small occupancies are deliberately
discarded, rather than resolved with precision set by their unknown size.

### Amplification is robust to an unrelated failure completion

Only the successful Stinespring blocks, not entire completed dilations, were
compared by that cutoff. A telescoping bound between arbitrary full U and U'
would therefore be unjustified. Use the singular-value two-plane proof instead.
Let the exact normalized target block be K0=sqrt(p)*V with V an isometry and
p=1/(2C). Suppose the constructed block K' satisfies ||K'-K0||<=xi<=sqrt(p)/4.
Every singular value s of K' then lies within xi of sqrt(p), and the polar
isometry V' of K' obeys

    ||V'-V|| <= 2*xi/(sqrt(p)-xi) <= 3*xi/sqrt(p).

Use the SAME known coin and number j of Grover iterations prescribed for p.
For each singular vector the actual angle is arcsin(beta*s), within 2*xi of
the intended theta'. Here j>=1, beta*sqrt(p)=sin(theta')<=1/2, so the derivative
bound is uniform. With k=2j+1<=4/sqrt(p), the final bad amplitude is at most
2*k*xi; the good amplitude differs from 1 by at most the same conservative
bound. Including the polar-isometry error gives a total Stinespring error
at most 19*xi/sqrt(p), and therefore diamond error at most
38*xi/sqrt(p). These loose constants are harmless since C<=64.

This argument holds for ANY unitary completion of K': the two-plane dynamics
depend on its singular values and polar isometry, not on a chosen failure
channel. A subsequent approximation of the specific compiled completion can
be bounded by ordinary circuit telescoping. Reserving a polynomially small
cutoff and gate-error budget, such as the parent's u^1000 allocation, pays
both effects. No exact-zero/PIT oracle, inverse tiny Schmidt link, environment
access to the unknown source, or full-dilation continuity assumption remains.

**Updated disposition:** the constant-core near-TP physical repair is closed
under the stated structural model and program-error bound. The complete native
learner still needs its independent proof that those hypotheses and numerical
budgets follow from noisy ordinary channel uses.
