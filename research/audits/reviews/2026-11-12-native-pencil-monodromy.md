# Every certified cubic Lefschetz pencil has full mod-ell symplectic monodromy

2026-11-12. Focused independent source audit of the native-pencil monodromy
interface in `SURFACE_CLASSICAL_NATIVE_RECONSTRUCTION.md`, after current
`STATE.md` and the partial paid geometry report. No Git, network, API,
archive, code, or numerical experiment. Interpreter if needed:
`/opt/anaconda3/bin/python`.

**Disposition.** For EVERY cubic Lefschetz pencil on a smooth quintic
surface satisfying the stated geometric certificate, in odd characteristic
p, the geometric image on fibre H1(F_ell) is Sp_62(F_ell) for every odd
prime ell different from p. In particular this proves the candidate's
ell>53 assertion in its p>|GSp_62(F_ell)| regime. There is no further
generic-pencil certificate and no unspecified exceptional set of ell.

The decisive source is Deligne's Corollaries 4.2.7--4.2.8, after the
generic-only Proposition 4.2.6. The separate modular group input is Hall
Theorem 3.1, whose stated hypotheses here do NOT include primitivity.
This closes this geometric monodromy obligation, not the whole native
classical algorithm or its remaining complexity/composition checks.

## 1. Primary passages actually checked

* Deligne, *La conjecture de Weil II*, retained
  `audits/sources/quintic_surface_selection/deligne_weil_ii.txt`:
  weak Lefschetz 4.1.6; 4.2.1--4.2.8, physical lines 3775--3885;
  4.3.2--4.3.3 and their finite-coefficient statement, about 3918--3970;
  and the specialization discussion 1.11.1--1.11.3.
* The already rendered primary PDF page, printed page 221, was viewed
  independently at `/tmp/qsearch-deligne-427.png`. Its first hypothesis
  in 4.2.7 visibly says p=2 AND n even, not ell=2 and not every pencil.
* Hall, *Big symplectic or orthogonal monodromy modulo ell*, actual
  `audits/sources/surface_module_2026/hall_monodromy.txt`, Section 3,
  physical lines 249--302, especially Theorem 3.1. The introductory
  Theorem 1.1 and its distinction from 3.1 were also read.

The partial report's source conclusion is not accepted merely because
the report labels other steps proved. The deductions below use the
actual statements and check their finite-coefficient hypotheses.

## 2. Geometric setting and nonzero local cycles

Work over the algebraic closure of the ground field. Let X be a smooth
quintic in P3 and let H be its hyperplane class. A certified pencil in
|3H| is a pencil of hyperplane sections after the cubic Veronese
embedding. Its transverse axis has 45 reduced basepoints. Blowing them
up gives f:X_tilde -> P1; the exceptional curves give geometric
sections. The regular fibre Y has

    2g(Y)-2=(3H)(3H+K_X)=60,
    g(Y)=31,      rank H1(Y)=62.

The Euler characteristic is 55+45=100 on the blowup, so a nodal
Lefschetz pencil has r=100-2(2-62)=220 singular fibres. The certificate
must really be a Lefschetz certificate: transverse base locus, distinct
critical values, and exactly one ordinary node in each singular fibre,
including the projective base's point at infinity if it is critical.

Every one-node fibre is geometrically irreducible. It is reduced and
connected; otherwise a nonreduced component gives nonisolated
singularities, or disconnectedness contradicts connectedness of an
ample section. If reducible, its only node joins two components A,B,
with A.B=1 and A+B=3H. After relabeling, a=H.A satisfies 1<=a<=7.
Then A^2=3a-1, whereas Hodge index gives A^2<=a^2/5. The resulting
inequality a^2-15a+5>=0 fails throughout 1<=a<=7.

Fix ell!=p and put Lambda=F_ell. The local vanishing-cycle sequence
for an irreducible one-node fibre Y_s contains

    H1(Y_s,Lambda) -> H1(Y,Lambda) -> Lambda(-1)
       -> H2(Y_s,Lambda) -> H2(Y,Lambda) -> 0.            (1)

