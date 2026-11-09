# Compact integral matrix similarity

2026-11-07. REVIEWED WRITTEN compact-output composition. Previous folded-chain pass
was PROGRESS; STATE/TRAPS matched its complete heading. Corpus been-tried,
then actual published BHJ/BJ08 sources and corpus baselines preceded admission.
No novelty, separation, expanded-output, short-witness or execution claim.

## Selected native question and comparative admission

Input: arbitrary growing A,B in Mat_n(Z), all entries in binary. Output NO,
or a polynomial-size arithmetic straight-line description of an INTEGER matrix
C with BC=CA and det(C)=+/-1. Target bounded-error quantum polynomial BIT/gate
cost in the native input and log(1/eta), under conservatively retained GRH,
using the published complete compact unit/PIP routines. ABORT counts against eta. No supplied
centralizer, Wedderburn map, maximal order, unit group, target ideal or witness.
Expanded C is excluded by the already-proved minimum-output family in
INTEGRAL_SIMILARITY_OUTPUT_SIZE.md; this is an explicit output contract, not
renaming an exponentially large matrix oracle. Consumers wanting expanded
entries must pay expansion. Positive certificates must be structural.

The proposed operation is compact conductor descent with a paid local-residue
map and a determinant character computed from SMALL lattice indices. It uses
known quantum arithmetic, not a new quantum primitive. Source BHJ Cor9.16
already states a quantum algorithm, but does not itself close the representation
issue. Source Algorithms8.3/9.13 and their proof obligations are checked directly.

Independent alternatives rejected before admission:
- Kronecker multiplicity sampling: Young-diagram native labels; desired sample
  law already supplied by Bravyi et al2302.11454. Proposed classical RSK
  composition already refuted at n=4 in this repo. No new normalized operation.
- Arbitrary noisy stabilizer-basis learning: copy input, output hidden frame;
  generalized spectral filtering lacks paid inverse-purity/gap access. Existing
  learners retain these promises; no new operation or general impossibility.
- Full growing-degree Galois-group reconstruction: explicit rational polynomial,
  output labeled permutation generators. Frobenius/class-unit routines do not
  provide a polynomial-size closure/action or coherent receiver. No admission.

The compact similarity repair instead removes an explicit obstruction to a
motivated complete problem. Strongest classical baseline is the SAME published
arithmetic reduction with classical unit/PIP/class-group/finite-ring routines.
The corpus names index calculus; no classical hardness or quantum separation
is inferred. The prospective asymptotic gain is replacement of the classical
number-field arithmetic bottleneck by the known quantum primitives; no matched
classical lower bound or new speedup is established. Existing rational conjugacy,
HNF/SNF and local module algorithms
are fully reused. No tuple extension: arbitrary tuple centralizers need not
satisfy the split-component promise (AMITSUR_ARITHMETIC_REUSE_AUDIT.md).

## Compact constructor

1. Classically compute rational similarity D, the centralizer E=C_Q(B),
   Omega=C_Z(B), I=C_Z(A,B)D^-1 and the explicit semisimple quotient rho.
   Actual BHJ Prop9.11 pays polynomial-height matrix-over-field coordinates
   for ONE matrix, including nonsemisimple B. All original lattice data are
   expanded; no arbitrary CSA compact splitting map is assumed.
2. In rho(E), use the BHJ maximal-order/local-freeness/conductor route.
   Nice-order conjugation S and expanded Steinitz row matrix W are computed
   before compact arithmetic. Fix the BHJ convention S*M*S^-1=M_a; all
   modules below use the same conjugation; for matrix size1 choose a=O.
   BJ08 rank-one Cor5.4 gives
   beta_nice=diag(1,...,1,gamma)W, with (gamma)=a*b; inverse is
   W^-1 diag(1,...,1,gamma^-1). Only gamma is large/compact. Source AppendixA
   pays the small Steinitz work. In original coordinates use
   beta0=S^-1*beta_nice*S. No elimination on compact entries.
