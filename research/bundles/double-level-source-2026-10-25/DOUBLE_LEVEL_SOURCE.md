# Double-Level Source And The Small-Prime Classical Falsifier

2026-10-25. Proposed conditional construction; independent review pending.
No native geometric source, unknown isogeny recovery or quantum execution
is supplied by this bundle. The previous completed passes and retained
PPAV dependencies remain authoritative for their narrower scopes.

## Research Decision

The proposed source can be extended to arbitrary degree n>=2 coprime to
p>3, including even degrees and noncyclic elliptic kernels, by lifting at
modulus 2n and working with the INTEGRAL operator (H-I)/2. The original
weak evaluator, source order, target curve and paid field promises do not
change. Only odd-prime weak evaluations are used in this new source path.

There is also a substantial classical falsifier: using this SAME source,
scaled certification queries recover each small-prime direction one digit
at a time. Fixed-prime-power scaling, including all dyadic degrees, cannot
establish a superpolynomial quantum advantage here. A dyadic quantum
receiver is unnecessary, and was deliberately not implemented.

Potential value remains replacing powersmooth quaternion lifting under
the native weak-isogeny input. Existing quantum weak-IsERP algorithms are
prior art. This is not a first quantum solution, a solution from bare
curve equations, or a demonstrated advantage over matched classical work.

## 1. Input And Output

Keep a supersingular E, the ORIGINAL modeled E', a single weak isogeny
phi:E->E' of known degree n coprime to p, and the full evaluable source
order O=End(E) with its integral quaternion dictionary. The order and phi
must be defined over the paid compatible common field. At each requested
odd prime, all ordered weak images share ONE nonzero scalar.

Factorization of n is verified and charged; a quantum algorithm may use
Shor preprocessing, but matched classical baselines receive the same
factorization. A split O/nO -> M2(Z/n) is public source algebra, not a
basis of E[n] points. The additional split at 2n will be computed below,
not granted as new secret-dependent advice.

Double Phi=phi x phi, of polarization multiplier n and geometric degree
n^2. Its kernel is K direct-sum K. Nonfree K is handled by the earlier
scalar-content reduction. Output is the original LEFT annihilator ideal,
not a supplied line, the residual cyclic ideal, or a new target instance.
Degree 1 is the separate isomorphism boundary and needs no hidden kernel.

The expected polynomial bound remains conditional on the complete modeled
PPAV source, its uniformly bounded geometric routines, exact canonical
markings, field embeddings, verified random clocks and workspace cleanup.
Those imported obligations are not established by these arithmetic tests.

## 2. Public Lift From n To 2n

For M in Sp4(Z/n), choose integral residues. If n is odd, combine M mod n
and I mod 2 by CRT. If n is even, set

    E=(M^T J M-J)/n mod 2.

This is an alternating matrix. Choose strictly upper-triangular Y with
Y+Y^T=E and solve M^T J X=Y mod 2. Then

    M'=M+nX mod 2n

is symplectic: the linear correction is n(Y-Y^T), which equals nE modulo
2n, and n^2 X^T J X vanishes there. The Pfaffian identity gives det M'=1
over this ring. M' reduces to the SAME M; no kernel enters the computation.
The tests include a matrix symplectic mod 2 but not mod 4 under naive
integer lifting. Keeping its entries unchanged would invalidate the proof.

### Compute the compatible order splitting

Since O is maximal and p is odd, O/2O is M2(F2). Search its 16 elements for
a nonzero nonidentity idempotent. A basis of the two-dimensional left ideal
Oe gives a faithful two-by-two left action. Verify its full multiplication,
unit, involution and coordinate-isomorphism tables. A ramified order at 2
does not satisfy this promise and is rejected.

To extend a SPECIFIED split at 2^k, lift its inverse image e0 of E11 via

    e=3e0^2-2e0^3 mod 2^(k+1).

The idempotent error squares under this polynomial, so one step suffices.
Let f0 lift the inverse image of E21. Use the module basis (e, f0 e).
Its reduction is (E11,E21); an odd two-row minor computes all left-action
coordinates. The ideal is a free rank-two direct summand over the local
ring, so this basis spans it. Every proposed action is checked against
all four module coordinates and the entire algebra table. It reduces to
the specified previous split, not a conjugate in silently changed coordinates.

