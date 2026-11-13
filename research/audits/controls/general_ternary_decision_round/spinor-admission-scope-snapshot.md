# Native indefinite ternary isometry through spinor genera

Current scope (Nov13): GENERAL native DECISION is reviewed WRITTEN under the
retained complete GRH assumptions; see DYADIC_NONFULL_SPINOR_TRANSPORT.md.
Historical OPEN paragraphs below are superseded for that decision contract.

2026-11-07. Reviewed admission pass COMPLETE; full native route PARKED. No full algorithm,
novelty, separation, hardness or quantum execution is established.

## Scientific question and independent choice

Can integral-isometry DECISION for arbitrary ternary forms over a growing
number field be compiled into polynomial quantum BIT/gate time, under the
existing explicit GRH arithmetic assumptions, using the actual spinor-genus
ray-class quotient without a supplied rational transporter?

Native input: an explicit totally real number field K of charged growing
degree with expanded maximal-order basis/table, and two nonsingular integral
3-by-3 symmetric Gram matrices A,B over O_K. Both are indefinite at some
real place; differing signatures/genus invariants may be rejected. Decide
whether U^T A U=B for U in GL_3(O_K), failure at most eta. No rational
isometry, common ambient embedding, local transporter, local spinor groups,
class/unit group, ray-class group or factored exceptional support is advice.
A witness, short witness, positive-definite LIP, Hermitian HAWK and arbitrary
rank are different contracts and are not asserted here.

Fresh STATE/TRAPS and corpus been-tried/baselines preceded primary reading.
An independent selection compared this endpoint with local Kummer/2-Selmer
and growing-degree Legendre recovery. Local HALF still lacks a uniform
actual-point conditioning operation; Legendre has no new paid receiver.
The present candidate has a concrete finite arithmetic endpoint in an actual
primary source. Corpus no-match is not novelty or hardness evidence.

Mechanism: pay rational ternary isometry via even Clifford/quaternion
arithmetic; compare local integral genera and obtain local transporters;
compute local proper spinor-norm generators; form the finite ray-class
quotient from Kirschmer Theorem5.4.6; decide its obstruction. Corollary5.4.10
identifies spinor genus with class for indefinite rank>=3. Since rank3 is
odd, -I is an improper integral automorphism, so ordinary/proper classes
coincide. Known quantum factoring and class/unit arithmetic would replace
the expensive arithmetic in the SAME classical reduction.

Target polynomial in all native bits and log(1/eta), without class-number
or field-degree constants hidden in the exponent. Strongest classical
baseline is the same spinor/ray-class algorithm with classical class/unit
arithmetic, plus genus tests, lattice reduction and existing indefinite-LIP
attacks. No lower bound follows from that comparison.

Resource/proof gates: obtaining and evaluating a rational transporter with
known polynomial-size exceptional support; local dyadic generators without
2^[K_p:Q_2] enumeration; local transporters at paid finite precision; complete
ray-class/unit data with compact residues and certified signs; capped clocks.
An abstract compact CSA map does not automatically give its bad primes.
A common ambient space in the source is not free native-input data.

## Actual source scope

Frozen Kirschmer2016 Habilitationsschrift, source.json under
 audits/sources/spinor_genus_admission/, actual sections5.1 and5.4.
https://math.uni-paderborn.de/fileadmin/mathematik/AG-Computeralgebra/Publications-kirschmer/Definite_quadratic_and_hermitian_forms_with_small_class_number.pdf

Theorem5.4.5 assumes lattices inside a COMMON quadratic space and local
proper isometries. Theorem5.4.6 uses the ray modulus with finite factors
p^(1+ord_p4), infinite anisotropic places, local spinor generators and
ray-class squares. Corollary5.4.10 uses strong approximation in the
indefinite case; it is not a polynomial-time constructive transporter claim.
Odd local spinor norms are explicit in5.4.4. Dyadic computation refers to
Beli2003. Primary ePrint2024/1475 and2026/890 fetches returned403; their
abstracts/search descriptions are leads only, not admitted theorems.

## Cheapest classical falsifier: ordinary class group is insufficient

For prime p=17, and uniformly for primes p=17 mod72, let

    A=diag(1,p^2,-p^4), x=(1,0,1), q=3,
    P=[[3,0,1/3],[0,1,0],[0,0,1/3]],
    B=P^T A P=[[9,0,1],[0,p^2,0],[1,0,(1-p^4)/9]].

The vectorx is primitive mod3 and its norm1-p^4 is divisible9. The
3-neighbor of L=Z^3 formed from {y:B_A(y,x)=0 mod3} and x/3 is exactly
P Z^3. Both Gram matrices are integral, determinant -p^6 and signature(2,1).
Kirschmer Lemma5.4.9 supplies a local proper transporter with spinor norm3;
other local lattices are equal, so they are in the same genus.

Atp, the Jordan lines have valuations0,2,4 and unit coefficients1,1,-1.
All are squareclasses1 sincep=1 mod4; Theorem5.4.4 makes theta(L_p) the
square subgroup. At every other odd prime the lattice is unimodular, so
theta is units times squares. The quadratic Hecke character of Q(sqrt p),
conductorp, is trivial at infinity and at2 becausep=1 mod8. It kills all
these local spinor groups and the diagonal Q* by reciprocity. Yet it takes
value (3/p)=-1 on the neighbor idele, sincep=5 mod12. Thus L and PZ^3
are in different proper spinor genera, hence are not integrally isometric.
Odd rank makes this also an ordinary-isometry obstruction.

