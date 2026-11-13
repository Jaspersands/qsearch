# Stabilizer rank versus Pauli purity

2026-11-13. Status: polynomial lower bound OPEN; every cubic bound REFUTED.

## Native question and algorithmic contract

Input: fresh IID copies of an unknown normalized n-qubit pure state psi and
an integer k promising exact stabilizer rank chi(psi)<=k. No decomposition,
coefficient bound, Gram conditioning, preparation/reflection oracle, conjugated
copies or amplitude access is supplied. Output: a classical stabilizer tableau
phi with squared overlap at least c*k^-C, with failure at most eta. Target:
poly(n,k,log(1/eta)) gates and copies. Verification uses the returned Clifford
measurement and fresh copies at the inverse-polynomial overlap scale.

The single missing proposed mechanism is a uniform inequality

    Pi(psi)=2^-n sum_(a,b) |<psi|X^a Z^b|psi>|^4 >= c*k^-C,

for absolute c>0,C<infinity. For f(x)=2^(n/2) psi_x, Pi=||f||_U3^8.
No bounded-function inverse theorem applies merely from E|f|^2=1.
Actual quantum-state inverse theorems give a Bell-difference signal Q with
Pi^2<=Q<=Pi, and stabilizer fidelity Omega(Q^C0). The copies-only
self-corrector then gives the desired tableau in polynomial inverse-signal
time. Marton Cor8.6 removes its algorithmic-PFR assumption. This is a
CONDITIONAL component-discovery composition, not a full tomography theorem.

Strongest checked baseline: Sinha--Lovitz 2610.06819v1 Theorem1.1 gives squared
extent 2^O(sqrt(k log(k+1))); Cor1.6 already gives copies-only full tomography
in poly(n,1/epsilon,log(1/eta))*2^O(sqrt(k log(k+1))). The contemplated gain is
polynomial dependence on k for the weaker component output. No classical
hardness or quantum advantage is asserted: the input is quantum copies,
and a supplied bounded-coefficient tableau decomposition is a different model.

## Exact cubic falsifier

Let q=1/8 and psi0=(|0^6>-|+^6>)/sqrt(7/4). For a,b in F2^6,

 <psi0|X^a Z^b|psi0>
   = [1_(a=0)+1_(b=0)-q*(1+(-1)^(a.b))]/[2*(1-q)].

Thus the identity contributes 1; exactly one zero index gives 126 terms of
magnitude 3/7; nonzero orthogonal indices give 63*31=1953 terms of magnitude
1/7; all other terms vanish. Consequently Pi(psi0)=65/686<1/8. It has exact
rank two, since its nonzero Pauli expectation 3/7 excludes a stabilizer state.
For every r>=1, chi(psi0^tensor r)<=2^r and
Pi(psi0^tensor r)=(65/686)^r. Therefore no absolute c>0 can satisfy a uniform
c*k^-3 lower bound. Any uniform polynomial exponent must obey
C>=log2(686/65)>3.39. This is an exact tensor-family deduction, not an
extrapolation from finite tests. It does not refute any sufficiently large C.

## Obligations, falsifiers and boundaries

Construct a dimension-independent cancellation inequality with some absolute
exponent C, or give explicit k_j-term states with -log(Pi)/log(k_j) unbounded.
A fixed tensor-product counterexample only bounds C from below. Small Gram
singular values alone do not refute the statement, since alternative outside-
span stabilizer decompositions are allowed. Do not repeat the published
Pauli-projector elimination (extent Lemma3.4) as a new construction. A polynomial
bound would imply exponential rank lower bounds for tensor powers of T states
(Pi(T)=3/4), so this is a substantial open problem, not a routine lemma.

Greedy residual subtraction can increase rank; polynomial extent and full
rank-k tomography do not follow without a separate argument. No passing
finite control, agent acceptance, missing baseline or failed counterexample
search proves the inequality. No quantum implementation is justified yet.

Selection compared this with canonical cubic Gauss phase and expanded split-
CSA output. The former lacks a new representative-product operation; the
latter's actual source solves a simultaneous S-unit coboundary relation,
not the scalar norm tower needed for the proposed height argument. Full
comparison: audits/reviews/2026-11-13-post-folded-selection.md (179 LF), read
by parent. Corpus been-tried/baselines checked by selection reviewer before
primary sources; current arXiv versions checked 2026-11-13. Exact current
statements: extent.txt LF132-140,220-227,655-675; structure.txt LF180-214,
932-978; marton.txt LF3148-3178. All sources retained under audits/sources/.
Searches for rank/purity and rank/Renyi supplied no verified replacement
bound. This is not a novelty claim.

Next experiment: one independent constructive Pauli-moment certificate and
one explicit family attack, with the cubic counterexample and exact source
hypotheses supplied. An independent rank-two analytic audit is a cheap C=4
falsifier; it cannot certify general k. Stop this line if no new operation
survives; compare independent directions rather than extending rank slices.

## Further parent deduction: the gate is polynomial rank--fidelity

For any stabilizer phi, its rank-one projector is 2^-n times its signed
stabilizer group. Holder on that group gives

    |<phi|psi>|^2 <= [2^-n sum_(P in S_phi) |<psi|P|psi>|^4]^(1/4)
                  <= Pi(psi)^(1/4).

