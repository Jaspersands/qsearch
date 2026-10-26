# Independent reconstruction of the quantum argument

Status: proved deductions below are the reviewer's mathematical derivations,
not claims of formal proof-assistant verification. They assume the standard
finite-field character bound and the explicitly justified deterministic
GS/Roth–Ruckenstein algorithms. No existing source files are modified.

## Input, Fourier convention, and preparation

Let F=F_(2^n), D=RS_alpha[N,K], C=D^perp=ker H with
H_(j,i)=alpha_i^j. The field modulus and basis, N distinct points, and
b in F_2^N are supplied. N<=q is necessary. The annihilator with respect to
Tr(sum d_i x_i) equals the *field-linear* dual: if a field inner product
were nonzero, multiplying d by an appropriate scalar would detect it under
the nondegenerate trace pairing. There is no binary-dual/field-dual gap.

Set S_i={x:Tr(inv0(x))=b_i}. Inversion with zero fixed is a permutation,
so |S_i|=q/2. A uniform affine trace hyperplane has an exact circuit from
n-1 Hadamards and binary affine maps. Apply reversible totalized inversion
and clean its workspace. The result is |S_i>. The trace-character QFT is
an n-qubit Hadamard transform combined with a public invertible binary map
derived from the trace Gram matrix. No arbitrary rotation or q-entry table
is necessary. Inversion can be exponentiation to q-2 with O(n) field
multiplications, with an explicit q=2/zero branch. All these are polynomial
Boolean circuits and admit exact classical reversible implementations.

For B_i(u)=sum_(x in S_i) chi(ux), the Fourier amplitude is
a_i(u)=sqrt(2) B_i(u)/q, with a_i(0)=1/sqrt(2).
Orthogonality gives sum_u B_i(u)B_i(u+d)=q B_i(d).
For d!=0 the two terms u=0,d already equal q B_i(d), hence the remaining
signed correlation is zero. This uses real characteristic-two characters.

## Why truncation is controlled

Write A=|D|^(-1/2) sum_(d in D) T_d, so A* A=sum_d T_d.
Let m depend only on the zero/nonzero pattern, |m|<=1. In the correlation
for a fixed displacement d, partition coordinates by the two zero patterns
of e and e+d. The product conjugate(m(e))m(e+d) is constant on each cell.
At a coordinate with d_i!=0 the both-nonzero cell sums to zero; the only
surviving cells have e_i=0 or e_i=d_i. Summing their absolute contributions
gives 2|a_i(0)a_i(d_i)|=|2B_i(d_i)/q|<=beta.
At d_i=0 the corresponding summed contribution is sum_u |a_i(u)|²=1.
Thus the absolute correlation is <=beta^wt(d), even for nonradial complex
support masks. Therefore

    | ||A(ma)||² - ||ma||² | <= sum_(d!=0) beta^wt(d) <= eta,
    eta=(q^K-1) beta^(N-K+1).

The first bound may use the sharper MDS enumerator, but the stated coarse
bound suffices. The tail mask wt(e)>w is allowed and its ordinary mass is
delta=Pr[Bin(N,1/2)>w]. Its coherent image norm is <=sqrt(delta+eta).
This does NOT control arbitrary label-dependent or arithmetic-error vectors.
Such implementation errors should instead be bounded through the physical
circuit's trace-distance contractivity, without applying A to them.

## Complete decoding and the actual heralded state

Prepare |D|^(-1/2) sum_d |d> sum_e a(e)|e>. Measure only wt(e)<=w,
add d into the second register, compute the entire radius-w list for z=d+e,
and measure only the singleton flag. Translation invariance of the linear
code means singleton status depends on e's coset, not on the initial d.
Let U be the retained errors with singleton lists. Each coset contains at
most one U error. The decoded d equals the original d since that original
codeword is within the radius. XOR it away and uncompute all payload/history.
The unnormalized accepted register is exactly

    g(z)=|D|^(-1/2) sum_(d in D) a(z+d)1_U(z+d)=A(1_U a)(z).

The norm is ||g||²=Pr[e in U]; there is no hidden q^K herald penalty.
The decoder must run on unchanged z during uncomputation. A measured flag
can be cleaned on its accepted branch. Measuring the message, exact weight,
support, or root path instead would leave which-path information and break
this derivation. An incomplete list invalidates the singleton assertion.

Put v=Aa. Its inverse Fourier transform is

    F^(-1)v(x)=sqrt(|D|) 1_C(x) (2/q)^(N/2) prod_i 1_S_i(x_i).

