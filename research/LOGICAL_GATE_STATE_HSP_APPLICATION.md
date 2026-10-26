# Logical-Gate Discovery: Conditional Reduction And Gap Obstruction

2026-10-21. APPLICATION AUDIT, NOT AN ADMITTED ALGORITHM. This connects
the proposed twisted receiver to a concrete task, then rejects a tempting
unconditional application claim. The new contribution of this pass is the
access/gap audit, not the standard Choi correspondence or a new search lower
bound. Full receiver correctness and useful advantage remain unestablished.

## 1. A Concrete Task Instead Of Another Hiding Oracle

Supply an encoding isometry V:C^d->C^D by a quantum encoder operating on
arbitrary logical inputs. Supply efficient controlled LINEAR gate families
A:G_A->U(D) and B:G_B->U(d), each with explicit exponent-p Lie coordinates.
Let G=G_A x G_B have fixed class c and class(G')<=3, with the prime guard
from TWISTED_STATE_SYMMETRY_RECEIVER.md. Gate description and action costs
are charged in addition to log d and log D. A family specified only by
projective gate labels needs a separately costed linear central extension.
General qubit Clifford/T gate sets are NOT covered by this large-prime,
fixed-class exponent-p contract. Full Clifford groups have other prime
factors; universally generated gate groups need not even be finite. A
specific admissible subgroup must be supplied and its bounds checked.

The output is the relation subgroup

```
H_V = {(a,b) : A(a)V = chi(a,b) V B(b) for some |chi(a,b)|=1}.
```

It describes physical gates implementing logical gates IN THE SUPPLIED
FAMILY. It does not find all logical gates, a universal gate set, a decoder,
an unknown ambient group, or an encoder from arbitrary code-state copies.
If A is transversal, the relations are transversal logical gates; otherwise
that word is not justified. B=1 learns the pointwise scalar kernel, not all
code-preserving physical gates. The latter can have logical actions outside B.

## 2. Correct Source And Exact Gap

Prepare one normalized Choi state using a maximally entangled logical pair
and ONE forward call to V:

```
|J_V> = d^(-1/2) sum_x V|x> tensor |x>,
R(a,b) = A(a) tensor conjugate(B(b)),
z(a,b) = <J_V|R(a,b)|J_V>
       = Tr(V^dag A(a) V B(b)^dag)/d.
```

Then |z|=1 exactly on H_V. The group law holds because A and B are linear
representations on separate factors. H_V's phase is a character. This does
NOT need V^dag or conjugate(V), but DOES need conjugate(B), available from
its known gate implementation or an explicit access contract. Black-box B
does not automatically supply it. Retain the reference register: tracing
it out leaves VV^dag/d and loses the physical-to-logical correspondence.

The decisive identity is

```
min_|u|=1 ||A(a)V-u V B(b)||_F^2 / d = 2*(1-|z(a,b)|).
```

Both isometries have squared Frobenius norm d; optimize the cross term's
phase. Therefore the receiver requires a GLOBAL promise

```
min_|u|=1 ||A(a)V-u V B(b)||_F^2 / d >= 2*gamma
for EVERY (a,b) outside H_V.
```

This is a normalized, phase-optimized average-input separation. A constant
operator-norm error, a nonzero commutator, a large physical gate weight,
or a large code distance is NOT a replacement. Nor does passing finitely
many overlap checks certify the promise over an exponential gate family.

Conditioned on the whole proposed receiver and this promise, the task
reduces to its original-copy twisted input. If B_src bounds all receiver
source packets, it costs

```
B_src * O((log |G|+log B_src+log(1/delta))/gamma)
```

forward encoder calls plus controlled A/conjugate(B) calls, with additional
known-subgroup character-learning copies and all receiver gates charged.
The huge degree-dependent erasure-tree constants remain. This is not a
practical gate-discovery backend or a new sample-optimal result.

## 3. What A Correctly Learned Relation Enables

Given a verified correct basis of log H_V <= L_A direct-sum L_B, solve

```
(a,b) = sum_j t_j h_j.
```

The physical coordinates impose a public linear system in t. Its solutions
give either no logical gate in the supplied family, or an affine fiber of
logical LOG coordinates. The homogeneous fiber is the vertical kernel
{b:(0,b) in log H_V}. Do not assume it is zero: scalar phases or a
nonfaithful B can give multiple labels for the same logical action.
Exponentiation/lifting uses the supplied group charts. Group multiplication
is not replaced by vector addition outside this Lie-coordinate computation.

theorems/logical_gate_source.py implements only this post-learning algebra,
including exact 127-bit arithmetic. It does not learn H_V or validate a
claimed hidden subgroup by checking linear independence.

Nonnormality is a genuine possibility. For V=I and A=B the projectively
faithful left regular representation of a nonabelian G, H_V is diagonal(G)
in G x G, which is not normal. For a Heisenberg Lie algebra,
[(x,0),(y,y)]=(z,0) is not diagonal. This distinguishes the mathematical
task from a normal-core-only guarantee. V=I is an EASY control, not a hard
instance or evidence for advantage.

## 4. A Marked-Codeword Counterexample

Take d>=2 logical words, a fixed odd prime p (p=5 suffices), and an oracle
f that is either identically zero or one at exactly one unknown word x*.
Define the legitimate encoding isometry and supplied gate family

```
V_f|x> = |x>|f(x)>,
A(t)=I tensor Z_p^t,       B=1,       G_A=C_p.
```

This is a lower-bound control, NOT a proposed toy-oracle research candidate.
For f=0 every t is a scalar symmetry. For one marked word, only t=0 is:

```
z_t = 1-1/d + omega^t/d,
gamma_min = 1-sqrt(1-4*(d-1)/d^2 * sin(pi/p)^2).
```

With a=(d-1)/d^2, elementary sine bounds give the exact rational enclosure

```
8*a/p^2 <= gamma_min <= min(1,40*a/p^2).
```

Thus the inverse gap is exponential in logical qubits even at FIXED p.
A middle power has a constant phase-optimized operator-norm discrepancy
from every scalar action on the code, while its Choi gap is O(1/d).
One severely wrong logical word can be nearly invisible to average-input
probing. The bound implementation never enumerates d words or p labels.

The two normalized encoder Choi states have inner product 1-1/d.
Their k-copy pure-state trace distance obeys

```
D_k^2 = 1-(1-1/d)^(2k) <= 2k/d.
```

For equal-prior binary discrimination with success s>1/2, Helstrom's
bound requires D_k>=2s-1, hence k>=d*(2s-1)^2/2. In particular k>=d/18
for success 2/3. This is an Omega(d) lower bound for IID Choi copies,
not for arbitrary encoder queries. The extra p^2 in the overlap-gap
bound is NOT a p^2 copy lower bound: these two input states' overlap is
independent of p. No matching optimal dependence on p is claimed.

Even a stronger algorithm with arbitrary coherent encoder/inverse queries
cannot solve all such exact symmetry tasks in poly(log d): each encoder
query is simulated with O(1) marked-item oracle queries, so distinguishing
the two subgroups entails unstructured search's Omega(sqrt(d)) query
bound. See [Bennett--Bernstein--Brassard--Vazirani](https://arxiv.org/abs/quant-ph/9701001).
This is an oracle-model obstruction. A public white-box f may expose its
mark immediately; no hardness claim is made for that different input.

## 5. Error-Correcting Distance Does Not Repair The Gap

Compose with ANY supplied parent code isometry E:C^(d*p)->H_phys that
corrects an error set {F_i}. Its Knill--Laflamme conditions are

```
E^dag F_i^dag F_j E = c_ij I_(d*p).
```

The subcode with encoder W_f=E V_f inherits them EXACTLY:

```
W_f^dag F_i^dag F_j W_f = c_ij I_d.
```

Thus its distance is at least the parent's distance for the same physical
weight model. If a physical A_phys implements the parent's flag Z,
A_phys E=E(I tensor Z_p), the W_f overlap is still z_t above. A known
stabilizer parent encoding ell+1 p-level logical systems, d=p^ell, has a
logical flag-Z representative that is a tensor product of physical Paulis.
That representative is transversal. The subcode can therefore inherit
the parent's large distance AND have this exponentially small symmetry
gap for a supplied transversal gate. The subcode need not itself be a
stabilizer code; silently imposing that extra promise changes the task.

This is a direct deduction from the standard error-correction conditions,
not a new code construction; see [Knill--Laflamme](https://arxiv.org/abs/quant-ph/9604034).
The finite test checks abstract syndrome/KL algebra and gap preservation,
not a growing physical-distance code implementation.

## 6. What Could Still Make The Application Viable?

A valid sufficient condition is a POPULATION separation: for every
nonrelation and every global phase u, at least alpha*d singular values
of A(a)V-u V B(b) are at least eta. Then gamma>=alpha*eta^2/2. Both
alpha and eta must be inverse polynomial in the actual input size, and
their proof must come from the encoder/gate structure, not a sampled
minimum. This is a sufficient promise, not a derived property of codes.

Another sufficient special case is that every physical gate outside the
code-preserving family sends the entire code into an orthogonal subspace,
while every wrong logical label within that family has a proved normalized
character gap. Such a promise must be established for a motivated family;
planting an unknown coset code simply repackages HSP.

Neither sufficient condition is currently established for a natural,
nonadditive, nonnormal, growing-prime family that defeats direct classical
or known quantum learners. Without one, this remains an application
interface and an obstruction, not a breakthrough candidate.

## 7. Prior Art And Access-Matched Baselines

The vectorization idea is not new. [Holt--Subramanian, Section 10](https://arxiv.org/html/2609.38085v2#S10)
studies unitary/other-object symmetries through state reductions. Our
rectangular two-family relation uses a phase-optimized normalized norm;
it does not import an unexamined Bose absolute-gap implication.
[Cao--Lackey, Quantum Lego Power-up](https://arxiv.org/html/2603.03542v1)
already connects encoding-tensor symmetries with transversal logical gates.
Using this connection is not novelty. A new result would require a valid
algorithm in a genuinely additional group/access regime.

Before claiming usefulness, compare:

- Classical stabilizer/tableau arithmetic when the encoder and gate family
  expose that structure; known stabilizer-learning algorithms when they do not.
- Explicit tensor contraction, operator pushing, and low-width tensor-network
  methods when the construction supplies them. A succinct tensor network is
  not automatically hard, and high width is not a lower bound.
- Direct matrix methods or tomography when D and d are polynomial in the
  input size. Their cost is not polynomial merely in the number of qubits.
- Existing abelian/nil-2 and phase-symmetry learners. Known conjugation of a
  Pauli group does NOT raise its nilpotency class; relabeling those gates
  cannot justify the new higher-class receiver.
- Explicit sparse-Pauli/finite-field group-action baselines already documented
  in CLASS_THREE_APPLICATION_AUDIT.md. Do not hide a public description from
  the classical competitor while granting it to the quantum implementation.

The conditional advantage target is polynomial-time learning of a compact
logical-relation subgroup without full process tomography or exponential
gate enumeration. No access-matched lower bound separating this from all
classical strategies is established, and no Shor-level significance follows
from the task's quantum input.

## 8. Decision And Next Experiment

Retain the conditional reduction and exact fiber recovery. Reject the
claim that arbitrary encoded-code access, large distance, transversality
or a constant worst-case gate error supplies the required gap. Do NOT open
a candidate campaign, run code-design sweeps or promote this application.

The next admissible application experiment must identify ONE independently
motivated encoder/gate family, prove its GLOBAL population gap, and compare
the same input against existing classical/tensor and abelian quantum
methods. If no such family is available, prioritize independent validation
of the core nonabelian theorem over generating planted codes or more gap
examples. This audit does not refute the core HSP receiver proposal.
