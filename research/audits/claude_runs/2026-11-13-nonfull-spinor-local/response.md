# Review of the nonfull-spinor two-move theorem

## Verdict

**I found no counterexample.** I did not find an isometric pair with proper H for which `12(x), 23(z)` fails.

The local theorem holds as a deduction from a short list of source theorems. It needs two repairs:

- one missing justification in Case 1;
- one source-dependence that the visual PDF check does not cover: a strict inequality in Lemma 1.7.1(i), used in Case 3.

The full-H skip also checks out: no transporter is needed at that place.

## A. Source assumptions versus deductions

Everything below is deduced only from these source inputs.

- **S1.** Beli Theorem 3.1, the ternary classification:
  - (ii) d(a₁b₁) ≥ α₁ and d(a₁a₂b₁b₂) ≥ α₂;
  - determinant and Hasse invariants agree;
  - (iv) if α₁+α₂ > 2e, then b₁ is represented by [a₁,a₂].
- **S2.** Good-BONG validity:
  - m, n ≥ −2e;
  - m + d(C) ≥ 0 and n + d(D) ≥ 0, hence h, k ≥ 0;
  - m+n ≥ 0;
  - R_i are isometry invariants.
- **S3.** Lemma 1.4.11: property A plus failure of property B gives full H. The property-B inequalities are as visually corrected.
- **S4.** Corollary 1.4.10(ii): G(a_{i+1}/a_i) ⊆ θ(O⁺(L)). This is in the excerpt.
- **S5.** The Section 1.7 dichotomy: without property A, H is F* or O*F*². The excerpt does not quote this. It does support it: an L′ without property A and without hyperbolic splitting has full image, and θ(O⁺(πʳA(0,0))) contains O*F*².
  - Only "H proper ⇒ H ⊆ O*F*²" is needed.
  - That follows from "H ⊇ O*F*²", because [F* : O*F*²] = 2.
- **S6.** Lemma 1.7.1(i): G(π^g ε_iε_{i+1}) ⊆ O*F*² iff g is even and either d(−ε_iε_{i+1}) = 2e or d(−ε_iε_{i+1}) > e − g/2, **strict**. See Section E for why this matters.
- **S7.** Standard Hilbert-symbol facts:
  - if d(a)+d(b) > 2e, then (a,b) = 1;
  - the unramified unit class pairs trivially with every unit.
- **Interface, accepted as reviewed:** move ij(η) is legal iff η ∈ U_threshold ∩ N(−a_i a_j). The threshold is h(·) for edge 12 and k(·) for edge 23, evaluated at the current pair.

## B. Preliminary checks (proved)

**1. Hasse identity (2).** I expanded the difference of Hasse invariants between ⟨a₁,a₂,a₃⟩ and ⟨a₁x, a₂xz, a₃z⟩:

(a₁a₂(−1), x) + (a₂a₃(−1), z) + (x,z) = ⟨C,x⟩ + ⟨D,z⟩ + ⟨x,z⟩. ✓

**2. Agreement with Beli's full α_i.** Beli's α₁ also contains the term m+n+d(D), and the note's min(h, m+k) includes it. The extra term e+m+n/2 in min(h, m+k) is never smaller than e+m/2, since m+n ≥ 0. The same holds for α₂ by symmetry. So the note's α_i equal Beli's. ✓

**3. Classification gives the defect bounds.**
- d(x) ≥ α₁ follows from S1(ii).
- Determinant matching gives b₂/a₂ ∼ xz, so d(a₁a₂b₁b₂) = d(z). Hence d(z) ≥ α₂.

**4. Endpoint thresholds.**
- After 12(x), the 23-threshold is k(x) = K(d(Dx)).
- The target's own edges are C_target ∼ Cz and D_target ∼ Dx.

**5. Final rescaling.** b₂/(a₂xz) = (b₁b₂b₃)/(a₁a₂a₃) · (xz)⁻², which lies in O*². Unit rescaling of BONG vectors preserves the BONG.
- Repair (cosmetic): each move's realization may also introduce unit-square factors on *any* coordinate, not only the middle one. All of these are harmless for the same reason.

## C. Case-by-case audit

### Case 1: m > 2e, or symmetrically n > 2e

- Since d(C) ≥ 0 and m > 2e, we get m + d(C) > e + m/2, so h = e + m/2 > 2e.
- **Repair.** The note asserts α₁ > 2e without justification. The missing step is that k ≥ 0 (S2), so m + k ≥ m > 2e. Hence α₁ > 2e, so d(x) = ∞ and x is a square.
- α₂ = k because n + h = e + n/2 + (m+n)/2 ≥ e + n/2 ≥ k. Also k(x) = k since x is a square.
- Hasse then gives ⟨D,z⟩ = 0, and d(z) ≥ α₂ = k. So 23(z) is legal.
- Symmetric case n > 2e:
  - h ≥ 0 gives n + h > 2e, so α₂ > 2e and z is a square.
  - α₁ = h, since m + k > m + 2e ≥ e + m/2 ≥ h, using m ≥ −2e.
  - Hasse gives ⟨C,x⟩ = 0, so 12(x) is legal.
  - 23(z) then has d(z) = ∞ ≥ k(x), with ⟨Dx,z⟩ = ⟨C,x⟩ = 0 by the Hasse identity.
- Case 1 does not use H. ✓

### Case 2: m, n ≤ 2e and R₁ < R₃

- Property A holds, so S3 gives: H proper ⇒ property B.
- Under the corrected definition, a gap is *triggered* if it is odd and ≤ 2e+1, or even