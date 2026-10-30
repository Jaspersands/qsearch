# A Stronger Classical Gate For The Refined AG Window

## Research Decision

The refined unambiguous-decoder argument does not make easy-to-generate
hyperelliptic examples evidence of a speedup. Uniform classical sampling
from the ORIGINAL affine code fiber already succeeds with certified
constant probability on a concrete example where the cubic-annihilator
baseline has zero-dimensional kernel. More generally, this sampler is
efficient throughout the standard AG regime on curves of bounded or
logarithmic F_q-gonality, and in a sufficiently large-alphabet regime.

The method is ordinary linear algebra, limited independence and rejection
sampling, not a newly discovered algorithm. The useful project contribution
is the matched guarantee and the resulting exclusion of an apparent escape
from the previous baseline. Proofs here are written deductions with controls,
not independently reviewed or formally verified.

Do not change the native inverse-trace, cubic-orbit or HSP statuses. The
relation here remains exactly B y=s, y_i!=0 for ALL i. No oracle is supplied.

## 1. Uniform Fiber Sampler

Input: explicit full-row-rank B in F_q^(k by m) and arbitrary syndrome s.
Find one solution y0 and a basis K of ker(B) by Gaussian elimination. For
each independent trial, choose every coefficient of z uniformly in F_q
(including zero), set y=y0+Kz, and accept iff every y_i is nonzero. Verify
the returned vector against the ORIGINAL B,s.

The coefficient map is a bijection onto the affine fiber. Consequently a
successful output is exactly uniform among the full-support words in that
fiber under independent uniform random coins. This also holds conditioned
on success before any fixed attempt cap: each valid word has the same
geometric-series weight. Seeded pseudorandom replays test implementation,
not the statistical claim. A cap failure is UNKNOWN, not hardness or UNSAT.

Preprocessing is polynomial matrix arithmetic; each trial uses m-k uniform
field elements, O(m(m-k)) field operations to form the sample, and a direct
verification. No curve reconstruction, Schur cube, alphabet enumeration,
hidden valid starting state or quantum routine is needed. The implementation
supports odd primes below2^63; the mathematical sampler works over explicit
finite fields in general.

## 2. Certify Acceptance With Dual Distance

Let V=rowspan(B) have minimum Hamming weight at least delta. Uniform sampling
from ANY affine fiber B y=s has uniform marginals on every set of fewer than
delta coordinates. Proof: failure of surjectivity of projection from ker(B)
onto such a set S would give a nonzero vector in V supported on S, contrary
to |S|<delta. Translating the fiber does not change this surjectivity.

For Z=number of zero coordinates and j<delta, therefore

    E[binomial(Z,j)] = binomial(m,j)/q^j.

Bonferroni gives, for any odd h<delta,

    Pr[Z=0] >= L_h := sum_{j=0}^h (-1)^j binomial(m,j)/q^j.       (1)

Use the largest positive available bound, or zero if all are nonpositive.
A positive L_h certifies expected at most1/L_h trials for EVERY syndrome.
After T trials, abort probability is at most(1-L_h)^T.

The helper computes exact rational numbers. It does NOT verify a supplied
distance or independence assumption. The false-promise regression has a
positive formal bound but a coordinate forced to zero; the sampler finds
no witness. Applications must separately establish the hypothesis.

## 3. Polynomial Regimes, Not Finite-Size Inference

Let mu=m/q and q>=3. For an odd h and s0=h+1, Taylor's remainder for
(1-x)^m at x=1/q yields

    0 <= (1-1/q)^m - L_h <= binomial(m,s0)/q^s0
                             <= (e*mu/s0)^s0.

Choose the even s0=2*ceil(4*(mu+1)), provided s0<=delta. Then s0>=8*(mu+1)
and e/8<exp(-1), so the remainder is at most exp(-8*(mu+1)). Also

    (1-1/q)^m >= exp(-m/(q-1)) >= exp(-3*mu/2).

It follows that

    L_h >= (1/2)*(1-1/q)^m >= (1/2)*exp(-3*mu/2).                (2)

Thus if mu<=C*ln(m) and delta eventually exceeds8*mu+10, expected trial
count is at most2*m^(3C/2), polynomial in the explicit input size. For
bounded mu it is constant. The matrix algorithm itself does not need to
know C, a curve map, or the acceptance probability; the finite capped
version reports its actual attempts and may return UNKNOWN.

For AG evaluation rowspace V=ev_D L(G), d=deg G<m and D distinct rational
points disjoint from G, the usual zero-divisor argument gives delta>=m-d.
Monomial equivalence preserves this distance statement. In the standard
refined-quantum range considered in the preceding note, m>2d, so delta>m/2.

If the curve has an F_q-defined map of degree gamma to P^1, then

    m <= #X(F_q) <= gamma*(q+1),
    mu <= gamma*(1+1/q) <= 4*gamma/3.

