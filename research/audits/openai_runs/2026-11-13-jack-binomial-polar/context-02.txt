# 2026-11-13 — Independent coherent Jack branching construction

ACCEPT the written full transform at FIXED alpha=3, numerical degree D,
with a deterministic circuit of size poly(D,1/epsilon), 0<epsilon<1. On the valid shape
subspace it maps |mu>|0> to |Jhat_mu>|0> within epsilon in isometry/operator
norm, uniformly on arbitrary superpositions. Here the output coordinates
are the orthonormal power-sum occupations, not physical particle positions.
This is a proof of a native circuit construction, not an implementation,
novelty claim, classical lower bound, or demonstrated useful advantage.

The elementary principal-square-root compiler below pays the complete
precision clock. It does NOT claim poly(D,log(1/epsilon)); that stronger
precision dependence would need a separately checked phase-synthesis route.
No supplied Jack reflection, coefficient oracle, recursive state-preparation
inverse, measurement, postselection, or enumeration of partitions/paths is used.

Inputs checked: JACK_COHERENT_BRANCHING_TRANSFORM; the stable all-degree
intertwiner and overlap reviews; actual Mickler–Moll source. For simulation,
actual Aharonov–Ta-Shma quant-ph/0301023v2, retained `aharonov_tashma.txt`,
Lemma 1 and §5 (physical LF 855–1039) give constructive sparse simulation,
including clean 2-by-2 blocks and operator-norm error. Actual Gilyen et al.
1806.01838v1, `gilyen_qsvt.txt` 1640–1673, does supply positive singular-vector
transformation at the stated query cost; its phase compiler is unnecessary
for the weaker, completely explicit precision dependence proved here.

## 1. Exact positive branching coefficients

Let F_n be the degree-n power-sum space and H_d=F[w]_d. All basis vectors
below are normalized in the alpha=3 Hall inner product. Put d=n-1,
V=A_d^dagger/sqrt(3n), and write v_(lambda,s)=psi_(lambda,s)/||psi_(lambda,s)||.
The established identity A_d psi_(lambda,s)=J_(lambda+s) and AA^dagger=3n I
imply

    V Jhat_mu = sum_(r in R_mu) sqrt(q_mu,r) v_(mu-r,r),
    q_mu,r = ||J_mu||^2/[3n ||psi_(mu-r,r)||^2] > 0,
    sum_r q_mu,r=1.

These coefficients are POSITIVE, using pi0 psi=J and the positive norm.
No undetermined relative eigenvector phase remains. The q values can be
computed without evaluating a Jack polynomial: if a_i are addable contents
of mu and b_j=c(r_j)+2 its outer-corner contents, then

    q_mu,r_j = -Res_(u=b_j) 1/m_mu(u) /(3n),
    m_mu(u)=product_j(u-b_j)/product_i(u-a_i).

The residue is a product/quotient of O(n) nonzero integers of magnitude O(n).
Thus each rational has O(n log(n+1)) numerator/denominator bits before any
cancellation; exact prefix sums also have polynomial bits. The independent
bounds q>=1/n and tau>=3/(16d) for d>0 hold. The d=0 up overlap is one.

## 2. Global polar pairs, including content degeneracies

For a fixed content c let P_c be the GLOBAL spectral projector of L_d, and
let P0 be the marker-zero projector. The orthogonal cyclic decomposition
and simple spectrum inside each Z_lambda give the exact singular expansion

    P0 P_c = sum_(lambda: c in A_lambda)
               sqrt(tau_lambda,c) |Jhat_lambda><v_lambda,c|.

There is at most one corner of content c for any given lambda. The left
vectors are orthonormal across lambda, as are the right vectors. Hence this
is a genuine singular decomposition, despite global L_d degeneracies.
In particular every vector in the valid P_c image has nonzero singular value
at least 1/(4d) for d>=1, using the weaker tau>=1/(16d^2).

Let

    W_c=(2P0-I)(2P_c-I).

