# Referee review: CONJUGATE_CHIRP_REPAIR

Note: `research/CONJUGATE_CHIRP_REPAIR.md`. Reviewed 2026-10-22 by audit-correction-2026-10-22. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges agreed that the bilinear identity, the Kloosterman/Salie coordinate bound, the Fourier mean bound, the joint-moment tail certificate and the REJECT decision hold, and the quoted numbers match the artifact (p101,n16 advantage bound 9.87e-6; order-16 tail bound 9.99e-10). Both flagged the z=0 efficiency sentence; I confirmed it from the producer (A^2=max(rho/(1-rho),(1-rho)/rho), degree allowed up to m): 'bounded list densities' does not give H<=exp(O(n)) and no restriction on ell is stated. The judges disagreed on 'vanishes rapidly as p,n grow': B called it a gap because eta=1 for p<=17 and the n=1 bound does not vanish. I kept it as holds: the sentence is asymptotic in joint growth of p and n, the vacuity at p<=17 is explicit in eta=min(1,...), and fixed n=1 is not growth in n.

## Claims

### 1. gap

> m=Theta(n), bounded list densities and p>=m+1, H<=exp(O(n)) but p^n grows as exp(Omega(n log n

- Step: Projecting The Extra Register To Zero Does Not Repair Efficiency
- Finding: The producer sets A^2=max(rho/(1-rho),(1-rho)/rho) (theorems/conjugate_chirp_repair.py, postselection_bound), so H<=(1+A^2)^m=exp(O(n)) needs list densities bounded away from 0 and 1. Every density is trivially bounded, so 'bounded' states no condition. For singleton lists rho=1/p, A^2=p-1 and H>=binom(m,ell)(p-1)^ell. The bound is stated for arbitrary degree ell (the code accepts ell up to m), so with ell>=n the ratio H/p^n need not be small. The 'not polynomial' conclusion needs either densities in [delta,1-delta] or ell<=(1-Omega(1))n, and the note states neither.
- Conceded by the note's own self-check: no

### 2. holds

> With r=x-z, u=x+z (a bijection in odd characteristic

- Step: Proposed Constructive Mechanism
- Finding: For symmetric C, (x+z)^T C (x-z)=x^T C x-z^T C z, and (x,z)->(x-z,x+z) is invertible because 2 is a unit mod odd p. Both judges agree.
- Conceded by the note's own self-check: no

### 3. holds

> Native x-marginal purities range0.074..0.201, and fidelity with the intended pure quadratic target ranges0.112..0.323 on these controls

- Step: What The Receiver Actually Prepares
- Finding: Artifact native_controls give purities 0.0743-0.2006, target fidelities 0.1118-0.3230, linear-DQI purity 1 to 1e-15 and nonsquare-q probabilities 0.602, 0.738 and 0.753, matching '60%..75%'. Both judges agree.
- Conceded by the note's own self-check: no

### 4. holds

> EXPECTED satisfied-fraction advantage over this legal classical baseline vanishes rapidly as p,n grow

- Step: Diagonal Heuristic: Uniform Expected-Score Falsifier
- Finding: Judge B's gap was dropped. eta=min(1,4sqrt(p)/(p-1)) is below 1 only for p>=19, so the bound is vacuous on the three diagonal native controls (artifact advantage uppers 17/20, 25/28, 29/40; the rank-one controls store no such bound). The sentence, however, is an asymptotic statement under joint growth of p and n, and for p>=19, n>=2 the bound sqrt((p-1)rho(1-rho))eta^n plus the classical term sqrt((p-1)rho(1-rho))p^(-n/2) tends to 0. The n=1 counterexample keeps n fixed. The stored p101,n16 bound is 9.87e-6, below 1e-4 as stated.
- Conceded by the note's own self-check: no

### 5. holds

> arbitrary fixed s makes constant-gap success negligible against any fixed polynomial repetition budget

- Step: Separate Tail Falsifier For The Same Diagonal Readout
- Finding: The Vandermonde zero-block count, the |a|+|b|<=2 reduction, the (2m)^k delta_k comparison, the symmetrization and the (2s-1)!! m^s moment all check, and Markov gives the displayed certificate. With p>=m+1 and log p polynomial in n, the dependence term is exp(-Omega(n log n)/s) and the first term is O(m^-s). The artifact's order-16 control at n1024,m2048,p65537 stores a tail bound of 9.99e-10, below 1e-6. Both judges agree.
- Conceded by the note's own self-check: no

### 6. holds

> REJECT this proposal as a same-target quadratic-DQI repair

- Step: Resources, Failure Decision And Next Science
- Finding: The exact identity shows the output is P(sum g_i(u^T C_i r)), not the single-register target, independently of the six controls. The decision is scoped to same-target preparation and creates no broad negative. Both judges agree.
- Conceded by the note's own self-check: no
