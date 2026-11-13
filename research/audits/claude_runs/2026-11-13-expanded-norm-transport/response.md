# Audit report: expanded norm witnesses and quaternion/ternary common space

**Labels used below.**
- **[D]**: my own deduction from the packet's definitions.
- **[S]**: a supplied theorem or contract that I did not re-verify.
- **[O]**: open.

## Verdict

I found no decisive error in the three requested steps. I tried the cheapest attacks first:

- a sign error in the E-split norm identity;
- failure of root existence for X^d−c, a0/c, d0/t and detA/detB;
- hidden field-degree or support growth as d grows;
- unsupplied coordinates (primitive element, K-basis, maximal orders, embeddings).

All of these fail. Each step holds for every input inside the stated contracts. The proofs depend only on the following interfaces:

- **[S1]** The admitted backend returns NO, or a non-nested power product of polynomially many polynomial-size expanded L-atoms with binary exponents and exact norm a. This holds under GRH, at bounded error, with expanded targets only.
- **[S2]** Lenstra (IW213/82, Thm 3.7, as described in the packet; I have not read it) factors f∈Q(α)[X]. Here α has a monic integral minimal polynomial. Both the operation count and the integer bit lengths are polynomial in [Q(α):Q], deg f and the coefficient bits.
- **[S3]** The charged Hilbert-symbol/ramification tests, including dyadic places.
- **[S4]** Buchmann–Lenstra maximal orders from Shor-factored discriminants, and Shor factoring itself.

**What is established:** an exactly verified, polynomial-size rational isometry between the ternary spaces, plus a polynomial, factorable exceptional prime set.

**What is not established:** the integral-isometry decision **[O]**.

## 1. Exponent-residue decompactification, growing d

**Claim [D | S1, S2].** The inputs are:
- fields K⊆L with maximal-order tables and an embedding, d=[L:K];
- a∈K*;
- β=∏_{i≤t} b_i^{e_i} with N_{L/K}(β)=a, where the b_i are nonzero expanded atoms and the e_i are binary.

Then a deterministic classical procedure outputs an expanded β′ with N_{L/K}(β′)=a. Its time and output size are polynomial in the input bits, t, the maximum atom size and d.

**Identity.**
- Write e_i=dq_i+r_i with 0≤r_i<d. Floor division handles negative e_i.
- Then β=β0·γ^d, where β0=∏b_i^{r_i} and γ=∏b_i^{q_i}.
- Since N_{L/K}(γ^d)=N(γ)^d, we get c:=N(β0)/a=(N(γ)^{-1})^d. So c is a d-th power in K: **base-field root existence holds.**
- On K, N_{L/K} restricts to z↦z^d. Hence for any z∈K with z^d=c, N(β0/z)=N(β0)/c=a.
- Different roots differ by d-th roots of unity in K; all of them are valid.
- γ and β are never evaluated.

Two edge cases:
- If "signed" in [S1] means an overall ±1 or root-of-unity factor, treat that factor as an atom with exponent 1.
- If any atom is itself a nested compact representation, flatten it first. Then t counts the flattened atoms.

**Size bounds [D].**
- Use the integral basis, whose structure constants are integers with |c_ijk|≤2^τ.
- For integral x, y: ‖xy‖∞ ≤ N²·2^τ·‖x‖∞‖y‖∞, where N=[L:Q].
- Write each atom as b_i=b_i′/D_i with b_i′ integral and D_i∈Z.
- A product of k≤t(d−1) atoms then has bit size ≤ Σ size(b_i) + k(τ+2log N).
- This is linear in d, and d≤N is an input dimension. No splitting field or compositum is formed.

**Norm computation [D].**
- Compute N_{L/K}(β0)=∏N_{L/K}(b_i)^{r_i}.
- Each factor is a d×d determinant over K, taken in a K-basis of L.
- The K-basis is chosen greedily from the Q-basis, using Q-rank tests on the products {κ_j ℓ_i}.
- Fraction-free elimination keeps every intermediate a minor, so sizes stay polynomial.
- Obligation: the N×N rational determinant gives N_{L/Q}, not N_{L/K}. "Norm by determinant" must mean the K-linear one.

**The root has intrinsically small size [D].** This holds whatever algorithm finds z.
- Pick D∈Z with Dc∈O_K. Then (Dz)^d=D^{d−1}(Dc)∈O_K, so Dz∈O_K.
- Moreover |σ(Dz)|=D·|σ(c)|^{1/d} at every embedding σ.
- Inverting the embedding matrix then bounds the integer coordinates of Dz polynomially.
- Check z^d=c exactly.

**Finding z [S2].** Factor X^d−c over K=Q(α) and take any linear factor.

**The primitive-element deduction is correct [D].**
- For a next basis element b, call t bad if σ(α+tb)=τ(α+tb) for some pair of distinct embeddings σ≠τ of Q(α,b).
- If σ(b)=τ(b), then σ(α)≠τ(α), so no t is bad for that pair. Otherwise exactly one t is bad. So there are at most n(n−1)/2 bad values.
- Hence at least one of the n(n−1)/2+1 tried values is good.
- Every candidate α+tb has degree ≤[Q(α,b):Q], with equality exactly when it generates. So the maximal-degree candidate generates.
- α is an integer combination of integral basis elements, so its minimal polynomial is monic in Z[x].
- The procedure needs O(n³) exact minimal-polynomial computations, all of polynomial size.

**Scope.** The output preserves the exact fractional norm only. It does not preserve integrality, S-support, archimedean signs or β itself. Pell-type integral bounds are therefore irrelevant.

