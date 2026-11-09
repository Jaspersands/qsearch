# Rees core composition: independent proof check, steps 1–2

Date: 2026-11-01. Reviewer: Claude Code (Opus 5.5, high effort), one side session.
Brief: `research/REES_CORE_PROOF_CHECK_BRIEF.md`. This file covers §3 steps 1 and 2 only.
Steps 3–5 are left to a second session, which should add its sections below §4 of this file.
The claim is still not established: steps 3–5 are open, and nothing here has had human review.
I changed no other repository file.

Checked text: `docs/papers/rees-hsp/main.tex` as corrected on 2026-10-31 (Definition 159,
Theorem 223, Lemma 241, Lemma 283, Proposition 299, Lemma 326, Proposition 370, §4.2 at 394),
and `research/REES_HSP_REDUCTION.md` §§2–4 (lines 60–184).

Scripts (outside the repo, in the session notes folder, so the checkout stays untouched):
`/Users/jaspersands/Library/Application Support/Claude/side-session-notes/local_82ea8e9d-f8c7-4b78-b5f6-291cbf4bed0b/rees_steps_1_2/`
(`liealg.py`, `step1_check.py`, `step2_check.py`). They were written from scratch for this check.
Their only repo import is a read-only cross-check against `theorems/uniform_bch_rees.py:bch_via_ode`.
`git status --short` was identical before and after the runs.

Reproduce:

```bash
cd "/Users/jaspersands/Library/Application Support/Claude/side-session-notes/local_82ea8e9d-f8c7-4b78-b5f6-291cbf4bed0b/rees_steps_1_2"
```
```bash
/opt/anaconda3/bin/python -u step1_check.py
```
```bash
/opt/anaconda3/bin/python -u step2_check.py
```


## 1. Step 1: tuple group and BCH transport, general class c < p

**Verdict: Holds.** Evidence: a written proof (below, standard Lazard theory), plus exact
machine checks on ten algebras with 2 ≤ c ≤ 6, including the boundary case c = p − 1.
The general-class BCH/Lazard transport is still outside Lean, as the paper says.

### 1.1 Exact claim

Let p be prime and L ≅ F_p^m a Lie algebra over F_p of nilpotency class exactly c, with
1 ≤ c < p. Let G = (L, ∗) be the group with the BCH product truncated at degree c. Let H ≤ G be
**any** subgroup and h = log H (as coordinates, h = H). Define A = ⊕_{k=1}^c t^k γ_k(L) ⊂ L[t]
with [t^i x, t^j y] = t^{i+j}[x,y], G̃ = (A, ∗), the evaluations E_s(Σ t^k x_k) = Σ s^k x_k and
the dilations δ_λ(t^k x) = λ^k t^k x. Then:

1. A is a Lie algebra of class exactly c, its top grade t^cγ_c(L) is central, and G̃ and G are
   groups of class c. Every E_s (s ∈ F_p) is a group homomorphism G̃ → G, onto when s ≠ 0.
   Every δ_λ (λ ≠ 0) is an automorphism of G̃, and E_s ∘ δ_λ = E_{λs}. Also
   E_s(⊕_{j≥k} t^jγ_j) = γ_k(L) = log γ_k(G) for s ≠ 0.
2. h is an F_p-linear Lie subalgebra of L (Lazard), for every subgroup H, normal or not.
3. h̃ = ⊕_k t^k(h ∩ γ_k(L)) is a Lie subalgebra of A. exp(h̃) is a subgroup of G̃, preserved by
   every δ_λ with λ ≠ 0, and h̃ = ∩_{s∈F_p^×} E_s^{-1}(h). For any c distinct nonzero
   s_1, …, s_c, it also equals ∩_i E_{s_i}^{-1}(h).
4. Tuple oracle: for a, b ∈ G̃, (f(E_{s_i}(a)))_i = (f(E_{s_i}(b)))_i if and only if a^{-1} ∗ b ∈ exp(h̃).
   Here f is any function with f(x) = f(y) ⇔ x^{-1} ∗ y ∈ H (left cosets, as in Definition
   `main.tex:159`).
5. For 1 ≤ d ≤ c, I_d = ⊕_{k>d} A_k is a graded ideal. The projection G̃ → G_d = (A/I_d, ∗) is a
   group homomorphism, and the top grade of A/I_d is central and elementary abelian (this is
   used in step 2).

### 1.2 Proof

*(a) BCH over F_p in class c < p.* In the Dynkin formula, every term of total degree N has
coefficient (−1)^{n−1}/(n·N·Π r_i! s_i!) with n ≤ N. So the degree-≤c truncation BCH_c is a Lie
polynomial with coefficients in Z[1/c!]. Associativity, BCH_c(x, 0) = x and BCH_c(x, −x) = 0 hold
in the free nilpotent Lie algebra of class c over Q. Both sides of each identity are Z[1/c!]-Lie
polynomials, because substituting such polynomials into one another keeps the coefficients in
Z[1/c!]. The free class-c nilpotent Lie ring over Z[1/c!] is a free module (Hall basis) and embeds
in its Q-form, so the identities hold over Z[1/c!]. Since c! is invertible mod p, L is a
Z[1/c!]-algebra, and specialising gives the identities in any class-c Lie algebra over F_p.
Hence (L, ∗) and (A, ∗) are groups. Any Lie homomorphism φ commutes with every Lie polynomial,
so φ(x ∗ y) = φx ∗ φy. Because x^k = kx for the BCH product, G has exponent p. This is the
standard Lazard setting (Lazard 1954; Khukhro, *p-Automorphisms of Finite p-Groups*, Ch. 9–10).
The paper's one-line proof of Theorem 223(iii) (`main.tex:235`) states the homomorphism half and
leaves the group-law half to "because c < p". That is acceptable with a citation; see §3, item 1.

*(b) Cover facts.* [γ_i, γ_j] ⊆ γ_{i+j}, and γ_{i+j} = 0 when i + j > c, so A is closed under the
polynomial bracket. That bracket is genuinely zero in degrees above c, not truncated. A k-fold
bracket has t-degree at least k, so γ_{c+1}(A) = 0. Lifting a nonzero c-fold bracket of L to t·L
shows the class is exactly c. E_s is the restriction of the evaluation L[t] → L, hence a Lie
homomorphism. The identity [E_s t^i x, E_s t^j y] = s^{i+j}[x,y] needs [x,y] = 0 when i + j > c,
which holds because [x,y] ∈ γ_{i+j}. E_s(tx) = sx gives surjectivity. δ_λ is a graded
automorphism, and E_s δ_λ = E_{λs}. All of these pass to the groups by (a).
E_s(⊕_{j≥k} t^jγ_j) = Σ_{j≥k} γ_j = γ_k, and γ_k(L) = log γ_k(G) by Lazard.
For (5), [A_i, I_d] ⊆ I_d because grades only increase. The quotient bracket is the A-bracket with
degrees above d discarded, so the projection is a Lie, hence group, homomorphism. A_d is central
modulo I_d because [A_i, A_d] ⊆ A_{i+d} ⊆ I_d. On central elements BCH is addition, so the top
grade is elementary abelian.

*(c) Lazard linearity.* For class < p, the Lazard correspondence maps subgroups of G bijectively to
Lie subrings of L: additive subgroups closed under [ , ] (Khukhro, Thm 10.13). Its proof uses the
inverse BCH (Zassenhaus) formulas, which write x + y and [x, y] as group words in x, y with
Z[1/c!]-rational exponents. These are defined in a finite p-group and keep H closed. An additive
subgroup of an F_p-vector space is an F_p-subspace, so h is F_p-linear. Nothing here uses
normality of H or any intersection with the lower central series.

*(d) h̃.* For homogeneous elements t^i x, t^j y with x ∈ h ∩ γ_i and y ∈ h ∩ γ_j, the bracket
t^{i+j}[x, y] has [x, y] ∈ h ∩ γ_{i+j} (zero if i + j > c). By bilinearity, h̃ is a subalgebra, so
exp(h̃) is a subgroup by (a). δ_λ multiplies each graded piece by a scalar, so it preserves h̃.
Write C = Σ t^k C_k with C_k ∈ γ_k. If every C_k ∈ h, then E_s(C) ∈ h for all s. Conversely, the
c conditions Σ_k s_i^k C_k ∈ h use the matrix (s_i^k), which is diag(s_i) times a Vandermonde
matrix and so invertible. It needs c distinct nonzero points, which exist because p − 1 ≥ c.
Linearity of h then gives each C_k ∈ h.

