# Three-quadratic-field multinorm bridge for Page GBuild over Q

## 0. Verdict

**The global bridge works.** It removes GBuild's smooth-relation search for K=Q, but it does not give an end-to-end generator algorithm.

- **Step 1 is correct and costs polynomially many bits.** It uses GRH for the prime-in-progression search and paid quadratic-form solving. The third embedding Q(√(aD))→A is free in closed form once a=s²+t² is computed.
- **Step 2 is true.** I give a complete class-field-theory proof that the multinorm group N₁N₂N₃ equals K* whenever some place has local degree 4. Prasad–Rapinchuk Lemma 4.8 is not needed for this; it only gives the failure direction. This proof uses standard class field theory, not the supplied text.
- **Step 3 extends verbatim to E = L₁×L₂×L₃.** Combined with Step 2 it gives ∏ᵢN(O_{Lᵢ,S}^*) = Z_S^×, with S of polynomial total bit length.
- **Step 4 produces q_p ∈ O[1/S]^× with nrd(q_p)=p, and q₋₁ with norm −1.** The integrality certificate works block by block. S does not grow.
- **Two new blockers appear in Step 4.** Valuations of the compact words at S-primes are polynomial in bits but can be exponential in magnitude. Page's local machinery is linear in those magnitudes.
- **The remaining gap is local alignment at the split primes of S.** This includes the large primes a, the embedding-denominator primes and the primes of nrd(I). The precise statement is in §6.

## 1. Step 1: presentation and its cost

**Claim.** Let D=∏p be squarefree with an even number of prime factors. Let a be a prime with a≡1 (mod 8) if D is odd, a≡5 (mod 8) if D is even, and (a/p)=−1 for every odd p|D. Then (a,D)_Q is ramified exactly at the primes dividing D, so (a,D) ≅ A by Hasse classification.

**Proof by Hilbert symbols.**

- **Odd p|D:** p∤a and v_p(D)=1, so (a,D)_p=(a/p)=−1.
- **p=2, D=2D′:**
  - (a,2)₂ = (−1)^{(a²−1)/8} = −1, since a≡5 (mod 8).
  - (a,D′)₂ = (−1)^{((a−1)/2)((D′−1)/2)} = 1, since a≡1 (mod 4).
  - So (a,D)₂ = −1.
