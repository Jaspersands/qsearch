# NEW native polynomial-pencil repair: mixed input/half resultants

Focused proof attack/construction, not retry of earlier six broad compiler
jobs. Parent has now derived an actual algebraic operation intended to remove
the mixed-input/half conditioning blocker. Verify or refute the following exact
lemma, cheapest symbolic counterexample first. No tools available. Keep outputs
within this claim, but write a complete proof if true.

f monic squarefree in Z2[x], degree n=2g+1. Actual reduced graph divisor
[a,b], a monic squarefree of degree e<=g, deg b<e, a divides f-b². Set
c=(f-b²)/a, monic degree m=n-e. e=0 uses a=1,b=0,Disc(a)=1.
Assume all coefficients of a,b have valuations >=-S0 and their discriminant
and branch-resultant values have paid polynomial caps. S0 is a numerical
polynomial from a separate coordinate-tail theorem, not input advice.
The known source-compatible operation for scalar u in Z2 is

 A_u=c-2ub-u²a,  b_u=-b-u a,   [A_u,b_u]=[a,b].

A_u is monic of degree m<=2g+1 for EVERY u. This identity follows from
f-b_u²=a A_u; actual divisor equivalence must retain multiplicity/branch
hypotheses. A successful u is required squarefree and coprimef.

Let W be the monic degree-g reduced support polynomial of ANY half Q of
[a,b]; it is UNKNOWN to the algorithm. Suppose its coefficients and its
branch value v2 Res(W,f) have paid caps. No supplied Q or support fields.

Parent claim1: write R_W(u)=Res_x(W,A_u). Over the splitting field of W,
for EACH root beta, b(beta)²+a(beta)c(beta)=f(beta). Hence

 min(v2 c(beta), 1+v2 b(beta), v2 a(beta))
                       <=1+v2 f(beta)/2.

This is the coefficient Gauss valuation of c(beta)-2u b(beta)-u²a(beta).
Gauss multiplicativity gives the UNIFORM content bound

 content_u R_W <= g+v2 Res(W,f)/2.

Pay denominator clearing explicitly: if coefficients A_u >=-S,
2^(gS)R_W may need MORE if W nonintegral; use a correct bound from W poles.
Do not silently use signed resultant valuations to bound individual losses.
The claimed UPPER content bound still holds before scaling, with all scaling
charges then added. W and f are monic; no missing leading factors.

Parent claim2: Disc_x(A_u), as a polynomial in u, has degree EXACTLY4g and
leading coefficient

 +/- (m-e)^(m-e) Disc(a),   m-e=2g+1-2e odd.

Thus its content is <=v2 Disc(a) before an explicitly paid integral scaling.
Proposed proof: e roots tend to distinct roots of a as u->infinity; N=m-e
large roots scale u^(2/N) times Nth roots of1. The large-root discriminant
contributes +/-N^N u^(2(N-1)); cross differences contribute u^(4e);
finite-root discriminant tendsDisc(a). Total exponent 2(N-1)+4e=4g.
Need rigorous coefficient identity over characteristiczero, not a heuristic
real limit or finite test. Check edge e=0 and arbitrary poles/coefficients.

Claim3: For an integral one-variable polynomial P of degree d, contentgamma,
Pr_{u HaarZ2}(v2P(u)>gamma+t)<=d*2^(-t/d), up to an explicitly harmless
integer-rounding constant. Prove using Gauss norm and root balls, including
roots outside Q2 and outside the unit ball. The visibility event below
integer capK depends only on u mod2^(K+1), so finite integer-grid sampling
transfers EXACTLY after integral scaling. Only polynomially many independent
draws, never enumerate the grid. Compare with Markov's weaker 1/t bound,
which would NOT pay a union over exponentially many halves.

Using claim1 plus known branch-pencil bound from the supplied perturbation
note and claim2, derive a paid polynomial threshold and finite-grid bitdepth
for simultaneous visible Res(f,A_u), Disc(A_u), and mixed Res(W,A_u).
For UNKNOWN rational half choices there are at most2^(2g); union bound with
failure2^(-O(g)) must not enumerate them. Could use individual-polynomial
sublevel bounds rather than their exponential-degree product. Explain which
checks are algorithm-visible: input/branch/discriminant yes, mixed W no;
probability analysis may control the latter, but a later Stoll augmented
matrix certificate must enforce actual acceptance. Does this create any
circular reliance on selecting the square-root branch? All half bounds were
assumed jointly before choosingu, not assumed for a retrospectively chosen one.

Conclusion sought is ONLY this polynomial-pencil regularization lemma.
It does not materialize a reduced [a,b] from a signed divisor, prove a
Haar-to-sigma finite-grid stability radius, or by itself establish ONE-HALF.
Give exact corrections/falsifiers and separate every proved/conditional gate.