Every rational point maps to a rational point, and each fiber contains at
most gamma distinct points. This bound does not require knowing the map
inside the sampler. Therefore:

- For fixed gamma, the classical sampler uses a bounded expected number of
  trials on sufficiently large inputs in this range.
- For gamma<=c*ln(m), it uses at most2*m^(2c) expected trials asymptotically.
- All hyperelliptic controls (gamma<=2) are included. Increasing genus alone
  cannot evade this attack, even if the cubic-annihilator kernel vanishes.

These claims concern gonality OVER F_q, not just geometric gonality over
an extension. A missing map certificate cannot be supplied as free advice.
Alternatively the same conclusion follows directly from m/q=O(log m)
and the distance promise, without invoking gonality at all.

## 4. Actual Countercontrol In The Refined Gap

Use the smooth projective model of y^2=x^7+3x over F13, genus3. The polynomial
is squarefree. There are25 affine rational points. Fix19 of them: one at
each of the13 x-values, followed by six distinct conjugate partners. They
are recorded explicitly in receipt.json. Let G=7*infinity and take original
parity rows evaluating 1,x,x^2,x^3,y on those points. Then

    m=19, k=5, dim(V^2)=12, dim(V^3)=19.

The cubic annihilator is ZERO. This is not merely a failed random choice
of h. The prior classical cubic baseline has no usable annihilator here.

The refined quantum estimate from the previous note is nonvacuous:

    E <= (13^5-1)*13^12/12^19 < 0.027077,
    conditional ideal quantum success lower > 0.9729.

This is a conditional analytic estimate, not a quantum execution. The
classical probability is also certified on the SAME B,s. A nonzero
a(x)+b*y, deg(a)<=3, has at most7 evaluation zeros: if b!=0, eliminate y
to the nonzero degree7 polynomial a(x)^2-b^2*(x^7+3x), with at most one
matching y per root. If b=0 there are at most six points above the at most
three roots of a. Hence delta>=12 and h=11 is legal in (1). It gives

    Pr[classical success] >= 30126834384/137858491849
                          > 0.21853448,
    expected trials <= 4.575937.

128 trials fail with probability below10^-12 under independent uniform
coins. For syndrome(1,2,3,4,5), seed26026 gives a verified witness after
four trials and56 field draws. The receipt includes the actual original
matrix, points and witness. Other targets include zero, all basis targets
and32 independently specified syndromes in the tests.

This is an intentionally decisive countercontrol: p<m, no cubic h exists,
and the refined quantum guarantee holds, yet a cheap classical method
finds exactly uniform valid outputs. Do NOT count it as quantum progress.

## 5. Fixed Small Prime Fields Also Fail Asymptotically

There is a separate parameter feasibility restriction, not a runtime test.
For standard complete AG V with2g+1<=d<m, the exact E obeys the lower bound

    E >= (q^k-1) q^(dim(W)-m),  k=d-g+1.

If m<=2d, write a=ell(2G-D)<=2d-m+1, so dim(W)>=m-g and E>1.
If m>2d, dim(W)=2d-g+1. The lower bound rules out m<k+dim(W).
At equality the extra factor (q/(q-1))^wt(c)>=q/(q-1), and k>=2,
still give E>1. Consequently

    E<1 ==> m>=k+dim(W)+1=3d-2g+3>=4g+6.                         (3)

The Drinfeld-Vladut bound says the asymptotic rational-point/genus ratio
over fixed F_q is at most sqrt(q)-1. A research reference for this and
the distinction between prime-field class-field constructions and familiar
non-prime-field recursive towers is
[Beelen's survey](https://arxiv.org/html/2203.03310).
Thus no unbounded-genus family over a FIXED odd prime q<=23 can satisfy
E<1 in this standard range. The finite F13 control above is not a
contradiction: an asymptotic point bound does not forbid finite exceptions.
Changing to a square extension field is not a free rescue: it changes the
input model and invokes the extension-field linear-ansatz attacks already
noted in [Ragavan-Shutty, Section6](https://arxiv.org/html/2610.00502v1#S6).
No general implementation/proof of those additional attacks is claimed here.

## 6. What Survives This Pass

The unambiguous transfer lemma is not refuted. Its proof/review status is
unchanged. Neither is every large-genus AG family classically solved.

A serious next family must avoid the proved low-gonality/large-alphabet
sampling regimes, supply enough actual rational points, and meet the
refined decoder bound. In a fixed prime field it must at least use q>=29
and growing gonality. Lack of a Bonferroni certificate is not evidence of
hardness. Auxiliary-code norm methods and other classical constructions
still require analysis on any such actual input.

Do not generate abstract tuples (q,g,d,m) and treat them as curves. Do not
spend on larger hyperelliptic benchmarks or resurrect legacy circuit search.
The next scientific bottleneck is an explicit genuinely uncovered input
family plus matched classical attacks, not more sampler infrastructure.