- **p=2, D odd:** a≡1 (mod 8) is a 2-adic square, so the symbol is +1.
- **p=a:** (a,D)_a = (D/a). Since a≡1 (mod 4), reciprocity gives (p/a)=(a/p) for odd p.
  - D odd: (D/a) = (−1)^{#primes of D} = +1.
  - D even: (D/a) = (2/a)·(−1)^{#odd primes} = (−1)(−1) = +1, because the number of odd primes is odd.
- **∞:** a>0, so the symbol is +1.
- **Other p:** both entries are units at p, so the symbol is +1. ∎

**Local degree 4 at ramified primes.** Take p|D (odd p, or p=2 when D is even).
- Q_p(√a) is the unramified quadratic extension, because a is a nonresidue (or a≡5 mod 8 at 2).
- Q_p(√D) is ramified.
- So F_p has degree 4, where F=Q(√a,√D).

The same three-field local test shows that L₁=Q(√a), L₂=Q(√D) and L₃=Q(√(aD)) each embed in A. Each Lᵢ ⊗ Q_p is a field at every p|D, and A is split at ∞.

**Cost of Step 1.** Every input and output below has polynomial bit length.

1. **Primes of D.** D² = disc(O) is a Gram determinant. Factor D with Shor (paid), or read the primes off the ramification.
2. **Nonresidues and progression class.** Find a nonresidue mod each odd p|D (randomized, expected O(1) tries each). Combine by CRT into a class r mod M=8∏p ≤ 8D.
3. **Prime a ≡ r (mod M).**
   - Sample t uniformly from [0, M²) and test r+tM with AKS or Miller–Rabin.
   - Under GRH, the progression count up to X=M³ is π(X)/φ(M)+O(√X log X), with main term ≫ M²/log M.
   - So each sample succeeds with probability ≫1/log M. Cap the number of trials at O(log M·log(1/η)).
   - Then a ≤ M³, i.e. O(log D) bits. Ascending enumeration would be an exponential loop, so it is not used.
4. **Two squares.** Write a = s²+t², which is possible because a≡1 (mod 4). Use √−1 mod a from a random nonresidue, then Cornacchia. This is randomized polynomial; no factoring is needed.
5. **i′ with i′² = a.** Find a nontrivial zero (x,w) of the quaternary form (x ↦ x² on A⁰) ⊥ ⟨−a⟩. It is isotropic because L₁ embeds.
   - Any nontrivial zero has w≠0. If w=0, x would be a nonzero nilpotent, contradicting that A is a division algebra.
   - Set i′ = x/w.
   - Solver: existing indefinite-quadratic-form algorithms that use the determinant's factorization, e.g. Simon. These are outside the supplied packet and their locators are unverified. Factor the determinant with Shor.
6. **j′ anticommuting with i′, j′² = D.**
   - Pick any nonzero e in A⁰ that anticommutes with i′, and put c=e².
   - Then (xe+y·i′e)² = c(x²−ay²).
   - Since (a,c) ≅ A ≅ (a,D), the ratio D/c is a norm from Q(√a). Solving x²−ay² = D/c is a K=Q, d=2 relative-norm instance.
   - Use the reviewed relative-norm theorem (RELATIVE_NORM_TENSOR_SUPPORT.md) or classical conic solving with Shor-factored coefficients.
7. **Closed-form embedding of L₃.** Put k′ = i′j′, so (xj′+yk′)² = D(x²−ay²).
   - x=s/t, y=1/t solves x²−ay² = −1. Multiplying by √a gives (a/t)² − a(s/t)² = a.
   - Hence z = (a/t)·j′ + (s/t)·k′ satisfies z² = aD. No conic solve is needed.
8. **Embedding denominators.** Let c₁, c₂, c₃ be the denominators of φᵢ(generator of O_{Lᵢ}) in the Z-basis of O. Factor c₁c₂c₃ and t with Shor.

**Hand-checked arithmetic (not a run control): D=6.**
- a=5: 5≡5 (mod 8) and (5/3)=−1.
- 5 = 2²+1², so t=1 and z = 5j′+2k′, with z² = 6(25−20) = 30.
- At every p≡43 (mod 120): χ₅(p)=−1, χ₆(p)=+1, χ₃₀(p)=−1. So Q(√6) supplies the norm lift, consistent with the supplied palette review §3.

## 2. Step 2: multinorm theorem

**Theorem.** Let F/K be biquadratic with Gal(F/K) = {1,h₁,h₂,h₃}, and Lᵢ = F^{⟨hᵢ⟩}. If some place v₀ has [F_{v₀}:K_{v₀}] = 4, then N₁N₂N₃ = K*.

Notation:
- ψ_v: K_v^× → D_v ⊂ G is the local Artin map, surjective onto the decomposition group D_v.
- Hᵢ = ⟨hᵢ⟩.

**Fact (i): norm criterion.** n ∈ Nᵢ if and only if ψ_v(n) ∈ Hᵢ for all v.
- Restricting ψ_v to Lᵢ is the local Artin map of Lᵢ, so ψ_v(n) ∈ Hᵢ means n is a local norm from Lᵢ at v.
- The Hasse norm theorem for cyclic Lᵢ/K then gives a global norm. For quadratic Lᵢ this is Hasse–Minkowski for ternary forms.

**Fact (ii): realizability.** Let (σ_v) satisfy σ_v ∈ D_v, σ_v = 1 for almost all v, and ∏_v σ_v = 1. Then some n ∈ K* has ψ_v(n) = σ_v for every v.
- Choose an idele t with ψ_v(t_v) = σ_v, and t_v = 1 where σ_v = 1.
- The global Artin symbol of t is ∏σ_v = 1. By Artin reciprocity, t = n·N_{F/K}(s) for some n ∈ K*.
- Local norms have trivial symbol, so ψ_v(n) = σ_v.

This is the V₄ analogue of the Exercise 2.16 statement quoted in the Prasad–Rapinchuk footnote.

**Proof of the theorem.**

1. Let x ∈ K* and set τ_v = ψ_v(x). Then τ_v ∈ D_v, τ_v is almost always 1, and ∏τ_v = 1.

2. At each v, write τ_v = s₁ᵥs₂ᵥs₃ᵥ with s_{iv} ∈ Hᵢ ∩ D_v:
   - **D_v = G:** the homomorphism H₁×H₂×H₃ → G is surjective. Its kernel is {1,(h₁,h₂,h₃)}, because h₁h₂h₃ = 1. So there are exactly two decompositions, differing by flipping all three coordinates.
   - **D_v = Hᵢ:** the decomposition is forced: s_{iv} = τ_v and the other two are 1.
   - **D_v = 1:** all s_{iv} = 1.

3. Let πᵢ = ∏_v s_{iv} ∈ Hᵢ. Then π₁π₂π₃ = ∏τ_v = 1. Since h₁^{e₁}h₂^{e₂}h₃^{e₃} = 1 iff e₁=e₂=e₃ (mod 2), the parity vector is (0,0,0) or (1,1,1).

4. If it is (1,1,1), flip the decomposition at v₀. This makes every πᵢ trivial, and the supports stay finite.

5. By Fact (ii) there are nᵢ ∈ K* with ψ_v(nᵢ) = s_{iv}. By Fact (i), nᵢ ∈ Nᵢ.

6. Put w = x/(n₁n₂n₃). Then ψ_v(w) = 1 for all v, so w ∈ N₁ by Fact (i). Hence x = (n₁w)·n₂·n₃. ∎

**Relation to the supplied lemma.** The parity (1,1,1) is exactly the obstruction that Prasad–Rapinchuk Lemma 4.8 realizes when no place has degree 4. Their ϕ detects it. I do not claim that the converse appears in their paper.

**Application.** For our triple, every p|D is a degree-4 place, and D>1. So N₁N₂N₃ = Q*, including the sign −1, with no positivity promise. The archimedean places impose nothing because all Lᵢ are real.

## 3. Step 3: support theorem for E = L₁×L₂×L₃

Write 𝒩(y₁,y₂,y₃) = ∏ N_{Lᵢ/Q}(yᵢ).

**Factors of E⊗E.** E⊗_Q E = ∏_{i,j} Lᵢ⊗Lⱼ.
- For i=j: Lᵢ⊗Lᵢ ≅ Lᵢ×Lᵢ, giving the identity and conjugate pairings.
- For i≠j: Lᵢ⊗Lⱼ ≅ F, since the fields are linearly disjoint.

**Pair elements.** For b in a factor M of Lᵢ⊗Lⱼ, define y_M(b) to have N_{M/ι₁Lᵢ}(b) in coordinate i, N_{M/ι₂Lⱼ}(b)^{−1} in coordinate j, and 1 elsewhere. By transitivity, 𝒩(y_M(b)) = N_{M/Q}(b)/N_{M/Q}(b) = 1.

**Kernel generation at q ∉ S.** Assume S contains every prime ramified in some Lᵢ (the primes dividing 2aD).
- Concatenate all primes of L₁, L₂ and L₃ over q into a single residue-degree row (f_P).
- An x with v_q(𝒩(x)) = 0 has divisor vector in the kernel of this row.
- Every pair (P,P′), including pairs inside one field, occurs as (Lᵢ⊗Lⱼ)_q ⊃ L_{i,P}⊗L_{j,P′} ≠ 0.
- The reviewed gcd/lcm argument therefore applies verbatim: the pair vectors (f_{P′}/g)e_P − (f_P/g)e_{P′} span the full integer kernel.

**Choice of S.** S consists of:
- all primes dividing 2aD;
- all rational primes ≤ B₀, the GRH class-generation bound for F and for each Lᵢ (the constant per BS §8.2 as cited in the reviewed note);
- the primes of c₁c₂c₃ and of t;
- the primes of nrd(I).

**Bit size.** log|d_F| = log|d₁d₂d₃| = O(log D), using a ≤ (8D)³. So B₀ = O(log²D) numerically and |S| is polynomial. S is computed without any unknown solution.

**Lifting.** Lift the outside-S divisor to divisors D_M on the factors. Since the class groups of F and of each Lᵢ are generated by S-primes, D_M + A_M = (b_M) with A_M supported on S. Then x/∏_M y_M(b_M) is an S-unit of E with the same 𝒩. This uses ordinary class groups only; no 2-torsion shortcut is used.

**Conclusion.** 𝒩(O_{E,S}^×) = Z_S^× ∩ 𝒩(E*) = Z_S^×.

## 4. Step 4: compiler and integrality

**Algorithm.**

1. **S-units.** Compute complete compact S-unit generators of each real quadratic field Lᵢ. Use the quantum Biasse–Song algorithm under GRH (as cited in the reviewed note). Torsion is ±1.
2. **Atom norms.** For every atom β_l, compute N(β_l) ∈ Q.
3. **Certified norm vectors.** Factor each atom norm with Shor. Check exactly that the exponent-weighted valuations cancel at every prime outside S, which certifies that each unit's norm lies in Z_S^×. Record the sign and the vector (v_p)_{p∈S}.
4. **Integer system.** Solve for −1 and for each p ∈ S by HNF. Feasibility is guaranteed by §2–3. Infeasibility therefore falsifies GRH, source completeness, or this proof. Solutions have polynomial bits (pivot/Cramer argument from the reviewed note).
5. **Norm lift.** Set q_p = φ₁(u₁)·φ₂(u₂)·φ₃(u₃), with uᵢ ∈ O_{Lᵢ,S}^×. Then nrd(q_p) = p, because nrd restricted to φᵢ(Lᵢ) is N_{Lᵢ/Q}.

**Integrality and certificate.**
- Since φᵢ(O_{Lᵢ}) ⊂ O[1/cᵢ] and the primes of cᵢ lie in S, each block lies in O[1/S]^×, and so does q_p.
- For q ∈ S, a lower bound m_{i,q} on uᵢ's valuations at the primes above q gives q^{m′+v_q(cᵢ)}·φᵢ(uᵢ) ∈ O_q.
- So c_p = ∏_{q∈S} q^{e_q} makes c_p·q_p ∈ O, and nrd(c_p q_p) = c_p²·p.
- The certificate is purely commutative, block by block, and polynomial-bit. **S never grows.**
- Atoms can be made integral by scaling: cᵢ·φᵢ(γ_l) with β_l = γ_l/n_l. Compensate with central factors ∏(cᵢn_l)^{−e_l}. Their non-S primes cancel, and this is checkable.

**What this delivers to GBuild.**
- For K=Q indefinite, Cl_A(Q) = 1 (Page LF143–152). The missing part after Step 4 is the 2-elementary group C from the proof of Theorem 4.8 (LF900–941).
- X = {central p ∈ S, −1} ∪ {c_p q_p} gives ⟨nrd X⟩ = ⟨B⟩. Definition 3.11(ii) holds with φ trivial, which replaces GBuild Steps 5–15.
- Heuristic 4.7, the smoothness and equidistribution assumptions, is no longer needed for the global part.

**Two caveats.**

- **(C1) Exponential valuation magnitudes.** The valuations e_q of the words at S-primes are poly-bit but can be numerically as large as the class number, around √|d|.
  - So c_p must be kept in factored form.
  - Page's Theorem 4.9 bounds PReduce iterations by v_p(nrd J) ≤ log₂(N_X·N(I)). With compact X this can be exponential.
  - Small-valuation relations are unproved; skewed relation lattices are possible.
- **(C2) Compact evaluation of J = cI.** Evaluating cI with compact c needs local evaluation at the S-primes. The plan: factor out uniformizers per block, raise local units to powers in (O_{Lᵢ}/q^k)^×, then map through φᵢ into A_q. This is a proof obligation that I sketch but do not prove.

## 5. Proof obligations and falsifiers

**Proof obligations.**

| ID | Obligation |
|---|---|
| O1 | Polynomial-bit outputs for the quaternary isotropic solver and the conic solver (external sources; locators unverified). |
| O2 | The GRH prime-in-progression density estimate used in Step 1. |
| O3 | Biasse–Song completeness and compact-size guarantees for the Lᵢ, with |S| polynomial. |
| O4 | Local evaluation of compact words for C2. |
| O5 | A valuation bound for C1, or a local reducer that works with compact words. |

**Falsifiers.**
- Any x ∈ Q* outside N₁N₂N₃ for a triple with a degree-4 place.
- A rank- or sign-deficient HNF of the norm matrix for the S defined above.
- A block φᵢ(uᵢ) that is not in O[1/S].
- A Hilbert-symbol miscomputation in §1.
- A suggested finite control (not run): A=(2,3), a=5, fields Q(√5), Q(√6), Q(√30). Check the full rank of the norm matrix and nrd(q_p) for every p ∈ S. A pass would be a check, not evidence for all D.

## 6. Precise remaining gap

**Global norm lift.** Let n = nrd(I). Solving for the target n directly gives g ∈ O[1/S]^× with nrd(g) = n.

**Residual alignment problem.** Find h ∈ A^× with:
- nrd(h) = 1, after adjusting signs and central squares;
- h ∈ O_q^× for q ∉ S;
- h·g·O_q = I_q at every split q ∈ S.

Then α = hg satisfies αO = I.

**Where it is automatic, and where not.**
- At q|D it is automatic: a local maximal order in a division algebra has a unique right ideal of each norm.
- At split q it is an action problem on the product of Bruhat–Tits trees.

**Unpaid items.**
- **Large primes:** for large q (a, the primes of t and of cᵢ, large primes of n), Page's P1Search/PBuild requires q+1 neighbour tables. Heuristic 4.5 is also unpaid.
- **Long walks at small primes:** at small q, the distance to walk can be numerically exponential (C1).
- **Large-p local machinery:** no source in this packet supplies a constructive word or membership compiler for PSL₂(F_q) with large q. I do not import one.

**Not claimed.** No end-to-end algorithm, novelty, speedup or hardness claim is made. Classical subexponential S-units give the matched baseline.

## 7. Locators

| Source | Locators used |
|---|---|
| Page | Thm 2.2 LF131–140; Thm 2.3 LF143–152; Def 3.11, GReduce, Prop 3.13 LF492–569; P1Search, PBuild, GBuild, Prop 3.21 LF573–676; Heuristic 4.7, Thms 4.8–4.9 LF762–941 |
| Prasad–Rapinchuk | Lemma 4.8 and footnote, LF817–866 |
| RELATIVE_NORM_TENSOR_SUPPORT.md | "Relative support theorem"; "Polynomial support"; "Exact relative norm coordinates" |
| Palette review | §§1–3 |
| Standard, not supplied (no locators given) | Artin reciprocity and the cyclic Hasse norm theorem; GRH bounds; Cornacchia; AKS; Simon |