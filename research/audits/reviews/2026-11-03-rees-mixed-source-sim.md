# Rees mixed spectral source substituted into the core: exact simulation (item 9), 2026-11-03

AI session only; human review still required. Scope: `rem:mixed-source` in
`docs/papers/rees-hsp/main.tex` (its sentence "This extension is argued, not simulated"), and
`research/REES_MIXED_SPECTRAL_SOURCE.md` §§2–4. This answers the second "Still missing" item of
`2026-11-02-rees-cited-notes.md`.

Artifacts: `theorems/rees_mixed_source_sim.py` (imports `theorems/rees_end_to_end_sim.py`,
which was not edited) and `tests/test_rees_mixed_source_sim.py`. Fast suite: 57 passed and
2 skipped in about 25 s. `REES_MIXED_SLOW=1` runs every n4(F_5) case (72 passed, 130 s). Full report:
`python -m theorems.rees_mixed_source_sim --out report.json` (183 s; the JSON was not committed
because this row may write only the two files above).

## Verdict

**No counterexample.** The substitution works on every instance tried. On 61 nonflat states,
for 17 hidden subgroups of Heis(F_3), Heis(F_5) and n4(F_5), 9 of them nonnormal, the
following hold:
- (i) holds at every offset;
- through the zero-moment design, the lifted source is exactly ρ_{exp(hlift)} in the
  ℓ → ∞ limit;
- the unchanged exact Rees core recovers log H in all 78 runs.

Four wrong sources fail exactly where the theory predicts. Two side findings are in §4.

## 1. Setting and access model

- G = (L, BCH), with L = Heis(F_3), Heis(F_5) or n4(F_5). The Rees cover, evaluations and
  core come from `rees_end_to_end_sim.py`. R is the **left-regular** representation on C[G],
  with d = |G| = 27, 125 or 625.
- The eigenvectors of ρ are H-eigenvectors with entries in Z[ζ_p]. The basic ones are the
  atoms u_{x,λ} = Σ_h ω^{−λ(h)} e_{h·x}, with λ a functional on L vanishing on [h,h]. Then
  R(h)u = ω^{λ(h)}u, checked exactly. Profiles:
  - A: (2/5, 1/4, 1/4, 99/1000, 1/1000). It has a degenerate pair, a tail below w, and the
    top two eigenvectors are u_a ± u_b on two cosets.
  - B: (1/2, 3/10, 1/5), with r̄ = rank + 1.
  - C: (41/100, 2/5, 19/100). The 1/100 gap is below w = 1/96, so the offset decides
    whether the two top eigenvalues share a flag level. This gives two distinct flag sets.
  - D: the p atoms on H·z^k·x₀ (z central, z ∉ H), combined by a Helmert matrix, with
    weights (p, …, 1)/(p(p+1)/2). z fixes the full flag but no smaller one, so
    0 < |φ(z^m)| < 1 and σ_ℓ ≠ ρ_{H̃} at finite ℓ.
- The promise δ is the measured minimum TD (float), rounded down to 1/64 (capped at 1/2)
  or to 1/4096. Every promise is true. The grid is w = δ/(16r̄), J = ⌈1/w⌉, β = 1/2, and
  M₀ = 64 or 128.
- **Reference access.** The spectrum and eigenvectors are supplied so the ideal Ψ can be
  built. The rank learner, the DME threshold instrument and the growth instrument of (ii)
  are not simulated. The family is classically easy: H can be read off the atoms. Nothing
  here is an application.

## 2. What was checked, with labels

