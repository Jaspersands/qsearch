# Referee review: PRIME_CHARACTER_CAPACITY_SOURCE

Note: `research/PRIME_CHARACTER_CAPACITY_SOURCE.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The two judges agree on every claim: the flat 1/(p-1) Fourier spectrum, the sqrt(5)/6 p5 spread, the whole-ball collision count, the fiber bound M and the pure-distance bound hold. My recomputation confirms epsilon_32=3.19794e-99, TD^2=5.2658e-69, the 42.6x M22 countercontrol, 577/4969/26713 and 343/6859/79507. Both judges flag the headline 'YES', and the gap is confirmed. A non-trivial bound exists only at N127,K39,p=2^61-1 for ell24/32; the bound is already 1 in coherent distance at ell37 (epsilon=2.77e-5, M=2.4e32) and trivially 1 at ell38. The bounded N6 controls have bad-mass bounds 1, 1/3 and 1/7, so ambiguity is not negligible there either.

## Claims

### 1. gap

> without randomizing input shifts? YES for the flat-spectrum primes below

- Step: Question And Decision
- Finding: The YES is unqualified by radius or instance. Non-trivial bounds are certified only at one large instance (N127,K39,p=2^61-1, both zero conventions) for ell24 and ell32. Recomputed: ell37 gives epsilon=2.77e-5 but M*epsilon>>1, so the coherent distance bound is 1, and ell38 is the trivial 1 (stated only in Executed Evidence). The bounded N6,K3,ell2 controls have any-radial-weight bad-mass bounds 1 (p7), 1/3 (p19) and 1/7 (p43). The decision does not say that the control fails as the radius approaches capacity, the regime that capacity-DQI targets.
- Conceded by the note's own self-check: no

### 2. holds

> Consequently EVERY nonzero Fourier probability is exactly1/(p-1)

- Step: Exact Local Source
- Finding: With tau_p=i*sqrt(p), |eta+s*chi*i*sqrt(p)|^2=1+p, so each probability is (p+1)/(p^2-1)=1/(p-1). At p=5 (tau real), (1+sqrt5)^2-(1-sqrt5)^2=4sqrt5 over 24 gives the stated sqrt(5)/6 spread.
- Conceded by the note's own self-check: no

### 3. holds

> It bounds bad source mass for ANY normalized radial weights

- Step: Ambiguity Against The Entire Ball
- Finding: When |S union T|>K, the intersection dimension is j+r-K, and h<=j+r-K-1 is exactly that condition. Spheres have disjoint supports, so the per-sphere bound passes to any radial weights. The formula recomputes to epsilon_32=3.19794e-99.
- Conceded by the note's own self-check: no

### 4. holds

> is well defined, and P(unique herald)>=1-epsilon, trace_distance^2 <= M*epsilon/(1-epsilon+M*epsilon)

- Step: Coherent Error Is Not Bad Mass
- Finding: For orthogonal G and B, TD^2=||B||^2/(||G||^2+||B||^2), which increases in both arguments, giving the bound. The M22, epsilon 0.01 control gives TD=sqrt(0.22/1.21)=0.426, i.e. 42.6 times epsilon, consistent with 'over40 times'.
- Conceded by the note's own self-check: no

### 5. holds

> Fixed-input source ambiguity upper bound is about3.198e-99

- Step: Executed Evidence And Limits
- Finding: Exact recomputation gives epsilon_32=3.19794e-99, M=1.6466e30, TD^2=5.2658e-69 and TV=7.2566e-35, matching the stated 5.266e-69. The artifact's ell19 bound is exactly 0 and its ell38 bound exactly 1.
- Conceded by the note's own self-check: no

### 6. holds

> They enumerate all577/4969/26713 ball errors and343/6859/79507 coefficient words

- Step: Executed Evidence And Limits
- Finding: 1+6(p-1)+15(p-1)^2 gives 577, 4969 and 26713 for p=7, 19 and 43, and p^3 gives 343, 6859 and 79507. The artifact's actual bad masses (0.288889/0.1/0.046032) match the text.
- Conceded by the note's own self-check: no
