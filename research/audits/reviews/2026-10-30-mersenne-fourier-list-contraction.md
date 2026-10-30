# Mersenne Final-Fourier List Contraction

2026-10-30. Task D. **Exact conditional identity and scoped quantitative
failures; no native final-Fourier sampler.** Written derivations, checked
against bounded exact controls below, not native execution, independent
review, formal verification, novelty, or classical hardness claims.

## 1. Scope And Result

Keep EXACTLY the native problem:

    n odd prime >=17, q=2^n, N=n^2, K=(N-1)/8;
    s=floor((n-3)/4), f_s(x)=Tr(inv0(x)^(2^s-1)), inv0(0)=0;
    arbitrary distinct public alpha_i, arbitrary target bits b_i;
    H[j,i]=alpha_i^j, 0<=j<K;
    C=ker H, D=rowspan H, M=|D|=q^K;
    find x in C with f_s(x_i)=b_i for every i.

No witness, favorable layout, changed predicate, or free source is added.
Uniform native sampling is stronger than finding and verifying one witness.

Read before deriving: the current AGENT_HANDOFF top and its Mersenne access
handoff, MERSENNE_RECIPROCAL_RESEARCH_TARGET, MERSENNE_GLOBAL_FOURIER_ACCESS,
MERSENNE_COORDINATE_SCHMIDT_FILTER, MERSENNE_COMPLETION_MOMENTS, the relevant
EXACT_PREDICATE_CHANNEL identities, and the elementary list bound in
BALANCED_CODEWORD_FILTER. Selective searches found no instance of the
two-counter overlap identity below. No priority claim follows from that.

**Result:** the field-label sums in a partial Fourier marginal DO contract
exactly, to two-counter polynomials and one signed weighted sum over D.
This removes q-sized local overlap sums. It does NOT reduce that last sum
to a polynomial number of complete-list entries. Fourier conditioning
punctures D; it does not shorten D. The residual radius stays w, not w-t.
There is an early polynomial-list conditional sampler, but complete lists
eventually contain exponentially many entries, with explicit lower bounds.
Discarding codeword interference instead loses almost all parity-valid mass.
None of these statements uses the coordinate-Schmidt obstruction.

## 2. Exact Prefix-Conditioned State

Use the established, original signed amplitudes and radius:

    chi(v)=(-1)^Tr(v), W(u)=sum_x (-1)^(f_s(x)+Tr(u*x));
    w=floor(3N/5);
    a_i(u)=(q*[u=0]+(-1)^b_i W(u))/(sqrt(2)*q);
    g(e)=[wt(e)<=w]*product_i a_i(e_i);
    A=M^(-1/2)*sum_(d in D) T_d;
    tau=||g||^2, Z=||Ag||^2;
    (1-eta_N)*tau <= Z <= (1+eta_N)*tau, eta_N<1/2.

The final law here is conditioned on the quantum herald, NOT on native
verification: p(x)=|F^-1 Ag(x)|^2/Z. Fourier normalization is q^(-1/2)
per field coordinate, with trace pairing. Translations are additions in
characteristic two. The pre-Fourier R-proposal and B^2/(P R) construction
are inherited; no missing-Walsh-oracle claim is being made.

Take ANY measured coordinate set I, |I|=t, complement J, |J|=m=N-t,
and a proposed measured value x_I. Define

    epsilon_i=(-1)^(b_i+f_s(x_i)), i in I;
    A_I(U)=product_(i in I)(1+epsilon_i U);
    c_I(r)=sum_(j=0)^min(t,r) [U^j] A_I(U), with c_I(r)=0 for r<0.

The elementary local Fourier identity is

    sum_(u!=0) chi(x_i*u)*a_i(u)=epsilon_i/sqrt(2),
    a_i(0)=1/sqrt(2).

Consequently the partially transformed SOURCE slice is exactly

    v_x(e_J)=(2q)^(-t/2)*product_(j in J) a_j(e_j)
             *c_I(w-wt(e_J)).                              (1)