*(e) Tuple oracle.* f(E_{s_i}a) = f(E_{s_i}b) ⇔ (E_{s_i}a)^{-1} ∗ E_{s_i}b ∈ H ⇔ E_{s_i}(a^{-1} ∗ b) ∈ h,
since E_{s_i} is a group homomorphism. Then apply (d). ∎

The paper's proofs of Theorem 223 and Lemma 241 (`main.tex:223–255`) and
`REES_HSP_REDUCTION.md:60–128` follow this argument and are correct. Dilation invariance is
proved for every H without using any intersection operationally. The intersections appear only
in the proof.

### 1.3 Machine checks (exact mod p; script `step1_check.py`)

Algebras: Heis/F3 and Heis/F5 (c = 2, and c = p − 1 at p = 3); filiform class 4 over F5
(c = p − 1); filiform class 5 over F7; Dixmier–Lister over F5 and F7, with the corrected table
from `main.tex` §2.3 (lower central dimensions (8, 4, 2), Jacobi verified); random Lie subalgebras
of strictly upper-triangular n_N, namely n4-sub/F5 (dim 4, c = 3), n5-sub/F7 (dim 4, c = 3), n6-sub/F7 (dim 8, c = 5) and n7-sub/F11 (dim 11, c = 6, lower central dimensions (11, 9, 8, 6, 3, 1)). For each algebra the script checks:

- Jacobi for L and A; class(A) = c; top grade central.
- My Dynkin-formula BCH against the repo's independent ODE BCH (`bch_via_ode`) on random pairs,
  in both L and A. For the matrix algebras, also against the matrix log(exp X · exp Y).
- Associativity, inverses, and x^k = kx for k ≤ p, on random elements of L and A.
- E_s is a Lie homomorphism on all basis pairs for every s ∈ F_p, a group homomorphism on random
  pairs, and onto for s ≠ 0. δ_λ is a Lie and group automorphism, E_s δ_λ = E_{λs}, and
  E_1(A_{≥k}) = γ_k.
- For every d, A/I_d satisfies Jacobi and the projection is a BCH homomorphism.
- Subgroups (Lazard): where p^m is small, the subgroup generated by 1–3 random elements (some with
  a central direction added) is enumerated by closure under ∗. Its log is checked to be a subspace
  equal to the Lie subalgebra generated by the same elements. Otherwise exp(h) is checked closed
  under ∗ on random pairs.
- h̃ equals the intersection over all s ≠ 0 of E_s^{-1}(h), and over the c points 1, …, c. These
  are exact linear-algebra intersections. h̃ is a subalgebra, δ-stable and BCH-closed.
- The tuple-fibre criterion on random pairs (a, a ∗ x), with x ∈ h̃, with x in the intersection
  over only c − 1 points (a near miss), and with x random.

Result: `FAILURES: 0` on all ten algebras (exit code 0, run 2026-11-01). No counterexample. Subgroups were enumerated by closure only where p^m ≤ 4·10^5 and the generated subalgebra has order ≤ 4000, which covers seven of the ten algebras. DL/F7, n6-sub/F7 and n7-sub/F11 were not enumerated. There, and for larger subgroups, the Lazard direction (subgroup ⇒ subspace) rests on the proof, not on enumeration.

### 1.4 What a human reviewer must still check (step 1)

- That the cited forms of Lazard's correspondence apply: subgroups ↔ Lie subrings for p-groups of
  class < p, and the Z[1/c!] denominator property of the degree-c BCH truncation. Both are textbook
  results, but the paper cites only Lazard 1954.
- Nothing in step 1 depends on finite tests. The checks only guard against a misread definition,
  such as the left-coset convention or the dilation exponents.

## 2. Step 2: measured channel and central descent, general class

**Verdict: Holds**, as a branchwise exact identity, for every finite group G, every central
elementary abelian Z, and every H with δ_s(H) = H. This covers every stage d = c, …, 2 of the
recursion and every c < p. Evidence: written proof (below); an exact cyclotomic group-algebra check
on the Dixmier–Lister cover at p = 5; a float check with explicit operators on the Heisenberg
covers at p = 3 and 5. It assumes a valid nonzero SDE witness exists for the observed labels.
Whether one exists, and at what arity and cost, is step 3.

### 2.1 Exact claims

Setting: G is any finite group; Z ≤ Z(G) is elementary abelian, written additively, with
characters χ_λ; H ≤ G; K = H ∩ Z; R_g|x⟩ = |x g^{-1}⟩; ρ_H = |G|^{-1} Σ_{h∈H} R_h (this is the mixed
left-coset state, with entries [u^{-1}v ∈ H]/|G|); Π_λ = |Z|^{-1} Σ_z χ_λ(−z) R_z.

- **(2a) Branch law, `main.tex:326`.** Pr(λ) = |K|/|Z| if λ ∈ K^⊥ and 0 otherwise. For λ ∈ K^⊥,
  ρ_λ = (|G||K|)^{-1} Σ_{h,z} χ_λ(−z) R_{hz}, and Tr(ρ_λ R_g) = χ_λ(z) when g = hz ∈ HZ, and 0 when
  g ∉ HZ. This holds for arbitrary K, including K = 1 and K = Z, with no normality or
  transversality.
- **(2b) Instrument.** The circuit "Fourier-prepare a Z ancilla, apply controlled R_z, inverse
  Fourier, measure λ" has Kraus operators exactly Π_λ.
- **(2c) Pointwise conversion, `main.tex:370`.** Suppose public automorphisms δ_s (s ≠ 0) preserve H
  and act on Z as z ↦ s^d z. Take fresh sources in the product state ρ_H^{⊗M}, measure each one's
  label, and choose any nonzero s ∈ F_p^M with Σ s_i^d λ_i = 0. Prepare the uniform
  **superposition** |Q|^{-1/2} Σ_q |q⟩ on Q = G/Z, apply controlled R_{δ_{s_i}(σ(q))} to each target
  with s_i ≠ 0, discard the targets with s_i = 0 untouched, and trace out all targets. For every
  positive-probability label tuple and every valid witness, the Q register is then exactly
  ρ_{HZ/Z}. Here σ is any set-theoretic section.
- **(2d) Independence.** Let R be the full classical record: labels, solver randomness, chosen
  witnesses, aborts and retries. The joint state of all records and stage outputs is
  Σ_R Pr(R) |R⟩⟨R| ⊗ ρ_{HZ/Z}^{⊗ n(R)}, where n(R) is the number of blocks that found a witness.
  Conditioned on **any** classical event (for example solver success), the outputs are still
  independent copies of ρ_{HZ/Z}. So each stage feeds the next stage fresh independent sources.
  The record may decide how many outputs there are, but not their state.
- **(2e) Recursion instance (§4.2, `main.tex:394`).** Take G_d = (A/I_d, ∗), Z_d = t^dγ_d(L) and
  H_d = exp(⊕_{k≤d} t^k(h ∩ γ_k)). The section σ inserts zero top coordinates. Then δ_s preserves
  H_d and acts on Z_d by s^d, K_d = t^d(h ∩ γ_d), and the labels lie in K_d^⊥ of rank
  a_d = g_d − dim(h ∩ γ_d). Also H_d Z_d / Z_d = H_{d−1} under G_d/Z_d = G_{d−1}, because a
  homogeneous subspace projects onto its lower graded pieces and hz = h + z for central z. So
  (2c) maps sources on G_d to sources on G_{d−1}, ending at (tL, th) after d = 2.

### 2.2 Proof

(2a) R is a representation, since R_g R_{g'} = R_{gg'}, and Z is central, so Π_λ commutes with
every R_h and is the χ_λ-isotypic projector: R_z Π_λ = χ_λ(z) Π_λ. Tr R_g = |G|·[g = 1], so
Tr(ρ_H Π_λ) = |Z|^{-1} Σ_{z∈K} χ_λ(−z), which gives the probability. Dividing ρ_H Π_λ by it gives
ρ_λ. In Tr(ρ_λ R_g), a term survives only when hzg = 1, that is g = h^{-1}(−z) ∈ HZ. Each
g ∈ HZ has exactly |K| decompositions, and they share one character value because λ ⊥ K. The
count cancels the 1/|K|.

(2b) ⟨λ|F^†|z⟩⟨z|F|0⟩ = |Z|^{-1} χ_λ(−z), so the Kraus operator is Σ_z |Z|^{-1} χ_λ(−z) R_z = Π_λ.

