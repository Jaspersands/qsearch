# Constructive Next Target: Unmatched Native Cubic Program Factory

IMPLEMENTED AT FIXED FIELD ROOT / REVIEW PENDING. See the completed derivation
and source-accounted implementation in `TERNARY_CUBIC_PROGRAM_FACTORY.md`
and `theorems/ternary_cubic_program_factory.py`. The text below is the original
design specification, not a claim of growing-depth completion. It follows
`TERNARY_QUADRATIC_PROGRAM_RECEIVER.md`; no new speedup is accepted.

## Replace The Matching Factory, Not The Receiver

At original even level4, independently acquired carry packets have field3
component phases Q_(j,l)(z) of degree<=3. Their public functions differ;
no identical packets or leading-tensor match is promised. Fix data width d
and restrict surplus logical coordinates by actual measured complements,
retaining every outcome. Each retained packet is still flat and its cubic
part is computable from its actual low rows and frame.

Represent the cubic component coefficients in the canonical F3 basis
with each variable exponent<=2 and total degree3. There are

    R = n*(binomial(d+2,3)-d)

entries. The removed d terms z_i^3 are linear as functions on F3. A batch
of R+1 independently supplied programs guarantees a NONZERO F3 linear
relation c_j among these vectors. Gaussian elimination computes it. This
is polynomial at FIELD ROOT; do not call the analogous growing-degree
tensor expansion polynomial at d growing with n.

The relation can be selected using only the low cubic data. Charge EVERY
program acquired in the cohort, not just the nonzero c_j. Original parent
IDs must be disjoint. Programs with c_j=0 remain live; they are not magically
returned as unconditioned fresh IID samples.

## Physically Realize Signed Coefficients With One Use Each

Prepare a KNOWN Bell pair on data/reference registers of width d.
For each selected supplied program

    3^(-d/2) sum_u omega^(<s,Q_j(u)>) |u>,

apply SUM from data z into program u with coefficient -c_j, then measure
all program wires, recording m_j. Conditional on each m_j, the data acquires
the diagonal phase Q_j(m_j+c_j*z). The outcome is uniform with probability
3^-d on ANY input, including entangled data. Every outcome is accepted.
Each supplied unknown program is consumed once; no inverse is requested.

Its cubic coefficients are c_j^3 times the original cubic coefficients,
namely c_j over F3, and are unchanged by m_j. Thus the total public phase

    G_l(z) = sum_(j:c_j!=0) Q_(j,l)(m_j+c_j*z)

is quadratic for ALL components and ALL measured m_j. Crucially c_j=2 is
realized by a DOMAIN sign, not two copies of the same unknown program or
an unprovided complex-conjugate state. Lower terms must be recomputed from
actual m_j; matching cubic tensors is unnecessary.

The data/reference is a quadratic Choi program. Keep it directly, or uncopy
the reference by inverse SUM to recover one flat quadratic program plus
known zero junk. Then choose the isotropic input from its public matrices
and apply the implemented one-use receiver. Do not choose its input before
the measurement-dependent quadratic matrices are known.

## The More Useful Label Law

For each native odd field-root input, use the conditional frequency chart

    a_i = ell_i+3*alpha_i,
    c_i = 2*a_i+3*delta_i mod9.

Conditional on all low rows, alpha_i,delta_i are independent uniform F3^n.
The high contribution after kernel division is

    alpha_i*t_i(z) + delta_i*1[t_i(z)=2] mod3.

On an affine packet frame t_i(z)=b_i+D_i*z, the alpha terms are purely
linear. They give independent uniform linear coefficients because D has
full column rank. The delta terms give the quadratic matrices. These are
independent after conditioning on the low rows and actual uniform measured
complements. Any claim must verify this decomposition against TRUE original
frequencies, not assume independent alpha/delta after arbitrary selection.

In the proposed cohort, relation selection uses LOW tensors only; all
injection outcomes m_j are uniform independently of the program phases.
At least one selected full-rank frame supplies a uniform alpha linear
contribution. Therefore the final beta_l should remain uniform independent
of the final matrices and all other relevant transcript, componentwise.
Make this a proved SOURCE lemma, not just a histogram fit.

The implemented isotropic algorithm reads only matrices. For any nonzero v,
beta_l*v is consequently uniform. Full gradient rank is NOT required for
uniform equation labels across this source ensemble. Requiring it would
unnecessarily reject valid programs. If v reads beta, however, the law can
fail completely; the current receiver tests give such a counterexample.

At d>=(n+1)^3-n the common-isotropy algorithm guarantees a direction using
polynomial public arithmetic. With the proven fresh-beta law, independent
cohorts could then supply enough exact field equations without matched
program copies or a generic stabilizer tomography procedure.

## Scope And Likely Failure At The Real Goal

Even if implemented exactly as described, this is not a Shor-level result.
For q9 the known sieve is already polynomial; the large tensor/cohort
construction may be MUCH more expensive. Its leverage is removing the
matching and identical-copy assumptions from a constructive architecture.

At q=poly(n), native additive depth grows. Odd top terms can change sign
under domain negation, but even top terms do not. Their cancellation needs
a different supported zero-sum step. Repeating polynomial-cost cohorts for
O(log q) depths can still cost n^O(log q), and expanded tensor dimensions can
already be quasipolynomial. Do NOT promote a field-root factory to a
full-depth polynomial algorithm. Lower-degree/source transitions and useful
throughput need new proofs. No cryptographic reduction supply is granted.

## Required Implementation And Falsifiers

1. Inspect `ternary_schur_tensor.py`, `ternary_correlated_packet_acquisition.py`
   and the new receiver before editing. Add a sourced cubic-program schema
   and fixed-width complement map, not synthetic oracle candidates.
2. Derive a LOW-only coefficient relation; enforce disjoint original ancestry
   and include acquired-but-unselected programs in the input ledger.
3. Compile each one-use injection with its signed SUM recipe, keeping a data
   reference. Replay ALL outcomes on bounded source controls.
4. Compare G at all bounded words to actual original-root phases; verify ALL
   mixed cubic terms vanish and infer its quadratic matrices from public
   evaluations. Numerical cancellation of one secret is insufficient.
5. Prove and independently census the conditional alpha/delta and fresh-beta
   law. Test that high-dependent cohort selection or beta-dependent directions
   are not assigned that source theorem.
6. Apply the isotropic receiver AFTER the Choi program is known. Check exact
   equations, branch masses, source costs and conditional rank recovery.
7. Compare with the KNOWN q9 sieve. Preserve factory/workbench status and
   all growing-depth blockers; do not register an accepted speedup.

Hard falsifiers: reused source ancestors; coefficient2 realized by cloning;
postselected zero m_j; cubic cancellation broken by shifts; alpha correlated
with quadratic data after selection; nonuniform fresh-beta labels; or a
runtime/copy ledger hiding exponential source or tensor costs.

GPT owns this mathematical construction and its focused verification.
Gemini/Antigravity owns routine CLI/registry/UI/full-suite/Git integration.
