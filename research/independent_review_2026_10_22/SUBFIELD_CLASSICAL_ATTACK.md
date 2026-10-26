# A polynomial classical attack on even-degree native inputs

**Later strengthening:** SUBFIELD_EXTENSION_ATTACK.md removes the
favorable-point rank assumption using multiple buffers, and gives a
separate attack when the field degree is divisible by three. The
single-buffer algorithm and its failure example below remain valid
scoped results, but no longer describe the strongest attack.

**Status: proved conditional algorithm and average-case deduction.** This
is a solver for the original supplied input when its explicitly checkable
rank condition holds. It adds no witness or oracle. It is not a solver
for every native input: odd field degrees, too few zero targets, and
rank-deficient public points remain outside the guarantee.

## The subfield supplies accepted zero values

Let n=2m, q=2^n, Q=2^m, F=F_q, and k=F_Q. For every a in k,

    Tr_(F/F_2)(inv0(a))=0.

Indeed relative trace from F to k vanishes on k, including at zero.
Thus every zero-target coordinate may range over an entire m-dimensional
binary subspace. The subfield is computable from the supplied field:
the image of z -> z+z^Q equals k; binary elimination extracts a basis.
No subfield basis or favorable representation is supplied for free.

For a set U of zero-target coordinates, define the k-linear map

    L_U : k^U -> F^K,       a -> sum_(i in U) H_i a_i.

Its image is contained in

    W={h in F^K : h_0 in k},       dim_k W=2K-1,

because the first entry of every Vandermonde column H_i is one. The
attack checks whether rank_k L_U=2K-1. Equivalently its binary matrix
has rank m*(2K-1). When this holds, every syndrome in W can be corrected
using accepted zero-target values only.

## Complete algorithm, including the odd-parity obstruction

Assume at least 2K target bits are zero, Q>=16, and K<Q. If all bits
are zero, return x=0. Otherwise choose t with Tr_F(inv0(t))=1, for
example by finding a trace-one basis element c and setting t=1/c.
Necessarily t is outside k. Put t on every one-target coordinate.

If the number of one targets is even, their sum is zero. Let U contain
all zero-target coordinates.

If it is odd, reserve one zero-target coordinate as a buffer. Choose
u in t+k with Tr_F(inv0(u))=0, and put u at that buffer. Let U contain
the remaining zero-target coordinates. Then t+u is in k, so the sum of
all fixed coordinates is again in k. The existence and sampling cost
of u are justified below; they are not assumed.

Compute the syndrome h contributed by the fixed coordinates. Its first
entry lies in k, hence h is in W. Check the rank of L_U. If it is full
in W, solve L_U a=-h by binary Gaussian elimination, put a_i in the
remaining zero coordinates, and verify the original Hx=0 and all trace
bits. If the rank condition fails, report UNKNOWN (one may still try
the actual affine solve, but the theorem does not promise success).

There are at least 2K-1 columns in U. All operations are polynomial in
N and n. No search over q field elements, all subsets, or codewords is
performed. The algorithm preserves the public points and target bits.

## The buffer is found with constant expected work

Choose theta in F with theta+theta^Q=1 and write
theta²+theta=d in k, where Tr_k(d)=1. For any nonzero y in k, the coset
of elements with relative trace y is {y*(a+theta):a in k}. Directly,

    Tr_F(1/[y*(a+theta)])
       = Tr_k((1/y)/(a²+a+d)).

Let chi(z)=(-1)^Tr_k(z), and write
K_Q(c)=sum_(z!=0) chi(z+c/z), W_Q(c)=1+K_Q(c). The sum of signs on
that coset is exactly

    sum_(a in k) chi((1/y)/(a²+a+d)) = -W_Q(1/y).

Proof: a²+a+d runs twice through the trace-one elements; replace their
indicator by (1-chi(z))/2. The first resulting nonzero-field character
sum is -1, and the second is K_Q(1/y).

