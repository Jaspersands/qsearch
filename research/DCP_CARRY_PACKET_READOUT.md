# Carry Packets: A Batch-Sieve Interface, Not A Decoder

Status: LOCAL DERIVATION / REVIEW PENDING. No independent theorem review,
formal proof, novelty, major speedup or standard-LWE attack is claimed.

## Decision

Retaining an entire low-parity fiber is a legal sample-only operation. It
retains many qubits but NOT many independent phase states. This pass supplies
an exact public chart, carry representation, conditional Bell readout,
partial-equation compiler and a common-isotropic product extractor. It also
tests the simplest decoder against a classical code-conductor calculation.

The revised high-variance target is to extract a CONSTANT FRACTION of product
phase outputs per level, with native uniform labels and polynomial construction
cost. Losing a factor n at each of O(log n) levels gives quasi-polynomial
sample cost; losing only a constant factor could give polynomial sample cost.
Neither that improved extraction nor a general multi-level decoder exists.
The follow-up [higher-carry gate](DCP_CARRY_THROUGHPUT_GATE.md) now excludes
constant-fraction FIXED-DIRECTION, ALL-OUTCOME extraction for native m=3n
at q>=8, subject to local theorem review. Outcome-adaptive extraction and
correlated decoding remain open; do not optimize a closed subclass.
The [native source audit](DCP_CARRY_SOURCE_LAW.md) also charges overlap
postselection and tests whether accepted labels really remain jointly IID.
The implemented greedy q=4 extractor retains only about m/n outputs on
generic source sizes; it is a meaningful baseline, not a breakthrough.

## Literature Boundary

