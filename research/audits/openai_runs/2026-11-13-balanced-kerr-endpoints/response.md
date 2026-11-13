## Verdict — no fatal interpolation error found; one dependency needs completion

**The strongest gap is the scalar-evaluation citation:** the claimed log-factorial routine, LF201–216 of an unprovided file, cannot be verified from this package. A self-contained polynomial-bit replacement is given below.

The identities, physical sign, entire-function product, contour estimate, and coefficient/denominator bounds check out. The quoted real-Hiary theorem has the required normalized polynomial weights and permits growing degree. Its precision conversion also checks out.

**Conclusion:** using the quoted Hiary Theorem 1.1 as an external theorem, the endpoint-amplitude claim survives, with the scalar completion and explicit finite-bit choices below. This is not an independent verification of Hiary’s omitted analytic proofs or an executed implementation. Numerical bounds for its fixed constants remain an implementation obligation, not input-dependent advice. No ACCEPT label or unprovided repository material is used.

## 1. Exact identities and physical convention

Write \(\rho=\min(r,K-r)\), applying the upper-endpoint reduction before choosing subsequent parameters.

The first identity is correct:
\[
K_r(K-n)=\sum_{j=0}^{r}(-1)^{r-j}2^j
 {K-j\choose r-j}{n\choose j}.
\]
Indeed,
\[
(1-z)^{K-n}(1+z)^n
=(1-z)^K\left(1+\frac{2z}{1-z}\right)^n.
\]
Coefficient extraction gives the identity, including its sign and leading coefficient \(2^r/r!\).

For integer \(x\in[0,K]\), reversing the generating polynomial gives
\[
z^K(1-z^{-1})^x(1+z^{-1})^{K-x}
=(-1)^x(1-z)^x(1+z)^{K-x},
\]
hence
\[
K_{K-s}(x)=(-1)^xK_s(x).
\]
Consequently, \(r=K-s\) is reduced to \(s\) by multiplying the answer by \((-1)^K\) and shifting the linear phase by \(1/2\). The normalization is unchanged. This reduction requires the identity only at integer summation points.

The advertised physical sign is also correct for initial state \(|K,0\rangle\), with \(n,r\) counting mode \(a\). The first rotation supplies
\[
2^{-K/2}(-1)^{K-n}\sqrt{{K\choose n}}.
\]
The second matrix entry is
\[
2^{-K/2}(-1)^n
\sqrt{\frac{{K\choose n}}{{K\choose r}}}\,K_r(n).
\]
Using \(K_r(n)=(-1)^rK_r(K-n)\) gives physical amplitude
\[
(-1)^{K+r}A_r.
\]
This sign must be applied for a literal complex-amplitude contract.

Finally, Vandermonde’s identity gives
\[
|K_\rho(K-n)|\le {K\choose \rho}\le(K+1)^\rho.
\]
The normalization integer has \(O(\rho\log(K+1))\) bits and needs only \(\rho\) multiplicative factors, not a numerical-\(K\) factorial computation.

## 2. Window and entire interpolation: the estimates are valid

Use the submitted parameters, with \(r\) now meaning the reduced endpoint:
\[
\ell=\operatorname{bitlength}(K+1),\quad
Q=p+(r+1)\ell+20,\quad J=2048Q.
\]

The direct branch \(K\le2^{30}Q^2\) is legitimate: its term count and even expanded factorial lengths are polynomial in the charged resources. \(K=0\) is immediate.

Otherwise, with
\[
c=K/2,\quad w=\lceil\sqrt{KQ}\rceil,\quad
L=\lceil c-w\rceil,\quad U=\lfloor c+w\rfloor,
\]
the cutoff implies \(w<K/4\) and \(w>J/2+1\). All endpoints and nodes can be computed by integer arithmetic.

Hoeffding gives
\[
\sum_{n\notin[L,U]}P_K(n)\le2e^{-2w^2/K}\le2e^{-2Q}.
\]
After multiplying by the deliberately loose Krawtchouk bound and discarding the normalization’s beneficial effect, the amplitude error is at most
\[
2^{r\ell+1-2Q}<2^{-p-20}.
\]

