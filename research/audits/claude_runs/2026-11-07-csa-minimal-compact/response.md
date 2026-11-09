# Review of §§3–4: the extraction lemma survives, with corrections

## Verdict

I found no fatal flaw in the §3 extraction. Both predicted ranks are correct theorems, not sampled observations. Consistency holds, and the Schwartz–Zippel bound for `f` is valid. The modular pivots are only ever used as one-sided nonzero witnesses, so the step needs no zero test and no arithmetic-circuit PIT.

The extraction is classical and zero-error given the contract: every non-ABORT output is correct, and ABORT has bounded probability. Four statements need correction or boundaries:

1. **"Canonical" is only transcript-relative.** The output depends on the grid sample `c` and on which pivot sets the random primes expose. An input-canonical choice, such as lexicographically first pivots, would require certifying that earlier minors vanish. That is a zero test on compact data, which is exactly the PIT the note disclaims. The defensible claim is a deterministic reconstruction from a recorded transcript.
2. **The no-zero-test claim moves the zero-test burden onto ρ.** Both rank upper bounds, and hence `e² = e`, are proved only if ρ is exactly a unital homomorphism. If ρ's multiplicativity were established by modular spot checks, exactness reverts to bounded-error PIT. If ρ is wrong, the extraction can silently output a non-idempotent. The KM certificate must prove multiplicativity, which the brief treats as a separately paid contract.
3. **Primitivity depends on the classical index lower bound.** The existence of ρ only proves `ind(A) | d`. Stage 3's predicted rank `m·d'²` matches for any `d'`, so it cannot detect a wrong `d`.
4. **The fresh-prime bound is cited, not shown.** §4 defers to "reduced-norm note §6", which I have not seen. A self-contained bound is given below. Modular evaluation must also reject primes dividing any denominator in the DAG, including Cramer denominators certified at earlier primes.

There is no left/right error:
- The intertwining equation `L_b f = f R_b` is correct for `f(ρ(b)v) = b·f(v)`.
- `l_j e = l_j` is the correct right-identity equation for a left ideal.

There is no representation blowup beyond polynomial DAG size. The cost is polynomial but heavy, dominated by Berkowitz on an `s₁ = RN−N ≤ m²n³d` matrix.

## Attack log (cheapest first)

| Attack | Result |
|---|---|
| Is V simple? (dimension count) | Survives. Any nonzero unital A-module has K-dimension a multiple of `n·ind`. `dim_K V = nd` and `ind ≥ d` (classical) together give `ind = d` and V simple. |
| Does ρ need to be F-linear, or unital? | Only the unital K-algebra action on V is used. For an F-algebra homomorphism `A⊗F → M_n(F)`, unitality is automatic if ρ ≠ 0: the source is simple, so ρ is injective onto `M_n(F)` by dimension. |
| Stage-1 rank `RN−N` | Survives. Q-linear maps commuting with all `L_b` are automatically K-linear, since `K·1 ⊂ A` is central. Hence the kernel equals `Hom_A(V,A)`. Since `A ≅ S^r`, `dim_K Hom_A(S^k, A) = k·r·d² = dim_K S^k`. So the kernel has Q-dimension N. |
| Circular upper rank? | No. The upper bound uses only (contract ρ) + (CSA promise). The certified minor gives the lower bound. The kernel of the selected rows has dimension N and contains Hom, so it equals Hom. |
| Full-column-rank `f` | Survives. An injective A-map `V → A` exists. A minor nonzero at that map is a nonzero degree-N polynomial in `c`. On a grid of size 4N, P(zero) ≤ 1/4. |
| Stage-3 rank `m·d²` | Survives. Kernel of `e ↦ (l_j e)_j` on `L = Ae₀` is `{e ∈ Ae₀ : e₀e = 0} = (1−e₀)Ae₀`. So rank = `dim_Q e₀Ae₀ = dim_Q D^op = m·d²`. |
| Consistency | Survives. `e₀` itself solves. Rank-ρ rows span the row space and `[M|c]` has rank ρ, so the pivot solution satisfies all equations. |
| Hidden PIT | None in the extraction. Zero identities are theorems; modular tests only certify nonzero. Bounded randomized EquSLP (coRP) is used only in its sound direction. |
| Canonicity | Fails as an input-canonical claim (Correction 1). |
| Wrong d, or a non-hom ρ | Undetected by the extraction (Corrections 2 and 3). A one-sided detector exists; see Falsifiers. |

