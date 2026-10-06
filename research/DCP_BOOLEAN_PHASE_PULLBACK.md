# Consumed Phase Programs And Public Boolean Pullbacks

LOCAL DERIVATION / REVIEW PENDING. A constructive access interface, NOT a new
algorithm, independently reviewed theorem, novelty claim or speedup. Known
stochastic phase programming is prior art; the new research task is to find a
source-faithful decoder using it, not to rename the processor a breakthrough.

## Motivation And Prior Art

Linear carry charts retain entanglement but their direct product throughput
has scoped obstructions. Consider nonlinear processing without importing a
hidden-phase oracle or the inverse of an unknown state preparation.
[Vidal, Masanes and Cirac](https://arxiv.org/abs/quant-ph/0102037) establish
stochastic U(1) program-state processing. This note derives the elementary
instrument explicitly and preserves the actual random-label input model.
It does not import their stronger stored resources to correct unknown signs.

## Exact One-Shot Instrument

The supplied program is |+_theta>=(|0>+exp(i theta)|1>)/sqrt(2), where
theta=2pi A.s/q is UNKNOWN. For any efficiently computed PUBLIC Boolean
function f(z), compute f into a clean accumulator, CNOT accumulator to the
program, measure the PROGRAM in Z with outcome b, then uncompute f.
The target/reference Kraus operator is diagonal with entries

    K_b(z) = exp(i theta (b xor f(z)))/sqrt(2)
           = exp(i theta b) exp(i (-1)^b theta f(z))/sqrt(2).

Thus K_b^dagger K_b=I/2, even on targets entangled with an untouched reference.
Every outcome has probability1/2, independent of secret, labels and target.
The program is consumed. Keep both outcomes and update the public label to
(-1)^b A. No unknown rotation correction or unknown inverse is used. For
preexisting physical Z errors, extra phases are (-1)^(e f(z)); do not treat
nonlinear f as independent logical output errors. Raw biased basis programs
do not have this unitary instrument unless a justified prior gauge applies.

With m supplied programs, the branch probability is 2^-m and the prepared
target from |+>^ell has phase

    exp(2pi i s . sum_i A'_i f_i(z)/q), A'_i=(-1)^b_i A_i.

All m programs are consumed once. Fresh target/work qubits and every public
compute/uncompute are charged. This supplies one sampled phase transformation,
not a reusable function oracle. More calls change labels unless an actual
same-label source is provided. Conditioning on particular signs costs source
attempts and must not be hidden in an abstract controlled oracle.

## Native Carry Pullback Without An Inverse

Let K be the binary parity kernel of the supplied native low label matrix,
and let h:F2^ell -> F2^k be any compact PUBLIC Boolean map. Set
f_i(z)=(K h(z))_i. Sign updates do not change A mod2, so A'K remains even.
For Q=q/2 and the zero-origin packet residual F_(A',K), the target is exactly

    2^(-ell/2) sum_z exp(2pi i s.F_(A',K)(h(z))/Q)|z>.

h need not be injective and needs no inverse. This changes the layout and
weighting of packet phase information through a known nonlinear domain map.
It is NOT uniform subset-sum-fiber preparation and does not implement the
inverse of the random packet's phase map. Retained qubits need not be product
phase states or independent secret equations.

For h the identity, this is a different physical realization of the existing
carry packet, not new algorithmic leverage. Ordinary affine-chart origin o
can also be absorbed by label signs: x=o xor Kz gives
A(x-o)=A diag((-1)^o) Kz. This normalizes origins, NOT the independent higher
coefficients or quadratic tensors of distinct packets. No copy/alignment
theorem follows. Nonlinear h is the genuinely different design space.

## Exact Source Law And A Broader Selector Class

If K,h depend only on current LOW labels and prior data, higher labels remain
native IID after the random column signs: for each fixed b, A->A' is a
bijective sign transformation within each parity class. Branch probabilities
are uniform. The complete bounded source control enumerates every higher
table and every sign outcome and confirms constant updated-table multiplicity.
This is a sufficient source-preserving class, NOT a lower bound on selectors.

Do not reject all high-label selection. Let R_i=min_lex(A_i,-A_i mod q), and
choose h by any public function of all R_i. Then h(A)=h(A') for EVERY branch.
Unconditional A' retains the native uniform label law, and the selector is
the intended public selector recomputed on A'. Conditional on R, each column
is an independent uniform element of its sign orbit, of size1 or2. This is
an EXACT source representation, not IID uniform HIGHER bits. The old fixed-
low-chart source-character moment proofs cannot simply be reused.

For example, at q8 selecting R=3 leaves updated labels3,5 only. An arbitrary
noncovariant selector f(A)=1[A<4] also gives a legal quantum circuit, but its
selector/update joint law cannot be replaced by f(A') and uniform conditional
labels. The complete countercontrol has counts[2,1,1,1,0,1,1,1] conditional
on f(A)=1. Such selectors need their actual joint pushforward/selection ledger,
not a blanket impossibility declaration. Sign-orbit selection is an explicit
larger class with a transparent law; success/construction cost remain open.

## Representation And Verification

`BooleanANFMap` represents a known function using XORs of monomial masks.
No 2^ell truth table is required; 64-bit input examples are evaluated compactly.
`packet_pullback_functions` composes K with h by XOR cancellation of ANF terms.
`consumed_program_plan` records states, measurements, controlled evaluator
calls, public gate upper bounds and clean workspace. It is a mathematical
compile plan; a physical gate backend and precision analysis are NOT exported.

For a degree-d monomial, an AND chain of d-1 clean ancillas, XOR into the
accumulator and reverse chain costs2(d-1) Toffolis when d>=2. The whole
evaluator is then uncomputed after injection. Linear terms are CNOTs and
constant terms X gates. The report charges these conservative costs without
assuming optimized synthesis or shared intermediate products.

Module `theorems/dcp_boolean_phase_pullback.py --save` writes
`research/phase_workbench/dcp_boolean_phase_pullback.json`. Controls include
q8,16,128 exact physical Kraus phase identities; every q8 higher table/sign/
secret/target assignment for a nonlinear many-to-one map; exact label-update
multiplicities; and source gates that reject free reuse or missing lineage.
Small controls calibrate the actual native resource instrument, not toy
oracle candidates or evidence of asymptotic advantage.

## A Further Product-Factory Falsifier

For f_i FIXED as current higher labels vary, suppose the flat target is a
product phase state for EVERY higher-label table and EVERY secret. Vary one
physical coefficient A_(l,i) by2 and take secret component s_l=1. Each mixed
two-variable phase derivative then forces the integer Boolean derivative of
f_i to vanish modulo Q=q/2. That derivative lies in [-2,2]. For q>=8 it must
vanish literally. All mixed derivatives vanishing makes f_i real-affine on
the Boolean cube; a Boolean-valued real-affine function is constant, one
variable or its complement. Conversely these functions always give products.

`source_universal_product_gate` implements this exact compact criterion. Even
ANF degree1 is insufficient: XOR of two variables has integer mixed derivative
of magnitude2 and generically produces entanglement. The criterion agrees
with all16 two-bit Boolean functions; only the six constants/literals pass.
This closes a LOW-SELECTED source-universal nonlinear product shortcut, not
nonproduct inference, higher-label/sign-orbit adaptive maps, arbitrary
measurements or a general quantum algorithm. At q4 the modulo argument fails
and the gate refuses the transfer. Nonlinear h should be pursued as a
collective inference resource, not a guaranteed independent-qubit factory.

## Try To Kill This Direction

1. The instrument is known. Implementing it alone contributes no new algorithm.
   A decoder must exploit a new structural choice of h or collective readout.
2. One program cannot make two generic copies or supply doubled phases. For
   a single generic theta, copying would require phase theta(x+y), but a
   Boolean f(x,y) takes only0,1, not2. Stored doubled-label resources are not
   available. This is a scope check, not a universal cloning lower bound.
3. Choosing h that already solves random subset sums, or has exponential ANF
   size, transfers the hard computation into preprocessing. Cost it honestly.
4. All-outcome phase signs may destroy a desired collision geometry. A scheme
   requiring the favorable sign branch pays2^-m unless a public byproduct
   covariance or a different accepted source law is proved.
5. A curved map does not automatically evade the old conductor cap: product
   output equations need a NEW proof. Treat every apparent signal as a
   candidate-dependent statistic until a full unknown-residue decoder exists.
6. Publicly computable h may make the induced inference classically tractable
   or merely rearrange its hard likelihood. Compare end-to-end inference, not
   phase complexity, collision means or target register size.
7. Sign-orbit selectors preserve a declared source, but their conditional law
   loses the old higher-label averaging. Analyze that law; do not count a
   reused rank-moment theorem as evidence.

Next high-upside experiment: construct a polynomial-size nonlinear h or
sign-covariant selector with an efficient UNKNOWN-residue inference primitive
at q=poly(n), keeping every sampled sign and all input consumption. Test
public byproduct covariance, conditional sign-orbit source structure and
classical inference attacks FIRST. A failed construction is a retained
negative result, not justification to resume legacy circuit enumeration.
