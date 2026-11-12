# Source-scope audit: native tilted-walk OPI note vs. 2609.40088v1 excerpts

## 0. Verdict

**Closed, narrow conclusion, subject to five repairs (R1–R5 in §4).**

- **MAX-k-CSP import.** The note does not use Lemma 3.3's `L = O(1/n)`, the hypercube value `ω = 1/n`, the Pauli-mixer claim, or any MAX-k-CSP comparison. No improper import appears in its equations.
- **Free normalizer.** The obstruction does not need a free normalizer. It does not use `ν` in any essential way.
- **Free target.** It does not need a free target either. `γ` is certified by a verified Prange codeword, and `Gmax ≤ 1` holds trivially for `G = 1/2 + H/(2m)`.

The note has three real scope defects:

1. Its "same slope" restriction does not cover the max-normalized scores the source most plausibly intends.
2. The "computable" Section 7.3 normalizer is not computable for the native chain. It needs a certified LSI constant `ω`, and none exists.
3. Two source conventions are used silently and need explicit statement: the meaning of `D(P)` and whether `L2(G)` is a root or a square.

None of these reverses the conclusion. Each narrows or re-justifies what is covered.

---

## 1. Cheapest decisive check: the source's own guarantee is trivial in this family

This needs no paired-walk lemma.

Substitute (121) into the boost factor in (120). The `n` cancels:

```
2^{κn/2} = exp( b*(A0−μ)·E_{π_S}[log(G/(1−ρ))] / (3L) ),   A0 = 1−ρ−L.
```

The bound on the exponent follows from three inequalities:

- `A0 − μ ≤ Gmax − μ =: Γ`, because `S` must contain a point with `G ≥ 1−ρ`.
- `V ≥ s r² Γ²`, from the note's (REG).
- `L ≥ s r Γ / Gmax`.

Write `ω̄` for the proved basis-vector upper bound on any valid `ω`; §2 gives its value. Then

```
b* ≤ 4ω²(A0−μ)/V ≤ 4ω̄²/(s r² Γ)
```

and the exponent is at most

```
4ω̄² ln(1/(1−ρ)) / (3 s² r³ Γ)  =  O(Λ^{-2})     (since ω̄ = O(s/Λ)).
```

**Consequence.** Take `T = X`, the uniform start, so `π(T) = 1`. Then (120) promises only

```
|⟨S|C|X⟩| ≥ ((η−ρ−L)/η) · (M+1)^{-1} · √π(S) · (1 + O(Λ^{-2})).
```

That is no better than uniformly sampling `S`, up to a polynomial factor. This kills the source-certified admission. It is a statement about the guarantee only. Whether the actual output is sampleable classically remains the paired-walk lemma's job, which is not repeated here.

**Tightening of the note.** The note's (TILT) dropped a factor `(A0−μ) ≤ Γ`. Correctly:

```
b*·M ≤ 4[ln(1/(1−η))/(r³Γ²) + s/(r²Γ)]/Λ².
```

The note had `γ³`. Its version is valid but looser.

---

## 2. Item-by-item check against the supplied text

