# Referee review: JACOBI_SURFACE_RECONSTRUCTION

Note: `research/JACOBI_SURFACE_RECONSTRUCTION.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Judge A rated the note sound; judge B flagged the opening 'superseding' paragraph as a scope gap. I kept B's gap but corrected its finding: that paragraph does say the imported recovery algorithm is not implemented, but it states the removal of the prime-conductor opening without the condition that the known-norm note's local application of Theorem 1.3 is review pending, which the closing section concedes. Both judges agreed on, and I re-checked, the technical core: brute-force projective counts at (p,d)=(7,3),(13,3),(13,4),(11,5) equal p^2+p+1+C with B=(d-1)(d^2-3d+3) terms of modulus p, and the primary congruence held on 1398 prime-conductor triples. The artifact confirms 14 controls, 1032 triple records, 64/64 balanced LLL rows, 246 phase checks, the six d in {3,5,7} completed reconstructions, and the 61-bit point count equal to p^2+p+1+C with |C|<=910p.

## Claims

### 1. gap

> Under the stated Jacobi/primary identities this removes the prime-conductor asymptotic quantum opening

- Step: Superseding classical comparison (opening paragraph)
- Finding: The headline paragraph states the removal as established, while it rests on JACOBI_KNOWN_NORM_REDUCTION's local application of Lenstra-Silverberg Theorem 1.3, which is review pending (artifact flags local_reduction_independently_or_formally_reviewed=false); this note's closing section says 'Independent review of the local application is still needed'. The paragraph does already state that the imported recovery algorithm is not implemented here.
- Conceded by the note's own self-check: yes

### 2. holds

> Character orthogonality gives this projective formula

- Step: Exact Reduction
- Finding: Brute-force projective counts of X^d+Y^d+Z^d=W^d equal p^2+p+1+C at (7,3),(13,3),(13,4),(11,5): 99, 261, 108, 405, matching the artifact's point counts.
- Conceded by the note's own self-check: no

### 3. holds

> The number of terms is B=(d-1)(d^2-3d+3), and each has absolute value p

- Step: Exact Reduction
- Finding: (d-1)^3-(d-1)(d-2)=(d-1)(d^2-3d+3); enumeration gave 6, 21, 52 admissible triples for d=3,4,5 and |J|=p for every one, including the a+b=0 case.
- Conceded by the note's own self-check: no

### 4. holds

> It satisfies e_t+e_(-t)=2 and sum e_t=phi(d

- Step: Ideal And Valuation Conventions
- Finding: S_(-t)=3d-S_t and d does not divide S_t when a+b+c is nonzero mod d, so the two floors sum to 1 and e_t+e_(-t)=2; summing over phi(d)/2 pairs gives phi(d).
- Conceded by the note's own self-check: no

### 5. holds

> Thus this primary condition selects the correct root multiple of a balanced generator CLASSICALLY

- Step: Prime Conductors Need No Phase Oracle
- Finding: The count p^2-3p+3=1 mod ell and the linear-coefficient argument are correct; a direct check of A(1)=1, A'(1)=0 mod ell on 1398 triples for ell in {3,5,7,11} found no failure, and the 2ell roots +/-zeta^k have distinct residues mod lambda^2.
- Conceded by the note's own self-check: no

### 6. holds

> LLL plus primary normalization reproduces all six prime-conductor native surface controls

- Step: Live End-To-End Classical Result
- Finding: Artifact: exactly the d=3,5,7 controls (six) have status CLASSICAL_PUBLIC_IDEAL_RECONSTRUCTION_COMPLETED with matching point counts; the composite d=4,8,9,12 controls do not. The p=2^61-1, d=11 control has 51 profiles, 200 triples, point count equal to p^2+p+1+C, |C|<=910p and C=910 mod 11, and is scoped as a certificate without an LLL success theorem.
- Conceded by the note's own self-check: no