## 2. Quaternion isomorphism A=(c,d0) → B=(a0,b)

### Split branch [D]

With i=[[0,a0],[1,0]] and j=[[x,−a0y],[y,−x]], where x²−a0y²=b:
- i²=a0I.
- j²=(x²−a0y²)I=bI.
- ij=[[a0y,−a0x],[x,−a0y]]=−ji.

A nonzero homomorphism from a central simple algebra into M2(K) is injective, hence an isomorphism. If a0=s² is a square, use i=diag(s,−s) and j=[[0,b],[1,0]]. Two split algebras are matched by composing through M2(K) and inverting a 4×4 K-linear map.

### Division branch: constructing x with x²=c [D]

Since A and B are division algebras, c∉K² and a0∉K². Let E=K(√c).

**Case a0∈E².** If (u+v√c)²∈K then uv=0. Since a0∉K², this forces a0=cs² with s∈K*. Then x=i_B/s satisfies x²=c.

**Case a0∉E².** E embeds in A≅B, so B_E is split and b∈N(E(√a0)*). The first norm equation is therefore soluble.
- Call [S1] on E(√a0)/E. The absolute degree is 4m, where m=[K:Q], and the target b is expanded.
- Decompactify with d=2, so at most t atoms.
- Under √a0↦i, q=z+j satisfies Nrd(q)=N(z)−b=0, and q≠0.
- Write q=u+v√c with u, v∈B. Then

  Nrd_{B_E}(q) = q·q̄ = (Nrd u + c·Nrd v) + Trd(u v̄)·√c.

- Both bracketed terms lie in K and {1,√c} is a K-basis of E, so both vanish. **The packet's sign (+c) is correct.**
- If v=0, then u would be a nonzero norm-zero element of the division algebra B. So v≠0 and Nrd v≠0.
- Set x=u v^{-1}=u v̄/Nrd v. Then Trd x=0 and Nrd x=−c. The reduced characteristic polynomial gives x²=Trd(x)·x−Nrd(x)=c.
- x∉K, because c∉K².

### Second relative norm [D]

**The anticommuter.**
- Since x² is central, conjugation by x is an involution of B.
- Its +1-eigenspace is the centralizer K(x), of dimension 2 because K(x) is a maximal subfield. So the anticommuter W has dimension 2.
- Write y0=s+p with s∈K and p pure. Then xy0+y0x=2s·x+Trd(xp). So y0∈W forces s=0: y0 is pure.
- Hence t=y0²=−Nrd y0∈K*, using that B is division.
- K(x)·y0⊆W has dimension 2, so W=K(x)·y0.

**Solubility.** This self-contained proof replaces the packet's appeal to the "classification".
- Let ψ:A→B be any isomorphism; one exists by hypothesis.
- ψ(i_A)²=c=x², so by Skolem–Noether some conjugate of ψ satisfies ψ(i_A)=x.
- Then ψ(j_A)∈W, so ψ(j_A)=w(x)y0 for some w∈E*.
- Squaring gives d0=w(x)·y0·w(x)·y0=w(x)·w̄(x)·y0²=N_{E/K}(w)·t.
- **So d0/t∈N(E*).**

**Converse.** Every solution w gives y=w(x)y0 with:
- xy=−yx;
- y²=N(w)·t=d0, using y0·w(x)=w̄(x)·y0.

Then i_A↦x, j_A↦y is an isomorphism, since it is a homomorphism from a central simple algebra between equal dimensions.

**Sizes and verification.** The chain z → u, v → x → (4×4 kernel) y0 → t → w (decompactified) → y consists of polynomially many exact operations on polynomial-size data. The relations x²=c, y²=d0 and xy=−yx are checked exactly.

Solubility is guaranteed in every call made inside the division branch. So a backend NO there is a detectable failure; it is retried or reported as an inconsistency in [S3]. It is never silently trusted.

## 3. Ternary determinant normalization [D]

**Diagonalize.**
- Find P_A with P_Aᵀ A P_A=diag(a1,a2,a3). In characteristic 0, a pivot vector with q≠0 always exists; this is fixed rank and polynomial.
- Take q(e_k)=a_k. Then C0≅(−a1a2, −a2a3) via i=e1e2, j=e2e3.

**The volume element.**
- ω=e1e2e3 is central in C(V), with ω²=−a1a2a3=−det.
- The reversion τ gives τ(ω)=−ω, and τ restricts to the canonical involution on C0.
- For v∈V, ωv lies in the pure part of C0. Concretely: ωe1=a1e2e3, ωe2=−a2e1e3, ωe3=a3e1e2.
- Its reduced norm is Nrd(ωv)=ωv·τ(ωv)=q(v)·ω·τ(ω)=**det·q(v)**. The packet's sign is correct.
- If one uses squares instead, (ωv)²=−det·q(v). The extra sign cancels in the ratio below.

**The similitude and the scalar correction.**
- Any isomorphism φ:C0(A)→C0(B) preserves Nrd and maps pure elements to pure elements.
- Define Ψ(v)=ω_B^{-1}·φ(ω_A v). This lies in V_B, because ω_B·V_B equals the pure part of C0(B) by an injectivity and dimension count.
- Then q_B(Ψv)=(detA/detB)·q_A(v).
- If detA/detB=s², then X=s^{-1}Ψ is an isometry. Conjugating back by P_A and P_B gives the isometry for the original Gram matrices.
- Conversely, any isometry induces a C0-isomorphism and mak