### Entire extension

For \(K>0\),
\[
f(c+u)=\frac{2^{-K}\Gamma(K+1)}
 {\Gamma(c+u+1)\Gamma(c-u+1)}
\]
is entire. Pairing opposite shifts in Euler’s gamma limit gives
\[
\frac{f(c+u)}{f(c)}
=\prod_{l=0}^{\infty}
 \left(1-\frac{u^2}{(c+1+l)^2}\right).
\]
The finite-product prefactors cancel; convergence is locally uniform because the reciprocal-square series converges. There is no omitted exponential factor.

Duplication and the beta integral yield
\[
f(c)=\frac1\pi\int_0^1
 t^{c-1/2}(1-t)^{-1/2}\,dt\le1.
\]
Also
\[
\sum_{l\ge0}(c+1+l)^{-2}\le\int_c^\infty t^{-2}\,dt=2/K.
\]
Thus, for every complex \(u\),
\[
|f(c+u)|\le e^{2|u|^2/K}.
\]

### Contour error, including odd \(K\)

The nodes
\[
n_i=\lfloor c\rfloor-J/2+i,\qquad 0\le i\le J
\]
are integers because \(J\) is even. For odd \(K\), their center is displaced by \(1/2\); nevertheless
\[
|n_i-c|\le J/2+1/2<w,
\]
so all nodes remain inside the window.

Let \(\omega(z)=\prod_i(z-n_i)\). The residue formula is
\[
f(n)-I_J(n)=\frac1{2\pi i}
 \oint_{|z-c|=8w}
 \frac{f(z)\omega(n)}{\omega(z)(z-n)}\,dz.
\]
At nodes the error is zero. Elsewhere in the window,
\[
|n-n_i|\le2w,\qquad |z-n_i|,\ |z-n|\ge7w.
\]
Since \(w^2/K\le4Q\),
\[
\sup_{|z-c|=8w}|f(z)|
 \le e^{512Q}\le2^{1024Q}.
\]
Therefore
\[
|f(n)-I_J(n)|
\le\frac87\,2^{1024Q}(2/7)^{J+1}
\le2^{-1024Q}.
\]

Summing against the endpoint polynomial costs at most
\[
(K+1)^{r+1}2^{-1024Q}<2^{-p-20}.
\]

**Clustered nodes cause no missing analytic error factor.** Their numerical conditioning is paid separately through exact coefficient construction and additional precision.

## 3. Exact coefficients really have polynomial bit length

Set \(M=U-L\) and \(x=(n-L)/M\). The adjacent ratios
\[
q_i=\prod_{t=0}^{i-1}\frac{K-n_0-t}{n_0+t+1}
\]
are exact positive rationals with \(O(J\ell)\)-bit numerator and denominator. Their bound \(q_i\le(K+1)^J\) is valid.

The submitted Lagrange basis has the correct denominator and sign:
\[
l_i(x)=
\frac{\prod_{j\ne i}(Mx-(n_j-L))}
 {(-1)^{J-i}i!(J-i)!}.
\]
Each numerator has coefficient norm at most \((2M)^J\). Hence
\[
\|R_J\|_1\le(J+1)[2(K+1)^2]^J.
\]

A common denominator is exactly available as
\[
D_{\rm node}J!,\qquad
D_{\rm node}=\prod_{t=0}^{J-1}(n_0+t+1).
\]
Each ratio’s prefix denominator divides \(D_{\rm node}\), and each basis denominator divides \(J!\). Its bit length is
\[
O(J(\ell+\log(J+1))).
\]
Using this common denominator prevents artificial denominator explosion during addition.

For the Krawtchouk polynomial, each falling-factorial factor satisfies
\[
\|(L+Mx)-t\|_1=|L-t|+M\le2K
\]
for the relevant \(t\). The claimed bound follows:
\[
\|K_r(K-L-Mx)\|_1\le(r+1)[4(K+1)]^r.
\]
A denominator \(r!\) suffices.

Thus \(W=R_JK_r(K-L-Mx)\) has degree \(d=J+r\), common denominator
\[
D_{\rm node}J!r!,
\]
and the stated bound \(\|W\|_1\le2^E\). Numerator lengths are bounded by the denominator length plus \(E+O(1)\). Dense exact construction is polynomial-time.

