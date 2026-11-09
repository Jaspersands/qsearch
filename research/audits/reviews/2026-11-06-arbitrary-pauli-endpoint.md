# Arbitrary-Pauli one-rotation endpoint: independent scope and covariance review

2026-11-06. REVIEWED local coordinate/correction interface and native endpoint.
This review does NOT close the separately assigned odd-Y Bell-law/gap or
active-block extraction proofs. No implementation, numerical control, novelty,
classical separation or quantum execution is asserted.

Read: STATE.md, TRAPS.md, ONE_ROTATION_MAGIC_LEARNING.md, the closed
one-rotation cubic-axis review, and the actual retained Haug2609.27128 text
(Theorem2, Eq11, Corollary3, Theorem4 and the process-learning discussion).
Focused corpus been-tried/baselines queries were run before the assessment.
The catalog's tensor-network suggestion does not by itself simulate an
unknown Clifford-hidden source. No external service or network was used.

## 1. Exact native endpoint and why it is a meaningful bounded extension

Input: fresh exact copies of

    |psi> = C exp(-i*pi*P/8)|H>^n,

where C is an unknown n-qubit Clifford and P is an arbitrary Hermitian
Pauli, including arbitrary support and X/Y/Z factors. No C, P, support,
preparation inverse, controlled source, conjugate source or process-query
access is supplied. Output is a known polynomial-size pure-state preparation
within trace distance epsilon, with failure at most eta and target cost
poly(n,1/epsilon,log1/eta). Recovering the original C or P is NOT required.
P=+/-I is just the known Clifford-product family up to global phase.

This is exactly the state-learning endpoint

    C_out T_j C_in |H>^n,

up to global phase: put C=C_out C_in and P=C_in^dagger Z_j C_in.
Conversely every nonidentity Pauli can be obtained this way by a Clifford.
The sign of P is immaterial to the class because a Pauli pi/4 rotation is
Clifford. This is one ADDITIONAL T gate on an extensive magic-state input;
it is not a one-T circuit on a stabilizer input.

Removing the all-qubits-Z promise therefore completes a recognizable circuit
architecture rather than merely adding another numeric parameter. It is a
reasonable bounded closure of the cubic mechanism, conditional on the gates
below. It remains a quantum-input learning result, not the desired classical-
input superpolynomial quantum algorithm. It does not justify automatically
extending to two rotations, noise, general MPS inputs or channel recovery.

## 2. Explicit local affine normal form

Use one-qubit labels (x,z), q_i=xz and B_i={0,X,Z}. For each local label p_i
choose the following affine map g_i(v)=A_i v+t_i:

    p_i=I or Z:  g_i(x,z)=(x,z);
    p_i=X:       g_i(x,z)=(z,x);
    p_i=Y:       g_i(x,z)=(x+z+1,z).

Every A_i is symplectic. Each full affine map preserves q_i and permutes
B_i. In the Y case, A_i=[[1,1],[0,1]], t_i=(1,0), and

    (x+z+1)z = xz

in the Boolean ring. Its action on B_i swaps 0 and X and fixes Z. These
maps are the usual local-Clifford Bell relabelings (the Y map can be
realized by a square-root-X Clifford). Their implementation is not required
by the learner: the unknown local choices are proof coordinates only.

Let A be their direct sum, g their product, B=product_i B_i, and w=wt(P).
Then A p has Z on the active w sites and I elsewhere, g(B)=B, and g
preserves q=sum_i q_i. Consequently the IDEAL support set obeys

    g((B union(B+p)) intersect {q=0})
       = (B union(B+A p)) intersect {q=0}
       = S_w x B_(inactive).

The second equality uses q=0 on every inactive B_i. It is a set identity;
it does NOT assert that the actual odd-Y Bell distribution has this whole
support. Interference can remove points. Equality of the required low-degree
vanishing kernels, or another adequate source theorem, remains necessary.

## 3. Physical axes use the LINEAR part, not the affine point image

The decisive guard is

    g(v+p)=g(v)+A p.

In particular, for p_i=Y the displayed map has g_i(Y)=Y but A_i Y=Z.
Using g_i(p_i) as the physical transformed Pauli would therefore be wrong.
Translations act on Bell outcome coordinates; they do not act on Pauli
conjugation labels.