| Claim | Check | Label |
|---|---|---|
| B-formula, 0 ≤ B ≤ ρ, Tr(ρ−B) < δ/8, nested flags, K ≤ r̄, Σr_l ≤ min(r̄(r̄+1)/2, 16r̄/δ) | every offset of every case; brute force over all J thresholds when J ≤ 5000 | exact |
| #offsets with a threshold within w/(4M₀) of the spectrum ≤ r̄ | every case (observed at most 2, with r̄ ≥ 3) | exact |
| ray stabilizer of Ψ = H | φ_l(g) = det(B_l†R(g)B_l)/Π‖v_i‖², tested as N = ζ^k·D in Z[ζ_p] for all g ∈ G and every distinct flag set; \|φ\| = 1 forces a p-th root of unity, since R(g)^p = 1 | exact |
| phase on H = Π_l det(R\|_{ran Q_l}) | exponent of φ on H equals Σ_l Σ_{i∈Q_l} λ_i | exact |
| \|φ(g)\| ≤ 1 − δ²/8 off H | max observed 0.5, at least 0.497 below the bound | float |
| ⟨Ω\|R(g)^{⊗r}\|Ω⟩ = det(B†R(g)B)/det(B†B) | explicit antisymmetric tensors on Heis(F_3), r = 2, 3 (error 9e−16) | float |
| address density σ[a,b] = Π_s φ(E_s(b⁻¹∗a))/N | explicit controlled R^{⊗2}(E_s a) on a rank-2 wedge, target traced out, on the Heis(F_3) cover (error 3e−18); E_s(b⁻¹∗a) = E_s(b)⁻¹E_s(a) for all 81² pairs | float / exact |
| {x : E_s x ∈ Stab ∀s ∈ S} = exp(hlift), and in-coset phase ≡ 0 | all x ∈ G̃ (order 81, 625, 78125); designs (1,1,1,2,2,2), (1,2,3,4), (1,2,3,4) | exact |
| core on the ideal source returns log H, with every stage output = ρ_{H_d} and every label law uniform on K_d^⊥ | 78 runs (one per distinct flag set, at most 3 per case) of the unchanged `ExactBackend`, no oracle calls | exact |
| finite ℓ: TD(σ_ℓ, ρ_H̃) ≤ √N(1−γ)^ℓ/2, top-label TV ≤ TD, `DenseBackend` core recovers | Heis(F_3)/(F_5), ℓ = 1, 4, 16, 64 | float |

Finite-ℓ detail (profile D, Heis(F_3), H = ⟨x⟩). TD(σ_ℓ, ρ_H̃) is 0.118, 2.2e−4 and 2e−14 at
ℓ = 1, 4 and 16. Recovery succeeds even at ℓ = 1, where the largest stage-output TD is 0.152.
The bound √N(1−γ)^ℓ/2 is vacuous (> 1) at every ℓ tried, because γ = δ²/8 ≈ 0.003; the true
decay is far faster. Profiles A–C with single atoms give φ = 0 exactly off H, so their σ₁
already equals ρ_H̃. Profile D exists to avoid that degenerate case.

## 3. Negative controls (all match their prediction)

Every smallest failing instance below is on Heis(F_3), H = ⟨x⟩ (nonnormal) unless stated.

1. **Whole-support wedge** (the withdrawn shortcut). ρ has p eigenvectors R(z^k)u, with
   eigenvalues spaced 1/2000 apart. The single support wedge has ray stabilizer ⟨x, z⟩ at
   all 64 offsets. The core returns log⟨x,z⟩ = span{x, z}, not log H. The same happens at
   p = 5.
2. **Overstated δ** (promise 1/2; the true gap is 0.001 at p = 3 and 0.002 at p = 5). At 57
   of 64 offsets (87 of 128 at p = 5) rounding merges the levels, z fixes every flag, and the
   core returns span{x, z}. With the true δ (1/1024, 1/512) the same state passes at every
   offset. This confirms the remark's "the global gap cannot be dropped".
3. **No design**: Ψ through the c-point lift (1, …, c). The predicted outcome is the moment
   sum Σ_j (Σ_s s^j) λ_Ψ(h ∩ γ_j). The smallest failure is Heis(F_3), H = Z(G): the in-coset
   phase is nonzero. Heis(F_3), H = ⟨x⟩ **passes**, as predicted (Σs ≡ 0 and h ∩ γ₂ = 0).
   At p = 5 both subgroups fail, and recovery is also wrong.
4. **Two offsets inside one design block** (profile C, offsets 0 and 24, flag ranks (3,2,1)
   and (3,2)). Each offset alone cancels the phase. Alternating them across the design
   points does not, so the stage outputs are wrong and recovery fails. This confirms "the
   same offset must be used for every copy".

Mutation tests: a character inserted on the grade-one part of the correct support breaks the
stage outputs (H = ⟨x⟩ on Heis(F_5)).

## 4. Side findings

- **A phase error on the top central grade is invisible to recovery.** For H ≤ Z(G) on the
  Heisenberg group, a wrong in-coset character lives only on t²·z. The first central
  instrument measures it out. Every stage output is still ρ_{H_d}, and log H is still
  recovered. Only the label law (no longer uniform on K_d^⊥) shows the error. See control 3
  at p = 3 and `test_tampered_top_center_phase_is_caught_only_by_the_label_law`. This does
  not contradict the paper, which claims uniform label laws for the correct source. It does
  mean that "recovers log H" alone is too weak as a falsifier for source phases; the label-
  law check is needed. Schedule 3 uses the uniform law, so there a wrong phase would matter.
