# Odd Cyclic Degree: Composite Lifts And Certified Local Recovery

2026-10-25. Proposed conditional construction; independent review and novelty
assessment pending. No geometric source, unknown kernel or quantum circuit
is executed here. This extends the native elliptic reduction, not an opaque
oracle benchmark. Its possible contribution is avoiding powersmooth lifting,
not the already-known existence of quantum weak-isogeny algorithms.

## Research Question And Decision

Can the new prime-only source cover a cyclic isogeny of arbitrary odd degree
n, including large prime powers and arbitrarily many distinct prime factors,
without introducing powersmooth quaternion lifting or a rare global filter?

The proposed answer is conditional YES. A unit-pivot elementary compiler
extends the geometric source to Sp4(Z/n). CRT isolates primary components.
Square-unit affine phase sampling produces each local kernel line with
constant probability, independent of the exponent. Two checks using the
FULL doubled source then certify the candidate exactly, including at 3.

The certificate is necessary: over Z/9, three distinct lines have the SAME
SL2 stabilizer. A finite-field uniqueness argument would be wrong. Also,
sampling square units globally instead of locally incurs a factor 2^-omega(n).
These are explicit falsifiers, not merely concerns about implementation.

## 1. Native Input, Output And Dependencies

Keep supersingular E and the ORIGINAL E' in characteristic p>3, full known
evaluable O=End(E) with its integral quaternion dictionary, paid compatible
definition fields, and one genuine weak isogeny phi:E->E'. Require:

    deg(phi)=n odd, gcd(n,p)=1, ker(phi) cyclic of order n.

