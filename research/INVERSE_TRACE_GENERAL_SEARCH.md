# Arbitrary-Target Native Search Has A Classical Polynomial Algorithm

30 October 2026. Mathematical deduction importing published/preprint
theorems; independently checked by automated reviewers, not human peer
reviewed, Lean verified, or a novelty claim. This supersedes the earlier
statement that arbitrary-target SEARCH remained open within this project.
It does not settle uniform native witness SAMPLING.

## Statement And Exact Input

Let n be odd, n>=61, q=2^n, N=n^2, K=floor(N/8), and let alpha_i be
ANY N distinct public elements of F_q in an explicit polynomial basis.
For ANY public bits b_i, an expected-polynomial classical algorithm finds
x in F_q^N satisfying the ORIGINAL relation

```
sum_i alpha_i^j*x_i = 0  (0<=j<K),
Tr(inv0(x_i)) = b_i,    inv0(0)=0.
```

The algorithm uses deterministic balancing, two independent genus-zero
norm searches, and disjoint assembly. It does not change targets, discard
one-target constraints, reduce the original K, or obtain hidden advice.
The polynomial guarantee charges field construction/arithmetic, polynomial
factorization, random sampling and verification. Expected-polynomial
finite-field factorization and independent uniform random bits are used.
The O(n^6) bound below counts proposals, not total bit operations.

Classical search hardness cannot support a superpolynomial quantum search
separation on this native sequence. Polynomial quantum improvements are
not ruled out by this result.
The large conservative threshold and trial bound are not performance
predictions. A capped seeded implementation can still return UNKNOWN.

## 1. Deterministically Split Into Two Trace-Affine Blocks

Put B=sum_i(-1)^b_i and T(c)=sum_i(-1)^(b_i+Tr(c*alpha_i)). Character
orthogonality and distinct points give

```
E_(c!=0) T(c)^2 = (q*N-B^2)/(q-1) < N+1  (n>=5).
```

Find a nonzero functional with no larger square by conditional expectation,
without enumerating F_q. In coordinate bits, fix a low-t-bit prefix p of
a linear functional u. Let R=2^(n-t), delta=1_(p=0), and

```
S_h = sum_(alpha_i >> t = h) (-1)^(b_i+popcount(p & alpha_i)).
Q_t(p) = [R*sum_h S_h^2 - delta*B^2]/[R-delta].
```

This is exactly the mean square over all nonzero completions of p.
It follows by character orthogonality on the remaining coordinates;
the subtraction removes u=0 when that completion exists. Skip an empty
child, otherwise choose the child with smaller rational Q. The parent is
the completion-count-weighted average of its children, so Q cannot grow.
After n steps u!=0 and Q=T^2. There are O(nN) occupied-bucket updates
with polynomial-size integers. Sorted scans can replace dictionaries if
a worst-case implementation bound for the container is desired.

Solve Tr(c*e_j)=u_j in the ORIGINAL basis. The trace pairing is
nondegenerate, hence c!=0. Do not identify the bit encoding of u with c.
The integer T satisfies |T|<=n. Partition indices according to
b_i XOR Tr(c*alpha_i), with offsets d0=0 and d1=1 (odd n). Thus each
block has trace-affine targets and size

```
(N-n)/2 <= M <= (N+n)/2.
```

Each block retains ALL K original parity checks. Assemble the two block
words on their disjoint coordinates. Their syndromes add to zero and
their targets cover all original coordinates exactly once. Empty or
all-zero-target blocks can use the zero word directly. No such shortcut
is required for the asymptotic proof.

## 2. Exact First Moment On A Shorter Block

Use the algorithm, normalization and divisor second moment in
[INVERSE_TRACE_GENUS_ZERO_NORM.md](INVERSE_TRACE_GENUS_ZERO_NORM.md), with
block length M and unchanged K. Put

```
r=M-K-1, e=2r+1, s=M-2K-1,
P=prod_(i in block)(X-alpha_i), D=P',
F=(D^2 mod P)+P*T,  T uniform monic of degree s.
```

Let R(F) be the number of normalized lifts
U^2+U*A+(cX+d0)*A^2=F, deg U<=r, deg A=r, A_r=kappa=c^(-1/2).
Let J(F) count those with A(alpha_i)!=0 at every one-target. Local
coordinates a_i=A_i/D_i, v_i=U_i/D_i satisfy
v_i^2+a_i*v_i+C_i*a_i^2=1, C_i=c*alpha_i+d0. The exact local transform is

```
q*1_(xi=zeta=0) + psi(C_i)*Kl(xi^2+xi*zeta+C_i*zeta^2)
                 - b_i*psi(zeta),
Kl(t)=sum_(z!=0) psi(z+t/z),  psi(t)=(-1)^Tr(t), Kl(0)=-1.
```

