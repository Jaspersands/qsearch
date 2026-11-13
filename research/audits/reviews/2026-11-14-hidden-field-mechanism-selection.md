# Hidden-field Jacobi and cubic-derivative admission

2026-11-14; independent local derivation. STATE/TRAPS and both requested
topic notes read; corpus `been-tried` and `baselines` run before derivation.
No network, API, Git, finite sweep, or shared-status edit.

**Decision:** the explicit Jacobi instrument below is implementable, but
its measured labels contain exactly no hidden-field information. Keeping
its quantum output preserves an unresolved character-phase decoding task.
The cubic-derivative correlation alternative also supplies no charged
multiplication-tensor decoder. These are scoped failures of concrete
operations, not an impossibility theorem for collective measurements.

## 1. Native inputs and a free-of-advice preprocessing step

Put q=p^n, p odd, n>=2, V=F_p^n. The unknown invertible linear map L:V->K,
K=F_q, defines F(x)=chi_K(Lx) off zero and F(0)=1. The identity
chi_K(z)=lambda_p(Norm(z)) gives the stated norm-character model.
The output must be a normalized multiplication tensor/norm circuit, up to
the existing scalar/Frobenius ambiguity, in poly(n,log p) native work.

A chosen coherent sign oracle and fresh copies of
q^(-1/2) sum_x F(x)|x> are DISTINCT resources. Neither supplies field
values Lx, hidden multiplication, or an exact Singer coset oracle.
The public test x!=0 projects a copy to

    |h> = (q-1)^(-1/2) sum_x h(x)|x>,  h(x)=chi_K(Lx), h(0)=0,

with probability 1-1/q. Fresh-copy retries can be capped logarithmically;
no inverse source preparation is required for this preprocessing.

## 2. Exact three-copy Jacobi instrument and its complete label law

Take three copies |h>. Reversibly map (x,y,z) to (s=x+y+z,x,y), Fourier
transform x and y over the PUBLIC additive coordinates, and measure their
labels b,c. Retain s. This has polynomial gate cost; no postselection yet.

For each dual label t, define beta_t only for analysis by
Tr(beta_t Lx)=t dot x, and h*(t)=chi_K(beta_t), including h*(0)=0.
The additive character convention is exp(2 pi i (t dot x)/p).
The quadratic Gauss identity gives

    Fourier(|h>) = gamma (q-1)^(-1/2) sum_t h*(t)|t>, |gamma|=1.

The identity needs no algorithm computing beta_t. Fourier-transforming s
as well therefore gives joint amplitude

    gamma^3 h*(t)h*(t+b)h*(t+c)/(q-1)^(3/2).                 (1)

Indeed the Fourier exponent is t(x+y+z)+b x+c y; it factors into the
three Gauss transforms. Consequently, with d(b,c)=|{0,-b,-c}|,

    Pr(b,c) = (q-d(b,c))/(q-1)^3.                           (2)

This is EXACTLY independent of L. Conditional on these labels, the
retained Fourier-s register is the normalized three-shift character state
with numerator h*(t)h*(t+b)h*(t+c) and norm sqrt(q-d(b,c)). Measuring t
too gives the public uniform law on t outside those d excluded points.
Discarding the retained register, or treating b,c as tensor samples,
therefore loses all information; retaining it does not decode its phases.

In particular b=c=0 occurs with probability (q-1)^(-2), and its retained
s-state is |h> up to a global phase. Directly, the additive convolutions
satisfy

    h*h = chi_K(-1)(q delta_0 - 1),
    h*h*h = chi_K(-1) q h.                                 (3)

The first formula follows by completing the square at nonzero argument;
the second follows since sum h=0. More generally, Fourier erasure to zero
after summing r copies succeeds exactly (q-1)^(1-r), by the flat nonzero
Gauss spectrum and Parseval. For odd r its successful state is again |h>.
Pure copies supply no Grover reflection. Even with a chosen-oracle
reflection, the r=3 rare branch costs order q amplification and returns
no new tensor. This rejects that specific Jacobi-erasure shortcut.

All identities above are ideal unitary identities. Ordinary finite-bit
additive Fourier compilation approximates the complete instrument in
channel norm. With error epsilon, its label law is within epsilon of (2).
No larger informative signal follows from compilation; a deliberately
different measurement is outside this argument.