| Item | Supplied source text | Note's usage | Status |
|---|---|---|---|
| **Condition 3.4 operator** | `⟨ψ\|D\|ψ⟩ ≤ 1 − ωEnt_π(r_ψ)` with "D(P)". `D` is undefined in the excerpts. The filter uses "D + bG", so `D` acts on functions on `X`. | Uses `P_s` itself. | **Unknown.** Equivalent only if `D(P)` is the discriminant `√(P(x,y)P(y,x))`, which equals `P_s` for symmetric `P` with uniform `π`. If `D` were a doubled-space Szegedy operator, the basis-vector test must be redone. (R1) |
| **Entropy convention** | `r_ψ = μ_ψ/π`, `Ent_π(r_ψ)`. Log base not shown. `κ` contains `log 2`. Hypercube `ω = 1/n` is asserted. | `Λ = log D`, base unspecified. | My deduction: Gross's inequality for the walk `P = (1/n)Σ flips` is tight at `α = 1/n` in natural log. So the source's `ω = 1/n` claim is consistent only with natural log (it would be false in base 2 by a factor `ln 2`). Not textually confirmed. **Repair: use `ω̄ := 3s/(2kt)`**, which bounds every valid `ω` in both conventions (natural: `s(1−1/q)/(kt ln2)`; base 2: `s/(kt)`). The basis-vector test itself is correct: `⟨x\|P_s\|x⟩ = 1 − s(1−1/q)` and `Ent = log D`. |
| **`L2(G)` convention** | "upper bound on the one-step quadratic variation". But (65)–(66) use `G − PG ≤ (Σ_y P(G(x)−G(y))²)^{1/2} ≤ L2(G)`, (62) scales `L2(G)` linearly in `1/Rc`, and (119) and (343) use `L2(G)²`. | Puts `V ≥ max_x Σ P_s(ΔG)²` where the source has `L2(G)²`. | Consistent with the root reading, which (66) and (62) require internally. Under the opposite (squared) reading, `b* ≤ 4ω̄²/(s²r⁴Γ³)` and `b*M = O(1/(sΛ²))`. The note's "arbitrary laziness" then fails as `s → 0`. **Repair: restrict to `s ≥ s_min` constant** to cover both readings. (R2) |
| **Theorem 4.6 `b*`** | (119), as printed. | `b* = min(1, (√(1+8ω²A0(A0−μ)/V) − 1)/A0)`. | Matches under the root reading. `b*` is increasing in `ω`, so the upper bound `ω̄` suffices. Correct. |
| **Theorem 4.6 `M`** | (118): `M = max_{x∈S} ⌈log(G(x)/(1−η))/L⌉`. | `M ≤ log(1/(1−η))/(srγ) + 1`. | Correct, but uses `G ≤ 1`. For trials with `G` up to `3/2`, replace with `log(G_ub/(1−η))`. |
| **`maxG = 1`** | Lemma 3.3: `G` "defined by (50)", `Rc = Hmax + Ac`, slope `1/(2Rc)` by (64), `G ≥ 1/2` in (67). Equation (50) itself is **not supplied**. Theorem 4.6's statement as excerpted does not list `maxG = 1`. | Uses `1/2 + H/(2m)`, whose max is `1/2 + Hmax/(2m)`, and claims "not an unproved extension when maxG<1". | **Internal tension.** If (50) forces `maxG = 1` (unknown), the simple score is in scope only if `Hmax = m`. That is plausible by first moment, `q^k·2^{-m} → ∞`, but unproved: no second moment has been done. **Repair: the scale-trial family `G_h` in §3**, which contains the max-normalized score at `h = Hmax`. (R3) |
| **Unknown `Hmax` / Section 7.3** | Section 3 says "Section 7.3 discusses the unknown optimum and normalization parameters". Lines 3051–3120 show only the normalizer replacement. | "analysis convention or ... paid parameter trials". | How the source handles unknown `Hmax` is **unknown** from the excerpts. The existence of source parameter trials is **unverified**. |
| **Computable normalizer** | (343): `E_b^ub = 1 + bμ_G + b²L2(G)²/(8ω²)` from "known upper bounds" `μ_G`, `L2(G)`. Implicitly also needs a valid `ω`. | "pays a computable replacement". | **Not computable for native `P_s`.** No certified lower bound on `ω` exists. Plugging in `ω̄` gives a value below `E_b^ub`, which is invalid as a normalizer. The certified alternative `ν ≥ 1 + b·G_ub` needs no `ω`. Within this prescription it costs at most `e^{bM} = 1 + O(Λ^{-2})`. (R4) |
| **`T`** | `Tη ⊆ T`, with `Tη` undefined in the excerpts. | "uniform codeword state". | Must be stated as `T = X`. Any smaller `T` needs separate paid preparation and is not covered. (R5) |
| **Source executability** | `b*` itself needs `ω`. | — | For the native chain, Theorem 4.6 is not an executable prescription at all. This matters only for a positive claim; the obstruction covers any valid `ω`. |

The note's own derivations check out:

- DRIFT uses only one-row marginals. This is correct even though all outside-`A` rows are driven by a single `z` and are therefore jointly correlated.
- REG uses Jensen conditional on the `P0` branch. Correct.
- The Prange identity is correct: `H(c) = k + Bin(m−k, 1/2)`, with Hoeffding tail `exp(−k²/(8(m−k)))` and `Γ ≥ k/(8m)`.

---

## 3. Explicit rational score and parameter-trial contract

**Preprocessing (classical, paid).**
- Run up to `P` Prange completions: choose `k` rows, pick accepted values, interpolate, evaluate all `m` rows.
- Keep `c0` with `H0 := H(c0) ≥ ⌈m/2 + k/4⌉`.
- Abort probability is at most `exp(−P·k²/(8(m−k)))`.
- Cost per completion: `O(k²)` field operations, `m` evaluations, `m` table lookups.
- Set `r := (m−k+1)/m`.

**Trial indices.** All grids are finite and polynomial in size.

1. **Laziness.** `s ∈ S_grid 