# Simon clock: HNF minimization and a definite-majorant replacement

2026-11-13. Independent review of L1 and L2 only. Fixed dimension
`2 <= n <= 9`; integer factorization is an explicitly allowed resource.
The Bosma--Stevenhagen backend is outside this review.

**Disposition.** Both replacements have polynomial bit cost. The paid
report requires three corrections: Lemma 6 occurs at most once **per
prime**, the minimization rules must be looped with invariants recomputed,
and HNF diagonal entries satisfy a non-strict bound. Arbitrary finite-field
basis changes must not be assumed to lift unimodularly. Direct lattice
construction avoids that issue entirely. The definite-majorant replacement
does produce a full maximal totally isotropic basis, by integral splitting.

Primary source checked: `audits/sources/selmer_classical_two/simon_dim4.txt`,
physical lines 112--184 (unimodular case), 239--343 (Lemmas 4--9 and
Algorithm 3). Advisory report:
`audits/claude_runs/2026-11-13-simon-bit-clock/response.md`, L1--L2.
The source's indefinite-reduction clock and its unpublished `[10]`
dimension-nine assertion are not used.

## L1. Realize each rule as a lattice operation

Let `Q0` be the initial nonsingular integral symmetric matrix,
`D=|det Q0|`, and `max |Q0_ij| <= 2^B`. Store the current form as

\[
 Q=c A^tQ_0 A,\qquad L=A\mathbf Z^n\subset\mathbf Q^n,
 \qquad c=1/C>0.                                        \tag{1}
\]

The scalar is stored separately: division of the form by a nonsquare
prime is not a rational congruence. For isotropy, the backmap is `A`;
the positive scalar preserves the zero set and the signature.

Fix `p|det Q`, put `v=v_p(det Q)` and let `R` be the radical of `Q mod p`,
of dimension `d`. The bilinear form

\[
 \widetilde Q(r,s)=Q(\widetilde r,\widetilde s)/p\pmod p
 \quad(r,s\in R)                                       \tag{2}
\]

is independent of the integer lifts. Changing a lift by `p z` changes
the numerator by a multiple of `p^2`, since `R` is the radical. The usual
block determinant/Schur-complement calculation gives
`d<=v`, with equality exactly when (2) is nondegenerate.

The source's rules can now be implemented without lifting a matrix in
`GL_n(F_p)` to `GL_n(Z)`:

| Rule | New lattice, in current coordinates | Scalar change | Determinant change |
|---|---|---|---|
| 4, `d=n` | unchanged | divide by `p` | `p^{-n}` |
| 5, `d<v` | add `1/p` times lifts of `ker(tilde Q)` | none | `p^{-2k}`, `k=dim ker(tilde Q)>=1` |
| 6, odd `n`, `d=v>=2` even | inverse image of `R` modulo `p` | divide by `p` | `p^{n-2d}` |
| 7, `d=v>=3` | add `1/p` times an isotropic line of `tilde Q` | none | `p^{-2}` |
| 8, `d=v=2`, isotropic `tilde Q` | same line construction | none | `p^{-2}` |
| 9, source hypotheses | inverse image of `R` plus a maximal isotropic subspace of `U` | divide by `p` | `p^{-v}` |

Here `U` is the nondegenerate quotient form modulo `p`. In rule 9 its
isotropic dimension is `m=(n-d)/2`. A preimage of dimension `r` has lattice
index `p^(n-r)`; hence the last determinant factor is
`p^{2(n-d-m)-n}=p^{-d}=p^{-v}`. Isotropic subspaces here have zero
restricted **bilinear Gram matrix**, also at `p=2`.

For a superlattice step, use the generators of `L` together with the
chosen divided lifts. For a sublattice step, use `pL` together with the
chosen undivided lifts. HNF computes the new basis. The congruences in
(2) prove integral Gram entries, and the finite-field ranks give exactly
the indices in the table. No unverified unimodular lift or primitive
completion is required. At `p=2`, the needed fixed-dimensional subspaces
can be found by exhaustive finite-field linear algebra; this costs only
a dimension-dependent constant.