For z_J define the twisted list sum

    B_x(z_J)=sum_(d in D) chi(sum_(i in I) x_i*d_i)
                          *v_x(z_J+d_J).

The marginal of the actual final Fourier law is

    p_I(x_I)=sum_(z_J) |B_x(z_J)|^2/(M*Z).                 (2)

Its residual pre-Fourier conditional state is B_x/sqrt(M Z p_I), when
p_I>0. Applying Fourier on J gives the desired conditional suffix law.
For another measured set T disjoint from I, its conditional probability
is p_(I union T)(x_I,x_T)/p_I(x_I). Thus (2) is an actual prefix-mass
identity, not a point-amplitude or unnormalized-state surrogate.

If x_I satisfies its prescribed local predicates, all epsilon_i=1 and
c_I(r)>0 for every r>=0. Therefore the surviving residual support mask
is EXACTLY wt(e_J)<=min(w,m), apart from zeros of individual W labels.
It cannot be replaced by wt(e_J)<=w-t. Measuring a Fourier coordinate
does not assert that the corresponding original error was nonzero.

## 3. Exact Pair-Overlap Contraction

For h in F_q introduce the unmeasured local two-counter polynomial

    L_i(U,V;h)=sum_e a_i(e)*a_i(e+h)
                         *U^[e!=0]*V^[e+h!=0].

Then

    L_i(U,V;0)=(1+UV)/2;
    L_i(U,V;h)=((-1)^b_i W(h)/(2q))*(U+V), h!=0.          (3)

Proof: balance and Parseval give a_i(0)^2=1/2 and
sum_(e!=0) a_i(e)^2=1/2. For h!=0, Fourier orthogonality applied to
the squared normalized accepted-root state gives

    sum_e a_i(e)*a_i(e+h)=(-1)^b_i W(h)/q
                        =2*a_i(0)*a_i(h).

Thus the entire contribution with e!=0 AND e+h!=0 cancels exactly.
This is a signed cancellation; substituting absolute amplitudes is invalid.
At a measured coordinate the analogous independent pair sum is simply
(1+epsilon_i U)*(1+epsilon_i V)/2.

Write [U^<=w V^<=w] for the SUM of coefficients with both degrees <=w,
not a single coefficient. For d in D let h=wt(d_J), and set

    C_(I,h)=[U^<=w V^<=w]
             A_I(U)*A_I(V)*(1+UV)^(m-h)*(U+V)^h.

Expanding (2), putting d=d_1+d_2, and translating the common unmeasured
received word removes one of the two codeword sums. There are exactly M
ordered pairs with each difference d. Applying (3) gives

    p_I(x_I)=q^(-t)/(2^N Z) * sum_(d in D)
        chi(sum_(i in I) x_i*d_i) * C_(I,wt(d_J))
        *product_(j in J:d_j!=0) ((-1)^b_j W(d_j)/q).       (4)

An especially convenient integer version is

    S_I(x_I)=sum_(d in D) chi(sum_(i in I) x_i*d_i)
        *C_(I,h)*q^(m-h)*product_(j in J:d_j!=0) (-1)^b_j W(d_j);
    p_I(x_I)=S_I(x_I)/(2^N*q^N*Z).                       (5)

Hence S_I>=0 despite its signed expansion, and

    sum_(u in F_q) S_(I union {i})(x_I,u)=S_I(x_I);
    Pr[X_i=u | X_I=x_I]=S_(I union {i})(x_I,u)/S_I(x_I).

Unknown Z cancels from conditional probabilities. Merely evaluating all
q next-symbol probabilities would still be exponential in n; a simulator
would need a paid sampling mechanism or suitable bit-marginal access too.

