# 2026-11-13 — Independent composition of the native Macdonald transform

**Admitted scoped theorem.** For numerical D, the fixed parameters
t=D/(D+1), q=t^3, used at EVERY degree stage, admit a clean shape-to-integral-
Macdonald transform in poly(D,log(1/epsilon)) classical BIT, gates and workspace.
The error is a restricted operator norm, including all workspace and an arbitrary
reference. No table over partitions, eigenvector oracle, postselection, or unknown
overlap is supplied. This is a written construction, not an implementation,
novelty claim, useful-speedup claim, or unrestricted classical-sampling lower bound.

The decisive simplification is exact marker nilpotence: the native creation
exponential is a polynomial of degree D, so its real-arithmetic block is EXACT.
There is no need to compare arbitrary dilations of nearby block operators.
Rectangular polar bookkeeping, private markers in its powers, coherent content
readout, and the final finite-gate compilation are essential qualifications.

Read: STATE/TRAPS; MACDONALD_NATIVE_TRANSFORM; actual mickler_2026.txt Sections
2–4 through Corollary 4.9 (physical lines 105–1151); the complete prior
jack-logprecision-independent review and the overlap review's interlacing proof.
No network, API, Git, implementation, or finite sweep was used. Only this review
was edited. The source's generic-parameter proofs are not silently specialized.

## 1. Generic identities really extend to q=t^3

Write w=z^-1, N=D+1, and H_lambda=||J_lambda||^2. The source metric is

    ||w^ell p_mu||^2 = q^ell z_mu product_k r_k^m_k,
    r_k=(1-q^k)/(1-t^k)=1+t^k+t^(2k) in [1,3].

It is positive for 0<q,t<1. Macdonald polynomials are regular there: perform
orthogonal triangular elimination in any total extension of dominance order.
The relevant Gram determinants are positive; the integral-form hook factors
are nonzero. This proves local analytic dependence without invoking a generic
eigenvalue denominator. L=Qcal^dagger D_(t/q) Qcal is likewise analytic in each
finite degree sector and is self-adjoint for this positive metric.

In corner coordinates (I_k,L_k) from the actual source, addable corners are
(I_k,L_(k+1)) and shifted removable corners are (I_k,L_k). Along this boundary
i increases and j decreases. Thus t^i q^-j strictly decreases; the two corner
families strictly interlace for EVERY 0<q,t<1. In particular:

* distinct addable corners of ONE partition never collide;
* an addable and a shifted-removable corner of that partition never collide;
* every hook in Lemma 3.15 is positive and its tau is positive.

Define the UNHATTED eigenvector by the source Proposition 3.13 formula

    Psi_(lambda,s) = tau_(lambda,s)^-1
       product_(a in A_lambda, a!=s) (L-[a])/([s]-[a]) J_lambda.       (1)

All denominators are nonzero throughout this positive domain. The generic
identities for (1) therefore extend by analytic continuity. In particular

    L Psi=[s] Psi,  pi0 Psi=J_lambda,
    J_lambda=sum_s tau_(lambda,s) Psi_(lambda,s),
    ||Psi_(lambda,s)||^2=H_lambda/tau_(lambda,s).

Cyclic spaces Z_lambda are mutually orthogonal by the transfer-operator
identity and self-adjointness, exactly as in Proposition 3.13. Their eigenvectors
are orthogonal and nonzero. The source's dimension count then gives a complete
basis, even when different cyclic spaces have the SAME eigenvalue.

The unhatted right-hand side of Proposition 4.8 is also regular: its only new
denominators are [a]-[s^+] within lambda+s, covered by strict interlacing.
Consequently its generic identity extends, giving

    w Psi_(lambda,s)=q^-j phi_(lambda+s,s),
    Q phi_(mu,r)=J_mu,
    Q w Psi_(lambda,s)=q^-j J_(lambda+s),                         (2)

where j is the column of s and Q=pi0 Q(z) on positive markers. The scalar is
POSITIVE. This does not rerun the source's generic projection argument at a
collision. It extends a regular vector identity already proved generically.

The hatted basis in Definition 4.6 is NOT admitted at this specialization:
varpi and/or [s]-1 can vanish. No hatted vector, varpi division, or full-space
resolvent at a collided eigenvalue is used. Likewise Corollary 4.9 is regular
in its unhatted form; it is not needed as an additional algorithmic primitive.

