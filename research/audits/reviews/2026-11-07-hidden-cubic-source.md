# Hidden cubic: bounded actual-source scope review

7 November2026. Read STATE/TRAPS and the exact candidate contract in
`audits/claude_inputs/2026-11-07-hidden-cubic/contract.md`. No network, Git/API, implementation, or
full-paper/generalization audit. Locators below are local extracted-text line numbers. **None of these checked
statements supplies the requested uniform polynomial-time learner for every unknown Clifford image of a
maximum-occurrence2 cubic phase state.** This does not prove hardness or nonexistence of such a learner; the
candidate stays open.

## ABB2208.07851v2: known physical phase frame

Primary `audits/sources/hidden_cubic_learning/phase_learning.txt`. The input/output model at128--136 is copies of
the binary phase state psi_f itself, unknown polynomial f, with classical polynomial output; it explicitly
distinguishes stronger chosen-function query access. Definition1 at711--713 measures coordinate k in X and all
others in Z. Lines702--710 show why this yields a UNIFORM y and the EXACT label D_k f(y). This identity uses the
computational phase-state frame, not an unknown Clifford image of that frame. Measuring those physical axes after
arbitrary unknown C need not yield these derivative labels.

Section3.1 lines817--838 and Algorithm1 at873--881 form derivative evaluation matrices and solve them by classical
F2 linear algebra. Theorem3 at884--920 gives O(2^d n^d) copies and single-qubit X/Z measurements, with
high-probability exact identification, for d<=n/2. Table1 at157--159 records O(n^(3d-2)) time. Thus cubic learning
in a KNOWN frame is already polynomial, without the occurrence promise. The union bound at900--918 also permits
logarithmic confidence amplification in the sample count. The finitely many n<6 cases are constant-size exceptions
to the theorem's displayed d<=n/2 condition, not an asymptotic obstruction. Global constant phase is irrelevant for
the candidate's state output.

A known Clifford can be inverted on fresh copies before using the theorem; an unknown Clifford cannot. An
X/CNOT-type coordinate permutation alone preserves a phase description, but an arbitrary Clifford can destroy the
uniform computational-basis amplitude promise. The lower-copy entangled Theorem4 at935--942 is a PGM identification
result, not a polynomial-time replacement: the table at161--163 records exponential runtime and the authors
explicitly leave these runtime improvements open at470--476. Neither the uniform-y polynomial anti-concentration
proof nor this PGM statement pays the proposed Bell-distribution K5 gap or frame extraction.

## Fechisin2610.00464v1: supplied stabilizer description

Primary `audits/sources/hidden_cubic_learning/hierarchy_stabilizers.txt`. SectionIV.B lines814--848 assumes an XCd
stabilizer SUBGROUP H is GIVEN, fully encoded by pairs `(v_i,f_i)` for its elements, and uniquely stabilizes the
state. Algorithm1 input at894--899 repeats that supplied-description requirement. No copy measurements learn H or
hidden Clifford axes there. The ambient form X(v)D[f] is itself a selected computational monomial frame; general
Clifford conjugation need not preserve this displayed form.

Moreover this canonical-form procedure is not stated as a polynomial-BIT copy learner: lines854--856 compute the
common diagonal zero set by evaluating f(y) over all y, and lines941--949 explicitly loop over every x in F_p^ell to
construct phi(x). Its output can therefore contain an exponential phase table. Supplying stabilizers or assuming
their inference would add advice absent from the native contract. This is useful structural classification, not a
source-paid polynomial hidden-frame algorithm.

## Haug2609.27128v1: hidden PRODUCT cuts, not internal phase axes

Primary `audits/sources/one_rotation_learning/haug.txt`. The class C_(n,k), lines72--97, permits an UNKNOWN
Clifford, unknown pure blocks and partition, with largest block k. Theorem2 at188--208 genuinely uses two-copy Bell
samples and polynomial classical inference to recover the irreducible product subspaces, given gamma2>=gamma, in
O(gamma^-1*(n^2+log(1/delta))) samples. Each sample consumes two copies. Lines211--212 retain freedom of LOCAL
Clifford bases, Pauli phases and block order. Hence exact product recovery does not determine a phase-state
computational frame inside an irreducible growing block.

Every pure state formally lies in C_(n,n), but this does not give efficient full learning. Lines213--228 require
block tomography with O(r*2^k*epsilon^-2*log(r/delta)) copies and corresponding dependence on block dimension.
Theorem4 at215--223 removes gamma2 dependence but still requires an affine gap and time/copies polynomial in2^k. The
native occurrence2 promise supplies neither a checked logarithmic Clifford-product width bound nor the required
uniform gap theorem. Large hypergraph components alone do not prove large Clifford-product width either. Exceptions
already covered include promised small-width/gap families, stabilizer states, and disjoint constant-size cubic
blocks; none covers every growing overlap component without an additional argument.

AppendixI at1872--1883 assumes a SUPPLIED MPS. Lines1963--1977 give O(n*chi^3) arithmetic operations per classical
Bell sample and then assume a KNOWN Clifford C to compute its affine relabeling. This does not learn an unknown MPS,
f, or C from copies. Likewise the parent's supplied-f,C quadratic-Fourier Bell sampler is a matched classical
sampling baseline, not an unknown-copy learner or evidence of quantum advantage. Bell samples can feed the same
classical inference once available; obtaining samples and inferring hidden phase axes are different obligations.

Disposition: retain ABB AFTER a valid phase frame is found, and Haug under its gap/width promises. The later
independently accepted factored-event gap pays exclusion of false products of at most5 affine forms. It does not
identify these products, recover a phase frame, or assert full K5 recovery. The source scope above is unchanged.

## Admission addendum: unrestricted factor search and graph coloring

Independently checked the current main note's graph reduction. Work in the Boolean ring F2[x_1,...,x_m]/(x_i^2-x_i),
with constant, linear, and squarefree quadratic features: 1+m+choose(m,2) columns. Evaluation on the explicit
simple-graph points S_G={e_u+e_v:uv in E(G)} and its full nullspace are polynomial constructions. Products are
reduced in this ring; diagonal squares contribute to linear coefficients.

For P=(1+ell_1)(1+ell_2), assign vertex v color (ell_1(e_v),ell_2(e_v)) in F2^2. Then P(e_u+e_v)=1 exactly when
endpoint colors agree. Thus a vanishing such P exists iff G is4-colorable; its2m factor coefficients give a
polynomial certificate/coloring. P(0)=1 ensures a nonzero Boolean product. Conversely two affine factors with
product value1 at0 each have constant1. A disjoint K4 preserves4-colorability and forces rank2 of the homogeneous
forms, since rank<=1 permits at most two vertex colors.

The prescribed nonzero value is ESSENTIAL: without it V_G already contains the easy linear polynomial sum_i x_i,
vanishing on every edge vector. This is NP-completeness of unrestricted prescribed-value two-factor decision, not
every unconstrained factor-finding problem. NP membership follows by supplying factors and checking membership via
polynomial linear algebra. The reduction is self-contained; this addendum did not reread Huang's externally
inspected primary text.

No realization of these graph point sets as native Bell supports is demonstrated, so no hardness transfers to
promised sample nullspaces or phase-frame extraction. Full K5 would also be extra advice unless learned.
Promise-specific extraction could still succeed. Nevertheless no paid valid-frame extraction is available, and the
accepted narrow gap does not supply one. PARK after this single admission pass, without further gap/refinement
sweeps, is justified research allocation; it is not a universal no-go, hardness theorem, or failure of the
identities.
