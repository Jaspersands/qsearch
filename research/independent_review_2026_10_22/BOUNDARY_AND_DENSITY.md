# Consequences of the exact native-success identity

Status: proved deductions in this review. These refine the sufficient
quantum theorem; they are not classical hardness or novelty claims.

## The rate-1/4 boundary is included

Keep the same inverse-trace relation, but take K=floor(N/4), N=n², and
w=floor(N/2). Put a=N-w, h=K-1 and g=a²-Nh. For N>=8, h>0 and

    g >= N > 0,
    L <= N*(a-h)/g = O(N).

Thus the complete GS decoder exists strictly inside its finite Johnson
condition, despite the limiting rate being 1/4. The multiplicity choice
s=floor(Nh/g)+1 is O(N); its interpolation and complete root-list work
are polynomial in N,n, although substantially larger than at fixed slack.
Choose the fixed padded list length P as in QUANTUM_AUDIT.md; P=O(N).

For the balanced source, tau=Pr[Bin(N,1/2)<=floor(N/2)]>=1/2. The inverse-
trace fiber-count bound gives lambda_b=1-o(1), uniformly over every target
and every permitted set of distinct public points. For example the crude
bound (q^K-1)*beta^(N-K+1), beta=O(q^-1/2), already tends to zero here:
its leading exponent in log_q is K-(N-K+1)/2=-N/8+O(1).

The exact formula from EXACT_PATTERN_CHANNEL.md therefore yields

    Pr[native-valid and heralded] = lambda_b*tau²/P = Omega(1/N).

Verification and polynomially many restarts give a bounded-error quantum
solver, and conditional outputs remain uniform native witnesses. The tail
delta is approximately 1/2, so the negligible-tail hypotheses of the
Horinaga–Yamakawa theorem are not established at this boundary by this
choice. The direct full-list calculation establishes it instead.

Self-attack: constant list size or negligible truncation cannot be claimed
here. Both would be false. The accepted conclusion pays a growing list and
inverse-polynomial success. This extends a mathematical sufficient regime,
not the practical promise of the audited native rate 1/8. Jo's related OPI
results also reach a limiting 3/4 primal rate; no priority claim is made.

## Exact accepted amplitude for nonbalanced root sets

Let arbitrary nonempty sets S_i have densities p_i=|S_i|/q. Prepare their
normalized product root state R. Let Q_i,0 be the Fourier zero projector
and Q_i,1 its complement. At every accepted x_i in S_i,

    (F^-1 Q_i,0 F R_i)(x_i) = p_i R_i(x_i),
    (F^-1 Q_i,1 F R_i)(x_i) = (1-p_i) R_i(x_i).

For a support-only mask m, tensoring and summing gives, on every point of
the product root set,

    (F^-1 m F R)(x) = tau_m R(x),
    tau_m = E[m(sigma)],  sigma_i independent Bernoulli(1-p_i).

After code coalescence and a fixed-P complete-list projection, define

    lambda = |D| * |C intersect product_i S_i| / product_i |S_i|.

Then the unconditional native success is EXACTLY

    lambda * |tau_m|²/P.

For a Boolean Hamming-ball mask, tau_m is also its ordinary source mass.
Conditional native outputs are uniform. This proof needs no assumption
about the amplitudes on rejected root patterns. It applies to any nonempty
S_i, including p_i=1, provided preparation, the mask and the complete list
operation are actually implementable at the charged cost. It does not
turn an arbitrary membership oracle into a free uniform-root preparer.

Self-attack: label-dependent masks invalidate the pointwise factorization.
Different normalization for different decoder lists also invalidates the
single 1/P factor. These are explicit falsifiers, not suppressed technical
conditions. The balanced local basis is already part of DQI; the formula
is an independently derived corollary, not a new algorithmic primitive.
