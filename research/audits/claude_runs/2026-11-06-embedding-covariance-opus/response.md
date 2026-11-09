# Verdict: **ACCEPT** for this conditional removal only

Choosing any root of t^ell = A classically, and evaluating every algebraic quantity in Sections 3–4 under the single embedding that root induces, removes all quantum Gauss-phase calls from those sections.

- **No failed identity.** Every equivariance identity checks with the stated signs.
- **Output invariance follows** because the selected exponent a is embedding-independent, and every later step is exact abstract arithmetic.

The acceptance depends on four written obligations (O1–O4, below). None is a new primitive. Two of them (O1, O3) already existed silently in the old text. Under the new text a convention error would no longer be visible, so they must be stated explicitly.

The end-to-end bound remains quantum because of the upstream sources. This is not a classical recovery of the physical Gauss-sum phase.

## 1. One fixed abstract isomorphism

Fix the physical field L = Q(zeta, zeta_p)^{...} = K(zeta) inside C, with zeta = exp(2πi/ell) and zeta_p = exp(2πi/p). Physical Gauss sums use this zeta_p; physical c and alpha are defined by (1).

**Conditional on the Jacobi convention (O1):** J_a = J(chi^a, chi) = tau(chi^a)tau(chi)/tau(chi^{a+1}) for 1 ≤ a ≤ ell−2. Then:

- tau(chi)^j = P_j · tau(chi^j).
- tau(chi)^ell = P_{ell−1} · tau(chi) · tau(bar chi) = P_{ell−1} · chi(−1) · p = A, since chi(−1) = 1 for odd ell.

So there is a unique Q(zeta)-isomorphism φ: E → L with φ(t) = tau(chi). It satisfies:

- φ(tau_j) = tau(chi^j).
- φ(p/t) = tau(bar chi).
- Physical sigma (zeta_p ↦ zeta_p^g) sends tau(chi) to bar chi(g)·tau(chi) = zeta^{−1}·tau(chi). This matches the abstract sigma(t) = zeta^{−1}t, so φ∘sigma_abs = sigma_phys∘φ.

Define the abstract elements c_abs := φ^{−1}(c), alpha_abs := φ^{−1}(alpha), and P_L as the unique prime of E above (zeta − r, p). That prime is totally ramified, hence sigma-fixed and embedding-independent.

The proof never needs to know φ. It needs only that φ exists. Write iota_0 := incl∘φ. The embeddings of E fixing zeta are exactly iota_b := iota_0∘sigma^b, with iota_b(t) = zeta^{−b}·iota_0(t). The classical choice picks some unknown b.

**On "c analytic vs abstract".** The correct statement is not that φ_b^{−1}(c) satisfies (2) under iota_b. The correct statement is that the same c_abs satisfies (2) under every iota_b (Section 2). The alternative isomorphisms φ∘sigma^b are never used. This sidesteps the apparent paradox that "the true c" moves with the isomorphism.

## 2. Covariance identities (signs checked)

Write T_j^b(x) = Σ_t zeta^{jt} log|iota_b(sigma^t x)|.

**(i) Unit modes rotate.**
T_j^b(x) = Σ_t zeta^{jt} log|iota_0 sigma^{t+b} x| = zeta^{−jb}·T_j^0(x).

**(ii) Gauss terms rotate the same way.**
iota_b(tau_j) = iota_0(sigma^b(t)^j)/P_j = zeta^{−jb}·iota_0(tau_j). This uses that P_j ∈ Q(zeta) is fixed by sigma and that zeta is not moved.

**(iii) Unchanged quantities.** L(1, bar chi^j) and (1 − zeta^{−j}) depend only on chi and on the fixed embedding of zeta.

**(iv) Formula (2) under iota_b.**
T_j^b(c_abs) = zeta^{−jb}·T_j^0(c_abs) = zeta^{−jb}·RHS_0 = (1 − zeta^{−j})·iota_b(tau_j)·L(1, bar chi^j)/2.
So (2) holds in every iota_b for the same abstract c_abs. The physical identity (2) is assumed, not re-audited.

**(v) Module action.**
T_j^b(sigma x) = zeta^{−j}·T_j^b(x), hence T_j^b(c0^u) = u(zeta^{−j})·T_j^b(c0) for every b.

**(vi) Real units stay real.** For a real unit v of R, v(zeta^{−j}) is real, because its conjugate is v(zeta^{j}) = bar v(zeta^{−j}) = v(zeta^{−j}).

**Consequences.** Write c_abs = c0^u with u = zeta^a·v. The quotient RHS_b / T_j^b(c0) = zeta^{−aj}·v(zeta^{−j}) does not depend on b.

- Its phase modulo π selects the same a.
- The largest-mode choice is unchanged, because |T_j^b| = |T_j^0|.
- The error budget only improves: iota_b(tau_j) is now an exact algebraic number known to any requested precision. The phase budget pi/(8ell) is then spent only on the L-phase and on the root factor.

## 3. Output invariance

After a is fixed, every remaining step is exact abstract arithmetic:

- c1 = sigma^a(c0);
- the residue test of c1² mod P;
- the cyclotomic unit eta_{a0};
- the integer coordinate solve for epsilon;
- alpha2 = beta·epsilon;
- the quotient alpha2·t/p reduced mod P_L.

None of these reads an embedding. The proof of (6)–(7) applies verbatim to c_abs, alpha_abs and p/t = φ^{−1}(tau(bar chi)). So the abstract alpha2, and the residue alpha2/(p/t) mod P_L, are identical for every b, and equal k! mod p.

