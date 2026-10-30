# Low-Rank Conjugation Symmetry: Scoped Application Filters

29 October 2026. Application audit and written deductions, not a new
implemented learner, exhaustive impossibility theorem, or speedup claim.
No credible family surviving these matched-access baselines was found.

## 1. Input, Target, And Boundaries

The reference contract is [REES_SUBSPACE_SYMMETRY_SOURCE.md](REES_SUBSPACE_SYMMETRY_SOURCE.md):
fresh IID copies of an UNKNOWN exact flat state rho=P/r, supplied correct
rank r=poly(input length), an explicit exponent-p Lazard group G of fixed
class c<p, and an efficiently controlled LINEAR unitary representation R.
The target is H={g:R(g)P R(g)^dagger=P}. A supplied delta>0 obeys
TD(rho,R(g)rho R(g)^dagger)>=delta for EVERY g outside H, where
TD(a,b)=||a-b||_1/2. Inverse delta and all charged operations are polynomial.
No basis of P, preparation inverse, conjugate copies, projector oracle,
prepared coset state, or oracle explicitly hiding H is supplied.

Each filter below states its EXTRA structure. Quantum-assisted baselines
are not classical simulations; classical postprocessing of paid quantum
measurements is a legitimate same-input competitor. Flatness is essential.
The general nonflat mixed-state spectral reduction is separate work.

## 2. Usual Heisenberg Actions Collapse To An Abelian Quotient

Let G=Heis_p^m, p odd, with its usual tensor Schrodinger representation.
Its center acts by scalar phases even on states entangled across all blocks.
Thus conjugation factors through A=G/Z(G)=F_p^(2m), and H=pi^-1(K) for a
subspace K<=A. In particular H is normal; block entanglement cannot change
this representation-theoretic fact. This does NOT cover nonscalar centers.

Use symmetric Weyl representatives W(v), so W(av)=W(v)^a. For flat rho,
the reference note prepares Omega_P, the top exterior state, from copies.
The projective action V(v)=W(v)^(tensor r) has ray stabilizer K and
|<Omega_P|V(v)|Omega_P>|<=1-delta^2/2 outside K. Its multiplier is the
usual Weyl multiplier raised to r; no assumption r<p is needed.

