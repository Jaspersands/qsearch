# Audit of the coordinate and sparse-basis interface for the tagged-U batch schedule

**Scope.** This audit covers only the coordinate and sparse-basis interface: §2 of `compiler-sections-2-4.md`, the parts of §5 step 4, §7 and §8 that touch coordinates, and the coordinate routine of `2026-11-13-tagged-tower-conditional-composition.md`. It does not audit scheduling, witness-shortening, ERH gluing or payload counts.

**Assumptions taken as given** (labelled [A]; nothing is promoted from them):
- **[A1] Operation 1.** The exact pair sequence, kernel ⟨([d],0)⟩ and surjectivity, as in review §2.
- **[A2] Operation 2.** The bound on N(M), as in review §3, eq. (3).
- **[A3] Operation 3.** The square-reset bound, as in review §3, eq. (4).
- **[A4] Children.** Every child returns a complete pair basis of its stated presentation.

## 0. Verdict

- **No counterexample exists to the sparsity and rank assertions.** They are elementary linear-algebra theorems once the tag image is identified, and I prove them below.
- **The normalization map is a genuine group isomorphism.**
- **The coordinate recursion is a binary tree of depth ≤ h.** Presentation dimensions grow additively along it, and query heights obey L ≤ N·(L₀+P\*). There is no exponential recursion and no cyclic or unbounded call circuit.

The interface as written is not correct without four amendments. One is a false statement and three are missing