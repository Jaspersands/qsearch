# Induced-Source End-To-End Resource Audit

2026-10-22. Conditional mathematical argument and exact arithmetic
certificate. NOT an executed receiver, a single end-to-end Lean theorem,
a novelty certificate, or an admitted speedup.

Later refinement: AMBIENT_FILTERED_INDUCED_RECEIVER.md uses the ACTUAL
ambient lower-central filtration, coordinate-specific potential degrees
and component-separated full Taylor jets. It reduces weighted degree kc
to c and supplies a separate exact schedule. For the c9/k4 witness the
query ceil-log2 bound becomes4496 at p43 instead of333018. The uniform
support theorem here remains a conservative comparison; do not lower its
degree guard without implementing the filtered coordinates and transport.

## Verdict

The new right-fiber route has a fixed-class polynomial resource argument
under explicit source, transport and implementation contracts. This audit
found no additional exponential dependence on log(p) in the cited SDE
dependency. It does not close the general Lie-to-compiler refinement or
the complete adaptive receiver implementation. Its sufficient constants
are enormous. A lower upper bound is not a faster implemented algorithm,
and certainly not evidence of a useful application.

The old quadratic resource certificate was insufficient for this route.
The new contribution is a source-specific, higher-degree support theorem
and a separate exact schedule. Reusing a generic weighted-degree bound
alone would not justify its smaller equation counts.

## Input And Access Contract

Fix ambient nilpotency class c and normal class bound k, with
2<=k<=floor(c/2). Supply an explicit n-dimensional Lie algebra L/F_p,
N=L' metabelian, class(N)<=k, and p>kc. Public structure constants must
satisfy the Lie identities and the stated class and derived-series
conditions. The certificate does NOT establish these conditions merely
from dimension integers. It can accept hypothetical dimension envelopes
that need not be realized by an algebra.

The input oracle is the ordinary coherent, deterministic-label hiding
oracle for left cosets gH in exp(L), with unique public Lie coordinates.
Count each invocation and charge its output register length. There is no
hidden-potential evaluator, subgroup-state oracle, quantum RAM, character
nonresidue oracle, or full-table preprocessing of F_p. The conclusion is
relative to this oracle, not a claim about every explicit function whose
level sets happen to be cosets.

For one transverse call, H intersect exp(N)=1. Choose a PUBLIC abelian
ideal N'<=I<=N and a linear complement A, with dimensions b and r.
Let m=dim(L/N), D=c. The right chart is r(x)exp(i), not exp(i)r(x).
The proof-only potential Q(q) has degree <=D in every component. Its
coefficients are formal variables shared across every leaf of this call.
Neither those coefficients nor the hidden support U enter the controller.

## Higher-Degree Source Support

Write Q=A0+B0, X=s(x). The actual cocycle is

```
kappa(Q,x) = log(exp(-A0-X) exp(A0+B0) exp(X)).
```

It is a polynomial of total degree <=k in Q,x. Each Lie word with two
I inputs vanishes: at their lowest common ancestor both branches lie in
the ideal I, and [I,I]=0. Hence at most one B0 coefficient occurs in a
nonzero term. Setting B0=X=0 gives the identity, so every pure-A0 term
requires a carrier factor; its Q degree is at most k-1. Setting Q=0 also
gives the identity, so there are NO parameter-free terms.

Replace each Q component by its formal degree-D polynomial in q. Apply
the public affine carrier alignment, fixing the measured spectators.
For a monomial of parameter degree h the resulting phase satisfies

```
1 <= h <= k;
at most one I parameter;
pure-A parameter terms have h < k;
total q degree <= hD;
total retained-jet degree <= k-h.
```

The actual Taylor pullback is (q,t)->(Y+s*q,Z+A(Y,s)*t). It does not mix
q into t or t into q, and introduces no hidden parameters. Therefore it
preserves all these bounds, including after constants lower degrees.
Phase merging ADDS pulled-back phases; it does not multiply them.
The bounds consequently hold inductively at every weighted node and
every measured outcome. This is a written polynomial argument, not a
new Lean derivation from the general Lie chart.

