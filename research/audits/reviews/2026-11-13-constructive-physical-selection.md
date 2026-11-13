# 2026-11-13 — Constructive physical-learning selection

**Decision: select neither as a new research operation.** Both screens produced
concrete end-to-end constructions, but the subsequently supplied PRIMARY texts
already contain the mechanisms and the proposed access models. This is a
positive baseline match, not an unexplained gap or a general learning barrier.
No paid task, nearby parameter extension, or implementation is recommended.

Read current STATE/TRAPS. For EACH direction, ran corpus `been-tried` before
`baselines`, with the mathematical queries “stroboscopic local Hamiltonian
learning fixed time evolution linked cluster logarithm” and “learning locality
preserving unitary quantum cellular automaton support algebra chiral index
forward Choi”. The corpus returned generic locality/tomography precedents;
the baseline catalogue returned tensor simulation. These lexical results did
not decide admission. Exact bibliography leads were found locally, the parent
supplied the primary files, and the theorem/proof checks below decide it.
No Git, network, API, archives, numerical tests, or status edits were used.

## 1. Recovering local interactions from one fixed-time physical evolution

**Native problem.** A reproducible memoryless device applies
U=exp(-it H(a)), H(a)=sum_P a_P P, on chosen inputs. The distinct nonidentity
Pauli terms are known, have weight <=k, each qubit participates in <=Delta
terms, and |a_P|<=1. k,Delta are fixed. The one available duration t is known
and sufficiently small on the LOCAL interaction scale, not necessarily 1/n
or epsilon. Output all coefficients to infinity error epsilon, failure eta.
Identity energy offsets are excluded because the channel cannot reveal them.
Access means fresh preparation, one or more forward device uses, and measured
outputs; it does NOT include controlled-U, U inverse, or a conjugate oracle.

The external value is direct many-body device calibration without arbitrarily
fine time resolution. The hoped-for resource target is polynomial(n,1/epsilon,
log(1/eta)) at a fixed nonzero t; numerical 1/t must be charged if t varies.
State preparations and readouts cost O(n) per experiment. Treating physical
source preparation as an uncharged mathematical expectation is not allowed.

**Concrete operation independently derived in the screen.** For each term P,
choose a one-qubit Pauli Q anticommuting with it, and put R=iPQ. Then

 F_P(a)=2^(-n) Tr[R exp(itH(a)) Q exp(-itH(a))]/(2t)
        =a_P+nonlinear remainder.

The normalized trace is measured using random product eigenstates of R,
random maximally mixed completion, their known eigenvalue signs, one forward
U, and a Q measurement. It is an expectation of a bounded classical score.
No entangled probe or inverse evolution is needed.

Set c=2kDelta. Rooted nested-commutator counts are at most c^r r! in norm;
the difference of an r-th term at coefficient vectors a,b costs an extra
r||a-b||_infinity. Consequently, for ct<=1/2,

 ||(F(a)-a)-(F(b)-b)||_infinity <=4c^2 t ||a-b||_infinity.

For t<=1/(16c^2), clipped fixed-point inversion is a contraction. The proposed
computational improvement over enumerating all commutator words is to collect
connected interaction sets, using subset inclusion-exclusion to sum words
that use precisely one set. Truncation order O(log(1/epsilon)), bounded-degree
connected-set enumeration, and matrices on O(k log(1/epsilon)) qubits give
a polynomial classical evaluator. Thus even this construction uses classical
postprocessing of product-input/Pauli-output data, not a computational quantum
advantage. Coefficient estimates have finite dyadic precision; no unknown
spectral gap or exponentially small global Gibbs eigenvalue is inverted.

**Actual prior-art check: exact match.** Read Haah–Kothari–Tang,
`sources/constructive_physical_selection/haah_kothari_tang.txt`, actual
arXiv2108.04842v3 (the retained title is *Optimal learning of quantum
Hamiltonians from high-temperature Gibbs states*). Theorem1.3, LF274–290,
and Appendix A, LF2771–3039, explicitly cover a known SINGLE small constant
time and forward black-box channels. The introduction expressly contrasts
this with earlier epsilon-scale time resolution. Theorem A.2/Lemmas A.3–A.4,
LF2814–2941, supply connected-cluster series, coefficient control and their
classical computation. Lemma A.5 uses random product preparations and Pauli
measurements; LF3012–3026 invert the nearly diagonal map classically.

