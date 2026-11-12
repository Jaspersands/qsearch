# A native separated-scale falsifier for the nearby-band shortcut

2026-11-12. Reviewed written parent derivation; the complete256line independent proof
was parent-read (audits/reviews/2026-11-12-conductivity-separated-scales.md). This attacks a
specific proposed classical estimator, not classical computation or the
written quantum algorithm. Parent started STATE/TRAPS, corpus lookups then
actual Mourrat source. No new quantum implementation. The full polynomial
classical match remains OPEN.

## Contract and candidate

Use the exact circuit-input conductivity problem in
PERIODIC_CONDUCTIVITY_NATIVE_ADMISSION.md: L=2^n, fixed contrast, arbitrary
Boolean material circuit, additive scalar energy. Let Pi be the constant
coefficient gradient projection and eta=e1/L on L^2 nodes. Put v=Sigma eta.
The third projection moment is

    T2=<v,Pi Sigma Pi Sigma Pi v>=||Pi Sigma Pi v||^2.

Define A_-1=Pi(1-exp(-Kedge)),
A_l=Pi(exp(-2^l Kedge)-exp(-2^(l+1)Kedge)), l>=0,
where Kedge acts componentwise by the scalar torus Laplacian. These positive
commuting contractions sum to Pi; they are the exact integrated heat bands.
The proposed shortcut retains only triples (i,j,k) with max-min<=w. Call the
result T2^(w). It is an ANALYTICAL sum, not a free kernel sampling oracle.
The hoped-for width O(r+log1/epsilon), independent of n, would remove some
scale enumeration. The reviewed theorem refutes that particular shortcut.

## Explicit native circuit and the full moment

For n>=2 set h(x)=1[x<L/2] and

    Sigma(x,y)=h(x)(-1)^x+(1-h(x))(-1)^y,

on both edge directions. One selector, the coordinate MSB and two parity
bits give a size O(n) circuit (indeed the decision uses three bits).
This is an ordinary two-phase material; no planted source or external advice.
Write vA=h(x)(-1)^x e1/L, vB=(1-h(x))(-1)^y e1/L.
Since L/2 is even, vA has mean zero and is a one-dimensional gradient:
Pi vA=vA and ||vA||^2=1/2. The second summand has Fourier ky=L/2, so

    ||Pi vB||^2 <= (1/4)||D_x(1-h)/L||^2 =1/(2L).

Sigma vA=h e1/L. Its gradient projection is
u=(h-1/2)e1/L, with ||u||=1/2. Therefore

    ||Pi Sigma Pi v-u|| <=1/sqrt(2L),
    |T2-1/4| <=1/sqrt(2L)+1/(2L).

Thus the full moment retains constant mass for a genuinely native family.

## Outer-band approximation with an explicit total error

Let a_-1(lambda)=1-exp(-lambda) and
 a_l(lambda)=exp(-2^l lambda)-exp(-2^(l+1)lambda).
All a_l(4) are nonnegative and sum to1. The four boundary sites of the
windowed alternating vector give

    ||(Kedge-4)vA||^2 <=4/L.

On the spectrum below2 this bounds ||P_<2 vA||<=1/sqrtL. On [2,8],
every a_l has derivative bounded by1. Hence, for every l,

    ||A_l v-a_l(4)vA|| <=5/sqrtL.

The Pi vB contribution is included. Take J=3n. The smallest positive
Laplacian eigenvalue is at least16/L^2, so

    sum_(l>J)||A_l v|| <=2 exp(-32L).

The scalar a_l(4) tail is smaller. Consequently, with

    E=5(3n+2)/sqrtL+3 exp(-32L),

we have sum_l ||A_l v-a_l(4)vA|| <=E. All sums are over l=-1,0,... .
These generous constants are not numerical evidence; spectral inequalities
prove the bound for all n. A finite exact control checks only transcription.

## Nearby-band sum, including all signs and cancellations

For fixed outer i,k with |i-k|<=w, sum the admissible middle bands into
B_ik. It is a positive contraction because it is a subset of the positive
resolution of Pi. Replacing each outer A_i v by a_i(4)vA changes the TOTAL
truncated sum by at most 2E+E^2, without an extra number-of-bands factor:
use ||B_ik||<=1 and sum the outer norms/errors.

After replacement, Sigma vA=h e1/L, so every scalar
<h e1/L,B_ik h e1/L> is nonnegative. Let a=ceil(log2 n).
If both outer indices are <=a, every admitted middle index is <=a+w.
The sum of their weights is at most1. If either outer index exceeds a,
the total scalar contribution is at most
sum_(i>a)a_i(4)=exp(-4*2^(a+1)), since ||h e1/L||^2=1/2.
For T=2^(a+w+1), positivity and 1-exp(-T lambda)<=T lambda give

    <h e1/L, sum_(j<=a+w) A_j h e1/L>
       <=T <h e1/L,Kedge h e1/L>=2T/L.

Therefore

    |T2^(w)| <=2^(a+w+2)/L+exp(-4*2^(a+1))+2E+E^2.

For every nonnegative integer width w(n)=o(n), this tends to0, while T2
tends to1/4. In particular a width depending only on fixed epsilon and
r=2 cannot give a uniform additive epsilon<1/4 approximation. Large
individual terms alone would not prove this: the positive middle-band
summation and total outer-error estimate control the actual discarded sum.

## Scientific disposition and next experiment

