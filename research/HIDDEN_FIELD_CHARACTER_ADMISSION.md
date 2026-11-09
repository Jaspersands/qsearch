# Hidden field characters: classical baseline and Singer scope

2026-11-06. Actual-text independently reviewed written classical reduction.
Section3 is an independently checked application of published coset-state
discrimination bounds. No new efficient quantum receiver, novelty, classical
hardness, or quantum execution is claimed.

## 1. Question, native access and first tests

Let p be an odd prime, n>=2, V=Fp^n, and K an explicitly represented field
of order p^n. An unknown invertible Fp-linear L:V->K defines

    F(x)=lambda_p(Norm_K/Fp(Lx)),  lambda_p(0)=+1.

The chosen-query model supplies a Boolean sign oracle (coherent XOR queries
when needed). A separate, weaker source supplies fresh global pure states
p^(-n/2) sum_x F(x)|x>. They are not interchangeable for chosen affine lines.
The output is an explicit norm circuit G proportional to Norm(Lx), or a
normalized field multiplication on V. Recovering the original L uniquely
is not required: scalar and Frobenius changes give genuine ambiguity.

This is a structured growing-degree character-reconstruction candidate.
Its sign labels also describe the quadratic-residue Cayley relation under
a linear relabeling of its additive coordinates. This interpretation is
motivation, not a claimed cryptographic reduction or new published task.
Desired quantum resources are polynomial(n,logp,log1eta), including source
preparation and output. The tentative mechanism is recovery of the hidden
field symmetry algebra using collective measurements. No such circuit has
been supplied. In particular, a sign oracle is NOT an exact coset-hiding
oracle for a conjugate Singer subgroup; no free reduction between them is
assumed. Scalar/Frobenius stabilizers and all fingerprint costs would need
to be paid in any proposed reduction.

Corpus queries `hidden field norm character Singer subgroup GL conjugate`
and `hidden finite field norm form quadratic character reconstruction`
were run first. The latter names Groebner/linearization attacks; the former
exposed a retained, invalid universal Singer barrier. Current literature
searches supplied no new paid norm-character measurement. The classical
attack below is stronger than merely trying a finite Groebner solve.
Existing generic univariate quantum decoding still has exp(O(n logn))
dependence when applied to chosen lines. Full norm-value access is stronger
than the declared sign input and must not be inserted into this comparison.

## 2. Classical chosen-sign reconstruction

For EVERY invertible L, n>=2 and p>=65536n^2, there is a written classical
algorithm using O(p n log(n/eta)) sign queries and polynomial(n,p,log1eta)
work, returning the exact normalized field algebra and norm or ABORT with
probability at most eta. This is not polynomial in logp. Public finite-field
arithmetic, verified factorization, random choices and retry caps are paid.

The line decoder is the already reviewed Kopparty-based construction in
SYMMETRIC_DETERMINANT_CHARACTER_READOUT.md, classical-baseline section,
using actual AlgorithmA threshold d<=(epsilon/16)sqrt(p), epsilon=1/16.
The source is cached as audits/sources/legendre_prf/kopparty_noisy_2601_07137.*.
Its reuse here does not claim that Kopparty states the whole norm algorithm.

Fix any public v!=0, so Norm(Lv)!=0. Write phi(x)=L(x)/L(v) only for
analysis; neither L nor this division is initially available to the algorithm.

### Verified line primitive

For a public d, query all p values F(v+u d). Try both sign orientations in
the complete-table decoder. Accept only a monic IRREDUCIBLE degree-n output
q(u), q(0)!=0, whose character table disagrees with the attempted table at
at most n points. Every accepted output certifies

    R_d(u)=q(u)/q(0)=Norm(1+u phi(d)).                         (1)

The retained verification proof covers even non-squarefree actual line
polynomials: if q times the actual degree-at-most-n polynomial is not a
nonzero scalar times a square, Weil contradicts the near-total character
agreement. In the exceptional scalar-square case, irreducibility and degree
force proportionality. The actual line is nonzero since u=0 gives Norm(Lv).
Padded zero signs and unknown leading sign are included. Thus a false
generator line is never silently accepted.

