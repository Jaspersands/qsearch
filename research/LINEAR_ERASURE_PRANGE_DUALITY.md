# Affine Erasure Instruments Have Matched Classical Samplers

LOCAL DERIVATION / EXTERNAL REVIEW AND NOVELTY CHECK PENDING.
This is a mechanism-level dequantization audit, not a new quantum speedup,
a general measurement no-go theorem, or a state-only hidden-shift decoder.
It implements an actual constant-size partial quantum decoder and a scalable
classical sampler. The classical problem is fully specified Gibbs sampling,
with public affine maps and factors; no oracle problem is manufactured.

The literature prompt is [Zhou et al.](https://arxiv.org/html/2609.40345v1),
Section3.2 and AppendixB: their product-USD decoder has a classical Prange
counterpart. The general affine-mixture correspondence below is a local
derivation, not a theorem imported from that paper. Random-hypergraph
shattering and stable-algorithm results do NOT transfer to this ensemble.

## A Precise Instrument Contract

Work over F2^k. A canonical pure-state channel has

    |psi_d> = sum_y sqrt(q_y)*(-1)^(d.y)|y>, q_y>0.

Suppose its KNOWN distribution has an explicit normalized positive mixture
of uniform AFFINE subspaces a_l+V_l with independent direction bases B_l:

    q_y = sum_l w_l*1[y in a_l+V_l]/|V_l|,
    w_l>=0, sum_l w_l=1, r_l=dim(V_l).                     (1)

A known branch-splitting isometry on a basis frequency y is

    |y> -> sum_(l:y in a_l+V_l) sqrt(w_l/(|V_l|*q_y))|y,l>.

Its column norm is1 by equation(1); its columns are orthogonal because y is
retained. Within branch l, reversibly express y=a_l+B_l*t, clear the complement
coordinates, then apply H on its r_l coordinate bits. Thus

    |psi_d> -> sum_l sqrt(w_l)*(-1)^(d.a_l)
                         |B_l^T*d,l>|0_complement>.       (2)

For a SINGLE CODEWORD d, branch probability is w_l, the r_l reported linear
bits are exact, and k-r_l bits remain unknown. This does NOT grant a global
decoder. It does NOT imply this branch law for an arbitrary normalized
coherent sum of codewords. The producer executes the actual local isometry,
preserves all branch amplitudes, and checks that counterexample separately.

Equation(2) preserves inner products exactly: its output Gram entry is
sum_l w_l*(-1)^((d-e).a_l)*1[B_l^T(d-e)=0], equal to the Walsh transform
of equation(1). Affine branch phases must NOT be discarded. Once a GLOBAL
codeword has actually been recovered, the known phase can be corrected by
computing d.a_l. Before recovery it is unknown phase information.
The constant-size conformance uses square roots numerically, but mixture,
Gram and optimization identities are replayed with exact rational arithmetic.
There is no dense global unitary or exponential global-state simulation.
Universal gate compilation and physical approximation errors remain open.

## An Explicit Four-Message Partial Decoder

Take four binary pure-state channels with known overlap 0<c<1 and constrain
their bits to even parity: d4=d1+d2+d3. Put p0=(1+c)/2, p1=(1-c)/2.
The public quotient transform y_i=x_i+x4, t=x4 is followed by a controlled
one-qubit rotation clearing t. Its eight cases have exact masses

    q_y=p0^(4-w)*p1^w + p0^w*p1^(4-w), w=HammingWeight(y),
    q0=(1+6*c^2+c^4)/8,
    q_y=(1-c^4)/8                    for w1 or3,
    q_y=(1-c^2)^2/8                  for w2.              (3)

Equation(1) now has only SIX branches:

    V=F2^3:       weight (1-c^2)^2,       reveal3 bits;
    V=span(v):    weight (c^2-c^4)/2 EACH,
                  v in{001,010,100,111}, reveal1 bit;
    V={0}:        weight c^4,             reveal0 bits.   (4)

For each codeword the four one-bit branches reveal one of the physical
channel bits. The actual instrument has a16-dimensional input and a
96-dimensional output, including the clean parity scratch. It is an
isometry, not a postselected table labeled as a quantum algorithm.

Mean unresolved logical bits:

    partial collective instrument: 4*c^2-c^4;
    independent USD + parity:      6*c^2-4*c^3+c^4;
    full-block USD or total erase: 6*c^2-3*c^4.            (5)

Both improvements are strict in the stated interval. At c1/2 the loads are
15/16,17/16,21/16. Partial outcomes matter: simply increasing block size and
keeping only complete decoding would discard useful information.

For a normalized SUM of all eight nonorthogonal inputs, the branch law is
instead w_l/(|V_l|*q0). This follows because that sum is proportional to the
zero-frequency vector. The executable instrument checks this law, not just
a classical-codeword Monte Carlo approximation. No global quantum Gibbs
success claim is inferred from equation(5).

## Exact Optimality In The Stated Cone

Could a different positive subspace decomposition improve equation(5)?
Let z0=3, z_y=1 for odd Hamming weight, and z_y=-7/3 for weight2. For ALL
51 affine subspaces a+V of F2^3 (including all16 origin-linear spaces),

    average_(y in a+V) z_y <= 3-dim(V).                  (6)

The exact certificate enumerates all51 spaces, not just the chosen six.
For any positive affine-subspace decomposition of q, multiply each inequality
by its branch weight and sum:

    mean unresolved bits >= sum_y q_y*z_y =4*c^2-c^4.

The constructed six-branch instrument attains equality. This proves optimal
mean unresolved dimension WITHIN THIS CONE for every0<c<1, not optimal
quantum decoding, accessible information, minimum-error measurement or
performance under a nonuniform coherent prior. No floating LP value accepts
the optimality claim; the fixed dual works at all parameter values.

## The Matched Classical Algorithm

For B blocks with public maps y_i(x)=A_i*x+b_i, define the positive outer
Gibbs weight

    G(x)=prod_i f_i(y_i(x)), f_i(y)=2^k*q_y,
    f_i(y)=sum_l w_l*2^(k-r_l)*1[y in a_l+V_l].           (7)

For the four-message channel, equation(7) is exactly the factor obtained
by summing a block spin z_i in prod_(j=1..4)(1+c*(-1)^z_i*g_ij(x)) and
dividing by2. Relative labels and signs are A_ij=a_ij+a_i4 and
b_ij=j_ij+j_i4. Random independent original labels/signs give random
independent relative maps. Original clauses are not replaced by a secret
input oracle. Each eliminated spin can be sampled from its exact conditional
law if a joint outer/inner sample is wanted; the generic implementation
samples the precisely defined outer distribution.

Choose each branch independently with probability w_l. Its membership test
is U_l*(A_i*x+b_i+a_l)=0, where U_l is a basis of V_l's annihilator. This gives
EXACTLY k-r_l affine equations, equal to the unresolved quantum bits.
Combine these equations, test full row rank by GF2 elimination, and draw all
free coordinates uniformly. On rank failure, return a declared fallback;
never condition failure away. The implementation uses exact rational coins
and FLINT elimination, with polynomial cost in the public representation.

The equality of rank criteria is exact, not only equality of mean counts.
Form the quantum code C={d:sum_i A_i^T*d_i=0}. In a fixed branch, unresolved
differences are d_i in ker(B_li^T)=V_li^perp, with basis columns U_li^T.
The quantum reconstruction matrix is the concatenation of A_i^T*U_li^T;
the classical equation matrix stacks U_li*A_i. They are TRANSPOSES. Full
column rank for unique quantum reconstruction is exactly full row rank for
classical affine sampling. The actual coherent quantum prior still needs its
own normalization/success proof; this rank correspondence does not supply it.

This correspondence is NOT a classical simulator of quantum state-only
discrimination. The classical algorithm has the public factors and maps of
the Gibbs problem. It does not receive the unknown d of |psi_d> as classical
data. Comparing different access problems would be invalid.

## Normalization Is Essential

For selected branch vector l let D=sum_i(k-r_li), Z_l its affine solution
count, nu_l the branch proposal probability, and T_l=2^(D-h)*Z_l, where h is
the outer dimension. The EXACT Gibbs branch law is nu_l*T_l/E_nu T, not nu.
A positive full-space branch (or an exact small-channel support cover)
guarantees that this normalizer is nonzero for every signed instance. Growing
channels without a full-space branch need another scalable positivity proof.

Full row rank implies T_l=1. Defects can have T_l=0 or exponentially large
tilts. Complete fixed-instance controls retain those tilts and all fallbacks:

    TV(output,Gibbs)<=TV(nu,nu*T/E_nu T)+Pr_nu[rank bad].  (8)

For independent UNIFORM sign masks b_i, every branch's annihilator maps the
signs onto a uniform RHS, even if the selected LABEL equations are dependent.
Hence E_sign T_l=1. If epsilon=Pr_nu[rank bad], the positive-part argument
from PARITY_BLOCK_USD_PRANGE.md yields

    E_sign TV(output,Gibbs)<=min(1,3*epsilon).             (9)

It is not an arbitrary fixed-sign guarantee. The planted-sign counterexample
and its alternative zero-outer classical sampler remain relevant. A small
rank-failure probability by itself is not a fixed-instance Gibbs certificate.

For independent uniform public A_i, each selected U_l*A_i has independent
uniform rows since U_l has full row rank; this holds conditional on branches.
If D<=s0<h, rank failure is at most(2^s0-1)/2^h. For the four-message mixture,
D_i has masses(1-c^2)^2 at0,2*c^2*(1-c^2) at2, and c^4 at3. For any t>1,

    Pr[D>s0]<=min(1,[(1-c^2)^2+2*c^2*(1-c^2)*t^2+c^4*t^3]^B/t^(s0+1)).

All finite scaling certificates use rational t9/8 and retain the cutoff and
rank margin. At c1/2,h/B approximately21/20, the classical mean-TV bound
vanishes, although product-USD's mean load17/16 exceeds that outer rate.
A classical sampler therefore kills the apparent threshold improvement.
The corresponding QUANTUM global coherent-prior success is not supplied.

## Escape Conditions And Adversarial Limits

The cone is restrictive. Every origin-linear mixture obeys q0>=q_y and has
nonnegative Walsh coefficients. The positive distribution
q=(1/10,3/10,3/10,3/10) violates these conditions: q0-q1=-1/5 and all three
nonzero Walsh coefficients are-1/5. This excludes only the ORIGIN-linear cone.
It is NOT a hard problem or a quantum advantage. In fact it has an explicit
better AFFINE decomposition: full F2^2 has weight2/5, and the three lines
{1,2},{1,3},{2,3} each have weight1/5. It reveals both bits with probability
2/5 and one bit otherwise, for mean unresolved load3/5. The actual instrument
preserves its negative Gram entries through the affine phases in equation(2).
Dropping those phases would change the quantum channel.

The dual z=(-3,1,1,1) satisfies average_(a+V) z<=2-dim(V) on ALL11 affine
spaces of F2^2. Its q expectation is3/5, proving this affine instrument's
optimality within the cone. A matched public-matrix sampler has exact TV0 on
the supplied independent-column control. Negative overlaps and failure of an
origin-linear mixture are therefore NOT sufficient escape signatures.
An additional ALL16-sign census on a dependent public matrix retains affine
offsets, frustration, partition tilts and failures, and checks equation(9).

Every positive q has an affine POINT-MASS decomposition, but that leaves k
bits unknown per block and imposes k classical constraints. The relevant
question is efficient LOW-LOAD representation, not whether any affine mixture
exists. A representation of exponential size is not a scalable algorithm.

Other escape routes include noncommuting or minimum-error instruments,
overlapping factors with useful global dependence, and channels without an
efficient positive affine mixture at the claimed rate. None is automatically
advantageous. A genuinely useful target must provide:

- A complete coherent receiver and its actual input/normalization contract.
- A scalable, naturally specified computational problem and charged access.
- A stronger classical attack than product USD or independent-clause Prange.
- Proof that the proposed decoder does something not captured by this affine cone,
  rather than a claim based solely on improved local success.
- Partition-weight control and an asymptotic complexity argument.

NEXT: prioritize a receiver outside this exactly matched cone, or a concrete
classical attack on its proposed global advantage. Do not create a candidate
from the four-message local improvement or the outside-cone distribution.
Gemini owns production CLI, central-registry integration and routine wiring.