Thus v has zero invalid-answer component, without assuming ||v||=1.
This also independently identifies ||v||²=q^K (2/q)^N |C intersect prod S_i|.

## Ambiguity, list size, and overall failure

Put a=N-w, t=a-K+1. If a wrong codeword lies in the retained list, it
agrees with e at >=a coordinates. It has at most K-1 zeros, hence >=t
nonzero agreements. If each nonzero source symbol has probability <=mu,
independence and a union bound yield

    epsilon <= min(1,(q^K-1) binom(N,t) mu^t).

This can overcount harmless events, but it includes every ambiguity. The
list cap follows by choosing a agreements per candidate and counting their
pairwise intersections:

    ell a²/N <= a+ (ell-1)(K-1),
    ell <= N(a-K+1)/(a²-N(K-1)).

Taking its floor gives L. Each retained coset has <=L errors. Cauchy–Schwarz
within each coset gives ||A(1_B a)||²<=L Pr[B]<=L epsilon for ambiguous B.
Consequently ||v-g||<=sqrt(delta+eta)+sqrt(L epsilon). Projection onto
invalid outputs, together with the rejected mass <=delta+epsilon, gives

    P[no valid answer in one ideal attempt]
      <= 3 delta+(2L+1) epsilon+2 eta.

Normalization after heralding is never used to drop probability. The
verifier checks all N trace bits and the K field equations, so no false
answer is accepted. Independent repetition amplifies bounded success.

## Decoder and bit complexity

For h=K-1>0, a²>Nh and s=floor(Nh/(a²-Nh))+1, weighted degree D0=sa-1
suffices. If u=sa=l h+r, 0<=r<h, the monomial count is

    h*l*(l+1)/2+(l+1)r
      = u²/(2h)+u/2+r(h-r)/(2h)
      > Ns(s+1)/2.

The final inequality follows from s(a²-Nh)>Nh>=h(N-a).
Canonical Gaussian elimination yields nonzero Q. At >=a agreements,
Q(X,f(X)) has >=sa roots counting multiplicity but degree <sa, so is zero.

Roth–Ruckenstein normalization makes Q(0,Y) nonzero. A root gamma of
multiplicity m gives, after Y=gamma+XY, a nonzero X^m Y^m coefficient;
the removed X valuation v is <=m. Every Y^r term carries >=r powers of X,
so the child's specialization degree is <=v<=m. Summing over roots bounds
the width by deg_Y Q and the node count by 1+K deg_Y Q. The substitution
is injective on nonzero polynomials; it cannot manufacture a zero Q node.
After K coefficients, test the complete formal identity, then the native
radius. No early zero-prefix rule is valid.

All field roots can be found deterministically: gcd(f,Y^q-Y), with n modular
squarings, followed by trace-basis splitting of the squarefree split factor.
The n trace coordinates separate every pair of field elements. Repeated
roots, zero roots and rootless factors are therefore covered with polynomial
degree/bit work. Normalize, sort, pad all slots and clocks. Classical
deterministic polynomial Boolean computation converts to reversible
compute-copy-uncompute with polynomial history storage. The proof does not
require the current Python implementation to be a physical quantum circuit.

At a fixed R=K/N<1/4, choose sqrt(R)<A0<1/2 and a~A0 N. Then A0>2R,
L,s,deg_Y Q are bounded constants, dense interpolation takes O(N³) field
operations, and RR depths/degrees are polynomial. With q=2^n, N=n²,
beta<= (1+2sqrt(q))/q and mu<=4/q, the three failure terms vanish:
delta=exp(-Omega(N)), epsilon=q^(-Omega(N)), eta=q^(-Omega(N)).
Exact Clifford+Toffoli-style reversible arithmetic and Hadamards suffice
in the ideal circuit model. A chosen noisy/approximate implementation would
need a total circuit-error budget; it is not evidence against polynomial
ideal complexity by itself. No practical cost advantage has been shown.

For clarity about the compact input, the modulus and N public n-bit points
take O(Nn) bits; the Vandermonde matrix is constructed and its O(NK) field
operations are charged. At fixed slack, the interpolation matrix has
O(N) rows and columns, and RR has constant Y degree, O(N) nodes and
O(N) X degree throughout. A conservative elementary Boolean upper bound
is O(N³*n³) for a padded deterministic decoder, allowing cubic-bit field
inversion. Reversible history storage may be of that same polynomial
order under the simplest compilation. This is an existence bound, not a
measured gate count, optimized implementation, or practical estimate.
For N=n² the bound is O(n^9), polynomial in the O(n³)-bit explicit input.
The comparator 2^K is exponential in N, but subexponential in that compact
input length; neither comparison establishes a separation from all
classical algorithms.

