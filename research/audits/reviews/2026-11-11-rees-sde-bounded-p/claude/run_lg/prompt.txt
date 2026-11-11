Adversarial referee task (one narrow proof obligation). The context file defines a finite
"gadget" feasibility problem over F_p (S = kappa-th powers with 0) and gives short proofs of
Lemma K, Lemma V, Lemma 1, Theorem LG, Theorem LG_R and Corollaries 1-2. The repo's prior lemmas
(Lemma 2, R, Q/N) and the finite inputs are given; treat them as true.

Your job: decide whether each of Lemma K, Lemma V, Lemma 1, Theorem LG, Theorem LG_R, Corollary 1,
Corollary 2 is correct AS STATED, with the quantifiers stated. For each give ACCEPT, ACCEPT WITH
FIX (state the exact fix), or REJECT (give a concrete counterexample, preferably a tiny one at
p = 3, 5 or 7 with explicit labels, Phi and gamma, or an exact logical gap).

Points that deserve the most scrutiny:
 (a) the reparametrization step (restricting alpha to an injective B: F_p^2 -> F_p^d) really yields a
     family of the required form with Phi' in S^2, and its kernel is B^{-1}(K);
 (b) Lemma 1's use of Lemma Q/N to make Phi' P-equivariant for k = 1, and the dimension count;
 (c) in Theorem LG, the step "codim(K_u cap K_w) <= 1 for all pairs => a common hyperplane H"
     (including the cases where some K_u = F_p^d), and the final step y_{r alpha} = r y_alpha;
 (d) whether LG's hypothesis on planar sections is used only for sections that contain two
     independent full lines (so that Lemma K applies there);
 (e) Corollary 2's description of the labels of a sub-piece;
 (f) whether any claim silently assumes one column per label (multiplicities are arbitrary in
     the application).
Do not re-derive the repo lemmas. Be concise: at most about 1200 words of final text. If
everything holds, say so plainly and list the one weakest step.
