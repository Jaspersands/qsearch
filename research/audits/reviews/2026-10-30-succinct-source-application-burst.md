# Succinct Polynomial Stabilizers: A Constructive Separated Source

30 October 2026. Focused read-only review, except this note. No subagents,
commits, installations, network writes, or changes to existing research.

## Result And Status

**Proved deduction below:** a public division-free arithmetic circuit for a
formal polynomial DOES supply an efficiently preparable, globally separated
group-orbit source. Use an evaluation GRAPH state over a sufficiently large
extension field, or its full-character-tag Fourier transform. No additional
amplitude-access or orbit-gap promise is needed in this input model.

**Fatal qualification:** a single fixed additive-character phase state does
NOT have this property, even over arbitrarily large extensions. Trace can
erase a nonzero formal polynomial and all information about its stabilizer.

**Conditional consequence only:** stabilizer recovery still inherits the
receiver, group-coordinate, and runtime obligations. The source construction
neither establishes classical hardness nor identifies a useful hard family.
The existing ordinary fixed-fingerprint oracle already supplies the cleanest
interface to `UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md`; no new mixed-order
receiver or projective-character cancellation machinery is called for.

Read: `SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT.md`,
`POLYNOMIAL_ORBIT_MODULE_CLASSICAL_FILTER.md`,
`ITERATED_QUADRATIC_JET_FILTER.md`,
`FINITE_DIFFERENCE_LOG_STABILIZER_FILTER.md`, the ring-to-field note,
`STATE_SYMMETRY_COSET_TRANSFER.md`, `REES_PROJECTIVE_STATE_SOURCE.md`, and
`NATIVE_ORBIT_SOURCE_ACCESS.md`; inspected the succinct-fingerprint and
state-transfer implementations and their tests. This is not another
finite-difference/log-kernel attack.

## 1. Source Theorem For The Original Formal Problem

Input: a size-s division-free binary arithmetic DAG C over F_p in D variables,
a valid formal total-degree bound Delta, and explicit matrices generating
Gamma <= GL(D,F_p). Define

    F = polynomial computed by C,
    T_g F(x) = F(g^-1 x),
    H = {g in Gamma : T_g F = F as FORMAL polynomials}.

The source lemma works for any such matrix group. A unipotent p-group, a
class bound, or a Lazard chart is needed only by the chosen recovery theorem.
If Delta=0, return H=Gamma immediately. Otherwise choose an explicit field
E=F_q, q=p^m, with q>=2*Delta, and prepare

    |V_F> = q^(-D/2) sum_(x in E^D) |x>|F(x)>.

Let R(g)|x>|y> = |g*x>|y>. This is a LINEAR unitary representation, not an
assumed unitary action on polynomial coefficients. A change of variables gives

    R(g)|V_F> = |V_(T_g F)>,
    <V_F|R(g)|V_F> = Pr_(x uniform in E^D)[F(g^-1 x)=F(x)].

For g outside H, the difference is a nonzero formal polynomial over E of
degree at most Delta. Scalar extension cannot make its coefficients zero.
The polynomial root bound therefore gives, simultaneously for EVERY g,

    <V_F|R(h)|V_F> = 1                         (h in H),
    0 <= <V_F|R(g)|V_F> <= Delta/q <= 1/2      (g outside H).

This is an exact global overlap gap gamma>=1/2 in the ideal circuit
model. It is also the exact ray stabilizer: these overlaps are nonnegative
real numbers, so unit modulus forces overlap one. More generally, two orbit
states coincide exactly on the left cosets gH, and otherwise have overlap
at most Delta/q. There is NO random choice of a test point in this proof,
and hence no all-pairs union bound or unverified good-point event.