## Self-attack and current boundary

The proof depends critically on balance, signed amplitudes, the two masks
being support-only for the tail, complete decoding on *every* received word,
and erasing all work records. The ambiguity mask is label-dependent and is
handled by L, not by the support lemma. I find no gap in those transitions.
The standard Kloosterman constant and zero convention were subsequently
checked via the Artin–Schreier genus formula: 1/x+d*x has simple poles at
zero and infinity, genus one, and projective point count q+1+K(d). Thus
|K(d)|<=2sqrt(q) and W(d)=1+K(d). See `LITERATURE.md` for sources and scope.
Neither finite tests nor the absence of a discovered counterexample
establishes classical advantage.

The same estimates also show approximate uniformity on native solutions:
v/||v|| is their uniform superposition after inverse QFT. Put
d0=sqrt(delta+eta)+sqrt(L epsilon), p0=||g||². The normalized successful
herald state differs in Euclidean norm by at most 2d0/sqrt(p0), using
| ||v||-||g|| |<=d0. This bounds measurement TV as well. It does not provide
a classical sampler or a lower bound on classical sampling.

## Later shared update: independently audited full-list projection

At 11:23 UTC the recent priority section pointed to the newly resident
BALANCED_FILTER_CHANNEL_AUDIT.md. I reconstructed its new list projection
separately. This changes the reviewed construction's scope: low ambiguity
is sufficient for the original protocol but is no longer indispensable
for every variant.

Let B be the retained weight ball and P a fixed power of two at least the
maximum complete list size, with P<=q^K. Pad each list to P distinct message
labels. On a retained input (m,z), completeness ensures m is listed. Compute
its index j reversibly, clear m using lookup(j), apply Hadamards to j, and
herald only j=0. Uncompute the list from unchanged z. Every listed message
has the same positive accepted amplitude 1/sqrt(P), so the physical branch is

    h=A(1_B a)/sqrt(P).

The initial uniform-message factor remains 1/sqrt(q^K); there is no missing
normalization. A reversible index computation can clear its own temporary
work before erasing m. Padding finds enough unused labels among 0,...,P-1
in polynomial work and is not an enumeration of all q^K messages. The
fixed P, complete list and absence of surviving index/list records matter.

**Proved sharper bound.** Write g=A(1_B a), t=A(1_(B complement) a), and
v=g+t. The support-mask estimate directly gives

    ||g||² >= 1-delta-eta,    ||t||² <= delta+eta.

Since v is native-valid, Pi_invalid*g=-Pi_invalid*t. Therefore

    P[valid AND list herald] >= max(0,1-2*delta-2*eta)/P,
    P[invalid AND list herald] <= (delta+eta)/P,
    (1-delta-eta)/P <= P[list herald] <= (1-delta+eta)/P,

with the probability bounds clipped to [0,1] when needed. The shared note's
(1-2*delta-3*eta)/(2P) lower bound is valid but unnecessarily weaker: it
uses a triangle inequality where the direct ball norm already suffices.
No point-mass bound, ambiguity probability, or singleton assumption enters
these inequalities. This is a proof-level improvement, not a new circuit
run or a speedup claim. For the listed native budgets P=8, the sufficient
success approaches 1/8 per attempt rather than 1/16.

**Self-attack.** A branch-dependent P would weight different z differently;
an incomplete list could leave m nonzero; duplicated padding would defeat
the inverse lookup; a retained message or index destroys the asserted
coherent state. The exact state derivation above excludes each fault. The
stronger success bound follows from two inequalities already proved for
support masks, so its falsifier is an actual violation of that lemma or of
the physical branch identity, not finite list ambiguity by itself.

For a code with a complete polynomial-list decoder at the source's typical
weight, this yields a useful abstract theorem whenever the enumerator
E_D(beta)=sum_(d!=0) beta^wt(d) is small. Ordinary RS at fixed R<1/4 supplies
such a decoder here. It does not establish a better rate or a classical
separation. A new code/source pair would require its own input, source,
list-size, bit-complexity and classical-attack analysis.

## Implementation boundary checked by inspection

The current Python decoder has explicit degree/matrix caps and calls the
repository's field(bits) backend, rather than accepting an arbitrary supplied
modulus through its public function signature. The exhaustive channel
controls are also capped. Thus these files do not themselves implement the
entire asymptotic, arbitrary-modulus input contract. The standard field
arithmetic and deterministic decoder construction above do meet that
mathematical contract in principle. No unavailable backend was opened,
reconstructed, or imported, and no shared test artifacts were overwritten.