Write F_C for the physical Pauli conjugation matrix of the outer Clifford.
From the canonical proof coordinates to the observed Bell labels the
linear map is F_C A^(-1). The closed cubic construction transports by
conjugation on its endomorphisms and by the forward linear map on lambda.
Thus its canonical total-active axis p_Z=A p returns

    F_C A^(-1) p_Z = F_C p,

which is exactly the Pauli correction axis on the native state. It is
neither an affine image of p nor an inverse-transpose label. The local
normalization does not need to be reconstructed to make this conclusion.

If a known Clifford D first separates the active block, the recovered
block label is transported back by F_D. This is ordinary known-tableau
arithmetic; it adds no hidden-frame advice. Apply the resulting physical
Pauli pi/8 correction to FRESH native copies, not to the measured Bell
copies. Either correction sign leaves a Clifford-product state on the
correct axis, since the two choices differ by a Pauli pi/4 Clifford.
Nonuniqueness of the axis or decomposition causes no identifiability
problem for approximate state preparation with fresh-copy verification.

## 4. Active support and source obligations that remain separate

For canonical ideal S_w with w>=4, the closed calculation gives K1=0
and K2=<q_active>; each inactive B_i has K1=0 and K2=<q_i>.
The product support therefore has quadratic kernel spanned by these
individual forms, with no additional mixed quadratic equations. One way
to see the latter is to use the full affine spans of each factor: mixed
bilinear coefficients are forced to zero by independently varying the
two factors. Constants and single-factor terms then separate.

Hence, IF the actual source has the same degree<=3 kernel and a paid
inverse-polynomial quadratic/cubic gap, Haug's actual product-structure
theorem supplies the active block and inactive singletons in polynomial
time. There is at most one block of width greater than one in this
canonical large-support branch. Applying the known decoder to fresh copies
and discarding the other product factors prepares the active pure source;
there is no rare-outcome conditioning. The cubic algorithm then runs on
that block and returns a polynomial list containing its physical axis.

The following are dependencies, NOT conclusions of this review:

1. The actual arbitrary-P Bell law, including interference for odd numbers
   of Y factors; a support-union assertion alone is insufficient.
2. A uniform low-degree kernel/gap theorem for the chosen large-w range.
   An overlap-mass estimate must dominate the relevant degree-D violation
   probability before it can establish equality of kernels.
3. A paid treatment of every remaining small-w instance, including Pauli
   stabilizers and degenerate product decompositions. Constant-width block
   tomography is an adequate endpoint; exact finite-orbit identification
   need not be assumed.
4. A final confidence/accuracy allocation across block recovery, branch
   clocks and candidate verification. If a branch uses approximate block
   tomography, do not reuse an all-zero test argument requiring the correct
   candidate to pass with probability exactly one. Use a suitable fidelity
   tolerance, or finish that branch through the established approximate
   tomography guarantee without that exact-acceptance premise.

No local Clifford can eliminate these source obligations: it transports
the actual interference along with the state.

## 5. Strongest applicable baselines and disposition

The actual Haug Theorem2/Eq11 already learns logarithmic-width product-block
states in polynomial resources when its gap condition is paid; Theorem4
has an approximate version under its affine-gap promise. Therefore bounded
or O(log n) support alone is not a new endpoint. The retained all-Z family
has width n and a constant separation from nontrivial Clifford PURE products,
so the arbitrary-P class contains states outside this logarithmic-width
route. This is a source-applicability statement, not a learning lower bound.

Haug's random T-doped result starts from |0>^n, uses independent random
Cliffords and t<n, and has a stated ensemble failure contribution. It is
not a worst-case theorem for one extra T on |H>^n. Its magic-depth-one
PROCESS learner uses process/Choi access; a single output state's copies
do not supply that access. Supplying the hidden classical circuit would
also trivialize this preparation-output task and changes the input model.

The pre-Clifford state is a sum of two products and has bond dimension at
most two. Classical sampling of a SUPPLIED Clifford-augmented MPS does not
learn the missing Clifford or source representation from native copies.
No classical complexity separation is established by the absence of that
representation, and no general single-copy-measurement lower bound is claimed.

Disposition: ACCEPT the endpoint, local affine normal form and physical-axis
transport as a meaningful bounded completion of the existing mechanism.
No fatal class enlargement or point-identifiability obstruction was found.
Keep the full arbitrary-P learner CONDITIONAL until the four dependencies
above are checked in the integrated theorem. No broader program or additional
simulation is recommended by this review.