## 2. Exact creation, normalization, and positive common paths

Let H_d be the full marker/Fock space of total degree d. The isometry
I:H_(n-1)->w H_(n-1) is multiplication by w/sqrt(q). Put A=Q I. Then

    A Psi_(lambda,s)=q^(-j-1/2) J_(lambda+s).                    (3)

The block form of L gives AA^dagger=Q Q^dagger=T_2-I on Fock degree n.
Expanding the ACTUAL transfer function (Proposition 3.7) through u^-2 gives

    (T_2-I)J_mu=chi_mu J_mu,
    chi_mu=(1-t)(q^-1-1) sum_(box in mu) [box].                  (4)

For every box at every n<=D, 1/4<[box]<21: t^D>=e^-1>1/4 and
t^(-3D)<=e^3<21. Also

    3 <= N(q^-1-1) = 3+6/D+4/D^2+1/D^3 <=14.

Hence, for n>=1,

    3n/(4N^2) <= chi_mu < 300n/N^2.                            (5)

Using 27 instead of 21 in the preceding box bound would only yield 378 by
this particular multiplication; the displayed 300 bound uses e^3<21.

The canonical rectangular polar isometry is

    V=A^dagger(AA^dagger)^(-1/2): Fock_n -> H_(n-1).

Completeness and orthogonality of the Psi basis, together with (3), imply

    V Jhat_mu = sum_(r in R_mu) sqrt(p_(mu,r)) Psihat_(mu-r,r),
    p_(mu,r)=q^(-2j(r)-1) tau_(mu-r,r) H_mu/(chi_mu H_(mu-r)).   (6)

There is no additional component in a globally degenerate eigenspace: pairing
against the COMPLETE orthogonal Psi basis proves (6). All amplitudes are positive
and their squares sum to one because V is an isometry. Individual p values need
not have an inverse-polynomial lower bound for this construction.

For the second polar step, Lemma 3.15 and

    (1-t^a)/(1-t^(a+r)) >= a/(a+r)       (a,r positive integers)

give tau_Mac>=q^j tau_Jack(alpha=3). This follows, for example, because
(1-e^-x)/x is decreasing. The row hook increment is 3 and the column hook
increment is 1; thus the product comparison is EXACTLY the Jack hook product,
not a product of independently weakened constant factors. The checked Jack
interlacing/area proof gives tau_Jack>=3/(16d) for d=|lambda|>0. Since
q^j>=t^(3D)>=e^-3>1/27,

    tau_Mac>=1/(144d) for d>0;  tau_empty=1.                   (7)

Fix a_H=1/(256N), safely below every required tau.

Let P_k be the full spectral projector for L_(n-1) with content t^k, and P0
the marker-zero projector. On each needed cyclic Jordan plane,

    W_k=(2P0-I)(2P_k-I),   cos(theta)=sqrt(tau),

has phases +/-2theta. Its principal square root sends Psihat_(lambda,s) to
Jhat_lambda with positive phase. The tau=1 line is the identity. Orthogonal
cyclic spaces make the statement uniform despite global degeneracies. No
lambda or tau register is supplied to this operation.

Thus a Fock-side down map B_n applies V, records k=i-3j coherently, then applies
this square root. A shape-side C_n prepares the probabilities (6) and maps
(mu,r) reversibly to (mu-r,k(r)). Given the parent shape and k there is at most
one addable corner, so the old shape and row index can be erased reversibly.
Both maps have the SAME positive amplitudes. At the vacuum their complete
removal-path states agree. After the fixed vacuum recoding,

    B_down^dagger C_down |lambda> = |Jhat_lambda>               (8)

with every path register erased. Global q,t must stay fixed for this identity.

## 3. An exact native block, using finite nilpotence

On normalized occupation/marker coordinates,

    C=sum_(k=1)^D w_k a_k^dagger T_(-k),
    w_k=sqrt((1-t^k)(1-q^k)/(k q^k)).

The elementary estimates 1-t^k<=k/N, 1-t^(3k)<=3k/N and
q^-k<=e^3 show w_k<=16 sqrt(k)/N. Set gamma_k=N w_k/sqrt(k)<=16.