[Holt--Subramanian, Sections 9.1--9.2](https://arxiv.org/html/2609.38085v2#S9)
give efficiently constructible a_1=1,...,a_t, t<=4, with sum a_j=0 and
sum a_j^2=0 modulo odd p. Then B(v)=tensor_j V(a_j v) is LINEAR on A.
It fixes Omega_P^(tensor t) exactly on K: the eigenphases cancel.
Outside K its overlap has the same upper bound, using the first factor.
Abelian Fourier samples lie in K-perp. Every v outside K violates a
sampled character equation with probability at least delta^2/4; a union
bound over A gives M=O((m log p+log(1/epsilon))/delta^2) samples.
Classical finite-field elimination recovers K and lifts it with the center.

The reference hard-clock preparation costs O(M r^2 log(rM/epsilon)) raw
copies and O(Mr) original controlled actions, plus charged growth/swap
circuits and precision. Rank one needs no growth. This is a copy-only
quantum-assisted abelian baseline, not a nonabelian Rees application.
No promise about unrelated Paulis on the exterior registers is imported.

## 3. Faithful Permutation EPR Pairing: Easy Even For Variable p

On a two-p-qudit block define R(a,b,c)|x,y>=|x+a,y+bx+c>, over F_p.
Composition gives (a,b,c)(a',b',c')=(a+a',b+b',c+c'+b a'). For odd p this
is a faithful class-two exponent-p Heisenberg action; its center translates
y and is NOT scalar. Controlled modular arithmetic costs poly(log p).

Let m be an even number of labeled blocks with an unknown perfect matching.
On every matched pair prepare Phi_(p^2)=p^-1 sum_(x,y)|x,y>|x,y>.
The global state has rank one and efficient preparation by entanglement
distribution; the learner receives copies, not the preparation wiring.
This physical source does not assume a subgroup oracle or a coset state.

For a pair, <Phi|R(g) tensor R(h)|Phi>=Tr(R(g)^T R(h))/p^2. It equals one
exactly when g=h. A nonidentity affine permutation fixes either zero or p
basis points: a!=0 fixes none; a=0,b!=0 fixes one x and all y; nonzero
central translations fix none. Hence the overlap outside the diagonal
subgroup is at most 1/p. Product overlaps show a GLOBAL trace-distance gap
sqrt(1-p^-2). The stabilizer is a product of diagonal Heisenberg groups,
which are nonnormal in their paired ambient factors.

Computational-basis measurements defeat this candidate WITHOUT tomography.
In each copy true partners receive the same uniform z=(x,y) in F_p^2;
different matched pairs receive independent z. Across L IID copies assign
each block its length-L signature. True partners always agree. Any two
unrelated blocks agree with probability p^(-2L). Union bounding by m^2:

    L=ceil(log(m^2/beta)/(2 log p))  =>  Pr(any false match)<=beta.

Group equal signatures and return each size-two class as a pair. Abort if
any class has another size; under the source promise a false collision
merges whole pairs and is detectable. There is no independence assumption
between collision events. Use exact signature comparisons after hashing,
or deterministic sorting, to avoid uncharged hash-collision errors.
Storage is O(m L log p) bits; sorting costs O(m L log p log m) bit operations.
Each recovered pair directly supplies the three simultaneous generators
(a,b,c)=(1,0,0),(0,1,0),(0,0,1) on its endpoints, identity elsewhere.
Thus original-coordinate subgroup output is constructive. Preparation and
measurement inaccuracies require their own budget. No p^4 tomography cost
is needed, and this attack remains polynomial in log p, not numerical p.

## 4. Local Parent Projector Filter

Assume additionally that P projects onto the ENTIRE kernel of
L=sum_(j=1)^t Q_j, with 0<=Q_j<=I, Q_j supported on S_j of size at most s,
and L>=lambda(I-P), lambda>0. Require t>=1 and 1<=s<=n.
There are n blocks of dimension d; t and
1/lambda are polynomial. The local-measurement theorem below takes s,d
and the local finite group size as constants, or charges their growth.
The parent need not be supplied to the learner: its existence, locality
bound, term-count bound and gap lower bound are additional source promises.

For sigma=R(g)rho R(g)^dagger=P'/r, the two projectors have EQUAL rank r.
Their principal angles theta_i give the exact identities

    TD(rho,sigma)=(1/r) sum_i sin(theta_i),
    1-Tr(P sigma)=(1/r) sum_i sin(theta_i)^2.

Cauchy--Schwarz, the parent gap, and Q_j rho=0 consequently imply

    TD(rho,sigma)^2 <= 1-Tr(P sigma)
      <= Tr(L sigma)/lambda
      <= (1/lambda) sum_j TD(rho_(S_j),sigma_(S_j)).

The last step uses the variational bound for the effect 0<=Q_j<=I on its
support, not an unnormalized operator-norm comparison. Every nonsymmetry
therefore changes some marginal by at least lambda*delta^2/t.

For constant-depth bounded-fan-in U and a product projector P_0=tensor_i P_i,
take Q_i=U(I-P_i)_i U^dagger. Their sum has kernel U im(P_0), gap one,
and bounded forward light cones, even when the output is entangled.
This covers shallow flat mixtures and pure shallow states. It also covers
other entire gapped frustration-free ground-space projectors satisfying
the table contract below. A SELECTED state inside a degenerate kernel is
not covered: the parent does not separate it from other ground states.

## 5. Observable Table And Noise-Safe Colors

Suppose the public physical action factors through a supplied subgroup
Gamma<=K wr S_n, where K is an explicit finite local group of order kappa
with a known d-dimensional representation. Site permutations alone use
K={1}. Gamma must be solvable; the supplied p-group promise suffices.
Local group enumeration, multiplication, representation matrices, and
measurement of the observables below must be efficient and charged.

Choose a Hermitian Hilbert--Schmidt orthonormal basis B_1,...,B_(d^2)
with ||B_a||_infinity<=1. Index ALL tensor products on subsets T, 1<=|T|<=s,
using local factors R_K(k) B_a R_K(k)^dagger, k in K. Retain duplicate
operators as distinct indices. This table is exactly closed under the
public action by multiplying k labels and permuting sites. Its size is

    M=sum_(ell=1)^s binom(n,ell)*(kappa*d^2)^ell.

No ambient Hilbert-space matrix is expanded. For a D=d^ell dimensional
marginal difference, if every original basis coefficient is at most u,
then TD<=D^(3/2)*u/2. The conservative constant C=d^(2s) therefore works.
By Section 4, some table means differ under every nonsymmetry by at least
tau=lambda*delta^2/(t*C). This uses the k=identity entries of the table.

Write mu_i=Tr(rho O_i), all real in [-1,1], and allocate failure beta.
Use charged rational lower bounds delta,lambda and rational 0<beta<1.
Set h=tau/4 and e=beta*h/(16M). Choose a uniform random offset
theta=h J/Q, with J in {0,...,Q-1} and Q a power of two >=16M/beta.
Define IDEAL colors c_i=floor((mu_i-theta)/h). For each fixed mu_i,
the probability of distance <=2e from any grid boundary is at most
4e/h+2/Q. Union over all M means bounds this bad-offset probability by
3 beta/8. Unknown exact values are not inspected to select the offset;
the separation event is probabilistic, not a certified observation.

Estimate EVERY mean to additive error e, simultaneously except with
probability beta/2. Independent estimation noise is allowed. On the
good-offset and good-estimation events, computed colors equal ideal colors
EXACTLY, so equal exact means cannot be split. Rational grid arithmetic
uses polynomial precision in log M, log(1/beta), and the input bounds.
For bounded outcomes, separate fresh-copy measurements cost
O(M e^-2 log(M/beta)) copies; measurement implementation costs are additional.
The remaining beta/8 pays total acquisition/implementation error.

Every true symmetry preserves ideal colors. Conversely, color preservation
implies |mu_i-mu_(g.i)|<h for every index, contradicting the >=tau witness
of a nonsymmetry. Thus the computed color stabilizer is EXACTLY the target
image on the good events. This is not threshold clustering of noisy means.
The cost is polynomial only in the displayed table size and precisions;
growing s, d or kappa can invalidate polynomial-in-physical-input claims.

## 6. Constructive Subgroup Output And Kernel Accounting

[Luks's solvable-group set-stabilizer theorem](https://arxiv.org/html/1704.08529#S6)
(Theorem 10 there) yields color stabilizers by successive set stabilizers.
Apply it to the EXPLICIT finite permutation action, not to an implicitly
exponential observable domain. Charge its polynomial permutation-group work.

To avoid losing the table-action kernel, augment the M indices by a
faithful reference action F of Gamma. For K wr S_n, use the n disjoint
regular K-fibers: degree n*kappa, with site permutations transporting fibers
and local K acting by regular multiplication. Give all reference points
one reserved color; this adds no constraint. The combined action has degree
M+n*kappa and is faithful. All permutations of the input generators are
constructed explicitly. Table-kernel elements are retained, not discarded.

Require the original map pi:G->Gamma to be supplied on generators, with
efficient original-group arithmetic and generators of ker(pi) if nontrivial.
For coordinate-labeled G<=K^n or supplied site-permutation groups pi is
injective. Otherwise kernel generation is an EXTRA charged obligation;
an unspecified nonfaithful black box is not covered by this filter.

Build a base and strong generating set for the augmented image, retaining
each Schreier generator and transversal as a straight-line program in the
input image generators. Sift each returned generator through this chain
and compose the recorded programs to obtain constructive membership words.
Evaluate these programs in the original G generators, without exponentially
expanding words, and add the supplied ker(pi) generators. Charge this
polynomial constructive permutation-group step and original arithmetic;
no such backend is implemented in this note. The result generates the full
preimage: any element differs from a word in the chosen lifts by ker(pi).
Thus neither preimages nor invisible kernels are assumed free.

## 7. Other Filters, Verification Scope, And Decision

Stabilizer-code projectors have r=p^k; polynomial rank restricts k accordingly.
Under Paulis their conjugation stabilizer is S-perp modulo phases, with
gap one. Under Clifford actions distinct equal-rank code projectors have
Tr(PP')/r<=1/p, hence TD>=1-1/p by measuring P. Learn the signed stabilizer
from copies first, then apply the defining-characteristic p-group subspace
baseline to the signed Weyl-coordinate subspace. This does not confuse
scalar-support with conjugation symmetry; see [mixed stabilizer learning](https://arxiv.org/html/2609.38085v2#S9.SS3.SSS1)
and [CLASS_THREE_APPLICATION_AUDIT.md](CLASS_THREE_APPLICATION_AUDIT.md).

Product flat states admit tomography at the CHARGED local dimension.
A computational-basis uniform
mixture of r distinct strings exposes its support in O(r log(r/beta)) copies.
Arbitrary correlated nonorthogonal product mixtures are NOT thereby solved.
Nor does the [finite-field TT filter](TENSOR_TRAIN_CLASSICAL_FILTER.md) prove
learnability of unknown complex MPS/PEPS, arbitrary tensor networks, or
nonflat densities. None of these scope exclusions is hardness evidence.

Small rank and efficient preparation do not establish the global gap:
cos(theta)|0^n>+sin(theta)|1^n> has nontrivial correlated Z symmetries, yet
TD(psi,Z_1 psi)=|sin(2 theta)| sin(pi/p). Taking theta=2^-n gives an
exponentially small gap with a succinct preparation; this is not a hard family.

Prior in-memory controls found qutrit Weyl gaps one, a faithful affine
rank-three code gap 2/3, and the EPR gap sqrt(8/9); 40 actions checked the
parent-energy inequalities on a rank-three nonstabilizer shallow source.
These finite numerical controls are not asymptotic proofs or executed
learners. The arguments above are written proofs with explicit contracts.
The unresolved application must evade these filters AND prove its own
global gap; no oracle planting, generic infrastructure plan, or promotion
of a surviving natural hard family is justified by this audit.