The independent review confirms the proof; reject ONLY nearby-scale
truncation/common-scale replacement. A coupled estimator retaining distant
scale excursions, wavelet or variational algorithm is untouched. This family
has simple microstructure and is not a hardness instance. Full polynomial
classical matching stays OPEN, and no quantum separation is inferred.
The five paid obligations are now terminal; four completed nonempty reports
are checked, one empty truncation has no findings. See
CONDUCTIVITY_MULTISCALE_API_DISPOSITIONS. A future return requires a new
cancellation-preserving full-law estimator with poly(n,r) C^r work and second
moment. The current research selection pivots to native local divisor arithmetic.

Completed exact L8 control: Pi vA=vA, ||vA||²=1/2,
||Pi vB||²=3/68<=1/16, ||Pi Sigma vA||²=1/4, T2=3137/13872.
Artifact audits/controls/conductivity_separated_scales/result.json. This
checks algebraic transcription only; the all-n conclusion uses the proof.
The independent proof gives the slightly tighter E_n=4(3n+2)/sqrtL+
3exp(-32L) and sqrt2 E_n+E_n² in place of the safe parent constants.
No additional size, heat-exponential numerical test or sweep is needed.

## Complete scalar-output consequence (proved, focused paid audit checked)

The completed full-energy-excursion report was read in full and checked by
the parent. This strengthens the moment counterexample to the actual scalar
finite-series shortcut. Let e=Pi vB, u=(h-1/2)eta, q0=Sigma vA=h eta,
M=Pi Sigma Pi, and epsilon_L=1/sqrt(2L). Direct multiplication gives

    M vA=u,       M u=(vA-e)/2,
    e perpendicular vA,u,  ||Pi v||<=1.

The two-step recurrence and ||M||<=1 imply, uniformly over all k>=0,

    M^(2k)vA=2^(-k)vA+error_(2k),
    M^(2k+1)vA=2^(-k)u+error_(2k+1),
    ||error_r|| <= (sum_(j>=1)2^(-j))||e|| <=||e||.

Writing T_r=<Pi v,M^r Pi v>, orthogonality removes the e pairing with the
main term. The two remaining errors each have size<=||e||. Hence

    |T_r-t_r|<=2||e||<=sqrt(2/L),
    t_(2k)=2^(-k-1), t_(2k+1)=0, T0=1/2+||e||².

The already proved native series and meanSigma=0 therefore give

    Kstar=2c(1-z²)/(2-z²),
    |K-Kstar|<=c z² sqrt(2)/[(1-z)sqrtL].

This uses finite operators, not a continuum laminate assumption.

For the restricted moments use the exact window inclusion-exclusion

    1{max indices-min indices<=w}
      =sum_(s>=-1)[1{all indices in[s,s+w]}
                       -1{all indices in[s+1,s+w]}].

Put P_s=sum_(j=s)^(s+w) A_j, P'_s=sum_(j=s+1)^(s+w) A_j and
G_r(P)=<v,P(Sigma P)^r v>. For r>=1,

    T_r^(w)=sum_s [G_r(P_s)-G_r(P'_s)],
    G_r(P)=<Pv,(Sigma P)^(r-1)Sigma Pv>.

The sums converge absolutely at each finiteL by the heat-band tail. Write
P_sv=C_s vA+e^s. Outer replacement costs sqrt2||e^s||+||e^s||².
Every band occurs in AT MOST w+1 windows, including the boundary at -1;
therefore sum_s||e^s||<=(w+1)E and sum_s||e^s||²<=(w+1)E², with
E=4(3n+2)/sqrtL+3exp(-32L). Same bounds hold for primed windows.
For r=1 the ideal term vanishes. For r>=2 it is

    C_s² <q0,P_s(Sigma P_s)^(r-2)q0>.

For every positive contractionP, P(Sigma P)^m=P^(1/2)
(P^(1/2)Sigma P^(1/2))^m P^(1/2), so its quadratic form is bounded in
absolute value by <q0,Pq0>, uniformly in m. Put a=ceil(log2n),
T=2^(a+w+1), tau=exp(-4*2^(a+1))<=exp(-8n). For s<=a,
<q0,P_sq0><=T<q0,Ke q0>=2T/L. For s>a, C_s<=tau and
sum_s C_s<=w+1. Primed main terms obey the same bounds. Thus ALL r>=1 obey

    |T_r^(w)|<=B_n(w)
      =(a+2)2^(a+w+3)/L +(w+1)exp(-8n)
                        +2(w+1)(sqrt2 E+E²).

B_n(w)->0 for every w=o(n), independent of the series cutoff R. Consequently

    |K^(w,R)-c(1-z²T0)|<=c z³ B_n(w)/(1-z),
    K^(w,R)->c(1-z²/2),
    gap=c z^4/[2(2-z²)]>0.

Choose fixed epsilon<gap/4 and an honest contrast cutoff R with true-series
tail c z^(R+2)/(1-z)<=epsilon/8. Any w=o(n) still misses the limiting gap;
the usual R,w=O(logn) schedule fails as well. No positivity of the full
restricted sum, infinite tuple count or cancellation assumption is used.

Corrections to advisory report: distinguish u=Pi Sigma vA from q0=Sigma vA;
window multiplicity is AT MOST w+1; the proved convergence error is O(L^-1/2),
not its heuristic O(1/L). No optimal constant in required width is claimed.
General correlated estimators, alternative resummations and full classical
polynomial matching remain open. The one exact L8 control already paid
transcription; no further numerical sweep is necessary.
