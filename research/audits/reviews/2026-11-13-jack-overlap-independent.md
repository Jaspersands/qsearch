# 2026-11-13 — Jack corner overlaps and exact no-reset clock

ACCEPT the two parent bounds at fixed alpha=3. In fact the elementary boundary
geometry gives tau>=3/(16d) for d>=1 and q>=1/(d+1), as in the completed paid
overlap report. The stronger claims below were checked directly. The exact
alternating-measurement law is also proved, including both failure outcomes.
Assume the separately reviewed all-degree identity A_d psi_(lambda,s)=J_(lambda+s).
No finite-precision circuit, coherent full transform, classical separation,
or Macdonald consequence is claimed here.

Primary source: retained Mickler–Moll `mickler_moll.txt`, physical LF lines
145–153 identify j=J at (epsilon1,epsilon2)=(3,-1); 174–183 define outer
corners and content; Theorem 1.4 (210–256), Lemmas 3.3–3.5 (387–427), and
(2.4) (333–344) give the cyclic spaces and transition residues. Appendix
(A.7), (A.10)–(A.12), Theorem A.5 and (A.25)–(A.32) give compressed spectra
and the normalization of their residues. In particular the source explicitly
distinguishes its UNNORMALIZED compressed function from the cotransition
probability transform (996–1000).

## 1. Contents, signs and the first overlap

For a nonempty partition lambda of size d with m removable corners, write
its outer corners as (X_j,Y_j), where

    0=X_0<X_1<...<X_m,  Y_1>...>Y_m>Y_(m+1)=0.

Its addable corners are (X_i,Y_(i+1)), 0<=i<=m. Put

    a_i=3X_i-Y_(i+1),  b_j=3X_j-Y_j,
    g_j=b_j-a_(j-1)=3(X_j-X_(j-1))>=3,
    h_j=a_j-b_j=Y_j-Y_(j+1)>=1.

Thus a_0<b_1<a_1<...<b_m<a_m. The zeros b_j are the REMOVABLE contents
PLUS TWO, since the source uses R^+=R+(1,1). The content of a removable
box itself is b_j-2. All numbers are integers. The extreme poles are
-height(lambda) and 3 width(lambda), so their distance W is <=4d.
Global content degeneracies across different partitions do not change this
strict within-partition interlacing.

For m_lambda(u)=product_j(u-b_j)/product_i(u-a_i), the source gives

    tau_i=Res_(u=a_i) m_lambda(u)>0,
    sum_i tau_i=1,
    tau_i=||J_lambda||^2/||psi_(lambda,s_i)||^2
         =|<Jhat_lambda,psihat_(lambda,s_i)>|^2.

Thus tau is a probability, not an amplitude. The original parent estimate
already follows by pairing factors on each side of a_i. The left product
is at least 1/(a_i-a_0) when i>0, and the right product is at least
1/(a_m-a_i) when i<m; successive factors telescope and the final positive
integer gap is at least one. An empty endpoint side contributes 1. Hence

    tau_i >= 1/W^2 >= 1/(16d^2).

