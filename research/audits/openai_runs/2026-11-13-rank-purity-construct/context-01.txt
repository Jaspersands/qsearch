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