The existing public compiler now enforces the separated bounds. A new
negative control replaces t_weight2 by t_weight2+q: that substitution
preserves the old weight bound but violates this source support. It must
not be accepted as a transport for the sharper resource certificate.

This envelope deliberately does not exploit the extra identities when
I=N', or the degree improvement available from including the full center.
The baseline degree remains D=c, not c-2.

## Count The Equations Actually Needed

Put hA=r*binom(m+D,m), hI=b*binom(m+D,m). For each h=1,...,k the number
of supported parameter monomials is bounded by

```
H_h = [h<k] binom(hA+h-1,h) + hI binom(hA+h-2,h-1).
sum_h H_h = (1+hI) binom(hA+k-1,k-1) - 1.
```

A jet variable of weight j has multiplicity
n_j=r*binom(m+D-j,m), 1<=j<=D. The coefficient of u^t v^w in
product_j (1-u*v^j)^(-n_j) counts jet monomials of total degree t and
weight w. A finite exact dynamic program computes these coefficients.

Let C_w(Q,T) count q/jet monomials of exact weight w, q degree <=Q and
jet degree <=T. Multiply each jet coefficient at weight w' by
binom(m+w-w'-1,w-w'), retaining 0<=w-w'<=Q and t<=T. Then use

```
Ew_w = sum_(h=1..k) H_h C_w(hD,k-h),  1<=w<=kD;
Eo_j = hA binom(m+j-1,j),             1<=j<=D.
```

The second line follows because the negative curve Fourier readout
introduces only eta.F(q), linear in the A-potential coefficients.
Public affine ordinary pullbacks preserve that linearity. A constant
phase is irrelevant; no parameter-free nonconstant phase is introduced.
The counts may include impossible coefficient/physical-monomial pairs,
which is safe overcounting, not an independence assumption about Q.

Coefficientwise cancellation is over these formal parameter monomials.
It is sufficient to cancel for all possible hidden values and never
requires learning those values. The diagonal relation is chosen before
the new shear outcomes: the leading weighted action is scaling by s^w,
independent of the new lower-weight offsets.

## Solver And Finite Schedule

Use a_1(E)=E+1 and

```
a_j(E) = [j^(j(j-1)/2) (E+1)^j]^ceil(log2(j+1)), j>=2.
```

