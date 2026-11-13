# 2026-11-13 Post-transport selection: balanced expanded Witt reduction

Selection only. STATE/TRAPS/GOAL, the current transport checkpoint, the compact
isotropy and binary-Fock notes, the constant-slope conic proof, and the two new
Witt primary texts were read in the targeted sections below. No API/network/Git,
new test, archive, or quantum implementation. Parent owns corpus/literature
admission and shared status. The three operations below have different central
obligations; the first two share arithmetic backends, not a seed/height proof.

**Recommendation:** test a balanced, expanded Witt-basis compiler over arbitrary
TOTALLY IMAGINARY number fields. The new operation is a depth-log(d) merge of
bounded anisotropic cores, with a degree-independent affine height ledger.
Expanding one isotropic vector is a useful corollary, but is not the selected
scientific claim. Do not continue the dyadic seed line without a coupled search
construction. The outside-arithmetic comparator is a coherent classical
resummation of a binary-large one-axis-twisting count law; it is currently less
complete. No novelty, classical lower bound, or quantum advantage is inferred.

## 1. Coupled dyadic seeds for integral ternary isometry

Native endpoint: the actual `INDEFINITE_TERNARY_SPINOR_ADMISSION.md` contract:
growing-degree totally real K, expanded O_K and integral ternary A,B, indefinite
at a real place; decide integral isometry, with no transporter/local advice.
The quantum global rational map and finite spinor/ray-class decision would give
poly(native bits, log(1/eta)) under the admitted GRH arithmetic imports IF a
uniform local integral seed compiler were supplied.

A concrete possible new operation would be a **coupled finite-jet lift**: retain
an affine family of matrix residues, rather than one arbitrary residue, while
solving diagonal quadratic and off-diagonal bilinear conditions together.
The native local target is X in GL3(O/pi^h), X^t A X=B mod pi^h, with
h=v(det B)+2v(2)+1. After that, the reviewed inverse-square-root and four-sign
spinor charts finish with polynomial precision. A local norm solver may be
quantum, but field norm membership alone is not this lattice-constrained search.

The strongest existing attacks are decisive against simpler versions. The
all-m pair A=diag(1,4,-25*2^(2m)), B=diag(5,20,-2^(2m)) has an integral isometry,
yet matching the distinct Jordan lines separately fails, and no isometry is
I mod 2. An arbitrary initial mod-2 branch can be a dead end. Beli's two actual
proofs use classification at the coordinate-realization step; First only pays
the odd/unimodular case. These facts do not show that coupled lifting is hard.
The same classical spinor/ray-class algorithm, with classical class/unit data,
is the matched baseline; rational/low-degree easy fields are not an advantage.

Exact next constructive experiment: on this all-m family, symbolically retain
all extendable mod-2 families, and prove that one lift step can be represented
by polynomially many affine/quadratic constraints and compressed branches,
independently of m, e and residue degree. A scheme whose list doubles at each
precision is falsified as a proposed clock, even if it finds small examples.
At present there is no invariant controlling that branch representation. This
is a meaningful local algorithm question, but no new full construction emerged
from the source audit, so it loses to route 2 for this pass.

## 2. Balanced expanded Witt bases: selected operation

Native input: arbitrary explicitly encoded totally imaginary number field K of
growing degree n, compatible maximal order/basis/table, nonsingular symmetric
d-by-d A over K, and eta. Both n and d grow. Output an EXPANDED P in GL_d(K),
an integer w, and an anisotropic C of rank r<=4 with

    P^t A P = H^(orthogonal w) orthogonal C,
    H = [[0,1],[1,0]],             2w+r=d.

A fixed-rank core comparison would then give expanded rational-isometry maps
between two arbitrary-rank forms over the same field. This is not integral
lattice isometry, a short integral witness, or a claim over fields with real
embeddings. The arithmetic motivation is constructive quadratic-space
classification with an explicit native basis, rather than a circuit for a point.

