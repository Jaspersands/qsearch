# Referee review: NATIVE_RLWE_QUATERNION_KERNEL_AUDIT

Note: `research/NATIVE_RLWE_QUATERNION_KERNEL_AUDIT.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges rated the note sound and agreed on every claim; my rechecks agree. For q = 3 mod 8 and d >= 4, R/qR = E x E with conjugation swapping the factors, so a real nonzero residue is a unit and the Hamilton gate forces M*bar(M) = -1; the compatible count |E|-1 of |E|^2 matches the artifact (8/81, 120/14641, 80/6561) and the exponents 2304/12288/61440 equal (d/2)log2 q. The left-ideal closure, the always-principal basis with determinant q^d, the d2/q257 bound ||g||^2 >= 15870 against the norm-5 relation (-1,2) (256 = -1 mod 257), and the norm-one unit classification check. I also checked the mixture weight: a product of two uniform field elements is uniform with weight 1-1/|E| plus a point mass 1/|E| at zero, exactly as stated, and 4v/mu^2 ~ 0.1008 at d64 gives about 0.899 > 0.89. Judge A's remark that step 2 could get h in R directly from J(M,1) in R^2 is a shorter route, not a defect.

## Claims

### 1. holds

> Such a J exists if and only if M*bar(M)=-1 mod q

- Step: 2. Strong Original-Metric Gate, steps 1-5
- Finding: Unitarity plus Z*bar(Z) = -I gives Z^T = -Z, so Z = [0,h;-h,0]. q = 3 mod 8 has order d/2 mod 2d and -1 is not in <q>, so conjugation swaps the two CRT factors and the real residue beta is either 0 or a unit; q^d | Norm(beta) forces beta = 0. J_0 gives the converse. Both judges agree.
- Conceded by the note's own self-check: no

### 2. holds

> For IID full-ring public ratios the compatible count is |E|-1 among |E|^2

- Step: 2. Strong Original-Metric Gate, probability
- Finding: For each nonzero a in E there is a unique b with a*tau(b) = -1. Artifact exhaustive counts 8/81, 120/14641, 80/6561, and the d2/q3 exception 4/9. Both judges agree.
- Conceded by the note's own self-check: no

### 3. holds

> Lambda_M is a LEFT O_rho ideal because rho+M*bar(M)=0 mod q

- Step: 3. An Explicit Definite Quaternion Order
- Finding: (a,b)*(Mf,f) = (aMf - rho*b*bar(f), af + b*bar(M)*bar(f)); first minus M times second is -(rho + M*bar(M))*b*bar(f) = 0 mod q. Both judges agree.
- Conceded by the note's own self-check: no

### 4. holds

> Thus EVERY principal generator is much longer than the available relation

- Step: 4. Always Principal Does Not Mean Useful
- Finding: rho = 257 - 16384 = -16127; nrd = +/-257 since the index is 257^2; f = 0 forces q | g; otherwise ||g||^2 = nrd + 16127||f||^2 >= 15870, against (-1,2) of norm 5 (256 = -1 mod 257). Both judges agree.
- Conceded by the note's own self-check: no

### 5. holds

> At d64 the conservative bound exceeds 0.89

- Step: 5. Distortion Is Unavoidable For This Entire Lift Class
- Finding: lambda_max(C_rho)^2 >= trace(C_rho^2)/d = ||rho||^2 >= S; Chebyshev gives Pr[S >= mu/2] >= alpha*(1-4v/mu^2), and 4v/mu^2 ~ 0.1008 at d=64, so about 0.899. The mixture weights 1-1/|E| and 1/|E| are exact for a product of independent uniform field elements. Both judges agree.
- Conceded by the note's own self-check: no

### 6. holds

> Thus searching these units cannot shorten a fixed-reduced-norm generator

- Step: 6. Norm-One Units Do Not Improve Fixed-Norm Generators Here
- Finding: C_rho >= I with ||g||^2 + f^T C_rho f = 1 forces a single signed monomial block; equal-norm generators of one principal left ideal differ by a norm-one unit, and these preserve physical length. Artifact counts 128 (d64) and 4 (d2). Both judges agree.
- Conceded by the note's own self-check: no