3. Use a proper conductor uniformly, e.g. g=2*g_central, f=gM, to include
   maximal-order components and the empty-prime-set edge case. Pay factor2.
   The local normalization xi is expanded polynomial-height. Set X1=X0*xi,
   beta1=beta0*xi. Compact units and finite-group binary exponents remain
   powerproducts. Actual BHJ Section7 lifts finite SL residues to a polynomial
   product of expanded elementary matrices v. Field-unit lift u is a nice-order
   conjugate of diag(epsilon,1,...,1), with epsilon a compact unit.
4. Return g0=(v*u)^-1 beta1 xi^-1=(v*u)^-1 beta0 in the original projected
   lattice. Do not undo xi twice. Before finite-ring operations, evaluate compact
   atoms with the valuation-normalized procedure below. Individual leaves may
   be nonunits despite a final unit; fractional coordinate sums require small
   denominator enlargement and exact division in finite lattices, not inversion
   of a denominator modulo the conductor.
5. Lift g0 with a precomputed Z-linear section rho(I)->I, obtained from expanded
   HNF/SNF bases. Evaluating its fixed rational-linear formulas gives a compact
   alpha in I. C=alpha*D is therefore integral and intertwines structurally.
   No general compact-sum equality or integrality oracle is used.
6. The original representation's determinant character is
   det_Q(alpha)=product_(i,j) Norm_(K_i/Q)(det rho_ij(alpha))^j,
   where j is the Jordan-block length, NOT matrix-block size. It follows from
   the f_i-adic filtration. Radical lifts do not change it. Since det(v)=1 and
   det(u) is a field unit, each absolute norm equals that of beta0. Compute it
   from the expanded row-lattice covolume e11(M X0)/e11(M); alternatively its
   d_i-th power is the expanded full-lattice covolume ratio (M X0)/M. Exact
   rational root extraction is polynomial and checked, never a floating estimate.
   Multiply by |det D| and weights j. This gives |det C| without expanding C.
   A structurally valid run gives a positive integer;1 means unimodular.
   Source Thm3.4/Prop9.12 pay NO otherwise. Invalid intermediate certificates
   or exhausted clocks give ABORT, not a false mathematical NO.

The exact joins are proved below and independently reviewed. Falsifiers: uncharged
large-unit elimination, improper conductor edge case, nonunit residue leaves,
wrong determinant exponent/index orientation, failure of lattice lift or
unit completeness, or a matching classical primitive. An ACCEPT label or
passing finite example proves none of the full contract.

## Local residue lemma and prior reuse

COMPACT_RESIDUE_CONDUCTOR_DECISION.md already proves this product-residue
interface and a COMMUTATIVE coprime-conductor decision composition. Its
enlarged-denominator HNF method and the denominator-ideal method below are
alternative local evaluations. This pass reuses that result; the full matrix
witness, radical lift and determinant test are the additional composition.

Input: number field K of arbitrary growing degree by explicit polynomial/table,
expanded maximal order O with polynomial-bit arithmetic data; a nonzero integral
ideal a in HNF with supplied prime-ideal factorization product P^k; nonzero
expanded atoms x_i∈K and binary signed exponents e_i. No expanded value alpha=prod
x_i^e_i is available. Complexity target polynomial in ALL these input bits.
Output: if alpha is P-integral for every P|a, its residue in the product O/P^k
(and CRT class in O/a), else identify a P with negative valuation.
This is local integrality at modulus primes, not a test of global integrality.
Whole native algorithm pays factoring and prime-ideal decomposition, not this lemma.