On one singular plane, write u=Jhat_lambda and
v=v_lambda,c=cos(theta)u+sin(theta)u_perp, where cos(theta)=sqrt(tau)>0.
In the ordered basis (u,u_perp),

    W_c = [[cos(2theta), sin(2theta)],[-sin(2theta), cos(2theta)]].

Its PRINCIPAL square root is the same rotation through half the angle,
so W_c^(1/2) v=u with positive coefficient one. If tau=1, the common line
has W_c=1 and the map is identity. For tau<1, the two eigenphases are
+-2theta and their distance from the principal-branch cut at -1 is

    pi-2theta=2 arcsin(sqrt(tau)) >= 2 sqrt(tau).

For every stage d<=D, the conservative rational lower bound

    g0=1/[2(D+1)]

therefore separates every REQUIRED eigenphase from the cut. Zero-singular
or P0-only blocks may have W_c=-1, but are outside the promised P_c input.
The algorithm below still defines a unitary circuit on them; no assertion
of approximation to a discontinuous square root on the whole ambient space
is needed. The required Jordan planes are mutually orthogonal and reduce
both native projectors.

## 3. A finite positive-polar compiler using ordinary coherent QPE

This section gives a uniform restricted-operator-norm error, not merely a
basis-state probability bound. To approximate the positive polar map within
zeta (0<zeta<1/2), set

    h=min(g0/4,zeta/4),  xi=zeta^2/64,
    M=the least power of two >=16/(xi h^2).

Apply ordinary coherent M-point phase estimation to W_c, interpret its
estimate phihat in [-pi,pi), apply the phase exp(i phihat/2) to the phase
register, and UNCOMPUTE phase estimation. The phase operation is elementary:
for estimate j, it is exp(i*pi*j/M), with an additional minus sign when
j>=M/2. It uses binary controlled one-qubit phases, not QSVT phase synthesis.

For a W_c eigenphase phi, let p_j be its QPE outcome probabilities. The exact
Dirichlet-kernel amplitude at circular angular distance a from phi is at
most pi/(M a). Therefore

    Pr(circular phase error>h) <= pi^2/(M h^2) <= xi.

This intentionally loose bound sums over all M bins; it already gives a
polynomial clock. On the good bins, h<g0 ensures no branch-cut crossing and
|exp(i phihat/2)-exp(i phi/2)|<=h/2. Uncomputation gives the EXACT identity

    ||U_polar(|omega>|0>)-exp(i phi/2)|omega>|0>||^2
      = sum_j p_j |exp(i phihat_j/2)-exp(i phi/2)|^2.

Thus the clean-vector error is at most h/2+2sqrt(xi)<=3zeta/8. The circuit
and ideal function are block diagonal in the W_c eigenspaces, so the same
bound is an OPERATOR NORM bound on their entire required direct sum. There
is no factor depending on its dimension. Controlled c blocks obey the same
maximum bound; the circuit never needs lambda or tau.

There are fewer than 2M controlled W_c calls including uncomputation.
Approximate each by operator error <=zeta/(32M), and allocate total error
<=zeta/8 to the ordinary QFT and half-phase gates. A hybrid bound gives total
error <zeta. All gates remain unitary, with no discarded failure history.
The phase workspace is within zeta of zero on every promised input.

Here M=poly(D,1/zeta); its register length and every angle precision are
O(log(D+1)+log(1/zeta)). Repeated powers of W_c are implemented by their
charged number of ordinary calls, not an unprovided fast-forwarding oracle.
The construction is a unitary extension on all inputs, including bad/cut
blocks; only its desired-subspace approximation is used in composition.

## 4. Native content extraction, simulation and the isometry V

Use occupation counts (m_1,...,m_D) and marker l, with sum k*m_k+l=d.
This uses O(D log(D+1)) qubits; invalid encodings can be assigned a zero
Hamiltonian. L_d has diagonal 2l and the two possible mode-k edges

    (m,l) <-> (m-e_k,l+k),  weight sqrt(3k m_k).

There are O(D) neighbors, each weight is computed to any specified bit
accuracy by reversible integer/square-root arithmetic, and the norm is
polynomial (indeed <=3d on the valid space by the source spectrum).
No partition-space matrix is constructed.

