# Joint Parity-Block Decoding Has A Matched Classical Sampler

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. This implements an actual
constant-size collective quantum decoder and a scalable classical sampler
for a structured signed-XOR Ising family. It is not an LWE decoder or a
quantum advantage claim. The negative result concerns this proposed route,
not DQI, quantum decoding or collective measurement in general.

## Literature Prompt And Research Decision

[Zhou et al., Section3.2 and AppendixB](https://arxiv.org/html/2609.40345v1)
connect DQI Gibbs sampling to quantum decoding, while a classical Prange
method matches their product-USD threshold. Their general mechanism suggests
trying collective local decoding. The family and block calculation BELOW
are our local extension; their random-hypergraph or stable-sampler theorems
are not imported for this different ensemble. No novelty is asserted.

The proposed triple measurement DOES improve on independent USD followed
by local parity repair. However, eliminating the Hamiltonian's block spin
gives a correlated classical sampler with exactly the same erasure/rank
condition. Comparing only against independent-clause Prange would be a false
advantage signal. The improvement remains a useful reusable coherent decoder.

## An Explicit Four-Qubit Program

Let the known overlap be0<c<1 and p0=(1+c)/2, p1=(1-c)/2. The Fourier-frame
binary pure-state channel is

    |phi_d>=sqrt(p0)|0>+(-1)^d sqrt(p1)|1>.

This is the Hadamard frame of the bit-flip-amplitude channel, with
c=2*sqrt(gamma*(1-gamma)). A parity-constrained triple has codeword
d=(u,v,u+v) overF2, and input tensor_i |phi_(d_i)>. Its four states have
unit diagonal Gram and common off-diagonal overlap c^2.

On basis frequencies(x1,x2,x3), compute quotient
(v1,v2,t)=(x1+x3,x2+x3,x3) with two CNOTs. At each quotient v, apply the
explicit one-qubit rotation sending the positive conditional t-vector to|0>.
Both squared rotation entries are recorded as rational mass ratios; no
fiber-count oracle or unknown codeword appears. There are only FOUR cases:

    q00=p0^3+p1^3=(1+3c^2)/4,
    q01=q10=q11=p0*p1=(1-c^2)/4=:qmin.

Use one herald qubit with success amplitude sqrt(qmin/q_v), then two
Hadamards on the quotient ONLY on success. The resulting vector is exactly

    sqrt(1-c^2)|u,v>|0_t>|success>
          +c|0,0>|0_t>|erasure>.                           (1)

The failure vector is codeword-INDEPENDENT, not dirty logical information.
Its nonzero amplitude comes only from v00, where q00-qmin=c^2. Every relative
sign and scratch register is retained. The producer executes the actual
16-dimensional gate program for all four codewords, checks unitarity, and
records exact rational gate ingredients and Gram identities separately from
floating numerical conformance. Universal gate synthesis/error budgeting is
not implemented. This is a constant-size circuit, not a dense global decoder.

For EACH classical codeword input, joint erasure is c^2. Independent USD erases each symbol with probability c;
parity repair succeeds only with at most one erasure, giving
1-3c^2+2c^3, strictly below the joint success1-c^2.

## Global Structured Code And Real Hamiltonian

Take B blocks, h outer bits x, and one inner spin z_i per block. Each block
has three independent public binary label vectors a_i1,a_i2,a_i3 inF2^h
and random sign bits j_i1,j_i2,j_i3. Define

    g_ik(x)=(-1)^(a_ik.x+j_ik),
    H(x,z)=-sum_(i,k) (-1)^(z_i)*g_ik(x),
    c=tanh(beta).

These are ordinary fully specified Ising/XOR constraints, not a new oracle
problem. The corresponding decoding code has local parity d_i3=d_i1+d_i2
and h outer parity constraints. In logical coordinates its two columns per
block are a_i1+a_i3 and a_i2+a_i3. They are IID uniform h-bit columns under
the stated random-label ensemble. A joint-erased block introduces two unknown
logical bits. The erasure pattern consists of independent blocks with
probability c^2 FOR A CODEWORD INPUT; recovery by Gaussian elimination succeeds whenever those
2|S| columns have full rank. This criterion does not depend on the codeword.

Coherent global decoding needs reversible elimination and inverse-computation
with its failures/precision charged; the local program alone is not that full
hardware compiler. Equation(1) identifies the erasure mechanism constructively,
without granting a decoder for general syndromes. The rank reconstruction is
an ordinary polynomial GF2 system, not SIS, CVP or a high-alphabet fiber.

This is not an input-independent Bernoulli law for arbitrary coherent code
superpositions. Normalize the SUM of all four nonorthogonal local inputs.
Its squared norm before normalization is4*(1+3*c^2); equation(1) gives
erasure probability4*c^2/(1+3*c^2), which is4/7 at c1/2, not1/4.
The actual gate program checks this counterexample. A quantum Gibbs reduction
must specify its input amplitudes and prove its own success/normalization
bound; it cannot substitute the classical-codeword erasure law. This artifact
does NOT execute or prove a complete coherent global Gibbs sampler.

## The Classical Attack That Kills The Apparent Advantage

Use exact rational Gibbs weights prod_(i,k)[1+c*(-1)^z_i*g_ik(x)]; their
omitted cosh(beta) factors cancel globally. Sum over z_i. The block weight is

    2*(1-c^2)+8*c^2*I[g_i1=g_i2=g_i3]
      =2*(1-c^2)*[1+lambda*I], lambda=4*c^2/(1-c^2).         (2)

The indicator enforces TWO linear equations
(a_i1+a_i3).x=j_i1+j_i3 and
(a_i2+a_i3).x=j_i2+j_i3. Thus retain whole blocks with probability

    theta=lambda/(4+lambda)=c^2,                            (3)

solve those affine equations, sample ALL free coordinates uniformly, then
sample each inner spin from its exact conditional probability. Reject rank-
deficient selected systems by a declared fallback; never condition them away.
The implementation uses FLINT GF2 RREF and exact rational random choices.
It runs polynomially without enumerating spins or selected subsets.

For comparison, independent-clause Prange introduces mean effective outer
constraint load B*(3c^2-c^3). The joint decoder and CORRELATED classical
block method both have mean load2B*c^2. At c1/2 and h/B11/20, the latter
clear the asymptotic rank threshold while independent-clause Prange does not.
This demonstrates why that weaker baseline would produce a false lead.

## Finite Normalization And Failure Bound

Let nu(S) be the independent block proposal, Z_S its solution count and

    T_S=2^(2|S|-h)*Z_S, Ztilde=E_nu[T_S].

The EXACT Gibbs subset law is nu(S)*T_S/Ztilde, not nu(S). Full rank implies
T_S=1. Otherwise T_S is0 for inconsistency or2^(2|S|-rank). These tilts can
be large: small observed failure alone does not justify a FIXED-instance
Gibbs claim. Complete bounded controls calculate the tilt and both full laws.
Their output-TV inequality is

    TV(sampler,Gibbs)<=TV(nu,nu*T/Ztilde)+nu(rank failure).   (4)

For RANDOM independent clause signs, the two sign differences per block are
IID uniform, so E_signs[T_S]=1 for every fixed label matrix and S. If
epsilon=Pr_(S~nu)[rank failure], then
E_signs E_nu[(1-T_S)_+]<=epsilon, and
E_signs[(Ztilde-1)_+]=E_signs[(1-Ztilde)_+]<=epsilon.
Pointwise TV(nu,nu*T/Ztilde) is at most
E_nu[(1-T)_+]+(Ztilde-1)_+: for Ztilde<=1 division only increases T;
for Ztilde>=1 expand1-T/Ztilde and bound its positive part.
Therefore the COMPLETE sampler obeys

    E_signs TV(sampler,Gibbs)<=min(1,3*epsilon).             (5)

This is an averaged-sign guarantee, not an arbitrary fixed-sign theorem.
For random labels, a selected2s-by-h matrix has rank-failure probability
at most(2^(2s)-1)/2^h. At any committed cutoff s0,

    E_labels epsilon <=Pr[Bin(B,c^2)>s0]+(2^(2s0)-1)/2^h,   (6)

capped at1. The report uses an exact binomial tail and a public cutoff;
neither asymptotic fits nor floating thresholds accept a regime. If
h/B>2c^2 with constant slack, a cutoff with constant slack on both sides
makes both terms exponentially small. The live cutoff instead leaves an
explicit logarithmic rank margin and preserves its finite numerical losses.

## Planted Signs Falsify The Unqualified Classical Guarantee

Set ALL sign bits to zero and keep random independent label vectors. The
outer block factor, normalized to have unit mean for nonzero x, is

    f_i(x)=1+c^2*sum_(three pairs) g_ik(x)*g_il(x).

It has f_i(0)=1+3*c^2, while E_labels f_i(x)=1 for every nonzero x.
For A0=(1+3*c^2)^B and Y=sum_(x!=0) prod_i f_i(x)/A0,
Gibbs P(x=0)=1/(1+Y). Consequently

    E_labels[1-P(x=0)]<=E Y=(2^h-1)/A0<=1/R,
    R=(1+3*c^2)^B/2^h.                                    (7)

An ACTUAL alternative classical sampler fixes x=0 and samples every inner
spin from its exact conditional law. Its mean output-TV is at most min(1,1/R).
It rejects nonzero-sign instances instead of pretending to be general.

For block-Prange, if |S|<=s0 and the system has full row rank, its outer-zero
atom is2^(2|S|-h). Failures use the declared zero fallback. Thus

    E_labels P_Prange(x=0)
       <=Pr[Bin(B,c^2)>s0]+(2^(2s0)-1)/2^h+2^(2s0-h),
    E_labels TV(P_Prange,Gibbs)
       >=max(0,1-1/R-[the preceding upper bound]).          (8)

At the same asymptotic rank-feasible threshold, R can grow exponentially.
Block-Prange then fails badly on these planted signs although its averaged-
random-sign bound is small. The DIFFERENT zero-outer classical sampler
succeeds. This kills an arbitrary-fixed-sign interpretation of equation(5),
not classical sampling generally, and certainly not a quantum advantage.

## Scope And Next Research Decision

Three complete sign censuses test192 actual fixed signed instances, including
rank defects and frustration. Four scaling bounds reach B4096. Thirty-two
live classical samples use a public24-block instance without enumeration.
Local numerical controls are gate conformance, not global Gibbs executions.

The negative result is the matched algorithm and threshold, not a lower bound
against every quantum method. Non-parity inner codes, overlapping blocks,
nonclassical decoders or a signed block factor without a positive hard-
constraint mixture could escape this exact argument. Merely increasing block
size or reporting better USD than a product decoder is insufficient.

NEXT: investigate collective decoders whose corresponding eliminated
Hamiltonian factor does NOT admit an efficient positive affine-constraint
mixture. Any proposed separation must still confront list recovery,
information-set decoding, algebraic elimination and true partition weights.
Do not claim that random-hypergraph stable-algorithm barriers prove advantage
for this block ensemble. Gemini owns CLI/central registry/hardware wiring.
