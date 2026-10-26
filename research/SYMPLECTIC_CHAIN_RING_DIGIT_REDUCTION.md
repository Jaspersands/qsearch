# Siegel HSP Over Odd-Residue Chain Rings: Digit Recovery

2026-10-23. PROPOSED THEOREM; local proof and exact controls, independent
review pending. No quantum HSP/HPGP learner was executed. No novelty,
natural-problem hardness, cryptanalytic application or Shor-level result
is claimed. This extends the prime-square reduction by a digit-learning
mechanism, not by assuming an oracle on smaller quotient rings.

## Result And Impact Limit

Let R be an effectively presented finite COMMUTATIVE chain ring of length
e>=2, maximal ideal (pi), and residue field k=F_q of odd characteristic p.
Let n>=2. Given an ordinary coherent oracle on Sp_(2n)(R) hiding the full
stabilizer of an unknown free Lagrangian direct summand W, the proposed
algorithm recovers W in bounded-error time polynomial in n, log|R| and
log(1/epsilon). The chain length need not be fixed.

After learning W modulo pi, each intermediate digit uses ONE abelian HSP
to recover a complete symmetric-matrix digit. Only the final digit uses
the existing n degree-two hidden-polynomial calls. The proposed general
Rees receiver is NOT a dependency. The quantum primitives are published.

There is also a full-oracle opaque-label classical query lower bound for
the deepest-digit family: success after Q queries is at most

    min(1, q^(-m) + Q(Q-1)/(2q)),      m=n(n+1)/2.

Its scope is an oracle separation in growing q, not an explicit classical
computational lower bound. It proves no exponential dependence on n or e.
The missing meaningful input source remains the impact blocker. Further
ring/field variants without such a source are not the next priority.

## Input Model And Prior Work

Supply ring arithmetic, pi, e, residue arithmetic, a residue-section map,
an F_p basis of k, and extraction of successive pi-adic digits, all with
polynomial bit cost. Unit inversion and canonical encodings are charged.
An arbitrary quotient of an unknown number field is not this presentation.
Labels have fixed polynomial width, with

    f(g)=f(h) iff gW=hW iff g P_W=h P_W.

They do not reveal an image-submodule basis. A field oracle cannot be
extended to R, and a ring oracle cannot be descended to R/(pi^r), for free.
Every query below is an actual matrix in the ORIGINAL group over R.