Actual Aharonov–Ta-Shma Lemma 1 applies. Its Claim 5 computes the common
2-by-2 block label, rotates, and uncomputes that label; its norm bound is a
MAXIMUM over blocks, not a sum over Hilbert-space dimension. One can also
use an explicit native decomposition here: split each mode-k chain according
to parity of the larger m_k into two disjoint edge matchings, and keep 2l
as the diagonal term. This gives 2d+1 terms, each composed of 1-by-1 or
2-by-2 blocks. Their total norm bound is <=8(D+1)^2. Reversible matching
labels are polynomial-time functions of the occupations and marker. Label
each pair by its higher-m_k endpoint and that endpoint's weight: the computed
metadata is identical at both endpoints and can be uncomputed after rotation.

For evolution time |t|<=8 and desired error rho, set Lambda=8(D+1)^2
and use R=ceil(260 Lambda^2/rho) first-order product-formula slices.
The unitary Duhamel bound is t^2 Lambda^2/(2R)<=rho/8. Approximate each of
the R(2d+1) component exponentials within rho/[8R(2d+1)], contributing
another rho/8. Computing pi and the evolution time is included in the
remaining operator-error budget. Clean block-rotation synthesis follows.
This proves a fixed polynomial gate clock in D and 1/rho. Angles t*sqrt(3k m_k) and diagonal phases have polynomial
bit algorithms. Ordinary finite-universal-set one-qubit gate synthesis
adds polynomial overhead; all controlled versions have the same norm bounds.
Gate synthesis approximates specified unitaries in OPERATOR norm, preserving
their phases. Controlled gates are compiled directly or with tracked phase
corrections; an unknown block-dependent global phase cannot be dropped.
This also supplies a direct native specialization of the retained source.

For integer-content extraction choose

    M0=2^ceil(log2(8(D+1))).

On the valid space all eigenvalues lie in [-d,3d], inside (-M0/2,M0/2).
Exact ideal QPE for exp(2pi i L_d/M0) therefore returns c mod M0 with
amplitude EXACTLY +1; a reversible signed interpretation yields c. All
controlled powers need evolution time <2pi. Approximate simulations and
ordinary QFT gates with a total operator budget rho give a clean content
extractor within rho. This avoids an ambiguous sign convention from merely
requiring a modulus larger than the spectral width.

Compute content, compare it with the stored c, apply the appropriate phase,
and uncompute content to implement the reflection 2P_c-I. P0 is just a
marker-zero test. Controlled reflections used inside W_c-QPE are native
controlled versions of these circuits. The two global reflection signs are
fixed consistently so their product is exactly the W_c in §2.

The other native isometry is

    V|m> = sum_(k:m_k>0) sqrt(k m_k/n)|m-e_k,l=k-1>.

Prepare the mode label k-1 coherently from the integer weights k m_k/n,
then decrement m_k controlled on that marker. The decrement is a permutation
on the padded occupation registers; valid inputs never wrap. Prefix-tree
rotations have polynomially many branches and polynomial-bit weights.
All arithmetic is computed and uncomputed while m is available. This is
an explicit full unitary on padded registers with marker initially zero;
its inverse restores m before reversing the mode preparation. No supplied
inverse of a Jack preparation appears.

## 5. Clean B_n and C_n, including reversible label erasure

Define the ideal B_n as follows: apply V, coherently extract content c, and
apply the c-controlled positive polar map of §2. The marker is now zero,
and all auxiliary polar/content workspace is zero in the ideal map. Thus

    B_n: Jhat_mu |0> -> sum_r sqrt(q_mu,r) Jhat_(mu-r)|c(r)>.

All relative phases are positive: this follows separately from the native
V weights, the source-normalized intertwiner, exact integer QPE, and the
principal-root calculation. Different content values are retained, not
silently merged under the many-to-one map A_d.