The same genus-one bound used in the quantum audit gives
|W_Q(c)|<=1+2*sqrt(Q). Therefore the fraction of zero-bit elements in
each nonzero-relative-trace coset is at least

    (Q-1-2*sqrt(Q))/(2Q) >= 7/32,       Q>=16.

Uniformly sampling a in k and testing u=t+a consequently uses fewer
than 32/7 trials on average. A fixed cap B fails with probability at
most (25/32)^B and never returns a false witness. The field operations
and predicate evaluations in every trial are charged.

## The rank condition holds for random public points

This is a deduction about a specified input distribution, not a promise
silently imposed on arbitrary inputs. Sample N distinct public points
uniformly without replacement from F, independently of the target bits.
For any fixed U of size at least 2K-1, its first 2K-1 columns span W
except with probability at most

    rho = min(1, (2K-1)*Q*(K-1)/(q-N)),       q>N.        (1)

To prove this, every nonzero k-linear functional on W evaluates on a
Vandermonde column as a nonzero polynomial of the form

    a_0 + sum_(j=1)^(K-1) [c_j X^j+c_j^Q X^(Q*j)],

where a_0 is in k. This polynomial is nonzero because K<Q prevents
overlap between its nonconstant low and high exponents. Its degree is
at most Q*(K-1). At each stage of sequential column selection, any
proper current span has such an annihilating functional. The next point
misses that span unless it is a root of the polynomial. A root bound
and a union bound over 2K-1 choices prove (1). Conditioning on already
chosen distinct points costs at most the denominator q-N.

At the native N=n², K=floor(N/8), rho is O(n^4*2^(-n/2)). For uniform
independent target bits, fewer than 2K zeros occurs with probability
at most exp(-N/8), by Hoeffding. Thus this classical algorithm succeeds
on random distinct points and random targets, along even n, with
probability at least

    1 - exp(-N/8) - rho - (25/32)^B.

Taking B polynomial in n gives an ordinary bounded-time polynomial
algorithm with negligible failure on that distribution. Expected-time
buffer sampling eliminates the last term. This defeats an asymptotic
quantum-advantage claim on this natural even-degree average-case slice.
It does not establish a classical solver for the entire worst-case
native relation or for odd n.

## Strongest falsifier and scope check

The rank hypothesis is indispensable. If all public points lie in k,
the image of L_U is contained in k^K, with k-dimension at most K,
rather than 2K-1. For K>=2 and a one-hot target at j, the single-buffer
construction at a distinct index ell has relative-trace syndrome in
row one equal to y*(alpha_j+alpha_ell)!=0, where
y=t+t^Q=u+u^Q. It cannot be corrected by coordinates in k. Such inputs
are valid native inputs once Q>=N, and full native witnesses still
exist asymptotically. This is an explicit failure of the attack's
ansatz, not an empty-fiber exception or a quantum-proof error.

Likewise, all-one targets do not provide the required zero coordinates.
The attack does not change their bits or claim to solve them. The next
decisive classical question is whether a comparable construction can
handle these rank-deficient and odd-degree instances, or whether a
proposed hardness distribution explicitly avoids the subfield attack.

## Bounded native control

`subfield_attack.py` uses only this directory's independent field
arithmetic and writes `subfield_attack_receipt.json`. One n=20 instance
with N=400, K=50, modulus X^20+X^3+1, 400 distinct sampled public points,
and a fixed sampled target was checked together with its one-bit variant.
The two targets had 198 and 199 one bits. Both gave the required binary
rank 990 and witnesses satisfying all original equations. The odd branch
used three buffer trials. The same execution checked the one-hot,
subfield-point failure example: rank 500, inconsistent affine correction,
and UNKNOWN. No input was regenerated after a failed rank test.

These finite observations check normalization, parity and implementation
interfaces. The asymptotic attack rests on the algebra and probability
bounds above, not extrapolation from this control.