The last nonzero map is an isomorphism: both groups have the fundamental
class of one reduced irreducible curve, and specialization preserves
degree. Equivalently a smooth point of Y_s lifts over a strict local
trait and supplies a degree-one class on both fibres. Thus the middle
functional to Lambda(-1) is surjective. Picard--Lefschetz identifies
it with pairing against the vanishing cycle delta_s, up to a unit.
Hence delta_s is NONZERO modulo ell for every ell!=p. Its compatible
Z_ell-cycle is primitive in the free H1(Y,Z_ell) lattice.

This uses the local theory with finite coefficients, which Deligne
4.2.1 explicitly states, not a rational-coefficient invariant-cycle
claim reduced without justification. Local inertia acts by

    T_delta(lambda)(v)=v+lambda <v,delta> delta.          (2)

The reduced inertia image is a genuine nontrivial transvection group,
of order ell; its nonidentity elements have drop one and determinant
one. Over the geometric field the Tate-valued pairing can be trivialized
once, yielding the perfect alternating pairing used below.

## 3. Finite-coefficient spanning, without mod-ell hard Lefschetz

Use Deligne's definition 4.2.4: Delta is the set of vanishing cycles
obtained by ALL permitted paths from the reference fibre to a branch
trait, including monodromy transports and signs. Write Ev for their
F_ell-span. Proposition 4.3.3 is explicitly a Z/m-coefficient statement
and gives

    Ev^perp = image[H1(X,F_ell) -> H1(Y,F_ell)].          (3)

Weak Lefschetz with finite coefficients for the smooth hypersurface
X in P3 gives H1(X,F_ell)=H1(P3,F_ell)=0. The pairing on H1(Y,F_ell)
is perfect, so (3) implies

    span_(F_ell)(Delta mod ell)=H1(Y,F_ell).             (4)

In particular no surface hard-Lefschetz isomorphism modulo ell, and no
assertion that torsion-freeness implies such an isomorphism, is used.

There is also the direct section/Leray check requested in the task.
The local calculation (1)--(2) gives R1 f_*Lambda=j_*L for
L=R1 f_*Lambda|U. The low-degree Leray sequence contains

    H1(X_tilde,Lambda) -> H0(P1,R1 f_*Lambda)
       -> H2(P1,Lambda) -> H2(X_tilde,Lambda).

The first group is zero: blowing up points does not change H1. The
last map is injective because any exceptional section splits f^*.
Therefore H0(U,L)=0. Invariants are the intersection of the orthogonals
to ALL transported local cycles, by (2) and inertia generation, so
their vanishing again gives (4). The section is geometric; no F_p-
rational basepoint is being supplied to an algorithm by this proof.

Do not replace Delta by one ARBITRARILY transported vector for each
of the 220 nodes. Such representatives need not themselves span:
changing the paths conjugates them. A distinguished system that
generates the monodromy would suffice, but is unnecessary here.
The source's all-paths definition and (3) avoid this quantifier error.

## 4. Conjugacy for every certified pencil, integrally and modulo ell

Proposition 4.2.6 is indeed stated for a generic pencil. It is not the
last source statement. Corollary 4.2.7 adds an extra sufficiently-general
pencil hypothesis ONLY in the exceptional case

    ground characteristic p=2 AND fibre dimension n even.

Here the fibre dimension is n=1, although the surface has dimension
two. Thus 4.2.7(i) applies to every Lefschetz pencil under consideration.
It says that the homomorphisms Z_ell(1) -> the monodromy group in (2)
are conjugate. Its proof explicitly passes from the generic pencil to
the stated general case by Section 1.11. Corollary 4.2.8 consequently
states conjugacy up to sign of the cycles in rational ell-adic H1.

The acting group here is the ACTUAL image on H1(Y,Z_ell), as defined
in 4.2.5, not its rational Zariski closure. Thus the conjugating element
g preserves the integral lattice. One can see the precise reduction
without any denominator-clearing assumption: conjugacy of the
homomorphisms with the same parameter lambda gives

    N_(g delta)=N_epsilon,
    N_v(w)=<w,v>v.

Over Q_ell, equality of these nonzero rank-one operators implies
g delta=c epsilon and c^2=1, hence

    g delta=+epsilon or -epsilon.                       (5)

Both sides are integral, and H1(Y,Z_ell) is torsion-free. Equality in
its rationalization is therefore equality in the lattice. Its reduction
is exactly H1(Y,F_ell): H2(Y,Z_ell) is also torsion-free, so there is
no extra universal-coefficient term. Reducing (5) gives conjugacy up
to sign under the ACTUAL group G_ell. The primitive local calculation
ensures these reduced vectors do not become zero.

