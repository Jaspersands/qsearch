# Independent review: resultant hyperplane reconstruction

2026-11-05. Scope: the proposed abelian-Fourier reconstruction from native
quadratic-character phase copies of an unknown irreducible polynomial.
Read `research/STATE.md` and `research/TRAPS.md`. No archive, network, Git,
registry, manuscript, or external-service action. No numerical experiment is
used as evidence for the asymptotic statements below.

## Verdict and exact scope

The central construction and its probability argument are correct as a
WRITTEN fixed-degree, sufficiently-large-prime quantum algorithm. I found no
hidden extension-field oracle, hidden root, polar transform, or uncharged
conditioning in the construction described below. Its clean coefficient
encoding can be implemented with a single public randomized preprocessing
step that succeeds simultaneously for every split input polynomial. Only
standard finite-field arithmetic, reversible classical computation, and
approximate abelian Fourier transforms are needed.

This is NOT a novelty, classical-hardness, separation, executed-quantum, or
uniform-polynomial-in-degree claim. The parent is conducting the prior-art
check and complete resource/error ledger. Small primes must not be covered
by an automatic finite fallback: the raw promise can have indistinguishable
character tables or phase states there. Concretely over F_3, the distinct
irreducibles X^3+2X+1 and X^3+2X+2 have constant character values +1 and -1,
so their phase states are identical up to global phase. This was also checked
exactly in Sage; the symbolic reason is x^3=x on F_3. For bit access, degree
4 already has 18 monic irreducibles but only 8 nonzero sign tables at p=3,
so bit-oracle identifiability also fails in some small-prime cases. Keep the theorem restricted to sufficiently large
p for each fixed d unless identifiability is separately established.

Let d>=2 be fixed, p an odd prime, and Q in F_p[X] an unknown monic
irreducible polynomial of degree d. The source supplies fresh exact pure
copies

    |f_Q> = p^(-1/2) sum_x chi_p(Q(x)) |x>.

The construction also applies when each copy is produced by one native raw
phase query, or a bit-oracle phase kickback. It does not need a controlled
unknown unitary, an inverse source, or classical access to hidden Q.

One sufficient, deliberately conservative threshold used throughout is

    p >= max{d(d-1), 16 d!, 16(2d-1)^2}.

All constants below may depend on d. Fresh tensor-power source is essential.

## 1. Actual state and clean encoding

Take d source copies and project onto pairwise distinct x_i. The success
probability is rho=(p)_d/p^d, independent of Q, and rho>=1/2 at the stated
threshold. On success, reversible sorting gives a sorted-root register and
a uniform permutation register. The latter is exactly a tensor factor,
independent of the roots and Q, because the product phase is symmetric.
It can be unprepared or discarded without decohering the root register.
There is no d! postselection penalty: folding is a unitary change of labels
with a known tensor factor.

Prepare a coherent uniform a in F_p^* with phase chi_p(a)^d. This is a
public state, not a classical random choice of a. The approximate preparation
cost, or any range-rejection flag used to implement it, must be charged.
Map (a, sorted roots) to the coefficients of

    R(X)=a product_i (X-x_i).

On the fully split squarefree degree-d locus S this is a bijection. Write
N_s=|S|=(p-1) binom(p,d). After cleaning the root registers, the state is,
up to the Q-independent global phase chi_p(-1)^d,

    |S_Q> = N_s^(-1/2) sum_{R in S} chi_p(Res(Q,R)) |coeff(R)>.

The sign follows from Res(Q,R)=(-1)^d a^d product_i Q(x_i).
Every phase is nonzero since d>=2 and Q is irreducible.

### A uniform public seed pays coherent root erasure

Pick L independent uniform public shifts a_j in F_p. For two distinct
r,s in F_p, exactly (p-3)/2 shifts give
chi_p(r+a_j)=chi_p(s+a_j), including the zero as its own trit. This follows
from sum_a chi_p((a+r)(a+s))=-1 and the two zero locations.
Consequently, with probability at least 1-p^2*2^(-L), all p trit signatures
(chi_p(r+a_j))_j are distinct simultaneously. Choose
L=ceil(log_2(p^2/epsilon_seed)). This is a proof by union bound; it does NOT
require examining p elements or certifying the seed classically.

For a monic split R of degree d, successive polynomial gcds with

    X+a_j, and (X+a_j)^((p-1)/2)-1

partition its roots according to these trit signatures; the remaining
factor gives the -1 branch. On the single good-seed event, this factors
EVERY split R into distinct linear factors. Canonical sorting of the roots
makes the output a deterministic function of R and the seed. Modular
exponentiation, gcd, and sorting take poly(d,log p,L) arithmetic/bit work.
Reversible compute-copy-uncompute therefore erases the input roots cleanly.
Failure seeds have total probability <=epsilon_seed and are charged as a
single global failure event, with no branch-dependent advice or restart.
A total implementation can return a failure flag if a factor remains
nonlinear; that bad-seed behavior does not affect the good-event proof.

## 2. Virtual comparison state and Fourier flatness

