# Referee review: PRIME_CHARACTER_FINITE_READOUT

Note: `research/PRIME_CHARACTER_FINITE_READOUT.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The radial near-isometry, the 2delta/(1-delta) one-extra-radius bound and the sharp integer tail bound hold, and the numbers reproduce on recomputation (epsilon_33=2.1228e-80 giving delta=1.0269e-49; herald TV 7.2566e-35; tail floors 0.314586, 0.050965, 0.779295 and 0.997627; and 106.75, 108.58 and 114.66 against 109). Both judges found a headline-scope gap but quoted different sentences: A quoted the 'certified' radius-32 mean, and B quoted the 'Yes' answer, saying it reads as a general certifier. B's single-instance and radius-37/38 points do not survive: the next sentence names the instance, and the 'when ... sufficiently small radial Gram error' clause is exactly the condition that fails at radii 37/38. What survives is A's point, kept as the one gap: the Result calls the mean 'certified' without the review-pending application or the exact-decoder premise. Those premises appear only in the status line, and the Result conditions only the tail sentence on the receiver.

## Claims

### 1. gap

> radius32, the certified normalized mean is about 0.9028547353515506

- Step: Question And Result, second paragraph
- Finding: The value matches the artifact (ell32 heralded mean lower bound) and recomputation (127*0.9028547=114.66). But the Result calls it 'certified' without saying that the Gram/readout application and the source bad-mass lemma it uses are review pending. It also does not say that the mean holds only for the ideal heralded state under an exact source and exact unique decoder. Only the status line states those premises; within the Result, 'Conditional on the stated receiver' is attached only to the tail sentence.
- Conceded by the note's own self-check: no

### 2. holds

> Therefore 1-epsilon <= ||A u||^2 <= 1+(M-1)*epsilon

- Step: Radial Near-Isometry
- Finding: Spheres have disjoint supports, so bad mass is a weighted average of the epsilon_j. Each fiber has at most M preimages, and Cauchy-Schwarz bounds the bad image by M*b. Recomputed at L=33: epsilon=2.1228e-80 and M=4.8374e30 give delta=1.0269e-49, matching the stated 1.027e-49.
- Conceded by the note's own self-check: no

### 3. holds

> mu_ideal-mu0| <= 2delta/(1-delta), provided delta<1

- Step: The Score Reaches One Extra Radius
- Finding: The numerator u*(G-I)Tu - mu0(u*Gu-1) is at most delta+delta, using ||T||<=1 and mu0 in [0,1]. The denominator is at least 1-delta. The stated mean correction 2.054e-49 is 2*1.027e-49, consistent with this bound for small delta.
- Conceded by the note's own self-check: no

### 4. holds

> This is sharp given only that mean: failed mass can sit at k-1 and success at N

- Step: Finite Tail Without Inventing A Distribution
- Finding: Markov's inequality on N-S. Recomputed from mu=0.9028547353515506: (114.66255-109)/18=0.314586 and (114.66255-114)/13=0.050965. The 4- and 16-attempt values are 1-(1-0.314586)^m=0.779295 and 0.997627, matching the note.
- Conceded by the note's own self-check: no

### 5. holds

> Herald-output TV<=7.257e-35, which dominates that correction

- Step: Rational Evaluation, Not A Floating Eigenvalue Claim
- Finding: Recomputed at ell32: M=1.6466e30 and epsilon=3.19794e-99 give TD^2=5.2658e-69, so TV=7.2566e-35. That is far above the 2.054e-49 mean correction.
- Conceded by the note's own self-check: no

### 6. holds

> The easier radius22/24 means do NOT exceed the saved classical word

- Step: Decisive Controls And Classical Comparison
- Finding: 127*0.840571=106.75 and 127*0.854932=108.58 are below 109, and 127*0.902855=114.66 is above it. The note correctly calls 109/127 a single witness, not an optimum, and says no matched runtime exists.
- Conceded by the note's own self-check: no
