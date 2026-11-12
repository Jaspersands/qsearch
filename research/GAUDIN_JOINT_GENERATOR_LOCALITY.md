# Native Gaudin joint transport needs more than three-site generators

2026-11-13. REVIEWED exact mechanism-specific falsifier. Both independent
reviews (150 and157lines) and the full paid locality report were parent-read.
No general preparation, approximation or growing-N lower bound.

Native charges are Q_i(g)=n_i+(g/2)sum_(j!=i)(Pij-I)/(eps_i-eps_j), with
distinct real/rational sites and n_i=(I+Z_i)/2. An exact universal JOINT
Hermitian adiabatic generator A must satisfy
 [Q_j,Q_i'+i[A,Q_i]]=0 for every i,j.
Writing A=S+iK with S real symmetric and K real antisymmetric separates
real and imaginary parts: K must solve [Q_j,V_i-[K,Q_i]]=0. Phase gauges
cannot alter this necessary real equation. Since the charges preserve M,
sector compression is valid even for number-nonconserving A.

At N4,M2,eps(0,1,3,7),g1/3, exact rational linear algebra gives a UNIQUE
antisymmetric K (rank15/15) and
 <0011|K|1100>=355248848800449/125250068977266446 !=0.
Every sum of operators acting on at most3sites has this Hamming4 matrix
element ZERO. Therefore no such Hermitian joint generator exists. The
current ansatz C_ab,Z_c C_ab spans the12 allowed antisymmetric entries;
its system has rank12/13 and a13term exact left-null certificate yA=0,yb=1.
The full solution is a positive control, not an efficient scalable method.

Independent verification rebuilt16dimensional matrices from native Pauli
tensor products, projected the sector, checked all576 constraints and
native commutativity as a polynomial in g, and certified simple Q_0 by
squarefree characteristic polynomial. It did not rerun the original
swap-entry code or use floating eigenvectors.

The paid Claude locality report supplied a useful stronger symbolic claim.
For ANY distinct four-site tuple, complementary occupied two-subsets v,w,
e_S=sum_(i in S)eps_i, Delta=e_w-e_v and
 Pi=product_(x in v,y in w)(eps_x-eps_y),
 <w|K(g)|v>=-(3/4)*(Delta/Pi)*g²+O(g⁴).
A single exact rational-function calculation in four independent site
variables checked the full second-order doublecommutator source, equal
to(3/4)*Delta³/Pi. Permutation symmetry gives every complement entry.
Spin complement C gives C Q_i(g) C=I-Q_i(-g), so K(-g)=-C K(g) C and
these entries are even. Joint projectors are analytic near0: the explicit
combination Q1+2Q2+4Q3+8Q4 has distinct binary-subset eigenvalues there.
This extends the formula across accidental pair-sum degeneracies of
sum eps_i Q_i without dividing by those zero gaps.

At least two of the three Deltas are nonzero for distinct sites. Thus
for each such tuple there is a punctured small-g interval with no exact
three-site universal joint generator. No uniform polynomial radius or
integrated norm bound is proved. Correct the report's claim that EACH
entry is nonidenticallyzero: Delta0 does not establish that. Nor does the
local expansion prove nonvanishing at arbitrary g; the exact1/3 certificate
is separate. No N6 or nearby locality sweep is queued.

Established scope: exact simultaneous transport of the ENTIRE joint
basis. A chosen-branch generator, approximate or higher-support control,
polynomial nonlocal description, other parameter path and the conditional
joint-dephasing route remain OPEN. Failed3locality gives no quantum
hardness or classical simulation theorem.

Evidence: audits/controls/gaudin_local_agp/; independent notes
 audits/reviews/2026-11-13-gaudin-three-local.md,
 audits/reviews/2026-11-13-gaudin-complement-series.md,
with separate exact verification scripts/results in corresponding folders.
Paid advisory report: audits/claude_runs/2026-11-13-gaudin-locality/.
Next independent constructive selection remains in
NEXT_CONSTRUCTIVE_MECHANISMS.md; no quantum implementation.

## All-size bulk strengthening

The completed OpenAI generator report and independent
`audits/reviews/2026-11-13-gaudin-bulk-double-transfer.md` were fully
parent-read. Local operator identities, rather than finite-size
extrapolation, extend the obstruction to EVERY N>=4, 2<=M<=N-2,
and every pairwise distinct real site tuple.

Write d_ab=eps_a-eps_b, C_ab=sigma_a^+sigma_b^- - sigma_a^-sigma_b^+,
T_ab=sigma_a^+sigma_b^- + sigma_a^-sigma_b^+, D=sum eps_a n_a,
and V=(1/2)sum_(a<b)T_ab. The native weighted charge is
D+gV-(g/2)M(N-M)I. Its necessary equation is
ad_(D+gV)^2 K=-[D,V]. The complete first two coefficients are

 K0=-(1/2)sum_(a<b)C_ab/d_ab,
 K1=(1/4)sum_(a<b)sum_(c!=a,b)
        (1/d_ab)(1/d_ac+1/d_bc) Z_c C_ab.

With B=[V,K0], B_diag=(1/4)sum_(a<b)(Z_a-Z_b)/d_ab and
B_off=-(1/4)sum_(a<b,c!=a,b)(1/d_ac+1/d_bc)Z_c T_ab.
The second-order equation is
 [D,[D,K2]]=-[D,[V,K1]]-[V,B_diag].
The last term has only single transfers. In
[T_xy,Z_c C_ab]=[T_xy,Z_c]C_ab+Z_c[T_xy,C_ab], a double transfer can
only arise from xy=cd with d outside {a,b,c}; [T_cd,Z_c]=-2C_cd.
Thus every double-transfer term has exactly quartet support and no
external spectator occupation. This proves reuse of the checked
four-variable symbolic coefficient in arbitrary size.

For x=R union{a,b}, y=R union{c,d}, Delta=eps_a+eps_b-eps_c-eps_d,
Pi=d_ac*d_ad*d_bc*d_bd, the exact expansion is

 <x|K(g)|y>=-(3/4)(Delta/Pi)g^2+O(g^3).

Joint occupation labels at g=0 are simple. The joint constraint map on
antisymmetric matrices is injective there, so analytic joint projectors
extend the formula across accidental subset-sum coincidences. Only site
differences remain in its denominators. The general remainder is O(g^3),
NOT the four-site complementary O(g^4). Choosing a,b the two lowest of
any quartet and c,d the highest gives Delta<0, and R exists in precisely
the stated bulk sectors. Consequently no exact at-most-three-site joint
generator exists on any full [0,G], G>0. Arbitrarily diagonally dressed
single exchanges are also excluded: their Hamming-four entries vanish.

This does NOT prove support growing beyond four sites, a complete K2,
a uniform small-coupling radius, controlled truncation, a full-path norm
bound, branch-specific impossibility or state-preparation hardness.
The forced coefficients have polynomial-bit rational formulas, but that
alone pays neither integrated operator norm nor the missing remainder.