(2c) The state after the controlled actions is |Q|^{-1} Σ_{q,r} |q⟩⟨r| ⊗ ⊗_i U_q^{(i)} ρ_{λ_i} U_r^{(i)†}.
Tracing the targets gives entries |Q|^{-1} Π_i Tr(ρ_{λ_i} R_{δ_{s_i}(g)}), with g = σ(r)^{-1}σ(q).
This uses Tr(U_q ρ U_r^†) = Tr(ρ R_{δ(σ(r))}^{-1} R_{δ(σ(q))}) and the facts that δ is a homomorphism
and R a representation. Unused targets contribute trace 1. If g ∉ HZ, then δ_{s_i}(g) ∉ HZ for
every active i (δ_{s_i} is a bijection preserving HZ), and there is at least one active target, so
the entry is 0. If g = hz, then δ_{s_i}(g) = δ_{s_i}(h)·s_i^d z with δ_{s_i}(h) ∈ H, and by (2a) the
product is χ_{Σ s_i^d λ_i}(z) = 1. Since π: G → Q is a homomorphism with π^{-1}(HZ/Z) = HZ,
g ∈ HZ ⇔ r^{-1}q ∈ HZ/Z. The entry is therefore [r^{-1}q ∈ HZ/Z]/|Q|, which is ρ_{HZ/Z}. The proof
never uses K, a coset representative, the label law or the solver's choice among witnesses.

(2d) Instruments act tensor-wise on a product input, so the post-measurement cq-state is
Σ_λ Π_i Pr(λ_i) |λ⟩⟨λ| ⊗ ⊗_i ρ_{λ_i}. The solver is a classical randomized map of the record
alone. By (2c), the quantum output of a block is ρ_{HZ/Z} for every value of that block's record.
Blocks use disjoint fresh sources and channels that act only on their own block. So for every
full record the outputs form a product of copies of ρ_{HZ/Z}, and summing over records gives
(2d). This also justifies the paper's "solver retries reuse the same saved label list"
(`main.tex:407`). The traced-out targets may be entangled with the output, but they are never
touched again, so later stages see only the reduced state.

(2e) is the content of step 1, item (5), together with homogeneity of h̃.

**Oracle model and cleanup.** The controlled right actions are public: compute g = δ_s(σ(q)) from
q, replace the target x by x ∗ g^{-1} (a reversible bijection), then uncompute g. They use **no**
oracle calls. Oracle calls happen only when a lifted source is prepared. Prepare Σ_a |a⟩ on G̃,
compute each E_{s_i}(a) reversibly, query f into its own label register, and uncompute E_{s_i}(a),
which is a public linear function of the retained a. That is exactly c queries and no
uncomputation queries, because the labels are kept and then traced out. Tracing the labels gives
entries |G̃|^{-1}[f̂(a) = f̂(b)] = ρ_{exp(h̃)} by step 1(4). If a workspace E_{s_i}(a) were discarded
instead of uncomputed, it would act as a which-address record and destroy the coset coherence,
as the paper warns at `main.tex:254`. For copy input (Lemma 283), the i-th copy is acted on by
R_{E_{s_i}(a)}. The entry is |G̃|^{-1} Π_i Tr(ρ_H R_{E_{s_i}(b^{-1}a)}) = |G̃|^{-1} Π_i 1_H(E_{s_i}(b^{-1}a)),
which is ρ_{exp(h̃)} by step 1. That is c copies and no oracle. So "c oracle calls per lifted
source, or c copies" (`main.tex:83–92`) is correct for source preparation. All descent
operations are oracle-free.

### 2.3 Machine checks

**Exact (`step2_check.py` Part A, plus `step2_extra.py`), Dixmier–Lister cover at p = 5.** Here
dim A = 14 and (g_1, g_2, g_3) = (8, 4, 2). For each hidden subgroup, ρ_H Π_λ is multiplied out in
the right-regular group algebra using the actual BCH product; the code does not assume
h ∗ z = h + z, and checks it separately. Coefficients lie in Z[ω], stored as integer count
vectors in the basis 1, ω, …, ω^{p−2}, so all comparisons are exact. For **every** λ ∈ F_5^{g_d}
the script checks Pr(λ) = |K|/|Z| on K^⊥ and 0 off it. For every λ ∈ K^⊥ and every g ∈ HZ it
checks that Tr(ρ_λ R_g) is exactly χ_λ(z_g). It checks δ_s(HZ) = HZ, and the per-target identity
Tr(ρ_λ R_{δ_s(g)}) = χ_λ(s^d z_g) for all λ ∈ K^⊥, all s ∈ F_5^×, and all g ∈ HZ. The channel output
is then a product of these exact per-target values. On top of that, the script enumerates label
tuples and **all** nonzero witnesses and checks that the output equals the indicator of HZ. It
also checks σ(r)^{-1}σ(q) ∈ HZ ⇔ r^{-1}q ∈ H_{d−1} on 200 random (q, r) pairs per case, computed
in G_{d−1}.

| h generated by | stage | dim h̃ | dim K | a_d | M | label tuples | witnesses | bad |
|---|---|---|---|---|---|---|---|---|
| 0 (H = 1) | d=3 | 0 | 0 | 2 | 3 | all 15625 | 77500 | 0 |
| e1 | d=3 | 1 | 0 | 2 | 3 | all 15625 | 77500 | 0 |
| e1+e8 | d=3 | 1 | 0 | 2 | 3 | all 15625 | 77500 | 0 |
| e2, e3 | d=3 | 5 | 1 | 1 | 2 | all 25 | 120 | 0 |
| central line of γ3 | d=3 | 3 | 1 | 1 | 2 | all 25 | 120 | 0 |
| e4 + a γ3 line | d=3 | 4 | 1 | 1 | 2 | all 25 | 120 | 0 |
| γ3 (K = Z) | d=3 | 6 | 2 | 0 | 1 | all 1 | 4 | 0 |
| 0 (H = 1) | d=2 | 0 | 0 | 4 | 9 | 300 sampled | 119548 | 0 |
| e1 | d=2 | 1 | 0 | 4 | 9 | 300 sampled | 119904 | 0 |
| e1+e8 | d=2 | 1 | 0 | 4 | 9 | 300 sampled | 120000 | 0 |
| central line of γ3 | d=2 | 2 | 1 | 3 | 7 | 300 sampled | 111668 | 0 |
| e4 + a γ3 line | d=2 | 3 | 1 | 3 | 7 | 300 sampled | 114608 | 0 |

The arity M is only used to guarantee that a witness exists in this check. At d = 3, cubing is a
bijection of F_5 (gcd(3, 4) = 1), so M = a_3 + 1 works. At d = 2, Chevalley–Warning gives
M = 2a_2 + 1. These are not the paper's schedules; those are step 3. Every enumerated tuple had a
nonzero witness. Stage d = 3 is exhaustive over all positive-probability label tuples, as the
brief asks. Stage d = 2 is exhaustive per target, since the per-target identity is checked for all
λ, s and g, while the tuple enumeration there is sampled; the sampled tuples use at most 400
random witnesses each. Cases with |H||Z| > 1.2·10^5 were skipped at d = 2 (h ⊇ γ2 or larger),
along with the random two-generator h, which generates dimension ≥ 6.

**Float, explicit operators (`step2_check.py` Part B; tolerance 1e-9).** Rees covers of Heis(F_3)
and Heis(F_5), with c = 2, |G̃| = 81 and 625, Q = tL. These cover **all** 19 and 39 subgroups,
including K = Z. Checked: R is a representation; the ancilla circuit's Kraus operators equal Π_λ
and form a complete instrument; Pr(λ) is correct; and the channel output **matrix**, built from
explicit permutation matrices and ρ_λ = Π_λ ρ_H Π_λ / Pr, equals ρ_{tH} on tL. At p = 3 this covers
all label tuples and all witnesses, with full 27×27 output matrices: 3054 witness instances. At
p = 5 it covers 5 rows and at most 8 witnesses per subgroup: 280 instances. At p = 3 the
copy-only lift was checked on all 81 × 81 entries for all 19 subgroups. Finally, the
partial-trace identity behind (2c) was checked with full density matrices on random small
instances.

Result: `FAILURES: 0` in `step2_check.py` and `step2_extra.py` (both exit code 0). No counterexample. The exact DL/F5 rows are a machine check; the Heisenberg rows are a float check.

### 2.4 Growing-class barriers

The barrier the corpus records is `NEG-NILPOTENT-CENTRAL-DESCENT-BARRIER`
(`research/registry/negative_results.json`): dihedral 2-groups D_{2^k}, reflection subgroups with
H ∩ Z_i = 1, and cyclic carry. The composition does not evade it. It sits outside that barrier's
hypotheses in three independent ways:

