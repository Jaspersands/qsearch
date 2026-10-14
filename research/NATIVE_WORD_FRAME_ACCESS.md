# Native Word Frame: Row Access, Garbage And Noise

Local derivation / external review pending. This is an access contract and
bounded receiver reference, not an efficient fibre circuit or new algorithm.
It specializes the existing projected-comparison and canonical-PGM audits
to the ACTUAL ternary word map and original noisy records.

## A Legal Alternative Preparation, Not An Unknown Input Oracle

For each paired original record(a,y1),(c,y2), compile the three phases
(y1,y2-y1,-y2) and frequencies(a,c-a,-c), including the known source mask.
A Hadamard on the power-two cohort register and F3 on M qutrits, followed by
cohort-controlled known diagonal phases, prepares

```
|psi_y> = D^(-1/2) sum_x omega^(eta_x) |x>,  D=B*3^M.
sigma_x = sum of actual selected original frequencies.
eta_x = sigma_x.(s+mask) + beta_x.e (modq).
```

This is a separately compiled feature state from the same original data.
It is NOT automatically the previous native point seed, an unknown input
inverse, or a new chosen-frequency oracle. The all-word table is not needed
to compile the indexed local phases: all2BM original rows, B*M controlled
local diagonal gates and their precision must be charged. The finite
reference below materializes a table only under a hard calibration cap.

## Three Different Access Primitives

Let eta_sigma count words with public frequency sigma, p_sigma=eta_sigma/D,
and |F_sigma>=eta_sigma^(-1/2) sum_(x:sigma_x=sigma)|x>.

```
V: |x>|0> -> |x>|sigma_x>                 [easy forward computation]
J: |x> -> D^(-1/2)|sigma_x>               [projected comparison block]
Q: |F_sigma> -> |sigma>                  [clean normalized fibre erasure]
```

J J^dagger=diag(p_sigma). Its singular values are sqrt(p_sigma), not1.
Q is J's partial polar isometry; it requires multiplication by p_sigma^(-1/2)
on support. A condition number close to1 does not remove that absolute scale.
A balanced family has singular values1/sqrt(N), N=q^n, even at huge D.
Applying J to the feature state and inverse GROUP Fourier transform gives
the previous weighted kernel, with ideal herald sum p_sigma^2 and ideal
correct-and-herald1/N. Repeating that postselection or ordinary amplification
does not constitute a new normalized-row implementation.

The inverse of clean Q prepares normalized uniform fibres, not merely one
valid word per target. A short-preimage receipt alone does not implement Q.
Discarding the word pointer after V gives diag(p_sigma), for ALL actual
compiled phases. It has no secret phase; a subsequent group Fourier
measurement is uniform1/N. Forward computation plus throwing away garbage
is not normalized fibre erasure. This argument is scoped to that discarded
pointer, not all possible entangled-work circuits.

## Conditional Clean Receiver And Actual Noise Leakage

On the ideal feature state, Q followed by inverse Fourier on(Z_q)^n has
unconditional true-secret success

```
P_ideal = (sum_sigma sqrt(eta_sigma))^2/(D*N).
```

With actual phases define z_sigma=D^(-1)sum_(x:sigma_x=sigma)omega^(eta_x).
The hypothetical clean receiver's good amplitude is z_sigma/sqrt(p_sigma).
Its herald is sum |z_sigma|^2/p_sigma <=1; the remainder is fibre-orthogonal
failure, not silently discarded. The reference dilation explicitly retains
(I-P_fibre)|psi_y> in a failure register and preserves total norm.
The Fourier transform is the product/group transform, not a cyclic QFT_(q^n)
on a lexicographic index. That distinction matters for n>1.

For fixed original unwrapped errors e, averaging selector words cancels all
cross-site terms, even when those ORIGINAL errors are correlated/noncentred:

```
average_x (beta_x.e)^2
 = 2/(3B) sum_(original pairs)(e1^2+e2^2-e1*e2)
 <= (1/B) sum_(original rows)e_i^2.
delta_pure^2 <= (4*pi^2/q^2)*average_x(beta_x.e)^2.
```

Thus marginal E e_i^2<=V suffices for E delta_pure^2<=8*pi^2*M*V/q^2.
The implemented rational conservative bound uses pi^2<10, giving80MV/q^2.
No original independence, centring, or fresh errors per word is required.
Contractivity of the COMPLETE good+failure measurement and Jensen give
mean loss<=sqrt(min(1,80MV/q^2)) from the ideal reference's unconditional
success. This is not conditioned on herald, a coverage guarantee, or a
generic gate-noise budget. The ideal success may itself depend on labels;
noise moments do not establish balanced fibres. Physical synthesis/gate
errors must be added separately before any algorithm claim.

## Actual Random-Label Coverage, Not Hypothetical Exact Balance

For IID uniform original public labels over(Z_q)^n, ANY two distinct native
words collide with probability1/N. A distinct selector pair has a difference
with at least one coefficient1,-1,2 or-2; these are units modulo3^r. Across
cohorts the original labels are independent. Consequently

```
E sum_sigma p_sigma^2 = 1/N + (1-1/N)/D.
E [N sum_sigma(p_sigma-1/N)^2] = (N-1)/D.
```

Write F=sum_sigma sqrt(p_sigma/N), so P_ideal=F^2. Since
(sqrt(p)-sqrt(1/N))^2 <= N*(p-1/N)^2 and1-F^2<=2(1-F),

```
E P_ideal >= max(0,1-(N-1)/D).
E P_actual_complete >= max(0,1-min(1,(N-1)/D)-noise_loss_upper).
```

This is an UNCONDITIONAL expectation over the original dataset and complete
receiver, not a per-dataset guarantee or an assumption of exact balance.
The noise bound allows original errors to depend on labels; its true marginal
moment premise must hold under the same population. Labels must be IID
uniform for each fixed secret; neither that law nor the marginal moments is
established by finite controls. All failure branches remain charged.
For q=3^n,M=n^2+24,B=1, the coverage loss is at most3^(-24), and the stated
moment profile gives noise lossO(n^(-2)). This makes a clean normalized-fibre
receiver a meaningful conditional target, NOT an efficiently constructed
algorithm. Runtime/access, rather than ideal statistical information, is
the decisive unresolved obligation in this regime.

The square-root ledger is rationally enclosed, not computed using floating
point. Finite matrices/receiver laws are diagnostic floating controls with
explicit residual tolerances, not exact certificates of scalable circuits.

## Why This Could Matter, And Why It Probably Fails

The high-root phase/noise regime need not by itself destroy a truly efficient
normalized-row receiver. The bottleneck is now explicit: coherent fibre
preparation/erasure at actual original-data cost, rather than the easy
forward label evaluator. That primitive may be as hard as the original
problem. Granting it without a gate construction only renames the problem.
An efficient classical target-word helper also triggers the preceding
original-data classical reduction, not a uniquely quantum contribution.

Falsifiers: dropping the pointer is counted as Q; noise leakage is normalized
away; random-label coverage is inferred from deterministic controls; replacing
sqrt(p) by1 is called cost-free conditioning; or dense reference matrices
are presented as a scalable circuit. Conversely, a concrete structured
clean-row implementation with polynomial cost would falsify this current
missing-primitive diagnosis and deserves priority review.

Known background: [Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044)
connect dihedral optimal measurement implementation to subset-sum solution
sampling. The present native/noisy specialization is a local derivation;
that paper is not a theorem about this source or its error law.

Run `python theorems/native_word_frame_access.py --write` and its tests.
