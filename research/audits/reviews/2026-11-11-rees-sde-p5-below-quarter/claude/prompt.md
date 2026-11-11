You are an adversarial referee. The context file states the problem, the prior proved inputs (Lemma 1,
Lemma 2, Fact F5, Fact T3; treat these as given) and two NEW claims. Treat the new claims as unproved.

Proof obligations, in order of importance:

1. Claim 1 (SPARSE2). Decide whether the algorithm is correct and the bound
   m ≥ 0.24 n² + 0.48 n log_5 n + 3n + 3 follows, deterministically in poly(n, m) time, for EVERY
   input (worst case). Check specifically: (a) that a 2-dim subspace W of D0 supported on Y = supp W
   lets Lemma 2(A) and Fact F5 be applied with Y as the piece (realizers supported on Y, the
   γ-terms being dependencies of Y); (b) the averaging identity ρ_r = (5^{r−2}−1)/(5^r−1) and the
   inequality min ≤ average for the support, including labels g_i = 0 (coloops of D0); (c) that returning
   X ∖ Y to the pool and continuing in V/⟨h1,h2⟩ is compatible with Lemma 1 (disjointness of pieces,
   witnesses found in a quotient); (d) the pool requirement and the summation/closed form; (e) the
   running time of the enumeration. If any step fails, give a concrete counterexample or the exact gap.

2. Claim 2 (lifting lemma and simplex corollary). Check the induction step: is K_H a subspace; is
   "K_H = 0 ⇒ strongly nondegenerate restriction" right; does the pigeonhole (≥ 156 hyperplanes vs 31
   lines) and the conclusion y_{2α} = 2y_α ⇒ degeneracy hold for weak nondegeneracy as defined; is
   Lemma 2(B) correctly applied to conclude R(X_r) has no 3-dim subgroup; is "every 2-dim subcode of the
   simplex code has support 5^r − 5^{r−2}" right.

3. Briefly: is there an evident way, inside this framework, to get a leading constant below 6/25 at
   p = 5 (e.g. a better-than-averaging choice of W, or a provably feasible family of 3-dim label sets that
   a selection rule can force), or an evident reason it cannot work? One concrete idea or reason is
   enough; do not survey.

Answer with a verdict per claim (ACCEPT / ACCEPT WITH FIXES / REJECT), numbered findings with the exact
location, and keep the report under 1500 words.