For fixed interaction parameters the theorem states O(log(n/eta)/(t epsilon^2))
device uses and O(n log(n/eta)/(t epsilon^2)) time. Remark A.1 explicitly
explains the improvement from the proved t^-2 measurement procedure to t^-1
by repeating U to reach a constant duration. No arbitrary short-time access
is hidden in that improvement. Its Section2.2, LF479–509, uses word-RAM
arithmetic and notes that the iterative method allows per-step error. These
are source algorithm bounds, not a new bit-optimal theorem from this selection.

**Cheapest decisive falsifier and disposition.** The actual appendix already
contains the proposed operation and stronger sharing of experimental samples.
Our simple local contraction does not create a new endpoint. Do not reopen
at larger times merely to escape this match: identifiability itself changes.
No missing primary-source gate remains for this screen; no follow-up is selected.

## 2. Learning a strictly causal unitary channel without inverse access

**Native problem.** A reproducible forward n-qubit unitary device U on a known
one-dimensional ring has fixed causal range R: U^dagger P_i U is supported
in the neighborhood of i for each one-qubit Pauli. The device may be a QCA,
including a shift, rather than a shallow circuit on the original register.
Learn a usable quantum-channel circuit to diamond error epsilon, failure eta,
using chosen known product inputs and local output measurements. Ancilla
discard is permitted; the output is not merely an approximate normalized Choi
state. Every source invocation/preparation/readout is charged. No U inverse,
conjugate device, supplied decomposition, or hidden support algebra is input.
This targets spatially causal device identification and Floquet/QCA experiments.

**Concrete operation.** Let S_i swap system qubit i with its ancilla, and S be
the product of all swaps. The exact identity is

 U tensor U^dagger = S product_i [(U^dagger tensor I) S_i (U tensor I)],
 (U^dagger tensor I) S_i (U tensor I)
     = (I + sum_(P=X,Y,Z) (U^dagger P_i U) tensor P_i)/2.       (1)

The factors commute exactly and each acts only on a causal neighborhood plus
one ancilla. They can be learned from FORWARD product experiments: coefficient
Tr[Q U^dagger P_i U]/2^n is a signed input/output Pauli correlation. Local
tomography to operator error O(epsilon/n), polar rounding of each near-unitary
factor, and circuit telescoping give diamond error O(epsilon). The exact
factor has singular values one, so the rounding has a paid constant gap.
Applying the sewn circuit to rho tensor |0><0| and discarding the second
register implements U rho U^dagger. The symbol U^dagger in (1) is an analysis
identity, not an available inverse query. A crude direct implementation costs
poly(n,2^O(R),1/epsilon,log(1/eta)); finite local matrices and gate synthesis
are charged, with no exponential Choi-to-diamond conversion.

**Actual prior-art check: exact match, INCLUDING the suggested QCA escape.**
Read Huang–Liu–Broughton–Kim–Anshu–Landau–McClean,
`sources/constructive_physical_selection/huang_shallow_circuits.txt`, actual
arXiv2401.10095v1. LF187–208 specifies precisely the product-input/Pauli-output
classical dataset and the 2n-qubit U tensor U^dagger output with discarded
ancillas. Theorem1/2, LF210–237, give polynomial classical learning and small
diamond error. Section2.1.2, LF473–535, gives EXACTLY (1).
Definition15/Lemma8/Lemma9, LF1714–1852, give polar rounding, the sewn circuit,
and the diamond-norm sum of local operator errors. No inverse source is used.

Most decisively, LF242–255 EXPLICITLY says the proof applies without
modification to quantum cellular automata, and discusses a shift as an example
not representable by a shallow geometrically local circuit. Thus strict causal
range, a nontrivial shift/index, or absence of a supplied gate decomposition is
not a new loophole. The same physical dataset with classical processing is
the matched competitor; classical simulation of the unknown U on arbitrary
inputs is not needed for learning it.

**Disposition.** The exact sewing identity and QCA scope are the cheapest
decisive checks, and they match. The proposed operation supplies no new gap
to work on. Do not broaden the access, accuracy, or geometry solely to leave
a residual. Both native questions are externally useful, but neither is a
new high-upside quantum candidate after the actual source checks. No further
source request or paid agent obligation is recommended from this comparison.