This all-family proof is independently CLOSED and parent-read. It rejects
replacing the ray-class quotient by the ordinary class group, which is
trivial for Q. It does not reject the full ray-class algorithm. The exact
p17 control checks the concrete matrices/neighbor/characters only; it does
not infer nonisometry or an asymptotic theorem from finite data.

## Constructive local dyadic gate

For a specified dyadic prime P of the expanded native number field, proper
spinor-norm GENERATORS of an arbitrary integral ternary lattice have a
classical polynomial-BIT compilation. This is a derivation from Beli's actual2001
thesis formulas and Voight's uniform local Hilbert-symbol algorithm; it is
not a claim that either source states the combined complexity theorem.
The proof and all source locators are in the CLOSED review
 audits/reviews/2026-11-07-spinor-genus-sources.md.

First split the Gram matrix by a minimum-valuation diagonal entry, or by a
minimum off-diagonal binary block when both its diagonals have larger
valuation. The determinant of that block has exactly twice the minimum
valuation. Norm generators come from the three basis vectors or three pair
sums. Beli Lemma1.4.5 repairs a bad binary summand by O(x+z)+Oy and an
orthogonal complement (or dualization). Lemma1.4.6 decreases the NUMBER of
bad summands, giving at most3 repairs. The resulting good BONG uses only a
constant number of matrices of size at most3 over the ORIGINAL K, so exact
expanded coefficients retain polynomial bit height. This avoids an assumed
unbounded p-adic pivot/precision search.

Write e=v_P(2), f=residue degree, ef<=degreeK. Choose pi in P outsideP²
from an integral basis and residue F2-basis lifts b_l. The squareclasses
are generated by pi and1+pi^j*b_l for1<=j<=2e,1<=l<=f. There are1+2ef
entries. Successive unit quotients are additive residue fields; residue
units have odd order and U_(2e+1) consists of squares. A full Hilbert-pairing
matrix supplies relations and coordinates. Quadratic norm groups are linear
kernels; products/intersections are F2 spans/intersections. Forr>=1 the
unit subgroup U_r is spanned by generators withj>=r. A unit's defect is
the largest such filtration level containing its class, or infinity if
square. Exact valuations are bounded by expanded field-norm heights; unit
classes need relative precision2e+1 after normalization.

Apply Beli's two binary G formulas to the adjacent BONG ratios. His actual
property-A theorem applies when R1<R3, with extra U_floor((R3-R1)/2).
When R1=R3 use the separate units-versus-full theorem, not that formula.
Keep two guards: Beli's U_0 means the WHOLE squareclass group, and the
exception a in(-1/4)O*² gives only UNIT classes. Parent visually inspected
the scanned PDF physical pages40,81,123 (printed29,70,112); the exact case
transcription is retained in the dyadic_compilation Claude input packet.

Voight Theorem6.1 and Algorithms6.2–6.6 actually pay polynomial BIT Hilbert
symbols uniformly in number-field degree. The retained erratum only changes
Algorithm3.22, not these algorithms. Prime identification/factorization and
the expanded maximal-order data remain charged input/preprocessing. No
all-squareclass enumeration, local root/output oracle, or full rotation
matrix construction is being supplied by this generator operation.

Two new exact controls are CLOSED/PASS under
 audits/controls/spinor_genus_admission/. The neighbor control verifies the
p17 matrices, HNF lattice indices and characters; one JSON integer repair.
The separate dyadic_control verifies Hilbert ranks4 and5 and filtration
ranks(3,1,0) and(4,3,3,2,2,1,0) in actual e1f2 and e3f1 fields; one Sage
residue-vector API repair. These are finite component checks only; no
uniform theorem or nonisometry is inferred from them. No old control rerun.

## Remaining full-input gates and paid-agent disposition

Global rational/common-ambient transport with a known, affordable exceptional
prime support is still OPEN. A compact CSA map or a compact rational
isometry does not by itself pay factoring its coordinate sums/denominators.
Local integral transporter OFFSETS are a separate gate. Beli chapter2
assumes nested lattices and computes a spinor subgroup for an inclusion;
it does not construct a transporter or the offset of a nonnested
same-covolume isometry coset. Scaling to make lattices nested changes that
problem and would require a new reduction.

Claude bundle2026-11-07-spinor-transport-support terminated with provider
stop_reason=refusal, EMPTY response, process reaped. Estimated reported
usageUSD0.034984; no findings or retry by rephrasing. A DISTINCT local
proof attack,2026-11-07-spinor-dyadic-compilation, exhausted16384 tokens
with an EMPTY report; process reaped, no findings or retry. Its reported
estimate isUSD0.844160; the two pass estimates totalUSD0.879144. Aggregate
74 nonpartial estimatesUSD58.116572/37 completed reports is not a balance.
Two older timeouts have UNKNOWN billing; their partial counters remain
excluded. Neither paid request supplies mathematical evidence here.

No full native algorithm, novel quantum primitive, classical separation,
HAWK/DEFI attack or general impossibility is claimed. Reopen only with a
paid common-ambient/relative obstruction operation and local offset method,
then compose full ray-class/error clocks. Otherwise reselect independently;
no generic isometry backend or nearby local formula campaign is queued.
Scoped milestone: audits/controls/spinor_genus_admission/checkpoint.json.
Core/source reviews are CLOSED, parent-read, and two new exact controls are
frozen. No full suite, registry/site, quantum backend or Git operation.
Next pass starts with independent selection. For re-entry the concrete
experiment is to derive the relative spinor obstruction from JUST native
Gram matrices and check that it separates the retained3-neighbor pair,
without factoring an unexpanded compact sum or supplying an ambient map.
That finite check is necessary only; all growing-degree resource gates
would still require proof.