If phi(d) has full degree n, the actual line polynomial is irreducible of
degree n and the decoder succeeds. Conversely, if phi(d) lies in a proper
subfield, its degree-n characteristic polynomial has repeated factors;
(1) cannot pass the irreducible filter. For d=0 the polynomial is constant.

### Public field model from one generator

Sample uniform d in V until a line is accepted; call its direction w.
The fraction of non-generators in K is at most

    sum_(ell prime divisor of n) p^(-n(1-1/ell))
        <=omega(n) p^(-n/2).

Define g_a(Z)=Z^n R_w(-1/Z), a monic irreducible polynomial, and construct
the PUBLIC field K'=Fp[Z]/g_a with a=Z mod g_a. There is a unique field
isomorphism sending the analysis element phi(w) to this a. In the rest of
the proof, phi is understood through that isomorphism.

### Frobenius alignment of each basis image

For each public basis vector b, write beta=phi(b) for analysis. Choose
s uniformly in Fp^*, and decode the line in direction w+s b. On acceptance,
its reciprocal polynomial is the minimal polynomial of c=a+s beta.
Factor it in public K', obtaining its n distinct Frobenius roots c_j.
The n candidates beta_j=(c_j-a)/s include the true beta. No hidden
multiplication or discrete logarithm is used in constructing these candidates.

Next choose uniform t in Fp^*, decode the line in direction w+t b, and
compare its R with the public polynomial Norm_K'/Fp(1+u(a+t beta_j)) for
every candidate. Keep all matches. Return this basis image only when exactly
one candidate remains; otherwise draw another t. The true image is never
removed by an exact accepted line.

Two elementary facts bound the clock. First, the affine line a+Fp beta
meets each maximal proper subfield in at most one point. Two intersections
would put their difference beta and then a in that subfield, impossible.
Thus at most omega(n) choices of s or t fail the generator test.

Second, equality of the accepted line norm polynomials for a false beta_j
requires, for some 0<=k<n,

    a+t beta_j = (a+t beta)^(p^k).

For k=0 this is impossible at t!=0. For each k!=0, a^(p^k)!=a, so the
displayed linear equation permits at most one t in Fp. All false candidates
together therefore spoil at most (n-1)^2 choices. An alignment attempt is
uniquely correct with probability at least

    1-[(n-1)^2+omega(n)]/(p-1).

At the stated p threshold each success probability exceeds1/2. There are
2n+1 search stages: one generator, n candidate-building stages and n
alignment stages. Cap each at R=ceil(log2(4(2n+1)/eta)) attempts, allocating
at most eta/4 to their union of clock failures. Allocate eta/4 separately
to capped, verified public finite-field factorization (including any used
by line decoding). Incorrect factorizations are never accepted: certify
irreducibility, the roots, distinctness and reconstructed products.

Unbiased sampling is also capped. After fixing these polynomial arithmetic
and factorization clocks, let Dmax be a public polynomial upper bound on
the number of required base-field draws. For Fp, draw ceil(log2 p) bits as z
and accept z<p. For Fp^*, draw ceil(log2(p-1)) bits as z, accept z<p-1 and
RETURN z+1; rejecting zero directly would miss an endpoint in some cases.
Each trial succeeds with probability at least1/2. Cap each draw at
ceil(log2(4Dmax/eta)) trials, returning ABORT on exhaustion; the union
probability is at most eta/4. Conditional draws remain exactly uniform.
Uniform V draws use n independent base-field draws, included in Dmax.
Thus total abort is at most3eta/4<=eta and worst-case work is polynomial;
there is no unbounded sampling or retry clock hidden in the stated bound.
Arithmetic is exact finite-field arithmetic. This is a written bound,
not an executed Kopparty/factorization pipeline.

The recovered images define B:V->K'. Output

    x star y = B^(-1)((Bx)(By)),
    G(x)=Norm_K'/Fp(Bx)=Norm_K/Fp(Lx)/Norm_K/Fp(Lv).

The algebra identity is v. Multiplication pulled back through UNNORMALIZED
L is not invariant under the allowed scalar ambiguity; that is not the output.
The line inputs must remain chosen-query inputs. A fresh global copy does
not supply a selected affine-line state: selecting a prescribed line costs
probability p^(1-n), absent another paid operation.

