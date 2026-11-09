# Two-cluster Gaudin fusion: exact finite-spacing and all-family review

2026-11-07. CLOSED independent mathematical review. Read current STATE/TRAPS
and the retained native charge definition in gaudin_gap_geometry/lutz_v3.txt.
No network/API/Git or numerical control was run. The bounds below are
operator identities/inequalities, independent of optimizer output.

**Disposition:** the fusion construction is correct, including the singular
internal terms and an explicit polynomial finite-spacing error. The critical
weighted-path identity and two-tent variational argument give an ALL-FAMILY
upper bound on same-particle-sector joint separation squared. They refute a
uniform Omega(1/N) squared-separation claim. They do NOT prove a
superpolynomially small gap, inefficient preparation, or a quantum/classical
separation. A polynomial lower bound with a different exponent remains open.

## 1. Native family and exact fused operator

Let n>=2, N=2n, g>0 rational and delta>0 rational. Label sites by A_i,B_i,
0<=i<n, with eps_Ai=delta i and eps_Bi=1+delta i. Assume
delta(n-1)<=1/2, so all sites are distinct. Work in the physical sector with
n occupied spins, equivalently S_A^z+S_B^z=0. Use exactly the native charges

    Q_i=n_i+(g/2) sum_(j!=i)(SWAP_ij-I)/(eps_i-eps_j).

Let P project onto the subspace symmetric separately in clusters A and B,
within this particle sector. Each cluster has spin S=n/2; ran P has dimension
n+1 and orthonormal basis |m>_A|-m>_B, -S<=m<=S.

Write Q_i=A_i/delta+B_i(delta), separating within-cluster and cross-cluster
terms. Then A_i P=P A_i=0 exactly. On ran P,

    P n_Ai P = 1/2+S_A^z/n,
    P sum_j(SWAP_Ai,Bj-I) P = (2/n)S_A dot S_B-n/2.

Consequently the finite parts at delta=0 are

    F_Ai=P B_Ai(0) P = c_A I+H/n,
    F_Bi=P B_Bi(0) P = c_B I-H/n,
    c_A=1/2+gn/4,  c_B=1/2-gn/4,
    H=S_A^z-g S_A dot S_B.

In the stated m basis, H has diagonal m+g m^2 and off-diagonal
-g[S(S+1)-m(m+1)]/2 between m and m+1. There is no missing square root:
the two spin-raising/lowering factors are equal positive square roots,
whose product is S(S+1)-m(m+1). All entries are rational. Every off-diagonal
is nonzero for g>0, so the real symmetric tridiagonal has simple spectrum
(its first eigenvector coordinate determines all others by recurrence).

## 2. Isolated invariant subspace at nonzero rational delta

Define a charge combination, with the SAME local index in both clusters,

    T_delta=-(2delta/g) sum_i i(Q_Ai+Q_Bi).

Pairing the two within-cluster contributions gives exactly

    T_delta=K_A+K_B+E_delta,
    K_C=sum_(i<j in C)(I-SWAP_ij).

The error is explicitly

    E_delta=-(2delta/g) sum_i i(n_Ai+n_Bi)
       +delta sum_(i,j) (i-j)/(1-delta(i-j)) (SWAP_Ai,Bj-I).

Since sum_(i,j)|i-j|=n(n^2-1)/3 and ||SWAP-I||=2,

    ||E_delta|| <= delta C_E,
    C_E=2n(n-1)/g+(4/3)n(n^2-1).

The cluster identity K_C=S(S+1)-S_C^2 shows that its first nonzero
eigenvalue is n. Thus K_A+K_B has kernel P and gap at least n on P's
orthogonal complement, also after restricting to the particle sector.
Set eta=delta C_E and suppose eta<=n/4. The spectral projector P_delta
of T_delta below n/2 has the same rank as P and commutes with every Q_i,
because the native charges commute.

A dimension-free subspace bound is

    ||P_delta-P|| <= eta/(n-eta) <=2eta/n.

For completeness, the off-diagonal map X=(I-P)P_delta satisfies a Sylvester
equation with left spectrum >=n and right spectrum <=eta. The integral
solution using exp(-t K_complement) and exp(t T_low) bounds its norm by
eta/(n-eta). Equal projector ranks identify this with the largest sine of
the principal angles. The direct-rotation unitary U mapping P to P_delta
then obeys ||U-I||<=2||P_delta-P||<=4eta/n.

No exponential matrix or projector is constructed algorithmically here.
These are proof-only operators proving existence of actual joint states.

## 3. Singular terms have O(delta), not O(1), compressed error

Uniformly over the 2n charges,

    ||A_i|| <= g(n-1),
    ||B_i(0)|| <=1+gn,
    ||B_i(delta)-B_i(0)|| <=g n(n-1)delta.

The last bound uses |1/(1-delta(i-j))-1|<=2delta|i-j| and
max_i sum_j|i-j|=n(n-1)/2. Let c=4delta C_E/n. Since A_i annihilates P on
both sides,

    P U^dagger A_i U P=P(U^dagger-I)A_i(U-I)P.

