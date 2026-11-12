# Exact obstruction to a universal three-site Gaudin joint AGP

2026-11-13. Independent core review of the proposed strengthened locality
falsifier. STATE, `NEXT_CONSTRUCTIVE_MECHANISMS.md`, the retained control
and certificate, and the actual charge normalization in the retained
Lutz text were checked. One targeted exact rational verification was run;
no parameter sweep, eigensolver, floating residual, network, API, or Git.

**REFUTED:** a universal exact joint adiabatic gauge potential supported
on at most three physical sites for the stated native Gaudin family.
At the instance below, no such Hermitian operator exists, even with
arbitrary real-symmetric gauge terms and without assuming particle-number
conservation of the proposed operator. This is stronger than rejection
of the displayed current ansatz, and remains a statement about exact
transport of the ENTIRE joint eigenbasis/eigenspace family.

## 1. Native matrices and independent exact verification

Use N=4, the M=2 sector, sites (0,1,3,7), and g=1/3. The ordered sector
basis is

    0011, 0101, 0110, 1001, 1010, 1100.

Here bit 0 has Z=+1 and `n_i=(I+Z_i)/2`. At N=4,M=2 the Hamming weight
and the n-occupation both equal 2. The native charges are

    Q_i=n_i+(g/4) sum_(j!=i)(X_i X_j+Y_i Y_j+Z_i Z_j-I)/(eps_i-eps_j)
       =n_i+(g/2) sum_(j!=i)(P_ij-I)/(eps_i-eps_j).

This is retained Lutz Eq.(10), physical text lines 220--241; the swap
identity is `X_iX_j+Y_iY_j+Z_iZ_j=2P_ij-I`. Let V_i=dQ_i/dg.

The independent check reconstructs the FULL 16-dimensional operators by
Pauli tensor products, using `Y=iJ` and the rational matrix J, and then
projects to the six basis states. Thus it does not reuse the control's
swap-entry implementation. It verifies:

* all four Q_i and V_i agree exactly with the stored certificate;
* every coefficient of `[Q_i(g),Q_j(g)]` as a quadratic polynomial in g
  vanishes, and the sector sums are `sum Q_i=2I`, `sum V_i=0`;
* stored K is real antisymmetric and satisfies ALL 576 entries of
  `[Q_j,V_i-[K,Q_i]]=0`, for all i,j;
* the map on the full 15-dimensional antisymmetric space has rank 15,
  and its augmentation by the right side has rank 15;
* the subspace with the three Hamming-distance-four entries set to zero
  has dimension/rank 12, while its augmented system has rank 13;
* the independently tensor-constructed current generators agree with
  the certificate, and its 13-term left-null witness pairs to 0 with
  every current column and to 1 with the right side.

The first charge also has squarefree characteristic polynomial:
`gcd(charpoly(Q_0),charpoly(Q_0)')=1` exactly. Thus the sector joint
spectrum is simple here; no degeneracy convention is being exploited.

Reproducible independent artifacts are
`audits/reviews/2026-11-13-gaudin-three-local/verify.py` and `result.json`.
The verification was launched by `/opt/anaconda3/bin/python` through the
installed Sage `-c` interface; it did not rerun or overwrite the original
control. The result records the checked certificate SHA256, all rank
results, a nonzero exact 15-row determinant, and the characteristic
polynomial. For example, the selected full-rank minor has determinant

    -496052898184463759383 / 6332627885807415128861820844069632.

Rank over Q equals rank over R, so uniqueness is not a restriction to
rational generator coefficients.

## 2. Necessary transport equation and sign convention

Fix the convention `U'=-i A U`, with A Hermitian, for transport of the
joint eigenbasis. Write `Q_i=U D_i U^dagger`. Differentiation gives

    Q_i'+i[A,Q_i]=U D_i' U^dagger.

The right side commutes with every Q_j. Consequently every exact joint
AGP must satisfy

    [Q_j,Q_i'+i[A,Q_i]]=0                            (1)

for all i,j. This is a necessary condition, not an assumed sufficient
ansatz for selected individual branches. At this instance Q_0 is simple,
so smooth local eigenbranches and arbitrary phase gauges are well defined.

In the real computational basis decompose ANY Hermitian A as

    A=S+iK,       S real symmetric, K real antisymmetric.

Since Q_i and V_i are real, (1) separates into real and imaginary parts:

    [Q_j,V_i-[K,Q_i]]=0,
    [Q_j,[S,Q_i]]=0.                                 (2)

In particular real-symmetric terms cannot cancel a failure of the first
equation. With the adopted convention the stored solution corresponds
to A=iK, since `i[iK,Q_i]=-[K,Q_i]`. Reversing the transport convention
would reverse K's sign, not remove its nonzero entry. Because Q_0 is
simple, the second equation merely makes S diagonal in its real
eigenbasis, hence a commuting phase gauge.

The exact rank-15 calculation proves that the first equation in (2)
has ONE real antisymmetric solution. Its forbidden entry is

    <0011|K|1100>
       =355248848800449 / 125250068977266446 != 0.      (3)

The stored K satisfies every native constraint, so (3) belongs to that
unique solution rather than to a choice among possible antisymmetric
gauges.

## 3. Why arbitrary three-site Hermitian terms cannot evade it

If an operator term acts nontrivially on at most three of the four sites,
then at least one site is outside its support. The strings 0011 and 1100
differ at ALL four sites, so their matrix element through that identity
factor is zero. Hence every sum of at-most-three-site terms satisfies

    <0011|A|1100>=0.

This is independent of its coefficients, Pauli expansion, symmetry,
number conservation, or locality of the proposed phase gauge. Splitting
this zero complex entry into real and imaginary parts requires K's entry
to vanish, contradicting (3). Adding a real-symmetric term cannot cancel
a nonzero purely imaginary part.

Number-nonconserving terms do not change this argument. Let P project
onto the fixed M=2 sector. Since the native Q_i and V_i preserve M,
compression of (1) gives the same condition for `A_M=PAP` and the
restricted charges. In particular

    P[Q_j,[A,Q_i]]P=[Q_(j,M),[A_M,Q_(i,M)]].

Off-sector blocks cannot affect these compressed constraints. Moreover,
compression leaves the indicated computational-basis matrix element
unchanged. Thus a three-site operator on the full four-qubit space
cannot induce an admissible imaginary sector block through leakage terms.

## 4. Exact disposition

This single exact native counterexample disproves a formula asserting
that an exact joint AGP ALWAYS has at-most-three-site support. It requires
at least four-site support at this instance. The full antisymmetric
positive control establishes that the transport constraints themselves
are consistent; the obstruction is locality.

It does not disprove an operator tailored to one selected eigenbranch,
approximate transport, higher-support generators, efficient circuit or
state preparation, other parameter families, or a general Gaudin
transport mechanism. It gives no growing-N support lower bound, gap
bound, norm-cost bound, hardness result, or quantum advantage claim.
