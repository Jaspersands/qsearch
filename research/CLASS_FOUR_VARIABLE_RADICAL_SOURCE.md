# Class-Four Sources With Variable Radicals

2026-10-21. PROPOSED mathematical extension, with public algebra controls.
Not an independently reviewed theorem, executed HSP algorithm, new central
claim, novelty certificate or external application. The prior UT5 argument's
invertible Weyl maps are NOT assumed here.

2026-10-21 alternative: CENTRAL_REGULAR_JET_SOURCE.md retains the whole
noncentral carrier after Fourier-transforming only the center. Its Weyl
map has an identity X block for every label, so this note's variable-radical
and equivariant-label arguments are not required by that preferred source
route. The irreducible route remains valid reference material, not a
mandatory dependency. Its cost/phase-degree formulas are not interchangeable.

## The Scientific Gap

Learning K=H intersect G' and passing to its normalizer quotient does not
preserve the direct-product Heisenberg presentation used by the UT5 module.
More generally, an alternating commutator-form family can have zero COMMON
radical but every individual form can be singular. Choosing a supposedly
generic nondegenerate character is therefore not a valid repair.

This is not just a constructed matrix puzzle. In the free class-four Lie
algebra on three generators over characteristic >4, the derived algebra has
three noncentral degree-two directions. Their three mutual brackets are
independent degree-four elements. Degrees three and four are central inside
the derived algebra. Thus N/Z(N) has dimension three, while a nonzero
alternating form on it has rank two and a label-dependent radical. Independent
truncated-associative-word controls verify this structural example.

The question is whether sufficiently many independent public label relations
can preserve ALL unknown polynomial jets despite these moving kernels.

## 1. Source For A General Class-Two Normal Group

For the core assume an explicitly represented exponent-p group G of class
at most four, p>4, an ordinary hiding oracle separating gH, and H intersect
N=1 for N=G'. Let m=dim(G/N), Z=Z(N), z=dim Z, W=N/Z, w=dim W.
If w=0 use the previous metabelian route. Otherwise the public bracket is

    beta: W x W -> Z,
    B_lambda(v,v')=lambda(beta(v,v')),

with common radical zero. N has class at most two. Also gamma_3(G)<=Z(N).
Prepare the ordinary MIXED coset state by tracing the hiding-output
register. Do not condition on a retained oracle-output label: the
multiplicity-factor calculation below is for that mixed source.
The fixed, proof-only section potential from the earlier argument gives

    F(q)=exp(q-pi(q)) h(pi(q)) exp(-q) in N,
    Q(q)=log F(q), deg Q<=4, deg Q_W<=2.

The unknown projection pi and hidden linear lift are never computed. H is
abelian by transversality, so the group-word action identity still holds.

For the proposed extension from unique-encoding black-box groups, see
CLASS_FOUR_BLACK_BOX_INPUT.md. Forward encoding and charged abelian-HSP
setup can avoid a coherent original-coordinate decoder. This is a written
input reduction with tested group words, not an implemented quantum setup.

For every central character lambda, public alternating-form elimination
constructs a map D_lambda:W->F_p^(2s) and radical-coordinate map R_lambda
such that

    B_lambda = D_lambda^T Omega D_lambda,
    ker D_lambda = rad B_lambda,
    (D_lambda,R_lambda) is invertible, 2s=rank B_lambda.

The irrep indexed by (lambda,alpha), alpha a character of the radical, is

    rho_(lambda,alpha)(exp(v,c))
      = omega^(lambda(c)+alpha(R_lambda v)) D(D_lambda v).       (1)

Use the symmetric Weyl convention in UT5_MATRIX_PHASE_ALIGNMENT.md.
The matrices here are descriptions of maps on O(w) field registers, not
tables of p^s-dimensional unitaries.

Efficient partial QFT instrument: Fourier transform c and measure lambda;
compute the public congruence basis; change v to coordinates (x,zeta,t);
apply omega^(-x.zeta/2), negative Fourier transforms on zeta and t, and
relabel i=j+x. This gives conjugated representation entries with amplitude
sqrt(p^s/|N|). Measure alpha, trace the independent row register. When
s=0 this is an ordinary character transform, not a rejected sector.
Approximate F_p transforms and field arithmetic must be costed; this is a
written circuit decomposition, not an implemented coherent compiler.

### Complete Fourier Factorization And Its Cost