Mechanism:
1. Diagonalize A once by polynomial-bit fraction-free rational linear algebra.
2. Make a balanced tree of its one-dimensional diagonal leaves.
3. At each node retain previously produced hyperbolic planes unchanged, and
   combine only its two anisotropic cores. Their total rank is at most eight:
   over a totally imaginary number field every rank>=5 form is isotropic.
4. Apply at most four fixed-rank isotropic-vector/hyperbolic-splitting steps to
   that core. Return its <=4-dimensional anisotropic remainder and the actual
   coordinate map. Compose maps along the tree, not along a d-step chain.

The new exponent-residue norm operation permits an expanded quaternion splitting
from a genuine compact quadratic norm witness. The existing q3/q4 descent then
uses only constant-size minors, a possible quadratic discriminant extension,
and field arithmetic. For rank>=5, the existing single-five-plane reduction
needs integral CRT parameters s,t and a bounded-height q4. A basis change of
fixed rank has bounded algebraic degree; this matters to the height slope.

The decisive lemma is stronger than “polynomial height per node.” Use the
extensive height H_K=n*h and fixed-rank tuple sums. Need

    H(core_out, merge_map) <= C*H(core_in) + P(field),        (W)

with an ABSOLUTE C, not n^c and not H(core_in)^c. After h<=ceil(log2 d) levels,
C^h is polynomial in d. A degree factor n at each level would instead give
n^Theta(log d), and a nonlinear height recurrence could be worse. Basis columns
combine through at most eight child columns per node, so the same fixed-arity
height calculation can control their original-coordinate embeddings. Final
growing-size inversion occurs only once and does not feed a recurrence.

There is a concrete route to (W), not a new isotropy oracle:
* The reviewed conic-witness shortening has absolute slope 64, independent of
  the old witness and field degree. Its only original-tower-specific input was
  square-root extraction in K; the now-paid number-field factor/root routine
  replaces that input. Its ideal/discriminant/LLL argument otherwise works over
  arbitrary K. This transfer still needs explicit final proof, not a label.
* For the totally imaginary q5 step, there are no real sign conditions. Make
  local s,t integral by common local scaling (which changes the represented
  value by a square). Prove that the required CRT ideal I has
  log N(I)<=C0*H(core_in)+P(field), with absolute C0.
* **Small-height CRT operation:** take short nonzero gamma in I by the already
  paid Minkowski-Gram LLL routine. Reduce any integral CRT representative u0
  modulo the sublattice gamma*O_K, using the original basis omega_i. The result
  u is still u0 mod I. If W bounds all |sigma(omega_i)|, then
  |sigma(u)|<=(nW/2)*max_sigma|sigma(gamma)|. LLL bounds the latter by
  exp(O(n))*|disc K|^(1/(2n))*N(I)^(1/n). Hence

      H_K(u) <= log N(I) + (1/2)log|disc K| + O(n^2+n log(nW)).

  This has slope ONE in the CRT modulus mass. The reduction is exact linear
  algebra/rounding in the gamma*omega_i basis, not ideal principalization.
  Integral targets are important: an unnecessary rational denominator clearing
  can reintroduce a degree multiplier. All field/basis constants are charged.

Charged resources: O(d) fixed-rank merges/calls, degree<=4n temporary fields,
maximal-order/factoring/ideal arithmetic, exact root extraction, constant-slope
postprocessing, all original-basis conversions, output d^2 field coordinates,
and eta/O(d) error allocation. Temporary basis-conditioning bounds may affect
runtime, but must not enter the propagated intrinsic-height slope; auxiliary
discriminants must use their coefficient-height bounds. If (W) is proved, polynomial input/output height
makes every expanded norm call polynomial, and the total target is
poly(n,d,field bits,A bits,log(1/eta)) under GRH. No assertion about the current
absolute exponent or practical performance is needed.

