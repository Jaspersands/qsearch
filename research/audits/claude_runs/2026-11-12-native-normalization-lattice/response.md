# Review: polynomial-bit free integral bases for a growing-degree plane curve via Δ-denominators + local jets

## 0. Verdict (one line)

**Not falsified; closed modulo exactly one height obligation.** Every structural step of the proposed route is correct and is proved below with explicit degree/row/column/bit bounds (trace containment, spanning of B/A[y] by reduced numerators, K-linearity of integrality, exact stopping order, direct-sum residue algebras, a free basis without Hermite normal form, multiplication tables, the infinity chart with the correct exponent, and Laurent transition matrices). The single thing not proved here is that the truncated branch jets at the places over roots of Δ have polynomial *bit* height — an explicit Eisenstein-type bound. The supplied Kozen text does **not** prove it (its "coefficients remain small" is unquantified; its §5 analysis counts tree size only), the naive propagation along the resolution tree gives an exponential bound, and the archimedean half is proved here. The non-archimedean half is a known theorem in the literature (named below, **not in the supplied evidence**, must be retrieved and matched). No finite controls were run (no tools).

Notation: d = deg_y F, D = total degree, H = log height of F, h = [K:Q] with charged multiplication table, Δ = disc_y F ∈ K[x], δ := deg Δ ≤ (2d−1)D ≤ 2D², A = K[x], R = A[y] = A[Y]/(F), B = integral closure of A in K(C). Heights of Δ: Δ is a (2d−1)×(2d−1) Sylvester determinant, so h(Δ) ≤ (2d−1)(H + log(D+1)) + log((2d−1)!) = O(D(H + log D)).

---

## 1. Cheapest decisive attacks on the route — all fail (route survives)

**1.1 Trace containment [PROVED].** B ⊂ Δ⁻¹R. Let b ∈ B, b = Σ_{i<d} c_i y^i, c_i ∈ K(x). Tr(b y^j) ∈ A for all j (b y^j integral). With T = (Tr(y^{i+j}))_{i,j}, det T = Δ ≠ 0 (