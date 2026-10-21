# Referee review: NATIVE_RLWE_IDEAL_CLASS_ORBIT_AUDIT

Note: `research/NATIVE_RLWE_IDEAL_CLASS_ORBIT_AUDIT.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The classification holds: saturation makes alpha a unit of O_0, the cited signature theorem plus the coefficient trace leave only v*X^k and v*X^k*j, and these act as M->X^(2k)M and M->-M^-1; the count G/(2d)+1 and the d4/q3 and d8/q3 controls (56 in 8 classes, 6320 in 396) reproduce. Judge A rated the note sound; judge B added one gap, that the title drops the generic-source restriction, the q prime 3 mod 8 condition and the review-pending dependency. I kept B's gap because the title reads as a statement about all native quaternion ideal classes, while Section 1 restricts to M and beta units and the note itself says no claim about arbitrary classes follows. All other claims the two judges marked holds survived my check, including an independent re-enumeration of the d4/q3 orbits.

## Claims

### 1. gap

> Native Quaternion Ideal Classes: Public Dihedral Orbits

- Step: Title (headline scope)
- Finding: The title presents native quaternion ideal classes in general as public dihedral orbits. The classification in Sections 1-3 holds only on the generic source (M a unit and beta=1+M*bar(M) a unit mod q), with q prime 3 mod 8 and d>=4 a power of two, and it rests on the review-pending saturation step and the cited unit-signature theorem. Native ratios outside that source, such as the x-1 unit ratios with norm -1 and nonunit M, are not classified. The title needs the generic-source restriction.
- Conceded by the note's own self-check: no

### 2. holds

> two native fractional left O_q ideals are equivalent if and only if their ratios belong

- Step: 1. Question and Answer / 2. Global Equivalence Proof
- Finding: Necessity: O_0*Lambda_M=O_0 because Lambda_M+j*Lambda_M contains qO_0 and the columns (M,1),(-1,bar M) with determinant Norm(beta) coprime to q, so alpha is a unit of O_0. Right X^k sends (g,f) to (gX^k,fX^-k), ratio X^(2k)M; right j sends (g,f) to (-f,g), ratio -M^-1. Sufficiency follows because these units transport the lattice. Both judges agreed.
- Conceded by the note's own self-check: no

### 3. holds

> So alpha is a UNIT of O_0, not an arbitrary small quaternion or local unit

- Step: 2. Global Equivalence Proof
- Finding: O_0=O_0*alpha gives alpha in O_0 and 1=beta*alpha with beta in O_0. The subsequent reduction to v*X^k or v*X^k*j uses the published signature theorem, which the note discloses in Section 5.
- Conceded by the note's own self-check: no

### 4. holds

> Number of classes represented by generic native source = G/(2d)+1

- Step: 3. Exact Source Counts
- Finding: Rotations act freely; reflection fixed points force z=M/l with z^2=1 and norm z=1, and with conjugation swapping the two CRT factors only z=+/-1 survive, so only the 2d signed monomials have a stabilizer and form two orbits of size d. That gives (G-2d)/(2d)+2. Divisibility holds because q=3 mod 8 has order d/2 mod 2d, so x=q^(d/2)=1 mod 2d.
- Conceded by the note's own self-check: no

### 5. holds

> Complete controls: d4/q3 gives56 ratios in8 classes (two size4, six size8

- Step: 3. Exact Source Counts
- Finding: My own enumeration of F_3[X]/(X^4+1) gives 56 generic ratios in orbits {4:2, 8:6}. Both judges also reproduced d8/q3 (6320 ratios, 396 classes, {8:2, 16:394}). These match artifact complete_finite_source_orbits, and the d64 orbit size 128=2d matches same_saved_native_d64_kernel.orbit_size.
- Conceded by the note's own self-check: no

### 6. holds

> These transports are signed coefficient isometries. Thus equivalent native ideals admit a CHEAP EXACT isometry

- Step: 2. Global Equivalence Proof
- Finding: Right X^k and right j permute and sign coefficients, and the central unit v fixes the lattice (v*Lambda=Lambda), so equivalent ideals in this family are related by an explicit signed coefficient permutation.
- Conceded by the note's own self-check: no
