# Polynomial Cosets Are Not Automatically Hidden Polynomial Graph Inputs

2026-10-22. Targeted prior-art and reduction audit. The new chart lemma is
a written argument under review, with exact algebraic controls. This is
NOT independent correctness verification of Rees, a novelty certificate,
a new quantum algorithm, or a no-go theorem against general reductions.

## 1. The Scientific Question And Decision

An order-p subgroup of a class-c Lazard group has cosets parametrized by
bounded-degree BCH polynomials. Does this alone make the proposed Rees
theorem a corollary of existing hidden-polynomial algorithms?

No such implication has been established. The established HPGP input
requires translates of ONE common graph, not arbitrary polynomial curves.
The source-dependent coefficients in a nonabelian normal factor cannot
be discarded as unknown additive offsets without proof.

This audit strengthens the old missing-interface observation in
CLASS_THREE_HSP_THEOREM_DRAFT.md in two specific ways:

1. A public fibre-preserving injective coordinate recoding can cover only
   an abelian coset of transverse hidden-subgroup parameters. For an
   explicit class-three family this is a tight p^(-m) coverage fraction.
2. Tracing out a public quotient-kernel register need not produce the
   hidden subgroup's image state. A growing-prime family of actual mixed
   sources loses almost all of the desired Fourier-support probability.

Neither result excludes an adaptive, collective or otherwise different
HPGP reduction. A separate bound below also addresses approximate graph
states produced by a single fixed chart. The goal is to distinguish the
actual proposed state-conversion contribution from ingredients already in the literature,
not to certify novelty by eliminating two shortcuts.

## 2. What The Inspected Papers Actually Supply

