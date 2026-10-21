# Referee review: NATIVE_RLWE_SPARSE_WITNESS_AUDIT

Note: `research/NATIVE_RLWE_SPARSE_WITNESS_AUDIT.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The density lemma, the union bounds (1)-(2), the integer certificate (4) at k=44/193/796 and the h=2+X unit checks all reproduce. Both judges found the same headline gap: the 'sufficiently short' decision rests on R=2*sqrt(dq) (exactly 2^40, 2^53, 2^66), which the note never ties to the decoder's passing radius R0=ceil(t_star/(2E)), and at R0 inequality (4) certifies only k=22, 87 and 332/327, which I recomputed. They disagreed only on A's extra gap that 'add |H|' should be a multiplicative factor. I dropped it as a wording slip, because the note's own worked catalogue charges 4e-8 instead of 2e-8 for |H|=2, which fixes the multiplicative meaning. All other claims hold.

## Claims

### 1. gap

> On typical native labels this does not produce a sufficiently short point

- Step: 1. Decision (headline scope)
- Finding: The certificate covers witnesses of norm <=R with R=2^40, 2^53, 2^66, which equals 2*sqrt(dq) at the three references; the note never shows R is the decoder's passing radius. The rotational decoder accepts up to R0=ceil(t_star/(2E)) = 1478681177790966 (about 2^50.4) at d64, about 2^69.5 at d256 and about 2^89 at d1024 (research/certificates/native_rlwe_subfield_cover_bounds.json). Rerunning inequality (4) at R0 certifies only k=22, 87 and 332 (327 elliptical), not 44/193/796. Sparse witnesses with support 23-44 at d64 and norm in (R,R0] are not excluded. Section 6 lists larger radii as out of 
- Conceded by the note's own self-check: no

### 2. holds

> Then v is a uniform UNIT ring vector and T is a uniform ring multiplication matrix INDEPENDENT of v

- Step: 2. Distribution And Exact Finite Bound
- Finding: v=bar(a1)^-1 is uniform on units, and for each fixed a1 the map a2->a2/a1 is a bijection of R_q, so T is uniform and independent of v.
- Conceded by the note's own self-check: no

### 3. holds

> Subtracting independent T*y is convolution of probability laws and cannot increase the maximum point probability

- Step: 2. Distribution And Exact Finite Bound
- Finding: With q an odd prime (stated) and t!=0, t*v has maximum point mass 1/#R_q^*; convolution with an independent law cannot raise it. The union over at most N_d(R) residues, S_(d,k)(R) choices of y and q-1 labels gives (1), including adaptive choices.
- Conceded by the note's own self-check: no

### 4. holds

> Thus with probability at least 1-(1-p_U)-2e-8 under the stated input law

- Step: 4. Entirely Integer Reference Certificates
- Finding: This follows from (2) with beta<=1e-8 from (4). The swapped-block case conditioned on a2 a unit plus the explicit 1-p_U charge gives (2). For the two-entry catalogue the note charges 4e-8, which is the correct multiplicative |H| factor. Judge A's gap on the wording 'add |H|' at Section 3 was dropped as a wording slip this worked instance resolves.
- Conceded by the note's own self-check: no

### 5. holds

> EVERY radius-R scalar-syndrome witness has MORE THAN k nonzero coefficients in EACH original block

- Step: 4. Entirely Integer Reference Certificates
- Finding: I recomputed inequality (4) exactly with the reference moduli: the largest passing k are 44, 193 and 796 at R=2^40, 2^53, 2^66, each failing at k+1. Valid as stated at radius R; the scope problem is the headline, not this sentence.
- Conceded by the note's own self-check: no

### 6. holds

> is a unit at ALL THREE saved d^12 references, checked exactly by 2^d+1!=0 mod q

- Step: 3. Sparse Either Block, And Fixed Unit Polynomial Syndromes
- Finding: Res(X+2, X^d+1)=2^d+1 for even d, and I checked pow(2,d,q)+1 != 0 mod q at the three moduli 4722366484553272393819, 79228162514320210376421021211 and 1329227995784916208980425653176240211.
- Conceded by the note's own self-check: no
