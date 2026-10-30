# Exact Full-Output Baseline For Transfer Products

2026-10-25. Local, unreviewed derivation; no novelty claim. The exact sampler
below is implemented for explicit REAL RATIONAL transfer parameters. It
does not assume a prepared state, amplitude table, or quantum oracle.
It is not an efficient general thermal sampler. Bond size is exponential
in the number of transfer factors and is explicitly charged.

## Why This Follows The Hidden-Mode Pass

The hidden-mode construction would prepare a full canonical pilot if its
active frequency and overlap costs are paid. Testing only its spectrum or
local observables would miss the relevant classical competitor. This pass
constructs the FULL native output distribution for finite transfer products,
including destructive interference and exact conditional probabilities.

The native generators remain

    O_i=X_i product_{max(0,i-R)<=j<i} Z_j,   H=sum_i J_i O_i.

Use the ordered word P(y)=O_0^y_0 ... O_{m-1}^y_{m-1}. It satisfies
P(y)|0>=|y>, and its normalized trace is zero unless y=0. Thus the pilot
of any word-algebra operator A=sum_y a_y P(y) is A|0>=sum_y a_y|y>, with
norm squared sum_y |a_y|^2=tau(A^dagger A). No cycle quotient or sector
restriction is allowed. Output is the native word, with optional local
Hadamards before measurement and arbitrary classical postprocessing.
An arbitrary coherent decoder or entangled measurement is NOT simulated.

## Exact Transfer Automaton

Define the independent-set transfer polynomial

    T(u)=sum_{S independent} (-u)^|S| product_{i in S} J_i O_i,
    A=T(u_1) ... T(u_L).

Independence means successive selected sites in one factor are more than R
apart. Scan sites from left to right. A state c=(c_1,...,c_L) records, for
each factor, how many steps remain before another selection is legal:
each c_l lies in {0,...,R}. Initially all are zero. At site i choose any
subset B of factors whose c_l=0. Emit y_i=|B| modulo two, and update

    c'_l=R if l in B, otherwise max(c_l-1,0).

The transition weight is

    (-1)^I product_{l in B} (-u_l J_i),
    I=sum_{q in B} #{p>q: c_p>0}.

Proof of the sign: expanding A orders first by factor, then by site. To
reorder into canonical site order, a term at an earlier site in factor p
crosses a newly selected term in factor q precisely when p>q. It contributes
a minus sign exactly when the sites are within distance R. One factor has
at most one selected site in that window, and c_p>0 records exactly this
event. Equal-site copies commute and cancel in pairs because O_i^2=I.
Consequently the emitted parity and displayed sign account for ALL word
multiplication, not just support or absolute coefficients.

The resulting two sparse transition matrices M_i(0),M_i(1) have bond

    D=(R+1)^L,
    a_y=e_0^T M_0(y_0) ... M_{m-1}(y_{m-1}) 1.

The final vector is ALL ONES: cooldowns need not expire before the chain
ends. Replacing its outer product by the identity erases interference and
is incorrect. No independent-set or native-word enumeration is needed to
build these matrices. There are at most D*2^L transitions per site.

For X-basis output replace M_i(b) with M_i(0)+(-1)^b M_i(1). The omitted
1/sqrt(2) at each site is a common scalar and cancels from probabilities.
The new norm is 2^m times the physical norm. This is not a free coherent
change of basis on an arbitrary unknown state: the tensors are explicit.

## Exact Sequential Sampling

Build right environments with R_m=1 1^T and

    R_i=sum_b M_i(b) R_{i+1} M_i(b)^T.

For current row v, candidate rows v_b=v M_i(b) have masses
q_b=v_b R_{i+1} v_b^T. Draw bit b with probability q_b/(q_0+q_1), then
continue with v_b. This gives the full normalized squared-amplitude law by
conditional probability. It is not a rejection sampler; there is no average
sign or small postselection probability hidden in its runtime. Zero norm
is rejected. Negative exact masses raise an error, never a clipping fix.

With real rational J,u, all amplitudes, environments, conditional masses,
and Bernoulli draws are exact. A common denominator of polynomial bit length
is obtained from the input denominators to powers O(mL); path counts add
only O(mL) numerator bits. Squaring and conditioning keep polynomial bit
length. Very small nonzero conditional probabilities therefore need more
random bits, not exponentially many rejection attempts. `randrange` samples
the rational Bernoulli exactly in expected polynomial random-bit work.

Conservative arithmetic costs are O(m D^2 4^L) preprocessing and O(m D^2)
per sample, with O(m D^2) stored environments. These are exponential in L,
not polynomial in the original input for arbitrary L. Constant L gives
polynomial cost even for growing R. The implementation uses sparse
transitions but does not assume a compressed bond rank observed in tests.

## Transfer Products Versus The True Thermal State