The deletion term excludes (a,v)=(0,1) only at one-targets. Weighted
interpolation gives sum alpha_i^j*a_i=0 for j<K and =kappa for j=K;
v has only the j<K constraints. Therefore, exactly,

```
E J = q^(-M) sum_(deg p<=K, deg g<K) psi(kappa*p_K)
      prod_i [q*1_(p_i=g_i=0)
              +psi(C_i)*Kl(p_i^2+p_i*g_i+C_i*g_i^2)-b_i*psi(g_i)].
```

The q^(-(2K+1)) constraint normalization, divided by q^s proposals,
is q^(-M). There are no missing D_i factors in this expression.
The zero dual frequency contributes exactly (1-1/q)^z, where z counts
zero-targets. The earlier pointwise Fourier bound loses too much when
M is about N/2. The following short-sum estimate repairs that loss.

## 3. Imported Trace-Sum Bound And Its Hypotheses

[Sawin--Shusterman, arXiv:2512.24080v1, Theorem 1.3, Section 4](https://arxiv.org/pdf/2512.24080v1)
proves, for L distinct evaluation
points and 1<=k<=L, that suitable normalized local trace functions obey

```
|sum_(deg f<k) prod_i t_i(f(alpha_i))|
 <= q^((k+1)/2) [Z^k] prod_i (r_i+(r_i+cF_i)*Z)
 <= q^((k+1)/2) B^L,  B=max_i(2*r_i+cF_i).
```

The explicit sqrt(q) and growing-L constant come from the proof, not
an unspecified big-O constant. This theorem removes the multiplicative
character requirement in the older trace-sum theorem. Do not substitute
that older theorem here. The modulus is the product of the L distinct
linear factors. Required sheaf properties and their checks for
t(x)=q^(-1/2)*Kl(x^2+zeta*x+C*zeta^2) are:

- Rank-two Kloosterman middle extension, normalized by q^(-1/2) and
  a constant arithmetic sign twist, has nonpositive weights. Its trace
  at argument zero is -q^(-1/2), not zero. Extension by zero is WRONG.
- For zeta!=0 the quadratic map is a connected finite etale double
  cover away from its zero fibers. Restricting connected geometric
  monodromy SL_2 to a finite-index subgroup retains SL_2. Thus there
  are no constant or rank-one Artin--Schreier constituents.
- For zeta=0 it is Frobenius pullback; the etale-topos equivalence
  preserves irreducibility, and Kl(x^2)=Kl(x) over all finite extensions.
- At infinity the base breaks are 1/2. For zeta!=0 the local extension
  y^2+y=t/zeta^2+C has ramification break 1. Its inverse Herbrand map
  is u for u<=1 and 2u-1 for u>=1; restriction keeps breaks <=1/2.
  DO NOT apply a prime-to-characteristic tame pullback formula here.
- The middle extension has no finitely supported sections. Its finite
  singularities are tame with drop one at each of at most two geometric
  roots. The Fourier conductor equals the finite conductor because all
  infinity breaks are <=1. Hence cF<=2 and 2r+cF<=6. We conservatively
  use B=8 throughout, including after nonzero affine changes of x.

Sources for these checks:
[Katz, Gauss Sums, Kloosterman Sums, and Monodromy Groups, 4.1.1--4.1.2, 7.4.3 and 11.1](https://web.math.princeton.edu/~nmk/Katz-GKM.pdf);
[Sawin--Shusterman, arXiv:2008.09905, Definition 3.8 and Lemma 3.10](https://arxiv.org/pdf/2008.09905);
[Thomas, Proposition 2.1, Artin--Schreier ramification](https://www.numdam.org/item/10.5802/jtnb.514.pdf).

These geometric hypotheses were independently audited by Franklin.
The theorem is used ONLY on the Kloosterman terms, not on the delta or
constant deletion terms of the full local coefficient.

## 4. Expand Before Applying The Theorem

Expand the local product into delta, Kloosterman and deletion choices.
Let T index the delta choices, t=|T|, and ell count Kloosterman choices.
For t>=K+1, the delta constraints force p=g=0. For t<=K write
p=P_T*p_tilde, g=P_T*g_tilde and k=K-t. There are q^k choices of g_tilde.
Fix the leading coefficient of p_tilde (q choices). The remaining
coefficients are a degree-<k polynomial. P_T(alpha_i)!=0 outside T,
so its appearance is an allowed nonzero affine change of the local
trace variable. The deletion factors and psi(kappa*p_K) are now constant
in the lower coefficients of p_tilde.

For 1<=k<=ell, the entire expansion term is bounded by

```
q^(t-M) * q^k * q * 8^ell*q^((ell+k+1)/2)
 = 8^ell*q^((3K-t+ell+3-2M)/2)
 <= 8^M*q^((3K+3-M)/2).
```

For k=0 or ell<k, count all p,g and use |Kl|<=2sqrt(q). The bound is
2^ell*q^(t+2k+1+ell/2-M), which is at most the same displayed upper
bound when M>=2K+1. These cases do not invoke Theorem 1.3.
There are at most 3^M expansion choices.

To remove the zero dual frequency from t<=K terms, FIRST regroup their
non-delta choices: -psi(C_i)-b_i equals -1 at zero-targets and 0 at
one-targets. If w=M-z the correction is exactly

```
q^(-M) sum_(t=w..K) binom(z,t-w)*(-1)^(M-t)*q^t,
```

with an empty sum when w>K. Its magnitude is at most 2^M*q^(K-M).
Taking absolute values before this regrouping would lose that constant.
Combining terms gives the useful absolute first-moment bound

```
|E J-(1-1/q)^z| <= epsilon,
epsilon = 2*24^M*q^((3K+3-M)/2).                         (1)
```

Planck independently verified the identity, expansion, exceptional cases,
zero-frequency regrouping and constants. Small exhaustive enumeration is
a regression check only, not the justification for the geometric import.

## 5. Acceptance, Native Threshold And Runtime

Use the SAME second moment as the earlier norm proof. Write H=binom(e+3,3),
C1=(4^M-binom(M+3,3))*binom(3M-4,s), C2=4^(M-1)*binom(3M-3,s+1).
[Sawin, arXiv:2102.09730, Lemma 8.7](https://arxiv.org/pdf/2102.09730#page=59) yields

```
E R^2 <= B2=(q/(q-1))^M*H+2*C1*q^(-s/2)+2*C2*q^(-(s-1)/2).
```

This uses the original squarefree modulus P, invertible residue D^2,
and d_4(F) majorant; there is no extra scalar multiplicity. Sample every
norm allocation uniformly, including repeated-factor interior allocations.
Then Pr[valid output]=E[J/R], taking J/R=0 when R=0, and

```
Pr[valid output] >= (E J)^2 / E R^2.
```

For odd n>=61, N=n^2, K=(N-1)/8 and balanced M, elementary estimates
log2(24)<5 and M>=(N-n)/2 give

```
log2(epsilon) <= [16+(44-n)*N-19*n]/16 <= -N.
```

The coefficient of M is negative for n>=11. At n=61 the displayed
upper bound is -4025, below -N=-3721; it decreases thereafter.
The combined divisor error is at most

```
2^(5M+1)*q^(-(s-1)/2),
log2(error) <= [8+(22-n)*N-13*n]/8 <= -N.
```

Therefore E J>=1-M/q-2^(-N)>1/2. Also (q/(q-1))^M<4/3 and the
divisor error is <1, so B2<2H. Each block succeeds with probability
greater than 1/(8H) per independent trial. Keep a successful block while
retrying the other: expected proposals ADD, at most 8(H0+H1)=O(n^6).
All degrees are O(n^2), field encodings have n bits, and each proposal
uses polynomial work with expected-polynomial factorization. Success is
always checked against the full original input. This is a Las Vegas
search algorithm, not deterministic runtime or a uniform witness sampler.

## 6. Implementation, Finite Controls And Falsifiers

- `theorems/inverse_trace_affine_partition.py`: exact reduction, original
  verifier, deterministic balancer, fixed seeds/caps and retained failures.
- `theorems/inverse_trace_short_sums.py`: integer/rational certificate
  for (1) and the second moment; no floating-point acceptance decisions.
- `inverse_trace_singleton_subinstance_n17.json`: one original target
  equal to one, M145 subinstance, SAME K36, witness after 2 proposals.
- `inverse_trace_sparse_partition_n17.json`: fixed 18-one pattern,
  blocks139/150, SAME K36, witnesses after23/13 proposals.
- `inverse_trace_partition_matched_flats_n17.json`: the existing d3
  flat attack also solves BOTH exact original instances, with independent
  binary verification, in about0.6s each on this machine. These finite
  examples are NOT difficult classical benchmarks or quantum evidence.

The old pointwise bounds are inconclusive for those short n17 blocks.
The new theorem is not proved by those runs; no n61 factorization campaign
was executed. The singleton zero-extension escapes a scoped high-genus
full-support proposal obstruction, not its valid statement or all samplers.

Decisive falsifiers: an incorrect zero-stalk convention, a forbidden
rank-one constituent, infinity break>1, a hidden growing-degree constant,
lost deletion/zero-frequency term, factor allocation bias, or charging
neither rejected proposals nor factoring. Every such step is exposed
above. The two new independent reviews found no fatal gap in their
complementary scopes; formal verification and expert review remain absent.

Research consequence: deprioritize arbitrary-target native SEARCH as a
quantum advantage target. The ideal coherent construction may still
uniformly sample the full witness set, but a classical sampling separation
or useful native application has not been proved. Biased classical search
does not automatically dequantize sampling. Nor is failure of this
particular norm sampler a lower bound against all classical samplers.
