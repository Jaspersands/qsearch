# Gaudin bulk double-transfer coefficient: independent disposition

2026-11-13. Narrow review of the completed
`openai_runs/2026-11-13-gaudin-generator/response.md`. Current STATE was
read. This proof uses local spin identities and the previously verified
symbolic four-site coefficient. No new model size, N=6 calculation,
parameter sweep, network, API, Git, or implementation was used.

**Accepted:** for every N>=4, 2<=M<=N-2, and pairwise distinct real sites,
the first two displayed coefficients K0,K1 are correct. The g^2
coefficient for transferring two occupied sites to two empty sites is
independent of every external spectator occupation. This rules out
exact joint generators consisting of at-most-three-site terms, or of
arbitrarily diagonally dressed single exchanges, on any full coupling
interval [0,G] with G>0. It does not provide a complete path generator
or require support growing beyond four sites.

## 1. Signs and the complete first two coefficients

Keep `n_a=(I+Z_a)/2`, and put

    E_ab=sigma_a^+ sigma_b^-,
    C_ab=E_ab-E_ba,    T_ab=E_ab+E_ba,
    d_ab=eps_a-eps_b,
    D=sum_a eps_a n_a, V=(1/2)sum_(a<b) T_ab.

Thus C_ab has matrix element +1 for transfer b->a. On a fixed-M sector,
the actual native combination is

    sum_a eps_a Q_a(g)=D+gV-(g/2)M(N-M)I.

Its scalar term does not affect transport equations. With the established
convention A=iK, any joint generator obeys

    ad_(D+gV)^2 K=-[D,V].                            (1)

Derive first at sites with distinct fixed-M subset sums, a dense open
set. The antisymmetric solution has zero diagonal in the occupation
basis. Since `[D,C_ab]=d_ab T_ab`, its constant term is

    K0=-(1/2)sum_(a<b) C_ab/d_ab.                    (2)

There is no missing one-body or diagonal term in this real antisymmetric
coefficient. Direct two/three-site spin commutators give, for B=[V,K0],

    B_diag=(1/4)sum_(a<b)(Z_a-Z_b)/d_ab,

    B_off=-(1/4)sum_(a<b)sum_(c!=a,b)
                (1/d_ac+1/d_bc) Z_c T_ab.            (3)

For example `[T_ab,C_ab]=Z_b-Z_a`, and
`[T_ac,C_bc]=Z_c T_ab`; disjoint edge operators commute. These identities
include every possible overlap of the two edge supports, so (3) is the
complete commutator, not only its three-site projection.

The first-order equation from (1) is `[D,K1]=-B_off`. Therefore

    K1=(1/4)sum_(a<b)sum_(c!=a,b)
             (1/d_ab)(1/d_ac+1/d_bc) Z_c C_ab.        (4)

This confirms both its sign and completeness. In particular K1 only
connects states by one exchange; the spectator occupations dress that
matrix entry but do not create another transfer.

## 2. Why external spectators disappear from the next coefficient

The second-order expansion of (1), using (3)--(4), is exactly

    [D,[D,K2]]=-[D,[V,K1]]-[V,B_diag].               (5)

Indeed the terms involving `[V,B_off]` cancel. The last commutator in
(5) has only single-transfer entries because B_diag is diagonal (in fact
it is a one-body diagonal operator).

Now inspect a term of [V,K1]:

    [T_xy,Z_c C_ab]
       =[T_xy,Z_c] C_ab + Z_c[T_xy,C_ab].             (6)

The second term is diagonal or a diagonally dressed SINGLE transfer:
when the edges overlap, their current/exchange commutator has that form;
when disjoint it is zero. It cannot give a Hamming-distance-four entry.

The first term can give a double transfer only if T_xy acts on the
spectator c and a fourth site d outside {a,b,c}. In that case

    [T_cd,Z_c]=-2C_cd,

and the resulting product involves precisely the quartet {a,b,c,d},
with no remaining spectator Z. All edge-pairings of a quartet are summed;
one such current product need not act on every two-occupation pattern.
If its fourth site overlaps a or b,
there are only three sites and no double-transfer entry. This exhausts
(6). Consequently the DOUBLE-TRANSFER part of [V,K1] is a sum of genuine
four-site operators with coefficients independent of all other spins.

For occupation states x=R union {a,b} and y=R union {c,d}, only operators
on exactly this quartet contribute. The external R is unchanged. Thus
this entry of [V,K1] is exactly its N=4,M=2 value, whose symbolic
rational-function calculation was already independently verified in
`2026-11-13-gaudin-complement-series.md` and its accompanying artifacts.
No finite-size extrapolation or larger-sector calculation is involved.

Writing

    Delta=eps_a+eps_b-eps_c-eps_d,
    Pi=d_ac*d_ad*d_bc*d_bd,

the verified value is

    [V,K1]_(x,y)
       =(3/4)(1/d_ac+1/d_bd)(1/d_ad+1/d_bc)
       =(3/4)*Delta^2/Pi.                            (7)

Equation (5), for Delta!=0, now gives

    (K2)_(x,y)=-(3/4)*Delta/Pi.                       (8)

This matches the returned report's bra/ket orientation. For example its
bra {1,2}, ket {3,4} orientation reverses the orientation used in the
previous complement-series calculation and hence reverses that sign.

## 3. Subset-sum coincidences and the all-input consequence

No nondegeneracy of D is required in the final statement. At g=0 the
joint charges are n_i, whose joint occupation labels are distinct. For
x!=y, their antisymmetric constraint map contains

    [n_j,[K,n_i]]_(x,y)
      =-(n_j(x)-n_j(y))(n_i(x)-n_i(y)) K_(x,y).

Taking i=j at a site where the states differ shows injectivity. Smooth
joint projectors, or a fixed separating weighted charge, consequently
give a unique analytic real antisymmetric K near g=0. This is a proof
device, not an exponentially sized construction being charged as an
algorithm. Its coefficients depend continuously on distinct site data.
Equations (2), (4) and (8) have only site-difference denominators, so the
dense-set identities extend across accidental subset-sum degeneracies.
If Delta=0, the asserted coefficient is zero; no nonvanishing of that
particular entry is inferred.

For every quartet of distinct real sites, label its two lowest sites
a,b and two highest c,d. Then Delta<0 and Pi!=0. An external R with M-2
occupied sites exists precisely when 2<=M<=N-2. Hence

    <Rab|K(g)|Rcd>=-(3/4)(Delta/Pi)g^2+O(g^3)

is nonzero throughout some sufficiently small punctured neighborhood of
zero. The remainder is O(g^3) in general: global complementation changes
external occupations, so the N=4 evenness argument must not be imported.

Every at-most-three-site operator has zero matrix element between these
states. Multiplying a single-exchange operator on either side by ANY
diagonal occupation function also leaves it with zero Hamming-distance-
four entries, as does a linear combination of such dressed exchanges. The prior real/imaginary gauge and sector-compression proof
therefore excludes both exact JOINT-generator classes on every interval
[0,G], G>0. The small interval may depend on the sites; no uniform
simulation or truncation error bound is supplied.

The accepted strengthening is genuine quartet support at order g^2 for
all bulk sectors. It does not prove a complete K2, growing support with N,
exponential representation size, a branch-specific obstruction, a gap or
integrated-norm bound, approximate-transport failure, preparation hardness,
or a full-path algorithm. Polynomial-bit evaluation of the displayed
rational coefficients is separate from paying inverse-separation-dependent
operator norms or a controlled remainder.
