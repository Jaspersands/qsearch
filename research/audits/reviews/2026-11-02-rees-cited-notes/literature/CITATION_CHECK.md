# Citation check: research/REES_MIXED_SPECTRAL_SOURCE.md (2026-11-02)

Full texts were fetched and read but are not kept in the repo (it is public); re-fetch from the arXiv IDs below. Nothing executed.

1. Kimmel-Lin-Low-Ozols-Yoder, arXiv:1608.00281 (only v1 exists, 31 Jul 2016).
   Appendix C "Controlled Density Matrix Exponentiation", Theorem 20: O(t^2/delta)
   copies give controlled-e^{-i rho t} to diamond error delta; first proof uses
   program |1><1| (x) rho (the note's "enlarged-program construction").
   Theorem 1 (LMR) allows t of either sign. Verdict: matches.

2. Go-Kwon-Park-Patel-Wilde, arXiv:2412.02134v3 (29 Sep 2025). Section IV, Theorem 2:
   for t>=0, n>t, half-diamond error <= 4t^2/n for every state sigma (diamond norm
   includes arbitrary reference). Corollary 3: n <= 4t^2/eps. Stated for t>=0 only;
   uncontrolled. Controlled form via program |1><1|(x)rho is covered since sigma is
   arbitrary (also Appendix E). Verdict: matches with fix (state n>t, t>=0; take
   negative time from Kimmel Thm 1 or by the sign-symmetric proof). The note's own
   2t^2/n in Sec. 8 is its separate elementary bound, not Go's constant.

3. Bene Watts-Bostanci-Caro-Grier-Liu-Mahajan, arXiv:2610.06737v1 (5 Oct 2026),
   "Anti-symmetrization is cheap and useful". Section 3, Algorithm 2, Theorem 5:
   input n iid copies of rho, no parameters; always outputs an antisymmetric state;
   if rho has rank r and min nonzero eigenvalue lambda_min, outputs the unique
   antisymmetric state over supp(rho) (proportional to Pi_anti^r(phi_1..phi_r),
   i.e. the normalized top wedge up to phase) w.p. >= 1 - r(1-lambda_min/r)^n
   >= 1 - r exp(-n lambda_min/r). r, lambda_min are properties, not inputs; the
   loop runs while k<d. The known-rank stopping rule (loop k<r) is Remark 6, not
   Theorem 5. Discard handling: Algorithm 2 step 3(c) and paragraph after Remark 6.
   Word "nonflat" is not in the paper (Theorem 5 is simply for general rho).
   Note's use: n = N_l+1 copies, lambda_min(rho_l) >= w, so failure
   <= r_l exp(-N_l w/r_l) <= r_l 2^-b holds (monotone in lambda_min; conservative).
   Verdict: matches with fix (cite "Theorem 5 and Remark 6"; drop or gloss "NONFLAT").

4. Holt-Subramanian, arXiv:2609.38085v2 ("Learning quantum symmetries", v1 29 Sep 2026).
   Section 10.4 is "Learning symmetries of subspaces": Problem 10.13 SubspaceSL and
   Problem 10.14 ConjugateSL (mixed-state conjugation symmetry, separation in an
   unspecified "specified norm"), plus a maximally-mixed reduction with trace norm.
   Normalized Frobenius appears in Section 10.1 (unitaries) and Theorem 10.8 in
   Section 10.2 (Hamiltonians, needs spectral spread mu), not 10.4.
   Verdict: matches with fix (cite Sec. 10.2 / Theorem 10.8 for the Frobenius sentence).
