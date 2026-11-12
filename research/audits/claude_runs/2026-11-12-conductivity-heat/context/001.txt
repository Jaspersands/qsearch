Previously independently reviewed repository lemma; use only its stated finite BIT contract.

### 3a. Binary binomial sampler with a finite clock

For N in binary, rational p=a/b in[0,1], and TV tolerance0<delta<=1/4,
treat N0 and p0,1 separately. Set mu=Np, v=Np(1-p), and integer
t=ceil(log2(8/delta)). Use w=isqrt(ceil(2vt))+1 and integer radius
r=w+ceil(2t/3). The interval I=[ceil(mu-r),floor(mu+r)] intersect[0,N]
has tail probability<=2exp(-t)<=delta/4 by Bernstein's inequality.
Its length J<=2sqrt(2vt)+4t/3+7. All endpoint arithmetic is rational/integer.

A degree-independent envelope follows directly from Fourier inversion:
|1-p+pe^(iu)|^N <=exp(-2v sin²(u/2))<=exp(-2v u²/pi²), |u|<=pi.
Thus max_k BinPMF(k)<=sqrt(pi)/(2sqrt(2v))<1/sqrt(v), and also<=1.
Let d=isqrt(N*a*(b-a))>=1, M=min(1,b/d). This is a certified rational
UPPER envelope, withinfactor2 of min(1,1/sqrt(v)); J*M<=16t. No clipping
of a genuinely excessive PMF ratio is hidden here.

Use a SINGLE clock: in each round draw h=ceil(log2J) fair bits, discard
j>=J, otherwise propose k=I_min+j and accept with probability
q(k)=BinPMF(k)/M. The exact round success probability is
P(I)/(2^h M)>=3/(8JM)>=3/(128t). Compute a clipped dyadic q_tilde with
absolute error<=e=delta/(64t). Then round success>=1/(64t).
Run R_bin=ceil(64t*ceil(log2(4/delta))) rounds, output floor(mu) on timeout.
The timeout probability<=delta/4. Conditional on success, normalized
q_tilde differs from normalizedq by TV<=JM*e/P(I)<=delta/3.
Together with interval truncation<=delta/4 this is strictly less thandelta.
The bit coin for q_tilde is exact and finite; no nested unbounded rejection.

Evaluate ell=logPMF(k)-logM using logGamma(N+1)-logGamma(k+1)
-logGamma(N-k+1)+klogp+(N-k)log(1-p)-logM. Absolute ell error<=e/8
suffices: if an approximation is below -log(16/e), set q_tilde0; otherwise
compute its exponential, clip to[0,1], and dyadically round within e/8.
Tiny probabilities need no relative precision. A fixed margin in the
cutoff and exponential error covers the uncertain cutoff band.

Here is a complete BIT justification for logfactorials. For x>=2r_s,
the r_s-term positive-real Stirling expansion for logGamma(x) has remainder
bounded by its first omitted term (NIST DLMF5.11(ii),
https://dlmf.nist.gov/5.11#ii, actual statement checked), at most
    4(2r_s)!/((2pi)^(2r_s+2) x^(2r_s+1))
    <=(2r_s/(2pi*x))^(2r_s)<=2^(-5r_s).
Take r_s>=ceil(P/5)+1. If n+1<2r_s, shift log(n!) to
log((n+2r_s)!)-log(product_(j=1)^(2r_s)(n+j)); the correction product
has O(r_s log r_s) bits. Exact Bernoulli coefficients require polynomial
bits/time inr_s. Choose P=O(log(N+2)+log1/e+log(bitlength(b)+2)) with
sufficient guard bits for the O(r_s) sums. The logN term pays multiplication
of logerrors by N, NOT a numericN loop. Standard argument reduction and
2atanh((y-1)/(y+1)),1<=y<2, compute logs with a geometrically convergent
series; the extra log(bitlength(b)+2) precision pays the exponent timeslog2.
Pi and the remaining elementary operations are computed to the same fixed
precision. The total bitlength/time is polynomial in log(N+2), bitlength(p),
and log1/delta. Multinomial sampling uses m-1 conditional binomials, with
parameter p_i/(1-sum_(j<i)p_j), residual photon count, and deterministic
zero-count/zero-probability cases. Per-call TV allocations sum to the
requested proposal error.
