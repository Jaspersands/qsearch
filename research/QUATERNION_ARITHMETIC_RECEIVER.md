# Arithmetic Shadows: The Unpaid Contraction

2026-10-30. Continuation of QUATERNION_RECEIVER_CLASSICAL_FILTER.md.
The question is computational decoding, not another existence proof for
informative measurements. No native principalization algorithm, quantum
execution, general hardness claim or novel speedup is established here.

## 1. Native Contract And Published Primitive

Keep the explicit norm-exact left-ideal input O,I,q and its normalized
lattice L_I=O*a in the product SU(2)^d. The desired output is an exact
generator, recovered from a sufficiently accurate representative of H*a.
The reference/source states are the specified finite positive preparations,
not free shortest-vector states, arbitrary unknown-rotation probes or
uniform affine subspaces substituted for a lattice.

Let p>=5 be prime, let m be the number of prime-coordinate registers,
and let D=p^m. Use a full random m-qudit Clifford C, then a nonzero cubic
phase T on the first register, then its Fourier gate F, then measurement.
The physical order is U=F_1*T_1*C, and a record represents
`|s_b>=C^dagger*T_1^dagger*F_1^dagger|b>`.

[Mao--Yi--Zhu, Theorem 4 and Appendix B](https://arxiv.org/html/2410.13572v2)
give, for a traceless observable Delta, a shadow second-moment bound
`gamma_p*||Delta||_HS^2`, where for one magic gate

```text
gamma_p = 3+4*(p-2)/p  if p != 1 mod 3,
          15/2        if p == 1 mod 3.
```

The inverse channel remains `(D+1)|s_b><s_b|-I`. This is an existing
measurement theorem, not a decoder or a promise of poly(log p) classical
simulation. The ordinary formula x^3 over F_3 is linear; p=3 needs the
paper's separate ninth-root gate, not the p>=5 construction.

Known public modular arithmetic and Fourier gates can describe the
measurement succinctly. A compiled prime-register source/measurement is
not implemented here. Its approximation, padding, modular inverses, gate
synthesis and coherent cleanup must still be charged in a future backend.

## 2. What Precision Is Actually Necessary

For a normalized candidate reference phi, define

```text
A=<s_b|phi>,       X_phi=(D+1)*|A|^2-1.
```

Uniform additive score error epsilon follows from amplitude error of
order epsilon/D. At an amplitude of order 1/sqrt(D), order epsilon/sqrt(D)
suffices. These errors need only polynomially many precision BITS, but
a Monte Carlo method polynomial in inverse additive error is exponential.
This is a cost of those methods, not a lower bound on arithmetic algorithms.

### Close Reference Proxies Are Allowed

Fix the reference and its proxy INDEPENDENTLY of the records being scored.
Let phi_tilde be a normalized proxy, ||phi-phi_tilde||<=e, and put
Delta=|phi><phi|-|phi_tilde><phi_tilde|. The observable is traceless and
`||Delta||_HS^2=2*(1-|<phi|phi_tilde>|^2)<=2e^2`. Therefore

```text
E_Born[(X_phi-X_phi_tilde)^2] <= 15*e^2.
```

Here the record distribution is the ACTUAL source's Born law, not the
uniform distribution on measurement outcomes. The fidelity bias is at
most `sqrt(1-|<phi|phi_tilde>|^2)<=e`. This allows a constant-accuracy
reference proxy with constant-gap decoding. It does not require every
record's two scores to be close. The remaining requirement is an efficient
algorithm to score that proxy; calling a comb a Gaussian does not supply it.
An adaptively fitted proxy needs independent holdout records, or a suitable
uniform guarantee over a specified family. Record-by-record norm closeness
alone is insufficient: for p=5, rotating |0> toward each observed record
by transverse amplitude 0.01 gives MSE about 0.002802, exceeding the
purported bound 15e^2 about 0.001500. This countercontrol does not refute
the fixed-observable theorem. A fidelity gap g needs 2e<g before other
errors; competing proxy families must share the same measurement encoding.

### Relative Probability Evaluation Is Another Sufficient Contract

If an evaluator returns `q_tilde` with |q_tilde-q|<=r*q for
q=|A|^2, then |X_tilde-X|<=r*(X+1). Since the published bound implies
Var(X)<=15/2 and E[X] is a fidelity in [0,1],

```text
|E[X_tilde-X]| <= 2r,
E[(X_tilde-X)^2] <= (23/2)*r^2.
```

Thus relative-probability evaluation could suffice statistically without
uniform 1/D absolute precision. This is an explicit algorithmic promise,
not something implied by CT amplitude access. Zero probabilities, failure
events, and conditioning near cancellations must be handled. A randomized
evaluator needs a charged failure bound for all consumed records; do not
allow rare arbitrarily large score errors and retain the variance claim.
Even clipping estimated probabilities to [0,1] leaves up to
`(D+1)^2*delta` extra unconditional MSE at failure probability delta.
A union bound on successful finite decoding is a different contract.

## 3. Literature Contracts, Not A Free Theta Oracle

The following capabilities are materially different:

- [Cai--Chen--Lipton--Lu, Theorem 1.1](https://arxiv.org/pdf/1005.2632)
  evaluates COMPLETE unweighted quadratic exponential sums in time
  polynomial in dimension and log(modulus), including unknown modulus
  factorization. Over a prime, affine constraints can first be eliminated.
  Interval restrictions, nonuniform Gaussian amplitudes and a cubic
  factor are not part of that algorithm. Its general cubic hardness
  classification does not prove hardness of quadratic plus ONE cubic.
- [Hiary, Theorem 1.1](https://arxiv.org/pdf/0711.5002) evaluates truncated
  one-dimensional quadratic moments `K^-j*sum_(u=0..K)u^j*exp(2pi*i*(a*u+b*u^2))`
  with polynomial work and bit precision in `(j+1)*log(K/eta)`.
  This is genuinely useful at exponential K, but is not a general
  growing-dimensional weighted contraction.
- [Hiary, Theorem 2.2](https://arxiv.org/pdf/0711.5005) also treats
  incomplete cubics with coefficient `0<=c<=K^(mu-3)`, mu<=1, AFTER
  preprocessing of order `K^(4mu)*polylog(K/eta)`. For K comparable
  to p, even coefficient 1/p does not satisfy the small-cubic premise.
- [Elkies--Kieffer, Theorem 1.4](https://arxiv.org/html/2505.22382v2#S1.SS3)
  evaluate modified theta functions at reduced inputs with precision
  cost near linear in requested bits, but dimension factor
  `2^O(g*log(g)^2)`. Argument reduction and its precision loss cannot
  silently be omitted. A reduced-input/fixed-dimension theorem is not
  a uniform polynomial solver in the growing center degree.
- [Barvinok, Theorem 3.3](https://arxiv.org/pdf/2208.05405) gives a
  relative-error approximation algorithm for certain real quadratic
  Gaussians with imaginary LINEAR phase under explicit spectral bounds.
  One sufficient regime is `s*I<=B<=(s+exp(s)/5)*I`, s>=3. It does not
  cover arbitrary imaginary quadratic forms or a cubic phase.

A general scalar complete cubic reduces to a finite-field Airy sum
`sum_(u in F_p) exp(2pi*i*(a*u^3+b*u)/p)`, a nonzero. Square-root
bounds and a rank-two sheaf description do not by themselves evaluate
its individual complex value in poly(log p,precision) time. The reviewed
literature supplies no such general evaluator. This is not a proof that
one cannot exist. Continuous Airy integrals are different objects;
discrete transformations must retain all boundary terms and remainders.

## 4. A Constructive Weak-Cubic Contraction Regime

There IS a useful sufficient condition, derived from the quadratic-moment
algorithm rather than assuming a complete-cubic oracle. Consider

```text
S=sum_(|u|<=W) exp(-lambda*u^2)
                 *exp(2pi*i*(alpha*u+beta*u^2+c*u^3)),
R=lambda*W^2+2pi*|c|*W^3.
```

If R is polynomially bounded in the charged input size and requested
accuracy bits b, then S can be evaluated to error 2^-b with polynomial
work in R,b,log(W), using Hiary's quadratic moments. W itself may be
exponential. This is a promise on the ACTUAL summation interval and
coefficient, not merely on polynomial degree.
Require integer W>=1, lambda>=0, real alpha,beta,c, and polynomial-time
access to certified approximations of those parameters. A negative lambda
would invalidate this definition of R; an uncomputable real is not input.

Put v=u/W. Expand `exp(-lambda*W^2*v^2+2pi*i*c*W^3*v^3)` through
Taylor order L-1, where

```text
L >= max(2*e*R, R/log(2)+log2(2W+1)+b+3).
```

The polynomial has degree at most 3(L-1). The pointwise exponential
remainder is at most exp(R)*2^-L, because L!>=(L/e)^L. Summing the
2W+1 terms therefore costs at most 2^(-b-3). Use a certified upper bound
on R for rounded parameters. Put epsilon=2^-b and J=2W+1. If
P(v)=sum_j a_j*v^j, then ||a||_1<=exp(R), but the moments
`M_j=sum_(|u|<=W)(u/W)^j*exp(2pi*i*(alpha*u+beta*u^2))`
have magnitude at most J, NOT one. Sufficient separate allocations are

```text
max_j |delta M_j| <= epsilon*exp(-R)/16,
||delta a||_1 <= epsilon/[16*(J+1)],
|delta S|_input <= J*[W^2*|delta lambda|
                 +2pi*(W*|delta alpha|+W^2*|delta beta|+W^3*|delta c|)].
```

Keep original and rounded decay nonnegative. Set the last expression
below epsilon/8, reserve epsilon/8 for final arithmetic, and separately
budget the Taylor remainder. Coefficient construction thus needs log(W)
as well as b,R and log(L) guard bits; input rounding needs b+O(log W)
bits with the displayed powers charged. For example, M_2 is of order W,
so an O(2^-b) coefficient error is NOT an O(2^-b) sum error. These are
polynomial precision costs, not an exponential-time obstruction.

Hiary's Theorem1.1 returns error A_1*v^kappa_1*epsilon_internal, where
`v=(j+1)*log(W/epsilon_internal)`, using O(v^2)-bit arithmetic. Choose
epsilon_internal small enough to absorb that polynomial factor. The
theorem is uniform in growing j; all required j are O(L). In its
nonnegative-index convention, reflection gives exactly

```text
M_j=F(W,j;alpha,beta)+(-1)^j*F(W,j;-alpha,beta)-indicator(j=0).
```

The last term removes the duplicate origin. Reduce phase parameters
modulo one. Input, coefficient, moment and arithmetic bounds together
give the stated polynomial-cost ADDITIVE evaluation of the unnormalized
sum, not automatic relative evaluation or a normalized overlap. Even
positive decay and a nonzero cubic allow cancellation: W=1,
lambda=log(2), c=1/5, alpha=-1/5, beta=1/2 gives S=0 exactly.

This yields, for example, a valid regime c=1/p, W of order p^(1/3)
and polynomial lambda*W^2. On the FULL prime interval W of order p,
the same smallest nonzero cubic coefficient gives R of order p^2,
which is exponential in log(p). Narrow physical packets do not imply
that a record's auxiliary cubic variable is localized to the first
regime. Growing-dimensional factorization must also be supplied, not
inferred from the presence of just one cubic gate.

## 5. Exact Record Formula, Including Singular Charts

This formula is derived here; the measurement theorem is prior art. Write
`C^dagger=xi*W(a,d)*mu(S)`, where |xi|=1, the symplectic matrix in
position/momentum order has blocks `[A B; G H]`, and
`W(a,d)|z>=omega^(d.(z+a/2))|z+a>`. All phase arithmetic below is over
F_p. Put r=rank(B). When `B*v=x-a-A*y`, define

```text
Q(x,y) = [(A*y).(G*y)+2*(G*y).(B*v)+(B*v).(H*v)]/2
         +d.(x-a/2).
```

The value is independent of the chosen lift v: B^T*H is symmetric, so
changing v by a kernel vector changes none of these terms. A linear
section on im(B) makes Q quadratic on its affine support relation. The
kernel is `xi*p^(-r/2)*omega^Q`, zero off that relation. For
`y(t)=(t,b_tail)` the normalized record is exactly

```text
chi_b(x) = xi*p^(-(r+1)/2)
           *sum_(t: x-a-A*y(t) in im(B)) omega^(Q(x,y(t))-f(t)-b_1*t).
```

For ANY actual normalized finite source amplitudes a_g(x), its score is

```text
Z_g = sum_(x,t: x-a-A*y(t) in im(B))
          a_g(x)*omega^(-Q(x,y(t))+f(t)+b_1*t),
X_g = (p^m+1)*p^(-(r+1))*|Z_g|^2-1.
```

This includes nonuniform sequential probabilities and full-cell packet
integrals. Replacing those amplitudes requires an approximation proof.
Put `u=A*e_1`, `x_0=a+A*(0,b_tail)`, and `s=rank([B,u])`:

- If s=r+1, the support is exactly `x_0+im([B,u])`. Every x determines
  one affine t(x); the modulus is flat and the phase is quadratic minus
  one rank-one cubic. This is a cubic in GRID coordinates, not in rounded
  lattice coefficients.
- If s=r, all p values of t remain at each x in `x_0+im(B)`. Translating
  t leaves a scalar sum `sum_t omega^(-alpha*t^3+L(x)*t)` times a
  quadratic phase, where L is nonconstant affine. Full-rank B is in this
  case. Magnitudes are nonflat. One cannot replace this sum by a single
  cubic phase or silently evaluate it in poly(log p).

The cancellation support is exact. A sum of p p-th roots vanishes iff
its exponent histogram is uniform, hence iff `a*t^3+l*t` permutes F_p.
For p=1 mod3, its power sum of degree (p-1)/3 rules this out. For p=2
mod3, the power sum of degree (p+1)/3 forces l=0, which is sufficient.
Thus the summed case has full affine support when p=1 mod3, but loses
the hyperplane L=0 when p=2 mod3. The latter support is NOT affine.
Parseval gives `sum_L |sum_t omega^(-alpha*t^3+L*t)|^2=p^2`;
each L occurs p^(r-1) times, proving normalization with the same factor.

Polynomially enumerable occupied support K makes the transverse case
scoreable in K modular solves and amplitude queries. In the summed case
this elementary method costs K*p. Alternatively, a polynomially
enumerable constrained pair set (x,t) suffices. Membership access alone
does not enumerate either set. These are genuine charged subclasses,
not promises established for the native broad lattice source.

### The Simpler Chart Is Rare, And Conditioning Changes The Measurement

For a uniformly random full Clifford, the transverse event s=r+1 has
probability EXACTLY 1/(p+1), for every m>=1. To see this, let V be the
vertical Lagrangian and L=S*V. There are
`N_r=[m choose r]_p*p^(r*(r+1)/2)` Lagrangians with position projection
rank r. Conditional on L, `S^-1*(L intersect V)=ker(B)` is a uniform
(m-r)-subspace of V. Symplecticity gives

```text
A*e_1 in im(B) iff ker(B) is contained in e_1^perp,
Pr[this | r]=(p^r-1)/(p^m-1).
```

The q-binomial identity
`sum_r N_r*z^r=product_(j=1..m)(1+z*p^j)` gives
`E[p^r]=(1+p^(m+1))/(1+p)`, hence Pr[s=r+1]=1/(p+1).
Inverting a uniform symplectic matrix preserves its distribution; this
does not assert that the event is invariant on each individual matrix.
Displacements do not affect the event. Rejection sampling therefore
costs p+1 settings on average, exponential in log(p) when p is large.

More fundamentally, conditioning does not preserve the original frame
inverse or shadow guarantee. At m=1 the transverse condition is B=0;
every record has squared modulus 1/p in every computational coordinate.
All diagonal density matrices then produce identical setting/outcome
distributions. The old fidelity score for target |0> is always 1/p,
even for inputs |0> and |1>. This is nonidentifiability, not a variance
lower bound and not a no-go for other structured multiqudit ensembles.

## 6. A Close Arithmetic Proxy, Without A False Encoding Identity

Use the GAUSSIAN-CELL source from QUATERNION_COVARIANT_RECEIVER.md,
not the older straddle source. Let N=4d, L=M_g*Z^N, and

```text
w_z=exp(-pi*||M_g*z||^2/s^2),   Z=sum_z w_z^2,
phi_x(u)=nu^(-N/2)*exp(-pi*||u-x||^2/(2nu^2)),
q_x(k)=(h/nu)^(N/2)*exp(-pi*||h*k-x||^2/(2nu^2)).
```

The continuous comb G=sum_z w_z*phi_(M_g*z)/sqrt(Z) has norm at least
one. Define the sampled comb Q=sum_z w_z*q_(M_g*z)/sqrt(Z). Let
`eta=rho_(sqrt(8)*nu)(L)-1`, `theta(t)=sum_j exp(-pi*t^2*j^2)`, and
`xi_h=theta(nu/h)^N-1`. Poisson summation gives the sampled Gram identity

```text
<q_x,q_y> = exp(-pi*||x-y||^2/(4nu^2))*Theta_h((x+y)/2),
|Theta_h(v)-1| <= xi_h.
```

The bound is uniform in v and therefore in rotations. Consequently
`1-xi_h <= ||Q||^2 <= (1+xi_h)*(1+eta)`. The coefficient normalizer Z
is NOT the packet-comb normalizer.

Here is an explicit point-sampling estimate. Keep the existing cells
`h*(k+[0,1)^N)` and sample at their LEFT endpoints h*k. Embed Q as
constant on those same cells. For a translation v within one cell, compare
the sampled squared norm of G(.+v)-G with its continuous norm. Its four
Gram terms differ by at most `4*xi_h*(1+eta)`, using the shifted-theta
maximum at zero and Schur row bounds. Also

```text
<grad(phi_x),grad(phi_y)>
 = [pi*N/(2nu^2)-pi^2*||x-y||^2/(4nu^4)]*<phi_x,phi_y>.
```

Because w_z are positive, dropping the negative term proves
`||grad(G)||^2 <= pi*N*(1+eta)/(2nu^2)`. Averaging
`||G(.+v)-G||^2<=||v||^2*||grad(G)||^2` over the cell, whose mean
squared distance from the left endpoint is N*h^2/3, gives

```text
d_h^2 = pi*N^2*(1+eta)*(h/nu)^2/6 +4*(1+eta)*xi_h,
||normalized(G)-normalized(step(Q))|| <= 2*d_h.
```

Sampling at cell centers would replace 1/6 by 1/24, but would also
require the physical offset h/2 in every proxy formula. No such change
to the existing encoding is made here.

This deliberately bounds the sum by Gram operators, not by exponentially
many packet amplitudes. If the actual finite cell source is within
epsilon_fin of normalized G in the common step embedding, its distance
from normalized Q is at most epsilon_fin+2*d_h, before cropping. The
source's pre-existing width, center, coefficient and window errors still
belong in epsilon_fin. Choosing h/nu=O(epsilon/N), together with those
budgets, uses polynomially many bits. It does not obtain arbitrary
accuracy at previously fixed widths.

### Crop, Normalize, Then Encode

Choose R so the squared coefficient tail outside ||M_g*z||<=R is at
most tau, and K=[-B,B]^N with h*B>=R+T*nu and T>h/nu. A conservative
bound on the norm of the discarded part of normalized Q is

```text
e_tail <= [sqrt((1+xi_h)*(1+eta)*tau)
           +sqrt(beta_h+(1+xi_h)*eta)]/sqrt(1-xi_h),
beta_h = N*theta(nu/h)^(N-1)*erfc(sqrt(pi)*(T-h/nu)).
```

The first term is the sampled Gram bound on omitted coefficients. For
retained coefficients the DISCARDED-PART Gram, formed from
`(I-Pi_K)*q_x`, has diagonal at most beta_h and
off-diagonal row sum at most (1+xi_h)*eta. This proves the second term
without multiplying a tail estimate by the number of lattice points.
Cropping and renormalizing costs at most 2*e_tail in ket distance. The
total proxy error is bounded by epsilon_fin+2*d_h+2*e_tail. Require
xi_h<1 and e_tail<1 before normalizing.

Let B_source bound the ACTUAL finite source's coordinate support,
uniformly over every queried orientation. Encode BOTH source and proxy
using the same signed-label map into F_p^N with
`p>2*max(B,B_source)`. This is an isometric relabeling of their common
finite space, NOT a periodic Gaussian. Padding for the proxy alone
would not preserve the comparison if distinct source labels collided.
Small discarded
probability does not justify coherently folding all omitted aliases into
the retained labels: a finite exact control has 1% discarded probability
but fidelity below 1/2 after aliasing. Gaussian-specific alias bounds
would require a separate proof. The needed B and p can have polynomial
bit length while being exponentially large as integers. For the ideal
Gaussian coefficient law, a concrete radius certificate is
`tau_R<=2^(N/2)*exp(-pi*R^2/s^2)`: split one of the two Gaussian
factors on the tail and use the Poisson bound
`rho_s(L)/rho_(s/sqrt(2))(L)<=2^(N/2)`. The existing finite coefficient
caps likewise give a common B_source. No support enumeration is needed
to state these bounds or implied to be efficient by them.

### What The Proxy Does And Does Not Simplify

The joint (z,k) exponent

```text
||M_g*z||^2/s^2 + ||h*k-M_g*z||^2/(2nu^2)
```

is genuinely positive definite quadratic, even for irrational embeddings:
the k block is h^2*I/(2nu^2), and its Schur complement is
M_g^T*M_g/s^2. Its overlap with an arithmetic record therefore retains
Gaussian weights, affine congruences, finite windows and, in general,
an auxiliary cubic variable. Neither its normalization nor its dense
score contraction is supplied by this representation.

There is also an amplitude-evaluable proxy retaining the actual finite
coefficient law P and disjoint packet windows W_z:

```text
b_tilde(k)=sqrt(P(z))*exp(-pi*||h*k-m_tilde_z||^2/(2nu^2))
           /sqrt(sum_(j in W_z) exp(-pi*||h*j-m_tilde_z||^2/nu^2)).
```

Keep the specified rounded center, support and unique recovered z. The
denominator factors into finite one-dimensional Gaussian sums. Direct
summation at small nu/h, or Euler--Maclaurin at large nu/h, evaluates
them with polynomial precision work; do not enumerate an exponential
window. For r=nu/h an order-2j remainder is bounded by
`4*exp(pi)*ell*(2j)!/(2pi*r)^(2j)`, where ell=O(T*r) is the interval
length. For absolute error 2^-b, a sufficient concrete choice is

```text
j=max(1,ceil([b+log2(4*exp(pi)*max(1,ell))]/2)),
r>=2*j/pi.
```

Then `(2j)!<=(2j)^(2j)` proves the remainder bound. In the complementary
regime direct summation costs O(T*j). This uses the source's POLYNOMIAL
VALUE bound on T, not just its bit length; increasing j indefinitely at
fixed r is invalid.
All endpoints, derivative arithmetic and Gaussian integrals are charged.
A conservative cellwise density comparison gives ket error at most
`exp(kappa)-1`, with `kappa=pi*N*(2*T*h/nu+9*(h/nu)^2)` under the
existing T*nu+4h window convention. It is not an ordinary theta function:
P, rounded centers, and hard windows remain part of the amplitudes.
Efficient access to those quantities is the earlier source contract;
errors in their numerical preparation remain additional budgets.

Finally, a larger prime does NOT remove irrational rounding. Native
I=O*(1+i), q=2, has a normalized rotation with coordinates n/sqrt(2).
Labels round(2^12*n/sqrt(2)) begin 0,2896,5793,8689; their squared
labels have third difference -17378, nonzero modulo 2^61-1 without
wrap. An exact affine pullback requires the genuine promise M_g/h
integral. Rounding the BASIS instead preserves linearity but incurs an
error growing with the coefficient range, not just h/nu. Modular
algebraic reduction is also not a real metric embedding.

## 7. One Cubic Gate Is Not Automatically Cheap Stabilizer Simulation

For p>=5 and a!=0, the normalized cubic seed has overlap at most
2/sqrt(p) with any normalized stabilizer: computational overlaps are
1/sqrt(p); other one-qudit stabilizers give a degree-three additive
character sum divided by p. The additive Weil bound applies. See
[Howard's cubic/Alltop analysis](https://arxiv.org/pdf/1501.05319) and
the [explicit Weil hypotheses, Eq.13](https://doi.org/10.1007/s40993-022-00310-3).

Computational ancillas preserve this maximal squared overlap exactly:
projecting a stabilizer onto fixed ancillas gives either zero or
sqrt(q) times a normalized stabilizer, with q<=1. Full Cliffords also
preserve it, so EVERY record in Section5 has stabilizer fidelity <=4/p.
For any decomposition v=sum_j c_j*s_j with ||v-chi||<=epsilon,

```text
sum_j |c_j| >= sqrt(p)*(1-epsilon)_+/2,
(sum_j |c_j|)^2 >= p*(1-epsilon)_+^2/4.
```

This follows from `1-epsilon<=|<chi,v>|`, triangle inequality and the
overlap bound; v need not be normalized. It is the dimension-independent
witness argument underlying [stabilizer extent](https://arxiv.org/pdf/1808.00128),
not a new simulation theorem. In ONE orthonormal stabilizer basis,
k retained terms additionally require `epsilon^2>=1-4k/p`.

Neither result lower-bounds arbitrary nonorthogonal stabilizer RANK.
The exact rank-two state (|0>-|+>)/sqrt(2-2/sqrt(7)) has stabilizer
fidelity below 1/2, refuting the tempting inference rank>=1/fidelity.
No lower bound on nonlinear arithmetic scoring or Born-weighted average
score approximation follows. These are cost warnings for specified
decomposition methods, not a hardness proof or a quantum advantage.

## 8. Decision And Next Scientific Gate

The arithmetic representation is now explicit; a native Gaussian-cell
source can use a close, fixed point-Gaussian proxy at proof level. The
weak-cubic lemma is a real sufficient contraction regime. These remove
ambiguities, but neither supplies an end-to-end principalization algorithm.

Do NOT implement a generic arithmetic-shadow backend on the assumption
that one cubic gate, an exponential-precision float, or an existing theta
library makes the decoder polynomial. The standard complete-sum theorems
do not apply to these weighted finite sums. Selecting the easier chart
does not repair this: it is rare and can destroy identifiability. Cheap
overlap and parity features retain the previous matched classical attacks.

The next constructive re-entry condition is an ACTUAL uniform contraction
for a meaningful native family: specify a record-independent proxy within
a chosen constant error, and prove either a bounded effective-dimensional
factorization or localization sufficient for Section4, on the consumed
measurement distribution. Charge normalization, all congruences/windows,
input precision, failure probabilities and preprocessing. A fixed-degree
center or polynomial occupied support cannot be silently extrapolated to
growing center degree. Test its easiest arithmetic subclass against the
existing CT simulators before asserting any advantage.

Even that contraction would resolve only score evaluation. Searching the
SU(2)^d orientation space remains separate: an exponentially fine exhaustive
net is not an efficient decoder. A successful proposed contraction must
state how its statistic drives an affordable reconstruction and exact
generator verification. No such algorithm was found in this pass.

This is a STOP condition for generic interface expansion, not for quantum
research. If no concrete family/receiver meets that contract, compare an
independent native mechanism rather than repeating adjacent arithmetic
barrier notes. Do not count files, tests, agents or blocked claims as a
measured increase in breakthrough probability.

## 9. Review And Verification Scope

Six focused agents contributed: exact record/support derivation; primary
summation literature; finite encoding/proxy construction; stabilizer-cost
review; independent score/precision review; and independent Gaussian-proxy
review. The exact record agent also checked the transverse-probability
calculation. This is automated adversarial review, not human peer review
or Lean certification. All six agents are now closed. The parent
integrated corrections and ran the combined regression below.

Review repairs included record-independent proxies, complete coefficient
and input precision, the left-endpoint cell constant, the discarded-part
Gram interpretation and shared source/proxy prime padding. The score
reviewer reread the precision repairs and reran its 11 controls. The
Gaussian reviewer approved the conditional analytic claims subject to
the stated repairs; the parent implemented and checked those final edits,
which were not independently reread. Neither review certifies an
algorithm or novelty.

New controls live in tests/test_quaternion_arithmetic_record.py,
test_quaternion_arithmetic_encoding.py, test_quaternion_arithmetic_proxy.py
and test_quaternion_cubic_magic_cost.py. They check exact finite algebra,
rigorous overlap enclosures, and bounded numerical identities. They do
NOT run Hiary's fast algorithm, prove Weil in a proof assistant, execute
a quantum source, or demonstrate asymptotic scaling of a decoder.

Checkpoint verification (Python /opt/anaconda3/bin/python, plugin
autoload disabled, bytecode/cache writes disabled for pytest, -W error):

- 564 selected regression tests passed in 37.69s: all quaternion files
  plus adjacent compact-residue, arithmetic-reduction, native-RLWE,
  registry/CLI and holdout-jet controls.
- All 101 new tests passed again in 7.18s after the common-padding fix:
  45 record, 10 encoding, 11 proxy and 35 stabilizer-cost controls.
- All four new Python files compiled; all 12 site JavaScript files
  passed node --check; tracked-file diff whitespace checks passed.
- python qsearch.py validate returned valid:true and issues:[], with
  8 candidates, 796 experiments, 807 results and 969 retained negatives.
- All 13 registry JSON files remained byte-identical to the starting
  checkpoint: filename/content aggregate SHA-256
  `79c8b3fca6c2bb7c70cca8116b8356bc3dc69734c682feeba16a8bbf1949c0fd`.

This is NOT a full-repository test claim. The previously recorded corpus
SQLite connection-lifetime warnings remain a separate mechanical task.
No CLI/UI/backend, registry promotion, Git write or quantum run occurred.