For the proof ONLY, let E=F_p[X]/(Q) and theta=X mod Q. The linear map

    L_Q: F_p^(d+1) -> E, coeff(R) |-> R(theta)

is surjective, with kernel K=span(coeff(Q)). The quadratic extension-field
character satisfies chi_E(z)=chi_p(Norm_E/Fp(z)). Thus the virtual state

    |N_Q> = [p(p^d-1)]^(-1/2) sum_R chi_E(R(theta)) |coeff(R)>

is normalized, is constant along K, and restricts on S to the actual phases.
It is never prepared. Hence

    <N_Q|S_Q> = sqrt(delta),
    delta = (p-1)binom(p,d) / [p(p^d-1)].

For the ordinary coordinate Fourier transform over F_p^(d+1), let
H=K^perp. Outside H the Fourier amplitude of N_Q vanishes by summing over K.
For y in H, the corresponding additive functional on E has the form
z |-> Tr(tz). The t=0 amplitude vanishes; at each t!=0 the nontrivial
quadratic Gauss sum has magnitude p^(d/2). Including the p-element kernel
and both normalization factors gives exactly

    |<y|F N_Q>| = 1/sqrt(p^d-1),  y in H\{0}.

This uses E only in a proof of an observable distribution. Neither E, theta,
Q, the dual t, nor a Gauss phase is supplied to the algorithm.

## 3. Escape, reconstruction, and all flags

For every proper linear subspace W<H,

    ||Pi_W F N_Q||^2 <= (p^(d-1)-1)/(p^d-1) < 1/p.

Cauchy-Schwarz and the overlap identity imply

    sqrt(delta) <= 1/sqrt(p)
                    + sqrt(Pr_{F S_Q}[y in H\W]).

Therefore each normalized successful Fourier sample escapes every such W
while staying in H with probability at least

    (sqrt(delta)-1/sqrt(p))^2.

At p>=d(d-1), (p)_d/p^d>=1/2, so delta>=1/(4d!). At p>=16d! the escape
bound is at least 1/(16d!). Including the distinct-root projection gives
at least 1/(32d!) per ATTEMPT, before public encoding/QFT approximation.
Any extra heralded public state preparation must be included too, or
implemented as an approximate deterministic circuit.

Make a block of d independent Fourier attempts. Conditional on the first
j samples lying in H and being independent, their span is a proper W<H,
so the same escape bound applies to the next sample. Thus a block consumes
d^2 source copies and, ideally, produces d independent vectors spanning H
with probability at least

    beta_d = [1/(32d!)]^d.

The algorithm does not need to identify which individual samples were good.
For every block, solve its d linear equations in d+1 unknowns. If rank<d,
leading coefficient is zero, or the resulting normalized polynomial is not
irreducible of degree d, reject. On the all-good event, the nullspace is
exactly span(Q), so normalization returns Q. Outlier blocks merely produce
candidates to be checked; they do not require an efficient general noisy
linear-system decoder.

## 4. Native verification and precision

For distinct monic irreducibles Q,Q' of degree d, Q Q' is squarefree and
not a square. The usual degree-2d multiplicative-character Weil bound gives

    |<f_Q|f_Q'>| <= (2d-1)/sqrt(p) <= 1/4.

A fresh-copy projection onto the publicly prepared f_Q' therefore accepts
a wrong candidate with probability <=1/16 and the true candidate with
probability 1, ideally. This requires only a public candidate circuit and
its inverse, never the inverse of an unknown source. Alternatively, native
fresh classical bit queries agree with a wrong candidate with probability
at most 5/8 at this threshold.

Repeat O(beta_d^(-1) log(1/eta)) independent blocks and use
O(log(R/eta)) fresh verification copies per candidate. A bounded schedule
and a union bound suppress missed true blocks and false acceptance.
Approximate public state preparation/QFT/candidate-projection circuits
should have total accumulated trace-distance error <=a designated part
of eta. Their per-call precision can be eta/poly(R,K,d); its logarithm
is polynomial in log(1/eta) for fixed d. The public seed failure above is
another designated part of eta. This yields a WRITTEN polynomial gate and
copy bound in log p and log(1/eta), with potentially very large d-dependent
constants; the parent must state its chosen explicit error allocation.

## Falsifiers and retained boundaries

- A purported coherent encoding that measures a, retains Q-dependent roots,
  or erases sorted roots without the paid inverse is not this algorithm.
- A Fourier proof on a supplied extension-field oracle would change the
  native model. The extension field here occurs only in analysis.
- The escape proof uses overlap with a flat spectrum, not just total mass
  on H. Total mass alone would not guarantee rank growth.
- Degrees growing with the input invalidate a polynomial conclusion from
  beta_d: factorial/exponential dependence is explicit.
- Small-prime character-table nonidentifiability is not repaired by more
  quantum copies. No unrestricted all-p theorem is reviewed here.
- Nothing here establishes a classical lower bound or novelty. No quantum
  receiver has been compiled or run in this review.