No two-dimensional polynomial multiplication is necessary:

    C_(I,h)=sum_(k=0)^(m-h) binom(m-h,k)
               *sum_(j=0)^h binom(h,j)
                 *c_I(w-k-j)*c_I(w-k-h+j).                (6)

The c values and all h values can be computed in polynomial integer time;
O(N^3) arithmetic operations is a conservative bound. They depend on x_I
only through t and the number of negative epsilon_i. Every fixed-d term
then costs at most m exact signed Walsh queries and polynomial arithmetic.
The inherited conservative Walsh cost is O(n^45) time, O(n^21) bits of
serial workspace. Signed integers throughout (5) have O(nN+nK) bits.
Direct evaluation of its q^K terms is exponential, not a polynomial
construction merely because each term is polynomially evaluable.

Checks on normalization: I empty yields S_empty=2^N q^N Z. For I all
coordinates, m=0 and character orthogonality gives

    k_w(v)=2^(-N)*sum_(sigma in {0,1}^N:wt(sigma)<=w) (-1)^(sigma dot v);
    p(x)=2^N*|k_w(b+f_s(x))|^2/(q^(N-K)*Z), x in C,
    p(x)=0 otherwise,

exactly the existing final-channel law. Thus (4) retains, rather than
dephases, the codeword interference responsible for Hx=0.

## 4. Puncturing, Shortening, And Concrete List Sizes

In (2), Fourier conditioning attaches a phase to d_I; it does NOT fix d_I.
For m>=K, projection d->d_J is injective and its image is the punctured
RS[m,K] code on the ORIGINAL remaining points. Each nonzero term belongs
to its complete radius-rho list, rho=min(w,m). It is not RS[m,K-t].

When m>w, put a=m-w. The elementary pairwise-agreement argument gives

    gap_m=a^2-m*(K-1);
    if gap_m>0: L_m <= floor(m*(a-K+1)/gap_m).              (7)

This is a polynomial bound since a positive integer gap is at least one.
It is constant only with a proportional gap, not throughout puncturing.
The inherited complete GS decoder applies with changed parameters and
charged interpolation/root extraction: multiplicity
floor(m*(K-1)/gap_m)+1 suffices. It is polynomial here, but the original
multiplicity-four implementation budget and fixed P=8 do not transfer
unchanged. With a=N-w, the original unpunctured L<=7 is recovered.

At the canonical w, condition (7) persists asymptotically only while

    t/N < 1-[3/5+1/16+sqrt((1/8)^2+4*(3/5)*(1/8))/2]
        = 0.0565974368... .

Integer evaluations, not native runs:

| n | N | K | w | Last t with gap_m>0 | L_m bound there | First t forcing >=q entries | First t with all q^K messages |
|---|---|---|---|---|---|---|---|
| 17 | 289 | 36 | 173 | 18 | 143 | 81 | 116 |
| 31 | 961 | 120 | 576 | 57 | 23617 | 266 | 385 |
| 61 | 3721 | 465 | 2232 | 213 | 6139 | 1025 | 1489 |

The exponential columns follow from an explicit interpolation family,
not from failure of the Johnson sufficient inequality. For m>=K and ANY
received z_J, choose r=max(m-w,0)<K of its coordinates. Every polynomial
of degree <K agreeing with z_J there lies within radius w. These are an
affine space of exactly q^(K-r) DISTINCT residual codewords. Therefore

    |List_J(z_J,w)| >= q^(K-max(m-w,0)) whenever max(m-w,0)<K. (8)

At m=w+K-1 this is already q=2^n for EVERY z_J. At m<=w, m>=K,
the list contains all q^K messages. The range between losing (7) and
reaching (8) is NOT proved to have large lists by these arguments.