For even n, extend only its dyadic factor and keep the odd-factor actions.
For odd n, combine the new mod-2 split with the existing mod-n split.
CRT then produces O/2n with exactly the prescribed reduction modulo n.
This generalizes the repository's existing odd-prime idempotent lift;
idempotent lifting itself is not a new mathematical result. Its deterministic
cost is polynomial in the paid order coordinates and log n. No high-order
torsion fields or unknown target order are involved.

## 3. The Integral Half-Polarization

Compile M' in SL4(Z/2n) using the CRT unit-pivot method, now allowing 2.
The same bound of 36 elementary factors applies. Replace within-factor
elementaries by the four-factor cross commutator and lift their quaternion
coefficients to centered residues modulo 2n. This gives an exact integral
automorphism sigma, its inverse, and at most 144 quaternion factors.
Each source-basis coefficient has absolute value at most n.

Unlike the earlier odd-trace construction, append NO parity shear. We get

    S=sigma^dagger sigma=I+2nT0,
    H=Phi S Phi^-1=I+2 Phi T0 Phi^dagger.

Both H and A=(H-I)/2 are actual integral endomorphisms. H is positive,
symmetric, unimodular, and satisfies H^2-tH+I=0 with t>=2. To see t=2
modulo 4, write the self-adjoint S=I+2B. Its Moore determinant is

    1=det_M(S)=1+2 tr_M(B)+4 det_M(B).

Both coefficients are integers for this integral hermitian matrix. Hence
tr_M(B) is even, and t=2+2 tr_M(B)=2 mod 4. Put s=(t-2)/4. Then

    A^2=sH,    (A+I)^2=(s+1)H,    H=I+2A.

The boundary t=2, s=0 is valid. For the positive actual H it gives H=I;
the formal norm identity below also holds in the degenerate quadratic ring.
An old schema requiring trace>=3 must not discard this case.

### A concrete falsifier for insufficient congruence

In the known characteristic-11 order take h=(1+j)/2, q=h-i,
alpha=1+i, Phi=alpha x alpha and sigma=[[1,2q],[0,1]]. The degree is n=2
and S=I mod 2, so this is a valid original-level query lift. The conjugate
H is integral and has trace 18, already 2 mod 4. Nevertheless (H-I)/2 is
NOT integral. Thus neither a trace congruence nor merely S=I mod n justifies
halving after conjugation. The stronger S=I mod 2n is essential.

### Uniform bound

For B0 equal to the sum of the four source-basis norms, each elementary
factor's squared Frobenius norm is at most U=2+4n^2 B0. Submultiplicativity
gives one public bound

    t <= T=U^144.

The coefficient and trace bit lengths are polynomial in the paid input.
The trace is not substituted for T when selecting the global weak levels.

## 4. Odd-Prime Norm Certificate For Every Degree

Choose a SINGLE odd squarefree D>T^2, coprime to pn, as a product of
successive allowed small primes. For s>0 set

    X=D mod s,    Y=(D-(s+1)X)/s.

For s=0 set X=D,Y=0. Since s,s+1 are consecutive and D>=s(s+1), X,Y are
nonnegative and (s+1)X+sY=D. Four-square witnesses for X,Y give the eight
commuting integral coefficients a_i(A+I), b_i A, whose squared sum is DH.
The eight-square norm matrix and its adjoint therefore yield

    C^dagger C=C C^dagger=D H8,
    F=H8^-1 C^dagger,
    FC=CF=D I,    F^dagger H8 F=D I.

Use the integral coefficient ring Z[A]/(A^2-2sA-s), not fractional
coefficients forced into the old Z[H] schema. The implementation verifies
both-sided identities exactly in this ring. Its SymPy witnesses remain
finite controls; the prior unconditional four-square clock is an imported
algorithmic obligation, not an empirical timing claim.

For each r|D, the previous Smith/adjoint argument gives
ker(F mod r)=im(C mod r), dimension 16 and maximal isotropic, including
nonsemisimple discriminant primes. A=(H-I)/2 mod r is computable because
r is odd. All these r are coprime to n; the SAME original masked Phi data
provide H on their torsion. Transport markings using D^-1 C at disjoint
odd primes, with marking product R0^2>8*16^3*n^2.

