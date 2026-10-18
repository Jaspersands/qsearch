# Retained Fibers: An All-Measurement Question, Not A Holevo Promise

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. This is a constructive reduction
of the next research question to weighted additive geometry, NOT a proved
native no-go, a decoder, a novel algorithm, or a hardness claim.

Run `python theorems/dcp_fiber_accessible_information.py --write`.

## Why This Is The Next Mathematical Question

The mod4 syndrome circuit retains a correlated block with a linear clean/noisy
Holevo lower bound in the established parameter regime. But Holevo is an upper
bound on accessible information, not a promise that an efficient, or even an
arbitrary single-block measurement obtains that many bits. The distinction is
not merely computational; [information locking](https://arxiv.org/abs/quant-ph/0303088)
provides general context. No locking theorem is imported for this source.

Before designing a receiver around the retained entropy, ask whether these
particular fibers admit ANY informative single-block POVM under the actual
uniform-secret prior. The random-X/Y audit covers only that readout; the lemma
below covers every finite POVM, subject to a new, explicitly unresolved
weighted fourth-moment bound.

## Exact All-POVM Lemma

Fix the FULL public source matrix A, q=2^t and a nonempty syndrome fiber
F={x in{0,1}^m:A*x=y mod4}, with D=|F|. Retain the original Boolean wires.
Assume the full map x->A*x modq is injective ON THIS fiber. For uniform
residual secret s in Z_Q^n, Q=q/4, the normalized clean states are

    |psi_s>=D^(-1/2) sum_(x in F) exp(2*pi*i*<A*x,s>/q)|x>.

The common residue y contributes only a global phase when identifying s modQ.
The average state is I_F/D by character orthogonality, so its clean Holevo
information is log2(D). For any complex coefficient vector c with sum|c_x|^2=1,
let

    f_c(s)=sum_(x in F) c_x exp(2*pi*i*<A*x,s>/q),
    K_F=sup_c E_s |f_c(s)|^4.

Then EVERY finite POVM on one such block has mutual information at most
log2(K_F). This also covers any secret-independent channel applied to the
clean block, including the original independent Z dephasing: any measurement
after that channel pulls back to a POVM on the clean state.

Proof: refine an arbitrary POVM into rank-one effects lambda_z|w_z><w_z|,
with ||w_z||=1. Refinement cannot decrease mutual information. The outcome
prior is p(z)=lambda_z/D. Its posterior likelihood ratio against the uniform
secret prior is L_z(s)=|f_(conjugate(w_z))(s)|^2, with E_s L_z=1. Jensen under
the posterior gives

    KL(p(s|z)||p(s)) = E_s L_z log2 L_z
                    <= log2 E_s L_z^2 <= log2 K_F.

Average over z. Zero-probability effects may be discarded. The proof uses no
fiber inverse, implementable PGM, state-preparation inverse or cost-free
likelihood oracle. It even allows expensive measurements for an UPPER bound.

IMPORTANT: this is a SINGLE-BLOCK, UNIFORM-PRIOR theorem. Conditioning on prior
records changes the secret prior. Do not multiply this bound through adaptive
packet histories or extend it to a joint POVM on many blocks without a new
argument. Side information can matter. It also says nothing by itself about
an algorithm using the original phase source WITHOUT this syndrome projection.

## Exactly What Must Be Bounded

Character orthogonality gives the exact quartic expression

    E_s |f_c(s)|^4
      = sum_g |sum_(x,z in F: A*(x+z)=g modq) c_x*c_z|^2.

If each unordered pair sum, INCLUDING repeated vertices, is distinct, F is
Sidon for this frequency map. Then the expression is
2- sum_x|c_x|^4 <=2-1/D. Every POVM obtains less than one bit even when the
clean Holevo information log2(D) grows. The uniform coefficients attain this
fourth-moment maximum in the Sidon case, not necessarily the information bound.

More generally, if R is the maximum ORDERED pair-sum multiplicity, Cauchy in
each bucket gives K_F<=R<=D. The code computes this exact safe upper bound.
It can be weak: a large matching of complementary vertices produces a large
bucket, but does not necessarily maximize the quartic form on rank-one
coefficients c tensor c. Thus R growing exponentially is NOT evidence of a
useful measurement or a refutation of a stronger weighted bound.

Likewise, a small fourth moment for UNIFORM coefficients is only one witness,
not a bound over all measurement vectors. The existing source-averaged counting
calculation cannot be promoted to an all-POVM theorem by changing its label.
This supremum, not additional unweighted counting, is the missing research task.

## Remove Accidental Full-Modulus Aliases Without An Oracle

For native IID uniform A in Z_(2^t)^(n x m), an unintended four-vertex equality
has A*c=0 modq for nonzero integer c in{-2,-1,0,1,2}^m. If any coefficient is
odd its probability is q^-n. Otherwise c=2d with a unit coefficient in d,
giving probability(2/q)^n. Union over all such coefficient vectors gives

    Pr[some noninteger-parallelogram alias]
       <= (5^m-3^m)/q^n + (3^m-1)*(2/q)^n.

This event is defined BEFORE choosing y and holds simultaneously for ALL
fibers. It also supplies the needed injectivity. At t=n+8:

- m=3n: failure <=2^(-n^2-n+1).
- m=4n: failure <=2^(-n^2+2n+1), meaningful in the stated n>=4 range.

On its complement, only INTEGER Boolean parallelograms x1+x2=x3+x4 remain.
The unresolved problem is therefore a weighted Lambda(4)-type inequality for
actual random mod4 fibers of the Boolean cube. Higher-label accidents are
not the main obstacle. Do not replace those fibers by independent random
subsets, ignore their correlations, or condition on favorable y for free.

## Controls That Can Falsify The Reasoning

Three complete finite POVM controls are compared with exact moment buckets:

- A=(1,5,13,29),q=64,y=1: four one-hot vertices, Sidon frequency sums,
  K_F=7/4 and ALL-POVM information<=log2(7/4), versus clean Holevo2 bits.
- A=(1,17,33,49),q=64,y=1: same fiber size but modular aliases; K_F=4.
  This prevents using the Sidon formula just because frequencies are distinct.
- A=(4,8,16),q=32,y=0: known dyadic source, D=8, K_F=8, and the inverse
  index DFT obtains3 bits exactly. This refutes a universal constant bound
  for arbitrary supplied matrices. It is NOT a native high-probability source
  or a new algorithm; the structured dyadic source was already a control.

Three seeded native fragments retain original source labels and actual Born
syndromes, but remain explicitly finite/selected diagnostics. Dense POVM
tables are bounded simulations, not compiled gates or scalable decoders.
Tests replay complex coefficient moments, nonprojective frames, actual
conditional density operators with noise, degeneracies and native alias counts.

## Next Research Decision And Kill Criteria

Attempt a high-probability or Born-weighted bound on K_F for m=3n or4n,
using the real mod4 random linear constraint, not IID vertex thinning. A
constant bound would limit ANY one-block measurement to O(1) uniform-prior
bits; a poly(n) bound would give O(log n). Neither is currently proved.

Try to falsify that conjecture first: search for normalized coefficient
vectors concentrated on structured subfibers whose fourth moment grows.
A witness refutes a proposed upper bound but does NOT supply a POVM with
large mutual information. A positive receiver must also provide a complete
measurement, its full outcome law, gate/source cost and a decoder.

If one-block accessibility really is small, prioritize joint-packet
measurements, paid side information, or avoiding the syndrome projection.
If accessibility is large, find its coefficient/measurement structure rather
than assuming generic local rotations or a free fiber inverse can access it.