Zeros of W can remove terms from a weighted list, so (8) alone is a raw
complete-list obstruction, not a lower bound on nonzero amplitudes. A
separate actual-amplitude endpoint removes this caveat: at m=K, D_J=F_q^K.
For ANY accepted x_I and ANY z_J, (1) has one nonzero list entry for every
choice of K symbols from {0} union supp(W). The established fourth moment
sum pi^2<=Delta/q, sum pi=1, implies |supp(W)|>=ceil(q/Delta), with
Delta=14 or 30 according to n-4s=3 or 5. Thus the number of NONZERO
summands is at least

    (1+ceil(q/Delta))^K > (q/Delta)^K=2^(nK-K log2 Delta).  (9)

At n=17 this lower bound already exceeds 2^435. This does not assert
that the m=K endpoint is computationally hard: its residual parity equations
are invertible, and algebraic summation can bypass enumeration. It shows
specifically that a complete nonzero-list representation is not polynomial.

For m<K, punctured CODEWORDS have dimension m, but each has q^(K-m)
message lifts. The twist sums to zero on all lifts unless x_I annihilates
the kernel {d in D:d_J=0}. Equivalently, -H_I*x_I must lie in im(H_J).
When compatible, the multiplicity is q^(K-m) times a representative's phase.
Silently counting those lifts once changes both cancellation and normalization.

There IS a shortening interpretation in (4), but for codeword DIFFERENCES:
fix their zero set T inside J. Then their polynomial has the form

    d(X)=product_(j in T)(X-alpha_j)*u(X), deg u<K-|T|.

For exact support h, |T|=m-h and the shortened dimension is K-m+h,
with nonzero constraints at the other positions. This is not a bounded
list: choosing |T|=K-1 gives q-1 scalar multiples, all with exact support
h=m-K+1 on J. In particular, even before puncturing, exponentially many
different pair differences occur ACROSS received words despite each
individual received word having at most seven list entries.

Geometric ball overlap excludes a difference only when h>2w. Here
2w>=N>=m, so it excludes none of these support classes. For accepted x_I,
every C_(I,h)>0: in (6) choose k=0 and j=floor(h/2). Individual Walsh
factors may still vanish or signed sums may cancel; no lower bound on
their weighted sum or general sampling-hardness conclusion is asserted.

## 5. What The Bounded-List Window Does Constructively Give

The norm of the conditional source slice (1) is explicitly computable:

    S_source=||v_x||^2=(2q)^(-t)*2^(-m)
                         *sum_h binom(m,h)*c_I(w-h)^2.     (10)

To sample its squared amplitudes, draw h with weights
binom(m,h)*c_I(w-h)^2, a uniform support of size h, then independent labels
from the established pi=W^2/q^2 sampler. Approximate label access and
finite-bit/capped randomness must retain their errors and ABORT flags.

For m>=K, draw a uniform punctured codeword and use the twisted B_x of
(2), R_x=sum_d |v_x(z_J+d_J)|^2, and fixed public padding P_m>=L_m.
The same Cauchy rejection rule |B_x|^2/(P_m R_x) has ideal mean acceptance

    Z*p_I(x_I)/(P_m*S_source).                            (11)

This is a useful CONDITIONAL pre-Fourier contraction, not a final sampler.
Indeed v_x remains in the residual pattern subspace. Fourier conjugating
the twisted code sum projects onto H_J*y=-H_I*x_I. The established
all-pattern, all-syndrome Gram bound gives

    (1-eta_m)*S_source <= Z*p_I(x_I) <= (1+eta_m)*S_source.

In the early Johnson window m>=4K, the existing eta_m<1 bounds therefore
give polynomial acceptance and a finite-clock approximate residual
PRE-Fourier sampler, by the existing error-budget method with P_m and the
new support weights. No new compiled or native execution is claimed.
Outside the certified list window this argument has no complete polynomial
decoder premise. Independently, sampling the initial prefix or its next
Fourier coordinate requires conditional mass access; measuring its residual
computational-basis label instead would change the target law.

## 6. Quantitative Failure Of Dropping The Cross Terms

Deleting all d_1!=d_2 terms from the codeword superposition and normalizing
gives the final distribution

    mu_diag(x)=|F^-1 g(x)|^2/tau.