The preceding circuit sketch can be checked as a complete instrument,
not just a list of unitary representations. This uses standard class-two
representation theory and Weyl/abelian transforms; it is NOT proposed
as a new QFT. Compare the Weyl-Heisenberg circuit in
[Krovi--Roetteler, Appendix A](https://arxiv.org/pdf/0810.3695), keeping
track of their unsymmetrized coordinates and Fourier-sign convention.

Use BCH normal coordinates with multiplication

```
(v,c)*(v',c') = (v+v', c+c'+beta(v,v')/2).
```

For fixed lambda let r=rank(B_lambda)/2 and k=w-2r. Write the public
invertible coordinates as (a,b,t)=(D_lambda v,R_lambda v), where a,b
have r entries and t has k. With the note's Omega convention,

```
B_lambda(v,v') = b.a' - a.b',
rho_(lambda,alpha)(v,c)_(i,j)
  = [i=j+a] omega^(lambda.c + alpha.t + a.b/2 + b.j).
```

The Weyl product law and the BCH half-bracket show these are actual
representations. The a,b coordinates range over all translations and
characters, so their joint commutant consists of scalars: each is
irreducible. Different lambda are distinguished on the center. For a
fixed lambda, different alpha are distinguished by v in ker D_lambda,
on which R_lambda is an isomorphism. No extra copies are included.

Define F_- on a field register by
`|x> -> p^(-1/2) sum_y omega^(-xy)|y>`. The following sequence uses
exactly w+z field registers, with layout interpreted using lambda:

1. Apply F_- to all z central coordinates, producing lambda.
2. Reversibly map v to (a,b,t) using the public invertible matrix.
3. Apply the diagonal phase omega^(-a.b/2).
4. Apply F_- to the r coordinates of b and k coordinates of t,
   producing j and alpha. Leave a coherent.
5. Reversibly replace a by i=a+j and order output as (lambda,alpha,i,j).

For every input (v,c), the output amplitude is exactly

```
p^(-(z+k+r)/2) [i=j+a]
    * omega^(-lambda.c-alpha.t-a.b/2-b.j)
  = sqrt(p^r/|N|) conjugate(rho_(lambda,alpha)(v,c)_(i,j)).
```

All stages are unitary. For each lambda the remaining register count is
k+2r=w, even when r changes. Thus no rank-dependent dimensions are
silently created, discarded or padded in THIS QFT (later carrier padding
is a separate operation). Counting outputs also gives
`sum_(lambda,alpha) d_(lambda,alpha)^2 = p^(w+z)`.
The complete transform is therefore unitary in the exact mathematical
gate model. Unlike the fixed-sector lemma, this argument rules out a
reducible extra copy or a missing radical character.

**Measured implementation.** All stages after the first preserve lambda,
so measure it immediately and compute its basis classically. This is
exactly the same instrument as the complete QFT followed by label
measurement, not postselection or a promise about the input. Alpha may
likewise be measured after its Fourier transform; trace the row i only
after the final addition, retaining j. Neither v nor a may be measured
in their place. This implementation needs public finite-field elimination
only for the observed lambda, not an exponential lookup table or a
coherent enumeration of all p^z labels. A coherent version can instead
reversibly compute and uncompute the same basis from retained lambda.

Computing B_lambda takes O(z*w^2) field operations. Deterministic pivoting,
alternating-form elimination and inversion use polynomially many field
operations (a conservative O(w^5) bound suffices for the reference
strategy). Synthesis of an invertible w-coordinate map uses polynomially
many modular arithmetic gates. There are z+k+r<=z+w cyclic transforms,
r products for the half-phase, and r additions at the end. Using standard
[approximate cyclic QFTs](https://arxiv.org/abs/quant-ph/0212002), the
resulting instrument has cost polynomial in w,z,log p,log(1/eta) for
joint channel error eta. This is a circuit existence/cost argument under
the EXPLICIT BCH coordinate promise, not a compiled gate-list benchmark.
The classical dense diagnostic below deliberately does NOT have that
runtime and must never be used as the asymptotic implementation.

For a bounded execution with at most Q_source uses, allocate a uniform
joint instrument error at most epsilon_QFT/Q_source to each use. Charge
all cyclic transforms and phase synthesis inside that allocation; exact
reversible field arithmetic still costs gates. The hybrid bound includes
the measured labels, row discard, subsequent adaptive choices and ABORT.
Do not divide by the probability of a rare label and claim the resulting
normalized branch has the same error guarantee. Input-to-BCH transport
and the rest of the receiver retain their own error/resource costs.

**Independent finite falsifiers.**
`tests/test_class_two_fourier_instrument.py` applies the Fourier,
permutation, diagonal-phase and addition stages to basis columns, then
compares against independently assembled representation coefficients.
It covers moving radicals, rank 0/2/4 forms, and nonzero central labels
with zero Weyl rank; the whole map is unitary. An actual ordinary-coset
source gives the expected matrix kernel in every sector. Omitting the
half-phase preserves unitarity but fails the BCH representation law and
the required coefficients. Unitarity alone is therefore not a convention
or source certificate. These are reference controls, not a new oracle
problem, a Lean completeness proof, or a full class-four solver.

### Plancherel Source And Normalization

Under Plancherel the central lambda is UNIFORM on F_p^z: there are
p^(w-2s) radical characters, each of squared irrep dimension p^(2s), so
their total weight is p^w/|N|=p^(-z), independent of rank. Conditional
alpha is uniform. Transversality is what licenses this Plancherel source.
The normalized active kernel is

    1/(p^m p^s) 1[q'-q in U] W(q)^dagger W(q'),
    W(q)=rho_(lambda,alpha)(F(q)).                            (2)

Normalization audit. With V=G/N, d=dim rho and q in V, the actual
ordinary mixed source is

    rho_H=1/|G| sum_(g,h in H) |g><gh|.

In the normal-first chart g=n exp(q), transversality gives one h for each
u in U, with right action (n,q)->(n F(q)^-1 F(q+u),q+u). For the
CONJUGATED normal QFT, Schur orthogonality gives

    sum_n conjugate(rho(n)_ij) rho(n t)_kl
       = |N|/d delta_ik rho(t)_jl.

Including both QFT amplitudes leaves the unnormalized irrep block
delta_ik rho(t)_jl/(|N||V|). Its probability is d^2/|N|. Tracing i and
dividing by that probability gives (2), with t=F(q)^-1 F(q'). No extra
|H| factor, pure-coset promise or conditioned hiding-output register is
present. Independent representation-sector controls check this trace
for both positive and zero Weyl ranks. They are not a complete group
oracle execution.

### Formal Ordinary-Source Derivation

`formal/Formal/CosetMatrixSource.lean` now starts one step earlier than
the assumed matrix kernel. For a function f separating actual H cosets,
it traces the finite amplitudes of the uniformly queried state and obtains
`|G|^-1 [g^-1*g' in H]`. It also proves the section-word identity for any
group section s and hidden homomorphism h with a linear retraction pi:

    F(q)=s(q-pi(q)) h(pi(q)) s(q)^-1,
    s(q) h(u)=F(q)^-1 F(q+u) s(q+u).

Quotient compatibility puts F(q) in the normal kernel. An actual
normal-first coordinate equivalence then supplies the right-action law.
The hidden parametrization must cover ALL H. Neither pi, the hidden lift
nor F is supplied as efficient oracle advice to the receiver.

The row trace gives a simpler proof than retaining the full Schur block:

    sum_i conjugate(rho(n)_ij) rho(n t)_ik = rho(t)_jk.

This uses only unitary representation multiplication. The formal finite
Fourier sums therefore produce `d/|G| rho(F(q)^-1 F(q'))` on the correct
support. The trace is d^2/|N|, and division yields exactly (2). The
`source_from_normal_chart` theorem composes the chart, section-word and
normalized source steps; it does not assume the desired matrix kernel
or its normal-coordinate action law as an extra axiom.

This simplification has a sharp boundary. Unitarity of ONE representation
does not establish completeness or physical validity of the whole chosen
Fourier transform. Two copies of the trivial representation of C_3 give
d^2/|N|=4/3 under the same sector scaling. The algebraic trace identity is
true, but that sector is not a physical Kraus branch. The complete
class-two factorization above supplies a separate written argument and
finite controls, not a Lean proof of QFT completeness. No claim of a
valid QFT for arbitrary N follows from this representation-general lemma.

Nine guarded universal theorems are accompanied by a finite reference
with actual nonabelian-normal group cosets, a proper quotient support and
a COMPLETE normal QFT. All sectors match (2). Reversing multiplication
fails; conditioning on one hiding-output label preserves only a single
quotient coset and does not give the required uniform mixed source.
These controls are not new oracle problems or a scalable group solver.

What remains: effective input-to-chart transport, the class-four degree
and representation facts, full QFT completeness/circuits, Clifford
realization and adaptive algorithm composition are not all
machine-checked. The proof extends a source interface, not an admitted
new algorithm or asymptotic speedup. Ordinary Fourier analysis of coset
states is established prior art, including
[Krovi and Roetteler](https://arxiv.org/abs/0810.3695); these verification
lemmas are not a claim to have invented nonabelian Fourier sampling.

Discard only lambda=0, at cost 1/(1-p^(-z))<5/4 in expectation.
Do NOT discard other labels with rank zero or condition on high rank.
Their radical characters still contribute phases. There is no p>=2r or
all-components-nonzero condition in this proposed replacement.

## 2. An Equivariant Label-Selection Lemma

Let a block contain A_4(z) independent uniform NONZERO labels in F_p^z.
Compute a nonzero witness beta satisfying sum beta_i^4 lambda_i=0, using
only the canonical row space of the label matrix and independent random
bits. Verify against the ORIGINAL labels. Canonical row reduction before
any fixed-degree diagonal solver enforces this invariance; the solver need
not otherwise be equivariant.

Fix its random seed. Left multiplication of all labels by A in GL_z(F_p)
does not change the canonical row space, witness, abort decision, or first
active index. The input distribution is invariant under this action.
Therefore the label at that selected active index is uniform on the
nonzero vectors, even conditional on successful capped solving and on the
witness/selected index. GL_z is transitive on those vectors. This is a
distributional argument, not a claim that the physical group is invariant
under arbitrary changes of central characters.

Independent local retries preserve independence BETWEEN blocks. Witness
selection must not use the Weyl rank, radical character, hidden state,
preferred coordinate of lambda, or future shear outcomes. Such selection
can bias the active label. An explicit biased-selector control fails
uniformity, while the square-witness control is invariant under all 2016
elements of GL_2(F_7).

### Checked Conditioning Boundary

`Formal/EquivariantLabelSelection.lean` now proves the weighted finite-
experiment statement behind this step. An invariant input law, invariant
acceptance event and equivariant selected label imply equal accepted mass
at every label in a transitive action. Division by NONZERO accepted mass
gives the uniform conditional law. A fixed record may be added to the
conditioning only when that record is also invariant. Zero-probability
records are covered by the unnormalized identity, not a conditional law.

For this application the label-matrix relation kernel is unchanged by
postcomposition with any invertible central linear map. The module checks
that identity and the resulting selected-column equivariance for a
kernel-only controller. Canonical row space contains the same information
as this kernel. Seed, witness, selected index, attempt count and capped
success decision can therefore be included WHEN computed from that
invariant data. Finite capped local retries can be viewed as one finite
experiment on the whole local stream and seeds, with the same symmetry.

Do not condition this uniformity claim on the FULL physical transcript.
The observed labels themselves are not invariant; radical-character
dimensions and ranks can also change under a central basis transformation.
The probability proof marginalizes those ignored records. Retaining them
for the quantum source/independence proof is compatible with marginalizing
them for this rank estimate. A rank bound conditional on each fully fixed
label transcript would be false. In adaptive use, condition on the PRIOR
history and its valid fixed chart, then draw fresh blocks and average their
new labels. The bound is uniform over such prior histories, not over all
new label outcomes.

The formal separate-postselection product identity also requires a
PRODUCT input law and a PRODUCT of local acceptance events. Uniform block
marginals do not suffice; a coupled acceptance rule can correlate them.
The new exact controls show (i) verified quartic witnesses surviving a
label-biased abort filter and (ii) uniform block marginals whose joint bad
event exceeds the multiplied per-block bound. No source/controller
implementation may replace these premises with marginal diagnostics.

These are guarded conditional Lean theorems, not a complete machine proof
of (5)-(7). GL transitivity on nonzero vectors, the per-vector hyperplane
count, the full SDE success guarantee and their actual quantum-source
instantiation remain written mathematical dependencies. The final real-
arithmetic inequality `(p^L-1)*(2/p)^(2L+2)<=1/p` for p>=5 is separately
checked. No full rank-probability certificate or new algorithm is claimed.

For p=3 mod4 use the existing square construction on canonical rows:
find gamma with sum gamma_i^2 lambda_i=0, then beta_i=gamma_i^((p+1)/4).
This needs A_4(z)=(z+1)^2 inputs. Its current implementation is a reference
machine-word backend with an uncapped internal conic loop. Bounded
arbitrary-precision production execution remains missing. For general p
the fixed-degree SDE theorem supplies the safe explicit arity
A_4(z)=4^18*(z+1)^12 from its unrounded collision recurrence, subject to
the same canonical-input/capped-failure contract. See
[the complete draft](CLASS_FOUR_HSP_THEOREM_DRAFT.md) for the rounding
caveat, four prime regimes and exact conditional resource calculator.

## 3. A Rank Bound That Does Not Require Invertible D_lambda

Set L=w(m+2), and take B=2L+2 independent successful relation blocks.
Multiply each block's witness by an independent uniform nonzero scalar
tau_b. This preserves its quartic identity. Perform the usual fresh-uniform-q
shear q_i=Y_i+s_i q on ALL active packets. Every Y_i is independent uniform
conditional on the labels; no particular outcome is postselected.

As before write the unknown quadratic noncentral potential as

    Q_W(q)=c+Aq+(1/2) sum_jk C_jk q_j q_k,
    T=stack(A,C_1,...,C_m), D=w(m+1).

The public displacement maps now have possibly different block heights:

    K_i=s_i^2 D_(lambda_i),
    J_i=[s_i D_(lambda_i), s_i Y_i1 D_(lambda_i), ...].        (3)

Their quadratic image is isotropic because

    K^T Omega K = sum_i s_i^4 B_(lambda_i)=0.                (4)

For ANY fixed nonzero c in W,

    Pr_lambda[D_lambda c=0] <= 1/p.                        (5)

Indeed c is not in the common radical, so beta(c,v)!=0 for some public
v. A uniform nonzero lambda annihilates that nonzero central vector with
probability (p^(z-1)-1)/(p^z-1) <=1/p. No maximal-rank form is required.

Fix a nonzero proposed kernel vector (c0,c1,c2,...,c_(m+1)) for [K|J].
Its selected row block vanishes only if

    D_lambda(s c0+c1+sum_j Y_j c_(j+1))=0.                 (6)

If some c_(j+1)!=0, (5) fails with probability at most 1/p. Otherwise,
condition on labels/scales and other Y coordinates: at most one value of
Y_j solves (6). Hence the bad probability is at most 2/p. If all those
derivative directions vanish but c0!=0, use the independent nonzero tau_b
instead: except with probability <=1/p, at most one of p-1 multipliers
works. The total bound is again <=1/p+(1-1/p)/(p-1)=2/p. If only c1 is
nonzero, (5) suffices.

The selected labels are independent across the independently prepared
blocks. Vanishing on ALL active rows implies vanishing on these selected
rows. Union bound over the p^L-1 possible nonzero kernel vectors gives

    Pr[rank(K|J)<L] <= (p^L-1)(2/p)^B <= 1/p,              (7)

since p>=5 and B=2L+2. Rank is checked publicly, with a bounded number of
fresh full-block retries. For a bad realized design do not invent a
certificate, reuse consumed packets, or quote (7) as a deterministic pass.
The bound counts solving/label aborts separately; it is conditional on
independent successful block preparation.

This repairs the earlier UT5 argument's essential gap: D_lambda may be
rectangular, rank-changing, or zero, and w may be odd. The witness's row-space
invariance and independent block multipliers are essential assumptions,
not implementation conveniences.

### Formal Matrix-Batch Channel And Conditional Alignment

`formal/Formal/MatrixBatchShear.lean` now checks the batch channel for
arbitrary unitary matrix gauges and arbitrary, possibly different, finite
carrier types C_i. It reuses the scalar proof's common-support lemma.
For n independent normalized matrix sources with the SAME U, let

```
Q = F_p^m,     C = product_i C_i,
W_Y(q) = tensor_i W_i(Y_i+s_i*q),
K_Y[(q,t),(a,r)] = |Q|^(-1/2) [a_i=Y_i+s_i*q for all i] [r=t].
```

K_Y is exactly a fresh coherent uniform q, subtraction of s_i*q from
every old quotient, measurement of all those old quotients, and retention
of the carriers. It contains no U or hidden gauge coefficients. From the
TWO full Kraus sums the proof derives

```
K_Y (tensor_i rho(U,W_i)) K_Y^dagger = |Q|^(-n) rho(U,W_Y),
Pr[Y] = |Q|^(-n),
sum_Y K_Y^dagger K_Y = I.
```

The first identity requires some s_i != 0. Carrier multiplication is
proved explicitly: the kernel of the tensor gauge is the product of the
individual W_i(q_i)^dagger W_i(q_i') kernels, including all dimension
normalizers. Completeness does not need any source promise or nonzero
weight. The operator definitions are mathematical kernels; implementing
the shear uses O(n*m) field arithmetic operations plus fresh uniform
state preparation and measurement, NOT a table of K_Y entries.

Consequently the full Y_i tuple really is independent uniform, conditional
on a fixed complete public transcript for PRODUCT inputs. Fresh ordinary
oracle preparations on the same instance provide that premise; correctness
of isolated marginals does not. Classical selection based on the recorded
labels/scales may be conditioned on, but it cannot license recycling
consumed sources or retaining shared preparation purifications.

Zero weights have a precise treatment. A zero-weight input contributes
only an identity carrier kernel and a maximally mixed carrier factor.
It can be discarded. If discarded before the shear, n in the outcome law
counts only the active inputs and there is no random Y_i to record for
that discarded slot. If EVERY weight is zero, the output is full-support
uniform q coherence times the mixed carrier, independent of U. This is
proved separately, not classified as a successful merge. Wasted original
queries remain charged to the source budget.

For an actual carrier unitary C_Y, fixed within the observed branch, the
formal double-sum calculation gives the source with gauges

```
W'_Y(q) = C_Y W_Y(q) C_Y^dagger.
```

Only C_Y is physically applied. W'_Y is a proof description of the
resulting kernel, not an instruction to evaluate the hidden W_Y or T.
Common left multiplication of all gauges cancels from W(q)^dagger W(q');
left multiplication alone would therefore fail to represent the actual
carrier basis change. Right-only multiplication by C_Y^dagger gives an
equivalent kernel, but conjugation is the useful Weyl-coordinate form.

`aligned_branch_identity` composes this with the batch Kraus identity.
`conjugation_to_scalar` then composes physical carrier conjugation and
spectator measurement whenever the EXACT resulting gauge is the monomial
one with displacement `(a+Tq,b)` and constant spectator b. Its output is
the existing `AffineSupportErasure.rho` on graph(-T on U), with phase
conjugate gamma. This is not an inference from a finite-field rank check.
C_Y denotes a Hilbert-space unitary, NOT the public symplectic matrix S;
the Lean proof still assumes the correctly phased realization of S. The
public arithmetic-qudit compiler described below now supplies a written
constructive realization, separately from that formal proof.
The equivalence/reindexing of tensor carriers with retained/spectator
coordinates, mixed padding, polynomial cancellation and SAME T/parameter
provenance across batches are not all composed in Lean here.

Ten independent finite controls in `tests/test_matrix_batch_shear.py`
contract sparse physical Kraus operators. They cover all outcomes with
different carrier sizes, active/zero/all-zero scales, carrier conjugation,
and a three-stage shear/alignment/spectator composition with proper U.
Four premise falsifiers are particularly important:

- A shared random coset gives correct single-source marginals but correlated
  Y outcomes: only one third of tuples occur in the control.
- Different supports intersect under the shear. The control becomes
  completely mixed even though outcome probabilities stay uniform.
- A maximally mixed rather than coherent fresh register also leaves
  uniform outcome rates but destroys all useful support coherence.
- Reusing an old pivot fixes its Y to zero. That alternative needs a new
  rank analysis; it is not the independent-outcome instrument proved here.

All eight headline Lean guards allow only the standard axioms. These
results verify a conditional algorithmic interface, not a new quantum
algorithm or novelty of coordinate-shear phase cancellation. The latter
is established work, including
[Decker--Hoyer--Ivanyos--Santha](https://arxiv.org/abs/1305.1543).

## 4. Padding, Canonical Support And Cubic Phase

Let R0=sum_i rank(B_(lambda_i))/2. Append freshly prepared maximally mixed
qudits until R=max(R0,D+w). Appending I/p is a real channel: prepare a
maximally entangled pair and discard its partner, independently per qudit.
It is NOT an all-zero ancilla, retained purification, reusable classical
seed or hidden state-preparation oracle. It costs O((D+w) log p) qubits,
Fourier/field gates and discarded workspace, no extra hiding queries.
The enlarged gauge is W(q) tensor I, normalized with carrier dimension p^R.

After passing (7), K is injective and im K intersects im J trivially.
[DETERMINISTIC_JET_ALIGNMENT.md](DETERMINISTIC_JET_ALIGNMENT.md) replaces
the former random transverse-Lagrangian step. Explicit targets for K,J
preserve their full alternating Gram matrix; at most 2(w+D) deterministic
transvections extend this isometry. It applies to odd w and degenerate
restricted Gram matrices. No alignment failure probability or retry cap
remains. The verified public Clifford symplectic matrix S satisfies

    (SK)_X=0, (SJ)_X=(I_D,0).                              (8)

Thus the X displacement is constant+(Tq,0), IDENTICAL across new batches.
The Z displacement has degree at most two. Before the Clifford, scalar
phase is

    psi(q)=sum_i lambda_i Q_Z(Y_i+s_i q)
                 +alpha_i R_(lambda_i) Q_W(Y_i+s_i q).

Its quartic part cancels by the same label relation; the radical-character
term has degree at most two. Hence psi has degree <=3. The symmetric-Weyl
conversion adds one half X.Z, also degree <=3. Measuring only the spectator
carrier coordinates, accepting all outcomes, leaves the fixed scalar support

    U_jet={(u,-Tu):u in U} <= F_p^(m+D)

with scalar potential degree at most THREE, exactly as in the scoped UT5
route. Keep the radical phase even for zero-dimensional Weyl carriers.

### Public Clifford Realization

`theorems/prime_clifford_realization.py` now compiles the verified S into
at most `4*R^2+3*R` one/two-qudit modular primitives, with O(R^3) field
operations and O(R^2) field-element storage. It handles singular X/X
blocks and arbitrary-size odd primes without field or state enumeration.
Only S and p are inputs. Its universal primitive/elimination argument is
in [PRIME_CLIFFORD_REALIZATION.md](PRIME_CLIFFORD_REALIZATION.md).

Every primitive satisfies EXACT symmetric-Weyl covariance, so
`C_S D(v) C_S^dagger=D(Sv)` without a v-dependent phase. Therefore
`omega^psi(q) D(v(q))` becomes `omega^psi(q) D(Sv(q))`; psi is unchanged.
The usual `t*(t-1)/2` phase gate has the same tableau but adds a linear
character and is explicitly rejected by an independent dense control.
This is known Clifford synthesis with a checked local convention, not a
new algorithm. The plan is not Lean-certified or a native qubit backend;
approximate transforms/rotations and total channel errors remain charged.

### Common Scalar Parameter

The generic public compiler now exists in
`theorems/class_four_scalar_phase_compiler.py`. It substitutes the public
affine maps into formal Q_W/Q_Z coefficients, retains each label's radical
character, applies the verified S, and constructs

    P(q,t)=-psi(q)-A(q).B(q)/2-B(q).t,

substituting ONLY measured spectator values. It checks transcript
compatibility and cubic degree. The Weyl-to-scalar step is shared with
the UT5 compiler; their source-specific parameter schemas remain distinct.
No unknown coefficient is evaluated by the controller. Exact tests compare
to separately evaluated gauges at one and two variables, including mixed
monomials, different carrier widths and a 127-bit prime.

The parameter basis is fixed across batches. Set

    hW=w*C(m+2,2), hZ=z*C(m+4,4), h=hW+hZ.

Only the hW noncentral coefficients participate in products, so the common
lift (1,theta,all noncentral coefficient pairs) has dimension at most
P=1+h+hW(hW+1)/2. The existing packet property's larger bound
1+h+h(h+1)/2 is safe but loose; sparse terms do not materialize absent
central products. D_lambda, R_lambda, alpha, S, Y and spectator outcomes
are public coefficient-map data, not new hidden parameters.

Equal descriptor bases do NOT establish equal hidden parameters. Every
tree must use one oracle instance and one fixed chart. An explicit
countercontrol makes two identical public maps cancel formally while
different hidden coefficient assignments leave a nonconstant phase.
The scalar compiler does not certify this provenance, prepare the source
or execute its coherent instrument. The public Clifford plan above has
the required covariance; a different backend must preserve it or compute
and include every linear phase correction, not silently omit one.

### Why The Jet Is Actually Common

Matching packet metadata does not prove this. There is a universal
algebraic argument, now checked in `Formal/CommonQuadraticJet.lean`.
Write the SAME fixed proof-only potential as

```
Q_W(q)=a+L(q)+B(q,q),
T(q)=(L(q), [y -> B(q,y)+B(y,q)]).
```

B is any bilinear representation of its quadratic part; symmetry is not
required. Over the present odd field one may choose the symmetric one.
In the fixed quotient basis, evaluation of the second component on basis
vectors is exactly the C_1,...,C_m block order in (3). Thus this abstract
jet has dimension w*(m+1), not a function table of exponential size.

Embed each label-dependent D_i in the joint carrier with the existing X/Z
ordering and zero padding. For arbitrary scales and outcomes, bilinearity
gives the identity

```
v(q) = v(0) + J(T(q)) + K(B(q,q)).
```

Here K(w)=sum_i s_i^2 D_i(w), and
J(j_0,j_1)=sum_i s_i D_i(j_0+j_1(Y_i)). These are exactly the existing
public maps, not maps depending on L or B. If A is the X projection after
the public S, the checked identities AK=0 and AJ(j)=(j,0) imply

```
A(v(q)) = (a_Y + T(q), b_Y).
```

The affine constants can depend on the entire branch and unknown
potential. The derivative T CANNOT depend on lambda, alpha, scales,
Y, alignment randomness, carrier size or spectator outcome. The Lean
`different_batches_same_jet` theorem permits different source index sets
and carrier spaces. `quadratic_source_to_scalar` composes the derived
affine displacement with the previous actual spectator Kraus theorem:
every batch yields the same graph(-T on U). The finite-field rank
certificates remain hypotheses, as do the upstream genuine quadratic
potential and correct physical Clifford/source realization. Neither T
nor B is an operational input.

### Shared Parameters Survive The Erasure Tree

Fix the oracle, chart, proof-only projection/lift and the ordered formal
coefficients theta ONCE. Public transcript data only change coefficients
c_(i,alpha,tau) in

```
P_i(x;theta)=sum_(alpha,tau) c_(i,alpha,tau) x^alpha theta^tau,
```

where |alpha|<=3 and tau is empty, a single base index, or a pair of
noncentral base indices. All nodes use this SAME theta, including zero
coefficients absent from a sparse dictionary. Translate and combine:
P_new(x;theta)=sum_i P_i(y_i+s_i*x;theta). For |alpha|=d, its degree-d
coefficient at theta^tau is exactly

```
sum_i s_i^d c_(i,alpha,tau).
```

Translation does not alter the leading coefficient; substitution and
addition never multiply two theta monomials. A verified diagonal witness
annihilating EVERY public (alpha,tau) row therefore lowers the degree for
EVERY fixed theta, preserves the parameter lift, and leaves the common
graph support unchanged by `AffineSupportErasure.mixed_branch_identity`.
The unknown lift need not be surjective or recoverable: cancellation in
the larger formal parameter space is sufficient. Sparse row compression
must preserve all original equations, and the square solver needs
(rank+1)^2 inputs in its implemented congruence regime, not rank+1.
This binomial/substitution argument is written, not yet a Lean polynomial
degree theorem. Degree erasure is a known method, not itself novelty.

Independence is a protocol property. Use a forest of DISJOINT fresh oracle
preparations; retain the full classical transcript and random choices.
Conditioned on that full transcript, each root has the stated source
kernel, and roots on disjoint leaves factor. Public adaptive choices are
then fixed maps; each legal merge consumes its roots, including zero-scale
inputs. Induction preserves the product premise and common theta. Averaging
over discarded shared records or reusing a physical root can break it.
Instance/chart strings and Python object identities cannot prove this.

The existing sparse adapter now rejects a repeated wrapper in a single
merge as well as consumed wrappers. Its incorrect helper imports, conic
keyword and report's understated square-stage arity were corrected.
Distinct fresh sources with identical public maps remain legal. Controls
also reject a witness that cancels only at one diagnostic theta assignment,
and show that changing the hidden chart can change support despite an
identical public transcript. These fixes do not make the diagnostic
erasure tree or truth-supplied class-descent sampler a quantum execution.

### Formal Measurement Bridge

`formal/Formal/WeylSourceScalarization.lean` now checks the conditional
matrix-to-scalar step for arbitrary finite module dimensions, hidden U and
unit-modulus phases. Define the actual monomial matrix entries by

    W(q)[r,t]=1[r=A(q)+t] gamma(q,t),
    gamma(q,t)=omega^(psi(q)+A(q).B(q)/2+B(q).t).

Its adjoint product is evaluated by summing over r, not assumed as a
target scalar formula. With carrier C=J x S and A(q)=(a+Tq,b), the
spectator Kraus operator is the coordinate selector

    K_s[(q,j),(q',(j',s'))]=1[(q',(j',s'))=(q,(j,s))].

The two sums defining K_s rho K_s^dagger give exactly

    |S|^-1 rho(graph(-T on U), conjugate gamma(q,(j,s))).    (10)

All spectator outcomes have trace |S|^-1 and the Kraus family is complete.
No outcome is postselected. The output is literally the scalar `rho`
definition consumed by `Formal/AffineSupportErasure.lean`; no separate
notion of phase packet is substituted. Thus this part does not depend on
the small-prime fixtures or polynomial interpolation. T,U are proof
witnesses, not inputs to the measurement operations. Equality of U,T
across separately prepared packets remains an upstream obligation.

The proof also identifies a stronger falsifier. If the measured spectator
has displacement b+Lq, the output support is graph(-T on U intersect ker L),
not generally graph(-T on U). Its outcome probabilities are STILL uniform.
Only L|_U=0 preserves the intended support; global L=0 is the sufficient
condition certified by the canonical alignment. Measuring the entire
affine carrier retains only U intersect ker T and is completely dephasing
when T is injective. Independent density-matrix controls include a proper
U, a leaking spectator and a noninjective T. This rules out accepting a
measurement because its trace/normalization tests pass.

The seven guarded Lean headlines use only the standard axioms. This does
NOT itself formalize the normal QFT, Schur conversion, common
class-four potential, Clifford realization, polynomial cancellation,
source independence, complete HSP reduction or costs. Positivity of the
input kernel is not separately proved in this module. It is a conditional
channel identity, not a certification of the preceding whole proposal.

## 5. Proposed Arbitrary-H Completion And Its Cost

The obstruction motivating this pass can now be addressed CONDITIONALLY
on the full generic source proof and earlier cubic erasure argument:

1. Use the known nil-2 HSP algorithm on the ORIGINAL oracle restricted to
   N=G' to learn K=H intersect N. Charge this call and its error budget.
   Correct K is a premise of the subsequent ideal proof. Membership tests
   on returned generators alone cannot detect a missed part of K; retain
   the published solver's failure guarantee in the global error budget.
2. Compute M=N_G(K) publicly. In Lazard coordinates this is the linear
   condition [x,log K] subset log K. H normalizes K, so H<=M.
3. Work in M/K, with explicit quotient coordinates and reversible choice
   of representatives. Since K<=H and K is normal in M, one original
   oracle call gives a legitimate hiding oracle for H/K. It is not a
   free quotient-source or postselection service.
4. The new derived group is class two and H/K intersects it trivially:
   M'<=G', so a representative in H intersect M'K is in K. Apply the
   GENERIC source above, not the direct-product UT5 representation schema.
5. After learning its quotient image, restrict to its public preimage.
   For a transverse Hbar and Nbar=Gbar', (Hbar Nbar)' is contained in
   gamma_3(Gbar), so this preimage T1 has class at most three. One
   class-three quotient-image call learns Hbar*T1'/T1'; its preimage T2
   has commutator in gamma_4(Gbar), hence class at most two. A second
   known nil-2 HSP call on T2 recovers Hbar. Lift with K. The argument
   in CLASS_FOUR_HSP_THEOREM_DRAFT.md avoids relying on the broader
   metabelian descent controller or a supplied ideal Fourier sampler.

All group and representation dimensions are polynomial in the explicit
input size; the degree bound is fixed. One scalar packet consumes
B*A_4(z) accepted normal-source packets, including zero-scale waste.
The later cubic, quadratic and linear erasure arities MULTIPLY this cost.
Retries, the nil-2 call, public arithmetic, mixed padding, field transforms,
Clifford synthesis, all approximation errors and the final descent must
be budgeted jointly. The polynomials can be impractically large.

This suggests removing the transverse-H/direct-product restriction at
the written class-four core level. It does NOT make a completed theorem.
Extending from exponent-p explicit cores to the full subgroup/quotient-closed
class-four family also requires the actual published group-theoretic
reduction promises and treatment of small primes. Those are dependencies,
not consequences of the new numerical controls.

## 6. Bounded Source And Error Contract

This is a proposed finite schedule, NOT implemented by the current reference
backends. Assume correct initial K and the exact group/source promises.
For error target 0<epsilon<1 in one quotient-image call, set v=m+D and
use the fixed lifted parameter dimension P above (or its safe larger bound).
At scalar degree j there are at most

    E_j=P*C(v+j-1,j)

public homogeneous coefficient equations. Let a1=E_1+1 and let a2,a3 be
valid polynomial SDE arities for degrees two and three. In the p=11 mod12
reference regime, a2=(E_2+1)^2 and a3=E_3+1 suffice. For other p use the
published fixed-degree diagonal algorithm, not these special-prime formulas.
The degree-one step is ordinary linear dependence, not the d>=2 theorem.
Define

    t=v+ceil(log_p(4/epsilon)),
    M=t*a1*a2*a3, T=B*A_4(z).

Here M bounds matrix-to-scalar packets, and T bounds accepted nonzero
central labels per matrix packet. This counts zero-scale waste. There is
no additional scalar quartic-erasure stage. The t erased Fourier roots
span the true annihilator except with probability at most
p^(v-t)/(p-1)<epsilon/4. Independent fresh trees and exact erased sources
are essential to that bound.

One bounded matrix-packet attempt can have total failure <1/4:

- Fill every label slot with at most
  r_label=ceil(log_(p^z)(100T)) fresh ordinary-source draws. The probability
  that any slot never sees lambda!=0 is <=1/100. Accept all ranks/alphas.
- On canonical row-space input, cap/verify each quartic witness so its
  failure is <=1/(100B). All witness aborts total <=1/100. This needs a
  proven runtime or success guarantee for the solver; a timeout alone is
  not such a guarantee. Classical solver retries happen before shear.
- Public jet-rank failure is <=1/p<=1/5, conditional on successful label
  and witness preparation. A failed shear consumes that entire packet.
- Alignment is now deterministic, with ZERO failure on a valid rank/isotropy
  design. Retain <=1/100 for the independent nonzero block multipliers:
  each bit-string rejection draw succeeds with probability >=1/2, so
  ceil(log2(100B)) draws per multiplier suffice. Conditional uniformity
  and independence are preserved; preferred-coordinate selection is not
  a replacement. Quartic-solver randomness is in its separate allocation.

These bounds sum to 3/100+1/p<1/4. Use fresh independent full attempts, capped at

    r_mat=ceil(log_4(4M/epsilon)).

The chance that any of M requested matrix packets exhausts its cap is
then <=epsilon/4. This produces the explicit original hiding-query bound

    Q_source <= M*r_mat*T*r_label.                         (9)

Each source query also pays reversible group/quotient encoding costs.
No conditional source, retained measurement purification or previously
consumed packet is free. The bound is deliberately conservative.

There are at most M scalar SDE merges in these trees. Give each a
verified capped classical failure probability <=epsilon/(4M), totaling
<=epsilon/4. Reattempting a solver on the same UNMERGED packets need not
consume new oracle queries, but its bounded computation/time is charged.
The existing square backend's uncapped conic loop and machine-word field
arithmetic do not satisfy this execution contract. The published general
fixed-degree algorithm is a mathematical dependency, not code present here.

Finally allocate <=epsilon/4 TOTAL channel error over every approximate
field transform, source operation and Clifford implementation in the
worst-case bounded adaptive schedule. Choose per-operation precision from
that operation count. Compose channels WITH an explicit ABORT branch;
do not divide the error by the probability of a selected rare outcome.
The four error allocations sum to epsilon. Public rank checks and terminal
membership tests do not independently repair approximate-source loss of H.

All dimensions and arities are polynomial in the explicit group size
description and log p at fixed degree, though the polynomial can be enormous.
Every classical SDE solve, symbolic operation, mixed ancilla and Clifford
gate must also be counted; (9) is a query bound, not the whole runtime.
Add independent error allocations and costs for initial nil-2 solving and
the subsequent class-three descent. Across fresh subgroup restrictions
these costs SUM; within one erasure tree its arities MULTIPLY. A written
finite schedule is not a completed coherent implementation or formal proof.

`theorems/class_four_complete_budget.py` now evaluates this schedule using
exact integers/rationals, including all four prime-residue regimes. Its
standalone report is an analytic envelope, NOT a source execution or a
complete arbitrary-H gate budget. The consolidated theorem draft makes
the two quotient-image/two nil-2 calls and their remaining premises explicit.

## 7. Adversarial Prior-Art Comparison

The diagonal-solver/phase-cancellation method is prior art, not the proposed
contribution. Ivanyos--Santha's stated univariate phase-graph result and
their specific semidirect-product reduction do not by themselves implement
the varying-rank normal source here. Reuse them with their actual promises.

Decker--Ivanyos--Santha--Wocjan's multivariate HPGP reduction uses the full
oracle f(x,y), with equality determined by y-Q(x). Its line restrictions
query f(vx,y). Here the available objects are mixed phase states with
support on an UNKNOWN U_jet; such a restricted full graph oracle has not
been supplied. Thus the HPGP theorem cannot simply be called on these
packets. This interface difference is NOT a proof of novelty: another
reduction or equivalent literature formulation could subsume the proposal.

Known nil-2 HSP, bounded-class group reductions and quotient-image recursion
remain external dependencies. The review target is the complete ordinary
source -> variable-radical canonical jets -> common-parameter scalar erasure
composition. Literature searches and internal tests have not established
that this is new, correct in every case, or algorithmically useful outside
the oracle setting. Independent full-proof review remains necessary.

## Falsifiers And Evidence

Classical/impact filter: the existing bounded-class chosen-value
derivative attack still applies whenever the ORIGINAL hiding labels are
bounded-degree field polynomials and its characteristic promises hold.
The polynomial quantum intermediate does not supply classical access to
those coefficients. Opaque-label HSP is the research interface, not a
demonstrated practical application or hardness assumption for a concrete
encoding. Existing transporter/canonicalization costs also still apply.
This proposed broader source does not establish a speedup for factoring,
graph isomorphism, lattices, code equivalence or another external task.

- Non-Plancherel labels before a valid normalizer quotient invalidate (5).
- A unitary representation alone does not certify a complete normal QFT;
  fixed-sector traces may even exceed one for a reducible non-QFT family.
- Keeping one hiding-output label is not the mixed ordinary source assumed
  here. Its quotient diagonal can be restricted to one proper affine coset.
- Rank-dependent or coordinate-biased witness selection invalidates the
  equivariance lemma. A successful quartic equation alone is insufficient.
- A nonzero common radical means the public normal-group center was not
  fully removed; the current rank proof rejects it explicitly.
- Constant block multipliers can leave K equal to the first J block;
  public full-rank rejection is essential.
- Replacing mixed padding by pure zero states invalidates the uniform
  carrier density used in the source-to-scalar proof.
- Dropping radical characters can destroy QFT unitarity even when all
  Weyl maps and symplectic identities appear correct.
- Uniform measured-outcome probabilities do not certify preserved support:
  a spectator varying as Lq removes all U directions outside ker L.
- Matching matrices or passing tests does not validate the complete
  adaptive protocol, establish novelty or supply a non-oracle application.

`class_four_matrix_source.py` implements exact public alternating-form
factorization, varying-height jet maps, padding accounting, verified
symplectic alignment and the exact rank-bound expression. The shared
geometry was extracted from the UT5 controller, whose controls remain.
`test_class_four_matrix_source.py` includes the actual free-Lie structural
example, exhaustive small-form ranks, GL_2 equivariance, a biased selector,
exact one-block probability counts, variable-radical alignment, explicit
padding, zero-Weyl-rank sectors and QFT radical-character checks.

The generic compiler adds controls for multiple batches sharing a fixed
symbolic basis, mixed multivariate monomials, large-prime coefficients,
zero-Weyl radical phases, incompatible transcripts and wrong-instance
cancellation. Direct Schur traces check sector probabilities and normalized
matrix kernels, without replacing them by a pure-state assumption.

Verification: this compiler/trace extension adds 12 controls. All 58 focused
tests and 582 connected Python tests PASS (65.83s for the connected run,
RuntimeWarning fatal). Touched Python syntax, the existing formal crosscheck,
site JS/site checks and qsearch validate (valid:true, issues:[]) PASS.
Full repository Python tests and a new Lean build were NOT run. These checks
do not formally certify the derivation, the finite schedule or novelty.

Measurement-bridge extension: seven guarded universal Lean headlines and
three new density-matrix controls. The connected Python suite now has
585 passing tests (69.11s, RuntimeWarning fatal), including 61 focused
tests. Touched Python syntax, existing formal crosscheck, site checks and
qsearch validation pass. The normal Lean library `lake build --wfail` passes
(3312 jobs), including all seven guards. Full repository Python tests were
not run. This does not turn the conditional interface into an HSP proof.

Ordinary-source extension: nine additional guarded Lean headlines and two
new finite source tests, including several failure controls. The normal
library `lake build --wfail` passes (3313 jobs). All 587 connected Python
tests pass (70.87s, RuntimeWarning fatal), including 63 focused tests;
syntax, existing formal crosscheck, site checks and qsearch validate also
pass. Full repository Python tests were not run. The new formal source
identity still does not certify full QFT realization or the whole algorithm.

Matrix-batch extension: eight new guarded Lean headlines in the normal
library build (3314 jobs PASS), ten new physical controls, 79 focused
tests and 622 connected Python tests PASS (75.28s, RuntimeWarning fatal).
New Python syntax, generated formal crosscheck, site checks, qsearch
validate and whitespace checks pass. Full-repository Python tests were
not run. Exact aligned-gauge realization remains an explicit premise.

Public-Clifford extension: 30 new controls and 652 connected Python tests
PASS (81.46s, RuntimeWarning fatal). Touched Python syntax, formal generated
crosscheck, site checks, qsearch validate and whitespace PASS. Full-repository
Python and Lean build not rerun; no Lean source changed in this extension.
The arithmetic-qudit realization has a written universal proof, not a
Lean compiler certificate or a native qubit/error-synthesis backend.

Common-jet extension: seven guarded Lean headlines, full normal build
PASS (3315 jobs), four common-jet controls and five adapter regressions.
The adapter's previously unrun tests exposed API and reference-budget
errors, now corrected. All 673 connected Python tests PASS (136.33s,
RuntimeWarning fatal), as do syntax, formal crosscheck, site checks,
qsearch validate and whitespace. Its standalone report was regenerated
with explicit ideal-fixture/symbolic-only scope. Full-repository Python
tests were not run; no algorithm claim was admitted.

NEXT: isolate and adversarially review the precise end-to-end theorem,
its dependencies/costs and credible impact route. The
ordinary fixed-sector conversion and conditional spectator instrument are
now machine-checked, as are the matrix batch shear and conditional
carrier-conjugation/scalar bridge and common-jet algebra above. Do not
re-prove them with more fixtures. Effective
input transport, complete QFT/circuit/capped-solver, independent review and
external-application gaps remain. Do not extend class by analogy or promote
a claim because the reference suite passes.

Selection/conditioning extension: eight new guarded headlines in
EquivariantLabelSelection, normal Lean build PASS (3316 jobs). Two new
failure controls and 285 connected Python tests PASS (54.77s,
RuntimeWarning fatal), as do touched syntax, formal generated crosscheck,
site JS/site checks, qsearch validate and whitespace. Full-repository
Python tests were not run. Conditional balance and the final arithmetic
bound are machine-checked, NOT the entire rank/source/composition theorem.

Primary dependencies, not novelty endorsements:
[Ivanyos, Sanselme and Santha](https://arxiv.org/abs/0707.1260) supply nil-2
HSP and a general bounded-class group reduction;
[Ivanyos and Santha](https://arxiv.org/abs/1503.09016) supply fixed-degree
diagonal solvers;
[Decker, Ivanyos, Santha and Wocjan](https://arxiv.org/abs/1107.2189)
give the full-oracle multivariate HPGP reduction;
[Imran and Ivanyos](https://arxiv.org/abs/2304.08376)
establish the quotient-image/restriction strategy in their stated regime.
The variable-radical rank argument (3)-(8) is local proposed work and
has not been independently certified.

Efficient modular Clifford descriptions and one/two-qudit decompositions
are also established work, not a proposed novelty here:
[Hostens, Dehaene and De Moor](https://arxiv.org/abs/quant-ph/0408190).
The local formal measurement proof does not implement that decomposition.
The separate public compiler above fixes and checks its phase convention
at the arithmetic-qudit level; native synthesis remains separate.