Therefore division by delta costs only ||A_i||c^2/delta=O(delta).
The regular part changes by at most g n(n-1)delta+2(1+gn)c. In total,
for the EXACT compressed charges Qtilde_i=P U^dagger Q_i U P,

    ||Qtilde_i-F_i|| <= e=delta C_Q,
    C_Q=16g(n-1) C_E^2/n^2 +g n(n-1)+8(1+gn)C_E/n.

All quantities are explicit rationals. The compressed charges commute
exactly, as P_delta is invariant. Merely applying an O(delta) subspace
bound directly to the full ||Q_i||=O(1/delta) would miss this cancellation;
the displayed double-annihilation identity is essential.

## 4. Transfer of fused eigenvalue gaps to actual joint labels

Let h_0<...<h_n be the spectrum of H. Use Qtilde_A0 as anchor and order a
simultaneous orthonormal eigenbasis by its eigenvalues lambda_j. Weyl gives

    |lambda_j-(c_A+h_j/n)| <= e.

Moreover ||Qtilde_Ai-Qtilde_A0||<=2e and
||Qtilde_Bi+Qtilde_A0-I||<=2e. Thus every component of the j-th joint label
is within3e of its corresponding fused component. Mapping these vectors
through U gives actual orthogonal joint eigenstates of the original charges.
For any j<k their squared joint-label distance is bounded by

    distance^2 <= (2/n)(h_k-h_j+6n e)^2.                 (TRANSFER)

This argument does not perturb individual eigenvectors of H and needs no
inverse minimum gap of H. If e<(h_k-h_j)/(2n), the anchor eigenvalues are
distinct as well. Without that extra condition the two joint states are
still orthogonal; any coincident full joint labels would itself give zero
separation and fail the required rank-one-separation premise.

If exact rational enclosures give 0<d_low<h_k-h_j<d_high<1/2, choose any
positive rational delta satisfying

    delta <= min(1/[2(n-1)], n/[4C_E],
                 d_low/[4n C_Q], (1/2-d_high)/[12n C_Q]).

Then the actual states have distinct anchor values and distance^2<1/(2n).
This is a finite rational native counterexample, not an inference from
near-degeneracy at delta=0. The separately supplied n64 enclosure
67/250< h_1-h_0 <27/100 is sufficient; its exact Sturm certificate is owned
by the separate control reviewer and was not rerun here.

## 5. Critical weighted-path identity and all-family upper bound

Now set g=1/(2n), k=m+n/2 in{0,...,n}, and

    a_k=(n-k)(k+1)/(4n), 0<=k<n.

With boundary weights a_-1=a_n=0, the weighted path Laplacian L_a has
off-diagonal -a_k and diagonal a_(k-1)+a_k. Direct calculation gives

    H+(3n/8+1/4)I = L_a+diag(k^2/n) >=0.               (PATH)

For n>=27 put ell=floor(n^(1/3)). Use two real triangular tents, supported
on[0,2ell] and[3ell,5ell], zero at their endpoints, with peaks1 at ell and
4ell and slopes +/-1/ell. Both lie in the path since5ell<=n. Their supports
and nonzero-gradient edges are disjoint, so their mutual norm, Laplacian
and potential cross forms vanish. Each has exact squared norm

    (2ell^2+1)/(3ell) >=2ell/3.

Each has2ell nonzero edge differences of magnitude1/ell, and on their
edges a_k<=5ell/4. Its Laplacian Rayleigh quotient is therefore at most
15/(4ell). The potential quotient is at most25ell^2/n. Every vector in
their two-dimensional span obeys the same total bound. Min--max and (PATH)
give

    h_1-h_0 <=15/(4ell)+25ell^2/n <=33 n^(-1/3).

Indeed ell>=2 n^(1/3)/3 for n>=27, which gives the stronger constant245/8;
33 is a safe rational simplification. Positivity of (PATH), not a numerical
estimate for the ground energy, pays the subtraction of h_0.

Finally take delta=n^(-8). At critical g the preceding constants satisfy
C_E<=6n^3 and C_Q<=400n^4. All site/projector conditions hold for n>=27,
and e<=400n^(-4). In detail, delta C_E<=6n^(-5)<=n/4, while
6n e<=2400n^(-3)<=n^(-1/3) because n^(8/3)>=27^(8/3)=6561>2400.
Applying (TRANSFER)
to the first two fused levels proves the native all-family estimate

    min_same-sector separation^2 <=2312 n^(-5/3),  N=2n. (FAMILY)

This is o(1/N), so it refutes a uniform Omega(1/N) squared-separation floor.
For the n64 strict finite counterexample, delta=2^(-48), e<=25/1048576,
and6n e<=75/8192<1/100. The separately certified positive gap lower bound
makes its anchor eigenvalues distinct by a large margin. Its upper bound
is proved without a new numerical calculation:

    distance^2 < (1/32)(27/100+1/100)^2
               =49/20000 <1/400 <1/128.

The sites have O(log n)-bit rational descriptions, minimum spacing n^-8,
and g=1/(2n). Thus inverse spacing and charge norms grow only polynomially
in n. The counterfamily does not exploit an exponentially ill-conditioned
binary input. No matching lower bound, precise n^-1/3 asymptotic, or
superpolynomial obstruction is proved. Conditional joint-charge preparation
could remain polynomial under a smaller polynomial gap.
