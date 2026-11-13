# Classical sequential sampler for two-color full-reversal rational scattering: exact recurrences, a falsifier, and the open step

## Verdict

**OPEN.** I could not derive a positive, polynomial-size representation that stays closed under observing one more output bit, for arbitrary extensive-weight b.

What I can supply:

- **(i)** An exact sequential recurrence. It is closed under one more bit, but its state is exponential.
- **(ii)** An exact positive (density-operator) formula for any k-bit prefix marginal. Its Kraus operators are rational-XXX monodromy entries. It is polynomial only for k = O(log N).
- **(iii)** An exact classical Markov chain for the first output bit.
- **(iv)** A decisive N=3 falsifier of the natural classical closure of (iii).
- **(v)** The precise "promotion" step that would have to be compressed.

All finite checks below are by hand against the attached controls. I executed no code.

## 1. Conventions

G(d) acts on an adjacent position pair as follows:

- |00⟩ and |11⟩ are fixed.
- |01⟩ ↦ (c|01⟩ + i d|10⟩)/(c+id).
- |10⟩ ↦ (c|10⟩ + i d|01⟩)/(c+id).
- d = v_left − v_right > 0, with rapidities tracked through crossings.
- In the classical-coin language, transmit (colors follow lines) has probability τ(d) = d²/(c²+d²), and reflect has probability c²/(c²+d²).

**Peeling word.** Move the *smallest* remaining rapidity from the right end to the leftmost unfinished position, then recurse.

- **Proved, given the parameter-dependent YBE:** Ř₁₂(x)Ř₂₃(x+y)Ř₁₂(y) = Ř₂₃(y)Ř₁₂(x+y)Ř₂₃(x), with Ř ∝ dP − ic. This is the note's z₂ = z₁ + z₃, which the attached control checked.
- With that YBE, Matsumoto's theorem implies every reduced word of w₀ with tracked rapidities gives the same U.
- So the peeling word equals the note's bubble word.
- After chain k, output position k is never touched again.

## 2. Exact recurrence R1 (closed under one more bit; exponential state)

**Invariant at stage k.**

- Positions k..N−1 hold the lines v₀ > … > v_{N−1−k}.
- The state is ψ_k ∈ span{|z⟩ : z ∈ {0,1}^{N−k}, |z| = M − |x_{<k}|}.
- Exact Q(i) entries, with ‖ψ_k‖² = p(x_{<k}).
- Initial condition: ψ₀ = |b⟩.

**Update.**

1. For j = N−2−k down to 0, apply G on positions (k+j, k+j+1) with d = v_j − v_{N−1−k}. Call the result φ.
2. Compute p(x_k = s | x_{<k}) = ‖⟨s|_k φ‖² / ‖ψ_k‖².
3. Set ψ_{k+1} = ⟨x_k|_k φ.

**Correctness.**

- Measuring position k right after chain k equals measuring at the end, because no later gate touches it.
- Normalization is exact by unitarity.

**Clocks.**

- Each gate multiplies denominators by (c+id), which has O(L) bits. Entry bit lengths are therefore O(N²L).
- Each conditional is an exact rational. An exact Bernoulli draw by lazy comparison with uniform bits uses O(1) expected random bits.
- So the TV error is 0 and the bit/conditioning clock is polynomial.
- **Size is the only failure:** the state has dimension C(N−k, m_k).
- A provable side bound: ψ_k is a sequentially generated MPS whose ancilla is the k-qubit block (see §3). Its Schmidt rank across any cut is therefore ≤ 2^k. This is still exponential, and I make no improvement claim.

**Hand checks.**

N=3, c=1, v=(2,1,0), input |010⟩:

- Chain 0 gives [(|010⟩ + 2i|100⟩)/(1+2i) + i|001⟩]/(1+i), so p(x₀=1) = 4/10 = 2/5.
- Conditioning on x₀=0 leaves a|10⟩ + b|01⟩ on positions 1,2, with a = (−1−3i)/10 and b = (1+i)/2.
- Applying G(1) gives |a+ib|²/2 = 1/5 and |ia+b|²/2 = 2/5.
- This matches (2/5, 1/5, 2/5).

N=4, v=(3,2,1,0), input |1010⟩:

- p(x₀=0) = 9/100 + 9/20 = 27/50, so p(x₀=1) = 23/50 = p01+p02+p03 ✓.
- Continuing one stage gives p23 = |−6/((1+3i)(1+2i))|² · 2/5 = 36/125 ✓.

## 3. Positive k-prefix channel R2

Call lines a_l = v_{N−l} (l = 1..k) the *block*; they become outputs 0..k−1. Lines j = 0..N−k−1 are the *environment*.

**Algorithm.**

1. Set ρ₀ = U_blk |b_{N−k}…b_{N−1}⟩⟨·| U_blk†. This is the full reversal of the last k inputs, after which block position l−1 holds a_l.
2. For j = N−k−1 down to 0:
   - Prepend an environment qubit e = |b_j⟩ on the left.
   - Apply G₍₀,₁₎(v_j − v_{N−1}), then G₍₁,₂₎(v_j − v_{N−2}), …, then G₍ₖ₋₁,ₖ₎(v_j − v_{N−k}).
   - Trace out position k.
3. Output p(x_{<k}) = ⟨x_{<k}|ρ|x_{<k}⟩.

**Proof.**

- *(a) Unitary cancellation.* In the peeling word, chains ≥ k act only on positions ≥ k, after chains < k. They commute with Π_{x<k} ⊗ I and cancel in the doubled network. This is the only unitarity cancellation available, and it is exact.
- *(b) Reordering.* The remaining crossings are block–block and block–environment. The schedule above respects every line's crossing order, so it is the same wiring diagram up to dis