[Ivanyos--Santha, 1503.09016, Definition of HPGP-prime, Corollary 6,
Proposition 7, Sections 4.1 and 5](https://arxiv.org/pdf/1503.09016)
solve fixed-degree vector-output univariate graph learning from states
of the form

```
p^(-1/2) sum_t |t>|u+Q(t)>,
```

where the SAME Q occurs across copies and u is a fresh unknown offset.
Output dimension may grow. Fourier measurement removes u as a global
phase, leaving public coefficient maps multiplying fixed hidden parameters.
The paper explicitly reduces abelian-normal-by-cyclic p-groups to this
input. The SDE solver and final phase elimination are already known.

[Decker--Ivanyos--Santha--Wocjan, 1107.2189, Theorem 5 and Section 5.3](https://arxiv.org/pdf/1107.2189)
extend scalar-output multivariate HPGP via chosen oracle restrictions.
They require a level-set promise y-Q(x). An arbitrary unknown coset state
does not supply those chosen restrictions. This is not a lower bound on
other ways of obtaining them.

[Decker--Draisma--Wocjan, 0706.1219, Definition 2.1, Remark 2.2 and
Lemma 2.4](https://arxiv.org/pdf/0706.1219) use "hidden polynomial problem"
for a GRAPH restriction in that paper. Their stated efficient regime fixes
both degree and variable count; the displayed recursive interpolation uses
1+d+...+d^(m-1) univariate calls. That particular bound is not polynomial
in growing m, and must not be confused with the later improved graph result.
Nor is this a lower bound on other multivariate algorithms.

[Decker--Hoyer--Ivanyos--Santha, 1305.1543, Theorems 1 and 2](https://arxiv.org/pdf/1305.1543)
separate two input contracts: translated univariate graph copies, and an
oracle for E(g(y)-f(x)) with known g and fixed degrees. Their bivariate
level-set algorithm, including its curve examples, does not assert a
solver for arbitrary growing-dimensional vector-output BCH coset varieties.
Calling every polynomial coset a "hidden curve" does not supply either
contract. Generalizing these algorithms remains possible, but requires
an actual reduction or a new algorithm with its full resource analysis.

The search and these inspected definitions do not establish that ALL
prior work fails to subsume Rees. No global novelty flag should change.

## 3. Exact Public-Chart Model

Let G=N semidirect C_p be exponent p, with a public order-p lift r of the
cyclic quotient. Use the unique normal form n*r^t. For each v in N,

```
H_v = <v*r>,       (v*r)^t = v_t*r^t.
```

Every H_v is order p and transverse to N, and distinct v give distinct
subgroups: there is exactly one member of H_v at quotient coordinate1.
Its left cosets are {n*v_t*r^t : t in F_p}, indexed by n in N.

Consider a fixed public basis recoding

```
(t,n) -> (t,phi_t(n)),
```

where each phi_t is injective into an additive abelian output group.
It may be nonlinear, depend on t, use extra output coordinates, and have
unbounded computational power. It must not depend on the hidden v.
Allowing an abelian group rather than just F_p^M strengthens the statement.

Call v GOOD when all its cosets become translates of a single graph:

```
phi_t(n*v_t) = phi_0(n)+Q_v(t)    for every n,t,   Q_v(0)=0.
```

We impose no degree bound on Q_v. Thus failure in this relaxed model
also excludes the standard fixed-degree HPGP promise for this chart.
This defines EXACT success. Section 4 also gives a separate approximate
state bound; it is not inferred merely from failure of exact recoding.

## 4. Good Parameters Lie In An Abelian Coset

**Lemma.** For any fixed chart, its good set S is contained in one coset
of an abelian subgroup of N. In particular |S| is at most the order of
a largest abelian subgroup of N.

**Proof.** There is nothing to prove if S is empty. Choose v0 in S and
write q_v=Q_v(1). The t=1 equations for v and v0 imply, for every n,

```
phi_0(n*v*v0^-1) = phi_0(n)+(q_v-q_v0).
```

Thus right multiplication by each u=v*v0^-1 acts as translation in the
phi_0 coordinates. Two such translations commute. Applying their two
orders to any n, then using injectivity of phi_0, gives u*w=w*u.
All these elements generate an abelian subgroup A, and S is contained
in A*v0. This proves the bound. Only t=0 and t=1 were used.

As a corollary, a chart good for EVERY v requires N itself to be abelian.
More locally, if the chart is good for 1,a,b then a,b must commute.
The executable verifies this second statement by an INTEGER combination
of eight formal equations E(n,v)=phi_1(n*v)-phi_0(n)-q_v. They reduce to
phi_0(b*a)-phi_0(a*b), without choosing numerical output labels. This is
stronger than testing one unlucky coordinate convention, but narrower
than a theorem about arbitrary quantum transformations.

For K fixed charts, a union bound covers at most K times the maximum
abelian order. For a chart drawn randomly INDEPENDENTLY of hidden v,
the average exact-promise success over uniform v has the same one-chart
bound. This allows some special v to be easy. It does not cover charts
chosen using previously learned hidden-subgroup information.

### Approximate Charts: A Separate Stability Bound

The t=0,1 proof alone is insufficient for approximation: those two fibres
have small amplitude when p is large. The following argument averages ALL
time pairs and closes that particular gap.

For a finite group N let cp(N)=Pr_(u,w)[u*w=w*u]. For any two injective
maps f,g:N->B into an additive abelian group define

```
M(u) = max_a Pr_n[f(n*u)-g(n)=a],
delta = 1 - average_u M(u).
```

**Agreement lemma.** delta >= (1-cp(N))/8.

To prove it, choose maximizers a_u and a parameter u0 whose error is at
most delta. Comparing the equations for (n,u) and (n*u*u0^-1,u0) gives

```
g(n*w)=g(n)+b_w,     w=u*u0^-1,  b_w=a_u-a_u0,
```

with average error at most2*delta over uniform n,w. Applying this relation
twice in the order w,z and twice in the order z,w uses four equations.
Their union failure probability is at most8*delta: each base point remains
uniform under translation, and no independence of failures is needed.
If all four equations hold, injectivity forces w*z=z*w. Consequently
1-cp(N)<=8*delta. This proves the lemma without computational assumptions.

Now let tau_v be the recoded mixed H_v coset source. For any function Q_v,
let P_Qv project onto the span of its full graph-offset states. It accepts
any valid mixture of those graph states with probability one. Directly
expanding the density gives

```
Tr(P_Qv tau_v)
 = Pr_(n,s,t)[phi_t(n*v_t)-Q_v(t) = phi_s(n*v_s)-Q_v(s)].
```

For s!=t, reparameterize n*v_s as the uniform base point. The corresponding
tail multiplier is v_s^-1*v_t = alpha_s(v_(t-s)), where alpha is conjugation
by r. As v ranges uniformly over N, this multiplier is uniform over N:
in an exponent-p group, raising to the nonzero power t-s bijects quotient
slice1 with slice(t-s), and alpha_s is an automorphism. Thus the agreement
lemma applies to each ordered unequal pair s,t. It even allows an optimal
additive difference for each v and pair, a relaxation of choosing ONE Q_v.
Equal times contribute1. Averaging yields

```
average_v Tr(P_Qv tau_v)
 <= 1 - (1-1/p)*(1-cp(N))/8.
```

The graph-support projector is also a distinguishing measurement, so for
ANY chosen valid graph-state mixture sigma_Qv,

```
average_v trace_distance(tau_v,sigma_Qv)
 >= (1-1/p)*(1-cp(N))/8.
```

The target graph can depend arbitrarily on v in this comparison. Therefore
the bound is not a consequence of choosing an inconvenient polynomial.
For the family below, cp(N^m)=(2/p^2-1/p^4)^m, giving a constant lower
bound approaching1/8 as p grows. Some hidden subgroups are still represented exactly.
This is a single-fixed-chart, average-over-hidden-parameters statement,
not a lower bound on arbitrary quantum algorithms, adaptive charts, or
multi-copy state conversion. It is a local proof under review, not an
independent theorem certification.

## 5. A Tight Fixed-Class Family

Inside UT4(F_p), p>3, let N=ker(x12), and write its coordinates as
(b,d,c,e,f)=(x23,x13,x34,x24,x14). Multiplication is

```
(b,d,c,e,f)*(B,D,C,E,F)
  = (b+B, d+D, c+C, e+E+b*C, f+F+d*C).
```

The center has coordinates e,f and order p^2. On N/Z the commutator is

```
[(b,d,c),(B,D,C)] = (b*C-B*c, d*C-D*c).
```

If an abelian subgroup projects to a space containing a vector with
c!=0, these equations force every projected vector to be proportional
to that vector, so its projection dimension is at most1. Otherwise its
projection lies in the two-dimensional c=0 plane. Hence its order is
at most p^4. The subgroup A={c=0} attains p^4. This uses only the
additive quotient and exact commutators, not a guessed numerical scaling.

Take N^m and let one common C_p generator r act by conjugation with
I+E12 in every block. The resulting G_m has order p^(5m+1), exponent p,
and nilpotency class3. It embeds into UT4(F_p)^m with all x12 entries
equal. Its largest abelian subgroup INSIDE N^m has order p^(4m): projections
of an abelian subgroup onto the factors are abelian, and A^m attains the
product bound. Therefore

```
one fixed chart:          |S|/|N^m| <= p^(-m),
K fixed charts:           covered fraction <= min(1,K/p^m),
complete chart coverage:  K >= p^m.
```

For completeness, count commuting pairs in the three-dimensional quotient.
The zero vector commutes with p^3 partners; each of the p^2-1 nonzero
c=0 vectors has p^2 partners; each of the (p-1)*p^2 vectors with c!=0
has p partners. Dividing their total 2p^4-p^2 by p^6 gives
cp(N)=2/p^2-1/p^4. Independent factors multiply commuting probabilities.

This is exponential in the natural (5m+1)*log(p) coordinate width as
parameters grow. It is a bound on this class of recodings, not query,
sample or gate complexity for the HSP.

The bound is tight. In the displayed coordinates, for v=(b,d,c,e,f),
the N component of (v*r)^t is

```
(t*b,
 t*d + choose(t,2)*b,
 t*c,
 t*e + choose(t,2)*b*c,
 t*f + choose(t,2)*(e+d*c) + choose(t,3)*b*c).
```

Every coset is indeed a cubic polynomial curve. When c=0 its N component
lies in A and right multiplication simply adds it to ANY coset offset n.
The raw chart therefore gives a common degree-two graph for all v in A.
When c!=0, the e,f slopes additionally contain t*c*b_n and t*c*d_n,
which depend on the unobserved offset n. They are not global phases or
fixed hidden coefficients shared across independently drawn sources.

The same argument blockwise gives exactly the fraction p^(-m). Thus it
both preserves the legitimate known-HPGP cases and identifies the failed
generalization. The code verifies the cubic formula by independent matrix
powers, including a127-bit prime, and the good c=0 cosets exhaustively
only at p5. Large-prime powering uses a binary loop, not enumeration or
the machine-integer-limited FLINT exponent wrapper.

## 6. Why Discarding The Normal Factor Is Not A Free Repair

One might first replace N by its abelianization and then invoke the known
semidirect-product result. Doing so requires converting rho_H into
rho_(HK/K), where K is a suitable normal subgroup. It is not a change of
classical names. The copy-only transport in REES_COPY_ONLY_OUTER_REDUCTION.md
authorizes a straightforward quotient when a KNOWN K is contained in H.
An arbitrary commutator subgroup does not satisfy that premise.

For a public section s:G/K->G, encode g=s(q)*k and trace the k register.
The output is

```
rho_out[q,r] = (1/|G|) sum_(k in K)
               1_H(k^-1 * s(r)^-1*s(q) * k).
```

The desired quotient state instead has entry
1_(HK)(s(r)^-1*s(q))/|G/K|. Normality of K alone does not equate these.

**Quantitative example.** In UT3(F_p) with coordinates (a,b,z), take
H={ (t,t,t^2/2) }, K=Z(G), and s(a,b)=(a,b,0). Here K intersect H is
trivial. Trace the center of the actual mixed coset density, not a guessed
pure branch. For t=a-A=b-B, the retained off-diagonal entry is nonzero
only when -A*t=t^2/2; when t!=0 this says A=-t/2.

Within each of the p quotient-line blocks, the normalized output is

```
sigma = (I + S - |0><0|)/p,
```

where S reflects a to -a. The desired block is the uniform rank-one
projector. Hence the probability in the desired quotient Fourier support
is exactly (2p-1)/p^2, versus1 for a correct quotient source. Trace distance
is at least 1-(2p-1)/p^2, approaching1 as p grows. This is not a finite-fit
extrapolation. The dense p5 and p7 controls construct literal right
translation matrices, form rho_H, actually trace the register, and measure
the desired support projector. At p5 the mass is9/25 and the trace
distance is about0.6472, above the exact lower bound16/25.

This does not exclude central erasure using several copies, a different
costed section-dependent protocol, or another legal quotient construction.
It explains why such a construction remains substantive work.

## 7. What Could Prove This Audit Wrong Or Make It Irrelevant

- Exhibit a promised fixed chart violating the abelian-coset lemma. Check
  injectivity, the SAME chart for all hidden v, and ALL coset offsets.
- Exhibit a known theorem accepting variable source-dependent coefficients
  with their exact access model; update the comparison, not the theorem's
  premises. A genuine reduction would settle the prior-art question more
  strongly than the current negative chart result.
- Produce an adaptive, collective, non-fibre-preserving, or oracle-based
  conversion with polynomial full cost. None is excluded here. Approximation
  alone within the same fixed-chart model faces the separate stability
  bound, but approximate protocols outside that model remain open.
- Publicly learning part of H before choosing a chart is legitimate if
  that learning step is supplied and charged. It is not a counterexample
  to the fixed-chart lemma.
- Arbitrary polynomial-curve learning, chosen restrictions, repetitions
  of a selected unknown coset, and quotient erasure are not free inputs.
- A failure of these two shortcuts does NOT establish Rees correctness,
  novelty, a natural application, or a quantum speedup.

The proposed Rees cover plus complete central instrument explicitly
changes and combines source states. It is outside the chart lemma's
scope. The full composition remains the object requiring independent
review. No new candidate or central negative-result record is admitted.

## 8. Reproduction

```
python -m pytest tests/test_hpgp_coset_interface.py -q
python -m theorems.hpgp_coset_interface --write
```

The live artifact is research/reductions/hpgp_coset_interface.json.
For p43,m8, even1000 fixed charts cover at most
1000/11,688,200,277,601 of uniform transverse parameters. This is an
analytic certificate, not an executed enormous-group search.