Primitivity is used for nonvanishing after reduction, not to smuggle a
rational conjugator into an integral group. The latter is already paid
by 4.2.7. Conjugacy of the parameterized homomorphisms is also stronger
than merely conjugacy of their image subgroups, which could leave an
undetermined scalar in the root vector.

Thus Delta mod ell is a single G_ell-orbit up to sign, and spans the
whole 62-dimensional space by (4), for EVERY ell!=p.

## 5. Irreducibility and Hall's actual finite-group theorem

Deligne 4.2.5 gives topological generation of monodromy by the
transported inertia images. After reduction, G_ell is therefore
generated by nontrivial transvections from (2). It is contained in
Sp(V), with V=H1(Y,F_ell).

Let W be a nonzero G_ell-stable subspace. If every delta in Delta
were orthogonal to W, (4) and the perfect pairing would force W=0.
Hence there are w in W and delta with <w,delta>!=0. The difference

    T_delta(1)w-w=<w,delta> delta

shows delta belongs to W. By (5), W then contains all transported
cycles up to sign, and (4) gives W=V. Thus G_ell is irreducible over
F_ell. No assumption of absolute irreducibility is needed here.

Hall Section 3 fixes an ODD PRIME ell. In its alternating case
Theorem 3.1 assumes an irreducible subgroup, a generating set S and
a subset S_0 with three explicit drop/order/count conditions. Take

    Hall's r=1,
    S=the nonidentity transvection generators above,
    S_0=empty.

Every generator has drop one and is a pseudoreflection; its order ell
is also prime to (r+1)!=2. The count condition is 0<=dim V. The pairing
is alternating and the group contains a transvection. All hypotheses
of Hall 3.1 hold, and its conclusion is

    G_ell=Sp(V)=Sp_62(F_ell).                            (6)

The theorem has no separate primitivity premise. That premise occurs
in the introductory, weakened Theorem 1.1; conflating the two creates
a spurious missing assumption. Even if one uses 1.1, primitivity is
easy here: if a transvection of odd prime order ell moved blocks in a
direct-sum imprimitivity decomposition, a nontrivial block cycle would
have length ell. On ell blocks of dimension h it would have drop at
least (ell-1)h>=2, contradicting drop one. Thus every generating
transvection fixes every block, contradicting irreducibility unless
there is just one block. This auxiliary argument is not needed by 3.1.

All inputs were checked for each ell separately. This proves (6) for
every odd ell!=p, and hence the requested every ell>53 statement.
Rational Zariski density or openness alone would not have justified
this uniform finite-field conclusion; neither is being used as a
substitute for (1)--(5) and Hall's theorem.

## 6. Scope and disposition of the partial paid report

The following claimed gaps are rejected:

* Its assertion that the retained source supplies conjugacy only for
  generic pencils stops at 4.2.6 and misses 4.2.7--4.2.8. No additional
  Katz-open-set or complement-fundamental-group certificate is needed
  for the fibre-dimension-one Lefschetz pencils here.
* Its assertion that the invoked Hall criterion leaves a separate
  primitivity hypothesis uses the introductory theorem instead of
  actual Theorem 3.1. The latter's hypotheses are all verified above.
* Its phrase that "the 220 cycles span" needs a path/generator
  qualification. The proved source statement uses all transported
  vanishing cycles; this is sufficient and introduces no computation
  of paths or cycles as algorithmic advice.

The report's local nonzero-cycle argument, section/Leray idea, and
Hodge-index irreducibility calculation are consistent with the verified
proof above. Its last truncated section supplies no further conclusion.
No other source or running-time claim of that partial report is
promoted by this focused audit.

The native certificate must still establish an actual Lefschetz pencil;
calling a pencil merely generic is not a certificate. Given that
certificate, the monodromy conclusion is direct in the native odd
characteristic as well as in characteristic zero. Therefore the
candidate's p>|GSp| condition is sufficient but is not needed by THIS
monodromy proof; it may remain for the other already scoped interfaces.
This review does not change that regime or re-prove the bounded-degree
random-pencil search, integer lifting, arithmetic height chain, or final
reconstruction. It adds no hidden monodromy basis, exceptional-ell
list, or group-recognition oracle to those interfaces.