At every used small odd prime, the complete ordered basis images share ONE
nonzero scalar. Reuse that response in both copies of Phi=phi x phi. The
target is the publicly modeled product (E')^2 with product polarization.
Phi has geometric degree n^2 and polarization multiplier n. Its kernel is
W=L direct-sum L, where L is a free primitive line over R=Z/n.

Obtain and verify n=product q_i^e_i. The quantum algorithm may use Shor's
factoring algorithm once as preprocessing; factorization is not charged as
a classical polynomial primitive. The arithmetic prototype takes the verified
factorization as input. Give this same factorization to matched classical
baselines, so factoring alone cannot be advertised as our new separation.
Keep a paid compatible split O/nO -> M_2(R); this is abstract algebra, not
an accessible basis of E[n].

Output the actual original kernel as a primitive R-line, its integral left
annihilator ideal, and optionally the existing ideal-to-isogeny output route.
The output does not enumerate n-torsion points. Noncyclic kernels, even n,
inseparability and unknown source orders are OUTSIDE this theorem.

All geometric obligations of PRIME_ONLY_SOURCE.md and its field audit remain:
modeled PPAV operations, point transport, ONE joint marking isomorphism,
fixed coefficient-field embeddings, uniform clocks, canonical outputs and
workspace cleanup. This note cannot discharge them by arithmetic testing.

## 2. A Bounded Elementary Word Over Z/n

A nonzero matrix entry need not be a unit. For example [[3,1],[5,2]] has
determinant1 modulo15, but neither entry of its first column is a unit.
The prime-field compiler cannot be reused unchanged.

In an invertible d by d matrix, after earlier columns have been eliminated,
the remaining pivot column is unimodular. For each q|n:

- If the current diagonal entry is nonzero modulo q, add no lower row there.
- Otherwise choose one lower entry nonzero modulo q and add its row there.

CRT combines these local 0/1 choices into coefficients for at most d-j-1
row additions at pivot j. The resulting diagonal entry is a unit modulo
every q, hence modulo n. Clear all other entries in that column using its
inverse. Earlier columns stay diagonal. After all columns, the diagonal
matrix has unit entries and determinant1. Express each paired diagonal
diag(a,a^-1) with the usual six elementary factors.

The resulting product has at most

    d(d-1)/2 + d(d-1) + 6(d-1)

elementary factors: at most36 for d=4. This is a derived worst-case bound,
not an observed maximum. CRT uses the supplied factors; no search through
all residues, nonunit division or factoring inside a coherent group query
is required.

For M in Sp4(R), replace each same-elliptic-factor elementary matrix by its
four-factor commutator through the other factor, as in the original lift.
There are at most144 quaternion off-diagonal elementary factors. Lift every
quaternion coefficient z to 2*center_n(2^-1 z), so all coefficients are even
and at most n-1 in absolute value, while preserving the residue modulo n.
Append tau=[[1,n],[0,1]] in M_2(O).

This yields an actual integral automorphism sigma with explicit inverse,
sigma mod n=M, and sigma mod2=[[1,1],[0,1]]. Therefore

    S=sigma^dagger sigma=I+nT0,
    S^2-tS+I=0,   t odd and t>=3.

For B0=sum of the four source basis norms, the uniform bound is

    U=2+4(n-1)^2 B0,    t<=T=U^144(2+n^2).

All coefficient sizes are polynomial in the paid input length. The compiler
works for all Sp4(R) queries, including the certificate queries below, not
only the two-dimensional affine subgroup.

## 3. Same Prime-Only Geometry, With Composite Isogeny Degree

No primality of n was used in the following steps of the preceding proof:

    H=Phi S Phi^-1=I+Phi T0 Phi^dagger,
    H positive symmetric integral, H^-1=tI-H.

Choose a SINGLE odd squarefree multiplier D>T^2, coprime to pn, using
successive allowed small primes. Since t is odd, t+2 and t-2 are coprime;
the same nonnegative coin witness and two four-square representations give

    C^dagger C=C C^dagger=D H8,
    F=H8^-1 C^dagger,
    FC=CF=D I,  F^dagger H8 F=D I.

At each r|D, ker(F mod r)=im(C mod r), of dimension16 and maximal isotropic.
These quotients only need weak Phi data at PRIME r, all coprime to n.
Transport markings using D^-1 C at disjoint primes. The geometric dimension
is still16 and each explicit kernel list has r^16 points.

The trace-free projective rigidity proof also does not require n prime.
Choose marking product R0 with R0^2>8*16^3*n^2. The constructed joint labels
then satisfy, under the complete geometric proof,

    f(M)=f(M') iff M W=M' W,  M,M' in Sp4(Z/n).

The old common-field/scalar-Frobenius argument still applies. Public
level-4 theta data remain required; absence of weak order-4 queries is not
absence of that model machinery. The fixed-tape Las Vegas argument is
already in SMOOTH_REPOLARIZATION.md. Here |Sp4(Z/n)|<n^10, so its logarithmic
union-bound overhead remains polynomial; no new coherence theorem is needed.

The bound and plan are global. A finite input transcript is usable only if
it contains the NEW required levels. The old prime-degree transcript must
not be silently upgraded. An original full weak evaluator can supply them.

## 4. Local Affine Sampling, Not A Global Square Filter

For a primary component m=q^e, CRT embeds SL2(Z/m) in the first elliptic
factor of Sp4(Z/n), as identity everywhere else. The hidden local line
L_m is primitive. One of the two public SL2 charts C=I and
C=[[0,-1],[1,0]] makes C^-1 L_m=span((z,1)). Try both.

Put S_m=(R_m^*)^2. Its size is q^(e-1)(q-1)/2: each square unit has exactly
two square roots because q is odd. For t in S_m, choose a square root a,
and for u in R_m define the PUBLIC query

    g(t,u)=[[a,u/a],[0,1/a]],    det g=1.

It sends z to t*z+u. The two roots give matrices differing by -I; these
act identically on every primitive line. Query the original f on the CRT
embedding of diag(g(t,u) C^-1,I_2). On a good chart, its fibers are EXACTLY
the fibers of t*z+u; this uses the original marked geometric source, not
a new supplied affine oracle.

Prepare the uniform superposition over S_m times R_m. Measure the source
label, leaving for some unknown z0 the state

    |S_m|^-1/2 sum_t |t>|z0-t*z>.

Apply the negative-sign Fourier transform on the second register and
measure frequency k. It is uniform in R_m. Discard k not a unit. Up to an
irrelevant global phase, the first register is

    |S_m|^-1/2 sum_t exp(2*pi*i*k*z*t/m)|t>.

Apply the negative-sign Fourier transform over ALL of the additive ring
R_m, with zero amplitude outside S_m. The probability of output y=k*z is
EXACTLY |S_m|/m=(q-1)/(2q), since those phases cancel in the y=k*z term.
No Gauss-sum estimate or finite-field substitution is needed for this term.
The candidate z=k^-1*y is consequently correct per fresh attempt with
probability at least

    (1-1/q)*(q-1)/(2q) >= 2/9.

This is a candidate probability, NOT a claim that the true peak is uniquely
largest. At q=3 there can be tied peaks; certification below is essential.

### State preparation and charged costs

Prepare uniform units a in Z/m by rejecting multiples of q (success>=2/3).
The reversible map a -> (a^2, sign(a)) is a bijection onto S_m times {+,-},
where sign is relative to a deterministic choice of square root. The sign
register is independent |+> and can be erased. Square roots use finite-field
root finding plus Hensel lifting, with known q and separately capped clocks.
None of these gates depends on z. QFT precision, non-power-of-two uniform
preparation, arithmetic workspace and every geometric source call are paid.

Do NOT apply this directly to S_n. Its density is phi(n)/(2^omega(n)*n),
potentially exponentially small in the number of prime factors. Processing
each CRT component separately keeps the density uniformly constant.

## 5. Exact Certification Using The Full Doubled Source

The statement 'a transvection fixes the line iff its vector lies in the
line' is false over prime-power rings. For U=[[1,1],[0,1]], a primitive
line spanned by (x,y) is U-invariant iff y^2=0, not iff y=0. Modulo9,
lines span(1,0), span(1,3), span(1,6) have identical full SL2 stabilizers:
all are the upper-triangular subgroup of size54. The test enumerates this
small arithmetic counterexample; it is not a new oracle search problem.

For a proposed primitive v, construct C_v in SL2(R_m) with first column v.
Conjugate the following TWO Sp4 matrices by diag(C_v,C_v):

    U1=diag([[1,1],[0,1]],I2),
    A=[[1,1],[0,1]],
    D_A: (x1,x2)->A(x1,x2), (y1,y2)->A^-T(y1,y2).

In paired coordinates D_A is

    [[1, 0, 1, 0],
     [0, 1, 0, 0],
     [0, 0, 1, 0],
     [0,-1, 0, 1]].

Embed both as identity on the other primary components, and compare each
original source label to f(I). Accept only if BOTH comparisons succeed.

Proof: in the C_v frame the true doubled line is L' direct-sum L', with
L'=span((x,y)) primitive. D_A preserves this doubled line iff x*y=0;
its cross-factor increments are (x,0) and (0,-y), and membership in L'
is exactly the vanishing of their determinants with (x,y). In the local
ring one of x,y is a unit, so this forces L' to be either coordinate axis.
U1 fixes the first axis and not the second. Thus both checks hold iff
L'=span(e1), equivalently the proposed local line is EXACTLY correct.

The second query is genuinely outside the restricted one-factor SL2 source.
It supplies the information absent from that group's coinciding stabilizers.
It requires no hidden point, known slope or extra native evaluation level.
Bad charts and false Fourier candidates cannot pass an exact source.

With r=omega(n) components, allow h attempts in each of two charts, where
r*(7/9)^h<=epsilon. There are at most2rh coherent source queries and4rh+1
classical source comparisons. Return ABORT on exhaustion. Add source-clock,
state-preparation and approximate-QFT errors separately by a hybrid bound;
the exact-certificate guarantee is conditional on the exact source promise.

## 6. Global Output

CRT-combine a primitive vector from each recovered local line. The resulting
global vector is primitive, but neither coordinate need be a unit modulo n.
For example (6,10) modulo15 combines the lines (0,1) mod3 and (1,0) mod5.
Construct its determinant-one complement componentwise and CRT-combine;
do not divide by an arbitrarily selected global coordinate.

The left ideal I={a in O:aL=0 mod n} has index n^2 and reduced norm n.
Pull back the matrices with first column zero in the (L,complement) frame,
adjoin nO, and take HNF. This is the same left-annihilator convention as
the prime corollary. It has common kernel exactly L. Existing unconditional
IdealToIsogeny conversion applies only AFTER this recovery; it and effective
target-order conversion are imported geometric algorithms, not executed
by the HNF tests.

## 7. Prior Art, Falsifiers And Research Value

[Denney--Moore--Russell, 0809.2445v5](https://arxiv.org/pdf/0809.2445),
Sections 5-6, already use square-multiplier affine groups and Fourier peaks
to recover finite-field Borel stabilizers. Their prime-power q denotes a
FIELD F_q, not Z/q^e. Our local-ring derivation and full-source certificate
must be checked independently, but the sampling mechanism is not new.

[Chen et al., 2305.19897v1](https://arxiv.org/html/2305.19897v1), Section 3.2,
already solve a GL2(Z/n) Borel HSP, and their Appendix A discusses composite
unit pivots. Their isogeny implementation uses powersmooth quaternion lifts.
The 2025 Chen--Petit work further covers general isogeny degrees under stated
heuristics, as recorded in ELLIPTIC_COROLLARY.md. Do not advertise arbitrary
odd degree as an unknown quantum problem or claim this is the first solver.

Potential value is a uniform SOURCE route avoiding that norm-lifting step,
now without the former prime-degree restriction for cyclic odd kernels.
Its core new geometric proof is still independently unreviewed. The current
implementation supplies arithmetic and phase-formula controls, not an
end-to-end native computation or demonstrated asymptotic advantage.

Decisive failure modes remain: invalid native weak data; a noncyclic kernel;
incorrect repolarization, descent or joint canonicalization; a superpolynomial
geometric clock; uncharged point fields; an incorrect local phase sign; and
an existing classical attack exploiting real geometric labels rather than
only equality. Full target-order advice or known Hom modules are not free.
Conversely, strong same-input attacks should be granted the factorization,
source order and all paid transcript data that the quantum route uses.

Existing sign enumeration upgrades weak evaluations to a compact strong
representation; it does not by itself output this original kernel ideal.
Keep that distinction when reporting baselines. Product-target and extra-map
attacks remain mandatory; the doubled product target falls into two copies
of the SAME elliptic residual problem, not automatically into their mixing
recovery case. No classical lower bound follows from any finite control.

Next decisive work is falsification or geometric execution of this FULL
source chain, not additional opaque-label receiver timing experiments.

## 8. Executed Controls And Complexity Recheck

The degree-25 control uses the actual algebraic endomorphism alpha=3+4i
on the known supersingular j=1728 source in characteristic11. Its norm25
and rank1 reduction modulo5 certify a cyclic kernel. With Phi=alpha x alpha
and sigma=[[1,25j],[0,1]], where j^2=-11, the pulled-back polarization has
trace6877. Exact order arithmetic and modular Tate actions verify the norm
identity, masked conjugation, and seven maximal-isotropic prime kernels,
including the nonsemisimple prime3. Neither curve points nor quotients are
computed. Alpha is SUPPLIED; this control does not recover an unknown map.

The four-square complexity dependency was rechecked against
[Pollack--Trevino](https://math.colgate.edu/~integers/sjs15/sjs15.pdf),
pp.1-2: unconditional randomized polynomial-time variants exist, with
polynomial-size operands and a stated conversion to bit cost. This is NOT
a newly discharged obligation: the preceding smooth-source proof already
cited that unconditional route. Its fixed-tape compilation still requires
a uniform expected bound. SymPy's witness finder is only a checked finite
control, not the promised implementation of that bound.

The tests also check exact lift inverses, quadratic identities, modular
parity, source bounds, affine-query fibers and root-sign invariance, local
phase normalization and success, the mod9 stabilizer collision, two-query
certificates, mixed-primary CRT lines, and left-ideal orientation/index.
Enumerative fixture generation and numerical Fourier arrays are explicitly
not scalable source or quantum implementations. See VERIFICATION.md and
receipt.json for the final executed scope; do not infer one from the other.