## 3. What the cubic derivative actually exposes

For public a,b,c, put s_e=e1*a+e2*b+e3*c, e in {0,1}^3, and
D(x)=product_e F(x+s_e). In the chosen-oracle model eight sign queries
prepare q^(-1/2) sum_x D(x)|x>. Its Fourier law is exactly

    P(t)=q^(-2) |sum_x D(x) exp(2 pi i (t dot x)/p)|^2.       (4)

This is a character-product Fourier law, not a quadratic phase obtained
by differentiating a cubic polynomial. With eight distinct public shifts,
the zero-frequency amplitude is a degree-eight squarefree character sum:
the usual quadratic-character Weil bound gives

    |q^(-1) sum_x D(x)| <= 7/sqrt(q)+8/q.                   (5)

The 8/q term accounts for the padded values at the eight roots. More
generally, cancel every even-multiplicity shift in any r-sign correlation.
If m distinct odd-multiplicity shifts remain, its mean is exactly 1 for
m=0, and has absolute value <=(m-1)/sqrt(q)+m/q for m>0. The degeneracy
test uses only public additive equality, because L is injective.
This is the same squarefree character-sum theorem already used in the
hidden-field admission note; no generic-degree or random-L promise is added.

Every such mean also has a classical bounded estimator: uniform x and
the product of the r chosen sign answers, costing
O(r epsilon^(-2) log(1/delta)) queries. Thus robust polynomially many
inverse-polynomial additive correlations are classically matched in the
chosen-sign model. Multiplying the tiny mean by sqrt(q) requires charging
the corresponding precision; it is not a tensor-value oracle.
This does NOT simulate (4), rule out its full-law decoder, or transfer
chosen queries to a pure-copy source. A prescribed affine-line restriction
of a fresh global copy still costs probability p^(1-n).

## 4. Independent algebraic comparison: explicit diagonal cubic recovery

Consider explicit homogeneous cubic f over F_p, p>3, promised to equal
sum_i c_i ell_i(x)^3 with c_i!=0 and the n linear forms ell_i independent.
Output those forms and coefficients up to scaling/permutation. This is a
classical-input tensor-decomposition endpoint; it does not hide norm signs.
A phase-derivative/Hessian quantum sampler is unnecessary here.

Write L for the row matrix of ell_i. The public Hessians satisfy
H(a)=6 L^T diag(c_i ell_i(a))L. Work over a constructible extension E/F_p
of size Q>=4n^2, choose uniform a,b, and require H(a) invertible and
H(a)^(-1)H(b) to have distinct eigenvalues. Failure probability is at most
n/Q+binomial(n,2)/Q<1/2. Its left eigenlines are the rows of L. Normalize
a nonzero entry of each eigenvector to 1: every resulting entry lies in
F_p, despite using E for the generic pencil. Recover coefficients by
evaluation on the dual basis and verify the entire explicit cubic.
Capped retries, finite-field factoring, and exact linear algebra cost
randomized poly(n,log p,log(1/delta)). There is no hidden basis advice.
This pays a concrete classical comparator, not general cubic equivalence.

The corpus already records generic explicit-form Hessian/QFT as rejected
(STATE:1517 and FUNCTION_FIELD_RELATIONS_RANDOM_SPECIALIZATION.md:28-33).
This independent endpoint therefore supplies no new paid direction either.

## 5. Decision-changing sources and precise reopening condition

Retain the existing classical chosen-sign poly(n,p) reconstruction for
p>=65536n^2; it is not poly(n,log p), and does not apply to pure copies.
The current general hidden-field target remains UNKNOWN, not hard.

Actual sources worth requesting are an algorithm reconstructing a finite
field from its additive group and quadratic-residue/Paley adjacency oracle,
or a collective character-state decoder that outputs the hidden linear
algebra with a polynomial probability and circuit clock. Carlitz-style
automorphism classification alone would establish ambiguity, not a decoder.
Van Dam--Hallgren--Ip shifted-character algorithms must be checked for
their KNOWN reference field/phase-correction requirement; silently using
the unknown dual character in (1) would be circular here.
No additional Jacobi-moment sweep, Singer wrapper, or paid generic receiver
request is justified by (1)--(5). A useful reopening must implement a new
operation on the RETAINED phase states, with its outcome law and decoder,
or supply a genuine chosen-sign classical reconstruction improvement.