**Distinction from recovering the Gauss phase.** The algorithm never learns b. It does not output, or implicitly determine, arg tau(chi) in C. Invariance of the output is not a classical Gauss-phase computation. It only shows that this particular residue is independent of the choice of root.

Any later step that read a physical complex value would silently re-import the debt. Examples:
- comparing with c computed from exp(2πi/p);
- numerical identification of tau(chi) itself;
- reuse of the chosen root as "the" Gauss sum elsewhere.

## 4. Falsifier: computed, not just predicted

**Mixed embeddings.** Suppose the Gauss terms use iota_{b'} but the unit modes use iota_b, with s = b' − b.

- By (i)–(ii), the right-hand side gains an extra factor zeta^{−js}. The selected exponent becomes a' = a + s.
- Then c1' = sigma^{a+s}(c0), and c_abs = c1'^{zeta^{−s}v}.
- The residue c1'² mod P equals c0² mod P, because sigma acts trivially on the residue field. So b and a0 are unchanged.
- Then c2' = c_abs^{w'} with w' = zeta^s·w, where w is the correct real value with w ≡ 1 mod λ².
- Hence w' ≡ 1 + sλ mod λ², and b'' = (w' − 1)/λ ≡ s mod λ.
- The argument behind (6) gives alpha2'/alpha_abs = delta^{b''}, up to a sigma-fixed norm-one unit, which is +1 in odd degree.
- Reducing at P gives alpha2'/alpha_abs ≡ r^{s}, because delta ≡ r at P and λR ∩ Z = ellZ.

The mixed output is therefore k!·r^{s}, with the sign of s convention-dependent. It is wrong exactly when s ≢ 0 mod ell.

**Consistent embeddings.** Changing both choices together gives s = 0, and the output is unchanged.

This confirms the cheapest falsifier and pins its exponent to the root-index mismatch.

## 5. Proof obligations to write into the text

**O1. Jacobi orientation certificate.** Existence of φ requires the abstract J_a to be Jacobi sums of exactly our chi, with chi(g) = zeta. They must not belong to bar chi or to any chi^m with m ≠ 1.

- *Why it matters now:* under the old text a wrong orientation also failed silently, since the "nearest root" was chosen anyway. Under the new text no geometric check remains, so this must be certified.
- *Cheap exact certificate:* check J_a ≡ 0 mod (zeta − r, p) for every 1 ≤ a ≤ ell−2. Section 4 already asserts this vanishing; it should be performed as a runtime check.
- *Why it certifies m = 1:* if the source sums are J(chi^{ma}, chi^m), their reductions are Σ_x x^{⟨ma⟩k}(1−x)^{⟨m⟩k}.
  - If ⟨ma⟩ + ⟨m⟩ < ell, every exponent lies in (0, p−1), so the sum is 0.
  - Otherwise the sum equals −binom(⟨m⟩k, p−1−⟨ma⟩k), with all entries less than p. By Lucas this is nonzero mod p.
  - For m ≠ 1, take a ≡ −m^{−1}, which lies in [1, ell−2]. Then ⟨ma⟩ = ell−1, so the sum is nonzero.
- *Consequence:* vanishing for all a forces m = 1. Cost: ell reductions.
- Mixing up Tal's zeta ↦ r^{−1} source prime with our local zeta ↦ r prime is exactly the error this test catches.

**O2. The embedding of K is induced, never chosen separately.** Numerical eta_i must be computed as iota_b(eta_i) = (−1 + Σ_j iota_b(tau_j)·zeta^{?})/ell. The exponent comes from the identity eta_i = sigma^i(eta_0), with exact abstract sigma.

Equivalently, choose one real root for eta_0 and generate eta_1, eta_2, … with the exact sigma-polynomial. In that case the Gauss terms must use t = Σ zeta^i eta_i under that same assignment.

Sorting the real roots of the period polynomial, or ordering them independently, is precisely the mixed-embedding falsifier of Section 4.

**O3. The c0 source uses the same sigma convention.** The R-module structure of the supplied generator c0 (zeta acting as sigma) must be the abstract sigma with sigma(t) = zeta^{−1}t, equivalently eta_i ↦ eta_{i+1}.

If the source used sigma^{−1}, then T_j acquires a j ↦ −j twist relative to (2), and a is wrong by a nontrivial residue power. This is the same "replace j by −j in only one place" error the text already forbids. Under the old text it also existed and was hidden.

**O4. Delete or replace the quantum lines.**
- Section 3: "Known Gauss-phase estimation has polynomial(logp, ell) cost at these tolerances."
- Section 4: "The known Gauss-phase primitive … selects the intended t = tau(chi)," and "identifies the correct real embedding of K." Replace these with: any root gives a valid real embedding of K compatible with sigma. Correctness of the output is proved by covariance, not by physical identification.
- Charge the replacement cost: evaluate A ∈ Z[zeta], whose coefficients have poly bits and |A| = p^{ell/2}. Extract one ell-th root by certified Newton iteration to poly(ell, log p) bits. Form the ell−1 values tau_j, then the eta_i. All of this is classical poly(ell, log p) work.

## 6. Scope

This removes quantum Gauss-phase estimation from Sections 3–4 only, conditional on:

- the reviewed exact class/unit/Fitting/c0 sources;
- formula (2);
- the local congruence (7);
- the classical dyadic L1 estimator.

It does not dequantize S-units, factoring, class generation or any upstream source that might itself fix an embedding. Any such upstream source must also output exact algebraic data, or be covariant in the same way. It implies no classical algorithm for physical Gauss-sum phases, and no general classical factorial computation.