This is the conservative all-input construction of
[Ivanyos--Santha, Theorem 11 and Section 3.3](https://arxiv.org/pdf/1503.09016).
Their Section 3.1 avoids a supplied nonresidue by classifying encountered
elements in a growing subgroup; only the fixed degree is factored, not
p-1. General degrees reduce to gcd(j,p-1). Thus the dependency is uniform
in log(p). The repository's executable g<=2 subset is not this solver.
Returned-witness verification alone would not establish all-input success.

Stages run in order weighted kD,...,1, then ordinary D,...,1, with their
own E values above. For target epsilon use

```
t = m + ceil_log_p(4/epsilon)
M = t * product(all stage arities)
ell = binom(m+D,m+1), J = r*ell
B = (ell+1)*bit_length(p)+2
a = ceil_log_p(8B)
R = ceil_log_2(4M/epsilon)
Qraw = M*R*B
Sdraw = Qraw*a
Bbinary = ceil_log_2(8Sdraw/epsilon).
```

The rank feature row divided by its nonzero scale consists of all
monomials in (s,Y) of degree <=D-1. Since p>kD>=2D, the root fraction
on F_p^* x F_p^m is <1/2. A union bound over fewer than p^ell relations
with B rows gives rank failure <=1/(4p). All Fourier labels, including
zero, are retained. Uniformity of the new outcomes is conditioned on
prior records and scales, not on an already selected new outcome.

A leaf attempt fails with conditional probability at most
B*p^(-a)+1/(4p)<1/2. Fresh attempts give exhaustion <=M*2^(-R), without
assuming IID successful records. Each input is consumed once, including
zero-scale discards; rejected batches are discarded completely. Keep the
full classical record so disjoint live factors remain conditionally
independent. Reusing an unlucky seed does not satisfy this premise.

Count each stage's nodes as t times the product of later arities. If
Cread=t*product(ordinary arities), a sufficient complete-instrument count is

```
Icalls = Qraw + M*R + sum(stage nodes) + Cread + t.
```

Require half-diamond error <=epsilon/(8Icalls) per COMPLETE instrument,
uniform over its classical history and including ABORT. Telescoping
CPTP hybrids give total error <=epsilon/8, with no division by a rare
outcome probability. The approximate process is compared to the whole
ideal process; it need not itself have exact conditional product form.

The four failure allowances are leaf exhaustion <=epsilon/4, final
annihilator spanning <=epsilon/4, binary sampling <=epsilon/8 and
instrument error <=epsilon/8. Total <=3epsilon/4. Solver failure or a
nonuniform implementation is not covered by naming this unused slack.

## Bit Complexity And General-H Recursion

At fixed c,k and n bounding each dimension, hA,hI=O_c(n^(c+1)),
J=O_c(n^c). There are at most O_c(n^(hc+c(k-h)))=O_c(n^(kc)) physical
monomials for a fixed h block: q degree <=hc and jet degree <=k-h.
Combining parameter counts gives the loose but sufficient bound
Ew_w=O_(c,k)(n^(k(2c+1))); Eo_j=O_c(n^(2c+1)). There are kc+c stages.
Their arities and product are polynomial in n only because c,k are fixed.
R is logarithmic in M/epsilon and B is polynomial in n and log(p).

This proves polynomial schedule size, not a gate count. The following
operations must additionally be charged:

- Validate public Lie data, compute bases/ideals/normalizers/quotients,
  and evaluate fixed-class BCH using modular arithmetic. BCH rational
  coefficients depend only on c; p>c makes their denominators invertible.
- Compile the public universal cocycle and formal coefficient tables,
  retaining the full parameter basis. Fixed k,D bound their polynomial
  expansion size. Arithmetic is reduced modulo p throughout.
- Compute the GL split, inverse and Taylor maps by finite-field linear
  algebra; synthesize their reversible action on valid field encodings.
- Run the all-input diagonal solver on public coefficient vectors, with
  its classical bit operations and storage charged at every node.
- Implement uniform states and coherent F_p Fourier transforms to the
  complete-instrument tolerance. Arbitrary-order QFT is a standard
  constructive dependency, not a p-by-p matrix implementation; see
  [Mosca--Zalka](https://arxiv.org/abs/quant-ph/0301093). Gate approximation
  and ancillary cleanup must still satisfy the full channel contract.
- Charge oracle output registers, reversible arithmetic, synthesis and
  solver workspace, and storage of complete classical transcripts.

The certificate's logical-register bound is only
(m+J)*(1+sum(arity-1))+B*(m+r+b)+m. It excludes those extra workspaces.
It is not a total-memory or physical-qubit estimate. Invalid binary
encodings need an explicit unitary extension, not postselection.

For arbitrary H first solve H intersect N within the metabelian ambient
N. Learn its intersection with N' abelianly, pass to its normalizer
quotient, and descend in class. This costs at most k-1 image calls.
The outer normalizer quotient then has transverse hidden subgroup;
successive image preimages descend from class at most c, costing at most
c-1 additional image calls. Derived ideals must be RECOMPUTED after each
normalizer quotient. The old N need not lie in that normalizer.

The caps are therefore c+k-2 image calls and at most three abelian calls,
not c+1. For a whole-run error epsilon allocate delta=epsilon/(c+k+1)
to each call and use a first-error union bound on correct histories.
Use global dimension n and class bounds c,k for a uniform image cost
envelope, not actual dimensions known only on a fortunate adaptive path.
The degree/support envelope also dominates smaller-class and scalar
branches. Add at most (c+k-2)*Qimage plus three abelian-query caps;
DO NOT multiply query costs across recursive calls. Charge public
oracle-embedding arithmetic separately. This general-H argument is
written mathematics, not part of the new single-call JSON certificate.

## Live Arithmetic And Evidence Boundary

Run `python -m theorems.induced_resource_certificate --write`.
The separate JSON uses the strict c9,k4 witness dimensions m2,r7,b10.
With epsilon=1/8:

| Prime | Generic sufficient query cap | Supported sufficient query cap |
| --- | ---: | ---: |
| 43 | <=2^1081434 | <=2^333018 |
| 2^127-1 | <=2^1081439 | <=2^333022 |

These are exact CEIL logarithms of sufficient caps, not floor logs,
measurements, lower bounds or claims of practicality. Exact integers
remain reconstructible from the JSON inputs and factory. No giant
receiver tree was executed. The generic comparison uses the same sharper
ordinary stage, changing only the weighted envelope.

Evidence now available:

| Obligation | Evidence | Still not established |
| --- | --- | --- |
| Right-fiber source and scalarization | Generic Lean identities; exact original-oracle composition control | General Lie/Lazard compiler refinement |
| Actual higher-degree coefficients | Public universal-word compiler; independent exact coefficient checks | One universal machine-checked compiler theorem |
| Separated support and counts | Written induction; independent enumeration and adversarial substitutions | General source-support Lean theorem |
| Finite adaptive resource schedule | Written history/error proof and exact arithmetic certificate | Executable physical controller and full formal composition |
| General SDE and QFT | Published constructive dependencies | General local solver and synthesized receiver |
| Scope extension | Explicit c9,k4 ambient witness | Independent novelty review and useful hard application |

The connected tests exercise genuine cubic/quartic parameter phases,
larger abelian fibers, actual Taylor pullbacks, nonzero spectator offsets,
invalid source supports and corrupted resource clocks. The new arithmetic
tests also use a 127-bit prime, but do not simulate a quantum computation
over that field. The general-H cap is not a result measured by these tests.

Verification: 519 connected Python tests pass (206.56s, RuntimeWarning
fatal), including 18 new resource/support controls. Full cached
`lake build --wfail` passes (3466 jobs). Python syntax, formal crosscheck,
site JavaScript/site checks, `qsearch.py validate`, and whitespace pass.
All owned processes are terminal. The full repository Python suite was
not run. No new Lean theorem, central registry admission, CLI/UI change,
commit or push was made in this pass.

## Attempt To Kill The Proposal

1. An actual source term outside the separated support invalidates the
   reduced schedule. It does not invalidate the generic schedule by
   itself. Full-coefficient comparisons and cross-block controls pass.
2. A mismatch between the Lie cocycle and the public compiler invalidates
   the receiver regardless of degree bounds. Current exact comparisons
   pass; the universal refinement remains a real proof obligation.
3. Hidden dependence of alignment on Q, or record-dependent selection
   with nonuniform retained roots, invalidates the query/error proof.
   Keep public alignment and all outcomes; no rare-branch renormalization.
4. An implementation that enumerates F_p, factors p-1, postselects a
   favorable character, or uses the partial SDE solver at all stages
   invalidates the uniform runtime claim. None is licensed here.
5. A theorem with the same uniform-large-prime, arbitrary-H and source
   scope could subsume this route. The targeted literature check did not
   establish such subsumption; that is not a novelty proof. The broader
   [bounded-prime nilpotent result](https://arxiv.org/abs/2304.08376) and
   prior polynomial-graph/state-access distinctions remain relevant.
6. Even if correct and new, this may have no useful hard application.
   Fixed-class constants are prohibitive and existing explicit graph,
   code and matrix-action examples have strong classical attacks. No
   conclusion about DCP, lattices, general graph isomorphism or cryptography
   follows from this scope witness.

Research decision: the route remains a plausible theorem target, not a
Shor-level result. The next substantive step is an independent complete
proof/refinement or a mechanism that removes the large erasure tree.
Do not spend another pass generating nearby filiform examples, exposing
this arithmetic through UI/CLI, or calling a smaller cap a discovery.
