# Native Prefix Schmidt Audit

LOCAL DERIVATION / REVIEW PENDING. Source-weighted fixed-cut MPS fidelity
bound, NOT a quantum hardness, general tensor-network, or novelty claim.

## Why This Matters

A final nuisance fiber can have few words while intermediate low-prefix
measurements create large entanglement. A multiscale decoder that explicitly
stores a low-bond matrix-product state must handle the intermediate states,
not merely the endpoint. This audit tests that particular representation.
The broader bounded-entanglement simulation setting is established in
[Vidal](https://arxiv.org/abs/quant-ph/0301063); the native population argument
below is locally derived and needs independent mathematical review.

## Exact Native Schmidt Weights

Use the original full-root native product phase state with M=nr-2 qutrits.
Split its word registers at a FIXED public position l, independent of labels.
Let L=3^l, R=3^(M-l), D=LR. Measure the summed frequency modulo3^d in every
coordinate; its group has size H=3^(nd). For left/right projected counts
c_L(z),c_R(z), the prefix outcome y has size

    C_y=sum_z c_L(z)*c_R(y-z), probability C_y/D.

Within each left/right syndrome class, the original unknown phase still
factors between the two sides. Different classes are orthogonal. Consequently
the squared Schmidt coefficients, for EVERY fixed full secret, are exactly

    lambda_(y,z)=c_L(z)*c_R(y-z)/C_y,
    purity P_y=sum_z lambda_(y,z)^2.

Empty branches have zero Born mass and no conditional normalized state.
The implementation retains EVERY branch, uses actual Born weights rather
than a uniform target average, and replays selected actual phase matrices
with dense SVD. The source secret enters only calibration, not a receiver.

## Full IID Population Bound

Set mu=D/H. Uniform native label differences between distinct words are
uniform on the prefix group. Thus for an independent uniform target,

    E[C_y]=mu, Var(C_y)=mu*(1-1/H).

The physical target law is the size-biased uniform-target law C_y/mu. On the
bad sector C_y<mu/2, Chebyshev and this size bias give mean Born mass at most
2*(1-1/H)/mu. This is a bound, not an algorithm that selects good fibers.

On the good sector, C_y>=mu/2, the Born-weighted purity is bounded by

    (2/(D*mu))*sum_y,z [c_L(z)*c_R(y-z)]^2.

The sum factors into (sum_z c_L(z)^2)*(sum_w c_R(w)^2). Native labels on
the two disjoint word halves are independent, so its mean is

    D*A, A=(1+(L-1)/H)*(1+(R-1)/H).

Since purity<=1 on the bad sector, the full source-weighted mean satisfies

    E_labels,Born[P_y] <= min(1, [2*(1-1/H)+2*A]/mu).

At a balanced middle scale L=R=H, this is less than10/H. Jensen gives mean
Renyi-2 entropy at least-log2 of that purity bound. Entropy floats in reports
are diagnostics; the exact rational purity bound is the proof-bearing record.

For a rank-chi approximation, its largest possible squared overlap with a
given pure state is the sum of its largest chi Schmidt weights. By
Cauchy-Schwarz it is at most sqrt(chi*P_y). Jensen then yields

    (E_labels,Born[best squared overlap])^2 <= chi*E_labels,Born[P_y].

More generally an algorithm may allocate different bond ranks chi_(labels,y)
to different outcomes. Cauchy-Schwarz on this SAME full source distribution
gives E[squared overlap]<=sqrt(E[chi]*E[P]). No independence between that
allocation and purity is needed. The recorded chi is therefore a MEAN bond
budget, not only a worst-case cap. The word partition itself remains fixed.

Thus achieving mean squared overlap>=9/10 requires
E[chi]>=(81/100)/purity_upper. A polynomial mean explicit bond budget cannot faithfully
represent these middle-scale states at growing roots. The live ledger
separates this source-average claim from finite prespecified controls.

## Scope And Ways This Could Fail To Matter

The PREFIX OUTCOME MARGINAL is exactly classically simulatable: sample a
uniform native word x and evaluate its public low-frequency sum. This gives
Pr(y)=C_y/D for every secret using polynomial arithmetic, with no phase oracle.
The implementation supplies this explicit-evaluator baseline and tests the
complete small-word law. It does not prepare the coherent conditioned state,
but demonstrates that the measured prefix statistics themselves carry ZERO
secret information. High entanglement is not automatically a useful signal.

- High Schmidt rank is not quantum hardness: many highly entangled states
  have short circuits or other compact symbolic descriptions.
- This does not bound all tensor-network geometries, adaptive label-selected
  partitions, operator/observable approximations, or algorithms that never
  construct these particular prefix-conditioned pure states.
- A decoder can jump directly to a high-prefix measurement without passing
  through the particular middle-conditioned states audited here. Small final
  rank still does not grant access to the unknown word basis or its amplitudes.
- A full-state fidelity obstruction does not prove that a trit observable
  needs faithful state simulation. Observable-specific compression remains open.
- The proof uses ALL IID original native rows and the true Born law. It does
  not transfer automatically to a sieve's retained or adversarial label law.
- Low-dimensional stabilizer/quadratic representations can handle large
  Schmidt rank. The full-root generic label structure must be analyzed, not
  dismissed using an MPS rank alone.
- Finite label cases are controls, not estimates of an asymptotic population.
  All source-count enumerations and dense SVD cells are explicitly charged.

## Workflow

`python theorems/ternary_prefix_schmidt.py --write` creates the exact prefix
branch records and large-root analytical certificates. The next research
question is an implicit carry/stabilizer or observable-specific transform
that can survive this intermediate entanglement without storing a full
explicit-bond state. No candidate promotion is authorized by this audit.
