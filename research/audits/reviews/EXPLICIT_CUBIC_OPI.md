# Referee review: EXPLICIT_CUBIC_OPI

Note: `research/EXPLICIT_CUBIC_OPI.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges rated the note needs-work for the same title gap and agreed on everything else, so there was no disagreement to resolve. I confirmed the gap: the title calls the attack a falsifier, while the body limits it to a finite best-of-four versus mean comparison at four predeclared sizes and shows that under its IID premise the attack cannot beat (1+R)/2, below the DQI target. Against the artifact I checked the best scores 7,7/27,27/30,30/105,104 and the 50 forced predicates (exposed prefix 51, 9 free bits, 512 messages) at N=127 and 11 forced (15 free bits, 32768 messages) at N=31. I recomputed the IID tail bound 2048*Pr(Bin(76,1/2)>=53)=0.78293, matching 3610635178399977029/2^62. The first-moment flat bound is 1/2 at t=3, d=2, N=1, as the artifact records.

## Claims

### 1. gap

> Explicit Cubic-Target OPI: A Structural Classical Falsifier

- Step: Title
- Finding: The headline drops the body's scope: the 'falsifier' is a finite, seeded, best-of-four classical score against a one-shot quantum mean at four sizes, with no matched tails or runtime, and the narrowest margin is 104/127=0.8189 vs 0.8168. The note's own conditional analysis says that if E/N->R the attack cannot beat (1+R)/2, which is below the DQI target.
- Conceded by the note's own self-check: yes

### 2. holds

> There is no finite best-score advantage in these comparisons

- Step: Live Results
- Finding: Artifact best scores 7/7, 7/7; 27/31, 27/31; 30/31, 30/31; 105/127, 104/127 all exceed the stored filter means 0.688982, 0.747358, 0.816830; all 32 attempts are EXACT_RESIDUAL_AFFINE_OPTIMUM.
- Conceded by the note's own self-check: no

### 3. holds

> min(1, N * 2^t * [t-1 choose d]_2 * 2^(-D3(d

- Step: Why The Quadratic Rank Argument Does Not Automatically Transfer
- Finding: 2^(t-1-d)[t-1 choose d]_2 base flats times 2^(d+1) heights times 2^-D3(d); at t=3, d=2, N=1 this is 8/16=1/2 and D3(20)=1351, as in the artifact.
- Conceded by the note's own self-check: no

### 4. holds

> At 127 positions each attempt forces 50 accepted predicates

- Step: Live Results
- Finding: All eight N=127 attempts have 50 forced positions, free dimension 9 and 512 candidates (exposed prefix 51 counts the unused terminal flat); the t=31, N=31 attempts force 11 with 32768 candidates.
- Conceded by the note's own self-check: no

### 5. holds

> Pr(best pool score >= k) <= min(1, S * Pr(Binomial(N-E,1/2) >= k-E

- Step: Why This Does Not Settle The Asymptotic Question
- Finding: Union bound over a prefix-fixed pool of IID Bernoulli(1/2) suffixes; recomputed at E=51, S=2048, k=104 as 0.78293, matching the artifact, and vacuous at the other sizes as the note admits.
- Conceded by the note's own self-check: no

### 6. holds

> since R/2-R^2/4 > R^2/4

- Step: Why This Does Not Settle The Asymptotic Question
- Finding: Equivalent to R/2>R^2/2, i.e. 0<R<1, so 1/2+sqrt(R/2(1-R/2)) exceeds (1+R)/2.
- Conceded by the note's own self-check: no