## Corrected lemma (classical, Las Vegas)

**Inputs (contract).**

- **(I1) K and A.** K is given by a Q-basis `ω_1..ω_m` with an exact multiplication table. A is given by a K-basis `a_1..a_{n²}`, structure constants, and identity. Promise: A is a central simple algebra of degree n.
- **(I2) The index.** An integer `d | n` with an externally paid proof that `ind(A) ≥ d`.
- **(I3) The module.**
  - A rational arithmetic DAG Γ of size τ with leaf bit-height ≤ h.
  - Γ computes rational N×N matrices `R_b`, with `N = mnd`, for a Q-basis `b` of A (`R = mn²` elements).
  - **Contract C.**
    - `b ↦ R_b` is a unital Q-algebra homomorphism `A → M_N(Q)`.
    - Every inverse node of Γ has a nonzero input.
  - C is proved upstream (KM small-atom certificate), not tested here.

F and ρ's F-structure are irrelevant beyond supplying Γ.

**Output.** Either ABORT, or the following:
- a transcript `𝒯`: pivot index sets, grid vector `c`, primes, and residues;
- DAGs for `e` and for `l_1..l_N`;
- the action matrices `R_b`.

These satisfy all of the following:
- `e² = e`;
- `Ae = span_Q{l_j}` is a minimal left ideal;
- `b·l_j = Σ_k (R_b)_{kj} l_k`.

**Guarantees.**
- Under the contract, every non-ABORT output is correct.
- P(ABORT) ≤ η.
- Bit cost is `poly(τ, h, m, n, log 1/η)`.
- Given `𝒯`, the DAGs are deterministically reconstructible.
- A third party can recheck every nonzero certificate in polynomial time.
- The output is not unique and not an input-canonical function.

## Proof

**Algorithm.**

- **S1.** Assemble the `(R²N)×(RN)` matrix `M₁` of `L_b f − f R_b = 0`. Draw a fresh prime and run Gaussian elimination mod p.
  - If rank_p = `RN−N`, record the pivot sets `(I₁, J₁)`.
  - If the rank is lower, retry with a new prime.
  - If any evaluated node has a denominator ≡ 0 mod p, discard that prime.
- **S2.** Let `k_1..k_N` be the Cramer kernel basis scaled by `Δ₁ = det M₁[I₁,J₁]`. These are division-free adjugate columns via Berkowitz. Sample `c ∈ {1..4N}^N` and set `f = Σ c_i k_i`. Draw a fresh prime and seek a nonzero N×N minor of `f`. If none is found, resample `c`.
- **S3.** Set `e = f(y)`. Assemble the `(NR)×N` system `l_j f(y) = l_j`. Draw a fresh prime and find a nonzero `m·d²` minor `Δ₃`. Set the nonpivot entries of `y` to 0 and solve by Cramer, with the single scalar inverse `Δ₃⁻¹`.

**S1 correctness.**
- Unitality of ρ makes V a unital module, so `V ≅ S^k`.
- The index lower bound (I2), together with `dim_K V = nd`, gives `k = 1` and `ind = d`.
- The kernel of `M₁` is `Hom_A(V,A)`, of Q-dimension N (shown above), so `rank M₁ = RN−N`.
- If the mod-p evaluation is a valid ring reduction, a nonzero mod-p minor implies a nonzero rational minor.
- Rows `I₁` therefore have rank `RN−N`, and their kernel has dimension N and contains Hom, so it equals Hom.

