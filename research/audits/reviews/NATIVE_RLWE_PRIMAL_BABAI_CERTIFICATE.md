# Referee review: NATIVE_RLWE_PRIMAL_BABAI_CERTIFICATE

Note: `research/NATIVE_RLWE_PRIMAL_BABAI_CERTIFICATE.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The Babai sufficient condition (1), the centered discrete-Gaussian MGF behind (2), the shared-shape mixture MGF (3) with Z_j ~ Exp(2pi) and prod(1-alpha p_j) >= 1-alpha, and the rational surrogates (163/60 < e, (163/60)^25 > 2^36, pi > 3, (d/2)e^-4pi <= 1/4096) all check against theorems/native_rlwe_primal_babai.py. Both judges flagged only the title, which states decoding at the lower modulus with no qualifier although two seeded d=64 labels are certified under the exact discrete reference law with transfer, anchor and precision losses unpaid; I confirm that gap. Judge A said the table's '.012670270530' disagrees with the saved rational 0.01267027052934 in the last digit; I drop that remark, because all four table entries are the saved upper bounds rounded up at 12 decimals (ceil), which is consistent and conservative. Both judges noted that 'RAISED to 4096' should read capped (the code uses min(k,4096)); the bound is conservative either way, so this is wording, not a defect. Controls (radii 1-100 decode, 1000/5000 fail) and timings match the saved certificates.

## Claims

### 1. gap

> Native Ring-LWE: Direct Classical Decoding At The Lower Modulus

- Step: Title
- Finding: Headline scope (both judges). Read alone, the title asserts classical decoding at the q-near-d^4 modulus in general. The note certifies only two seeded labels at d=64, q=16777259, under the exact discrete reference law, with source-discretization, anchor and precision losses outside the bounds and the derivation LOCAL / REVIEW PENDING; d=256/1024 are 'parameter choices, NOT results' and the PRS error-family assumptions were not reverified.
- Conceded by the note's own self-check: yes

### 2. holds

> Exact nearest plane returns the planted point whenever

- Step: 2. Original-Coordinate Decoder, (1)
- Finding: Standard nearest-plane sufficient condition: t-P in the centered Gram-Schmidt parallelepiped, i.e. |<u_i,w>| < ell_i/2. The basis depends only on a, which is independent of (s,e). Both judges agree.
- Conceded by the note's own self-check: no

### 3. holds

> Chernoff, symmetry and (1) therefore imply

- Step: 3. Spherical Source Certificate, (2)
- Finding: Completed square plus rho_s(Z^n+c) <= rho_s(Z^n) gives MGF <= exp(rho^2 v^2/(4pi)); v = 2pi r/rho^2 with r = ell/2 gives exp(-pi ell^2/(4rho^2)), doubled for both sides; the union bound needs no independence. Saved spherical bounds 0.0054417918650 and 0.0058834050005 match the table. Both judges agree.
- Conceded by the note's own self-check: no

### 4. holds

> The final inequality uses product_j(1-alpha*p_j)>=1-alpha

- Step: 4. Shared Hidden Shape, (3)-(4)
- Finding: Z_j = x^2+y^2 with x,y of variance 1/(4pi) is Exp(rate 2pi), giving 1/(1-lambda/(2pi)) with lambda/(2pi) = d(log d)^2 v^2 p_j/(16pi^2); Weierstrass gives the product inequality. The table's shared-shape column equals the unconditional-mixture bound (0.0107054649, 0.0126702705), the minimum against the shape-conditioned totals 0.0230/0.0268. Both judges agree.
- Conceded by the note's own self-check: no

### 5. holds

> Also (163/60)^25>2^36, so e>2^(36/25), and pi>3

- Step: 5. Exact Rational Arithmetic
- Finding: 25 ln(163/60) = 24.985 > 36 ln 2 = 24.953, so exp(-pi l^2/(4h)) <= 2^-(27 l^2/(25h)). The next sentence's 'RAISED to 4096' is inverted wording: the code takes min(k,4096), which raises the term and keeps the bound conservative. Both judges agree.
- Conceded by the note's own self-check: no

### 6. holds

> These decimals are approximations to saved EXACT RATIONAL upper bounds

- Step: 1. Research Decision table
- Finding: Saved rationals: 0.0054417918649996, 0.0107054648889957, 0.0058834050005325, 0.0126702705293418. Every table entry is the 12-decimal ceiling of its rational, so '.012670270530' is consistent rounding-up of an upper bound; judge A's last-digit discrepancy is dropped. LLL 9.93/10.34 s and totals 15.94/16.23 s match.
- Conceded by the note's own self-check: no