Unconditional classical procedure for each P^k:
1. Compute v_i=v_P(x_i) from expanded fractional principal ideals. These are
numerically polynomial-bounded in atom/field input bits by numerator/denominator
norm-height bounds, despite e_i being enormous. No factoring alpha.
2. Choose pi∈P\P² from an expanded Z-basis of P: some basis element is outside
P². All arithmetic and pi heights are polynomial in explicit lattice input.
3. Expand u_i=x_i*pi^(-v_i). The exponent |v_i| is polynomial, so coefficients
stay polynomial-bit. u_i has v_P=0. Form denominator ideal
D_i={b∈O: b*u_i∈O} by rational linear algebra/HNF. Since u_i is P-integral,
D_i not contained in P. Pick a basis element b_i∈D_i\P, put a_i=b_i*u_i∈O.
Thus u_i=a_i/b_i with b_i a unit mod P^k, even if its original rational integer
denominator was divisible by the rational prime under P.
4. Reduce u_i mod P^k, use binary modular powering (negative e_i allowed because
u_i is a local unit), and compute v=sum e_i v_i as a binary integer. If v<0,
return negative valuation; if v>=k, local residue0; otherwise multiply the unit
product by pi^v (0<=v<k). Since P^k is expanded, k<=log2 Norm(P^k) is charged.
5. CRT the local residues. This handles ramified and dyadic primes, not only tame
or unramified ones. Exact HNF/unit tests operate on expanded polynomial-height data.

Cheap falsifier motivating this: in Q(sqrt2), prod 2^E*(sqrt2)^(-2E)=1 has only
nonunit leaves at the ramified prime. Final-unit status does not license reducing
leaves then inverting them. Also a P-unit may have a rational denominator divisible
by the rational prime, so simply clearing an integer denominator is insufficient.