## Addendum: main-note retry and precision review

Read `research/LEGENDRE_RESULTANT_HYPERPLANE_READOUT.md` Sections 4--5
on 2026-11-05 after the initial review above. Its actual retry/error
allocation is accepted with the explicit implementation details below.
For q0=(32d!)^(-d), per-block event error <=q0/4 leaves true candidate
probability >=3q0/4, so the note's >=q0/2 is conservative. Per-test event
error <=min(1/16,1/(4K)) gives wrong acceptance <=1/8 and true K-test
acceptance >=1-K/(4K)=3/4. Thus accepted true probability per block is
at least q0/4. The stated

    R=ceil((4/q0)ln(4/eta)), K=ceil(ln(4R/eta)/ln8)

bounds missed true blocks and all false acceptances by eta/4 each.
All probabilities are conditioned on the ONE shared good public seed.
No independence of repeated good-seed events is assumed. Fresh source
copies make the block/test conditional bounds applicable after all earlier
classical outcomes.

The chosen L=ceil(log2(8p^2/eta)) has bad-signature probability <=eta/16:
use binom(p,2)<=p^2/2 in the union bound. To make public random sampling
bounded, for each shift draw n=ceil(log2 p) fair bits and reject values>=p,
with J=ceil(log2(8L/eta)) attempts per shift. Each acceptance probability
exceeds 1/2; the union probability of sampler ABORT is <=eta/8. Conditional
on no ABORT, the shifts are still independent and exactly uniform. This
uses O(L J log p) random bits and no unbounded loop.

Public uniform interval states for the scalar and permutation rank can
be prepared using a binary prefix tree: at each bit, rotate according to
the counts of valid completions in each child interval. Those counts have
O(log p) bits, are explicitly computable by integer arithmetic, and require
only polynomial-precision angle arithmetic. They are coherent states;
classically sampling the scalar is not an acceptable replacement. The
standard uniform approximate arbitrary-modulus QFT theorem supplies the
F_p Fourier operation with poly(log p,log(1/epsilon)) gates. This should be
cited as a standard circuit theorem, not assumed to be an exact primitive.
If the sum of state-preparation and QFT operator errors in a block is at
most q0/8, the difference in any event probability is at most q0/4 by the
hybrid argument and pure-state norm bound. Analogous per-test synthesis
with total operator error at most half the designated event error pays
the verification budget. The resulting precision logarithms have the
claimed fixed-d polynomial dependence.

These are logical-circuit error bounds, not a tolerance theorem for noisy
hardware or imperfect/correlated source copies. With the explicit sampler
cap, the total displayed error is at most eta/4+eta/4+eta/16+eta/8,
strictly below eta. No additional full-computation approximation error
should be added a second time: it is already included in the per-block
and per-test probability guarantees.

## Addendum: independent cubic classical-window proof review

I also independently read
`research/audits/reviews/2026-11-05-cubic-character-window-review.md`.
Its deterministic p-query rank-three theorem for every monic irreducible
cubic and every prime p>=23 is ACCEPTED as a written mathematical result.
The acceptance is based on the all-p proof, not its p=13,17,19 scans.

The key checks are:

1. Reduction modulo X^p-X aliases the high coefficients of Q^h only into
   degrees <=h, so all four coefficients in each proposed equation for
   h+3<=n<=2h-1 are native table data. A null perturbation H gives exactly
   Q^(h-1)(HQ'-H'Q), up to the nonzero scalar h.
2. For nonzero H of degree k<=2, W=HQ'-H'Q is nonzero of degree k+2<=4.
   Removing X^r gives V with V(0)!=0 and r+deg V<=4. The polynomial
   E=Q^(h-1)V satisfies AE'=BE with A=QV, A(0)!=0, deg A=a<=7, and
   leading B coefficient N A_a, where N=deg E=p+e.
3. At p>=23 the prescribed gap length h-3>=8 is at least a. The forward
   recurrence coefficient is j A(0), so zeros propagate to p-1 without
   crossing the zero coefficient at j=p. The reverse coefficient is
   A_a(k-N); L-e=7-(r+deg V)>=3 ensures propagation down to e+1 without
   crossing k=e. Hence E=U_0+X^p Z, both low polynomials having degree<=e<=h.
4. Q^(h-2) divides E'Z-EZ'=U_0'Z-U_0 Z'. Its degree 3h-6 exceeds
   the latter's bound 2e-1<=2h-1, forcing zero. After gcd cancellation,
   each reduced numerator/denominator divides its derivative. Their
   degrees are <p, so both are constant, including the U_0=0 case.
   Thus E=Z(X+c)^p. Irreducibility forces Q^(h-1)|Z, contradicting deg Z<=h.

This proves full rank, and three-column elimination costs O(p) field
operations. Standard fast product-tree interpolation costs O(M(p)log p).
The finite script's Lagrange interpolation is not evidence that this fast
implementation was run. This classical result is quasilinear in p and
therefore exponential in log p; it does not remove the classical
poly(log p) question or establish a separation/novelty claim.