The original geometric quotient and joint-marking arguments would then give

    f(M)=f(M') iff M(K direct-sum K)=M'(K direct-sum K).

No weak query at 2, 4 or a growing dyadic order is needed by this path.
Public level-4 theta models and their fields are STILL paid dependencies.
The geometric dimension is still 16, including r^16 explicit kernel lists.
This is theoretical fixed-dimension complexity, not practical execution.

## 5. Matched Classical Digit Recovery

At q^e|n, first use the two unipotent period families from the content
reduction. They determine a and d=e-2a using at most 2(e+1) source
comparisons. The same proof works at q=2. A scalar component d=0 needs
no direction. For d>0, the doubled kernel's stability depends only on a
primitive local line modulo q^d.

Given a candidate v and desired prefix length j<=d, choose its local SL2
frame C_v at the FULL q^e level. Put z=q^(d-j). Conjugate by diag(C_v,C_v)
the matrices U_z in the first factor and the cross-factor matrix D_z:

    U_z=diag([[1,z],[0,1]],I2),
    D_z=[[1,0,z,0],[0,1,0,0],[0,0,1,0],[0,-z,0,1]].

Compare BOTH original source labels with f(I), after full-component CRT
embedding. In this frame, writing the true line as (x,y), the conditions
are z*y^2=0 and z*x*y=0 modulo q^d. A primitive vector has a unit coordinate.
If y is a unit the first fails; if x is a unit the second is equivalent to
y=0 modulo q^j. Therefore both comparisons accept EXACTLY the candidate
prefix modulo q^j, even at q=2 and for nonfree original kernels.

Enumerate q+1 lines modulo q. Having found the correct chart/prefix, try
the q next digits at each further level. Exactly one succeeds under the
source promise. The resulting deterministic bound is

    2(q*d+1) source comparisons, plus one shared identity evaluation.

The implementation checks uniqueness and charges the declared budget
before running. It does not mislabel O(q*d) as polynomial in log q.
For q=2 this is linear in d. More generally, if all prime factors are
bounded by a polynomial in paid input length, the entire same-input
direction problem is classically polynomial CONDITIONAL on this source.
Thus fixed-small-q, growing-exponent experiments are dequantized here.

For large odd primes the prior quantum square-unit method remains a
conditional alternative with constant candidate probability per local
attempt, followed by exact certification. No quantum dyadic branch is
needed. A large-prime classical gap in THIS baseline is not a hardness
proof: attacks may exploit the actual geometric label contents.

## 6. Original Ideal And Executed Scope

Set c=product q^a and m=n/c^2. CRT-combine all positive-depth directions,
using local determinant-one frames, even when neither global coordinate
is a unit. Pull back the matrices annihilating that line to obtain I_psi.
Return I_phi=c I_psi with index n^2; if m=1 return cO. The proof from the
content reduction is unchanged and now includes dyadic local data.

The control phi=1+i, degree 2, uses a noncommuting source shear and checks
an integral half-polarization of trace 178, its norm matrix, masked
conjugation and five odd-prime isotropic kernels. The mixed noncyclic map
phi=2(1+i)(3+4i), degree 200, gives scalar content 2 and residual degree 50;
the reconstructed ideal equals O*phi in both lattice directions.
These maps and kernels are SUPPLIED. No unknown map, curve points or
geometric quotient is computed. See VERIFICATION.md and receipt.json.

## 7. Failure Modes And Next Decision

- Reject incomplete/ramified source orders, inseparable degree and invalid
  split coordinates. A generic unknown-target splitting is not granted.
- Verify S=I mod 2n and integrality of A; the explicit bad lift above shows
  why a trace-only test is insufficient.
- Keep n, 2n, residual depth and full CRT components distinct. Prefix
  queries live at q^e even when the hidden direction has depth d<e.
- Charge global levels and fixed clocks before coherent source evaluation.
  No per-query multiplier selection, independent masks or field conjugation
  is permitted. All prior descent/canonicalization obligations remain.
- Treat small-prime classical recovery as a falsifier of proposed quantum
  scaling signals. Do not promote finite failure at large q to hardness.
- Do not claim this source is independently reviewed, implemented
  geometrically, practical or novel. The old one authorized Rees reviewer
  reviewed a different proof and is closed.

The next important question is the full geometric source or its leakage,
not another degree extension. This pass removes the obvious parity/input
restriction and supplies the missing matched small-prime baseline; it does
not resolve the central implementation and review debt.

Primary prior art and imported scope are recorded in the preceding source
notes. [Chen--Petit 2025](https://research.birmingham.ac.uk/en/publications/computing-the-endomorphism-ring-of-a-supersingular-elliptic-curve/)
already covers general-degree quantum weak-IsERP. The new argument must be
compared to the full proof before any novelty claim. The full manuscript
was not available in the previous retrieval attempt. No new claim about
its detailed assumptions is inferred from the abstract here.