[Imran, arXiv:2610.28368v2](https://arxiv.org/html/2610.28368) gives the GL
chain-ring parabolic algorithm and motivates socle/digit probes. Its
GL theorem is not an Sp theorem. The specific symplectic scalar action,
carry-corrected queries and certificates below are derived here.
[Ivanyos--Santha](https://arxiv.org/html/1503.09016), Theorem 5 and Corollary 6,
provide the prime-field univariate constant-degree HPGP' primitive with
growing output dimension. Here the degree is two and the output dimension
is [k:F_p]*m. Neither that primitive nor abelian HSP is new.

This may be a straightforward or previously known application of those
ingredients. Targeted searches and a reread are not novelty certification.
The Rees whole-proof reread found no new counterexample but does not count
as an independent review or support this separate theorem.

## 1. Obtain And Certify The Residue Chart

Put J=[[0,I],[-I,0]]. For X in sp_(2n)(k), choose any entrywise lift X_tilde.
The map

    X -> I+pi^(e-1) X_tilde

is an injective additive homomorphism into Sp_(2n)(R). The quadratic term
vanishes, and changing a lift changes nothing. Purity of a free direct
summand gives W intersect pi^(e-1)V=pi^(e-1)W. Hence restricting f to this
socle group hides the residue stabilizer algebra p_Wbar.

Use abelian HSP on its [k:F_p]*n(2n+1) prime-field coordinates. In odd
characteristic the matrix trace pairing on sp is nondegenerate. The
annihilator of p_Wbar is the square-zero radical u_Wbar, whose image-column
span is Wbar. This is the same algebraic argument as the prime-square
note, with pi^(e-1) replacing p; it does not use an invalid map I+X over k.

Certify a proposed Wbar: check rank n and isotropy, construct a k-basis of
its stabilizer algebra, and query membership for the corresponding socle
matrices. Successful checks imply containment in the actual stabilizer
algebra. Both have dimension n^2+m, hence equality, and trace duality
identifies the same Wbar. A partial unverified HSP kernel is insufficient.

Extend Wbar to a symplectic basis over k and lift it to B over R. This
does not require a field embedding in R. One constructive lift corrects
precision one digit at a time: if B^T J B=J+pi^j D modulo pi^(j+1), put

    C=(1/2) J D over k,       B <- B(I+pi^j C_tilde).

Then C^T J+JC=-D and the defect vanishes at the next precision. Repeat for
j=1,...,e-1. Invertibility follows from the residue; all digits are public.
Conjugate f by B. The hidden submodule now has the unique graph form

    W_S = image [I;S],        S=S^T in pi*Mat_n(R).

This is a certified chart, not an untested random chart.

## 2. Recover One Entire Intermediate Digit

Suppose S^(r) is the already certified symmetric prefix modulo pi^r,
where 1<=r<=e-2. Write S-S^(r)=pi^r S_r modulo pi^(r+1), with S_r in
Sym_n(k). Let a=e-1-r>=1. For t in the PRIME SUBFIELD F_p choose a lift
t_tilde and define

    u_t=1+pi^a t_tilde,       A_t=u_t I.

These are units for every t, including zero. Let U_Y=[[I,0],[Y,I]] and
D_A=diag(A,A^(-T)). All U_Y for symmetric Y and all these D_A are symplectic.
Compute the KNOWN correction in the original ring, not just in k:

    Delta_t = A_t^(-T) S^(r) A_t^(-1) - S^(r).

For X in Sym_n(k), form the public query

    g_r(X,t) = U_(pi^(e-1) X_tilde - Delta_t) D_(A_t).

Its action on W_S has graph parameter

    S + pi^(e-1) X_tilde + (u_t^(-2)-1)(S-S^(r)).

Since u_t^(-2)=1-2pi^a t_tilde modulo pi^(a+1), and 2a+r>=e,
this is exactly S+pi^(e-1)(X-2t S_r), with the parenthesis interpreted
through the socle identification. Higher unknown digits vanish.

Define F0(X)=f_B(U_(pi^(e-1)X_tilde)). This function is injective: different
socle shifts give different graphs. The exact label identity is therefore

    f_B(g_r(X,t)) = F0(X-2t S_r).

It is an additive HSP on F_p times Sym_n(k), of dimension 1+[k:F_p]*m,
hiding the ONE-DIMENSIONAL F_p line {(t,2t S_r)}. Normalize any nonzero
vector in its complete learned kernel to recover every entry of S_r.
This does not require n separate polynomial learners for each ring digit.

The query map itself need NOT be a group homomorphism: representative
carries and the scalar units can violate that property. The label-fiber
identity, not a false embedded-field claim, is the HSP promise.

A two-query certificate compares f_B(g_r(0,1)) and F0(-2 S_candidate).
Injectivity and invertibility of 2 make this exact under the certified
prefix premise. On acceptance update the prefix by pi^r times the chosen
symmetric lift of S_r. Dropping Delta_t or computing it only modulo pi
can change labels: the exact controls exhibit this carry failure.

## 3. The Final Digit Needs A Different Probe

At r=e-1, the scalar choice would be 1+t, which is not a unit at t=-1.
Do not discard that parameter and invoke a full-field HSP/HPGP theorem.
Instead use E=E_ij, i!=j, and

    A_t=I+t_tilde E,       A_t^(-1)=I-t_tilde E.

All parameters are legal because E^2=0. Use the SAME definition of Delta_t
and g_r(X,t), now with the final known prefix S^(e-1). If T is the remaining
residue digit, direct multiplication gives

    f_B(g_(e-1)(X,t)) = F0(X+P_ij(t)),
    P_ij(t)=t B_ij+t^2 C_ij,
    B_ij=-(E^T T+T E),       C_ij=E^T T E.

Uniform X,t, one original oracle call and clean workspace uncomputation
produce HPGP' states p^(-1/2) sum_t |t>|z-P_ij(t)>, with uniform z.
Expand all k entries in the supplied F_p basis; t remains in F_p. Thus the
published degree-two theorem applies with growing output dimension, even
when k is an extension field. Its learned Q=-P coefficients must be negated.

Choose j=(i+1) mod n for each i. The linear coefficient gives column i:

    T_(k,i)=-B_ij[k,j] for k!=j;     T_(j,i)=-B_ij[j,j]/2.

For each learned pair B,C compare f_B(g_(e-1)(0,t)) and F0(tB+t^2 C) at
t=1,-1. Together with zero constant term these are exact degree-two
certificates for every odd p, including p=3. A check only at 1 is unsound.
Symmetry and cross-column consistency are additional shape checks, not
replacements for the oracle certificates. Return B*[I;S] in original
coordinates after all digits are reconstructed.

## 4. Costs And Complete Error Accounting

There is one initial abelian HSP, e-2 intermediate abelian HSPs, and n
degree-two HPGP calls, regardless of chain length. Each derived source
query uses one original f call plus paid ring arithmetic and uncomputation.
The intermediate additive dimensions are 1+[k:F_p]*m; initial dimension
is [k:F_p]*n(2n+1). Write Q_A(d,eta), Q_2(d,log p,eta) for FULL published
subroutine query bounds, including their precision and capped clocks.
A sufficient original-query accounting before independent-repeat overhead is

    Q_A([k:F_p]*n(2n+1),eta) + (n^2+m+1)
    + (e-2)*(Q_A(1+[k:F_p]*m,eta)+2)
    + n*(Q_2([k:F_p]*m,log p,eta)+4).

All calls must have bounded clocks on all histories. Allocate failure over
e+n calls, repeat independent constant-success learners with finite caps,
and retain ABORT on exhaustion. With exact oracle answers, accepted digits
are correct by induction through the certificates. Approximate quantum
instruments need a separate whole-computation error budget. There is no
free postselection, coherent inverse of a state source, or use of the
hidden next digit by a real query constructor.

Ring arithmetic, symplectic lifting and prefix storage are polynomial in
n and log|R|. A basis of W specifies the answer. If explicit P_W generators
are required, conjugate standard Siegel generators and charge construction
of GL_n(R) and unit-group generators; no factoring speedup is credited as
a new contribution. Concretely, additive generators pi^r*sigma(b_j) give
elementary matrices and symmetric unipotents. A lift of a primitive element
of k^*, together with 1+pi^r*sigma(b_j) for 1<=r<e, generates R^* by its
successive unit filtration. Construct and verify the residue generator
using paid standard finite-field order/factoring algorithms. Gaussian
elimination over a local ring then gives GL_n(R) generation. There is no
assumption that R^* itself is cyclic. The e=1 field case belongs to the
separate field note.

## 5. Full-Oracle Classical Bound For The Last Digit

Fix W_T=image[I;pi^(e-1)T] for uniform T in Sym_n(k), and independently
assign random injective opaque labels to its left cosets. All lower digits
are public. For ANY g=[[A,B],[C,D]] in Sp_(2n)(R), stabilization is equivalent to

    C + pi^(e-1)(Dbar*T-T*Abar) = 0,

because pi^(2e-2)=0. If C is not in pi^(e-1)Mat, there is no fixed T.
Otherwise write C=pi^(e-1)C_star; the condition is the affine-linear system

    C_star+Dbar*T-T*Abar=0 over k.

If it is not identically zero, one nonzero affine coordinate equation
shows that at most a 1/q fraction of T is fixed. If it is identically zero,
T=0 gives C=0, T=I gives Dbar=Abar, and commutation with all symmetric
matrix units forces Abar=lambda I. Symplecticity gives lambda^2=1.
Consequently the common stabilizer is the public subgroup

    K_common = {g : C=0 over R, Abar=+I or -I}.

It is MUCH larger than the center. The field proof's center-only collision
simulation is invalid here: noncentral upper unipotents fix every W_T.

Simulate an adaptive classical algorithm by assigning fresh independent
labels to distinct left cosets g K_common. This path is independent of T.
Couple it to the real oracle until two distinct such cosets acquire equal
P_W labels. Each pair has probability at most 1/q of causing divergence,
so the union bound gives Q(Q-1)/(2q). The simulated output guesses T with
probability at most q^(-m). This proves the displayed success bound without
incorrectly asserting that conditioning on noncollisions leaves T uniform.
The digit certificates imply distinct T have distinct stabilizers at n>=2,
so the same bound applies to subgroup output, not only submodule output.

It yields Omega(sqrt(q)) classical queries for constant success, exponential
in log q at fixed n,e. It says nothing comparable at fixed q and growing
n or e, and is not a lower bound for efficiently structured image labels.
A random lookup oracle need not have a small natural reversible circuit.

## 6. Adversarial Scope Checks

- Odd residue characteristic is essential for trace duality and division
  by two. No binary-ring theorem is asserted.
- W must be a free Lagrangian DIRECT SUMMAND. Purity, residue rank and
  graph uniqueness are not valid for arbitrary torsion submodules.
- Rank n>=2 is essential to the final probes. The existing distinct-line,
  same-stabilizer example over Z/9 is retained, not contradicted.
- The field's unipotent-only final certificate FAILS over rings. Every
  upper unipotent preserves image[I;pi^r T] when 2r>=e, even for T!=0.
  That does not make this graph the top coordinate Lagrangian.
- The field's transvection membership equivalence ALSO FAILS over rings.
  A primitive v=e_1+pi^r f_1 with 2r>=e is outside the top Lagrangian,
  yet its symplectic transvection preserves it. The old field classical
  algorithm cannot simply be imported for lifted digits.
- These failures do not prove classical hardness. Numeric image labels,
  complete Hom-module data or explicit kernel advice can trivialize the
  actual application, as the existing natural-source audits demonstrate.
- The complete quantum learning dependencies and independent novelty
  review remain external to these arithmetic tests. No extra ambient
  group extension should be prioritized without a useful input bridge.

## Implementation And Verification

`theorems/symplectic_prime_power_digits.py` implements Z/p^e public queries,
full-precision prefix corrections, scalar-kernel postprocessing, exact
verification pairs and public symplectic Hensel lifting. It is NOT a
quantum learner or a generic chain-ring backend.

The tests use actual matrix images and independent FLINT inversion over
Z/p^e. They check complete small fibers, every digit, depth seven, a
127-bit prime, reconstruction from supplied correct answers, bad prefixes,
carry losses, nonhomomorphic query maps and both failed field shortcuts.
Separate truncated-polynomial controls over F_p[z]/(z^e), with deliberately
nonhomomorphic residue lifts, check the written equal-characteristic
identity. They do not constitute a generic-ring implementation.

The deepest-digit fixed-point controls enumerate GL_2(F3) and GL_2(F5)
actions on every symmetric residue matrix, compare actual ring actions,
and attain the 1/q bound. These are proof falsifiers, not timed quantum
experiments or a synthetic random-label research campaign.

Verification: 39 new controls and 213 selected tests PASS in 7.55s.
The selection includes both earlier symplectic suites, bounded-codimension
reduction, uniform BCH, polynomial fingerprints and the orbit-module
classical baseline. New Python syntax and whitespace checks PASS. No
full-repository run, CLI integration, registry admission or quantum
execution is claimed.

Next: independent proof/prior-art review and an actual source for this
stabilizer promise. The isogeny label-equivalence and efficient coherent
evaluation gaps are NOT closed by this receiver extension.