Here is an actual block for C^dagger, with D global at EVERY stage. On a valid
occupation/marker input of total degree n<=D, prepare k with amplitude
sqrt(k m_k/D). The remaining mass is [D-(n-ell)]/D, on a separate failure
label. Rotate by gamma_k/16, subtract one from m_k, and increase ell by k.
Keep k, then project it onto a fixed uniform M-label state, D<=M<2D.
The successful block is

    N C^dagger/(16 sqrt(D M)).

The distribution preparation and final uniform projection are DIFFERENT
unitaries; no input-dependent preparation is incorrectly uncomputed after
changing the occupation. The labelled shift is an injective reversible integer
translation on its successful domain and has a padded permutation extension.
All arithmetic scratch is cleaned before the occupation changes. Invalid
encodings have specified safe branches. These are blocks, not postselections.
The normalization is <=32; a known additional attenuation gives C^dagger/32.
Reversing this unitary gives C/32.

Every term of C lowers the nonnegative marker by at least one. Consequently
C^(D+1)=0 on every valid degree sector. Monotone truncation also implies

    Qcal=pi_(ell>=0) Q(z) = exp(C) = sum_(j=0)^D C^j/j!.        (9)

Indeed any intermediate negative marker can never return to a nonnegative
one, so truncating after each multiplication agrees with truncating the whole
commutative creation series. Equation (9) is an EXACT finite sum, not an
accuracy-dependent Taylor approximation.

Take G=2^48>exp(32). A compact LCU with weights 32^j/(G j!), fresh block
signals for the D factors, and remaining weight split equally between I and
-I has block Qcal/G exactly in real arithmetic. It has O(D) C-block calls;
it does not enumerate words or partitions. Its factorial weights have
O(D log(D+1)) bits. The marker is LOGICAL within these powers of C.

D_(t/q) has entries t^(-2ell)<8. Therefore fresh product signals give exact
real-arithmetic blocks of

    L/Gamma,   Gamma=8G^2,
    A/G and A^dagger/G,

using the diagonal block D_(t/q)/8, the Qcal block and its adjoint, and marker
projections/reindexing. All selectors, weights, diagonal factors and marker
updates are explicit native arithmetic. Normalizations are absolute constants.

## 4. Rectangular polar compiler: the necessary private markers

Put B=A^dagger/G. Its input is Fock_n and output is H_(n-1). From (5), the
squared singular values lie in [a_A,1], with the safe choice

    a_A=1/(16G^2 N^2).

Let U_B be its exact block unitary, P its INPUT projector and Q its OUTPUT
projector, so Q U_B P=B under the stated embeddings. These projectors are
different: the output marker is retained and may be nonzero. A degree/tag
register gives a reversible common ambient embedding if needed.

The contraction R=I-B^dagger B on Fock_n has normalization ONE, by

    R = P U_B^dagger (I-Q) U_B P.                              (10)

Implement I-Q as an exact flag projector and use the SAME U_B banks for its
actual inverse. Crucially each occurrence of R has a PRIVATE zero-initialized
marker and private block flags. Its logical system is only the Fock occupation.
Projecting that private marker back to zero enforces P at the factor boundary.
Any degree/tag part of P is also inserted by an exact flag test at both
boundaries; it is not inferred from an uncontrolled dilation's failure space.
Later R occurrences do not touch earlier private markers, so their all-zero
block really is R^j. A leaked marker cannot disappear in a later factor.
Reusing one logical marker without these compressions would not prove R^j.

For b_j=binom(2j,j)/4^j, define

    q_K(x)=sum_(j=0)^K b_j(1-x)^j,
    F_K=B q_K(B^dagger B),  s_K=sum_(j=0)^K b_j<=K+1.

A compact selector over j and K separate R blocks gives F_K/s_K. The FINAL
B has a distinct retained output marker. The input/output projectors of this
whole block test all OTHER signal banks zero; only the output projector permits
the retained output marker to vary. This is a rectangular block throughout.

For every squared singular value x>=a_A,

    t_K(x)=sqrt(x)q_K(x) in [0,1],
    1-t_K(x)<=exp(-a_A(K+1))/a_A.                              (11)

Dilute by s_K sin(theta_*), where m=4(K+1) and theta_*=pi/(4m+2).
This factor is <pi/16<1. If U is the diluted block, use rectangular OAA

    (-U(I-2P)U^dagger(I-2Q))^m U.                             (12)