The ECF transfer identities and mode construction are prior art:
[Elman, Chapman and Flammia, Lemma 2 and Eqs. 75, 81-95](https://arxiv.org/html/2012.07857).
With the same occupation operators Z_k, they give

    T(u)=product_k (I-u epsilon_k Z_k),
    H=sum_k epsilon_k Z_k.

The transfer logarithmic derivative has odd power sums sum epsilon_k^j Z_k
and even scalar power sums. Integrating it at T(0)=I gives this product.
CAR makes the canonical trace uniform over occupation sectors, with all
spectator degeneracy retained. The first pass checks the needed simple-root
and probe-residue premises. The exact word sampler itself needs none of
those spectral assumptions; it works directly from the finite products.

For a conservative constructive thermal control take u=beta/(2L), all L
factors equal, and let M2=sum_i J_i^2=sum_k epsilon_k^2. If beta sqrt(M2)<=L,
then z_k=beta epsilon_k/(2L)<=1/2. After scalar normalization, the kth
factor of the product has angle

    theta'_k=atan(tanh(L atanh(z_k))),

where the true thermal angle is theta_k=atan(tanh(beta epsilon_k/2)). Since
the derivative of atan(tanh x) has magnitude <=1 and
atanh(z)-z <= z^3/[3(1-z^2)] <=4z^3/9 on [0,1/2],

    |theta'_k-theta_k| <= beta^3 epsilon_k^3/(18 L^2).

Uniform occupation sectors give overlap product_k cos(theta'_k-theta_k).
Thus the normalized FULL pilot vector error, and any subsequent measurement
TV distance, are at most

    beta^3 sqrt(sum_k epsilon_k^6)/(18 L^2)
       <= beta^3 M2^(3/2)/(18 L^2).

The executable records the square of this upper bound as an exact rational.
No dense matrix is used to certify it. Dense tests compare the actual
native vector, not a thermal spectrum or isolated marginal.

This repeated-factor approximation is deliberately NOT promoted as the
best classical baseline. For fixed output error and beta=1, the displayed
bound can require L growing as M2^(3/4), and the bond then explodes. Low
temperature does not become cheap because each transfer factor is cheap.

## Higher-Upside Classical Attack: Rational Thermal Compression

Here is a CONDITIONAL extension, not an implemented solver. Suppose an
explicit real rational function r(x)=O(x)/E(x) approximates
tanh(beta x/2) on [0,Emax] to error delta, with O odd, E even and no zero
of E on the interval. Set p(x)=E(x)-O(x), factor it into L linear factors,
and form the corresponding transfer product. Its kth mode is proportional
to I-r(epsilon_k) Z_k; the even denominator contributes only a common
scalar across occupation choices. The angle error is <=delta, so full
state error is <=sqrt(alpha)*delta. Factorization roots may be complex;
conjugate pairs give real final coefficients. Zeros of p on the spectrum
are not automatically fatal, but a zero common E factor is.

[Lin, Lu, Ying and E, Section 2.2](https://arxiv.org/html/0906.1319) give
gapless rational Fermi-function approximations with exponential convergence
in degree divided by log spectral width. [Moussa](https://arxiv.org/html/1605.03085)
reviews logarithmic pole counts and warns of ill-conditioned polynomial
representations. Odd symmetrization preserves the approximation order but
can increase degree by a constant factor.

IF the resulting degree is O(log(2+beta Emax)*log(alpha/error)), and
coefficient/factor rounding is certified at the required precision, the
automaton gives a quasipolynomial classical full-output upper bound, not
just local-observable simulation. For polynomial beta,Emax and inverse
error it has log D=O(log(R+1)*log(m)*log(m/error)). This is a serious
competitor to any proposed major speedup on growing-range paths.

Unfinished obligations: instantiate a numerically stable rational
approximation with explicit constants; certify denominator nonvanishing,
parity, factor rounding and final normalized-state error; support exact
Gaussian-rational transfer parameters and conjugate environments in code.
The current REAL-rational repeated-factor sampler does not discharge them.
Do not label the quasipolynomial extension a completed bit-complexity
theorem or a polynomial dequantization. No generic eigenmode oracle is
needed by the proposed classical construction.

## Falsifiers And Research Decision

- Direct Pauli multiplication must match ALL signed native amplitudes.
  Unsigned independent-layer enumeration fails already on a three-vertex
  path: the full-word coefficient has the opposite sign.
- Every conditional mass must equal an exhaustive suffix sum in bounded
  controls; positive-looking samples alone are insufficient.
- T(1)T(-1)=0 for the rational complete-graph fixture J=(3/5,4/5).
  That is no probability distribution and is explicitly rejected.
- A finite product's exact sampler is not an exact thermal sampler unless
  a separate approximation bound applies.
- Efficient local correlations, transfer traces or positive stationary
  weights do not substitute for this full word distribution.
- No support for arbitrary coherent downstream decoders is claimed.

Research priority: pursue certified rational compression before building
the expensive hidden-mode quantum compiler. It could make the proposed
quantum family substantially less interesting. If it stalls, record the
precise degree/conditioning obstruction instead of treating that failure
as classical hardness. This pass establishes an exact signed full-output
component and a conservative thermal regime, not a breakthrough.