### Termination and the once-per-prime correction

At each prime, repeatedly apply rule 4 or 5 while possible, recompute
`d,v`, and then apply an eligible rule 6, 7, 8, or 9; after every change
restart the tests. Stop at that prime when none applies. This is the
looped interpretation needed for Proposition 10, rather than a literal
single application of the printed step 3.

Only rule 6 can increase `v`. Immediately after that rule,

\[
 d_{\rm new}=v_{\rm new}=n-d\quad\text{is odd and }<n.   \tag{3}
\]

Rule 4 is then impossible because it requires `v>=d=n`. Rules 5 and 7
decrease `v` by an even positive integer. Rule 8 requires the unreachable
even value 2, and rule 9 ends at zero. Thus rule 6 cannot recur at this
prime. Operations at other primes are invertible over `Z_p`, up to a
`p`-adic unit scalar, and cannot change these local invariants.

If `v0=v_p(det Q0)`, the one possible increase is at most `n-4`.
Consequently the number `K_p` of rule applications satisfies the safe
bound

\[
 K_p\le v_0+n,\qquad
 K=\sum_p K_p\le\sum_p v_p(D)+n\omega(D).                \tag{4}
\]

No new determinant prime appears. The terminal conditions agree with
Proposition 10: in odd dimension only `d=v=1` can remain, and not at 2;
in even dimension `d=v<=2`, with `v<=1` at 2 and the indicated residual
isotropy test when `v=2`.

### Original-coordinate HNF gives the height bound

Maintain positive integers `N1,N2` such that

\[
 N_1\mathbf Z^n\subset L\subset N_2^{-1}\mathbf Z^n.
\]

A superlattice step multiplies `N2` by `p`; a sublattice step multiplies
`N1` by `p`; a pure scalar step changes neither. By (4),

\[
 N_1N_2\le\prod_{p|D}p^{v_p(D)+n}
       \le D^{n+1},\qquad C\le D^{n+1}.                 \tag{5}
\]

After each step take the HNF basis `H` of the integral lattice `N2 L`
and set `A=H/N2`. Since `N2 L` contains `(N1 N2)Z^n`, every HNF diagonal
entry divides `N1 N2`; its reduced off-diagonal entries are smaller than
a diagonal pivot. Thus **all** entries have magnitude at most `N1 N2`,
including the equality case. In particular `|A_ij|<=N1`, and

\[
 |Q_{ij}|\le n^2 2^B D^{2(n+1)}.                        \tag{6}
\]

Recompute `Q=H^t Q0 H/(C N2^2)` exactly in original coordinates. The
denominator divides every numerator by the integral-lattice construction.
The matrices, common denominators, scalar, and backmap all have
`O_n(B+log D)` bits. Since `log D=O_n(B+1)`, fixed-dimensional HNF,
finite-field linear algebra, and these exact operations have polynomial
bit cost. In particular, tracking a long product of arbitrary basis
changes is unnecessary.

For completeness, the modular randomness can have a finite clock. After
diagonalization at odd `p`, a ternary isotropic vector is obtained by
fixing one coordinate to 1, sampling another, and testing whether the
required square is a residue. The elementary quadratic-character sum
shows at least `(p-1)/2` successful choices. A raw `ceil(log2 p)`-bit
trial, rejected when out of range, therefore succeeds with probability
at least `1/6`. A verified Tonelli--Shanks nonresidue has at least the
same success bound. Allow `6 ceil(log2(J/eta))` trials per randomized
subcall, where a fixed dimension-dependent multiple of `K+1` bounds their
total number `J`. Exhaustion is `ABORT`, not a mathematical obstruction.
This gives total abort probability at most `eta` and a clock polynomial
in `B,log(1/eta)`. All modular witnesses are checked exactly.

## L2. A deterministic majorant replacement for unimodular reduction