On each singular pair its clean amplitude is the desired polar direction
times sin((2m+1)arcsin(t_K sin(theta_*))). If 1-t_K<=delta, the full clean
vector error is <=pi delta<4delta, including rejected signals. This follows
from 2(1-cos(Delta)) for the squared error, with
Delta<=(2m+1)tan(theta_*)delta<=pi delta. SVD orthogonality makes it an
operator bound, without an input-count factor. At most 32(K+1)^2 native
B/B^dagger calls suffice. Every occurrence of U^dagger in (12) uses the same
banks and reversed word; fresh banks are for DIFFERENT factors in powers.

For the half phase of W_k the prior compiler applies unchanged: set
H=(2I+W_k+W_k^dagger)/4 and use (I+W_k)q_K(H)/2. The normalization-one
block of I-H is the uniform selector I,I,-W_k,-W_k^dagger. Its binomial
defect obeys (11) with a_H; the same known-angle OAA gives full clean error
<4delta with <=32(K+1)^2 W/W^dagger calls. No unknown overlap enters OAA.

## 5. Clean noninteger content readout at logarithmic error cost

All possible contents are t^k, -3D<=k<=D. They lie in [1/4,21] and distinct
adjacent values differ by at least 1/(4N). Use phase estimation for
exp(2pi i L/64), with M=2^ceil(log2(2^16 N)) phase labels. A QPE output
within 1/(1024N) of the true phase has the correct nearest k. The standard
QPE probability formula and sin(pi x)>=2|x| give outside this interval a
tail <1/16, since M/(1024N)>=64. Exact rational comparisons with t^k/64
compute the nearest k in polynomial bits. There is no wrap-around ambiguity.

Repeat this CONSTANT-success experiment R_e times in coherent separate banks,
compute the majority nearest label, copy only that label, then reverse all
QPE and temporary-label computations. If p_wrong is the majority failure
probability, the clean-vector error is <=2 sqrt(p_wrong). This follows by
comparing the copied-label state BEFORE the common inverse; the squared norm
is 2 p_wrong. It is not an assertion that inverse QPE erases an arbitrary
measurement record exactly. Hoeffding gives p_wrong<=exp(-R_e/8), so
R_e=O(log(1/eta)) gives clean error eta. Eigenspaces are orthogonal, hence
the same bound holds uniformly on superpositions and references.
Using XOR to copy the majority gives the same 2 sqrt(p_wrong) bound for an
arbitrary initial logical label, by bounding each wrong-label XOR difference
by 2. Thus a full logical extraction unitary is available when needed.

Controlled evolution times in one QPE are 2pi 2^j/64, with total O(M)=O(N).
They are NOT all constant times as in the integer Jack case. Nevertheless
the exact native block of L pays them: with Gamma above, R_s=ceil(64 Gamma M)
segments suffice for every needed time. A compact Taylor LCU in a segment,
padded to normalization 2 and followed by cubic OAA, has full clean error
<=sqrt(30 beta) when its half-unitary block error is beta. Taking

    J_s=ceil(log2(2^14 R_s^2/rho^2))

Taylor terms gives whole-simulation error <=rho, with every signal retained.
This is the previously checked direct Taylor/OAA proof, applied to the EXACT
Hermitian L block. All inverse calls reverse the same banks and gate word.

Content reflection is extraction, the exact equality phase, and actual inverse
extraction. An eta-accurate extractor gives a 2eta-accurate reflection on the
WHOLE degree sector, for every retained logical k. Its temporary label bank
is distinct from the retained outer content label. This full logical guarantee
is what permits its use inside the half-phase compiler and its inverses.

## 6. One noncircular finite-bit allocation

For 0<epsilon<1/2 choose these quantities IN ORDER:

    zeta=epsilon/(256N),  delta=zeta/64,
    K_X=ceil(a_X^-1 (1+ceil(log2(1/(a_X delta)))))  (X=A,H),
    Q_X=32(K_X+1)^2,
    eta=zeta/[64(Q_H+1)].

Use the exact degree-D creation LCU. The V compiler contributes <4delta;
the ideal half-phase compiler contributes <4delta. Replacing its W calls by
the content-reflection circuits contributes <=2Q_H eta, and the outer
content extraction contributes <=eta. Their sum is <zeta/2 per B_n.

For each extractor set

    R_e=2 ceil(32 log2(64/eta))+1,
    ell=log2 M,  J_e=2 R_e ell,
    rho=eta/[32(J_e+1)].

