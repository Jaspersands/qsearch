# Referee review: PRIME_CHARACTER_OPI

Note: `research/PRIME_CHARACTER_OPI.md`. Reviewed 2026-10-22 by claude-opus-5.5-subagent-2026-10-21-calibration-r2-judge-d. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The power-completion and strict zero-avoidance derivations check out: F^(1/r) truncation gives deg(R^r-F)<=(r-1)D-1, and the shifted root R+c raises the degree by at most one. The quadratic-jet character-sum bound also holds. Every live count I checked (344 witnesses, 16 stages, 1934 proposals, 11 moves, 116319 Horner evaluations, and the 108/110, 102->109, 118->124/122 and 29->30 scores) matches the artifact. The tight-degree p5 counterexample holds only for the square coset, which the note does not state; with the nonsquare coset the constant Q=3 is a perfect strict solution at K2. The header's list of open cases leaves out unsolved saved high-rate mixed sources: N31,K16 seed71 (30/31) and the r=3/r=4 mixed controls.

## Claims

### 1. holds

> Thus ALL common-coset inputs are solved perfectly

- Step: Constructive Classical Power Completion
- Finding: Verified: F=lambda^r X^D(...) so F^(1/r)=R+O(1/X), giving deg(F-R^r)<=(r-1)D-1; Q(a_i)-t_i=beta*R(a_i)^r since W vanishes on selected points. Saved global thresholds hold (N16K8: 8<=8; N31K16: 16<=16; N127K77: 64<=77; r3 N63K46: 42<=46; r4 N32K24: 24<=24) and the artifact reports all of these global sources perfect. Holds in the zero-including mode, which is the section's scope.
- Conceded by the note's own self-check: no

### 2. holds

> Hence K>=b+1 is a uniform sufficient condition for perfect STRICT common-coset completion

- Step: Strict Nonzero Powers: Constructive Zero Avoidance
- Finding: c in {0..M} avoids at most M forbidden values -R(a_i) since M<p; (R+c)^r-R^r has degree <=(r-1)D=b. Artifact: all ten strict controls report NATIVE_COMPLETION_WITNESS with full score (the r=4 strict sibling uses K25=b+1).
- Conceded by the note's own self-check: no

### 3. gap

> all25 native polynomials fail perfect strict satisfaction

- Step: Tight degree paragraph (p5,N4,K2,r2, shifts (0,0,0,1))
- Finding: The coset orientation is not stated, and the claim depends on it. Exhaustive check: with the common square coset (orientation 0, the one tests/test_prime_character_opi.py uses), 0/25 polynomials are perfect. With the common nonsquare coset beta=2, the constant Q=3 gives residuals (3,3,3,2), all nonzero nonsquares, so 1/25 is perfect at K2. The counterexample needs 'square coset' added.
- Conceded by the note's own self-check: no

### 4. holds

> Uniform proposals therefore succeed with probability>=1/3

- Step: Mixed-Coset Quadratic Jet Attack
- Finding: sum_z chi(z^2+a/beta)=-1 for a!=0 gives an accepted count of (p-chi(beta/beta_i)+Z)/2>=(p-1)/2, and (p-1)/(2p)>=1/3 for every odd p>=3. The degree bookkeeping (h=max(0,2D-K+1), deg(2R0L+L^2)<K) also checks out.
- Conceded by the note's own self-check: no

### 5. holds

> For N127,K77,118/118 improves to124/122

- Step: Adaptive Root-Value Exchange Is Now Executed
- Finding: Matches the artifact: K77 mixed 118->124 (seed29) and 118->122 (seed71); K39 102->109 for both seeds; 16 repair stages, 1934 proposals, 11 accepted moves and 116319 Horner evaluations; 344 retained witnesses (=4 r2 configs x4 sources x17 + 2 higher-r configs x4 x9). The pass bound N-initial_score+1 follows from strict improvements.
- Conceded by the note's own self-check: no

### 6. gap

> K39 and general fixed-input/asymptotic solvability remain open

- Step: Header / Live Controls summary
- Finding: The open-case list names only K39, but other saved high-rate mixed sources are also not perfect in the artifact. N31,K16 mixed seed71 is best 30/31 (r=2, R+rho=16/31+1/2>1, so in the published perfect-search regime). The r=3 N63,K46 mixed sources are 55/63 and 56/63 (R+rho~1.06>1), and the r=4 N32,K24 mixed sources are 28/32 and 27/32. The superseding norm attack covers only N127,K77. The Live Controls paragraph also reports only the r=3/r=4 global controls ('also perfect') and omits these mixed scores.
- Conceded by the note's own self-check: no