- it needs p > c, while D_{2^k} has p = 2 and class k − 1;
- it needs exponent p, since the input is an F_p-Lie algebra and x^p = px = 0 in the BCH group, so
  there is no cyclic carry;
- its cost is polynomial only for fixed c.

The barrier's mechanism of trivial central intersection is not an obstruction here: (2a) allows
K = 1, and the dilation-plus-SDE cancellation needs no K. This is consistent with
`BOUNDED_CLASS_METABELIAN_HSP.md:837–839` (growing class loses the fixed-parameter guarantee; no
DCP via dihedral 2-groups) and `REES_HSP_REDUCTION.md:210–213` (dimension exponent
1 + Σ_{d=2}^c d⌈log₂(d+1)⌉, polynomial only for fixed c). I found nothing in steps 1–2 that
claims more. Whether the SDE arity is in fact bounded polynomially at fixed c is step 3/4.

### 2.5 What a human reviewer must still check (step 2)

- The exact identities (2a)–(2e) are proved in writing above and match the paper. The checks are
  diagnostics: exhaustive at d = 3 on DL/F5, per-target exhaustive at d = 2, and sampled tuples at
  d = 2.
- Exactness over a finite gate set (QFT over Z, the BCH arithmetic, uniform superpositions) is an
  approximation question for step 4. Here the instruments are treated as exact.

## 3. Needed text changes (listed, not applied)

1. `main.tex:235` (Theorem 223(iii)): add the group-law half of the argument (Z[1/c!] Dynkin
   denominators, associativity in the free class-c Lie ring over Z[1/c!]) or cite it exactly
   (Khukhro Ch. 9–10). Likewise cite the subgroup form of the Lazard correspondence where
   `main.tex:166` invokes it.
2. `main.tex:367`: "On a uniform Q address register" should say *uniform superposition*
   |Q|^{-1/2} Σ_q |q⟩. A maximally mixed address register gives a diagonal output, not ρ_{HZ/Z}.
   `REES_HSP_REDUCTION.md:166` ("initialize the q register uniformly") has the same ambiguity.
   Lemma 283 already says "superposition".
3. `main.tex:379–381` (after Proposition 370): optionally state (2d) explicitly. The output is
   independent of the record, branch by branch, so conditioning on any classical event (solver
   success, retries) leaves i.i.d. ρ_{HZ/Z}. The current sentence says this only for "fresh
   disjoint preparations".
4. Lemma 326 states the setting for "any finite group G". The proof also uses that R is the right
   regular representation with the stated convention, and that Tr R_g = |G|[g = 1]. It is correct
   as written; this is only for clarity.

No counterexample and no gap was found in steps 1–2.

## 4. Handoff to step 3 (and steps 4–5)

Steps 3–5 may assume the following, all proved above for every prime p and every class c with
1 ≤ c < p, every subgroup H ≤ G, and any c distinct points s_i ∈ F_p^×:

- **Source.** One lifted source ρ_{exp(h̃)} on G̃ costs exactly c oracle queries, or c copies of ρ_H.
  h̃ = ⊕_k t^k(h ∩ γ_k) is homogeneous and δ-stable.
- **Stage d (d = c, …, 2).** The input is independent sources ρ_{H_d} on G_d = A/I_d. Measuring
  Z_d = t^dγ_d(L) gives labels λ_i, i.i.d. uniform on K_d^⊥ ⊆ F_p^{g_d}, of rank
  a_d = g_d − dim(h ∩ γ_d). They are uniform by (2a) and independent by the product form; this is
  the "random law of labels" step 3 asks about. Given **any** nonzero s ∈ F_p^M with
  Σ_i s_i^d λ_i = 0 (a system of g_d diagonal degree-d equations, of rank ≤ a_d after row-reducing
  the observed labels), the channel outputs exactly ρ_{H_{d−1}} on G_{d−1}. This holds for every
  label tuple and every witness, and independently of the record. Zero coordinates of s consume
  their sources. Classical retries need no new sources.
- **Terminal.** After d = 2 the group is the additive group tL and the hidden subgroup is th
  (step 1, item (5), plus homogeneity), not h + γ_2 or an image in L/[L, L]. Step 5 should
  confirm the readout and its error bound.

**Open for step 3; nothing here blocks it.**

- Existence of a nonzero witness for the observed labels at the paper's arities. B_d(a), the
  symmetric schedule (a+1)((δ−1)a+1) with p ≥ 16δ^{2δ+2}, and the random column M = 4u with
  p ≥ 16u² all still need checking.
- The cost of finding the witness, and whether the paper's Ivanyos–Santha attribution is right.
- Step 3 may use that the labels are i.i.d. uniform on an unknown subspace K_d^⊥ of known
  ambient dimension g_d. That fact is unconditional; the a_d themselves are unknown to the
  algorithm.
- If no nonzero witness exists for some positive-probability tuple at the chosen arity, that
  block is lost, and no correctness claim in (2c) is affected. The loss shows up only in step 4's
  budget.

**Assumptions steps 3–5 must not add.** No transversality H ∩ Z = 1, no knowledge of K_d or a_d,
no correlated banks. Proposition 299's counterexample still applies to correlated banks:
independence comes from fresh disjoint preparation, not from correct marginals.

---

# Steps 3–5, priority rulings 5a/5b, overall verdict

Date: 2026-11-01. Reviewer: Claude Code (Opus 5.5), second side session. Brief:
`research/REES_CORE_PROOF_CHECK_BRIEF.md` §3 steps 3–5. Sections 1–4 above are unchanged.
I took everything under "Steps 3–5 may assume" (§4) as given and added none of the
assumptions listed there as forbidden. Nothing here has had human review. I changed no
other repository file; `git status --short` was identical before and after the runs.

Checked text: `docs/papers/rees-hsp/main.tex` lines 83–92, 165–200, 393–455, 456–475;
`research/REES_HSP_REDUCTION.md` §5 (lines 186–228) and lines 293–320;
`research/POWER_SDE_SYMMETRIC_CONTRACTION.md` lines 7–180;
`formal/Formal/ReesCentralQuotient.lean` lines 330–350. Primary source: Ivanyos–Santha
arXiv:1503.09016v2, fetched once from arxiv.org, read in §§1, 3 and 5 (the paper's own
Theorem 3, Theorem 11, Lemma 12, §3.3 and the proof of Theorem 5). The quotes for 5a/5b
come from `2026-11-01-rees-priority-check.md` §5; I refetched nothing else.

Scripts (outside the repo, in the session notes folder next to the steps 1–2 scripts):
`/Users/jaspersands/Library/Application Support/Claude/side-session-notes/local_82ea8e9d-f8c7-4b78-b5f8-c0fb77b522d8/rees_steps_3_5/`
(`sde_core.py`, `step3_check.py`, `envelope.py`, with outputs `step3_out.txt`, `envelope_out.txt`).
They were written from scratch for this check and import nothing from the repo. Reproduce
(step3_check.py takes about 2 minutes):

```bash
cd "/Users/jaspersands/Library/Application Support/Claude/side-session-notes/local_82ea8e9d-f8c7-4b78-b5f8-c0fb77b522d8/rees_steps_3_5"
```
```bash
/opt/anaconda3/bin/python -u step3_check.py
```
```bash
/opt/anaconda3/bin/python -u envelope.py
```

## 5. Step 3: SDE step

Target, at a stage-d node with M columns λ_1, …, λ_M ∈ F_p^{g_d} (the observed labels):
find s ∈ F_p^M, s ≠ 0, with Σ_i s_i^d λ_i = 0. By §4, any such s is enough. Write
κ = κ_d = gcd(d, p−1), P_κ = {x^κ : x ∈ F_p^×} (|P_κ| = h = (p−1)/κ), and let a ≤ a_d be the
rank of the observed label matrix.

### 5.1 Verdicts

| Schedule | Arity | Prime condition | Witness exists | Found by | Law of labels used | Verdict |
|---|---|---|---|---|---|---|
| 1 (IS) | B_d(g_d) | p > c only | every column tuple | deterministic, poly(g_d, log p) for fixed d | no | **Holds** |
| 2 (symmetric) | (a+1)((κ−1)a+1), a = g_d | p ≥ 16κ^{2κ+2} if κ ≥ 2 | every column tuple | Las Vegas, abort ≤ 2^{−k} | no | **Holds** (proof checked in writing; stays "conditional" in the paper only by label) |
| 3 (random column) | 4u | p ≥ 16u², u ≥ c, u > max a_d | not for every tuple when u ≥ 5; w.p. ≥ 1 − 4/μ − 2p^{a−M} under the label law | rejection sampling, 4κ^M B trials | yes (i.i.d. uniform on K_d^⊥) | **Holds** for i.i.d. uniform banks only |