This is the essential cancellation argument: coefficients may be enormous numerically, but their **bit lengths** and the required extra precision are polynomial.

## 4. Actual Hiary interface and finite-bit reduction

Writing \(W(x)=\sum_{j=0}^d w_jx^j\), translation gives exactly
\[
\frac{b_0}{\sqrt{{K\choose r}}}\,
e(AL+BL^2)
\sum_{j=0}^d w_j F(M,j;A+2BL,B).
\]
The quoted source defines
\[
F(M,j;a,b)=\sum_{k=0}^{M}(k/M)^j e(ak+bk^2),
\]
with \(0^0=1\). There is no missing \(M^j\), \(1/M\), or endpoint term. All arguments supplied to Hiary are real. Call each \(F\) separately; the source’s bounded initial coefficient condition is then satisfied.

The formal Theorem 1.1 explicitly covers every integer \(j\ge0\), with polynomial dependence on \((j+1)\log(M/\eta)\). No fixed-degree extrapolation is needed.

### Error-prefactor conversion

Let \(\tau\) be a desired error per \(F\), \(q_0=\lceil\log_2(1/\tau)\rceil\), and \(m=\lceil\log_2(M+1)\rceil\). Fix integers
\[
a_0\ge\log_2\max(1,A_1),\qquad s\ge\max(1,\kappa_1).
\]
The attached reduction’s choice
\[
X=q_0+m+j+a_0+s+10,\qquad
q=16(s+1)^2X^2,\qquad \eta=2^{-q}
\]
works. Indeed,
\[
\nu=(j+1)\log(M/\eta)\le32X^5,\qquad
\log_2\nu\le3X,
\]
and therefore
\[
A_1\nu^{\kappa_1}\eta
\le2^{a_0+3sX-q}\le\tau/2.
\]
The precision allocation is noncircular and polynomial.

### Huge denominators and branch decisions

First compute the translated phases and constant phase **exactly modulo one**, charging their original encoding length. Round the two arguments of \(F\) to dyadics with
\[
R=q_0+3m+8
\]
fractional bits. The derivative bounds imply total perturbation at most
\[
16(M+1)^3\,2^{-R}\le\tau/16.
\]
Thus an arbitrarily long input denominator does not force that denominator into the theorem’s operand-size bound. Its bits are still read and processed.

The rational branch guard in the attached review is correct. For normalized
\[
a=A_0/D,\quad b=C_0/D,\quad D\ \text{even},\quad
0\le C_0\le D/4,
\]
a nonboundary iteration has common denominator
\[
D'=4C_0\le D,
\]
with numerators \(2A_0,-D\). Integer reductions, conjugation, and half-shifts preserve this denominator. Floors and ceilings are therefore exact polynomial-bit operations. When the quadratic argument vanishes, use the boundary procedure, not division by it.

The new length is at most \(\lceil M/2\rceil\); outside the small-length branch there are \(O(\log(M+1))\) iterations.

One useful implementation completion is to avoid an exact comparison involving a logarithm in the small-length test. Since
\[
1000\nu^6\le
1000[(j+1)(m+q)]^6,
\]
use the integer right-hand side as a conservative direct-evaluation cutoff. This can only enlarge the direct branch by a polynomial amount. There is no uncharged binary-large enumeration.

The omitted boundary analysis is supplied by the **quoted theorem**, not independently established by the excerpt’s pseudocode.

## 5. Scalar repair and complete precision budget

Here is a replacement for the unavailable log-factorial routine.

For desired absolute log accuracy \(2^{-S}\), take \(t=S+O(1)\). To evaluate \(\log(m!)\), choose
\[
N=\max(m,4t)
\]
and use
\[
\log(N!)=(N+\tfrac12)\log N-N+\tfrac12\log(2\pi)
+\sum_{k=1}^{t-1}
 \frac{B_{2k}}{2k(2k-1)N^{2k-1}}+R_t.
\]
The positive-real Stirling remainder satisfies
\[
|R_t|\le
\frac{|B_{2t}|}{2t(2t-1)N^{2t-1}}.
\]
The bound \(|B_{2t}|\le4(2t)!/(2\pi)^{2t}\), together with \(N\ge4t\), makes this exponentially smaller than \(2^{-S}\) with a fixed additive margin in \(t\).