All translated components have this same Fourier Born law. The exact
projection identity F^-1 A F=sqrt(M)*Pi_C implies

    mu_diag(C)=Z/(M*tau) in [(1-eta_N)/q^K,(1+eta_N)/q^K];
    TV(mu_diag,p) >= 1-(1+eta_N)/q^K.                     (12)

So diagonalizing the pairs is almost maximally wrong, quantitatively on
this very native family. At n=17, q^K=2^612. Rejection of mu_diag onto C
would recover EXACTLY p, but needs expected M*tau/Z attempts, between
q^K/(1+eta_N) and q^K/(1-eta_N).

This is not an inaccessible-proposal argument: mu_diag can itself be
sampled using the pattern law k_w(t)^2/tau, which depends only on wt(t),
followed by independent uniform local roots with bits b+t. Its N+1
weight probabilities use binomial/Krawtchouk integer sums; rational coins
have expected polynomial cost, or finite clocks give charged approximation
and ABORT. Local roots cost O(N*n^3) schoolbook Boolean work. The subsequent
parity rejection still pays (12). It is worse than the existing systematic
accepted-completion baseline of about 2^K attempts, not evidence of hardness.

Input checking and reading, public field arithmetic, and final verification
remain charged. Computing Hx costs O(NK) field operations and all predicates
O(Nn) field operations. A generic O(n^3) bit bound per field operation
gives a conservative O((NK+Nn)*n^3) verification bound. Verified native
acceptance under the EXACT final law is uniform on Omega_b; approximate
conditional simulation would require its own TV/failure analysis.

## 7. Exact Controls And Decision

Executed two bounded controls in memory with Python integer arithmetic,
without writing code, reports, caches, or registry records:

    GF(8), modulus X^3+X+1;
    N=5, K=2, alpha=(0,1,2,4,7), b=(0,1,0,1,1);
    (s,w)=(1,2) and (2,3).

For each, direct enumeration computed g, every code translation, B,
and the complete additive Fourier transform using the actual field trace
pairing. Summing squared Fourier amplitudes independently supplied every
whole-coordinate prefix marginal, including empty/full and zero-mass ones.
All 37,449 prefixes per case matched (5) EXACTLY: 74,898 checks total.
The 16 local overlap identities per case and the dephasing mass identity
also passed exactly. No floating tolerance or native-size execution was used.
These are off-regime algebra/normalization controls, not canonical instances.

A compact regression prescription for the parent is to scale
g_num(e)=[wt(e)<=w]*product_i(q*[e_i=0]+(-1)^b_i W(e_i)), let
B_num=sum_d T_d g_num, and use the UNNORMALIZED trace Fourier transform.
For every prefix, the checked all-integer equality was

    sum_(x_J) Fourier(B_num)(x_I,x_J)^2 = M*q^(2N)*S_I(x_I).

The canonical table in Section 4 was separately evaluated with exact integer
inequalities. It is a parameter calculation, not a decoder experiment.
A separate exhaustive GF(8), K=2, w=2 list control on the first m points
of the displayed tuple checked all received words: m=5 had list sizes
0..2 (32,768 words), m=3 had sizes 21..22 (512 words), and m=2 had size
64 everywhere (64 words). These check the original list cap and the
punctured interpolation lower bound, again outside the canonical regime.

**Decision:** retain (3)-(6) as a concrete conditional-contraction interface.
It genuinely eliminates the local field-label sums and exposes a signed
shortened-code partition sum. Do not extend P=8 through Fourier conditioning,
replace puncturing by shortening, infer small total pair count from seven
entries at one received word, or discard interference. Those shortcuts fail
by (8), (9), and (12), with the weighted-versus-raw distinction explicit.
A polynomial non-enumerative evaluation/sampling of the surviving weighted
sum remains open; failure of these specific shortcuts does not prove hardness.