### 5.2 Existence (all three schedules)

Chevalley–Warning: a system of g equations Σ_i y_i^κ λ_i = 0 in M > κ·rank variables has a
nonzero solution (IS p. 2 states this for diagonal systems). After the gcd reduction (5.3)
this is the target system.

- Schedule 1: B_d(a) > d·a ≥ κ·a for every a ≥ 1, d ≥ 1. Exists for every tuple.
- Schedule 2: (a+1)((κ−1)a+1) = (κ−1)a² + κa + 1 > κa. Exists for every tuple.
- Schedule 3: 4u > κ·a is guaranteed by κ ≤ u, a ≤ u−1 only when 4u > u(u−1), i.e. u ≤ 4.
  For u ≥ 5 there is no worst-case guarantee, and the schedule does not claim one. Under the
  label law, see 5.5.

So no positive-probability tuple loses its block at the arities of Schedules 1 and 2. That
part of the §4 handoff ("if no nonzero witness exists … that block is lost") never occurs
for them.

### 5.3 Schedule 1: Ivanyos–Santha attribution, read from arXiv:1503.09016v2

What the paper proves (my reading of §3):

1. *Gcd reduction* (§3, first paragraph). If d ∤ q−1, solve with d' = gcd(d, q−1) and lift
   by x ↦ x^t with td ≡ d' (mod q−1). Since G(d', m) ≤ G(d, m) and
   ⌈log₂(d'+1)⌉ ≤ ⌈log₂(d+1)⌉, the d-bound stays sufficient. The paper's sentence (main.tex:420)
   is right.
2. *Theorem 11* (§3.2): for d | q−1 and G(d, m) = d^{d(d−1)/2}(m+1)^d input vectors, it finds
   disjoint I ≠ ∅, J and nonzero γ_j with Σ_I γ_i^d v_i = Σ_J γ_j^d v_j. Proof: Lemma 12
   (recursion B_{ℓ+1} = d^ℓ(m+1)B_ℓ, B_1 = m+1) to ℓ = d, then the sign identity
   Σ_{a∈S_d} sgn(a) w_a = 0.
3. *Accumulation* (§3.3): G(d,m)^ℓ vectors give one vector with 2^ℓ representations with
   pairwise disjoint supports; at 2^ℓ ≥ d+1, Fact 2 (van de Woestijne: a nontrivial zero of
   z_1^d + … + z_{d+1}^d, deterministic, poly(d, log q)) gives the zero vector. Hence
   C(d, m) ≤ G(d, m)^{⌈log₂(d+1)⌉} = B_d(m). This is exactly main.tex (eq:is-arity).
   I checked the steps the proof leaves implicit: a zero intermediate vector, or J = ∅,
   already yields a witness from a nonempty representation; all representations are
   nonempty otherwise, so the final witness is nonzero.
4. *Determinism.* The introduction claims "the existence of a deterministic algorithm"
   (p. 2). §3.1 classifies field elements without nonresidues: it works in the subgroup
   generated by the π-parts seen so far (π = primes of d), uses Pohlig–Hellman there
   (poly(d, log q), since that subgroup's order has only prime factors dividing d), and restarts
   at most log q times when a new element escapes the subgroup. The restarts change the time,
   not the vector count. Randomness appears only in the warm-up Propositions 9–10 (p. 5:
   "randomization in these algorithms is only required to obtain quadratic and cubic
   nonresidues"). The paper's statement (main.tex:420) is right. One caveat: Theorem 3 itself
   says "can be solved in time polynomial", not "deterministically"; the determinism is in the
   introduction and the proof.

**Error in main.tex:420.** It says the bound printed in IS Theorem 3 "is looser". The printed
threshold (font check of the PDF: superscripts d²log d and d log d) is
n > d^{d² log d}(m+1)^{d log d}. Its m-exponent d·log d is *smaller* than the proof's
d·⌈log₂(d+1)⌉ for every d ≥ 2 (d = 2: 2 vs 4; d = 9: 28.5 vs 36). So the last inequality of
IS §3.3, C(d,m) ≤ G^{⌈log₂(d+1)⌉} ≤ d^{d² log d}(m+1)^{d log d}, is false for large m
(d = 2, m = 10: B = 6.0·10⁴ > 2⁴·11² = 1936). `step3_check.py` part A tabulates both: neither bound
dominates the other, and for every d the printed one is smaller once m is large. So the
printed Theorem 3 is not supported by its own proof as written, and B_d(a) is the bound the
proof gives. The paper's arity choice is therefore right, and its query exponent
1 + Σ d⌈log₂(d+1)⌉ (145 at c = 9) is the correct one. Only the word "looser" is wrong: it
should say that the printed threshold has a smaller m-exponent than the proof supports, so the
paper uses the proof's count.

**Machine check (exact mod p).** `sde_core.IS` implements Lemma 12, Theorem 11, §3.3 and
Fact 2 as written. It deviates from IS in two places only: cosets are classified with a
discrete-log table instead of the §3.1 procedure, and Fact 2 is solved by brute force. Neither
changes the column count. At exactly M = B_d(a) columns, for random columns and five adversarial
families (all columns equal; the paper's e_1…e_1e_2… blocks; 90 % zeros; rank one; v and
g·v alternating with g a non-d-th power), every run returned a nonzero s that passes the exact check:

```text
p=13 d=2 a=1 M=B_d(a)=64: 16/16 exact witnesses (0.0s)
p=13 d=2 a=2 M=B_d(a)=324: 10/10 exact witnesses (0.0s)
p=37 d=2 a=3 M=B_d(a)=1024: 8/8 exact witnesses (0.0s)
p=7 d=3 a=1 M=B_d(a)=46656: 6/6 exact witnesses (0.2s)
p=13 d=3 a=1 M=B_d(a)=46656: 6/6 exact witnesses (0.2s)
```

Gcd/Bezout lift. The reduced-degree runs use B_κ(a) columns (or a+1 when κ = 1), fewer than the
B_d(a) the paper allots, which is listed in brackets:

```text
Bezout: p=7 d=4 kappa=2 t=2 a=1 M=64 (B_d(a)=2.81e+14): 6/6 exact witnesses
Bezout: p=7 d=4 kappa=2 t=2 a=2 M=324 (B_d(a)=3.65e+16): 6/6 exact witnesses
Bezout: p=11 d=3 kappa=1 t=7 a=2 M=3 (B_d(a)=5.31e+05): 6/6 exact witnesses
```

The lift x ↦ x^t with td ≡ κ (mod p−1) passes the check at the ORIGINAL degree d.

**What remains open for Schedule 1:** nothing mathematical that I found. A human should
re-read IS §3.1 (classification with restarts) against the claim that the vector count is
unaffected, and confirm that the IS time bound, polynomial for constant d, is
poly(B_d(g_d), log p) with a d-dependent exponent only.

### 5.4 Schedule 2: two-level symmetric contraction

Claim (main.tex Theorem power-sde (ii), from `POWER_SDE_SYMMETRIC_CONTRACTION.md`): for κ ≥ 2,
κ | p−1 (after the gcd reduction), p ≥ 16κ^{2κ+2} and any M = (r+1)((κ−1)r+1) columns in
F_p^r, a Las Vegas algorithm finds a nonzero witness.

Proof check (written, by me):

1. *Level one.* Blocks of r+1 columns have a nonzero linear dependence; scale it so a chosen
   nonzero coefficient lies in P_κ; write each nonzero coefficient as z_i b^κ. Cells
   T_i = Σ b^κ v satisfy Σ_i z_i T_i = 0, with disjoint supports and T_0 nonempty.
2. *Level two.* The first κ−1 cell values of each block form a vector in F_p^{(κ−1)r}, so
   (κ−1)r+1 blocks have a dependence α. Since z_{κ−1} ≠ 0, the last cell also satisfies
   Σ_β α_β T^β_{κ−1} = 0. Normalising α into cosets gives T_ij with Σ_j z_j T_ij = 0 for each i
   (from α) and Σ_i z_i T_ij = 0 for each j (from level one). T_00 has nonempty support.
3. *Contraction.* With C_ij = z_i z_j (t_i + t_j),
   Σ_{ij} C_ij T_ij = Σ_i z_i t_i Σ_j z_j T_ij + Σ_j z_j t_j Σ_i z_i T_ij = 0. If every C_ij is a
   nonzero κ-th power, taking roots gives an original-coordinate witness, nonzero on T_00's
   support since C_00 = 1.
4. *Scalars.* Stage j imposes k = j+1 ≤ κ coset conditions on t at the k distinct affine roots
   {0, −t_0, …, −t_{j−1}}. The Weil bound for Σχ(∏(t − a_i)^{e_i}) (not a constant times a
   κ-th power, since some 0 < e_i < κ) gives N_k ≥ p/κ^k − k√p − (k−1) ≥ p/(2κ^k) when
   √p ≥ 4κ^{κ+1}, i.e. p ≥ 16κ^{2κ+2}. This holds uniformly over prefixes, so 2κ^{j+1}B uniform
   trials fail with probability ≤ 2^{−B} per stage.

I found no gap. The cost is (number of trials ≈ 2κ^{κ}B) × poly(r, log p), plus Las Vegas
κ-th roots and coset generators, so (1+κ^κ)·poly(a, κ, log p, k) for abort 2^{−k} is right.
The paper calls (ii) "a proposed corollary checked only by automated review"; it now has a
written check, but no human one.

**Machine check (exact):** ```text
p=1031 kappa=2 a=3 M=16: 11/11 exact witnesses
p=1031 kappa=2 a=6 M=49: 8/8 exact witnesses
p=105019 kappa=3 a=2 M=15: 9/9 exact witnesses
p=105019 kappa=3 a=4 M=45: 7/7 exact witnesses
```

Same six column families as Schedule 1, plus extra random draws. Every witness was verified at degree κ.

**Open for Schedule 2:** only the prime condition p ≥ 16κ_d^{2κ_d+2} (covered for all grades by
p ≥ 16c^{2c+2}) and human review of the Weil-count step. It is not needed by the main theorem.

### 5.5 Schedule 3: random-column kernel rejection

Uses the label law from §4: the columns are i.i.d. uniform on the unknown K_d^⊥ (dimension
a_d), and are independent of every earlier record.

Proof check of Theorem random-column (i), written by me. Let N be the number of nonzero
y ∈ (P_κ ∪ {0})^M in the kernel. These y are exactly the witnesses in power coordinates
(y_i = s_i^κ), and one sample is accepted with probability N/p^{M−r}, r the observed rank.
In K_d^⊥ coordinates the label matrix A is uniform a×M. For y ≠ 0, Pr[Ay = 0] = p^{−a}.
Two non-proportional y, y' are independent, and y' = ty with y' in the set iff t ∈ P_κ (h
values). Hence E N = N_0 p^{−a} with N_0 = (h+1)^M − 1, and Var N ≤ h·E N, so
Var N/(E N)² ≤ 1/μ with μ = N_0/(h p^a), exactly the paper's μ. Chebyshev gives
N ≥ E N/2 outside probability 4/μ. Pr[r < a] ≤ (p^a−1)/(p−1)·p^{−M} ≤ 2p^{a−M}. Outside
both events, acceptance ≥ N_0/(2p^M) ≥ (κ^{−M} − p^{−M})/2 ≥ 1/(4κ^M), using
h+1 ≥ p/κ and p ≥ 2κ. Finally μ ≥ p^{3u}κ^{1−4u} ≥ 2^{12u}u^{2u+1} ≥ 2^{8u+1}u^{2u+1} from
p ≥ 16u², κ ≤ u, a ≤ u−1. (ii): per tree, 3·2^{−B}·(#nodes) ≤ 3/64, and the bank events,
summed over ≤ (4u)^{c−1} nodes, are ≤ 2^{−6u}; so abort ≤ 1/16. Hoeffding on 4m' trees with
success ≥ 15/16 gives ≤ e^{−3.78m'} ≤ 2^{−2m'}. Kept trees still output i.i.d. ρ_{th},
because by (2d) the output does not depend on the record. No gap.

It depends on the law: for an adversarial or correlated bank there is no acceptance bound, and
for u ≥ 5 not even worst-case existence (5.2). The choice u = max(c, max_d g_d + 1) uses
only known data, so the forbidden knowledge of a_d is not needed. The cost is
2^{O(u log u)}·poly, so this schedule is polynomial only when every a_d is O(log m/log log m).
It is not a route to the main theorem.

**Exact counts per bank** (`step3_check.py` part D; DP over partial sums, int64 exact where
(h+1)^M < 2^62, float64 otherwise). "Exists" = the bank has a nonzero witness; acceptance =
N/p^{M−r}:

```text
p=   5 d=2 kappa=2 a=1 u=2 M=8 cond=False: witness exists 400/400; acceptance mean 1.679e-02 min 1.554e-02; 1/(4k^M)=9.766e-04; banks below 0/400; paper bank bound 6.12e-03
p=   5 d=4 kappa=4 a=1 u=2 M=8 cond=False: witness exists 400/400; acceptance mean 6.601e-04 min 3.456e-04; 1/(4k^M)=3.815e-06; banks below 0/400; paper bank bound 7.85e-02
p=   5 d=4 kappa=4 a=3 u=4 M=16 cond=False: witness exists 300/300; acceptance mean 4.309e-07 min 3.785e-07; 1/(4k^M)=5.821e-11; banks below 0/300; paper bank bound 7.63e-03
p=   7 d=2 kappa=2 a=1 u=2 M=8 cond=False: witness exists 400/400; acceptance mean 1.137e-02 min 8.703e-03; 1/(4k^M)=9.766e-04; banks below 0/400; paper bank bound 1.28e-03
p=   7 d=3 kappa=3 a=1 u=3 M=12 cond=False: witness exists 400/400; acceptance mean 3.839e-05 min 3.725e-05; 1/(4k^M)=4.704e-07; banks below 0/400; paper bank bound 1.05e-04
p=   7 d=3 kappa=3 a=2 u=3 M=12 cond=False: witness exists 300/300; acceptance mean 3.846e-05 min 3.479e-05; 1/(4k^M)=4.704e-07; banks below 0/300; paper bank bound 7.38e-04
p=  67 d=2 kappa=2 a=1 u=2 M=8 cond=True: witness exists 300/300; acceptance mean 4.398e-03 min 4.398e-03; 1/(4k^M)=9.766e-04; banks below 0/300; paper bank bound 4.95e-09
p= 151 d=2 kappa=2 a=2 u=3 M=12 cond=True: witness exists 100/100; acceptance mean 2.643e-04 min 2.643e-04; 1/(4k^M)=6.104e-05; banks below 0/100; paper bank bound 1.84e-16
p= 151 d=3 kappa=3 a=2 u=3 M=12 cond=True: witness exists 100/100; acceptance mean 2.204e-06 min 2.204e-06; 1/(4k^M)=4.704e-07; banks below 0/100; paper bank bound 1.47e-14
```

Reading: every sampled bank had a nonzero witness, and no bank fell below the paper's
per-trial acceptance 1/(4κ^M), including the six rows at p = 5, 7 where the prime condition
fails (there the theorem makes no promise). At p = 5, d = 4 (κ = p−1, the zero-sum case) a
witness always exists at M = 8 ≥ D(C_5) = 5 for a = 1, and at M = 16 ≥ D(C_5^3) = 13 for a = 3.
The 400/300/100-bank samples cannot see events of probability below about 10^{-2}–10^{-3}; the
bound itself is the written proof above.

At p = 5 and 7 (the brief's small primes) the prime condition p ≥ 16u² fails, so the theorem
does not apply there; the table reports what happens anyway.

### 5.6 What a human reviewer must still check (step 3)

- IS §3.1 (deterministic classification with restarts) and the IS running time for constant d.
- The IS Theorem 3 misstatement (5.3): confirm that the printed threshold is not implied by
  the proof, and decide whether to tell the authors.
- The Weil-bound step of Schedule 2 (composite κ included).
- That Schedules 2–3 are presented as alternatives; the main theorem needs only Schedule 1.

## 6. Step 4: complexity envelope, end to end

### 6.1 Verdict

**Holds** for Schedule 1. Evidence: written derivation plus exact integer evaluation
(`envelope.py`), which reproduces the paper's class-9 profile.

### 6.2 The envelope

Inputs: m = dim L, g_d = dim γ_d(L) ≤ m (g_1 = m), n = Σ g_d ≤ cm, p > c, ε, oracle label
width w, oracle cost T_f. Put

- t = ⌈log_p(3/ε)⌉, S = m + t terminal samples (main.tex:402; the reduction note's "n + t"
  uses n for dim L, so it is the same count in that note's notation; with n = cover dimension it
  would be a valid overcount);
- M_d = B_d(g_d), P = Π_{d=2}^c M_d leaves per terminal sample;
- original queries Q = c·S·P;
- merges N_merge = S·Σ_{d=2}^c Π_{d'=2}^{d−1} M_{d'} (stage-d merges per sample are the
  product of the arities below d), which is also the number N_solver of IS calls;
- complete instruments N_instr = S·P (leaves) + N_merge + S (final readouts);
- QFT precision η = ε/(3N_instr q_max), q_max = max(m, max_d M_d g_d) transforms per instrument,
  so ⌈log₂(1/η)⌉ = O(log N_instr + log q_max + log(1/ε)) bits.

Running time ≤ Q·T_f
+ S·P·[c evaluation maps (O(nm) field ops each) + clean-up + w-qubit label handling]
+ Σ_d (merges at stage d)·[M_d·g_d QFT_{F_p} at precision η + M_d controlled right actions, each 4 BCH
  evaluations of (c−1)c(c+1)(c+2)/6 brackets at O(n³) field ops + T_IS(d, M_d, log p)]
+ S·[m QFT_{F_p}] + O(m³) field ops for the nullspace,
with field operations costing poly(log p) bit operations.

Every factor is polynomial in (m, log p, w, log(1/ε)) at fixed c. r_d = g_d ≤ m, so
B_d(r_d) ≤ B_d(m) = O_d(m^{d⌈log₂(d+1)⌉}), and Q = O_c((m + log(1/ε))·m^{Σ_{d=2}^c d⌈log₂(d+1)⌉}).

**Where p enters:** field-element size (log p bits) in every arithmetic and QFT gate, the IS
time (poly in log p), and t = ⌈log_p(3/ε)⌉, which decreases in p. The only prime condition
for Schedule 1 is p > c (Lazard/BCH and IS need nothing more). No step is polynomial in p.

### 6.3 Error budget

The ideal process is exactly correct for every record and witness (§4, (2c)–(2d)). The only
failure sources are:

- *rank*: the S terminal samples are i.i.d. uniform on (th)^⊥ (independence comes from fresh
  sources, (2d)); Pr[no spanning set] ≤ (p^k−1)/((p−1)p^S) ≤ 1/((p−1)p^t) ≤ ε/3 with
  k = dim(th)^⊥ ≤ m;
- *solver*: zero for Schedule 1, since IS is deterministic and total for every column tuple at
  arity B_d(g_d) (5.2–5.3);
- *approximation*: each of the N_instr instruments within ε/(3N_instr) in diamond norm. These
  errors add over a sequential composition, including adaptive classical control, so the total is ≤ ε/3.

Total ≤ 2ε/3 < ε. The paper's three-way split is valid but leaves its solver third unused under
Schedule 1. The Markov cap (expected time T, cutoff 2T, ⌈log₂(3N_solver/ε)⌉ attempts) is
correct whenever T bounds the expected time *for every instance*: true for Schedule 2
(worst-case Las Vegas), and not used by Schedule 3, which has its own split. One
convention point: an isometry error ‖V − U‖ ≤ η gives trace distance ≤ η in the ½‖·‖₁
convention (≤ 2η in ‖·‖₁). The note should state the convention, but the factor does not
matter for the claim.

### 6.4 Machine check (`envelope.py`)

```text
== paper's class-9 profile (rees_hsp_reduction.json): g=(19,17,16,14,12,9,6,3,1)
 p=11: t=1 S=20 n=97 log2 Q=1572.7 log2 N_instr=1569.5 eta_bits=2066 rank_fail=9.09e-03
 p=2305843009213693951: t=1 S=20 n=97 log2 Q=1572.7 log2 N_instr=1569.5 eta_bits=2066 rank_fail=1.88e-37
 paper: final samples 20, queries <= 2^1573, instrument calls <= 2^1570, exponent 145; formula exponent(9) = 145

== growth in m at fixed c (g_d = m for every d: worst case g_d <= m)
 c=2: exponent formula 5; empirical d(log Q)/d(log m) = 4.81, 4.98, 5.00; eta_bits at m=10^4: 146; brackets/BCH 4
 c=3: exponent formula 11; empirical d(log Q)/d(log m) = 10.59, 10.96, 11.00; eta_bits at m=10^4: 269; brackets/BCH 20
 c=4: exponent formula 23; empirical d(log Q)/d(log m) = 22.15, 22.91, 22.99; eta_bits at m=10^4: 571; brackets/BCH 60
 c=5: exponent formula 38; empirical d(log Q)/d(log m) = 36.59, 37.85, 37.99; eta_bits at m=10^4: 913; brackets/BCH 140

== dependence on p at fixed (c, m): only t, field bits and the p > c condition
 p=5: t=10 log2 Q=47.35 rank_fail<=eps/3: True field bits=3
 p=7: t=8 log2 Q=47.25 rank_fail<=eps/3: True field bits=3
 p=101: t=4 log2 Q=47.03 rank_fail<=eps/3: True field bits=7
 p=2147483647: t=1 log2 Q=46.83 rank_fail<=eps/3: True field bits=31
 p=170141183460469231731687303715884105727: t=1 log2 Q=46.83 rank_fail<=eps/3: True field bits=127

== error budget check (Schedule 1): rank + solver + approximation <= eps
 eps=3.3e-01 p=5: rank=1.00e-02 solver=0 approx=1.11e-01 total<=eps: True  (unused third: solver)
 eps=3.3e-01 p=2305843009213693951: rank=1.88e-37 solver=0 approx=1.11e-01 total<=eps: True  (unused third: solver)
 eps=1.0e-06 p=5: rank=2.56e-08 solver=0 approx=3.33e-07 total<=eps: True  (unused third: solver)
 eps=1.0e-06 p=2305843009213693951: rank=1.88e-37 solver=0 approx=3.33e-07 total<=eps: True  (unused third: solver)
 eps=6.2e-61 p=5: rank=3.87e-62 solver=0 approx=2.07e-61 total<=eps: True  (unused third: solver)
 eps=6.2e-61 p=2305843009213693951: rank=1.53e-92 solver=0 approx=2.07e-61 total<=eps: True  (unused third: solver)
```

The class-9 profile reproduces the paper's figures: 20 final samples, log₂Q = 1572.7 (paper: at most
2^1573), log₂N_instr = 1569.5 (paper: at most 2^1570), exponent 145. The empirical slope of log Q
against log m tends to 1 + Σ d⌈log₂(d+1)⌉ (5, 11, 23, 38 for c = 2..5). In p, Q changes only
through t.

### 6.5 Reviewer items (step 4)

- The gate-level constants (bracket count, BCH clean-up with 4 evaluations, QFT compilation)
  come from main.tex Theorem uniform-compilation, which I read but did not re-derive.
- The oracle's internal cost and label width enter linearly; the main theorem states the bound
  "polynomial in … the oracle label width", which matches.

## 7. Step 5: final readout and preserved H

### 7.1 Verdict

**Holds.** Evidence: proof (below) on top of §§1–2 items (5) and (2c); Lean
`terminalEquiv` (`formal/Formal/ReesCentralQuotient.lean:333`) states that the degree-one
truncation is linearly equivalent to all of L, not its abelianization.

### 7.2 Exact claim and proof

- *Terminal quotient.* After stage 2 the group is A/⊕_{k≥2} A_k = tL with the BCH product
  reduced to addition (all brackets land in grades ≥ 2), and the hidden subgroup is
  t(h ∩ γ_1) = th. The corrected text says exactly this (main.tex:400, also lines 145–150).
  The pre-correction L/[L, L] is gone. Lean `terminal_bracket` gives the vanishing bracket.
- *Preserved H at every quotient.* At stage d the hidden subgroup is the homogeneous image
  ⊕_{k≤d} t^k(h ∩ γ_k) (§4 "Stage d"), which every dilation preserves. The channel outputs
  ρ_{H_{d−1}} for every record and witness ((2c), steps 1–2), so H is never replaced by a
  different subgroup along the recursion.
- *Readout.* An exact QFT_{F_p}^{⊗m} on the coset state of th in F_p^m gives the uniform law on
  (th)^⊥. S = m + t independent samples span it except with probability ≤ 1/((p−1)p^t) (6.3).
  The nullspace of the samples is then exactly th. This recovers all of h, not h modulo
  [L, L] or another subspace.
- *From h to H.* In the explicit chart, log = exp = identity on coordinates
  (main.tex Definition input-contract (ii)), so a basis of h is the output the theorem
  promises. To get generators: the subgroup K = ⟨exp b_1, …, exp b_k⟩ ⊆ H satisfies that log K
  is a Lie subalgebra (Lazard) containing every b_i, so log K ⊇ h and K = H.
- *Approximate readout.* The claim needs an error bound for the final readout: the theorem
  is bounded-error over a finite gate set. The bound: each final readout is one complete
  instrument with error ≤ ε/(3N_instr) in diamond norm (QFT error at most m·η). Hence the total
  variation between the actual and ideal joint law of the S samples is ≤ S·ε/(3N_instr) ≤ ε/3,
  already included in 6.3. The classical post-processing is exact. This bound is argued, not
  Lean-checked; Lean covers only the exact terminal retention.

### 7.3 Reviewer items (step 5)

- Lean does not cover the readout probability or the approximate QFT; both are argued above.
- No text change is needed for the terminal quotient. Optionally, main.tex:400 could add the one-line
  generation argument for H = ⟨exp b_i⟩.

## 8. Priority rulings 5a and 5b

### 8.1 Ruling 5a (Ivanyos–Santha Cor 8 against A2 and A4), settled together with the
step-3 attribution

**A4 (growing prime at fixed class): partly known; Cor 8 is a strict special case of the
Rees regime.** Cor 8's groups are G_B = F_p ⋉_B F_p^m with B^p = I, of class d =
min{j : (B−I)^j = 0} (IS §4.1, Prop 7 proof). For constant d and p > d (all large p), G_B is a
p-group of class d < p. The matrices M_B(x, v) − I are nilpotent of index ≤ d+1 ≤ p, so the
matrix logarithm gives its Lazard Lie algebra explicitly in poly(m, log p) time, and the
oracle can be pulled back through exp. Its hidden family (order-p subgroups H_v not in
F_p^m) is a special case of arbitrary H. So, if the Rees main theorem is correct, it contains IS
Cor 8 for p > d, and the growing-prime, fixed-class feature is not new by itself. What is new
is arbitrary H in arbitrary Lazard groups of class < p. The priority check's 4th open
question ("whether every such G is a Lazard group of class < p") is answered: yes whenever
p > d, which is every case once p exceeds the constant class; class d = p needs m ≥ p and
so lies outside "constant class, p growing".

**A2 (grade-by-grade central descent by scalar weights): known as a mechanism, from IS §5 —
more than the priority check's provisional "not covered".** The proof of IS Theorem 5
(§5, pp. 12–13) Fourier-measures labels Y^i of level-set states. It then finds a nonzero δ
with Σ_i δ_i^d Y^i_d = 0, an SDE whose columns are the measured labels, and adds a fresh
register x with the substitution x_i ↦ x_i + δ_i x, so that the degree-d phase terms cancel.
It measures the rest and recurses on degree d−1, …, 1 in a tree with n^{d−1} leaves. IS states that the new
point is eliminating "all the degree d terms simultaneously, in one step". This is the same
mechanism as the Rees stage-d channel: scaling by δ multiplies the degree-j coefficient by
δ^j, exactly as the graded dilation scales grade j by s^j. It eliminates whole grades,
the tree arity equals the SDE arity, and the leaf product is Π M_d. The only difference is the setting: IS
works on univariate polynomial-graph states (equivalently F_p ⋉ F_p^m with the restricted H),
where the grading is given by the polynomial degree. The Rees cover (A1) supplies that grading
for an arbitrary Lazard group and arbitrary H. So the A2 mechanism is not new; its use
after A1 is. main.tex:112 already credits IS for "scalings … align random central
characters", and main.tex:116 cites Cor 8 correctly. The related-work paragraph should add
two statements: (i) IS Cor 8 (with DHIS) is a special case of the main theorem's regime for p
> class, and (ii) the grade-by-grade elimination is IS §5's degree-by-degree elimination
transplanted through the Rees cover. On attribution: Section 3 of IS is correctly cited as
the solver and B_d is the right arity (5.3). §5 should also be cited as the source of the
descent pattern.

### 8.2 Ruling 5b (Imran–Ivanyos)

**Agree with the provisional ruling: unconditional only for primes bounded by a constant;
for growing primes conditional on a zero-sum method; smooth order is posed as an open
problem, not claimed.** From the quotes, Thm 1 assumes "prime factors of |G| are also bounded by a
constant", and Thm 2 supplies the zero-sum method there (S(p,n) = p^{O(p log² p)}n^{O(p log² p)},
polynomial in n only for p = O(1)). Prop 2 and §6 make larger primes conditional, and the smooth
case is stated as what "a positive answer would imply".

One addition. Even conditionally, that route cannot reach the Rees regime of p
superpolynomial in m. By Olson's theorem the Davenport constant of C_p^n is n(p−1)+1, so a
worst-case zero-sum method needs at least n(p−1)+1 elements. That is why the open question
asks for poly(np) time on (np)^d elements, which gives the smooth case at best. A method on
poly(n log p) elements would have to use the distribution of the sequences, and for uniform
elements that is a binary-weight short-solution problem of SIS type, not known to be easy. Rees avoids this
by using scalar weights s^d from a set of size (p−1)/κ, where fixed-degree SDE is easy (IS).
This contrast supports the priority check's "A1 possibly new". It is not a novelty proof:
gate `novelty_established` stays false.

## 9. Overall verdict on the composition

Claim checked: main.tex Theorem main ("Proposed explicit-Lie theorem"). For fixed c, every
prime p > c, every finite p-group G of class c given by an explicit Lazard Lie algebra
L ≅ F_p^m (Definition input-contract), every subgroup H ≤ G, with access by a coherent oracle
(or fresh copies of ρ_H, c per lifted source), the procedure returns a basis of h = log H
with probability ≥ 1−ε in time polynomial in m, log p, the label width and log(1/ε), using
Schedule 1 (Ivanyos–Santha).

| Step | Verdict | Evidence |
|---|---|---|
| 1 Tuple group/BCH, every c < p, every H | Holds | proof + exact checks (§1) |
| 2 Measured channel, central descent | Holds | proof + exact checks (§2) |
| 3 SDE: Schedule 1 | Holds (deterministic, every tuple, every p > c) | IS proof read; exact scaffold runs at B_d(a) |
| 3 SDE: Schedule 2 | Holds under p ≥ 16κ^{2κ+2} | written proof; exact runs |
| 3 SDE: Schedule 3 | Holds for i.i.d. uniform banks under p ≥ 16u² | written proof; exact per-bank counts |
| 4 Envelope | Holds: Q = c(m+t)Π B_d(g_d), exponent 1+Σ d⌈log₂(d+1)⌉, error ≤ 2ε/3 | derivation + exact evaluation |
| 5 Readout, preserved H | Holds: terminal tL, hidden th, all of h recovered | proof + Lean terminalEquiv |

**Overall: no gap or counterexample found; the composition holds as a written proof checked
by two AI sessions, with exact small-case checks, pending human review.** Nothing blocks the
claim. The conditional parts are Schedules 2 and 3, which the main theorem does not use:
Schedule 2 on its prime bound, Schedule 3 on the prime bound and the i.i.d. label law. Steps
1–5 do not cover the black-box extension, the derived-dimension corollary (Cor fpt-r) or the
torsion-rank row.

**Claim gates that must stay false** (`research/reductions/rees_hsp_reduction.json`):
`independent_review` (this check, done by AI sessions, does not count as the human review
the brief requires), `novelty_established` (5a shows A2 and A4 are partly known; A1 is only
"possibly new"), `speedup_claim_allowed` (no application; the constants are astronomical,
2^1573 queries at the class-9 profile), `coherent_receiver_implemented`,
`general_sde_implemented` and `formal_compiler_checked`.

**Ranked fixes (listed, not applied):**

1. main.tex:116 related work: state that IS Cor 8 (and DHIS) is a special case of the regime
   for p > class, and that the grade-by-grade elimination is IS §5's degree-by-degree
   elimination via the Rees cover (8.1).
2. main.tex:420: replace "The cleaner bound … stated in its Theorem 3 is looser" with the
   correct relation: the printed threshold has m-exponent d log d < d⌈log₂(d+1)⌉ and is not
   implied by the proof, so the paper uses the proof's count (5.3).
3. main.tex:436–437: Schedule 2 (ii) can say "proof checked in writing (this review)",
   pending human review, instead of "checked only by automated review". Keep it labelled
   conditional until a human has read it.
4. main.tex:402–406: optionally note that under Schedule 1 the solver third is zero, and state
   the norm convention for the QFT isometry error.
5. main.tex:400: optionally add the one-line argument that H = ⟨exp b_i⟩ for a basis b_i of h.
6. The §3 items of the steps 1–2 report (uniform *superposition* at main.tex:367 and the rest)
   still apply.