Let `Q` be integral, `det Q=+/-1`, and indefinite. Compute its leading
principal minors `d_i`, with `d_0=1`. If a leading block of size `i<n`
is singular, any nonzero kernel vector of that block, padded with zeros,
is isotropic. Rational linear algebra, clearing denominators, and dividing
by the integer gcd give a primitive vector with polynomially many bits.

Otherwise rational LDL decomposition gives

\[
 Q=L^t D_0 L,\quad D_0=\operatorname{diag}(d_i/d_{i-1}),
 \quad P=L^t|D_0|L.                                    \tag{7}
\]

The unit triangular matrix `L` and the positive definite rational matrix
`P` have polynomial bit length. Moreover `det P=1` and

\[
 |Q(u,v)|\le\sqrt{P(u)P(v)}.                            \tag{8}
\]

Clear the denominators of `P` by one positive scalar and run ordinary
exact definite LLL with parameter `3/4`. Scaling does not change the
reduction conditions. It returns a unimodular integer basis matrix `U`
with polynomial bit length. Write its columns as `b_i` and its
Gram--Schmidt squared lengths for `P` as `B_i`.

If `P(b1)<1`, then the integer `Q(b1)` has absolute value below 1, so it
is zero. Otherwise size reduction and Lovasz give

\[
 B_i\ge2^{-(i-1)},\qquad \prod_i B_i=1,
 \qquad B_i\le2^{n(n-1)/2}.
\]

Consequently

\[
 P(b_i)\le C_n:=n2^{n(n-1)/2},\qquad
 |(U^t Q U)_{ij}|\le C_n.                               \tag{9}
\]

There are only finitely many integral symmetric matrices with the bounds
(9), determinant `+/-1`, and indefinite signature, for fixed `n`. Each
is isotropic by the standard indefinite-integral-unimodular existence
theorem explicitly invoked in Simon section 1, `[7, Th. V.3]`.
Enumerating integer vectors in increasing boxes therefore terminates
within a constant depending only on `n`. This is a proof from that
universal theorem and finiteness, **not** an inference from a finite scan.
The constant is effective: enumerate the finite matrix set and search
for a zero of each; the theorem proves that this input-independent
precomputation halts. No such scan was run or assumed as evidence here.

Thus one can find an isotropic vector of the bounded matrix and multiply
it by `U`, obtaining polynomial coordinate size and polynomial bit cost
in the original input. The constants may be enormous. This is not a
uniform polynomial algorithm when `n` grows.

### Full integral splitting, not merely one vector

Make the resulting vector `v` primitive. Since `Q` is unimodular, `Qv`
is primitive. Extended gcd gives an integer `w` with `v^t Qw=1`, of
polynomial bit length. Replace

\[
 w\leftarrow w-\lfloor Q(w)/2\rfloor v.
\]

Then the plane spanned by `v,w` has Gram matrix
`H_epsilon=[[0,1],[1,epsilon]]`, where `epsilon` is 0 or 1. Its determinant
is `-1` and its signature is `(1,1)`. The integral orthogonal projection
onto its complement is explicitly

\[
 \Pi(x)=x-(Q(w,x)-\epsilon Q(v,x))v-Q(v,x)w.              \tag{10}
\]

The image of the integer matrix `Pi` is the entire orthogonal-complement
lattice: every integral vector already in the complement is fixed.
Compute an HNF basis of the lattice generated by `Pi(e_i)`. Together
with `v,w` it is a basis of `Z^n`, because (10) gives an integral direct
sum. The complement is integral unimodular, has determinant `-det Q`
and signature `(r-1,s-1)`, and has polynomial coefficient size.

Recurse while the complement is indefinite. The depth is at most
`floor(n/2)`, a fixed constant. Taking the first vector from each plane
gives a totally isotropic basis of dimension `min(r,s)`, and all
coordinate maps have polynomial bit length. A merely rational kernel
basis, which could miss the saturated complement lattice, is not used.

These arguments close L1 and L2 at their stated fixed-dimensional scope.
They do not supply the separately reviewed binary-class-group algorithm
or certify the rest of Simon's composition by association.