**S2 correctness.**
- The certified N-minor makes `f` injective.
- `f` is A-linear, so `L = f(V)` is a left ideal with `dim_K L = nd`. It is minimal because `L ≅ V`.

**S3 correctness.**
- The system is consistent, with `e₀` a solution.
- Its rank is exactly `m·d²`, as shown above. The certified minor makes the pivot rows a basis of the row space, so the Cramer solution satisfies every equation.
- Then `Le = L` and `e ∈ L` give `e² = e` and `L ⊆ Ae ⊆ L`, so `Ae = L` is minimal and `e` is primitive.
- The action follows from `b·f(v_j) = f(R_b v_j)`.
- Edge cases: `d = n` gives `e = 1`; `d = 1` gives the column ideal.

**Fresh-prime clock (self-contained).**
- **Height bound.** Take a stage DAG G with T nodes and leaf height ≤ h. Adding or multiplying two fractions with numerator and denominator of ≤ S bits gives ≤ 2S+1 bits; inversion swaps them. Hence every node has ≤ `S* = 2^T(h+1)` bits.
- **Bad primes.** Let Z be the product of the target minor's numerator and all node denominators. Then `log₂Z ≤ (T+1)S*`. At most `log₂Z / log₂Y` primes greater than Y divide Z.
- **Probability.** Draw a uniform prime from `(Y, 2Y]` by random integers plus AKS, with a capped number of trials whose failure is charged. Using a standard explicit prime-count bound (Rosser–Schoenfeld type: at least `Y/(2 ln Y)` primes for Y ≥ an absolute `Y₀`), P(bad) ≤ `3(T+1)S*/Y`.
- **Prime size.** Choose `log₂Y ≈ T + log(T+1) + log(h+1) + log(1/ε) + 2`, which is polynomial.
- **Conditioning.** Each stage's DAG is fixed before its prime is drawn. So the bound holds conditionally on all history (earlier primes, pivots, `c`). DAG sizes are capped in advance, so Y can be fixed in advance.
- **Retries.** S2 succeeds with probability ≥ 3/4 − ε per trial, so `O(log 1/η)` trials suffice. A union bound over the polynomially many prime draws completes the argument.

**Size.**
- `T ≤ τ + O(s₁⁴ + N·s₁³ + N³R + (md²)⁴)`, with `s₁ = RN−N`.
- This is polynomial, though large: about `m⁸n¹²d⁴` Berkowitz nodes.

## Boundaries and proof obligations

1. **Contract C is a theorem, not a test.** The homomorphism property must be proved exactly: from the LS cochain identity on small expanded atoms, plus a proof that the canonical reconstruction of ρ preserves multiplication. This lemma inherits any gap there.
2. **(I2) is required.** Without `ind ≥ d`, the output is an idempotent of a possibly non-minimal ideal. The extraction cannot tell the difference.
3. **"Canonical" means transcript-determined.** Removing the dependence on randomness needs either zero certification (PIT) or a separate canonicalization theorem.
4. **Classical only.** No quantum step occurs in §3. All quantum cost sits in producing Γ.
5. **No size promise.** The expanded coordinates of `e` may have exponentially many bits. Only the DAG is polynomial.
6. **Promise violations are not recognized.** If A is not a central simple algebra, or C is false, the output is unspecified.

## Falsifiers

**One-sided checks of the lemma's preconditions.** These are optional and sound only for detecting contract violations.
- A nonzero `(RN−N+1)`-minor of `M₁` mod p proves the contract or promise is false.
- A nonzero `(md²+1)`-minor of the S3 system mod p proves the same.
- A nonzero residue of `e² − e` mod p proves the same.

**Falsifiers of the lemma itself.**
- An explicit central simple algebra and an exact homomorphism ρ for which `dim Hom_A(V,A) ≠ N` would refute the lemma; the theorem above rules this out.
- A proof that C cannot be certified without zero-testing compact power products would move the PIT objection upstream, not into §3.