The majority error is <eta/4. There are J_e controlled simulations, including
the inverse QPE banks, so their accumulated error is <eta/32. This leaves
ample slack for the claimed eta bound before final gate rounding. Choose
R_s,J_s as in Section 5. All loop lengths are now fixed polynomial functions
of D and log(1/epsilon). Shape-side C_n probabilities are treated at this
intermediate step as their specified exact real rotations.

Unroll this finite circuit, including the actual B_down inverse, and count
a computable upper bound T>=1 on its variable rotations/phases. This is
polynomial: a creation block has O(D) C calls, each using O(D) selector
rotations; the two polar blocks use Q_A and Q_H calls; each extractor has
J_e simulations; each simulation has O(R_s J_s) L-block calls. Selector and
Fourier circuits also have explicit polynomial loop lengths. This count is
made BEFORE setting bottom rotation accuracy, not from an unknown final gate
count or a numerical refinement stopping rule.

Use the prior explicit finite-palette compiler at

    b_0=max(8,ceil(2 log2(2^12 T/epsilon))).

For completeness that compiler writes a real rotation as cI+s(XZ), or a
controlled phase using iI. A uniform b_0-bit seed and reversible comparisons
allocate signed I/XZ (or iI) counts approximating its half block; cancelling
I,-I padding and cubic OAA give full clean error <16*2^(-b_0/2). It uses
only a fixed finite gate palette and exact integer arithmetic. Every inverse
is the reverse of the same compiled word, including controlled scalar signs.
Thus all bottom errors sum to <epsilon/256. No free exact real gate remains.

Coefficient computation is polynomial BIT as well. Powers t^k and q^k for
|k|<=O(D) have O(D log N) bits; hook products contain O(D) such factors.
Consequently H, tau, chi and every branching probability have polynomial bit
length. Prefix probabilities and square roots can be computed with polynomial
extra precision even when a positive probability is small. Creation weights
32^j/(G j!) and binomial weights have polynomial bits in D and K; simulation
weights require only polynomially many bits in J_s, log N and log(1/rho).
Sines, cosines, pi and square roots have elementary polynomial-bit evaluation
on these bounded arguments. Invalid encodings use specified safe branches.

The nested-workspace rule is indispensable: each lower gate approximates its
entire logical unitary on a clean lower bank, INCLUDING arbitrary upper
signals. In the ideal hybrid that lower bank is zero at its occurrence.
Accumulated leakage is bounded unitarily, not discarded. The inverse-on-range
identity ||(T^dagger-U^dagger)U|_S||=||(U-T)|_S|| pays actual inverses.
Private banks for power factors, same banks for actual inverses, and retained
final scratch are all included in this guarantee.

Finally B_down is within D zeta/2 of its ideal on every Fock input. The ideal
C_down range is precisely the ideal B_down range by (8), so the ACTUAL inverse
has the same error there. Adding bottom rounding gives error <epsilon for
B_down^dagger C_down, jointly with all workspace and any reference. No factor
equal to the number of partitions, eigenvectors, or paths occurs. D=0 is the
identity; the stated parameter choice applies to D>=1.

## 7. Scope and rejected shortcuts

The whole native transform is admitted under the numerical-D, fixed-global-
parameter contract. Nothing in the argument grants arbitrary input-state
loading, physical position-space wavefunctions, novelty, classical hardness,
or a useful asymptotic advantage. Rows and columns retain polynomial classical
weighted-cycle samplers. The unrestricted classical comparator remains open.

The following shortcuts would NOT prove this theorem: using the singular
hatted basis; changing q,t between stages; inferring a common path from only
squared overlaps; sharing an uncompressed marker across powers of R; using
one projector for both sides of rectangular OAA; normalization-2 LCU powers
for I-B^dagger B; silently resetting signals; single-QPE inverse-accuracy tails;
or hybridizing arbitrary dilations merely because their top blocks are close.

The last shortcut is avoided here by exact nilpotence. If an alternative
implementation instead truncates Qcal early, it must pay the actual-block
comparison. A useful elementary bound for contractions B,C is

    ||B q_K(B^dagger B)-C q_K(C^dagger C)||
       <=(K+1)^2 ||B-C||,

obtained by telescoping the powers of I-B^dagger B. This is a possible repair,
not an uncharged premise of the exact finite-sum construction above.