Native application (not part of this lemma's proof): repair BHJ compact integral
matrix similarity. A,B∈Mat_n(Z), output NO or compact C∈GL_n(Z) with BC=CA under
existing GRH compact class/unit/PIP primitives. Preserve small-lattice computations,
powerproduct units, finite conductor residues, and local SL lifts; avoid general
compact-sum equality or expanding C. Existing exponential-output family and actual
BHJ Cor9.16 do not by themselves establish the repair. No novelty or speedup claim.


## Structural certification and scope

To verify compact PIP/unit claims positively, factor norms/denominators of the
POLYNOMIAL-HEIGHT atoms, decompose their principal ideals, and retain checked
prime-ideal factorizations. Huge exponents enter only binary valuation-vector
sums. This certifies (gamma)=a*b and (epsilon)=O without expanding ideal powers
or compact values. Construction pays integer factoring; checking the supplied
prime/ideal factors is classical. Full unit/PIP completeness remains needed
for NO, and is not inferred from these positive checks.

Finite conductor relations and the elementary lift certificate establish
membership/generation of g0; the fixed lattice section establishes integral
intertwining. Small lattice-index determinant characters establish |det C|=1.
The output grammar is small rational constants, expanded field tables/atoms,
binary powerproducts, and rational-linear/matrix arithmetic. Negative powers
invert only small atoms or use the explicit beta/u inverse formulas. There is
no inversion or Gaussian elimination on an unrestricted compact expression.
No general arithmetic-DAG integrality/PIT, short generator or expanded witness.

## Exact joins: descent, radical and determinant

Write J=X0*xi and beta1=beta0*xi. The paid finite-group calculation produces
abar in (Lambda/f)^* and u in M^* such that nr(beta1*abar)=nr(u) mod g.
Section7 gives v in SL(M) with v=beta1*abar*u^-1 mod f. Hence
alpha1=(v*u)^-1*beta1 belongs to M and alpha1=abar^-1 mod f. Thus
Lambda*alpha1+f=Lambda and M*alpha1=M*J. BHJ Lem4.2 applied to both
lattices yields Lambda*alpha1=M*J intersect Lambda=J. Multiplying right by
xi^-1 proves Lambda*g0=X0. This proves membership as well as generation;
no compact-entry membership test is hidden.

The surjection rho:I->X0 is a map of expanded free Z-lattices. HNF/SNF
preimages give a Z-linear section: fixed rational-linear coordinate formulas
which are integral on X0 by construction. Apply it to g0. Every resulting
alpha is in I, so C=alpha*D is an integral intertwiner. A general rational
section without this lattice property would be insufficient.

Over a splitting field of f_i, the f_i-primary summand has Jordan modules
of lengths j with multiplicities d_ij. An endomorphism preserving this module
has, on the associated filtration, the same diagonal d_ij-by-d_ij factor
j times; cross-length maps are triangular in the length filtration. Therefore
its determinant is product_j det(rho_ij(alpha))^j at each embedding. Taking
all embeddings gives the stated rational norm character. Equivalently the
radical acts trivially on the simple composition factors; multiplying by
1+radical changes no determinant. This proves lift independence, including
nonsemisimple inputs.

For each block right multiplication by beta0 takes the expanded row lattice
e11*M bijectively to e11*(M*X0). Its Q-determinant is Norm(det beta0).
Consequently the POSITIVE covolume ratio is |Norm(det beta0)|, with target
covolume divided by source covolume. On the full matrix lattice the ratio is
its d_ij-th power. Both calculations involve expanded small lattices; exact
rational roots may be used as a check, with numerator/denominator verified.
Units u have absolute norm1 and v has determinant1, so |det C| is
|det D| times these ratios to the powers j. Use ORIGINAL X0, not X1, unless
the xi determinant is explicitly canceled. The answer is a positive integer
on structurally valid data. If it is1 the witness is unimodular. If not1,
BHJ Thm3.4 and Prop9.12 show that no other lift or generator could have
supplied an isomorphism. This avoids a general compact determinant oracle.

## Fractional sums and finite-lattice residues

Every expression needing a conductor residue is a polynomial-size sum of
small coefficients times gamma, epsilon, or their explicit products, in each
field component. Their principal fractional ideals are known: (gamma)=a*b
and (epsilon)=O. A polynomial-bit integer D clears all term ideals and the
expanded lattice M into T=product Mat_d(O_K). Choose small positive integers
l,q with l*T contained in M and q*M contained in f, using expanded bases.
Then evaluate each integral term of D*z modulo D*l*q*T using the local
product lemma, and add. If r is the resulting expanded representative, then
D*z-r is in D*l*q*T, which is contained in D*f and D*M. Since z is in M,
r is in D*M. Exact division of the SMALL representative by D and reduction
in M/f yields z mod f. No inverse of D modulo f is taken. Polynomial bit
length of D follows from the expanded coefficient and gamma ideals; huge
unit exponents do not affect it. Newly introduced modulus primes are factored
and charged. This guard applies to the structured sums here, not arbitrary
compact arithmetic circuits or unknown additive cancellation.

## Reused quantum primitive and finite error clocks

Biasse--Song, corrected2510.02280v2: actual Theorem1, complete-generation
Theorem5, compact-output Proposition7 and PIP Algorithm6 are reused; see
ARBITRARY_DEGREE_NUMBER_FIELD_REGULATOR_BARRIER.md and the retained PDF
research/literature_cache/arxiv_2510_02280v2.pdf. Its SHA256 is
037f365f75cd9c8d00870fe20ca3d04a78c2b23831cf91e5b53d7d6c31d58a4a.
The native theorem here retains the conservative GRH hypothesis. The source
S-unit and maximal-order PIP statements themselves do NOT require GRH; its
class-group statement does. No short-generator or expanded-output theorem
is imported. No line-by-line reproof of the quantum number-field source is
claimed.

In fact PIP can be implemented with S equal to the support of the expanded
target ideal: factor its numerator/denominator, compute complete compact
S-units, and solve the integer valuation system by HNF/SNF. The same small-
atom valuation method verifies each principal ideal. A polynomial-bit integer
solution gives a compact generator; a missing solution is NO only on the
complete-generation event. Units use S empty and INCLUDE torsion. There is
no need to assume supplied class-group data or a complete factor base.

All field degrees, discriminant lengths, lattice ranks, ideal norms' lengths,
coefficient heights and modulus lengths are polynomial in native input length.
The BHJ small-lattice front end supplies these bounds; algebra/lattice dimensions are
at most n^2, normal-form matrices have polynomial dimensions, and all field
factors arise from the characteristic polynomial.
The compact factors and binary exponents have polynomial length by the
number-field source and integer linear algebra. Thus the written BIT/gate
cost is polynomial in native input and log(1/eta), with potentially enormous
polynomial constants/exponents. No practical resource claim follows.

Allocate eta over the polynomial number of quantum arithmetic calls,
finite-field random calls and classical weak-approximation trials. Verify
factoring, prime ideals, principal ideals and returned units exactly. Capped
Las Vegas calls are restarted independently a logarithmic number of times;
exhaustion or malformed data is ABORT and counts as failure. For complete
unit/S-unit lists, union polynomially many independent VERIFIED lists: one
complete successful run makes the union complete, and no extra verified
S-unit enlarges beyond the target group. This amplifies completeness without
comparing noncanonical bases or asserting a cheap completeness certificate.
Use the source error/precision analysis and ordinary finite circuit
compilation, with total error union-bounded by eta. Mathematical NO branches
are source Steps5/6/10, rational nonsimilarity, or the final determinant test;
a false NO caused by incomplete primitives is included in eta. Every accepted
positive output has the structural certificate described above, independently
of completeness and GRH under the explicit field/algebra promises.

## Reviews, exact falsifiers and Claude dispositions

Actual-source review CLOSED: audits/reviews/2026-11-07-integral-similarity-sources.md.
Core review CLOSED: audits/reviews/2026-11-07-compact-integral-similarity-core.md.
Parent checked both reviews against the proof/source and reconciled all joins.
Primary PDFs and source hashes are
under audits/sources/compact_integral_similarity/. BHJ Prop9.11 and Algorithms
8.3/9.13, Lem4.2, Thm3.4, Prop9.12, Sections6/7 and AppendixA were checked;
BJ08 Lem5.2, Prop5.3 and Cor5.4 supply the rank-one row formula. Cohen is not
claimed read or used to justify compact operations. BHJ Cor9.16 is existing
prior art; this pass is a representation repair, not a novel quantum result.

One exact Sage run, audits/controls/compact_integral_similarity/control.py
and result.json, PASS. It checks dyadic nonunit leaves with E=2^200+1;
enlarged-modulus division of ((3+2sqrt2)^E-1)/2 against a binary geometric
sum; split11 P-unit denominator repair and the opposite negative valuation;
and a dimension10 mixed-Jordan commutant. The last determinant is -136 and
unchanged by a radical term; the wrong multiplicity exponent gives578.
These are finite CLASSICAL falsifiers only. No full similarity solver or
quantum execution. The old Pell output-size controls were not rerun.

Claude audits/claude_runs/2026-11-07-integral-local-residues completed,
estimatedUSD0.738650. Accepted: local normalization, denominator-ideal proof,
bit bounds, semilocal interpretation and CRT. Repaired two report errors:
Norm(P) is a PRIME POWER p^f, not necessarily prime; verify p and the field
O/P, not primality of Norm(P). Its L5 denominator-independence display swaps
the inverse denominators; the correct identity is a*b^-1=a'*b'^-1 when
a*b'=a'*b. These do not invalidate the algorithm. The report is limited to
the residue lemma and does not certify the full similarity construction.
Claude audits/claude_runs/2026-11-07-integral-determinant-character truncated
at16384 tokens with EMPTY report, estimatedUSD0.354432: no findings or retry.
Both terminal/reaped; totalUSD1.093082. No billing/balance inference.

Next decision: after one scoped milestone, reselect
independently by external scientific value. No backend, nearby tuple variant,
Pell sweep, generic compact-PIT project or additional agreement audit queued.

Frozen scoped milestone PASS: audits/controls/compact_integral_similarity/checkpoint.json.
No control rerun, broad suite, registry/site changes or quantum execution.