Taking the maximum gives Pi>=F_stab^4. Combined with the actual quantum
inverse F_stab>=a*Pi^(2b), a polynomial rank--purity bound is equivalent,
up to absolute exponents, to polynomial rank--fidelity. Thus the question is
a substantive open rank bound, not an omitted compiler. The existing
subexponential extent bound only gives Pi>=2^-O(sqrt(k log(k+1))).
This prevents the conditional learner from being counted as new progress.

One Sage exact-rational arithmetic check independently confirms65/686 and
8*Pi<1; it only checks arithmetic in the displayed all-r proof. No broader
numerical or quantum experiment is warranted.

## Conditional endpoint independently audited

Full140-LF independent review in audits/reviews/2026-11-13-rank-purity-endpoint.md
was read and checked by the parent. The source output is an explicit Clifford
image of an enumerated small stabilizer and an observed computational string,
so it supplies a classical tableau. The source distinguishes direct p_psi
Bell sampling (which would require conjugated copies) from the permitted
copy-only Bell-difference routines; no conjugation access is added here.
The actual Marton footnote14 pays the polynomial flatness loss in the BSG
sampling interface. These are checked source compositions, not a reproof
of the whole PFR theorem. Polynomial rank--fidelity itself remains OPEN.

## Rank-two falsifier exhausted analytically

Independent review audits/reviews/2026-11-13-rank-two-purity.md was fully
read by the parent; its simpler addendum was independently checked in both
directions. The admitted decision-level claim is: every normalized state
of exact stabilizer rank at most two has Pi>=701/10240>1/16.

Clifford invariance and stabilizer spectators reduce any pair to either
(|0^m>,|+^m>) or (|0>|0^m>,|1>|+^m>). The latter has Pi>=1/8 by its exact
Pauli formula. In the nonorthogonal case let s=2^(-m/2), normalize the two
coefficients so |alpha|²+|beta|²=1, and set t=2 Re(conj(alpha) beta),
z=|alpha|²-|beta|². The state norm squared is 1+s*t. For m<=3 the identity
alone gives Pi>=1/8. For m>=4, s<=1/4. The identity and two one-zero Pauli
families, convexity in z, and monotonicity in t give

 L(s)=s²+2(1-s²)*[(1/2-s)/(1-s)]^4 <= Pi.

 L(s)-1/16 = [1-11s+45s²-63s³+16s⁴+16s⁵]/[16(1-s)^3].

On s in[0,1/4], the numerator's degree-five Bernstein coefficients are
[1,9/20,29/160,61/640,17/160,5/32]. They are all >=61/640; hence
Pi>=1/16+61/10240=701/10240. The normal forms include arbitrary relative
phase, imbalance, orthogonality and spectators; a zero vector is excluded.

This is an all-dimension exact argument, not finite evidence. It rules out
rank-two counterexamples to Pi>=k^-4. It proves nothing for general k, and
does not justify a rank-three sweep. The review's additional sharper global
minimum is not needed or used for the next scientific decision.

## Paid report status

Claude attack12681 terminated truncated with EMPTY response after its token
cap; estimated usage USD1.319040, reaped. It supplies no scientific evidence
and is not retried. OpenAI construction85642 is still pending. Local request
ceilings are not billing caps or actual charges; owner actual spend remains
separate from these runner estimates.

## Terminal construction report and stop decision

OpenAI85642 completed, full response parent-read and session reaped; estimated
USD1.671910. Claude's EMPTY attempt remains no evidence and is not retried.
Estimated round2.990950, not actual billing. The general bound remains OPEN.

Accepted after direct formula checking: zeta=(-31+3i*sqrt(7))/32 gives
omega=(|0^6>+zeta|+^6>)/sqrt(225/128), with
Pi(omega)=8986816/94921875<65/686. Tensoring forces any uniform polynomial
exponent C>=log2(94921875/8986816), about3.4009. This is a fixed exponent
obstruction only; it neither refutes C4 nor all polynomial bounds.

For a mathematical supplied list s_i only, let U be the union of its unsigned
stabilizer groups and V_U=2^-n sum_(P in U)|<P>|². Cauchy--Schwarz gives
Pi>=V_U²/k. The exact two-summand visibility minimum is
nu=(29-12sqrt(2))/56, attained by the three-qubit minus pair. Tensoring the
list makes U and V multiplicative, refuting EVERY a*k^-2 visibility bound
for fixed a>0. This refutes a proposed visibility proof step, not purity.
The dyad-span map also has a kernel already for s_1=|0>,s_2=|1>, where
|0><1| has zero visible coefficients. Positivity of |psi><psi| would have
to do new work; a uniform inverse on all dyads is impossible.

The report's proposed V_U>=k^-3 lemma is UNPROVED. It would imply Pi>=k^-7
and F_stab>=k^-4, but supplies no polynomial-cost induction or new operation.
Its restricted orthogonal-list control V_U>=k^-2 is valid and is not a
native input promise. The report independently confirms rank-two C4; that
confirmation does not raise the general claim status.

Decision: PARK this line after the bounded construction/attack round. Retain
exact falsifiers and source-checked conditional learner, but do not extend
rank slices, repeat the empty request, or commission another visibility
wrapper. Resume only with a concrete new general-k cancellation operation.
Next candidate comparison is independent community-label recovery, subject
to actual multi-community source scope and classical attack first.
