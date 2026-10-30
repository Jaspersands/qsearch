# Classical Membership On The Original Weak-Isogeny Input

2026-10-25. Conditional reduction plus exact supplied-map controls.
INDEPENDENT MATHEMATICAL REVIEW PENDING. No geometric interpolator executed.

## Research Decision

Small-prime growing-exponent cases are not credible superpolynomial quantum
separations here. Their classical recovery does not need our new dimension-16
coset-label construction: original-target interpolation suffices under the
published PPAV model and the native promises below. The implemented arithmetic
connects the existing integrality lemma to single-elliptic prefix queries,
including singular endomorphisms and even/noncyclic degrees.

This is NOT a first smooth-degree IsERP algorithm. The classical smooth Borel
reduction and iterative removal of smooth factors, including powers of two,
already appear in Chen et al., Sections 3.1, 4.2 and Appendix D.1 of
[Hidden Stabilizers](https://arxiv.org/html/2305.19897v1). Chen--Petit also
explicitly describes smooth-degree classical tractability in the indexed text
of [their paper](https://dipot.ulb.ac.be/dspace/bitstream/2013/392160/3/suborder_to_endomorphism_ring.pdf).
The latter full PDF still redirects to an invalid holding and was NOT reviewed
in full. The potentially useful distinction in this local reduction is avoiding
the proposed coset labels and any powersmooth-norm lift for the probes. Novelty
is unestablished; do not register this as a new quantum candidate.

## 1. Fixed Input And Accounting

E and E' are original modeled supersingular elliptic curves in characteristic
p>3. A genuine weak representation belongs to ONE isogeny phi:E->E' of
known degree n>=2 coprime to p. At each queried auxiliary order one nonzero
scalar masks the ENTIRE ordered torsion basis. Scalars may differ by order,
but not by basis column or by incompatible evaluations of that basis.

The supplied full order O=End(E), its integral quaternion dictionary, evaluation
algorithms, and abstract split O/nO -> M2(Z/n) are paid inputs. Factorization
of n is supplied/charged equally to both baselines. No large q^e torsion
points, End(E'), kernel, or unknown repolarization are granted. The common
definition field for phi and the full source order, its embedding, and each
auxiliary extension are charged. This is not the bare-curve isogeny problem.

The code computes public arithmetic and runs exact controls with a SUPPLIED
phi and KNOWN target order. Only those controls know phi's coordinates. The
native test below instead invokes a published geometric primitive; it is not
installed here and no fake substitute is wired into a CLI or registry.

## 2. A Uniform Public Lift And Transcript

For A in M2(Z/n), invert the supplied split coordinate map. Lift its four
coordinates by CRT to alpha congruent to A modulo nO and to 1 modulo pO.
Use centered representatives of modulus np. With

    B0 = sum_i reduced_norm(basis_i),
    Nmax = 4*(np)^2*B0,

Cauchy--Schwarz in the positive quaternion norm gives
0 < N=norm(alpha) <= Nmax and N=1 mod p. Alpha cannot be zero since it is
1 mod pO. No assumption gcd(N,n)=1 is made: singular prefix tests NEED norms
sharing factors with n. All coefficient and norm lengths are polynomial in
the paid input length. This is not a search for a powersmooth norm.

Before adaptive queries, choose an odd squarefree product P of primes away
from np such that P>8*n^2*Nmax^2. Obtain the genuine weak basis images once
at every chosen prime. For each alpha omit primes dividing N, retaining M.
The omitted product divides N and is at most Nmax. Consequently

    M >= P/Nmax > 8*n^2*Nmax,
    M > N,  M^2 > 8*n^2*N,  gcd(M,Nnp)=1.

This overestimates the needed level deliberately. Testing N modulo the fixed
small primes requires no factorization of N. At most log2(np) distinct primes
are excluded by np; O(log P + log(np)) successive primes suffice. Their
largest size is polynomial in paid bit length, not proportional to n or p.
The implementation rejects an insufficient finite transcript rather than
quietly buying additional adaptive weak evaluations. Planning is not evidence
that any points/images were obtained.

## 3. Exact Original-Target Membership

Let gamma=phi alpha phi^dagger/n. It is a rational endomorphism of E' of
norm N. By descent through the quotient E/ker(phi),

    gamma integral <=> alpha(ker(phi)) contained in ker(phi).

Containment, not equality, is essential. This is the existing lemma in
ppav-source-2026-10-23/PPAV_SOURCE_DECISION.md, Section 5, now applied to
elliptic arbitrary-n inputs. Every nonzero elliptic endomorphism is polarized
by its reduced norm; no extra Hermitian lift is needed for these probes.

At retained prime r, write the source action of alpha in basis P_r as A_r.
The known target basis is Q_r=lambda_r*phi(P_r), and the exact predicted
images of gamma are Q_r*A_r. The common scalar cancels. Since r does not
divide Nn, both target tuples are full bases. Source actions require small
torsion arithmetic and bounded-size discrete logarithms, not large-torsion
access. They are not computed by the abstract modulo-n split alone.

Apply Theorem 7.1 / Algorithm 6 of
[A computational framework for principally polarized abelian varieties](https://eprint.iacr.org/2026/1142)
to E' and E' with their ORIGINAL polarizations, multiplier N, and level M.
Pages 36-38 of the retained PDF explicitly give an isogeny or failure, with
bounded negative branches and input/prime-dependent polynomial runtime at
fixed dimension. Its internal dimension is 8 for our elliptic calls. This is
still an enormous fixed-dimensional primitive, not a practical implementation.
Use unconditional expected-polynomial four-square variants; the SymPy witness
used in one finite graph control makes no uniform runtime claim.

If an interpolant gamma0 is returned, then

    Delta = n*gamma0 - phi alpha phi^dagger

is integral and kills E'[M]. It factors as [M]*theta with theta integral.
The Rosati norm triangle inequality gives ||Delta|| <= 2n*sqrt(2N) < M.
Every nonzero integral theta has positive integral squared Rosati norm, so
theta=0. Thus gamma0=gamma and the answer is true exactly on containment.
Conversely integral gamma is the required N-isogeny. Failure is a negative
answer only for the exact published algorithm, never for a timeout/backend
exception. A practical incomplete backend must return UNKNOWN separately.

### Negative Inputs Still Have Legal Quotient Data

The rational gamma satisfies gamma^dagger gamma=N even when not integral.
Modulo every retained r its action is invertible and has pairing multiplier N.
In Algorithm 6, set m=M-N and use its four-square matrix W, W*W^dagger=mI.
The graph generators (W^dagger P, gamma(P)) have zero product Weil pairing
because m+N=M. Their bottom projection is invertible at r, hence the graph
has full half-rank 8 and is maximal isotropic. Thus nonmembership does not
invalidate the quotient call. The final verification/failure branch decides
whether these locally compatible data extend to an integral map.

The paid common-field promise makes Frobenius scalar; the earlier
source-field-audit-2026-10-23/SOURCE_FIELD_AUDIT.md supplies the fixed quadratic
extension for theta models and descent. Use SEPARATE auxiliary extensions
of degree at most r-1 over that fixed base for prime-only torsion, with fixed
embeddings. Do not form their potentially enormous compositum or quotient
labels by field automorphisms. This remains an imported field argument.

## 4. Single-Factor Content And Prefix Recovery

At q^e dividing n, let R=Z/q^e and

    K = q^a R v + q^(e-a) R w,
    0 <= 2a <= e, det(v,w)=1, d=e-2a.

An arbitrary matrix preserves K by containment exactly when its lower-left
entry in frame (v,w) is zero modulo q^d. If d=0 all matrices preserve K.
For d>0 only the primitive direction modulo q^d matters.

For v=(x,y), upper and lower unipotents of parameter q^k test respectively
q^k*y^2=0 and q^k*x^2=0 modulo q^d. The two first-success thresholds are
max(0,d-2v_q(y)) and max(0,d-2v_q(x)); their maximum is d. This gives a in
2(e+1) calls, with monotonicity/parity checks. Those checks alone cannot prove
that a backend implements the native promise.

For a candidate direction and precision j<=d, conjugate the following by its
SL2 frame at FULL q^e precision:

    U_s = [[1,s],[0,1]],  P_s = [[s,0],[0,0]],  s=q^(d-j).

In that candidate frame let the true direction be (x,y). The two containment
conditions are s*y^2=0 and s*x*y=0 modulo q^d. If y were a unit the first
would fail. Hence x is a unit, and the second implies q^j divides y. The
converse is immediate. This proof works at q=2 without square-root ambiguity.
U alone is insufficient: at q=3, depth 2, (1,3) passes U_1 for proposal (1,0)
but fails P_1. P_s is noninvertible and must NOT be rejected for that reason.

Embed the query at q^e into the original modulo-n action by CRT, choosing
identity on every other primary component. Enumerate q+1 directions at the
first digit, then q extensions per digit in the selected chart. Exactly one
candidate survives, costing 2(q*d+1) containment calls. The implementation
prechecks a worst-case budget before the first callback. Scalar components
have no direction search. Reconstruct the ORIGINAL left ideal with the
previous content-aware pullback, including the scalar factor.

Total calls are sum_q [2(e_q+1)+2(q*d_q+1) for d_q>0], with the second term
omitted for d_q=0. This is polynomial for prime factors bounded polynomially
in paid input length. It is NOT polynomial in log(q) for large q.

## 5. Two Necessary Falsifiers

First, a shared scalar is essential. For phi=1+i, alpha=i, r=7 in the
characteristic-11 order, different column masks 1 and 2 yield the wrong
inferred gamma even though determinant/pairing checks still pass.

Second, the paper's uniqueness bound only compares INTEGRAL interpolants.
In the same supersingular order take phi=1+3j (degree n=100), alpha=i (N=1),
and M=3. The rational gamma is nonintegral but equals i on E[3]. The actual
integral map i is therefore a valid interpolant. M>N and M^2>8N hold, yet
membership would be falsely accepted. M^2>8n^2N fails. This is an elliptic
supersingular version of the previously recorded ordinary-surface falsifier,
not a new flaw in the published theorem. No interpolator was run to check it;
the exact supplied maps prove the collision.

A separate supplied phi=1+i, alpha=(1+j)/2 example has nonintegral gamma of
norm 3 while its candidate graph is full isotropic at 5,7,13. It exercises
valid negative input rather than mistaking malformed points for rejection.

## 6. Boolean Membership Cannot Replace The Full Quantum Source

This deduction concerns ONLY the Boolean interface after discarding original
geometric data, not native IsERP hardness. At prime degree q, the unknown
kernel is a projective line L among q+1 possibilities. Query A returns
whether A L is contained in L. A scalar matrix accepts every line. Any
nonscalar 2x2 matrix fixes at most two lines: three invariant lines would
force two eigenvalues to coincide and the matrix to be scalar. This includes
noninvertible matrices and characteristic two.

Reduce unique unstructured search on q+1 marked possibilities to this
interface. For any A, compute its zero, one, or two invariant lines using
free input-independent computation; answer by OR of at most two mark bits.
Scalar queries have a known answer. Coherent simulation uses a constant
number of mark-oracle calls, including cleanup. Consequently a bounded-error
T-query membership solver gives an O(T)-query search algorithm. The standard
[quantum search lower bound](https://arxiv.org/abs/quant-ph/9711070)
implies Omega(sqrt(q)); the classical bound is Omega(q). Conversely every
line has a conjugated nontrivial unipotent with that UNIQUE invariant line.
Grover search gives O(sqrt(q)) membership queries, so these query bounds are
tight. This is a proof deduction, independently unreviewed; finite incidence
checks only guard the algebra used in it.

No reduction here simulates the original modeled E', weak evaluator,
interpolation output encodings, or marked coset labels from a search oracle.
Therefore this is NOT a hardness result for the native problem and does not
exclude geometric leakage. It does rule out claiming a poly(log q) HSP
algorithm using only this Boolean membership interface. Returning the same
failure symbol outside a stabilizer is not a valid full hiding function.

## 7. What Would Falsify Or Improve This Pass

- A failure of the imported original-target model, descent, or exact negative
  interpolation guarantee blocks the conditional native baseline.
- Per-column masks, insufficient weak levels, or a missing common field are
  DIFFERENT inputs, not reasons to silently reuse this reduction.
- A query violating the exact prefix equivalence, lift bound, or uniform
  filtering inequality falsifies the corresponding arithmetic lemma.
- A real native backend recovering an unknown kernel would improve execution
  evidence. Supplied-map integrality controls cannot establish that.
- Exploiting actual geometric outputs at large primes would beat the Boolean
  abstraction, not contradict its narrowly scoped query bound.

Next high-value question: does the proposed full marked source remove the
published powersmooth-lifting heuristics for LARGE-prime IsERP inputs under
the exact same representation model, or does an uncharged conversion remain?
Prioritize that end-to-end theorem/input comparison and actual geometric
leakage. Do not add more smooth-degree demonstrations or derive native
hardness from the Boolean query bound.