There is a stronger area estimate. For an interior i define
P_k=3(X_i-X_k), Q_k=Y_(k+1)-Y_(i+1). The left product is
product_(k<i)(P_(k+1)+Q_k)/(P_k+Q_k). Using
(P'+Q)/(P+Q)>=P'/P until its last factor telescopes to

    left >= [g_i h_i/(g_i+h_i)]/(3X_i) >= 1/(4X_i).

On the right, the same argument with vertical differences, using
(P+Q)/(P+Q')>=Q/Q', gives

    right >= [g_(i+1) h_(i+1)/(g_(i+1)+h_(i+1))]/Y_(i+1)
           >= 3/(4Y_(i+1)).

Here gh/(g+h)>=3/4 for g>=3,h>=1. Since the rectangle of width X_i and
height Y_(i+1)+1 lies in lambda, X_i Y_(i+1)<d. Thus interior tau_i is
>=3/(16X_iY_(i+1))>3/(16d). At the two endpoints the nonempty one-sided
bounds are respectively 3/(4Y_1) and 1/(4X_m), also >=3/(16d).
For d=0 there is one addable corner, m_empty(u)=1/u, and tau=1.

These statements use the exact lattice at fixed alpha=3. They do not grant
uniform inverse-polynomial spectral gaps when an arbitrary rational Jack
parameter is supplied only in binary. The measured content in degree d is
always 3x-y, with distinct global values separated by at least one.

## 2. The second overlap: degree d+1 and the minus residue

Put N=d+1 and mu=lambda+s. Euler's identity gives A_d A_d^dagger=3N I.
Let V=A_d^dagger/sqrt(3N), so P_A=VV^dagger is an orthogonal projector.
Under the isometric identification w F[w]_d with F[w]_d,

    L_N = [[0,A_d],[A_d^dagger,L_d+2I]].

Let S_mu be the span of psi_(mu-r,r) over removable r of mu. The global
orthogonal psi basis and A psi=J imply A_d^dagger J_mu lies in S_mu:
its coefficient on every other psi is zero by Jack orthogonality.
Moreover A maps S_mu into C J_mu. Consequently P_A preserves S_mu and
restricts there to the rank-one projector onto v=V Jhat_mu. The removable
contents are distinct, so each relevant content projector of L_d restricts
to a rank-one projector on S_mu.

The block identity shows C J_mu + w S_mu is L_N-invariant and contains
J_mu. Its dimension is |R_mu|+1=|A_mu|=dim Z_mu, hence

    Z_mu=C J_mu orthogonal-sum w S_mu.

The compression of L_N to J_mu^perp in Z_mu is therefore L_d+2 on S_mu.
Its eigenvalues are b_j=c(r_j)+2, the zeros of m_mu. The measured degree-d
content is c(r_j), NOT b_j. Since <J_mu,L_N J_mu>=0, actual source (A.7) gives

    Ttilde_mu(u)=u-1/m_mu(u),
    kappa_j=-Res_(u=b_j) [1/m_mu(u)]>0,
    sum_j kappa_j=||A_d^dagger J_mu||^2/||J_mu||^2=3N.

The minus sign and the factor 3N are essential. The spectral measure of
normalized v for L_d thus has probabilities

    q_j=kappa_j/(3N)=|<v,psihat_(mu-r_j,r_j)>|^2.

For the ascending interlacing poles and zeros of mu, the residue formula is

    kappa_j=(b_j-a_(j-1))(a_j-b_j)
             * product_(l<j) (b_j-a_(l-1))/(b_j-b_l)
             * product_(l>j) (a_l-b_j)/(b_l-b_j).

Every far ratio is greater than one. The adjacent factors are g_j>=3 and
h_j>=1. Therefore kappa_j>=3, and

    q_j >= 1/N >= 1/(3N).

Both adjacent poles exist even for the extreme zero. If mu has one removable
corner, its single q is exactly 1; this includes mu=(1), d=0. The second
overlap and the asserted invariant space use A psi=J; the first overlap does not.

## 3. Exact alternating measurements retain every failure branch

Let P,Q restrict to the rank-one lines u,v on an invariant two-dimensional
space, and gamma=|<u,v>|^2. Start in u. First measure Q; stop on success.
After failure, KEEP the resulting state v_perp. Repeatedly measure P and
then Q, stopping only on Q-success, irrespective of the P outcome.

From v_perp, the P outcomes u,u_perp occur with probabilities 1-gamma,gamma.
Their subsequent Q-success probabilities are gamma,1-gamma. Thus each full
(P,Q) cycle after a failed Q succeeds with probability 2gamma(1-gamma).
Every failed Q returns to the SAME line v_perp. After an initial Q test and
M cycles the exact failure probability is

    (1-gamma) [gamma^2+(1-gamma)^2]^M.

The measurement count is <=1+2M. No source-state reset, recursive state
preparation inverse, postselected restart, or unknown Jack projector occurs.
Swapping P and Q gives the identical return/rewind formula.

For stage 1, take P=pi0 and Q=the requested L_d content projector. Source
Lemma 3.3 and self-adjointness preserve Z_lambda and both complementary
outcomes; on it P is the J_lambda line and Q the chosen psi line.
For stage 2, start in the chosen psi and target P_A inside S_mu. The argument
in §2 supplies the corresponding invariant two-dimensional space.

A lower bound on gamma ALONE would not give a uniform logarithmic tail when
gamma approaches one. Here the complete corner distributions supply the
missing upper bound. For d>=1 there are at least two tau masses; each is
>=a=3/(16d), so gamma lies in [a,1-a]. For q there is either one mass and
success is immediate, or all masses are >=b=1/N and gamma lies in [b,1-b].
For a lower bound l<=1/2 on both gamma and 1-gamma,
2gamma(1-gamma)>=l, so the failure is <=exp(-l M).

Writing L_eta=ceil(log2(1/eta)), valid undiluted cycle caps are

    M_up=ceil(16d L_eta/3)  (d>=1),
    M_down=N L_eta        (or zero cycles in the one-mass case).

The degree-zero first stage is deterministic. The original weaker parent
bounds also give valid caps 16d^2 L_eta and 3N L_eta. Thus the paid report's
generic near-one warning is valid for arbitrary projector pairs, but does
not create a gap for these Jack corner distributions.

## 4. Universal ancilla dilution also works without knowing gamma

There is an alternative that needs no complementary-overlap argument. Use

    P'=P tensor |0><0|,  Q'=Q tensor |+><+|,

starting in u tensor |0>. Their invariant plane is spanned by u tensor |0>
and v tensor |+>, and the overlap is gamma'=gamma/2<=1/2. If gamma>=l,
then 2gamma'(1-gamma')>=l/2. Therefore

    M=ceil(2 L_eta/l)

cycles suffice. A successful measurement leaves v tensor |+>; a Hadamard
returns that known ancilla to zero. The reverse direction is identical, or
one can swap the roles before introducing the ancilla. No overlap estimate
or input partition label is required.

The implementation must measure the BINARY joint projector {P',I-P'}, not
separately reveal the P and ancilla failure outcomes. A controlled native
reflection I-2P, conditioned on ancilla zero, is exactly I-2P'; conjugating
the ancilla by Hadamards gives the corresponding Q' reflection. The usual
one-bit reflection measurement therefore gives the required joint instrument.
Here P,Q are the GLOBAL native pi0/P_A/content projectors; their rank-one
restrictions are used only in the proof, never supplied as Jack reflections.
Finite-precision compilation of those controlled reflections is a separate
obligation.

For a fixed D-box growth path with D>=1, allocating eta/(2D) to each of its two stages
per box gives an ideal exact-projector clock O(D^2 log(D/eta)) with total
failure <=eta, using either the stronger undiluted bounds or universal
dilution. Successful stages return the specified pure state up to global
phase; all failed states are retained during the bounded alternation.
The same per-corner statement justifies exact nondemolition return after a
sampled up/down content, without knowing the input Jack label.

These results do not clean lambda-dependent coherent histories, prove an
operator-norm full decoder, or pay approximate spectral measurement. Those
remain separate from this overlap and exact-measurement review.