[Boucher--Fouque--Shen, v1, September 28](https://arxiv.org/html/2609.34996v1)
introduce a cyclotomic sample problem and a prime-power sieve. Their Sections
4.2--4.3 reduce the phase level by combining a zero-sum subsequence; the stated
complexity is quasi-polynomial with polynomial quantum space. They explicitly
distinguish independent samples from preparation/inverse access and do not
claim a standard-LWE attack from the limited approximate states in known
reductions. We use this as motivation for auditing state throughput, not as
independently verified proof or a new algorithm in this repository.

Stabilizer Bell learning is established [prior work](https://arxiv.org/abs/1707.04012).
The new [adaptive single-copy result](https://arxiv.org/abs/2610.02031) still
learns a fixed unknown state from multiple samples of it. Native DCP labels
change between samples: an unknown packet cannot simply be copied or redrawn.
The public-label code algebra is also established; see
[Randriambololona, Sections 2.11 and 2.42](https://arxiv.org/html/1312.0022v3).
The local source/carry interface derivations below remain review-pending;
no literature search here establishes their novelty.

## 1. Source And Public Clifford Chart

Use generalized DCP on `(Z_(2^t))^n`, t>=2. This is an actual group/coset
state family, not a newly manufactured oracle problem. A batch has m independent
phase qubits, with public uniform labels forming the columns of A:

    psi_s = 2^(-m/2) sum_x omega_q^(s^T A x) |x>,
    A in (Z_q)^(n by m), q=2^t, unknown s in (Z_q)^n.

Only these supplied states and public labels are available. No oracle for
unknown phases, same-label sample factory, state-preparation inverse, QRAM or
reused quantum copy is granted. The bridge from a particular lattice/LWE
source must separately preserve parameters, state count and approximation.
For cyclic DCP n=1 and t=log2 N; do not confuse t with the vector dimension.

Put B=A mod2, r=rank(B), k=m-r. Public GF(2) RREF produces pivot coordinates
P, free coordinates F, and an affine chart

    x(z)=x0 XOR Kz,   z in F_2^k,   BK=0.

The actual CNOT schedule sends each free coordinate to a pivot when indicated
by RREF. Measuring those pivots obtains syndrome y. Every y has probability
2^-r for ideal inputs, independently of s and A. ALL y are retained; there
is no success-normalized postselection. Exactly k qubits remain.

The origin x0 has y in pivot coordinates and zero in free coordinates.
The remaining state, up to a global phase, is

    2^(-k/2) sum_z omega_(q/2)^(s^T F_y(z)) |z>,
    F_y(z)=(A x(z)-A x0)/2 mod(q/2).                    (1)

Division in (1) is exact over integers because the difference is even.
It is not inversion of two modulo q. Computing F_y from the chart is polynomial
in the expanded label/chart size. Having this PUBLIC vector-valued evaluator
does not supply the unknown scalar phase s^T F_y or prepare its state.

## 2. Carries Are Genuine Interactions

For a physical row i, XOR expansion gives

    x_i(z)-x0_i = epsilon_i sum_(T nonempty subset supp K_i)
                              (-2)^(|T|-1) product_(j in T) z_j,
    epsilon_i=1-2*x0_i.

For |T|=1, the vector coefficient of F_y is
`(1/2) sum_i epsilon_i A_i product_(j in T) K_ij`, an integer.
For |T|>=2 it is

    (-1)^(|T|-1) 2^(|T|-2) sum_i epsilon_i A_i product_(j in T) K_ij.

Modulo 2^(t-1), terms of degree >=t+1 vanish. Thus the first quotient has
degree at most t, not degree one. Dense expansion can cost k^t; the compact
parity-sum evaluator avoids that expansion but does not remove decoding cost.
The module refuses dense expansion beyond its small calibration cap.

At q=4 each component is a quadratic Boolean polynomial

    F_l(z)=L_l.z + sum_(j<h) Q_l[j,h] z_j z_h,
    Q_l=K^T diag(B_l) K.                                (2)

The diagonal of Q_l is zero because BK=0. These are alternating matrices.
Q depends only on low labels and K, not higher label bits or syndrome y.
For a secret, the actual graph-phase matrix is Q_s=sum_l s_l Q_l mod2.

Countercontrols: A=(1,1,1), q=4 gives a two-logical-qubit packet with reduced
purity 1/2, NOT two product phase states. A=(1,1,1,1), q=8 retains a cubic
coefficient 2 modulo four. Do not apply the quadratic compiler at larger q.

## 3. Bell Readout With Matching Or Partial Matching

Take two ACTUAL q=4 packets of equal logical width k and the same secret.
Their linear coefficients may differ. Bell measurement is CNOT left to right,
then Hadamards on the left, followed by computational measurements. Write
u for the measured XOR and v for the Hadamard outcome. The XOR is uniform.

If their public quadratic tensors match componentwise, then

    v_j = sum_l s_l [L1_lj+L2_lj+(Q2_l u)_j] mod2.       (3)

Thus a polynomial circuit gives k linear equations, without unknown inverse
access, normalization or quantum witness guessing. Their RANK, not just count,
determines usable information. Finding compatible packets on the unconditional
native source is a separate algorithmic problem. Fixed matching low-label
matrices in the controls are CONDITIONAL identities, not source coverage.

Full matching is sufficient but unnecessary. Define

    D = intersection_l ker(Q1_l+Q2_l).

For any PUBLIC h in D, Bell outcomes obey the guaranteed linear equation

    h.v = sum_l s_l [h.(L1_l+L2_l+Q2_l u)+q_delta_l(h)],
    q_delta_l(h)=sum_(j<h') (Q1_l+Q2_l)[j,h'] h_j h_h'.  (4)

The module computes D and compiles (4). For this Bell-then-linear-parity
readout, D exhausts directions guaranteed deterministic for EVERY secret:
outside D, a basis secret gives a nonzero quadratic derivative, making that
parity's conditional expectation zero. Secret-dependent directions, different
measurements, coordinate alignment and multi-packet architectures are outside
this statement. A direction may depend on public u, but still must lie in D.

Countercontrols retain BOTH extremes: a mismatched pair with fully uniform
Bell outcomes, and a mismatched pair with a useful one-dimensional D. The
unconditional canonical-chart controls have no D at n=4,8,16,32 in the eight
trials per size. That finite observation is NOT an asymptotic impossibility
or a rejection of adaptive chart alignment.

## 4. The Single-Packet Conductor Gate

For a direct Hadamard parity readout WITHOUT measuring extra logical Z bits,
the public guaranteed directions are intersection_l ker Q_l. Write
C=rowspace(B) and x=Kh. Equation (2) says precisely

    x in C^perp AND x*C subset C,
    x in C^perp intersect Cond(C,C).                    (5)

The standard extended stabilizing algebra is
`Cond(C,C)=(C*C^perp)^perp`. Its binary idempotents are coordinate-block
indicators from the finest direct-sum decomposition of C, including zero
coordinates. The implementation computes those components from the public
fundamental bipartite graph of `[I|R]`. Keep only components whose indicator
is orthogonal to C, and convert them back to logical directions. This exactly
matches brute-force conductor membership and the quadratic-kernel calculation.

For native uniform n-by-3n binary labels, there is a scoped source bound:

    Pr[nonzero guaranteed direct Hadamard direction]
         <= min(1, (3n+2)2^-n + U_n),                  (6)
    U_n=sum_(a=1..n,b=0..n,(a,b)!=(n,n))
           C(n-1,a-1) C(n,b) 2^[-a(n-b)-(n-a)b].

Proof: the first 2n columns fail rank n with probability <2^-n, by a union
bound over nonzero left annihilators. On full rank, choose pivots there.
Condition on that prefix; the final n columns remain independent uniform,
and their systematic-coordinate graph is an n-by-n fair bipartite graph.
Its disconnection probability is at most U_n, summing all proper cuts
containing the first pivot. If connected, every remaining nonzero coordinate
attaches to its component. Any zero column costs at most 3n*2^-n in total.
Otherwise the conductor consists only of constants. Its nonzero indicator
lies in C^perp only when ALL original row weights are even, probability 2^-n.
These events need not be independent. The bound covers every kernel-basis
chart and every initial syndrome of this SAME full batch.

The cut bound is exponentially small: condition on left side size a. For
1<=a<=n/2, summing b gives
`C(n-1,a-1)2^-an(1+2^-(n-2a))^n`. The a=1 edge is O(n*2^-n);
splitting at a=n/4 bounds the remaining small-a terms by a geometric
exponential tail and the middle cuts by O(2^(2n-n^2/4)). Complement symmetry
treats large a, including isolated right vertices. Exact finite dyadic
bounds are retained, not a floating-point fit.

IMPORTANT ESCAPE: (6) does NOT cover measuring additional logical Z bits,
selecting a different physical subbatch, Bell pairing, general Clifford
measurements or arbitrary quantum measurements. The next primitive does
escape it. A blanket 'no stabilizer decoder' conclusion would be false.

## 5. Common-Isotropic Product Extraction: Positive Baseline

Choose independent logical directions u_1,...,u_d such that

    u_i^T Q_l u_j=0 for every i,j,l.                    (7)

Extend them to a public logical basis. Measure the complementary k-d
coordinates in Z, retaining EVERY outcome. Let z0 be the resulting background.
The residual phase is linear on the retained subspace because its quadratic
restriction vanishes. Its known output labels are

    a'_j = F_y(z0+u_j)+F_y(z0) in F_2^n.                (8)

The d retained qubits are EXACT PRODUCT phase states for s mod2. Hadamards
give the d linear equations. Neither full radical membership nor paired-state
matching is necessary. Logical basis changes, Z measurements and evaluation
of (8) have polynomial cost. The circuit is specified; SDK gate export is
delegated. A one-dimensional isotropic choice always exists when k>0.

The implemented polynomial greedy constructor adds a vector orthogonal to
all existing directions under every Q_l. After d selections it has at most
nd linear constraints. Since the existing d-dimensional isotropic span lies
in their nullspace, another direction exists whenever k>(n+1)d. Thus

    d >= ceil(k/(n+1)).                                 (9)

This reproduces the meaningful n-sized consumption scale; it does not remove
it. Maximizing d is a different task, and a stalled greedy run is NOT a maximum.
In physical coordinates U=span(Ku_j), (7) becomes the reusable coding target

    U*U subset C^perp,

where x*x=x ensures U itself lies in C^perp. Large Schur-orthogonal subcode
synthesis is a more precise search space than free-form circuit mutation.

There is a SOURCE UNIFORMITY guarantee when directions/bases are selected
using ONLY low labels. Write A=B+2H, with independent uniform high bits H.
Condition on B, initial syndrome and complementary Z outcomes; all measured
probabilities are uniform and do not bias H. Equation (8) has form

    A' = known_low_carry + H * [Ku_1 ... Ku_d] mod2.

The physical direction columns are independent, so this is a uniform n-by-d
matrix. Output labels are JOINTLY independent, not only marginally uniform.
Choosing directions from H can invalidate this argument and needs a new law.
The exact controls exhaust higher bits in three fixed-low-label strata;
they are identity controls, not invented candidate families.

At q>4, quadratic isotropy alone does not remove higher carries. A surviving
multi-level scheme needs correctly divisible weighted intersections of all
relevant orders, or a genuinely correlated decoder instead of product states.
The present code rejects that unsupported extension rather than extrapolating.

## 6. Noise, Classical Checks And Ways This Can Fail

A specified physical Z-error mask e becomes logical Z mask K^T e. In the
Bell primitive the equation-error vector is `K1^T e1+K2^T e2`. Thus one
physical fault may corrupt many reported equations; independent-bit-noise
assumptions are unjustified. Hidden fault masks are not accessible controls.
The tests cover this propagation identity, not arbitrary corruption, Regev's
complete f=1 promise, fault tolerance or a robust full decoder.

Known-secret graph-state simulation checks formulas but is NOT dequantization
of the UNKNOWN-input problem. Genuine competitors must use legal public labels
and destructive measurements of the supplied states, or actual classical
natural-problem data under a verified reduction. Existing zero-sum sieves are
the sample/time baseline; polynomial success at fixed q=4 is already expected
and by itself has no Shor-level significance.

Why the high-yield route is likely to fail: random public codes may contain
only small jointly Schur-orthogonal subspaces; adding n constraints can cost
a factor n at every stage. Finding a large subspace may itself be exponential.
At growing t, higher divisibility, source uniformity and noise can destroy
the apparent yield. Bell-aligned forms may be as difficult to obtain as the
original decoding problem. Neither information capacity nor stabilizer
learnability supplies native compatible copies.

Falsifiers: prove maximal d=o(m) on the native source for the declared
product-extraction class; prove construction cost exponential; show apparent
gain needs high-label conditioning without a valid law; exhibit lost cubic
terms or sample-reuse assumptions; or show the reduction cannot provide the
required number/quality of states. These reject the corresponding proposal,
not all quantum algorithms. Conversely a maximum-d theorem alone would not
establish efficient construction or multi-level composition.

## Next Work And Reproduction

GPT: study outcome-adaptive extraction or a non-product packet decoder;
first read the higher-carry conductor obstruction. Demand a polynomial construction, constant
fraction yield across growing t, uniform output law and robust readout before
candidate promotion. Common-radical or greedy-isotropy improvements alone
need complete sample accounting; do not optimize a constant-q toy benchmark.

Gemini: expose the public circuit/packet schema, partial Bell equations,
conductor gate and greedy baseline through qsearch and experiment registries;
keep conditional tests separate from native source rows. No candidate should
be accepted merely because a primitive's identity checks pass. Integrate
literature IDs and claim gates; run routine production regression/validation.

    python theorems/dcp_carry_packets.py --save
    python -m pytest -q tests/test_dcp_carry_packets.py

The implicit evaluator is exercised on 128 input qubits. Dense state tests
are bounded circuit/algebra controls only; their arrays are not the scalable
primitive's memory cost. All source probability certificates use exact dyadic
hex numerator / binary-denominator encoding, avoiding float or integer-string
conversion limits. No accepted candidate, production CLI wiring or commit
is produced by this theory pass.
