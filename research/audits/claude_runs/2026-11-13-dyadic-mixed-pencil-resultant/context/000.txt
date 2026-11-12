# Certified dyadic perturbations and a branch-resultant repair

2026-11-12. Two scoped constructions from the completed OpenAI report
audits/openai_runs/2026-11-12-fast-kummer-build/response.md were independently
reviewed in audits/reviews/2026-11-12-kummer-grid-resultant.md and parent-checked.
They do not yet compose into ONE-HALF or a complete native local Kummer image.
The native monic squarefree odd-degree integer f, arbitrary bad reduction at2,
original seed lattice L and E=2L are those of LOCAL_HALVING_SATURATION.md.
All pole/precision parameters below are numerical costs, not logarithmic advice.

Keep the ACTUAL seed exponent n_s>=2 and t_i=2^n_s*i. Let D0 be the
previously proved seed-log determinant valuation, R=D0+1, and
H=n_s*g*(g-1)+sum_(i<j) v2(j²-i²). With
F(z)=z^(2g+1)f(1/z), use actual points
P(t)=[(t^-2,t^(-2g-1)*sqrt(F(t²)))-infinity], root1mod8. Define

    sigma(z)=sum_i (P(t_i+2^R*z_i)-P(t_i)),  z in Z2^g.

The derivative W_(k,i)=-t_i^(2k)/sqrt(F(t_i²)) has determinant valuation H.
The checked expansion is log sigma=2^R*W*(z+epsilon(z)), with epsilon a
restricted strict contraction: every coefficient has valuation at least
D0-H>=2g. Thus sigma maps onto a full-rank subgroup U of the ORIGINAL E,
log U=2^R W Z2^g, and finite integer grids give exact uniform classes in
U/2^m U. No numerical inverse logarithm is used. Normalized Haar volume is
2^(-gR-H), and log2[E:U]=(g-1)D0+H. This is generally a strict subgroup.
The explicit parameter, square-root equation/residue and certified series
truncation name actual points; a signed divisor of length2g suffices without
a compositum. Keeping h_z=h+2sigma(z) preserves h+E and moves any half by
sigma(z). It provides no Stoll conditioning probability or computed half.

Separately, suppose an ACTUAL reduced Mumford pair [a,b] is already given
with monic degree e<=g, a|(f-b²), and all coefficient valuations >=-S0.
Set n=2g+1, m=n-e, S=(m+2)S0, c=(f-b²)/a and
A_u=c-2ub-u²a. The source identity [A_u,-b-ua]=[a,b] preserves the point.
Among u=0,...,2n there is a candidate with

    v2 Res(f,2^S A_u) <= Kbr=v2(disc f)+2nS+v2((2n)!).

Proof: differentiating f=b²+ac bounds the Gauss content at every root of f;
multiplicativity bounds resultant content by v2(disc f)+2nS; interpolation
at2n+1 consecutive integers costs at most v2((2n)!). Roots are analysis only.
The integral Sylvester matrix then has every Smith valuation <=Kbr.
Monic long division loses at most (r+1)S0 at coefficient depth r; input
precision Kbr+S+1 suffices for a nonzero resultant certificate. This repairs
a branch gcd/CRT operation, not the Stoll M_j/B_j matrices.

The interface remains OPEN: reduce h+2sigma(z) to a certified Mumford pair
with polynomial NUMERICAL S0, pay squarefree/root and all tested rank
decisions, and return an actual half certificate. Individual support-point
pole bounds do not imply that reduced-coordinate bound. Finite-grid uniformity
does not imply success without paid low-jet content and analytic tail bounds.

The paired Claude report's elementary coset-volume inequality and monic
root-ball tail are accepted only with the corrections in
audits/reviews/2026-11-12-kummer-coset-volume-report.md: equal volumes do not
exclude a bad coset; a successful-halving loss is infinite outside2G; an
existential best representation need not be findable; materialization must
preserve the actual good-conditioning scale. No native all-representative
counterfamily or complete halving algorithm was obtained.

Selection: preserve these exact subresults, park further extension while
the independently compared surface route has a more concrete closure path.
Next useful experiment is a proof of the reduced-coordinate interface on
this explicit sigma, with a native falsifier if it fails; no sweep/quantum code.
Claims of complete Selmer composition, hardness, novelty and speedup stay false.