The only polynomial identity estimate used here is the standard root bound,
restated as Lemma 1.3 in
[Dvir--Oliveira--Shpilka](https://arxiv.org/pdf/1401.3714).
Their shift-equivalence algorithm is not being imported as a stabilizer
solver. The source theorem is an elementary composition, not a novelty claim.

## 2. Preparation And Bit Costs Are Actually Paid

For the smallest allowed m,

    m = O(1 + log(Delta+1)/log p),
    log q = O(log p + log(Delta+1)).

The numeric field size may be exponential. Its representation length is
not: a binary arithmetic DAG has a syntactic bound Delta<=2^s. Use a verified
irreducible degree-m polynomial and polynomial-basis field arithmetic.
Random monic candidates, Frobenius/gcd irreducibility tests, and a capped
O(m*log(1/delta_field)) trial count give polynomial preprocessing with an
explicit failure allowance. For the intended p>4 regime, a random candidate
has irreducibility probability at least 1/(2m). No p-element table is used.

Prepare D*m uniform F_p coordinate registers; reversibly evaluate the public
DAG, copy the canonical field output to its value register, and uncompute
all evaluation workspace. Cost is polynomial in s,D,m,log p and gate precision.
The retained state uses (D+1)*m*ceil(log2 p) qubits; a direct reversible
implementation additionally uses O(s*m*ceil(log2 p)) evaluation workspace.
Controlled matrix action and its inverse cost polynomially many bit operations.
On invalid binary encodings the action can be extended by the identity.

Uniform F_p preparation is not a free p-dimensional Hadamard: binary interval
preparation with computable conditional rotations and charged synthesis
precision suffices in polynomial time in log p and log(1/eta). Ideal exact
states specify the mathematical source; compiled gates approximate its
complete preparation/action channel. There is no postselection on F(x),
unknown normalizing constant, coefficient enumeration, QRAM, or oracle for
normalized amplitudes. All displayed sums describe circuits, not tables.

An efficient evaluator does NOT in general supply a normalized coefficient
state or value-amplitude state. Finite-field coefficients are not complex
amplitudes, and the induced substitution action on a naive coefficient norm
need not be unitary. Those are different input models, unnecessary here.
Likewise a Boolean/base-field evaluator without extension-field semantics,
division gates with untreated poles, or a binary iteration macro with unpaid
evaluation time does not satisfy this theorem. For P^T, the existing unary-T
contract pays O(T*size(P)) evaluation and log Delta=O(T).

## 3. Which Phase State Works, And A Decisive Failure

Let chi(z)=exp(2*pi*i*Tr_(E/F_p)(z)/p). Fourier-transforming the graph state's
value register, using the nondegenerate trace pairing, yields

    |W_F> = q^(-(D+1)/2) sum_(x in E^D, u in E) chi(u*F(x)) |x>|u>.

The identity q^-1*sum_u chi(u*d)=1[d=0] gives exactly the SAME overlaps and
formal stabilizer as the graph state. The full E-valued tag matters. A direct
compiler prepares uniform x,u, computes F(x), u*F(x) and its trace, applies
the phase with paid precision, then uncomputes the arithmetic. Retaining the
tag requires just one extra field register, not q separate state copies.
There is no need to invoke a general Fourier compiler to prove preparation.

By contrast, the often-suggested state

    |P_F> = q^(-D/2) sum_x chi(F(x)) |x>

can forget the entire formal polynomial. For every extension E/F_p,
Tr(A(x)^p-A(x))=0. Thus F=A^p-A makes |P_F> the uniform vector, independent
of A. Enlarging q, tensoring copies, or erasing projective phases does not
recover information that is absent already in the input state.

Concrete nonabelian falsifier: Gamma=UT_3(F_p), p>=5,

    g(a,b,c) = [[1,a,c],[0,1,b],[0,0,1]],   F=x_1^p-x_1.

Here g^-1 sends x_1 to x_1-a*x_2+(a*b-c)*x_3. Comparing the degree-p and
degree-one coefficients proves H={g(0,b,0):b in F_p}, a proper nonnormal
subgroup. Nevertheless |P_F> is fixed by ALL of Gamma over every E.
For E=F_(p^m), m>=2, the graph overlap outside H is exactly p/q: the nonzero
linear form in x_2,x_3 is uniform in E, and t^p-t has precisely p roots.

This is an easy, orbit-rank-at-most-three calibration, not a hard candidate.
It falsifies the single-character SOURCE premise, not a logarithm algorithm.
Restricting the new tag u to F_p would still fail on this example. Full
E-character averaging repairs it. For the mixed ensemble rho obtained from
fresh uniform E-valued tags, the same averaging preserves the correlation
Tr(rho R(g))=Pr_x[F(g^-1 x)=F(x)]; this is not a pure-state overlap of rho.
Independent preparations of that ensemble meet the source contract, whereas
one fixed tag does not inherit the theorem.

Separately, graph encoding on an inadequately sized field only computes
FUNCTION symmetry. F=x_1^q-x_1 vanishes on E^D yet has the same proper formal
stabilizer. Here Delta=q violates the source theorem's guard. Reduction
modulo x_i^q-x_i is not permitted when the target is formal equality.

## 4. Complete Orbit-Source Interface, Not Just Pairwise Gaps

Let N bound |Gamma|, and let B cap ALL reduced-source calls in a receiver,
including failed trials and adaptive restrictions/quotients. For a public
address set A of size J<=N with reversible representatives r(a), use t fresh
graph states, controlled R(r(a)), cleanup, and discard the graph registers.
The actual address density is

    sigma_t[a,b] = <V_F|R(r(b)^-1*r(a))|V_F>^t / J.

The ideal hiding density tau has entries 1/J on equal H fibers and zero
otherwise. Hence

    ||sigma_t-tau||_F <= (Delta/q)^t,
    TD(sigma_t,tau) <= sqrt(N)*(Delta/q)^t/2 <= sqrt(N)*2^-t/2.

Taking t=O(log N+log B+log(1/epsilon_source)) bounds the whole fresh-source
hybrid by epsilon_source. Total cost is B*t state preparations and controlled
actions. Charge per-call channel error eta so B*t*eta fits the remaining
error allowance; field-construction failure is a separate shared event.
Sequential copies may use the same address, but may not reuse a consumed
target or replace IID copies by correlated marginals. No exponential Gram
matrix is computed. This instantiates the existing state-transfer reducer
with a PROVED gap, rather than feeding it an asserted parameter.

The statement covers public sections of legitimate quotients K<=H and
subgroup restrictions. It does not manufacture K, uniform group coordinates,
or a Lie chart. A receiver needing classical label bits rather than reduced
sources cannot silently use this interface. The public preparer does have
an inverse, but that alone is not a classical XOR hiding oracle.

For the current ring-to-field theorem, prefer the ALREADY AVAILABLE ordinary
oracle f_z(g)=C(g^-1 z) with one fixed uniform z and
q_0>=Delta*N^2/delta. Its single global separation event has failure <=delta
and its field bit length is still polynomial. It supplies actual canonical
labels and their reversible evaluation. Restricting/quotienting that oracle
is already handled by the latest reduction. Graph states give a smaller-field,
deterministically gapped interface, not a new application regime or better
end-to-end asymptotic recovery theorem.

## 5. Classical Comparator And Remaining Application Obligation

The same public C permits classical extension-field evaluation and PIT.
Preparing its quantum graph state grants no additional promise about C.
Ordinary derivatives under their characteristic guard, exposed Frobenius
deflation/lifting, small orbit-module discovery with a faithful matrix block,
Moore recognition, factorization, and fixed-anchor jets remain applicable.
The finite-difference obstruction does not defeat these guarded methods.

The iterated-quadratic reserve is not rescued by the source theorem: its
source is legal, but the existing jet/propagation filters already solve the
reported controls. Failure of a filter is not a classical lower bound.
Explicit amplitude access therefore is NOT the remaining fatal assumption
for genuine arithmetic DAGs. The missing application evidence is an
independently motivated family surviving access-matched classical attacks,
plus a valid and costed recovery theorem in its actual group parameters.
For an explicit class-c<p Lie input, recompute derived rank after classical
restriction and use the latest ring-to-field/field bound conditionally;
do not resurrect direct mixed-order machinery or assert it applies to an
uncharted matrix group for free.

## 6. Verification, Falsifier, And Next Action

**Experiments, not proof or a quantum execution:** an in-memory FLINT check
used F25=F5[z]/(z^2+4z+2) and all 125 UT3 elements. It checked all 15,625 orbit
Gram entries: formal stabilizer order 5, orbit size 25, graph overlap 1/5 off
H, and single-trace-phase overlap 1 everywhere. All 25 character sums were
checked exactly by trace histograms. Numerical full-density eigenvalue checks
agreed with TD=(24/25)*5^-t for t=1,2,4, namely 24/125, 24/625, 24/15625.
The wrong-field control x^25-x vanished at all 25 field elements.

The existing planner with N=125, gap=1/2, B=10 and error=1/100 returns 38
copies per source, 380 total preparations, and hybrid bound 155/65536. This
is conservative budget arithmetic, not measured performance. Existing tests:

    /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider \
      tests/test_succinct_polynomial_stabilizer.py \
      tests/test_state_symmetry_coset_transfer.py

Result: 40 passed in 0.86s. No full suite, quantum gate compilation, HSP run,
or new general stabilizer backend was performed. No hard-family, speedup,
novelty, or registry status is promoted. No speculative hardness conclusion
is drawn from the remaining coverage gap.

**Persisted regression follow-up:** `tests/test_polynomial_graph_source.py`
now contains four standalone exact tests. Coverage was checked first: the
existing succinct tests cover fixed-point fingerprints and base-field aliasing,
and the state-transfer tests cover generic source densities; neither covered
this F25 trace-phase failure and full-character-tag repair. The new file uses
existing FLINT matrix helpers, an explicit F25 modulus, and formal polynomial
coefficients to check H and a nonnormal conjugation witness. It evaluates only
the 25 distinct inverse first rows on the 25^3 domain points, then checks all
125 group elements. Character sums use exact trace histograms and the identity
1+w+w^2+w^3+w^4=0, with rational overlaps; no floating phases or spectra occur
in these tests. The wrong-field test also checks a formally non-invariant shear.

    /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider \
      tests/test_polynomial_graph_source.py

Result: 4 passed in 4.30s. A combined run of that file with
`tests/test_succinct_polynomial_stabilizer.py` and
`tests/test_state_symmetry_coset_transfer.py` passed all 44 tests in 3.89s.
Only the new test and this note were edited; no production/UI changes or
algorithm/candidate compilation was performed.

**Precise falsifier:** reject a claimed formal-stabilizer source if it sends
x_1^p-x_1 under UT3 to the uniform single-character phase state and nevertheless
claims H={g(0,b,0)}. Reject a graph source with unpaid extension semantics or
a degree bound permitting formal/function aliasing. Neither failure applies
to the fully costed graph/full-tag construction above.

**Next action:** stop treating generic source preparation as the application
bottleneck. Select one independently motivated public circuit family, specify
its intended stabilizer output, and attack that SAME input with the existing
orbit-module and fixed-anchor/propagation filters before allocating receiver
work. Require a surviving restricted group and its measured or proved resource
parameters, not merely high degree or a failed log kernel. Without such a
family, the correct disposition is SOURCE FEASIBLE / APPLICATION UNESTABLISHED.