Recover \(\log(m!)\) by subtracting at most \(4t\) logarithms. Bernoulli coefficients can be generated exactly by their finite recurrence with polynomial-bit common denominators. Powers, Stirling coefficients, and shift terms have polynomial bit length.

Evaluate logarithms with enough additional fractional bits to pay multiplication by \(N\) and summation. This requires
\[
S+\operatorname{bitlength}(N)+O(\log(t+1))
\]
fractional bits, still polynomial. In particular, the large values of the three log-factorials do not invalidate subtraction at prescribed **absolute** accuracy.

Apply this to
\[
\log b_0=\log(K!)-\log(n_0!)
-\log((K-n_0)!)-K\log2.
\]
The multiplication by \(K\) needs \(\ell+O(1)\) extra fractional bits. No \(K!\) or denominator \(2^K\) is expanded.

Because \(\log b_0\le0\), exponentiation after clipping the approximate logarithm to the nonpositive axis is Lipschitz with constant one. Certified underflow clipping is safe; otherwise the retained exponent has magnitude \(O(P)\). All elementary-function work is polynomial-bit. The inverse square root of the already expanded \({K\choose r}\) is likewise polynomial-bit.

Now take the submitted budgets:
\[
\tau=2^{-p-E-\operatorname{bitlength}(d+1)-20},
\]
\[
P=p+E+\ell+\operatorname{bitlength}(d+1)+50.
\]
The total weighted Hiary error is at most \(2^E\tau\). The exact pre-scalar sum has modulus at most
\[
(M+1)\|W\|_1\le2^{E+\ell}.
\]
Computing each scalar to absolute \(2^{-P}\), clipping the two nonnegative scalars to \([0,1]\), therefore leaves ample margin.

For final assembly, round the \(F\) outputs to a common dyadic precision and combine them with the exact common coefficient denominator. The products and sum can then be performed exactly as rationals of polynomial bit length. Only the final output rounding needs another small error allocation.

The tail, interpolation, Hiary, scalar, and final-rounding errors sum to less than \(2^{-p}\).

## 6. Attacks, falsifiers, and charged scope

The requested edge attacks do not expose a counterexample:

- **Endpoint and parity:** the reciprocal identity handles \(r=K-s\) exactly. Odd \(K\) changes the central-node displacement by only \(1/2\), already covered.
- **Huge rational denominator:** only bit-length-dependent rational arithmetic and certified dyadic rounding are used. No period enumeration or cyclotomic-field construction occurs.
- **Cancellation:** every bound is absolute and phase-uniform. Neither a nonzero answer nor relative accuracy is assumed.
- **Growing endpoint degree:** \(r\le Y\), \(J=O(p+(Y+1)\ell)\), and all coefficient lengths and requested precisions remain polynomial.

Useful **symbolic falsifiers for an implementation**, not substitutes for the uniform proof, are:

1. For integer Kerr phase, \(A_r=\mathbf1_{r=0}\); the physical amplitude at \(r=0\) is \((-1)^K\).
2. For \(K=1\), Kerr is identically trivial: physical amplitudes are \(-1,0\). Dropping the physical sign fails immediately.
3. \(F(M,0;0,0)=M+1\); returning \(1\) detects an erroneous interval normalization.
4. Zero quadratic argument and exact integer floor boundaries must not trigger an unguarded reciprocal or rounded branch comparison.

All native input bits are charged, including the full phase encoding. Direct loops occur only under explicit polynomial cutoffs; scalar shifts and polynomial construction also have polynomially bounded loop counts. Final output uses \(O(p)\) bits per component. This is a classical scalar computation with no state-preparation or amplitude oracle.

**Final status:** the endpoint reduction is mathematically sound relative to the quoted real-Hiary theorem, after the scalar completion above. It establishes neither a sampler nor a CDF compiler, bulk result, quantum speedup, hardness claim, or executed implementation.