Actual classical sources checked:
* Fukshansky, *On effective Witt decomposition and Cartan–Dieudonne theorem*,
  retained `fukshansky_witt.txt` LF37–64, 210–230, 483–504, 567–601. Theorem 1.3
  gives explicit small-height **existence/search bounds**. Its proof starts with
  an existential small maximal totally isotropic subspace. This already rules
  out claiming new existence of small Witt components, but is not a polynomial
  native construction from the stated input.
* Koprowski–Rothkegel, arXiv:2109.04172v1, retained
  `koprowski_rothkegel_anisotropic.txt` LF29–39, 79–100, 177–186, 464–528.
  It distinguishes constructing an abstract anisotropic form from finding
  isotropic vectors. It explicitly assumes principal generators, S-class and
  S-unit routines. Algorithm 8 enlarges S until an F2 system becomes solvable
  and returns an anisotropic form. These passages do not supply the proposed
  polynomial BIT clock and embedded full basis. Their implemented algorithm,
  the same classical class/unit/norm machinery, and stronger special-field
  factoring algorithms remain the applicable baselines. Absence of a clock in
  these passages is not a literature-wide absence or hardness claim.

Exact next constructive experiment: first prove the fixed-rank (W) ledger,
including integral q5 targets and the CRT mass bound; then symbolically compose
four rank<=4 cores through two tree levels, keeping every coordinate conversion.
The acceptance test is an absolute affine slope and an exact P^tAP identity.
A hidden n multiplier, coefficient-power recurrence, compact atom sum requiring
expansion, or a classical native polynomial theorem already covering this output
would decisively change selection. A finite height plot would not prove (W).

## 3. Outside arithmetic: one-axis-twisting coherent resummation

Native physical/computational target: binary K, initial |K,0>, two explicit
passive two-mode rotations around one Kerr pulse
exp(2pi*i*(a/b)*binom(n1,2)), and one final count sampled within epsilon TV.
All angle bits and log(K) count; the pulse denominator b may be exponentially
large in those bits. This is a specific collective-spin quench, not arbitrary
BQP circuit simulation or a supplied many-body state.

The reviewed `BINARY_FOCK_KERR_SAMPLING.md` gives the known quantum endpoint via
coherent Hermite transforms and modular phases, poly(native bits,log(1/epsilon)).
Its constructive classical branch sampler costs polynomial in the numerical
Fourier-branch count 2b; ordinary passive/bunched sampling and small-denominator
revivals are already matched. Generic circuit universality says nothing specific
about this one-pulse law. A large Hilbert space or b supplies no hardness claim.

The potentially new operation is a **coherent theta/Gauss resummation** of the
quadratic-phase binomial/Krawtchouk sum, using rational approximation and Poisson
reciprocity to replace enumerating revival branches. It must yield a bounded
CDF/rejection sampler in poly(log K,angle bits,1/epsilon), uniformly across
revivals and caustics, while retaining lattice/parity fringes. Such a result would
be a strong classical match for an apparently useful succinct quantum endpoint.

Cheapest constructive test: derive an exact reciprocal representation for the
one-pulse probability/CDF and a uniform envelope in the hard transition
b~sqrt(K). Check both exact low-denominator revivals and perturbations by
O(K^-2); a weak semiclassical limit is insufficient for count-level TV.
The already retained TV=1/2 coherent-versus-mixture example rejects dropping
interference. Actual primary gates before work: Iyer/Prakash QHT scope, and
uniform one-axis-twisting/Gauss-sum asymptotics; these are not inferred from titles.
There is currently no such envelope here, so this route has a motivated target
but a less complete constructive path than route 2. Do not expand it into a
bosonic gap, general-circuit classical simulation, or another barrier survey.

The single recommended next question is therefore (W) and its balanced-tree
composition. Passing it would close an expanded arbitrary-rank arithmetic
endpoint; failing it would identify an exact height operation to discard. It
requires neither a new local seed conjecture nor an unmotivated oracle.