For C_n, from an explicit shape mu enumerate removable corners and compute
its rational q values by §1. Coherently prepare their content register with
POSITIVE amplitudes sqrt(q). Ordinary binary-prefix state preparation has
polynomial arithmetic and gate cost. Exact rational prefix sums have
polynomial bit length; nonzero conditional probabilities are bounded below
by 1/n, and exact zero/one cases are decided by integer arithmetic.
Angle approximation and all workspace cleanup are therefore uniform over
all valid shapes, without enumerating their exponentially many possibilities.

Update (mu,c) to (mu-r(c),c). This map is injective on valid pairs: from
(lambda,c), the unique addable corner of content c reconstructs mu. Both
forward and inverse are polynomial-time shape operations. A clean reversible
extension can be built by computing the forward map into a blank register,
swapping, then XOR-erasing the old input with the computed inverse. Invalid
pairs can use any fixed total definitions; the complete circuit is still
unitary, and the work register is zero on valid pairs. Hence

    C_n: |mu>|0> -> sum_r sqrt(q_mu,r)|mu-r>|c(r)>

has a native unitary extension. It retains no hidden copy of mu. This does
not assume that an arbitrary rectangular isometry has a free inverse.

Execute B_D,...,B_1 downward. The result is vacuum times a removal-path
state, with each path amplitude the positive square root of its product of
q values. Execute C_D,...,C_1 on a label: it gives the IDENTICAL path state
and the empty shape. Any valid content path reconstructs its original shape
uniquely by reversing from the empty partition; addable contents are distinct
at each step. Thus different original shapes have disjoint path supports,
even though isolated contents have global degeneracies.

Pad workspaces with zeros so both downward maps use a common vacuum/path
register layout. The empty shape and Fock vacuum are fixed zero encodings,
so they can be identified/re-encoded by a known unitary. Now execute the ACTUAL inverse
circuits B_1^dagger,...,B_D^dagger. They erase every path register and output
Jhat_mu. Their use is legitimate on the whole path-state range just proved
equal to the range of the B-down isometry. No path enumeration occurs.

## 6. Uniform composition and final finite clock

There is a useful inverse-on-range bound. If two full unitaries U and Utilde
satisfy ||(Utilde-U)|S||<=a, then on U(S),

    ||(Utilde^dagger-U^dagger)U|S||
      = ||Utilde^dagger(U-Utilde)|S|| <= a.

Therefore forward approximation of each B construction on its promised
clean input already pays the use of its ACTUAL circuit inverse on the
corresponding path range. No global approximation to the polar square root
on irrelevant cut blocks is needed.

For D>=1 take zeta=epsilon/[16(D+1)]. Budget each B_n at <=4zeta and each
C_n at <=2zeta on its valid clean input, using the concrete subroutine
allocations above. Their forward downward compositions have errors at most
4D zeta and 2D zeta by unitary hybrid bounds. The exact C path range is the
exact B path range after the fixed vacuum recoding. Applying the inverse-on-
range bound and then the approximate C error gives endpoint error at most

    6D zeta < epsilon.

Every bound is restricted OPERATOR norm: controlled arithmetic is a direct
sum over classical labels, the polar error is a maximum over orthogonal
eigenblocks, and simulation errors are global operator bounds. Hence this
holds uniformly for arbitrary input superpositions and reference systems,
with no factor p(D). Workspace is epsilon-close to its clean target; it is
never measured or discarded to repair the state. D=0 is the trivial vacuum.

All loops have fixed polynomial bounds: D stages, polynomially many shape
arithmetic operations, M=poly(D,1/zeta) polar queries, and native simulation
at inverse-polynomial accuracies in those parameters. Elementary angle and
rational arithmetic use polynomial bits, and standard finite gate synthesis
preserves a polynomial total gate/description cost. Thus the proof gives
poly(D,1/epsilon) resources with a fixed exponent independent of the partition
count. No overlap parameter or source-state inverse is supplied as advice.

The construction closes the full clean basis-change interface at this weaker
precision dependence. It leaves polylogarithmic precision dependence,
implementation, applications, and any matched classical-sampling separation
outside the admitted conclusion.