- The δ²/8 gap is loose on this family: the largest off-H overlap is 0.5 against bounds
  ≥ 0.97. This is no evidence about tightness in general.

## Exact statement that now holds

*Exact finite computation, AI-checked, pending human review.* Take L = Heis(F_3), Heis(F_5)
or n4(F_5), R the left-regular representation, and the 61 listed states with exact
rational spectra (ranks 3 and 5, nonflat, including degenerate, near-degenerate and below-w
eigenvalues) and true promises δ. Then:
- for every offset a ∈ {0, …, M₀−1}, the identities of `rem:mixed-source`(i) hold, and the
  ray stabilizer of Ψ is exactly H with phase Π_l det(R|_{ran Q_l});
- with the public zero-moment design, the ℓ → ∞ address density is exactly ρ_{exp(hlift)};
- the exact Rees core run on it returns log H, with every intermediate source equal to
  ρ_{H_d} and every label law uniform on K_d^⊥.

At finite ℓ, a float run of the core on σ_ℓ recovers log H for ℓ ≥ 1 on the Heisenberg
covers. This is a finite check only. It proves nothing for other groups, representations or
states.

## Still missing

- Part (ii): the copies-only rank learner, the DME threshold instrument, and growth from the
  filtered nonflat states ρ_l. Nothing here touches them; the spectrum is reference access.
- An exact (not ℓ → ∞) run at finite ℓ, together with a whole-run hybrid bound. The float
  stage-output TDs are conditional on the sampled labels and are not the hybrid quantity.
- Human review; a family with a proved global gap, polynomial rank and a nonnormal H that is
  not classically trivial; non-permutation representations.

## Claim gates that must stay false

`speedup_claim_allowed`, `novelty_established`, `native_application_established`,
`quantum_receiver_implemented`, `circuit_generator_implemented`,
`nonflat_conjugation_symmetry_covered`, `whole_rees_correctness_certified`, and every Rees
candidate or proof promotion. `mixed_spectral_source.json` is unchanged.

## Proposed paper text

Target: `rem:mixed-source`, the paragraph after the remark. Replace the sentence
"This extension is argued, not simulated." with the text below. The status label is
"argued" for the general extension and "exact finite computation, AI-checked, pending human
review" for the simulation.

```latex
This extension is argued in general. The artifact \file{theorems/rees_mixed_source_sim.py} (report \file{research/audits/reviews/2026-11-03-rees-mixed-source-sim.md}; exact finite computation, AI-checked, pending human review) runs it on the Heisenberg groups over $\mathbb{F}_3$ and $\mathbb{F}_5$ and on $\mathfrak{n}_4(\mathbb{F}_5)$, with $R$ the left-regular representation, for $61$ nonflat states and $17$ hidden subgroups, $9$ of them nonnormal. It builds the ideal $\Psi$ from the supplied spectrum, so it tests~(i) and the substitution, not the instruments of~(ii). For every offset it checks exactly in $\mathbb{Z}[\zeta_p]$ that the ray stabilizer of $\Psi$ is $H$ with phase $\prod_l \det(R(\cdot)|_{\operatorname{ran}Q_l})$. Through the zero-moment design, the lifted source then has support $\exp(\hlift)$ and trivial in-coset phase, and the unchanged exact core of the end-to-end simulation returns $\log H$ in all $78$ runs, with every intermediate source equal to $\rho_{H_d}$ and every label law uniform on $K_d^\perp$. In floating point, the core run on the address density at $\ell = 1$, which lies at trace distance $0.12$ from $\rho_{\exp(\hlift)}$, already recovers $\log H$. Four wrong sources fail as predicted. For $H = \langle x\rangle$ in the Heisenberg group over $\mathbb{F}_3$, the whole-support wedge and an overstated $\delta$ both give a stabilizer containing $Z(G)$ and return $\log\langle x, z\rangle$. Omitting the design, or mixing two offsets within one design block, leaves a nonzero in-coset phase exactly when $\sum_j \sum_s s^j\lambda_s(\hh\cap\gamma_j(\mathcal{L})) \ne 0$, where $\lambda_s$ is the phase functional of the copy used at the point $s$. The family has a classical solution and supplies no application.
```

Optional, same paragraph, after "the global gap cannot be dropped":

```latex
A wrong phase supported on the top central grade is measured out by the first central instrument and does not change the recovered subgroup; only the uniform label law, which Schedule~3 uses, detects it (exact finite computation, same report).
```