## 3. Singer coset copies: the actual known-theorem boundary

This section uses a DIFFERENT input: ordinary coset states for G=GL_n(Fp),
with hidden T one of the N=|G|/[n(p^n-1)] conjugate Singer subgroups. Let
t=|T|=p^n-1 and D=|G|. Standard states are

    rho_T = (t/D) P_T,

where P_T is the rank-D/t projector averaging the right regular T action.
Left/right conventions are equivalent by the known inversion permutation.
Copies are fresh independent states for one fixed hidden subgroup.

The field algebra E_T={0} union T is an embedded copy of F_(p^n). For
distinct T,T', E_T intersect E_T' is a proper finite field containing Fp.
Its degree e divides n and satisfies e<=n/2. Consequently

    |T intersect T'|=p^e-1,
    |T intersect T'|/t <= p^(-n/2).                         (2)

Theorem2.5 and its actual proof in Hayashi--Kawachi--Kobayashi,
[Quantum Measurements for Hidden Subgroup Problems with Optimal Sample
Complexity](https://arxiv.org/abs/quant-ph/0604174), give a PGM whose error
for EACH hidden T is at most

    4 sum_(T'!=T) (|T intersect T'|/t)^k
        <=4(N-1) p^(-nk/2).                                (3)

Thus k=ceil(2 log(4(N-1)/eta)/(n logp)) copies suffice. This is a POVM
statement, with no efficient circuit asserted. It does not require assuming
that blind irrep labels contain the hidden orientation.

For any POVM on k copies, rho_T^tensor(k)<=(t/D)^k I. Averaging its success
over the N equiprobable T and summing the POVM traces gives success<=t^k/N.
Therefore worst-case success >=1-eta requires

    k >= log((1-eta)N)/log t.                               (4)

This is also the direct argument behind the source's Theorem2.3. Since

    N=(p^(n(n-1))/n) product_(j=1)^(n-1)(1-p^(-j)),

(3)--(4) prove Theta(n) STANDARD COSET-COPY complexity at fixed error,
uniformly over odd p as n grows. The cited general theorem already supplies
the method; no new measurement primitive or priority claim is made.
Neither bound is a time bound, nor a bound on all adaptive oracle algorithms.

## 4. Specific legacy claims withdrawn

SINGER_CYCLE_TORAL_HSP_OBSTRUCTION_DELIGNE_LUSZTIG_BARRIER.md incorrectly
states all of the following as general obstructions:

- Every nonscalar Singer element has irreducible degree-n characteristic
  polynomial. At n=4, multiplication by a in F_(p^2) minus Fp instead has
  characteristic polynomial minpoly(a)^2 and preserves proper subspaces.
  This also refutes the old assertion that T has no parabolic elements.
  The ENTIRE Singer group is irreducible; those are different assertions.
- Every pair of classical queries collides with probability at most t/D.
  For odd p, g and c g with c in Fp^* minus {1} collide for EVERY hidden T.
  This rejects the stated bound, without giving a classical HSP solver or
  disproving every possible classical lower bound.
- Identification requires Omega(n^2) standard copies. Equation (3)
  contradicts that assertion. Large commutant/irrep dimensions also do not
  furnish the claimed universal exponential gate lower bound. Its argument
  is withdrawn; an efficient Singer measurement is still not supplied.

Valid scope retained: no nonidentity unipotent lies in T, since p does not
divide p^n-1; final weak irrep labels are conjugacy-invariant. The GL2(F3)
finite calculations do not prove the discarded asymptotic claims.

## 5. Exact finite controls

classical_baselines/hidden_field_scope_control.py/.json preserves two
Sage controls. The first uses K=F81, primitive c of order80, and a=c^10.
It gives minpoly(a)=X²+2X+2 and regular charpoly=minpoly². The public
Fp-linear S(x)=x+c x^9 has determinant2. E intersect S E S^-1 has dimension2,
nine elements and eight units, while each Singer subgroup has order80.
This directly falsifies the old nonscalar claim and checks the proper-
subfield overlap formula, without enumerating GL4(F3).

The second is an ACTUAL finite native classical attack at p3,n3. At p3,
chi_p(z)=z as a prime-field value away from zero, and zero is public because
L is invertible. The producer queried all26 nonzero vectors, built exact
symbolic norm equations plus field equations and invertibility, and used
Sage/Singular Groebner arithmetic. The ten-variable,37-equation system
returned39 solutions. All39 recover the same exact formal norm polynomial
and hidden regular field algebra. Only the validator uses the secret L.
The single run completed inside its30-second cap; no fallback was needed.
The stored count is observed, not evidence of an all-n classification.

This tiny full-domain attack neither proves scalable Groebner recovery nor
executes Section2's high-p Kopparty pipeline. It gives no quantum evidence.
The script was archived from the completed scratch run with only its JSON
destination made relative to its own path; the completed run was not repeated.

## 6. Decision and next scientific gate

No quantum hidden-field subsystem is admitted. The new baseline is classical
poly(n,p), not poly(n,logp); the sign-to-Singer source and efficient collective
receiver remain unpaid. The legacy barrier must not exclude future concrete
receivers, but its correction does not promote this candidate.
Any re-entry must supply a native sign/copy operation with normalization and
decoder cost, and beat the applicable classical baseline under the SAME input.
Generic PGM existence or a small finite solver failure is not acceptance.
Mechanical quarantine/evidence updates belong to MECHANICAL_FOLLOW_UP_PLAN.md;
no registry, manuscript or unrelated test changes are made here.


## 7. Two-copy Bell admission check

6 November 2026. This independent comparison produced a paid operation but
no constructive hidden-multiplication decoder. Let q=p^n and retain the
EXACT padded fresh-copy source of Section1. Two copies, public subtraction
and the additive Fourier transform produce joint amplitude

    q^(-3/2) sum_x F(x)F(x+a) psi(b.x).

The displacement a is exactly uniform. Given a, the normalized b-amplitude
is q^-1 times the sum, not the joint amplitude. This consumes two copies
and polynomial(n,logp,log1epsilon) gates at total error epsilon.

For a!=0, put z=L(a) and define beta only for analysis by
Tr(beta L(x))=b.x; put c=z beta. The conditional amplitude is

    q^-1 [ sum_t chi_K(t(t+1)) Psi(c t)
           + chi_K(z)(1+chi_K(-1)Psi(-c)) ].

The second term is the exact correction at t=0,-1 caused by padding.
Changing the Fourier sign changes both phase signs. The hidden c is NOT
an output label or a callable Kloosterman argument. Obtaining repeated
samples at one prescribed a by rejection costs expected q attempts; no
inverse preparation or reflection is supplied by fresh copies.

A specific linear/bilinear-moment proposal has a cheap analytic falsifier.
For any public v,

    E[psi(b.v)|a] = q^-1 sum_x F(x)F(x+a)F(x+v)F(x+a+v).

When a!=0 and v is neither0 nor +/-a, the four distinct roots give the
quartic Weil bound3/sqrt(q); padding changes at most four summands, giving
absolute value<=3/sqrt(q)+4/q. For v=+/-a, cancellation leaves a two-point
character autocorrelation of nonzero shift2a, bounded by3/q after padding.
For v=0 the expectation is1. For a=0, b=0 deterministically.
Consequently, for EVERY public Fp-linear matrix R,

    |E psi(b.Ra) - p^(-rank R)| <= 3/sqrt(q)+4/q.

Here p^(-rank R) is exactly the probability Ra=0 for uniform a; the other
conditional terms have the stated bound. No independence of a and b or
unavailable hidden coordinates is assumed. The displayed features are
therefore tiny perturbations of public, field-independent quantities;
this does not supply the proposed multiplication-tensor readout. It is
NOT a lower bound for decoding the complete joint law or other receivers.

Corpus and primary-literature admission checks found no paid full-law
decoder. The existing classical poly(n,p) chosen-sign baseline and its
finite controls remain stronger than an unrun generic attack; chosen signs
are not supplied by copies. No Bell, moment or norm-field subsystem/scan
is queued. The independent class-group source comparison produced a
constructive odd-Galois composition instead; see
ODD_GALOIS_CLASS_GROUP_COMPOSITION.md. The parent independently checked
the two endpoint corrections and both autocorrelation cases after the
helper's derivation. No new finite computation is needed for this identity.
