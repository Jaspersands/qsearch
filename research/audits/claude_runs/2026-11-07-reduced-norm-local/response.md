# Audit: monic irreducible degree‑n polynomial over a local field with prescribed constant term

## Verdict

The lemma holds as stated, with three qualifications:

- **Randomised algorithm.** The residue step is Las Vegas, so the work bound is in expectation.
- **No Newton theorem needed.** For both the exact and the perturbed polynomial, irreducibility follows from a short elementary root‑valuation argument plus an e·f degree count. Ore's theorem is not required.
- **Wild ramification is harmless.** The argument never uses tameness or separability, so p | e causes no problem.

I found no counterexample.

## 1. Cheapest falsification attempts (finite checks, not proof)

| Case | Construction | Result |
|---|---|---|
| ℚ₂, n=2, c=2 (wild, p=e=2) | v=1, k=0, g=1, e=2, h=1, φ=Y+1 | P = X²+2, Eisenstein, irreducible |
| ℚ₂, n=2, c=3 | v₀=0, g=2, φ=Y²+Y+1 | P = X²+X+3; discriminant −11 ≡ 5 (mod 8), non‑square, so irreducible |
| ℚ₂, n=2, c=−1 | same φ | P = X²+X−1; discriminant 5, non‑square in ℚ₂, so irreducible |

Two edge cases also survive:

- **v < 0.** Then k < 0 and P has non‑integral coefficients. P is still monic, irreducible, and in F[X]. If integral coefficients are required, v ≥ 0 is forced anyway, since the constant term of a monic integral polynomial is integral.
- **g = 1.** Then φ = Y + ū₀ with ū₀ ≠ 0, which is automatically irreducible.

## 2. The construction is well‑formed (elementary)

Setup: v₀ ∈ [0, n−1] and gcd(h, e) = 1. In the degenerate case v₀ = 0 we have h = 0 and e = 1.

Expanding P = π^{kn} P₀(X/π^k):

P = Σ_{j=0}^{g} u_j · π^{(h+ke)(g−j)} · X^{ej}.

- **Monic:** the j = g term is X^n with coefficient 1.
- **Constant term:** u₀ · π^{v₀+kn} = c exactly.
- **Integrality:** P ∈ O_F[X] when v ≥ 0.
- **Sparsity:** only g+1 coefficients are nonzero.

## 3. Irreducibility proof (elementary)

Set s* = v/n = k + h/e. Write the coefficients of a possibly perturbed P̃ as a_i, with:

- **(A)** a_n = 1 and a₀ = c exactly;
- **(B)** v(a_i) > s*(n−i) for 0 < i < n with e ∤ i;
- **(C)** v(a_{ej} − u_j π^{(h+ke)(g−j)}) > (h+ke)(g−j) = s*(n−ej) for 0 < j < g.

The exact candidate satisfies (A)–(C) trivially.

**Step 1: every root has valuation s\*.** Let α be a root and s = v(α). Each term satisfies v(a_i α^i) ≥ s*(n−i) + s·i.

- If s < s*, the term X^n has valuation ns. Every other term exceeds it by at least (s*−s)(n−i) > 0. A unique strict minimum cannot cancel, so this is a contradiction.
- If s > s*, the constant term has valuation s*n, and every other term exceeds it by at least i(s−s*) > 0. Same contradiction.

Hence s = s*.

**Step 2: ramification.** In lowest terms s* has denominator exactly e. The value group of F(α), normalised so v(π) = 1, therefore contains 1/e. So the ramification index satisfies e(F(α)/F) ≥ e.

**Step 3: residue degree.** Let β = α^e / π^{h+ke}. Then v(β) = 0. Dividing the equation P̃(α) = 0 by π^v gives

Σ_j u_j β^j + (terms of positive valuation) = 0.

The remaining terms have positive valuation by (B) and (C). Reducing mod the maximal ideal gives φ(β̄) = 0. Since φ is irreducible of degree g, the residue degree satisfies f(F(α)/F) ≥ g.

**Step 4: degree count.** We get n = eg ≤ e·f ≤ [F(α):F] ≤ n. So P̃ is irreducible. The resulting extension has ramification index e and residue degree g.

## 4. Sufficient coefficient precision

It suffices to know coefficient i (for 0 < i < n) modulo π^{⌊v(n−i)/n⌋+1}, with the leading coefficient and the constant c exact. A simpler uniform sufficient condition is precision π^{max(v,0)+1}.

In the construction itself the u_j can be fixed finite representatives, so no precision loss occurs.

## 5. Residue‑polynomial argument (checked, elementary)

**Roots and fibre.** Let a = ū₀ ≠ 0. A monic irreducible φ of degree g with φ(0) = a has as roots exactly the g conjugates of some θ ∈ F_{q^g} that has full degree g and norm N(θ) = (−1)^g a. The norm map is surjective, so this fibre has H = (q^g−1)/(q−1) elements.

**Subfield intersection.** Take d | g with d < g and θ ∈ F_{q^d}. Then N_g(θ) = N_d(θ)^{g/d}. The equation y^{g/d} = b has at most g/d solutions y ∈ F_q^*, and each fibre of N_d has size (q^d−1)/(q−1). Every proper subfield lies in some F_{q^{g/ℓ}} with ℓ a prime dividing g. Hence the number of bad elements is at most Σ_ℓ ℓ(q^{g/ℓ}−1)/(q−1).

**Bad fraction ≤ 2/3.**

- **g prime:** bad fraction ≤ g/(1+q+…+q^{g−1}) ≤ g/(2^g−1) ≤ 2/3.
- **g = 4:** bad fraction ≤ 2/(q²+1) ≤ 2/5.
- **Composite g ≥ 6:**
  - The sum of distinct prime divisors of g is at most their product, which is at most g.
  - Since g/ℓ ≤ g/2 for every prime ℓ | g, each term satisfies (q^{g/ℓ}−1)/(q^g−1) ≤ 1/(q^{g/2}+1). This also holds for odd g, as real numbers.
  - So the bad fraction is ≤ g/(2^{g/2}+1), which is decreasing in g and equals 2/3 at g = 6.

**Probability.** There are at least H/(3g) good polynomials among q^{g−1} candidates. So the probability is at least (1+q+…+q^{g−1})/(3g·q^{g−1}) ≥ 1/(3g). The argument is correct.

## 6. Cost accounting

**Assumptions that must be charged or granted:**
- an exact uniformiser π;
- exact representation of c, plus a valuation oracle;
- exact division by π;
- an explicit model of F_q;
- random bits.

**Work:**
- **Integer steps:** computing v, k, v₀ and the gcd costs poly(log n, log |v|).
- **Residue step:** expected O(g) trials. Each trial is an irreducibility test (Rabin or Ben‑Or) costing poly(g, log q). This is Las Vegas.
- **Output:** g+1 nonzero coefficients. Storing π‑exponents as integers, this is poly(n, log |v|, input size). Writing π^v out digit‑by‑digit would cost v, which matches the size of c in that representation.

**What is not claimed:** this gives no deterministic version. Deterministic construction of irreducible polynomials over F_q for large p is not provided here.

## 7. Falsifiers

The result would be refuted by any of the following:

- a perturbed polynomial satisfying (A)–(C) that factors;
- an error in the bound on the fibre's intersection with a maximal subfield F_{q^{g/ℓ}};
- a value g ≥ 6 with g/(2^{g/2}+1) > 2/3, which is impossible since the function is monotone decreasing.

None of these occurs, and Sections 3 and 5 prove the claims rather than relying on the finite checks.